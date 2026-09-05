"""Pre-registered weight tuning (DECISIONS.md D-009).

Tune the two predictive indices' weights on the tuning repos only, by a fixed
grid, with a fixed objective, and freeze the result to a TOML file. The test
repos are never read here. Indices are recomputed from the cached training
substrates' percentiles, so tuning needs no re-extraction.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import replace
from pathlib import Path
from typing import Any

from ..config import ALLOWED_INPUTS, IndexWeights, SubstrateConfig
from ..derived import compute_indices
from .config import ValidationConfig
from .holdout import FIX_TYPES
from .stats import average_precision, roc_auc
from .substrates import SubstrateCache, canonical_resolver

GRID_STEP = 0.1


def compositions(keys: list[str], step: float) -> list[dict[str, float]]:
    """All weight vectors over `keys` with entries in {0, step, 2·step, …} summing to 1."""
    n = len(keys)
    units = int(round(1.0 / step))
    out = []
    for cuts in itertools.combinations(range(units + n - 1), n - 1):
        parts = []
        prev = -1
        for c in cuts + (units + n - 1,):
            parts.append(c - prev - 1)
            prev = c
        out.append({k: round(p * step, 6) for k, p in zip(keys, parts, strict=True)})
    return out


def _holdout_context(repo: Path, cache: SubstrateCache, vcfg: ValidationConfig, cfg: SubstrateConfig) -> dict[str, Any]:
    """Everything the objective needs for one repo: eligible ids, labels, baselines, and the
    per-node inputs (percentiles, metrics, proximity, recent share) to recompute indices."""
    full = cache.get(repo, "HEAD")
    timeline = full["timeline"]
    n = len(timeline)
    split_idx = int(math.floor(n * (1.0 - vcfg.holdout_frac)))
    split_sha = timeline[split_idx - 1]["sha"]
    holdout = timeline[split_idx:]
    train = cache.get(repo, split_sha, truncate=True)
    canon = canonical_resolver(full)
    head_nodes = {nd["id"] for nd in full["nodes"]}
    positives = {canon(p) for c in holdout if c["type"] in FIX_TYPES for p in c["nodes_touched"]}
    ids, labels, nodes = [], [], []
    for nd in train["nodes"]:
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
    recency = [1.0 - (nd["derived"]["percentiles"].get("last_touched_days") or 0.0) for nd in nodes]
    busyness = [float(nd["metrics"].get("commit_count") or 0) for nd in nodes]
    best_roc = max(roc_auc(recency, labels), roc_auc(busyness, labels))
    best_pr = max(average_precision(recency, labels), average_precision(busyness, labels))
    # recent_commit_share is not stored; neglect is not tuned, so pass None (its weight renormalizes).
    return {"name": full["repo"]["name"], "ids": ids, "labels": labels, "nodes": nodes,
            "best_roc": best_roc, "best_pr": best_pr, "graph_degraded": train["summary"]["graph_degraded"]}


def _score(ctx: dict[str, Any], index: str, weights: dict[str, float], cfg: SubstrateConfig) -> tuple[float, float]:
    w = replace(cfg.weights, **{index: weights})
    c = replace(cfg, weights=w)
    scores = []
    for nd in ctx["nodes"]:
        idx = compute_indices(nd["derived"]["percentiles"], nd["metrics"],
                              1.0 if nd["metrics"].get("has_sibling_test") else 0.0, None,
                              ctx["graph_degraded"], c)
        scores.append(float(idx[index] or 0.0))
    return roc_auc(scores, ctx["labels"]) - ctx["best_roc"], average_precision(scores, ctx["labels"]) / ctx["best_pr"]


def tune(tuning_repos: list[Path], cache: SubstrateCache, vcfg: ValidationConfig, cfg: SubstrateConfig,
         indices: tuple[str, ...] = ("bug_pressure_index", "change_pressure_index")) -> dict[str, Any]:
    ctxs = [_holdout_context(r, cache, vcfg, cfg) for r in tuning_repos]
    result: dict[str, Any] = {"tuning_repos": [c["name"] for c in ctxs], "grid_step": GRID_STEP,
                              "objective": "min over tuning repos of (ROC-AUC − best baseline ROC-AUC); tie: min PR-AUC ratio",
                              "indices": {}}
    for index in indices:
        keys = sorted(ALLOWED_INPUTS[index])
        grid = compositions(keys, GRID_STEP)
        rows = []
        for wts in grid:
            per = [_score(c, index, wts, cfg) for c in ctxs]
            obj = (min(d for d, _ in per), min(r for _, r in per))
            rows.append((obj, wts, per))
        rows.sort(key=lambda t: (-t[0][0], -t[0][1]))
        best_obj, best_w, best_per = rows[0]
        baseline_w = getattr(cfg.weights, index)
        base_per = [_score(c, index, baseline_w, cfg) for c in ctxs]
        result["indices"][index] = {
            "inputs": keys,
            "grid_size": len(grid),
            "chosen": {k: v for k, v in best_w.items() if v > 0},
            "chosen_objective": {"min_delta_roc": best_obj[0], "min_pr_ratio": best_obj[1]},
            "chosen_per_repo": [{"name": c["name"], "delta_roc": d, "pr_ratio": r} for c, (d, r) in zip(ctxs, best_per, strict=True)],
            "spec_placeholder": {k: v for k, v in baseline_w.items()},
            "spec_placeholder_per_repo": [{"name": c["name"], "delta_roc": d, "pr_ratio": r} for c, (d, r) in zip(ctxs, base_per, strict=True)],
            "top10": [{"weights": {k: v for k, v in w.items() if v > 0}, "min_delta_roc": o[0], "min_pr_ratio": o[1]} for o, w, _ in rows[:10]],
        }
    return result


def write_tuned_toml(result: dict[str, Any], cfg: SubstrateConfig, path: Path) -> None:
    w = cfg.weights
    lines = ["# Tuned index weights — frozen per DECISIONS.md D-009 before the test set is run.",
             f"# tuning repos: {', '.join(result['tuning_repos'])}; grid step {result['grid_step']}",
             f"# objective: {result['objective']}", "", "[weights]"]
    for name in ("load_index", "change_pressure_index", "bug_pressure_index", "neglect_index", "complexity_proxy_index"):
        chosen = result["indices"].get(name, {}).get("chosen") or getattr(w, name)
        items = ", ".join(f'"{k}" = {v}' for k, v in chosen.items())
        lines.append(f"{name} = {{ {items} }}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def _load_weights_toml(_: IndexWeights) -> None:  # pragma: no cover — documented in SubstrateConfig.load
    pass
