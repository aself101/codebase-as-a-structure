"""Combine per-repo results into per-signal verdicts and the validation.json
document (validation-spec §3.8, §2.4.4, §4, §6.1; D-009 roles; D-011)."""

from __future__ import annotations

import math
from dataclasses import asdict
from datetime import UTC, datetime
from typing import Any

from .asserted import RepoAsserted
from .config import GROUNDING, PREDICTIVE_SIGNALS, ValidationConfig
from .holdout import RepoHoldout

VALIDATION_VERSION = "0.3.0"


def _clean(v: Any) -> Any:
    """NaN → None for JSON; recurse."""
    if isinstance(v, float) and math.isnan(v):
        return None
    if isinstance(v, dict):
        return {k: _clean(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_clean(x) for x in v]
    return v


def predictive_verdict(
    sig: str,
    holdouts: list[RepoHoldout],
    roles: dict[str, str],
    vcfg: ValidationConfig,
    asserted: list[RepoAsserted] | None = None,
) -> dict[str, Any]:
    """D-009: only repos with role == "test" count toward `validated`. Tuning repos are
    scored and reported (in-sample) but cannot confer or block the verdict."""
    per_repo = []
    passes = 0
    ran = 0
    recog_by_repo = {a.name: (a.recognition.get(sig), a.recognition_ref) for a in (asserted or [])}
    for h in holdouts:
        role = roles.get(h.name, "test")
        entry: dict[str, Any] = {
            "name": h.name,
            "role": role,
            "split_sha": h.split_sha,
            "coverage": h.coverage,
            "n_eligible": h.n_eligible,
            "holdout_positives": h.n_positives,
            "base_rate": h.base_rate,
            "degenerate": h.degenerate,
        }
        rec, ref = recog_by_repo.get(h.name, (None, None))
        if rec:
            entry["recognition"] = {**rec, "ref": ref}
        m = h.signals.get(sig)
        if m is not None:
            entry.update(
                {
                    k: m[k]
                    for k in (
                        "roc_auc",
                        "pr_auc",
                        "precision_at_k",
                        "recall_at_k",
                        "passed",
                        "failed_clauses",
                        "best_baseline",
                        "tau_vs_best_baseline",
                    )
                }
            )
            entry["baselines"] = h.baselines
        if role == "test" and h.degenerate is None and m is not None:
            ran += 1
            if m["passed"]:
                passes += 1
        per_repo.append(entry)
    n_test = sum(1 for h in holdouts if roles.get(h.name, "test") == "test")
    if n_test == 0:
        status, reason = "untested", "no_test_repos"
    elif ran == 0:
        status, reason = "untested", "all_test_repos_degenerate"
    elif passes >= vcfg.min_repos:
        status, reason = "validated", None
    else:
        status, reason = (
            "unvalidated",
            f"passed_on_{passes}_of_{ran}_test_repos_need_{vcfg.min_repos}",
        )
    out: dict[str, Any] = {
        "status": status,
        "kind": "predictive",
        "holdout": {
            "per_repo": per_repo,
            "test_passes": passes,
            "test_ran": ran,
            "n_test_repos": n_test,
        },
    }
    if reason:
        out["reason"] = reason
    return out


def _repo_pass(
    sig: str, a: RepoAsserted, resolved: dict[str, dict[str, Any]]
) -> tuple[bool, str | None]:
    """Per-repo pass for a descriptive signal under its grounding class."""
    st = a.stability.get(sig, {})
    if st.get("passed") is not True:
        return False, st.get("reason") or "no_stability_data"
    g = GROUNDING[sig]
    cls = g["class"]
    if cls in ("G2", "G3"):
        cm = a.corroboration.get(sig, {})
        if cm.get("passed") is not True:
            return False, cm.get("reason") or "corroboration_fail"
    if cls in ("G3", "G4"):
        for inp in g.get("inputs", []):
            if resolved.get(inp, {}).get("status") != "asserted":
                return False, f"input_not_asserted:{inp}"
    return True, None


def descriptive_verdict(
    sig: str,
    asserted: list[RepoAsserted],
    vcfg: ValidationConfig,
    resolved: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    g = GROUNDING[sig]
    per_repo = []
    passes = 0
    reasons: list[str] = []
    lower_cis: list[float] = []
    for a in asserted:
        ok, why = _repo_pass(sig, a, resolved)
        entry = {
            "name": a.name,
            "perturbed_sha": a.perturbed_sha,
            "passed": ok,
            "reason": why,
            "stability": a.stability.get(sig, {}),
            "corroboration": a.corroboration.get(sig, {}),
            "correlates": a.correlates.get(sig, {}),
        }
        per_repo.append(entry)
        ci = (a.corroboration.get(sig) or {}).get("tau_b_ci")
        if ci and ci[0] is not None and not math.isnan(ci[0]):
            lower_cis.append(ci[0])
        if ok:
            passes += 1
        elif why:
            reasons.append(why)
    reason: str | None
    if passes >= vcfg.m_asserted:
        status, reason = "asserted", None
    else:
        status = "untested"
        # the most specific reason wins: an actual failure over an inability to test
        for cand in ("degenerate", "unstable", "corroboration_fail"):
            if cand in reasons:
                reason = cand
                break
        else:
            inp = next((r for r in reasons if r.startswith("input_not_asserted")), None)
            reason = inp or (
                reasons[0] if reasons else f"passed_on_{passes}_repos_need_{vcfg.m_asserted}"
            )
    # D-011 retirement criterion: a counterpart that cannot fail is not a falsifier.
    non_discriminating = (
        bool(lower_cis) and len(lower_cis) == len(asserted) and min(lower_cis) >= vcfg.tau_retire
    )
    out: dict[str, Any] = {
        "status": status,
        "kind": "descriptive",
        "grounding_class": g["class"],
        "flag": bool(g.get("flag", False)),
        "counterpart": g.get("counterpart"),
        "inputs": g.get("inputs"),
        "instrument": g.get("instrument"),
        "heuristic": g.get("heuristic"),
        "non_discriminating": non_discriminating if g["class"] in ("G2", "G3") else None,
        # D-014: a pair that cannot fail on the reference set still counts if a committed adversarial
        # fixture proves it can fail on constructed input; without one it would not.
        "adversarial_fixture": g.get("adversarial_fixture"),
        "retirement_backed": (bool(g.get("adversarial_fixture")) if non_discriminating else None),
        "grounding": {"per_repo": per_repo, "repos_passed": passes},
    }
    if reason:
        out["reason"] = reason
    return out


def _resolution_order() -> list[str]:
    """G1/G2 and input-free G3 first, then anything with inputs in dependency order."""
    order = [s for s, g in GROUNDING.items() if not g.get("inputs")]
    remaining = [s for s, g in GROUNDING.items() if g.get("inputs")]
    while remaining:
        progressed = False
        for s in list(remaining):
            if all(i in order for i in GROUNDING[s]["inputs"]):
                order.append(s)
                remaining.remove(s)
                progressed = True
        if not progressed:
            raise ValueError(f"cyclic or unknown grounding inputs: {remaining}")
    return order


def build_validation(
    holdouts: list[RepoHoldout],
    asserted: list[RepoAsserted],
    vcfg: ValidationConfig,
    substrate_fingerprint: str,
    reference_repos: list[dict[str, Any]],
    tuned_config_commit: str | None = None,
    substrate_effective_config: dict[str, Any] | None = None,
    substrate_attestations: dict[str, dict[str, str]] | None = None,
) -> dict[str, Any]:
    roles = {r["name"]: r.get("role", "test") for r in reference_repos}
    signals: dict[str, Any] = {}
    for sig in PREDICTIVE_SIGNALS:
        signals[sig] = predictive_verdict(sig, holdouts, roles, vcfg, asserted)
    for sig in _resolution_order():
        signals[sig] = descriptive_verdict(sig, asserted, vcfg, signals)
    # §3.8 kind/status legality is by construction here; assert it anyway so a refactor cannot break it.
    for name, s in signals.items():
        if s["kind"] == "predictive":
            assert s["status"] in ("validated", "unvalidated", "untested"), name
        else:
            assert s["status"] in ("asserted", "untested"), name
    doc = {
        "schema_version": "0.3",
        "validation_version": VALIDATION_VERSION,
        "validated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "substrate_config_fingerprint": substrate_fingerprint,
        "validation_config_fingerprint": vcfg.fingerprint(
            [
                {"name": r["name"], "head_sha": r["head_sha"], "role": r.get("role", "test")}
                for r in reference_repos
            ]
        ),
        "validation_config": asdict(vcfg),
        # The substrate fingerprint's preimage (circumvention A7): what weights and toolchain these verdicts validate.
        "substrate_effective_config": substrate_effective_config,
        # Per cached document: seed + sha256 of the bytes scored (circumvention A2 / audit: cache poisoning).
        "substrate_attestations": dict(sorted((substrate_attestations or {}).items())),
        "tuned_config_commit": tuned_config_commit,
        "reference_repos": reference_repos,
        "signals": dict(sorted(signals.items())),
    }
    return _clean(doc)
