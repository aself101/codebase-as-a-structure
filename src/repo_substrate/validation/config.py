"""Validation configuration (validation-spec §3.7, §2.4, §7). Every threshold
feeds ``validation_config_fingerprint`` so a moved verdict resolves to a diff.

Grounding classes for descriptive signals (validation-spec §2.4.2 as revised by D-008):

- G1 ``measurement``  — a direct git or file fact (commit count, blame age, line count).
  Correctness is the instrument's (git, the file); the bar is stability only. The name
  of the metric is literal, so no meaning is being smuggled by the label.
- G2 ``instrument``   — a resolver-dependent fact (fan_in) checked against an independent
  second instrument measuring the same property (``fan_in_alt``, a separate scanner;
  ``test_fan_in`` for reinforcement). Bar: stability + τ-b lower CI ≥ ``tau_instrument``.
- G3 ``cross-modal``  — a signal checked against a different-modality measurement of the
  same present-tense property (age ↔ blame age). Bar: stability + τ-b lower CI ≥ ``tau_asserted``.
- G4 ``derived``      — a fixed-weight blend or graph function of asserted inputs (load_index,
  centrality). Bar: stability + every input asserted. The composite's *name* carries no
  claim beyond its inputs (D-004 Q3); correlates are reported, never gated.
"""

from __future__ import annotations

import hashlib
import json
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

PREDICTIVE_SIGNALS: tuple[str, ...] = ("bug_pressure_index", "change_pressure_index")

# signal -> grounding spec. `counterpart` for G2/G3; `inputs` for G4; `correlates` reported only.
GROUNDING: dict[str, dict[str, Any]] = {
    # G1 measurements
    "commit_count":      {"class": "G1", "instrument": "git log"},
    "churn_lines":       {"class": "G1", "instrument": "git log --numstat"},
    "fix_count":         {"class": "G1", "instrument": "git log + §7 classifier"},
    "revert_count":      {"class": "G1", "instrument": "git log + §7 classifier"},
    "author_count":      {"class": "G1", "instrument": "git log (email, no mailmap)"},
    "last_touched_days": {"class": "G1", "instrument": "git log author_date"},
    "size_loc":          {"class": "G1", "instrument": "non-blank line count"},
    "nesting_proxy":     {"class": "G1", "instrument": "indent counter (§6.2.2)"},
    "cochange_degree":   {"class": "G1", "instrument": "git log co-occurrence (§5)"},
    "blame_age_median":  {"class": "G1", "instrument": "git blame -w"},
    # G2 instrument-checked
    "fan_in":            {"class": "G2", "counterpart": "fan_in_alt"},
    "fan_in_nonzero":    {"class": "G2", "counterpart": "fan_in_alt"},
    "fan_out":           {"class": "G2", "counterpart": "fan_out_alt"},
    "has_sibling_test":  {"class": "G2", "counterpart": "test_fan_in"},
    # G3 cross-modal
    "age_days":          {"class": "G3", "counterpart": "blame_age_median"},
    "neglect_index":     {"class": "G3", "counterpart": "blame_age_median", "correlates": ["cochange_degree"]},
    # G4 derived from asserted inputs
    "centrality":              {"class": "G4", "inputs": ["fan_in"], "correlates": ["cochange_degree"]},
    "load_index":              {"class": "G4", "inputs": ["fan_in_nonzero", "centrality", "fan_out", "size_loc"],
                                "correlates": ["cochange_degree", "test_fan_in"]},
    "complexity_proxy_index":  {"class": "G4", "inputs": ["size_loc", "nesting_proxy", "fan_out"]},
    "reinforcement_index":     {"class": "G4", "inputs": ["has_sibling_test"], "correlates": ["test_fan_in"]},
}
DESCRIPTIVE_SIGNALS: tuple[str, ...] = tuple(GROUNDING)

# Blind-ranking list number -> signal it is compared against (blind/TEMPLATE.md).
RECOGNITION_LISTS: dict[int, str] = {1: "load_index", 2: "bug_pressure_index", 3: "change_pressure_index", 4: "neglect_index"}


@dataclass(frozen=True)
class ValidationConfig:
    # §3.1 split
    holdout_frac: float = 0.20
    # §3.7 pass criteria
    auc_margin: float = 0.05
    pr_auc_mult: float = 1.20
    coverage_min: float = 0.50
    signal_floor_mult: float = 1.5
    min_repos: int = 2
    # §2.4 asserted bar
    stability_perturbation_k: int = 5
    stability_eps: float = 0.05
    stability_delta: float = 0.15
    tau_asserted: float = 0.30      # G3 cross-modal floor
    tau_instrument: float = 0.60    # G2 second-instrument floor (same property: agreement should be high)
    m_asserted: int = 2
    # uncertainty
    bootstrap_n: int = 1000
    permutation_n: int = 1000
    rng_seed: int = 20260904
    # population choices (on the page)
    holdout_include_tests: bool = True

    @classmethod
    def load(cls, path: Path | None) -> ValidationConfig:
        if path is None:
            return cls()
        raw: dict[str, Any] = tomllib.loads(Path(path).read_text())
        unknown = set(raw) - set(cls.__dataclass_fields__)
        if unknown:
            raise ValueError(f"unknown validation config keys: {sorted(unknown)}")
        return cls(**raw)

    def fingerprint(self, reference_repos: list[dict[str, str]]) -> str:
        payload = {"config": asdict(self), "grounding": GROUNDING, "predictive": PREDICTIVE_SIGNALS,
                   "reference_repos": sorted(reference_repos, key=lambda r: r["name"])}
        return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
