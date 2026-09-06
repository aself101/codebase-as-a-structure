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

BRIEF_VERSION = "0.2.1"
MAX_ATTEMPTS_CAP = 3  # D-030: regeneration is bounded and every attempt's refusals are on the page
DEFAULT_MODEL = "claude-opus-5"

# ---------------------------------------------------------------- 1. the facts sheet

STANCE = (
    "The building is drawn as it is, warts and all. The diagnosis presupposes a norm of "
    "health — load should be reinforced, old load-bearing code should be visited, fixes "
    "should not concentrate — and that norm is a maintenance stance the reader may reject, "
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
    for e in feats.values():
        e["rooms"] = sorted(set(e["rooms"]))
        e["count"] = len(e["rooms"])
    wings: dict[str, int] = {}
    depth = int((skeleton.get("geometry") or {}).get("wing_depth", 1))
    for nid in skeleton["strata"]["by_node"]:
        parts = nid.split("/")
        w = "/".join(parts[:depth]) if len(parts) > depth else "(root)"
        wings[w] = wings.get(w, 0) + 1
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
        "gate": dict(sorted(skeleton["gate"]["signals"].items())),
        "diagnostic_count": sum(e["count"] for e in feats.values() if e["diagnostic"]),
        "diagnostic_count_base": s["diagnostic_count"],
        "decorative": {
            "count": s["decorative_count"],
            "features": sorted(s.get("decorative_features") or []),
        },
        "co_located_count": s.get("co_located_count", 0),
        "calibration": "in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page",
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
    r"not a claim about what (breaks|happens|fails|follows)[^.;,]*",
    r"(denotes|names|is) (a )?position[^.;,]*",
    r"a position in the import graph[^.;,]*",
    r"position, not [^.;,]*",
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
        [
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
            "eleven",
            "twelve",
            "thirteen",
            "fourteen",
            "fifteen",
            "sixteen",
            "seventeen",
            "eighteen",
            "nineteen",
            "twenty",
        ]
    )
}
WORD_NUMBERS.update(
    {
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90,
        "hundred": 100,
    }
)
WORD_NUMBER = re.compile(
    r"\b(" + "|".join(WORD_NUMBERS) + r")(?:-(one|two|three|four|five|six|seven|eight|nine))?\b",
    re.IGNORECASE,
)
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
    allowed_numbers.add(facts_doc["co_located_count"])
    allowed_numbers.update(facts_doc["wings"].values())
    for f in facts_doc["features"]:
        allowed_numbers.add(f["count"])
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
            if named:
                covered: set[str] = set()
                for cname, _c, _r in _citations(sent):
                    cf = by_key.get(cname) or by_feature.get(cname)
                    if cf:
                        covered.update(cf["rooms"])
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
            cite_sentences = [
                sent
                for sent in SENTENCE.split(para)
                if re.search(r"\[" + re.escape(name) + r"\b", sent)
            ]
            disclosed_here = any(
                "decorative" in sent.lower()
                and ("not a diagnosis" in sent.lower() or "no diagnosis" in sent.lower())
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
        stripped = BRACKET.sub("", para)
        para_allowed = set(allowed_numbers)
        for rid in room_ids:
            if rid in room_metrics and _mentions(para, rid):
                para_allowed.update(v for v in room_metrics[rid].values() if isinstance(v, int))
        for n in INTEGER.findall(stripped):
            if int(n) not in para_allowed:
                out.append(
                    Violation("R3-number", i, para[:160], f"number {n} is not in the facts sheet")
                )
        for m in WORD_NUMBER.finditer(stripped):
            if m.group(0).lower() == "one":
                continue  # the determiner, not a measurement (D-032 addendum)
            val = WORD_NUMBERS[m.group(1).lower()] + (
                WORD_NUMBERS[m.group(2).lower()] if m.group(2) else 0
            )
            if val not in para_allowed:
                out.append(
                    Violation(
                        "R3-number",
                        i,
                        para[:160],
                        f"number '{m.group(0)}' ({val}) is not in the facts sheet",
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
    dec_words = {w for w, v in WORD_NUMBERS.items() if v == dec_count} | {
        f"{tens}-{ones}"
        for tens, tv in WORD_NUMBERS.items()
        for ones, ov in WORD_NUMBERS.items()
        if tv >= 20 and 0 < ov < 10 and tv + ov == dec_count
    }
    prose_only = BRACKET.sub("", text)
    low_prose = prose_only.lower()
    stated = str(dec_count) in prose_only or any(
        re.search(rf"\b{w}\b", low_prose) for w in dec_words
    )
    diag = facts_doc["diagnostic_count"]
    if str(diag) not in prose_only:
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
        f"numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. "
        f"What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile {facts_doc['profile']}"
        + (f" + {', '.join(facts_doc['overlays'])}" if facts_doc["overlays"] else "")
        + f", geometry {facts_doc['geometry']}, skeleton `{facts_doc['skeleton_hash'][:12]}…`, facts `{facts_doc['facts_hash'][:12]}…`. "
        f"Calibration: {facts_doc.get('calibration', 'in-repo, self-relative')}.*\n\n"
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
        lint_md += "No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations.\n"
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
