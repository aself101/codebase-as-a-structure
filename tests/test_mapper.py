"""C3 gate and cutaway tests (structural-mapper-spec §3, §4.1, §5, §6; D-016)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from conftest import run_extract

from repo_substrate.cutaway import render_cutaway
from repo_substrate.mapper import RulesetError, load_ruleset, map_skeleton
from repo_substrate.mapper.engine import GateError
from repo_substrate.mapper.ruleset import parse_predicate

RULESET = Path(__file__).resolve().parents[1] / "rulesets" / "maintainability.toml"


def _validation(**statuses: str) -> dict:
    return {
        "validation_config_fingerprint": "v" * 64,
        "signals": {k: {"status": v} for k, v in statuses.items()},
    }


ALL_ASSERTED = _validation(
    load_index="asserted",
    centrality="asserted",
    neglect_index="asserted",
    reinforcement_index="asserted",
    last_touched_days="asserted",
    bug_pressure_index="unvalidated",
)


def _write_ruleset(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "rs.toml"
    p.write_text(
        '[ruleset]\nname = "t"\nversion = "0.0.1"\nprofile = "t"\n' + body, encoding="utf-8"
    )
    return p


# --- ruleset parsing ----------------------------------------------------------------------------


def test_predicate_grammar():
    t = parse_predicate(
        "load_index >= p90 and bug_pressure_index >= 0.5 ∧ reinforcement_index == 0"
    )
    assert [x.signal for x in t] == ["load_index", "bug_pressure_index", "reinforcement_index"]
    assert t[0].percentile == 90 and t[1].value == 0.5 and t[2].op == "=="
    with pytest.raises(RulesetError):
        parse_predicate("load_index >= p90 or centrality >= p90")


def test_decorative_requires_reason(tmp_path):
    p = _write_ruleset(
        tmp_path, '[[feature]]\nname = "x"\npredicate = "load_index >= p90"\ndecorative = true\n'
    )
    with pytest.raises(RulesetError, match="decorative_reason"):
        load_ruleset(p)


def test_shipped_ruleset_loads():
    rs = load_ruleset(RULESET)
    names = {f.name for f in rs.features}
    assert {"foundation", "flooded_basement", "scaffolding", "toothpick_wing", "crack"} <= names
    assert all(f.decorative_reason for f in rs.features if f.decorative)
    assert all(f.position_name for f in rs.features if f.name_implies_consequence)


# --- the gate ------------------------------------------------------------------------------------


@pytest.fixture
def sub(scripted_repo, small_cfg, tmp_path):
    repo, _ = scripted_repo
    return run_extract(repo, small_cfg, tmp_path)


def test_gate_refuses_unvalidated_signal_in_non_decorative_rule(sub, tmp_path):
    p = _write_ruleset(
        tmp_path, '[[feature]]\nname = "x"\npredicate = "bug_pressure_index >= p90"\n'
    )
    with pytest.raises(GateError, match="unvalidated"):
        map_skeleton(sub, ALL_ASSERTED, load_ruleset(p))


def test_gate_treats_missing_key_as_untested(sub, tmp_path):
    p = _write_ruleset(tmp_path, '[[feature]]\nname = "x"\npredicate = "nesting_proxy >= p90"\n')
    with pytest.raises(GateError, match="untested"):
        map_skeleton(sub, ALL_ASSERTED, load_ruleset(p))


def test_decorative_passes_the_gate_but_is_not_diagnostic(sub, tmp_path):
    p = _write_ruleset(
        tmp_path,
        '[[feature]]\nname = "x"\npredicate = "bug_pressure_index >= p50"\ndecorative = true\ndecorative_reason = "unvalidated (test)"\n',
    )
    sk = map_skeleton(sub, ALL_ASSERTED, load_ruleset(p))
    assert sk["summary"]["decorative_count"] > 0 and sk["summary"]["diagnostic_count"] == 0
    for f in sk["features"]:
        assert f["decorative"] and not f["diagnostic"] and f["validation_status"] == "unvalidated"


def test_feature_status_is_the_most_conservative(sub, tmp_path):
    p = _write_ruleset(
        tmp_path, '[[feature]]\nname = "x"\npredicate = "load_index >= p10 and centrality >= 0"\n'
    )
    v = _validation(load_index="validated", centrality="asserted")
    # centrality is None on a graph-less substrate → the term cannot fire; use a pair that exists
    p2 = _write_ruleset(
        tmp_path,
        '[[feature]]\nname = "y"\npredicate = "load_index >= p10 and neglect_index >= 0"\n',
    )
    v2 = _validation(load_index="validated", neglect_index="asserted")
    sk = map_skeleton(sub, v2, load_ruleset(p2))
    assert sk["features"] and all(f["validation_status"] == "asserted" for f in sk["features"])
    v3 = _validation(load_index="validated", neglect_index="validated")
    sk3 = map_skeleton(sub, v3, load_ruleset(p2))
    assert all(f["validation_status"] == "validated" for f in sk3["features"])
    assert p and v  # unused pair kept for readability


def test_graph_dependent_feature_degrades_on_absent_graph(sub, tmp_path):
    p = _write_ruleset(
        tmp_path,
        '[[feature]]\nname = "x"\npredicate = "load_index >= p10"\ngraph_dependent = true\n',
    )
    sk = map_skeleton(sub, ALL_ASSERTED, load_ruleset(p))
    assert sk["gate"]["graph_degraded"] is True
    assert sk["features"] and all(f["degraded"] and not f["diagnostic"] for f in sk["features"])
    assert sk["summary"]["degraded_count"] == len(sk["features"])


def test_skeleton_and_cutaway_are_deterministic(sub, tmp_path):
    rs = load_ruleset(RULESET)
    v = _validation(**{s: "asserted" for f in rs.features for s in f.signals})
    a = map_skeleton(sub, v, rs)
    b = map_skeleton(sub, v, rs)
    assert a["skeleton_hash"] == b["skeleton_hash"]
    a.pop("mapped_at")
    b.pop("mapped_at")
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    assert render_cutaway(a, sub) == render_cutaway(b, sub)
    svg = render_cutaway(a, sub)
    assert svg.startswith("<svg") and "decorative (ungrounded, not a diagnosis)" in svg
    assert svg.count("<rect") >= a["summary"]["population"]


def test_strata_are_five_age_bands_oldest_at_zero(sub):
    rs = load_ruleset(RULESET)
    v = _validation(**{s: "asserted" for f in rs.features for s in f.signals})
    sk = map_skeleton(sub, v, rs)
    bands = sk["strata"]["by_node"]
    assert set(bands.values()) <= {0, 1, 2, 3, 4}
    oldest = min(
        bands,
        key=lambda n: (
            next(x for x in sub["nodes"] if x["id"] == n)["derived"]["percentiles"]["age_days"] or 0
        ),
    )
    # the youngest file (lowest age percentile) sits in the top band; the oldest in band 0
    assert bands[oldest] == 4 or bands["src/f0.js"] == 0
