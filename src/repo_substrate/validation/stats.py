"""Statistics for the validation gate (validation-spec §3.6, §2.4.2, §3A.5).

Everything here is deterministic: bootstrap and permutation draws come from a
seeded generator whose seed is part of the validation config and therefore of
the fingerprint. Ties are broken by node id where a ranking needs a total order.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from scipy import stats


def kendall_tau_b(x: Sequence[float], y: Sequence[float]) -> float:
    """Tie-corrected Kendall τ-b (scipy default). NaN when either side is constant."""
    if len(x) < 2:
        return float("nan")
    t = stats.kendalltau(np.asarray(x, dtype=float), np.asarray(y, dtype=float), variant="b").statistic
    return float(t)


def bootstrap_ci(
    x: Sequence[float], y: Sequence[float], stat, n: int, seed: int, alpha: float = 0.05
) -> tuple[float, float]:
    """Percentile bootstrap over files (resample indices with replacement)."""
    xa = np.asarray(x, dtype=float)
    ya = np.asarray(y, dtype=float)
    rng = np.random.default_rng(seed)
    m = len(xa)
    if m < 3:
        return float("nan"), float("nan")
    vals = np.empty(n)
    for i in range(n):
        idx = rng.integers(0, m, m)
        vals[i] = stat(xa[idx], ya[idx])
    vals = vals[~np.isnan(vals)]
    if len(vals) == 0:
        return float("nan"), float("nan")
    return float(np.quantile(vals, alpha / 2)), float(np.quantile(vals, 1 - alpha / 2))


def permutation_p(x: Sequence[float], y: Sequence[float], stat, n: int, seed: int) -> float:
    """Two-sided p-value of |stat| against a label-permutation null."""
    xa = np.asarray(x, dtype=float)
    ya = np.asarray(y, dtype=float)
    rng = np.random.default_rng(seed)
    observed = abs(stat(xa, ya))
    if np.isnan(observed):
        return float("nan")
    count = 0
    for _ in range(n):
        s = stat(xa, rng.permutation(ya))
        if not np.isnan(s) and abs(s) >= observed:
            count += 1
    return (count + 1) / (n + 1)


def roc_auc(scores: Sequence[float], labels: Sequence[int]) -> float:
    """Mann–Whitney AUC with average ranks for ties. NaN if a class is empty."""
    s = np.asarray(scores, dtype=float)
    y = np.asarray(labels, dtype=int)
    n_pos = int(y.sum())
    n_neg = len(y) - n_pos
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    ranks = stats.rankdata(s, method="average")
    return float((ranks[y == 1].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def average_precision(scores: Sequence[float], labels: Sequence[int]) -> float:
    """PR-AUC as average precision over the ranked list, ties grouped (a tied block
    contributes at the block's end so ordering inside a tie cannot inflate it)."""
    s = np.asarray(scores, dtype=float)
    y = np.asarray(labels, dtype=int)
    n_pos = int(y.sum())
    if n_pos == 0:
        return float("nan")
    order = np.argsort(-s, kind="stable")
    s, y = s[order], y[order]
    tp = 0
    seen = 0
    ap = 0.0
    i = 0
    n = len(s)
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        block_pos = int(y[i:j].sum())
        tp += block_pos
        seen = j
        if block_pos:
            ap += (tp / seen) * block_pos
        i = j
    return float(ap / n_pos)


def precision_recall_at_k(
    scores: Sequence[float], labels: Sequence[int], ids: Sequence[str], k: int
) -> tuple[float, float]:
    """Top-k by score desc, ties broken by id asc (a total order, so deterministic)."""
    order = sorted(range(len(scores)), key=lambda i: (-scores[i], ids[i]))
    top = order[:k]
    tp = sum(labels[i] for i in top)
    n_pos = sum(labels)
    return (tp / k if k else float("nan")), (tp / n_pos if n_pos else float("nan"))


def base_rate(labels: Sequence[int]) -> float:
    return (sum(labels) / len(labels)) if labels else float("nan")
