"""Derived signals (repo-substrate-spec §6): percentiles and composite indices.

Three layers of increasing synthesis: raw facts (§5) → repo-relative position
(§6.1) → composite pressure (§6.2). The first is measurement; the second is
normalization; the third is a small, versioned model whose weights live in
config and feed the fingerprint.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from .config import SubstrateConfig

# The exhaustive percentile keyset (§6.1). Every index input that is a percentile is here.
PERCENTILE_METRICS: tuple[str, ...] = (
    "size_loc", "age_days", "last_touched_days", "commit_count", "churn_lines",
    "fix_count", "revert_count", "author_count", "fan_in", "fan_out",
    "cochange_degree", "blame_age_median", "test_fan_in",
)
NONZERO_VARIANTS: tuple[str, ...] = ("fan_in", "fix_count", "revert_count", "test_fan_in")
DERIVED_PERCENTILED: tuple[str, ...] = ("centrality", "nesting_proxy")


def ecdf_percentiles(values: Mapping[str, float | int | None]) -> dict[str, float | None]:
    """Empirical CDF with average-rank ties, over the non-null population.
    pct(x) = (#strictly-less + (#equal + 1) / 2) / N, range (0, 1]. A null value
    gets a null percentile and does not count in N."""
    pop = sorted(v for v in values.values() if v is not None)
    n = len(pop)
    out: dict[str, float | None] = {}
    if n == 0:
        return {k: None for k in values}
    # counts by value for O(1) lookup
    less: dict[float, int] = {}
    equal: dict[float, int] = {}
    i = 0
    while i < n:
        j = i
        while j < n and pop[j] == pop[i]:
            j += 1
        less[pop[i]] = i
        equal[pop[i]] = j - i
        i = j
    for k, v in values.items():
        if v is None:
            out[k] = None
        else:
            out[k] = (less[v] + (equal[v] + 1) / 2.0) / n
    return out


def compute_percentiles(
    metrics_by_node: Mapping[str, Mapping[str, float | int | None]],
    population: Sequence[str],
) -> dict[str, dict[str, float | None]]:
    """§6.1: percentiles for every node, ranked against ``population`` only.
    Nodes outside the population (tests, orphans) still receive a percentile —
    their position relative to the reference distribution — computed by inserting
    the value into the population's ECDF without counting it."""
    pop_set = set(population)
    result: dict[str, dict[str, float | None]] = {n: {} for n in metrics_by_node}
    keys = list(PERCENTILE_METRICS) + list(DERIVED_PERCENTILED)
    for key in keys:
        pop_vals = {n: metrics_by_node[n].get(key) for n in population}
        pop_sorted = sorted(v for v in pop_vals.values() if v is not None)
        n_pop = len(pop_sorted)
        pop_pct = ecdf_percentiles(pop_vals)
        for node, m in metrics_by_node.items():
            v = m.get(key)
            if node in pop_set:
                result[node][key] = pop_pct[node]
            elif v is None or n_pop == 0:
                result[node][key] = None
            else:
                less = sum(1 for x in pop_sorted if x < v)
                equal = sum(1 for x in pop_sorted if x == v)
                result[node][key] = (less + (equal + 1) / 2.0) / n_pop if equal else (less + 0.5) / n_pop
        if key in NONZERO_VARIANTS:
            nz_pop = {n: (v if (v is not None and v > 0) else None) for n, v in pop_vals.items()}
            nz_sorted = sorted(v for v in nz_pop.values() if v is not None)
            nz_pct = ecdf_percentiles(nz_pop)
            for node, m in metrics_by_node.items():
                v = m.get(key)
                if v is None or v <= 0:
                    result[node][f"{key}_nonzero"] = None
                elif node in pop_set:
                    result[node][f"{key}_nonzero"] = nz_pct[node]
                elif not nz_sorted:
                    result[node][f"{key}_nonzero"] = None
                else:
                    less = sum(1 for x in nz_sorted if x < v)
                    equal = sum(1 for x in nz_sorted if x == v)
                    result[node][f"{key}_nonzero"] = (less + (equal + 1) / 2.0) / len(nz_sorted) if equal else (less + 0.5) / len(nz_sorted)
    return result


def _weighted(inputs: dict[str, float | None], weights: Mapping[str, float]) -> tuple[float | None, bool]:
    """Weighted sum over available inputs with renormalization (§6.2.1). Returns
    (value, degraded). degraded is True when any weighted input was unavailable.
    All-unavailable → (None, True)."""
    total_w = 0.0
    acc = 0.0
    degraded = False
    for k, w in weights.items():
        v = inputs.get(k)
        if v is None:
            degraded = True
            continue
        acc += w * v
        total_w += w
    if total_w == 0.0:
        return None, True
    return acc / total_w, degraded


def compute_indices(
    pct: Mapping[str, float | None],
    metrics: Mapping[str, float | int | None],
    test_fan_in: int,
    recent_commit_share: float | None,
    graph_degraded: bool,
    cfg: SubstrateConfig,
) -> dict[str, float | bool | None]:
    """§6.2 indices for one node. Every input is in [0,1]; every output is in [0,1] or None."""
    w = cfg.weights

    def inv(x: float | None) -> float | None:
        return None if x is None else 1.0 - x

    fan_in_nz = pct.get("fan_in_nonzero")
    # A floor file (fan_in == 0) has no nonzero percentile and contributes 0.0 load from that term (§6.1).
    fan_in_input = 0.0 if (fan_in_nz is None and metrics.get("fan_in") == 0) else fan_in_nz
    fix_nz = pct.get("fix_count_nonzero")
    fix_input = 0.0 if (fix_nz is None and metrics.get("fix_count") == 0) else fix_nz
    cc = metrics.get("commit_count") or 0
    fix_ratio = (metrics.get("fix_count") or 0) / cc if cc else None

    load_inputs = {
        "fan_in_nonzero": None if graph_degraded else fan_in_input,
        "centrality": None if graph_degraded else pct.get("centrality"),
        "inv_fan_out": inv(pct.get("fan_out")),
        "size_loc": pct.get("size_loc"),
    }
    load, load_deg = _weighted(load_inputs, w.load_index)
    load_deg = load_deg or graph_degraded

    change, _ = _weighted({
        "churn_lines": pct.get("churn_lines"),
        "commit_count": pct.get("commit_count"),
        "recency": inv(pct.get("last_touched_days")),
    }, w.change_pressure_index)

    # The candidate input set is wider than the pinned formula so the D-009 tuning grid can
    # reach recency/busyness terms; config.validate() confines weight keys to this set.
    bug, _ = _weighted({
        "fix_count_nonzero": fix_input,
        "fix_count": pct.get("fix_count"),
        "revert_count": pct.get("revert_count"),
        "fix_ratio": fix_ratio,
        "recency": inv(pct.get("last_touched_days")),
        "commit_count": pct.get("commit_count"),
    }, w.bug_pressure_index)

    neglect, _ = _weighted({
        "age_days": pct.get("age_days"),
        "last_touched_days": pct.get("last_touched_days"),
        "inv_recent_commit_share": inv(recent_commit_share),
    }, w.neglect_index)

    complexity, _ = _weighted({
        "size_loc": pct.get("size_loc"),
        "nesting_proxy": pct.get("nesting_proxy"),
        "fan_out": pct.get("fan_out"),
    }, w.complexity_proxy_index)

    # reinforcement_index (§6.2 as revised by D-011): the import-graph reading. 0.0 when no test
    # imports the file; otherwise 0.5 + 0.5 · percentile among files that some test imports, so
    # "one test touches it" and "the most-tested file in the repo" are distinguishable. Path
    # convention (has_sibling_test / test_proximity) is kept as a metric and reported correlate,
    # not an input: it is convention-dependent and disagreed with the graph on 3 of 4 reference repos.
    if graph_degraded:
        reinforcement: float | None = None
    elif test_fan_in <= 0:
        reinforcement = 0.0
    else:
        tp = pct.get("test_fan_in_nonzero")
        reinforcement = 0.5 + 0.5 * (tp if tp is not None else 0.0)

    return {
        "load_index": load,
        "load_index_degraded": load_deg,
        "change_pressure_index": change,
        "bug_pressure_index": bug,
        "neglect_index": neglect,
        "reinforcement_index": reinforcement,
        "reinforcement_index_degraded": graph_degraded,
        "complexity_proxy_index": complexity,
    }
