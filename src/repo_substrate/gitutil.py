"""Thin git helpers. Everything static is read from a detached worktree at the
analyzed revision, never from the caller's working tree, so ``--rev`` and
``--truncate-at`` see exactly the tree at that SHA (repo-substrate-spec §8).

All subprocess I/O is decoded as UTF-8 explicitly: the locale must never reach
the output (2026-09-04 audit — ``LC_ALL=C`` crashed on a non-ASCII path and a
latin-1 locale would have produced mojibake node ids under an unchanged fingerprint).
"""

from __future__ import annotations

import contextlib
import re
import shutil
import subprocess
import tempfile
from collections.abc import Iterator
from pathlib import Path

GIT_TIMEOUT = 600  # seconds; a hung git must fail loudly, not block forever


class GitError(RuntimeError):
    pass


def run_git(repo: Path, *args: str, check: bool = True) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), *args], capture_output=True, check=False,
            timeout=GIT_TIMEOUT,
        )
    except subprocess.TimeoutExpired as e:
        raise GitError(f"git {' '.join(args)} timed out after {GIT_TIMEOUT}s") from e
    if check and proc.returncode != 0:
        raise GitError(f"git {' '.join(args)} failed ({proc.returncode}): {proc.stderr.decode('utf-8', 'replace').strip()}")
    return proc.stdout.decode("utf-8", "surrogateescape")


def resolve_rev(repo: Path, rev: str) -> str:
    return run_git(repo, "rev-parse", "--verify", f"{rev}^{{commit}}").strip()


def root_commit_sha(repo: Path, rev: str) -> str:
    """§8: the first parentless ancestor of ``rev``. If history has several roots
    (a merged-in unrelated history), take the lexicographically smallest SHA so
    the value is still deterministic; the count is recorded by the caller."""
    out = run_git(repo, "rev-list", "--max-parents=0", rev).split()
    if not out:
        raise GitError(f"no root commit reachable from {rev}")
    return min(out)


def branch_name(repo: Path) -> str:
    out = run_git(repo, "rev-parse", "--abbrev-ref", "HEAD", check=False).strip()
    return out or "HEAD"


def ls_tree(repo: Path, rev: str) -> list[tuple[str, str]]:
    """All blobs at ``rev`` as ``(path, blob_sha)``, sorted by path. Submodules
    (gitlinks) and symlinks are skipped: they are not source the substrate measures."""
    out = run_git(repo, "ls-tree", "-r", "-z", rev)
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


def cat_blobs(repo: Path, shas: list[str]) -> dict[str, bytes]:
    """Read blob contents by SHA via one ``git cat-file --batch``. Reading by blob rather
    than by worktree path is what makes the inventory immune to case-insensitive
    filesystems: on APFS a tree holding both ``A.ts`` and ``a.ts`` checks out one file,
    and a path read returns the other file's bytes with no error (2026-09-04 audit)."""
    if not shas:
        return {}
    uniq = sorted(set(shas))
    proc = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "--batch"],
        input=("\n".join(uniq) + "\n").encode("ascii"), capture_output=True, check=False,
        timeout=GIT_TIMEOUT,
    )
    if proc.returncode != 0:
        raise GitError(f"git cat-file --batch failed: {proc.stderr.decode('utf-8', 'replace')[-300:]}")
    data = proc.stdout
    out: dict[str, bytes] = {}
    pos = 0
    for sha in uniq:
        nl = data.index(b"\n", pos)
        header = data[pos:nl].decode("ascii")
        parts = header.split()
        if len(parts) != 3 or parts[0] != sha:
            raise GitError(f"cat-file: unexpected header {header!r} for {sha}")
        size = int(parts[2])
        start = nl + 1
        out[sha] = data[start:start + size]
        pos = start + size + 1  # trailing newline after each object
    return out


def git_version() -> str:
    out = subprocess.run(["git", "--version"], capture_output=True, check=True, timeout=30).stdout.decode("utf-8", "replace")
    m = re.search(r"\d+\.\d+(\.\d+)?", out)
    return m.group(0) if m else out.strip()


@contextlib.contextmanager
def detached_worktree(repo: Path, rev: str, scratch_dir: Path | None = None) -> Iterator[Path]:
    """Check ``rev`` out into a temporary detached worktree and yield its path.
    Removed on exit whatever happens (the temp dir is created inside the try, and
    removal falls back to rmtree so a failed ``worktree remove`` cannot leak a checkout)."""
    base: Path | None = None
    try:
        base = Path(tempfile.mkdtemp(prefix="substrate-wt-", dir=scratch_dir))
        wt = base / "wt"
        run_git(repo, "worktree", "add", "--detach", "--quiet", str(wt), rev)
        yield wt
    finally:
        if base is not None:
            run_git(repo, "worktree", "remove", "--force", str(base / "wt"), check=False)
            shutil.rmtree(base, ignore_errors=True)
            run_git(repo, "worktree", "prune", check=False)
