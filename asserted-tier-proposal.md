# Proposal — Operationalizing the asserted tier (resolving the tribunal's root finding)

> **Status: ADOPTED with one substitution, 2026-09-04 — see `DECISIONS.md` D-004.** Parts 1, 3, and 4 were folded into the live specs as proposed. Part 2's blind human panel (2b) was replaced by cross-modal corroboration (`validation-spec.md` §2.4.2) because a single-developer project cannot field three blind rankers; the developer's sealed n=1 ranking is kept as a recorded, non-gating check (§2.4.3). This file is retained as the review-history record of the proposal as it stood on June 19 and must not be edited independently.

*Original status line: DRAFT for review. Not yet folded into the live specs — it walks back a doctrine the corpus currently asserts in four places, so it needs sign-off first.*

## The problem the tribunal found

Five lenses converged on one root: **asserted-tier exceptionalism** — the claim that recognition-grounded `asserted` signals are *"a different kind of truth, not a weaker grade."*

- **Popper:** "`load_index` correctly identifies load-bearing files" has no non-confirmation-biased falsifier. Recognition is confirmation-biased *by construction* (`load_index ≈ 0.5·fan_in + 0.3·centrality`; the files you'd "recognize" as load-bearing are the same high-fan-in files). Stability is un-operationalized (open #3) and tests *robustness, not correctness* (`load_index ≡ 0.5` is perfectly stable and useless).
- **Hume:** recognition is habit, not evidence; the parity claim is *itself* ungrounded — holdout-grounding can return negative, recognition almost never does.
- **Contradiction (the smoking gun):** the only place the doctrine is operationalized — the min-over-signals operator (mapper §5) — treats `asserted` as *absorbing/lower-grade*. The spec doesn't act as if its own doctrine is true.
- **Circumvention:** the asserted tier is self-certifiable (the weight-tuner writes the grounding notes) and the relabel laundered a failed predictor into it.

This proposal resolves all four in three parts, plus a disclosure.

---

## Part 1 — Resolve the contradiction: walk back the parity overclaim

**Decision: keep "different KIND," drop "not a weaker one / neither subsumes the other."**

The min-operator (mapper §5) is *correct*: a hybrid feature that mixes a forecast and a description cannot honestly present as a pure forecast, so it's labeled by its more conservative claim type. What's wrong is not the operator — it's the *rhetoric of parity* layered on top of it. The honest statement:

> `validated` and `asserted` rest on **different evidence types** (a holdout-confirmed forecast vs. a confirmed present-tense description). They are genuinely different *kinds*. But they are **not equal in corroboration**: a `validated` signal's falsifier can return negative; an `asserted` signal's falsifier (as currently specified) cannot. So for the purpose of *what a feature may claim*, `validated` is stronger — which is exactly the ordering the min-operator already encodes. `asserted` is **a different and currently weaker grounding, with a defined path to parity (Part 2).**

This is a deliberate reversal of the earlier (Nietzsche-driven) reframe, which over-corrected from *"confession"* all the way to *"fully equal, just different."* The tribunal showed that over-correction is the root vulnerability. The right resting place is **in between**: not a confession of inferiority, not a claim of parity — a different kind of grounding that is honestly weaker until it earns a real falsifier.

*Lands in:* validation §2.1 (drop the parity sentences), system §3, mapper §3, and the §3.8 verdict wording. The min-operator (mapper §5) stays exactly as is — it was right.

---

## Part 2 — Give `asserted` a real falsifier (close open #3)

A signal earns `asserted` only by passing **both** gates below. Either alone is insufficient — that pairing is the whole point (Popper's CMP-3 constraint: stability alone certifies constants).

### 2a — Stability budget (objective, falsifiable; tests *robustness*)

Operationalizes open question #3 with an actual number.

- **Protocol:** recompute the substrate at HEAD with the last *K* commits removed (config `stability_perturbation_k`, default 5), and measure each signal's percentile movement vs. the unperturbed run.
- **Pass iff** `median(|Δpercentile|) ≤ ε` (config `stability_eps`, default `0.05`) **and** `max(|Δpercentile|) ≤ δ` (config `stability_delta`, default `0.15`) across the population.
- Numbers feed `config_fingerprint`. A signal that swings past budget on a small edit is `unvalidated`, not `asserted`.
- **Popper's caveat is honored, not ignored:** this proves the description is *stable*, not *correct* — a constant passes. That is why 2b is mandatory.

### 2b — Blind, pre-registered recognition (tests *correctness*; removes confirmation bias)

Replaces the "wince" — which Popper showed is a tautology (you recognize the list built from `fan_in`) — with a protocol that *can return negative*.

- **Before** seeing any substrate output, **≥3 developers who know the repo** each *independently* produce a ranking (or top-K) of the files they consider load-bearing.
- **Pre-register** the pass bar: rank-correlation between the signal and the *pooled* human ranking `≥ τ_min` (config, default Kendall's **τ ≥ 0.5**), on **≥ M reference repos** (default 2).
- **Separation of duties:** the recognizers are **not** the people who tuned the weights (closes circumvention A4 — self-certification).
- This is falsifiable: the humans can rank differently, and then the signal is *refuted*, not asserted. It defeats Popper's tautology objection because the human ranking is produced *blind and prior*, not as assent to a list the metric already drew.

### 2c — The discriminating gate

`asserted` ≝ **passed 2a (stability) AND 2b (blind recognition) on ≥ M repos.** A constant `load_index ≡ 0.5` passes 2a but fails 2b (it correlates with nothing), so it cannot be `asserted` — which is precisely the failure mode Popper named. Failing either gate → `unvalidated`/`untested`, never silently `asserted`. The `validation.json` `grounding` block now records *both* a `stability` number and a `recognition` object (`{tau, n_devs, repos, prereg_ref}`), not a bare pointer to a notes file.

*Lands in:* a new validation §2.4 ("Operationalizing the asserted bar"), with §2.1 pointing to it; the §6.1 `grounding` schema gains the `stability` + structured `recognition` fields; closes system-spec open question #3.

---

## Part 3 — The feature-name leak (Popper's deepest point + circumvention A5)

Even fully operationalized, the *names* — "foundation," "load-bearing wing on toothpicks" — import the counterfactual "if it breaks, much falls," which only `blast_radius_index` can back. C5 register discipline can't stop it: the inference rides the noun.

**Principle:** a feature whose *name* asserts a consequence may voice that consequence as a diagnostic claim **only** when a `validated` consequence signal (`blast_radius_index`, §2.3) backs it. Until then, C3 should either (i) prefer **position** names over **consequence** names where possible ("hub" / "high-traffic junction" rather than "load-bearing wall that will collapse"), or (ii) the C5 brief must explicitly disclose that the name denotes *structural position*, not a breakage forecast. Plus the **deterministic C5 register lint** (circumvention A5): a post-hoc check that flags forbidden consequence words ("fragile," "will collapse," "ripple") when their source signal is `asserted`.

*Lands in:* the C3 spec (structural-mapper) ontology + a C5-spec lint requirement. This is downstream of C1, so it's logged, not blocking.

---

## Part 4 — Disclose the normative stance (Hume)

The "diagnostic / warts-and-all / condemnation-surveyor-not-a-realtor" framing is a **chosen evaluative stance** (seek fault; presume the codebase has pathologies worth surfacing), not the neutral content of "what the codebase *is*." A diagnosis presupposes a norm of health. This should be **declared an ought**, not smuggled as description. Similarly `neglect_index`: a finished, correct, stable utility is "old + untouched" but not *neglected* — the name encodes a maintenance-oriented value that should be stated, or the name softened ("dormancy_index").

*Lands in:* a one-paragraph "stance disclosure" in the system spec intro.

---

## Decisions I need from you

1. **Walk back parity** (Part 1) — keep "different kind," drop "not weaker / neither subsumes," leave the min-operator as is? *(Recommend yes — it's the root fix, and it's honest.)*
2. **Adopt the blind-recognition protocol** (2b) as the asserted *correctness* bar? Cost: ≥3 devs per repo + pre-registration before each validation. *(Recommend yes — it is the only thing that makes `asserted` falsifiable at all.)*
3. **Feature-name leak** (Part 3) — position-names, disclosure, or wait-for-`blast_radius_index`? *(Recommend disclosure + the C5 lint now; position-names as C3 is designed.)*
4. **Numbers** — ε=0.05, δ=0.15, K=5, τ≥0.5, M≥2 are placeholders. Tune, or accept as v0 starting points?

On your sign-off I'll fold Parts 1–2 into the live specs (validation + system + mapper), log Parts 3–4 as C3/C5 requirements, and the asserted tier stops being the thing every review keeps circling back to.
