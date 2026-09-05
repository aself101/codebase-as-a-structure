"""Apply a ruleset to a substrate under the gate; emit skeleton.json (mapper spec §3–§6).

Gate (mapper §3, validation §5): before any predicate is evaluated, every signal a
non-decorative feature reads must have status `validated` or `asserted` in validation.json.
A missing key is `untested`. Any violation is a hard error: the skeleton is not emitted.

Feature status (mapper §5): the most conservative claim type across all signals read —
`validated` only if every signal is validated, else `asserted`; a decorative feature
carries the worst status among its signals and is excluded from diagnostic claims.

Graph gating (mapper §4.1): a `graph_dependent` feature is emitted with `degraded: true`
and excluded from diagnostic claims when the substrate's graph is degraded or the node's
`load_index_degraded` is set. Degrading is not suppressing: the geometry still exists.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any

from .. import __version__
from ..derived import ecdf_percentiles
from .ruleset import Feature, Ruleset, RulesetError, Term

SKELETON_SCHEMA = "0.1"
OK_STATUSES = ("validated", "asserted")


class GateError(RulesetError):
    """The anti-horoscope gate refused the ruleset."""


def _signal_status(validation: dict[str, Any], sig: str) -> str:
    return ((validation.get("signals") or {}).get(sig) or {}).get("status", "untested")


def _node_value(node: dict[str, Any], sig: str) -> float | None:
    d = node.get("derived") or {}
    idx = d.get("indices") or {}
    if sig in idx:
        v = idx[sig]
        return None if isinstance(v, bool) else v
    pct = d.get("percentiles") or {}
    if sig in pct:
        return pct[sig]
    v = node["metrics"].get(sig)
    if isinstance(v, bool):
        return 1.0 if v else 0.0
    return v


def check_gate(ruleset: Ruleset, validation: dict[str, Any]) -> dict[str, str]:
    """Return signal→status for every signal the ruleset reads; raise on a violation."""
    statuses: dict[str, str] = {}
    problems: list[str] = []
    for f in ruleset.features:
        for sig in f.signals:
            st = _signal_status(validation, sig)
            statuses[sig] = st
            if not f.decorative and st not in OK_STATUSES:
                problems.append(f"feature {f.name!r} reads {sig!r} with status {st!r}")
    if problems:
        raise GateError(
            "anti-horoscope gate: "
            + "; ".join(problems)
            + ". Re-ground the signal, or tag the rule decorative = true with a decorative_reason."
        )
    return statuses


def _feature_status(f: Feature, statuses: dict[str, str]) -> str:
    sts = [statuses[s] for s in f.signals]
    if any(s not in OK_STATUSES for s in sts):
        # only reachable for decorative features (the gate rejected the others)
        return "untested" if "untested" in sts else "unvalidated"
    return "validated" if all(s == "validated" for s in sts) else "asserted"


def _resolve_thresholds(
    terms: tuple[Term, ...], population: list[dict[str, Any]]
) -> dict[tuple[str, int], float]:
    """pNN → the NN-th percentile value of that signal across the population
    (linear interpolation on the sorted values; deterministic)."""
    out: dict[tuple[str, int], float] = {}
    for t in terms:
        if t.percentile is None:
            continue
        vals = sorted(v for v in (_node_value(n, t.signal) for n in population) if v is not None)
        if not vals:
            out[(t.signal, t.percentile)] = float("inf")
            continue
        k = (len(vals) - 1) * t.percentile / 100.0
        lo, hi = int(k), min(int(k) + 1, len(vals) - 1)
        out[(t.signal, t.percentile)] = vals[lo] + (vals[hi] - vals[lo]) * (k - lo)
    return out


def _cmp(v: float, op: str, thr: float) -> bool:
    return {
        ">=": v >= thr,
        "<=": v <= thr,
        ">": v > thr,
        "<": v < thr,
        "==": abs(v - thr) < 1e-12,
    }[op]


def map_skeleton(
    substrate: dict[str, Any], validation: dict[str, Any], ruleset: Ruleset
) -> dict[str, Any]:
    statuses = check_gate(ruleset, validation)
    population = [
        n
        for n in substrate["nodes"]
        if (n.get("derived") or {}).get("indices") is not None and not n["metrics"].get("is_test")
    ]
    graph_degraded = bool(substrate["summary"].get("graph_degraded"))
    features_out: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    decorative_features: set[str] = set()
    for f in ruleset.features:
        thr = _resolve_thresholds(f.terms, population)
        f_status = _feature_status(f, statuses)
        resolved = {
            t.render(): (thr[(t.signal, t.percentile)] if t.percentile is not None else t.value)
            for t in f.terms
        }
        for n in sorted(population, key=lambda x: x["id"]):
            fired = True
            evidence: dict[str, Any] = {}
            for t in f.terms:
                v = _node_value(n, t.signal)
                evidence[t.signal] = v
                if v is None:
                    fired = False
                    break
                th = thr[(t.signal, t.percentile)] if t.percentile is not None else t.value
                if not _cmp(float(v), t.op, float(th)):
                    fired = False
                    break
            if not fired:
                continue
            degraded = f.graph_dependent and (
                graph_degraded or bool((n["derived"]["indices"] or {}).get("load_index_degraded"))
            )
            diagnostic = (not f.decorative) and (not degraded)
            features_out.append(
                {
                    "feature": f.name,
                    "node": n["id"],
                    "predicate": f.predicate,
                    "thresholds": resolved,
                    "evidence": evidence,
                    "signals": {s: statuses[s] for s in f.signals},
                    "validation_status": f_status,
                    "decorative": f.decorative,
                    "decorative_reason": f.decorative_reason,
                    "degraded": degraded,
                    "diagnostic": diagnostic,
                    "name_implies_consequence": f.name_implies_consequence,
                    "position_name": f.position_name,
                }
            )
            counts[f.name] = counts.get(f.name, 0) + 1
            if f.decorative:
                decorative_features.add(f.name)
    # strata: the vertical dimension of the cutaway, profile-independent (§6): percentile of
    # the strata signal over the population, bucketed into five bands (0 = oldest/bottom).
    strata_vals = {n["id"]: _node_value(n, ruleset.strata_signal) for n in population}
    strata_pct = ecdf_percentiles(strata_vals)
    strata = {
        nid: (min(4, int((1.0 - (p or 0.0)) * 5)) if p is not None else 2)
        for nid, p in strata_pct.items()
    }
    doc = {
        "schema_version": SKELETON_SCHEMA,
        "mapper_version": __version__,
        "mapped_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "ruleset": {"name": ruleset.name, "version": ruleset.version, "source": ruleset.source},
        "profile": {"name": ruleset.profile, "version": ruleset.version},
        "substrate_seed": substrate["seed"],
        "substrate_config_fingerprint": substrate["repo"]["config_fingerprint"],
        "validation_config_fingerprint": validation.get("validation_config_fingerprint"),
        "repo": {"name": substrate["repo"]["name"], "head_sha": substrate["repo"]["head_sha"]},
        "archetype": None,  # mapper §7 Q1: unresolved in v0 — and therefore not claimed
        "gate": {"signals": dict(sorted(statuses.items())), "graph_degraded": graph_degraded},
        "strata": {
            "signal": ruleset.strata_signal,
            "bands": 5,
            "by_node": dict(sorted(strata.items())),
        },
        "features": features_out,
        "overlays": [],
        "summary": {
            "population": len(population),
            "feature_counts": dict(sorted(counts.items())),
            "diagnostic_count": sum(1 for x in features_out if x["diagnostic"]),
            "decorative_count": sum(1 for x in features_out if x["decorative"]),
            "degraded_count": sum(1 for x in features_out if x["degraded"]),
            "decorative_features": sorted(decorative_features),
        },
    }
    payload = json.dumps({k: v for k, v in doc.items() if k != "mapped_at"}, sort_keys=True)
    doc["skeleton_hash"] = hashlib.sha256(payload.encode()).hexdigest()
    return doc
