"""Ruleset loading and validation (structural-mapper-spec §3, §4, §5.5 of the system spec).

A ruleset is a versioned TOML document: a `[ruleset]` header and `[[feature]]` entries,
each with a predicate over substrate signals. Predicate grammar (deliberately small):

    term ( and term )*
    term := <signal> <op> <value>
    op   := >= | <= | > | < | ==
    value := pNN            -- the NN-th percentile of that signal across the population
           | <float>        -- an absolute threshold (indices and percentiles are in [0, 1])

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
    strata_signal: str = (
        "age_days"  # what the cutaway stacks vertically (§6: geometry is profile-independent)
    )
    wing_depth: int = 1  # directory depth that defines a wing
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
        if not decorative and reason:
            raise RulesetError(f"feature {name}: decorative_reason given but decorative = false")
        feats.append(
            Feature(
                name=name,
                predicate=pred,
                terms=parse_predicate(pred),
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
        strata_signal=str(hdr.get("strata_signal", "age_days")),
        wing_depth=int(hdr.get("wing_depth", 1)),
    )
