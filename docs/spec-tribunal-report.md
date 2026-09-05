# Spec Tribunal — codebase-as-structure (pre-C1 gate)

*Final adversarial review before Component 1 (repo-substrate) implementation. Five lenses: architect (buildability), Popper (falsifiability), Hume (evidence), contradiction-detector (consistency), circumvention-forecaster (exploitability), plus synthesis.*

**Date:** 2026-06-19 · **Verdict:** PROCEED-TO-C1 **CONDITIONALLY** · **Weighted tribunal score:** 78.16/100

---

## Lens scorecard

| Lens | Decision | Score | Weight | One-line |
|---|---|---|---|---|
| pre-implementation-architect | PROCEED | 88 | 28% | Buildable as a whole; found a real denominator bug |
| popper-analyst | UNCORROBORATED (prov.) | 90 | 24% | The asserted tier has no non-confirmation-biased falsifier; validated tier untested |
| hume-analyst | UNGROUNDED (borderline) | 72 | 24% | Recognition is habit, not evidence; "different kind not weaker" is itself ungrounded; pathology framing smuggles an ought |
| contradiction-detector | CONTRADICTED | 84 | 12% | 3 genuine contradictions (asserted-grade, percentile denominator, no-mapping-vs-§9) |
| circumvention-forecaster | VULNERABLE | 38 | 12% | 2 critical exploits; the anti-horoscope gate doesn't survive a deadline |

**Read the 78.16 with care.** The synthesis flagged that the weighted average blends *orthogonal axes* — the architect (28%) measures *can it be built*, the others measure *is what's built valid* — and the lowest-weighted lens (circumvention, 38) carries the highest-severity finding. A passing-looking 78 co-exists with a core gate that is one config edit from defeated. Do not read it as a pass.

---

## The single root

**Asserted-tier exceptionalism** — the doctrine that recognition-grounded `asserted` signals are *a different kind of truth, not a weaker grade*. This one construct is the central finding of four of the five lenses, and the fifth funnels into it:

- **Popper:** "`load_index` correctly identifies load-bearing files" has no non-confirmation-biased falsifier. Recognition ("if the lists don't make you wince, the signals are wrong") is confirmation-biased *by construction* — `load_index ≈ 0.5·fan_in + 0.3·centrality`, and the files a developer recognizes as load-bearing are the same high-fan-in files, so assent is structurally assured. Stability is falsifiable-in-principle but un-operationalized (open #3) and tests *robustness, not correctness* (`load_index ≡ 0.5` is perfectly stable and useless).
- **Hume:** recognition is habit-masquerading-as-necessity; the parity claim ("different kind, not weaker") is *itself* ungrounded — holdout-grounding can return negative, recognition almost never does. Not parity.
- **Contradiction (C1, the smoking gun):** the doctrine ("a different KIND not a lower GRADE / neither subsumes the other," asserted in 4 places) is contradicted by the only place it is operationalized — the min-over-signals operator (structural-mapper §5) makes `asserted` *absorbing* and calls it "most conservative." **The spec's own mapper treats asserted as a lower grade.**
- **Circumvention:** five exploit paths converge on the asserted tier as the soft underbelly (relabel laundering, self-certified recognition, register leakage, decorative bypass).
- **Architect:** the graph-rate bug forces `graph_degraded` everywhere → reliance shifts *onto* the asserted tier — the bug funnels the product into precisely the tier the other four condemn.

---

## Unfalsifiability index

Of 8 named load-bearing claims: **~50% are unfalsifiable or un-operationalized** (load_index-correctness, the parity doctrine, recognition-confirms-description, asserted stability), a further **25% are falsifiable-but-never-exercised** (bug_pressure/change_pressure — corroboration depth zero; no holdout has been run, the `validation.json` numbers are illustrative placeholders). Load-weighted it is worse than 50%: the untestable cluster gates the three headline features (foundation/corridor/toothpick), while the testable claims sit untested.

---

## Key cross-lens insights

- **CMP-1 (critical):** the asserted doctrine is unfalsifiable *in word* (Popper/Hume), contradicted *in operation* (the min-operator, C1), AND exploitable *in practice* (relabel laundering). A soft epistemic critique hardened by a mechanical line of spec and an exploit path.
- **CMP-2 (critical):** the weighted score structurally hides the risk — the axis measuring whether the safeguards survive adversarial pressure is weighted lowest.
- **RSN-1:** the graph-rate denominator bug is *doubly* load-bearing — a correctness defect AND a gate-neutering incentive (the product renders empty on every npm repo, so the rational fix is to disable the gate).
- **RSN-2:** the C5 register constraint is porous from two independent vectors — the feature *names* ("foundation," "toothpick") import the forbidden counterfactual regardless of register discipline (Popper), and the LLM's lowest-energy phrasing for "toothpick" *is* "fragile, will collapse, changes ripple" (circumvention A5).

---

## Remediation (ordered)

### Must-fix-before-coding C1 (substrate-level; mechanical)
1. **Graph-rate denominator split** — exclude external-package imports from `unresolved_imports`; compute `graph_resolution_rate` from in-repo resolution *failures* only. *Highest leverage: correctness + removes the gate-neutering incentive (RSN-1). Shipping the current denominator bakes in the A1 exploit.*
2. **Orphan-node behavior** — specify HEAD-file-with-no-FileHistory (zeroed+flagged, or proven impossible).
3. **Toolchain version capture/normalization** — pin the hashed-string format (`name@semver` resolver per tool); it is load-bearing for determinism.
4. **Percentile-population denominator** (contradiction C2) — reconcile §5 "equal to the live inventory" vs §6.1's default `is_test` exclusion.

### Design-decision-required (logged as hard gates before the asserted tier / C3 are load-bearing)
5. **Resolve the root contradiction (C1):** either drop "different kind, not weaker," OR change the min-operator so it no longer treats `asserted` as absorbing/lower-grade. Pick one.
6. **Replace recognition with stability + SZZ, gated** — stability paired with a discriminating correctness signal so it cannot certify a constant (CMP-3).
7. **Run the holdout** for bug_pressure/change_pressure; replace placeholder `validation.json` before any "validated" label is load-bearing.
8. **Reconcile §3.7 margins (+0.05 / 1.20×) with the §3.4.1 AUC ceiling** — the test may be unpassable as written.
9. **Harden the asserted relabel** — forbid `kind: predictive → descriptive` without re-validation; separate the signal-tuner from the grounding-note author (circumvention A2/A4).
10. **Resolve substrate/report layering** (contradiction C3) — substrate claims "no metric→feature mapping" but §9 runs the toothpick/flooded-basement predicates.

### Accept / monitor (disclose; not blockers)
- C5 register leakage via feature names + LLM phrasing (RSN-2) — accept as known residual or rename; flag C5 as structurally porous.
- Pathology / is-ought framing ("diagnostic / warts and all / condemnation surveyor") and `neglect_index` naming — accept **with explicit disclosure** that the diagnostic stance is a chosen norm, not neutral description (Hume).
- A9 — the "unmanipulable" fix-label is a regex over commit *subjects* (an injectable input language) — monitor.

---

## Verdict

**PROCEED to C1 conditionally.** The substrate's deterministic measurement layer is largely sound and buildable. C1 may proceed once must-fix #1–#4 are resolved — and **not** under the current graph-rate denominator, which bakes in the highest-severity exploit. The asserted-tier design decisions (#5–#10) are mostly downstream of C1, but #5 (the root contradiction) should be settled before any code commits to the parity doctrine. The honest one-liner: **buildable substrate, conditionally; epistemically unsettled superstructure.**
