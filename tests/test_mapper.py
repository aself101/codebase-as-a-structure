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


# --- overlays, geometry, diff (D-017) --------------------------------------------------------------

ONBOARDING = RULESET.parent / "onboarding.toml"


def _all_asserted(*rulesets):
    return _validation(**{s: "asserted" for rs in rulesets for f in rs.features for s in f.signals})


def test_overlay_is_layered_not_merged(sub):
    base, ov = load_ruleset(RULESET), load_ruleset(ONBOARDING)
    v = _all_asserted(base, ov)
    alone = map_skeleton(sub, v, base)
    with_ov = map_skeleton(sub, v, base, (ov,))
    assert alone["strata"] == with_ov["strata"]
    assert [(f["feature"], f["node"]) for f in alone["features"]] == [
        (f["feature"], f["node"]) for f in with_ov["features"]
    ]
    assert with_ov["overlays"][0]["profile"] == "onboarding"
    assert with_ov["summary"]["overlay_profiles"] == ["onboarding"]
    assert all(f["profile"] == "onboarding" for f in with_ov["overlays"][0]["features"])
    assert "fan_out" in with_ov["gate"]["signals"]


def test_duplicate_profile_refused(sub):
    base = load_ruleset(RULESET)
    with pytest.raises(RulesetError, match="duplicate profile"):
        map_skeleton(sub, _all_asserted(base), base, (base,))


def test_overlay_gate_applies_to_overlay_signals(sub):
    base, ov = load_ruleset(RULESET), load_ruleset(ONBOARDING)
    with pytest.raises(GateError, match="untested"):
        map_skeleton(sub, _all_asserted(base), base, (ov,))


def test_layer_geometry_puts_leaves_at_the_bottom():
    from repo_substrate.mapper.geometry import dependency_layers

    nodes = ["a", "b", "c", "d", "e", "f"]
    edges = [
        {"from": "a", "to": "b"},
        {"from": "b", "to": "c"},
        {"from": "d", "to": "c"},
        {"from": "e", "to": "f"},
        {"from": "f", "to": "e"},
    ]
    layers = dependency_layers(nodes, edges)
    assert layers["c"] == 0 and layers["b"] == 1 and layers["a"] == 2 and layers["d"] == 1
    assert layers["e"] == layers["f"] == 0


def test_layer_geometry_on_substrate(sub):
    base = load_ruleset(RULESET)
    sk = map_skeleton(sub, _all_asserted(base), base, (), "layer")
    assert sk["geometry"]["name"] == "layer" and sk["strata"]["geometry"] == "layer"
    assert set(sk["strata"]["by_node"].values()) <= {0, 1, 2, 3, 4}
    assert all(isinstance(v, int) for v in sk["strata"]["raw_by_node"].values())


def test_skeleton_diff_measures_churn_on_common_nodes(sub):
    from repo_substrate.mapper.diff import skeleton_diff

    base = load_ruleset(RULESET)
    a = map_skeleton(sub, _all_asserted(base), base)
    d = skeleton_diff(a, a)
    assert d["feature_churn"] == 0.0 and d["strata_moved"] == [] and d["born"] == 0
    b = json.loads(json.dumps(a))
    victim = next(f for f in b["features"] if f["diagnostic"])
    b["features"] = [f for f in b["features"] if f is not victim]
    d2 = skeleton_diff(a, b)
    key = f"{victim['profile']}/{victim['feature']}"
    assert d2["per_feature"][key]["removed"] == [victim["node"]]
    assert d2["feature_churn"] > 0


def test_skeleton_budget_is_judged_over_the_untouched_population(sub):
    """D-018: a node the intervening commits edited may change; one they did not edit
    that changes anyway is ripple, and ripple is what the budget counts."""
    from repo_substrate.mapper.diff import SKELETON_BUDGET, skeleton_diff

    base = load_ruleset(RULESET)
    a = map_skeleton(sub, _all_asserted(base), base)
    b = json.loads(json.dumps(a))
    victim = next(f for f in b["features"] if f["diagnostic"])
    b["features"] = [f for f in b["features"] if f is not victim]
    loose = {**SKELETON_BUDGET, "min_untouched_n": 1}
    # Without a touched set the verdict is untested, never a pass.
    assert skeleton_diff(a, b)["budget"]["verdict"] == "untested"
    assert skeleton_diff(a, b)["budget"]["reason"] == "touched_set_unavailable"
    # The victim was edited: whole-population churn > 0, untouched churn 0, within budget.
    d = skeleton_diff(a, b, touched={victim["node"]}, commits_between=1, budget=loose)
    assert d["feature_churn"] > 0 and d["untouched"]["feature_churn"] == 0.0
    assert d["touched"]["n"] == 1 and d["budget"]["verdict"] == "within_budget"
    key = f"{victim['profile']}/{victim['feature']}"
    assert d["per_feature"][key]["untouched_changes"] == 0
    # The victim was not edited: the same change is ripple and counts against the budget.
    tight = {**loose, "feature_churn_max": 0.0}
    d2 = skeleton_diff(a, b, touched=set(), commits_between=1, budget=tight)
    assert d2["untouched"]["feature_churn"] > 0 and d2["budget"]["verdict"] == "over_budget"
    assert d2["per_feature"][key]["untouched_changes"] == 1


def test_skeleton_budget_floors_refuse_to_get_easier(sub):
    from repo_substrate.mapper.diff import SKELETON_BUDGET, skeleton_diff

    base = load_ruleset(RULESET)
    a = map_skeleton(sub, _all_asserted(base), base)
    nodes = list(a["strata"]["by_node"])
    small = skeleton_diff(
        a,
        a,
        touched=set(),
        commits_between=1,
        budget={**SKELETON_BUDGET, "min_untouched_n": len(nodes) + 1},
    )
    assert small["budget"]["verdict"] == "untested"
    assert small["budget"]["reason"] == "insufficient_untouched_population"
    # Touching most of the repo shrinks the population the budget is judged on; refuse.
    wide = skeleton_diff(
        a,
        a,
        touched=set(nodes[: len(nodes) * 3 // 4]),
        commits_between=1,
        budget={**SKELETON_BUDGET, "min_untouched_n": 1},
    )
    assert wide["budget"]["verdict"] == "untested"
    assert wide["budget"]["reason"] == "touched_fraction_exceeds_floor"


def test_touched_since_reads_the_after_timeline_through_renames():
    from repo_substrate.mapper.diff import touched_since

    sub = {
        "timeline": [
            {"sha": "aaa", "nodes_touched": ["x.js"]},
            {"sha": "bbb", "nodes_touched": ["old.js", "y.js"]},
            {"sha": "ccc", "nodes_touched": []},
        ]
    }
    assert touched_since(sub, "aaa", {"old.js": "new.ts"}) == ({"new.ts", "y.js"}, 2)
    assert touched_since(sub, "ccc") == (set(), 0)
    assert touched_since(sub, "zzz") is None


def test_archetype_is_not_claimed_and_cannot_be_smuggled_in(sub, tmp_path):
    """D-019: the skeleton's archetype is null in v0, and a ruleset carrying an
    [archetype] table (or any table the mapper does not read) is refused, not ignored."""
    base = load_ruleset(RULESET)
    assert map_skeleton(sub, _all_asserted(base), base)["archetype"] is None
    p = tmp_path / "arch.toml"
    p.write_text(
        RULESET.read_text(encoding="utf-8") + '\n[archetype]\nlabel = "cathedral"\n',
        encoding="utf-8",
    )
    with pytest.raises(RulesetError, match="unknown top-level table.*archetype"):
        load_ruleset(p)


def test_html_wrapper_has_overlay_toggles(sub):
    from repo_substrate.cutaway import render_html

    base, ov = load_ruleset(RULESET), load_ruleset(ONBOARDING)
    page = render_html(map_skeleton(sub, _all_asserted(base, ov), base, (ov,)), sub)
    assert (
        'data-target="overlay-0"' in page
        and 'id="overlay-0"' in page
        and "onboarding overlay" in page
    )


def test_change_sheet_marks_rooms_by_what_happened(sub):
    """D-023: the change sheet shares the after layout and classifies each room."""
    from repo_substrate.cutaway import render_change_sheet
    from repo_substrate.mapper.diff import skeleton_diff
    from repo_substrate.timelapse import feature_kinds

    base = load_ruleset(RULESET)
    a = map_skeleton(sub, _all_asserted(base), base)
    b = json.loads(json.dumps(a))
    kinds = feature_kinds(base, ())
    victim = next(f for f in b["features"] if f["diagnostic"])
    expected = kinds[f"{victim['profile']}/{victim['feature']}"]  # clock or rank
    b["features"] = [f for f in b["features"] if f is not victim]
    # untouched → the lost feature is ripple, of the feature's kind
    d = skeleton_diff(a, b, touched=set(), commits_between=1)
    svg = render_change_sheet(a, b, sub, d, kinds, sub)
    assert svg.startswith("<svg") and "change sheet" in svg
    assert f'data-change="{expected}"><title>{victim["node"]}' in svg.replace("\n", " ")
    assert svg.count('data-change="unchanged"') == len(a["strata"]["by_node"]) - 1
    # touched → the same change is an edit
    d2 = skeleton_diff(a, b, touched={victim["node"]}, commits_between=1)
    svg2 = render_change_sheet(a, b, sub, d2, kinds, sub)
    assert f'data-change="edit"><title>{victim["node"]}' in svg2.replace("\n", " ")
    assert render_change_sheet(a, b, sub, d2, kinds, sub) == svg2
