"""Geometry (mapper §6, D-017): strata and wings are a property of the substrate, not of
any profile. Two strata definitions exist (system spec §5.1):

- ``age``:   five percentile bands of ``age_days`` — era strata, oldest at the bottom.
- ``layer``: dependency layering — the longest import path from a node down to a leaf
  (a node that imports nothing in-repo). Leaves are layer 0 and sit at the bottom: they
  are what everything else rests on. Cycles are collapsed to strongly connected
  components first (Tarjan), so every node in a cycle shares one layer. Bands are five
  quantile bands of the layer number.

The chosen geometry is recorded in the skeleton so two renders differ only where the
substrate differs.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from typing import Any

from ..derived import ecdf_percentiles

STRATA_BANDS = 5
GEOMETRIES = ("age", "layer")


def _sccs(nodes: list[str], out_edges: dict[str, set[str]]) -> dict[str, int]:
    """Tarjan's SCC; returns node -> component id. Iterative to survive deep graphs."""
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    on_stack: set[str] = set()
    stack: list[str] = []
    comp: dict[str, int] = {}
    counter = 0
    ncomp = 0
    for root in sorted(nodes):
        if root in index:
            continue
        work: list[tuple[str, iter]] = [(root, iter(sorted(out_edges.get(root, ()))))]
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on_stack.add(root)
        while work:
            v, it = work[-1]
            advanced = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack.add(w)
                    work.append((w, iter(sorted(out_edges.get(w, ())))))
                    advanced = True
                    break
                if w in on_stack:
                    low[v] = min(low[v], index[w])
            if advanced:
                continue
            work.pop()
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[v])
            if low[v] == index[v]:
                while True:
                    w = stack.pop()
                    on_stack.discard(w)
                    comp[w] = ncomp
                    if w == v:
                        break
                ncomp += 1
    return comp


def dependency_layers(nodes: list[str], edges: list[dict[str, str]]) -> dict[str, int]:
    """Longest path (in edges) from each node to a leaf, over the SCC condensation."""
    node_set = set(nodes)
    out_edges: dict[str, set[str]] = defaultdict(set)
    for e in edges:
        a, b = e["from"], e["to"]
        if a in node_set and b in node_set and a != b:
            out_edges[a].add(b)
    comp = _sccs(nodes, out_edges)
    comp_out: dict[int, set[int]] = defaultdict(set)
    for a, bs in out_edges.items():
        for b in bs:
            if comp[a] != comp[b]:
                comp_out[comp[a]].add(comp[b])
    # longest path on the DAG of components, memoized; recursion depth bounded by the DAG height
    sys.setrecursionlimit(max(10000, sys.getrecursionlimit()))
    memo: dict[int, int] = {}

    def depth(c: int) -> int:
        if c in memo:
            return memo[c]
        d = 0
        for n in sorted(comp_out.get(c, ())):
            d = max(d, 1 + depth(n))
        memo[c] = d
        return d

    return {n: depth(comp[n]) for n in nodes}


def compute_strata(
    population: list[dict[str, Any]], substrate: dict[str, Any], geometry: str
) -> tuple[dict[str, int], dict[str, float | int | None]]:
    """(band by node, raw strata value by node). Band 0 = bottom."""
    if geometry not in GEOMETRIES:
        raise ValueError(f"unknown geometry {geometry!r}; choose from {GEOMETRIES}")
    ids = [n["id"] for n in population]
    if geometry == "age":
        raw: dict[str, float | int | None] = {
            n["id"]: ((n.get("derived") or {}).get("percentiles") or {}).get("age_days")
            for n in population
        }
        # oldest (highest age percentile) at the bottom
        bands = {
            nid: (
                min(STRATA_BANDS - 1, int((1.0 - (p or 0.0)) * STRATA_BANDS))
                if p is not None
                else 2
            )
            for nid, p in raw.items()
        }
        return bands, raw
    layers = dependency_layers(ids, substrate.get("edges") or [])
    raw = dict(layers)
    pct = ecdf_percentiles({k: float(v) for k, v in layers.items()})
    # leaves (layer 0, lowest percentile) at the bottom
    bands = {
        nid: (min(STRATA_BANDS - 1, int((1.0 - (p or 0.0)) * STRATA_BANDS)) if p is not None else 2)
        for nid, p in pct.items()
    }
    # ecdf gives high percentile to high layer → 1-p puts high layers in band 0; invert so leaves are band 0
    bands = {nid: STRATA_BANDS - 1 - b for nid, b in bands.items()}
    return bands, raw
