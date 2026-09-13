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
# D-048: a word in a position name that names a record, and the signals that read that record;
# a blend (load_index) is not an import — its floor is cleared by a leaf nothing imports
# D-050: the phrases a position name wears for a pNN in its predicate — one phrase per quantile
# term; "long-untouched" wears last_touched_days >= p90, "at or above the median" wears p50,
# "at or above the upper quartile" wears p75, "high" wears p75 or above (D-048)
QUANTILE_PHRASES = r"\b(?:upper quartile|lower quartile|upper decile|lower decile|high|long|median|top|most|percentile)\b"

POSITION_RECORD_WORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("imported", ("fan_in", "fan_in_nonzero", "is_package_entry", "test_fan_in", "reinforcement_index")),
    ("importing", ("fan_out",)),
    ("import-graph", ("fan_in", "fan_out", "centrality")),
    ("root", ("fan_in",)),
    ("leaf", ("fan_out",)),
    ("reinforced", ("reinforcement_index", "test_fan_in")),
    ("unreinforced", ("reinforcement_index", "test_fan_in")),
    ("untouched", ("last_touched_days", "age_days", "blame_age_median")),
    ("touched", ("last_touched_days", "age_days", "blame_age_median")),
    ("edit", ("commit_count", "churn_lines", "fix_count", "bug_pressure_index", "change_pressure_index")),
    ("load", ("load_index",)),
    ("centrality", ("centrality",)),
    ("fan-out", ("fan_out",)),
    ("fan-in", ("fan_in", "fan_in_nonzero")),
    ("package entry", ("is_package_entry",)),
)
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
    # D-054: the part of decorative_reason that is about a signal, keyed by signal — written once
    # in the ruleset's [signal_reason] table and composed into every feature that reads the signal
    decorative_signal_reasons: dict[str, str] = field(default_factory=dict, compare=False)
    graph_dependent: bool = False
    name_implies_consequence: bool = False
    position_name: str | None = None  # the position-denoting alternative name (D-004 Q3)
    # D-041/D-042: a limit on what the predicate can read — never a claim about a repository (the
    # sixth seating found one false of the room it sat beside)
    caveat: str | None = None
    # D-060: the caveat's live case as a predicate over raw metrics (literal terms only), so the page
    # can count how many of the feature's rooms are the case — a caveat says "can" and D-042 forbids
    # it a repository fact; on registry the flooded_basement case was 12 of 26 and the page could not say so
    caveat_case: str | None = None
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
    signal_reasons: dict[str, str] = field(default_factory=dict, compare=False)  # D-054
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
    unknown = sorted(set(raw) - {"ruleset", "feature", "signal_reason"})  # D-054: signal_reason
    if unknown:
        raise RulesetError(
            f"unknown top-level table(s) {unknown}; a ruleset carries [ruleset], [[feature]] and [signal_reason] only"
        )
    hdr = raw.get("ruleset") or {}
    for key in ("name", "version", "profile"):
        if not hdr.get(key):
            raise RulesetError(f"[ruleset] missing {key}")
    feats: list[Feature] = []
    seen: set[str] = set()
    sr_raw = raw.get("signal_reason") or {}
    if not isinstance(sr_raw, dict) or not all(isinstance(v, str) and v.strip() for v in sr_raw.values()):
        raise RulesetError("[signal_reason] maps signal names to non-empty strings")
    signal_reasons: dict[str, str] = {str(k): str(v).strip() for k, v in sr_raw.items()}
    signals_excused: set[str] = set()
    raw_names = [str(x.get("name")) for x in raw.get("feature") or [] if x.get("name")]
    for f in raw.get("feature") or []:
        name = f.get("name")
        if not name or name in seen:
            raise RulesetError(f"feature name missing or duplicated: {name!r}")
        seen.add(name)
        pred = f.get("predicate")
        if not pred:
            raise RulesetError(f"feature {name}: missing predicate")
        decorative = bool(f.get("decorative", False))
        own_reason = f.get("decorative_reason")
        terms_ = parse_predicate(pred)
        # D-054 (fifteenth seating): a reason about a signal belongs to the signal. crack's row said
        # "unvalidated" and toothpick_wing's said what the tuning did to the blend, on one signal;
        # the [signal_reason] table says it once and every feature reading the signal carries it.
        sig_reasons = {t.signal: signal_reasons[t.signal] for t in terms_ if t.signal in signal_reasons}
        if sig_reasons and not decorative:
            raise RulesetError(
                f"feature {name}: reads {', '.join(sorted(sig_reasons))}, which [signal_reason] excuses, without decorative = true"
            )
        for sg in sig_reasons:
            signals_excused.add(sg)
        composed = " ".join(
            [f"{sg} is {txt.rstrip('.')}." for sg, txt in sorted(sig_reasons.items())]
            + ([str(own_reason).strip()] if own_reason else [])
        )
        reason = composed or None
        # mapper §3 (D-004): the hatch is audited — a decorative rule must say why.
        if decorative and not reason:
            raise RulesetError(f"feature {name}: decorative = true requires decorative_reason or a [signal_reason] for a signal it reads")
        if decorative and reason and not any(t.signal in str(reason) for t in terms_):
            # mapper §3: the reason must NAME the ungrounded signal; a non-empty string is not a reason (D-030)
            raise RulesetError(
                f"feature {name}: decorative_reason must name the ungrounded signal(s) it excuses ({', '.join(sorted({t.signal for t in terms_}))})"
            )
        caveat_case = f.get("caveat_case")
        if caveat_case:
            if not f.get("caveat"):
                raise RulesetError(f"feature {name}: caveat_case given without a caveat")
            for t in parse_predicate(str(caveat_case)):
                if t.percentile is not None:
                    raise RulesetError(f"feature {name}: caveat_case reads a percentile ({t}); the case is counted on raw metrics, literal terms only")
        implied = any(w in str(name).lower() for w in NAME_CONSEQUENCE_WORDS)
        if implied and not bool(f.get("name_implies_consequence", False)):
            raise RulesetError(
                f"feature {name}: the name carries a consequence word ({', '.join(w for w in NAME_CONSEQUENCE_WORDS if w in str(name).lower())}); declare name_implies_consequence = true with a position_name (D-030)"
            )
        # D-047: a position name describes what the predicate reads; a quantile word in it (median,
        # top, most, decile, percentile) needs a pNN in the predicate — scaffolding's claimed a median
        # no predicate computed, for eight ruleset versions
        pos = str(f.get("position_name") or "").lower()
        if (
            pos
            and re.search(r"\b(?:median|top|most|decile|quartile|percentile|upper|lower)\b", pos)
            and not re.search(r"\bp\d{1,2}\b", str(f.get("predicate", "")))
        ):
            raise RulesetError(
                f"feature {name}: position_name {f.get('position_name')!r} claims a quantile the predicate {f.get('predicate')!r} does not read (D-047)"
            )
        # D-048: a record word in a position name names a record the predicate reads —
        # flooded_basement's "still-imported" labelled a load blend a leaf clears with no importer,
        # 27 of its 75 rooms on eslint; and "high" is worn once per top-quartile-or-above pNN
        # (corridor's "high-fan-out" labelled p50 beside "high-centrality" at p90)
        pred_s = str(f.get("predicate", ""))
        for word, sigs in POSITION_RECORD_WORDS:
            if re.search(rf"\b{word}\b", pos) and not any(
                re.search(rf"\b{s}\b", pred_s) for s in sigs
            ):
                raise RulesetError(
                    f"feature {name}: position_name {f.get('position_name')!r} says {word!r} but the predicate {pred_s!r} reads none of {', '.join(sigs)} (D-048)"
                )
        highs = len(re.findall(r"\bhigh\b", pos))
        upper = sum(1 for q in re.findall(r"\bp(\d{1,2})\b", pred_s) if int(q) >= 75)
        if highs > upper:
            raise RulesetError(
                f"feature {name}: position_name {f.get('position_name')!r} says 'high' {highs} time(s) but the predicate {pred_s!r} carries {upper} pNN at or above p75 (D-048)"
            )
        # D-049: a position name wears no other feature's name — foundation's 'high-load hub' called
        # every foundation room a hub while its own relation cell recorded no containment with hub
        for other in raw_names:
            if other != name and re.search(rf"\b{re.escape(str(other))}\b", pos):
                raise RulesetError(
                    f"feature {name}: position_name {f.get('position_name')!r} names the feature {other!r}; a position is a place in a record, not another feature's set (D-049)"
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
        # D-050: the converse — every quantile the predicate reads is worn by the name. D-047 and
        # D-048 refused a quantile word the predicate did not carry; nothing refused a pNN the name
        # left out, and "import-graph root" (fan_in == 0 and fan_out >= p75) and "imported leaf"
        # (fan_out == 0 and fan_in >= p75) each named one conjunct of two beside a count column
        # (the twelfth seating: 1 printed against 23 rooms with no fan-in; 33 against 110 leaves)
        pos_l = str(pos or "").lower()
        if pos_l:
            worn = len(re.findall(QUANTILE_PHRASES, pos_l))
            read = len(re.findall(r"\bp\d{1,2}\b", pred_s))
            if worn < read:
                raise RulesetError(
                    f"feature {name}: position_name {f.get('position_name')!r} wears {worn} quantile phrase(s) but the predicate {pred_s!r} reads {read} pNN — a conjunct at a quantile is unnamed (D-050)"
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
                decorative_signal_reasons=sig_reasons,
                graph_dependent=bool(f.get("graph_dependent", False)),
                name_implies_consequence=bool(f.get("name_implies_consequence", False)),
                position_name=f.get("position_name"),
                caveat=f.get("caveat"),
                caveat_case=caveat_case,
                note=str(f.get("note", "")),
            )
        )
    if not feats:
        raise RulesetError("ruleset has no features")
    orphan = set(signal_reasons) - signals_excused
    if orphan:
        raise RulesetError(f"[signal_reason] names signals no feature reads: {', '.join(sorted(orphan))}")
    return Ruleset(
        name=hdr["name"],
        version=str(hdr["version"]),
        profile=hdr["profile"],
        description=str(hdr.get("description", "")),
        features=tuple(feats),
        source=str(path),
        wing_depth=int(hdr.get("wing_depth", 1)),
        signal_reasons=signal_reasons,
    )
