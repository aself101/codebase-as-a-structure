"""Validation configuration (validation-spec §3.7, §2.4, §7). Every threshold
feeds ``validation_config_fingerprint`` so a moved verdict resolves to a diff.

Grounding classes for descriptive signals (validation-spec §2.4.2, D-008 as amended by D-011):

- G1 ``measurement``  — a direct git or file fact. Bar: stability + non-degeneracy. Where the
  instrument embeds a heuristic (the §7 subject classifier, the indent proxy, email identity),
  the entry says so in ``heuristic``: that is a declared, bounded risk, not a certification.
- G2 ``instrument``   — a resolver-dependent fact checked against an independent second
  instrument measuring the same property (``fan_in`` ↔ ``fan_in_alt``; ``test_fan_in`` ↔
  ``test_fan_in_alt``, both from the separate scanner). Bar: stability + τ-b lower CI ≥
  ``tau_instrument``. A pair whose min lower-CI τ across all reference repos is ≥ ``tau_retire``
  is flagged non-discriminating (it cannot fail) and an adversarial fixture is required.
- G3 ``cross-modal``  — a different-modality measurement of the same property (age ↔ blame age).
  Bar: stability + τ-b lower CI ≥ ``tau_asserted``. A G3 signal that is also a blend carries
  ``inputs`` and must satisfy the G4 input rule too.
- G4 ``derived``      — a fixed-weight blend or graph function of asserted inputs. Bar:
  stability + every input asserted. The composite's *name* carries no claim beyond its inputs.
"""

from __future__ import annotations

import hashlib
import json
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

PREDICTIVE_SIGNALS: tuple[str, ...] = ("bug_pressure_index", "change_pressure_index")

# signal -> grounding spec. `counterpart` for G2/G3; `inputs` for G4 (and G3 blends); `correlates` reported only.
GROUNDING: dict[str, dict[str, Any]] = {
    # G1 measurements
    "commit_count": {"class": "G1", "instrument": "git log"},
    "churn_lines": {"class": "G1", "instrument": "git log --numstat"},
    "fix_count": {
        "class": "G1",
        "instrument": "git log",
        "heuristic": "§7 subject classifier (regex over commit subjects; also the holdout label)",
    },
    "revert_count": {"class": "G1", "instrument": "git log", "heuristic": "§7 subject classifier"},
    "author_count": {
        "class": "G1",
        "instrument": "git log",
        "heuristic": "author email, no mailmap (inflates on multi-email authors)",
    },
    "last_touched_days": {"class": "G1", "instrument": "git log author_date"},
    "recent_commit_share": {
        "class": "G1",
        "instrument": "git log (timeline-relative window, §6.2.2)",
    },
    "size_loc": {"class": "G1", "instrument": "non-blank line count"},
    "nesting_proxy": {
        "class": "G1",
        "instrument": "indent counter (§6.2.2)",
        "heuristic": "indentation depth as a stand-in for nesting",
    },
    "cochange_degree": {"class": "G1", "instrument": "git log co-occurrence (§5)"},
    "blame_age_median": {
        "class": "G1",
        "instrument": "git blame -w",
        "heuristic": "blame line attribution; no -M/-C",
    },
    "has_sibling_test": {
        "class": "G1",
        "instrument": "path convention config (§6.2.2)",
        "heuristic": "filename adjacency; literal name, convention-dependent",
    },
    # G2 instrument-checked (counterparts come from altdeps.py, which shares no code with dependency-cruiser)
    "fan_in": {
        "class": "G2",
        "counterpart": "fan_in_alt",
        "adversarial_fixture": "tests/test_instruments.py",
    },
    "fan_out": {
        "class": "G2",
        "counterpart": "fan_out_alt",
        "adversarial_fixture": "tests/test_instruments.py",
    },
    "test_fan_in": {
        "class": "G2",
        "counterpart": "test_fan_in_alt",
        "adversarial_fixture": "tests/test_instruments.py",
    },
    # G3 cross-modal
    "age_days": {"class": "G3", "counterpart": "blame_age_median"},
    "neglect_index": {
        "class": "G3",
        "counterpart": "blame_age_median",
        "inputs": ["age_days", "last_touched_days", "recent_commit_share"],
        "correlates": ["cochange_degree"],
    },
    # G4 derived from asserted inputs
    "fan_in_nonzero": {"class": "G4", "inputs": ["fan_in"]},
    "centrality": {"class": "G4", "inputs": ["fan_in"], "correlates": ["cochange_degree"]},
    "load_index": {
        "class": "G4",
        "inputs": ["fan_in_nonzero", "centrality", "fan_out", "size_loc"],
        "correlates": ["cochange_degree", "test_fan_in"],
    },
    "complexity_proxy_index": {"class": "G4", "inputs": ["size_loc", "nesting_proxy", "fan_out"]},
    "reinforcement_index": {
        "class": "G4",
        "inputs": ["test_fan_in"],
        "correlates": ["has_sibling_test"],
    },
}
DESCRIPTIVE_SIGNALS: tuple[str, ...] = tuple(GROUNDING)

# Index weight key -> the grounded signal it is a transform of (used to check G4 input lists
# against the actual formulas, so the two cannot drift; tested in tests/test_validation.py).
WEIGHT_KEY_SIGNAL: dict[str, str] = {
    "fan_in_nonzero": "fan_in_nonzero",
    "centrality": "centrality",
    "inv_fan_out": "fan_out",
    "size_loc": "size_loc",
    "nesting_proxy": "nesting_proxy",
    "fan_out": "fan_out",
    "age_days": "age_days",
    "last_touched_days": "last_touched_days",
    "inv_recent_commit_share": "recent_commit_share",
    "churn_lines": "churn_lines",
    "commit_count": "commit_count",
    "recency": "last_touched_days",
    "fix_count_nonzero": "fix_count",
    "fix_count": "fix_count",
    "revert_count": "revert_count",
    "fix_ratio": "fix_count",
}

# Blind-ranking list number -> signal it is compared against (blind/TEMPLATE.md).
RECOGNITION_LISTS: dict[int, str] = {
    1: "load_index",
    2: "bug_pressure_index",
    3: "change_pressure_index",
    4: "neglect_index",
}

# Which instrument produces each metric. A G2/G3 counterpart must come from a DIFFERENT
# instrument than the signal (circumvention A4: a self- or kin-counterpart gives tau = 1).
# Tested in tests/test_validation.py; editing this table changes the fingerprint.
METRIC_INSTRUMENT: dict[str, str] = {
    "fan_in": "dependency-cruiser",
    "fan_out": "dependency-cruiser",
    "test_fan_in": "dependency-cruiser",
    "centrality": "dependency-cruiser",
    "fan_in_nonzero": "dependency-cruiser",
    "fan_in_alt": "altdeps",
    "fan_out_alt": "altdeps",
    "test_fan_in_alt": "altdeps",
    "age_days": "git-log",
    "last_touched_days": "git-log",
    "commit_count": "git-log",
    "churn_lines": "git-log",
    "fix_count": "git-log",
    "revert_count": "git-log",
    "author_count": "git-log",
    "recent_commit_share": "git-log",
    "cochange_degree": "git-log",
    "blame_age_median": "git-blame",
    "size_loc": "file",
    "nesting_proxy": "file",
    "has_sibling_test": "path-convention",
    "neglect_index": "git-log",
    "load_index": "dependency-cruiser",
    "complexity_proxy_index": "file",
    "reinforcement_index": "dependency-cruiser",
}

# The spec's G1 membership (validation-spec §2.4.2 table). Pinned so a reclassification to
# "stability only" is a test failure, not a silent config edit (circumvention A5).
SPEC_G1: frozenset[str] = frozenset(
    {
        "commit_count",
        "churn_lines",
        "fix_count",
        "revert_count",
        "author_count",
        "last_touched_days",
        "recent_commit_share",
        "size_loc",
        "nesting_proxy",
        "cochange_degree",
        "blame_age_median",
        "has_sibling_test",
    }
)

# D-009 pre-registered roles. The gate warns loudly when the repos it is handed differ.
EXPECTED_TUNING_REPOS: tuple[str, ...] = ("uluops-registry-api", "eslint")
EXPECTED_TEST_REPOS: tuple[str, ...] = ("typeorm", "mcp-secure-server")


@dataclass(frozen=True)
class ValidationConfig:
    # §3.1 split
    holdout_frac: float = 0.20
    # §3.7 pass criteria
    auc_margin: float = 0.05
    pr_auc_mult: float = 1.20
    coverage_min: float = 0.50
    signal_floor_mult: float = 1.5
    min_repos: int = 2  # test-role repos that must pass (D-009)
    # §2.4 asserted bar
    stability_perturbation_k: int = 5
    stability_eps: float = 0.05
    stability_delta: float = 0.15
    stability_min_n: int = 30  # D-011: untested (insufficient_stability_population) below this
    stability_max_excluded_frac: float = 0.5
    # D-011/D-014: a signal whose modal value covers more than this share of the population is
    # degenerate (a constant is 1.0; a binary flag with a 5% minority class is 0.95 and passes).
    degenerate_max_modal_share: float = 0.97
    tau_asserted: float = 0.30  # G3 cross-modal floor
    tau_instrument: float = 0.60  # G2 second-instrument floor
    tau_retire: float = (
        0.85  # D-011: G2/G3 pair with min lower-CI tau >= this on all repos is non-discriminating
    )
    m_asserted: int = 2
    # uncertainty
    bootstrap_n: int = 1000
    permutation_n: int = 1000
    rng_seed: int = 20260904
    # population choices (on the page)
    holdout_include_tests: bool = True
    # §3.4 label classifier (circumvention A9). The holdout LABEL is derived from this regex
    # — frozen here, in the validation fingerprint — not from the substrate's feature-side
    # fix_subject_regex. Narrowing the feature regex cannot move the labels. Both are reported.
    label_subject_regex: str = r"\b(bug|hotfix|patch)\b"

    @classmethod
    def load(cls, path: Path | None) -> ValidationConfig:
        if path is None:
            cfg = cls()
        else:
            raw: dict[str, Any] = tomllib.loads(Path(path).read_text(encoding="utf-8"))
            unknown = set(raw) - set(cls.__dataclass_fields__)
            if unknown:
                raise ValueError(f"unknown validation config keys: {sorted(unknown)}")
            cfg = cls(**raw)
        cfg.validate()
        return cfg

    def validate(self) -> None:
        """Range-check every floor (circumvention A1/A8; audit: holdout_frac never checked).
        The spec defaults are the minimums: a config may tighten a bar, never loosen it below spec."""
        checks = [
            (0.0 < self.holdout_frac < 0.5, "holdout_frac must be in (0, 0.5)"),
            (self.auc_margin >= 0.05, "auc_margin may not be below the spec default 0.05"),
            (self.pr_auc_mult >= 1.20, "pr_auc_mult may not be below the spec default 1.20"),
            (0.0 < self.coverage_min <= 1.0, "coverage_min must be in (0, 1]"),
            (self.signal_floor_mult >= 1.0, "signal_floor_mult must be >= 1"),
            (self.min_repos >= 2, "min_repos must be >= 2"),
            (self.m_asserted >= 2, "m_asserted must be >= 2"),
            (self.stability_perturbation_k >= 1, "stability_perturbation_k must be >= 1"),
            (0.0 < self.stability_eps <= 0.05, "stability_eps must be in (0, 0.05]"),
            (
                self.stability_eps < self.stability_delta <= 0.15,
                "stability_delta must be in (eps, 0.15]",
            ),
            (self.stability_min_n >= 30, "stability_min_n must be >= 30"),
            (
                0.0 < self.stability_max_excluded_frac <= 0.5,
                "stability_max_excluded_frac must be in (0, 0.5]",
            ),
            (
                0.5 <= self.degenerate_max_modal_share <= 0.99,
                "degenerate_max_modal_share must be in [0.5, 0.99]",
            ),
            (self.tau_asserted >= 0.30, "tau_asserted may not be below the spec default 0.30"),
            (self.tau_instrument >= 0.60, "tau_instrument may not be below the spec default 0.60"),
            (self.tau_retire > self.tau_instrument, "tau_retire must exceed tau_instrument"),
            (
                self.bootstrap_n >= 200 and self.permutation_n >= 200,
                "bootstrap_n and permutation_n must be >= 200",
            ),
            (
                isinstance(self.holdout_frac, float) and isinstance(self.min_repos, int),
                "numeric types must match the schema",
            ),
        ]
        bad = [msg for ok, msg in checks if not ok]
        if bad:
            raise ValueError("invalid validation config: " + "; ".join(bad))
        import re

        re.compile(self.label_subject_regex)

    def fingerprint(self, reference_repos: list[dict[str, str]]) -> str:
        payload = {
            "config": asdict(self),
            "grounding": GROUNDING,
            "predictive": PREDICTIVE_SIGNALS,
            "reference_repos": sorted(reference_repos, key=lambda r: r["name"]),
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
