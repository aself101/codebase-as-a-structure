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
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .config import LANGUAGE_BY_EXT, SubstrateConfig
from .gitutil import cat_blobs, ls_tree


@dataclass
class StaticNode:
    path: str
    blob_sha: str
    lang: str
    size_loc: int
    is_test: bool
    test_proximity: float  # 1.0 sibling / 0.5 same-dir-or-mirror / 0.0 none (§6.2.2)
    nesting_proxy: int | None
    package: str = ""  # nearest ancestor directory holding a package.json ("" = repo root) (D-029)
    is_package_entry: bool = (
        False  # declared entry of its package (package.json main/module/types/bin/exports) (D-029)
    )


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
            d = d[len(root) :]
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
        if (d, stem) in sibling_keys or stem in test_stems and stem_counts[stem] == 1:
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


SOURCE_EXTS = (".ts", ".tsx", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs", ".py")
ENTRY_FIELDS = ("main", "module", "browser", "types", "typings")


def _entry_strings(value) -> list[str]:
    """Every string reachable in a package.json entry value (`exports` nests by condition)."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [x for v in value.values() for x in _entry_strings(v)]
    if isinstance(value, list):
        return [x for v in value for x in _entry_strings(v)]
    return []


def _resolve_entry(pkg_dir: str, target: str, present: set[str]) -> str | None:
    """Map a declared entry to an inventory path. Exact first; then the declared heuristic
    (recorded in the grounding table): a built entry `./index.js` maps to a source
    `index.ts`, `src/index.ts`, `lib/index.js` …, and a directory to its index. Returns the
    first present candidate, or None."""
    t = target.strip()
    if not t or t.startswith(("http:", "https:", "node:")):
        return None
    t = t.removeprefix("./")
    rel = re.sub(r"/+", "/", t).strip("/")
    if not rel:
        rel = "index"
    rel_stem = re.sub(r"\.(d\.ts|d\.mts|[cm]?[jt]sx?|py)$", "", rel)
    root = f"{pkg_dir}/" if pkg_dir else ""
    cands: list[str] = [root + rel]
    for pre in ("", "src/", "lib/", "source/"):
        stem = f"{root}{pre}{rel_stem}"
        for ext in SOURCE_EXTS:
            cands.append(stem + ext)
            cands.append(f"{stem}/index{ext}")
    for c in cands:
        c = re.sub(r"/+", "/", c)
        if c in present:
            return c
    return None


def package_facts(
    entries: list[tuple[str, str]], included: list[tuple[str, str]], repo: Path
) -> tuple[dict[str, str], set[str]]:
    """(package_of: included path → nearest package dir, entry paths) from every
    package.json in the tree (D-029). `node_modules` and the exclude globs are honoured by
    the caller's `included` list for nodes; package.json files under node_modules are skipped."""
    pkg_blobs = [
        (path, sha)
        for path, sha in entries
        if PurePosixPath(path).name == "package.json" and "node_modules" not in path.split("/")
    ]
    present = {p for p, _ in included}
    pkg_dirs: list[str] = []
    entry_paths: set[str] = set()
    if pkg_blobs:
        blobs = cat_blobs(repo, [sha for _, sha in pkg_blobs])
        for path, sha in pkg_blobs:
            pkg_dir = str(PurePosixPath(path).parent)
            pkg_dir = "" if pkg_dir == "." else pkg_dir
            pkg_dirs.append(pkg_dir)
            try:
                doc = json.loads(blobs[sha].decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                continue
            if not isinstance(doc, dict):
                continue
            declared: list[str] = []
            for f in ENTRY_FIELDS:
                declared += _entry_strings(doc.get(f))
            declared += _entry_strings(doc.get("bin"))
            declared += _entry_strings(doc.get("exports"))
            for d in declared:
                r = _resolve_entry(pkg_dir, d, present)
                if r:
                    entry_paths.add(r)
    pkg_dirs = sorted(set(pkg_dirs), key=len, reverse=True)
    package_of: dict[str, str] = {}
    for path in present:
        owner = ""
        for d in pkg_dirs:
            if d and path.startswith(d + "/"):
                owner = d
                break
        package_of[path] = owner
    return package_of, entry_paths


def build_inventory(repo: Path, rev: str, cfg: SubstrateConfig) -> tuple[list[StaticNode], str]:
    """Nodes at ``rev`` and the seed. Contents are read by blob SHA (``git cat-file``),
    never by worktree path, so a case-insensitive filesystem cannot swap two files."""
    entries = ls_tree(repo, rev)
    included = included_paths(entries, cfg)
    seed = tree_seed(included)
    package_of, entry_paths = package_facts(entries, included, repo)
    paths = [p for p, _ in included]
    prox = test_proximity(paths, cfg)
    blobs = cat_blobs(repo, [sha for _, sha in included])
    nodes: list[StaticNode] = []
    for path, sha in included:
        data = blobs[sha]
        nodes.append(
            StaticNode(
                path=path,
                blob_sha=sha,
                lang=LANGUAGE_BY_EXT[PurePosixPath(path).suffix],
                size_loc=count_loc(data),
                is_test=is_test_path(path, cfg),
                test_proximity=prox[path],
                nesting_proxy=nesting_proxy(data, cfg.nesting_max_bytes),
                package=package_of.get(path, ""),
                is_package_entry=path in entry_paths,
            )
        )
    return nodes, seed
