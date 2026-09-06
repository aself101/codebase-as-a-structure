"""Verdict-path tests for the validation gate (validation-spec §2.4, §3, §3.8; D-009; D-011).
These are the tests the 2026-09-04 review found missing: the holdout split and labels,
the stability exclusion, verdict legality built from fabricated results, cache integrity,
the tuning/test roles, and the config floors."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from repo_substrate.config import ALLOWED_INPUTS, IndexWeights, SubstrateConfig
from repo_substrate.validation.asserted import RepoAsserted, _signal_value, run_stability
from repo_substrate.validation.config import (
    EXPECTED_TEST_REPOS,
    EXPECTED_TUNING_REPOS,
    GROUNDING,
    METRIC_INSTRUMENT,
    PREDICTIVE_SIGNALS,
    SPEC_G1,
    WEIGHT_KEY_SIGNAL,
    ValidationConfig,
)
from repo_substrate.validation.gate import build_validation, descriptive_verdict, predictive_verdict
from repo_substrate.validation.holdout import RepoHoldout, run_holdout, split_and_eligible
from repo_substrate.validation.substrates import SubstrateCache


def _vcfg(**kw) -> ValidationConfig:
    # Tests construct directly (validate() is only invoked by load()) so the tiny synthetic
    # population can exercise the code paths that real floors would refuse.
    return ValidationConfig(**kw)


@pytest.fixture
def cache(scripted_repo, small_cfg, tmp_path):
    return SubstrateCache(
        tmp_path / "cache", small_cfg, None, scratch_dir=tmp_path, blame_workers=2
    )


# --- §3.1–§3.4 split, eligibility, labels ---------------------------------------------------


def test_split_is_training_prefix(scripted_repo, cache):
    repo, shas = scripted_repo
    ctx = split_and_eligible(repo.path, cache, _vcfg(holdout_frac=0.25))
    # 12 commits, frac 0.25 → floor(9) = 9 training commits; split sha is the 9th; 3 holdout
    assert ctx.split_sha == shas[8]
    assert ctx.n_holdout_commits == 3
    assert ctx.n_commits == 12


def test_labels_and_eligibility(scripted_repo, cache):
    repo, shas = scripted_repo
    ctx = split_and_eligible(repo.path, cache, _vcfg(holdout_frac=0.25))
    lab = dict(zip(ctx.ids, ctx.labels, strict=True))
    # holdout = [chore: touch f2, merge, fix: f3] → only f3 is a fix-positive
    assert lab["src/f3.js"] == 1
    assert lab["src/f2.js"] == 0
    assert "src/side.js" in lab  # committed before the split (9th commit) → eligible
    assert (
        "src/merge_only.js" not in lab
    )  # born in the holdout window AND an orphan → not eligible (§3.3)
    assert ctx.coverage == pytest.approx(len(ctx.ids) / ctx.n_head_nodes)


def test_split_guard_refuses_wraparound(make_repo, small_cfg, tmp_path):
    r = make_repo("one")
    r.write("a.js", "1\n")
    r.commit("feat: only")
    c = SubstrateCache(tmp_path / "c", small_cfg, None, scratch_dir=tmp_path, blame_workers=1)
    with pytest.raises(ValueError, match="too few"):
        split_and_eligible(r.path, c, _vcfg())


def test_holdout_labels_use_frozen_label_regex_not_feature_regex(scripted_repo, tmp_path):
    """Narrowing the substrate's fix regex must not move the holdout labels (circumvention A9)."""
    repo, _ = scripted_repo
    narrow = SubstrateConfig(n_min=2, fix_subject_regex=r"\bNEVER-MATCHES\b")
    c = SubstrateCache(tmp_path / "c2", narrow, None, scratch_dir=tmp_path, blame_workers=2)
    ctx = split_and_eligible(repo.path, c, _vcfg(holdout_frac=0.25))
    assert (
        sum(ctx.labels) == 1
    )  # "fix: f3 latest" is still a positive (conventional prefix, frozen regex)


def test_run_holdout_degenerate_when_no_negatives(make_repo, small_cfg, tmp_path):
    r = make_repo("allpos")
    for i in range(3):
        r.write(f"f{i}.js", "1\n")
    r.commit("feat: init")
    for i in range(3):
        r.write(f"f{i}.js", f"{i + 2}\n")
        r.commit(f"chore: touch {i}")
    r.write("f0.js", "9\n")
    r.write("f1.js", "9\n")
    r.write("f2.js", "9\n")
    r.commit("fix: everything")
    c = SubstrateCache(tmp_path / "c3", small_cfg, None, scratch_dir=tmp_path, blame_workers=1)
    rh = run_holdout(r.path, c, _vcfg(holdout_frac=0.2))
    assert rh.degenerate == "no_holdout_negatives"
    assert rh.signals == {}


# --- §2.4.1 stability -----------------------------------------------------------------------


def test_stability_excludes_nodes_touched_by_removed_commits(scripted_repo, cache):
    repo, shas = scripted_repo
    full = cache.get(repo.path, "HEAD")
    pert = cache.get(repo.path, shas[-2], truncate=True)  # remove the last commit (fix: f3)
    v = _vcfg(stability_perturbation_k=1, stability_min_n=1, stability_max_excluded_frac=0.9)
    out, n_common, n_excluded = run_stability(full, pert, v)
    assert n_excluded == 1  # src/f3.js was touched → excluded
    assert n_common >= 4
    assert all(o["n_excluded_touched"] == 1 for o in out.values())


def test_stability_population_floor_yields_untested(scripted_repo, cache):
    repo, shas = scripted_repo
    full = cache.get(repo.path, "HEAD")
    pert = cache.get(repo.path, shas[-2], truncate=True)
    out, _, _ = run_stability(
        full, pert, _vcfg(stability_perturbation_k=1)
    )  # default min_n=30 > population
    assert all(
        o["passed"] is None and o["reason"] == "insufficient_stability_population"
        for o in out.values()
    )


def test_signal_value_reaches_percentile_only_signals(scripted_repo, cache):
    repo, _ = scripted_repo
    full = cache.get(repo.path, "HEAD")
    pop = [n for n in full["nodes"] if n["derived"]["indices"] is not None]
    for sig, g in GROUNDING.items():
        if g["class"] == "G2" or sig in ("centrality", "reinforcement_index", "fan_in_nonzero"):
            continue  # graph-dependent: absent by construction with no extractor
        assert any(_signal_value(n, sig) is not None for n in pop), sig


# --- §3.8 legality and D-009 roles, from fabricated results -------------------------------------


def _holdout(name, passed, degenerate=None) -> RepoHoldout:
    h = RepoHoldout(
        name=name,
        head_sha="h",
        split_sha="s",
        n_commits=100,
        n_holdout_commits=20,
        n_head_nodes=50,
        n_eligible=40,
        n_positives=10,
        coverage=0.8,
        base_rate=0.25,
        fix_label_rate=0.3,
        degenerate=degenerate,
    )
    h.baselines = {
        "busyness": {"roc_auc": 0.7, "pr_auc": 0.4},
        "recency": {"roc_auc": 0.6, "pr_auc": 0.3},
    }
    h.best_baseline = "busyness"
    for s in PREDICTIVE_SIGNALS:
        h.signals[s] = {
            "roc_auc": 0.8 if passed else 0.6,
            "pr_auc": 0.6 if passed else 0.3,
            "precision_at_k": {},
            "recall_at_k": {},
            "passed": passed and degenerate is None,
            "failed_clauses": [] if passed else ["roc_margin"],
            "best_baseline": "busyness",
            "tau_vs_best_baseline": 0.5,
        }
    return h


def _asserted(name, stable=True, corroborated=True, degenerate=False) -> RepoAsserted:
    a = RepoAsserted(
        name=name,
        head_sha="h",
        perturbed_sha="p",
        n_population=100,
        n_compared=80,
        n_excluded_touched=5,
    )
    for sig, g in GROUNDING.items():
        a.stability[sig] = {
            "passed": (not degenerate) and stable,
            "reason": "degenerate" if degenerate else (None if stable else "unstable"),
            "median_abs_delta": 0.0,
            "max_abs_delta": 0.0,
            "p95_abs_delta": 0.0,
            "n": 80,
            "distinct_values": 2 if degenerate else 40,
            "modal_share": 0.99 if degenerate else 0.3,
        }
        if g["class"] in ("G2", "G3"):
            a.corroboration[sig] = {
                "counterpart": g["counterpart"],
                "passed": corroborated,
                "tau_b": 0.7,
                "tau_b_ci": [0.6, 0.8],
                "reason": None if corroborated else "corroboration_fail",
                "n": 80,
            }
        else:
            a.corroboration[sig] = {"passed": True if g["class"] == "G1" else None}
    return a


def test_predictive_can_never_be_asserted_and_descriptive_never_validated():
    v = _vcfg()
    doc = build_validation(
        [_holdout("a", True), _holdout("b", True), _holdout("c", True)],
        [_asserted("a"), _asserted("b"), _asserted("c")],  # M_asserted = 3 since D-033
        v,
        "fp",
        [
            {"name": "a", "head_sha": "h", "role": "test"},
            {"name": "b", "head_sha": "h", "role": "test"},
            {"name": "c", "head_sha": "h", "role": "test"},
        ],
    )
    for name, s in doc["signals"].items():
        if s["kind"] == "predictive":
            assert s["status"] in ("validated", "unvalidated", "untested")
        else:
            assert s["status"] in ("asserted", "untested")
    assert doc["signals"]["bug_pressure_index"]["status"] == "validated"
    assert doc["signals"]["load_index"]["status"] == "asserted"


def test_tuning_repos_cannot_confer_validated():
    v = _vcfg()
    roles = {"a": "tuning", "b": "tuning"}
    r = predictive_verdict(
        "bug_pressure_index", [_holdout("a", True), _holdout("b", True)], roles, v
    )
    assert r["status"] == "untested" and r["reason"] == "no_test_repos"
    roles = {"a": "tuning", "b": "test"}
    r = predictive_verdict(
        "bug_pressure_index", [_holdout("a", True), _holdout("b", True)], roles, v
    )
    assert r["status"] == "unvalidated"  # one passing test repo, need two
    assert r["holdout"]["test_passes"] == 1 and r["holdout"]["n_test_repos"] == 1


def test_degenerate_signal_is_never_asserted():
    v = _vcfg()
    resolved: dict = {}
    r = descriptive_verdict(
        "revert_count",
        [_asserted("a", degenerate=True), _asserted("b", degenerate=True)],
        v,
        resolved,
    )
    assert r["status"] == "untested" and r["reason"] == "degenerate"


def test_g4_requires_every_input_asserted():
    v = _vcfg()
    resolved = {"fan_in": {"status": "untested"}}
    r = descriptive_verdict("fan_in_nonzero", [_asserted("a"), _asserted("b")], v, resolved)
    assert r["status"] == "untested" and r["reason"] == "input_not_asserted:fan_in"


def test_retirement_flag_when_counterpart_cannot_fail():
    v = _vcfg()
    a, b = _asserted("a"), _asserted("b")
    for x in (a, b):
        x.corroboration["fan_in"]["tau_b_ci"] = [0.9, 0.95]
    r = descriptive_verdict("fan_in", [a, b], v, {})
    assert r["non_discriminating"] is True


# --- config integrity (circumvention A1/A4/A5/A6) ---------------------------------------------


def test_validation_config_floors_cannot_be_loosened():
    for bad in (
        {"m_asserted": 0},
        {"min_repos": 1},
        {"holdout_frac": 0.95},
        {"tau_instrument": 0.3},
        {"stability_eps": 0.3},
        {"auc_margin": 0.0},
    ):
        with pytest.raises(ValueError):
            ValidationConfig(**bad).validate()
    ValidationConfig().validate()


def test_counterparts_come_from_a_different_instrument():
    for sig, g in GROUNDING.items():
        if g["class"] in ("G2", "G3"):
            assert METRIC_INSTRUMENT[g["counterpart"]] != METRIC_INSTRUMENT[sig], sig
            assert g["counterpart"] != sig
            # and never one of the signal's own formula inputs
            keys = ALLOWED_INPUTS.get(sig, set())
            assert g["counterpart"] not in {WEIGHT_KEY_SIGNAL[k] for k in keys}, sig


def test_g1_membership_is_pinned_to_the_spec():
    assert {s for s, g in GROUNDING.items() if g["class"] == "G1"} == set(SPEC_G1)


def test_g4_inputs_match_the_index_formulas():
    w = IndexWeights()
    for index in ("load_index", "complexity_proxy_index", "neglect_index"):
        formula = {WEIGHT_KEY_SIGNAL[k] for k in getattr(w, index)}
        assert formula == set(GROUNDING[index]["inputs"]), index


def test_pre_registered_roles_are_disjoint():
    assert not set(EXPECTED_TEST_REPOS) & set(EXPECTED_TUNING_REPOS)


# --- cache integrity (circumvention A2; audit) -------------------------------------------------


def test_cache_rejects_foreign_fingerprint_and_corrupt_entries(scripted_repo, small_cfg, tmp_path):
    repo, _ = scripted_repo
    c = SubstrateCache(tmp_path / "cc", small_cfg, None, scratch_dir=tmp_path, blame_workers=2)
    doc = c.get(repo.path, "HEAD")
    p = c.path_for(repo.path, doc["repo"]["head_sha"], truncate=False)
    assert p.exists()
    # foreign fingerprint → rejected and re-extracted
    tampered = dict(doc)
    tampered["repo"] = {**doc["repo"], "config_fingerprint": "0" * 64}
    p.write_text(json.dumps(tampered), encoding="utf-8")
    again = c.get(repo.path, "HEAD")
    assert again["repo"]["config_fingerprint"] == c.fingerprint
    # corrupt bytes → treated as a miss, not a crash
    p.write_bytes(b'{"schema_version": "0.2", "repo": {')
    again = c.get(repo.path, "HEAD")
    assert again["seed"] == doc["seed"]
    att = c.attestations[p.name]
    assert att["seed"] == doc["seed"] and len(att["bytes_sha256"]) == 64


def test_cache_key_separates_truncated_from_tip(scripted_repo, small_cfg, tmp_path):
    repo, shas = scripted_repo
    c = SubstrateCache(tmp_path / "ck", small_cfg, None, scratch_dir=tmp_path, blame_workers=2)
    assert c.path_for(Path(repo.path), shas[5], True) != c.path_for(Path(repo.path), shas[5], False)


def test_local_signals_read_zero_after_reranking(scripted_repo, cache):
    """D-033: once percentiles are ranked over the untouched population in both runs, a signal
    computed from the file's own content and history cannot move — the zeros check the class assignment (an own signal that moves is
    misclassified) and the re-ranking's implementation — not the coupled readings (D-035); the
    tail operand for coupled signals is p95."""
    from repo_substrate.validation.config import GROUNDING

    repo, shas = scripted_repo
    full = cache.get(repo.path, "HEAD")
    pert = cache.get(repo.path, shas[-2], truncate=True)
    v = _vcfg(stability_perturbation_k=1, stability_min_n=1, stability_max_excluded_frac=0.9)
    out, _, _ = run_stability(full, pert, v)
    for sig, st in out.items():
        if st.get("max_abs_delta") is None or st.get("reason") == "degenerate":
            continue
        ripple = GROUNDING[sig].get("ripple", "own")
        assert st["ripple"] == ripple and st["operand"] == ("p95" if ripple == "coupled" else "max")
        if ripple == "own":
            assert st["max_abs_delta"] == 0.0, (sig, st)
