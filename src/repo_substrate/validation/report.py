"""The holdout report (validation-spec §6.2): writes down where the indices lie."""

from __future__ import annotations

from typing import Any


def _f(v: Any, dp: int = 3) -> str:
    if v is None:
        return "–"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, float):
        return f"{v:.{dp}f}"
    return str(v)


def render_holdout_report(doc: dict[str, Any]) -> str:
    sig = doc["signals"]
    out: list[str] = []
    out.append("# Holdout report — validation gate\n")
    out.append(f"*validation `{doc['validation_version']}` · substrate fingerprint `{doc['substrate_config_fingerprint'][:12]}…` · "
               f"validation fingerprint `{doc['validation_config_fingerprint'][:12]}…`. "
               "Verdicts are stated for fix-**activity** (the declared §3.4.1 proxy), never defect origin.*\n")

    out.append("## Reference repos\n")
    out.append("| repo | HEAD | commits | nodes | split | holdout commits | eligible | coverage | positives | base rate | fix-label rate | degenerate |")
    out.append("|---|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|")
    for r in doc["reference_repos"]:
        h = r.get("holdout", {})
        out.append(f"| `{r['name']}` | `{r['head_sha'][:10]}` | {h.get('n_commits','–')} | {h.get('n_head_nodes','–')} | "
                   f"`{str(h.get('split_sha',''))[:10]}` | {h.get('n_holdout_commits','–')} | {h.get('n_eligible','–')} | "
                   f"{_f(h.get('coverage'))} | {h.get('n_positives','–')} | {_f(h.get('base_rate'))} | {_f(h.get('fix_label_rate'))} | {h.get('degenerate') or '–'} |")
    out.append("")

    out.append("## 1. Verdict table — predictive signals\n")
    out.append("| signal | status | repo | ROC-AUC | best-baseline ROC | PR-AUC | best-baseline PR | base rate | p@10 | passed | failed clauses |")
    out.append("|---|---|---|---:|---:|---:|---:|---:|---:|---|---|")
    for name, s in sig.items():
        if s["kind"] != "predictive":
            continue
        for r in s["holdout"]["per_repo"]:
            bb = r.get("best_baseline")
            bm = (r.get("baselines") or {}).get(bb, {}) if bb else {}
            out.append(f"| `{name}` | **{s['status']}** | `{r['name']}` | {_f(r.get('roc_auc'))} | {_f(bm.get('roc_auc'))} ({bb or '–'}) | "
                       f"{_f(r.get('pr_auc'))} | {_f(bm.get('pr_auc'))} | {_f(r.get('base_rate'))} | "
                       f"{_f((r.get('precision_at_k') or {}).get('10'))} | {_f(r.get('passed'))} | "
                       f"{', '.join(r.get('failed_clauses') or []) or (r.get('degenerate') or '–')} |")
    out.append("")

    out.append("## 2. Where it failed\n")
    any_fail = False
    for name, s in sig.items():
        if s["kind"] != "predictive" or s["status"] == "validated":
            continue
        any_fail = True
        out.append(f"- **`{name}`** — `{s['status']}` ({s.get('reason','')}).")
        for r in s["holdout"]["per_repo"]:
            if r.get("degenerate"):
                out.append(f"  - `{r['name']}`: not scored — {r['degenerate']}.")
                continue
            bb = r.get("best_baseline")
            bm = (r.get("baselines") or {}).get(bb, {})
            d_roc = (r.get("roc_auc") or 0) - (bm.get("roc_auc") or 0)
            ratio = ((r.get("pr_auc") or 0) / bm["pr_auc"]) if bm.get("pr_auc") else float("nan")
            out.append(f"  - `{r['name']}`: ROC-AUC {_f(r.get('roc_auc'))} vs {bb} {_f(bm.get('roc_auc'))} (Δ {d_roc:+.3f}, need +{doc['validation_config']['auc_margin']}); "
                       f"PR-AUC {_f(r.get('pr_auc'))} vs {_f(bm.get('pr_auc'))} (×{_f(ratio,2)}, need ×{doc['validation_config']['pr_auc_mult']}); "
                       f"{'passed' if r.get('passed') else 'failed: ' + ', '.join(r.get('failed_clauses') or [])}.")
    if not any_fail:
        out.append("- none")
    out.append("")

    out.append("## 3. Coverage caveats\n")
    for r in doc["reference_repos"]:
        h = r.get("holdout", {})
        note = f"coverage {_f(h.get('coverage'))} ({h.get('n_eligible')} of {h.get('n_head_nodes')} HEAD nodes eligible)"
        if h.get("degenerate"):
            note += f"; **{h['degenerate']}**"
        out.append(f"- `{r['name']}`: {note}.")
    for name, s in sig.items():
        if s["status"] == "untested":
            out.append(f"- `{name}`: untested — {s.get('reason')}.")
    out.append("")

    out.append("## 4. Descriptive signals (§2.4)\n")
    out.append("*Grounding classes: G1 measurement (stability only; instrument is git or the file), "
               "G2 second instrument (fan_in ↔ an independent scanner; floor τ ≥ "
               f"{doc['validation_config']['tau_instrument']}), G3 cross-modal (a different modality; floor τ ≥ "
               f"{doc['validation_config']['tau_asserted']}), G4 derived (stability + every input asserted; the name carries no "
               "claim beyond its inputs). Stability compares nodes untouched by the K removed commits.*\n")
    out.append("| signal | class | status | repo | reason | stability med / p95 / max Δ | stable | counterpart | τ-b | 95% CI | perm p | corroborated | recognition overlap@10 / τ |")
    out.append("|---|---|---|---|---|---:|---|---|---:|---|---:|---|---|")
    for name, s in sig.items():
        if s["kind"] != "descriptive":
            continue
        for r in s["grounding"]["per_repo"]:
            st, cm, rec = r.get("stability", {}), r.get("corroboration", {}), r.get("recognition")
            ci = cm.get("tau_b_ci")
            ci_s = f"[{_f(ci[0])}, {_f(ci[1])}]" if ci else "–"
            rec_s = f"{_f(rec.get('overlap_at_k'),2)} / {_f(rec.get('tau_b_on_ranked'),2)}" if rec and rec.get("ranked") else "–"
            corro = _f(cm.get("passed")) if cm.get("passed") is not None else (cm.get("reason") or "–")
            out.append(f"| `{name}` | {s['grounding_class']} | **{s['status']}** | `{r['name']}` | {r.get('reason') or '–'} | "
                       f"{_f(st.get('median_abs_delta'))} / {_f(st.get('p95_abs_delta'))} / {_f(st.get('max_abs_delta'))} | {_f(st.get('passed'))} | "
                       f"`{cm.get('counterpart') or cm.get('instrument') or '–'}` | {_f(cm.get('tau_b'))} | {ci_s} | {_f(cm.get('permutation_p'))} | {corro} | {rec_s} |")
    out.append("")
    out.append("**τ distribution across repos (the §2.4 known limit — a counterpart that cannot fail is not a falsifier):**\n")
    for name, s in sig.items():
        if s["kind"] != "descriptive" or s.get("counterpart") is None:
            continue
        taus = [r["corroboration"].get("tau_b") for r in s["grounding"]["per_repo"] if r.get("corroboration", {}).get("tau_b") is not None]
        out.append(f"- `{name}` ↔ `{s['counterpart']}` ({s['grounding_class']}): " + ", ".join(_f(t, 2) for t in taus))
    out.append("")
    out.append("**Reported correlates (never gating):**\n")
    for name, s in sig.items():
        if s["kind"] != "descriptive":
            continue
        for r in s["grounding"]["per_repo"]:
            for c, blk in (r.get("correlates") or {}).items():
                if blk.get("tau_b") is not None:
                    ci = blk.get("tau_b_ci") or [None, None]
                    out.append(f"- `{name}` ~ `{c}` on `{r['name']}`: τ {_f(blk['tau_b'],2)} [{_f(ci[0],2)}, {_f(ci[1],2)}]")
    out.append("")
    out.append("## 5. Cross-source corroboration (§3A)\n")
    out.append("- Not run in M1 (D-005): §3A is built after the holdout leaves a `validated` signal to corroborate.\n")
    return "\n".join(out)
