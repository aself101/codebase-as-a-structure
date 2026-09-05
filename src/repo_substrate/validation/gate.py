"""Combine per-repo results into per-signal verdicts and the validation.json
document (validation-spec §3.8, §2.4.4, §4, §6.1)."""

from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime
from typing import Any

from .asserted import RepoAsserted
from .config import GROUNDING, PREDICTIVE_SIGNALS, ValidationConfig
from .holdout import RepoHoldout

VALIDATION_VERSION = "0.2.0"


def _clean(v: Any) -> Any:
    """NaN → None for JSON; recurse."""
    if isinstance(v, float) and v != v:
        return None
    if isinstance(v, dict):
        return {k: _clean(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_clean(x) for x in v]
    return v


def predictive_verdict(sig: str, holdouts: list[RepoHoldout], vcfg: ValidationConfig) -> dict[str, Any]:
    per_repo = []
    passes = 0
    ran = 0
    for h in holdouts:
        entry: dict[str, Any] = {"name": h.name, "split_sha": h.split_sha, "coverage": h.coverage,
                                 "n_eligible": h.n_eligible, "holdout_positives": h.n_positives,
                                 "base_rate": h.base_rate, "degenerate": h.degenerate}
        m = h.signals.get(sig)
        if m is not None:
            entry.update({k: m[k] for k in ("roc_auc", "pr_auc", "precision_at_k", "recall_at_k", "passed",
                                            "failed_clauses", "best_baseline")})
            entry["baselines"] = h.baselines
        if h.degenerate is None and m is not None:
            ran += 1
            if m["passed"]:
                passes += 1
        per_repo.append(entry)
    if ran == 0:
        status = "untested"
        reason = "all_repos_degenerate"
    elif passes >= vcfg.min_repos:
        status, reason = "validated", None
    else:
        status, reason = "unvalidated", f"passed_on_{passes}_of_{ran}_repos_need_{vcfg.min_repos}"
    out = {"status": status, "kind": "predictive", "holdout": {"per_repo": per_repo, "passes": passes, "ran": ran}}
    if reason:
        out["reason"] = reason
    return out


def _repo_pass(sig: str, a: RepoAsserted, resolved: dict[str, dict[str, Any]]) -> tuple[bool, str | None]:
    """Per-repo pass for a descriptive signal under its grounding class."""
    st = a.stability.get(sig, {})
    if st.get("passed") is False:
        return False, "unstable"
    if st.get("passed") is None:
        return False, "no_stability_data"
    g = GROUNDING[sig]
    cls = g["class"]
    if cls == "G1":
        return True, None
    cm = a.corroboration.get(sig, {})
    if cls in ("G2", "G3"):
        if cm.get("passed") is True:
            return True, None
        return False, cm.get("reason") or "corroboration_fail"
    # G4: every input must already be asserted overall
    for inp in g["inputs"]:
        if resolved.get(inp, {}).get("status") != "asserted":
            return False, f"input_not_asserted:{inp}"
    return True, None


def descriptive_verdict(sig: str, asserted: list[RepoAsserted], vcfg: ValidationConfig,
                        resolved: dict[str, dict[str, Any]]) -> dict[str, Any]:
    g = GROUNDING[sig]
    per_repo = []
    passes = 0
    reasons: list[str] = []
    for a in asserted:
        ok, why = _repo_pass(sig, a, resolved)
        entry = {"name": a.name, "perturbed_sha": a.perturbed_sha, "passed": ok, "reason": why,
                 "stability": a.stability.get(sig, {}), "corroboration": a.corroboration.get(sig, {}),
                 "correlates": a.correlates.get(sig, {})}
        rec = a.recognition.get(sig)
        if rec:
            entry["recognition"] = {**rec, "ref": a.recognition_ref}
        per_repo.append(entry)
        if ok:
            passes += 1
        elif why:
            reasons.append(why)
    if passes >= vcfg.m_asserted:
        status, reason = "asserted", None
    else:
        status = "untested"
        # the most specific reason wins: an actual failure over an inability to test
        for cand in ("unstable", "corroboration_fail"):
            if cand in reasons:
                reason = cand
                break
        else:
            inp = next((r for r in reasons if r.startswith("input_not_asserted")), None)
            reason = inp or (reasons[0] if reasons else f"passed_on_{passes}_repos_need_{vcfg.m_asserted}")
    out = {"status": status, "kind": "descriptive", "grounding_class": g["class"],
           "counterpart": g.get("counterpart"), "inputs": g.get("inputs"), "instrument": g.get("instrument"),
           "grounding": {"per_repo": per_repo, "repos_passed": passes}}
    if reason:
        out["reason"] = reason
    return out


def build_validation(
    holdouts: list[RepoHoldout], asserted: list[RepoAsserted], vcfg: ValidationConfig,
    substrate_fingerprint: str, reference_repos: list[dict[str, Any]],
) -> dict[str, Any]:
    signals: dict[str, Any] = {}
    for sig in PREDICTIVE_SIGNALS:
        signals[sig] = predictive_verdict(sig, holdouts, vcfg)
    # G1–G3 first, then G4 in dependency order (inputs before the signals that read them).
    order = [s for s, g in GROUNDING.items() if g["class"] != "G4"]
    remaining = [s for s, g in GROUNDING.items() if g["class"] == "G4"]
    while remaining:
        progressed = False
        for s in list(remaining):
            if all(i in order for i in GROUNDING[s]["inputs"]):
                order.append(s)
                remaining.remove(s)
                progressed = True
        if not progressed:
            raise ValueError(f"cyclic or unknown G4 inputs: {remaining}")
    for sig in order:
        signals[sig] = descriptive_verdict(sig, asserted, vcfg, signals)
    # §3.8 kind/status legality is by construction here; assert it anyway so a refactor cannot break it.
    for name, s in signals.items():
        if s["kind"] == "predictive":
            assert s["status"] in ("validated", "unvalidated", "untested"), name
        else:
            assert s["status"] in ("asserted", "untested"), name
    doc = {
        "schema_version": "0.2",
        "validation_version": VALIDATION_VERSION,
        "validated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "substrate_config_fingerprint": substrate_fingerprint,
        "validation_config_fingerprint": vcfg.fingerprint([{"name": r["name"], "head_sha": r["head_sha"]} for r in reference_repos]),
        "validation_config": asdict(vcfg),
        "reference_repos": reference_repos,
        "signals": dict(sorted(signals.items())),
    }
    return _clean(doc)
