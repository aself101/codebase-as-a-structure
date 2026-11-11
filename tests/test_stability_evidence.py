"""D-080: transition observables, unknown evidence, and preserved budget operands."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from repo_substrate.cutaway import render_change_sheet
from repo_substrate.mapper import load_ruleset, map_skeleton
from repo_substrate.mapper.diff import skeleton_diff

FP = "f" * 64


def _rules(tmp_path):
    p = tmp_path / "rules.toml"
    p.write_text('[ruleset]\nname = "test"\nversion = "1"\nprofile = "test"\n'
                 '[[feature]]\nname = "large"\npredicate = "size_loc >= p90"\n')
    return load_ruleset(p)


def _substrate(values, sha, edges=()):
    nodes = [{"id": f"f{i}.ts", "metrics": {"size_loc": v, "is_test": False,
              "file_kind": "source"}, "derived": {"indices": {"load_index": 0.2},
              "percentiles": {"age_days": 0.5}}} for i, v in enumerate(values)]
    return {"repo": {"name": "synthetic", "head_sha": sha, "config_fingerprint": FP},
            "seed": sha, "nodes": nodes, "summary": {"graph_degraded": False},
            "edges": [{"from": f"f{a}.ts", "to": f"f{b}.ts"} for a, b in edges]}


def _map(sub, rs, geometry="age"):
    return map_skeleton(sub, {"substrate_config_fingerprint": FP,
                        "signals": {"size_loc": {"status": "asserted"}}}, rs, geometry=geometry)


def test_threshold_crossing_records_the_unfired_side(tmp_path):
    rs = _rules(tmp_path)
    a = _substrate(list(range(40)), "a")
    values = list(range(40))
    values[:5] = [100, 101, 102, 103, 104]
    b = _substrate(values, "b")
    d = skeleton_diff(_map(a, rs), _map(b, rs), touched={f"f{i}.ts" for i in range(5)},
                      commits_between=25, before_substrate=a, after_substrate=b)
    x = d["per_feature"]["test/large"]["transition_evidence"]["f37.ts"]
    assert [x[s]["terms"][0]["value"] for s in ["before", "after"]] == [37, 37]
    assert x["before"]["terms"][0]["threshold"] == pytest.approx(35.1)
    assert x["after"]["terms"][0]["threshold"] == pytest.approx(100.1)
    assert x["before"]["predicate_passed"] is True
    assert x["after"]["predicate_passed"] is False
    assert x["after"]["diagnostic_eligible"] is True
    assert x["after"]["population_n"] == 40
    assert x["after"]["population_floor"]["met"] is True
    svg = render_change_sheet(_map(a, rs), _map(b, rs), b, d, {"test/large": "rank"}, a)
    assert "before:" in svg and "after:" in svg
    assert "threshold=35.1" in svg and "threshold=100.1" in svg


def test_missing_substrate_is_unknown_not_a_failed_predicate(tmp_path):
    rs = _rules(tmp_path)
    a = _map(_substrate(list(range(40)), "a"), rs)
    b = copy.deepcopy(a)
    b["features"] = [f for f in b["features"] if f["node"] != "f37.ts"]
    x = skeleton_diff(a, b)["per_feature"]["test/large"]["transition_evidence"]["f37.ts"]
    assert x["after"]["availability"] == "unavailable"
    assert x["after"]["predicate_passed"] is None
    assert x["after"]["diagnostic_eligible"] is None


def test_evidence_rejects_a_substrate_from_another_revision(tmp_path):
    rs = _rules(tmp_path)
    s = _substrate(list(range(40)), "a")
    sk = _map(s, rs)
    other = copy.deepcopy(s)
    other["repo"]["head_sha"] = "b"
    with pytest.raises(ValueError, match="revision"):
        skeleton_diff(sk, sk, before_substrate=other)


def test_scc_depth_change_is_distinct_from_quantile_band_change(tmp_path):
    rs = _rules(tmp_path)
    edges = [(i, i + 1) for start in [0, 20] for i in range(start, start + 19)]
    a = _substrate(list(range(40)), "a", edges)
    b = _substrate(list(range(40)), "b", edges + [(15, 5)])
    d = skeleton_diff(_map(a, rs, "layer"), _map(b, rs, "layer"),
                      touched={"f15.ts"}, commits_between=25,
                      before_substrate=a, after_substrate=b)
    x = d["strata_evidence"]["f0.ts"]
    assert [x[s]["raw"] for s in ["before", "after"]] == [19, 9]
    assert x["attribution"] == "raw_depth_changed" and x["untouched"]
    y = d["strata_evidence"]["f32.ts"]
    assert [y[s]["raw"] for s in ["before", "after"]] == [7, 7]
    assert y["before"]["band"] != y["after"]["band"]
    assert y["attribution"] == "band_only"
    legacy = copy.deepcopy(_map(a, rs, "layer"))
    legacy["strata"].pop("raw_by_node")
    assert skeleton_diff(legacy, _map(b, rs, "layer"))["strata_evidence"]["f0.ts"]["attribution"] == "unknown"


@pytest.mark.parametrize("geometry", ["age", "layer"])
def test_pinned_mcp_failure_stays_four_assignments_over_thirty_five(geometry):
    fixture = json.loads((Path(__file__).parent / "fixtures/stability-mcp-pinned.json").read_text())[geometry]
    d = skeleton_diff(fixture["before"], fixture["after"], touched=set(fixture["touched"]),
                      commits_between=fixture["commits_between"])
    u = d["untouched"]
    assert u["jitter_assignment_changes"] == 4 and u["jitter_assignment_union"] == 35
    assert u["jitter_churn"] == 4 / 35
    assert u["jitter_affected_rooms"] == ["src/index.ts", "src/types/index.ts"]
    assert u["jitter_affected_room_count"] == 2
    assert u["jitter_room_union"] == 23
    assert d["budget"]["verdict"] == "over_budget"
    assert d["budget"]["feature_churn_max"] == 0.05
    assert u["strata_moved_frac"] == (4 / 35 if geometry == "layer" else 0)


def test_legacy_eligibility_and_missing_value_are_unknown(tmp_path):
    rs = _rules(tmp_path)
    a = _substrate(list(range(40)), "a")
    before = _map(a, rs)
    b = copy.deepcopy(a)
    b["repo"]["head_sha"] = b["seed"] = "b"
    b["nodes"][37]["metrics"]["size_loc"] = None
    after = _map(b, rs)
    after["profile"]["roster"][0].pop("graph_dependent")
    d = skeleton_diff(before, after, before_substrate=a, after_substrate=b)
    x = d["per_feature"]["test/large"]["transition_evidence"]["f37.ts"]["after"]
    assert x["predicate_passed"] is None
    assert x["terms"][0]["reason"] == "value_unavailable"
    assert x["diagnostic_eligible"] is None
    assert x["eligibility_reason"] == "eligibility_metadata_missing"


def test_missing_node_degradation_is_unknown_when_graph_dependent(tmp_path):
    rs = _rules(tmp_path)
    a = _substrate(list(range(40)), "a")
    before = _map(a, rs)
    b = copy.deepcopy(a)
    b["repo"]["head_sha"] = b["seed"] = "b"
    b["nodes"][37]["metrics"]["size_loc"] = 0
    after = _map(b, rs)
    for sk in [before, after]:
        sk["profile"]["roster"][0]["graph_dependent"] = True
    d = skeleton_diff(before, after, before_substrate=a, after_substrate=b)
    x = d["per_feature"]["test/large"]["transition_evidence"]["f37.ts"]["after"]
    assert x["node_load_degraded"] is None
    assert x["diagnostic_eligible"] is None
    assert x["eligibility_reason"] == "eligibility_metadata_missing"
    svg = render_change_sheet(before, after, b, d, {"test/large": "rank"}, a)
    assert "diagnostic eligible=unknown (eligibility_metadata_missing)" in svg
    after["gate"]["graph_degraded"] = True
    known = skeleton_diff(before, after, before_substrate=a, after_substrate=b)
    assert known["per_feature"]["test/large"]["transition_evidence"]["f37.ts"]["after"]["diagnostic_eligible"] is False
    after["gate"]["signals"].pop("size_loc")
    missing_status = skeleton_diff(before, after, before_substrate=a, after_substrate=b)
    assert missing_status["per_feature"]["test/large"]["transition_evidence"]["f37.ts"]["after"]["diagnostic_eligible"] is False


def test_tooltip_discloses_unmet_floor_and_missing_term_reason(tmp_path):
    rs = _rules(tmp_path)
    a = _substrate(list(range(10)), "a")
    b = copy.deepcopy(a)
    b["repo"]["head_sha"] = b["seed"] = "b"
    a["nodes"][9]["metrics"]["size_loc"] = None
    before, after = _map(a, rs), _map(b, rs)
    d = skeleton_diff(before, after, before_substrate=a, after_substrate=b)
    svg = render_change_sheet(before, after, b, d, {"test/large": "rank"}, a)
    assert "population floor: n=10, min=30, met=False" in svg
    assert "unknown (value_unavailable)" in svg


# --- D-082: the verdict carries its resolution, its operand and its window -----------------


def test_fires_at_follows_the_verdicts_strict_comparison():
    from repo_substrate.mapper.diff import fires_at

    assert fires_at(0.05, 35) == 2  # 1/35 = 0.029, 2/35 = 0.057
    assert fires_at(0.05, 20) == 2  # 1/20 is the ceiling, not over it
    assert fires_at(0.05, 60) == 4  # 3/60 is the ceiling
    assert fires_at(0.05, 19) == 1
    assert fires_at(0.05, 0) is None
    for n in range(1, 400):
        k = fires_at(0.05, n)
        assert k / n > 0.05 and (k - 1) / n <= 0.05


def test_floors_admit_a_two_unit_ceiling():
    """The floors do not make either operand a rate: at the minimum admitted sizes two units
    exceed each ceiling. This is what D-026's withdrawn sentence denied."""
    from repo_substrate.mapper.diff import SKELETON_BUDGET, fires_at

    assert fires_at(SKELETON_BUDGET["feature_churn_max"], SKELETON_BUDGET["min_jitter_union"]) == 2
    assert fires_at(SKELETON_BUDGET["strata_moved_max"], SKELETON_BUDGET["min_untouched_n"]) == 2


@pytest.mark.parametrize("geometry", ["age", "layer"])
def test_pinned_mcp_budget_block_states_operand_resolution_and_window(geometry):
    fixture = json.loads((Path(__file__).parent / "fixtures/stability-mcp-pinned.json").read_text())[geometry]
    d = skeleton_diff(fixture["before"], fixture["after"], touched=set(fixture["touched"]),
                      commits_between=fixture["commits_between"])
    b = d["budget"]
    f, s = b["operands"]["features"], b["operands"]["floors"]
    assert (f["changes"], f["denominator"], f["fires_at"], f["distinct_rooms"]) == (4, 35, 2, 2)
    assert f["value"] == d["untouched"]["jitter_churn"] and f["exceeds_ceiling"] is True
    assert (s["denominator"], s["fires_at"]) == (35, 2)
    assert s["changes"] == (4 if geometry == "layer" else 0)
    assert b["fired"] == (["features", "floors"] if geometry == "layer" else ["features"])
    assert b["scope"] == "one window"
    assert b["window"] == {"before_sha": fixture["before"]["repo"]["head_sha"],
                           "after_sha": fixture["after"]["repo"]["head_sha"],
                           "commits_between": fixture["commits_between"]}
    # no substrates supplied: the crossing count is unknown, never zero
    assert f["distinct_crossings"] is None
    assert f["distinct_crossings_reason"] == "transition_evidence_unavailable"
    assert b["verdict"] == "over_budget"  # A changes no verdict


def test_one_room_leaving_two_features_on_one_term_is_one_crossing(tmp_path):
    p = tmp_path / "rules.toml"
    p.write_text('[ruleset]\nname = "test"\nversion = "1"\nprofile = "test"\n'
                 '[[feature]]\nname = "large"\npredicate = "size_loc >= p90"\n'
                 '[[feature]]\nname = "big"\npredicate = "size_loc >= p90"\n')
    rs = load_ruleset(p)
    a = _substrate(list(range(40)), "a")
    values = list(range(40))
    values[:5] = [100, 101, 102, 103, 104]
    b = _substrate(values, "b")
    d = skeleton_diff(_map(a, rs), _map(b, rs), touched={f"f{i}.ts" for i in range(5)},
                      commits_between=25, before_substrate=a, after_substrate=b)
    f = d["budget"]["operands"]["features"]
    assert f["changes"] == 2 * f["distinct_rooms"]  # each room counted under both features
    assert f["distinct_crossings"] == f["distinct_rooms"] and f["distinct_crossings_reason"] is None
    assert f["distinct_crossings"] >= 1


def test_an_unjudged_window_names_no_fired_operand(tmp_path):
    rs = _rules(tmp_path)
    a = _substrate(list(range(40)), "a")
    d = skeleton_diff(_map(a, rs), _map(a, rs), touched=set(), commits_between=5)
    assert d["budget"]["verdict"] == "untested" and d["budget"]["fired"] is None
    assert d["budget"]["operands"]["features"]["exceeds_ceiling"] is False


def test_change_sheet_prints_the_verdicts_scope_and_resolution(tmp_path):
    rs = _rules(tmp_path)
    a = _substrate(list(range(40)), "a")
    values = list(range(40))
    values[:5] = [100, 101, 102, 103, 104]
    b = _substrate(values, "b")
    d = skeleton_diff(_map(a, rs), _map(b, rs), touched={f"f{i}.ts" for i in range(5)},
                      commits_between=25, before_substrate=a, after_substrate=b)
    svg = render_change_sheet(_map(a, rs), _map(b, rs), b, d, {"test/large": "rank"}, a)
    f, s = d["budget"]["operands"]["features"], d["budget"]["operands"]["floors"]
    assert "one window" in svg
    assert f"features {f['changes']} of {f['denominator']} assignments (ceiling exceeded at {f['fires_at']})" in svg
    assert f"floors {s['changes']} of {s['denominator']} rooms (at {s['fires_at']})" in svg
