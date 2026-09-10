"""M3 — the architect brief (C5) with the register lint (`architect-brief-spec.md`, D-027).

Three parts, in the order the anti-horoscope contract wants them:

1. `facts(skeleton, substrate)` — the deterministic facts sheet: everything the brief may
   say, and nothing else. Diagnostic features with their rooms, decorative features by
   count only, the gate's per-signal statuses, position-name disclosures for names that
   imply a consequence, the stance disclosure. A pure function of the skeleton.
2. `generate(facts, ...)` — one call to a model under the condemnation-surveyor stance with
   the register rules in the system prompt. The only non-deterministic step; its
   provenance (model served, request id, facts hash) is written into the brief.
3. `lint(text, facts)` — the deterministic hostile reader. Consequence vocabulary,
   provenance of every citation, numbers, decorative exclusion, disclosure, no building
   label. A brief that fails is written marked FAILED and never passes silently.

The lint is the product; the generator is replaceable (`--draft` lints a hand-written
brief with no model in the path).
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

BRIEF_VERSION = "0.15.0"
MAX_ATTEMPTS_CAP = 3  # D-030: regeneration is bounded and every attempt's refusals are on the page
DEFAULT_MODEL = "claude-opus-5"

# ---------------------------------------------------------------- 1. the facts sheet

STANCE = (
    "The diagnosis presupposes a maintenance norm — that the positions it marks are worth a "
    "visit — which the reader may reject; it is stated as an ought, not a fact (system spec, "
    "stance disclosure)."
)


def facts(skeleton: dict[str, Any], substrate: dict[str, Any] | None = None) -> dict[str, Any]:
    """The facts sheet: the closed set of things the brief may say."""
    nodes = {n["id"]: n for n in (substrate or {}).get("nodes", [])}
    groups: list[tuple[str, list[dict[str, Any]]]] = [
        (skeleton["profile"]["name"], skeleton["features"])
    ]
    for od in skeleton.get("overlays") or []:
        groups.append((od["profile"], od["features"]))
    feats: dict[str, dict[str, Any]] = {}
    for profile, flist in groups:
        for f in flist:
            key = f"{profile}/{f['feature']}"
            entry = feats.setdefault(
                key,
                {
                    "profile": profile,
                    "feature": f["feature"],
                    "predicate": f["predicate"],
                    "diagnostic": bool(f["diagnostic"] and not f["decorative"]),
                    "decorative": bool(f["decorative"]),
                    "decorative_reason": f.get("decorative_reason"),
                    "validation_status": f.get("validation_status"),
                    "name_implies_consequence": bool(f.get("name_implies_consequence")),
                    "position_name": f.get("position_name"),
                    "caveat": f.get("caveat"),  # D-041: a ruleset's own warning about a predicate
                    "rooms": [],
                },
            )
            entry["rooms"].append(f["node"])
    depth = int((skeleton.get("geometry") or {}).get("wing_depth", 1))

    def wing_of(nid: str) -> str:
        parts = nid.split("/")
        return "/".join(parts[:depth]) if len(parts) > depth else "(root)"

    for e in feats.values():
        e["rooms"] = sorted(set(e["rooms"]))
        e["count"] = len(e["rooms"])
        # D-036: the share of a mark per wing is on the sheet, so the prose can state a count
        # per wing instead of an adverb ("mostly", "concentrated") the sheet cannot carry
        bw: dict[str, int] = {}
        for r in e["rooms"]:
            bw[wing_of(r)] = bw.get(wing_of(r), 0) + 1
        e["by_wing"] = dict(sorted(bw.items()))
        # D-037: the largest single directory in the set — the composition a two-room exemplar
        # list can hide (typeorm's dark_room is half src/error)
        bd: dict[str, int] = {}
        for r in e["rooms"]:
            d = r.rsplit("/", 1)[0] if "/" in r else "(root)"
            bd[d] = bd.get(d, 0) + 1
        top = max(bd.items(), key=lambda kv: (kv[1], kv[0])) if bd else ("(root)", 0)
        tied = (
            sum(1 for v in bd.values() if v == top[1]) > 1
        )  # D-040: a silent tie-break is a claim
        # D-038: the directory's population is the denominator the share needs — on a monorepo
        # one directory can be two thirds of the building, and a share without it is the base rate
        pop = sum(
            1
            for nid in skeleton["strata"]["by_node"]
            if (nid.rsplit("/", 1)[0] if "/" in nid else "(root)") == top[0]
        )
        # D-040: `dir` is the room's immediate parent (non-recursive), `population` the rooms whose
        # parent it is; `holds_third` is R15's bar — below it the register prints no directory
        e["dominant_dir"] = {
            "dir": top[0],
            "n": top[1],
            "population": pop,
            "tied": tied,
            "holds_third": bool(top[1] * DIRECTORY_SHARE >= len(e["rooms"])),
            # D-041: the size guard is its own field — a cell says the reason that is the reason
            "placeable": len(e["rooms"]) >= DIRECTORY_MIN_ROOMS,
        }
    wings: dict[str, int] = {}
    for nid in skeleton["strata"]["by_node"]:
        w = wing_of(nid)
        wings[w] = wings.get(w, 0) + 1
    # D-036: co-location across every profile (the base summary counts the base profile only)
    marks: dict[str, int] = {}
    for e in feats.values():
        if e["diagnostic"]:
            for r in e["rooms"]:
                marks[r] = marks.get(r, 0) + 1
    co_located_all = sum(1 for v in marks.values() if v >= 2)
    # D-036: two diagnostic features whose room sets coincide, or nest, are one set of rooms;
    # the sheet says so and R9 makes the prose say so
    overlaps: list[dict[str, Any]] = []
    # D-041: a set of fewer than three rooms is inside anything that contains it; no relation is drawn
    diag = [
        (k, set(e["rooms"]))
        for k, e in sorted(feats.items())
        if len(e["rooms"])
        >= RELATION_MIN_ROOMS  # D-044: decorative features too — the note promised every set
    ]
    for i, (ka, ra) in enumerate(diag):
        for kb, rb in diag[i + 1 :]:
            if ra == rb:
                # D-037: when two predicates draw one set, the conjuncts one has and the other
                # lacks did no work on this repository; the sheet names them so the prose cannot
                # read the identity as two measurements agreeing
                sa = set(feats[ka]["predicate"].replace("∧", "and").split(" and "))
                sb = set(feats[kb]["predicate"].replace("∧", "and").split(" and "))
                inert = sorted(t.strip() for t in (sa ^ sb))
                overlaps.append(
                    _flag(
                        feats,
                        {
                            "a": ka,
                            "b": kb,
                            "relation": "identical",
                            "n": len(ra),
                            "inert_terms": inert,
                            # D-038: the same predicate under two profiles is one measurement, not two agreeing
                            "shared_predicate": not inert,
                        },
                    )
                )
            elif ra < rb:
                overlaps.append(
                    _flag(
                        feats,
                        {
                            "a": ka,
                            "b": kb,
                            "relation": "within",
                            "n": len(ra),
                            "n_outside": len(rb - ra),
                        },
                    )
                )
            elif rb < ra:
                overlaps.append(
                    _flag(
                        feats,
                        {
                            "a": kb,
                            "b": ka,
                            "relation": "within",
                            "n": len(rb),
                            "n_outside": len(ra - rb),
                        },
                    )
                )
    # D-040/D-044: the diagnosis's counts come from diagnostic pairs only; a decorative pair is drawn
    # in the register (the note promises every set of three or more rooms) and counted nowhere
    diag_overlaps = [o for o in overlaps if o.get("diagnostic")]
    # D-040: how many distinct sets of rooms the diagnosis names — identical pairs are one set,
    # nestings stay two; and how many of the all-profile marks fall on identical pairs twice
    n_diag = sum(1 for e in feats.values() if e["diagnostic"] and e["rooms"])
    identical = [o for o in diag_overlaps if o["relation"] == "identical"]
    distinct_room_sets = n_diag - len(identical)
    # D-044: this number counts rooms an identical pair marks twice, not marks — it was named as marks
    rooms_marked_twice = sum(o["n"] for o in identical)
    relation_counts = {
        "identical": sum(1 for o in overlaps if o["relation"] == "identical"),
        "within": sum(1 for o in overlaps if o["relation"] == "within"),
        "total": len(overlaps),
    }
    # D-042: a number with two causes is two numbers — a gloss that names one cause is false of the other
    rooms_marked_twice_shared_predicate = sum(
        o["n"] for o in identical if o.get("shared_predicate")
    )
    rooms_marked_twice_inert_conjunct = sum(
        o["n"] for o in identical if not o.get("shared_predicate")
    )
    gate_fp = skeleton.get("substrate_config_fingerprint")
    if not gate_fp:
        raise ValueError(
            "skeleton carries no substrate_config_fingerprint; the brief cannot name its gate (D-036)"
        )
    s = skeleton["summary"]
    doc = {
        "brief_version": BRIEF_VERSION,
        "repo": {"name": skeleton["repo"]["name"], "head_sha": skeleton["repo"]["head_sha"]},
        "skeleton_hash": skeleton["skeleton_hash"],
        "profile": skeleton["profile"]["name"],
        "overlays": list(s.get("overlay_profiles") or []),
        "geometry": skeleton["geometry"]["name"],
        "population": s["population"],
        "wings": dict(sorted(wings.items())),
        "wing_count": len(wings),
        "gate": dict(sorted(skeleton["gate"]["signals"].items())),
        "diagnostic_count": sum(e["count"] for e in feats.values() if e["diagnostic"]),
        "diagnostic_count_base": s["diagnostic_count"],
        "decorative": {
            "count": s["decorative_count"],
            "features": sorted(s.get("decorative_features") or []),
        },
        "co_located_rooms": co_located_all,
        # D-046 addendum: the prose kept computing this to say "the N features name M sets"
        "diagnostic_features": n_diag,
        "distinct_room_sets": distinct_room_sets,
        "rooms_marked_twice": rooms_marked_twice,
        "rooms_marked_twice_shared_predicate": rooms_marked_twice_shared_predicate,
        "rooms_marked_twice_inert_conjunct": rooms_marked_twice_inert_conjunct,
        "relation_counts": relation_counts,
        # D-037: every building-level number carries its unit; a count of rooms is not a count of marks
        "units": {
            "population": "rooms",
            "wings": "rooms",
            "diagnostic_count": "marks",
            "diagnostic_count_base": "marks",
            "decorative.count": "marks",
            "co_located_rooms": "rooms carrying two or more diagnostic marks, across all profiles",
            "diagnostic_features": "diagnostic features that fired (features, not marks or rooms)",
            "distinct_room_sets": "sets of rooms the diagnostic features name, an identical pair counted once, a nesting twice",
            "rooms_marked_twice": "rooms an identical pair of diagnostic features marks twice (each such room carries two marks)",
            "rooms_marked_twice_shared_predicate": "of those, rooms where two profiles carry one predicate",
            "rooms_marked_twice_inert_conjunct": "of those, rooms where two predicates draw one set because a conjunct excludes nothing",
            "relation_counts": "relations the register draws, by kind, over every feature with enough rooms, decorative included",
            "dominant_dir": "the immediate parent directory (non-recursive) holding the most of a feature's rooms; shown only when it holds a third or more",
            "feature.count": "rooms (one mark per room)",
        },
        "overlaps": overlaps,
        "calibration": "in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page",
        "gate_fingerprint": gate_fp,
        "features": [feats[k] for k in sorted(feats)],
        "rooms": {
            nid: {
                "lines": nodes[nid]["metrics"]["size_loc"],
                "fan_in": nodes[nid]["metrics"].get("fan_in"),
                "fan_out": nodes[nid]["metrics"].get("fan_out"),
            }
            for nid in sorted(skeleton["strata"]["by_node"])
            if nid in nodes
        },
        "stance": STANCE,
    }
    raw = json.dumps(doc, sort_keys=True, ensure_ascii=False).encode("utf-8")
    doc["facts_hash"] = hashlib.sha256(raw).hexdigest()
    return doc


# ---------------------------------------------------------------- 3. the register lint

# Words that voice a consequence or a forecast. An `asserted` signal licenses a present
# structural position and nothing else (validation §2.1.1); these words cross the line.
CONSEQUENCE_WORDS = {
    "break",
    "breaks",
    "breaking",
    "broke",
    "broken",
    "will",
    "would",
    "shall",
    "risk",
    "risks",
    "risky",
    "fragile",
    "brittle",
    "dangerous",
    "danger",
    "blast",
    "ripple",
    "ripples",
    "cascade",
    "cascades",
    "cascading",
    "fail",
    "fails",
    "failure",
    "failing",
    "likely",
    "unlikely",
    "predict",
    "predicts",
    "prediction",
    "expect",
    "expected",
    "cause",
    "causes",
    "caused",
    "collapse",
    "collapses",
    "crumble",
    "vulnerable",
    "vulnerability",
    "exposed",
    "threat",
    "threatens",
    "prone",
    "future",
    "soon",
    "eventually",
    "inevitably",
    "bound",
    "doomed",
    "hazard",
    "hazardous",
    "impact",
    "impacts",
    "consequence",
    "consequences",
    "propagate",
    "propagates",
    "regress",
    "regression",
    "bug",
    "bugs",
    "defect",
    "defects",
    "unsafe",
    "safe",
    "critical",
}
# Consequence voiced as a relation between sets, without a listed word (Hume C1, D-028).
CONSEQUENCE_PHRASES = [
    r"\bagainst that\b",
    r"\boffsets?\b",
    r"\bcompensat\w*",
    r"\bmakes? up for\b",
    r"\bin exchange\b",
    r"\bcounterbalanc\w*",
    r"\bif [^.]{0,60}\b(changed|touched|removed|moved)\b",
]
# The disclosure clause is struck from a sentence before R1 reads it — the clause is not an
# amnesty for the rest of the sentence (Wittgenstein, D-028).
DISCLOSURE_CLAUSES = [
    r"not a claim about [^.;,]*",  # "what breaks", "damage", "condition" — the clause, not a phrase (D-037)
    r"(denotes|names|is) (a )?(position|location|place)[^.;,]*",
    r"a (position|location|place) in the import graph[^.;,]*",
    r"(position|location), not [^.;,]*",
]
# Whole-building labels (D-019: no archetype in v0).
BUILDING_LABELS = {
    "cathedral",
    "shantytown",
    "shanty",
    "bunker",
    "ruin",
    "ruins",
    "fortress",
    "palace",
    "slum",
    "temple",
    "monolith",
    "mansion",
    "hovel",
    "castle",
    "warehouse",
    "barn",
    "skyscraper",
    "tenement",
    "tower block",
    "labyrinth",
    "maze",
}
# [feature: a, b] · [feature ×N] · [feature ×N: a, b] · [f ×N; g ×M] · [f ×N, g ×M] — one bracket
# may chain several clauses; the count and the rooms of each are checked (D-032 addendum)
# "are not a diagnosis", "enter no part of this diagnosis", "nothing confirmed … diagnosis":
# the disclosure sentence negates diagnosis in its own words (R4).
NEGATED_DIAGNOSIS = re.compile(
    r"\b(?:not|no|nothing|never|neither|nor|without|outside|apart from|excluded from|excluding)\b"
    r"[^.;]{0,60}\bdiagnos"
)
# D-036: distributional words the sheet cannot carry (it carries counts per wing instead)
DISTRIBUTION = re.compile(
    r"\b(?:mostly|most of|largely|predominantly|mainly|chiefly|concentrated in|the bulk|"
    r"spread across|scattered|throughout|every wing|all wings|all of the wings|reaches into every|"
    r"accordingly|in proportion|proportionally|correspondingly|as one would expect|"
    r"near these|nearby|close to|adjacent|"
    r"and others|the others|the rest|the remainder|others under|others in)\b"
)
# D-037: comparatives and superlatives set one mark against another; the register forbids it
# D-041: two rooms as the ends of a span the page does not order
SPAN = re.compile(r"\bfrom\s+[\w./@-]+/[\w./@-]+\s+(?:through|to)\s+[\w./@-]+/[\w./@-]+")
COMPARISON = re.compile(
    r"\b(?:widest|largest|biggest|broadest|narrowest|smallest|fewest|greatest|"
    r"wider than|larger than|bigger than|smaller than|fewer than|more than any|the most \w+ set)\b"
)
# D-037: a number followed by its unit noun ("160 of those marks", "70 rooms")
UNIT_USE = re.compile(
    r"\b(\d{1,7}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+"
    r"(?:of\s+(?:those|these|the|its|the\s+\w+)\s+)?(rooms?|marks?|findings?|features?|relations?|nestings?|identical pairs?)\b",
    re.IGNORECASE,
)
# signal names a decorative_reason may cite (R4b)
_SIGNAL_LIKE = {
    "bug_pressure_index",
    "change_pressure_index",
    "blast_radius_index",
    "load_index",
    "neglect_index",
    "reinforcement_index",
    "complexity_proxy_index",
    "recent_commit_share",
    "centrality",
    "fan_in",
}
# D-045 addendum: an inference from what a predicate reads to what its rooms are
INFERENCE = re.compile(
    r"\b(?:and so|so not|therefore|thus|hence|which makes|making them|so they are)\b"
)
# D-043: a negated property whose noun is another feature's position
NEGATED_PROPERTY = re.compile(
    r"\b(?:not|never|no)\s+(?:an?\s+|the\s+)?(entrance|entry|entries|hub|hubs|root|roots|leaf|leaves|reinforced)\b"
)
PROPERTY_ALIASES = {
    "entrance": "package_entry",
    "entry": "package_entry",
    "entries": "package_entry",
    "hub": "hub",
    "hubs": "hub",
    "root": "import_root",
    "roots": "import_root",
    "leaf": "leaf_utility",
    "leaves": "leaf_utility",
    "reinforced": "scaffolding",
}
# D-046 addendum: likeness words claim a shared distribution only where a place is named —
# "marks sit there and in the smaller wings alike" is a claim, "corridor is likewise nested
# inside hub" is a connective between two relation statements
LIKENESS = re.compile(r"\b(?:alike|likewise|similarly|in the same way)\b")
# D-041: constructions that deny a relation
NO_RELATION = re.compile(
    r"\b(?:unshared|stands? apart|stand alone|no overlap|shares? no rooms|independent of|unrelated|overlaps? nothing)\b"
)
# D-038: nouns that make a nesting an identity
IDENTITY_NOUN = re.compile(
    r"\b(?:the same (?:\d+ )?rooms|one set of rooms|identical|one finding|coincide)\b"
)
# a directory-like token: two or more path segments, not ending in a file extension
DIRECTORY = re.compile(r"(?<![\w/@.-])([A-Za-z0-9_@.-]+(?:/[A-Za-z0-9_@.-]+)+)(?![\w/])")
BRACKET = re.compile(r"\[([a-z_][^\]]*)\]")
CLAUSE = re.compile(r"^([a-z_]+(?:/[a-z_]+)?)\s*(?:×\s*(\d+))?\s*(?::\s*(.+))?$")


def _citations(text: str):
    """Yield (feature, count, rooms) for every clause of every bracket in ``text``.

    Clauses chain on ``;``. A comma chains too, but only between bare counts
    (``[crack ×21, toothpick_wing ×3]``) — inside ``[hub: a.ts, b.ts]`` the comma
    separates rooms. A clause that does not parse is yielded by its raw text so
    it resolves to nothing and R2 refuses it.
    """
    for b in BRACKET.finditer(text):
        body = b.group(1)
        parts = [c.strip() for c in body.split(";")]
        if len(parts) == 1 and "," in body and ":" not in body:
            cs = [c.strip() for c in body.split(",")]
            if all((m := CLAUSE.match(c)) and m.group(2) for c in cs):
                parts = cs
        for c in parts:
            m = CLAUSE.match(c)
            if m:
                yield m.group(1), m.group(2), (m.group(3) or "").strip() or None
            else:
                yield c, None, None


INTEGER = re.compile(r"(?<![\w./-])(\d{1,7})(?![\w./%-])")
WORD_NUMBERS = {
    w: i
    for i, w in enumerate(
        "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
        "fifteen sixteen seventeen eighteen nineteen twenty".split()
    )
}
WORD_NUMBERS.update(
    {
        w: 10 * (i + 3)
        for i, w in enumerate("thirty forty fifty sixty seventy eighty ninety".split())
    }
)
_NUM_WORD = "|".join(sorted(list(WORD_NUMBERS) + ["hundred", "thousand"], key=len, reverse=True))
# "two hundred sixty-seven", "one hundred and thirty-three", "twenty-one": one span, one value.
# An ordinal ("seventy-fifth percentile") is a rank, not a count, and is left alone.
SPELLED_NUMBER = re.compile(
    rf"\b((?:(?:{_NUM_WORD})(?:[\s-]+(?:and[\s-]+)?(?=(?:{_NUM_WORD})\b))?)+)"
    r"\b(?!-?(?:first|second|third|fifth|[a-z]+th)\b)",
    re.IGNORECASE,
)


def _spelled_numbers(text: str):
    """Yield (span, value) for every number written in words."""
    for m in SPELLED_NUMBER.finditer(text):
        span = m.group(1).strip(" -")
        total = cur = 0
        for w in re.split(r"[\s-]+", span.lower()):
            if w in WORD_NUMBERS:
                cur += WORD_NUMBERS[w]
            elif w == "hundred":
                cur = (cur or 1) * 100
            elif w == "thousand":
                total += (cur or 1) * 1000
                cur = 0
        yield span, total + cur


# a sentence may begin with a lowercase feature name ("flooded_basement sits inside …"): the split
# accepts any letter, or a bracket or backtick, after the terminal (D-042 addendum — one merged
# "sentence" let an identity noun for one pair fire R13 on the nestings beside it)
SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Za-z_\[`])")


@dataclass
class Violation:
    rule: str
    paragraph: int
    text: str
    detail: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "rule": self.rule,
            "paragraph": self.paragraph,
            "text": self.text,
            "detail": self.detail,
        }


def _mentions(sentence: str, room: str) -> bool:
    """`src/index.ts` is not a mention of `packages/codemod/src/index.ts`: a room is named
    only as a whole path token."""
    return re.search(r"(?<![\w/.\-])" + re.escape(room) + r"(?![\w/.\-])", sentence) is not None


def _paragraphs(text: str) -> list[str]:
    body = text.split("\n## Provenance", 1)[0]
    return [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]


def lint(text: str, facts_doc: dict[str, Any], register: bool = False) -> list[Violation]:
    """The deterministic hostile reader. Returns the violations; empty means PASS."""
    out: list[Violation] = []
    by_feature = {f["feature"]: f for f in facts_doc["features"]}
    by_key = {f"{f['profile']}/{f['feature']}": f for f in facts_doc["features"]}
    allowed_numbers = set()
    allowed_numbers.add(facts_doc["population"])
    allowed_numbers.add(facts_doc["diagnostic_count"])
    allowed_numbers.add(facts_doc.get("diagnostic_count_base", facts_doc["diagnostic_count"]))
    allowed_numbers.add(facts_doc["decorative"]["count"])
    allowed_numbers.add(facts_doc["co_located_rooms"])
    allowed_numbers.update(facts_doc["wings"].values())
    allowed_numbers.add(facts_doc.get("wing_count", len(facts_doc["wings"])))
    # D-039 addendum: "the same predicate under two profiles" — the profile count is a sheet fact
    allowed_numbers.add(1 + len(facts_doc.get("overlays") or []))
    allowed_numbers.add(facts_doc.get("distinct_room_sets", 0))
    allowed_numbers.add(facts_doc.get("diagnostic_features", 0))
    allowed_numbers.add(len(facts_doc.get("overlaps") or []))  # "three relations" (D-040 addendum)
    allowed_numbers.add(facts_doc.get("rooms_marked_twice", 0))
    allowed_numbers.add(facts_doc.get("rooms_marked_twice_shared_predicate", 0))
    allowed_numbers.add(facts_doc.get("rooms_marked_twice_inert_conjunct", 0))
    allowed_numbers.update((facts_doc.get("relation_counts") or {}).values())
    # D-036 (hostile reading, run 17): a feature's numbers are admitted in the sentence that
    # cites the feature, not anywhere in the paragraph — "two sit outside src" passed because
    # 2 was some other feature's count
    feature_numbers: dict[str, set[int]] = {}
    for f in facts_doc["features"]:
        dd = f.get("dominant_dir") or {}
        nums = {
            f["count"],
            *f.get("by_wing", {}).values(),
            dd.get("n", f["count"]),
            dd.get("population", f["count"]),
        }
        feature_numbers[f["feature"]] = nums
        feature_numbers[f"{f['profile']}/{f['feature']}"] = nums
    wing_names = set(facts_doc["wings"])
    # R18 (D-045): families of marks the sheet does not define, built from its own profile and record names
    _families = [
        facts_doc["profile"],
        *(facts_doc.get("overlays") or []),
        *[n for n, _ in _RECORDS],
        "graph",
        "age",
        "import-graph",
        "load",
        "recency",
    ]
    family_words = re.compile(
        r"\b(?:the\s+)?(?:"
        + "|".join(re.escape(x) for x in _families)
        + r")\s+(?:marks|features|positions|set|sets)\b"
    )
    largest_wing = (
        max(facts_doc["wings"], key=lambda w: (facts_doc["wings"][w], w))
        if facts_doc["wings"]
        else None
    )
    # D-037: unit classes for R12 — feature counts are both (one mark per room)
    rooms_only = {facts_doc["population"], facts_doc["co_located_rooms"]} | set(
        facts_doc["wings"].values()
    )
    marks_only = {
        facts_doc["diagnostic_count"],
        facts_doc.get("diagnostic_count_base", 0),
        facts_doc["decorative"]["count"],
    }
    both = {f["count"] for f in facts_doc["features"]} | {
        v for f in facts_doc["features"] for v in f.get("by_wing", {}).values()
    }
    rooms_ok = both | rooms_only
    marks_ok = both | marks_only
    any_validated = any(v == "validated" for v in (facts_doc.get("gate") or {}).values())
    room_metrics = facts_doc.get("rooms", {})
    used_consequence_names: set[str] = set()
    first_use: dict[str, tuple[int, str]] = {}  # feature → (paragraph, paragraph text)
    room_ids = sorted(
        {r for f in facts_doc["features"] for r in f["rooms"]} | set(facts_doc.get("rooms", {})),
        key=len,
        reverse=True,
    )
    stance_key = facts_doc["stance"][:40].lower()
    for i, para in enumerate(_paragraphs(text), 1):
        if para.startswith(("#", "*Register lint")):
            continue
        low_para = para.lower()
        # the stance paragraph is the stance sentence, not any paragraph that quotes a phrase of it
        bare = BRACKET.sub("", low_para).strip()
        is_stance = bare.startswith(stance_key)
        is_disclosure = "decorative" in low_para and (
            "not a diagnosis" in low_para or "no diagnosis" in low_para
        )
        for f0 in facts_doc["features"]:
            if (
                f0["name_implies_consequence"]
                and f0["feature"] not in first_use
                and re.search(rf"\b{re.escape(f0['feature'])}\b", low_para)
            ):
                first_use[f0["feature"]] = (i, low_para)
        # R1 consequence vocabulary, per sentence. Bracket interiors are names, not claims,
        # and are stripped first; the disclosure clause is struck, not used as an amnesty.
        for sent in SENTENCE.split(para):
            bare_sent = BRACKET.sub("", sent)
            scan = BRACKET.sub("", sent).lower()
            for clause in DISCLOSURE_CLAUSES:
                scan = re.sub(clause, " ", scan)
            hits = sorted(w for w in CONSEQUENCE_WORDS if re.search(rf"\b{re.escape(w)}\b", scan))
            hits += [m.group(0) for pat in CONSEQUENCE_PHRASES for m in re.finditer(pat, scan)]
            if hits:
                out.append(
                    Violation(
                        "R1-consequence",
                        i,
                        sent[:160],
                        f"consequence/forecast vocabulary: {', '.join(hits)}",
                    )
                )
            # R6 building label
            labels = sorted(w for w in BUILDING_LABELS if re.search(rf"\b{re.escape(w)}\b", scan))
            if labels:
                out.append(
                    Violation(
                        "R6-archetype",
                        i,
                        sent[:160],
                        f"whole-building label: {', '.join(labels)} (D-019)",
                    )
                )
            # R2b (D-043, narrowed D-046): a citation warrants something in its sentence — the
            # feature named in prose, one of its rooms, or one of its numbers — or it is decoration.
            # Two forms warrant it otherwise: the decorative disclosure, whose whole discipline is to
            # cite by count and name no room (R4/R7), and a sentence continuing about a feature the
            # sentence before it named, where the subject is a pronoun.
            prev_sent = (
                SENTENCE.split(para)[max(0, SENTENCE.split(para).index(sent) - 1)]
                if sent in SENTENCE.split(para)
                else ""
            )
            dec_disclosure = bool(
                re.search(rf"\b{facts_doc['decorative']['count']}\b", bare_sent)
                and NEGATED_DIAGNOSIS.search(bare_sent.lower())
            )
            for cname, ccount, crooms in _citations(sent):
                cf = by_key.get(cname) or by_feature.get(cname)
                if not cf:
                    continue
                if dec_disclosure and cf["decorative"]:
                    continue
                named_in_prose = (
                    re.search(rf"\b{re.escape(cf['feature'])}\b", bare_sent) is not None
                )
                room_named = any(_mentions(bare_sent, r) for r in cf["rooms"])
                nums = {cf["count"], *cf.get("by_wing", {}).values()}
                number_used = any(re.search(rf"\b{n}\b", bare_sent) for n in nums)
                anaphora = bool(
                    prev_sent
                    and re.search(rf"\b{re.escape(cf['feature'])}\b", BRACKET.sub("", prev_sent))
                    and re.match(
                        r"\s*(?:it|its|it's|they|their|this|that|these|those)\b", bare_sent.lower()
                    )
                )
                if not (named_in_prose or room_named or number_used or anaphora):
                    out.append(
                        Violation(
                            "R2-provenance",
                            i,
                            sent[:160],
                            f"[{cname}] warrants nothing in this sentence: the feature, a room of it or its count must appear",
                        )
                    )
            # R8 attribution: a room named in a sentence is covered by a feature cited in it
            named = [rid for rid in room_ids if _mentions(sent, rid)]
            covered: set[str] = set()
            for cname, _c, _r in _citations(sent):
                cf = by_key.get(cname) or by_feature.get(cname)
                if cf:
                    covered.update(cf["rooms"])
            # R10 (D-036): a directory named in a sentence contains a room cited in it — R8 covered
            # rooms, and a distribution over four directories was asserted on the warrant of two
            for d in sorted(set(DIRECTORY.findall(BRACKET.sub("", sent)))):
                if d in room_ids or d in wing_names:
                    continue
                if not any(r.startswith(d + "/") for r in room_ids):
                    continue  # not a directory of this building; R2/R8 territory if it is a room
                if not any(r.startswith(d + "/") for r in covered):
                    out.append(
                        Violation(
                            "R10-prefix",
                            i,
                            sent[:160],
                            f"names the directory {d} but no room cited in the sentence sits in it",
                        )
                    )
            # R11 (D-036): a share is a number on the sheet (by_wing), not an adverb
            low_sent = bare_sent.lower().replace("across all profiles", "")
            for m in DISTRIBUTION.finditer(low_sent):
                out.append(
                    Violation(
                        "R11-share",
                        i,
                        sent[:160],
                        f"'{m.group(0)}' asserts a share the sheet does not carry; state the count per wing (by_wing)",
                    )
                )
            for m in SPAN.finditer(BRACKET.sub("", sent)):
                out.append(
                    Violation(
                        "R11-share",
                        i,
                        sent[:160],
                        f"'{m.group(0)[:60]}' presents two rooms as the ends of a span the page does not order (D-041)",
                    )
                )
            # D-046: R11 compares marks; a sentence that names no feature is comparing wings
            names_a_feature = any(
                re.search(rf"\b{re.escape(x['feature'])}\b", bare_sent)
                for x in facts_doc["features"]
            ) or any((by_key.get(c) or by_feature.get(c)) for c, _n, _r in _citations(sent))
            place_named = any(
                re.search(rf"(?<![\w/@.-]){re.escape(w)}(?![\w/])", bare_sent) for w in wing_names
            ) or any(
                (x.get("dominant_dir") or {}).get("dir")
                and re.search(
                    rf"(?<![\w/@.-]){re.escape(x['dominant_dir']['dir'])}(?![\w])", bare_sent
                )
                for x in facts_doc["features"]
            )
            if place_named:
                for m in LIKENESS.finditer(low_sent):
                    out.append(
                        Violation(
                            "R11-share",
                            i,
                            sent[:160],
                            f"'{m.group(0)}' claims a shared distribution the sheet does not carry; state the counts per wing",
                        )
                    )
            for m in COMPARISON.finditer(low_sent if names_a_feature else ""):
                out.append(
                    Violation(
                        "R11-share",
                        i,
                        sent[:160],
                        f"'{m.group(0)}' sets one mark against another; a p90 set has its size by construction (D-037)",
                    )
                )
            # R12 (D-037): a number wears its unit — a count of rooms is not "N marks"
            for m in UNIT_USE.finditer(BRACKET.sub("", sent)):
                raw = m.group(1).lower()
                n = int(raw) if raw.isdigit() else WORD_NUMBERS.get(raw, -1)
                unit = m.group(2).lower().rstrip("s")
                if unit == "finding":
                    # D-038: "one finding, two marks" counts features — a unit the sheet does not carry
                    out.append(
                        Violation(
                            "R12-unit", i, sent[:160], "'findings' is not a unit on the facts sheet"
                        )
                    )
                    continue
                if unit == "feature":
                    continue  # a count of feature names; the names themselves are checked
                if unit in ("relation", "nesting", "identical pair"):
                    # D-044: a count of relations is a sheet number by kind, not a coincidence
                    rc = facts_doc.get("relation_counts") or {}
                    want = {
                        "relation": rc.get("total"),
                        "nesting": rc.get("within"),
                        "identical pair": rc.get("identical"),
                    }[unit]
                    if want is not None and n != want:
                        out.append(
                            Violation(
                                "R12-unit", i, sent[:160], f"{n} {unit}s: the register draws {want}"
                            )
                        )
                    continue
                if unit == "mark" and n <= 3 and n <= len(facts_doc["features"]):
                    continue  # "two marks on one set": a count of features wearing the word (D-038 addendum)
                if unit == "mark" and n in rooms_only and n not in marks_ok:
                    out.append(
                        Violation(
                            "R12-unit",
                            i,
                            sent[:160],
                            f"{n} counts rooms on the facts sheet, not marks",
                        )
                    )
                if unit == "room" and n in marks_only and n not in rooms_ok:
                    out.append(
                        Violation(
                            "R12-unit",
                            i,
                            sent[:160],
                            f"{n} counts marks on the facts sheet, not rooms",
                        )
                    )
            # R12 (D-040): a ratio across units — "N rooms … out of M marks"
            if re.search(
                r"\b\d+\s+rooms?\b[^.;]{0,60}\bout of\s+\d+\s+(?:diagnostic\s+)?marks?\b", low_sent
            ) or re.search(r"\b\d+\s+marks?\b[^.;]{0,60}\bout of\s+\d+\s+rooms?\b", low_sent):
                out.append(
                    Violation(
                        "R12-unit",
                        i,
                        sent[:160],
                        "a count of rooms is not a share of marks, nor marks of rooms",
                    )
                )
            # R17 (D-041): a prose claim of no relation is checked against the overlaps list —
            # the first sentence false against the sheet (fifth seating) said a nested feature stood apart
            if NO_RELATION.search(low_sent):
                related = {
                    x
                    for ov in facts_doc.get("overlaps") or []
                    for x in (ov["a"].split("/")[-1], ov["b"].split("/")[-1])
                }
                for name in related:
                    if re.search(rf"\b{re.escape(name)}\b", sent):
                        out.append(
                            Violation(
                                "R17-relation",
                                i,
                                sent[:160],
                                f"{name} is said to stand apart but the sheet lists it in a relation",
                            )
                        )
            # R17b (D-043): "not an entrance" said of rooms some of which another feature marks as
            # entries — the caveat paraphrased into a property of rooms (seventh seating)
            for m in NEGATED_PROPERTY.finditer(low_sent):
                target = PROPERTY_ALIASES.get(m.group(1))
                tf = by_feature.get(target) if target else None
                if not tf:
                    continue
                # D-045 addendum: a caveat is a limit on the predicate (D-042) and the page prints it,
                # so a sentence that quotes it and draws no inference to the rooms is the caveat
                # speaking, not a claim about rooms. The seventh seating's sentence inferred ("reading
                # no fan-in and so not an entrance"); these do not.
                quoted = any(
                    (cf or {}).get("caveat")
                    and sum(
                        1
                        for w in {t for t in re.findall(r"[a-z_]{4,}", cf["caveat"].lower())}
                        if re.search(rf"\b{re.escape(w)}\b", low_sent)
                    )
                    >= 3
                    for cf in (by_key.get(c) or by_feature.get(c) for c, _n, _r in _citations(sent))
                )
                if quoted and not INFERENCE.search(low_sent):
                    continue
                for cname, _c, _r in _citations(sent):
                    cf = by_key.get(cname) or by_feature.get(cname)
                    if cf and cf is not tf and set(cf["rooms"]) & set(tf["rooms"]):
                        out.append(
                            Violation(
                                "R17-relation",
                                i,
                                sent[:160],
                                f"'{m.group(0)}' is said of {cf['feature']} rooms, {len(set(cf['rooms']) & set(tf['rooms']))} of which {target} marks",
                            )
                        )
                        break
            # R18 (D-045): a family of marks no field defines — "the graph marks", "the onboarding
            # marks", "the age marks" — is refused; the reading names features, the register names
            # profiles and records. Built from the sheet's profile names and the record names.
            for m in family_words.finditer(low_sent):
                word = m.group(0).lower().replace("the ", "").split()[0]
                record = {
                    "graph": "import graph",
                    "import-graph": "import graph",
                    "age": "clock",
                    "recency": "clock",
                    "load": "import graph",
                    "test": "test graph",
                    "edit": "edit record",
                    "size": "size",
                }.get(word)
                cited_here = [
                    c
                    for c in (by_key.get(x) or by_feature.get(x) for x, _n, _r in _citations(sent))
                    if c
                ]
                # D-046 addendum: the family is defined when every feature the sentence cites reads
                # that record (record_of) or carries that profile — the sheet defines it after all
                if cited_here and all(
                    (record and record in record_of(c["predicate"])) or c["profile"] == word
                    for c in cited_here
                ):
                    continue
                out.append(
                    Violation(
                        "R18-family",
                        i,
                        sent[:160],
                        f"'{m.group(0)}' groups features into a family the sheet does not define; name the features",
                    )
                )
            # R14 (D-037): "validated" names a status no signal holds in this gate
            if not any_validated and re.search(r"\bvalidated\b", low_sent):
                out.append(
                    Violation(
                        "R14-status",
                        i,
                        sent[:160],
                        "'validated' names a status no signal in this gate holds; every feature here rests on an asserted signal",
                    )
                )
            if named:
                for rid in named:
                    if rid not in covered:
                        out.append(
                            Violation(
                                "R8-attribution",
                                i,
                                sent[:160],
                                f"names {rid} but no feature cited in the sentence fired on it",
                            )
                        )
        # R2 provenance: citations resolve; every paragraph carries at least one
        cites = list(_citations(para))
        decorative_only = bool(cites) and all(
            (by_key.get(n) or by_feature.get(n) or {}).get("decorative") and c and not r
            for n, c, r in cites
        )
        if not cites and not is_stance and not (is_disclosure and decorative_only):
            out.append(
                Violation(
                    "R2-provenance",
                    i,
                    para[:160],
                    "paragraph carries no [feature: room] or [feature ×N] citation",
                )
            )
        for name, count, room in cites:
            if not count and not room:
                out.append(
                    Violation(
                        "R2-provenance", i, para[:160], f"[{name}] cites neither a room nor a count"
                    )
                )
                continue
            f = by_key.get(name) or by_feature.get(name)
            if f is None:
                out.append(
                    Violation(
                        "R2-provenance",
                        i,
                        para[:160],
                        f"citation names a feature not in the skeleton: {name}",
                    )
                )
                continue
            if f["decorative"] and room:
                out.append(
                    Violation(
                        "R4-decorative",
                        i,
                        para[:160],
                        f"a decorative feature is cited by count only; [{name}: …] singles out rooms it may not",
                    )
                )
            # A decorative feature is disclosed, not diagnosed, when the sentence that cites it
            # cites decorative features by count only and names no room — the wording is the
            # register's, the rule is the citation's (D-032 addendum; before, a phrase match).
            cite_sentences = [
                sent
                for sent in SENTENCE.split(para)
                if any(n == name for n, _c, _r in _citations(sent))
            ]
            disclosed_here = any(
                all(
                    (by_key.get(n) or by_feature.get(n) or {}).get("decorative") and c and not r
                    for n, c, r in _citations(sent)
                )
                and not any(_mentions(sent, rid) for rid in room_ids)
                and NEGATED_DIAGNOSIS.search(sent.lower())
                for sent in cite_sentences
            )
            if f["decorative"] and not disclosed_here:
                out.append(
                    Violation(
                        "R4-decorative",
                        i,
                        para[:160],
                        f"diagnostic claim cites a decorative feature: {name} (excluded from diagnosis, mapper §3)",
                    )
                )
            if room:
                for r in [x.strip() for x in room.split(",")]:
                    if r not in f["rooms"]:
                        out.append(
                            Violation("R2-provenance", i, para[:160], f"{name} did not fire on {r}")
                        )
            if count and int(count) != f["count"]:
                out.append(
                    Violation(
                        "R2-provenance",
                        i,
                        para[:160],
                        f"{name} ×{count}: the skeleton counts {f['count']}",
                    )
                )
            if f["name_implies_consequence"]:
                used_consequence_names.add(f["feature"])
        # R3 numbers — digits and number words alike; a room's own metrics are admitted only
        # in a paragraph that names the room (D-030: otherwise any small integer passes)
        for sent in SENTENCE.split(para):
            stripped = BRACKET.sub("", sent)
            sent_allowed = set(allowed_numbers)
            for cname, _c, _r in _citations(sent):
                sent_allowed |= feature_numbers.get(cname, set())
            # D-038 addendum: the numbers of an overlap belong to the sentence that names its pair
            pair_numbers: set[int] = set()
            for ov in facts_doc.get("overlaps") or []:
                oa, ob = ov["a"].split("/")[-1], ov["b"].split("/")[-1]
                if re.search(rf"\b{re.escape(oa)}\b", sent) and re.search(
                    rf"\b{re.escape(ob)}\b", sent
                ):
                    pair_numbers |= {ov["n"], ov.get("n_outside", ov["n"])}
            sent_allowed |= pair_numbers
            if register:
                # R16 (D-040, rebuilt D-041): the register's by-wing and directory numbers are sayable
                # only in a sentence that names the wing or directory they belong to — a binding, not a
                # refusal, so the deflating number is always sayable and the bare restatement is not
                cited = [by_key.get(c) or by_feature.get(c) for c, _n, _r in _citations(sent)]
                bare = BRACKET.sub("", sent)
                # the entitlement is the union over every cited feature — a number one cited
                # feature owns is not refused because another cited feature also carries it
                entitled = set(allowed_numbers) | pair_numbers
                for cf in cited:
                    if not cf:
                        continue
                    entitled.add(cf["count"])
                    for w, v in cf.get("by_wing", {}).items():
                        wing_named = (
                            re.search(rf"(?<![\w/@.-]){re.escape(w)}(?![\w/])", bare) is not None
                        )
                        if not wing_named:
                            continue
                        # D-045: a wing that holds all of a feature's rooms is that feature's register
                        # row, whether or not the number is in the prose — the citation carries it
                        # (S2: "import_root fires in the cookbook servers [×17]"); a feature of one or
                        # two rooms has no share to restate, its place is its room's name
                        if v == cf["count"] and cf["count"] >= RELATION_MIN_ROOMS:
                            out.append(
                                Violation(
                                    "R16-restatement",
                                    i,
                                    sent[:160],
                                    f"{cf['feature']}'s rooms all sit in {w}: that is its register row, not a reading — name its rooms or say nothing of the wing",
                                )
                            )
                            continue
                        # D-042: naming the largest wing costs nothing on a one-wing building, so its
                        # count stays the register's; a minority wing's count is the reading's to say
                        if w != largest_wing:
                            entitled.add(v)
                            # D-045: a located subset carries its total — "7 of the 42", never "7 in src"
                            if (
                                v < cf["count"]
                                and re.search(rf"\b{v}\b", bare)
                                and not re.search(rf"\b{cf['count']}\b", bare)
                            ):
                                out.append(
                                    Violation(
                                        "R16-restatement",
                                        i,
                                        sent[:160],
                                        f"{v} of {cf['feature']}'s rooms are placed in {w} without the {cf['count']} they are part of; say the total in the sentence",
                                    )
                                )
                    dd = cf.get("dominant_dir") or {}
                    if dd and re.search(rf"(?<![\w/@.-]){re.escape(dd['dir'])}(?![\w])", bare):
                        # D-046 addendum: a parent directory that shares a wing's name is sayable, but
                        # only as the parent — "the tools directory", "as parent", "not the wing" — since
                        # the wing and the directory hold different numbers of the feature's rooms
                        ambiguous = dd["dir"] in wing_names
                        marked = (
                            re.search(r"\bdirector(?:y|ies)\b|as parent|not the wing", bare)
                            is not None
                        )
                        if ambiguous and not marked:
                            if re.search(rf"\b{dd.get('n')}\b", bare) and dd.get("n") != cf.get(
                                "by_wing", {}
                            ).get(dd["dir"]):
                                out.append(
                                    Violation(
                                        "R16-restatement",
                                        i,
                                        sent[:160],
                                        f"{dd['dir']} names both a wing ({cf.get('by_wing', {}).get(dd['dir'])} of {cf['feature']}'s rooms) and their parent directory ({dd.get('n')}); say 'the {dd['dir']} directory' or name the wing's count",
                                    )
                                )
                        else:
                            entitled |= {dd.get("n"), dd.get("population")}
                            # D-045: a directory share carries its denominator in the same sentence, and
                            # a directory the register suppressed is named with both numbers or not at all
                            has_n = re.search(rf"\b{dd.get('n')}\b", bare) is not None
                            has_pop = re.search(rf"\b{dd.get('population')}\b", bare) is not None
                            if has_n != has_pop or (
                                not dd.get("holds_third") and not (has_n and has_pop)
                            ):
                                out.append(
                                    Violation(
                                        "R15-composition",
                                        i,
                                        sent[:160],
                                        f"{dd['dir']} is named for {cf['feature']} without both its share ({dd.get('n')}) and its rooms ({dd.get('population')}) in the sentence; a share carries its denominator",
                                    )
                                )
                for cf in cited:
                    if not cf:
                        continue
                    dd = cf.get("dominant_dir") or {}
                    for v in set(cf.get("by_wing", {}).values()) | {
                        dd.get("n"),
                        dd.get("population"),
                    }:
                        if v is None or v in entitled:
                            continue
                        sent_allowed.discard(v)
                        if re.search(rf"\b{v}\b", bare):
                            out.append(
                                Violation(
                                    "R16-restatement",
                                    i,
                                    sent[:160],
                                    (
                                        f"{v} is {cf['feature']}'s count in the largest wing ({largest_wing}), which is the register's; say a minority wing's count or leave it"
                                        if v == cf.get("by_wing", {}).get(largest_wing)
                                        else (
                                            f"{v} is {cf['feature']}'s count in a wing or directory this "
                                            f"sentence does not name (its wing counts are {cf.get('by_wing')}); "
                                            "name the place that holds it or leave the number to the register"
                                        )
                                    ),
                                )
                            )
            for rid in room_ids:
                if rid in room_metrics and _mentions(sent, rid):
                    sent_allowed.update(v for v in room_metrics[rid].values() if isinstance(v, int))
            for n in INTEGER.findall(stripped):
                if int(n) not in sent_allowed:
                    out.append(
                        Violation(
                            "R3-number",
                            i,
                            sent[:160],
                            f"number {n} is not in the facts sheet, or its feature is not cited in this sentence",
                        )
                    )
            for span, val in _spelled_numbers(stripped):
                if span.lower() == "one":
                    continue  # the determiner, not a measurement (D-032 addendum)
                if re.search(rf"\b{re.escape(span)}\s+or\s+more\b", stripped, re.IGNORECASE):
                    continue  # "two or more" is the sheet's own unit phrase for co_located_rooms (D-037)
                if val not in sent_allowed:
                    out.append(
                        Violation(
                            "R3-number",
                            i,
                            sent[:160],
                            f"number '{span}' ({val}) is not in the facts sheet, or its feature is not cited in this sentence",
                        )
                    )
    # R9 (D-036): two diagnostic features whose room sets coincide or nest are one set of rooms;
    # some sentence must name both features together (the sheet's `overlaps` says which)
    sentences_all = [snt for p in _paragraphs(text) for snt in SENTENCE.split(p)]
    for ov in facts_doc.get("overlaps") or []:
        if not ov.get("diagnostic", True):
            continue  # D-044: a decorative pair is the register's; prose never diagnoses it (R4)
        # D-039: with the register on the page the obligation to name the pair is met there; the
        # refusals (an identity noun on a nesting, two profiles read as agreeing) still bind the prose
        fa, fb = ov["a"].split("/")[-1], ov["b"].split("/")[-1]
        together = any(
            re.search(rf"\b{re.escape(fa)}\b", snt) and re.search(rf"\b{re.escape(fb)}\b", snt)
            for snt in sentences_all
        )
        if not together and not register:
            out.append(
                Violation(
                    "R9-overlap",
                    0,
                    "",
                    f"{ov['a']} and {ov['b']} mark {'the same' if ov['relation'] == 'identical' else 'nested'} rooms ({ov['n']}); no sentence names both",
                )
            )
        # R13 (D-037): an identity between predicates that differ is a conjunct that did no work,
        # and the sentence that names the pair says which
        pair_sents = [
            snt
            for snt in sentences_all
            if re.search(rf"\b{re.escape(fa)}\b", snt) and re.search(rf"\b{re.escape(fb)}\b", snt)
        ]
        if together and ov["relation"] == "within":
            # D-038: a nesting is not an identity — the sentence names the rooms outside and no identity noun
            n_out = ov.get("n_outside")
            asserts_identity = any(
                m
                for snt in pair_sents
                for m in IDENTITY_NOUN.finditer(snt.lower())
                # D-046 addendum: "two sets of rooms, not one finding" denies the identity
                if not re.search(
                    r"\b(?:not|never|rather than|instead of)\b[^.;]{0,20}$",
                    snt.lower()[: m.start()],
                )
            )
            if asserts_identity or not any(
                n_out is not None and re.search(rf"\b{n_out}\b", BRACKET.sub("", snt))
                for snt in pair_sents
            ):
                out.append(
                    Violation(
                        "R13-inert",
                        0,
                        "",
                        f"{ov['a']} sits within {ov['b']}: the sentence naming both states the {n_out} rooms outside and does not call them one set",
                    )
                )
        if together and ov["relation"] == "identical" and ov.get("shared_predicate"):
            # D-038: the same predicate under two profiles is one measurement; the sentence says so
            if not register and not any(
                re.search(r"\bpredicate\b", snt.lower()) for snt in pair_sents
            ):
                out.append(
                    Violation(
                        "R13-inert",
                        0,
                        "",
                        f"{ov['a']} and {ov['b']} carry the same predicate: the sentence naming both must say so, not read them as two measurements agreeing",
                    )
                )
        inert = ov.get("inert_terms") or []
        if together and ov["relation"] == "identical" and inert:
            sigs = sorted({re.split(r"\s*(?:>=|<=|==|>|<)\s*", t)[0].strip() for t in inert})
            said = any(
                re.search(rf"\b{re.escape(fa)}\b", snt)
                and re.search(rf"\b{re.escape(fb)}\b", snt)
                and all(re.search(rf"\b{re.escape(sig)}\b", snt) for sig in sigs)
                for snt in sentences_all
            )
            if not said and not register:
                out.append(
                    Violation(
                        "R13-inert",
                        0,
                        "",
                        f"{ov['a']} and {ov['b']} draw one set; the sentence naming both must say that {', '.join(sigs)} excludes nothing here",
                    )
                )
    # R15 (D-037): a feature whose rooms sit one third or more in one directory names that directory
    # in a sentence that cites the feature — and R10 then requires a cited room inside it, so the
    # exemplars cannot be drawn away from the set's composition
    for f in facts_doc["features"]:
        dd = f.get("dominant_dir") or {}
        if register or not f["diagnostic"] or not dd or f["count"] < 6 or dd["n"] * 3 < f["count"]:
            continue
        key, name = f"{f['profile']}/{f['feature']}", f["feature"]
        pop = dd.get("population")
        named_dir = any(
            any(c in (key, name) for c, _n, _r in _citations(snt))
            and re.search(rf"(?<![\w/@.-]){re.escape(dd['dir'])}(?![\w])", snt)
            and (pop is None or re.search(rf"\b{pop}\b", BRACKET.sub("", snt)))
            for snt in sentences_all
        )
        if not named_dir:
            out.append(
                Violation(
                    "R15-composition",
                    0,
                    "",
                    f"{key}: {dd['n']} of its {f['count']} rooms sit in {dd['dir']}, which holds {pop} rooms; no sentence citing it names that directory with its population (D-038: a share carries its denominator)",
                )
            )
    # R4b (D-038): the decorative disclosure says why — the ungrounded signal from decorative_reason
    for f in facts_doc["features"]:
        if register or not f["decorative"]:
            continue
        reason = f.get("decorative_reason") or ""
        sigs = [w for w in re.findall(r"[a-z_]+", reason) if w in _SIGNAL_LIKE]
        if not sigs:
            continue
        key, name = f"{f['profile']}/{f['feature']}", f["feature"]
        cited = [
            snt for snt in sentences_all if any(c in (key, name) for c, _n, _r in _citations(snt))
        ]
        if cited and not any(
            re.search(rf"\b{re.escape(sig)}\b", snt) for snt in cited for sig in sigs
        ):
            out.append(
                Violation(
                    "R4-decorative",
                    0,
                    "",
                    f"{key} is decorative because {reason}; no sentence citing it names {', '.join(sigs)}",
                )
            )
    # R5 disclosure: a consequence-implying name carries its position name in the paragraph
    # where it is first used (a disclosure in paragraph 1 does not license paragraph 9)
    low_all = text.lower()
    used_consequence_names |= set(first_use)
    for feat in sorted(used_consequence_names):
        pos = (by_feature[feat].get("position_name") or "").lower()
        # tolerate plurals and hyphen/space variation: "high-load hub" ~ "high load hubs"
        words = [re.escape(w) for w in re.split(r"[\s-]+", pos) if w]
        pattern = r"[\s-]+".join(w + r"(?:s|es)?" for w in words) if words else None
        where = first_use.get(feat, (0, low_all))
        if pattern and not re.search(pattern, where[1]):
            out.append(
                Violation(
                    "R5-disclosure",
                    where[0],
                    feat,
                    f"'{feat}' is first used here without its position name ('{pos}') in the same paragraph (D-004 Q3)",
                )
            )
    # R7 decorative count must be stated when there are decorative features — met by the register
    # when the page carries one (D-039)
    dec_count = facts_doc["decorative"]["count"]
    prose_only = BRACKET.sub("", text)
    in_prose = {int(d) for d in INTEGER.findall(prose_only)} | {
        v for _, v in _spelled_numbers(prose_only)
    }
    stated = dec_count in in_prose
    diag = facts_doc["diagnostic_count"]
    if not register and diag not in in_prose:
        out.append(
            Violation(
                "R7-counts",
                0,
                "",
                f"the brief must state the diagnostic-mark count ({diag}, all profiles) beside the population",
            )
        )
    if not register and dec_count and not stated:
        out.append(
            Violation(
                "R7-decorative-count",
                0,
                "",
                f"the brief must state the decorative count ({facts_doc['decorative']['count']}) where a reader sees it (mapper §3)",
            )
        )
    return out


# ---------------------------------------------------------------- 2. the generator

SYSTEM = """You are a condemnation surveyor writing the architect's brief for a building that is a codebase. The building is drawn from a skeleton of named structural features; you have the facts sheet and nothing else. You describe what is; you do not sell, soften, or forecast. The page you are writing for already carries a register: a table rendered from the facts sheet by code with one row per feature — position name, room count, counts per wing, dominant directory with its population, relations to other features (identical, within, with the rooms outside and the conjunct that did no work), and the reason a decorative feature is excluded. Do not restate the register: a feature's count in a wing or directory is sayable only in a sentence that names that wing or directory (R16) — say "8 of the 11 import_root rooms sit in scripts", never a bare "11" for a wing that holds 8. The building's largest wing is the exception: its count for any feature is the register's and is never sayable in the reading ("147 of the 164 sit in src" is refused when src is the largest wing) — say the minority wings' counts or say nothing. Never say a feature stands apart or shares no rooms unless the register's relation cell for it is "none" (R17). Never write "from room A to room B", "near", "alike", "similarly": rooms are not ordered and the page carries no distance. A caveat is a limit on what a predicate reads; never restate it as a property of rooms ("not an entrance"). Every bracket you write must warrant something in its own sentence — the feature's name, one of its rooms, or its count. Never say a wing holds "all" of a feature's rooms — that is its register row. Never name a wing that holds all of a feature's rooms beside that feature at all. When you place some of a feature's rooms ("7 of the 42 sit in src"), the total goes in the same sentence. When you name a directory for a feature, give its share and the directory's rooms together ("6 of the 22 hub rooms sit in cookbook/x/providers, which holds 6 rooms"). When a directory shares a wing's name, say "the tools directory" — the wing and the directory hold different numbers of a feature's rooms. Never write "the graph marks", "the onboarding marks", "the age marks" — name the features. The sheet's `relation_counts` gives how many relations the register draws by kind, and `diagnostic_features` how many features fired — "the 11 diagnostic features name 10 distinct sets of rooms", never "11 marks"; use those numbers or none. Do not restate the register otherwise: and the building's totals need no repeating. The sheet's `distinct_room_sets` is the number of distinct sets of rooms the diagnosis names — an identical pair is one set, a nesting is two — use that number rather than your own count. Write the reading: what shape the building has, where the marks sit relative to one another, what the overlaps mean for how many distinct sets of rooms there are, and what the decorative marks are excluded for. Every claim you make is still checked against the sheet.

Register, binding (validation-spec §2.1.1, mapper §3):
- Present tense only. Every feature rests on a signal that describes a present structural position. You may say where a room sits and what fires on it. You may not say what will happen, what breaks, what is at risk, what is fragile, what will ripple, what a change would cause. Those are predictions; none is licensed here. Avoid the words: break, will, would, risk, fragile, brittle, dangerous, ripple, cascade, fail, failure, likely, predict, expect, cause, collapse, vulnerable, exposed, threat, prone, future, soon, eventually, impact, consequence, propagate, bug, defect, safe, unsafe, critical.
- Every paragraph cites its evidence in brackets, where the bracket opens with the feature's own name from the facts sheet: [hub: src/db/connection.ts] for one room, [hub: src/a.ts, src/b.ts] for several, [hub ×27] for a count (×27 must equal that feature's count in the facts sheet). Several counts share one bracket separated by semicolons: [foundation ×21; onboarding/foundation ×21]. To name example rooms under a count, put them in the same bracket in the same sentence: [foundation ×21: src/a.ts, src/b.ts] — a room named in a later sentence needs its own bracket there. Never write the word "feature" inside a bracket; write the feature's name (foundation, hub, dark_room, scaffolding, corridor, …). A paragraph with no citation is struck.
- A room you name in a sentence must be covered by a feature you cite in that same sentence, and that feature must have fired on that room. Never name a room under a feature that did not fire on it.
- The register states the population, the mark counts and the co-located count; you may repeat a number when a sentence needs it, in the sentence that cites its feature, but do not open with an inventory.
- Name rooms; do not say what they do. A path is not a function: "src/error/QueryFailedError.ts" is a room, not "the error classes". Describe position and marks, not purpose.
- Do not set two features against each other ("against that", "offsets", "compensates"): the sets are independent measurements and the brief does not know their intersection unless the facts sheet states it.
- Disclose a consequence-implying name's position name in the same paragraph where the name first appears; the disclosure clause covers only itself, not the rest of the sentence.
- If the facts sheet lists `overlaps`, say so in one sentence naming both features: "The 70 flooded_basement rooms are the same 70 rooms as dark_room" — two marks on one set of rooms are one finding, not two.
- Never use "mostly", "concentrated", "the bulk", "spread across", "throughout", "every wing"; the register carries each feature's counts per wing — do not restate them (R16).
- A directory you name must contain a room you cite in the same sentence. A count you state must be the count (or a by_wing count) of a feature you cite in the same sentence, or a building-level count.
- Every number on the sheet has a unit (`units`): a count of rooms is never "N marks". `co_located_rooms` counts rooms carrying two or more marks.
- When `overlaps` lists `inert_terms`, say that the extra conjunct excludes nothing here, naming its signal: "flooded_basement adds load_index >= 0.10 to dark_room and it excludes nothing on this repository: the 70 rooms are the same 70".
- The register carries each feature's largest parent directory with its population; do not restate those numbers (R16). If you name a directory, cite a room in it in the same sentence (R10), and draw your example rooms from where the set's rooms are, not from where they flatter the mark.
- Never rank marks against each other ("the widest set", "larger than"); a p90 set has its size by construction. Never write "validated": no signal in this gate holds that status; every feature rests on an asserted signal.
- An overlap with `relation: within` is a nesting, not an identity: name both features, state the `n_outside` rooms the extra conjunct removed, and never call them one set or one finding. An identical overlap with `shared_predicate: true` is the same predicate under two profiles — say "the same predicate", never that two profiles agree.
- A share without its denominator is a base rate; the register states both and you state neither.
- The decorative disclosure names the ungrounded signal from `decorative_reason` ("crack and toothpick_wing rest on bug_pressure_index, which is unvalidated").
- "findings" is not a unit; count rooms or marks.
- Write every count as digits (267 rooms, not "two hundred sixty-seven"); every number must be a value on the facts sheet — never add, subtract, or count for yourself.
- The stance paragraph carries no citation.
- Use only numbers that appear in the facts sheet (counts, lines, fan-in, fan-out). No estimates, no percentages, no counts you computed yourself ("sixteen of the seventeen").
- Decorative features rest on nothing confirmed. Do not use them in any diagnosis and do not name the rooms they fired on. State the decorative count once, plainly, citing by count only, e.g. "27 decorative marks render but are not a diagnosis [crack ×27]."
- A feature whose name implies a consequence (foundation, toothpick_wing, crack) must be disclosed with its position name from the facts sheet, e.g. "foundation — a high-load hub, a position in the import graph, not a claim about what breaks".
- Do not give the building a one-word label (cathedral, shantytown, bunker, ruin). No archetype exists.
- The page header already states the calibration (in-repo, self-relative, one frame). Do not write a calibration or method paragraph.
- Do not invent rooms, wings, or features. Do not describe code you have not been given; the facts sheet is the whole building.

Form: 200–400 words of plain prose in short paragraphs; no headings, no bullet lists, no table; the surveyor's voice — exact, unimpressed, specific. Begin with the building's shape (wings and where the marks fall), then what the relations between marks make of it (how many distinct sets of rooms the diagnosis actually names), then the decorative disclosure in one sentence, then the stance sentence given in the facts sheet, verbatim or near it. The register is on the page; write what a reader of the register would still need said."""


def _user_message(facts_doc: dict[str, Any], violations: list[Violation] | None = None) -> str:
    slim = {k: v for k, v in facts_doc.items() if k not in ("rooms", "calibration")}
    msg = "FACTS SHEET (JSON):\n" + json.dumps(slim, indent=1, sort_keys=True, ensure_ascii=False)
    if violations:
        msg += (
            "\n\nYOUR PREVIOUS DRAFT FAILED THE REGISTER LINT. Fix every violation and rewrite the whole brief:\n"
            + "\n".join(
                f"- {v.rule} (paragraph {v.paragraph}): {v.detail} — «{v.text}»" for v in violations
            )
        )
    return msg


def anthropic_generator(
    model: str = DEFAULT_MODEL, effort: str = "high"
) -> Callable[[str, str], tuple[str, dict[str, Any]]]:
    """A generator over the Anthropic Messages API. Returns (text, provenance)."""
    import anthropic

    client = anthropic.Anthropic()

    def _gen(system: str, user: str) -> tuple[str, dict[str, Any]]:
        with client.beta.messages.stream(
            model=model,
            max_tokens=16000,
            system=system,
            messages=[{"role": "user", "content": user}],
            thinking={"type": "adaptive"},
            output_config={"effort": effort},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        ) as stream:
            resp = stream.get_final_message()
        if resp.stop_reason == "refusal":
            cat = getattr(getattr(resp, "stop_details", None), "category", None)
            raise RuntimeError(f"the model declined the request (refusal, category {cat!r})")
        text = "".join(b.text for b in resp.content if b.type == "text").strip()
        return text, {
            "model_requested": model,
            "model_served": resp.model,
            "request_id": getattr(resp, "_request_id", None),
            "stop_reason": resp.stop_reason,
            "effort": effort,
            "input_tokens": resp.usage.input_tokens,
            "output_tokens": resp.usage.output_tokens,
        }

    return _gen


# ---------------------------------------------------------------- the run


NL = "\n"


# D-043: the note is generated from the same constants the renderer computes with
RELATION_MIN_ROOMS = 3  # a set of fewer rooms is inside anything that contains it (D-041)
DIRECTORY_MIN_ROOMS = 6  # below this no directory is placed (D-040)
DIRECTORY_SHARE = 3  # a directory is shown when it holds a third or more (R15)
# D-043: the record a predicate reads, named beside each position so the gloss covers every row
_RECORDS: list[tuple[str, tuple[str, ...]]] = [
    (
        "import graph",
        ("fan_in", "fan_out", "centrality", "load_index", "fan_in_nonzero", "is_package_entry"),
    ),
    (
        "clock",
        (
            "age_days",
            "last_touched_days",
            "blame_age_median",
            "recent_commit_share",
            "neglect_index",
        ),
    ),
    ("test graph", ("test_fan_in", "reinforcement_index", "has_sibling_test")),
    (
        "edit record",
        (
            "commit_count",
            "churn_lines",
            "fix_count",
            "revert_count",
            "author_count",
            "bug_pressure_index",
            "change_pressure_index",
        ),
    ),
    ("size", ("size_loc", "nesting_proxy", "complexity_proxy_index")),
]


def _flag(feats: dict[str, dict[str, Any]], ov: dict[str, Any]) -> dict[str, Any]:
    """D-044: an overlap says whether both its features are diagnostic; only those count."""
    ov["diagnostic"] = bool(feats[ov["a"]]["diagnostic"] and feats[ov["b"]]["diagnostic"])
    return ov


def record_of(predicate: str) -> str:
    """The records a predicate reads, in a fixed order — 'import graph and clock' for
    flooded_basement. A position is a place in these records and nothing else."""
    found = [
        name for name, sigs in _RECORDS if any(re.search(rf"\b{sig}\b", predicate) for sig in sigs)
    ]
    return " and ".join(found) if found else "an unlisted record"


# D-042: the rules as the reader is told them — the header's checklist and the lint section both
# derive from this list, so the page cannot describe a rule the lint no longer applies
RULES: list[tuple[str, str]] = [
    ("R1", "consequence and forecast vocabulary refused outside a struck disclosure clause"),
    (
        "R2",
        "every citation resolves to a feature that fired on the rooms it names, with the count the skeleton records",
    ),
    ("R3", "a number is on the facts sheet and sits in the sentence that cites its feature"),
    (
        "R4",
        "decorative features cited by count only, never as diagnosis, with their ungrounded signal named",
    ),
    ("R5", "a consequence-implying name carries its position name where first used"),
    ("R6", "no whole-building label"),
    ("R7", "the diagnostic and decorative counts stated (met by the register)"),
    ("R8", "a room named in a sentence is covered by a feature cited in that sentence"),
    ("R9", "features with the same or nested rooms named together (met by the register)"),
    ("R10", "a directory named in a sentence contains a room cited in it"),
    ("R11", "no distributional adverb, ranking of marks, span or proximity between rooms"),
    (
        "R12",
        "a number wears its unit, a count of relations matches the register by kind; no ratio across units",
    ),
    (
        "R13",
        "a nesting is not an identity; a shared predicate is one measurement, not two agreeing",
    ),
    ("R14", "no 'validated' where no signal holds it"),
    ("R15", "a feature's largest directory named with its population (met by the register)"),
    (
        "R16",
        "a feature's count in a minority wing or a directory is sayable only where that wing or directory is named; the largest wing's count is the register's",
    ),
    (
        "R17",
        "a claim that a feature stands apart, or lacks a property another feature marks on its rooms, is checked against the register",
    ),
]


def render_register(facts_doc: dict[str, Any]) -> str:
    """D-039: the register — one row per feature with fixed slots, rendered from the facts sheet
    by code. It states what three hostile readings found the prose could only overclaim: the
    unit, the wing counts, the dominant directory with its denominator, the relations between
    features (identical / within, with the rooms outside and the inert conjunct), the reason a
    decorative feature is excluded. The prose beneath it is the reading, not the inventory."""

    def short(k: str) -> str:
        return k.split("/")[-1]

    def relations(key: str) -> str:
        out = []
        for ov in facts_doc.get("overlaps") or []:
            if key not in (ov["a"], ov["b"]):
                continue
            other = ov["b"] if ov["a"] == key else ov["a"]
            if ov["relation"] == "identical":
                if ov.get("shared_predicate"):
                    why = "same predicate, two profiles"
                elif ov.get("inert_terms"):
                    why = f"{', '.join(ov['inert_terms'])} excludes nothing"
                else:
                    why = ""
                out.append(f"= {short(other)}" + (f" ({why})" if why else ""))
            elif ov["a"] == key:
                # D-040: the remainder belongs to the superset — say whose rooms are outside
                out.append(
                    f"⊂ {short(other)} ({ov.get('n_outside')} {short(other)} room{'s' if ov.get('n_outside') != 1 else ''} outside this set)"
                )
            else:
                out.append(
                    f"⊃ {short(other)} ({ov.get('n_outside')} of these room{'s' if ov.get('n_outside') != 1 else ''} outside it)"
                )
        return "; ".join(out) or "no identity or containment"

    rows = []
    for f in facts_doc["features"]:
        key = f"{f['profile']}/{f['feature']}"
        bw = ", ".join(f"{k} {v}" for k, v in f.get("by_wing", {}).items())
        dd = f.get("dominant_dir") or {}
        # D-041: every fallback says the reason that is the reason, and a directory that is also a
        # wing name is marked as the parent, not the wing
        if not dd:
            dom = "no rooms"
        elif not dd.get("placeable", True):
            dom = f"too few rooms to place ({f['count']})"
        elif dd.get("holds_third"):
            as_parent = " (as parent, not the wing)" if dd["dir"] in facts_doc["wings"] else ""
            dom = f"{dd['dir']}{as_parent} {dd['n']} / {dd['population']}" + (
                " (tied)" if dd.get("tied") else ""
            )
        else:
            dom = "none holds a third"
        if f["decorative"]:
            what = f"decorative — {f.get('decorative_reason') or ''}".strip()
        else:
            what = f"`{f['predicate']}`"
        if f.get("caveat"):
            what += f" — caveat: {f['caveat']}"
        name = ("◌ " if f["decorative"] else "") + f["feature"]
        # D-041: the cell reads the field it claims to report; a consequence-implying name without a
        # position name is a ruleset defect and the page says so rather than denying it
        if f.get("position_name"):
            pos = f"{f['position_name']} ({record_of(f['predicate'])})"
        elif f.get("name_implies_consequence"):
            pos = f"POSITION NAME MISSING (ruleset defect); a position in the {record_of(f['predicate'])}"
        else:
            # D-044: the note promises the record beside every position; the lexicon is why there is
            # no position name, the record is what the predicate reads — both are said
            pos = f"no consequence word in the name (lexicon); a position in the {record_of(f['predicate'])}"
        rows.append(
            f"| {name} | {f['profile']} | {pos} | {f['count']} | {bw} | {dom} | {relations(key)} | {what} |"
        )
    wings = " · ".join(f"{k} {v}" for k, v in facts_doc["wings"].items())
    gate = facts_doc.get("gate") or {}
    asserted = sum(1 for v in gate.values() if v == "asserted")
    base = facts_doc.get("diagnostic_count_base", facts_doc["diagnostic_count"])
    dec = ", ".join(facts_doc["decorative"]["features"]) or "none"
    fp = (facts_doc.get("gate_fingerprint") or "?")[:12]
    head = (
        "## Register"
        + NL
        + NL
        + f"*Rendered from the facts sheet by code (brief {facts_doc.get('brief_version', BRIEF_VERSION)}); every cell is a field, no cell is a sentence. "
        + f"{facts_doc['population']} rooms in {facts_doc['wing_count']} wings ({wings}); {facts_doc['diagnostic_count']} diagnostic marks across all profiles "
        + f"({base} in the base profile), one mark per feature per room; identical pairs of diagnostic features mark {facts_doc.get('rooms_marked_twice', 0)} rooms twice ({facts_doc.get('rooms_marked_twice_shared_predicate', 0)} under one predicate in two profiles, {facts_doc.get('rooms_marked_twice_inert_conjunct', 0)} where two predicates draw one set because a conjunct excludes nothing); "
        + f"the diagnostic features name {facts_doc.get('distinct_room_sets', '?')} distinct sets of rooms; {facts_doc['decorative']['count']} decorative marks ({dec}); "
        + f"{facts_doc['co_located_rooms']} rooms carry two or more diagnostic marks; gate `{fp}`, {asserted} of {len(gate)} signals asserted, none validated. "
        + "◌ marks a decorative feature: excluded from the diagnosis. A position names where a room sits in the record its predicate reads — the record is named beside each position — and is not a claim about its condition (D-004 Q3). "
        + f"The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a {DIRECTORY_SHARE}rd or more of them and the feature has {DIRECTORY_MIN_ROOMS} or more rooms; a parent that shares a wing's name is marked as the parent. "
        + f"The relation column draws identity and containment, and only those, between features, diagnostic or decorative, with {RELATION_MIN_ROOMS} or more rooms; two sets that overlap without one containing the other are not related here, and 'no identity or containment' says exactly that. A caveat is the ruleset's own limit on what a predicate reads, never a claim about this repository. Every cell that is not a number is a cell's own answer, not a gap.*"
        + NL
        + NL
        + "| feature | profile | position | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate or reason |"
        + NL
        + "|---|---|---|---|---|---|---|---|"
        + NL
    )
    return head + NL.join(rows) + NL


def render_brief(
    text: str, facts_doc: dict[str, Any], violations: list[Violation], provenance: dict[str, Any]
) -> str:
    status = (
        "PASS"
        if not violations
        else f"FAILED ({len(violations)} violation{'s' if len(violations) != 1 else ''})"
    )
    if provenance.get("attempt"):
        status += f" on attempt {provenance['attempt']}"
    head = (
        f"# {facts_doc['repo']['name']} — architect's brief\n\n"
        f"*The register below is rendered from the facts sheet by code and carries the inventory (D-039); the reading beneath it is model-written and linted. "
        f"Register lint: **{status}**. What the lint checked: "
        + "; ".join(f"{rid} {desc}" for rid, desc in RULES)
        + ". "
        f"What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile {facts_doc['profile']}"
        + (f" + {', '.join(facts_doc['overlays'])}" if facts_doc["overlays"] else "")
        + f", geometry {facts_doc['geometry']}, skeleton `{facts_doc['skeleton_hash'][:12]}…`, facts `{facts_doc['facts_hash'][:12]}…`. "
        f"Calibration: {facts_doc.get('calibration', 'in-repo, self-relative')} — the time-lapse for this skeleton is the one under gate "
        f"`{(facts_doc.get('gate_fingerprint') or '?')[:12]}`. Brief {facts_doc.get('brief_version', BRIEF_VERSION)}; a PASS is a pass under that grammar (D-035).*\n\n"
    )
    prov = (
        "\n## Provenance\n\n"
        + "\n".join(f"- {k}: `{v}`" for k, v in sorted(provenance.items()) if v is not None)
        + "\n"
    )
    lint_md = "\n## Register lint\n\n"
    if violations:
        lint_md += (
            "| rule | paragraph | detail | text |\n|---|---|---|---|\n"
            + "\n".join(
                f"| {v.rule} | {v.paragraph} | {v.detail.replace('|', '/')} | {v.text.replace('|', '/')} |"
                for v in violations
            )
            + "\n\n**This brief failed the register lint and is not a diagnosis until it passes.**\n"
        )
    else:
        lint_md += (
            "No violations. Rules: "
            + ", ".join(f"{rid} {desc}" for rid, desc in RULES)
            + " (D-027 through D-042).\n"
        )
    register = render_register(facts_doc)
    return head + register + "\n## Reading\n\n" + text.strip() + "\n" + prov + lint_md


def relint(
    markdown: str, skeleton: dict[str, Any], substrate: dict[str, Any] | None
) -> dict[str, Any]:
    """Re-judge an existing brief.md under the current lint, keeping its prose and provenance."""
    body = markdown.split("\n## Provenance", 1)[0]
    paras = [p for p in re.split(r"\n\s*\n", body) if p.strip()]
    prose = "\n\n".join(
        p
        for p in paras
        if not p.startswith("#")
        and not p.startswith("*Register lint")
        and not p.startswith("*The register below")
        and not p.startswith("*Rendered from the facts sheet")
        and not p.lstrip().startswith("|")
    )
    prov: dict[str, Any] = {}
    m = re.search(r"## Provenance\n(.*?)(?:\n## |\Z)", markdown, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            mm = re.match(r"- ([^:]+): `(.*)`", line.strip())
            if mm:
                prov[mm.group(1)] = mm.group(2)
    f = facts(skeleton, substrate)
    viols = lint(prose, f, register=True)
    prov = {**prov, "relinted": f"brief {BRIEF_VERSION}", "facts_hash": f["facts_hash"]}
    return {
        "facts": f,
        "text": prose,
        "violations": [v.as_dict() for v in viols],
        "provenance": prov,
        "markdown": render_brief(prose, f, viols, prov),
        "passed": not viols,
    }


def run_brief(
    skeleton: dict[str, Any],
    substrate: dict[str, Any] | None,
    generate: Callable[[str, str], tuple[str, dict[str, Any]]] | None = None,
    draft: str | None = None,
    max_attempts: int = 2,
) -> dict[str, Any]:
    """Facts → (draft | generate) → lint → rendered brief. Returns a dict with
    `facts`, `text`, `violations`, `provenance`, `markdown`, `passed`."""
    f = facts(skeleton, substrate)
    if draft is not None:
        text, prov = draft, {"generator": "draft", "facts_hash": f["facts_hash"]}
        viols = lint(text, f, register=True)
    else:
        if generate is None:
            raise ValueError("no generator and no draft")
        viols: list[Violation] = []
        text, prov = "", {}
        attempts_log: list[dict[str, Any]] = []
        for attempt in range(1, min(max_attempts, MAX_ATTEMPTS_CAP) + 1):
            text, prov = generate(SYSTEM, _user_message(f, viols if attempt > 1 else None))
            viols = lint(text, f, register=True)
            attempts_log.append({"attempt": attempt, "violations": [v.rule for v in viols]})
            prov = {
                **prov,
                "attempt": attempt,
                "attempts_log": "; ".join(
                    f"{a['attempt']}: {', '.join(a['violations']) or 'pass'}" for a in attempts_log
                ),
                "facts_hash": f["facts_hash"],
                "brief_version": BRIEF_VERSION,
            }
            if not viols:
                break
    return {
        "facts": f,
        "text": text,
        "violations": [v.as_dict() for v in viols],
        "provenance": prov,
        "markdown": render_brief(text, f, viols, prov),
        "passed": not viols,
    }
