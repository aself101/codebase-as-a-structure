"""M3 — the architect brief and the register lint (architect-brief-spec.md, D-027)."""

from __future__ import annotations

import json
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
        f"The building has {f['population']} rooms and {f['diagnostic_count']} diagnostic marks; the wing {wing} holds {n} of them [{feat['feature']}: {room}].\n\n"
        f"The room {room} sits where {feat['feature']} fires [{feat['feature']} ×{feat['count']}].\n\n"
    )
    if f["decorative"]["count"]:
        names = ", ".join(
            x["feature"] + (f" — {x['position_name']}" if x.get("position_name") else "")
            for x in f["features"]
            if x["decorative"]
        )
        text += f"{f['decorative']['count']} decorative marks ({names}) render but are not a diagnosis [{feat['feature']} ×{feat['count']}].\n\n"
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
        f"{disclose}two marks share one bracket [{feat['feature']} ×{feat['count']}; {other['feature']} ×{other['count']}].\n\n"
        f"{disclose}one more in the comma form [{feat['feature']} ×{feat['count']}, {other['feature']} ×{other['count']}].\n\n"
    )
    assert lint(chained, f) == []
    wrong_count = (
        base
        + f"{disclose}bad [{feat['feature']} ×{feat['count'] + 1}; {other['feature']} ×{other['count']}].\n\n"
    )
    assert {v.rule for v in lint(wrong_count, f)} == {"R2-provenance"}
    hybrid = base + f"Under a count [{feat['feature']} ×{feat['count']}: {room}].\n\n"
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
    assert "overlaps" in f and "co_located_rooms_base_profile" in f and f["gate_fingerprint"]
    for x in f["features"]:
        assert sum(x["by_wing"].values()) == x["count"]
    assert f["co_located_rooms"] >= f["co_located_rooms_base_profile"]
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
            "dominant_dir": {"dir": "lib/inner", "n": 6},
        }
    )
    h["features"].append(deep)
    silent = base + f"Six rooms carry deep_mark [deep_mark ×6].\n\n"
    assert "R15-composition" in {v.rule for v in lint(silent, h)}
    shown = (
        base + f"Six rooms carry deep_mark, all 6 in lib/inner [deep_mark ×6: lib/inner/0.js].\n\n"
    )
    rules = {v.rule for v in lint(shown, h)}
    assert "R15-composition" not in rules and "R10-prefix" not in rules
