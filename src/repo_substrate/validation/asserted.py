"""The asserted bar (validation-spec §2.4): stability budget, second-instrument /
cross-modal corroboration, reported correlates, and the recorded (non-gating)
recognition check."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from statistics import median
from typing import Any

import numpy as np

from .config import GROUNDING, RECOGNITION_LISTS, ValidationConfig
from .stats import bootstrap_ci, kendall_tau_b, permutation_p
from .substrates import SubstrateCache, canonical_resolver


@dataclass
class RepoAsserted:
    name: str
    head_sha: str
    perturbed_sha: str
    n_population: int
    n_compared: int
    n_excluded_touched: int
    stability: dict[str, dict[str, Any]] = field(default_factory=dict)
    corroboration: dict[str, dict[str, Any]] = field(default_factory=dict)
    correlates: dict[str, dict[str, dict[str, Any]]] = field(default_factory=dict)
    recognition: dict[str, dict[str, Any]] = field(default_factory=dict)
    recognition_ref: str | None = None


def _signal_value(node: dict[str, Any], sig: str) -> float | None:
    d = node.get("derived") or {}
    idx = d.get("indices") or {}
    if sig in idx:
        return idx[sig]
    v = node["metrics"].get(sig)
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    return v


def _stability_value(node: dict[str, Any], sig: str) -> float | None:
    """Indices compare as themselves; everything else on its percentile (a raw count's
    movement is only meaningful relative to the distribution)."""
    d = node.get("derived") or {}
    idx = d.get("indices") or {}
    if sig in idx:
        return idx[sig]
    pct = d.get("percentiles") or {}
    if sig in pct:
        return pct[sig]
    v = node["metrics"].get(sig)
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    return v


def population(sub: dict[str, Any], exclude_tests: bool = True) -> list[dict[str, Any]]:
    return [nd for nd in sub["nodes"]
            if (nd.get("derived") or {}).get("indices") is not None
            and not (exclude_tests and nd["metrics"].get("is_test"))]


def run_stability(full: dict[str, Any], pert: dict[str, Any], vcfg: ValidationConfig) -> tuple[dict[str, dict[str, Any]], int, int]:
    """§2.4.1 (as revised by D-008): per-signal movement between HEAD and HEAD with the
    last K commits removed, over population nodes present in both runs and NOT touched
    by a removed commit. A touched file's recency and churn legitimately move — that is
    the signal reporting the edit, not instability. What the budget measures is whether
    editing *other* files moves *this* file's value."""
    canon = canonical_resolver(full)
    k = vcfg.stability_perturbation_k
    touched = {canon(p) for c in full["timeline"][-k:] for p in c["nodes_touched"]}
    head_pop = {nd["id"]: nd for nd in population(full)}
    pert_pop = {canon(nd["id"]): nd for nd in population(pert)}
    common_all = set(head_pop) & set(pert_pop)
    common = sorted(common_all - touched)
    out: dict[str, dict[str, Any]] = {}
    for sig in GROUNDING:
        deltas = []
        for p in common:
            a = _stability_value(head_pop[p], sig)
            b = _stability_value(pert_pop[p], sig)
            if a is None or b is None:
                continue
            deltas.append(abs(float(a) - float(b)))
        if not deltas:
            out[sig] = {"k": k, "median_abs_delta": None, "max_abs_delta": None, "p95_abs_delta": None, "passed": None, "n": 0}
            continue
        med, mx = float(median(deltas)), float(max(deltas))
        p95 = float(np.quantile(deltas, 0.95))
        out[sig] = {"k": k, "eps": vcfg.stability_eps, "delta": vcfg.stability_delta,
                    "median_abs_delta": med, "max_abs_delta": mx, "p95_abs_delta": p95, "n": len(deltas),
                    "passed": bool(med <= vcfg.stability_eps and mx <= vcfg.stability_delta)}
    return out, len(common), len(common_all) - len(common)


def _tau_block(pop: list[dict[str, Any]], sig: str, cp: str, vcfg: ValidationConfig, floor: float | None) -> dict[str, Any]:
    xs, ys = [], []
    for nd in pop:
        a = _signal_value(nd, sig)
        b = nd["metrics"].get(cp)
        if a is None or b is None:
            continue
        xs.append(float(a))
        ys.append(float(b))
    if len(xs) < 10:
        return {"counterpart": cp, "passed": None, "reason": "too_few_pairs", "n": len(xs)}
    tau = kendall_tau_b(xs, ys)
    lo, hi = bootstrap_ci(xs, ys, kendall_tau_b, vcfg.bootstrap_n, vcfg.rng_seed)
    pval = permutation_p(xs, ys, kendall_tau_b, vcfg.permutation_n, vcfg.rng_seed + 1)
    block: dict[str, Any] = {"counterpart": cp, "n": len(xs), "tau_b": tau, "tau_b_ci": [lo, hi], "permutation_p": pval}
    if floor is not None:
        passed = bool(lo == lo and lo >= floor)  # lo == lo filters NaN
        block.update({"tau_floor": floor, "passed": passed, "reason": None if passed else "corroboration_fail"})
    return block


def run_corroboration(full: dict[str, Any], vcfg: ValidationConfig) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, dict[str, Any]]]]:
    """§2.4.2: G2 second-instrument and G3 cross-modal τ-b with bootstrap lower CI bound;
    reported correlates for every signal that declares them."""
    pop = population(full)
    corr: dict[str, dict[str, Any]] = {}
    correlates: dict[str, dict[str, dict[str, Any]]] = {}
    for sig, g in GROUNDING.items():
        cls = g["class"]
        if cls == "G2":
            corr[sig] = _tau_block(pop, sig, g["counterpart"], vcfg, vcfg.tau_instrument)
        elif cls == "G3":
            corr[sig] = _tau_block(pop, sig, g["counterpart"], vcfg, vcfg.tau_asserted)
        elif cls == "G1":
            corr[sig] = {"counterpart": None, "instrument": g["instrument"], "passed": True, "reason": None}
        else:  # G4 — decided in the gate from its inputs
            corr[sig] = {"counterpart": None, "inputs": g["inputs"], "passed": None, "reason": "derived"}
        for c in g.get("correlates", []):
            correlates.setdefault(sig, {})[c] = _tau_block(pop, sig, c, vcfg, None)
    return corr, correlates


_LIST_HEADER = re.compile(r"^##\s*(\d+)\.")
_ITEM = re.compile(r"^\s*\d+\.\s*(.*?)\s*$")


def parse_blind_ranking(text: str) -> dict[int, list[str]]:
    """Numbered lists under `## N.` headers; items are paths, optionally in backticks."""
    lists: dict[int, list[str]] = {}
    current: int | None = None
    for line in text.splitlines():
        h = _LIST_HEADER.match(line)
        if h:
            current = int(h.group(1))
            lists.setdefault(current, [])
            continue
        if current is None:
            continue
        m = _ITEM.match(line)
        if m and m.group(1):
            item = m.group(1).strip().strip("`").strip()
            if item and not item.startswith("<"):
                lists[current].append(item)
    return lists


def run_recognition(full: dict[str, Any], blind_path: Path | None, k: int = 10) -> tuple[dict[str, dict[str, Any]], str | None]:
    """§2.4.3: overlap@k and τ-b between the developer's sealed ranks and the signal's
    values on the ranked files. Reported, never gating (n = 1)."""
    if blind_path is None or not blind_path.exists():
        return {}, None
    lists = parse_blind_ranking(blind_path.read_text())
    nodes = {nd["id"]: nd for nd in full["nodes"]}
    out: dict[str, dict[str, Any]] = {}
    for num, sig in RECOGNITION_LISTS.items():
        human = [p for p in lists.get(num, []) if p in nodes][:k]
        missing = [p for p in lists.get(num, []) if p not in nodes]
        if not human:
            out[sig] = {"n": 1, "list": num, "ranked": 0, "missing": missing}
            continue
        scored = sorted(((_signal_value(nd, sig) or 0.0, pid) for pid, nd in nodes.items()
                         if (nd.get("derived") or {}).get("indices") is not None), key=lambda t: (-t[0], t[1]))
        top = [pid for _, pid in scored[:k]]
        overlap = len(set(human) & set(top)) / k
        ranks = [float(-i) for i in range(len(human))]  # rank 1 → highest
        vals = [float(_signal_value(nodes[p], sig) or 0.0) for p in human]
        tau = kendall_tau_b(ranks, vals) if len(human) >= 3 else float("nan")
        out[sig] = {"n": 1, "list": num, "ranked": len(human), "missing": missing,
                    "overlap_at_k": overlap, "k": k, "tau_b_on_ranked": tau}
    return out, str(blind_path)


def run_asserted(repo: Path, cache: SubstrateCache, vcfg: ValidationConfig, blind_path: Path | None) -> RepoAsserted:
    full = cache.get(repo, "HEAD")
    timeline = full["timeline"]
    k = vcfg.stability_perturbation_k
    if len(timeline) <= k + 1:
        raise ValueError(f"{repo.name}: too few commits ({len(timeline)}) for stability perturbation K={k}")
    pert_sha = timeline[-(k + 1)]["sha"]
    pert = cache.get(repo, pert_sha, truncate=True)
    stability, n_common, n_touched = run_stability(full, pert, vcfg)
    corr, correlates = run_corroboration(full, vcfg)
    recog, ref = run_recognition(full, blind_path)
    return RepoAsserted(
        name=full["repo"]["name"], head_sha=full["repo"]["head_sha"], perturbed_sha=pert_sha,
        n_population=len(population(full)), n_compared=n_common, n_excluded_touched=n_touched,
        stability=stability, corroboration=corr, correlates=correlates, recognition=recog, recognition_ref=ref,
    )
