"""
history_miner.py — repo-substrate · history-mining component (spec §5 + §7).

Emits ONLY the history-derived signals. Deliberately does NOT compute:
  - size_loc                          -> file inventory at HEAD (static read)
  - fan_in / fan_out / centrality     -> DependencyExtractor (dependency graph)
  - is_test / has_sibling_test        -> path classifier
Holding that boundary is what keeps the substrate's components swappable and
the determinism contract auditable.

pydriller is hidden behind the HistoryMiner Protocol so a faster pygit2-backed
miner can replace it later without anything downstream noticing.

Requires pydriller >= 2.0 (uses ModifiedFile.added_lines / .deleted_lines;
pre-2.0 named these .added / .removed).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

from pydriller import Repository, ModificationType


# --- §7 commit-type classification -------------------------------------------

_CONVENTIONAL = re.compile(r"^(feat|fix|refactor|docs|test|chore|revert)\b", re.I)
_NATIVE_REVERT = re.compile(r'^revert[\s:"]', re.I)   # git's default `Revert "..."`
_FIX_FALLBACK = re.compile(r"\b(bug|hotfix|patch)\b", re.I)


def classify_commit(subject: str, is_merge: bool) -> tuple[str, str]:
    """Deterministic first-match cascade. Returns (type, matched_rule).

    AUDIT: subject-only. A squashed commit carrying many changes still gets one
    label; commit-body signals (BREAKING CHANGE, trailers) are ignored.
    """
    s = subject.strip()
    m = _CONVENTIONAL.match(s)
    if m:
        return m.group(1).lower(), "conventional-prefix"
    if _NATIVE_REVERT.match(s):
        return "revert", "native-revert-subject"
    if is_merge:
        return "merge", "merge-parents"
    if _FIX_FALLBACK.search(s):
        return "fix", "subject-regex"
    return "other", "default"


# --- result types ------------------------------------------------------------

@dataclass
class CommitRecord:
    sha: str
    ts: datetime
    author: str
    subject: str
    type: str
    matched_rule: str
    nodes_touched: list[str]
    added: int
    deleted: int
    is_merge: bool


@dataclass
class FileHistory:
    """Accumulates under a file's *canonical* (rename-followed) path."""
    path: str
    introduced_idx: int
    first_seen: datetime
    last_seen: datetime
    commit_count: int = 0
    churn_added: int = 0
    churn_deleted: int = 0
    fix_count: int = 0       # type in {fix, revert}  (spec §5)
    revert_count: int = 0    # type == revert
    authors: set[str] = field(default_factory=set, repr=False)

    @property
    def churn_lines(self) -> int:
        return self.churn_added + self.churn_deleted

    @property
    def author_count(self) -> int:
        return len(self.authors)

    def raw_metrics(self, as_of: datetime) -> dict:
        """The §5 history-derived subset. Day-counts are measured relative to
        HEAD (`as_of`), NEVER wall-clock — re-running tomorrow must not move a
        single value."""
        return {
            "commit_count": self.commit_count,
            "churn_lines": self.churn_lines,
            "fix_count": self.fix_count,
            "revert_count": self.revert_count,
            "author_count": self.author_count,
            "age_days": (as_of - self.first_seen).days,
            "last_touched_days": (as_of - self.last_seen).days,
            "introduced_idx": self.introduced_idx,
        }


@dataclass
class HistoryResult:
    head_sha: str
    as_of: datetime
    files: dict[str, FileHistory]
    timeline: list[CommitRecord]


# --- interface ---------------------------------------------------------------

class HistoryMiner(Protocol):
    def mine(self, repo_path: str, rev: str = "HEAD") -> HistoryResult: ...


# --- pydriller implementation ------------------------------------------------

class PydrillerHistoryMiner:
    """History miner backed by pydriller (GitPython underneath).

    Rename-following is the fiddly part: pydriller reports renames per-commit
    (old_path -> new_path); reconstructing a file's full lineage across renames
    is bookkeeping we own. This follows the common case and flags the edges.
    """

    def mine(self, repo_path: str, rev: str = "HEAD") -> HistoryResult:
        alias: dict[str, str] = {}            # historical path -> successor (one hop)
        files: dict[str, FileHistory] = {}    # canonical path -> history
        timeline: list[CommitRecord] = []
        head_sha = ""
        as_of: datetime | None = None

        def resolve(p: str) -> str:
            seen: set[str] = set()            # cycle guard, should never fire
            while p in alias and p not in seen:
                seen.add(p)
                p = alias[p]
            return p

        # TODO(rev): honor `rev` via to_commit=; default traverses the active
        # branch tip in chronological (oldest-first) order, so idx == build order.
        for idx, commit in enumerate(Repository(repo_path).traverse_commits()):
            head_sha = commit.hash
            # AUDIT: as_of is the tip's author_date. After a rebase the tip may
            # not hold the max date; max(committer_date) might be truer. It shifts
            # every age/last_touched uniformly, so it matters for absolute days.
            as_of = commit.author_date
            subject = (commit.msg or "").splitlines()[0] if commit.msg else ""
            ctype, rule = classify_commit(subject, commit.merge)
            # AUDIT: author identity = email, no mailmap. One human with several
            # emails inflates author_count, which is the bus-factor signal.
            author = commit.author.email or commit.author.name or "unknown"

            touched: list[str] = []
            c_added = c_deleted = 0

            for mf in commit.modified_files:
                raw_path = mf.new_path or mf.old_path
                if raw_path is None:
                    continue

                # A new file ADDed at a name previously renamed away is a DISTINCT
                # file. Break the stale alias so it isn't merged into the old one.
                # AUDIT: heuristic — verify against real path-reuse in history.
                if mf.change_type == ModificationType.ADD and raw_path in alias:
                    del alias[raw_path]

                if mf.change_type == ModificationType.RENAME and mf.old_path:
                    oc, nc = resolve(mf.old_path), mf.new_path
                    if nc and oc != nc:
                        alias[oc] = nc
                        if oc in files:        # migrate accumulated history
                            moved = files.pop(oc)
                            moved.path = nc
                            files[nc] = moved

                canon = resolve(raw_path)
                added = mf.added_lines or 0
                deleted = mf.deleted_lines or 0
                touched.append(canon)

                # AUDIT: merge commits re-touch files; we skip their churn to
                # avoid double-counting, but that also drops genuine conflict-
                # resolution work. Confirm that's the desired truth.
                if commit.merge:
                    continue

                fh = files.get(canon)
                if fh is None:
                    fh = FileHistory(
                        path=canon, introduced_idx=idx,
                        first_seen=commit.author_date, last_seen=commit.author_date,
                    )
                    files[canon] = fh

                fh.commit_count += 1
                fh.churn_added += added
                fh.churn_deleted += deleted
                fh.last_seen = commit.author_date
                fh.authors.add(author)
                if ctype in ("fix", "revert"):
                    fh.fix_count += 1
                if ctype == "revert":
                    fh.revert_count += 1

                c_added += added
                c_deleted += deleted

            timeline.append(CommitRecord(
                sha=commit.hash, ts=commit.author_date, author=author,
                subject=subject, type=ctype, matched_rule=rule,
                nodes_touched=touched, added=c_added, deleted=c_deleted,
                is_merge=commit.merge,
            ))

        if as_of is None:
            raise ValueError(f"no commits found in {repo_path!r}")
        return HistoryResult(head_sha, as_of, files, timeline)


# --- smoke harness (the precursor to the §9 report) --------------------------

if __name__ == "__main__":
    import sys
    from collections import Counter

    path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = PydrillerHistoryMiner().mine(path)

    print(f"head={result.head_sha[:10]}  as_of={result.as_of.date()}  "
          f"files={len(result.files)}  commits={len(result.timeline)}")
    print("commit types:", dict(Counter(c.type for c in result.timeline)))

    print("\ntop churn:")
    top = sorted(result.files.values(), key=lambda f: f.churn_lines, reverse=True)
    for f in top[:10]:
        m = f.raw_metrics(result.as_of)
        print(f"  {f.path:48.48}  churn={m['churn_lines']:6d}  "
              f"commits={m['commit_count']:3d}  fix={m['fix_count']:3d}  "
              f"age={m['age_days']:4d}d  last={m['last_touched_days']:4d}d  "
              f"authors={m['author_count']:2d}")
