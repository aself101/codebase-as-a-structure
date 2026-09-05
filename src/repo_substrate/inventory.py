"""File inventory at a revision, the seed, and the static per-file metrics
(repo-substrate-spec §3, §5, §6.2.2).

This module owns: which files are nodes (post-exclude inventory at the rev,
the §5 node-set invariant), the content-hash seed, ``size_loc``, ``lang``,
``is_test``, ``has_sibling_test`` / test proximity, and ``nesting_proxy``.
It does not read history and it does not read the dependency graph.
"""

from __future__ import annotations

import fnmatch
import hashlib
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .config import LANGUAGE_BY_EXT, SubstrateConfig
from .gitutil import ls_tree


@dataclass
class StaticNode:
    path: str
    blob_sha: str
    lang: str
    size_loc: int
    is_test: bool
    test_proximity: float  # 1.0 sibling / 0.5 same-dir-or-mirror / 0.0 none (§6.2.2)
    nesting_proxy: int | None


def _matches_any(path: str, globs: tuple[str, ...]) -> bool:
    # fnmatch's `*` matches `/`, so `**/x/**` behaves as "x anywhere in the path".
    return any(fnmatch.fnmatchcase(path, g) or fnmatch.fnmatchcase("/" + path, g) for g in globs)


def included_paths(entries: list[tuple[str, str]], cfg: SubstrateConfig) -> list[tuple[str, str]]:
    exts = set(cfg.include_extensions)
    out = []
    for path, sha in entries:
        if PurePosixPath(path).suffix not in exts:
            continue
        if _matches_any(path, cfg.exclude_globs):
            continue
        out.append((path, sha))
    return out


def tree_seed(included: list[tuple[str, str]]) -> str:
    """§3: sha256 over the sorted (path, blob) pairs of the *included* inventory.
    Content-addressed via blob SHAs, so identical trees hash identically across
    clones, and a change in exclude globs is a *fingerprint* change, not a seed
    change — except insofar as it changes which blobs are included, which it should."""
    h = hashlib.sha256()
    for path, sha in included:
        h.update(path.encode("utf-8"))
        h.update(b"\0")
        h.update(sha.encode("ascii"))
        h.update(b"\n")
    return h.hexdigest()


def is_test_path(path: str, cfg: SubstrateConfig) -> bool:
    return _matches_any(path, cfg.test_globs)


def _module_key(path: str, cfg: SubstrateConfig) -> tuple[str, str]:
    """(mirrored directory, stem-with-test-suffix-stripped) for sibling matching."""
    p = PurePosixPath(path)
    stem = p.name[: -len(p.suffix)] if p.suffix else p.name
    for suf in cfg.test_suffixes:
        if stem.endswith(suf):
            stem = stem[: -len(suf)]
            break
    d = str(p.parent) if str(p.parent) != "." else ""
    # strip a leading test root and a trailing __tests__ so tests/lib/x ↔ lib/x and lib/__tests__/x ↔ lib/x
    for root in cfg.test_roots:
        r = root.rstrip("/")
        if d == r:
            d = ""
        elif d.startswith(root):
            d = d[len(root):]
    for root in cfg.test_roots:
        r = root.rstrip("/")
        if d.endswith("/" + r):
            d = d[: -len(r) - 1]
        elif d == r:
            d = ""
    return d, stem


def test_proximity(all_paths: list[str], cfg: SubstrateConfig) -> dict[str, float]:
    """§6.2.2 tiers, pinned:
    1.0 — a name-matched test: a test file whose stem (test suffix stripped) equals the
          module's stem AND either its mirrored directory equals the module's directory
          (``tests/lib/x.js`` ↔ ``lib/x.js``, ``lib/__tests__/x.test.ts`` ↔ ``lib/x.ts``)
          or the stem is unique among non-test modules (so ``test/unit/utils/x.test.js``
          reaches ``src/security/utils/x.ts`` when there is exactly one module named ``x``).
    0.5 — proximity without a name match: a test file's mirrored directory equals the
          module's directory, or a stem-matched test exists but the stem is ambiguous
          (several modules named ``index``), so the mapping cannot be pinned to this file.
    0.0 — neither. Test files themselves get 0.0 (they do not reinforce themselves).
    """
    tests = [p for p in all_paths if is_test_path(p, cfg)]
    modules = [p for p in all_paths if not is_test_path(p, cfg)]
    sibling_keys = {_module_key(t, cfg) for t in tests}
    test_dirs = {_module_key(t, cfg)[0] for t in tests}
    test_stems = {_module_key(t, cfg)[1] for t in tests}
    stem_counts = Counter(_module_key(m, cfg)[1] for m in modules)
    out: dict[str, float] = {}
    for p in all_paths:
        if is_test_path(p, cfg):
            out[p] = 0.0
            continue
        d, stem = _module_key(p, cfg)
        if (d, stem) in sibling_keys:
            out[p] = 1.0
        elif stem in test_stems and stem_counts[stem] == 1:
            out[p] = 1.0
        elif d in test_dirs or stem in test_stems:
            out[p] = 0.5
        else:
            out[p] = 0.0
    return out


def count_loc(data: bytes) -> int:
    """Non-blank line count. Bytes, not str: encoding must not affect determinism."""
    return sum(1 for line in data.splitlines() if line.strip())


def nesting_proxy(data: bytes, max_bytes: int) -> int | None:
    """§6.2.2 pinned: max of tabs + floor(spaces / modal_width) over non-blank lines.
    modal_width = most common positive leading-space count among space-only-indented
    lines, ties toward the smaller width; 1 if no such line. None if oversize."""
    if len(data) > max_bytes:
        return None
    lines = [ln for ln in data.splitlines() if ln.strip()]
    if not lines:
        return 0
    space_counts: Counter[int] = Counter()
    leads: list[tuple[int, int]] = []
    for ln in lines:
        i = 0
        tabs = spaces = 0
        while i < len(ln) and ln[i] in (0x20, 0x09):
            if ln[i] == 0x09:
                tabs += 1
            else:
                spaces += 1
            i += 1
        leads.append((tabs, spaces))
        if tabs == 0 and spaces > 0:
            space_counts[spaces] += 1
    if space_counts:
        best = max(space_counts.values())
        width = min(w for w, c in space_counts.items() if c == best)
    else:
        width = 1
    return max(tabs + spaces // width for tabs, spaces in leads)


def build_inventory(repo: Path, worktree: Path, rev: str, cfg: SubstrateConfig) -> tuple[list[StaticNode], str]:
    """Nodes at ``rev`` (read from the detached worktree) and the seed."""
    included = included_paths(ls_tree(repo, rev), cfg)
    seed = tree_seed(included)
    paths = [p for p, _ in included]
    prox = test_proximity(paths, cfg)
    nodes: list[StaticNode] = []
    for path, sha in included:
        data = (worktree / path).read_bytes()
        nodes.append(StaticNode(
            path=path, blob_sha=sha,
            lang=LANGUAGE_BY_EXT[PurePosixPath(path).suffix],
            size_loc=count_loc(data),
            is_test=is_test_path(path, cfg),
            test_proximity=prox[path],
            nesting_proxy=nesting_proxy(data, cfg.nesting_max_bytes),
        ))
    return nodes, seed
