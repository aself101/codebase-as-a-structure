"""The substrate report (repo-substrate-spec §9): sorted evidence, no feature names.

Each section is a sorted query over continuous signals with its predicate
printed above the list. It names no building feature, archetype, or grade,
and C3 does not read it. Sections 4 and 5 are the toothpick and
flooded-basement queries, surfaced without naming them.
"""

from __future__ import annotations

from typing import Any

from .config import SubstrateConfig


def _rows(nodes: list[dict[str, Any]], key: str, k: int, pred=None) -> list[dict[str, Any]]:
    scored = []
    for n in nodes:
        d = n.get("derived") or {}
        idx = d.get("indices") or {}
        if idx.get(key) is None:
            continue
        if pred is not None and not pred(idx, n["metrics"]):
            continue
        scored.append((idx[key], n["id"], n))
    scored.sort(key=lambda t: (-t[0], t[1]))
    return [t[2] for t in scored[:k]]


def _fmt(v: Any) -> str:
    if v is None:
        return "–"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, float):
        return f"{v:.2f}"
    return str(v)


def _table(rows: list[dict[str, Any]], cols: list[tuple[str, str]]) -> str:
    if not rows:
        return "_(no nodes satisfy the predicate)_\n"
    head = "| file | " + " | ".join(c[0] for c in cols) + " |"
    sep = "|---|" + "|".join("---:" for _ in cols) + "|"
    lines = [head, sep]
    for n in rows:
        idx = (n.get("derived") or {}).get("indices") or {}
        m = n["metrics"]
        cells = []
        for _, k in cols:
            v = idx.get(k) if k in idx else m.get(k)
            cells.append(_fmt(v))
        lines.append(f"| `{n['id']}` | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def render_report(sub: dict[str, Any], cfg: SubstrateConfig) -> str:
    s = sub["summary"]
    r = sub["repo"]
    k, p, q = cfg.report_top_k, cfg.report_p, cfg.report_q
    nodes = sub["nodes"]
    out: list[str] = []
    out.append(f"# Substrate report — `{r['name']}` @ `{r['head_sha'][:10]}`\n")
    out.append(
        f"*Deterministic sorted evidence over continuous signals. No feature is named here; "
        f"naming is C3's job. Seed `{sub['seed'][:12]}…`, config fingerprint `{r['config_fingerprint'][:12]}…`, "
        f"as-of {r['as_of'][:10]}.*\n"
    )
    out.append(
        "> **UNGATED.** This report consults no `validation.json`. Every number below is a measurement or a "
        "fixed-weight blend of measurements; none has passed the anti-horoscope gate, and nothing here is a "
        "diagnosis. Diagnostic claims come only from C3 over gated signals (`structural-mapper-spec.md` §3).\n"
    )
    out.append("## Summary\n")
    out.append("| field | value |\n|---|---:|")
    for key in (
        "node_count",
        "population_size",
        "percentiles_valid",
        "orphan_nodes",
        "graph_available",
        "graph_resolution_rate",
        "fan_in_instrument_tau",
        "graph_instruments_disagree",
        "graph_degraded",
        "external_imports",
        "unresolved_imports",
        "non_node_imports",
        "blame_failed",
        "alt_scanner_unreadable",
        "tsconfig_malformed",
        "total_loc",
        "repo_age_days",
        "commit_count",
        "author_count",
        "authorship_gini",
        "test_loc_ratio",
        "dep_graph_density",
    ):
        out.append(f"| `{key}` | {_fmt(s.get(key))} |")
    out.append("")
    if not s["percentiles_valid"]:
        out.append(
            f"> **Percentiles invalid**: population {s['population_size']} < N_min {cfg.n_min}. "
            "Raw metrics only; no derived sections below.\n"
        )
        return "\n".join(out)
    if s["graph_degraded"]:
        out.append(
            "> **Graph degraded**: `load_index` computed without graph inputs and flagged "
            "`load_index_degraded` on every node. Graph-dependent claims must not be made from this run.\n"
        )

    load_cols = [
        ("load", "load_index"),
        ("degraded", "load_index_degraded"),
        ("fan_in", "fan_in"),
        ("centrality", "centrality"),
        ("fan_out", "fan_out"),
        ("loc", "size_loc"),
        ("cochange", "cochange_degree"),
    ]
    out.append(f"## 1. Highest `load_index` (top {k})\n")
    out.append(_table(_rows(nodes, "load_index", k), load_cols))

    change_cols = [
        ("change", "change_pressure_index"),
        ("churn", "churn_lines"),
        ("commits", "commit_count"),
        ("last_touched_d", "last_touched_days"),
    ]
    out.append(f"## 2. Highest `change_pressure_index` (top {k})\n")
    out.append(_table(_rows(nodes, "change_pressure_index", k), change_cols))

    bug_cols = [
        ("bug", "bug_pressure_index"),
        ("fixes", "fix_count"),
        ("reverts", "revert_count"),
        ("commits", "commit_count"),
        ("reinforcement", "reinforcement_index"),
    ]
    out.append(f"## 3. Highest `bug_pressure_index` (top {k})\n")
    out.append(_table(_rows(nodes, "bug_pressure_index", k), bug_cols))

    out.append(
        f"## 4. High load, low reinforcement — `load_index ≥ {p} ∧ reinforcement_index ≤ {q}` (top {k} by load)\n"
    )
    out.append(
        _table(
            _rows(
                nodes,
                "load_index",
                k,
                lambda i, m: (
                    (i.get("load_index") or 0) >= p and (i.get("reinforcement_index") or 0) <= q
                ),
            ),
            load_cols[:4]
            + [("reinforcement", "reinforcement_index"), ("bug", "bug_pressure_index")],
        )
    )

    out.append(
        f"## 5. Old, load-bearing, untouched — `neglect_index ≥ {p} ∧ load_index ≥ {q}` (top {k} by neglect)\n"
    )
    out.append(
        _table(
            _rows(
                nodes,
                "neglect_index",
                k,
                lambda i, m: (i.get("neglect_index") or 0) >= p and (i.get("load_index") or 0) >= q,
            ),
            [
                ("neglect", "neglect_index"),
                ("load", "load_index"),
                ("age_d", "age_days"),
                ("last_touched_d", "last_touched_days"),
                ("blame_age_d", "blame_age_median"),
                ("fan_in", "fan_in"),
            ],
        )
    )

    cav = sub.get("caveats", {})
    out.append("## Caveats\n")
    if cav.get("orphan_nodes"):
        out.append(
            f"- **Orphan nodes ({len(cav['orphan_nodes'])})** — files at the rev with no history (miner defect signal, §5): "
            + ", ".join(f"`{p}`" for p in cav["orphan_nodes"][:20])
            + ("…" if len(cav["orphan_nodes"]) > 20 else "")
        )
    if cav.get("unresolved_import_samples"):
        out.append(
            f"- **Unresolved in-repo imports** (first {len(cav['unresolved_import_samples'])} of {s['unresolved_imports']}): "
            + ", ".join(
                f"`{x['from']}` → `{x['specifier']}`" for x in cav["unresolved_import_samples"][:10]
            )
        )
    if not cav.get("orphan_nodes") and not cav.get("unresolved_import_samples"):
        out.append("- none")
    out.append("")
    return "\n".join(out)
