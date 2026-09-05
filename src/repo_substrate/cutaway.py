"""C6 (with C4 folded in, D-005): the 2D cutaway elevation, as a deterministic SVG, plus an
HTML wrapper with profile toggles (D-017).

The cutaway exposes the diagnosis by construction: strata are age bands or dependency
layers (bottom = oldest / leaves), wings are top-level directories, rooms are files sized
by lines, material is age, lighting is recency, and the named features from skeleton.json
are drawn as overlays. The base profile styles the room; each overlay profile adds a
corner badge in its own hue, so a room flagged by two lenses shows both marks side by
side and nothing is averaged (mapper §6). Decorative features are drawn dashed magenta
and their count is printed in the banner — the audited hatch (mapper §3) made visible.

Geometry depends only on the substrate and the strata (profile-independent). No
randomness: the same skeleton and substrate produce the same bytes.
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
MIN_W = 1760
MATERIAL = ["#e8e2d3", "#d9cfb8", "#c7b894", "#a99a75", "#7e6f52"]  # new glass → old stone

FEATURE_STYLE: dict[str, dict[str, str]] = {
    "foundation": {"stroke": "#2b2b2b", "stroke-width": "3"},
    "hub": {"stroke": "#8a4b00", "stroke-width": "2"},
    "flooded_basement": {"fill": "url(#water)"},
    "scaffolding": {"fill": "url(#scaffold)"},
    "dark_room": {"opacity": "0.45"},
    "lit_room": {"stroke": "#f2c14e", "stroke-width": "2"},
}
DECORATIVE_STYLE = {"stroke": "#c2185b", "stroke-width": "1.5", "stroke-dasharray": "4 3"}
OVERLAY_HUES = ["#1f6f8b", "#7a3e9d", "#2e7d32", "#b26a00"]  # one per overlay profile, in order


def _wing_of(path: str, depth: int) -> str:
    parts = path.split("/")
    return "/".join(parts[:depth]) if len(parts) > depth else "(root)"


def _room_w(size_loc: int) -> int:
    return int(min(64, max(10, 8 + 2 * math.sqrt(max(size_loc, 1)))))


def _strata_caption(skeleton: dict[str, Any]) -> str:
    if skeleton["strata"].get("geometry", "age") == "layer":
        return "strata = dependency layers (longest import path to a leaf), leaves at the bottom"
    return "strata = age_days percentile bands, oldest at the bottom"


def render_cutaway(skeleton: dict[str, Any], substrate: dict[str, Any]) -> str:
    wing_depth = int((skeleton.get("geometry") or {}).get("wing_depth", 1))
    nodes = {n["id"]: n for n in substrate["nodes"]}
    strata_by_node: dict[str, int] = skeleton["strata"]["by_node"]
    base_feats: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for f in skeleton["features"]:
        base_feats[f["node"]].append(f)
    overlays = skeleton.get("overlays") or []
    overlay_feats: list[dict[str, list[dict[str, Any]]]] = []
    for od in overlays:
        d: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for f in od["features"]:
            d[f["node"]].append(f)
        overlay_feats.append(d)
    population = sorted(strata_by_node)

    # --- layout: wings (columns) × strata (rows); rooms packed left→right within a band
    wings: dict[str, list[str]] = defaultdict(list)
    for nid in population:
        wings[_wing_of(nid, wing_depth)].append(nid)
    wing_names = sorted(wings)
    band_rows: dict[tuple[str, int], list[list[str]]] = {}
    wing_w: dict[str, int] = {}
    for w in wing_names:
        max_w = 0
        limit = max(160, int(30 * math.sqrt(len(wings[w])) + 60))
        for band in range(STRATA):
            ids = [n for n in wings[w] if strata_by_node[n] == band]
            rows: list[list[str]] = []
            cur: list[str] = []
            cur_w = 0
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
    total_w = max(MIN_W, MARGIN * 2 + sum(wing_w[w] + WING_GAP for w in wing_names))
    header_h = 140 + (18 if overlays else 0)
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
    base_profile = escape(skeleton["profile"]["name"])
    prof = base_profile + "".join(" + " + escape(o["profile"]) for o in overlays)
    out.append(
        f'<text x="{MARGIN}" y="26" font-size="16" font-weight="bold">{escape(r["name"])} @ {escape(r["head_sha"][:10])} — cutaway, profile {prof}</text>'
    )
    out.append(
        f'<text x="{MARGIN}" y="46">diagnostic features: {s["diagnostic_count"]} · '
        f'<tspan fill="#c2185b" font-weight="bold">decorative (ungrounded, not a diagnosis): {s["decorative_count"]}</tspan> · '
        f"degraded (graph): {s['degraded_count']} · population {s['population']} files"
        + (f" · co-located across profiles: {s.get('co_located_count', 0)}" if overlays else "")
        + "</text>"
    )
    gate = ", ".join(f"{k}={v}" for k, v in skeleton["gate"]["signals"].items())
    out.append(f'<text x="{MARGIN}" y="64" fill="#555">gate: {escape(gate)}</text>')
    out.append(
        f'<text x="{MARGIN}" y="82" fill="#555">seed {escape(skeleton["substrate_seed"][:12])}… · substrate fp {escape(skeleton["substrate_config_fingerprint"][:12])}… · '
        f"validation fp {escape((skeleton.get('validation_config_fingerprint') or '')[:12])}… · ruleset {escape(skeleton['ruleset']['name'])}@{escape(skeleton['ruleset']['version'])} · skeleton {escape(skeleton['skeleton_hash'][:12])}…</text>"
    )
    out.append(
        f'<text x="{MARGIN}" y="100" fill="#555">{escape(_strata_caption(skeleton))} · wings = top-level directory · room width ∝ √lines · '
        "material = age · every named feature denotes present structural position (validation §2.1.1)</text>"
    )
    # --- legend
    lx, ly = MARGIN, 128
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
    if overlays:
        lx, ly2 = MARGIN, ly + 18
        head = "overlays (corner badge per profile, shown side by side, never merged):"
        out.append(f'<text x="{lx}" y="{ly2 - 1}" fill="#333">{head}</text>')
        lx += 7 * len(head) + 12
        for i, od in enumerate(overlays):
            hue = OVERLAY_HUES[i % len(OVERLAY_HUES)]
            label = f"{od['profile']}: {', '.join(sorted(od['summary']['feature_counts']))}"
            out.append(
                f'<polygon points="{lx},{ly2 - 10} {lx + 10},{ly2 - 10} {lx},{ly2}" fill="{hue}"/>'
            )
            out.append(f'<text x="{lx + 14}" y="{ly2 - 1}" fill="#333">{escape(label)}</text>')
            lx += 14 + 7 * len(label) + 16
    # --- the building
    x = MARGIN
    y_top = header_h + 6
    rooms: list[str] = []
    badges: dict[int, list[str]] = defaultdict(list)
    for w in wing_names:
        rooms.append(
            f'<text x="{x}" y="{y_top - 2}" font-weight="bold" fill="#333">{escape(w)}</text>'
        )
        y = y_top + sum(band_h[b] for b in range(STRATA)) - BAND_GAP
        for band in range(STRATA):
            yb = y
            for row in band_rows[(w, band)]:
                rx = x
                for nid in row:
                    n = nodes[nid]
                    m = n["metrics"]
                    rw = _room_w(m["size_loc"])
                    pct = (n.get("derived") or {}).get("percentiles") or {}
                    mat = MATERIAL[min(4, int((pct.get("age_days") or 0.0) * 5))]
                    style = {"fill": mat, "stroke": "#8c8577", "stroke-width": "1"}
                    labels = []
                    for f in sorted(base_feats.get(nid, []), key=lambda t: t["feature"]):
                        if f["decorative"] or not f["diagnostic"]:
                            style.update(
                                DECORATIVE_STYLE if f["decorative"] else {"stroke-dasharray": "2 2"}
                            )
                            kind = "decorative" if f["decorative"] else "degraded"
                            labels.append(f"[{f['profile']}] {f['feature']} [{kind}]")
                        else:
                            style.update(FEATURE_STYLE.get(f["feature"], {}))
                            pos = f" (position: {f['position_name']})" if f["position_name"] else ""
                            labels.append(f"[{f['profile']}] {f['feature']}{pos}")
                    top, right = yb - ROOM_H, rx + rw
                    for i, od in enumerate(overlays):
                        fs = [f for f in overlay_feats[i].get(nid, []) if f["diagnostic"]]
                        if not fs:
                            continue
                        hue = OVERLAY_HUES[i % len(OVERLAY_HUES)]
                        pts = {
                            0: f"{rx},{top} {rx + 7},{top} {rx},{top + 7}",
                            1: f"{right},{top} {right - 7},{top} {right},{top + 7}",
                            2: f"{rx},{yb} {rx + 7},{yb} {rx},{yb - 7}",
                            3: f"{right},{yb} {right - 7},{yb} {right},{yb - 7}",
                        }[i % 4]
                        badges[i].append(f'<polygon points="{pts}" fill="{hue}"/>')
                        for f in sorted(fs, key=lambda t: t["feature"]):
                            pos = f" (position: {f['position_name']})" if f["position_name"] else ""
                            labels.append(f"[{f['profile']}] {f['feature']}{pos}")
                    sty = ";".join(f"{k}:{v}" for k, v in style.items())
                    title = (
                        f"{nid}\nlines {m['size_loc']} · fan_in {m.get('fan_in')} · fan_out {m.get('fan_out')} · "
                        f"age {m.get('age_days')}d · last touched {m.get('last_touched_days')}d\n"
                        + ("\n".join(labels) if labels else "no named feature")
                    )
                    rooms.append(
                        f'<rect x="{rx}" y="{top}" width="{rw}" height="{ROOM_H}" style="{sty}"><title>{escape(title)}</title></rect>'
                    )
                    rx += rw + ROOM_GAP
                yb -= ROOM_H + ROOM_GAP
            rooms.append(
                f'<line x1="{x - 4}" y1="{y + 2}" x2="{x + wing_w[w]}" y2="{y + 2}" stroke="#bbb" stroke-dasharray="2 4"/>'
            )
            y -= band_h[band]
        x += wing_w[w] + WING_GAP
    out.append(f'<g id="base" data-profile="{base_profile}">')
    out.extend(rooms)
    out.append("</g>")
    for i, od in enumerate(overlays):
        out.append(f'<g class="overlay" id="overlay-{i}" data-profile="{escape(od["profile"])}">')
        out.extend(badges[i])
        out.append("</g>")
    # --- footer
    fy = total_h - 12
    diag_counts = (
        ", ".join(
            f"{k}×{v}"
            for k, v in sorted(s["feature_counts"].items())
            if k not in s["decorative_features"]
        )
        or "none"
    )
    line = (
        f"diagnostic: {diag_counts}   ·   decorative: {s['decorative_count']} instance(s) of "
        f"{', '.join(s['decorative_features']) or 'none'}"
    )
    for od in overlays:
        oc = (
            ", ".join(f"{k}×{v}" for k, v in sorted(od["summary"]["feature_counts"].items()))
            or "none"
        )
        line += f"   ·   {od['profile']}: {oc}"
    out.append(f'<text x="{MARGIN}" y="{fy}" fill="#333">{escape(line)}</text>')
    out.append("</svg>")
    return "\n".join(out)


def render_html(skeleton: dict[str, Any], substrate: dict[str, Any]) -> str:
    """A standalone page around the SVG with a checkbox per overlay profile (toggles the
    `<g class="overlay">` layers). The base profile cannot be turned off: it is the building."""
    svg = render_cutaway(skeleton, substrate)
    overlays = skeleton.get("overlays") or []
    toggles = "".join(
        f'<label><input type="checkbox" checked data-target="overlay-{i}"> {escape(od["profile"])} overlay</label>'
        for i, od in enumerate(overlays)
    )
    name = escape(skeleton["repo"]["name"])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{name} — cutaway</title>
<style>
body{{margin:0;background:#e9e6df;color:#26221d;font-family:ui-monospace,Menlo,monospace;font-size:13px}}
.bar{{position:sticky;top:0;background:#faf8f3;border-bottom:1px solid #c9c2b4;padding:8px 16px;display:flex;gap:18px;align-items:center}}
.bar b{{font-weight:600}} label{{cursor:pointer}} .sheet{{overflow-x:auto;padding:8px}}
</style></head><body>
<div class="bar"><b>{name}</b> <span>base profile: {escape(skeleton["profile"]["name"])} (always on)</span>{toggles}
<span style="margin-left:auto;color:#6a6358">skeleton {escape(skeleton["skeleton_hash"][:12])}…</span></div>
<div class="sheet">{svg}</div>
<script>
document.querySelectorAll('input[data-target]').forEach(cb => cb.addEventListener('change', () => {{
  const g = document.getElementById(cb.dataset.target); if (g) g.style.display = cb.checked ? '' : 'none';
}}));
</script></body></html>
"""
