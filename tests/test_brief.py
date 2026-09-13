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


def _row(table: str, feature: str, decorative: bool = False, profile: str | None = None) -> str:
    """D-060: the position is the first column; a row is found by its feature cell."""
    cell = f"| {'◌ ' if decorative else ''}{feature} |" + (f" {profile} |" if profile else "")
    return next(line for line in table.splitlines() if line.startswith("| ") and cell in line)


def _at_floor(g, name):
    """A copy of the sheet where feature `name` has enough rooms for the relation cell (D-047)."""
    h = json.loads(json.dumps(g))
    for x in h["features"]:
        if x["feature"] == name:
            x["count"] = max(x["count"], 3)
    return h


def _good_draft(f):
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"] and x["rooms"])  # D-057: a roster row may be at 0
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
            if x["decorative"] and x["count"]
        )
        cites = "; ".join(f"{x['feature']} ×{x['count']}" for x in f["features"] if x["decorative"] and x["count"])
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
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"] and x["rooms"])
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


def test_run_brief_renders_by_code_and_lints_a_draft(sub):
    """D-049: without a draft the page is rendered by code and carries no reading; a draft is
    linted and appended, and a failing draft marks the page."""
    sk = _skeleton(sub)
    f = facts(sk, sub)
    good = _good_draft(f)
    r = run_brief(sk, sub)
    assert r["passed"] and r["text"] == "" and r["provenance"]["generator"] == "code"
    assert "## Reading" not in r["markdown"] and "## Register lint" not in r["markdown"]
    assert "no model wrote any of it" in r["markdown"] and "## Provenance" in r["markdown"]
    r2 = run_brief(sk, sub, draft=good + "It will fail.")
    assert not r2["passed"] and "FAILED (" in r2["markdown"] and len(r2["violations"]) >= 1
    r3 = run_brief(sk, sub, draft=good)
    assert r3["passed"] and r3["provenance"]["generator"] == "draft"
    assert "## Reading (draft)" in r3["markdown"] and "Register lint: **PASS**" in r3["markdown"]
    json.dumps(r3["facts"])  # serializable


def test_relint_keeps_prose_and_provenance(sub):
    from repo_substrate.brief import relint

    sk = _skeleton(sub)
    f = facts(sk, sub)
    good = _good_draft(f)
    r = run_brief(sk, sub, draft=good)
    r2 = relint(r["markdown"], sk, sub)
    assert r2["passed"] and r2["text"].strip() == good.strip()
    assert r2["provenance"]["generator"] == "draft" and "relinted" in r2["provenance"]
    # draft-time lint and relint must agree on the same prose
    bad = good + "Changing it will break much.\n\n"
    r3 = run_brief(sk, sub, draft=bad)
    r4 = relint(r3["markdown"], sk, sub)
    assert [v["rule"] for v in r3["violations"]] == [v["rule"] for v in r4["violations"]]
    # a page from before D-049 carries its reading under "## Reading"; relint recovers it
    old_page = r["markdown"].replace("## Reading (draft)", "## Reading")
    assert relint(old_page, sk, sub)["text"].strip() == good.strip()
    # a page with no reading relints to a pass with no prose
    r5 = relint(run_brief(sk, sub)["markdown"], sk, sub)
    assert r5["passed"] and r5["text"] == ""


def test_d030_lint_closes_the_perverse_routes(sub):
    """D-030: exemptions are narrow, numbers are paragraph-scoped, counts sit outside
    citations, attempts are bounded and logged."""
    sk = _skeleton(sub)
    f = facts(sk, sub)
    good = _good_draft(f)
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"] and x["rooms"])
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
    # (attempts were capped and logged from D-030 to D-049; there is no generator to cap now)


def test_lint_reads_chained_brackets_and_the_determiner_one(sub):
    """D-032 addendum: [f ×N; g ×M] and [f ×N, g ×M] are several citations in one bracket;
    the word "one" is a determiner, not a measurement; a room under a count must share its bracket."""
    f = facts(_skeleton(sub), sub)
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"] and x["rooms"])
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
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"] and x["rooms"])
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
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"] and x["rooms"])
    room = feat["rooms"][0]
    base = _good_draft(f)
    assert lint(base, f) == []
    # R3: a feature's count in a sentence that cites another feature is refused
    other = next(
        (
            x
            for x in f["features"]
            if x["diagnostic"] and x is not feat and x["count"] and x["count"] != feat["count"]  # D-057: not a roster row at 0
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
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"] and x["rooms"])
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
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"] and x["rooms"])
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
    # D-050: "none validated" is read from the gate, not a literal — validate one signal and the
    # register counts it in the clause that counts the asserted ones
    g = json.loads(json.dumps(f))
    sig = next(k for k, v in g["gate"].items() if v == "asserted")
    g["gate"][sig] = "validated"
    t2 = render_register(g)
    assert "1 validated" in t2 and "none validated" not in t2
    assert f"{sum(1 for v in g['gate'].values() if v == 'asserted')} of {len(g['gate'])} signals asserted" in t2
    prose = _good_draft(f)
    page = render_brief(prose, f, [], {"generator": "draft"})
    assert (
        "## Register" in page
        and "## Reading (draft)" in page
        and page.index("## Register") < page.index("## Reading (draft)")
    )
    r = relint(page, _skeleton(sub), sub)
    assert r["text"].strip() == prose.strip() and r["passed"]
    # a nesting called one set is still refused with the register present
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"] and x["rooms"])
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
    feat = next(x for x in g["features"] if x["diagnostic"] and x["rooms"])
    key = f"{feat['profile']}/{feat['feature']}"
    g["overlaps"] = [
        {"a": key, "b": "p/wider", "relation": "within", "n": feat["count"], "n_outside": 8}
    ]
    g["features"].append({**feat, "feature": "wider", "profile": "p", "count": feat["count"] + 8})
    table = render_register(_at_floor(g, feat["feature"]))
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
    assert "none holds a third" in render_register(_at_floor(g, feat["feature"]))
    assert (
        "distinct sets of rooms" in table
        and "rooms twice" in table
        and "under one predicate in two profiles" in table
    )
    base = _good_draft(f)
    wing, n = next(iter(feat["by_wing"].items()))
    if n != feat["count"] and n > 3 and n not in {f["population"], *f["wings"].values()}:
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
    feat = next(x for x in g["features"] if x["diagnostic"] and x["rooms"])
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
    g["features"].append(
        {**feat, "feature": "wider", "profile": "p", "count": max(feat["count"] + 1, 3)}
    )
    table = render_register(_at_floor(g, feat["feature"]))
    assert "too few rooms to place (1)" in table
    assert "POSITION NAME MISSING (ruleset defect)" in table
    assert "caveat: a caveat from the ruleset" in table
    assert "(1 wider room outside this set)" in table and "1 of these rooms outside it" in table  # D-057: the partitive stays plural
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
    assert "src (as parent, not the wing) 9 / 9" in render_register(_at_floor(g, feat["feature"]))
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
    if n != feat["count"] and n > 3 and n not in {f["population"], *f["wings"].values()}:
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
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"] and x["rooms"])
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
    assert record_of("last_touched_days >= p90 and load_index >= 0.10") == "import graph and clock and size"  # D-048: the load blend reads size
    assert "drawn as it is" not in STANCE and "reinforced" not in STANCE
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"] and x["rooms"])
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
    assert f["diagnostic_features"] == sum(
        1 for x in f["features"] if x["diagnostic"] and x["rooms"]
    )
    assert "features, not marks or rooms" in f["units"]["diagnostic_features"]
    table = render_register(f).split("### Rooms at the most positions", 1)[0]  # the feature table (D-049)
    records = [name for name, _ in _RECORDS] + ["an unlisted record"]
    for line in table.splitlines():
        if line.startswith("| ") and not line.startswith("| position") and "|---" not in line:
            pos = line.split("|")[1].strip()  # D-060: the position is the first column
            assert any(r in pos for r in records), pos
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"] and x["rooms"])
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
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"] and x["rooms"])
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
    # a family every cited feature's record defines is admitted; a bare one is not
    from repo_substrate.brief import record_of

    clockish = [
        x for x in f["features"] if x["diagnostic"] and "clock" in record_of(x["predicate"])
    ]
    if clockish:
        c0 = clockish[0]
        ok_fam = base + f"The age positions split [{c0['feature']} ×{c0['count']}].\n\n"
        assert "R18-family" not in {v.rule for v in lint(ok_fam, f, register=True)}


def test_every_refusal_admits_the_sentence_it_must_admit(sub):
    """D-046: the converse of D-045 — a refusal is no wider than its shape. Each case is a sentence
    the lint must ADMIT beside the one it must refuse. Three were found in one day by the pipeline
    refusing correct prose."""
    f = facts(_skeleton(sub), sub)
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"] and x["rooms"])
    base = _good_draft(f)
    largest = max(f["wings"], key=lambda w: (f["wings"][w], w))
    wings_only = (
        base
        + f"The building holds {f['population']} rooms in {f['wing_count']} wings, {largest} being the largest of them.\n\n"
    )
    assert "R11-share" not in {v.rule for v in lint(wings_only, f, register=True)}
    # likeness is a connective between relation statements unless a place is named
    conn = (
        base
        + f"{feat['feature']} is likewise nested inside another set [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R11-share" not in {v.rule for v in lint(conn, f, register=True)}
    shared = (
        base
        + f"{feat['feature']} marks sit in {largest} and the smaller wings alike [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R11-share" in {v.rule for v in lint(shared, f, register=True)}
    # the building's shape carries nothing to cite; "the largest wing" compares wings even beside a citation
    shape = f"This building has {f['population']} rooms in {f['wing_count']} wings.\n\n" + base
    assert "R2-provenance" not in {v.rule for v in lint(shape, f, register=True)}
    lw = (
        base
        + f"What sits outside the largest wing is {feat['count']} rooms [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R11-share" not in {v.rule for v in lint(lw, f, register=True)}
    ranked = (
        base + f"The largest set is {feat['feature']} [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R11-share" in {v.rule for v in lint(ranked, f, register=True)}
    dec = [x for x in f["features"] if x["decorative"]]
    if dec:
        cites = "; ".join(f"{x['feature']} ×{x['count']}" for x in dec)
        names = ", ".join(
            f"{x['feature']} — {x['position_name']}" for x in dec if x.get("position_name")
        )
        sigs = sorted(
            {w for x in dec for w in re.findall(r"[a-z_]+_index", x.get("decorative_reason") or "")}
        )
        without = (
            base
            + f"{names} rest on {', '.join(sigs)}, which is unvalidated, and their {f['decorative']['count']} marks render without entering the diagnosis [{cites}].\n\n"
        )
        assert "R4-decorative" not in {v.rule for v in lint(without, f, register=True)}
        # the prompt's own canonical decorative sentence: cited by count, no feature named in prose
        canonical = (
            base
            + f"{f['decorative']['count']} decorative marks render but are not a diagnosis [{cites}].\n\n"
        )
        assert not {v.rule for v in lint(canonical, f, register=True)} & {
            "R2-provenance",
            "R4-decorative",
        }
    # a sentence continuing about the feature the sentence before it named
    room = feat["rooms"][0]
    pair = base + (
        f"{feat['feature']} covers {feat['count']} rooms [{feat['feature']}: {room}]. "
        f"Its predicate reads what the register prints [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R2-provenance" not in {v.rule for v in lint(pair, f, register=True)}
    orphan = base + f"Nothing is said of it here [{feat['feature']} ×{feat['count']}].\n\n"
    assert "R2-provenance" in {v.rule for v in lint(orphan, f, register=True)}
    # a parent directory sharing a wing's name: sayable as the directory, refused bare
    g = json.loads(json.dumps(f))
    wing = max(g["wings"], key=lambda w: (g["wings"][w], w))
    tf = dict(feat)
    tf.update(
        {
            "feature": "amb_mark",
            "count": 19,
            "by_wing": {wing: 7},
            "rooms": feat["rooms"],
            "dominant_dir": {
                "dir": wing,
                "n": 5,
                "population": 13,
                "tied": False,
                "holds_third": False,
                "placeable": True,
            },
        }
    )
    g["features"].append(tf)
    bare_dir = (
        base + f"5 of the 19 amb_mark rooms sit in {wing} [amb_mark ×19: {feat['rooms'][0]}].\n\n"
    )
    assert "R16-restatement" in {v.rule for v in lint(bare_dir, g, register=True)}
    # the directory checks read the sentence they are checking, not the paragraph's last sentence
    two = base + (
        f"amb_mark places 5 of its 19 rooms in the {wing} directory, which holds 13 rooms "
        f"[amb_mark ×19: {feat['rooms'][0]}]. The register carries the rest.\n\n"
    )
    assert "R16-restatement" not in {v.rule for v in lint(two, g, register=True)}
    marked_dir = (
        base
        + f"5 of the 19 amb_mark rooms sit in the {wing} directory, which holds 13 rooms [amb_mark ×19: {feat['rooms'][0]}].\n\n"
    )
    rules = {v.rule for v in lint(marked_dir, g, register=True)}
    assert "R16-restatement" not in rules and "R15-composition" not in rules


def test_fixed_texts_are_tested_against_their_computation(sub):
    """D-047 (ninth seating, run 26): a fixed text on the page is tested against the computation it
    labels. rooms_marked_twice counts distinct rooms; the relation cell under the floor says so;
    every emitted rule id is described on the page; the root wing is nameable; a partial wing
    enumeration is refused."""
    from repo_substrate.brief import RULES, lint as _lint, render_register

    f = facts(_skeleton(sub), sub)
    g = json.loads(json.dumps(f))
    feat = next(x for x in g["features"] if x["diagnostic"] and x["rooms"])
    key = f"{feat['profile']}/{feat['feature']}"
    rooms = feat["rooms"]
    # two identical pairs sharing every room count the rooms once
    g["features"].append({**feat, "feature": "twin_a", "profile": "p", "count": len(rooms)})
    g["features"].append({**feat, "feature": "twin_b", "profile": "q", "count": len(rooms)})
    g["overlaps"] = [
        {
            "a": key,
            "b": "p/twin_a",
            "relation": "identical",
            "n": len(rooms),
            "inert_terms": [],
            "shared_predicate": True,
            "diagnostic": True,
        },
        {
            "a": key,
            "b": "q/twin_b",
            "relation": "identical",
            "n": len(rooms),
            "inert_terms": ["load_index >= 0.10"],
            "shared_predicate": False,
            "diagnostic": True,
        },
    ]
    from repo_substrate.brief import (
        facts as _facts,
    )  # the sheet computes it; the copy above only carries it

    assert f["rooms_marked_twice"] <= sum(x["count"] for x in f["features"] if x["diagnostic"])
    assert f["rooms_marked_twice"] == len(
        {
            r
            for o in f["overlaps"]
            if o["relation"] == "identical" and o.get("diagnostic")
            for x in f["features"]
            if f"{x['profile']}/{x['feature']}" == o["a"]
            for r in x["rooms"]
        }
    )
    # the relation cell under the floor
    tiny = next(x for x in f["features"] if x["count"] < 3)
    table = render_register(f)
    assert f"too few rooms to relate ({tiny['count']})" in table  # D-057: the D-047 wording where nothing is drawn
    # every rule id the lint can emit is on the page
    ids = {rid for rid, _ in RULES}
    import inspect, re as _re
    from repo_substrate import brief as _b

    emitted = set(_re.findall(r'"(R\d+)-[a-z]+"', inspect.getsource(_b)))
    assert emitted <= ids, emitted - ids
    # the root wing is nameable; a partial enumeration is refused
    base = _good_draft(f)
    if "(root)" in f["wings"]:
        rf = next((x for x in f["features"] if x["diagnostic"] and "(root)" in x["by_wing"]), None)
        if rf and rf["by_wing"]["(root)"] < rf["count"]:
            sent = (
                base
                + f"{rf['by_wing']['(root)']} of the {rf['count']} {rf['feature']} rooms sit in the root wing [{rf['feature']} ×{rf['count']}].\n\n"
            )
            assert "R16-restatement" not in {v.rule for v in _lint(sent, f, register=True)}
    if f["wing_count"] >= 2:
        one = next(iter(f["wings"]))
        partial = (
            f"The building has {f['population']} rooms in {f['wing_count']} wings: {one} at {f['wings'][one]}.\n\n"
            + base
        )
        assert "R16-restatement" in {v.rule for v in _lint(partial, f, register=True)}


def test_the_reading_is_bound_to_what_the_register_does_not_print(sub, tmp_path):
    """D-048 (tenth seating): the tokenizer splits before a digit, so every per-sentence rule binds
    over one sentence; the sheet lists the most-marked rooms and R19 binds the reading to name one
    under every feature that marks it; a position name's record word names a record the predicate
    reads; the prompt says what the lint does and what the model is given; a directory's numbers
    are rooms."""
    import inspect

    import repo_substrate.brief as _b
    from repo_substrate.brief import RULES, SENTENCE, record_of
    from repo_substrate.mapper.ruleset import RulesetError

    f = facts(_skeleton(sub), sub)
    feat = next(x for x in f["features"] if x["diagnostic"] and not x["name_implies_consequence"] and x["rooms"])
    base = _good_draft(f)
    # 1. a sentence opening with a digit is a sentence: the page's own pair, which R2b read as one
    pair = "The register draws 3 relations: 1 identical and 2 within. 254 rooms carry two or more diagnostic marks [hub ×50]."
    assert len(SENTENCE.split(pair)) == 2
    orphan = base + (
        f"The building has {f['population']} rooms. "
        f"{f['co_located_rooms']} rooms carry two or more diagnostic marks [{feat['feature']} ×{feat['count']}].\n\n"
    )
    assert "R2-provenance" in {v.rule for v in lint(orphan, f, register=True)}
    # 2. the sheet lists the most-marked rooms with every diagnostic feature that marks each; the
    # fixture has no room under two marks, so a second feature is made diagnostic on a copy
    assert f["most_marked_rooms"] == [] and "most_marked_rooms" in f["units"]
    f = json.loads(json.dumps(f))
    # D-052: the second feature must draw a different set — an identical set is one set, not two
    second = next(
        x for x in f["features"]
        if not x["diagnostic"] and feat["rooms"][0] in x["rooms"] and set(x["rooms"]) != set(feat["rooms"])
    )
    second["diagnostic"], second["decorative"] = True, False
    f["most_marked_rooms"] = _b.most_marked(f["features"])
    top = f["most_marked_rooms"]
    assert top and len(top) <= _b.MOST_MARKED_ROOMS
    diag_f = [x for x in f["features"] if x["diagnostic"]]
    for m in top:
        # D-050: a feature under two profiles is named with its profile, so names count marks
        assert len(m["features"]) == m["marks"] >= 2
        assert {n.split("/")[-1] for n in m["features"]} == {
            x["feature"] for x in diag_f if m["room"] in x["rooms"]
        }
        # sets counts distinct room sets among the features that mark the room
        assert m["sets"] == len({frozenset(x["rooms"]) for x in diag_f if m["room"] in x["rooms"]})
        assert 2 <= m["sets"] <= m["marks"]  # D-052: the floor is sets
        assert 1 <= m["listed_at_this_count"] <= m["rooms_at_this_count"]
    assert [(m["sets"], m["marks"]) for m in top] == sorted(((m["sets"], m["marks"]) for m in top), reverse=True)
    # 3. (R19, the obligation to name one of them, lived from D-048 to D-049; the register prints them now)
    ex = top[0]
    cites = "; ".join(f"{k}: {ex['room']}" for k in ex["features"])
    canonical = base + f"{ex['room']} carries {', '.join(ex['features'])} [{cites}].\n\n"
    rules = {v.rule for v in lint(canonical, f, register=True)}
    # 4. the admit-case: a room named under every feature that marks it is refused by nothing (D-046)
    assert not rules & {"R2-provenance", "R8-attribution", "R11-share", "R13-identity", "R17-apart"}, rules
    # naming the room does not name its directory: the R19 sentence is admitted when the room sits
    # in a feature's unplaced dominant directory (eslint's lib/config, 4 of 5, refused it under R15)
    h = json.loads(json.dumps(f))
    parent = ex["room"].rsplit("/", 1)[0]
    for x in h["features"]:
        if x["feature"] == ex["features"][0]:
            x["dominant_dir"] = {"dir": parent, "n": 1, "population": 3, "tied": False, "holds_third": False, "placeable": True}
    assert "R15-composition" not in {v.rule for v in lint(canonical, h, register=True)}
    # the marks count is a sheet number wearing the unit marks
    counted = base + (
        f"{ex['room']} carries {ex['marks']} diagnostic marks: {', '.join(ex['features'])} [{cites}].\n\n"
    )
    assert "R12-unit" not in {v.rule for v in lint(counted, f, register=True)}
    assert "R19" not in {rid for rid, _ in RULES}
    # 5. (the prompt and the input message went with the generator at D-049)
    # 6. the record list names the blend's inputs
    assert record_of("load_index >= p90") == "import graph and size"
    # 7. a directory's share and population are rooms
    dd = next((x for x in f["features"] if (x.get("dominant_dir") or {}).get("placeable")), None)
    if dd:
        g = json.loads(json.dumps(f))
        g["decorative"]["count"] = dd["dominant_dir"]["population"]  # the coincidence typeorm had
        d = dd["dominant_dir"]
        dsent = base + (
            f"{d['n']} of the {dd['count']} {dd['feature']} rooms sit in the {d['dir']} directory, which holds {d['population']} rooms "
            f"[{dd['feature']} ×{dd['count']}: {next(r for r in dd['rooms'] if r.startswith(d['dir'] + '/'))}].\n\n"
        )
        assert "R12-unit" not in {v.rule for v in lint(dsent, g, register=True)}
        # the denominator one sentence back, anchored on the directory's name, is admitted (D-046);
        # a bare share with no such sentence before it is not
        two = base + (
            f"{dd['feature']} places {d['n']} of its {dd['count']} rooms in the {d['dir']} directory, which holds {d['population']} rooms "
            f"[{dd['feature']} ×{dd['count']}: {next(r for r in dd['rooms'] if r.startswith(d['dir'] + '/'))}]. "
            f"{d['n']} of the {dd['count']} {dd['feature']} rooms sit there as well [{dd['feature']} ×{dd['count']}].\n\n"
        )
        assert "R15-composition" not in {v.rule for v in lint(two, g, register=True)}
        bare_share = base + (
            f"{d['n']} of the {dd['count']} {dd['feature']} rooms sit in the {d['dir']} directory [{dd['feature']} ×{dd['count']}].\n\n"
        )
        # (on the fixture the directory shares the wing's name, so the refusal may be R16's)
        assert {v.rule for v in lint(bare_share, g, register=True)} & {"R15-composition", "R16-restatement"}
    # 8. the loader: a record word names a record the predicate reads; 'high' is worn per upper pNN
    def _rs(pos, pred):
        p = tmp_path / "rs.toml"
        p.write_text(
            '[ruleset]\nname = "t"\nversion = "0.0.1"\nprofile = "t"\ndescription = "t"\nwing_depth = 1\n\n[[feature]]\nname = "x"\n'
            f'predicate = "{pred}"\nposition_name = "{pos}"\n',
            encoding="utf-8",
        )
        return load_ruleset(p)

    with pytest.raises(RulesetError, match="imported"):
        _rs("long-untouched, still-imported room", "last_touched_days >= p90 and load_index >= 0.10")
    _rs("long-untouched room above the load floor", "last_touched_days >= p90 and load_index >= 0.10")
    with pytest.raises(RulesetError, match="'high'"):
        _rs("high-centrality, high-fan-out junction", "centrality >= p90 and fan_out >= p50")
    _rs("high-centrality junction with fan-out at or above the median", "centrality >= p90 and fan_out >= p50")
    _rs("unreinforced high-load node with high edit pressure", "load_index >= p90 and bug_pressure_index >= p90 and reinforcement_index <= 0.0")
    # the shipped rulesets pass the loader (the fixtures load them) and every emitted id is on the page
    ids = {rid for rid, _ in RULES}
    emitted = set(re.findall(r'"(R\d+)-[a-z]+"', inspect.getsource(_b)))
    assert emitted <= ids


def test_a_position_wears_no_feature_name_and_the_most_marked_list_says_when_it_is_cut(sub, tmp_path):
    """D-049 (eleventh seating): a position name names no other feature (foundation's 'high-load hub'
    called every foundation room a hub while 12 of 48 were not); the sheet says how many rooms carry
    the most marks so a capped list is not a silent claim of completeness; the lint list carries no
    stale attribution literal."""
    import repo_substrate.brief as _b
    from repo_substrate.brief import render_brief
    from repo_substrate.mapper.ruleset import RulesetError

    # across both shipped rulesets, no position name carries any feature's name
    base, ov = load_ruleset(RULESET), load_ruleset(ONBOARDING)
    names = {f.name for rs in (base, ov) for f in rs.features}
    for rs in (base, ov):
        for f in rs.features:
            pos = (f.position_name or "").lower()
            for other in names - {f.name}:
                assert not re.search(rf"\b{re.escape(other)}\b", pos), (f.name, pos, other)
    p = tmp_path / "rs.toml"
    p.write_text(
        '[ruleset]\nname = "t"\nversion = "0.0.1"\nprofile = "t"\ndescription = "t"\nwing_depth = 1\n\n'
        '[[feature]]\nname = "hub"\npredicate = "centrality >= p90"\n\n'
        '[[feature]]\nname = "foundation"\npredicate = "load_index >= p90"\nname_implies_consequence = true\nposition_name = "high-load hub"\n',
        encoding="utf-8",
    )
    with pytest.raises(RulesetError, match="names the feature 'hub'"):
        load_ruleset(p)
    # D-050: the converse of D-048 — a pNN the predicate reads is worn by the name. "import-graph
    # root" named fan_in == 0 and not fan_out >= p75 beside a count of 1 (23 rooms have no fan-in)
    from repo_substrate.mapper.ruleset import QUANTILE_PHRASES
    p.write_text(
        '[ruleset]\nname = "t"\nversion = "0.0.1"\nprofile = "t"\ndescription = "t"\nwing_depth = 1\n\n'
        '[[feature]]\nname = "import_root"\npredicate = "fan_in == 0 and fan_out >= p75"\nposition_name = "import-graph root"\n',
        encoding="utf-8",
    )
    with pytest.raises(RulesetError, match="a conjunct at a quantile is unnamed"):
        load_ruleset(p)
    p.write_text(
        p.read_text(encoding="utf-8").replace(
            '"import-graph root"', '"import-graph root with fan-out at or above the upper quartile"'
        ),
        encoding="utf-8",
    )
    assert load_ruleset(p).features[0].position_name.endswith("upper quartile")
    for rs in (base, ov):
        for f in rs.features:
            if f.position_name:
                assert len(re.findall(QUANTILE_PHRASES, f.position_name.lower())) >= len(
                    re.findall(r"\bp\d{1,2}\b", f.predicate)
                ), (f.name, f.position_name, f.predicate)
    # the count of rooms at the most is on the sheet and is a rooms number (D-050: the most is sets)
    f = facts(_skeleton(sub), sub)
    assert f["rooms_at_most_sets"] == 0 and "rooms_at_most_sets" in f["units"]
    g = json.loads(json.dumps(f))
    feat = next(x for x in g["features"] if x["diagnostic"] and x["rooms"])
    second = next(x for x in g["features"] if not x["diagnostic"] and feat["rooms"][0] in x["rooms"] and set(x["rooms"]) != set(feat["rooms"]))  # D-052: a different set
    second["diagnostic"], second["decorative"] = True, False
    g["most_marked_rooms"] = _b.most_marked(g["features"])
    g["rooms_at_most_sets"] = 7
    ex = g["most_marked_rooms"][0]
    cites = "; ".join(f"{k.split('/')[-1]}: {ex['room']}" for k in ex["features"])
    text = _good_draft(g) + (
        f"7 rooms carry the most distinct diagnostic sets, {ex['sets']} each; {ex['room']} is one, under "
        f"{', '.join(k.split('/')[-1] for k in ex['features'])} [{cites}].\n\n"
    )
    rules = {v.rule for v in lint(text, g, register=True)}
    assert not rules & {"R3-number", "R12-unit"}, rules
    # the lint list on the page names no decision range
    page = render_brief(text, g, provenance={"attempt": 1}, violations=[])
    assert "through D-0" not in page and "each rule is dated" in page


def test_the_page_is_rendered_by_code_and_its_fixed_texts_match_their_fields(sub):
    """D-049 addendum (brief 0.18.0): the reading is cut. The page is header → register (feature
    table, most-marked rooms, shared-rooms matrix) → decorative disclosure → stance → provenance,
    all from the sheet; the shared counts recompute from the room lists; the most-marked lead says
    whether the list is cut; the disclosure names every ungrounded signal and position name."""
    import repo_substrate.brief as _b
    from repo_substrate.brief import render_brief, render_disclosure, render_most_marked, render_shared

    f = facts(_skeleton(sub), sub)
    page = run_brief(_skeleton(sub), sub)["markdown"]
    order = ["## Register", "### Rooms at the most positions", "### Shared rooms", "## Excluded marks (◌)", "## Stance", "## Provenance"]
    idx = [page.index(h) for h in order]
    assert idx == sorted(idx) and "## Reading" not in page and "## Register lint" not in page
    assert f["stance"] in page and "R19" not in page
    # the shared-rooms matrix: every pair of diagnostic features, counts from the room lists
    diag = {f"{x['profile']}/{x['feature']}": set(x["rooms"]) for x in f["features"] if x["diagnostic"]}
    keys = sorted(diag)
    assert len(f["shared_rooms"]) == len(keys) * (len(keys) - 1) // 2 and "shared_rooms" in f["units"]
    for sr in f["shared_rooms"]:
        assert sr["shared"] == len(diag[sr["a"]] & diag[sr["b"]])
    shared = render_shared(f)
    for x in f["features"]:
        if x["diagnostic"]:
            assert f"**{x['count']}**" in shared  # the diagonal is the feature's own count
    # a shared count is a sheet number in a draft sentence citing either feature
    a, b = keys[0], keys[-1]
    n = next(sr["shared"] for sr in f["shared_rooms"] if sr["a"] == a and sr["b"] == b)
    fa = next(x for x in f["features"] if f"{x['profile']}/{x['feature']}" == a)
    sent = _good_draft(f) + f"{n} rooms carry both {fa['feature']} and {b.split('/')[-1]} [{fa['feature']} ×{fa['count']}].\n\n"
    assert "R3-number" not in {v.rule for v in lint(sent, f, register=True)}
    # the most-marked lead says whether the list is cut, against rooms_at_most_marks
    g = json.loads(json.dumps(f))
    feat = next(x for x in g["features"] if x["diagnostic"] and x["rooms"])
    second = next(x for x in g["features"] if not x["diagnostic"] and feat["rooms"][0] in x["rooms"] and set(x["rooms"]) != set(feat["rooms"]))  # D-052: a different set
    second["diagnostic"], second["decorative"] = True, False
    g["most_marked_rooms"] = _b.most_marked(g["features"])
    g["rooms_at_most_sets"] = len(g["most_marked_rooms"])
    g["top_tier"] = _b.top_tier(g["features"], {r: {"size_loc": m["lines"]} for r, m in g["rooms"].items()})  # D-061: the rendered table is the whole top tier
    assert f"{len(g['top_tier']['rooms'])} room" in render_most_marked(g) and "in path order" in render_most_marked(g)
    assert "No room carries two distinct diagnostic sets" in render_most_marked(f)  # the fixture has none
    # D-050: the third case — fewer rooms at the most than the cap, the list filled from the next
    # count (typeorm: four at seven, then one of eight at six, first by path, under "all are listed")
    h = json.loads(json.dumps(g))
    h["most_marked_rooms"] = [
        {"room": "a.ts", "sets": 5, "marks": 7, "rooms_at_this_count": 1, "listed_at_this_count": 1, "features": ["x", "y"]},
        {"room": "b.ts", "sets": 4, "marks": 6, "rooms_at_this_count": 8, "listed_at_this_count": 1, "features": ["x", "y"]},
    ]
    h["rooms_at_most_sets"] = 1
    h.pop("top_tier", None)  # D-061: the D-050/D-052 fill-row shape lives in the legacy (capped) renderer
    mm = render_most_marked(h)
    # D-052: the lead says the ordering, the cap and the most; what a row is, its cell says
    assert "1 room carries the most (5). The listed column is rows listed of rooms at the row's sets count; where fewer are listed than carry the count, the listed are the first by path." in mm
    assert "| b.ts | 4 | 6 | 1 of 8 |" in mm and "| a.ts | 5 | 7 | 1 of 1 |" in mm
    assert "| room | positions (distinct sets) | marks | listed of rooms at this count |" in mm
    assert "first by path, and its row says" not in mm  # the clause that was false as a per-row label (D-052)
    # a feature under two profiles is profile-qualified wherever it is named: the relation cell
    # and the most-marked features column use the matrix's labels
    labels = _b.qualified_labels(["p/foundation", "q/foundation", "p/hub"])
    assert labels == {"p/foundation": "p/foundation", "q/foundation": "q/foundation", "p/hub": "hub"}
    # the matrix note says what a shared count equal to a diagonal is, and names the floor
    assert f"between features with {_b.RELATION_MIN_ROOMS} or more rooms" in render_shared(f) or not f["shared_rooms"]
    # the disclosure names every decorative feature, its position name and its ungrounded signal
    dis = render_disclosure(f)
    dec = [x for x in f["features"] if x["decorative"]]
    if dec:
        assert str(f["decorative"]["count"]) in dis and "excluded from the diagnosis" in dis  # D-062: one line
        for x in dec:
            assert f"◌ {x['feature']} {x['count']}" in dis  # D-062: one line — each ◌ feature with its count; the position and reason are on the row
            for sig in re.findall(r"[a-z_]+_index", x.get("decorative_reason") or ""):
                assert sig in dis
    else:
        assert "No decorative marks" in dis
    # a draft is the only prose and carries the lint section; nothing else on the page is linted
    r = run_brief(_skeleton(sub), sub, draft=_good_draft(f))
    assert r["passed"] and "## Reading (draft)" in r["markdown"] and "## Register lint" in r["markdown"]
    assert render_brief(None, f, [], {}).count("## ") == render_brief("", f, [], {}).count("## ")



# D-054 (fifteenth seating): the page cited "mapper §7" for a question §7 did not list, and the two
# citation tests below matched "§n.n" only — an undotted section was never checked, and a dotted
# one resolved to the first such heading in three specs concatenated, whichever spec it was in.
# This is the citation grammar the page and the rulesets use: an optional spec name, a section
# (dotted or not), an optional "Qn" item. A named citation resolves in the named spec only.
_SPEC_FILES = {
    "system spec": "codebase-as-structure-system-spec.md",
    "mapper": "structural-mapper-spec.md",
    "architect-brief spec": "architect-brief-spec.md",
    "validation spec": "validation-spec.md",  # D-060: the header defines the tier names against it
}
_CITE = re.compile(r"(?:(system spec|mapper|architect-brief spec|validation spec)\s+)?§\s*(\d+(?:\.\d+)?)(?:\s+Q(\d+))?")


def _section_body(text: str, heading: str) -> str | None:
    pat = rf"^#+\s*{re.escape(heading)}\b" if "." in heading else rf"^#+\s*{re.escape(heading)}\.?\s"
    m = re.search(pat, text, re.M)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r"^#{1,3}\s", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def _spec_citations(root: Path, text: str) -> list[tuple[str, str | None]]:
    """Every §-citation in `text` resolved to its section body (None when it does not resolve);
    a Qn suffix requires a numbered item n inside that section."""
    specs = {k: (root / v).read_text(encoding="utf-8") for k, v in _SPEC_FILES.items()}
    out: list[tuple[str, str | None]] = []
    for m in _CITE.finditer(text):
        name, sec, q = m.group(1), m.group(2), m.group(3)
        bodies = [specs[name]] if name else list(specs.values())
        body = next((b for b in (_section_body(t, sec) for t in bodies) if b is not None), None)
        if body is not None and q and not re.search(rf"^{q}\.\s", body, re.M):
            body = None
        out.append((m.group(0), body))
    return out

def test_a_citation_in_a_ruleset_text_that_reaches_the_page_cites_a_section_that_speaks_of_the_feature():
    """D-050: the twelfth seating found the import_root caveat citing "§5.5" — the system spec's
    section on the ruleset as a versioned artifact, which resolves but carries no fan-in/entrance
    limit; the limit is D-028/D-029. R2 checks bracket citations in prose; nothing checked a section
    or decision reference inside a cell. Resolution is not enough (§5.5 resolved): every "§n.n" in
    a position name, caveat or decorative reason names a spec section whose body speaks of the
    feature or a signal its predicate reads, and every "D-nnn" a log entry that does."""
    import tomllib

    root = Path(__file__).resolve().parents[1]
    specs = "\n".join(
        (root / n).read_text(encoding="utf-8")
        for n in ("codebase-as-structure-system-spec.md", "structural-mapper-spec.md", "architect-brief-spec.md")
    )
    log = (root / "DECISIONS.md").read_text(encoding="utf-8")

    def section(text: str, pattern: str) -> str | None:
        m = re.search(pattern, text, re.M)
        if not m:
            return None
        rest = text[m.end():]
        nxt = re.search(r"^#{1,3}\s", rest, re.M)
        return rest[: nxt.start()] if nxt else rest

    seen = 0
    for rs in ("maintainability.toml", "onboarding.toml"):
        doc = tomllib.loads((root / "rulesets" / rs).read_text(encoding="utf-8"))
        for f in doc["feature"]:
            words = {f["name"], *re.findall(r"[a-z_]+", str(f.get("predicate", "")))} - {"and", "or", "p"}
            for field in ("position_name", "caveat", "decorative_reason"):
                text = str(f.get(field) or "")
                for cite, body in _spec_citations(root, text):
                    seen += 1
                    assert body is not None, (rs, f["name"], field, f"{cite} resolves to no heading (or no Qn item)")
                    assert any(re.search(rf"\b{re.escape(w)}\b", body) for w in words), (rs, f["name"], field, f"{cite} speaks of none of {sorted(words)}")
                for d in re.findall(r"\bD-\d{3}\b", text):
                    seen += 1
                    body = section(log, rf"^## {d}\b")
                    assert body is not None, (rs, f["name"], field, f"{d} resolves to no entry")
                    assert any(re.search(rf"\b{re.escape(w)}\b", body) for w in words), (rs, f["name"], field, f"{d} speaks of none of {sorted(words)}")
    assert seen >= 1  # the import_root caveat cites D-029
    # the shape the seating found: §5.5 resolves and speaks of no signal import_root reads
    body = section(specs, r"^#+\s*5\.5\b")
    assert body is not None and not re.search(r"\bfan_in\b|\bimport_root\b", body)


def test_sets_are_one_computation_co_location_is_in_sets_and_the_entry_record_is_the_manifest(sub):
    """D-052 (thirteenth seating). (1) The header's distinct-set count subtracted identical
    overlaps, which are floored at three rooms; the table counted set identity with no floor —
    two identical features under the floor, or three identical features, made them disagree under
    one name. One computation now. (2) A room under one predicate in two profiles carries two
    marks and is co-located with nothing: co-location is counted in sets. (3) is_package_entry is
    read from package.json (D-029), not the import graph; its record says so."""
    import repo_substrate.brief as _b

    def feat(name, rooms, profile="p", diagnostic=True):
        return {"feature": name, "profile": profile, "diagnostic": diagnostic, "decorative": not diagnostic, "rooms": rooms}

    # three identical features under the floor, and one that differs on a room
    fs = [feat("a", ["r1", "r2"]), feat("b", ["r1", "r2"]), feat("c", ["r1", "r2"]), feat("d", ["r1", "r3"])]
    assert _b.distinct_sets(fs) == 2  # n_diag - identical pairs would say 4 - 0 (floored) or 4 - 3
    assert _b.sets_per_room(fs) == {"r1": 2, "r2": 1, "r3": 1}
    assert _b.co_located(fs) == 1  # r2 carries three marks and one set
    top = _b.most_marked(fs)
    assert [m["room"] for m in top] == ["r1"] and top[0]["sets"] == 2 and top[0]["marks"] == 4
    assert top[0]["rooms_at_this_count"] == 1 and top[0]["listed_at_this_count"] == 1
    # one predicate under two profiles: two marks, one set, not co-located
    gs = [feat("foundation", ["r1"], "p"), feat("foundation", ["r1"], "q"), feat("hub", ["r2"])]
    assert _b.co_located(gs) == 0 and _b.most_marked(gs) == [] and _b.distinct_sets(gs) == 2
    # a tier listed in part: six rooms at two sets, cap five, each row says "5 of 6"
    hs = [feat("x", [f"r{i}" for i in range(6)]), feat("y", [f"r{i}" for i in range(6)] + ["z"])]
    top = _b.most_marked(hs)
    assert len(top) == _b.MOST_MARKED_ROOMS and all(m["listed_at_this_count"] == 5 and m["rooms_at_this_count"] == 6 for m in top)
    assert "| r0 | 2 | 2 | 5 of 6 (unlisted: r5) |" in _b.render_most_marked({"most_marked_rooms": top, "rooms_at_most_sets": 6})  # D-060: the tier names its unlisted room
    # the sheet agrees with the helpers on the fixture
    f = facts(_skeleton(sub), sub)
    assert f["distinct_room_sets"] == _b.distinct_sets(f["features"])
    assert f["co_located_rooms"] == _b.co_located(f["features"]) and f["units"]["co_located_rooms"].startswith("rooms carrying two or more distinct")
    assert "distinct diagnostic sets; gate" in _b.render_register(f)
    # the record beside a position is the record the predicate reads
    assert _b.record_of("is_package_entry == 1") == "package manifest"
    assert _b.record_of("fan_in == 0 and fan_out >= p75") == "import graph"
    for x in f["features"]:
        if x["feature"] == "package_entry":
            assert "(package manifest)" in _b.render_register(f)


def test_a_citation_on_the_rendered_page_names_a_section_that_speaks_of_its_sentence(sub):
    """D-052: D-050's citation check read ruleset fields only; the page's own fixed texts cite
    D-004 Q3, D-049 and system spec §5.3 from renderer literals. Every §n.n and D-nnn on the
    rendered page resolves, and its target shares a content word with the sentence that cites it."""
    root = Path(__file__).resolve().parents[1]
    specs = "\n".join(
        (root / n).read_text(encoding="utf-8")
        for n in ("codebase-as-structure-system-spec.md", "structural-mapper-spec.md", "architect-brief-spec.md")
    )
    log = (root / "DECISIONS.md").read_text(encoding="utf-8")

    def section(text: str, pattern: str) -> str | None:
        m = re.search(pattern, text, re.M)
        if not m:
            return None
        rest = text[m.end():]
        nxt = re.search(r"^#{1,3}\s", rest, re.M)
        return rest[: nxt.start()] if nxt else rest

    page = run_brief(_skeleton(sub), sub)["markdown"]
    seen = 0
    for sent in re.split(r"(?<=[.;])\s+", page):
        cites = [(c, b) for c, b in _spec_citations(root, sent)] + [(x, section(log, rf"^## {x}\b")) for x in re.findall(r"\b(D-\d{3})\b", sent)]
        if not cites:
            continue
        words = {w.lower() for w in re.findall(r"[A-Za-z][a-z]{5,}", sent)}
        for ref, body in cites:
            seen += 1
            assert body is not None, (ref, sent[:120])
            low = body.lower()
            assert any(re.search(rf"\b{w}", low) for w in words), (ref, sorted(words), sent[:120])
    assert seen >= 5  # D-004 Q3, D-049, system spec §5.3, architect-brief spec §5, mapper §7 Q7 at least
    # the shape the seating found: an undotted, spec-named citation is checked in the named spec
    assert _spec_citations(root, "mapper §7 Q7")[0][1] is not None
    assert _spec_citations(root, "mapper §7 Q9")[0][1] is None  # no such item
    assert _spec_citations(root, "architect-brief spec §5.3")[0][1] is None  # the brief spec has no 5.3; the system spec does


def test_a_partly_listed_tier_is_the_first_by_marks_then_path_and_a_blend_names_every_record_it_reads(sub):
    """D-053 (fourteenth seating). (1) The lead said a partly listed tier shows "the first by path";
    most_marked orders a tier by marks then path, and on mcp-secure-server the first by path at four
    sets (google.ts, 4 marks) was not the listed room (5 marks). The fixture that tested the lead
    had uniform marks. (2) bug_pressure_index reads recency — the clock — and its record said
    "edit record"; a blend's records now come from config.ALLOWED_INPUTS. (3) A containment the
    predicates guarantee says so. (4) A wing and the package count are defined on the page."""
    import repo_substrate.brief as _b
    from repo_substrate.config import ALLOWED_INPUTS

    def feat(name, rooms, profile="p", predicate="x >= p90"):
        return {"feature": name, "profile": profile, "diagnostic": True, "decorative": False, "rooms": rooms, "predicate": predicate}

    # a tier of seven at two sets where one room carries a third mark: it leads the tier
    rooms = [f"r{i}" for i in range(7)]
    fs = [feat("x", rooms), feat("y", rooms + ["z"]), feat("w", ["r6", "q"])]
    top = _b.most_marked(fs)
    assert top[0]["room"] == "r6" and top[0]["sets"] == 3  # three sets: alone at the top
    tier = [m for m in top if m["sets"] == 2]
    assert [m["room"] for m in tier] == ["r0", "r1", "r2", "r3"] and all(m["listed_at_this_count"] == 4 and m["rooms_at_this_count"] == 6 for m in tier)
    gs = [feat("x", rooms), feat("y", rooms + ["z"]), feat("v", ["r5", "r6", "q1", "q2", "q3"], predicate="y >= p90"), feat("u", ["r5", "r6", "q1", "q2", "q3"], profile="o", predicate="y >= p90")]
    # r5 and r6: three sets (x, y, v=u); the rest of the tier two. D-053 ordered a tier by marks then
    # path; D-054 dropped marks from the key (test_a_tier_orders_by_path_and_the_scope_count_is_over_the_population)
    top = _b.most_marked(gs)
    three = [m for m in top if m["sets"] == 3]
    assert [m["room"] for m in three] == ["r5", "r6"] and three[0]["marks"] == 4
    assert "the first by path" in _b.render_most_marked({"most_marked_rooms": top, "rooms_at_most_sets": 2})
    # every blend names the records of its declared inputs; every input maps to a raw signal
    for index, inputs in ALLOWED_INPUTS.items():
        for inp in inputs:
            assert _b.records_of_signal(_b._INPUT_SIGNAL.get(inp, inp)), (index, inp)
    assert _b.record_of("bug_pressure_index >= p90") == "clock and edit record"
    assert _b.record_of("load_index >= p90") == "import graph and size"
    assert _b.record_of("neglect_index >= p90") == "clock"
    assert _b.record_of("complexity_proxy_index >= p90") == "import graph and size"
    assert _b.record_of("change_pressure_index >= p90") == "clock and edit record"
    assert _b.record_of("last_touched_days >= p90 and load_index >= 0.10") == "import graph and clock and size"
    # a containment by predicate
    hub = feat("hub", ["a", "b", "c", "d"], predicate="centrality >= p90")
    cor = feat("corridor", ["a", "b", "c"], profile="o", predicate="centrality >= p90 and fan_out >= p50")
    emp = feat("lit", ["a", "b", "c"], predicate="last_touched_days <= p10")
    assert _b._conjoins(cor, hub) and not _b._conjoins(emp, hub) and not _b._conjoins(hub, cor)
    # on the fixture: the sheet carries wing_depth and packages, and the note and calibration say them
    f = facts(_skeleton(sub), sub)
    assert f["wing_depth"] >= 1 and f["packages"] >= 1
    reg = _b.render_register(f)
    assert f"**wing** — a directory at depth {f['wing_depth']} of the tree" in reg  # D-062: the note is a legend
    assert (f"spans {f['packages']} package scopes" in reg) == (f["packages"] > 1) and ("one package scope" in reg) == (f["packages"] == 1)
    assert f"ranks this repository's own {f['population']} rooms" in reg  # D-062: the pNN fact lives in the bold rule, not the calibration string
    for ov in f["overlaps"]:
        if ov["relation"] == "within":
            assert "by_predicate" in ov
            if ov["by_predicate"]:
                cell = "by its predicate; "
            else:  # D-056: the complement is defined — the signals in common, or none
                cell = f"reads {', '.join(ov['shared_signals'])} with it; " if ov["shared_signals"] else "no raw signal in common, one edge set read twice; "
            assert f"({cell}{ov['n_outside']} " in reg  # D-055: no fallback admitted (the sixteenth seating quoted the `or`)
    # the flooded_basement caveat reaches the page
    for x in f["features"]:
        if x["feature"] == "flooded_basement":
            assert x.get("caveat") and "not an importer" in reg


def test_a_tier_orders_by_path_and_the_scope_count_is_over_the_population(sub, tmp_path):
    """D-054 (fifteenth seating, eslint 0.21.0). (1) The page said the 473 rooms span 21 package
    scopes; 21 was counted over every substrate node (1481) and the rooms span 6 — the three other
    pages coincided, so D-053's fixture could not fail. The count is over the population and the
    rooms per scope are on the page. (2) "(tied)" named no partner: package_entry's cell named
    packages/eslint-config-eslint 4 / 5 over lib 4 by name order. (3) Within a tier of equal sets,
    marks differ only by the double count the register discounts; the tier orders by path. (4) A
    reason about a signal is written once ([signal_reason]) and every row that reads the signal
    carries it — crack said "unvalidated" where toothpick_wing said what the tuning did; the
    tuning claim is tested against config/tuned.toml. (5) The page cited mapper §7 for a question
    it did not list (see the citation grammar above)."""
    import tomllib

    import repo_substrate.brief as _b
    from repo_substrate.config import ALLOWED_INPUTS
    from repo_substrate.mapper.ruleset import RulesetError

    root = Path(__file__).resolve().parents[1]
    sk = _skeleton(sub)
    # (1) nodes outside the population carry scopes the population does not
    sub2 = json.loads(json.dumps(sub))
    rooms = set(sk["strata"]["by_node"])
    for n in sub2["nodes"]:
        if n["id"] in rooms:
            n.setdefault("metrics", {})["package"] = "pkg/a" if n["id"] < "src/m" else ""
    sub2["nodes"].append({"id": "tests/x.test.ts", "kind": "file", "lang": "ts", "metrics": {"package": "tests/only"}, "derived": {}})
    sub2["nodes"].append({"id": "tests/y.test.ts", "kind": "file", "lang": "ts", "metrics": {"package": "tests/other"}, "derived": {}})
    f = facts(sk, sub2)
    over_rooms = {(lambda pk: f"{pk}/{_b.ROOT_SCOPE}" if pk else _b.ROOT_SCOPE)(next(n for n in sub2["nodes"] if n["id"] == r)["metrics"].get("package")) for r in rooms}
    assert f["packages"] == len(over_rooms) and {e["scope"] for e in f["by_package"]} == over_rooms
    assert sum(e["rooms"] for e in f["by_package"]) == f["population"]
    assert [e["rooms"] for e in f["by_package"]] == sorted((e["rooms"] for e in f["by_package"]), reverse=True)
    assert isinstance(f["by_package"], list)  # D-056: an ordered list survives the sheet's sorted keys
    reg = _b.render_register(f)
    scopes = " · ".join(f"{e['scope']} {e['rooms']}" for e in f["by_package"])
    assert f"spans {f['packages']} package scopes, pooled (rooms per scope, largest first, each scope named by the manifest that holds it: {scopes})" in reg  # D-062: in the wing legend line
    assert "pkg/a/package.json" in scopes and _b.ROOT_SCOPE == "package.json"
    assert "tests/only" not in reg and f"{f['packages']} package scopes pooled" in f["calibration"]  # D-062: the header keeps the pointer; the bold rule carries the pNN fact
    # (2) a tie names every partner with its numbers; the wing-named partner is marked as the parent
    sk2 = json.loads(json.dumps(sk))
    tmpl = next(x for x in sk2["features"] if x["diagnostic"] and not x["decorative"])
    tie_rooms = ("lib/a.ts", "lib/b.ts", "lib/c.ts", "pkg/d.ts", "pkg/e.ts", "pkg/f.ts")
    for nid in tie_rooms + ("lib/g.ts",):
        sk2["strata"]["by_node"][nid] = sk2["strata"]["by_node"][tmpl["node"]]
    sk2["features"] = [dict(tmpl, feature="tie", node=nid) for nid in tie_rooms]
    sk2["overlays"] = []
    g = facts(sk2, sub2)
    dd = next(x for x in g["features"] if x["feature"] == "tie")["dominant_dir"]
    assert dd["tied"] and dd["dir"] == "pkg" and dd["tied_with"] == [{"dir": "lib", "n": 3, "population": 4}]
    cell = _b.render_register(g)
    m = re.search(r"\| [^|]*tied[^|]*\|", cell)
    assert m and m.group(0) == "| pkg (as parent, not the wing) 3 / 3 (tied with lib (as parent, not the wing) 3 / 4) |", m.group(0) if m else cell
    # (3) equal sets, unequal marks: path orders the tier
    def feat(name, rooms, profile="p", predicate="x >= p90"):
        return {"feature": name, "profile": profile, "diagnostic": True, "decorative": False, "rooms": rooms, "predicate": predicate}

    # a: sets {x, w}, 2 marks; b: sets {x, y=y}, 3 marks — the same count of sets, one of b's doubled
    fs = [feat("x", ["a", "b"]), feat("w", ["a"], predicate="w >= p90"), feat("y", ["b"], predicate="y >= p90"), feat("y", ["b"], profile="o", predicate="y >= p90")]
    top = _b.most_marked(fs)
    assert [(m["room"], m["sets"], m["marks"]) for m in top] == [("a", 2, 2), ("b", 2, 3)]
    lead = _b.render_most_marked({"most_marked_rooms": top, "rooms_at_most_sets": 2})
    assert "then by path — marks (one per feature per profile) are shown and order nothing" in lead and "by marks" not in lead.split("order nothing")[1]
    # (4) the signal's reason on every row that reads it, once in the disclosure, and true of the tuning
    rs = load_ruleset(RULESET)
    dec = {x.name: x for x in rs.features if x.decorative}
    assert set(rs.signal_reasons) == {"bug_pressure_index"} and set(dec) == {"crack", "toothpick_wing"}
    for x in dec.values():
        assert x.decorative_reason.startswith("bug_pressure_index is " + rs.signal_reasons["bug_pressure_index"])
        assert x.decorative_signal_reasons == rs.signal_reasons
    assert "fragility half" in dec["toothpick_wing"].decorative_reason and "fragility half" not in dec["crack"].decorative_reason
    tuned = tomllib.loads((root / "config" / "tuned.toml").read_text(encoding="utf-8"))["weights"]["bug_pressure_index"]
    fix_inputs = [i for i in ALLOWED_INPUTS["bug_pressure_index"] if i.startswith("fix")]
    assert fix_inputs and all(tuned.get(i, 0) == 0 for i in fix_inputs)  # "assign zero to fix history"
    assert "zero to fix history" in rs.signal_reasons["bug_pressure_index"]
    page = run_brief(sk, sub)["markdown"]
    rows = [line for line in page.splitlines() if line.startswith("| ") and "| ◌ " in line]
    assert rows and any("| ◌ crack |" in r for r in rows)  # crack fires on the fixture
    assert all("zero to fix history" in r for r in rows)
    assert page.count("zero to fix history") == len(rows)  # every decorative row; D-062: the section no longer repeats it
    assert "excluded from the diagnosis: the signal they read (bug_pressure_index) is unvalidated; each row carries the reason." in page  # D-062: the section is one line; the reason is on the rows
    # the loader: a signal with a reason is read by decorative features only; no orphan reasons
    def _rs(body):
        p = tmp_path / "rs.toml"
        p.write_text('[ruleset]\nname = "t"\nversion = "0.0.1"\nprofile = "t"\ndescription = "t"\nwing_depth = 1\n\n' + body, encoding="utf-8")
        return load_ruleset(p)

    with pytest.raises(RulesetError, match="without decorative"):
        _rs('[signal_reason]\nbug_pressure_index = "unvalidated"\n\n[[feature]]\nname = "x"\npredicate = "bug_pressure_index >= p90"\n')
    with pytest.raises(RulesetError, match="no feature reads"):
        _rs('[signal_reason]\nneglect_index = "unvalidated"\n\n[[feature]]\nname = "x"\npredicate = "fan_in >= p90"\n')
    ok = _rs('[signal_reason]\nbug_pressure_index = "unvalidated (D-015)"\n\n[[feature]]\nname = "x"\npredicate = "bug_pressure_index >= p90"\ndecorative = true\n')
    assert ok.features[0].decorative_reason == "bug_pressure_index is unvalidated (D-015)."


def test_a_guaranteed_containment_is_drawn_under_the_floor_and_the_ordering_text_is_one(sub):
    """D-055 (sixteenth seating, typeorm 0.22.0). (1) toothpick_wing's two rooms were inside
    foundation and crack by conjunction and the cell said "too few rooms to relate (2)" — D-041's
    floor is for containment by accident; a containment the predicates guarantee is drawn at any
    count. (2) A decorative row prints its predicate ("the fragility half" of a reason was
    unresolvable from a row that showed the reason and not the conjunction). (3) The sheet's unit
    gloss for most_marked_rooms kept "then marks" after D-054 dropped it from the key; the lead and
    the gloss now share one text. (4) "(root)" was the wing and the scope in one note; the scope is
    "(root manifest)". (5) Every § on the page names its spec (D-054's third clause, made a rule)."""
    import repo_substrate.brief as _b

    root = Path(__file__).resolve().parents[1]
    sk = _skeleton(sub)
    # (1) a two-room feature whose predicate conjoins a larger feature's, and one whose does not
    sk2 = json.loads(json.dumps(sk))
    tmpl = next(x for x in sk2["features"] if x["diagnostic"] and not x["decorative"])
    big_rooms = sorted(sk2["strata"]["by_node"])[:4]  # the fixture's features carry one room each; build one with four
    big = dict(tmpl, feature="bigf", predicate="fan_in >= p90", decorative=False, decorative_reason=None)
    inner = dict(big, feature="tiny_in", predicate="fan_in >= p90 and lines >= p50", decorative=True, decorative_reason="tiny_in is decorative on purpose (lines)", diagnostic=False)
    loose = dict(big, feature="tiny_off", predicate="fan_in >= p95")
    sk2["features"] = [dict(big, node=r) for r in big_rooms] + [dict(inner, node=r) for r in big_rooms[:2]] + [dict(loose, node=r) for r in big_rooms[:2]]
    sk2["overlays"] = []
    g = facts(sk2, sub)
    key = lambda n: f"{sk2['profile']['name']}/{n}"  # noqa: E731
    drawn = [o for o in g["overlaps"] if o["a"] == key("tiny_in")]
    assert drawn and all(o["relation"] == "within" and o["by_predicate"] for o in drawn)
    assert any(o["b"] == key(big["feature"]) and o["n_outside"] == len(big_rooms) - 2 for o in drawn)
    assert not [o for o in g["overlaps"] if key("tiny_off") in (o["a"], o["b"])]
    reg = _b.render_register(g)
    row_in = _row(reg, "tiny_in", decorative=True)
    row_off = _row(reg, "tiny_off")
    assert f"⊂ {big['feature']} (by its predicate; {len(big_rooms) - 2} {big['feature']} room" in row_in and row_in.count("too few rooms for any other relation (2)") == 1
    assert "| too few rooms to relate (2) |" in row_off and "⊂" not in row_off  # D-057: no "other" without an antecedent
    # the other side draws it too, and the counts count it
    row_big = _row(reg, big["feature"])
    assert "⊃ ◌ tiny_in (by its predicate;" in row_big  # D-056: ◌ travels with the name
    assert g["relation_counts"]["within"] >= len(drawn)
    # (2) the decorative row prints its predicate before its reason
    assert f"| `{inner['predicate']}` — ◌ excluded from the diagnosis: tiny_in is decorative on purpose (lines) |" in row_in  # D-060
    assert "and a containment the predicates guarantee at any count" in reg and "predicate; caveat or reason |" in reg
    # (3) one ordering text
    f = facts(sk, sub)
    lead = _b._render_most_marked_legacy(g)  # D-061: the capped list is legacy; its lead and the sheet's gloss still share one text
    assert g["most_marked_rooms"] and _b.MOST_MARKED_ORDER in g["units"]["most_marked_rooms"] and _b.MOST_MARKED_ORDER in lead
    assert "then marks" not in f["units"]["most_marked_rooms"] and "by marks" not in f["units"]["most_marked_rooms"]
    # (4) the scope's root is not the wing's
    assert _b.ROOT_SCOPE != "(root)" and _b.ROOT_SCOPE in f["units"]["by_package"] and "ordered list" in f["units"]["by_package"]
    # (5) every § on the page names its spec
    page = run_brief(sk, sub)["markdown"]
    for m in re.finditer(r"§", page):
        before = page[max(0, m.start() - 24) : m.start()]
        assert re.search(r"(system spec|mapper|architect-brief spec|validation spec)\s*$", before), page[max(0, m.start() - 60) : m.start() + 10]
    assert page.count("§") >= 1  # system spec §5.3 at least; the pooled sentence needs two scopes


def test_a_containment_not_by_predicate_says_the_signal_in_common_and_a_scope_is_named_by_its_manifest(sub):
    """D-056 (seventeenth seating, mcp-secure-server 0.23.0). (1) toothpick_wing ⊂ lit_room was the
    one unmarked containment beside three "by its predicate" — read as independent news while
    bug_pressure_index reads recency, the clock lit_room reads; the complement of the marker is
    defined: the raw signals the two predicates read in common (blends expanded through
    ALLOWED_INPUTS), or "no signal in common". (2) "cookbook 136" (wing) and "cookbook 1" (scope)
    sat in one paragraph; a scope is named by its manifest path. (3) by_package is an ordered list
    (the sheet is written with sorted keys; "largest first" was false of the file). (4) ◌ travels
    with the name into relation cells. (5) Containers that are one set are one entry."""
    import repo_substrate.brief as _b

    sk = _skeleton(sub)
    sk2 = json.loads(json.dumps(sk))
    tmpl = next(x for x in sk2["features"] if x["diagnostic"] and not x["decorative"])
    rooms = sorted(sk2["strata"]["by_node"])
    mk = lambda **kw: dict(tmpl, **{"decorative": False, "decorative_reason": None, **kw})  # noqa: E731
    fresh = mk(feature="fresh", predicate="last_touched_days <= p10")  # the clock, directly
    hot = mk(feature="hot", predicate="bug_pressure_index >= p90", decorative=True, decorative_reason="hot rests on bug_pressure_index (unvalidated)")  # the clock, through a blend
    wide = mk(feature="wide", predicate="lines >= p50")
    narrow = mk(feature="narrow", predicate="fan_in >= p95")
    sk2["features"] = (
        [dict(fresh, node=r) for r in rooms[:5]] + [dict(hot, node=r) for r in rooms[:3]]
        + [dict(wide, node=r) for r in rooms[:6]] + [dict(narrow, node=r) for r in rooms[:3]]
    )
    # (5) wide under a second profile draws the same set
    sk2["overlays"] = [{"profile": "onboarding", "features": [dict(wide, node=r) for r in rooms[:6]]}]
    sub2 = json.loads(json.dumps(sub))
    wing = rooms[0].split("/")[0]
    for n in sub2["nodes"]:
        if n["id"] in rooms[:2]:
            n.setdefault("metrics", {})["package"] = wing  # a scope keyed by a wing's name — the cookbook shape
    g = facts(sk2, sub2)
    P = sk2["profile"]["name"]
    ov = {(o["a"], o["b"]): o for o in g["overlaps"] if o["relation"] == "within"}
    hot_fresh = ov[(f"{P}/hot", f"{P}/fresh")]
    assert not hot_fresh["by_predicate"] and hot_fresh["shared_signals"] == ["last_touched_days"]
    assert "last_touched_days" in _b._signals_read("bug_pressure_index >= p90") and _b._signals_read("x >= p90 and y <= 1") == {"x", "y"}
    narrow_wide = ov[(f"{P}/narrow", f"{P}/wide")]
    assert not narrow_wide["by_predicate"] and narrow_wide["shared_signals"] == []
    reg = _b.render_register(g)
    row_hot = _row(reg, "hot", decorative=True)
    assert "⊂ fresh (reads last_touched_days with it; 2 fresh rooms outside this set)" in row_hot
    row_narrow = _row(reg, "narrow")
    assert "⊂ maintainability/wide = onboarding/wide (no raw signal in common, one edge set read twice; 3 " in row_narrow and row_narrow.count("wide") == 3  # D-062: the cell carries its correction  # two names, one entry, one outside count
    # (4) the decorative name carries ◌ where a diagnostic row names it
    row_fresh = _row(reg, "fresh")
    assert "⊃ ◌ hot (reads last_touched_days with it; 2 of these rooms outside it)" in row_fresh
    # (2)/(3) the scope keyed by the wing's name is named by its manifest, and the list is ordered
    scopes = [e["scope"] for e in g["by_package"]]
    assert f"{wing}/package.json" in scopes and "package.json" in scopes and not set(scopes) & set(g["wings"])
    assert [e["rooms"] for e in g["by_package"]] == sorted((e["rooms"] for e in g["by_package"]), reverse=True)
    note = reg.split("|")[0]
    assert f"{wing} {g['wings'][wing]}" in note and f"{wing}/package.json 2" in note
    # the sheet round-trips through sorted keys with its order intact
    back = json.loads(json.dumps(g, sort_keys=True))
    assert back["by_package"] == g["by_package"]


def test_a_feature_that_fired_on_nothing_keeps_its_row_and_the_marker_is_defined_on_the_page(sub):
    """D-057 (eighteenth seating, registry 0.24.0). (1) toothpick_wing fired on no room and had no
    row; rows come from the ruleset's roster on the skeleton, so an unfired feature keeps a row at 0.
    (2) "no signal in common" was undefined on the page and read as independence; the note defines
    both values, and a derived index outside the tuned blends expands through its grounding
    (reinforcement_index → test_fan_in). (3) The import graph and the test graph are one edge set:
    a test file's import counts in fan_in and centrality and in test_fan_in — a fixed text, held
    to the substrate (fan_in >= test_fan_in on every node). (4) scaffolding's floor and its test
    convention are a caveat (maintainability 0.2.7). (5) Ruleset versions in the header."""
    import repo_substrate.brief as _b

    sk = _skeleton(sub)
    f = facts(sk, sub)
    # (1) the roster: every feature of both rulesets has a row, fired or not
    base, ov = load_ruleset(RULESET), load_ruleset(ONBOARDING)
    on_sheet = {(x["profile"], x["feature"]) for x in f["features"]}
    assert {(base.profile, x.name) for x in base.features} | {(ov.profile, x.name) for x in ov.features} <= on_sheet
    assert sk["profile"]["roster"] and sk["overlays"][0]["roster"]
    zero = [x for x in f["features"] if x["count"] == 0]
    assert zero, "the small fixture leaves at least one feature unfired"
    reg = _b.render_register(f)
    for x in zero:
        row = _row(reg, x["feature"], decorative=x["decorative"], profile=x["profile"])
        assert "| 0 | no wing (0) | no rooms | no rooms to relate (0) |" in row and f"`{x['predicate']}`" in row
    assert "keeps its row at 0" not in reg  # D-062 (Rams): the row says it; the sentence was a repetition
    dec0 = [x for x in zero if x["decorative"]]
    if dec0:
        dis = _b.render_disclosure(f)
        assert all(f"◌ {x['feature']} 0" in dis for x in dec0)  # D-062: the zero is in the one-line legend
        assert f"{dec0[0]['feature']} 0" in reg  # the header's decorative list carries the count
    # (2) the marker's values are defined on the page; the grounding expansion
    assert "Otherwise the cell says which raw signals the two predicates read in common (a blend or index expanded through its declared inputs), or 'no raw signal in common' — a signal, not an instrument." in reg
    assert _b._signals_read("reinforcement_index >= 0.5") == {"test_fan_in"}
    assert _b._signals_read("centrality >= p90 and fan_out >= p50") & _b._signals_read("reinforcement_index >= 0.5") == set()
    # (3) one edge set: the fixed text, and the invariant it states, on the substrate
    assert "one edge set read twice: a test file is a node whose imports count in fan_in and centrality, and test_fan_in counts those importers alone" in reg
    for n in sub["nodes"]:
        m = n["metrics"]
        assert m.get("fan_in", 0) >= m.get("test_fan_in", 0), n["id"]
    # (4) the caveat reaches the page; the floor it states is the index's
    sc = next(x for x in f["features"] if x["feature"] == "scaffolding")
    assert sc["caveat"] and "0.5 is its floor, not a midpoint" in reg and "helper or fixture under the test paths counts" in reg
    for n in sub["nodes"]:
        r = (n.get("derived") or {}).get("reinforcement_index")
        if r is not None:
            assert r == 0.0 or r >= 0.5, (n["id"], r)
    # (5) versions in the header
    page = run_brief(sk, sub)["markdown"]
    assert f"Profile {base.profile} {base.version} + {ov.profile} {ov.version}," in page
    assert f["profile_versions"] == {base.profile: base.version, ov.profile: ov.version}
    # a skeleton without a roster (older) still renders the fired set
    sk_old = json.loads(json.dumps(sk))
    sk_old["profile"].pop("roster")
    for od in sk_old["overlays"]:
        od.pop("roster")
    g = facts(sk_old, sub)
    assert all(x["count"] > 0 for x in g["features"])


def test_the_defence_sits_in_the_cell_it_defends_and_the_page_carries_its_snapshot(sub, tmp_path):
    """D-060 (the control seating and the skimmer, both on registry 0.25.1, both unpointed). Skimmer:
    the table read as a leaderboard, the note skipped whole, the feature name read for the position —
    the rule stands first in bold, the position is the first column, the tier table carries the rule
    over it, ◌ says "excluded". Control: the tier names are defined where they are used; the page
    carries its snapshot; a caveat's case is counted beside it; a partly listed tier names its
    unlisted rooms; a single-pNN row says the share the rank fixes by construction."""
    import repo_substrate.brief as _b
    from repo_substrate.mapper.ruleset import RulesetError

    sk = _skeleton(sub)
    f = facts(sk, sub)
    reg = _b.render_register(f)
    page = run_brief(sk, sub)["markdown"]
    # the rule first, bold, before the italic note; the position is the first column
    note_start = reg.index(f"*{f['population']} rooms in ")  # D-062: the note opens on the counts
    rule = reg.index("**A position names where a room sits in a record")
    assert rule < note_start and f"ranks this repository's own {f['population']} rooms" in reg[rule:note_start]
    header = next(line for line in reg.splitlines() if line.startswith("| position"))
    assert header.startswith("| position (the record it reads) | feature | profile | rooms |")
    # the tier table carries the rule over it and no longer calls itself "most-marked"
    assert "### Rooms at the most positions" in reg and "Most-marked" not in reg
    if f["most_marked_rooms"]:  # the small fixture has no tier; the caption is tested on a synthetic one below
        assert "**A count of the positions a room sits at; the order is the count, then the path — not a ranking and not a severity (D-004 Q3).**" in reg
    # ◌ = excluded, on the row, in the note and in the section
    assert "**◌** — an excluded feature (the ruleset's word is decorative)" in reg and "## Excluded marks (◌)" in page
    for x in f["features"]:
        if x["decorative"] and x["count"]:
            assert "— ◌ excluded from the diagnosis:" in _row(reg, x["feature"], decorative=True)
    # the snapshot and the tier names, in the header
    assert f["as_of"] == sub["repo"]["as_of"] and f"As of {str(f['as_of'])[:10]}, commit `{f['repo']['head_sha'][:12]}`." in page
    assert "asserted is a description that held under the stability budget and the corroboration its grounding class requires (validation spec §2.4), validated a forecast confirmed by a temporal holdout (validation spec §3)" in reg  # D-061: the gloss no longer claims a cross-modal check
    assert "stability is the `substrate timelapse` run under gate" in page and "not this page" in page  # D-062: said once
    # a single-pNN row states its share by construction; a conjunction does not
    # D-061: the sentence states the realized share and the cutoff, not "10% by construction" (eslint: 83 of 473, 80 tied at the cutoff)
    assert _b._share_by_construction("last_touched_days >= p90", 83, 473, {"last_touched_days >= p90": 533.966}, 80) == " — rooms at or above this repository's p90 on last_touched_days (here 533.966 days): 83 of 473, 17.5%; 80 at the cutoff value"
    assert _b._share_by_construction("last_touched_days >= p90", 70, 583, {"last_touched_days >= p90": 1629.7122}, 70).endswith("70 of 583, 12.0%; all 70 at the cutoff value")  # D-062: typeorm's one mass commit
    assert _b._share_by_construction("last_touched_days <= p10", 48, 473, {"last_touched_days <= p10": 12.5}) == " — rooms at or below this repository's p10 on last_touched_days (here 12.5 days): 48 of 473, 10.1%"
    assert _b._share_by_construction("fan_in >= p75", 148, 473, {}) == " — rooms at or above this repository's p75 on fan_in (here unresolved): 148 of 473, 31.3%"
    assert _b._share_by_construction("centrality >= p90 and fan_out >= p50") == "" and _b._share_by_construction("reinforcement_index >= 0.5") == ""
    dark = _row(reg, "dark_room")
    dk = next(x for x in f["features"] if x["feature"] == "dark_room")
    assert f"on last_touched_days (here {dk['thresholds']['last_touched_days >= p90']:g} days): {dk['count']} of {f['population']}, {100.0 * dk['count'] / f['population']:.1f}%" in dark
    # a caveat's case is counted beside the caveat, from the substrate's metrics
    fb = next(x for x in f["features"] if x["feature"] == "flooded_basement")
    assert fb["caveat_case"] == "fan_in == 0" and fb["caveat_case_count"] == sum(1 for r in fb["rooms"] if f["rooms"][r]["fan_in"] == 0)
    if fb["count"]:
        assert f"(this case: {fb['caveat_case_count']} of {fb['count']} here)" in _row(reg, "flooded_basement")
    assert _b._case_holds("fan_in == 0 and fan_out >= 2", {"fan_in": 0, "fan_out": 3}) and not _b._case_holds("fan_in == 0", {"fan_in": 1}) and not _b._case_holds("fan_in == 0", {})
    # a partly listed tier names the rooms it leaves out
    def feat(name, rooms, profile="p", predicate="x >= p90"):
        return {"feature": name, "profile": profile, "diagnostic": True, "decorative": False, "rooms": rooms, "predicate": predicate}

    rooms = [f"r{i}" for i in range(9)]
    top = _b.most_marked([feat("x", rooms), feat("y", rooms, predicate="y >= p90")])  # x and y draw one set: one set each, no tier
    assert top == []
    top = _b.most_marked([feat("x", rooms), feat("y", rooms + ["z"], predicate="y >= p90")])
    assert all(m["unlisted"] == ["r5", "r6", "r7", "r8"] for m in top)
    mm = _b.render_most_marked({"most_marked_rooms": top, "rooms_at_most_sets": 9})
    assert "5 of 9 (unlisted: r5, r6, r7, r8)" in mm
    assert "**A count of the positions a room sits at; the order is the count, then the path — not a ranking and not a severity (D-004 Q3).**" in mm
    big = _b.most_marked([feat("x", [f"q{i:02d}" for i in range(12)]), feat("y", [f"q{i:02d}" for i in range(12)] + ["z"], predicate="y >= p90")])
    assert "(unlisted: q05, q06, q07, q08, q09 and 2 more)" in _b.render_most_marked({"most_marked_rooms": big, "rooms_at_most_sets": 12})
    # the loader: a caveat_case needs a caveat and reads literals only
    def _rs(body):
        p = tmp_path / "rs.toml"
        p.write_text('[ruleset]\nname = "t"\nversion = "0.0.1"\nprofile = "t"\ndescription = "t"\nwing_depth = 1\n\n' + body, encoding="utf-8")
        return load_ruleset(p)

    with pytest.raises(RulesetError, match="without a caveat"):
        _rs('[[feature]]\nname = "x"\npredicate = "fan_in >= p90"\ncaveat_case = "fan_in == 0"\n')
    with pytest.raises(RulesetError, match="percentile"):
        _rs('[[feature]]\nname = "x"\npredicate = "fan_in >= p90"\ncaveat = "reads fan-in"\ncaveat_case = "fan_out >= p50"\n')


def test_a_row_states_its_realized_share_and_the_tier_table_is_the_whole_top_tier_by_path(sub):
    """D-061 (the eslint control and the second skimmer, both unpointed, on 0.26.0). (1) "the top 10%
    … by construction" stood beside dark_room 83 of 473 — 80 rooms tied at the cutoff; a row states
    the share it realized and the cutoff this population resolved to, from the sheet. (2) The bold
    caption over a capped, count-ordered list was read and bounced; the table is every room at the
    most positions, by path, with its size. (3) The population rule (a room is a source file outside
    the test convention; N of M files), the resolver's limit (unresolved / external imports) and the
    tier gloss (grounding class, not "cross-modal") are on the page, from the substrate."""
    import repo_substrate.brief as _b

    sk = _skeleton(sub)
    f = facts(sk, sub)
    reg = _b.render_register(f)
    # (1) thresholds travel and the row's share is computed from its count
    for x in f["features"]:
        if x["count"] and len(x["predicate"].split(" and ")) == 1 and "p" in x["predicate"].split()[-1]:
            assert x["predicate"] in x["thresholds"], x["feature"]
            share = 100.0 * x["count"] / f["population"]
            assert f"{x['count']} of {f['population']}, {share:.1f}%" in _row(reg, x["feature"], decorative=x["decorative"], profile=x["profile"])
    assert "by construction" not in reg.split("*Rendered")[0]  # the bold rule no longer says "a tenth by construction"
    assert "or more where rooms tie at the cutoff; each row states its share" in reg
    # (3) the population rule and the resolver's limit, from the substrate
    n_test = sum(1 for n in sub["nodes"] if n["metrics"].get("is_test"))
    n_unindexed = sum(1 for n in sub["nodes"] if not n["metrics"].get("is_test") and (n.get("derived") or {}).get("indices") is None)
    assert f["node_count"] == len(sub["nodes"]) and f["test_nodes"] == n_test and f["unindexed_nodes"] == n_unindexed
    assert f["population"] + n_test + n_unindexed == len(sub["nodes"])  # the mapper's population rule, restated on the page
    assert f"A room is a source file outside the test convention with computed signals: {f['population']} of the tree's {f['node_count']} files; the {n_test} test files are nodes of the import graph and not rooms" in reg
    if n_unindexed:
        assert f"{n_unindexed} file{'s' if n_unindexed != 1 else ''} with no computed signals" in reg
    assert f["unresolved_imports"] == sub["summary"]["unresolved_imports"] and f"The graph is resolved statically: {f['unresolved_imports']} imports in the tree did not resolve to a file and {f['external_imports']} are external packages" in reg
    assert "cross-modal" not in reg and "the corroboration its grounding class requires (validation spec §2.4)" in reg
    # (2) the tier table: every room at the top count, by path, with lines, and no count-ordered cap
    def feat(name, rooms, profile="p", predicate="x >= p90"):
        return {"feature": name, "profile": profile, "diagnostic": True, "decorative": False, "rooms": rooms, "predicate": predicate}

    rooms = [f"r{i:02d}" for i in range(9)]
    fs = [feat("x", rooms + ["z"]), feat("y", rooms, predicate="y >= p90"), feat("w", ["r03", "r07"], predicate="w >= p90")]
    tier = _b.top_tier(fs, {r: {"size_loc": 10 * (i + 1)} for i, r in enumerate(rooms)})
    assert tier["sets"] == 3 and [m["room"] for m in tier["rooms"]] == ["r03", "r07"] and tier["rooms"][0]["lines"] == 40
    doc = {"top_tier": tier, "co_located_rooms": 9}
    mm = _b.render_most_marked(doc)
    assert "### Rooms at the most positions (3)" in mm and "in path order — a set, not a ranking" in mm
    assert "| r03 | 40 | — | w, x, y |" in mm and "| r07 | 80 | — | w, x, y |" in mm and "marks" not in mm.split("|---")[0].split("| room")[1]  # D-062: no constant column; importers when known
    assert "2 rooms. " in mm and "9 rooms carry two or more distinct sets" in mm
    big = _b.top_tier([feat("x", [f"q{i:02d}" for i in range(30)]), feat("y", [f"q{i:02d}" for i in range(30)] + ["z"], predicate="y >= p90")], {})
    mmb = _b.render_most_marked({"top_tier": big})
    assert f"the first {_b.TOP_TIER_CAP} by path are listed and 5 more are not" in mmb and mmb.count("| q") == _b.TOP_TIER_CAP and "| q00 | — | — |" in mmb
    # a sheet without top_tier renders the legacy capped list
    assert "listed of rooms at this count" in _b.render_most_marked({"most_marked_rooms": _b.most_marked(fs), "rooms_at_most_sets": 2})
    # the real sheet's table is the whole top tier
    if f["top_tier"]["rooms"]:
        for m in f["top_tier"]["rooms"]:
            assert f"| {m['room']} |" in reg


def test_instance_counts_where_a_mechanism_dominates_and_the_note_is_a_legend(sub):
    """D-062 (the typeorm control, the third skimmer, the Rams audit — all unpointed, on 0.27.0).
    Control: all 70 dark rooms sat at the cutoff and the row said "ties"; every importer of the
    top room was a test file and the row said "one edge set"; a count each. Skimmer: the first
    row was the excluded feature; ◌ rows render last. Rams: the note repeated the header, the
    cells and the column headers — it is a legend now; two features drawing one set were two
    identical matrix rows — one row; the tier table's constant column is gone; the excluded
    section is one line; the scope list is gated as the calibration sentence is."""
    import repo_substrate.brief as _b

    sk = _skeleton(sub)
    f = facts(sk, sub)
    reg = _b.render_register(f)
    page = run_brief(sk, sub)["markdown"]
    # ties at the cutoff are counted on the sheet and said on the row
    for x in f["features"]:
        if x.get("at_cutoff") is not None and x["count"]:
            assert 0 <= x["at_cutoff"] <= x["count"]
            row = _row(reg, x["feature"], decorative=x["decorative"], profile=x["profile"])
            if x["at_cutoff"] > 1:
                assert (f"all {x['count']} at the cutoff value" if x["at_cutoff"] == x["count"] else f"{x['at_cutoff']} at the cutoff value") in row
            else:
                assert "at the cutoff value" not in row
    # importers from tests, per import-graph row, from the substrate
    nodes = {n["id"]: n for n in sub["nodes"]}
    for x in f["features"]:
        if x.get("importers"):
            assert x["importers"]["total"] == sum(nodes[r]["metrics"]["fan_in"] for r in x["rooms"])
            assert x["importers"]["from_tests"] == sum(nodes[r]["metrics"]["test_fan_in"] for r in x["rooms"])
            if x["importers"]["total"]:
                assert f"importers of these rooms: {x['importers']['total']}, {x['importers']['from_tests']} (" in _row(reg, x["feature"], decorative=x["decorative"], profile=x["profile"])
        elif x["count"] and _b._signals_read(x["predicate"]) & {"fan_in", "centrality"}:
            raise AssertionError(x["feature"])
    # cross-scope edges are counted; the sentence appears only on a multi-scope page
    assert f["cross_scope_edges"] == sum(1 for e in sub["edges"] if nodes[e["from"]]["metrics"].get("package", "") != nodes[e["to"]]["metrics"].get("package", ""))
    assert ("imports cross a package scope" in reg) == (f["packages"] > 1)
    # ◌ rows last
    order = [line for line in reg.splitlines() if line.startswith("| ") and "|---" not in line and not line.startswith("| position") and "| shared rooms" not in line]
    table_rows = order[: len(f["features"])]
    marks = [("| ◌ " in r) for r in table_rows]
    assert marks == sorted(marks), "excluded rows are not last"
    # the note is a legend: the counts, then one line per term; no repetition of the header or the zero-row sentence
    assert "- **wing** —" in reg and "- **◌** —" in reg and "- **relation to** —" in reg and "- **caveat** —" in reg and "- **the import graph and the test graph** —" in reg
    for gone in ("no cell is written", "The record a position is read from is named beside it", "keeps its row at 0", "is a cell's own answer, not a gap", "follow the table"):
        assert gone not in reg, gone
    assert page.count("was cut at D-049") == 0 and page.count("0.28.0") == 2  # header and provenance
    # two features drawing one set share one matrix row, named with both names
    ident = [o for o in f["overlaps"] if o["relation"] == "identical" and o.get("diagnostic")]
    shared = _b.render_shared(f)
    for o in ident:
        la, lb = _b.qualified_labels([o["a"], o["b"]]).values()
        assert f"| {la} = {lb} |" in shared or f"| {lb} = {la} |" in shared
        assert shared.count(f"| {la} |") == 0 and shared.count(f"| {lb} |") == 0
    # the tier table has no constant column; the excluded section is one line naming each ◌ feature with its count
    if f["top_tier"]["rooms"]:  # the small fixture has no tier; the header is tested on the synthetic sheet in the D-061 test
        assert "| room | lines | importers (from test files) | diagnostic features that mark it |" in page
    mm = _b.render_most_marked({"top_tier": {"sets": 2, "rooms": [{"room": "a", "lines": 3, "fan_in": 9, "test_fan_in": 4, "features": ["x", "y"]}]}})
    assert "| a | 3 | 9 (4) | x, y |" in mm and "| room | lines | importers (from test files) |" in mm
    dis = _b.render_disclosure(f)
    assert dis.count("\n") == 0 and all(f"◌ {x['feature']} {x['count']}" in dis for x in f["features"] if x["decorative"])
    # hub and lit_room name their position (maintainability 0.2.9)
    assert _row(reg, "hub").startswith("| high-centrality node (import graph) |") and _row(reg, "lit_room").startswith("| recently-touched room (clock) |")
    assert "no consequence word in the name (lexicon)" not in reg
