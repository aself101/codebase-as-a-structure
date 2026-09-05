"""The temporal-holdout protocol (validation-spec §3) for the two predictive indices.

Per repo: split the (ts, sha)-ordered timeline at 80% of commits, extract the
substrate truncated at the split, label eligible files by whether a fix/revert
commit touched them in the holdout window, and score each predictive index
against the stronger of the recency and busyness baselines.

``split_and_eligible`` is the single owner of §3.1–§3.4 so the tuning module
(tune.py) and the gate cannot drift apart on the split or the eligibility rule.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..history import classify_commit
from .config import PREDICTIVE_SIGNALS, ValidationConfig
from .stats import average_precision, base_rate, kendall_tau_b, precision_recall_at_k, roc_auc
from .substrates import SubstrateCache, canonical_resolver

FIX_TYPES = {"fix", "revert"}


@dataclass
class SplitContext:
    """Everything §3.1–§3.4 determines for one repo, before any index is scored."""

    name: str
    head_sha: str
    split_sha: str
    n_commits: int
    n_holdout_commits: int
    n_head_nodes: int
    ids: list[str]              # eligible train-node ids, sorted
    labels: list[int]           # §3.4 label per id
    nodes: list[dict[str, Any]]  # the train nodes, aligned with ids
    fix_label_rate: float
    graph_degraded: bool
    recency: list[float] = field(default_factory=list)
    busyness: list[float] = field(default_factory=list)

    @property
    def coverage(self) -> float:
        return len(self.ids) / self.n_head_nodes if self.n_head_nodes else 0.0

    @property
    def n_positives(self) -> int:
        return sum(self.labels)


def label_type(commit: dict[str, Any], label_regex: re.Pattern[str]) -> str:
    """§3.4 label classification, re-derived from the commit SUBJECT with the validation
    config's frozen regex (circumvention A9) — not read from the substrate's `type`, which
    the feature-side fix_subject_regex produced."""
    t, _ = classify_commit(commit["subject"], bool(commit.get("is_merge")) or commit["type"] == "merge", label_regex)
    return t


def split_and_eligible(repo: Path, cache: SubstrateCache, vcfg: ValidationConfig) -> SplitContext:
    full = cache.get(repo, "HEAD")
    timeline = full["timeline"]
    n = len(timeline)
    split_idx = math.floor(n * (1.0 - vcfg.holdout_frac))
    # Guard against negative-index wraparound (audit 2026-09-04): with n·(1−frac) < 1 the
    # split would silently become HEAD and the whole timeline the holdout.
    if split_idx < 1 or split_idx >= n:
        raise ValueError(f"{full['repo']['name']}: {n} commits is too few to split at holdout_frac={vcfg.holdout_frac}")
    split_sha = timeline[split_idx - 1]["sha"]
    holdout = timeline[split_idx:]
    train = cache.get(repo, split_sha, truncate=True)
    canon = canonical_resolver(full)
    head_nodes = {nd["id"] for nd in full["nodes"]}

    # §3.4 labels, from the frozen label regex
    label_regex = re.compile(vcfg.label_subject_regex, re.IGNORECASE)
    positives: set[str] = set()
    n_fix_commits = 0
    for c in holdout:
        if label_type(c, label_regex) in FIX_TYPES:
            n_fix_commits += 1
            for p in c["nodes_touched"]:
                positives.add(canon(p))

    # §3.3 eligible: introduced before the split (a train node with indices) and alive at HEAD.
    ids, labels, nodes = [], [], []
    for nd in sorted(train["nodes"], key=lambda x: x["id"]):
        if (nd.get("derived") or {}).get("indices") is None:
            continue
        if not vcfg.holdout_include_tests and nd["metrics"].get("is_test"):
            continue
        hid = canon(nd["id"])
        if hid not in head_nodes:
            continue
        ids.append(nd["id"])
        labels.append(1 if hid in positives else 0)
        nodes.append(nd)
    ctx = SplitContext(
        name=full["repo"]["name"], head_sha=full["repo"]["head_sha"], split_sha=split_sha,
        n_commits=n, n_holdout_commits=len(holdout), n_head_nodes=len(head_nodes),
        ids=ids, labels=labels, nodes=nodes,
        fix_label_rate=(n_fix_commits / len(holdout)) if holdout else 0.0,
        graph_degraded=bool(train["summary"]["graph_degraded"]),
    )
    ctx.recency = [1.0 - (nd["derived"]["percentiles"].get("last_touched_days") or 0.0) for nd in nodes]
    ctx.busyness = [float(nd["metrics"].get("commit_count") or 0) for nd in nodes]
    return ctx


@dataclass
class RepoHoldout:
    name: str
    head_sha: str
    split_sha: str
    n_commits: int
    n_holdout_commits: int
    n_head_nodes: int
    n_eligible: int
    n_positives: int
    coverage: float
    base_rate: float
    fix_label_rate: float  # share of holdout commits labeled fix/revert (label fidelity, §8 Q3)
    degenerate: str | None = None  # no_holdout_positives | insufficient_coverage | insufficient_signal
    baselines: dict[str, dict[str, float]] = field(default_factory=dict)
    signals: dict[str, dict[str, Any]] = field(default_factory=dict)
    best_baseline: str | None = None


def _metrics(scores: list[float], labels: list[int], ids: list[str], ks: list[int]) -> dict[str, Any]:
    return {
        "roc_auc": roc_auc(scores, labels),
        "pr_auc": average_precision(scores, labels),
        "precision_at_k": {str(k): precision_recall_at_k(scores, labels, ids, k)[0] for k in ks},
        "recall_at_k": {str(k): precision_recall_at_k(scores, labels, ids, k)[1] for k in ks},
    }


def run_holdout(repo: Path, cache: SubstrateCache, vcfg: ValidationConfig) -> RepoHoldout:
    ctx = split_and_eligible(repo, cache, vcfg)
    ids, labels = ctx.ids, ctx.labels
    n_pos = ctx.n_positives
    br = base_rate(labels) if ids else float("nan")
    rh = RepoHoldout(
        name=ctx.name, head_sha=ctx.head_sha, split_sha=ctx.split_sha,
        n_commits=ctx.n_commits, n_holdout_commits=ctx.n_holdout_commits, n_head_nodes=ctx.n_head_nodes,
        n_eligible=len(ids), n_positives=n_pos, coverage=ctx.coverage, base_rate=br,
        fix_label_rate=ctx.fix_label_rate,
    )
    if not ids:
        rh.degenerate = "population_too_small"  # §4 first case: a sub-N_min repo has no indices, hence no eligible set
        return rh
    if n_pos == 0:
        rh.degenerate = "no_holdout_positives"
        return rh
    if n_pos == len(ids):
        rh.degenerate = "no_holdout_negatives"  # AUC undefined with one class (audit: NaN was a false FAIL)
        return rh
    if ctx.coverage < vcfg.coverage_min:
        rh.degenerate = "insufficient_coverage"
        return rh

    ks = sorted({10, 20, max(1, math.ceil(0.05 * len(ids)))})
    rh.baselines = {"recency": _metrics(ctx.recency, labels, ids, ks), "busyness": _metrics(ctx.busyness, labels, ids, ks)}
    best = max(rh.baselines, key=lambda b: (rh.baselines[b]["roc_auc"], rh.baselines[b]["pr_auc"]))
    rh.best_baseline = best
    best_m = rh.baselines[best]
    best_scores = ctx.recency if best == "recency" else ctx.busyness
    # §3.7 clause 4 — the label-noise floor
    if best_m["pr_auc"] < vcfg.signal_floor_mult * br:
        rh.degenerate = "insufficient_signal"

    for sig in PREDICTIVE_SIGNALS:
        raw_scores = [nd["derived"]["indices"].get(sig) for nd in ctx.nodes]
        if any(s is None for s in raw_scores):
            # A degraded/absent index is unmeasurable on this repo, not a score of zero (audit).
            rh.signals[sig] = {"passed": False, "failed_clauses": ["index_unavailable"], "best_baseline": best,
                               "roc_auc": float("nan"), "pr_auc": float("nan"), "precision_at_k": {}, "recall_at_k": {},
                               "tau_vs_best_baseline": float("nan"), "unavailable": True}
            continue
        scores = [float(s) for s in raw_scores]
        m = _metrics(scores, labels, ids, ks)
        failed = []
        if math.isnan(m["roc_auc"]) or not (m["roc_auc"] >= best_m["roc_auc"] + vcfg.auc_margin):
            failed.append("roc_margin")
        if math.isnan(m["pr_auc"]) or not (m["pr_auc"] >= vcfg.pr_auc_mult * best_m["pr_auc"]):
            failed.append("pr_auc_mult")
        m["passed"] = (not failed) and rh.degenerate is None
        m["unavailable"] = False
        m["failed_clauses"] = failed
        m["best_baseline"] = best
        # D-011 (Popper C-7B): how much of the index *is* the baseline it must beat.
        m["tau_vs_best_baseline"] = kendall_tau_b(scores, best_scores)
        rh.signals[sig] = m
    return rh
