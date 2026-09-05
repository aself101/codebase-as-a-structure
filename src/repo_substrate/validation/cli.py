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
from .config import ValidationConfig
from .gate import build_validation
from .holdout import run_holdout
from .report import render_holdout_report
from .substrates import SubstrateCache


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="substrate-validate")
    sub = ap.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run")
    run.add_argument("--repo", type=Path, action="append", required=True)
    run.add_argument("--out", type=Path, required=True)
    run.add_argument("--config", type=Path, default=None)
    run.add_argument("--vconfig", type=Path, default=None)
    run.add_argument("--blind-dir", type=Path, default=Path("blind"))
    run.add_argument("--cache", type=Path, default=Path("out/cache"))
    run.add_argument("--scratch", type=Path, default=None)
    run.add_argument("--no-deps", action="store_true")
    run.add_argument("--blame-workers", type=int, default=8)
    args = ap.parse_args(argv)

    cfg = SubstrateConfig.load(args.config)
    vcfg = ValidationConfig.load(args.vconfig)
    extractor = None if args.no_deps else DependencyCruiserExtractor(TOOLS_DIR)
    cache = SubstrateCache(args.cache, cfg, extractor, args.scratch, args.blame_workers)

    holdouts, asserted, refs = [], [], []
    for repo in args.repo:
        repo = repo.resolve()
        print(f"[{repo.name}] holdout…", file=sys.stderr)
        h = run_holdout(repo, cache, vcfg)
        print(f"[{repo.name}] split={h.split_sha[:10]} eligible={h.n_eligible} positives={h.n_positives} "
              f"coverage={h.coverage:.2f} degenerate={h.degenerate}", file=sys.stderr)
        print(f"[{repo.name}] asserted bar…", file=sys.stderr)
        blind = args.blind_dir / f"{repo.name}.md"
        a = run_asserted(repo, cache, vcfg, blind if blind.exists() else None)
        holdouts.append(h)
        asserted.append(a)
        refs.append({"name": h.name, "head_sha": h.head_sha, "path": str(repo),
                     "holdout": {k: v for k, v in asdict(h).items() if k not in ("baselines", "signals")},
                     "asserted": {"perturbed_sha": a.perturbed_sha, "n_population": a.n_population,
                                  "n_compared": a.n_compared, "n_excluded_touched": a.n_excluded_touched,
                                  "recognition_ref": a.recognition_ref}})

    doc = build_validation(holdouts, asserted, vcfg, cache.fingerprint, refs)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "validation.json").write_text(json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
    (args.out / "holdout-report.md").write_text(render_holdout_report(doc))
    for name, s in doc["signals"].items():
        print(f"  {name:28s} {s['status']:12s} {s.get('reason','')}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
