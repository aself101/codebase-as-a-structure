"""CLI (validation-spec §7):

substrate-validate run --repo <path> [--repo <path> ...] --out <dir>
    [--config cfg.toml] [--vconfig v.toml] [--blind-dir blind/] [--cache out/cache] [--no-deps]
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from ..cli import TOOLS_DIR
from ..config import SubstrateConfig
from ..deps import DependencyCruiserExtractor
from .asserted import run_asserted
from .config import EXPECTED_TEST_REPOS, EXPECTED_TUNING_REPOS, ValidationConfig
from .gate import build_validation
from .holdout import run_holdout
from .report import render_holdout_report
from .substrates import SubstrateCache


def _expected_role(name: str) -> str | None:
    if name in EXPECTED_TEST_REPOS:
        return "test"
    if name in EXPECTED_TUNING_REPOS:
        return "tuning"
    return None


def _blind_seal(path: Path) -> dict[str, str | None]:
    """The sealed ranking's git identity (circumvention A10): blob sha as committed and the
    timestamp of the commit that added it. A file changed since its commit shows a
    different working-tree hash; a file never committed shows no commit."""
    import subprocess

    def git(*args: str) -> str:
        p = subprocess.run(["git", *args], capture_output=True, text=True, check=False, timeout=60)
        return p.stdout.strip() if p.returncode == 0 else ""

    return {
        "path": str(path),
        "worktree_blob": git("hash-object", str(path)) or None,
        "committed_blob": git("rev-parse", f"HEAD:{path.as_posix()}") or None,
        "first_commit": git("log", "--diff-filter=A", "--format=%H", "--", str(path)).splitlines()[
            -1:
        ]
        and git("log", "--diff-filter=A", "--format=%H", "--", str(path)).splitlines()[-1]
        or None,
        "first_commit_time": git(
            "log", "--diff-filter=A", "--format=%cI", "--", str(path)
        ).splitlines()[-1:]
        and git("log", "--diff-filter=A", "--format=%cI", "--", str(path)).splitlines()[-1]
        or None,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="substrate-validate")
    sub = ap.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run")
    run.add_argument(
        "--repo",
        "--test-repo",
        dest="test_repos",
        type=Path,
        action="append",
        default=[],
        help="TEST-role repo (D-009): only these can confer `validated`",
    )
    run.add_argument(
        "--tuning-repo",
        dest="tuning_repos",
        type=Path,
        action="append",
        default=[],
        help="TUNING-role repo: scored and reported in-sample, never counted toward the verdict",
    )
    run.add_argument(
        "--tuned-config-commit",
        default=None,
        help="commit hash that froze config/tuned.toml (D-009); auto-detected from git when omitted",
    )
    run.add_argument("--out", type=Path, required=True)
    run.add_argument("--config", type=Path, default=None)
    run.add_argument("--vconfig", type=Path, default=None)
    run.add_argument("--blind-dir", type=Path, default=Path("blind"))
    run.add_argument("--cache", type=Path, default=Path("out/cache"))
    run.add_argument("--scratch", type=Path, default=None)
    run.add_argument("--no-deps", action="store_true")
    run.add_argument("--blame-workers", type=int, default=8)
    tn = sub.add_parser(
        "tune", help="pre-registered weight tuning on the tuning repos only (D-009)"
    )
    tn.add_argument("--repo", type=Path, action="append", required=True, help="tuning repos ONLY")
    tn.add_argument(
        "--out", type=Path, required=True, help="directory for tuning.json + tuned.toml"
    )
    tn.add_argument("--config", type=Path, default=None)
    tn.add_argument("--vconfig", type=Path, default=None)
    tn.add_argument("--cache", type=Path, default=Path("out/cache"))
    tn.add_argument("--scratch", type=Path, default=None)
    tn.add_argument("--no-deps", action="store_true")
    tn.add_argument("--blame-workers", type=int, default=8)
    args = ap.parse_args(argv)

    cfg = SubstrateConfig.load(args.config)
    vcfg = ValidationConfig.load(args.vconfig)
    extractor = (
        None
        if args.no_deps
        else DependencyCruiserExtractor(TOOLS_DIR, cfg.dep_ts_pre_compilation_deps)
    )
    cache = SubstrateCache(args.cache, cfg, extractor, args.scratch, args.blame_workers)

    if args.cmd == "tune":
        from .tune import tune, write_tuned_toml

        result = tune([r.resolve() for r in args.repo], cache, vcfg, cfg)
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / "tuning.json").write_text(
            json.dumps(result, indent=1, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
        )
        write_tuned_toml(result, cfg, args.out / "tuned.toml")
        for name, r in result["indices"].items():
            print(
                f"{name}: chosen={r['chosen']} min_delta_roc={r['chosen_objective']['min_delta_roc']:+.3f} "
                f"min_pr_ratio={r['chosen_objective']['min_pr_ratio']:.2f}",
                file=sys.stderr,
            )
            for p in r["chosen_per_repo"]:
                print(
                    f"    {p['name']}: delta_roc={p['delta_roc']:+.3f} pr_ratio={p['pr_ratio']:.2f}",
                    file=sys.stderr,
                )
            print(
                f"  spec placeholder: {[(p['name'], round(p['delta_roc'], 3), round(p['pr_ratio'], 2)) for p in r['spec_placeholder_per_repo']]}",
                file=sys.stderr,
            )
        return 0

    holdouts, asserted, refs = [], [], []
    if not args.test_repos:
        ap.error(
            "at least one --repo/--test-repo is required (D-009: the verdict comes from test-role repos)"
        )
    repos = [(r, "test") for r in args.test_repos] + [(r, "tuning") for r in args.tuning_repos]
    tuned_commit = args.tuned_config_commit
    if tuned_commit is None and args.config is not None:
        import subprocess

        proc = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", str(args.config)],
            capture_output=True,
            text=True,
            check=False,
        )
        tuned_commit = proc.stdout.strip() or None
    for repo, role in repos:
        repo = repo.resolve()
        print(f"[{repo.name}] ({role}) holdout…", file=sys.stderr)
        h = run_holdout(repo, cache, vcfg)
        print(
            f"[{repo.name}] split={h.split_sha[:10]} eligible={h.n_eligible} positives={h.n_positives} "
            f"coverage={h.coverage:.2f} degenerate={h.degenerate}",
            file=sys.stderr,
        )
        print(f"[{repo.name}] asserted bar…", file=sys.stderr)
        blind = args.blind_dir / f"{repo.name}.md"
        a = run_asserted(repo, cache, vcfg, blind if blind.exists() else None)
        holdouts.append(h)
        asserted.append(a)
        refs.append(
            {
                "name": h.name,
                "head_sha": h.head_sha,
                "path": str(repo),
                "role": role,
                "expected_role": _expected_role(h.name),
                "holdout": {
                    k: v for k, v in asdict(h).items() if k not in ("baselines", "signals")
                },
                "asserted": {
                    "perturbed_sha": a.perturbed_sha,
                    "n_population": a.n_population,
                    "n_compared": a.n_compared,
                    "n_excluded_touched": a.n_excluded_touched,
                    "recognition_ref": a.recognition_ref,
                    "recognition_seal": _blind_seal(blind) if blind.exists() else None,
                },
            }
        )

    doc = build_validation(
        holdouts,
        asserted,
        vcfg,
        cache.fingerprint,
        refs,
        tuned_commit,
        cache.effective_config(),
        cache.attestations,
    )
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "validation.json").write_text(
        json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    (args.out / "holdout-report.md").write_text(render_holdout_report(doc), encoding="utf-8")
    for name, s in doc["signals"].items():
        print(f"  {name:28s} {s['status']:12s} {s.get('reason', '')}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
