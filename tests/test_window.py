"""D-083: the window page — one pair of commits, events only, no cause and no grade.

The fixture is two synthetic snapshots built here (window-page-spec.md §8): the pinned mcp
fixture has stripped skeletons and no substrates, and `out/` is not tracked. Each cell
state the renderer can print is reached by a case below.
"""
from __future__ import annotations

import copy
import re

import pytest

from repo_substrate import brief as _b
from repo_substrate.mapper import load_ruleset, map_skeleton
from repo_substrate.mapper.diff import skeleton_diff
from repo_substrate.window import (
    BANNED_WORDS,
    MECHANISM_WORDS,
    NOT_COUNTED_CLOCK,
    NOT_COUNTED_EXCLUDED,
    QUALIFIER_TEXT,
    ROOM_NOTE,
    SCOPE_TEXT,
    UNDER_TABLE_TEXT,
    WindowError,
    render_window,
    window_facts,
)

FP = "f" * 64
A_SHA, B_SHA = "a" * 40, "b" * 40
EDITED = {"f0.ts", "f1.ts", "f2.ts"}

BASE = """[ruleset]
name = "test"
version = "1"
profile = "test"
[[feature]]
name = "large"
predicate = "size_loc >= p90"
[[feature]]
name = "wide"
predicate = "size_loc >= p90 and fan_out >= 1"
[[feature]]
name = "linked"
predicate = "fan_out >= 3"
[[feature]]
name = "fresh"
predicate = "last_touched_days <= p10"
[[feature]]
name = "noisy"
predicate = "bugs >= p90"
decorative = true
decorative_reason = "bugs is unvalidated here"
"""
OVERLAY = """[ruleset]
name = "over"
version = "1"
profile = "onb"
[[feature]]
name = "big"
predicate = "size_loc >= p90"
"""


def _rules(tmp_path):
    (tmp_path / "base.toml").write_text(BASE)
    (tmp_path / "over.toml").write_text(OVERLAY)
    return load_ruleset(tmp_path / "base.toml"), load_ruleset(tmp_path / "over.toml")


def _node(i, size, fan_out=1, touched_days=None, bugs=None):
    return {"id": f"f{i}.ts",
            "metrics": {"size_loc": size, "fan_out": fan_out, "is_test": False, "file_kind": "source",
                        "last_touched_days": 10.0 * i + 5 if touched_days is None else touched_days,
                        "bugs": i if bugs is None else bugs},
            "derived": {"indices": {"load_index": 0.2}, "percentiles": {"age_days": 0.5}}}


def _sub(nodes, sha, timeline):
    return {"repo": {"name": "synthetic", "head_sha": sha, "config_fingerprint": FP}, "seed": sha,
            "nodes": nodes, "summary": {"graph_degraded": False}, "edges": [], "timeline": timeline}


def _snapshots():
    """before: f0..f39, size = index. after, with f0..f2 edited:
    (a) f36 keeps its value and the cutoff passes it          → passes / fails
    (b) f38's own value falls to 30 with no recorded change   → fails / fails
    (c) f20 rises to 200 with no recorded change: an entrant
    (f) f10's fan_out goes 2 → 3: a fixed-value term
    (j) f37's size is null on the later side
    (i) f39 is only in the earlier commit, f40 only in the later
    (k) the first commit in the window is dated before the before-commit"""
    before = [_node(i, i, fan_out=2 if i == 10 else 1) for i in range(40)]
    after = []
    for i in range(39):  # f39 is gone
        size = {0: 100, 1: 101, 2: 102, 38: 30, 20: 200, 37: None}.get(i, i)
        after.append(_node(i, size, fan_out=3 if i == 10 else 1,
                           touched_days=0.1 if i < 3 else 10.0 * i + 55,
                           bugs=100 + i if i < 3 else i))
    after.append(_node(40, 500, touched_days=0.2, bugs=0))
    t0 = [{"sha": A_SHA, "ts": "2026-03-01T12:00:00+00:00", "nodes_touched": []}]
    window = [{"sha": f"{n:040x}", "ts": f"2026-03-{n + 1:02d}T12:00:00+00:00", "nodes_touched": ["f0.ts"]}
              for n in range(1, 25)]
    window[0]["ts"] = "2026-02-20T09:00:00-10:00"  # (k) merged late, authored early
    window.append({"sha": B_SHA, "ts": "2026-03-27T12:00:00+00:00", "nodes_touched": sorted(EDITED)})
    return _sub(before, A_SHA, t0), _sub(after, B_SHA, t0 + window)


def _validation():
    return {"substrate_config_fingerprint": FP, "validation_config_fingerprint": "v" * 64,
            "signals": {"size_loc": {"status": "asserted"}, "fan_out": {"status": "asserted"},
                        "last_touched_days": {"status": "asserted"}, "bugs": {"status": "untested"}}}


def _diff(tmp_path, geometry="age", substrates=True):
    base, over = _rules(tmp_path)
    sa, sb = _snapshots()
    ska = map_skeleton(sa, _validation(), base, overlays=(over,), geometry=geometry)
    skb = map_skeleton(sb, _validation(), base, overlays=(over,), geometry=geometry)
    commits = [{"sha": e["sha"], "ts": e["ts"]} for e in sb["timeline"][1:]]
    return skeleton_diff(ska, skb, touched=set(EDITED), commits_between=25,
                         before_substrate=sa if substrates else None,
                         after_substrate=sb if substrates else None,
                         window_commits=commits if substrates else None), ska, skb


@pytest.fixture
def one(tmp_path):
    d, ska, skb = _diff(tmp_path)
    return d, ska, skb, window_facts([d], ["age.diff.json"], "gate", "synthetic.window.md")


def _line(f, room, term, key="crossings"):
    return next(x for x in f[key] if x["room"] == room and x["term"] == term)


# --- the diff's additive fields ---------------------------------------------------------


def test_row_sizes_count_rooms_only_one_commit_has(one):
    d, ska, skb, _ = one
    pf = d["per_feature"]["test/large"]
    fired = lambda sk: sum(1 for x in sk["features"] if x["feature"] == "large")  # noqa: E731
    assert (pf["rooms_before"], pf["rooms_after"]) == (fired(ska), fired(skb))
    assert pf["born_entered"] == ["f40.ts"] and pf["deleted_left"] == ["f39.ts"]
    # negative control: the common-room counts the operand uses are smaller on both sides
    assert pf["before"] == pf["rooms_before"] - 1 and pf["after"] == pf["rooms_after"] - 1
    assert d["rooms"] == {"born": ["f40.ts"], "deleted": ["f39.ts"]}


def test_excluded_rows_are_carried_outside_per_feature_and_without_evidence(one):
    d = one[0]
    assert "test/noisy" not in d["per_feature"]
    noisy = d["per_decorative_feature"]["test/noisy"]
    assert noisy["untouched_affected_rooms"] and "transition_evidence" not in noisy
    assert d["degraded_marks"] == {"before": 0, "after": 0}


def test_window_times_are_read_over_the_commits_counted_not_the_endpoints(one):
    w = one[0]["budget"]["window"]
    assert w["commit_count"] == 25 and w["before_ts"] == "2026-03-01T12:00:00+00:00"
    assert w["first_ts"] == "2026-02-20T09:00:00-10:00"  # earlier than the before-commit
    assert w["last_ts"] == w["after_ts"] == "2026-03-27T12:00:00+00:00"


def test_identity_records_both_sides_ruleset_overlays_and_both_fingerprints(one):
    i = one[0]["identity"]
    assert i["before"] == i["after"]
    assert i["after"]["ruleset"] == {"name": "test", "version": "1"}
    assert i["after"]["overlays"] == [{"name": "over", "version": "1"}]
    assert i["after"]["validation_config_fingerprint"] == "v" * 64


# --- crossings: two comparisons, never a cause -------------------------------------------


def test_cutoff_passed_it_and_own_value_fell_print_two_comparisons_each(one):
    f = one[3]
    a = _line(f, "f36.ts", "size_loc >= p90")
    assert (a["value_before"], a["value_after"]) == (36, 36)
    assert (a["later_value_vs_earlier_cutoff"], a["earlier_value_vs_later_cutoff"]) == (True, False)
    b = _line(f, "f38.ts", "size_loc >= p90")
    assert (b["value_before"], b["value_after"]) == (38, 30)
    assert (b["later_value_vs_earlier_cutoff"], b["earlier_value_vs_later_cutoff"]) == (False, False)
    page = render_window(f)
    row_a = next(ln for ln in page.splitlines() if "| f36.ts" in ln)
    row_b = next(ln for ln in page.splitlines() if "| f38.ts" in ln)
    assert "| passes | fails |" in row_a and "| fails | fails |" in row_b
    for row in (row_a, row_b):  # the same absence of a cause in both
        assert not any(w in row for w in MECHANISM_WORDS)


def test_an_entrant_is_compared_the_same_way_and_says_entered(one):
    c = _line(one[3], "f20.ts", "size_loc >= p90")
    assert (c["later_value_vs_earlier_cutoff"], c["earlier_value_vs_later_cutoff"]) == (True, False)
    assert all(r["direction"] == "entered" for r in c["rows"])


def test_one_predicate_under_two_profiles_is_one_row_and_a_shared_term_is_one_line(one):
    a = _line(one[3], "f36.ts", "size_loc >= p90")
    labels = [r["label"] for r in a["rows"]]
    assert "large (test) = big (onb)" in labels  # one predicate, two profiles: one entry
    assert "wide (test)" in labels               # a second predicate sharing the term: same line
    assert len(labels) == 2
    assert sum(1 for x in one[3]["crossings"] if x["room"] == "f36.ts") == 1


def test_a_fixed_value_term_has_no_second_comparison(one):
    f = one[3]
    x = _line(f, "f10.ts", "fan_out >= 3")
    assert x["fixed_threshold"] and x["later_value_vs_earlier_cutoff"] is None
    row = next(ln for ln in render_window(f).splitlines() if "| f10.ts" in ln)
    assert "fixed at 3" in row and row.count("fixed threshold") == 2


def test_a_null_outcome_is_not_available_not_a_crossing(one):
    f = one[3]
    x = _line(f, "f37.ts", "not available")
    assert x["state"] == "not_available"
    row = next(ln for ln in render_window(f).splitlines() if "| f37.ts" in ln)
    assert row.count("not available") == 5


def test_rows_column_counts_edited_rooms_and_rooms_only_one_commit_has(one):
    a = _line(one[3], "f36.ts", "size_loc >= p90")
    words = next(r["words"] for r in a["rows"] if r["label"].startswith("large"))
    assert words.startswith("left large (test) = big (onb) (")
    assert "2 edited rooms entered" in words  # f1, f2; f0 at 100 is under the later cutoff
    assert "1 room only in the later commit entered" in words
    assert "1 room only in the earlier commit left" in words


def test_membership_change_with_no_term_change_and_a_missing_side(tmp_path, one):
    d = copy.deepcopy(one[0])
    for name in ("test/large", "onb/big", "test/wide"):
        ev = d["per_feature"][name]["transition_evidence"]["f36.ts"]
        for t_b, t_a in zip(ev["before"]["terms"], ev["after"]["terms"]):
            t_a["passed"] = t_b["passed"]
        ev["after"]["diagnostic_eligible"] = False
    f = window_facts([d], ["x"], "caller")
    x = _line(f, "f36.ts", "none changed outcome")
    assert x["eligibility"]["before"]["diagnostic_eligible"] is True
    assert x["eligibility"]["after"]["diagnostic_eligible"] is False
    assert "none changed outcome" in render_window(f) and "eligible no" in render_window(f)
    bare, _, _ = _diff(tmp_path, substrates=False)  # no substrates: every side unavailable
    g = window_facts([bare], ["x"], "caller")
    assert g["crossings"] and all(x["state"] == "not_available" for x in g["crossings"])
    assert g["window"]["first_ts"] is None and "date not recorded" in render_window(g)


# --- clock rows, excluded rows, bands, the gate's reading --------------------------------


def test_clock_rows_get_the_same_numbers_and_comparisons_and_no_mechanism(one):
    f = one[3]
    assert [r["label"] for r in f["clock_rows"]] == ["fresh (test)"]
    assert f["clock_crossings"] and all(x["term_kind"] == "clock" for x in f["clock_crossings"])
    assert all(x["later_value_vs_earlier_cutoff"] is not None for x in f["clock_crossings"])
    assert not any(x["term"].startswith("last_touched_days") for x in f["crossings"])
    assert f"; {NOT_COUNTED_CLOCK}." in render_window(f)


def test_excluded_rows_are_counted_and_their_rooms_not_named(one):
    f = one[3]
    row = f["excluded_rows"][0]
    assert row["label"] == "noisy (test)" and isinstance(row["unedited_left"], int) and row["unedited_left"] >= 1
    line = next(ln for ln in render_window(f).splitlines() if ln.startswith("- **◌ noisy"))
    assert NOT_COUNTED_EXCLUDED in line and "→" in line
    # D-028: counted, never named — on the page and on the sheet
    assert ".ts" not in line and ".ts" not in str(f["excluded_rows"])
    assert f"{row['unedited_left']} room" in line


def test_two_geometries_are_two_readings_each_beside_its_numbers(tmp_path):
    age, _, _ = _diff(tmp_path, "age")
    layer, _, _ = _diff(tmp_path, "layer")
    f = window_facts([age, layer], ["age.json", "layer.json"], "gate")
    assert [g["geometry"] for g in f["gate_reading"]] == ["age", "layer"]
    assert [b["geometry"] for b in f["bands"]] == ["age", "layer"]
    page = render_window(f)
    assert page.count(" geometry — ") == 2 and page.count("Under the ") == 2
    for g in f["gate_reading"]:
        ft = g["operands"]["features"]
        assert (f"{ft['changes']} of {ft['denominator']} `(profile, feature, room)` assignments; "
                f"{ft['fires_at']} or more of {ft['denominator']} assignments is over 0.05 by the gate's rule") in page
        assert f"`{g['reason'] if g['token'] == 'untested' else g['token']}`" in page


def test_the_operand_named_floors_is_printed_as_bands(one):
    d = copy.deepcopy(one[0])
    d["budget"]["verdict"], d["budget"]["fired"] = "over_budget", ["features", "floors"]
    f = window_facts([d], ["x"], "caller")
    assert f["gate_reading"][0]["fired"] == ["features", "bands"]
    assert "The gate's token: `over_budget`, on features and bands." in render_window(f)
    d["budget"]["verdict"], d["budget"]["fired"], d["budget"]["reason"] = "untested", None, "below_pinned_k"
    assert "Not judged by the gate: `below_pinned_k`." in render_window(window_facts([d], ["x"], "caller"))


# --- the page's fixed text ----------------------------------------------------------------


def test_every_fixed_text_is_on_the_page_and_agrees_with_the_sheet(one):
    f = one[3]
    page = render_window(f)
    assert page.splitlines()[2] == f"**{SCOPE_TEXT}**" == f"**{f['scope_text']}**"
    assert f["origin_text"] in page and "chosen for the gate's test, not for this page" in f["origin_text"]
    assert UNDER_TABLE_TEXT.format(earlier=f["rooms"]["earlier"], later=f["rooms"]["later"]) in page
    assert (f["rooms"]["earlier"], f["rooms"]["later"]) == (40, 40)  # 39 in both + 1 each side
    assert QUALIFIER_TEXT in page and f["qualifier_text"] == QUALIFIER_TEXT
    assert f"{len(f['crossings'])} crossings: one line per room and predicate term" in page
    r = f["rooms"]
    assert (f"{r['common']} rooms are in both commits, 1 only in the later and 1 only in the earlier; "
            f"{r['edited']} of the {r['common']} rooms in both") in page
    assert f["scope"] == "one window" and f["page_file"] == "synthetic.window.md"


def test_the_window_is_in_every_crossing_line_and_the_room_note_too(one):
    page = render_window(one[3])
    rows = [ln for ln in page.splitlines() if ln.startswith("| ") and ".ts" in ln]
    assert rows and all(ln.startswith(f"| {A_SHA[:8]}→{B_SHA[:8]} | ") for ln in rows)
    assert all(f"({ROOM_NOTE})" in ln for ln in rows)


def test_no_property_word_and_no_mechanism_word_in_the_fixed_text(tmp_path):
    age, _, _ = _diff(tmp_path, "age")
    layer, _, _ = _diff(tmp_path, "layer")
    page = render_window(window_facts([age, layer], ["age.json", "layer.json"], "gate"))
    fixed = re.sub(r"`[^`]*`", "", page).lower()  # tokens, terms and hashes are quoted data
    for w in BANNED_WORDS + MECHANISM_WORDS:
        assert w not in fixed, w
    # negative control: the old clock sentence would have been caught
    assert any(w in "a clock row's membership moves with the checkpoint" for w in MECHANISM_WORDS)


# --- refusals ------------------------------------------------------------------------------


def test_refusals_each_with_its_reason(tmp_path):
    age, _, _ = _diff(tmp_path, "age")
    layer, _, _ = _diff(tmp_path, "layer")
    window_facts([age, layer], ["a", "b"])  # negative control: the matching pair is accepted
    with pytest.raises(WindowError, match="both diffs are of the age geometry"):
        window_facts([age, age], ["a", "b"])
    other = copy.deepcopy(layer)
    other["touched"]["nodes"] = other["touched"]["nodes"][:-1]
    with pytest.raises(WindowError, match="not one window: touched.nodes differs"):
        window_facts([age, other], ["a", "b"])
    gate = copy.deepcopy(layer)
    for side in ("before", "after"):
        gate["identity"][side]["validation_config_fingerprint"] = "w" * 64
    with pytest.raises(WindowError, match="not one window: identity differs"):
        window_facts([age, gate], ["a", "b"])
    old = copy.deepcopy(age)
    del old["per_decorative_feature"]
    with pytest.raises(WindowError, match="written before D-083"):
        window_facts([old], ["a"])
    drift = copy.deepcopy(age)
    drift["identity"]["after"]["ruleset"]["version"] = "2"
    with pytest.raises(WindowError, match="mapped under different ruleset"):
        window_facts([drift], ["a"])
    with pytest.raises(WindowError, match="one or two diffs"):
        window_facts([age, layer, age], ["a", "b", "c"])


# --- the brief's pointer --------------------------------------------------------------------


def test_the_brief_points_at_the_window_page_and_takes_no_count_from_it(one):
    _, _, skb, f = one
    ref = _b._window_ref(skb, f)
    assert ref == {"file": "synthetic.window.md", "before_sha": A_SHA, "after_sha": B_SHA,
                   "before_ts": "2026-03-01T12:00:00+00:00", "after_ts": "2026-03-27T12:00:00+00:00"}
    clause = _b._window_clause({"window_ref": ref})
    assert clause == (f"what differed between `{A_SHA[:12]}` (2026-03-01) and this commit is on the "
                      "window page `synthetic.window.md`, not this page")
    assert not re.search(r"\b\d+ (rooms?|crossings?)", clause)
    assert _b._window_clause({"window_ref": None}).startswith("no window page was rendered with this brief")
    assert _b._window_ref(skb, None) is None


def test_the_brief_refuses_a_sheet_about_another_commit_or_another_skeleton(one):
    _, ska, skb, f = one
    with pytest.raises(ValueError, match="not at this skeleton's commit"):
        _b._window_ref(ska, f)
    other = copy.deepcopy(f)
    other["sources"][0]["after_skeleton_hash"] = "0" * 40
    with pytest.raises(ValueError, match="age skeleton is 000000000000"):
        _b._window_ref(skb, other)
