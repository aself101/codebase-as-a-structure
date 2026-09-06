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
    out.append(
        f"*validation `{doc['validation_version']}` · substrate fingerprint `{doc['substrate_config_fingerprint'][:12]}…` · "
        f"validation fingerprint `{doc['validation_config_fingerprint'][:12]}…`. "
        "Verdicts are stated for fix-**activity** (the declared §3.4.1 proxy), never defect origin.*\n"
    )

    vc = doc["validation_config"]
    out.append("## Gate configuration (every floor, so a loosened one is visible here)\n")
    out.append(
        f"- holdout: frac {vc['holdout_frac']}, ROC margin +{vc['auc_margin']}, PR-AUC ×{vc['pr_auc_mult']}, coverage ≥ {vc['coverage_min']}, "
        f"signal floor ×{vc['signal_floor_mult']} base rate, **min test repos {vc['min_repos']}**"
    )
    out.append(
        f"- asserted: K {vc['stability_perturbation_k']}, **stability eps {vc['stability_eps']} / delta {vc['stability_delta']}**, "
        f"min compared {vc['stability_min_n']}, max excluded {vc['stability_max_excluded_frac']}, max modal share {vc['degenerate_max_modal_share']}, "
        f"τ floors G3 {vc['tau_asserted']} / G2 {vc['tau_instrument']}, retire {vc['tau_retire']}, **m_asserted {vc['m_asserted']}**"
    )
    out.append(
        f"- label regex (frozen, validation side): `{vc['label_subject_regex']}`; bootstrap {vc['bootstrap_n']}, permutation {vc['permutation_n']}, seed {vc['rng_seed']}"
    )
    sec = doc.get("substrate_effective_config") or {}
    w = sec.get("weights") or {}
    if w:
        out.append(
            "- substrate weights validated (the fingerprint's preimage): "
            + "; ".join(
                f"`{k}` = {{{', '.join(f'{i}: {v}' for i, v in ws.items())}}}"
                for k, ws in w.items()
            )
        )
        out.append(
            f"- substrate feature-side fix regex: `{sec.get('fix_subject_regex')}`"
            + (
                "  ⚠ differs from the label regex"
                if sec.get("fix_subject_regex") != vc["label_subject_regex"]
                else " (same as label regex)"
            )
        )
        out.append(
            f"- toolchain: {', '.join(f'{k}={v}' for k, v in (sec.get('toolchain_versions') or {}).items())}"
        )
    out.append("")

    out.append("## Reference repos\n")
    out.append(
        "| repo | role | expected (D-009) | HEAD | commits | nodes | population | split | holdout commits | eligible | coverage | positives | base rate | fix-label rate | degenerate |"
    )
    out.append("|---|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|")
    for r in doc["reference_repos"]:
        h = r.get("holdout", {})
        a = r.get("asserted", {})
        exp = r.get("expected_role")
        exp_s = (exp or "not pre-registered") + ("" if exp == r.get("role") else " ⚠ MISMATCH")
        out.append(
            f"| `{r['name']}` | {r.get('role', 'test')} | {exp_s} | `{r['head_sha'][:10]}` | {h.get('n_commits', '–')} | {h.get('n_head_nodes', '–')} | {a.get('n_population', '–')} | "
            f"`{str(h.get('split_sha', ''))[:10]}` | {h.get('n_holdout_commits', '–')} | {h.get('n_eligible', '–')} | "
            f"{_f(h.get('coverage'))} | {h.get('n_positives', '–')} | {_f(h.get('base_rate'))} | {_f(h.get('fix_label_rate'))} | {h.get('degenerate') or '–'} |"
        )
    out.append("")
    att = doc.get("substrate_attestations") or {}
    if att:
        out.append("**Substrate attestations** (cache file → seed, sha256 of the scored bytes):\n")
        for k, v in att.items():
            out.append(f"- `{k}`: seed `{v['seed'][:12]}…`, bytes `{v['bytes_sha256'][:12]}…`")
        out.append("")

    out.append("## 1. Verdict table — predictive signals\n")
    tc = doc.get("tuned_config_commit")
    out.append(
        f"*Verdicts count **test**-role repos only (D-009); tuning-role rows are in-sample and shown for the record. "
        f"Tuned config commit: `{tc[:12] if tc else 'none (spec placeholder weights)'}`.*\n"
    )
    out.append(
        "| signal | status | repo | role | ROC-AUC | best-baseline ROC | PR-AUC | best-baseline PR | base rate | p@10 | τ(index, baseline) | passed | failed clauses |"
    )
    out.append("|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|")
    for name, s in sig.items():
        if s["kind"] != "predictive":
            continue
        for r in s["holdout"]["per_repo"]:
            bb = r.get("best_baseline")
            bm = (r.get("baselines") or {}).get(bb, {}) if bb else {}
            out.append(
                f"| `{name}` | **{s['status']}** | `{r['name']}` | {r.get('role', 'test')} | {_f(r.get('roc_auc'))} | {_f(bm.get('roc_auc'))} ({bb or '–'}) | "
                f"{_f(r.get('pr_auc'))} | {_f(bm.get('pr_auc'))} | {_f(r.get('base_rate'))} | "
                f"{_f((r.get('precision_at_k') or {}).get('10'))} | {_f(r.get('tau_vs_best_baseline'), 2)} | {_f(r.get('passed'))} | "
                f"{', '.join(r.get('failed_clauses') or []) or (r.get('degenerate') or '–')} |"
            )
    out.append("")

    out.append("## 2. Where it failed\n")
    any_fail = False
    for name, s in sig.items():
        if s["kind"] != "predictive" or s["status"] == "validated":
            continue
        any_fail = True
        out.append(f"- **`{name}`** — `{s['status']}` ({s.get('reason', '')}).")
        for r in s["holdout"]["per_repo"]:
            if r.get("degenerate"):
                out.append(f"  - `{r['name']}`: not scored — {r['degenerate']}.")
                continue
            bb = r.get("best_baseline")
            bm = (r.get("baselines") or {}).get(bb, {})
            d_roc = (r.get("roc_auc") or 0) - (bm.get("roc_auc") or 0)
            ratio = ((r.get("pr_auc") or 0) / bm["pr_auc"]) if bm.get("pr_auc") else float("nan")
            out.append(
                f"  - `{r['name']}`: ROC-AUC {_f(r.get('roc_auc'))} vs {bb} {_f(bm.get('roc_auc'))} (Δ {d_roc:+.3f}, need +{doc['validation_config']['auc_margin']}); "
                f"PR-AUC {_f(r.get('pr_auc'))} vs {_f(bm.get('pr_auc'))} (×{_f(ratio, 2)}, need ×{doc['validation_config']['pr_auc_mult']}); "
                f"{'passed' if r.get('passed') else 'failed: ' + ', '.join(r.get('failed_clauses') or [])}."
            )
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
    out.append(
        "*Grounding classes: G1 measurement (stability only; instrument is git or the file), "
        "G2 second instrument (fan_in ↔ an independent scanner; floor τ ≥ "
        f"{doc['validation_config']['tau_instrument']}), G3 cross-modal (a different modality; floor τ ≥ "
        f"{doc['validation_config']['tau_asserted']}), G4 derived (stability + every input asserted; the name carries no "
        "claim beyond its inputs). Stability compares nodes untouched by the K removed commits.*\n"
    )
    out.append(
        "| signal | class | status | repo | reason | stability med / p95 / max Δ (n; tail operand) | distinct | stable | counterpart | n | τ-b | 95% CI | perm p | corroborated |"
    )
    out.append("|---|---|---|---|---|---:|---:|---|---|---:|---:|---|---:|---|")
    for name, s in sig.items():
        if s["kind"] != "descriptive":
            continue
        for r in s["grounding"]["per_repo"]:
            st, cm = r.get("stability", {}), r.get("corroboration", {})
            ci = cm.get("tau_b_ci")
            ci_s = f"[{_f(ci[0])}, {_f(ci[1])}]" if ci else "–"
            corro = (
                _f(cm.get("passed")) if cm.get("passed") is not None else (cm.get("reason") or "–")
            )
            inst = cm.get("counterpart") or s.get("instrument") or "–"
            out.append(
                f"| `{name}` | {s['grounding_class']} | **{s['status']}** | `{r['name']}` | {r.get('reason') or '–'} | "
                f"{_f(st.get('median_abs_delta'))} / {_f(st.get('p95_abs_delta'))} / {_f(st.get('max_abs_delta'))} ({st.get('n', '–')}; {st.get('operand', 'max')}) | {st.get('distinct_values', '–')} | {_f(st.get('passed'))} | "
                f"`{inst}` | {cm.get('n', '–')} | {_f(cm.get('tau_b'))} | {ci_s} | {_f(cm.get('permutation_p'))} | {corro} |"
            )
    out.append("")
    heur = [
        (n, s["heuristic"])
        for n, s in sig.items()
        if s["kind"] == "descriptive" and s.get("heuristic")
    ]
    if heur:
        out.append("**Declared heuristics inside G1 (bounded risks, not certifications):**\n")
        for n, h in heur:
            out.append(f"- `{n}`: {h}")
        out.append("")
    nd = [
        n
        + (
            " (fixture-backed: " + s["adversarial_fixture"] + ")"
            if s.get("adversarial_fixture")
            else " ⚠ NO FIXTURE"
        )
        for n, s in sig.items()
        if s["kind"] == "descriptive" and s.get("non_discriminating")
    ]
    out.append(
        f"**Non-discriminating pairs (min lower-CI τ ≥ {doc['validation_config']['tau_retire']} on every repo — cannot fail, so not a falsifier; adversarial fixture required):** "
        + (", ".join(f"`{n}`" for n in nd) if nd else "none")
        + "\n"
    )
    out.append(
        "**τ distribution across repos (the §2.4 known limit — a counterpart that cannot fail is not a falsifier):**\n"
    )
    for name, s in sig.items():
        if s["kind"] != "descriptive" or s.get("counterpart") is None:
            continue
        taus = [
            r["corroboration"].get("tau_b")
            for r in s["grounding"]["per_repo"]
            if r.get("corroboration", {}).get("tau_b") is not None
        ]
        out.append(
            f"- `{name}` ↔ `{s['counterpart']}` ({s['grounding_class']}): "
            + ", ".join(_f(t, 2) for t in taus)
        )
    out.append("")
    out.append("**Reported correlates (never gating):**\n")
    for name, s in sig.items():
        if s["kind"] != "descriptive":
            continue
        for r in s["grounding"]["per_repo"]:
            for c, blk in (r.get("correlates") or {}).items():
                if blk.get("tau_b") is not None:
                    ci = blk.get("tau_b_ci") or [None, None]
                    out.append(
                        f"- `{name}` ~ `{c}` on `{r['name']}`: τ {_f(blk['tau_b'], 2)} [{_f(ci[0], 2)}, {_f(ci[1], 2)}]"
                    )
    out.append("")
    out.append("## 5. Cross-source corroboration (§3A)\n")
    out.append(
        "- Not run in M1 (D-005): §3A is built after the holdout leaves a `validated` signal to corroborate.\n"
    )

    out.append("## 6. Recognition record (§2.4.3, D-010) — sealed rankings, n = 1, never gating\n")
    any_rec = False
    for r in doc["reference_repos"]:
        ref = (r.get("asserted") or {}).get("recognition_ref")
        if not ref:
            continue
        any_rec = True
        out.append(f"### `{r['name']}` — `{ref}`\n")
        try:
            from pathlib import Path

            text = Path(ref).read_text(encoding="utf-8")
        except OSError:
            out.append("_(file not readable at report time)_\n")
            continue
        prov = [ln for ln in text.splitlines() if ln.startswith("*Provenance")]
        if prov:
            out.append(prov[0] + "\n")
        # recognition numbers per signal
        rows = []
        for name, s in sig.items():
            for pr in (
                s.get("holdout", {}).get("per_repo")
                if s["kind"] == "predictive"
                else s.get("grounding", {}).get("per_repo")
            ) or []:
                if pr.get("name") == r["name"] and pr.get("recognition"):
                    rec = pr["recognition"]
                    rows.append(
                        f"| `{name}` | list {rec.get('list')} | {rec.get('ranked')} | {_f(rec.get('overlap_at_k'), 2)} | "
                        f"{_f(rec.get('tau_b_on_ranked'), 2)} | {', '.join(f'`{m}`' for m in (rec.get('missing') or [])[:6]) or '–'} |"
                    )
        if rows:
            out.append(
                "| signal | source | ranked & present | overlap@10 | τ-b on ranked | items not in substrate |"
            )
            out.append("|---|---|---:|---:|---:|---|")
            out.extend(rows)
            out.append("")
        # quote the pre-registered predictions verbatim
        for header in ("## 5.", "## 6."):
            start = text.find(header)
            if start < 0:
                continue
            end = text.find("\n## ", start + 1)
            block = text[start : end if end > 0 else None].strip()
            lines = [
                ln
                for ln in block.splitlines()
                if not ln.startswith('*"') and not ln.startswith("*Optional")
            ]
            out.append("> " + "\n> ".join(lines))
            out.append("")
    if not any_rec:
        out.append("- no sealed rankings found for these repos\n")
    return "\n".join(out)
