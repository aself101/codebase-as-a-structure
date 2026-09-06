"""Regenerate every downstream reading under a validation.json (D-029 chain, reusable).

    uv run python scripts/regenerate_readings.py --validation out/validation-m1c/validation.json --tag 2026-09-06 \
        [--skip-timelapse] [--skip-briefs] [--geometry age|layer|both]

Steps, each idempotent over the substrate cache:
  1. skeleton budget re-read (D-018 procedure): map the gate's HEAD and perturbation
     substrates, diff, write reports/<tag>-m2x/skeleton-budget.md
  2. time-lapses, twelve frames, per repo and geometry → out/timelapse-<tag>/ and the
     cross-repo reading reports/<tag>-phase1x/phase1-reading.md (via phase1_reports.py)
  3. architect briefs over the HEAD skeletons (age geometry) → reports/<tag>-m3x/
The reference repos and their tip/perturbation shas come from validation.json itself.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_PATHS = {
    "uluops-registry-api": Path.home() / "uluops" / "uluops-registry-api",
    "mcp-secure-server": Path.home() / "uluops" / "misc" / "npm-packages" / "mcp-secure-server",
    "eslint": ROOT / "reference" / "eslint",
    "typeorm": ROOT / "reference" / "typeorm",
}
SHORT = {"uluops-registry-api": "registry"}
RULESET = ["--ruleset", "rulesets/maintainability.toml", "--overlay", "rulesets/onboarding.toml"]


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    print("$", " ".join(cmd), flush=True)
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False, **kw)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--validation", type=Path, required=True)
    ap.add_argument(
        "--tag", required=True, help="date tag for the reports directories, e.g. 2026-09-06"
    )
    ap.add_argument("--config", type=Path, default=Path("config/tuned.toml"))
    ap.add_argument("--geometry", choices=["age", "layer", "both"], default="both")
    ap.add_argument("--frames", type=int, default=12)
    ap.add_argument("--skip-timelapse", action="store_true")
    ap.add_argument("--skip-briefs", action="store_true")
    ap.add_argument(
        "--relint-from",
        type=Path,
        help="directory of earlier briefs: relint each <short>.brief.md against the new skeleton instead of generating",
    )
    args = ap.parse_args()

    v = json.loads(args.validation.read_text(encoding="utf-8"))
    fp = v["substrate_config_fingerprint"][:12]
    repos = {
        r["name"]: (r["head_sha"][:12], r["asserted"]["perturbed_sha"][:12])
        for r in v["reference_repos"]
    }
    geoms = ["age", "layer"] if args.geometry == "both" else [args.geometry]
    vpath = str(args.validation)
    k = v["validation_config"]["stability_perturbation_k"]

    # 1. budget re-read
    m2 = ROOT / "reports" / f"{args.tag}-m2x"
    m2.mkdir(parents=True, exist_ok=True)
    work = ROOT / "out" / f"m2x-{args.tag}"
    work.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, (tip, pert) in repos.items():
        short = SHORT.get(name, name)
        for g in geoms:
            for sha, tag, mode in ((pert, "pert", "trunc"), (tip, "head", "tip")):
                sub = ROOT / "out" / "cache" / f"{name}-{sha}-{mode}-{fp}.substrate.json"
                if not sub.exists():
                    print(f"missing cache {sub.name}; run the gate first", file=sys.stderr)
                    return 2
                out = work / f"{short}.{g}.{tag}.skeleton.json"
                r = run(
                    [
                        "uv",
                        "run",
                        "substrate",
                        "map",
                        str(sub),
                        "--validation",
                        vpath,
                        *RULESET,
                        "--geometry",
                        g,
                        "-o",
                        str(out),
                    ]
                )
                if r.returncode:
                    print(r.stderr[-800:], file=sys.stderr)
                    return r.returncode
            d_out = m2 / f"{short}.{g}.diff.json"
            r = run(
                [
                    "uv",
                    "run",
                    "substrate",
                    "skeleton-diff",
                    str(work / f"{short}.{g}.pert.skeleton.json"),
                    str(work / f"{short}.{g}.head.skeleton.json"),
                    "--renames",
                    str(ROOT / "out" / "cache" / f"{name}-{tip}-tip-{fp}.substrate.json"),
                    "-o",
                    str(d_out),
                ]
            )
            if r.returncode:
                print(r.stderr[-800:], file=sys.stderr)
                return r.returncode
            d = json.loads(d_out.read_text())
            u = d["untouched"]
            rows.append(
                f"| {name} | {g} | {d['commits_between']} | {d['common_nodes']} | {d['born']}/{d['deleted']} | {d['touched']['n']} | "
                f"{d['feature_churn']:.3f} | {d['strata_moved_frac']:.3f} | {u['jitter_churn']:.3f} | {u['clock_churn']:.3f} | {u['strata_moved_frac']:.3f} | {d['budget']['verdict']} |"
            )
    (m2 / "skeleton-budget.md").write_text(
        f"# Skeleton-level stability budget — re-read under `{fp}` ({args.tag})\n\n"
        f"*Procedure of D-018 with the D-024/D-026 operand: before = the gate's stability-perturbation substrate (HEAD minus the last K = {k} timeline commits), after = HEAD; maintainability + onboarding; gate `{args.validation}`.*\n\n"
        "| repo | geometry | K | common | born/del | touched | churn (all) | strata (all) | jitter churn | clock churn | strata (untouched) | verdict |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n"
        + "\n".join(rows)
        + "\n",
        encoding="utf-8",
    )
    print(f"budget re-read → {m2}")

    # 2. time-lapses + reading
    if not args.skip_timelapse:
        tl_out = ROOT / "out" / f"timelapse-{args.tag}"
        for name in repos:
            short = SHORT.get(name, name)
            for g in geoms:
                r = run(
                    [
                        "uv",
                        "run",
                        "substrate",
                        "timelapse",
                        str(REPO_PATHS[name]),
                        "--validation",
                        vpath,
                        *RULESET,
                        "--geometry",
                        g,
                        "--frames",
                        str(args.frames),
                        "--config",
                        str(args.config),
                        "-o",
                        str(tl_out / f"{short}.{g}"),
                    ]
                )
                if r.returncode:
                    print(r.stderr[-800:], file=sys.stderr)
                    return r.returncode
                print(r.stderr.strip().splitlines()[-1][:160])
        env = {
            **os.environ,
            "PHASE1_SRC": str(tl_out),
            "PHASE1_DST": str(ROOT / "reports" / f"{args.tag}-phase1x"),
        }
        r = subprocess.run(
            ["uv", "run", "python", "scripts/phase1_reports.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        print(r.stdout.strip() or r.stderr[-400:])

    # 3. briefs
    if not args.skip_briefs:
        m3 = ROOT / "reports" / f"{args.tag}-m3x"
        m3.mkdir(parents=True, exist_ok=True)
        failed = False
        for name, (tip, _) in repos.items():
            short = SHORT.get(name, name)
            skel = work / f"{short}.age.head.skeleton.json"
            sub = ROOT / "out" / "cache" / f"{name}-{tip}-tip-{fp}.substrate.json"
            r = run(
                [
                    "uv",
                    "run",
                    "substrate",
                    "brief",
                    str(skel),
                    str(sub),
                    "-o",
                    str(m3 / f"{short}.brief.md"),
                    "--facts",
                    str(m3 / f"{short}.facts.json"),
                    "--max-attempts",
                    "3",
                    *(
                        ["--relint", str(args.relint_from / f"{short}.brief.md")]
                        if args.relint_from
                        else []
                    ),
                ]
            )
            if r.returncode:
                print(r.stderr[-1200:], file=sys.stderr)
                failed = True
            else:
                print((r.stderr.strip().splitlines() or [""])[0][:160])
    return 3 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
