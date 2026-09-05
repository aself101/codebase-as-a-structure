"""Graph metrics (repo-substrate-spec §6.2.2, §6.3): fan_in, fan_out, PageRank centrality.

PageRank is an in-package power iteration replicating networkx's pure-Python
``_pagerank_python`` semantics exactly (uniform dangling redistribution, L1
convergence test ``err < N * tol``), rather than calling networkx, so the
numeric path has no dependency on which BLAS or sparse backend a platform
happens to load. Parameters are pinned in config and hashed into the fingerprint.
"""

from __future__ import annotations

from collections import defaultdict


def fan_counts(
    nodes: list[str], edges: set[tuple[str, str]]
) -> tuple[dict[str, int], dict[str, int]]:
    fan_in: dict[str, int] = {n: 0 for n in nodes}
    fan_out: dict[str, int] = {n: 0 for n in nodes}
    for a, b in edges:
        fan_out[a] = fan_out.get(a, 0) + 1
        fan_in[b] = fan_in.get(b, 0) + 1
    return fan_in, fan_out


def pagerank(
    nodes: list[str], edges: set[tuple[str, str]], alpha: float, max_iter: int, tol: float
) -> dict[str, float]:
    """Deterministic PageRank. Node order is the sorted node list; iteration is
    plain Python floats summed in that fixed order."""
    n = len(nodes)
    if n == 0:
        return {}
    order = sorted(nodes)
    idx = {v: i for i, v in enumerate(order)}
    out_edges: dict[int, list[int]] = defaultdict(list)
    for a, b in sorted(edges):
        if a in idx and b in idx:
            out_edges[idx[a]].append(idx[b])
    out_deg = [len(out_edges[i]) for i in range(n)]
    x = [1.0 / n] * n
    p = 1.0 / n
    for _ in range(max_iter):
        xlast = x
        x = [0.0] * n
        dangle = alpha * sum(xlast[i] for i in range(n) if out_deg[i] == 0)
        for i in range(n):
            if out_deg[i] == 0:
                continue
            share = alpha * xlast[i] / out_deg[i]
            for j in out_edges[i]:
                x[j] += share
        for i in range(n):
            x[i] += dangle * p + (1.0 - alpha) * p
        err = sum(abs(x[i] - xlast[i]) for i in range(n))
        if err < n * tol:
            break
    return {order[i]: x[i] for i in range(n)}
