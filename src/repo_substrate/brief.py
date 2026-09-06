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

BRIEF_VERSION = "0.1.0"
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
        "diagnostic_count": s["diagnostic_count"],
        "decorative": {
            "count": s["decorative_count"],
            "features": sorted(s.get("decorative_features") or []),
        },
        "co_located_count": s.get("co_located_count", 0),
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
# [feature: a, b] · [feature ×N] · [feature ×N: a, b] — the count and the rooms are each checked
CITATION = re.compile(r"\[([a-z_]+(?:/[a-z_]+)?)(?:\s*×\s*(\d+))?(?::\s*([^\]]+?))?\]")
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
    allowed_numbers.add(facts_doc["decorative"]["count"])
    allowed_numbers.add(facts_doc["co_located_count"])
    allowed_numbers.update(facts_doc["wings"].values())
    for f in facts_doc["features"]:
        allowed_numbers.add(f["count"])
    for r in facts_doc.get("rooms", {}).values():
        for v in r.values():
            if isinstance(v, int):
                allowed_numbers.add(v)
    used_consequence_names: set[str] = set()
    stance_key = facts_doc["stance"][:40].lower()
    for i, para in enumerate(_paragraphs(text), 1):
        if para.startswith(("#", "*Register lint")):
            continue
        low_para = para.lower()
        is_stance = stance_key in low_para or "presupposes a norm of health" in low_para
        is_disclosure = "decorative" in low_para and (
            "not a diagnosis" in low_para or "no diagnosis" in low_para
        )
        # R1 consequence vocabulary, per sentence, unless the sentence is a disclosure
        for sent in SENTENCE.split(para):
            low = sent.lower()
            if "denotes position" in low or "position, not" in low or "not a claim" in low:
                continue
            hits = sorted(w for w in CONSEQUENCE_WORDS if re.search(rf"\b{re.escape(w)}\b", low))
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
            labels = sorted(w for w in BUILDING_LABELS if re.search(rf"\b{re.escape(w)}\b", low))
            if labels:
                out.append(
                    Violation(
                        "R6-archetype",
                        i,
                        sent[:160],
                        f"whole-building label: {', '.join(labels)} (D-019)",
                    )
                )
        # R2 provenance: citations resolve; every paragraph carries at least one
        cites = []
        for m in CITATION.finditer(para):
            name, count, room = m.group(1), m.group(2), m.group(3)
            if room and ";" in room:
                # [foundation: x; hub: x; dark_room: x] — several clauses in one bracket
                first, *rest = [c.strip() for c in room.split(";")]
                cites.append((name, count, first))
                for clause in rest:
                    cm = re.match(r"([a-z_]+(?:/[a-z_]+)?)\s*(?:×\s*(\d+))?\s*:?\s*(.*)", clause)
                    if cm:
                        cites.append((cm.group(1), cm.group(2), cm.group(3).strip()))
            else:
                cites.append((name, count, room))
        if not cites and not (is_stance or is_disclosure):
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
            if f["decorative"] and not is_disclosure:
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
        # R3 numbers
        for n in INTEGER.findall(re.sub(CITATION, "", para)):
            if int(n) not in allowed_numbers:
                out.append(
                    Violation("R3-number", i, para[:160], f"number {n} is not in the facts sheet")
                )
    # R5 disclosure: a consequence-implying name used anywhere in the brief must carry its position name
    low_all = text.lower()
    for f in facts_doc["features"]:
        if f["name_implies_consequence"] and re.search(rf"\b{re.escape(f['feature'])}\b", low_all):
            used_consequence_names.add(f["feature"])
    for feat in sorted(used_consequence_names):
        pos = (by_feature[feat].get("position_name") or "").lower()
        # tolerate plurals and hyphen/space variation: "high-load hub" ~ "high load hubs"
        words = [re.escape(w) for w in re.split(r"[\s-]+", pos) if w]
        pattern = r"[\s-]+".join(w + r"(?:s|es)?" for w in words) if words else None
        if pattern and not re.search(pattern, low_all):
            out.append(
                Violation(
                    "R5-disclosure",
                    0,
                    feat,
                    f"'{feat}' is used but its position name ('{pos}') is not disclosed (D-004 Q3)",
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
    stated = str(dec_count) in text or any(re.search(rf"\b{w}\b", low_all) for w in dec_words)
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
- Every paragraph cites its evidence in brackets, where the bracket opens with the feature's own name from the facts sheet: [hub: src/db/connection.ts] for one room, [hub: src/a.ts, src/b.ts] for several, [hub ×27] for a count (×27 must equal that feature's count in the facts sheet). Never write the word "feature" inside a bracket; write the feature's name (foundation, hub, dark_room, scaffolding, corridor, …). A paragraph with no citation is struck.
- Use only numbers that appear in the facts sheet (counts, lines, fan-in, fan-out). No estimates, no percentages.
- Decorative features rest on nothing confirmed. Do not use them in any diagnosis. State the decorative count once, plainly, e.g. "27 decorative marks (crack) render but are not a diagnosis."
- A feature whose name implies a consequence (foundation, toothpick_wing, crack) must be disclosed with its position name from the facts sheet, e.g. "foundation — a high-load hub, a position in the import graph, not a claim about what breaks".
- Do not give the building a one-word label (cathedral, shantytown, bunker, ruin). No archetype exists.
- Do not invent rooms, wings, or features. Do not describe code you have not been given; the facts sheet is the whole building.

Form: 300–600 words of plain prose in short paragraphs; no headings, no bullet lists; the surveyor's voice — exact, unimpressed, specific. Begin with the building's shape (wings and rooms), then the features by where they sit, then the decorative disclosure, then the stance sentence given in the facts sheet, verbatim or near it."""


def _user_message(facts_doc: dict[str, Any], violations: list[Violation] | None = None) -> str:
    slim = {k: v for k, v in facts_doc.items() if k != "rooms"}
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
    head = (
        f"# {facts_doc['repo']['name']} — architect's brief\n\n"
        f"*Register lint: **{status}**. Every claim below is licensed by an `asserted` signal and cites the feature and room it rests on; "
        f"a claim voices a present structural position, never a consequence. Profile {facts_doc['profile']}"
        + (f" + {', '.join(facts_doc['overlays'])}" if facts_doc["overlays"] else "")
        + f", geometry {facts_doc['geometry']}, skeleton `{facts_doc['skeleton_hash'][:12]}…`, facts `{facts_doc['facts_hash'][:12]}…`.*\n\n"
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
        lint_md += "No violations. Rules: R1 consequence vocabulary, R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features excluded from diagnosis, R5 position-name disclosure, R6 no whole-building label, R7 decorative count stated.\n"
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
        for attempt in range(1, max_attempts + 1):
            text, prov = generate(SYSTEM, _user_message(f, viols if attempt > 1 else None))
            viols = lint(text, f)
            prov = {
                **prov,
                "attempt": attempt,
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
