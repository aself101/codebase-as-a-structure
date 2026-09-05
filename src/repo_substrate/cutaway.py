"""C6 (with C4 folded in, D-005): the 2D cutaway elevation, as a deterministic SVG.

The cutaway exposes the diagnosis by construction: strata are age bands (oldest at the
bottom), wings are top-level directories, rooms are files sized by lines, material is
age, lighting is recency, and the named features from skeleton.json are drawn as
overlays. Decorative features are drawn in a distinct dashed style and their count is
printed in the banner — the audited hatch (mapper §3) made visible.

Geometry depends only on the substrate and the strata (mapper §6: profile-independent);
the profile changes what is overlaid. There is no randomness: the same skeleton and
substrate produce the same bytes. The seed is recorded for the stochastic form grammar
that a later phase may add.
"""

from __future__ import annotations

import math
from collections import defaultdict
from typing import Any
from xml.sax.saxutils import escape

STRATA = 5
ROOM_H = 16
ROOM_GAP = 3
WING_GAP = 28
MARGIN = 24
BAND_GAP = 10
MATERIAL = ["#e8e2d3", "#d9cfb8", "#c7b894", "#a99a75", "#7e6f52"]  # new glass → old stone

FEATURE_STYLE: dict[str, dict[str, str]] = {
    "foundation": {"stroke": "#2b2b2b", "stroke-width": "3"},
    "hub": {"stroke": "#8a4b00", "stroke-width": "2", "stroke-dasharray": "1 0"},
    "flooded_basement": {"fill": "url(#water)"},
    "scaffolding": {"fill": "url(#scaffold)"},
    "dark_room": {"opacity": "0.45"},
    "lit_room": {"stroke": "#f2c14e", "stroke-width": "2"},
}
DECORATIVE_STYLE = {"stroke": "#c2185b", "stroke-width": "1.5", "stroke-dasharray": "4 3"}


def _wing_of(path: str, depth: int) -> str:
    parts = path.split("/")
    return "/".join(parts[:depth]) if len(parts) > depth else "(root)"


def _room_w(size_loc: int) -> int:
    return int(min(64, max(10, 8 + 2 * math.sqrt(max(size_loc, 1)))))


def render_cutaway(skeleton: dict[str, Any], substrate: dict[str, Any], wing_depth: int = 1) -> str:
    nodes = {n["id"]: n for n in substrate["nodes"]}
    strata_by_node: dict[str, int] = skeleton["strata"]["by_node"]
    feats_by_node: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for f in skeleton["features"]:
        feats_by_node[f["node"]].append(f)
    population = sorted(strata_by_node)  # the mapper's population, deterministic order

    # --- layout: wings (columns) × strata (rows); rooms packed left→right within a band
    wings: dict[str, list[str]] = defaultdict(list)
    for nid in population:
        wings[_wing_of(nid, wing_depth)].append(nid)
    wing_names = sorted(wings)
    band_rows: dict[tuple[str, int], list[list[str]]] = {}
    wing_w: dict[str, int] = {}
    for w in wing_names:
        max_w = 0
        for band in range(STRATA):
            ids = [n for n in wings[w] if strata_by_node[n] == band]
            rows: list[list[str]] = []
            cur: list[str] = []
            cur_w = 0
            limit = max(160, int(30 * math.sqrt(len(wings[w])) + 60))
            for nid in ids:
                rw = _room_w(nodes[nid]["metrics"]["size_loc"])
                if cur and cur_w + rw + ROOM_GAP > limit:
                    rows.append(cur)
                    cur, cur_w = [], 0
                cur.append(nid)
                cur_w += rw + ROOM_GAP
            if cur:
                rows.append(cur)
            band_rows[(w, band)] = rows
            for r in rows:
                max_w = max(
                    max_w, sum(_room_w(nodes[n]["metrics"]["size_loc"]) + ROOM_GAP for n in r)
                )
        wing_w[w] = max(max_w, 80)
    band_h = [
        max(1, max(len(band_rows[(w, b)]) for w in wing_names)) * (ROOM_H + ROOM_GAP) + BAND_GAP
        for b in range(STRATA)
    ]
    # the banner and legend need ~1750px; a narrow building must not clip its own gate line
    total_w = max(1760, MARGIN * 2 + sum(wing_w[w] + WING_GAP for w in wing_names))
    header_h = 140
    total_h = header_h + sum(band_h) + MARGIN + 30

    s = skeleton["summary"]
    r = skeleton["repo"]
    out: list[str] = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" '
        f'viewBox="0 0 {total_w} {total_h}" font-family="ui-monospace, Menlo, monospace" font-size="11">'
    )
    out.append(
        "<defs>"
        '<pattern id="water" width="8" height="8" patternUnits="userSpaceOnUse">'
        '<rect width="8" height="8" fill="#9fc5e8"/><path d="M0 4 Q2 2 4 4 T8 4" stroke="#3d7ab8" fill="none"/></pattern>'
        '<pattern id="scaffold" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        '<rect width="8" height="8" fill="none"/><line x1="0" y1="0" x2="0" y2="8" stroke="#5c8a3a" stroke-width="2"/></pattern>'
        "</defs>"
    )
    out.append(f'<rect width="{total_w}" height="{total_h}" fill="#faf8f3"/>')
    # --- banner: what this picture is allowed to claim
    out.append(
        f'<text x="{MARGIN}" y="26" font-size="16" font-weight="bold">{escape(r["name"])} @ {escape(r["head_sha"][:10])} — cutaway, profile {escape(skeleton["profile"]["name"])}</text>'
    )
    out.append(
        f'<text x="{MARGIN}" y="46">diagnostic features: {s["diagnostic_count"]} · '
        f'<tspan fill="#c2185b" font-weight="bold">decorative (ungrounded, not a diagnosis): {s["decorative_count"]}</tspan> · '
        f"degraded (graph): {s['degraded_count']} · population {s['population']} files</text>"
    )
    gate = ", ".join(f"{k}={v}" for k, v in skeleton["gate"]["signals"].items())
    out.append(f'<text x="{MARGIN}" y="64" fill="#555">gate: {escape(gate)}</text>')
    out.append(
        f'<text x="{MARGIN}" y="82" fill="#555">seed {escape(skeleton["substrate_seed"][:12])}… · substrate fp {escape(skeleton["substrate_config_fingerprint"][:12])}… · '
        f"validation fp {escape((skeleton.get('validation_config_fingerprint') or '')[:12])}… · ruleset {escape(skeleton['ruleset']['name'])}@{escape(skeleton['ruleset']['version'])} · skeleton {escape(skeleton['skeleton_hash'][:12])}…</text>"
    )
    out.append(
        f'<text x="{MARGIN}" y="100" fill="#555">strata = {escape(skeleton["strata"]["signal"])} percentile bands, oldest at the bottom · wings = top-level directory · room width ∝ √lines · '
        "material = age · every named feature denotes present structural position (validation §2.1.1)</text>"
    )
    # --- legend
    lx = MARGIN
    ly = header_h - 12
    legend = [
        ("foundation / high-load hub", "stroke:#2b2b2b;stroke-width:3;fill:#d9cfb8"),
        ("hub", "stroke:#8a4b00;stroke-width:2;fill:#d9cfb8"),
        ("flooded basement", "fill:url(#water);stroke:#888"),
        ("scaffolding", "fill:url(#scaffold);stroke:#888"),
        ("dark room", "fill:#d9cfb8;opacity:0.45;stroke:#888"),
        ("lit room", "stroke:#f2c14e;stroke-width:2;fill:#d9cfb8"),
        (
            "decorative (ungrounded)",
            "stroke:#c2185b;stroke-width:1.5;stroke-dasharray:4 3;fill:#d9cfb8",
        ),
    ]
    for label, style in legend:
        out.append(f'<rect x="{lx}" y="{ly - 10}" width="14" height="10" style="{style}"/>')
        out.append(f'<text x="{lx + 18}" y="{ly - 1}" fill="#333">{escape(label)}</text>')
        lx += 18 + 7 * len(label) + 16
    # --- the building
    x = MARGIN
    y_top = header_h + 6
    for w in wing_names:
        out.append(
            f'<text x="{x}" y="{y_top - 2}" font-weight="bold" fill="#333">{escape(w)}</text>'
        )
        y = y_top + sum(band_h[b] for b in range(STRATA)) - BAND_GAP  # bottom of the lowest band
        for band in range(STRATA):  # band 0 = oldest, drawn at the bottom
            rows = band_rows[(w, band)]
            yb = y
            for row in rows:
                rx = x
                for nid in row:
                    n = nodes[nid]
                    m = n["metrics"]
                    rw = _room_w(m["size_loc"])
                    pct = (n.get("derived") or {}).get("percentiles") or {}
                    age_p = pct.get("age_days") or 0.0
                    mat = MATERIAL[min(4, int(age_p * 5))]
                    style = {"fill": mat, "stroke": "#8c8577", "stroke-width": "1"}
                    labels = []
                    for f in sorted(feats_by_node.get(nid, []), key=lambda t: t["feature"]):
                        if f["decorative"] or not f["diagnostic"]:
                            style.update(
                                DECORATIVE_STYLE if f["decorative"] else {"stroke-dasharray": "2 2"}
                            )
                            labels.append(
                                f"{f['feature']} [{'decorative' if f['decorative'] else 'degraded'}]"
                            )
                        else:
                            style.update(FEATURE_STYLE.get(f["feature"], {}))
                            labels.append(
                                f["feature"]
                                + (
                                    f" (position: {f['position_name']})"
                                    if f["position_name"]
                                    else ""
                                )
                            )
                    sty = ";".join(f"{k}:{v}" for k, v in style.items())
                    title = (
                        f"{nid}\nlines {m['size_loc']} · fan_in {m.get('fan_in')} · age {m.get('age_days')}d · last touched {m.get('last_touched_days')}d\n"
                        + ("\n".join(labels) if labels else "no named feature")
                    )
                    out.append(
                        f'<rect x="{rx}" y="{yb - ROOM_H}" width="{rw}" height="{ROOM_H}" style="{sty}"><title>{escape(title)}</title></rect>'
                    )
                    rx += rw + ROOM_GAP
                yb -= ROOM_H + ROOM_GAP
            # band baseline
            out.append(
                f'<line x1="{x - 4}" y1="{y + 2}" x2="{x + wing_w[w]}" y2="{y + 2}" stroke="#bbb" stroke-dasharray="2 4"/>'
            )
            y -= band_h[band]
        x += wing_w[w] + WING_GAP
    # --- feature list (diagnostic first)
    fy = total_h - 12
    diag = [f for f in skeleton["features"] if f["diagnostic"]]
    deco = [f for f in skeleton["features"] if f["decorative"]]
    out.append(
        f'<text x="{MARGIN}" y="{fy}" fill="#333">diagnostic: '
        + escape(
            ", ".join(
                f"{k}×{v}"
                for k, v in sorted(skeleton["summary"]["feature_counts"].items())
                if k not in skeleton["summary"]["decorative_features"]
            )
            or "none"
        )
        + f"   ·   decorative: {len(deco)} instance(s) of {escape(', '.join(skeleton['summary']['decorative_features']) or 'none')}"
        + f"   ·   {len(diag)} diagnostic instance(s) in total</text>"
    )
    out.append("</svg>")
    return "\n".join(out)
