"""M3 — the architect brief and the register lint (architect-brief-spec.md, D-027)."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from repo_substrate.brief import facts, lint, run_brief
from repo_substrate.mapper import load_ruleset, map_skeleton

from conftest import run_extract

RULESET = Path(__file__).resolve().parents[1] / "rulesets" / "maintainability.toml"
ONBOARDING = RULESET.parent / "onboarding.toml"


TEST_FP = "t" * 64


@pytest.fixture
def sub(scripted_repo, small_cfg, tmp_path):
    repo, _ = scripted_repo
    doc = run_extract(repo, small_cfg, tmp_path)
    doc["repo"]["config_fingerprint"] = TEST_FP  # bound to the test validation documents (D-034)
    return doc


def _validation(*rulesets, **override):
    st = {s: "asserted" for rs in rulesets for f in rs.features for s in f.signals}
    st.update(override)
    return {
        "validation_config_fingerprint": "v" * 64,
        "substrate_config_fingerprint": TEST_FP,
        "signals": {k: {"status": v} for k, v in st.items()},
    }


def _skeleton(sub):
    base, ov = load_ruleset(RULESET), load_ruleset(ONBOARDING)
    return map_skeleton(sub, _validation(base, ov, bug_pressure_index="unvalidated"), base, (ov,))


def test_facts_sheet_is_the_closed_set(sub):
    sk = _skeleton(sub)
    f = facts(sk, sub)
    assert (
        f["population"] == sk["summary"]["population"] and f["skeleton_hash"] == sk["skeleton_hash"]
    )
    names = {x["feature"] for x in f["features"]}
    assert {x["feature"] for x in sk["features"]} <= names
    dec = [x for x in f["features"] if x["decorative"]]
    assert (
        all(not x["diagnostic"] for x in dec)
        and f["decorative"]["count"] == sk["summary"]["decorative_count"]
    )
    assert facts(sk, sub)["facts_hash"] == f["facts_hash"]  # deterministic


def _good_draft(f):
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"])
    room = feat["rooms"][0]
    wing, n = next(iter(f["wings"].items()))
    text = (
        f"The building has {f['population']} rooms and {f['diagnostic_count']} diagnostic marks; the wing {wing} holds {n} of them, among them {feat['feature']}'s {room} [{feat['feature']}: {room}].\n\n"
        f"The room {room} sits where {feat['feature']} fires [{feat['feature']} ×{feat['count']}].\n\n"
    )
    if f["decorative"]["count"]:
        names = ", ".join(
            x["feature"] + (f" — {x['position_name']}" if x.get("position_name") else "")
            for x in f["features"]
            if x["decorative"]
        )
        cites = "; ".join(f"{x['feature']} ×{x['count']}" for x in f["features"] if x["decorative"])
        sigs = sorted(
            {
                s
                for x in f["features"]
                if x["decorative"]
                for s in re.findall(r"[a-z_]+_index", x.get("decorative_reason") or "")
            }
        )
        text += f"{f['decorative']['count']} decorative marks ({names}) render but are not a diagnosis; they rest on {', '.join(sigs) or 'nothing confirmed'}, which is unvalidated [{cites}].\n\n"
    return text


def test_lint_passes_a_disciplined_draft(sub):
    f = facts(_skeleton(sub), sub)
    assert lint(_good_draft(f), f) == []


def test_lint_catches_each_register_breach(sub):
    f = facts(_skeleton(sub), sub)
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"])
    room = feat["rooms"][0]
    good = _good_draft(f)

    def rules(text):
        return {v.rule for v in lint(text, f)}

    assert "R1-consequence" in rules(
        good + f"Changing {room} will break much [{feat['feature']}: {room}].\n\n"
    )
    assert "R2-provenance" in rules(good + "A paragraph with no citation at all.\n\n")
    assert "R2-provenance" in rules(good + f"A phantom [{feat['feature']}: not/a/room.ts].\n\n")
    assert "R2-provenance" in rules(
        good + f"Wrong count [{feat['feature']} ×{feat['count'] + 1}].\n\n"
    )
    assert "R3-number" in rules(good + f"There are 424242 rooms [{feat['feature']}: {room}].\n\n")
    other = next(
        x
        for x in f["features"]
        if x["diagnostic"] and x["feature"] != feat["feature"] and room not in x["rooms"]
    )
    assert "R8-attribution" in rules(
        good + f"The room {room} carries the mark [{other['feature']} ×{other['count']}].\n\n"
    )
    assert "R8-attribution" not in rules(
        good + f"The room {room} sits here [{feat['feature']}: {room}].\n\n"
    )
    assert "R7-counts" in rules(good.replace(str(f["diagnostic_count"]), "many", 1))
    # the disclosure clause is not an amnesty for the rest of the sentence
    assert "R1-consequence" in rules(
        good
        + f"This room is fragile, not a claim about what breaks [{feat['feature']}: {room}].\n\n"
    )
    assert "R1-consequence" in rules(
        good + f"Against that, other rooms hold reinforcement [{feat['feature']}: {room}].\n\n"
    )
    assert "R6-archetype" in rules(good + f"It is a cathedral [{feat['feature']}: {room}].\n\n")
    if f["decorative"]["features"]:
        dec = f["decorative"]["features"][0]
        assert "R4-decorative" in rules(
            good + f"The {dec} marks a diagnosis [{dec} ×{f['decorative']['count']}].\n\n"
        )
        assert "R7-decorative-count" in rules(good.replace(str(f["decorative"]["count"]), "many"))
        from repo_substrate.brief import WORD_NUMBERS

        word = next((w for w, v in WORD_NUMBERS.items() if v == f["decorative"]["count"]), None)
        if word:
            assert "R7-decorative-count" not in rules(
                good.replace(str(f["decorative"]["count"]), word.capitalize(), 1)
            )
    imp = next(
        (x for x in f["features"] if x["diagnostic"] and x["name_implies_consequence"]), None
    )
    if imp:
        assert "R5-disclosure" in rules(
            good + f"The foundation is here [{imp['feature']} ×{imp['count']}].\n\n"
        )
        disclosed = (
            good
            + f"The {imp['feature']} — {imp['position_name']} — denotes position, not a claim about what breaks [{imp['feature']} ×{imp['count']}].\n\n"
        )
        assert "R5-disclosure" not in rules(disclosed) and "R1-consequence" not in rules(disclosed)


def test_run_brief_regenerates_once_and_marks_failure(sub):
    sk = _skeleton(sub)
    f = facts(sk, sub)
    good = _good_draft(f)
    calls = []

    def fake(system, user):
        calls.append(user)
        return (good + "This will break." if len(calls) == 1 else good), {"model_served": "fake"}

    r = run_brief(sk, sub, fake)
    assert r["passed"] and r["provenance"]["attempt"] == 2 and "FAILED" in calls[1]
    assert (
        "Register lint: **PASS on attempt 2**" in r["markdown"] and "## Provenance" in r["markdown"]
    )
    r2 = run_brief(sk, sub, lambda s, u: (good + "It will fail.", {}), max_attempts=1)
    assert not r2["passed"] and "FAILED (" in r2["markdown"] and len(r2["violations"]) >= 1
    r3 = run_brief(sk, sub, draft=good)
    assert r3["passed"] and r3["provenance"]["generator"] == "draft"
    json.dumps(r3["facts"])  # serializable


def test_relint_keeps_prose_and_provenance(sub):
    from repo_substrate.brief import relint

    sk = _skeleton(sub)
    f = facts(sk, sub)
    good = _good_draft(f)
    r = run_brief(sk, sub, lambda s, u: (good, {"model_served": "fake", "request_id": "req_1"}))
    r2 = relint(r["markdown"], sk, sub)
    assert r2["passed"] and r2["text"].strip() == good.strip()
    assert r2["provenance"]["model_served"] == "fake" and r2["provenance"]["request_id"] == "req_1"
    assert "relinted" in r2["provenance"]
    # generation-time lint and relint must agree on the same prose
    bad = good + "Changing it will break much.\n\n"
    r3 = run_brief(sk, sub, lambda s, u: (bad, {}), max_attempts=1)
    r4 = relint(r3["markdown"], sk, sub)
    assert [v["rule"] for v in r3["violations"]] == [v["rule"] for v in r4["violations"]]


def test_d030_lint_closes_the_perverse_routes(sub):
    """D-030: exemptions are narrow, numbers are paragraph-scoped, counts sit outside
    citations, attempts are bounded and logged."""
    from repo_substrate.brief import MAX_ATTEMPTS_CAP

    sk = _skeleton(sub)
    f = facts(sk, sub)
    good = _good_draft(f)
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"])
    room = feat["rooms"][0]

    def rules(text):
        return {v.rule for v in lint(text, f)}

    # a phrase of the stance does not exempt an uncited paragraph; the stance paragraph itself does
    assert "R2-provenance" in rules(
        good + "No citation here, which presupposes a norm of health.\n\n"
    )
    assert "R2-provenance" not in rules(good + f["stance"] + "\n\n")
    # a room's metrics are allowed only where the room is named
    lines = f["rooms"][room]["lines"]
    if lines not in {
        f["population"],
        f["diagnostic_count"],
        f["decorative"]["count"],
        f["co_located_rooms"],
        *f["wings"].values(),
        *(x["count"] for x in f["features"]),
    }:
        assert "R3-number" in rules(
            good + f"There are {lines} things [{feat['feature']} ×{feat['count']}].\n\n"
        )
        assert "R3-number" not in rules(
            good + f"The room {room} has {lines} lines [{feat['feature']}: {room}].\n\n"
        )
    # counts must be stated outside citations
    only_cited = good.replace(f"{f['diagnostic_count']} diagnostic marks", "diagnostic marks")
    assert (
        "R7-counts" in rules(only_cited + f"[{feat['feature']} ×{f['diagnostic_count']}]\n\n")
        or str(f["diagnostic_count"]) in only_cited
    )
    # attempts are capped and logged
    calls = []

    def always_bad(system, user):
        calls.append(1)
        return good + "It will break.\n\n", {}

    r = run_brief(sk, sub, always_bad, max_attempts=10)
    assert len(calls) == MAX_ATTEMPTS_CAP and not r["passed"]
    assert r["provenance"]["attempts_log"].count("R1-consequence") == MAX_ATTEMPTS_CAP


def test_lint_reads_chained_brackets_and_the_determiner_one(sub):
    """D-032 addendum: [f ×N; g ×M] and [f ×N, g ×M] are several citations in one bracket;
    the word "one" is a determiner, not a measurement; a room under a count must share its bracket."""
    f = facts(_skeleton(sub), sub)
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"])
    other = next(x for x in f["features"] if x["diagnostic"] and x is not feat)
    # a consequence-implying name must be disclosed where first used (R5); do it in the chained sentence
    disclose = (
        f"{other['feature']} — {other['position_name']} — and "
        if other["name_implies_consequence"]
        else ""
    )
    room = feat["rooms"][0]
    base = _good_draft(f)
    chained = base + (
        f"{disclose}{feat['feature']} and {other['feature']} share one bracket [{feat['feature']} ×{feat['count']}; {other['feature']} ×{other['count']}].\n\n"
        f"{disclose}{feat['feature']} and {other['feature']} once more in the comma form [{feat['feature']} ×{feat['count']}, {other['feature']} ×{other['count']}].\n\n"
    )
    assert lint(chained, f) == []
    wrong_count = (
        base
        + f"{disclose}{feat['feature']} and {other['feature']} bad [{feat['feature']} ×{feat['count'] + 1}; {other['feature']} ×{other['count']}].\n\n"
    )
    assert {v.rule for v in lint(wrong_count, f)} == {"R2-provenance"}
    hybrid = (
        base + f"{feat['feature']} under a count [{feat['feature']} ×{feat['count']}: {room}].\n\n"
    )
    assert lint(hybrid, f) == []
    later = (
        base
        + f"A count here [{feat['feature']} ×{feat['count']}]. The room {room} is named here without one.\n\n"
    )
    assert "R8-attribution" in {v.rule for v in lint(later, f)}


def test_lint_reads_compound_spelled_numbers(sub):
    """D-032 addendum: 'two hundred sixty-seven' is one number, checked against the sheet as 267."""
    from repo_substrate.brief import _spelled_numbers

    assert dict(
        _spelled_numbers(
            "two hundred sixty-seven rooms, one hundred and thirty-three marks, twenty-one"
        )
    ) == {
        "two hundred sixty-seven": 267,
        "one hundred and thirty-three": 133,
        "twenty-one": 21,
    }
    assert list(_spelled_numbers("the seventy-fifth percentile")) == []
    f = facts(_skeleton(sub), sub)
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"])
    pop_words = {7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}.get(
        f["population"]
    )
    if pop_words is None:
        pytest.skip("scripted repo population outside the spelled range")
    ok = (
        _good_draft(f)
        + f"The building holds {pop_words} rooms in all [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R3-number" not in {v.rule for v in lint(ok, f)}
    bad = (
        _good_draft(f)
        + f"The building holds one thousand rooms [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R3-number" in {v.rule for v in lint(bad, f)}


def test_lint_reads_the_connective_prose(sub):
    """D-036 (hostile reading, run 17): the sentences between the brackets are checked —
    identical or nested room sets named together (R9), a named directory contains a cited
    room (R10), no distributional adverb (R11), and a number binds to the sentence that cites
    its feature (R3)."""
    f = facts(_skeleton(sub), sub)
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"])
    room = feat["rooms"][0]
    base = _good_draft(f)
    assert lint(base, f) == []
    # R3: a feature's count in a sentence that cites another feature is refused
    other = next(
        (
            x
            for x in f["features"]
            if x["diagnostic"] and x is not feat and x["count"] != feat["count"]
        ),
        None,
    )
    if other is not None:
        loose = (
            base
            + f"There are {other['count']} such rooms [{feat['feature']} ×{feat['count']}].\n\n"
        )
        assert "R3-number" in {v.rule for v in lint(loose, f)}
    # R11
    adverb = base + f"They sit mostly in src [{feat['feature']} ×{feat['count']}].\n\n"
    assert "R11-share" in {v.rule for v in lint(adverb, f)}
    # R9: declare an overlap the prose does not name together
    g = dict(f)
    g["overlaps"] = [
        {
            "a": f"{feat['profile']}/{feat['feature']}",
            "b": "p/other_mark",
            "relation": "identical",
            "n": feat["count"],
        }
    ]
    assert "R9-overlap" in {v.rule for v in lint(base, g)}
    named = (
        base
        + f"The {feat['feature']} rooms are the other_mark rooms [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R9-overlap" not in {v.rule for v in lint(named, g)}
    # R10: a directory of the building named without a cited room inside it
    h = json.loads(json.dumps(f))
    deep = dict(feat)
    deep.update(
        {
            "feature": "deep_mark",
            "profile": feat["profile"],
            "rooms": ["lib/inner/a.js", "lib/inner/b.js"],
            "count": 2,
            "by_wing": {"lib": 2},
        }
    )
    h["features"].append(deep)
    prefix = base + f"Two rooms sit in lib/inner [{feat['feature']} ×{feat['count']}].\n\n"
    rules = {v.rule for v in lint(prefix, h)}
    assert "R10-prefix" in rules
    ok = base + f"Two rooms sit in lib/inner [deep_mark: lib/inner/a.js, lib/inner/b.js].\n\n"
    assert "R10-prefix" not in {v.rule for v in lint(ok, h)}


def test_facts_sheet_carries_overlaps_wing_counts_and_all_profile_co_location(sub):
    f = facts(_skeleton(sub), sub)
    assert "overlaps" in f and "co_located_rooms" in f and f["gate_fingerprint"]
    for x in f["features"]:
        assert sum(x["by_wing"].values()) == x["count"]
    assert f["units"]["co_located_rooms"].startswith("rooms")
    for x in f["features"]:
        assert x["dominant_dir"]["n"] <= x["count"]


def test_lint_types_the_sheet(sub):
    """D-037 (second seating, run 18): a number wears its unit (R12), an identity between
    differing predicates names the inert conjunct (R13), 'validated' is refused where no signal
    holds it (R14), a feature's dominant directory is named and cited (R15), rankings are refused."""
    f = facts(_skeleton(sub), sub)
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"])
    base = _good_draft(f)
    assert lint(base, f) == []
    # R12: the diagnostic-mark count called rooms; the population called marks
    if f["diagnostic_count"] not in {x["count"] for x in f["features"]} | {f["population"]}:
        bad = (
            base
            + f"There are {f['diagnostic_count']} rooms in all [{feat['feature']} ×{feat['count']}].\n\n"
        )
        assert "R12-unit" in {v.rule for v in lint(bad, f)}
    if f["population"] not in {x["count"] for x in f["features"]}:
        bad = (
            base
            + f"The survey records {f['population']} marks [{feat['feature']} ×{feat['count']}].\n\n"
        )
        assert "R12-unit" in {v.rule for v in lint(bad, f)}
    # R14
    val = (
        base
        + f"None of these rests on a validated measure [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R14-status" in {v.rule for v in lint(val, f)}
    # R11 ranking
    rank = base + f"The widest set is {feat['feature']} [{feat['feature']} ×{feat['count']}].\n\n"
    assert "R11-share" in {v.rule for v in lint(rank, f)}
    # R13: an identical overlap with an inert conjunct must say the signal excludes nothing
    g = dict(f)
    key = f"{feat['profile']}/{feat['feature']}"
    g["overlaps"] = [
        {
            "a": key,
            "b": "p/other_mark",
            "relation": "identical",
            "n": feat["count"],
            "inert_terms": ["load_index >= 0.10"],
        }
    ]
    together = (
        base
        + f"The {feat['feature']} rooms are the other_mark rooms [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R13-inert" in {v.rule for v in lint(together, g)}
    said = (
        base
        + f"The {feat['feature']} rooms are the other_mark rooms; load_index excludes nothing here [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R13-inert" not in {v.rule for v in lint(said, g)}
    # R15: a feature whose rooms sit in one directory must name it where cited
    h = json.loads(json.dumps(f))
    rooms = [f"lib/inner/{i}.js" for i in range(6)]
    deep = dict(feat)
    deep.update(
        {
            "feature": "deep_mark",
            "rooms": rooms,
            "count": 6,
            "by_wing": {"lib": 6},
            "dominant_dir": {"dir": "lib/inner", "n": 6, "population": 9},
        }
    )
    h["features"].append(deep)
    silent = base + f"Six rooms carry deep_mark [deep_mark ×6].\n\n"
    assert "R15-composition" in {v.rule for v in lint(silent, h)}
    shown = (
        base
        + f"Six rooms carry deep_mark, all 6 in lib/inner, which holds 9 rooms [deep_mark ×6: lib/inner/0.js].\n\n"
    )
    rules = {v.rule for v in lint(shown, h)}
    assert "R15-composition" not in rules and "R10-prefix" not in rules


def test_lint_reads_nestings_shared_predicates_and_the_decorative_reason(sub):
    """D-038 (third seating, run 19): a within overlap states the rooms outside and no identity
    noun; an identical overlap with a shared predicate says so; 'findings' is not a unit."""
    f = facts(_skeleton(sub), sub)
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"])
    base = _good_draft(f)
    key = f"{feat['profile']}/{feat['feature']}"
    g = dict(f)
    g["overlaps"] = [
        {"a": key, "b": "p/wider_mark", "relation": "within", "n": feat["count"], "n_outside": 8}
    ]
    ident = (
        base
        + f"The {feat['feature']} rooms and the wider_mark rooms are one set of rooms [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R13-inert" in {v.rule for v in lint(ident, g)}
    nested = (
        base
        + f"The {feat['feature']} rooms sit within wider_mark, which marks 8 rooms outside them [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R13-inert" not in {v.rule for v in lint(nested, g)}
    g["overlaps"] = [
        {
            "a": key,
            "b": "p/twin_mark",
            "relation": "identical",
            "n": feat["count"],
            "inert_terms": [],
            "shared_predicate": True,
        }
    ]
    agree = (
        base
        + f"The {feat['feature']} rooms are the twin_mark rooms [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R13-inert" in {v.rule for v in lint(agree, g)}
    same = (
        base
        + f"The {feat['feature']} rooms are the twin_mark rooms: the same predicate under two profiles [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R13-inert" not in {v.rule for v in lint(same, g)}
    finding = base + f"One finding, two marks [{feat['feature']} ×{feat['count']}].\n\n"
    assert "R12-unit" in {v.rule for v in lint(finding, f)}


def test_register_table_carries_the_inventory_and_the_prose_is_the_reading(sub):
    """D-039: the page carries a register rendered by code; relint recovers only the prose; with
    the register present the inventory obligations (R7, R9/R13 naming, R15, R4b) are met by it
    while the refusals still bind the prose."""
    from repo_substrate.brief import relint, render_brief, render_register

    f = facts(_skeleton(sub), sub)
    table = render_register(f)
    for x in f["features"]:
        assert (
            x["feature"] in table
            and (x["position_name"] or "no consequence word in the name") in table
        )
        assert f"{x['count']} |" in table
    assert str(f["co_located_rooms"]) in table and "none validated" in table
    prose = _good_draft(f)
    page = render_brief(prose, f, [], {"generator": "draft"})
    assert (
        "## Register" in page
        and "## Reading" in page
        and page.index("## Register") < page.index("## Reading")
    )
    r = relint(page, _skeleton(sub), sub)
    assert r["text"].strip() == prose.strip() and r["passed"]
    # a nesting called one set is still refused with the register present
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"])
    g = dict(f)
    key = f"{feat['profile']}/{feat['feature']}"
    g["overlaps"] = [
        {"a": key, "b": "p/wider_mark", "relation": "within", "n": feat["count"], "n_outside": 8}
    ]
    ident = (
        prose
        + f"The {feat['feature']} rooms and the wider_mark rooms are one set of rooms [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R13-inert" in {v.rule for v in lint(ident, g, register=True)}
    # but the obligation to name the pair is the register's, not the prose's
    assert "R9-overlap" not in {v.rule for v in lint(prose, g, register=True)}
    assert "R9-overlap" in {v.rule for v in lint(prose, g)}


def test_register_cells_are_linted_by_their_tests(sub):
    """D-040: the register's derived cells are claims — the tests are its lint. The ⊂ cell says whose
    rooms are outside; a directory below the third prints none; the building line says how many
    marks fall on identical pairs twice and how many distinct room sets the diagnosis names; the
    reading may not restate the register's by-wing numbers."""
    from repo_substrate.brief import render_register

    f = facts(_skeleton(sub), sub)
    assert f["distinct_room_sets"] == sum(
        1 for x in f["features"] if x["diagnostic"] and x["rooms"]
    ) - sum(1 for o in f["overlaps"] if o["relation"] == "identical" and o.get("diagnostic"))
    for x in f["features"]:
        dd = x["dominant_dir"]
        assert dd["holds_third"] == (dd["n"] * 3 >= x["count"]) and dd["placeable"] == (
            x["count"] >= 6
        )
    g = json.loads(json.dumps(f))
    feat = next(x for x in g["features"] if x["diagnostic"])
    key = f"{feat['profile']}/{feat['feature']}"
    g["overlaps"] = [
        {"a": key, "b": "p/wider", "relation": "within", "n": feat["count"], "n_outside": 8}
    ]
    g["features"].append({**feat, "feature": "wider", "profile": "p", "count": feat["count"] + 8})
    table = render_register(g)
    assert "⊂ wider (8 wider rooms outside this set)" in table
    assert "8 of these rooms outside it" in table
    assert "of its rooms outside" not in table
    low = dict(feat)
    low.update(
        {
            "feature": "thin_mark",
            "count": 12,
            "dominant_dir": {
                "dir": "x/y",
                "n": 2,
                "population": 5,
                "tied": True,
                "holds_third": False,
            },
        }
    )
    g["features"].append(low)
    assert "none holds a third" in render_register(g)
    assert (
        "distinct sets of rooms" in table
        and "rooms twice" in table
        and "under one predicate in two profiles" in table
    )
    base = _good_draft(f)
    wing, n = next(iter(feat["by_wing"].items()))
    if n != feat["count"] and n not in {f["population"], *f["wings"].values()}:
        restated = (
            base
            + f"{feat['feature']} puts {n} of its rooms in {wing} [{feat['feature']} ×{feat['count']}].\n\n"
        )
        assert "R16-restatement" in {v.rule for v in lint(restated, f, register=True)}
        assert "R16-restatement" not in {v.rule for v in lint(restated, f)}
    ratio = (
        base
        + f"{f['co_located_rooms']} rooms carry two or more marks, out of {f['diagnostic_count']} diagnostic marks [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R12-unit" in {v.rule for v in lint(ratio, f, register=True)}


def test_register_fallbacks_say_the_reason_that_is_the_reason(sub):
    """D-041 (fifth seating, run 21): a cell's else-branch is where the next overclaim lived. Too few
    rooms says so; a missing position name on a consequence-implying name is a defect, not a denial;
    a parent that shares a wing's name is marked; a singular remainder is singular; a set under three
    rooms draws no relation; a ruleset caveat reaches the register; R17 and the span refusal bind the prose."""
    from repo_substrate.brief import render_register

    f = facts(_skeleton(sub), sub)
    for o in f["overlaps"]:
        assert o["n"] >= 3
    g = json.loads(json.dumps(f))
    feat = next(x for x in g["features"] if x["diagnostic"])
    key = f"{feat['profile']}/{feat['feature']}"
    tiny = dict(feat)
    tiny.update(
        {
            "feature": "tiny_mark",
            "count": 1,
            "rooms": [feat["rooms"][0]],
            "by_wing": {"src": 1},
            "dominant_dir": {
                "dir": "src",
                "n": 1,
                "population": f["wings"].get("src", 1),
                "tied": False,
                "holds_third": True,
                "placeable": False,
            },
            "position_name": None,
            "name_implies_consequence": True,
            "caveat": "a caveat from the ruleset",
        }
    )
    g["features"].append(tiny)
    g["overlaps"] = [
        {"a": key, "b": "p/wider", "relation": "within", "n": feat["count"], "n_outside": 1}
    ]
    g["features"].append({**feat, "feature": "wider", "profile": "p", "count": feat["count"] + 1})
    table = render_register(g)
    assert "too few rooms to place (1)" in table
    assert "POSITION NAME MISSING (ruleset defect)" in table
    assert "caveat: a caveat from the ruleset" in table
    assert "(1 wider room outside this set)" in table and "1 of these room outside it" in table
    big = dict(feat)
    big.update(
        {
            "feature": "wing_named",
            "count": 9,
            "dominant_dir": {
                "dir": "src",
                "n": 9,
                "population": 9,
                "tied": False,
                "holds_third": True,
                "placeable": True,
            },
        }
    )
    g["features"].append(big)
    assert "src (as parent, not the wing) 9 / 9" in render_register(g)
    base = _good_draft(f)
    apart = (
        base
        + f"The {feat['feature']} rooms stand apart from every other mark [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R17-relation" in {v.rule for v in lint(apart, g, register=True)}
    assert "R17-relation" not in {v.rule for v in lint(apart, f, register=True)} or any(
        feat["feature"] in (o["a"] + o["b"]) for o in f["overlaps"]
    )
    r0, r1 = feat["rooms"][0], feat["rooms"][-1]
    span = base + f"The set runs from {r0} to {r1} [{feat['feature']}: {r0}, {r1}].\n\n"
    assert "R11-share" in {v.rule for v in lint(span, f, register=True)}
    wing, n = next(iter(feat["by_wing"].items()))
    if n != feat["count"] and n not in {f["population"], *f["wings"].values()}:
        named = (
            base
            + f"{n} of the {feat['count']} {feat['feature']} rooms sit in {wing} [{feat['feature']} ×{feat['count']}].\n\n"
        )
        assert "R16-restatement" not in {v.rule for v in lint(named, f, register=True)}
        bare = (
            base
            + f"{feat['feature']} holds {n} rooms there [{feat['feature']} ×{feat['count']}].\n\n"
        )
        assert "R16-restatement" in {v.rule for v in lint(bare, f, register=True)}


def test_explanations_are_split_by_cause_and_the_rule_list_has_one_source(sub):
    """D-042 (sixth seating, run 22): a number with two causes is two numbers; the header and the
    lint section describe the same rules; the largest wing's count is the register's; the stance
    carries no condition idiom; 'accordingly' is refused."""
    from repo_substrate.brief import RULES, STANCE, render_brief

    f = facts(_skeleton(sub), sub)
    assert (
        f["rooms_marked_twice"]
        == f["rooms_marked_twice_shared_predicate"] + f["rooms_marked_twice_inert_conjunct"]
    )
    assert "warts" not in STANCE
    page = render_brief(_good_draft(f), f, [], {"generator": "draft"})
    for rid, desc in RULES:
        assert f"{rid} {desc}" in page
    assert "dominant directory is named with its population and cited" not in page
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"])
    base = _good_draft(f)
    largest = max(f["wings"], key=lambda w: (f["wings"][w], w))
    n = feat["by_wing"].get(largest)
    if n is not None and n != feat["count"] and n not in {f["population"], *f["wings"].values()}:
        big = (
            base
            + f"{n} of the {feat['feature']} rooms sit in {largest} [{feat['feature']} ×{feat['count']}].\n\n"
        )
        assert "R16-restatement" in {v.rule for v in lint(big, f, register=True)}
    acc = base + f"The marks sit in {largest} accordingly [{feat['feature']} ×{feat['count']}].\n\n"
    assert "R11-share" in {v.rule for v in lint(acc, f, register=True)}


def test_note_is_generated_from_the_constants_and_disclosures_cover_the_register(sub):
    """D-043 (seventh seating, run 23): the under-covering disclosure. The note states the
    relation predicate the column computes and the floor it uses; each position carries the
    record its predicate reads; the relation fallback names the predicate; the stance asserts no
    fidelity and no norm a decorative feature carries; a negated property another feature marks is
    refused; a citation must warrant something in its sentence; proximity words are refused."""
    from repo_substrate.brief import RELATION_MIN_ROOMS, STANCE, record_of, render_register

    f = facts(_skeleton(sub), sub)
    table = render_register(f)
    assert (
        f"with {RELATION_MIN_ROOMS} or more rooms" in table
        and "identity and containment, and only those" in table
    )
    assert "none |" not in table and (
        "no identity or containment" in table or "⊂" in table or "=" in table
    )
    for x in f["features"]:
        if x["position_name"]:
            assert f"{x['position_name']} ({record_of(x['predicate'])})" in table
    assert record_of("last_touched_days >= p90 and load_index >= 0.10") == "import graph and clock"
    assert "drawn as it is" not in STANCE and "reinforced" not in STANCE
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"])
    base = _good_draft(f)
    room = feat["rooms"][0]
    deco = base + f"Nothing more is said here [{feat['feature']} ×{feat['count']}].\n\n"
    assert "R2-provenance" in {v.rule for v in lint(deco, f, register=True)}
    near = base + f"The remaining marks sit near these [{feat['feature']}: {room}].\n\n"
    assert "R11-share" in {v.rule for v in lint(near, f, register=True)}
    g = json.loads(json.dumps(f))
    g["features"].append(
        {
            **feat,
            "feature": "package_entry",
            "profile": "onboarding",
            "rooms": [room],
            "count": 1,
            "by_wing": {},
            "position_name": "declared entry",
        }
    )
    neg = (
        base
        + f"{feat['feature']} rooms read no fan-in and so are not an entrance [{feat['feature']}: {room}].\n\n"
    )
    assert "R17-relation" in {v.rule for v in lint(neg, g, register=True)}
    # D-045 addendum: the same words quoted as the predicate's limit, drawing no inference to the
    # rooms, are the caveat speaking — R17b was wider than the shape it closed
    h = json.loads(json.dumps(g))
    for x in h["features"]:
        if x["feature"] == feat["feature"]:
            x["caveat"] = (
                "reads no fan-in, not entrance: a package entry that other rooms import cannot qualify"
            )
    limit = (
        base
        + f"{feat['feature']} reads no fan-in, not an entrance — a limit on the predicate, which cannot qualify a package entry that other rooms import [{feat['feature']}: {room}].\n\n"
    )
    assert "R17-relation" not in {v.rule for v in lint(limit, h, register=True)}


def test_register_relations_cover_every_set_and_positions_always_name_a_record(sub):
    """D-044 (eighth seating, run 24): a note generated from the constants but not the filter beside
    them. Relations are drawn over every feature with enough rooms, decorative included, so a
    fallback row has no superset among them; every position cell names a record; a count of
    relations matches the register by kind; a wing holding all of a feature's rooms is its row."""
    from repo_substrate.brief import RELATION_MIN_ROOMS, _RECORDS, render_register

    f = facts(_skeleton(sub), sub)
    sets = {
        f"{x['profile']}/{x['feature']}": set(x["rooms"])
        for x in f["features"]
        if len(x["rooms"]) >= RELATION_MIN_ROOMS
    }
    related = {k for o in f["overlaps"] for k in (o["a"], o["b"])}
    for k, rs in sets.items():
        if k in related:
            continue
        for k2, rs2 in sets.items():
            assert k2 == k or not (rs <= rs2 or rs2 <= rs), (k, k2)
    assert f["relation_counts"]["total"] == len(f["overlaps"])
    table = render_register(f)
    records = [name for name, _ in _RECORDS] + ["an unlisted record"]
    for line in table.splitlines():
        if line.startswith("| ") and not line.startswith("| feature") and "|---" not in line:
            pos = line.split("|")[3].strip()
            assert any(r in pos for r in records), pos
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"])
    base = _good_draft(f)
    largest = max(f["wings"], key=lambda w: (f["wings"][w], w))
    wing = next(
        (w for w, v in feat["by_wing"].items() if v == feat["count"] and w != largest), None
    )
    if wing:
        row = (
            base
            + f"All {feat['count']} {feat['feature']} rooms sit in {wing} [{feat['feature']} ×{feat['count']}].\n\n"
        )
        assert "R16-restatement" in {v.rule for v in lint(row, f, register=True)}
    bad = (
        base
        + f"There are {f['relation_counts']['total'] + 1} relations here [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R12-unit" in {v.rule for v in lint(bad, f, register=True)}
    others = (
        base
        + f"{feat['feature']} sits in {largest} and others under lib/x [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R11-share" in {v.rule for v in lint(others, f, register=True)}


def test_fixes_are_as_wide_as_the_shape_they_close(sub):
    """D-045 (paired reading, run 25): a wing holding all of a feature's rooms is refused whether or
    not the number is in the prose; a located subset carries its total; a named directory carries
    its share and its rooms; a family of marks the sheet does not define is refused."""
    f = facts(_skeleton(sub), sub)
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"])
    base = _good_draft(f)
    room = feat["rooms"][0]
    whole = next(
        (w for w, v in feat["by_wing"].items() if v == feat["count"] and feat["count"] >= 3), None
    )
    if whole:
        bare = (
            base
            + f"{feat['feature']} fires in {whole} [{feat['feature']} ×{feat['count']}: {room}].\n\n"
        )
        assert "R16-restatement" in {v.rule for v in lint(bare, f, register=True)}
    g = json.loads(json.dumps(f))
    tf = dict(feat)
    tf.update(
        {
            "feature": "split_mark",
            "count": 9,
            "rooms": feat["rooms"][:1] + ["lib/a/1.js", "lib/a/2.js", "lib/b/3.js"],
            "by_wing": {"src": 1, "lib": 8},
            "dominant_dir": {
                "dir": "lib/a",
                "n": 2,
                "population": 4,
                "tied": False,
                "holds_third": False,
                "placeable": True,
            },
        }
    )
    g["features"].append(tf)
    g["wings"] = {**g["wings"], "lib": 8}
    partial = base + f"split_mark places 1 of its rooms in src [split_mark: {room}].\n\n"
    assert "R16-restatement" in {v.rule for v in lint(partial, g, register=True)}
    whole_sent = base + f"split_mark places 1 of its 9 rooms in src [split_mark: {room}].\n\n"
    assert "R16-restatement" not in {v.rule for v in lint(whole_sent, g, register=True)}
    half = base + f"2 of the 9 split_mark rooms sit in lib/a [split_mark: lib/a/1.js].\n\n"
    assert "R15-composition" in {v.rule for v in lint(half, g, register=True)}
    full = (
        base
        + f"2 of the 9 split_mark rooms sit in lib/a, which holds 4 rooms [split_mark: lib/a/1.js].\n\n"
    )
    assert "R15-composition" not in {v.rule for v in lint(full, g, register=True)}
    fam = (
        base
        + f"The graph marks sit on the same two wings [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R18-family" in {v.rule for v in lint(fam, f, register=True)}
