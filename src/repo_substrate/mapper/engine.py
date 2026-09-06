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
from .geometry import GEOMETRIES, compute_strata
from .ruleset import Feature, Ruleset, RulesetError, Term

SKELETON_SCHEMA = "0.1"
OK_STATUSES = ("validated", "asserted")


class GateError(RulesetError):
    """The anti-horoscope gate refused the ruleset."""


def _signal_status(validation: dict[str, Any], sig: str) -> str:
    return ((validation.get("signals") or {}).get(sig) or {}).get("status", "untested")


def _node_value(node: dict[str, Any], sig: str) -> float | None:
    """The value a predicate name denotes (D-017): an index by its index name; otherwise the
    RAW metric (so `fan_out == 0` means what it says); a percentile only for names that exist
    solely as percentiles (`*_nonzero`). `pNN` thresholds are ranked over these same values,
    so `fan_out >= p75` is the 75th percentile of raw fan_out. Booleans read as 0/1."""
    d = node.get("derived") or {}
    idx = d.get("indices") or {}
    if sig in idx:
        v = idx[sig]
        return None if isinstance(v, bool) else v
    if sig in node["metrics"]:
        v = node["metrics"].get(sig)
        if isinstance(v, bool):
            return 1.0 if v else 0.0
        return v
    return (d.get("percentiles") or {}).get(sig)


def check_gate(ruleset: Ruleset, validation: dict[str, Any]) -> dict[str, str]:
    """Return signal→status for every signal the ruleset reads; raise on a violation."""
    statuses: dict[str, str] = {}
    problems: list[str] = []
    # validation §3.8 / §5 (D-032): a predictive signal may not arrive labelled asserted, nor a
    # descriptive one validated — the relabel route by which a failed predictor re-enters as a
    # description. The producer asserts this; the consumer, which is handed the document, checks it.
    for name, rec in (validation.get("signals") or {}).items():
        kind, status = rec.get("kind"), rec.get("status")
        if (kind == "predictive" and status == "asserted") or (
            kind == "descriptive" and status == "validated"
        ):
            raise GateError(
                f"malformed validation.json: signal {name!r} is {kind} but carries status {status!r} (validation §3.8)"
            )
    for f in ruleset.features:
        for sig in f.signals:
            st = _signal_status(validation, sig)
            statuses[sig] = st
            if not f.decorative and st not in OK_STATUSES:
                problems.append(f"feature {f.name!r} reads {sig!r} with status {st!r}")
        if f.decorative:
            # D-030/D-032: the reason must name the signal that is actually ungrounded here —
            # the loader cannot know which one that is; the gate can
            ungrounded = [s for s in f.signals if statuses[s] not in OK_STATUSES]
            if ungrounded and not any(s in str(f.decorative_reason) for s in ungrounded):
                raise RulesetError(
                    f"feature {f.name!r}: decorative_reason names none of its ungrounded signals {ungrounded}"
                )
        for t in f.terms:
            if t.percentile is not None and (
                (validation.get("signals") or {}).get(t.signal) or {}
            ).get("flag"):
                raise RulesetError(
                    f"feature {f.name!r}: {t.signal!r} is a flag (never ranked) and may not carry a percentile threshold (D-029)"
                )
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


def _apply(
    ruleset: Ruleset,
    population: list[dict[str, Any]],
    statuses: dict[str, str],
    graph_degraded: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
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
                    "profile": ruleset.profile,
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
    summary = {
        "feature_counts": dict(sorted(counts.items())),
        "diagnostic_count": sum(1 for x in features_out if x["diagnostic"]),
        "decorative_count": sum(1 for x in features_out if x["decorative"]),
        "degraded_count": sum(1 for x in features_out if x["degraded"]),
        "decorative_features": sorted(decorative_features),
    }
    return features_out, summary


def map_skeleton(
    substrate: dict[str, Any],
    validation: dict[str, Any],
    ruleset: Ruleset,
    overlays: tuple[Ruleset, ...] = (),
    geometry: str = "age",
) -> dict[str, Any]:
    """Base profile → `features`; further profiles → `overlays[]`, each gated on its own.
    Geometry (strata, wings) comes from the substrate and the `geometry` choice, never from
    a profile (mapper §6: layering, never unification)."""
    if geometry not in GEOMETRIES:
        raise RulesetError(f"unknown geometry {geometry!r}")
    profiles = [ruleset.profile] + [o.profile for o in overlays]
    if len(set(profiles)) != len(profiles):
        raise RulesetError(f"duplicate profile among base and overlays: {profiles}")
    statuses = check_gate(ruleset, validation)
    for o in overlays:
        statuses.update(check_gate(o, validation))
    population = [
        n
        for n in substrate["nodes"]
        if (n.get("derived") or {}).get("indices") is not None and not n["metrics"].get("is_test")
    ]
    graph_degraded = bool(substrate["summary"].get("graph_degraded"))
    features_out, summary = _apply(ruleset, population, statuses, graph_degraded)
    overlay_docs = []
    for o in overlays:
        of, osum = _apply(o, population, statuses, graph_degraded)
        overlay_docs.append(
            {
                "profile": o.profile,
                "ruleset": {"name": o.name, "version": o.version, "source": o.source},
                "features": of,
                "summary": osum,
            }
        )
    strata, strata_raw = compute_strata(population, substrate, geometry)
    # co-location (mapper §6): nodes flagged by more than one profile are shown, never averaged
    by_node_profiles: dict[str, set[str]] = {}
    for x in features_out:
        if x["diagnostic"]:
            by_node_profiles.setdefault(x["node"], set()).add(x["profile"])
    for od in overlay_docs:
        for x in od["features"]:
            if x["diagnostic"]:
                by_node_profiles.setdefault(x["node"], set()).add(x["profile"])
    co_located = sorted(n for n, ps in by_node_profiles.items() if len(ps) > 1)
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
        "archetype": None,  # D-019: not claimed in v0 — a whole-building label is corpus-relative (Phase 3)
        "gate": {"signals": dict(sorted(statuses.items())), "graph_degraded": graph_degraded},
        "geometry": {"name": geometry, "wing_depth": ruleset.wing_depth},
        "strata": {
            "geometry": geometry,
            "bands": 5,
            "by_node": dict(sorted(strata.items())),
            "raw_by_node": dict(sorted(strata_raw.items())),
        },
        "features": features_out,
        "overlays": overlay_docs,
        "co_located_nodes": co_located,
        "summary": {
            "population": len(population),
            **summary,
            "overlay_profiles": [o.profile for o in overlays],
            "co_located_count": len(co_located),
        },
    }
    payload = json.dumps({k: v for k, v in doc.items() if k != "mapped_at"}, sort_keys=True)
    doc["skeleton_hash"] = hashlib.sha256(payload.encode()).hexdigest()
    return doc
