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


def load_tsconfig(worktree: Path) -> dict | None:
    """tsconfig.json with comments and trailing commas stripped (it is JSONC in practice)."""
    p = worktree / "tsconfig.json"
    if not p.exists():
        return None
    text = p.read_text(errors="replace")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"(^|[^:\"'])//[^\n]*", r"\1", text)
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _usable_tsconfig(worktree: Path) -> str | None:
    """dependency-cruiser loads tsconfig through the TypeScript API, which fails hard when
    `extends` names a package that is not installed (a fresh clone has no node_modules).
    Path aliases are the only thing we need from it, so: if the config is self-contained,
    use it; if it extends a package, write a stripped copy into the (temporary) worktree
    with `extends` removed and use that; if there is nothing alias-relevant, skip it."""
    cfg = load_tsconfig(worktree)
    if cfg is None:
        return None
    ext = cfg.get("extends")
    if not ext:
        return "tsconfig.json"
    if isinstance(ext, str) and ext.startswith(".") and (worktree / ext).exists():
        return "tsconfig.json"
    stripped = {k: v for k, v in cfg.items() if k != "extends"}
    out = worktree / "tsconfig.substrate.json"
    out.write_text(json.dumps(stripped))
    return out.name


class DependencyCruiserExtractor:
    """Shells out to the pinned dependency-cruiser in this project's node_modules."""

    name = "dependency-cruiser"

    def __init__(self, tools_dir: Path):
        self.tools_dir = tools_dir
        self.bin = tools_dir / "node_modules" / ".bin" / "depcruise"
        if not self.bin.exists():
            raise RuntimeError(f"dependency-cruiser not installed at {self.bin}; run `npm install` in {tools_dir}")

    def version(self) -> str:
        pkg = json.loads((self.tools_dir / "node_modules" / "dependency-cruiser" / "package.json").read_text())
        return f"dependency-cruiser@{pkg['version']}"

    def extract(self, worktree: Path, node_paths: set[str]) -> DependencyResult:
        res = DependencyResult(backend_version=self.version())
        if not node_paths:
            return res
        # Roots: top-level directories/files that contain JS/TS nodes. Passing the repo
        # root would make depcruise crawl node_modules of the *target* if present.
        roots = sorted({p.split("/", 1)[0] for p in node_paths})
        args = [
            str(self.bin), "--no-config", "--output-type", "json",
            "--exclude", "(^|/)node_modules/",
            "--do-not-follow", "(^|/)node_modules/",
            "--max-depth", "0",
        ]
        ts_arg = _usable_tsconfig(worktree)
        if ts_arg:
            args += ["--ts-config", ts_arg]
        args += roots
        env = dict(os.environ)
        env["NODE_OPTIONS"] = env.get("NODE_OPTIONS", "") + " --max-old-space-size=4096"
        proc = subprocess.run(args, cwd=worktree, capture_output=True, text=True, check=False, env=env)
        if proc.returncode not in (0, 1) or not proc.stdout.strip():
            # depcruise exits 1 when its (absent) rules produce warnings; anything else is a failure.
            raise RuntimeError(f"depcruise failed ({proc.returncode}): {proc.stderr[-2000:]}")
        data = json.loads(proc.stdout)
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
                # extension such as .json/.css). Not an edge, not a failure.
        return res


def has_node() -> bool:
    return shutil.which("node") is not None
