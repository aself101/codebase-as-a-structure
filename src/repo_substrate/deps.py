"""Dependency extraction (repo-substrate-spec §8; D-006).

The edge contract is owned here, over whatever backend produced the raw
dependencies: directed ``import`` edges from importer to imported, self-loops
dropped, duplicates collapsed, only resolved in-repo targets become edges,
and the two kinds of non-edge are counted separately because the split is
load-bearing for §6.3:

- external: a bare specifier (``react``, ``node:fs``, ``@scope/pkg``) — a successful
  resolution to an out-of-repo target, whether or not node_modules is present.
  Counted, never a quality problem.
- unresolved: a relative/absolute/aliased specifier the backend could not place —
  a genuine in-repo resolution failure. This is the quality signal.

Backend v0: dependency-cruiser (pinned in package.json), run against a detached
worktree so it sees exactly the tree at the analyzed rev.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

_BARE_SPECIFIER = re.compile(r"^(node:)?[A-Za-z0-9@][^:]*$")


@dataclass
class DependencyResult:
    edges: set[tuple[str, str]] = field(default_factory=set)  # (from, to), in-repo, resolved
    external_imports: int = 0
    unresolved_imports: int = 0
    unresolved_samples: list[tuple[str, str]] = field(default_factory=list)  # (from, specifier)
    non_node_imports: int = 0  # resolved in-repo to a path that is not a node (excluded glob, .json/.css) — §8 third kind
    tsconfig_malformed: str | None = None
    backend_version: str = "unknown"


class DependencyExtractor(Protocol):
    name: str

    def extract(self, worktree: Path, node_paths: set[str]) -> DependencyResult: ...

    def version(self) -> str: ...


def _is_relative_or_alias(spec: str) -> bool:
    """A specifier that *should* resolve in-repo: relative, absolute, or alias-shaped
    (tsconfig paths like ``@/x`` or ``~/x``). Anything else is treated as external."""
    if spec.startswith((".", "/")):
        return True
    if spec.startswith(("@/", "~/", "#")):
        return True
    return False


class TsconfigMalformed(RuntimeError):
    """tsconfig.json exists but cannot be parsed. Distinct from 'absent' (None): a malformed
    config silently disables path aliases and systematically under-resolves imports, which
    must be a visible caveat, not a quiet default (2026-09-04 audit)."""


def load_tsconfig(worktree: Path) -> dict | None:
    """tsconfig.json with comments and trailing commas stripped (it is JSONC in practice).
    Returns None only when the file is absent; raises TsconfigMalformed when it is unparseable."""
    p = worktree / "tsconfig.json"
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"(^|[^:\"'])//[^\n]*", r"\1", text)
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise TsconfigMalformed(f"tsconfig.json unparseable: {e}") from e


def _usable_tsconfig(worktree: Path) -> str | None:
    """dependency-cruiser loads tsconfig through the TypeScript API, which fails hard when
    `extends` names a package that is not installed (a fresh clone has no node_modules).
    Path aliases are the only thing we need from it, so: if the config is self-contained,
    use it; if it extends a package, write a stripped copy into the (temporary) worktree
    with `extends` removed and use that; if there is nothing alias-relevant, skip it."""
    cfg = load_tsconfig(worktree)  # TsconfigMalformed propagates: the caller records it as a caveat
    if cfg is None:
        return None
    ext = cfg.get("extends")
    if not ext:
        return "tsconfig.json"
    if isinstance(ext, str) and ext.startswith(".") and (worktree / ext).exists():
        return "tsconfig.json"
    stripped = {k: v for k, v in cfg.items() if k != "extends"}
    out = worktree / "tsconfig.substrate.json"
    out.write_text(json.dumps(stripped), encoding="utf-8")
    return out.name


class DependencyCruiserExtractor:
    """Shells out to the pinned dependency-cruiser in this project's node_modules."""

    name = "dependency-cruiser"

    def __init__(self, tools_dir: Path, ts_pre_compilation_deps: bool = True, timeout: int = 900) -> None:
        self.tools_dir = tools_dir
        self.ts_pre_compilation_deps = ts_pre_compilation_deps
        self.timeout = timeout
        self.bin = tools_dir / "node_modules" / ".bin" / "depcruise"
        if not self.bin.exists():
            raise RuntimeError(f"dependency-cruiser not installed at {self.bin}; run `npm install` in {tools_dir}")

    def version(self) -> str:
        p = self.tools_dir / "node_modules" / "dependency-cruiser" / "package.json"
        try:
            pkg = json.loads(p.read_text(encoding="utf-8"))
            return f"dependency-cruiser@{pkg['version']}"
        except (OSError, json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"cannot read dependency-cruiser version from {p}: {e}") from e

    def extract(self, worktree: Path, node_paths: set[str]) -> DependencyResult:
        res = DependencyResult(backend_version=self.version())
        if not node_paths:
            return res
        try:
            ts_arg = _usable_tsconfig(worktree)
        except TsconfigMalformed as e:
            res.tsconfig_malformed = str(e)
            ts_arg = None
        # Roots: top-level directories/files that contain JS/TS nodes. Passing the repo
        # root would make depcruise crawl node_modules of the *target* if present.
        roots = sorted({p.split("/", 1)[0] for p in node_paths})
        args = [
            str(self.bin), "--no-config", "--output-type", "json",
            "--exclude", "(^|/)node_modules/",
            "--do-not-follow", "(^|/)node_modules/",
            "--max-depth", "0",
        ]
        if self.ts_pre_compilation_deps:
            # Without this, `import type { X } from "./x"` produces no edge (the import is erased
            # at compile time). The second instrument caught the gap on typeorm: 9 vs 621 importers.
            args.append("--ts-pre-compilation-deps")
        if ts_arg:
            args += ["--ts-config", ts_arg]
        args += roots
        env = dict(os.environ)
        env["NODE_OPTIONS"] = env.get("NODE_OPTIONS", "") + " --max-old-space-size=4096"
        try:
            proc = subprocess.run(args, cwd=worktree, capture_output=True, check=False, env=env,
                                  timeout=self.timeout)
        except subprocess.TimeoutExpired as e:
            raise RuntimeError(f"depcruise timed out after {self.timeout}s in {worktree.name}") from e
        stdout = proc.stdout.decode("utf-8", "replace")
        stderr = proc.stderr.decode("utf-8", "replace")
        if proc.returncode not in (0, 1) or not stdout.strip():
            # depcruise exits 1 when its (absent) rules produce warnings; anything else is a failure.
            raise RuntimeError(f"depcruise failed ({proc.returncode}): {stderr[-2000:]}")
        try:
            data = json.loads(stdout)
        except json.JSONDecodeError as e:
            raise RuntimeError(
                f"depcruise produced unparseable JSON (exit {proc.returncode}); "
                f"stdout starts {stdout[:200]!r}; stderr tail {stderr[-500:]!r}"
            ) from e
        for mod in data.get("modules", []):
            src = mod.get("source", "")
            if src not in node_paths:
                continue
            for dep in mod.get("dependencies", []):
                spec = dep.get("module", "")
                types = set(dep.get("dependencyTypes", []))
                resolved = dep.get("resolved", "")
                could_not = bool(dep.get("couldNotResolve"))
                if "core" in types:
                    res.external_imports += 1
                    continue
                if could_not or "unknown" in types or "undetermined" in types or "npm-unknown" in types:
                    if _is_relative_or_alias(spec):
                        res.unresolved_imports += 1
                        if len(res.unresolved_samples) < 50:
                            res.unresolved_samples.append((src, spec))
                    else:
                        res.external_imports += 1
                    continue
                if resolved in node_paths:
                    if resolved != src:
                        res.edges.add((src, resolved))
                    continue
                if resolved.startswith("node_modules/") or any(t.startswith("npm") for t in types):
                    res.external_imports += 1
                    continue
                # Resolved to an in-repo path that is not a node (excluded glob, non-source
                # extension such as .json/.css). Not an edge, not a failure — counted (§8 third kind).
                res.non_node_imports += 1
        res.unresolved_samples.sort()
        return res


def has_node() -> bool:
    return shutil.which("node") is not None
