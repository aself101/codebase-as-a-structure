"""C3 — the Structural Mapper (structural-mapper-spec.md, D-016).

The only component allowed to emit a discrete, named structural claim, under three
disciplines: the anti-horoscope gate (a rule may read a signal only if validation.json
says `validated` or `asserted`, or the rule is `decorative` with a reason), provenance
(every feature carries its predicate and the values that fired it), and determinism
(same substrate + ruleset + validation → same skeleton).
"""

from .engine import map_skeleton
from .ruleset import Ruleset, RulesetError, load_ruleset

__all__ = ["Ruleset", "RulesetError", "load_ruleset", "map_skeleton"]
