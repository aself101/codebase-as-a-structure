# Companion Checklist — Structural Mapper (C3)

*Conformance checklist for `structural-mapper-spec.md` (v0, DRAFT skeleton). The spec is a **skeleton**: it pins contracts and defers the full feature-by-feature ruleset to its own build. Items below are split accordingly — `[NOW]` pins authored in the skeleton (verify when C3 is built) vs. `[RULESET]` deferred to the ruleset build (the item exists, the test lands when the ruleset does). Each cites its section.*

**Scope:** C3's own artifact (`skeleton.json`) and its gate/profile contracts. The end-to-end anti-horoscope chain and the substrate/validation joins are verified in `system-integration.checklist.md`.

**Legend — contract class:** `[HOR]` anti-horoscope/grounding · `[DET]` determinism · `[SCH]` schema shape · `[GATE]` refuse/suppress · `[LAYER]` multi-profile · `[PROV]` provenance.
**Legend — phase:** `[NOW]` skeleton contract · `[RULESET]` deferred to ruleset build.
**Legend — verification:** `(unit)` · `(golden)` byte-identical diff · `(fixture)` reference-repo run · `(review)` human.

---

## A. Governing principle & determinism (§1, §2)

- [ ] `[NOW][HOR]` C3 is the **only** component that emits a discrete named structural claim; it does so only under the three disciplines (gate, provenance, determinism). *(§1)* `(review)`
- [ ] `[NOW][DET]` `skeleton.json` is a pure function of `(substrate.json, signal.json?, ruleset_version, profile_version)` — no randomness in C3 (stochastic form is C4). *(§2)* `(golden)`
- [ ] `[NOW][DET]` Same substrate + ruleset + profile → same skeleton, so two commits diff meaningfully (time-lapse continuity). *(§2)* `(golden)`

## B. The anti-horoscope gate — keystone (§3)

- [ ] `[NOW][HOR]` A rule may reference a signal only if its `validation_status` is `validated` or `asserted`, **or** the rule is `decorative: true`. *(§3)* `(unit)`
- [ ] `[NOW][HOR]` The gate is **signal-level**: every signal a predicate reads — composite index, percentile, **and** raw metric — is checked, closing the bare-percentile leak. *(§3)* `(unit)`
- [ ] `[NOW][GATE]` An `unvalidated` or `untested` signal feeding a non-decorative feature is a **hard error** — C3 refuses to emit the skeleton until re-grounded or tagged decorative. *(§3)* `(unit)`
- [ ] `[NOW][HOR]` `validated` and `asserted` **both fully license** a diagnostic feature; the distinction rides through provenance as a *register*, not a discount. *(§3)* `(review)`
- [ ] `[NOW][HOR]` Register constraint is binding: an `asserted` signal licenses only a present-structural statement; a consequence/forecast may be voiced only from a `validated` signal; a hybrid draws its forecast strictly from its validated half. *(§3, validation §2.1.1)* `(review)`
- [ ] `[NOW][GATE]` A `decorative: true` feature (neither predictive validation nor present-tense grounding) still renders but is flagged unvalidated and excluded from diagnostic claims in the brief. *(§3)* `(unit, review)`

## C. Mapping model & graph gating (§4, §4.1)

- [ ] `[RULESET]` The authored ruleset realizes the three axes — target ontology (building grammar), predicate strategy (in-repo percentile default), calibration (in-repo self-relative default). *(§4)* `(unit)`
- [ ] `[RULESET]` Multi-signal flagship features (toothpick, flooded basement) are conjunctions over indices, not single metrics. *(§4)* `(unit)`
- [ ] `[NOW][GATE]` Graph-dependent features (foundation, corridor, bridge, tower) **suppress or flag `degraded`** when `graph_available: false`, `graph_degraded: true`, or node `load_index_degraded: true` — never render confident structure on a weak graph. *(§4.1; substrate §6.3)* `(unit)`
- [ ] `[NOW][GATE]` A degraded graph-dependent feature is excluded from diagnostic claims, mirroring decorative treatment. *(§4.1)* `(unit)`

## D. Output — `skeleton.json` (§5)

- [ ] `[NOW][SCH]` Skeleton carries: `schema_version`, `mapper_version`, `ruleset_version`, `profile{name,version}`, `substrate_seed`, `archetype`, `features[]`, `overlays[]`. *(§5)* `(unit)`
- [ ] `[NOW][PROV]` Each feature carries `predicate`, `evidence` (the substrate values), `validation_status`, `decorative`, `degraded`. *(§5)* `(unit)`
- [ ] `[NOW][HOR]` Feature `validation_status` = most conservative across **all** signals read: (1) any `untested`/`unvalidated` → feature fails the gate; (2) else `validated` only if *all* signals are `validated`, else `asserted`. *(§5)* `(unit)`
- [ ] `[NOW][HOR]` Flagship hybrids (toothpick) resolve to `asserted` because they mix a description (`load_index`) with a forecast (`bug_pressure_index`) — `asserted` names the *kind*, not a doubt level. *(§5)* `(unit, review)`
- [ ] `[NOW][HOR]` A feature is `validated` only when **every** signal it reads is a predictive index (the whole claim is a forecast). *(§5)* `(unit)`
- [ ] `[NOW][PROV]` Both provenance chains are present and resolvable: `feature → predicate → evidence → substrate metric` and `feature → signal → validation_status → holdout report (or recorded §2.1 grounding)`. *(§5)* `(unit)`

## E. Multi-profile semantics — layering, never unification (§6)

- [ ] `[NOW][LAYER]` One repo → one profile-independent geometry; profiles change which features are foregrounded/styled, never where the rooms are. *(§6)* `(unit)`
- [ ] `[NOW][LAYER]` Output is a base layer plus named `overlays`; the renderer toggles them. *(§6)* `(unit)`
- [ ] `[NOW][LAYER]` Two lenses flagging the same node (Security fortress = Maintainability toothpick) is **shown, not averaged**; the system never reconciles a single merged verdict. *(§6)* `(unit, review)`

## F. Open questions — deferred, tracked (§7)

- [ ] `[RULESET]` **Archetype resolution** — how per-node features + `summary` aggregates resolve to one archetype label, and whether that label is itself gated (archetype on `unvalidated` signals → `decorative`). *(§7 Q1)* `(unit)`
- [ ] `[RULESET]` **Predicate threshold defaults** — `p`/`q` cutoffs for conjunctive features, set per-profile, interacting with the substrate percentile distribution (start from substrate §9 `p=0.90`, `q=0.10`). *(§7 Q2)* `(fixture)`
- [x] `[NOW][DET]` **Stability budget** — untouched feature churn ≤ 0.05 and untouched strata movement ≤ 0.05 per comparison, floors ≥ 30 untouched / ≤ 0.5 touched; verdict `untested` without a touched set, never a silent pass (D-018). *(§7 Q3)* `(unit: test_skeleton_budget_is_judged_over_the_untouched_population, test_skeleton_budget_floors_refuse_to_get_easier; fixture: reports/2026-09-05-m2/skeleton-budget.md)`
- [ ] `[RULESET]` **C2 (signal) coupling** — which features may read `signal.json` and which become unavailable when C2 is skipped (C2 optional in v0). *(§7 Q4)* `(unit)`

---

## Seams (verified in `system-integration.checklist.md`, not here)

- **Consumes:** `substrate.json` (signal-name join), optional `signal.json` (C2), a mapping profile + ruleset.
- **Produces:** `skeleton.json` consumed by C4 (geometry seed = `substrate_seed`) and C5 (every brief claim → a feature id).
- **Reads from validation:** `validation.json` signal statuses — the gate's lookup is `validation.signals[<name>].status`; a missing key = `untested` = hard error unless decorative.
- **Skeleton-status note:** this spec is a DRAFT skeleton; `[RULESET]` items are real contracts whose tests land when the authored ruleset is built (system spec Phase 0). They are listed now so the ruleset build inherits its conformance bar rather than inventing one.
