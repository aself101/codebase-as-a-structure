"""Cached substrate extraction for the gate. The gate needs three substrates per
repo (HEAD, the holdout split, the stability perturbation); each is a pure
function of (repo@sha, config fingerprint), so it is cached under that key."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..assemble import ExtractOptions, extract, toolchain_versions
from ..config import SubstrateConfig
from ..deps import DependencyExtractor
from ..gitutil import resolve_rev


class SubstrateCache:
    def __init__(self, cache_dir: Path, cfg: SubstrateConfig, extractor: DependencyExtractor | None,
                 scratch_dir: Path | None = None, blame_workers: int = 8):
        self.cache_dir = cache_dir
        self.cfg = cfg
        self.extractor = extractor
        self.scratch_dir = scratch_dir
        self.blame_workers = blame_workers
        self.fingerprint = cfg.fingerprint(toolchain_versions(extractor))
        cache_dir.mkdir(parents=True, exist_ok=True)

    def path_for(self, repo: Path, sha: str) -> Path:
        return self.cache_dir / f"{repo.name}-{sha[:12]}-{self.fingerprint[:12]}.substrate.json"

    def get(self, repo: Path, rev: str, truncate: bool = False) -> dict[str, Any]:
        sha = resolve_rev(repo, rev)
        p = self.path_for(repo, sha)
        if p.exists():
            return json.loads(p.read_text())
        opts = ExtractOptions(rev=sha, truncate_at=(sha if truncate else None),
                              scratch_dir=self.scratch_dir, blame_workers=self.blame_workers)
        sub = extract(repo, self.cfg, opts, self.extractor)
        p.write_text(json.dumps(sub, sort_keys=True, ensure_ascii=False))
        return sub


def canonical_resolver(sub: dict[str, Any]):
    """Chase the substrate's rename map to the name current at its rev."""
    renames: dict[str, str] = sub.get("renames", {})

    def canon(path: str) -> str:
        seen: set[str] = set()
        while path in renames and path not in seen:
            seen.add(path)
            path = renames[path]
        return path

    return canon
