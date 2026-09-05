"""Thin git helpers. Everything static is read from a detached worktree at the
analyzed revision, never from the caller's working tree, so ``--rev`` and
``--truncate-at`` see exactly the tree at that SHA (repo-substrate-spec §8).
"""

from __future__ import annotations

import contextlib
import re
import subprocess
import tempfile
from collections.abc import Iterator
from pathlib import Path


class GitError(RuntimeError):
    pass


def run_git(repo: Path, *args: str, check: bool = True, text: bool = True) -> str | bytes:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=text, check=False
    )
    if check and proc.returncode != 0:
        err = proc.stderr if text else proc.stderr.decode(errors="replace")
        raise GitError(f"git {' '.join(args)} failed ({proc.returncode}): {err.strip()}")
    return proc.stdout


def resolve_rev(repo: Path, rev: str) -> str:
    return str(run_git(repo, "rev-parse", "--verify", f"{rev}^{{commit}}")).strip()


def root_commit_sha(repo: Path, rev: str) -> str:
    """§8: the first parentless ancestor of ``rev``. If history has several roots
    (a merged-in unrelated history), take the lexicographically smallest SHA so
    the value is still deterministic; the count is recorded by the caller."""
    out = str(run_git(repo, "rev-list", "--max-parents=0", rev)).split()
    if not out:
        raise GitError(f"no root commit reachable from {rev}")
    return sorted(out)[0]


def branch_name(repo: Path) -> str:
    out = str(run_git(repo, "rev-parse", "--abbrev-ref", "HEAD", check=False)).strip()
    return out or "HEAD"


def ls_tree(repo: Path, rev: str) -> list[tuple[str, str]]:
    """All blobs at ``rev`` as ``(path, blob_sha)``, sorted by path. Submodules
    (gitlinks) and symlinks are skipped: they are not source the substrate measures."""
    out = str(run_git(repo, "ls-tree", "-r", "-z", rev))
    entries: list[tuple[str, str]] = []
    for rec in out.split("\0"):
        if not rec:
            continue
        meta, path = rec.split("\t", 1)
        mode, kind, sha = meta.split()
        if kind != "blob" or mode == "120000":
            continue
        entries.append((path, sha))
    entries.sort()
    return entries


def git_version() -> str:
    out = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True).stdout
    m = re.search(r"\d+\.\d+(\.\d+)?", out)
    return m.group(0) if m else out.strip()


@contextlib.contextmanager
def detached_worktree(repo: Path, rev: str, scratch_dir: Path | None = None) -> Iterator[Path]:
    """Check ``rev`` out into a temporary detached worktree and yield its path.
    Removed on exit. Static analysis runs here so it never sees uncommitted edits."""
    base = Path(tempfile.mkdtemp(prefix="substrate-wt-", dir=scratch_dir))
    wt = base / "wt"
    run_git(repo, "worktree", "add", "--detach", "--quiet", str(wt), rev)
    try:
        yield wt
    finally:
        run_git(repo, "worktree", "remove", "--force", str(wt), check=False)
        with contextlib.suppress(OSError):
            base.rmdir()
        run_git(repo, "worktree", "prune", check=False)
