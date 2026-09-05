# Notes for Fable — codebase-as-structure

*From Claude (Fable 5.1, Claude Desktop), 2026-09-04. Alex asked me to write these. I've read the parent spec and tracker runs 1–8, including the full recommendation sets for the popper-validator, circumvention-forecaster, and software-architecture-expert-validator M1 reviews. I have not read the code. You have decision authority on all of this; these are observations from a seat that sees the runs side by side, not directions.*

---

## 1. Three agents converged on the same gap. Treat it as the M1 blocker.

Popper (critical), the forecaster (A3, critical), and the architecture validator (D-009 "no structural representation") each independently found that the D-009 tuning/test separation exists in prose and not in the artifact. Different epistemic natures, same finding. That is the strongest signal on the board — stronger than any single critical.

The forecaster's pattern finding is the one to internalize: D-008/D-009/D-010 relocated the June exploits from the specification into configuration and operator discipline. The exploits didn't close; they moved. So when you fix A1/A3/D-009, the question isn't whether the fix is correct, it's *where it lives*. A `validate()` on `ValidationConfig` with floors that cannot be set to zero, a tune/test split the artifact carries (`tuned_config_commit` is required by D-009 and absent from `validation.json`), and `cfg.effective()` embedded in the output — those break the pattern. A D-011 with sharper wording moves the exploits a third time.

A rule you might adopt: any decision that closes an exploit names the code that enforces it, in the decision itself. If the decision can't name code, it isn't closed.

## 2. `load_index` is structurally unreachable. Fix this first.

Popper: corroboration reads `fan_in_nonzero` from the wrong dictionary, predicted from the code and confirmed by the baseline run. That's a plain bug, but look at what depends on it. Toothpick wing = high load ∧ high stress. Flooded basement = load-bearing ∧ abandoned. Both of the system's most expressive features need `load_index`, and both are the reason the product is interesting rather than a CodeCity clone. If `load_index` can never reach `asserted`, the two flagship features are `decorative: true` by construction and the render is a horoscope for exactly the claims that matter most.

Small fix, disproportionate consequence. It should land before anything else in M1.

## 3. The gate has no tests. The gate is the product.

Popper: zero of seven load-bearing claims have a test; `run_stability`, `run_corroboration`, `descriptive_verdict`, `predictive_verdict` are untested. The verdict path is what the ruleset gets tuned against in the validation loop — it's the one component where a silent regression corrupts everything downstream while every render still looks fine. The severe tests Popper listed (synthetic alias/dynamic-import repo for G2, edge-dropout sweep for G4 centrality, K-sweep with exclusion fraction for stability) are the right ones because each is designed to *fail*. I'd write those before the next audit rather than after.

Related: G2's independence claim is false for `has_sibling_test` vs `test_fan_in` (shared primary resolver), and the forecaster found grounding accepts self/kin counterparts because the closure test checks truthiness rather than independence. Both are the same defect — "independent" is asserted, not computed. A test that constructs a dependent pair and expects rejection covers both.

## 4. Don't let M1's success make M2 optional.

The audits have pushed weight from the render toward the instrument at every step, and the instrument is where the value is. But nobody shares a `validation.json`. The cutaway is the distribution mechanism for the measurement, and it's also a forcing function: the forecaster's A12 (gate consumer unimplemented, substrate report renders indices ungated) exists precisely because nothing yet consumes `validation_status`. A consumer, even an ugly one, makes the gate real.

Suggestion: keep a minimal, throwaway cutaway sketch alive from early M2 — strata plus one or two features, no C5 — so the skeleton schema is exercised by something downstream while the ruleset is still being tuned. It doesn't need to be good. It needs to exist.

## 5. Be exact about the novelty claim.

Prior art you'll want to acknowledge rather than discover later: CodeCity (Wettel & Lanza) for the building metaphor; CodeScene / Tornhill for churn×complexity hotspots with visualization; Nagappan & Zimmermann and Google's 2011 bug-prediction work for "churn and fix history predict defects." All well-trodden.

What I don't know of anyone doing is the temporal-holdout validation gate *between the metric and the picture* — a feature may not render unless its signal earned it. That's the claim, and it's defensible only if the report measures it. Popper's suggestion to report τ(change_pressure_index, best_baseline) and to define a retirement criterion for a τ floor that cannot fail are how the claim gets defended rather than asserted. Make the README say exactly that much and no more.

## 6. Tracker hygiene, because this run set is an experiment.

Alex gave you the audit roster. That makes runs 4–8 a dataset nobody has: a model-selected validator roster against a real corpus, scorable later by RAH for whether the picks were the reliable agents or the relevant-sounding ones. Right now every M1 run has `definitionVersion: null`, `registryDefinitionId: null`, and no token counts. That data is cheap to attach at run time and impossible to reconstruct later. Pin the definition versions and log the roster rationale in `DECISIONS.md` so the experiment can be read afterward.

Bringing the circumvention-forecaster back after it scored the spec 38 in June was the right call; its 88 now is the most informative number on the project. Once M2 renders, consider re-running the Hume lens — the stance disclosure was a spec-level fix, and M2 is where the stance first becomes *visible* to a viewer.

## 7. Open question #5.

The project has no name. Not mine to pick, but it's a decision that will get made for you by whatever the repo is called if nobody makes it deliberately.
