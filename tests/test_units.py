"""Unit tests for the pure functions of the substrate. Each test cites the spec
section whose contract it verifies (companion checklist item in brackets)."""

from __future__ import annotations

import re

import pytest

from repo_substrate.config import SubstrateConfig
from repo_substrate.derived import compute_indices, compute_percentiles, ecdf_percentiles
from repo_substrate.graph import fan_counts, pagerank
from repo_substrate.history import CommitRecord, classify_commit, cochange_degree
from repo_substrate.inventory import count_loc, nesting_proxy, tree_seed
from repo_substrate.inventory import (
    test_proximity as proximity_tiers,  # alias: pytest would collect the name
)

FIX = re.compile(r"\b(bug|hotfix|patch)\b", re.IGNORECASE)


# --- §7 classification [G] ------------------------------------------------------


@pytest.mark.parametrize(
    "subject,merge,expected",
    [
        ("fix: null deref", False, ("fix", "conventional-prefix")),
        (
            "Fix login bug",
            False,
            ("fix", "conventional-prefix"),
        ),  # colon optional, case-insensitive
        ("feat(api): add thing", False, ("feat", "conventional-prefix")),
        (
            'Revert "feat: x"',
            False,
            ("revert", "conventional-prefix"),
        ),  # stage 2 is dead: stage 1 catches it
        ("Merge branch 'x'", True, ("merge", "merge-parents")),
        ("fix typo", True, ("fix", "conventional-prefix")),  # prefix beats merge (order pinned)
        ("hotfix for prod", False, ("fix", "subject-regex")),
        ("Update README", False, ("other", "default")),
        ("fixture data added", False, ("other", "default")),  # \b: 'fixture' is not 'fix'
        (
            "Fixes #12 crash",
            False,
            ("other", "default"),
        ),  # 'Fixes' is not 'fix\\b' either — on the page
    ],
)
def test_classify_commit(subject, merge, expected):
    assert classify_commit(subject, merge, FIX) == expected


# --- §6.1 percentiles [D] ---------------------------------------------------------


def test_ecdf_average_rank_ties():
    p = ecdf_percentiles({"a": 1, "b": 2, "c": 2, "d": 5})
    assert p["a"] == pytest.approx(0.25)
    assert p["b"] == p["c"] == pytest.approx((1 + 1.5) / 4)
    assert p["d"] == pytest.approx(1.0)


def test_ecdf_null_excluded():
    p = ecdf_percentiles({"a": 1, "b": None, "c": 3})
    assert p["b"] is None and p["a"] == pytest.approx(0.5) and p["c"] == pytest.approx(1.0)


def test_nonzero_variant_and_out_of_population_nodes():
    metrics = {
        "a": {"fan_in": 0, "size_loc": 10},
        "b": {"fan_in": 0, "size_loc": 20},
        "c": {"fan_in": 3, "size_loc": 30},
        "d": {"fan_in": 9, "size_loc": 40},
        "t": {
            "fan_in": 9,
            "size_loc": 25,
        },  # test file: outside the population, still ranked against it
    }
    pct = compute_percentiles(metrics, ["a", "b", "c", "d"])
    assert pct["a"]["fan_in_nonzero"] is None and pct["b"]["fan_in_nonzero"] is None
    assert pct["c"]["fan_in_nonzero"] == pytest.approx(0.5)
    assert pct["d"]["fan_in_nonzero"] == pytest.approx(1.0)
    # out-of-population: value 25 sits between 20 and 30 → (2 + 0.5)/4
    assert pct["t"]["size_loc"] == pytest.approx(2.5 / 4)
    assert pct["t"]["fan_in_nonzero"] == pytest.approx(1.0)  # ties with d at the top


# --- §6.2 indices [E] --------------------------------------------------------------


def test_indices_bounded_and_renormalized():
    cfg = SubstrateConfig()
    pct = {
        "fan_in_nonzero": None,
        "centrality": None,
        "fan_out": 0.2,
        "size_loc": 0.8,
        "churn_lines": 0.5,
        "commit_count": 0.5,
        "last_touched_days": 0.5,
        "fix_count_nonzero": None,
        "revert_count": 0.3,
        "age_days": 0.9,
        "nesting_proxy": 0.4,
    }
    m = {"fan_in": 0, "fix_count": 0, "commit_count": 4}
    idx = compute_indices(pct, m, 0.5, 0.25, False, cfg)
    for k, v in idx.items():
        if isinstance(v, float):
            assert 0.0 <= v <= 1.0, k
    # floor file: fan_in_nonzero absent AND fan_in == 0 → contributes 0.0, not dropped (§6.1)
    # centrality absent → weight removed and renormalized → degraded flag set
    assert idx["load_index_degraded"] is True
    assert idx["load_index"] == pytest.approx((0.5 * 0.0 + 0.1 * 0.8 + 0.1 * 0.8) / 0.7)
    assert idx["reinforcement_index"] == 0.5


def test_graph_degraded_drops_graph_inputs():
    cfg = SubstrateConfig()
    pct = {"fan_in_nonzero": 0.9, "centrality": 0.9, "fan_out": 0.5, "size_loc": 0.5}
    idx = compute_indices(
        pct, {"fan_in": 5, "fix_count": 0, "commit_count": 1}, 0.0, None, True, cfg
    )
    assert idx["load_index_degraded"] is True
    assert idx["load_index"] == pytest.approx(
        0.5
    )  # only inv_fan_out and size_loc remain, equal weight


# --- §6.2.2 pagerank [E] ----------------------------------------------------------------


def test_pagerank_deterministic_and_sums_to_one():
    nodes = ["a", "b", "c", "d"]
    edges = {("a", "b"), ("b", "c"), ("c", "a"), ("d", "a")}
    p1 = pagerank(nodes, edges, 0.85, 100, 1e-6)
    p2 = pagerank(list(reversed(nodes)), set(sorted(edges, reverse=True)), 0.85, 100, 1e-6)
    assert p1 == p2
    assert sum(p1.values()) == pytest.approx(1.0, abs=1e-6)
    assert p1["a"] > p1["d"]  # a is pointed to by two nodes; d by none


def test_pagerank_matches_networkx_python_backend():
    nx = pytest.importorskip("networkx")
    from networkx.algorithms.link_analysis.pagerank_alg import _pagerank_python

    nodes = ["n0", "n1", "n2", "n3", "n4", "n5"]
    edges = {("n0", "n1"), ("n1", "n2"), ("n2", "n0"), ("n3", "n0"), ("n4", "n3"), ("n1", "n3")}
    g = nx.DiGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    ref = _pagerank_python(g, alpha=0.85, max_iter=100, tol=1e-6)
    ours = pagerank(nodes, edges, 0.85, 100, 1e-6)
    for n in nodes:
        assert ours[n] == pytest.approx(ref[n], abs=1e-9)


def test_fan_counts_and_edge_contract():
    fi, fo = fan_counts(["a", "b"], {("a", "b")})
    assert fi == {"a": 0, "b": 1} and fo == {"a": 1, "b": 0}


# --- §6.2.2 nesting proxy [E] ------------------------------------------------------------


def test_nesting_proxy_pinned_edge_cases():
    assert nesting_proxy(b"", 10**6) == 0
    assert nesting_proxy(b"a\nb\n", 10**6) == 0
    assert nesting_proxy(b"a\n  b\n    c\n", 10**6) == 2  # modal width 2
    assert (
        nesting_proxy(b"a\n    b\n    c\n        d\n  e\n", 10**6) == 2
    )  # widths {4:2, 8:1, 2:1} → 4; 8//4 = 2
    assert (
        nesting_proxy(b"a\n    b\n        c\n  d\n", 10**6) == 4
    )  # widths {4:1, 8:1, 2:1} tie → 2; 8//2 = 4
    assert nesting_proxy(b"a\n\tb\n\t\tc\n", 10**6) == 2  # tabs = one level each
    assert nesting_proxy(b"a\n  b\n    c\n\t  d\n", 10**6) == 2  # mixed: tabs + spaces//width → 1+1
    assert nesting_proxy(b"a\n  b\n    c\n", 3) is None  # oversize → None
    assert nesting_proxy(b"a\n\n   \nb\n", 10**6) == 0  # blank lines skipped
    assert (
        nesting_proxy(b"a\n  b\n   c\n", 10**6) == 1
    )  # tie {2:1, 3:1} → smaller width 2; 3//2 = 1


def test_count_loc_non_blank():
    assert count_loc(b"a\n\n  \nb\r\n") == 2


# --- §6.2.2 test proximity [E] ------------------------------------------------------------


def test_test_proximity_tiers():
    cfg = SubstrateConfig()
    paths = [
        "lib/rules/foo.js",
        "tests/lib/rules/foo.js",  # mirrored sibling → 1.0
        "src/util/bar.ts",
        "src/util/bar.test.ts",  # same-dir sibling → 1.0
        "src/a/baz.ts",
        "src/a/__tests__/baz.test.ts",  # __tests__ sibling → 1.0
        "src/security/utils/san.ts",
        "test/unit/utils/san.test.js",  # unique stem, different tree → 1.0
        "src/x/index.ts",
        "src/y/index.ts",
        "test/index.test.ts",  # ambiguous stem → 0.5 each
        "src/util/lonely.ts",  # same dir as bar's test → 0.5
        "src/nowhere/zzz.ts",  # → 0.0
    ]
    prox = proximity_tiers(paths, cfg)
    assert prox["lib/rules/foo.js"] == 1.0
    assert prox["src/util/bar.ts"] == 1.0
    assert prox["src/a/baz.ts"] == 1.0
    assert prox["src/security/utils/san.ts"] == 1.0
    assert prox["src/x/index.ts"] == 0.5 and prox["src/y/index.ts"] == 0.5
    assert prox["src/util/lonely.ts"] == 0.5
    assert prox["src/nowhere/zzz.ts"] == 0.0
    assert prox["tests/lib/rules/foo.js"] == 0.0


# --- §5 cochange [C] ---------------------------------------------------------------------


def _c(sha, touched, merge=False):
    from datetime import datetime

    return CommitRecord(
        sha, datetime(2026, 1, 1), "a@b", "x", "other", "default", touched, 0, 0, merge
    )


def test_cochange_degree_threshold_and_caps():
    tl = [
        _c("1", ["a", "b"]),
        _c("2", ["a", "b"]),  # a–b twice → counts
        _c("3", ["a", "c"]),  # a–c once → below cochange_min
        _c("4", ["a", "d"], merge=True),
        _c("5", ["a", "d"], merge=True),  # merges ignored
        _c("6", [f"f{i}" for i in range(40)] + ["a", "b"]),  # bulk commit > cap ignored
    ]
    deg = cochange_degree(tl, cochange_min=2, max_files=30)
    assert deg == {"a": 1, "b": 1}


# --- §3 seed [B] ---------------------------------------------------------------------------


def test_tree_seed_is_content_addressed():
    s1 = tree_seed([("a.ts", "aaaa"), ("b.ts", "bbbb")])
    s2 = tree_seed([("a.ts", "aaaa"), ("b.ts", "bbbb")])
    s3 = tree_seed([("a.ts", "aaaa"), ("b.ts", "cccc")])
    assert s1 == s2 != s3


# --- §3 fingerprint [B] --------------------------------------------------------------------


def test_fingerprint_moves_with_weights_and_toolchain():
    cfg = SubstrateConfig()
    tv = {"history": "pydriller@2.11"}
    f1 = cfg.fingerprint(tv)
    assert f1 == cfg.fingerprint(dict(tv))
    assert f1 != cfg.fingerprint({"history": "pydriller@2.12"})
    from dataclasses import replace

    from repo_substrate.config import IndexWeights

    w = IndexWeights(
        load_index={"fan_in_nonzero": 0.6, "centrality": 0.2, "inv_fan_out": 0.1, "size_loc": 0.1}
    )
    assert replace(cfg, weights=w).fingerprint(tv) != f1


def test_age_ranks_do_not_move_when_the_clock_crosses_a_day_boundary():
    """D-022: integer-day ages let a birth cohort tie or untie with the reference clock;
    fractional days keep the rank order fixed under any advance of as_of."""
    from datetime import UTC, datetime, timedelta

    from repo_substrate.derived import ecdf_percentiles
    from repo_substrate.history import _days

    tz = UTC
    births = {
        "a": datetime(2026, 1, 1, 1, 0, tzinfo=tz),
        "b": datetime(2026, 1, 1, 22, 0, tzinfo=tz),  # same calendar day as a, 21h later
        "c": datetime(2026, 1, 1, 22, 0, tzinfo=tz),  # born with b: a genuine tie
        "d": datetime(2026, 1, 3, 12, 0, tzinfo=tz),
    }
    as_of_1 = datetime(2026, 1, 10, 0, 30, tzinfo=tz)  # a: 8.98d, b: 8.10d — both 8 as integers
    as_of_2 = as_of_1 + timedelta(hours=14)  # crosses a day boundary for a but not for b/c
    # integer days: a and b tie at as_of_1 (both 8 days) and untie at as_of_2 (9 vs 8)
    assert (as_of_1 - births["a"]).days == (as_of_1 - births["b"]).days
    assert (as_of_2 - births["a"]).days != (as_of_2 - births["b"]).days
    # fractional days: the percentiles are identical at both clocks
    p1 = ecdf_percentiles({k: _days(as_of_1, v) for k, v in births.items()})
    p2 = ecdf_percentiles({k: _days(as_of_2, v) for k, v in births.items()})
    assert p1 == p2
    assert p1["b"] == p1["c"] and p1["a"] > p1["b"] > p1["d"]
    assert _days(as_of_1, as_of_2) == 0.0  # never negative


def test_package_facts_resolve_entries_and_owners(make_repo, small_cfg, tmp_path):
    """D-029: package.json entries map to source files (built → source heuristic), and each
    room knows the nearest package directory."""
    from repo_substrate.assemble import ExtractOptions, extract

    r = make_repo()
    r.write(
        "package.json",
        '{"name": "root", "main": "./index.js", "types": "index.d.ts", "bin": {"x": "./bin/cli.js"}}',
    )
    r.write("src/index.ts", "export const a = 1;\n")
    r.write("src/other.ts", "export const b = 2;\n")
    r.write("bin/cli.ts", "console.log(1);\n")
    r.write(
        "packages/sub/package.json",
        '{"name": "sub", "exports": {".": {"import": "./lib/main.mjs", "types": "./lib/main.d.ts"}}}',
    )
    r.write("packages/sub/lib/main.ts", "export const c = 3;\n")
    r.write("packages/sub/lib/helper.ts", "export const d = 4;\n")
    r.commit("feat: packages")
    sub = extract(
        r.path, small_cfg, ExtractOptions(scratch_dir=tmp_path, blame_workers=1), extractor=None
    )
    m = {n["id"]: n["metrics"] for n in sub["nodes"]}
    assert m["src/index.ts"]["is_package_entry"] and m["bin/cli.ts"]["is_package_entry"]
    assert m["packages/sub/lib/main.ts"]["is_package_entry"]
    assert not m["src/other.ts"]["is_package_entry"]
    assert not m["packages/sub/lib/helper.ts"]["is_package_entry"]
    assert (
        m["src/index.ts"]["package"] == ""
        and m["packages/sub/lib/helper.ts"]["package"] == "packages/sub"
    )


def test_built_entries_under_dist_resolve_to_source(make_repo, small_cfg, tmp_path):
    """D-030: the reference manifests point at dist/…; a build directory (and a types/
    segment) is stripped before the source is looked for."""
    from repo_substrate.assemble import ExtractOptions, extract

    r = make_repo()
    r.write(
        "package.json",
        '{"main": "./dist/index.js", "types": "./dist/types/index.d.ts", '
        '"exports": {"./server": {"default": "./dist/security/server.js"}}}',
    )
    r.write("src/index.ts", "export const a = 1;\n")
    r.write("src/security/server.ts", "export const s = 1;\n")
    r.write("src/security/other.ts", "export const o = 1;\n")
    r.commit("feat: built entries")
    sub = extract(
        r.path, small_cfg, ExtractOptions(scratch_dir=tmp_path, blame_workers=1), extractor=None
    )
    m = {n["id"]: n["metrics"] for n in sub["nodes"]}
    assert m["src/index.ts"]["is_package_entry"]
    assert m["src/security/server.ts"]["is_package_entry"]
    assert not m["src/security/other.ts"]["is_package_entry"]
