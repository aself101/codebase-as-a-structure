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
from dataclasses import dataclass
from typing import Any

BRIEF_VERSION = "0.24.0"  # D-056: a scope is named by its manifest path; by_package is an ordered list; a containment not by predicate says what signal the two read in common; ◌ travels with the name; containers that are one set are one entry

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
                    "decorative_signal_reasons": dict(f.get("decorative_signal_reasons") or {}),  # D-054
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
        def _parent_pop(d: str) -> int:
            return sum(
                1
                for nid in skeleton["strata"]["by_node"]
                if (nid.rsplit("/", 1)[0] if "/" in nid else "(root)") == d
            )

        pop = _parent_pop(top[0])
        # D-054 (fifteenth seating): "(tied)" named no partner — on eslint package_entry's cell
        # named packages/eslint-config-eslint 4 / 5 over lib 4 by name order, and the wing-named
        # parent the note promises to mark was the one left out. A tie names every partner with
        # its numbers (D-045 item 3: a directory the register names carries its numbers).
        tied_with = [
            {"dir": d, "n": n, "population": _parent_pop(d)}
            for d, n in sorted(bd.items())
            if n == top[1] and d != top[0]
        ]
        # D-040: `dir` is the room's immediate parent (non-recursive), `population` the rooms whose
        # parent it is; `holds_third` is R15's bar — below it the register prints no directory
        e["dominant_dir"] = {
            "dir": top[0],
            "n": top[1],
            "population": pop,
            "tied": tied,
            "tied_with": tied_with,
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
    # D-052: co-location is counted in distinct sets, the unit the most-marked table uses — a room
    # under one predicate in two profiles carries two marks and is not co-located with anything
    co_located_all = co_located(feats.values())
    # D-048: the rooms carrying the most diagnostic marks, each with every diagnostic feature that
    # marks it — the one thing the register does not print and the reading is bound to say (R19)
    most_marked_rooms = most_marked(feats.values())
    # D-049: the rooms two diagnostic features share, for every pair — the register draws identity
    # and containment in the relation column; the matrix says how the other sets sit against
    # each other (four rooms are both import_root and package_entry on eslint: the caveat's live case)
    _dkeys = sorted(k for k, e in feats.items() if e["diagnostic"])
    shared_rooms = [
        {"a": a, "b": b, "shared": len(set(feats[a]["rooms"]) & set(feats[b]["rooms"]))}
        for i, a in enumerate(_dkeys)
        for b in _dkeys[i + 1 :]
    ]
    # D-049: the list is capped; the sheet says how many rooms carry the most so a page can say
    # whether the cap bit (twelve rooms tied at seven on eslint; five were listed). D-050: the most
    # is counted in distinct sets, and every row carries the rooms at its own count — the twelfth
    # seating found a fill row (one of eight at six, first by path) under a lead that said "all"
    rooms_at_most_sets = most_marked_rooms[0]["rooms_at_this_count"] if most_marked_rooms else 0
    # D-036: two diagnostic features whose room sets coincide, or nest, are one set of rooms;
    # the sheet says so and R9 makes the prose say so
    overlaps: list[dict[str, Any]] = []
    # D-041: a set of fewer than three rooms is inside anything that contains it; no relation is drawn
    # D-055 (sixteenth seating): unless the predicates guarantee it — toothpick_wing's two rooms on
    # typeorm were inside foundation and crack by conjunction and the cell said "too few rooms".
    # The floor exists for containment by accident; a containment by predicate is not one.
    diag = [
        (k, set(e["rooms"]))
        for k, e in sorted(feats.items())
        if len(e["rooms"]) >= 1  # D-044: decorative features too — the note promised every set
    ]
    for i, (ka, ra) in enumerate(diag):
        for kb, rb in diag[i + 1 :]:
            under = len(ra) < RELATION_MIN_ROOMS or len(rb) < RELATION_MIN_ROOMS
            if under:
                if ra < rb and _conjoins(feats[ka], feats[kb]):
                    overlaps.append(_flag(feats, _within(feats, ka, kb, ra, rb)))
                elif rb < ra and _conjoins(feats[kb], feats[ka]):
                    overlaps.append(_flag(feats, _within(feats, kb, ka, rb, ra)))
                continue
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
                overlaps.append(_flag(feats, _within(feats, ka, kb, ra, rb)))
            elif rb < ra:
                overlaps.append(_flag(feats, _within(feats, kb, ka, rb, ra)))
    # D-040/D-044: the diagnosis's counts come from diagnostic pairs only; a decorative pair is drawn
    # in the register (the note promises every set of three or more rooms) and counted nowhere
    diag_overlaps = [o for o in overlaps if o.get("diagnostic")]
    # D-040: how many distinct sets of rooms the diagnosis names — identical pairs are one set,
    # nestings stay two; and how many of the all-profile marks fall on identical pairs twice
    # D-052: one computation — the sets themselves, the same identity the most-marked table
    # counts per room; n_diag minus the identical overlaps was floored at three rooms and would
    # have disagreed with the table on a triple or an under-floor twin
    n_diag = sum(1 for e in feats.values() if e["diagnostic"] and e["rooms"])
    identical = [o for o in diag_overlaps if o["relation"] == "identical"]
    distinct_room_sets = distinct_sets(feats.values())
    # D-044: this number counts rooms an identical pair marks twice, not marks — it was named as marks
    # D-047: distinct rooms — a room in two identical pairs is one room marked twice twice over,
    # not two rooms (typeorm: six rooms sit in both pairs; 129 summed, 123 distinct)
    _twice: set[str] = set()
    for o in identical:
        _twice |= set(feats[o["a"]]["rooms"])
    rooms_marked_twice = len(_twice)
    relation_counts = {
        "identical": sum(1 for o in overlaps if o["relation"] == "identical"),
        "within": sum(1 for o in overlaps if o["relation"] == "within"),
        "total": len(overlaps),
    }
    # D-042: a number with two causes is two numbers — a gloss that names one cause is false of the other
    _shared = {r for o in identical if o.get("shared_predicate") for r in feats[o["a"]]["rooms"]}
    _inert = {r for o in identical if not o.get("shared_predicate") for r in feats[o["a"]]["rooms"]}
    rooms_marked_twice_shared_predicate = len(_shared)
    rooms_marked_twice_inert_conjunct = len(_inert)
    rooms_in_both_kinds = len(_shared & _inert)
    gate_fp = skeleton.get("substrate_config_fingerprint")
    if not gate_fp:
        raise ValueError(
            "skeleton carries no substrate_config_fingerprint; the brief cannot name its gate (D-036)"
        )
    s = skeleton["summary"]
    # D-054 (fifteenth seating): D-053 counted package scopes over every substrate node — on eslint
    # 21 over 1481 nodes where the 473 rooms span 6 (the test files the population excludes carry
    # the other 15); the three other pages coincided. The count is over the population, and the
    # rooms per scope travel with it so the pooling the calibration sentence discloses has a size.
    by_package: dict[str, int] = {}
    for nid in skeleton["strata"]["by_node"]:
        # D-055 (sixteenth seating): "(root)" was the wing (3 rooms on typeorm) and the scope (502)
        # in one note; the scope's root is the repository's own manifest and is named as such
        pkg = ((nodes.get(nid) or {}).get("metrics") or {}).get("package", "")
        # D-056 (seventeenth seating): "cookbook 136" (the wing) and "cookbook 1" (the scope of
        # cookbook/package.json) sat in one paragraph; D-055 had renamed the root scope only. A
        # scope is named by its manifest path, which no wing name can equal.
        scope = f"{pkg}/{ROOT_SCOPE}" if pkg else ROOT_SCOPE
        by_package[scope] = by_package.get(scope, 0) + 1
    n_packages = len(by_package)
    population = s["population"]
    doc = {
        "brief_version": BRIEF_VERSION,
        "repo": {"name": skeleton["repo"]["name"], "head_sha": skeleton["repo"]["head_sha"]},
        "skeleton_hash": skeleton["skeleton_hash"],
        "profile": skeleton["profile"]["name"],
        "overlays": list(s.get("overlay_profiles") or []),
        "geometry": skeleton["geometry"]["name"],
        # D-053: what a wing is, and how many package scopes the one population spans
        "wing_depth": int(skeleton["geometry"].get("wing_depth", 1)),
        "packages": n_packages,
        # D-056: an ordered list — the sheet is written with sorted keys, and a dict's "largest
        # first" was true of the render and false of the file the viewer would read
        "by_package": [{"scope": k, "rooms": v} for k, v in sorted(by_package.items(), key=lambda kv: (-kv[1], kv[0]))],
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
        "most_marked_rooms": most_marked_rooms,
        "rooms_at_most_sets": rooms_at_most_sets,
        "shared_rooms": shared_rooms,
        # D-046 addendum: the prose kept computing this to say "the N features name M sets"
        "diagnostic_features": n_diag,
        "distinct_room_sets": distinct_room_sets,
        "rooms_marked_twice": rooms_marked_twice,
        "rooms_marked_twice_shared_predicate": rooms_marked_twice_shared_predicate,
        "rooms_marked_twice_inert_conjunct": rooms_marked_twice_inert_conjunct,
        "rooms_in_both_kinds": rooms_in_both_kinds,
        "relation_counts": relation_counts,
        # D-037: every building-level number carries its unit; a count of rooms is not a count of marks
        "units": {
            "population": "rooms",
            "wings": "rooms",
            "diagnostic_count": "marks",
            "diagnostic_count_base": "marks",
            "decorative.count": "marks",
            "co_located_rooms": "rooms carrying two or more distinct diagnostic sets, across all profiles (a predicate under two profiles is one set)",
            "most_marked_rooms": f"the rooms carrying the most distinct diagnostic sets (at most {MOST_MARKED_ROOMS}; {MOST_MARKED_ORDER}), each with every diagnostic feature that marks it, profile-qualified where a feature is under two profiles; sets counts distinct room sets; marks counts one per feature per profile; rooms_at_this_count is the rooms under two or more sets carrying the row's sets count, and listed_at_this_count how many of them the list carries, the first by path",
            "rooms_at_most_sets": "rooms carrying that most; when it exceeds the rooms listed at it, the list is the first of them by path",
            "shared_rooms": "rooms both features of a pair mark, for every pair of diagnostic features; identity and containment are the relation column's",
            "diagnostic_features": "diagnostic features that fired (features, not marks or rooms)",
            "distinct_room_sets": "sets of rooms the diagnostic features name — the room sets themselves, so identical sets are one whatever their size; a nesting is two",
            "rooms_marked_twice": "rooms an identical pair of diagnostic features marks twice (each such room carries two marks)",
            "rooms_marked_twice_shared_predicate": "of those, rooms where two profiles carry one predicate",
            "rooms_marked_twice_inert_conjunct": "of those, rooms where two predicates draw one set because a conjunct excludes nothing",
            "rooms_in_both_kinds": "rooms counted under both causes (the two counts overlap by this many)",
            "relation_counts": "relations the register draws, by kind, over every feature with enough rooms, decorative included, and containments the predicates guarantee at any count",
            "dominant_dir": "the immediate parent directory (non-recursive) holding the most of a feature's rooms; shown only when it holds a third or more; tied_with names every other directory holding as many",
            "by_package": f"rooms of the population per package scope, each named by its manifest path (the nearest package.json above the room; {ROOT_SCOPE} is the repository's own), an ordered list, largest first",
            "feature.count": "rooms (one mark per room)",
        },
        "overlaps": overlaps,
        "calibration": (
            f"in-repo, self-relative (system spec §5.3): every pNN ranks the {population} rooms as one population"
            + (f", across {n_packages} package scopes (package.json) pooled — per-package calibration is an open question of the mapper (architect-brief spec §5, mapper §7 Q7)" if n_packages > 1 else "")
            + "; one frame — stability is read from a time-lapse, not from this page"
        ),
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
# D-048: a sentence may open with a digit — the prompt requires digits — and the lookahead
# admitted only letters, so "… 2 within. 254 rooms …" was one sentence to every per-sentence
# rule and a bracket warranting nothing passed R2b on the merged span
SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Za-z0-9_\[`])")


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
    for m in facts_doc.get("most_marked_rooms") or []:
        allowed_numbers.update((m["marks"], m.get("sets", 0), m.get("rooms_at_this_count", 0)))
    allowed_numbers.add(facts_doc.get("rooms_at_most_sets", 0))
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
    allowed_numbers.add(facts_doc.get("rooms_in_both_kinds", 0))
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
    for sr in facts_doc.get("shared_rooms") or []:
        for k in (sr["a"], sr["b"], sr["a"].split("/")[-1], sr["b"].split("/")[-1]):
            feature_numbers.setdefault(k, set()).add(sr["shared"])
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
    rooms_only = (
        {facts_doc["population"], facts_doc["co_located_rooms"], facts_doc.get("rooms_at_most_sets", 0)}
        | {m.get("rooms_at_this_count", 0) for m in facts_doc.get("most_marked_rooms") or []}
        | set(facts_doc["wings"].values())
        # D-048: a directory's share and population are rooms — "which holds 61 rooms" was refused
        # as marks on typeorm because 61 was also a mark total
        | {
            v
            for f in facts_doc["features"]
            for v in ((f.get("dominant_dir") or {}).get("n"), (f.get("dominant_dir") or {}).get("population"))
            if v is not None
        }
    )
    marks_only = {
        *(m["marks"] for m in facts_doc.get("most_marked_rooms") or []),
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
                # D-046 addendum: "the largest wing" compares wings, whatever else the sentence cites
                window = low_sent[max(0, m.start() - 30) : m.end() + 30]
                if re.search(r"\bwings?\b|\bdirector(?:y|ies)\b", window):
                    continue
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
            # R16 (D-047): "N wings hold …:" followed by a list of fewer than N wings is a partial
            # enumeration presented as the whole; the building's wing counts are all sayable, so say all or none
            mw = re.search(rf"\b{facts_doc['wing_count']}\s+wings\b[^.;]*?:", low_sent)
            if mw:
                listed = sum(
                    1
                    for w in wing_names
                    if re.search(
                        rf"(?<![\w/@.-]){re.escape(w if w != '(root)' else 'root')}(?![\w/])",
                        low_sent,
                    )
                )
                if 0 < listed < facts_doc["wing_count"]:
                    out.append(
                        Violation(
                            "R16-restatement",
                            i,
                            sent[:160],
                            f"{facts_doc['wing_count']} wings announced and {listed} listed; name every wing with its rooms, or none",
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
        # D-046 addendum: a paragraph that names no feature and no room and states only building-level
        # numbers is the building's shape (wings, population) — the register's, with nothing to cite
        building_only = (
            not any(
                re.search(rf"\b{re.escape(x['feature'])}\b", para) for x in facts_doc["features"]
            )
            and not any(_mentions(para, rid) for rid in room_ids)
            and INTEGER.findall(BRACKET.sub("", para))
            and all(int(n) in allowed_numbers for n in INTEGER.findall(BRACKET.sub("", para)))
        )
        if (
            not cites
            and not is_stance
            and not building_only
            and not (is_disclosure and decorative_only)
        ):
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
            # D-048: the sentence before this one, in this loop (the first loop's prev_sent is stale here)
            _sents = SENTENCE.split(para)
            prev_sent = _sents[_sents.index(sent) - 1] if sent in _sents and _sents.index(sent) else ""
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
                            # D-047: "(root)" is written "the root" or "the root wing" in prose
                            or (
                                w == "(root)"
                                and re.search(r"\b(?:the\s+)?root(?:\s+wing|\s+level)?\b", bare)
                                is not None
                            )
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
                    # D-048: a directory is named, not a room inside it — "lib/config/default-config.js"
                    # does not name lib/config (the R19 sentence was refused for corridor's unplaced
                    # directory on eslint)
                    if dd and re.search(rf"(?<![\w/@.-]){re.escape(dd['dir'])}(?![\w/])", bare):
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
                            has_pop = re.search(rf"\b{dd.get('population')}\b", bare) is not None or (
                                # D-048: the population one sentence back, anchored on the directory's
                                # name — the split before a digit turned "which holds 22 rooms. 8 of
                                # the 27 … sit there" into two sentences, and a denominator a name
                                # anchors one sentence earlier is not a base rate
                                bool(prev_sent)
                                and re.search(
                                    rf"(?<![\w/@.-]){re.escape(dd['dir'])}(?![\w/])",
                                    BRACKET.sub("", prev_sent),
                                )
                                is not None
                                and re.search(
                                    rf"\b{dd.get('population')}\b", BRACKET.sub("", prev_sent)
                                )
                                is not None
                            )
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
            and re.search(rf"(?<![\w/@.-]){re.escape(dd['dir'])}(?![\w/])", snt)
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

# The model-written reading, its prompt (SYSTEM), its input message and the Anthropic generator
# lived here from D-027 to D-049. Eleven hostile seatings (tracker runs 17-28) found the reading
# reciting the register; everything it could add was a field. The page is rendered by code; the
# lint below stays for a hand-written draft (--draft). The prompt and generator are in the history
# at 0d8f5c0.


# ---------------------------------------------------------------- the run


NL = "\n"


# D-043: the note is generated from the same constants the renderer computes with
RELATION_MIN_ROOMS = 3  # a set of fewer rooms is inside anything that contains it (D-041)
MOST_MARKED_ROOMS = 5  # the sheet lists this many of the rooms carrying the most marks (D-048)
ROOT_SCOPE = "package.json"  # D-056: a scope is named by its manifest path — the root's is the bare file; "(root)" is the wing and no scope can share a wing's name
# D-055: the ordering the most-marked table uses, said once — the sheet's unit gloss kept "then marks"
# after D-054 dropped it from the key, and the lead said the opposite on the same page
MOST_MARKED_ORDER = "ordered by sets (a feature under two profiles, or two features drawing one set, is one set), then by path — marks (one per feature per profile) are shown and order nothing, since within a tier they differ only by the double count the register discounts"
DIRECTORY_MIN_ROOMS = 6  # below this no directory is placed (D-040)
DIRECTORY_SHARE = 3  # a directory is shown when it holds a third or more (R15)
# D-043: the record a predicate reads, named beside each position so the gloss covers every row.
# D-053: raw signals only — a blend's records are derived from the inputs config.ALLOWED_INPUTS
# declares for it (the fourteenth seating found bug_pressure_index filed under "edit record" while
# it reads recency, the clock, at 0.2; D-048 had fixed load_index alone, by hand)
_RECORDS: list[tuple[str, tuple[str, ...]]] = [
    ("import graph", ("fan_in", "fan_out", "centrality", "fan_in_nonzero")),
    # D-052: the declared entry is read from package.json (D-029), not from the import graph —
    # the thirteenth seating found "declared package entry (import graph)" on the register
    ("package manifest", ("is_package_entry",)),
    ("clock", ("age_days", "last_touched_days", "blame_age_median", "recent_commit_share")),
    ("test graph", ("test_fan_in", "reinforcement_index", "has_sibling_test")),
    ("edit record", ("commit_count", "churn_lines", "fix_count", "revert_count", "author_count")),
    ("size", ("size_loc", "nesting_proxy")),
]
# D-053: the raw signal each declared blend input is read from (derived.compute_indices)
_INPUT_SIGNAL: dict[str, str] = {
    "fan_in_nonzero": "fan_in",
    "inv_fan_out": "fan_out",
    "size_loc": "size_loc",
    "recency": "last_touched_days",
    "inv_recent_commit_share": "recent_commit_share",
    "fix_count_nonzero": "fix_count",
    "fix_ratio": "fix_count",
}


def records_of_signal(sig: str) -> list[str]:
    """D-053: the records a signal is read from — a raw signal's record, or every record of a
    blend's declared inputs (config.ALLOWED_INPUTS), so the lexicon cannot omit an input by hand."""
    from .config import ALLOWED_INPUTS

    if sig in ALLOWED_INPUTS:
        out: list[str] = []
        for inp in ALLOWED_INPUTS[sig]:
            for r in records_of_signal(_INPUT_SIGNAL.get(inp, inp)):
                if r not in out:
                    out.append(r)
        return [name for name, _ in _RECORDS if name in out]
    return [name for name, sigs in _RECORDS if sig in sigs]


def sets_per_room(features) -> dict[str, int]:
    """D-052: for every marked room, the number of distinct diagnostic room sets that contain it —
    one computation for the header's building count, the co-location count and the most-marked
    table, so no two cells can count sets two ways."""
    feats = [e for e in features if e["diagnostic"]]
    ids = {id(e): frozenset(e["rooms"]) for e in feats}
    rooms = {r for e in feats for r in e["rooms"]}
    return {r: len({ids[id(e)] for e in feats if r in ids[id(e)]}) for r in rooms}


def distinct_sets(features) -> int:
    """D-052: the number of distinct room sets the diagnostic features draw (an empty set is none)."""
    return len({frozenset(e["rooms"]) for e in features if e["diagnostic"] and e["rooms"]})


def co_located(features) -> int:
    """D-052: rooms under two or more distinct diagnostic sets."""
    return sum(1 for v in sets_per_room(features).values() if v >= 2)


def most_marked(features) -> list[dict[str, Any]]:
    """D-048: the rooms carrying the most diagnostic marks, each with every diagnostic feature that
    marks it. D-050: ordered by distinct sets (two features drawing one set of rooms, or one
    predicate under two profiles, mark a room once in this count — the unit the header uses for
    the building), then by marks, then by path; at most MOST_MARKED_ROOMS; each row carries the
    rooms at its own sets count. D-052: a room under one set is not listed (the floor is sets, as
    the co-location count is), and each row says how many rooms of its tier the list carries — the
    thirteenth seating found a tier of four listed as three under a lead that said "first by path"
    of every row. A feature under two profiles is named with its profile so names count marks."""
    feats = [e for e in features if e["diagnostic"]]
    twice = {e["feature"] for e in feats if sum(1 for x in feats if x["feature"] == e["feature"]) > 1}
    marks: dict[str, int] = {}
    for e in feats:
        for r in e["rooms"]:
            marks[r] = marks.get(r, 0) + 1
    set_ids = {id(e): frozenset(e["rooms"]) for e in feats}
    sets = sets_per_room(feats)
    at_count: dict[int, int] = {}
    for r, n in sets.items():
        if n >= 2:
            at_count[n] = at_count.get(n, 0) + 1
    # D-054 (fifteenth seating): within a tier of equal sets, marks differ only by the double count
    # the header discounts (a set under two profiles); on eslint's tier of 13 at six sets the marks
    # key was foundation's two profiles and nothing else. Sets, then path.
    top = [
        (r, n) for r, n in sorted(marks.items(), key=lambda kv: (-sets[kv[0]], kv[0])) if sets[r] >= 2
    ][:MOST_MARKED_ROOMS]
    listed: dict[int, int] = {}
    for r, _ in top:
        listed[sets[r]] = listed.get(sets[r], 0) + 1
    return [
        {
            "room": r,
            "sets": sets[r],
            "marks": n,
            "rooms_at_this_count": at_count[sets[r]],
            "listed_at_this_count": listed[sets[r]],
            "features": sorted(
                (f"{e['profile']}/{e['feature']}" if e["feature"] in twice else e["feature"])
                for e in feats
                if r in set_ids[id(e)]
            ),
        }
        for r, n in top
    ]


def _signals_read(predicate: str) -> set[str]:
    """D-056: the raw signals a predicate reads, a blend expanded through its declared inputs
    (config.ALLOWED_INPUTS, _INPUT_SIGNAL) — the same walk records_of_signal makes for the record column."""
    from .config import ALLOWED_INPUTS

    out: set[str] = set()
    for term in str(predicate or "").split(" and "):
        sig = term.strip().split(" ")[0]
        if not sig:
            continue
        if sig in ALLOWED_INPUTS:
            out |= {_INPUT_SIGNAL.get(i, i) for i in ALLOWED_INPUTS[sig]}
        else:
            out.add(sig)
    return out


def _conjoins(inner: dict[str, Any], outer: dict[str, Any]) -> bool:
    """D-053: a containment holds by predicate when the inner feature's predicate conjoins every
    term of the outer's — corridor ⊂ hub on every repository; toothpick_wing ⊂ lit_room on one.
    The fourteenth seating found five of six containments drawn like the one the repository decided."""
    terms = lambda p: {t.strip() for t in str(p or "").split(" and ")}  # noqa: E731
    return bool(terms(outer["predicate"])) and terms(outer["predicate"]) <= terms(inner["predicate"])


def _within(feats: dict[str, dict[str, Any]], inner: str, outer: str, ri: set[str], ro: set[str]) -> dict[str, Any]:
    """A containment overlap. D-053: by_predicate when the inner conjoins the outer's terms.
    D-056 (seventeenth seating): the silence of the marker had acquired a meaning — "independent"
    — the page never assigned; toothpick_wing ⊂ lit_room on mcp-secure-server is unmarked while
    bug_pressure_index reads recency, the clock lit_room reads. A containment not by predicate
    says which raw signals the two predicates read in common, or that there are none."""
    byp = _conjoins(feats[inner], feats[outer])
    shared = sorted(_signals_read(feats[inner]["predicate"]) & _signals_read(feats[outer]["predicate"])) if not byp else []
    return {"a": inner, "b": outer, "relation": "within", "n": len(ri), "n_outside": len(ro - ri), "by_predicate": byp, "shared_signals": shared}


def _flag(feats: dict[str, dict[str, Any]], ov: dict[str, Any]) -> dict[str, Any]:
    """D-044: an overlap says whether both its features are diagnostic; only those count."""
    ov["diagnostic"] = bool(feats[ov["a"]]["diagnostic"] and feats[ov["b"]]["diagnostic"])
    return ov


def record_of(predicate: str) -> str:
    """The records a predicate reads, in a fixed order — 'import graph and clock' for
    flooded_basement. A position is a place in these records and nothing else."""
    from .config import ALLOWED_INPUTS

    sigs = {sig for _, ss in _RECORDS for sig in ss} | set(ALLOWED_INPUTS)
    read = {r for sig in sigs if re.search(rf"\b{sig}\b", predicate) for r in records_of_signal(sig)}
    found = [name for name, _ in _RECORDS if name in read]
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
    (
        "R18",
        "no family of marks the sheet does not define (the graph marks, the onboarding marks); a family every cited feature's record reads is admitted",
    ),
]


def render_register(facts_doc: dict[str, Any]) -> str:
    """D-039: the register — one row per feature with fixed slots, rendered from the facts sheet
    by code. It states what three hostile readings found the prose could only overclaim: the
    unit, the wing counts, the dominant directory with its denominator, the relations between
    features (identical / within, with the rooms outside and the inert conjunct), the reason a
    decorative feature is excluded. The prose beneath it is the reading, not the inventory."""

    # D-050: a feature under two profiles is named with its profile everywhere it is named — the
    # matrix already did; the relation cell read "= foundation" on the foundation row
    _label = qualified_labels([f"{x['profile']}/{x['feature']}" for x in facts_doc["features"]])

    _dec = {f"{x['profile']}/{x['feature']}" for x in facts_doc["features"] if x["decorative"]}
    _rooms = {f"{x['profile']}/{x['feature']}": frozenset(x["rooms"]) for x in facts_doc["features"]}

    def plain(k: str) -> str:
        return _label.get(k, k.split("/")[-1])

    def short(k: str) -> str:
        # D-056: ◌ travels with the name — four relation cells named toothpick_wing without it
        return ("◌ " if k in _dec else "") + plain(k)

    def why_within(ov: dict[str, Any]) -> str:
        if ov.get("by_predicate"):
            return "by its predicate; "
        if "shared_signals" not in ov:
            return ""
        sh = ov["shared_signals"]
        return (f"reads {', '.join(sh)} with it; " if sh else "no signal in common; ")

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
                # D-040: the remainder belongs to the superset — say whose rooms are outside;
                # D-053: a containment the predicates guarantee says so; D-056: containers that
                # are one set of rooms are one entry, named with every name that draws the set
                same = [o for o in facts_doc.get("overlaps") or [] if o["a"] == key and o["relation"] == "within" and _rooms.get(o["b"]) == _rooms.get(other)]
                if same and same[0] is not ov:
                    continue
                names = " = ".join(short(o["b"]) for o in (same or [ov]))
                out.append(
                    f"⊂ {names} ({why_within(ov)}{ov.get('n_outside')} {plain(other)} room{'s' if ov.get('n_outside') != 1 else ''} outside this set)"
                )
            else:
                out.append(
                    f"⊃ {short(other)} ({why_within(ov)}{ov.get('n_outside')} of these room{'s' if ov.get('n_outside') != 1 else ''} outside it)"
                )
        return "; ".join(out) or "no identity or containment"

    def relation_cell(f: dict[str, Any], key: str) -> str:
        # D-047: a set under the floor was not related to anything; the cell says that, not "none".
        # D-055: except where the predicates guarantee a containment — drawn at any count
        if f["count"] < RELATION_MIN_ROOMS:
            drawn = relations(key)
            drawn = "" if drawn == "no identity or containment" else drawn + "; "
            return f"{drawn}too few rooms for any other relation ({f['count']})"
        return relations(key)

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
            partners = ", ".join(
                f"{t['dir']}{' (as parent, not the wing)' if t['dir'] in facts_doc['wings'] else ''} {t['n']} / {t['population']}"
                for t in dd.get("tied_with") or []
            )
            dom = f"{dd['dir']}{as_parent} {dd['n']} / {dd['population']}" + (
                (f" (tied with {partners})" if partners else " (tied)") if dd.get("tied") else ""
            )
        else:
            dom = "none holds a third"
        if f["decorative"]:
            # D-055: the predicate is on the row — "the fragility half" of a reason was unresolvable
            # from a row that printed the reason and not the conjunction it is half of
            what = f"`{f['predicate']}` — decorative: {f.get('decorative_reason') or ''}".strip()
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
            f"| {name} | {f['profile']} | {pos} | {f['count']} | {bw} | {dom} | {relation_cell(f, key)} | {what} |"
        )
    wings = " · ".join(f"{k} {v}" for k, v in facts_doc["wings"].items())
    scopes = " · ".join(f"{e['scope']} {e['rooms']}" for e in (facts_doc.get("by_package") or []))  # D-054; D-056: a list
    gate = facts_doc.get("gate") or {}
    asserted = sum(1 for v in gate.values() if v == "asserted")
    # D-050: "none validated" was a literal beside a counted "asserted"; both are read from the gate
    validated = sum(1 for v in gate.values() if v == "validated")
    validated_text = "none validated" if validated == 0 else f"{validated} validated"
    base = facts_doc.get("diagnostic_count_base", facts_doc["diagnostic_count"])
    dec = ", ".join(facts_doc["decorative"]["features"]) or "none"
    fp = (facts_doc.get("gate_fingerprint") or "?")[:12]
    head = (
        "## Register"
        + NL
        + NL
        + f"*Rendered from the facts sheet by code (brief {facts_doc.get('brief_version', BRIEF_VERSION)}); every cell is a field, a count, or a fixed text over them; no cell is written. "
        + f"{facts_doc['population']} rooms in {facts_doc['wing_count']} wings ({wings}); {facts_doc['diagnostic_count']} diagnostic marks across all profiles "
        + f"({base} in the base profile), one mark per feature per room; identical pairs of diagnostic features mark {facts_doc.get('rooms_marked_twice', 0)} rooms twice ({facts_doc.get('rooms_marked_twice_shared_predicate', 0)} under one predicate in two profiles, {facts_doc.get('rooms_marked_twice_inert_conjunct', 0)} where two predicates draw one set because a conjunct excludes nothing, {facts_doc.get('rooms_in_both_kinds', 0)} under both); "
        + f"the diagnostic features name {facts_doc.get('distinct_room_sets', '?')} distinct sets of rooms; {facts_doc['decorative']['count']} decorative marks ({dec}); "
        + f"{facts_doc['co_located_rooms']} rooms carry two or more distinct diagnostic sets; gate `{fp}`, {asserted} of {len(gate)} signals asserted, {validated_text}. "
        + f"A wing is a directory at depth {facts_doc.get('wing_depth', 1)} of the tree (the ruleset's wing_depth), not a package; the population spans {facts_doc.get('packages', 1)} package scope{'s' if facts_doc.get('packages', 1) != 1 else ''}"
        + (f" (rooms per scope, largest first, each scope named by the manifest that holds it: {scopes})" if facts_doc.get("by_package") else "")
        + ". "
        + "◌ marks a decorative feature: excluded from the diagnosis. A position names where a room sits in the record its predicate reads — the record is named beside each position — and is not a claim about its condition (D-004 Q3). "
        + f"The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a {DIRECTORY_SHARE}rd or more of them and the feature has {DIRECTORY_MIN_ROOMS} or more rooms; a parent that shares a wing's name is marked as the parent. "
        + f"The relation column draws identity and containment, and only those, between features, diagnostic or decorative, with {RELATION_MIN_ROOMS} or more rooms — and a containment the predicates guarantee at any count; two sets that overlap without one containing the other are not related here, and 'no identity or containment' says exactly that. A caveat is the ruleset's own limit on what a predicate reads, never a claim about this repository. Every cell that is not a number is a cell's own answer, not a gap. The most-marked rooms and the rooms each pair of diagnostic features shares follow the table.*"
        + NL
        + NL
        + "| feature | profile | position | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate; caveat or reason |"
        + NL
        + "|---|---|---|---|---|---|---|---|"
        + NL
    )
    return head + NL.join(rows) + NL + render_most_marked(facts_doc) + render_shared(facts_doc)


def qualified_labels(keys: list[str]) -> dict[str, str]:
    """D-050: the label a feature key prints under — the bare feature name, or profile/feature
    when the name is under two profiles, in every place a feature is named."""
    names = [k.split("/")[-1] for k in keys]
    return {k: (n if names.count(n) == 1 else k) for k, n in zip(keys, names)}


def render_most_marked(facts_doc: dict[str, Any]) -> str:
    """D-049: the rooms carrying the most, with the count of rooms at that most so a capped list is
    not a claim of completeness. D-050: the count is distinct sets. D-052: what the lead said of
    "a row below that count" was true of the list and false as a label on the second row of a
    tier; the cell now says it — "3 of 4" is three rows listed of four rooms at this count, the
    first by path — and the lead says only the ordering and the cap."""
    top = facts_doc.get("most_marked_rooms") or []
    if not top:
        return NL + "### Most-marked rooms" + NL + NL + "*No room carries two distinct diagnostic sets.*" + NL
    most = top[0].get("sets", top[0]["marks"])
    at = facts_doc.get("rooms_at_most_sets", top[0].get("rooms_at_this_count", len(top)))
    lead = (
        f"*Rooms under two or more distinct diagnostic sets, {MOST_MARKED_ORDER}; at most {MOST_MARKED_ROOMS} are listed. "
        f"{at} room{'s' if at != 1 else ''} carr{'y' if at != 1 else 'ies'} the most ({most}). "
        "The listed column is rows listed of rooms at the row's sets count; where fewer are listed than carry the count, the listed are the first by path.*"
    )
    body = NL.join(
        f"| {m['room']} | {m.get('sets', m['marks'])} | {m['marks']} | {m.get('listed_at_this_count', '')} of {m.get('rooms_at_this_count', '')} | {', '.join(m['features'])} |"
        for m in top
    )
    return (
        NL + "### Most-marked rooms" + NL + NL + lead + NL + NL
        + "| room | distinct sets | marks | listed of rooms at this count | diagnostic features that mark it |" + NL + "|---|---|---|---|---|" + NL + body + NL
    )


def render_shared(facts_doc: dict[str, Any]) -> str:
    """D-049: rooms each pair of diagnostic features shares, as a matrix; the diagonal is the
    feature's own count. Identity and containment are the relation column's; this is the rest."""
    pairs = facts_doc.get("shared_rooms") or []
    keys = sorted({k for sr in pairs for k in (sr["a"], sr["b"])})
    if not keys:
        return ""
    counts = {f"{f['profile']}/{f['feature']}": f["count"] for f in facts_doc["features"]}
    cell = {(sr["a"], sr["b"]): sr["shared"] for sr in pairs}
    cell.update({(b, a): n for (a, b), n in list(cell.items())})
    _label = qualified_labels(keys)
    labels = [_label[k] for k in keys]
    head = "| shared rooms | " + " | ".join(labels) + " |" + NL + "|---|" + "---|" * len(keys) + NL
    rows = NL.join(
        f"| {labels[i]} | "
        + " | ".join(
            f"**{counts.get(a, 0)}**" if a == b else str(cell.get((a, b), 0)) for b in keys
        )
        + " |"
        for i, a in enumerate(keys)
    )
    return (
        NL + "### Shared rooms" + NL + NL
        + "*Rooms both features mark, for every pair of diagnostic features (a feature under two profiles is two rows); the diagonal is the feature's own count. A shared count equal to the smaller of the two features' own counts is containment, and equal to both is identity; the relation column above draws those, and only between features with " + str(RELATION_MIN_ROOMS) + " or more rooms or where the predicates guarantee the containment — any other pair under that floor is read here and not there.*"
        + NL + NL + head + rows + NL
    )


def render_disclosure(facts_doc: dict[str, Any]) -> str:
    """D-049: the decorative disclosure, rendered from decorative_reason — the prompt's canonical
    sentence, now a fixed text tested against the fields it reads."""
    dec = [f for f in facts_doc["features"] if f["decorative"]]
    n = facts_doc["decorative"]["count"]
    if not dec:
        return "No decorative marks: every feature that fired rests on an asserted signal."
    sigs = sorted({w for f in dec for w in re.findall(r"[a-z_]+_index", f.get("decorative_reason") or "")})
    names = " and ".join(
        f"{f['feature']}" + (f" — {f['position_name']} —" if f.get("position_name") else "") for f in dec
    )
    # D-054: the signal's reason is on the signal and is said here once, the same words every row
    # that reads the signal carries — the tuning fact was on the 1-room row and not the 48-room one
    reasons: dict[str, str] = {}
    for f in dec:
        reasons.update(f.get("decorative_signal_reasons") or {})
    if len(sigs) == 1 and sigs[0] in reasons:
        which = f"which is {reasons[sigs[0]].rstrip('.')}."
    elif any(sg in reasons for sg in sigs):
        which = "which are unvalidated: " + "; ".join(f"{sg} is {reasons[sg].rstrip('.')}" for sg in sigs if sg in reasons) + "."
    else:
        which = "which is unvalidated."
    return (
        f"{n} decorative mark{'s' if n != 1 else ''} render but are not a diagnosis: {names} rest on "
        f"{', '.join(sigs) or 'nothing confirmed'}, {which}"
    )


def render_brief(
    text: str | None,
    facts_doc: dict[str, Any],
    violations: list[Violation],
    provenance: dict[str, Any],
) -> str:
    """D-049: header → register (with the most-marked rooms and the shared-rooms matrix) →
    decorative disclosure → stance → provenance, all rendered by code. A hand-written draft, if
    given, is appended as the reading with its lint section; nothing else on the page is prose."""
    draft = text is not None and text.strip() != ""
    fp = (facts_doc.get("gate_fingerprint") or "?")[:12]
    where = (
        f"Profile {facts_doc['profile']}"
        + (f" + {', '.join(facts_doc['overlays'])}" if facts_doc["overlays"] else "")
        + f", geometry {facts_doc['geometry']}, skeleton `{facts_doc['skeleton_hash'][:12]}…`, facts `{facts_doc['facts_hash'][:12]}…`. "
        f"Calibration: {facts_doc.get('calibration', 'in-repo, self-relative')} — the time-lapse for this skeleton is the one under gate `{fp}`. "
        f"Brief {facts_doc.get('brief_version', BRIEF_VERSION)}."
    )
    if draft:
        status = (
            "PASS"
            if not violations
            else f"FAILED ({len(violations)} violation{'s' if len(violations) != 1 else ''})"
        )
        head = (
            f"# {facts_doc['repo']['name']} — architect's brief\n\n"
            f"*The register below is rendered from the facts sheet by code; the reading beneath it is a hand-written draft, linted. "
            f"Register lint: **{status}**. What the lint checked: "
            + "; ".join(f"{rid} {desc}" for rid, desc in RULES)
            + ". What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. "
            + where
            + " A PASS is a pass under that grammar (D-035).*\n\n"
        )
    else:
        head = (
            f"# {facts_doc['repo']['name']} — architect's brief\n\n"
            f"*Rendered from the facts sheet by code; no model wrote any of it. The model-written reading was cut at D-049 after eleven hostile seatings found it reciting the register and everything it could add was a field. "
            f"Every cell is a field, and every fixed text on the page is tested against the computation it labels (`tests/test_brief.py`). "
            + where
            + "*\n\n"
        )
    prov = (
        "\n## Provenance\n\n"
        + "\n".join(f"- {k}: `{v}`" for k, v in sorted(provenance.items()) if v is not None)
        + "\n"
    )
    page = (
        head
        + render_register(facts_doc)
        + "\n## Decorative marks\n\n"
        + render_disclosure(facts_doc)
        + "\n\n## Stance\n\n"
        + facts_doc.get("stance", STANCE)
        + "\n"
    )
    if draft:
        page += "\n## Reading (draft)\n\n" + (text or "").strip() + "\n"
    page += prov
    if draft:
        lint_md = "\n## Register lint\n\n"
        if violations:
            lint_md += (
                "| rule | paragraph | detail | text |\n|---|---|---|---|\n"
                + "\n".join(
                    f"| {v.rule} | {v.paragraph} | {v.detail.replace('|', '/')} | {v.text.replace('|', '/')} |"
                    for v in violations
                )
                + "\n\n**This draft failed the register lint and is not a diagnosis until it passes.**\n"
            )
        else:
            lint_md += (
                "No violations. Rules: "
                + ", ".join(f"{rid} {desc}" for rid, desc in RULES)
                + " (each rule is dated in DECISIONS.md).\n"
            )
        page += lint_md
    return page


def relint(
    markdown: str, skeleton: dict[str, Any], substrate: dict[str, Any] | None
) -> dict[str, Any]:
    """Re-judge the reading of an existing brief.md under the current lint, keeping its provenance.
    A page from before D-049 carries its reading under "## Reading"; a page since carries a draft
    under "## Reading (draft)" or no reading at all."""
    m = re.search(r"\n## Reading(?: \(draft\))?\n(.*?)(?=\n## |\Z)", markdown, re.DOTALL)
    prose = m.group(1).strip() if m else ""
    prov: dict[str, Any] = {}
    pm = re.search(r"## Provenance\n(.*?)(?:\n## |\Z)", markdown, re.DOTALL)
    if pm:
        for line in pm.group(1).splitlines():
            mm = re.match(r"- ([^:]+): `(.*)`", line.strip())
            if mm:
                prov[mm.group(1)] = mm.group(2)
    f = facts(skeleton, substrate)
    viols = lint(prose, f, register=True) if prose else []
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
    draft: str | None = None,
) -> dict[str, Any]:
    """Facts → rendered brief (D-049: by code, no model). A hand-written draft, if given, is
    linted and appended as the reading. Returns a dict with `facts`, `text`, `violations`,
    `provenance`, `markdown`, `passed`."""
    f = facts(skeleton, substrate)
    if draft is not None:
        text, prov = draft, {"generator": "draft", "facts_hash": f["facts_hash"], "brief_version": BRIEF_VERSION}
        viols = lint(text, f, register=True)
    else:
        text, prov, viols = None, {"generator": "code", "facts_hash": f["facts_hash"], "brief_version": BRIEF_VERSION}, []
    return {
        "facts": f,
        "text": text or "",
        "violations": [v.as_dict() for v in viols],
        "provenance": prov,
        "markdown": render_brief(text, f, viols, prov),
        "passed": not viols,
    }
