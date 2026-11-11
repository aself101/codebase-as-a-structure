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


def _ruleset_versions(work: Path, repos: dict) -> str:
    for name in repos:
        for sk in sorted(work.glob(f"{SHORT.get(name, name)}.*.head.skeleton.json")):
            h = json.loads(sk.read_text())
            return ", ".join(
                [f"{h['ruleset']['name']} {h['ruleset']['version']}"]
                + [f"{o['ruleset']['name']} {o['ruleset']['version']}" for o in h.get("overlays", [])]
            )
    return "unknown"


def _series_break(m2: Path, short: str, g: str, d: dict) -> str:
    """D-082: the D-078 row and the row before it were two instruments printed as one series
    (186 common rooms, then 64). Compare this row with the most recent earlier table's diff
    for the same pair of commits and say so when the population differs."""
    pair = (d["before"]["repo"].get("head_sha"), d["after"]["repo"].get("head_sha"))
    for prev in sorted((p for p in m2.parent.glob("*-m2x") if p.name < m2.name), reverse=True):
        f = prev / f"{short}.{g}.diff.json"
        if not f.exists():
            continue
        o = json.loads(f.read_text())
        if (o["before"]["repo"].get("head_sha"), o["after"]["repo"].get("head_sha")) != pair:
            return f"new window (previous table {prev.name[:-4]} read other commits)"
        if o["common_nodes"] != d["common_nodes"]:
            return f"BREAK: common {o['common_nodes']} → {d['common_nodes']} against {prev.name[:-4]}"
        return f"continues {prev.name[:-4]}"
    return "first table"


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
                    "--before-substrate",
                    str(ROOT / "out" / "cache" / f"{name}-{pert}-trunc-{fp}.substrate.json"),
                    "-o",
                    str(d_out),
                ]
            )
            if r.returncode:
                print(r.stderr[-800:], file=sys.stderr)
                return r.returncode
            d = json.loads(d_out.read_text())
            u = d["untouched"]
            head = json.loads((work / f"{short}.{g}.head.skeleton.json").read_text())
            excluded = ", ".join(
                f"{k} {n}" for k, n in sorted(head["summary"].get("excluded_by_kind", {}).items()) if n
            ) or "none"
            ops = d["budget"]["operands"]
            fired = d["budget"]["fired"]
            rows.append(
                f"| {name} | {g} | {d['commits_between']} | {head['summary']['population']} | {excluded} | {d['common_nodes']} | {d['born']}/{d['deleted']} | {d['touched']['n']} | {u['n']} | "
                f"{d['feature_churn']:.3f} | {d['strata_moved_frac']:.3f} | "
                f"{ops['features']['changes']}/{ops['features']['denominator']} = {u['jitter_churn']:.3f} (over at {ops['features']['fires_at']}) | {u['clock_churn']:.3f} | "
                f"{ops['floors']['changes']}/{ops['floors']['denominator']} = {u['strata_moved_frac']:.3f} (over at {ops['floors']['fires_at']}) | "
                f"{d['budget']['verdict']}{' (' + ', '.join(fired) + ')' if fired else ''} | {_series_break(m2, short, g, d)} |"
            )
    (m2 / "skeleton-budget.md").write_text(
        f"# Skeleton-level stability budget — re-read under `{fp}` ({args.tag})\n\n"
        f"*Procedure of D-018 with the D-024/D-026 operand: before = the gate's stability-perturbation substrate (HEAD minus the last K = {k} timeline commits), after = HEAD; maintainability + onboarding; gate `{args.validation}`.*\n\n"
        f"*Reading a row (mapper spec §7 Q3, D-082): the verdict is a statement about one window — more than 5% of the rank and mixed assignments held by unedited rooms, or of the unedited rooms' floors, changed. \"over at n\" is the smallest count that exceeds the ceiling on that denominator. Rows are one series with another tag's table only where the gate, the ruleset versions ({_ruleset_versions(work, repos)}) and the rooms column all match; the last column marks a row whose population differs from the most recent earlier table for the same pair of commits.*\n\n"
        "| repo | geometry | K | rooms | excluded kinds | common | born/del | touched | untouched | churn (all) | strata (all) | jitter: assignments | clock churn | floors: untouched rooms | verdict (operand over) | series |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
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
    failed = False  # D-069: `--skip-briefs` reached the return with `failed` unbound
    if not args.skip_briefs:
        m3 = ROOT / "reports" / f"{args.tag}-m3x"
        m3.mkdir(parents=True, exist_ok=True)
        failed = False
        for name, (tip, _) in repos.items():
            short = SHORT.get(name, name)
            skel = work / f"{short}.age.head.skeleton.json"
            sub = ROOT / "out" / "cache" / f"{name}-{tip}-tip-{fp}.substrate.json"
            # D-083: the window page for the gate's pair, beside the brief that points at it
            wsheet = m3 / f"{short}.window.facts.json"
            wr = run(
                ["uv", "run", "substrate", "window",
                 *[str(m2 / f"{short}.{g}.diff.json") for g in geoms],
                 "--origin", "gate", "-o", str(m3 / f"{short}.window.md"), "--facts", str(wsheet)]
            )
            if wr.returncode:
                print(wr.stderr[-1200:], file=sys.stderr)
                failed = True
                continue
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
                    "--window",
                    str(wsheet),
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
