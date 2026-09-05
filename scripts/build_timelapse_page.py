"""Assemble the Skeleton Time-lapse viewer (the published page) from out/timelapse-b/<repo>.age/. Usage: uv run python scripts/build_timelapse_page.py out/skeleton-timelapse.html — writes an Artifact-style fragment (no doctype/html/body); wrap it for standalone use."""

from __future__ import annotations

import json
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = (
    Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("skeleton-timelapse.html")
)
REPOS = [
    ("registry", "uluops-registry-api", "a service API, eight months old"),
    ("mcp-secure-server", "mcp-secure-server", "a small server, nine months old"),
    ("eslint", "eslint", "thirteen years, eleven thousand commits"),
    ("typeorm", "typeorm", "ten years, six thousand commits"),
]


def load(key: str):
    d = ROOT / "out" / "timelapse-b" / f"{key}.age"
    if not (d / "frames.json").exists():
        return None
    m = json.loads((d / "frames.json").read_text(encoding="utf-8"))
    for f in m["frames"]:
        if f["status"] == "mapped":
            raw = (d / f"{f['stem']}.cutaway.svg").read_text(encoding="utf-8")
            # keep the room's name and its named features in the tooltip; drop the metric line
            f["svg"] = re.sub(
                r"<title>([^\n<]*)\n[^\n<]*\n?([^<]*)</title>",
                lambda m: (
                    "<title>" + m.group(1) + ("\n" + m.group(2) if m.group(2) else "") + "</title>"
                ),
                raw,
            ).replace("\n<", "<")
            if f.get("change_stem"):
                raw = (d / f"{f['change_stem']}.change.svg").read_text(encoding="utf-8")
                # the marks carry the reading; drop per-room tooltips to keep the page small
                f["change_svg"] = re.sub(r"<title>.*?</title>", "", raw, flags=re.S).replace(
                    "\n", ""
                )
    return m


repos = [(k, n, blurb, load(k)) for k, n, blurb in REPOS]
repos = [(k, n, b, m) for k, n, b, m in repos if m]

# ---------- pieces ----------


def share_bar(t: dict, height: int = 14) -> str:
    segs = [
        ("edits", t["edit_share"], "edits"),
        ("clock", t["ripple_clock_share"], "clock"),
        ("rank", t["ripple_rank_share"], "rank"),
        ("structural", t["structural_share"], "structural"),
    ]
    out = ['<div class="bar" style="height:%dpx">' % height]
    for cls, share, label in segs:
        if share <= 0:
            continue
        out.append(
            f'<span class="seg {cls}" style="flex:{share:.4f}" title="{label} {share:.0%}"></span>'
        )
    out.append("</div>")
    return "".join(out)


def summary_rows() -> str:
    rows = []
    for k, name, blurb, m in repos:
        t = m["totals"]
        rows.append(
            f'<div class="sum-row"><div class="sum-name"><b>{escape(name)}</b><span>{escape(blurb)}</span></div>'
            f"{share_bar(t)}"
            f'<div class="sum-nums"><span class="n edits">{t["edit_share"]:.0%}</span><span class="n clock">{t["ripple_clock_share"]:.0%}</span>'
            f'<span class="n rank">{t["ripple_rank_share"]:.0%}</span><span class="n structural">{t["structural_share"]:.0%}</span>'
            f'<span class="tot">{t["movement"]:,} moves · {t["commits_between"]:,} commits</span></div></div>'
        )
    return "".join(rows)


def repo_block(k: str, name: str, m: dict) -> str:
    frames = m["frames"]
    mapped = [f for f in frames if f["status"] == "mapped"]
    head = frames[-1]["commit_count"]
    # ruler ticks on a commit-count scale (the schedule's own unit)
    ticks = []
    for f in frames:
        x = 100.0 * f["commit_count"] / head
        cls = "tick" + (" skipped" if f["status"] == "skipped" else "")
        ticks.append(
            f'<div class="{cls}" style="left:{x:.2f}%" data-i="{f["index"]}">'
            f'<span class="tk-date">{escape(f["as_of"][:7])}</span><span class="tk-n">{f["commit_count"]:,}</span></div>'
        )
    # one stacked bar per transition, spanning previous mapped frame → this frame
    bars = []
    prev = None
    for f in frames:
        if f["status"] != "mapped":
            continue
        if prev is not None and f.get("diff"):
            d = f["diff"]
            x0 = 100.0 * prev["commit_count"] / head
            x1 = 100.0 * f["commit_count"] / head
            edits = d["feature_changes_touched"] + d["strata_moves_touched"]
            struct = d["born"] + d["deleted"]
            tot = edits + d["ripple_clock"] + d["ripple_rank"] + struct
            segs = "".join(
                f'<span class="seg {cls}" style="flex:{v / tot if tot else 0:.4f}"></span>'
                for cls, v in (
                    ("edits", edits),
                    ("clock", d["ripple_clock"]),
                    ("rank", d["ripple_rank"]),
                    ("structural", struct),
                )
                if v > 0
            )
            verdict = d["budget_verdict"].replace("_", " ")
            title = (
                f"{prev['commit_count']:,} → {f['commit_count']:,} ({d['commits_between']} commits): "
                f"edits {edits}, clock {d['ripple_clock']}, rank {d['ripple_rank']}, born/deleted {d['born']}/{d['deleted']}; budget {verdict}"
            )
            bars.append(
                f'<div class="tbar" style="left:{x0:.2f}%;width:{x1 - x0:.2f}%" data-i="{f["index"]}" title="{escape(title)}">{segs}</div>'
            )
        prev = f
    templates = "".join(
        f'<template data-i="{f["index"]}">{f["svg"]}</template>'
        + (
            f'<template data-change-i="{f["index"]}">{f["change_svg"]}</template>'
            if f.get("change_svg")
            else ""
        )
        for f in mapped
    )
    captions = {}
    for f in frames:
        c = {
            "i": f["index"],
            "sha": f["sha"][:8],
            "date": f["as_of"][:10],
            "commits": f["commit_count"],
            "rooms": f["population"],
            "status": f["status"],
            "reason": f.get("reason"),
        }
        d = f.get("diff")
        if d:
            c["diff"] = {
                "K": d["commits_between"],
                "born": d["born"],
                "deleted": d["deleted"],
                "edits": d["feature_changes_touched"] + d["strata_moves_touched"],
                "clock": d["ripple_clock"],
                "rank": d["ripple_rank"],
                "verdict": d["budget_verdict"],
                "reason": d["budget_reason"],
            }
        captions[f["index"]] = c
    last = mapped[-1]["index"]
    return f"""<section class="repo" data-repo="{k}" hidden>
<div class="ruler-wrap">
  <div class="ruler">{"".join(ticks)}</div>
  <div class="tbars">{"".join(bars)}</div>
  <input class="scrub" type="range" min="0" max="{frames[-1]["index"]}" value="{last}" aria-label="frame">
</div>
<div class="mode" role="group" aria-label="sheet"><button class="mbtn" data-mode="cutaway" aria-pressed="true">cutaway</button><button class="mbtn" data-mode="change" aria-pressed="false">change sheet</button><span class="mode-note">the change sheet marks each room by what happened to it since the previous frame, on the same layout</span></div>
<div class="cap" role="status"></div>
<div class="sheet"></div>
{templates}
<script type="application/json" class="caps">{json.dumps(captions)}</script>
</section>"""


tabs = "".join(
    f'<button class="tab" data-repo="{k}" role="tab" aria-selected="{"true" if i == 0 else "false"}">{escape(name)}</button>'
    for i, (k, name, _, _) in enumerate(repos)
)
blocks = "".join(repo_block(k, n, m) for k, n, _, m in repos)
gate = repos[0][3]["gate"]

page = f"""<title>Skeleton Time-lapse</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Condensed:wght@500;600&family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{
  --ground:#eef0ec; --sheet:#f7f8f5; --ink:#232830; --ink-2:#5a626e; --line:#c6ccc9; --accent:#1f4e9c; --accent-soft:#d8e3f4;
  --edits:#8a919c; --clock:#c58b1e; --rank:#c8322b; --structural:#4f7ea8;
  --sans:"IBM Plex Sans",system-ui,sans-serif; --cond:"IBM Plex Sans Condensed","IBM Plex Sans",system-ui,sans-serif; --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;
}}
@media (prefers-color-scheme: dark){{ :root:not([data-theme="light"]){{
  --ground:#101d31; --sheet:#182741; --ink:#d7dfe9; --ink-2:#93a2b6; --line:#2e4260; --accent:#7db2ff; --accent-soft:#213a5e;
  --edits:#6f7d92; --clock:#d9a84a; --rank:#e0564d; --structural:#6f9fca;
}} }}
:root[data-theme="dark"]{{
  --ground:#101d31; --sheet:#182741; --ink:#d7dfe9; --ink-2:#93a2b6; --line:#2e4260; --accent:#7db2ff; --accent-soft:#213a5e;
  --edits:#6f7d92; --clock:#d9a84a; --rank:#e0564d; --structural:#6f9fca;
}}
body{{background:var(--ground);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.5;margin:0}}
header{{padding:28px clamp(16px,4vw,48px) 18px;border-bottom:1px solid var(--line)}}
h1{{font-family:var(--cond);font-weight:600;font-size:30px;letter-spacing:.01em;margin:0 0 4px;text-wrap:balance}}
.q{{max-width:68ch;margin:0 0 18px;color:var(--ink-2)}}
.q b{{color:var(--ink);font-weight:600}}
.legend{{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--cond);font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--ink-2);margin-bottom:10px}}
.legend span::before{{content:"";display:inline-block;width:11px;height:11px;margin-right:6px;vertical-align:-1px;background:var(--c)}}
.sum{{display:grid;gap:8px;max-width:960px}}
.sum-row{{display:grid;grid-template-columns:minmax(180px,1fr) 3fr minmax(300px,2fr);gap:14px;align-items:center}}
.sum-name{{display:flex;flex-direction:column;line-height:1.25}} .sum-name b{{font-family:var(--mono);font-weight:500;font-size:14px}} .sum-name span{{font-size:12.5px;color:var(--ink-2)}}
.bar{{display:flex;width:100%;background:var(--line);overflow:hidden}}
.seg{{display:block;min-width:1px}} .seg.edits{{background:var(--edits)}} .seg.clock{{background:var(--clock)}} .seg.rank{{background:var(--rank)}} .seg.structural{{background:var(--structural)}}
.sum-nums{{display:flex;gap:10px;font-family:var(--mono);font-size:12.5px;font-variant-numeric:tabular-nums;align-items:baseline}}
.n{{min-width:34px}} .n.edits{{color:var(--ink-2)}} .n.clock{{color:var(--clock)}} .n.rank{{color:var(--rank);font-weight:500}} .n.structural{{color:var(--structural)}}
.tot{{color:var(--ink-2);font-size:12px;margin-left:auto;white-space:nowrap}}
nav{{display:flex;gap:2px;padding:14px clamp(16px,4vw,48px) 0;border-bottom:1px solid var(--line)}}
.tab{{font:500 14px var(--mono);color:var(--ink-2);background:transparent;border:1px solid transparent;border-bottom:none;padding:7px 14px;cursor:pointer;border-radius:3px 3px 0 0}}
.tab[aria-selected="true"]{{color:var(--ink);background:var(--sheet);border-color:var(--line);margin-bottom:-1px}}
.tab:focus-visible,.scrub:focus-visible,button:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.repo{{padding:18px clamp(16px,4vw,48px) 32px}} .repo[hidden]{{display:none}}
.ruler-wrap{{position:relative;height:96px;margin:0 8px 6px}}
.ruler{{position:absolute;left:0;right:0;top:0;height:40px;border-bottom:1px solid var(--ink-2)}}
.tick{{position:absolute;top:0;height:40px;border-left:1px solid var(--ink-2);padding-left:5px;font-family:var(--cond);font-size:12px;line-height:1.15;color:var(--ink-2);white-space:nowrap;cursor:pointer;transform:translateX(0)}}
.tick:last-child{{border-left-color:var(--ink)}} .tick .tk-n{{display:block;font-family:var(--mono);font-size:11px;font-variant-numeric:tabular-nums}}
.tick.skipped{{border-left-style:dashed;color:var(--line)}}
.tick.current{{color:var(--accent);border-left:2px solid var(--accent);font-weight:600}}
.tbars{{position:absolute;left:0;right:0;top:44px;height:16px}}
.tbar{{position:absolute;top:0;height:16px;display:flex;background:var(--line);cursor:pointer;border-right:1px solid var(--ground)}}
.tbar.current{{outline:2px solid var(--accent);outline-offset:1px}}
.scrub{{position:absolute;left:-8px;right:-8px;bottom:0;width:calc(100% + 16px);margin:0;accent-color:var(--accent)}}
.mode{{display:flex;gap:6px;align-items:center;margin:6px 0 0}}
.mbtn{{font:500 13px var(--mono);color:var(--ink-2);background:transparent;border:1px solid var(--line);padding:4px 10px;cursor:pointer;border-radius:3px}}
.mbtn[aria-pressed="true"]{{color:var(--ink);background:var(--accent-soft);border-color:var(--accent)}}
.mode-note{{font-size:12.5px;color:var(--ink-2);margin-left:8px}}
.cap{{font-family:var(--mono);font-size:13px;color:var(--ink);padding:8px 10px;background:var(--accent-soft);border-left:3px solid var(--accent);margin:8px 0 12px;min-height:1.5em}}
.cap .v-over{{color:var(--rank)}} .cap .v-within{{color:var(--structural)}} .cap .v-untested{{color:var(--ink-2)}}
.sheet{{overflow-x:auto;background:var(--sheet);border:1px solid var(--line);padding:10px}}
.sheet svg{{display:block;max-width:none}}
.foot{{padding:18px clamp(16px,4vw,48px) 40px;color:var(--ink-2);font-size:13px;max-width:78ch}}
.foot code{{font-family:var(--mono);font-size:12.5px}}
@media (max-width:760px){{.sum-row{{grid-template-columns:1fr}} .sum-nums{{flex-wrap:wrap}} .tot{{margin-left:0}}}}
@media (prefers-reduced-motion:no-preference){{.tick,.tbar{{transition:outline-color .12s}}}}
</style>
<header>
  <h1>Skeleton Time-lapse</h1>
  <p class="q">Twelve checkpoints on each repository's first-parent trunk, a skeleton per checkpoint under HEAD's gate, and the movement between adjacent skeletons decomposed. The phase's question: <b>is the named structure, over the history, structural change or the budget's jitter?</b> Only <b>rank</b> ripple is jitter: a feature or floor that moved under a room nobody touched because the percentile or the dependency layer shifted beneath it.</p>
  <div class="legend"><span style="--c:var(--edits)">edits — touched rooms</span><span style="--c:var(--clock)">clock — time reported</span><span style="--c:var(--rank)">rank — jitter</span><span style="--c:var(--structural)">structural — born / deleted</span></div>
  <div class="sum">{summary_rows()}</div>
</header>
<nav role="tablist">{tabs}</nav>
{blocks}
<p class="foot">Age geometry (strata are age bands, oldest at the bottom), maintainability profile with the onboarding overlay as corner badges. Substrate 0.3.0: age and recency are fractional days (D-022), after the time-lapse found integer-day ties flipping whole birth cohorts between floors. The change sheet (D-023) is one drawing per transition on the after frame's layout. Gate: <code>validation.json</code> at HEAD, substrate fingerprint <code>{escape((gate["substrate_config_fingerprint"] or "")[:12])}</code>, governs every frame — an early frame shows what HEAD's licensed structure looked like then, not what was licensed then. Percentiles re-rank per frame. The budget (D-018) was pinned at K = 5 commits; between these frames K runs from a dozen to fifteen hundred, so its verdicts here read as ripple accumulated over K, and its floors refuse most transitions on the large repositories. Arrow keys step frames. Spec: <code>time-lapse-spec.md</code>; decision: D-021.</p>
<script>
(function(){{
  const sections = Array.from(document.querySelectorAll('.repo'));
  const tabs = Array.from(document.querySelectorAll('.tab'));
  let active = null;
  function mount(sec, i){{
    const caps = JSON.parse(sec.querySelector('.caps').textContent);
    const c = caps[i]; if (!c) return;
    sec.querySelectorAll('.tick,.tbar').forEach(el => el.classList.toggle('current', +el.dataset.i === i));
    sec.querySelector('.scrub').value = i;
    const sheet = sec.querySelector('.sheet');
    sheet.replaceChildren();
    const mode = sec.dataset.mode || 'cutaway';
    let tpl = mode === 'change' ? sec.querySelector('template[data-change-i="' + i + '"]') : null;
    if (!tpl) tpl = sec.querySelector('template[data-i="' + i + '"]');
    let text = 'frame ' + c.i + ' · ' + c.sha + ' · ' + c.date + ' · ' + c.commits.toLocaleString() + ' commits · ' + c.rooms + ' rooms';
    if (c.status === 'skipped') text += ' · skipped: ' + c.reason;
    if (tpl) sheet.appendChild(tpl.content.cloneNode(true));
    const cap = sec.querySelector('.cap');
    cap.textContent = text;
    if (c.diff) {{
      const d = c.diff;
      const s = document.createElement('span');
      const cls = d.verdict === 'over_budget' ? 'v-over' : d.verdict === 'within_budget' ? 'v-within' : 'v-untested';
      s.innerHTML = ' · since previous: K=' + d.K + ', born ' + d.born + ', deleted ' + d.deleted + ', edits ' + d.edits + ', clock ' + d.clock + ', rank ' + d.rank + ' · budget <span class="' + cls + '">' + d.verdict.replace('_',' ') + (d.reason ? ' (' + d.reason.replace(/_/g,' ') + ')' : '') + '</span>';
      cap.appendChild(s);
    }}
    sec.dataset.current = i;
  }}
  function show(key){{
    sections.forEach(s => {{ s.hidden = s.dataset.repo !== key; }});
    tabs.forEach(t => t.setAttribute('aria-selected', t.dataset.repo === key ? 'true' : 'false'));
    active = sections.find(s => s.dataset.repo === key);
    mount(active, +(active.dataset.current ?? active.querySelector('.scrub').value));
  }}
  sections.forEach(sec => {{
    sec.querySelector('.scrub').addEventListener('input', e => mount(sec, +e.target.value));
    sec.querySelectorAll('.tick,.tbar').forEach(el => el.addEventListener('click', () => mount(sec, +el.dataset.i)));
    sec.querySelectorAll('.mbtn').forEach(btn => btn.addEventListener('click', () => {{
      sec.dataset.mode = btn.dataset.mode;
      sec.querySelectorAll('.mbtn').forEach(b => b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'));
      mount(sec, +(sec.dataset.current ?? sec.querySelector('.scrub').value));
    }}));
  }});
  tabs.forEach(t => t.addEventListener('click', () => show(t.dataset.repo)));
  document.addEventListener('keydown', e => {{
    if (!active || e.target.tagName === 'INPUT') return;
    const cur = +active.dataset.current, max = +active.querySelector('.scrub').max;
    if (e.key === 'ArrowLeft') mount(active, Math.max(0, cur - 1));
    if (e.key === 'ArrowRight') mount(active, Math.min(max, cur + 1));
  }});
  show(sections[0].dataset.repo);
}})();
</script>
"""
# --- hoist repeated inline SVG styles into classes (size: every room carries the same few styles)
styles: dict[str, str] = {}


def _cls(m):
    st = m.group(1)
    if st not in styles:
        styles[st] = f"s{len(styles)}"
    return f'class="{styles[st]}"'


page = (
    re.sub(r'style="([^"]*)"(?=[^>]*>)', lambda m: _cls(m) if page_svg_region else m.group(0), page)
    if False
    else page
)


# apply only inside <svg ...>...</svg> so the page's own inline styles are untouched
def _hoist(svg_m):
    return re.sub(r'style="([^"]*)"', _cls, svg_m.group(0))


page = re.sub(r"<svg\b.*?</svg>", _hoist, page, flags=re.S)
sheet = "<style>" + "".join(f".{c}{{{st}}}" for st, c in styles.items()) + "</style>"
page = page.replace("</style>", "</style>" + sheet, 1)
OUT.write_text(page, encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size / 1e6:.1f} MB) with {[k for k, *_ in repos]}")
