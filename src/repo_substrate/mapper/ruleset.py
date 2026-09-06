"""Ruleset loading and validation (structural-mapper-spec §3, §4, §5.5 of the system spec).

A ruleset is a versioned TOML document: a `[ruleset]` header and `[[feature]]` entries,
each with a predicate over substrate signals. Predicate grammar (deliberately small):

    term ( and term )*
    term := <signal> <op> <value>
    op   := >= | <= | > | < | ==
    value := pNN            -- the NN-th percentile of that signal across the population
           | <float>        -- an absolute threshold on the signal's own scale

A signal name denotes an index (by its index name) or else the RAW metric — `fan_out == 0`
means no in-repo imports — never the percentile of a raw metric; `pNN` ranks the raw values.
Names that exist only as percentiles (`fan_in_nonzero`) resolve to those. Why (D-017 addendum):
an ECDF percentile is never 0, so on the first layer-geometry render `entrance` (`fan_out == 0`)
never fired while the name resolved to a percentile; the raw metric is the only thing `== 0` can
be true of. `pNN` is ranked over the mapped repository's own population (in-repo, self-relative,
D-019): a top decile exists in every repository.

`and` may also be written `∧`. There is no `or` and no `not`: a feature is a conjunction,
and a different feature is a different conjunction.
"""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

_TERM = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*(>=|<=|==|>|<)\s*(p(\d{1,2})|\d*\.?\d+)\s*$")
_SPLIT = re.compile(r"\s+(?:and|∧)\s+")


# Words in a FEATURE NAME that carry a consequence or damage (D-004 Q3, D-028, D-030): a name
# containing one must be declared name_implies_consequence and carry a position_name. The
# list is the audit surface; a new metaphor that implies damage is added here.
NAME_CONSEQUENCE_WORDS = (
    "scaffold",  # temporary structure erected to be removed (D-035; written D-038)
    "crack",
    "flood",
    "toothpick",
    "rot",
    "decay",
    "collapse",
    "broken",
    "fragile",
    "danger",
    "dark",
    "neglect",
    "abandon",
    "dead",
    "leak",
    "fire",
    "ruin",
)


class RulesetError(ValueError):
    pass


@dataclass(frozen=True)
class Term:
    signal: str
    op: str
    percentile: int | None  # pNN
    value: float | None  # absolute

    def render(self) -> str:
        v = f"p{self.percentile}" if self.percentile is not None else f"{self.value:g}"
        return f"{self.signal} {self.op} {v}"


@dataclass(frozen=True)
class Feature:
    name: str
    predicate: str
    terms: tuple[Term, ...]
    decorative: bool = False
    decorative_reason: str | None = None
    graph_dependent: bool = False
    name_implies_consequence: bool = False
    position_name: str | None = None  # the position-denoting alternative name (D-004 Q3)
    note: str = ""

    @property
    def signals(self) -> tuple[str, ...]:
        return tuple(sorted({t.signal for t in self.terms}))


@dataclass(frozen=True)
class Ruleset:
    name: str
    version: str
    profile: str
    description: str
    features: tuple[Feature, ...]
    source: str = ""
    wing_depth: int = (
        1  # directory depth that defines a wing (geometry; the same for every profile)
    )
    _extra: dict = field(default_factory=dict, compare=False)


def parse_predicate(text: str) -> tuple[Term, ...]:
    parts = _SPLIT.split(text.strip())
    terms: list[Term] = []
    for part in parts:
        m = _TERM.match(part)
        if not m:
            raise RulesetError(f"cannot parse predicate term {part!r} in {text!r}")
        sig, op, raw, pct = m.group(1), m.group(2), m.group(3), m.group(4)
        if pct is not None:
            p = int(pct)
            if not 0 <= p <= 100:
                raise RulesetError(f"percentile out of range in {part!r}")
            terms.append(Term(sig, op, p, None))
        else:
            terms.append(Term(sig, op, None, float(raw)))
    return tuple(terms)


def load_ruleset(path: Path) -> Ruleset:
    raw = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    # D-019: a ruleset names per-node features and nothing else. An `[archetype]` table (or
    # any other whole-repo claim) has no reader here and must not ride along silently.
    unknown = sorted(set(raw) - {"ruleset", "feature"})
    if unknown:
        raise RulesetError(
            f"unknown top-level table(s) {unknown}; a ruleset carries [ruleset] and [[feature]] only"
        )
    hdr = raw.get("ruleset") or {}
    for key in ("name", "version", "profile"):
        if not hdr.get(key):
            raise RulesetError(f"[ruleset] missing {key}")
    feats: list[Feature] = []
    seen: set[str] = set()
    for f in raw.get("feature") or []:
        name = f.get("name")
        if not name or name in seen:
            raise RulesetError(f"feature name missing or duplicated: {name!r}")
        seen.add(name)
        pred = f.get("predicate")
        if not pred:
            raise RulesetError(f"feature {name}: missing predicate")
        decorative = bool(f.get("decorative", False))
        reason = f.get("decorative_reason")
        # mapper §3 (D-004): the hatch is audited — a decorative rule must say why.
        if decorative and not reason:
            raise RulesetError(f"feature {name}: decorative = true requires decorative_reason")
        terms_ = parse_predicate(pred)
        if decorative and reason and not any(t.signal in str(reason) for t in terms_):
            # mapper §3: the reason must NAME the ungrounded signal; a non-empty string is not a reason (D-030)
            raise RulesetError(
                f"feature {name}: decorative_reason must name the ungrounded signal(s) it excuses ({', '.join(sorted({t.signal for t in terms_}))})"
            )
        implied = any(w in str(name).lower() for w in NAME_CONSEQUENCE_WORDS)
        if implied and not bool(f.get("name_implies_consequence", False)):
            raise RulesetError(
                f"feature {name}: the name carries a consequence word ({', '.join(w for w in NAME_CONSEQUENCE_WORDS if w in str(name).lower())}); declare name_implies_consequence = true with a position_name (D-030)"
            )
        if not decorative and reason:
            raise RulesetError(f"feature {name}: decorative_reason given but decorative = false")
        # D-004 Q3 / D-024: the register hook has a grammar. A name that implies a consequence
        # must say what position it denotes, in words that are not the name.
        implies = bool(f.get("name_implies_consequence", False))
        pos = f.get("position_name")
        if implies and not pos:
            raise RulesetError(
                f"feature {name}: name_implies_consequence = true requires a position_name"
            )
        if pos is not None and str(pos).strip().lower() == str(name).replace("_", " ").lower():
            raise RulesetError(
                f"feature {name}: position_name repeats the feature name and discloses nothing"
            )
        try:
            wing_depth_ok = int(hdr.get("wing_depth", 1)) >= 1
        except (TypeError, ValueError):
            wing_depth_ok = False
        if not wing_depth_ok:
            raise RulesetError("[ruleset] wing_depth must be an integer >= 1")
        feats.append(
            Feature(
                name=name,
                predicate=pred,
                terms=terms_,
                decorative=decorative,
                decorative_reason=reason,
                graph_dependent=bool(f.get("graph_dependent", False)),
                name_implies_consequence=bool(f.get("name_implies_consequence", False)),
                position_name=f.get("position_name"),
                note=str(f.get("note", "")),
            )
        )
    if not feats:
        raise RulesetError("ruleset has no features")
    return Ruleset(
        name=hdr["name"],
        version=str(hdr["version"]),
        profile=hdr["profile"],
        description=str(hdr.get("description", "")),
        features=tuple(feats),
        source=str(path),
        wing_depth=int(hdr.get("wing_depth", 1)),
    )
