"""Pre-registered weight tuning (DECISIONS.md D-009).

Tune the two predictive indices' weights on the tuning repos only, by a fixed
grid, with a fixed objective, and freeze the result to a TOML file. The test
repos are never read here. Indices are recomputed from the cached training
substrates' percentiles, so tuning needs no re-extraction. The split and the
eligibility rule come from ``holdout.split_and_eligible`` — one owner.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import replace
from pathlib import Path
from typing import Any

from ..config import ALLOWED_INPUTS, SubstrateConfig
from ..derived import compute_indices
from .config import ValidationConfig
from .holdout import SplitContext, split_and_eligible
from .stats import average_precision, roc_auc
from .substrates import SubstrateCache

GRID_STEP = 0.1


def compositions(keys: list[str], step: float) -> list[dict[str, float]]:
    """All weight vectors over `keys` with entries in {0, step, 2·step, …} summing to 1."""
    n = len(keys)
    units = round(1.0 / step)
    out = []
    for cuts in itertools.combinations(range(units + n - 1), n - 1):
        parts = []
        prev = -1
        for c in cuts + (units + n - 1,):
            parts.append(c - prev - 1)
            prev = c
        out.append({k: round(p * step, 6) for k, p in zip(keys, parts, strict=True)})
    return out


def _baselines(ctx: SplitContext) -> tuple[float, float]:
    best_roc = max(roc_auc(ctx.recency, ctx.labels), roc_auc(ctx.busyness, ctx.labels))
    best_pr = max(
        average_precision(ctx.recency, ctx.labels), average_precision(ctx.busyness, ctx.labels)
    )
    return best_roc, best_pr


def _score(
    ctx: SplitContext,
    best: tuple[float, float],
    index: str,
    weights: dict[str, float],
    cfg: SubstrateConfig,
) -> tuple[float, float]:
    w = replace(cfg.weights, **{index: weights})
    c = replace(cfg, weights=w)
    scores = []
    for nd in ctx.nodes:
        m = nd["metrics"]
        idx = compute_indices(
            nd["derived"]["percentiles"],
            m,
            m.get("test_fan_in") or 0,
            m.get("recent_commit_share"),
            ctx.graph_degraded,
            c,
        )
        v = idx[index]
        if v is None:
            return float("nan"), float(
                "nan"
            )  # unmeasurable under these weights; sorts last (see tune())
        scores.append(float(v))
    return roc_auc(scores, ctx.labels) - best[0], average_precision(scores, ctx.labels) / best[1]


def _sort_key(
    row: tuple[tuple[float, float], dict[str, float], list[tuple[float, float]]],
) -> tuple[float, float]:
    """Descending objective; NaN objectives sort strictly last (a NaN key would otherwise
    leave Python's sort in input order)."""
    d, r = row[0]
    return (-d if not math.isnan(d) else float("inf"), -r if not math.isnan(r) else float("inf"))


def tune(
    tuning_repos: list[Path],
    cache: SubstrateCache,
    vcfg: ValidationConfig,
    cfg: SubstrateConfig,
    indices: tuple[str, ...] = ("bug_pressure_index", "change_pressure_index"),
) -> dict[str, Any]:
    ctxs = [split_and_eligible(r, cache, vcfg) for r in tuning_repos]
    # Degeneracy guards (audit: a NaN objective silently froze grid point #1 as the result).
    for c in ctxs:
        if not c.ids or c.n_positives == 0 or c.n_positives == len(c.ids):
            raise ValueError(
                f"{c.name}: degenerate tuning repo (eligible={len(c.ids)}, positives={c.n_positives}); refusing to tune"
            )
    bests = [_baselines(c) for c in ctxs]
    for c, (r, p) in zip(ctxs, bests, strict=True):
        if math.isnan(r) or math.isnan(p) or p == 0.0:
            raise ValueError(f"{c.name}: baseline undefined (roc={r}, pr={p}); refusing to tune")
    result: dict[str, Any] = {
        "tuning_repos": [c.name for c in ctxs],
        "grid_step": GRID_STEP,
        "objective": "min over tuning repos of (ROC-AUC − best baseline ROC-AUC); tie: min PR-AUC ratio",
        "indices": {},
    }
    for index in indices:
        keys = sorted(ALLOWED_INPUTS[index])
        grid = compositions(keys, GRID_STEP)
        rows = []
        for wts in grid:
            per = [_score(c, b, index, wts, cfg) for c, b in zip(ctxs, bests, strict=True)]
            obj = (min(d for d, _ in per), min(r for _, r in per))
            rows.append((obj, wts, per))
        rows.sort(key=_sort_key)
        best_obj, best_w, best_per = rows[0]
        if math.isnan(best_obj[0]):
            raise ValueError(
                f"{index}: every grid point was unmeasurable; refusing to freeze weights"
            )
        baseline_w = getattr(cfg.weights, index)
        base_per = [_score(c, b, index, baseline_w, cfg) for c, b in zip(ctxs, bests, strict=True)]
        result["indices"][index] = {
            "inputs": keys,
            "grid_size": len(grid),
            "chosen": {k: v for k, v in best_w.items() if v > 0},
            "chosen_objective": {"min_delta_roc": best_obj[0], "min_pr_ratio": best_obj[1]},
            "chosen_per_repo": [
                {"name": c.name, "delta_roc": d, "pr_ratio": r}
                for c, (d, r) in zip(ctxs, best_per, strict=True)
            ],
            "spec_placeholder": dict(baseline_w),
            "spec_placeholder_per_repo": [
                {"name": c.name, "delta_roc": d, "pr_ratio": r}
                for c, (d, r) in zip(ctxs, base_per, strict=True)
            ],
            "top10": [
                {
                    "weights": {k: v for k, v in w.items() if v > 0},
                    "min_delta_roc": o[0],
                    "min_pr_ratio": o[1],
                }
                for o, w, _ in rows[:10]
            ],
        }
    return result


def write_tuned_toml(result: dict[str, Any], cfg: SubstrateConfig, path: Path) -> None:
    w = cfg.weights
    lines = [
        "# Tuned index weights — frozen per DECISIONS.md D-009 before the test set is run.",
        f"# tuning repos: {', '.join(result['tuning_repos'])}; grid step {result['grid_step']}",
        f"# objective: {result['objective']}",
        "",
        "[weights]",
    ]
    for name in (
        "load_index",
        "change_pressure_index",
        "bug_pressure_index",
        "neglect_index",
        "complexity_proxy_index",
    ):
        chosen = result["indices"].get(name, {}).get("chosen") or getattr(w, name)
        items = ", ".join(f'"{k}" = {v}' for k, v in chosen.items())
        lines.append(f"{name} = {{ {items} }}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
