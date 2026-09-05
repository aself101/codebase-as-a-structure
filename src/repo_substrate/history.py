"""History mining (repo-substrate-spec §5, §7): per-file history metrics, the
classified timeline, co-change degree, and blame age.

Emits ONLY history-derived signals. Deliberately does not compute size_loc,
fan_in/fan_out/centrality, or is_test/has_sibling_test — those belong to the
inventory and the dependency extractor. Holding that boundary is what keeps
the substrate's components swappable and the determinism contract auditable.

pydriller is hidden behind the ``HistoryMiner`` protocol so a faster miner
can replace it without anything downstream noticing.

Audit notes carried from the prototype (on the page, not silently resolved):
- Classification is subject-only. A squashed commit gets one label; commit-body
  signals (BREAKING CHANGE, trailers) are ignored. The validation label inherits this.
- Author identity is the email with no mailmap; one human with several emails
  inflates author_count.
- Merge commits re-touch files; their churn is skipped to avoid double counting,
  which also drops genuine conflict-resolution work.
- ``as_of`` is the maximum author_date over the mined timeline (the last commit in
  (ts, sha) order), never wall-clock, so re-running tomorrow moves no value and
  age_days stays non-negative under clock skew or rebase.
"""

from __future__ import annotations

import re
import subprocess
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
from itertools import combinations
from pathlib import Path
from statistics import median
from typing import Protocol

from pydriller import ModificationType, Repository

# --- §7 commit-type classification --------------------------------------------

_CONVENTIONAL = re.compile(r"^(feat|fix|refactor|docs|test|chore|revert)\b", re.IGNORECASE)
_NATIVE_REVERT = re.compile(r'^revert[\s:"]', re.IGNORECASE)


def classify_commit(subject: str, is_merge: bool, fix_fallback: re.Pattern[str]) -> tuple[str, str]:
    """Deterministic first-match cascade (§7). Returns (type, matched_rule).

    Stage 2 (native revert) is dead by construction: stage 1's ``revert\\b`` already
    matches every subject it could. Kept so the cascade reads as the spec does;
    §7's open item decides whether to drop it or tighten stage 1. Changing stage 1
    moves validation labels and must be decided against the holdout.
    """
    s = subject.strip()
    m = _CONVENTIONAL.match(s)
    if m:
        return m.group(1).lower(), "conventional-prefix"
    if _NATIVE_REVERT.match(s):
        return "revert", "native-revert-subject"
    if is_merge:
        return "merge", "merge-parents"
    if fix_fallback.search(s):
        return "fix", "subject-regex"
    return "other", "default"


# --- result types --------------------------------------------------------------


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


def _days(as_of: datetime, t: datetime) -> float:
    """Fractional days from ``t`` to ``as_of``, floored at zero (clock skew, rebase) and
    rounded to a millisecond of a day so the JSON is stable across platforms."""
    return round(max(0.0, (as_of - t).total_seconds() / 86400.0), 5)


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
    fix_count: int = 0  # type in {fix, revert}  (§5)
    revert_count: int = 0
    authors: set[str] = field(default_factory=set, repr=False)
    commit_idxs: list[int] = field(default_factory=list, repr=False)

    @property
    def churn_lines(self) -> int:
        return self.churn_added + self.churn_deleted

    def raw_metrics(self, as_of: datetime) -> dict[str, int | float]:
        """Day counts relative to ``as_of`` (the tip), never wall-clock. Age and recency are
        **fractional** days (D-022): with integer truncation two files born hours apart tie
        or untie depending on where the reference clock falls, and under average-rank
        percentiles a whole birth cohort's rank then jumps when the clock crosses a day
        boundary — movement with no edit behind it. Fractional days tie only files with the
        same author_date (born in one commit), and those never untie."""
        return {
            "commit_count": self.commit_count,
            "churn_lines": self.churn_lines,
            "fix_count": self.fix_count,
            "revert_count": self.revert_count,
            "author_count": len(self.authors),
            "age_days": _days(as_of, self.first_seen),
            "last_touched_days": _days(as_of, self.last_seen),
            "introduced_idx": self.introduced_idx,
        }


@dataclass
class HistoryResult:
    head_sha: str
    as_of: datetime
    files: dict[str, FileHistory]
    timeline: list[CommitRecord]
    renames: dict[str, str] = field(default_factory=dict)  # historical path -> successor (one hop)

    def canonical(self, path: str) -> str:
        """Resolve a historical path to its name at the analyzed rev (follows the chain)."""
        seen: set[str] = set()
        while path in self.renames and path not in seen:
            seen.add(path)
            path = self.renames[path]
        return path


class HistoryMiner(Protocol):
    def mine(self, repo_path: Path, rev: str, fix_fallback: re.Pattern[str]) -> HistoryResult:
        """Mine every commit reachable from ``rev``, oldest first, and accumulate
        per-file history under rename-followed canonical paths."""
        ...


# --- pydriller implementation --------------------------------------------------


class PydrillerHistoryMiner:
    """Rename-following is the fiddly part: pydriller reports renames per commit
    (old_path -> new_path); reconstructing a file's lineage across renames is
    bookkeeping we own. This follows the common case and flags the edges."""

    def mine(self, repo_path: Path, rev: str, fix_fallback: re.Pattern[str]) -> HistoryResult:
        alias: dict[str, str] = {}  # historical path -> successor (one hop)
        files: dict[str, FileHistory] = {}
        raw: list[tuple[datetime, str, CommitRecord, list[tuple[str, int, int]]]] = []

        def resolve(p: str) -> str:
            seen: set[str] = set()
            while p in alias and p not in seen:
                seen.add(p)
                p = alias[p]
            return p

        # to_commit bounds the traversal at ``rev`` (the --truncate-at seam, §8).
        # pydriller's DEFAULT order is oldest-first (it passes reverse=True to git);
        # its order="reverse" option is newest-first — the name is inverted relative to
        # git's flag. Rename-following must run in causal order, so the default is required.
        # The timeline is re-sorted by (ts, sha) below so output ordering is stable regardless.
        repo = Repository(str(repo_path), to_commit=rev)
        for commit in repo.traverse_commits():
            subject = (commit.msg or "").splitlines()[0] if commit.msg else ""
            ctype, rule = classify_commit(subject, commit.merge, fix_fallback)
            author = commit.author.email or commit.author.name or "unknown"
            touched: list[tuple[str, int, int]] = []
            for mf in commit.modified_files:
                raw_path = mf.new_path or mf.old_path
                if raw_path is None:
                    continue
                # A file ADDed at a name previously renamed away is a distinct file:
                # break the stale alias. Covered by tests/test_golden.py path-reuse cases.
                if mf.change_type == ModificationType.ADD and raw_path in alias:
                    del alias[raw_path]
                if mf.change_type == ModificationType.RENAME and mf.old_path:
                    oc, nc = resolve(mf.old_path), mf.new_path
                    if nc and oc != nc:
                        # The rename TARGET may itself be a stale alias key (a name that was
                        # renamed away earlier and is now being reused by a different file).
                        # Break it, or the old lineage captures the new file — reproduced by the
                        # 2026-09-04 code audit: x→y, then z→x, then a fix to the new x landed on y.
                        alias.pop(nc, None)
                        alias[oc] = nc
                        if oc in files:
                            moved = files.pop(oc)
                            moved.path = nc
                            # A FileHistory already at `nc` belongs to a lineage deleted before this
                            # commit (git cannot rename onto a live path). It is not at the analyzed
                            # rev, so the assembler would drop it anyway; it is discarded here.
                            files[nc] = moved
                touched.append((resolve(raw_path), mf.added_lines or 0, mf.deleted_lines or 0))
            rec = CommitRecord(
                sha=commit.hash,
                ts=commit.author_date,
                author=author,
                subject=subject,
                type=ctype,
                matched_rule=rule,
                nodes_touched=[t[0] for t in touched],
                added=sum(t[1] for t in touched),
                deleted=sum(t[2] for t in touched),
                is_merge=commit.merge,
            )
            raw.append((commit.author_date, commit.hash, rec, touched))
            # Accumulate in traversal order so rename aliases apply in causal order;
            # introduced_idx is assigned after the (ts, sha) sort below.
            if commit.merge:
                continue
            for canon, added, deleted in touched:
                fh = files.get(canon)
                if fh is None:
                    fh = FileHistory(
                        path=canon,
                        introduced_idx=-1,
                        first_seen=commit.author_date,
                        last_seen=commit.author_date,
                    )
                    files[canon] = fh
                fh.commit_count += 1
                fh.churn_added += added
                fh.churn_deleted += deleted
                fh.first_seen = min(fh.first_seen, commit.author_date)
                fh.last_seen = max(fh.last_seen, commit.author_date)
                fh.authors.add(author)
                if ctype in ("fix", "revert"):
                    fh.fix_count += 1
                if ctype == "revert":
                    fh.revert_count += 1
                fh.commit_idxs.append(len(raw) - 1)  # provisional index, remapped below

        if not raw:
            raise ValueError(f"no commits reachable from {rev!r} in {repo_path}")

        # §3 stable ordering: timeline by (timestamp, sha); indices follow that order.
        order = sorted(range(len(raw)), key=lambda i: (raw[i][0], raw[i][1]))
        remap = {old: new for new, old in enumerate(order)}
        timeline = [raw[i][2] for i in order]
        for fh in files.values():
            fh.commit_idxs = sorted(remap[i] for i in fh.commit_idxs)
            fh.introduced_idx = fh.commit_idxs[0] if fh.commit_idxs else -1

        # Files whose only touches were merge commits have no FileHistory; they are
        # orphans if they exist at HEAD (§5) and are reported as such by the assembler.
        tip_sha = raw[order[-1]][1]
        as_of = raw[order[-1]][0]
        return HistoryResult(tip_sha, as_of, files, timeline, dict(alias))


# --- §5 cochange_degree ----------------------------------------------------------


def cochange_degree(
    timeline: list[CommitRecord], cochange_min: int, max_files: int
) -> dict[str, int]:
    """Distinct other files co-occurring with each file in ≥ cochange_min non-merge
    commits touching ≤ max_files files. Reads only nodes_touched — no edges, no timestamps —
    which is what makes it a valid cross-modal counterpart for import topology (validation §2.4.2)."""
    pair_counts: Counter[tuple[str, str]] = Counter()
    for c in timeline:
        if c.is_merge:
            continue
        touched = sorted(set(c.nodes_touched))
        if len(touched) < 2 or len(touched) > max_files:
            continue
        for a, b in combinations(touched, 2):
            pair_counts[(a, b)] += 1
    partners: dict[str, set[str]] = defaultdict(set)
    for (a, b), n in pair_counts.items():
        if n >= cochange_min:
            partners[a].add(b)
            partners[b].add(a)
    return {p: len(s) for p, s in partners.items()}


# --- §5 blame_age_median ---------------------------------------------------------

_AUTHOR_TIME = re.compile(rb"^author-time (\d+)$", re.MULTILINE)


class BlameFailure(RuntimeError):
    """git blame failed for a path: the instrument is broken, which is not the same as
    'no blame data' (an empty file). Carried as a value so the thread pool can finish."""


def _blame_one(
    repo: Path, rev: str, path: str, as_of_epoch: int, timeout: int = 300
) -> tuple[str, float | None | BlameFailure]:
    # -w: whitespace-insensitive. No -M/-C: cheaper, deterministic, and the metric is
    # "age of surviving text in this file", which is what we want (§5).
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), "blame", "-w", "--line-porcelain", rev, "--", path],
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return path, BlameFailure(f"git blame timed out after {timeout}s: {path}")
    if proc.returncode != 0:
        return path, BlameFailure(
            f"git blame exit {proc.returncode}: {path}: {proc.stderr.decode('utf-8', 'replace')[-200:]}"
        )
    out = proc.stdout
    # --line-porcelain repeats the header per line; the content line follows a tab.
    # Non-blank filter: pair each author-time with its content line.
    ages: list[float] = []
    lines = out.split(b"\n")
    current_time: int | None = None
    for ln in lines:
        if ln.startswith(b"author-time "):
            try:
                current_time = int(ln[12:])
            except ValueError:
                return path, BlameFailure(
                    f"unparseable author-time in blame porcelain: {path}: {ln[:40]!r}"
                )
        elif ln.startswith(b"\t"):
            if current_time is not None and ln[1:].strip():
                ages.append((as_of_epoch - current_time) / 86400.0)
            current_time = None
    if not ages:
        return path, None
    return path, float(median(ages))


def blame_age_median(
    repo: Path, rev: str, paths: list[str], as_of: datetime, workers: int = 8
) -> tuple[dict[str, float | None], list[str]]:
    """Returns (path -> median age or None for an empty file, [paths where blame FAILED]).
    Failures are reported separately so the assembler can count them; a broken instrument
    must not read as an absent measurement (2026-09-04 audit)."""
    as_of_epoch = int(as_of.timestamp())
    with ThreadPoolExecutor(max_workers=workers) as ex:
        results = list(ex.map(lambda p: _blame_one(repo, rev, p, as_of_epoch), paths))
    ages: dict[str, float | None] = {}
    failed: list[str] = []
    for p, v in results:
        if isinstance(v, BlameFailure):
            failed.append(p)
            ages[p] = None
        else:
            ages[p] = v
    return ages, sorted(failed)
