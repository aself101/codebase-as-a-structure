"""Skeleton diff (mapper §7 Q3, system spec §8; D-017): how much did the named structure
move between two skeletons of the same repository?

The measure the stability budget needs is feature churn over nodes present in both
skeletons: for each (profile, feature), the set of nodes it fired on before and after,
the symmetric difference, and the Jaccard similarity. Nodes born or deleted between the
two revisions are excluded from churn (they are structural change, not jitter) and
counted separately. This is the same discipline as the signal-level budget
(validation §2.4.1): measure the movement of what did not itself change.
"""

from __future__ import annotations

from typing import Any


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
    a: dict[str, Any], b: dict[str, Any], renames: dict[str, str] | None = None
) -> dict[str, Any]:
    """Compare skeleton `a` (earlier) with `b` (later). `renames` maps a-names to b-names."""
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
    per_feature = {}
    total_sym = 0
    total_union = 0
    for key in sorted(set(fa) | set(fb)):
        sa, sb = fa.get(key, set()), fb.get(key, set())
        added, removed = sorted(sb - sa), sorted(sa - sb)
        union = len(sa | sb)
        jacc = (len(sa & sb) / union) if union else 1.0
        total_sym += len(added) + len(removed)
        total_union += union
        per_feature[f"{key[0]}/{key[1]}"] = {
            "before": len(sa),
            "after": len(sb),
            "added": added,
            "removed": removed,
            "jaccard": jacc,
        }
    strata_moved = sorted(
        n
        for n in common
        if a["strata"]["by_node"].get(n) is not None
        and b["strata"]["by_node"].get(n) is not None
        and a["strata"]["by_node"][n] != b["strata"]["by_node"][n]
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
        "common_nodes": len(common),
        "born": len(b_nodes - a_nodes),
        "deleted": len(a_nodes - b_nodes),
        "feature_churn": (total_sym / total_union) if total_union else 0.0,
        "strata_moved": strata_moved,
        "strata_moved_frac": (len(strata_moved) / len(common)) if common else 0.0,
        "per_feature": per_feature,
    }
