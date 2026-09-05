"""The temporal-holdout protocol (validation-spec §3) for the two predictive indices.

Per repo: split the (ts, sha)-ordered timeline at 80% of commits, extract the
substrate truncated at the split, label eligible files by whether a fix/revert
commit touched them in the holdout window, and score each predictive index
against the stronger of the recency and busyness baselines.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config import PREDICTIVE_SIGNALS, ValidationConfig
from .stats import average_precision, base_rate, precision_recall_at_k, roc_auc
from .substrates import SubstrateCache, canonical_resolver

FIX_TYPES = {"fix", "revert"}


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
    full = cache.get(repo, "HEAD")
    timeline = full["timeline"]
    n = len(timeline)
    split_idx = int(math.floor(n * (1.0 - vcfg.holdout_frac)))
    split_sha = timeline[split_idx - 1]["sha"]
    holdout = timeline[split_idx:]
    train = cache.get(repo, split_sha, truncate=True)
    canon = canonical_resolver(full)
    head_nodes = {nd["id"] for nd in full["nodes"]}
    train_by_id = {nd["id"]: nd for nd in train["nodes"]}

    # §3.3 eligible: introduced before the split (a train node with indices) and alive at HEAD.
    eligible: dict[str, str] = {}  # train id -> head id
    for tid, nd in train_by_id.items():
        if (nd.get("derived") or {}).get("indices") is None:
            continue
        if not vcfg.holdout_include_tests and nd["metrics"].get("is_test"):
            continue
        hid = canon(tid)
        if hid in head_nodes:
            eligible[tid] = hid

    # §3.4 labels
    positives: set[str] = set()
    n_fix_commits = 0
    for c in holdout:
        if c["type"] in FIX_TYPES:
            n_fix_commits += 1
            for p in c["nodes_touched"]:
                positives.add(canon(p))
    ids = sorted(eligible)
    labels = [1 if eligible[t] in positives else 0 for t in ids]
    n_pos = sum(labels)
    coverage = len(ids) / len(head_nodes) if head_nodes else 0.0
    br = base_rate(labels) if ids else float("nan")

    rh = RepoHoldout(
        name=full["repo"]["name"], head_sha=full["repo"]["head_sha"], split_sha=split_sha,
        n_commits=n, n_holdout_commits=len(holdout), n_head_nodes=len(head_nodes),
        n_eligible=len(ids), n_positives=n_pos, coverage=coverage, base_rate=br,
        fix_label_rate=(n_fix_commits / len(holdout)) if holdout else 0.0,
    )
    if n_pos == 0:
        rh.degenerate = "no_holdout_positives"
        return rh
    if coverage < vcfg.coverage_min:
        rh.degenerate = "insufficient_coverage"
        return rh

    ks = sorted({10, 20, max(1, math.ceil(0.05 * len(ids)))})
    recency = [1.0 - (train_by_id[t]["derived"]["percentiles"].get("last_touched_days") or 0.0) for t in ids]
    busyness = [float(train_by_id[t]["metrics"].get("commit_count") or 0) for t in ids]
    rh.baselines = {"recency": _metrics(recency, labels, ids, ks), "busyness": _metrics(busyness, labels, ids, ks)}
    best = max(rh.baselines, key=lambda b: (rh.baselines[b]["roc_auc"], rh.baselines[b]["pr_auc"]))
    rh.best_baseline = best
    best_m = rh.baselines[best]
    # §3.7 clause 4 — the label-noise floor
    if best_m["pr_auc"] < vcfg.signal_floor_mult * br:
        rh.degenerate = "insufficient_signal"

    for sig in PREDICTIVE_SIGNALS:
        scores = [float(train_by_id[t]["derived"]["indices"].get(sig) or 0.0) for t in ids]
        m = _metrics(scores, labels, ids, ks)
        failed = []
        if not (m["roc_auc"] >= best_m["roc_auc"] + vcfg.auc_margin):
            failed.append("roc_margin")
        if not (m["pr_auc"] >= vcfg.pr_auc_mult * best_m["pr_auc"]):
            failed.append("pr_auc_mult")
        m["passed"] = (not failed) and rh.degenerate is None
        m["failed_clauses"] = failed
        m["best_baseline"] = best
        rh.signals[sig] = m
    return rh
