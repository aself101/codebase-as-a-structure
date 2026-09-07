"""PROTOTYPE — throwaway. Does a tabular architect's brief read at all? (D-038 item 7)

    uv run python scripts/prototype_tabular_brief.py [reports/<tag>-m3x] [out/prototype-tabular-brief.html]

Three variants of the brief rendered from the same facts sheets, switchable with ?variant=A|B|C
(or #variant=…) and a floating bar (← → keys). Nothing here is production: no lint, no tests,
no model; every number is read straight off the sheet so the page can be judged as a page.

  A — Register table: one row per feature with fixed slots (the D-038 proposal literally).
  B — Wing ledger: rows are wings, columns are features; composition first, marks second.
  C — Room roll: rows are rooms grouped by directory, columns are marks as dots; overlaps
      and composition are visible as patterns, no sentence anywhere except the stance.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "reports" / "2026-09-06g-m3x"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "out" / "prototype-tabular-brief.html"

sheets = {}
for p in sorted(SRC.glob("*.facts.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    d.pop("rooms", None)  # per-room metrics are not needed by any variant
    sheets[p.name.split(".")[0]] = d

PAGE = r"""<title>Tabular Brief Prototype</title>
<style>
:root{--bg:#f6f4ee;--ink:#1e1c18;--mute:#6b665c;--line:#d8d3c7;--card:#fffdf8;--acc:#7a4b12;--water:#5b7c99;--warn:#b0452b;--dot:#2b2b2b;--hatch:#c2185b}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#171613;--ink:#ebe6da;--mute:#a49d8e;--line:#3a3730;--card:#1f1d19;--acc:#d9a35a;--water:#8fb0cc;--warn:#e07a5f;--dot:#ebe6da;--hatch:#f06292}}
:root[data-theme="dark"]{--bg:#171613;--ink:#ebe6da;--mute:#a49d8e;--line:#3a3730;--card:#1f1d19;--acc:#d9a35a;--water:#8fb0cc;--warn:#e07a5f;--dot:#ebe6da;--hatch:#f06292}
body{background:var(--bg);color:var(--ink);font:14px/1.45 ui-sans-serif,system-ui,sans-serif;margin:0;padding:24px 28px 90px}
h1{font-size:18px;margin:0 0 4px;font-weight:600}h2{font-size:15px;margin:22px 0 8px;font-weight:600}
.note{color:var(--mute);font-size:12.5px;max-width:70ch}
.repo{margin:0 0 36px;padding:16px 18px;background:var(--card);border:1px solid var(--line);border-radius:6px}
.hdr{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px 18px;margin:8px 0 14px}
.hdr div b{display:block;font-size:11px;letter-spacing:.04em;text-transform:uppercase;color:var(--mute)}
.hdr div span{font-variant-numeric:tabular-nums}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}
th,td{border-bottom:1px solid var(--line);padding:5px 8px;text-align:left;vertical-align:top}
th{font-size:11px;letter-spacing:.04em;text-transform:uppercase;color:var(--mute);font-weight:600}
td.n,th.n{text-align:right}
.pos{color:var(--mute);font-size:12.5px}
.dec td{color:var(--mute)}.dec td:first-child{border-left:3px dashed var(--hatch);padding-left:6px}
.tag{display:inline-block;padding:0 6px;border:1px solid var(--line);border-radius:10px;font-size:11.5px;margin-right:4px;white-space:nowrap}
.rel{font-size:12.5px}
.wrap{overflow-x:auto}
.stance{margin-top:14px;font-size:12.5px;color:var(--mute);max-width:80ch}
.dots td{padding:2px 6px;font-size:12.5px;white-space:nowrap}
.dots .d{text-align:center;width:22px}
.dots .on{color:var(--dot)}.dots .dc{color:var(--hatch)}
.dir{background:var(--bg);font-weight:600}
.bar{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);background:#111;color:#fff;border-radius:999px;padding:8px 14px;display:flex;gap:14px;align-items:center;box-shadow:0 6px 24px rgba(0,0,0,.35);font-size:13px;z-index:9}
.bar button{background:transparent;color:#fff;border:1px solid #666;border-radius:999px;width:28px;height:28px;cursor:pointer}
.bar button:focus-visible{outline:2px solid #fff}
[hidden]{display:none!important}
</style>
<h1>Tabular brief — prototype (throwaway)</h1>
<p class="note">Three shapes of the same facts sheets (brief 0.5.0, gate 179d8acb7b0c). No sentence on this page was written by a model; every cell is a field. The question: can a reader take in a building from rows, and where does a sentence turn out to be needed after all? Flip with the bar or ← →.</p>
<div id="root"></div>
<div class="bar"><button id="prev" aria-label="previous variant">←</button><span id="label"></span><button id="next" aria-label="next variant">→</button></div>
<script>
const SHEETS = __DATA__;
const VARIANTS = {A:"Register table", B:"Wing ledger", C:"Room roll"};
const ORDER = Object.keys(VARIANTS);
function esc(s){return String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));}
function short(k){return k.split("/").pop();}
function header(f){
  const w = Object.entries(f.wings).map(([k,v])=>`${esc(k)} ${v}`).join(" · ");
  return `<div class="hdr">
    <div><b>rooms</b><span>${f.population} in ${f.wing_count} wings</span></div>
    <div><b>wings</b><span>${w}</span></div>
    <div><b>diagnostic marks</b><span>${f.diagnostic_count} (base profile ${f.diagnostic_count_base})</span></div>
    <div><b>decorative marks</b><span>${f.decorative.count}: ${f.decorative.features.join(", ")||"none"}</span></div>
    <div><b>rooms with 2+ marks</b><span>${f.co_located_rooms}</span></div>
    <div><b>gate</b><span>${(f.gate_fingerprint||"").slice(0,12)} · ${Object.values(f.gate).filter(v=>v==="asserted").length} of ${Object.keys(f.gate).length} signals asserted; none validated</span></div>
    <div><b>calibration</b><span>in-repo, self-relative; one frame</span></div>
  </div>`;
}
function relations(f, key){
  const out=[];
  for(const ov of f.overlaps||[]){
    if(ov.a!==key && ov.b!==key) continue;
    const other = ov.a===key? ov.b: ov.a;
    if(ov.relation==="identical"){
      out.push(`= ${esc(short(other))}${ov.shared_predicate? " (same predicate, two profiles)": ov.inert_terms&&ov.inert_terms.length? ` (${esc(ov.inert_terms.join(", "))} excludes nothing)`:""}`);
    } else if(ov.a===key){
      out.push(`⊂ ${esc(short(other))} (${ov.n_outside} of its rooms outside)`);
    } else {
      out.push(`⊃ ${esc(short(other))} (${ov.n_outside} outside it)`);
    }
  }
  return out.join("<br>");
}
function variantA(f){
  const rows = f.features.map(x=>{
    const key=`${x.profile}/${x.feature}`;
    const bw = Object.entries(x.by_wing).map(([k,v])=>`<span class="tag">${esc(k)} ${v}</span>`).join("");
    const dd = x.dominant_dir? `${esc(x.dominant_dir.dir)} ${x.dominant_dir.n} / ${x.dominant_dir.population}`:"";
    return `<tr class="${x.decorative?"dec":""}"><td>${esc(x.feature)}<div class="pos">${esc(x.profile)}${x.position_name?" · "+esc(x.position_name):""}</div></td>
      <td class="n">${x.count}</td><td>${bw}</td><td>${dd}</td><td class="rel">${relations(f,key)}</td>
      <td class="pos">${x.decorative? "decorative — "+esc(x.decorative_reason||""): esc(x.predicate)}</td></tr>`;
  }).join("");
  return `<div class="wrap"><table><thead><tr><th>feature · position</th><th class="n">rooms</th><th>by wing</th><th>dominant directory n / its rooms</th><th>relation to</th><th>predicate or reason</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}
function variantB(f){
  const feats = f.features;
  const wings = Object.keys(f.wings);
  const head = feats.map(x=>`<th class="n" title="${esc(x.position_name||x.predicate)}">${esc(x.feature)}${x.decorative?" ◌":""}</th>`).join("");
  const rows = wings.map(w=>{
    const cells = feats.map(x=>{const v=x.by_wing[w]||0; return `<td class="n" style="opacity:${v?1:.25}">${v||"·"}</td>`;}).join("");
    return `<tr><td>${esc(w)}<div class="pos">${f.wings[w]} rooms</div></td>${cells}</tr>`;
  }).join("");
  const tot = feats.map(x=>`<td class="n"><b>${x.count}</b></td>`).join("");
  const pos = feats.map(x=>`<td class="pos">${esc(x.position_name||"")}</td>`).join("");
  const rel = (f.overlaps||[]).map(ov=>`<span class="tag">${esc(short(ov.a))} ${ov.relation==="identical"?"=":"⊂"} ${esc(short(ov.b))}${ov.relation==="within"?` (+${ov.n_outside})`:(ov.shared_predicate?" (same predicate)":(ov.inert_terms&&ov.inert_terms.length?` (${esc(ov.inert_terms.join(", "))} inert)`:""))}</span>`).join(" ");
  return `<div class="wrap"><table><thead><tr><th>wing</th>${head}</tr></thead><tbody>${rows}<tr><td><b>all</b></td>${tot}</tr><tr><td class="pos">position</td>${pos}</tr></tbody></table></div>
    <h2>relations</h2><div class="rel">${rel||"none"}</div><p class="note">◌ decorative: ${f.decorative.features.map(n=>{const x=feats.find(y=>y.feature===n);return esc(n)+" — "+esc(x?x.decorative_reason:"");}).join("; ")}</p>`;
}
function variantC(f){
  const feats = f.features.filter(x=>!x.decorative);
  const dec = f.features.filter(x=>x.decorative);
  const byRoom = {};
  for(const x of f.features) for(const r of x.rooms){(byRoom[r]=byRoom[r]||new Set()).add(`${x.profile}/${x.feature}`);}
  const rooms = Object.keys(byRoom).sort((a,b)=>byRoom[b].size-byRoom[a].size || a.localeCompare(b));
  const groups = {};
  for(const r of rooms){const d=r.includes("/")?r.slice(0,r.lastIndexOf("/")):"(root)";(groups[d]=groups[d]||[]).push(r);}
  const dirs = Object.keys(groups).sort((a,b)=>groups[b].length-groups[a].length || a.localeCompare(b));
  const head = feats.map(x=>`<th class="d" title="${esc(x.position_name||x.predicate)}">${esc(x.feature.slice(0,4))}</th>`).join("")+dec.map(x=>`<th class="d dc" title="decorative — ${esc(x.decorative_reason||"")}">${esc(x.feature.slice(0,4))}</th>`).join("");
  let body="";
  let shown=0;
  for(const d of dirs){
    const rs = groups[d];
    body += `<tr class="dir"><td colspan="${feats.length+dec.length+1}">${esc(d)} — ${rs.length} marked of ${f.population} rooms</td></tr>`;
    for(const r of rs.slice(0,12)){
      const cells = feats.map(x=>`<td class="d ${byRoom[r].has(x.profile+"/"+x.feature)?"on":""}">${byRoom[r].has(x.profile+"/"+x.feature)?"●":"·"}</td>`).join("")
        + dec.map(x=>`<td class="d ${byRoom[r].has(x.profile+"/"+x.feature)?"dc":""}">${byRoom[r].has(x.profile+"/"+x.feature)?"◌":"·"}</td>`).join("");
      body += `<tr><td>${esc(r.slice(d.length+1)||r)}</td>${cells}</tr>`;
      shown++;
    }
    if(rs.length>12) body += `<tr><td class="pos" colspan="${feats.length+dec.length+1}">… ${rs.length-12} more rooms in ${esc(d)}</td></tr>`;
  }
  return `<p class="note">Rows are marked rooms grouped by directory, most-marked first; ● a diagnostic mark, ◌ a decorative one (excluded from diagnosis). Columns: ${feats.map(x=>esc(x.feature)).join(", ")}${dec.length?"; decorative: "+dec.map(x=>esc(x.feature)).join(", "):""}.</p>
    <div class="wrap"><table class="dots"><thead><tr><th>room</th>${head}</tr></thead><tbody>${body}</tbody></table></div>`;
}
function render(){
  const v = current();
  const root = document.getElementById("root");
  root.innerHTML = Object.entries(SHEETS).map(([name,f])=>`<section class="repo"><h1>${esc(f.repo.name)} <span class="pos">@ ${esc(f.repo.head_sha.slice(0,8))} · ${esc(f.profile)} + ${(f.overlays||[]).join(", ")} · ${esc(f.geometry)}</span></h1>${header(f)}${({A:variantA,B:variantB,C:variantC})[v](f)}<p class="stance">${esc(f.stance)}</p></section>`).join("");
  document.getElementById("label").textContent = `${v} (${VARIANTS[v]})`;
}
function current(){
  const q = new URLSearchParams(location.search).get("variant") || (location.hash.match(/variant=([ABC])/)||[])[1];
  return ORDER.includes(q)? q: "A";
}
function go(delta){
  const i = (ORDER.indexOf(current())+delta+ORDER.length)%ORDER.length;
  try{ const u=new URL(location.href); u.searchParams.set("variant",ORDER[i]); u.hash=`variant=${ORDER[i]}`; history.replaceState(null,"",u); }catch(e){ location.hash=`variant=${ORDER[i]}`; }
  render();
}
document.getElementById("prev").onclick=()=>go(-1);
document.getElementById("next").onclick=()=>go(1);
document.addEventListener("keydown",e=>{const t=e.target; if(t&&(t.tagName==="INPUT"||t.tagName==="TEXTAREA"||t.isContentEditable)) return; if(e.key==="ArrowLeft") go(-1); if(e.key==="ArrowRight") go(1);});
window.addEventListener("hashchange",render);
render();
</script>
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(PAGE.replace("__DATA__", json.dumps(sheets, ensure_ascii=False)), encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB) with {list(sheets)}; variants ?variant=A|B|C")
