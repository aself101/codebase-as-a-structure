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

from typing import Any

# D-018, operand revised D-024, K re-pinned D-026. The budget bounds JITTER: movement of
# untouched rooms through rank-only features, mixed features (a clock and a rank signal in
# one predicate — the rank component cannot be separated, so the whole is counted as
# jitter, the conservative side), and strata (a floor moves for an untouched room only
# because the population re-ranked around it, D-022 having removed the clock's way of
# moving it). Clock-only features are reported beside it, never judged.
# The ceilings are one room in twenty. The K: at K = 5 nothing fires the ceiling, not the
# reference set and not a ruleset written to break it (D-024); the K study (D-025/D-026,
# reports/2026-09-05-kstudy) read jitter churn per transition at K = 5…250 and found it
# grows with K at a rate set by the repository's growth. At K = 25 the ceiling sits between
# the reference set's median (0.02–0.05) and its 90th percentile (0.07–0.24) on every
# repository where it was read — it separates typical from tail without being fitted — so
# the budget is pinned at 25 and applied up to 50. Beyond that a comparison is
# `untested: beyond_pinned_k`. A jitter union under `min_jitter_union` rooms is
# `untested: insufficient_jitter_population` (two rooms flipping is not a rate).
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


def skeleton_diff(
    a: dict[str, Any],
    b: dict[str, Any],
    renames: dict[str, str] | None = None,
    touched: set[str] | None = None,
    commits_between: int | None = None,
    budget: dict[str, float | int] = SKELETON_BUDGET,
    kinds: dict[str, str] | None = None,
    unavailable_reason: str = "touched_set_unavailable",
) -> dict[str, Any]:
    """Compare skeleton `a` (earlier) with `b` (later). `renames` maps a-names to b-names.
    `touched` (b-names) is the set of nodes the intervening commits edited; when given,
    the budget verdict is computed over the untouched population's jitter, otherwise
    `untested` with `unavailable_reason`. `kinds` (feature → clock|rank|mixed) defaults to
    what the two skeletons' evidence says. Refuses skeletons that are not comparable."""
    renames = renames or {}
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
    fa = {k: {canon(n) for n in v} & common for k, v in _feature_sets(a).items()}
    fb = {k: v & common for k, v in _feature_sets(b).items()}
    touched = (touched or set()) & common
    untouched = common - touched
    per_feature = {}
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
    strata_moved = moved(common)
    u_moved = moved(untouched)
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
    elif touched_frac > budget["max_touched_frac"]:
        verdict, reason = "untested", "touched_fraction_exceeds_floor"
    elif len(untouched) < budget["min_untouched_n"]:
        verdict, reason = "untested", "insufficient_untouched_population"
    elif jitter_union < budget.get("min_jitter_union", 0):
        verdict, reason = "untested", "insufficient_jitter_population"
    elif jitter_churn > budget["feature_churn_max"] or u_strata > budget["strata_moved_max"]:
        verdict, reason = "over_budget", None
    else:
        verdict, reason = "within_budget", None

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
        },
    }
