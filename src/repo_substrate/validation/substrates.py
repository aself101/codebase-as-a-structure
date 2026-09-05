"""Cached substrate extraction for the gate. The gate needs three substrates per
repo (HEAD, the holdout split, the stability perturbation); each is a pure
function of (repo@sha, truncate, config fingerprint), so it is cached under
that key.

Integrity (2026-09-04 audit + circumvention A2): writes are atomic (tmp + rename),
a corrupt or foreign cache entry is a cache miss, a cached document must carry
the fingerprint the gate is running under, and every document handed to the
gate is attested by its content-hash seed and the sha256 of its bytes, both
recorded in validation.json. Renaming a cache file across fingerprints or
hand-editing a metric therefore changes an attestation the report prints.
"""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from ..assemble import SCHEMA_VERSION, ExtractOptions, extract, toolchain_versions
from ..config import SubstrateConfig
from ..deps import DependencyExtractor
from ..gitutil import resolve_rev


class SubstrateCache:
    def __init__(self, cache_dir: Path, cfg: SubstrateConfig, extractor: DependencyExtractor | None,
                 scratch_dir: Path | None = None, blame_workers: int = 8) -> None:
        self.cache_dir = cache_dir
        self.cfg = cfg
        self.extractor = extractor
        self.scratch_dir = scratch_dir
        self.blame_workers = blame_workers
        self.toolchain = toolchain_versions(extractor)
        self.fingerprint = cfg.fingerprint(self.toolchain)
        self.attestations: dict[str, dict[str, str]] = {}  # cache key -> {sha, seed, bytes_sha256, truncated}
        cache_dir.mkdir(parents=True, exist_ok=True)

    def effective_config(self) -> dict[str, Any]:
        """The fingerprint's preimage, embedded verbatim in validation.json (circumvention A7)."""
        return self.cfg.effective(self.toolchain)

    def path_for(self, repo: Path, sha: str, truncate: bool) -> Path:
        mode = "trunc" if truncate else "tip"
        return self.cache_dir / f"{repo.name}-{sha[:12]}-{mode}-{self.fingerprint[:12]}.substrate.json"

    def _load_valid(self, p: Path) -> dict[str, Any] | None:
        """A cached document is used only if it parses, is the current schema, and carries
        this run's fingerprint. Anything else is a miss (and a stale file is removed)."""
        try:
            raw = p.read_bytes()
            doc = json.loads(raw.decode("utf-8"))
        except (OSError, ValueError):
            p.unlink(missing_ok=True)
            return None
        if doc.get("schema_version") != SCHEMA_VERSION or (doc.get("repo") or {}).get("config_fingerprint") != self.fingerprint:
            p.unlink(missing_ok=True)
            return None
        self._attest(p, doc, raw)
        return doc

    def _attest(self, p: Path, doc: dict[str, Any], raw: bytes) -> None:
        self.attestations[p.name] = {
            "head_sha": doc["repo"]["head_sha"], "seed": doc["seed"],
            "bytes_sha256": hashlib.sha256(raw).hexdigest(),
            "truncated_at": doc["repo"].get("truncated_at"),
        }

    def get(self, repo: Path, rev: str, truncate: bool = False) -> dict[str, Any]:
        sha = resolve_rev(repo, rev)
        p = self.path_for(repo, sha, truncate)
        if p.exists():
            doc = self._load_valid(p)
            if doc is not None:
                return doc
        opts = ExtractOptions(rev=sha, truncate_at=(sha if truncate else None),
                              scratch_dir=self.scratch_dir, blame_workers=self.blame_workers)
        sub = extract(repo, self.cfg, opts, self.extractor)
        raw = json.dumps(sub, sort_keys=True, ensure_ascii=False).encode("utf-8")
        tmp = p.with_suffix(".tmp")
        tmp.write_bytes(raw)
        os.replace(tmp, p)  # atomic on POSIX: a reader never sees a partial file
        self._attest(p, sub, raw)
        return sub


def canonical_resolver(sub: dict[str, Any]) -> Callable[[str], str]:
    """Chase the substrate's rename map to the name current at its rev."""
    renames: dict[str, str] = sub.get("renames", {})

    def canon(path: str) -> str:
        seen: set[str] = set()
        while path in renames and path not in seen:
            seen.add(path)
            path = renames[path]
        return path

    return canon
