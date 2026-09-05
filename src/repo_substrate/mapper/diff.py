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

# D-018. Per comparison (the caller chooses K; `commits_between` is recorded), per geometry.
# One node in twenty. Measured ripple on the four reference repos at K = 5 sits well
# under it: untouched feature churn ≤ 0.014, untouched strata movement ≤ 0.032 (both
# maxima on mcp-secure-server, the latter under the layer geometry). A ceiling above the
# observed range but within a factor of two of the tightest reading — headroom, not a fit.
SKELETON_BUDGET: dict[str, float | int] = {
    "feature_churn_max": 0.05,
    "strata_moved_max": 0.05,
    "min_untouched_n": 30,
    "max_touched_frac": 0.5,
}


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


def _feature_sets(skeleton: dict[str, Any]) -> dict[tuple[str, str], set[str]]:
    sets: dict[tuple[str, str], set[str]] = {}
    for f in skeleton["features"]:
        if f["diagnostic"]:
            sets.setdefault((f["profile"], f["feature"]), set()).add(f["node"])
    for od in skeleton.get("overlays") or []:
        for f in od["features"]:
            if f["diagnostic"]:
                sets.setdefault((f["profile"], f["feature"]), set()).add(f["node"])
    return sets


def skeleton_diff(
    a: dict[str, Any],
    b: dict[str, Any],
    renames: dict[str, str] | None = None,
    touched: set[str] | None = None,
    commits_between: int | None = None,
    budget: dict[str, float | int] = SKELETON_BUDGET,
) -> dict[str, Any]:
    """Compare skeleton `a` (earlier) with `b` (later). `renames` maps a-names to b-names.
    `touched` (b-names) is the set of nodes the intervening commits edited; when given,
    the budget verdict is computed over the untouched population, otherwise `untested`."""
    renames = renames or {}

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
    for key in sorted(set(fa) | set(fb)):
        sa, sb = fa.get(key, set()), fb.get(key, set())
        added, removed = sorted(sb - sa), sorted(sa - sb)
        union = len(sa | sb)
        jacc = (len(sa & sb) / union) if union else 1.0
        tot["all"][0] += len(added) + len(removed)
        tot["all"][1] += union
        tot["untouched"][0] += len((sb ^ sa) & untouched)
        tot["untouched"][1] += len((sa | sb) & untouched)
        per_feature[f"{key[0]}/{key[1]}"] = {
            "before": len(sa),
            "after": len(sb),
            "added": added,
            "removed": removed,
            "jaccard": jacc,
            "untouched_changes": len((sb ^ sa) & untouched),
        }

    def moved(pop: set[str]) -> list[str]:
        return sorted(
            n
            for n in pop
            if a["strata"]["by_node"].get(n) is not None
            and b["strata"]["by_node"].get(n) is not None
            and a["strata"]["by_node"][n] != b["strata"]["by_node"][n]
        )

    strata_moved = moved(common)
    u_moved = moved(untouched)
    u_churn = (tot["untouched"][0] / tot["untouched"][1]) if tot["untouched"][1] else 0.0
    u_strata = (len(u_moved) / len(untouched)) if untouched else 0.0
    touched_frac = (len(touched) / len(common)) if common else 0.0

    if commits_between is None:
        verdict, reason = "untested", "touched_set_unavailable"
    elif len(untouched) < budget["min_untouched_n"]:
        verdict, reason = "untested", "insufficient_untouched_population"
    elif touched_frac > budget["max_touched_frac"]:
        verdict, reason = "untested", "touched_fraction_exceeds_floor"
    elif u_churn > budget["feature_churn_max"] or u_strata > budget["strata_moved_max"]:
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
        "touched": {"n": len(touched), "frac": touched_frac},
        "untouched": {
            "n": len(untouched),
            "feature_churn": u_churn,
            "strata_moved": u_moved,
            "strata_moved_frac": u_strata,
        },
        "budget": {**budget, "verdict": verdict, "reason": reason},
    }
