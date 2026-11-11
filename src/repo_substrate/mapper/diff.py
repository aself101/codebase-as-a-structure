"""Skeleton diff (mapper §7 Q3, system spec §8; D-017): how much did the named structure
move between two skeletons of the same repository?

The measure the stability budget needs is feature churn over nodes present in both
skeletons: for each (profile, feature), the set of nodes it fired on before and after,
the symmetric difference, and the Jaccard similarity. Nodes born or deleted between the
two revisions are excluded from churn (they are structural change, not jitter) and
counted separately. This is the same discipline as the signal-level budget
(validation §2.4.1): measure the movement of what did not itself change.

The budget (D-018) is applied one step further along the same line: a node the
intervening commits *edited* may legitimately change feature or stratum — that is the
skeleton reporting the edit. A node they did *not* edit that changes anyway moved by
ripple — a percentile threshold shifted under it, or a dependency's layer depth changed —
and ripple is the jitter a time-lapse must not show. So the budget is judged over the
**untouched** population, with the same floors as the signal-level budget: enough
untouched nodes to mean something, and not so many touched that the test gets easier
as the edit grows. The whole-population numbers are reported beside it because they are
what a reader of two adjacent pictures actually sees.
"""

from __future__ import annotations

import math
from typing import Any

from .engine import _cmp, _node_value, _resolve_thresholds
from .ruleset import parse_predicate

# D-018, operand revised D-024, K re-pinned D-026, meaning restated D-082. The budget
# bounds JITTER: movement of untouched rooms through rank-only features, mixed features (a
# clock and a rank signal in one predicate — the rank component cannot be separated, so
# the whole is counted as jitter, the conservative side), and strata (a floor moves for an
# untouched room only because the population re-ranked around it, D-022 having removed
# the clock's way of moving it). Clock-only features are reported beside it, never judged.
#
# Two operands, either one over its ceiling is `over_budget`: 5% of the (profile, feature,
# room) assignments of rank and mixed features held by untouched rooms, and 5% of untouched
# rooms for strata. The units differ, and one threshold crossing can be several assignments
# (one predicate under two profiles; two predicates sharing a term), so the budget block
# states each operand's unit, the smallest count that exceeds its ceiling (`fires_at`),
# and the distinct crossings (D-082).
#
# The K. At K = 5 nothing fires the ceiling, not the reference set and not a ruleset
# written to break it (D-024). The K study (D-025/D-026, reports/2026-09-05-kstudy;
# substrate 0.3.0) read jitter churn per transition and found it grows with K at a rate set
# by the repository's growth. Its readings, each at the K named: registry K = 25 median
# 0.034 / p90 0.143; mcp-secure-server K = 10 0.022 / 0.066; typeorm K = 50 0.027 / 0.235;
# eslint K = 100 0.028 / 0.125. K = 25 was read on the registry only; 25 is pinned as the
# smallest K at which the ceiling sat between median and p90 where it was read, applied up
# to 50, `untested: beyond_pinned_k` past that. The calibration has not been read on a
# population under about 200 rooms, and on the 65-room mcp-secure-server D-026's breaks-if
# is met for layer strata (D-082; reports/2026-11-11-stability). A verdict is therefore a
# statement about ONE WINDOW: whether it is typical or tail for the population is read
# separately.
#
# Floors. A jitter union under `min_jitter_union` assignments is
# `untested: insufficient_jitter_population`. The floors do not make the operand a rate at
# every admitted size: at the minimum union (20) and the minimum untouched population (30)
# each ceiling is exceeded by two units. D-026's comment here said "two rooms flipping is
# not a rate"; the floors never enforced that and the sentence is withdrawn (D-082) — the
# resolution travels on the datum instead of being asserted by a floor.
SKELETON_BUDGET: dict[str, float | int] = {
    "feature_churn_max": 0.05,
    "strata_moved_max": 0.05,
    "min_untouched_n": 30,
    "max_touched_frac": 0.5,
    "pinned_k": 25,
    "max_k": 50,
    "min_jitter_union": 20,
}

# Signals measured against the checkpoint's clock (substrate spec §5, §7; D-021). A feature
# over these alone is `clock`; over none of these is `rank`; over both kinds is `mixed`.
# Membership is pinned by test (D-024) against the substrate spec's own list.
CLOCK_SIGNALS = frozenset(
    {
        "age_days",
        "last_touched_days",
        "blame_age_median",
        "recent_commit_share",
        "neglect_index",
        "change_pressure_index",
    }
)


def classify_signals(signals) -> str:
    """'clock' | 'rank' | 'mixed' for the set of signals one predicate reads."""
    sig = set(signals)
    if not sig:
        return "rank"
    clock = {s for s in sig if s in CLOCK_SIGNALS}
    if clock == sig:
        return "clock"
    if not clock:
        return "rank"
    return "mixed"


def feature_kinds_from_skeleton(*skeletons: dict[str, Any]) -> dict[str, str]:
    """(profile/feature) → kind, read from the signals each fired feature records as
    evidence — so a diff of two skeletons needs no ruleset to classify movement."""
    signals: dict[str, set[str]] = {}
    for sk in skeletons:
        groups = [sk.get("features") or []] + [od["features"] for od in sk.get("overlays") or []]
        for feats in groups:
            for f in feats:
                key = f"{f['profile']}/{f['feature']}"
                signals.setdefault(key, set()).update((f.get("evidence") or {}).keys())
    return {k: classify_signals(v) for k, v in signals.items()}


def canonicalize(path: str, renames: dict[str, str]) -> str:
    """Chase a name through the renames map to the name current at the AFTER revision."""
    seen: set[str] = set()
    while path in renames and path not in seen:
        seen.add(path)
        path = renames[path]
    return path


def touched_since(
    substrate: dict[str, Any], before_sha: str, renames: dict[str, str] | None = None
) -> tuple[set[str], int] | None:
    """Nodes edited by the commits after `before_sha` in the AFTER substrate's timeline,
    in after-revision names, plus the number of those commits. None when `before_sha`
    is not in the timeline (the two skeletons are not on one recorded line)."""
    renames = renames or {}
    tl = substrate.get("timeline") or []
    idx = next((i for i, e in enumerate(tl) if e.get("sha") == before_sha), None)
    if idx is None:
        return None
    touched: set[str] = set()
    for e in tl[idx + 1 :]:
        for n in e.get("nodes_touched") or []:
            seen: set[str] = set()
            while n in renames and n not in seen:
                seen.add(n)
                n = renames[n]
            touched.add(n)
    return touched, len(tl) - idx - 1


def window_commits_since(substrate: dict[str, Any], before_sha: str) -> list[dict[str, Any]] | None:
    """The timeline entries `touched_since` counts — the same slice, so a window's dates are
    read over exactly the commits its touched set was (D-083). None as `touched_since`."""
    tl = substrate.get("timeline") or []
    idx = next((i for i, e in enumerate(tl) if e.get("sha") == before_sha), None)
    if idx is None:
        return None
    return [{"sha": e.get("sha"), "ts": e.get("ts")} for e in tl[idx + 1 :]]


def window_commits_between(before_sub: dict[str, Any], after_sub: dict[str, Any]) -> list[dict[str, Any]]:
    """The timeline entries `touched_between` counts (reachability, not timestamp order)."""
    before = {e.get("sha") for e in before_sub.get("timeline") or []}
    return [
        {"sha": e.get("sha"), "ts": e.get("ts")}
        for e in after_sub.get("timeline") or []
        if e.get("sha") not in before
    ]


def _window_times(a_sha: str | None, b_sha: str | None, commits: list[dict[str, Any]] | None,
                  after_substrate: dict[str, Any] | None) -> dict[str, Any]:
    """Timestamps of a window, as recorded (D-083). `first_ts`/`last_ts` are the earliest and
    latest INSTANT over the commits the caller counted — timeline order is by reachability, so
    the endpoints do not bound it. Null, never guessed, when the list or a timestamp is missing."""
    from datetime import datetime

    out: dict[str, Any] = {"before_ts": None, "after_ts": None, "first_ts": None, "last_ts": None,
                           "commit_count": len(commits) if commits is not None else None}
    by_sha = {e.get("sha"): e.get("ts") for e in (after_substrate or {}).get("timeline") or []}
    out["before_ts"], out["after_ts"] = by_sha.get(a_sha), by_sha.get(b_sha)
    if not commits or any(not c.get("ts") for c in commits):
        return out
    try:
        keyed = sorted(commits, key=lambda c: datetime.fromisoformat(c["ts"]))
    except (TypeError, ValueError):
        return out
    out["first_ts"], out["last_ts"] = keyed[0]["ts"], keyed[-1]["ts"]
    return out


def _side_identity(sk: dict[str, Any]) -> dict[str, Any]:
    rs = sk.get("ruleset") or {}
    return {
        "ruleset": {"name": rs.get("name"), "version": rs.get("version")},
        "overlays": [
            {"name": (o.get("ruleset") or {}).get("name"), "version": (o.get("ruleset") or {}).get("version")}
            for o in sk.get("overlays") or []
        ],
        # base profile first, then overlays in their order: the page names a row's profiles so
        "profiles": [(sk.get("profile") or {}).get("name")] + [o.get("profile") for o in sk.get("overlays") or []],
        "mapper_version": sk.get("mapper_version"),
        "substrate_config_fingerprint": sk.get("substrate_config_fingerprint"),
        "validation_config_fingerprint": sk.get("validation_config_fingerprint"),
    }


def _predicates(*skeletons: dict[str, Any]) -> dict[tuple[str, str], str]:
    """(profile, feature) → predicate text, from the roster where there is one and from the
    fired records otherwise."""
    out: dict[tuple[str, str], str] = {}
    for sk in skeletons:
        groups = [(sk.get("profile", {}).get("name"), sk.get("profile", {}).get("roster", []))]
        groups += [(o.get("profile"), o.get("roster", [])) for o in sk.get("overlays", [])]
        for prof, roster in groups:
            for f in roster or []:
                out.setdefault((prof, f["feature"]), f["predicate"])
        for feats in [sk.get("features") or []] + [o["features"] for o in sk.get("overlays") or []]:
            for f in feats:
                if f.get("predicate"):
                    out.setdefault((f["profile"], f["feature"]), f["predicate"])
    return out


def _position_names(*skeletons: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    """(profile, feature) → the ruleset's position name and its name_implies_consequence flag
    (D-074: a flagged name is paired with its position wherever it is read as a label). From
    the roster where there is one, the fired records otherwise."""
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for sk in skeletons:
        groups = [(sk.get("profile", {}).get("name"), sk.get("profile", {}).get("roster", []))]
        groups += [(o.get("profile"), o.get("roster", [])) for o in sk.get("overlays", [])]
        fired = [(f["profile"], f) for feats in
                 [sk.get("features") or []] + [o["features"] for o in sk.get("overlays") or []] for f in feats]
        for prof, f in [(p, f) for p, roster in groups for f in roster or []] + fired:
            out.setdefault((prof, f["feature"]), {
                "position_name": f.get("position_name"),
                "name_implies_consequence": bool(f.get("name_implies_consequence")),
            })
    return out


def _feature_sets(
    skeleton: dict[str, Any], decorative: bool = False
) -> dict[tuple[str, str], set[str]]:
    """Fired-node sets per (profile, feature) — diagnostic by default; `decorative=True`
    returns the decorative ones instead, so their flicker is reported too (D-030: the hatch
    excludes a feature from diagnosis, not from measurement)."""
    sets: dict[tuple[str, str], set[str]] = {}
    groups = [skeleton["features"]] + [od["features"] for od in skeleton.get("overlays") or []]
    for feats in groups:
        for f in feats:
            if bool(f["decorative"]) == decorative and (decorative or f["diagnostic"]):
                sets.setdefault((f["profile"], f["feature"]), set()).add(f["node"])
    return sets


def touched_between(
    before_sub: dict[str, Any], after_sub: dict[str, Any], renames: dict[str, str] | None = None
) -> tuple[set[str], int]:
    """Exact form of `touched_since` when both substrates are at hand (time-lapse §4): the
    nodes touched by commits present in the AFTER timeline and absent from the BEFORE
    timeline, in after-revision names, plus the number of those commits. Reachability,
    not timestamp order — a commit merged late but authored early is counted."""
    renames = renames or {}
    before = {e.get("sha") for e in before_sub.get("timeline") or []}
    touched: set[str] = set()
    n = 0
    for e in after_sub.get("timeline") or []:
        if e.get("sha") in before:
            continue
        n += 1
        for node in e.get("nodes_touched") or []:
            seen: set[str] = set()
            while node in renames and node not in seen:
                seen.add(node)
                node = renames[node]
            touched.add(node)
    return touched, n


def fires_at(ceiling: float, denominator: int) -> int | None:
    """The smallest whole count whose share of `denominator` exceeds `ceiling` under the
    verdict's own strict comparison (D-082). None when there is nothing to divide by."""
    if denominator <= 0:
        return None
    n = max(0, int(ceiling * denominator) - 1)
    while n / denominator <= ceiling:
        n += 1
    return n


def _distinct_crossings(per_feature: dict[str, Any]) -> tuple[int | None, str | None]:
    """Distinct (room, predicate term) pairs whose outcome differs between the two frames,
    over the untouched rooms of rank and mixed features (D-082). One room leaving two
    features that share a term is one crossing. Unknown — not zero — when either side's
    evidence is unavailable for any changed assignment."""
    seen: set[tuple[str, str]] = set()
    for pf in per_feature.values():
        if pf["kind"] not in ("rank", "mixed"):
            continue
        for room in pf["untouched_affected_rooms"]:
            ev = pf["transition_evidence"].get(room) or {}
            before, after = ev.get("before") or {}, ev.get("after") or {}
            tb, ta = before.get("terms"), after.get("terms")
            if (before.get("availability") != "available" or after.get("availability") != "available"
                    or tb is None or ta is None or len(tb) != len(ta)):
                return None, "transition_evidence_unavailable"
            for x, y in zip(tb, ta):
                if x["passed"] is None or y["passed"] is None:
                    return None, "term_outcome_unknown"
                if x["passed"] != y["passed"]:
                    seen.add((room, x["term"]))
    return len(seen), None


def _verify_substrate(skeleton: dict[str, Any], substrate: dict[str, Any] | None) -> None:
    if substrate is None:
        return
    for label, actual, expected in (
        ("revision", substrate["repo"]["head_sha"], skeleton["repo"]["head_sha"]),
        ("config fingerprint", substrate["repo"]["config_fingerprint"], skeleton.get("substrate_config_fingerprint")),
        ("seed", substrate.get("seed"), skeleton.get("substrate_seed")),
    ):
        if actual != expected:
            raise ValueError(f"transition substrate {label} does not match its skeleton")


def _transition_context(sk: dict[str, Any], sub: dict[str, Any] | None,
                        profile: str, feature: str) -> dict[str, Any]:
    population_ids = set(sk["strata"]["by_node"])
    context: dict[str, Any] = {"population_n": len(population_ids),
        "population_floor": sk.get("gate", {}).get("population_floor"),
        "population_ids": population_ids}
    if sub is None:
        return {**context, "availability": "unavailable", "reason": "substrate_not_supplied"}
    groups = [(sk.get("profile", {}).get("name"), sk.get("profile", {}).get("roster", []))]
    groups += [(o["profile"], o.get("roster", [])) for o in sk.get("overlays", [])]
    definition = next((f for p, roster in groups if p == profile for f in roster
                       if f["feature"] == feature), None)
    if definition is None:
        return {**context, "availability": "unavailable", "reason": "feature_definition_missing"}
    nodes = {n["id"]: n for n in sub["nodes"]}
    if not population_ids <= nodes.keys():
        raise ValueError("transition substrate is missing skeleton population nodes")
    terms = parse_predicate(definition["predicate"])
    return {**context, "availability": "available", "definition": definition,
            "nodes": nodes, "terms": terms,
            "thresholds": _resolve_thresholds(terms, [nodes[n] for n in population_ids]),
            "gate": sk.get("gate", {})}


def _transition_side(context: dict[str, Any], node: str) -> dict[str, Any]:
    side: dict[str, Any] = {"availability": context["availability"],
        "population_n": context["population_n"], "room_eligible": node in context["population_ids"],
        "population_floor": context["population_floor"]}
    if context["availability"] != "available":
        return {**side, "reason": context["reason"], "predicate_passed": None,
                "diagnostic_eligible": None}
    nd = context["nodes"].get(node)
    if nd is None:
        return {**side, "availability": "unavailable", "reason": "node_missing",
                "predicate_passed": None, "diagnostic_eligible": None}
    terms = []
    for t in context["terms"]:
        value = _node_value(nd, t.signal)
        threshold = context["thresholds"].get((t.signal, t.percentile)) if t.percentile is not None else t.value
        finite = threshold is not None and math.isfinite(threshold)
        passed = _cmp(float(value), t.op, float(threshold)) if value is not None and finite else None
        terms.append({"term": t.render(), "signal": t.signal, "operator": t.op,
                      "value": value, "threshold": threshold if finite else None, "passed": passed,
                      "reason": "value_unavailable" if value is None else (None if finite else "threshold_unavailable")})
    outcomes = [t["passed"] for t in terms]
    predicate_passed = False if False in outcomes else (None if None in outcomes else True)
    definition, gate = context["definition"], context["gate"]
    graph_dependent = definition.get("graph_dependent")
    graph_degraded = gate.get("graph_degraded")
    node_degraded = (nd.get("derived", {}).get("indices") or {}).get("load_index_degraded")
    statuses = {t.signal: gate.get("signals", {}).get(t.signal) for t in context["terms"]}
    if (definition.get("decorative") or not side["room_eligible"]
            or (graph_dependent and (graph_degraded is True or node_degraded is True))):
        eligible, reason = False, None
    elif (graph_dependent is None or any(v is None for v in statuses.values())
            or (graph_dependent and (graph_degraded is None or node_degraded is None))):
        eligible, reason = None, "eligibility_metadata_missing"
    else:
        eligible = all(v in ("asserted", "validated") for v in statuses.values())
        reason = None
    return {**side, "predicate": definition["predicate"], "terms": terms, "predicate_passed": predicate_passed,
            "diagnostic_eligible": eligible, "eligibility_reason": reason,
            "signals": statuses, "graph_degraded": graph_degraded,
            "node_load_degraded": node_degraded}


def skeleton_diff(
    a: dict[str, Any],
    b: dict[str, Any],
    renames: dict[str, str] | None = None,
    touched: set[str] | None = None,
    commits_between: int | None = None,
    budget: dict[str, float | int] = SKELETON_BUDGET,
    kinds: dict[str, str] | None = None,
    unavailable_reason: str = "touched_set_unavailable",
    before_substrate: dict[str, Any] | None = None,
    after_substrate: dict[str, Any] | None = None,
    window_commits: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compare skeleton `a` (earlier) with `b` (later). `renames` maps a-names to b-names.
    `touched` (b-names) is the set of nodes the intervening commits edited; when given,
    the budget verdict is computed over the untouched population's jitter, otherwise
    `untested` with `unavailable_reason`. `kinds` (feature → clock|rank|mixed) defaults to
    what the two skeletons' evidence says. Refuses skeletons that are not comparable."""
    renames = renames or {}
    _verify_substrate(a, before_substrate)
    _verify_substrate(b, after_substrate)
    for field, get in (
        ("repo", lambda sk: sk["repo"]["name"]),
        ("geometry", lambda sk: sk["geometry"]["name"]),
        ("ruleset", lambda sk: sk["ruleset"]["name"]),
    ):
        if get(a) != get(b):
            raise ValueError(
                f"skeletons are not comparable: {field} differs ({get(a)!r} vs {get(b)!r})"
            )
    kinds = kinds if kinds is not None else feature_kinds_from_skeleton(a, b)
    a_strata = {}
    for n, v in a["strata"]["by_node"].items():
        a_strata[canonicalize(n, renames)] = v
    a_evidence: dict[tuple[str, str], dict[str, dict[str, Any]]] = {}
    b_evidence: dict[tuple[str, str], dict[str, dict[str, Any]]] = {}
    for sk, store, canon_names in ((a, a_evidence, True), (b, b_evidence, False)):
        groups = [sk.get("features") or []] + [od["features"] for od in sk.get("overlays") or []]
        for feats in groups:
            for f in feats:
                node = canonicalize(f["node"], renames) if canon_names else f["node"]
                store.setdefault((f["profile"], f["feature"]), {})[node] = f.get("evidence") or {}

    def canon(p: str) -> str:
        seen: set[str] = set()
        while p in renames and p not in seen:
            seen.add(p)
            p = renames[p]
        return p

    a_nodes = {canon(n) for n in a["strata"]["by_node"]}
    b_nodes = set(b["strata"]["by_node"])
    common = a_nodes & b_nodes
    # D-083: the row's own size and the rooms only one commit has, beside the common-room
    # sets the operand is computed over. Additive; nothing below reads these for a verdict.
    full_a = {k: {canon(n) for n in v} for k, v in _feature_sets(a).items()}
    full_b = dict(_feature_sets(b).items())
    born_nodes, deleted_nodes = b_nodes - a_nodes, a_nodes - b_nodes
    predicates = _predicates(a, b)
    positions = _position_names(a, b)
    fa = {k: v & common for k, v in full_a.items()}
    fb = {k: v & common for k, v in full_b.items()}
    touched = (touched or set()) & common
    untouched = common - touched
    per_feature = {}
    a_original = {canon(n): n for n in a["strata"]["by_node"]}
    jitter_rooms: set[str] = set()
    jitter_affected: set[str] = set()
    tot = {"all": [0, 0], "untouched": [0, 0]}  # [symmetric difference, union]
    by_kind = {k: [0, 0] for k in ("clock", "rank", "mixed")}  # untouched [changes, union]
    for key in sorted(set(fa) | set(fb)):
        sa, sb = fa.get(key, set()), fb.get(key, set())
        added, removed = sorted(sb - sa), sorted(sa - sb)
        union = len(sa | sb)
        jacc = (len(sa & sb) / union) if union else 1.0
        name = f"{key[0]}/{key[1]}"
        kind = kinds.get(name, "rank")  # an unclassifiable feature counts as jitter
        u_changes = len((sb ^ sa) & untouched)
        tot["all"][0] += len(added) + len(removed)
        tot["all"][1] += union
        tot["untouched"][0] += u_changes
        tot["untouched"][1] += len((sa | sb) & untouched)
        by_kind[kind][0] += u_changes
        by_kind[kind][1] += len((sa | sb) & untouched)
        if kind in ("rank", "mixed"):
            jitter_rooms.update((sa | sb) & untouched)
            jitter_affected.update((sa ^ sb) & untouched)
        contexts = [_transition_context(sk, sub, *key) for sk, sub in
                    ((a, before_substrate), (b, after_substrate))]
        transition_evidence = {n: {"before": _transition_side(contexts[0], a_original.get(n, n)),
                                   "after": _transition_side(contexts[1], n)}
                               for n in added + removed}
        evidence = {
            **{n: {"before": None, "after": b_evidence.get(key, {}).get(n)} for n in added},
            **{n: {"before": a_evidence.get(key, {}).get(n), "after": None} for n in removed},
        }
        per_feature[name] = {
            "before": len(sa),
            "after": len(sb),
            "added": added,
            "removed": removed,
            "jaccard": jacc,
            "untouched_changes": u_changes,
            "kind": kind,
            "evidence": evidence,
            "transition_evidence": transition_evidence,
            "untouched_affected_rooms": sorted((sa ^ sb) & untouched),
            # D-083 (additive)
            "predicate": predicates.get(key),
            **positions.get(key, {"position_name": None, "name_implies_consequence": False}),
            "rooms_before": len(full_a.get(key, set())),
            "rooms_after": len(full_b.get(key, set())),
            "born_entered": sorted(full_b.get(key, set()) & born_nodes),
            "deleted_left": sorted(a_original.get(n, n) for n in full_a.get(key, set()) & deleted_nodes),
        }

    def moved(pop: set[str]) -> list[str]:
        return sorted(
            n
            for n in pop
            if a_strata.get(n) is not None
            and b["strata"]["by_node"].get(n) is not None
            and a_strata[n] != b["strata"]["by_node"][n]
        )

    # decorative flicker, reported and never judged
    da = {k: {canon(n) for n in v} & common for k, v in _feature_sets(a, True).items()}
    db = {k: v & common for k, v in _feature_sets(b, True).items()}
    dec_changes = sum(
        len((db.get(k, set()) ^ da.get(k, set())) & untouched) for k in set(da) | set(db)
    )
    dec_union = sum(
        len((db.get(k, set()) | da.get(k, set())) & untouched) for k in set(da) | set(db)
    )
    full_da = {k: {canon(n) for n in v} for k, v in _feature_sets(a, True).items()}
    full_db = dict(_feature_sets(b, True).items())
    per_decorative = {}
    for key in sorted(set(da) | set(db) | set(full_da) | set(full_db)):
        sa, sb = da.get(key, set()), db.get(key, set())
        name = f"{key[0]}/{key[1]}"
        per_decorative[name] = {
            "kind": kinds.get(name, "rank"),
            "predicate": predicates.get(key),
            **positions.get(key, {"position_name": None, "name_implies_consequence": False}),
            "before": len(sa),
            "after": len(sb),
            "added": sorted(sb - sa),
            "removed": sorted(sa - sb),
            "untouched_affected_rooms": sorted((sa ^ sb) & untouched),
            "rooms_before": len(full_da.get(key, set())),
            "rooms_after": len(full_db.get(key, set())),
            "born_entered": sorted(full_db.get(key, set()) & born_nodes),
            "deleted_left": sorted(a_original.get(n, n) for n in full_da.get(key, set()) & deleted_nodes),
        }

    def _degraded(sk: dict[str, Any]) -> int:
        groups = [sk.get("features") or []] + [od["features"] for od in sk.get("overlays") or []]
        return sum(1 for feats in groups for f in feats if not f["decorative"] and not f["diagnostic"])

    strata_moved = moved(common)
    u_moved = moved(untouched)
    strata_evidence = {}
    for n in strata_moved:
        raw_a = a["strata"].get("raw_by_node", {}).get(a_original.get(n, n))
        raw_b = b["strata"].get("raw_by_node", {}).get(n)
        attribution = "unknown" if raw_a is None or raw_b is None else (
            "band_only" if raw_a == raw_b else ("raw_depth_changed" if b["geometry"]["name"] == "layer" else "raw_value_changed"))
        strata_evidence[n] = {"before": {"raw": raw_a, "band": a_strata[n]},
                              "after": {"raw": raw_b, "band": b["strata"]["by_node"][n]},
                              "attribution": attribution, "untouched": n in untouched}
    u_churn = (tot["untouched"][0] / tot["untouched"][1]) if tot["untouched"][1] else 0.0
    u_strata = (len(u_moved) / len(untouched)) if untouched else 0.0
    touched_frac = (len(touched) / len(common)) if common else 0.0
    jitter_changes = by_kind["rank"][0] + by_kind["mixed"][0]
    jitter_union = by_kind["rank"][1] + by_kind["mixed"][1]
    jitter_churn = (jitter_changes / jitter_union) if jitter_union else 0.0
    clock_churn = (by_kind["clock"][0] / by_kind["clock"][1]) if by_kind["clock"][1] else 0.0

    if commits_between is None:
        verdict, reason = "untested", unavailable_reason
    elif commits_between > budget["max_k"]:
        verdict, reason = "untested", "beyond_pinned_k"
    elif commits_between < budget["pinned_k"]:
        # D-032: the token travels neither above nor below the K it was pinned at — at K = 5
        # the ceiling cannot fire (D-024), so a verdict there is vacuous
        verdict, reason = "untested", "below_pinned_k"
    elif touched_frac > budget["max_touched_frac"]:
        verdict, reason = "untested", "touched_fraction_exceeds_floor"
    elif len(untouched) < budget["min_untouched_n"]:
        verdict, reason = "untested", "insufficient_untouched_population"
    elif jitter_union < budget["min_jitter_union"]:
        verdict, reason = "untested", "insufficient_jitter_population"
    elif jitter_churn > budget["feature_churn_max"] or u_strata > budget["strata_moved_max"]:
        verdict, reason = "over_budget", None
    else:
        verdict, reason = "within_budget", None

    crossings, crossings_reason = _distinct_crossings(per_feature)
    f_ceiling, s_ceiling = budget["feature_churn_max"], budget["strata_moved_max"]
    operands = {
        "features": {
            "unit": "(profile, feature, room) assignments of rank and mixed features held by untouched rooms",
            "changes": jitter_changes,
            "denominator": jitter_union,
            "value": jitter_churn,
            "ceiling": f_ceiling,
            "fires_at": fires_at(f_ceiling, jitter_union),
            "exceeds_ceiling": jitter_churn > f_ceiling,
            "distinct_rooms": len(jitter_affected),
            "distinct_crossings": crossings,
            "distinct_crossings_reason": crossings_reason,
        },
        "floors": {
            "unit": "untouched rooms",
            "changes": len(u_moved),
            "denominator": len(untouched),
            "value": u_strata,
            "ceiling": s_ceiling,
            "fires_at": fires_at(s_ceiling, len(untouched)),
            "exceeds_ceiling": u_strata > s_ceiling,
        },
    }
    # which operand carried a judged verdict; None when the window was not judged
    fired = (
        None
        if verdict == "untested"
        else [k for k, v in operands.items() if v["exceeds_ceiling"]]
    )

    return {
        "before": {
            "repo": a["repo"],
            "skeleton_hash": a["skeleton_hash"],
            "geometry": a["geometry"]["name"],
        },
        "after": {
            "repo": b["repo"],
            "skeleton_hash": b["skeleton_hash"],
            "geometry": b["geometry"]["name"],
        },
        "churn_units": "(profile, feature, room) assignments; summed symmetric differences / summed unions",
        # D-083 (additive): what the window page reads
        "identity": {"before": _side_identity(a), "after": _side_identity(b)},
        "rooms": {
            "born": sorted(born_nodes),
            "deleted": sorted(a_original.get(n, n) for n in deleted_nodes),
        },
        "per_decorative_feature": per_decorative,
        "degraded_marks": {"before": _degraded(a), "after": _degraded(b)},
        "strata_evidence": strata_evidence,
        "common_nodes": len(common),
        "born": len(b_nodes - a_nodes),
        "deleted": len(a_nodes - b_nodes),
        "feature_churn": (tot["all"][0] / tot["all"][1]) if tot["all"][1] else 0.0,
        "strata_moved": strata_moved,
        "strata_moved_frac": (len(strata_moved) / len(common)) if common else 0.0,
        "per_feature": per_feature,
        "commits_between": commits_between,
        "touched": {"n": len(touched), "frac": touched_frac, "nodes": sorted(touched)},
        "untouched": {
            "n": len(untouched),
            "feature_churn": u_churn,
            "strata_moved": u_moved,
            "strata_moved_frac": u_strata,
            "by_kind": {
                k: {"changes": v[0], "union": v[1], "churn": (v[0] / v[1]) if v[1] else 0.0}
                for k, v in by_kind.items()
            },
            "jitter_churn": jitter_churn,
            "jitter_assignment_changes": jitter_changes,
            "jitter_assignment_union": jitter_union,
            "jitter_affected_rooms": sorted(jitter_affected),
            "jitter_affected_room_count": len(jitter_affected),
            "jitter_room_union": len(jitter_rooms),
            "clock_churn": clock_churn,
            "decorative_churn": (dec_changes / dec_union) if dec_union else 0.0,
            "decorative_changes": dec_changes,
        },
        "kinds": dict(sorted(kinds.items())),
        "budget": {
            **budget,
            "k": commits_between,
            "operand": "jitter: rank + mixed feature churn, and strata moves, over untouched rooms",
            "verdict": verdict,
            "reason": reason,
            # D-082: the verdict's resolution and scope travel with it
            "scope": "one window",
            "window": {
                "before_sha": a["repo"].get("head_sha"),
                "after_sha": b["repo"].get("head_sha"),
                "commits_between": commits_between,
                **_window_times(a["repo"].get("head_sha"), b["repo"].get("head_sha"),
                                window_commits, after_substrate),
            },
            "operands": operands,
            "fired": fired,
        },
    }
