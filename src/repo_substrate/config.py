"""Effective configuration for the substrate (repo-substrate-spec §3, §8).

Everything here that affects a value feeds ``config_fingerprint``. That is the
determinism contract's second half: the seed attributes a change to *code*,
the fingerprint attributes it to *configuration or toolchain*. A value that
moves under an unchanged seed and an unchanged fingerprint is a bug.

Defaults are the spec's v0 placeholders (§6.2.1 weights, §6.1 N_min, §6.3
graph_quality_min, §9 report thresholds, and the D-004 cross-modal knobs).
They are deliberately not tuned; the validation gate is the tuner.
"""

from __future__ import annotations

import hashlib
import json
import tomllib
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

# --- extension → language table (§4 `languages`; pinned so `lang` is a pure function of path)
LANGUAGE_BY_EXT: dict[str, str] = {
    ".ts": "ts", ".tsx": "ts", ".mts": "ts", ".cts": "ts",
    ".js": "js", ".jsx": "js", ".mjs": "js", ".cjs": "js",
    ".py": "py", ".pyi": "py",
    ".go": "go", ".rs": "rs", ".java": "java", ".kt": "kt", ".scala": "scala",
    ".rb": "rb", ".php": "php", ".cs": "cs", ".swift": "swift",
    ".c": "c", ".h": "c", ".cc": "cpp", ".cpp": "cpp", ".hpp": "cpp",
    ".sh": "sh", ".sql": "sql",
}

DEFAULT_EXCLUDE_GLOBS: tuple[str, ...] = (
    "**/node_modules/**", "**/dist/**", "**/build/**", "**/out/**", "**/coverage/**",
    "**/vendor/**", "**/third_party/**", "**/.git/**", "**/generated/**", "**/__generated__/**",
    "**/*.min.js", "**/*.d.ts", "**/*.map", "**/*.snap",
)

DEFAULT_TEST_GLOBS: tuple[str, ...] = (
    "**/*.test.*", "**/*.spec.*", "**/*_test.*", "**/test_*.py",
    "**/test/**", "**/tests/**", "**/__tests__/**", "**/spec/**", "**/__mocks__/**",
)

# Roots that, when stripped from a test path, yield the module path it mirrors (§6.2.2 test proximity).
DEFAULT_TEST_ROOTS: tuple[str, ...] = ("test/", "tests/", "__tests__/", "spec/")
DEFAULT_TEST_SUFFIXES: tuple[str, ...] = (".test", ".spec", "_test")


@dataclass(frozen=True)
class IndexWeights:
    """§6.2.1 pinned v0 weights. Keys are percentile names unless noted; each set sums to 1.0."""

    load_index: dict[str, float] = field(default_factory=lambda: {
        "fan_in_nonzero": 0.5, "centrality": 0.3, "inv_fan_out": 0.1, "size_loc": 0.1})
    change_pressure_index: dict[str, float] = field(default_factory=lambda: {
        "churn_lines": 0.4, "commit_count": 0.3, "recency": 0.3})
    bug_pressure_index: dict[str, float] = field(default_factory=lambda: {
        "fix_count_nonzero": 0.5, "revert_count": 0.2, "fix_ratio": 0.3})
    neglect_index: dict[str, float] = field(default_factory=lambda: {
        "age_days": 0.4, "last_touched_days": 0.4, "inv_recent_commit_share": 0.2})
    complexity_proxy_index: dict[str, float] = field(default_factory=lambda: {
        "size_loc": 0.4, "nesting_proxy": 0.4, "fan_out": 0.2})


@dataclass(frozen=True)
class SubstrateConfig:
    # --- population & percentiles (§6.1)
    exclude_globs: tuple[str, ...] = DEFAULT_EXCLUDE_GLOBS
    include_extensions: tuple[str, ...] = tuple(sorted(LANGUAGE_BY_EXT))
    test_globs: tuple[str, ...] = DEFAULT_TEST_GLOBS
    test_roots: tuple[str, ...] = DEFAULT_TEST_ROOTS
    test_suffixes: tuple[str, ...] = DEFAULT_TEST_SUFFIXES
    n_min: int = 30
    exclude_tests_from_population: bool = True
    rounding_dp: int = 4
    # --- history (§5, §7)
    fix_subject_regex: str = r"\b(bug|hotfix|patch)\b"
    cochange_min: int = 2
    cochange_max_files: int = 30
    recent_window_frac: float = 0.20
    # --- graph (§6.2.2, §6.3)
    pagerank_alpha: float = 0.85
    pagerank_max_iter: int = 100
    pagerank_tol: float = 1e-6
    pagerank_backend: str = "power-iteration-python"
    graph_quality_min: float = 0.80
    # --- static (§6.2.2)
    nesting_max_bytes: int = 2 * 1024 * 1024
    # --- report (§9)
    report_top_k: int = 10
    report_p: float = 0.90
    report_q: float = 0.10
    # --- indices (§6.2.1)
    weights: IndexWeights = field(default_factory=IndexWeights)

    @classmethod
    def load(cls, path: Path | None) -> SubstrateConfig:
        """Load a TOML override file on top of defaults. Unknown keys are an error:
        a typo in a config must not silently leave a default in place."""
        if path is None:
            return cls()
        raw: dict[str, Any] = tomllib.loads(Path(path).read_text())
        weights_raw = raw.pop("weights", None)
        known = {f for f in cls.__dataclass_fields__ if f != "weights"}
        unknown = set(raw) - known
        if unknown:
            raise ValueError(f"unknown config keys: {sorted(unknown)}")
        for k in ("exclude_globs", "include_extensions", "test_globs", "test_roots", "test_suffixes"):
            if k in raw:
                raw[k] = tuple(raw[k])
        weights = IndexWeights(**weights_raw) if weights_raw else IndexWeights()
        return cls(**raw, weights=weights)

    def effective(self, toolchain_versions: dict[str, str]) -> dict[str, Any]:
        """The full value-affecting configuration, including the toolchain (§3)."""
        d = asdict(self)
        d["toolchain_versions"] = dict(sorted(toolchain_versions.items()))
        return d

    def fingerprint(self, toolchain_versions: dict[str, str]) -> str:
        payload = json.dumps(self.effective(toolchain_versions), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode()).hexdigest()

    def validate(self) -> None:
        for name, w in asdict(self.weights).items():
            s = sum(w.values())
            if abs(s - 1.0) > 1e-9:
                raise ValueError(f"weights for {name} sum to {s}, not 1.0")
        if not (0 < self.recent_window_frac < 1):
            raise ValueError("recent_window_frac must be in (0,1)")
        if self.n_min < 2:
            raise ValueError("n_min must be >= 2")
