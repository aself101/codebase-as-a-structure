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
from .brief import DEFAULT_MODEL
from .config import SubstrateConfig
from .deps import DependencyCruiserExtractor
from .gitutil import GitError
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
    mp.add_argument(
        "--overlay",
        type=Path,
        action="append",
        default=[],
        help="additional profile(s), layered as overlays, never merged",
    )
    mp.add_argument(
        "--geometry",
        choices=("age", "layer"),
        default="age",
        help="strata: age bands or dependency layers",
    )
    mp.add_argument("-o", "--output", type=Path, required=True)
    rd = sub.add_parser(
        "render", help="C6: deterministic 2D cutaway SVG from skeleton.json + substrate.json"
    )
    rd.add_argument("skeleton", type=Path)
    rd.add_argument("substrate", type=Path)
    rd.add_argument("-o", "--output", type=Path, required=True)
    rd.add_argument(
        "--html",
        type=Path,
        default=None,
        help="also write a standalone HTML page with overlay toggles",
    )
    sd = sub.add_parser(
        "skeleton-diff", help="feature churn between two skeletons of the same repo (mapper §7 Q3)"
    )
    sd.add_argument("before", type=Path)
    sd.add_argument("after", type=Path)
    sd.add_argument(
        "--renames",
        type=Path,
        default=None,
        help="substrate.json of the AFTER revision: its renames map, and its timeline "
        "for the set of nodes the intervening commits touched (the budget population)",
    )
    sd.add_argument("-o", "--output", type=Path, default=None)
    tl = sub.add_parser(
        "timelapse",
        help="Phase 1: skeleton per trunk checkpoint under HEAD's gate, budget between frames, scrubber page",
    )
    tl.add_argument("repo", type=Path)
    tl.add_argument("--validation", type=Path, required=True)
    tl.add_argument("--ruleset", type=Path, required=True)
    tl.add_argument("--overlay", type=Path, action="append", default=[])
    tl.add_argument("--geometry", choices=["age", "layer"], default="age")
    sched = tl.add_mutually_exclusive_group(required=True)
    sched.add_argument(
        "--frames", type=int, help="N evenly spaced trunk checkpoints, first and HEAD inclusive"
    )
    sched.add_argument(
        "--every", type=int, help="a checkpoint every K trunk commits, walking back from HEAD"
    )
    tl.add_argument(
        "--config",
        type=Path,
        default=None,
        help="substrate config; must reproduce the gate's fingerprint",
    )
    tl.add_argument("--cache", type=Path, default=Path("out/cache"))
    tl.add_argument("--scratch", type=Path, default=None)
    tl.add_argument("--no-deps", action="store_true")
    tl.add_argument("--blame-workers", type=int, default=8)
    tl.add_argument("-o", "--output", type=Path, required=True, help="output directory")
    br = sub.add_parser(
        "brief",
        help="M3: the architect's brief over a skeleton, generated under the surveyor stance and checked by the register lint",
    )
    br.add_argument("skeleton", type=Path)
    br.add_argument("substrate", type=Path, nargs="?", default=None)
    br.add_argument("-o", "--output", type=Path, required=True, help="brief.md")
    br.add_argument("--facts", type=Path, default=None, help="also write the facts sheet JSON")
    br.add_argument(
        "--draft",
        type=Path,
        default=None,
        help="lint this hand-written brief instead of generating",
    )
    br.add_argument(
        "--relint",
        type=Path,
        default=None,
        help="re-judge an existing brief.md under the current lint, keeping its provenance",
    )
    br.add_argument("--model", default=None, help=f"generator model (default {DEFAULT_MODEL})")
    br.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    br.add_argument(
        "--max-attempts", type=int, default=2, help="regenerate once with the violations fed back"
    )
    args = ap.parse_args(argv)
    try:
        return _dispatch(args)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"substrate {args.cmd}: could not parse a JSON input ({e})", file=sys.stderr)
        return 2
    except FileNotFoundError as e:
        print(f"substrate {args.cmd}: {e}", file=sys.stderr)
        return 2
    except (ValueError, GitError) as e:  # RulesetError, GateError, TimelapseError, mismatches
        print(f"substrate {args.cmd}: {e}", file=sys.stderr)
        return 2


def _load_json(path: Path, what: str) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"{what} {path} is not valid JSON: {e}") from e


def _dispatch(args: argparse.Namespace) -> int:
    if args.cmd == "brief":
        from .brief import anthropic_generator, relint, run_brief

        skel = _load_json(args.skeleton, "skeleton")
        sub_doc = _load_json(args.substrate, "substrate") if args.substrate else None
        if args.relint:
            r = relint(args.relint.read_text(encoding="utf-8"), skel, sub_doc)
        else:
            draft = args.draft.read_text(encoding="utf-8") if args.draft else None
            gen = (
                None
                if draft is not None
                else anthropic_generator(args.model or DEFAULT_MODEL, args.effort)
            )
            r = run_brief(skel, sub_doc, gen, draft, args.max_attempts)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(r["markdown"], encoding="utf-8")
        if args.facts:
            args.facts.write_text(
                json.dumps(r["facts"], indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        status = "PASS" if r["passed"] else f"FAILED ({len(r['violations'])})"
        print(f"{skel['repo']['name']}: register lint {status} → {args.output}", file=sys.stderr)
        for v in r["violations"][:12]:
            print(f"  {v['rule']} ¶{v['paragraph']}: {v['detail']}", file=sys.stderr)
        return 0 if r["passed"] else 1
    if args.cmd == "timelapse":
        from .mapper import load_ruleset
        from .timelapse import run_timelapse
        from .validation.substrates import SubstrateCache

        cfg = SubstrateConfig.load(args.config)
        extractor = (
            None
            if args.no_deps
            else DependencyCruiserExtractor(TOOLS_DIR, cfg.dep_ts_pre_compilation_deps)
        )
        cache = SubstrateCache(args.cache, cfg, extractor, args.scratch, args.blame_workers)
        val_doc = _load_json(args.validation, "validation")
        rs = load_ruleset(args.ruleset)
        ovs = tuple(load_ruleset(p) for p in args.overlay)
        m = run_timelapse(
            args.repo,
            cache,
            val_doc,
            rs,
            ovs,
            args.geometry,
            None,
            args.output,
            log=lambda s: print(s, file=sys.stderr),
            frames_requested=args.frames,
            every=args.every,
        )
        if args.frames and m["schedule"]["realized"] < args.frames:
            print(
                f"note: {args.frames} frames requested, {m['schedule']['realized']} distinct checkpoints on a trunk of {m['repo']['trunk_length']}",
                file=sys.stderr,
            )
        t = m["totals"]
        print(
            f"{m['repo']['name']}: {t['mapped']} mapped / {t['skipped']} skipped; movement={t['movement']} "
            f"edit={t['edit_share']:.2f} clock={t['ripple_clock_share']:.2f} jitter={t['jitter_share']:.2f} structural={t['structural_share']:.2f}; "
            f"budget {t['budget_tally']} → {args.output}/timelapse.html",
            file=sys.stderr,
        )
        return 0

    if args.cmd == "skeleton-diff":
        from .mapper.diff import skeleton_diff, touched_since

        a = _load_json(args.before, "before skeleton")
        b = _load_json(args.after, "after skeleton")
        ren: dict[str, str] = {}
        touched: set[str] | None = None
        between: int | None = None
        reason = "renames_not_given"  # no --renames: the budget has no timeline to read
        if args.renames:
            after_sub = _load_json(args.renames, "after substrate")
            ren = after_sub.get("renames", {})
            ts = touched_since(after_sub, a["repo"]["head_sha"], ren)
            if ts is not None:
                touched, between = ts
            else:
                reason = "touched_set_unavailable"  # the before sha is not in the after timeline
        d = skeleton_diff(a, b, ren, touched, between, unavailable_reason=reason)
        text = json.dumps(d, indent=1, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
        else:
            sys.stdout.write(text)
        print(
            f"common={d['common_nodes']} born={d['born']} deleted={d['deleted']} "
            f"feature_churn={d['feature_churn']:.3f} strata_moved={len(d['strata_moved'])} ({d['strata_moved_frac']:.3f}) | "
            f"untouched n={d['untouched']['n']} churn={d['untouched']['feature_churn']:.3f} "
            f"(jitter {d['untouched']['jitter_churn']:.3f}, clock {d['untouched']['clock_churn']:.3f}) "
            f"strata={d['untouched']['strata_moved_frac']:.3f} → {d['budget']['verdict']}"
            + (f" ({d['budget']['reason']})" if d["budget"]["reason"] else ""),
            file=sys.stderr,
        )
        return 0
    if args.cmd == "map":
        from .mapper import load_ruleset, map_skeleton

        sub_doc = _load_json(args.substrate, "substrate")
        val_doc = _load_json(args.validation, "validation")
        rs = load_ruleset(args.ruleset)
        ovs = tuple(load_ruleset(p) for p in args.overlay)
        skel = map_skeleton(sub_doc, val_doc, rs, ovs, args.geometry)
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
        from .cutaway import render_cutaway, render_html

        skel = _load_json(args.skeleton, "skeleton")
        sub_doc = _load_json(args.substrate, "substrate")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(render_cutaway(skel, sub_doc), encoding="utf-8")
        if args.html:
            args.html.parent.mkdir(parents=True, exist_ok=True)
            args.html.write_text(render_html(skel, sub_doc), encoding="utf-8")
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
