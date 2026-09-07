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

BRIEF_VERSION = "0.5.0"
MAX_ATTEMPTS_CAP = 3  # D-030: regeneration is bounded and every attempt's refusals are on the page
DEFAULT_MODEL = "claude-opus-5"

# ---------------------------------------------------------------- 1. the facts sheet

STANCE = (
    "The building is drawn as it is, warts and all. The diagnosis presupposes a norm of "
    "health — load should be reinforced, old load-bearing code should be visited — and that "
    "norm is a maintenance stance the reader may reject, "
    "stated so it reads as an ought, not a fact (system spec, stance disclosure)."
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
        # D-038: the directory's population is the denominator the share needs — on a monorepo
        # one directory can be two thirds of the building, and a share without it is the base rate
        pop = sum(
            1
            for nid in skeleton["strata"]["by_node"]
            if (nid.rsplit("/", 1)[0] if "/" in nid else "(root)") == top[0]
        )
        e["dominant_dir"] = {"dir": top[0], "n": top[1], "population": pop}
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
    diag = [
        (k, set(e["rooms"])) for k, e in sorted(feats.items()) if e["diagnostic"] and e["rooms"]
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
                    {
                        "a": ka,
                        "b": kb,
                        "relation": "identical",
                        "n": len(ra),
                        "inert_terms": inert,
                        # D-038: the same predicate under two profiles is one measurement, not two agreeing
                        "shared_predicate": not inert,
                    }
                )
            elif ra < rb:
                overlaps.append(
                    {
                        "a": ka,
                        "b": kb,
                        "relation": "within",
                        "n": len(ra),
                        "n_outside": len(rb - ra),
                    }
                )
            elif rb < ra:
                overlaps.append(
                    {
                        "a": kb,
                        "b": ka,
                        "relation": "within",
                        "n": len(rb),
                        "n_outside": len(ra - rb),
                    }
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
        # D-037: every building-level number carries its unit; a count of rooms is not a count of marks
        "units": {
            "population": "rooms",
            "wings": "rooms",
            "diagnostic_count": "marks",
            "diagnostic_count_base": "marks",
            "decorative.count": "marks",
            "co_located_rooms": "rooms carrying two or more diagnostic marks, across all profiles",
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
NEGATED_DIAGNOSIS = re.compile(r"\b(?:not|no|nothing|never|neither|nor)\b[^.;]{0,60}\bdiagnos")
# D-036: distributional words the sheet cannot carry (it carries counts per wing instead)
DISTRIBUTION = re.compile(
    r"\b(?:mostly|most of|largely|predominantly|mainly|chiefly|concentrated in|the bulk|"
    r"spread across|scattered|throughout|every wing|all wings|all of the wings|reaches into every)\b"
)
# D-037: comparatives and superlatives set one mark against another; the register forbids it
COMPARISON = re.compile(
    r"\b(?:widest|largest|biggest|broadest|narrowest|smallest|fewest|greatest|"
    r"wider than|larger than|bigger than|smaller than|fewer than|more than any|the most \w+ set)\b"
)
# D-037: a number followed by its unit noun ("160 of those marks", "70 rooms")
UNIT_USE = re.compile(
    r"\b(\d{1,7}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+"
    r"(?:of\s+(?:those|these|the|its|the\s+\w+)\s+)?(rooms?|marks?|findings?|features?)\b",
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


SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\[])")


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


def lint(text: str, facts_doc: dict[str, Any]) -> list[Violation]:
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
            low_sent = BRACKET.sub("", sent).lower().replace("across all profiles", "")
            for m in DISTRIBUTION.finditer(low_sent):
                out.append(
                    Violation(
                        "R11-share",
                        i,
                        sent[:160],
                        f"'{m.group(0)}' asserts a share the sheet does not carry; state the count per wing (by_wing)",
                    )
                )
            for m in COMPARISON.finditer(low_sent):
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
            for ov in facts_doc.get("overlaps") or []:
                oa, ob = ov["a"].split("/")[-1], ov["b"].split("/")[-1]
                if re.search(rf"\b{re.escape(oa)}\b", sent) and re.search(
                    rf"\b{re.escape(ob)}\b", sent
                ):
                    sent_allowed |= {ov["n"], ov.get("n_outside", ov["n"])}
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
        fa, fb = ov["a"].split("/")[-1], ov["b"].split("/")[-1]
        together = any(
            re.search(rf"\b{re.escape(fa)}\b", snt) and re.search(rf"\b{re.escape(fb)}\b", snt)
            for snt in sentences_all
        )
        if not together:
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
            if any(IDENTITY_NOUN.search(snt.lower()) for snt in pair_sents) or not any(
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
            if not any(re.search(r"\bpredicate\b", snt.lower()) for snt in pair_sents):
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
            if not said:
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
        if not f["diagnostic"] or not dd or f["count"] < 6 or dd["n"] * 3 < f["count"]:
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
        if not f["decorative"]:
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
    # R7 decorative count must be stated when there are decorative features
    dec_count = facts_doc["decorative"]["count"]
    prose_only = BRACKET.sub("", text)
    in_prose = {int(d) for d in INTEGER.findall(prose_only)} | {
        v for _, v in _spelled_numbers(prose_only)
    }
    stated = dec_count in in_prose
    diag = facts_doc["diagnostic_count"]
    if diag not in in_prose:
        out.append(
            Violation(
                "R7-counts",
                0,
                "",
                f"the brief must state the diagnostic-mark count ({diag}, all profiles) beside the population",
            )
        )
    if dec_count and not stated:
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

SYSTEM = """You are a condemnation surveyor writing the architect's brief for a building that is a codebase. The building is drawn from a skeleton of named structural features; you have the facts sheet and nothing else. You describe what is; you do not sell, soften, or forecast.

Register, binding (validation-spec §2.1.1, mapper §3):
- Present tense only. Every feature rests on a signal that describes a present structural position. You may say where a room sits and what fires on it. You may not say what will happen, what breaks, what is at risk, what is fragile, what will ripple, what a change would cause. Those are predictions; none is licensed here. Avoid the words: break, will, would, risk, fragile, brittle, dangerous, ripple, cascade, fail, failure, likely, predict, expect, cause, collapse, vulnerable, exposed, threat, prone, future, soon, eventually, impact, consequence, propagate, bug, defect, safe, unsafe, critical.
- Every paragraph cites its evidence in brackets, where the bracket opens with the feature's own name from the facts sheet: [hub: src/db/connection.ts] for one room, [hub: src/a.ts, src/b.ts] for several, [hub ×27] for a count (×27 must equal that feature's count in the facts sheet). Several counts share one bracket separated by semicolons: [foundation ×21; onboarding/foundation ×21]. To name example rooms under a count, put them in the same bracket in the same sentence: [foundation ×21: src/a.ts, src/b.ts] — a room named in a later sentence needs its own bracket there. Never write the word "feature" inside a bracket; write the feature's name (foundation, hub, dark_room, scaffolding, corridor, …). A paragraph with no citation is struck.
- A room you name in a sentence must be covered by a feature you cite in that same sentence, and that feature must have fired on that room. Never name a room under a feature that did not fire on it.
- State the population, the diagnostic-mark count (all profiles), and the co-located count together, early.
- Name rooms; do not say what they do. A path is not a function: "src/error/QueryFailedError.ts" is a room, not "the error classes". Describe position and marks, not purpose.
- Do not set two features against each other ("against that", "offsets", "compensates"): the sets are independent measurements and the brief does not know their intersection unless the facts sheet states it.
- Disclose a consequence-implying name's position name in the same paragraph where the name first appears; the disclosure clause covers only itself, not the rest of the sentence.
- If the facts sheet lists `overlaps`, say so in one sentence naming both features: "The 70 flooded_basement rooms are the same 70 rooms as dark_room" — two marks on one set of rooms are one finding, not two.
- Never use "mostly", "concentrated", "the bulk", "spread across", "throughout", "every wing"; the sheet carries `by_wing` counts per feature — state those ("39 of the 70 sit in src, 31 in packages") in the sentence that cites the feature.
- A directory you name must contain a room you cite in the same sentence. A count you state must be the count (or a by_wing count) of a feature you cite in the same sentence, or a building-level count.
- Every number on the sheet has a unit (`units`): a count of rooms is never "N marks". `co_located_rooms` counts rooms carrying two or more marks.
- When `overlaps` lists `inert_terms`, say that the extra conjunct excludes nothing here, naming its signal: "flooded_basement adds load_index >= 0.10 to dark_room and it excludes nothing on this repository: the 70 rooms are the same 70".
- Each feature carries `dominant_dir`: when a third or more of its rooms sit in one directory, name that directory in the sentence that cites the feature, and cite a room from it — the sample must show the set's composition, not flatter it.
- Never rank marks against each other ("the widest set", "larger than"); a p90 set has its size by construction. Never write "validated": no signal in this gate holds that status; every feature rests on an asserted signal.
- An overlap with `relation: within` is a nesting, not an identity: name both features, state the `n_outside` rooms the extra conjunct removed, and never call them one set or one finding. An identical overlap with `shared_predicate: true` is the same predicate under two profiles — say "the same predicate", never that two profiles agree.
- When you name a feature's `dominant_dir`, state its `population` too ("98 of the 148 sit in lib/rules, which holds 305 of the building's 473 rooms") — a share without its denominator is a base rate.
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

Form: 300–600 words of plain prose in short paragraphs; no headings, no bullet lists; the surveyor's voice — exact, unimpressed, specific. Begin with the building's shape (wings and rooms), then the features by where they sit, then the decorative disclosure, then the stance sentence given in the facts sheet, verbatim or near it."""


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
        f"*Register lint: **{status}**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; "
        f"a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; "
        f"numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. "
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
        lint_md += "No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038).\n"
    return head + text.strip() + "\n" + prov + lint_md


def relint(
    markdown: str, skeleton: dict[str, Any], substrate: dict[str, Any] | None
) -> dict[str, Any]:
    """Re-judge an existing brief.md under the current lint, keeping its prose and provenance."""
    body = markdown.split("\n## Provenance", 1)[0]
    paras = [p for p in re.split(r"\n\s*\n", body) if p.strip()]
    prose = "\n\n".join(
        p for p in paras if not p.startswith("#") and not p.startswith("*Register lint")
    )
    prov: dict[str, Any] = {}
    m = re.search(r"## Provenance\n(.*?)(?:\n## |\Z)", markdown, re.DOTALL)
    if m:
        for line in m.group(1).splitlines():
            mm = re.match(r"- ([^:]+): `(.*)`", line.strip())
            if mm:
                prov[mm.group(1)] = mm.group(2)
    f = facts(skeleton, substrate)
    viols = lint(prose, f)
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
        viols = lint(text, f)
    else:
        if generate is None:
            raise ValueError("no generator and no draft")
        viols: list[Violation] = []
        text, prov = "", {}
        attempts_log: list[dict[str, Any]] = []
        for attempt in range(1, min(max_attempts, MAX_ATTEMPTS_CAP) + 1):
            text, prov = generate(SYSTEM, _user_message(f, viols if attempt > 1 else None))
            viols = lint(text, f)
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
