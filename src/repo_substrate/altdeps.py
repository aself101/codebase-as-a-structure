"""Second import instrument (validation-spec §2.4.2 grounding class G2; D-008).

An independent, regex-based JS/TS import scanner with its own resolver. It shares
no code with dependency-cruiser and is deliberately naive: it exists so that
``fan_in`` has a second measurement it can be checked against. Where the two
instruments disagree (path aliases, re-exports, dynamic imports, extension-less
resolution) the disagreement is the finding, not a bug to paper over.

Produces ``fan_in_alt`` per node: distinct in-repo importers found by this scanner.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path, PurePosixPath

from .deps import (  # JSONC parsing only; no resolution code is shared
    TsconfigMalformed,
    load_tsconfig,
)

_SPECIFIER = re.compile(
    r"""(?:^|[^\w$.])(?:import|export)\s*(?:[\w*{}\s,$]+?\s*from\s*)?['"]([^'"\n]+)['"]"""
    r"""|(?:^|[^\w$.])require\s*\(\s*['"]([^'"\n]+)['"]\s*\)"""
    r"""|(?:^|[^\w$.])import\s*\(\s*['"]([^'"\n]+)['"]\s*\)""",
    re.MULTILINE,
)
_EXTS = (".ts", ".tsx", ".mts", ".cts", ".js", ".jsx", ".mjs", ".cjs")
_STRIP_EXT = re.compile(r"\.(js|mjs|cjs|jsx|ts|tsx|mts|cts)$")


def _strip_comments(src: str) -> str:
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.DOTALL)
    return re.sub(r"(^|[^:\\\"'])//[^\n]*", r"\1", src)


def _normalize(p: PurePosixPath) -> str:
    parts: list[str] = []
    for seg in p.parts:
        if seg == "..":
            if parts:
                parts.pop()
        elif seg not in (".", ""):
            parts.append(seg)
    return "/".join(parts)


def _candidates(base: str) -> list[str]:
    out = [base]
    stem = _STRIP_EXT.sub("", base)
    out += [stem + e for e in _EXTS]
    out += [base + e for e in _EXTS]
    out += [base + "/index" + e for e in _EXTS]
    return out


def _alias_map(tsconfig: dict | None) -> tuple[str, list[tuple[str, list[str]]]]:
    if not tsconfig:
        return "", []
    co = tsconfig.get("compilerOptions") or {}
    base = (co.get("baseUrl") or "").strip("./")
    paths = co.get("paths") or {}
    pairs = []
    for pat, targets in paths.items():
        if isinstance(targets, list):
            pairs.append((pat, [str(t) for t in targets]))
    return base, pairs


def _resolve(
    spec: str, importer: str, nodes: set[str], base_url: str, aliases: list[tuple[str, list[str]]]
) -> str | None:
    spec = spec.split("?", 1)[0]
    targets: list[str] = []
    if spec.startswith("."):
        targets.append(_normalize(PurePosixPath(importer).parent / spec))
    elif spec.startswith("/"):
        return None
    else:
        for pat, outs in aliases:
            if pat.endswith("/*") and spec.startswith(pat[:-1]):
                rest = spec[len(pat) - 1 :]
                for o in outs:
                    o2 = o[:-1] + rest if o.endswith("*") else o
                    targets.append(_normalize(PurePosixPath(base_url) / o2))
            elif pat == spec:
                for o in outs:
                    targets.append(_normalize(PurePosixPath(base_url) / o))
        if base_url and not targets:
            targets.append(_normalize(PurePosixPath(base_url) / spec))
    for t in targets:
        for c in _candidates(t):
            if c in nodes:
                return c
    return None


def scan_fan_in_alt(
    worktree: Path, node_paths: set[str], test_paths: set[str] | None = None
) -> tuple[dict[str, int], dict[str, int], dict[str, int], list[str]]:
    """Returns (fan_in_alt, fan_out_alt, test_fan_in_alt, unreadable_paths) over in-repo resolved
    edges, self-loops dropped, duplicates collapsed — the same edge contract as the primary
    extractor (§8). test_fan_in_alt counts importers that are in `test_paths`."""
    try:
        base_url, aliases = _alias_map(load_tsconfig(worktree))
    except TsconfigMalformed:
        base_url, aliases = (
            "",
            [],
        )  # the primary extractor records the caveat; this instrument proceeds alias-less
    importers: dict[str, set[str]] = defaultdict(set)
    out_edges: dict[str, set[str]] = defaultdict(set)
    js_ts = {p for p in node_paths if PurePosixPath(p).suffix in _EXTS}
    unreadable: list[str] = []
    for p in sorted(js_ts):
        try:
            src = (worktree / p).read_text(encoding="utf-8", errors="replace")
        except OSError:
            unreadable.append(p)  # counted, not swallowed: an under-count moves a G2 verdict
            continue
        for m in _SPECIFIER.finditer(_strip_comments(src)):
            spec = m.group(1) or m.group(2) or m.group(3)
            if not spec:
                continue
            target = _resolve(spec, p, js_ts, base_url, aliases)
            if target and target != p:
                importers[target].add(p)
                out_edges[p].add(target)
    tests = test_paths or set()
    fan_in = {p: len(importers.get(p, ())) for p in node_paths}
    fan_out = {p: len(out_edges.get(p, ())) for p in node_paths}
    test_fan_in = {p: sum(1 for i in importers.get(p, ()) if i in tests) for p in node_paths}
    return fan_in, fan_out, test_fan_in, unreadable
