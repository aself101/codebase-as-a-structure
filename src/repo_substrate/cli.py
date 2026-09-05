"""CLI (repo-substrate-spec §8):

substrate extract <repo> [--rev HEAD] [--truncate-at <sha>] [--config cfg.toml]
                  -o substrate.json [--report substrate-report.md] [--no-deps]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .assemble import ExtractOptions, extract
from .config import SubstrateConfig
from .deps import DependencyCruiserExtractor
from .report import render_report

TOOLS_DIR = Path(__file__).resolve().parents[2]  # project root holds package.json / node_modules


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="substrate")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ex = sub.add_parser(
        "extract", help="emit substrate.json (+ report) for one repo at one revision"
    )
    ex.add_argument("repo", type=Path)
    ex.add_argument("--rev", default="HEAD")
    ex.add_argument(
        "--truncate-at", default=None, help="drop all commits after this SHA (validation split)"
    )
    ex.add_argument("--config", type=Path, default=None)
    ex.add_argument("-o", "--output", type=Path, required=True)
    ex.add_argument("--report", type=Path, default=None)
    ex.add_argument(
        "--no-deps", action="store_true", help="skip the dependency extractor (graph absent)"
    )
    ex.add_argument(
        "--scratch", type=Path, default=None, help="directory for the temporary worktree"
    )
    ex.add_argument("--blame-workers", type=int, default=8)
    mp = sub.add_parser(
        "map", help="C3: apply a ruleset under the anti-horoscope gate → skeleton.json"
    )
    mp.add_argument("substrate", type=Path)
    mp.add_argument("--validation", type=Path, required=True)
    mp.add_argument("--ruleset", type=Path, required=True)
    mp.add_argument("-o", "--output", type=Path, required=True)
    rd = sub.add_parser(
        "render", help="C6: deterministic 2D cutaway SVG from skeleton.json + substrate.json"
    )
    rd.add_argument("skeleton", type=Path)
    rd.add_argument("substrate", type=Path)
    rd.add_argument("-o", "--output", type=Path, required=True)
    args = ap.parse_args(argv)

    if args.cmd == "map":
        from .mapper import load_ruleset, map_skeleton

        sub_doc = json.loads(args.substrate.read_text(encoding="utf-8"))
        val_doc = json.loads(args.validation.read_text(encoding="utf-8"))
        rs = load_ruleset(args.ruleset)
        skel = map_skeleton(sub_doc, val_doc, rs)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(skel, indent=1, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        sm = skel["summary"]
        print(
            f"{skel['repo']['name']}: diagnostic={sm['diagnostic_count']} decorative={sm['decorative_count']} "
            f"degraded={sm['degraded_count']} counts={sm['feature_counts']}",
            file=sys.stderr,
        )
        return 0
    if args.cmd == "render":
        from .cutaway import render_cutaway

        skel = json.loads(args.skeleton.read_text(encoding="utf-8"))
        sub_doc = json.loads(args.substrate.read_text(encoding="utf-8"))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(render_cutaway(skel, sub_doc), encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
        return 0

    cfg = SubstrateConfig.load(args.config)
    extractor = (
        None
        if args.no_deps
        else DependencyCruiserExtractor(TOOLS_DIR, cfg.dep_ts_pre_compilation_deps)
    )
    opts = ExtractOptions(
        rev=args.rev,
        truncate_at=args.truncate_at,
        scratch_dir=args.scratch,
        blame_workers=args.blame_workers,
    )
    result = extract(args.repo, cfg, opts, extractor)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=1, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(render_report(result, cfg), encoding="utf-8")
    s = result["summary"]
    print(
        f"{result['repo']['name']}@{result['repo']['head_sha'][:10]}: nodes={s['node_count']} "
        f"population={s['population_size']} edges={len(result['edges'])} "
        f"resolution={s['graph_resolution_rate']} degraded={s['graph_degraded']} "
        f"orphans={s['orphan_nodes']} commits={s['commit_count']}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
