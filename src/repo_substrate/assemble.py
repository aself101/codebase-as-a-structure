"""Assemble ``substrate.json`` (repo-substrate-spec §4, §11 build order).

The assembler keys nodes off the HEAD (or --rev) inventory and attaches history
to them; a FileHistory whose canonical path is absent at the rev is dropped
(§5 node-set invariant), and a rev file with no FileHistory is an orphan
(§5, defect signal). It is the only place the components meet.
"""

from __future__ import annotations

import importlib.metadata
import math
import platform
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from . import __version__
from .altdeps import scan_fan_in_alt
from .config import SubstrateConfig
from .deps import DependencyExtractor, DependencyResult
from .derived import compute_indices, compute_percentiles
from .gitutil import (
    branch_name,
    detached_worktree,
    git_version,
    resolve_rev,
    root_commit_sha,
    run_git,
)
from .graph import fan_counts, pagerank
from .history import HistoryMiner, PydrillerHistoryMiner, blame_age_median, cochange_degree
from .inventory import build_inventory

SCHEMA_VERSION = "0.2"


@dataclass
class ExtractOptions:
    rev: str = "HEAD"
    truncate_at: str | None = None
    scratch_dir: Path | None = None
    blame_workers: int = 8


def _round(v: Any, dp: int) -> Any:
    if isinstance(v, float):
        return round(v, dp)
    if isinstance(v, dict):
        return {k: _round(x, dp) for k, x in v.items()}
    if isinstance(v, list):
        return [_round(x, dp) for x in v]
    return v


def _gini(counts: list[int]) -> float:
    if not counts or sum(counts) == 0:
        return 0.0
    xs = sorted(counts)
    n = len(xs)
    cum = 0.0
    for i, x in enumerate(xs, start=1):
        cum += i * x
    return (2.0 * cum) / (n * sum(xs)) - (n + 1.0) / n


def toolchain_versions(extractor: DependencyExtractor | None) -> dict[str, str]:
    """§3 pinned capture format: role → name@version as each tool's own resolver reports it."""
    tv = {
        "history": f"pydriller@{importlib.metadata.version('pydriller')}",
        "git": f"git@{git_version()}",
        "python": f"python@{platform.python_version()}",
        "substrate": f"repo-substrate@{__version__}",
    }
    if extractor is not None:
        tv["dep_extractor"] = extractor.version()
    return tv


def extract(
    repo: Path,
    cfg: SubstrateConfig,
    opts: ExtractOptions,
    extractor: DependencyExtractor | None,
    miner: HistoryMiner | None = None,
) -> dict[str, Any]:
    cfg.validate()
    repo = repo.resolve()
    miner = miner or PydrillerHistoryMiner()
    # --truncate-at implies the analyzed revision is the split SHA: inventory and history both stop there (§8).
    rev_spec = opts.truncate_at or opts.rev
    rev = resolve_rev(repo, rev_spec)
    tv = toolchain_versions(extractor)
    fingerprint = cfg.fingerprint(tv)
    fix_fallback = re.compile(cfg.fix_subject_regex, re.IGNORECASE)

    # --- steps 2–4: inventory + seed (by blob, no worktree), edges (worktree), history
    static_nodes, seed = build_inventory(repo, rev, cfg)
    node_paths = {n.path for n in static_nodes}
    static_by_path = {n.path: n for n in static_nodes}
    js_ts = {n.path for n in static_nodes if n.lang in ("ts", "js")}
    test_paths = {n.path for n in static_nodes if n.is_test}
    dep = DependencyResult()
    fan_in_alt: dict[str, int] = {}
    fan_out_alt: dict[str, int] = {}
    test_fan_in_alt: dict[str, int] = {}
    alt_unreadable: list[str] = []
    if js_ts:
        with detached_worktree(repo, rev, opts.scratch_dir) as wt:
            if extractor is not None:
                dep = extractor.extract(wt, js_ts)
            # Second instrument for the fan-in family (validation §2.4.2 G2, D-008/D-011): independent scanner.
            fan_in_alt, fan_out_alt, test_fan_in_alt, alt_unreadable = scan_fan_in_alt(
                wt, js_ts, test_paths
            )
    hist = miner.mine(repo, rev, fix_fallback)
    as_of = hist.as_of

    # --- §5 node-set invariant: nodes = rev inventory; attach history; count orphans
    paths = sorted(node_paths)
    cochange = cochange_degree(hist.timeline, cfg.cochange_min, cfg.cochange_max_files)
    blame, blame_failed = blame_age_median(repo, rev, paths, as_of, opts.blame_workers)
    fan_in, fan_out = fan_counts(paths, dep.edges)
    # test_fan_in: importers that are test files — the import-graph reading of reinforcement
    # (D-011): a test that imports X reinforces X, whatever the file is named.
    test_fan_in: dict[str, int] = {p: 0 for p in paths}
    for a, b in dep.edges:
        if a in test_paths and b in test_fan_in:
            test_fan_in[b] += 1
    graph_available = len(dep.edges) > 0
    denom = len(dep.edges) + dep.unresolved_imports
    resolution_rate = (len(dep.edges) / denom) if denom else None
    # Local second-instrument agreement (D-011): τ-b between the primary and alternate fan_in over
    # JS/TS non-test nodes. Resolution rate catches non-resolution; this catches the other failure —
    # a confident graph that another reader of the same source does not reproduce.
    instrument_tau: float | None = None
    if graph_available and js_ts:
        from scipy.stats import kendalltau

        pairs = [
            (fan_in.get(p, 0), fan_in_alt.get(p, 0)) for p in sorted(js_ts) if p not in test_paths
        ]
        if len(pairs) >= 10:
            t = kendalltau([a for a, _ in pairs], [b for _, b in pairs], variant="b").statistic
            instrument_tau = None if t != t else float(t)
    instruments_disagree = instrument_tau is not None and instrument_tau < cfg.instrument_tau_min
    graph_degraded = (
        (not graph_available)
        or (resolution_rate is not None and resolution_rate < cfg.graph_quality_min)
        or instruments_disagree
    )
    centrality = (
        pagerank(paths, dep.edges, cfg.pagerank_alpha, cfg.pagerank_max_iter, cfg.pagerank_tol)
        if graph_available
        else {}
    )

    n_commits = len(hist.timeline)
    # floor, mirroring the validation split (§3.1) so the two 0.20 windows coincide exactly
    recent_start = math.floor(n_commits * (1.0 - cfg.recent_window_frac))

    metrics_by_node: dict[str, dict[str, Any]] = {}
    orphans: list[str] = []
    recent_share: dict[str, float | None] = {}
    for p in paths:
        s = static_by_path[p]
        fh = hist.files.get(p)
        m: dict[str, Any] = {
            "size_loc": s.size_loc,
            "fan_in": fan_in.get(p, 0),
            "fan_out": fan_out.get(p, 0),
            "is_test": s.is_test,
            "has_sibling_test": s.test_proximity == 1.0,
            "nesting_proxy": s.nesting_proxy,
            "cochange_degree": cochange.get(p, 0),
            "blame_age_median": blame.get(p),
            "fan_in_alt": fan_in_alt.get(p, 0) if s.lang in ("ts", "js") else None,
            "fan_out_alt": fan_out_alt.get(p, 0) if s.lang in ("ts", "js") else None,
            "test_fan_in": test_fan_in.get(p, 0),
            "test_fan_in_alt": test_fan_in_alt.get(p, 0) if s.lang in ("ts", "js") else None,
            "test_proximity": s.test_proximity,
            "centrality": (round(centrality[p], cfg.rounding_dp) if p in centrality else None),
        }
        if fh is None:
            orphans.append(p)
            m.update(
                {
                    k: None
                    for k in (
                        "commit_count",
                        "churn_lines",
                        "fix_count",
                        "revert_count",
                        "author_count",
                        "age_days",
                        "last_touched_days",
                        "introduced_idx",
                    )
                }
            )
            m["history_missing"] = True
            recent_share[p] = None
        else:
            m.update(fh.raw_metrics(as_of))
            m["history_missing"] = False
            recent = sum(1 for i in fh.commit_idxs if i >= recent_start)
            recent_share[p] = recent / fh.commit_count if fh.commit_count else None
        m["recent_commit_share"] = recent_share[p]
        metrics_by_node[p] = m

    # --- §6.1 population and percentiles
    population = [
        p
        for p in paths
        if not metrics_by_node[p]["history_missing"]
        and not (cfg.exclude_tests_from_population and static_by_path[p].is_test)
    ]
    percentiles_valid = len(population) >= cfg.n_min
    pct = (
        compute_percentiles(metrics_by_node, population)
        if percentiles_valid
        else {p: None for p in paths}
    )

    # --- §6.2 indices
    nodes_out = []
    for p in paths:
        s = static_by_path[p]
        m = metrics_by_node[p]
        raw = dict(m)
        derived: dict[str, Any] | None
        node_pct = pct[p]
        if percentiles_valid and node_pct is not None and not m["history_missing"]:
            indices = compute_indices(
                node_pct, m, m["test_fan_in"], recent_share[p], graph_degraded, cfg
            )
            derived = {"percentiles": node_pct, "indices": indices}
        else:
            derived = {"percentiles": node_pct if percentiles_valid else None, "indices": None}
        nodes_out.append(
            {"id": p, "kind": "file", "lang": s.lang, "metrics": raw, "derived": derived}
        )

    # --- summary (§4 pinned definitions)
    non_merge_by_author: dict[str, int] = {}
    for c in hist.timeline:
        if not c.is_merge:
            non_merge_by_author[c.author] = non_merge_by_author.get(c.author, 0) + 1
    total_loc = sum(static_by_path[p].size_loc for p in paths)
    test_loc = sum(static_by_path[p].size_loc for p in paths if static_by_path[p].is_test)
    n = len(paths)
    root_sha = root_commit_sha(repo, rev)
    root_date = str(run_git(repo, "show", "-s", "--format=%aI", root_sha)).strip()
    repo_age_days = (as_of - datetime.fromisoformat(root_date)).days

    languages: dict[str, dict[str, int]] = {}
    for p in paths:
        s = static_by_path[p]
        lang = languages.setdefault(s.lang, {"files": 0, "loc": 0})
        lang["files"] += 1
        lang["loc"] += s.size_loc

    summary = {
        "node_count": n,
        "population_size": len(population),
        "percentiles_valid": percentiles_valid,
        "orphan_nodes": len(orphans),
        "graph_available": graph_available,
        "graph_resolution_rate": resolution_rate,
        "fan_in_instrument_tau": instrument_tau,
        "graph_instruments_disagree": instruments_disagree,
        "graph_degraded": graph_degraded,
        "external_imports": dep.external_imports,
        "unresolved_imports": dep.unresolved_imports,
        "non_node_imports": dep.non_node_imports,
        "blame_failed": len(blame_failed),
        "alt_scanner_unreadable": len(alt_unreadable),
        "tsconfig_malformed": dep.tsconfig_malformed is not None,
        "total_loc": total_loc,
        "repo_age_days": repo_age_days,
        "commit_count": n_commits,
        "author_count": len({c.author for c in hist.timeline}),
        "authorship_gini": _gini(list(non_merge_by_author.values())),
        "test_loc_ratio": (test_loc / total_loc) if total_loc else 0.0,
        "dep_graph_density": (len(dep.edges) / (n * (n - 1))) if n > 1 else 0.0,
    }

    timeline = [
        {
            "sha": c.sha,
            "ts": c.ts.isoformat(),
            "author": c.author,
            "subject": c.subject,
            "type": c.type,
            "matched_rule": c.matched_rule,
            "nodes_touched": sorted(set(c.nodes_touched)),
            "added": c.added,
            "deleted": c.deleted,
        }
        for c in hist.timeline
    ]

    out = {
        "schema_version": SCHEMA_VERSION,
        "extractor_version": __version__,
        "extracted_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "seed": seed,
        "repo": {
            "name": repo.name,
            "head_sha": rev,
            "branch": branch_name(repo),
            "root_commit_sha": root_sha,
            "as_of": as_of.isoformat(),
            "truncated_at": (rev if opts.truncate_at else None),
            "config_fingerprint": fingerprint,
            "toolchain_versions": dict(sorted(tv.items())),
        },
        "summary": summary,
        "languages": dict(sorted(languages.items())),
        "nodes": nodes_out,
        "edges": [{"from": a, "to": b, "kind": "import"} for a, b in sorted(dep.edges)],
        "timeline": timeline,
        # Historical path -> successor, one hop each; chase to reach the name at this rev.
        # nodes_touched in the timeline are recorded under the name current *at that commit*,
        # so a consumer joining timeline paths to nodes must resolve through this map.
        "renames": dict(sorted(hist.renames.items())),
        "caveats": {
            "orphan_nodes": orphans,
            "unresolved_import_samples": [
                {"from": a, "specifier": s} for a, s in dep.unresolved_samples
            ],
            "blame_failed": blame_failed,  # instrument broken, not absent (audit 2026-09-04)
            "alt_scanner_unreadable": alt_unreadable,
            "tsconfig_malformed": dep.tsconfig_malformed,
        },
    }
    return _round(out, cfg.rounding_dp)
