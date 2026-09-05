# Structural Mapper (C3) — Specification (v0, DRAFT skeleton)

*Component 3 of codebase-as-structure. This is the **diagnosis**: it takes the substrate's continuous signals and produces discrete, named structural facts — which nodes are foundation, where the wings attach, where stress concentrates, what archetype the whole resolves to. C1 measures; C3 names. Everything visual downstream (C4/C5/C6) reads from C3's output and adds nothing the skeleton doesn't license.*

*This document is a **skeleton**: it pins the contracts that the rest of the corpus depends on — the anti-horoscope gate, multi-profile semantics, graph-dependent gating, and the `skeleton.json` shape — and defers the full feature-by-feature ruleset to its own build (system spec Phase 0). Where it says "the ruleset," that ruleset is the thing authored and tuned later.*

*Input: `substrate.json` (`repo-substrate-spec.md`), optionally `signal.json` (C2), and a mapping profile. Output: `skeleton.json`. Determinism: deterministic given its versioned ruleset and profile.*

---

## 1. Governing principle

C3 is the **only** component allowed to emit a discrete, named structural claim. The substrate forbids it (`repo-substrate-spec.md` §1); C3 exists to do exactly that, under three disciplines that keep naming honest:

1. **Validation gate (anti-horoscope).** A name may rest on a signal only if that signal has earned it (§3).
2. **Provenance.** Every named feature carries the predicate and the substrate values that produced it, so "why is this a toothpick?" always resolves to numbers (§5).
3. **Determinism.** Given the same substrate, ruleset, and profile, the same skeleton — so two commits diff meaningfully (§2).

## 2. Scope & determinism

- **In scope (v0).** Apply a versioned `(feature → predicate over substrate)` ruleset under one profile to produce a typed feature set plus a single archetype resolution, each with evidence and validation status.
- **Determinism.** `skeleton.json` is a pure function of `(substrate.json, signal.json?, ruleset_version, profile_version)`. No randomness here — stochastic form is C4's job, seeded by the substrate's content hash. C3 is repeatable so the time-lapse (system spec §8) is continuous.
- **Out of scope.** Geometry, style, render (C4–C6); cross-repo corpus calibration (Phase 3).

## 3. The anti-horoscope gate (keystone contract)

This is the contract `validation-spec.md` §5 defines and C3 enforces. It is what makes the evocative metaphor a diagnosis rather than a horoscope.

> **A mapping rule may reference a *signal* in its predicate — a composite index, a percentile, or a raw metric — only if that signal's `validation_status` (from `validation.json`) is `validated` or `asserted` — OR the rule is explicitly tagged `decorative: true`.**

- **The gate is signal-level, not index-level.** A feature's predicate reads signals; *every* signal it reads is checked, whether or not an index sits in the path. This closes the leak where the v0-default percentile strategy (`fan_in` pctile ≥ p90) would otherwise bypass a gate scoped only to composite indices. Only the two predictive indices can be `validated` (they forecast); a bare percentile/raw signal is `asserted` when it carries a recorded recognition/stability grounding (`validation-spec.md` §2.2) — never `validated`, since it makes no forecast.
- An `unvalidated` or `untested` signal feeding a non-decorative feature is a **hard error** in ruleset validation: C3 refuses to emit the skeleton until the rule is either re-grounded on a validated/asserted signal or tagged decorative.
- `validated` (predicts where defects land, confirmed by the holdout) and `asserted` (describes a real present-tense structural fact, confirmed by recognition/stability per `validation-spec.md` §2.1–§2.2) **both fully license a diagnostic feature.** They are two *kinds* of grounding, not two grades of one: the distinction rides through provenance so C5 speaks in the right **register** — a forecast for `validated`, a description for `asserted` — not so it discounts the latter. An `asserted` diagnosis is a real diagnosis.
- **The register constraint is binding, not stylistic (the A2 boundary, `validation-spec.md` §2.1.1).** A claim's grounding bounds what the brief may say from it. An `asserted` signal licenses only a *present structural* statement ("sits at a high-load position in the import graph"); it may **not** be voiced as a *consequence or forecast* ("will break much," "is fragile," "changes here ripple") — that is a prediction, and predictions may be voiced only from `validated` signals. A hybrid feature (below) draws its forecast strictly from its validated half and its structural description strictly from its asserted half; C5 may not transfer predictive force from one to the other. Propagation/consequence claims wait for `blast_radius_index` (`validation-spec.md` §2.3).
- A `decorative: true` feature is the genuinely different case: a signal with **neither** predictive validation **nor** a present-tense structural grounding — an evocative pattern the team likes but cannot tie to any confirmed fact. It still renders, but is **flagged unvalidated** in the skeleton and **excluded from diagnostic claims** in the C5 brief. This is the honest hatch for "this looks structural and we like it, but it rests on nothing we can confirm" — and that humility belongs *here*, at the ungrounded tier, not at `asserted`.

The practical effect: the most diagnostically loaded features (toothpick, flooded basement) read `load_index` (a present-tense structural fact, `asserted`) *and* the pressure indices (`validated`). They are **hybrid diagnoses** — a confirmed description of load-bearingness joined to a confirmed prediction of fragility — and a feature that reaches *around* the indices to a raw percentile is held to the same standard. The skeleton records both kinds of grounding on its face.

## 4. Mapping model (carried from the system spec)

The full menu lives in the system spec §5 in summary; the canonical, authored version is the **ruleset** governed here. Three orthogonal axes:

- **Target ontology** — the building grammar (foundation, strata, wing, corridor, bridge, scaffolding, crack, toothpick, flooded basement, decay, fortress, tower, lighting, material). The multi-signal features (toothpick, flooded basement) are conjunctions over indices, not single metrics.
- **Predicate strategy** — absolute threshold, in-repo percentile (v0 default), composite index, graph-topological.
- **Calibration** — in-repo self-relative (v0 default); corpus-relative later.

A **mapping profile** (lens) selects which features are emphasized and with what weights — *Maintainability* foregrounds stress/decay/scaffolding, *Security* foregrounds fortress/entry/exposure, *Onboarding* foregrounds foundation/corridors/strata. Profiles and rulesets are both versioned, diffable YAML artifacts.

### 4.1 Graph-dependent feature gating

Features whose predicates read the dependency graph — **foundation, corridor, bridge, tower** (centrality, betweenness, articulation points, communities) — must degrade honestly when the graph is weak:

- When `summary.graph_available` is `false`, **`summary.graph_degraded` is `true`** (a present-but-low-quality graph, `repo-substrate-spec.md` §6.3), or a node's `load_index_degraded` is `true`, graph-dependent features **suppress** rather than render on mush — they are either omitted or emitted with a `degraded: true` flag and excluded from diagnostic claims, mirroring the decorative treatment. The trigger is graph *quality*, not just presence: a confident-looking "foundation" built on a partially-resolved graph is exactly the failure this gate exists to catch.
- This prevents the failure mode where an absent JS/TS extractor silently yields a confident-looking "foundation" that is really an artifact of a missing graph.

## 5. Output — `skeleton.json` (shape sketch)

Each feature carries enough to trace the whole chain back to a number *and* a validation verdict:

```json
{
  "schema_version": "0.1",
  "mapper_version": "0.1.0",
  "ruleset_version": "string",
  "profile": { "name": "maintainability", "version": "string" },
  "substrate_seed": "<from substrate.json>",
  "archetype": { "label": "string", "evidence": { "...": 0 }, "validation_status": "asserted" },
  "features": [
    {
      "feature": "toothpick",
      "node": "src/registry/core.ts",
      "predicate": "load_index >= p90 AND bug_pressure_index >= p90 AND reinforcement_index == 0",
      "evidence": {
        "load_index": 0.91, "load_index_degraded": false,
        "bug_pressure_index": 0.82, "reinforcement_index": 0.0
      },
      "validation_status": "asserted",
      "decorative": false,
      "degraded": false
    }
  ],
  "overlays": [ { "profile": "security", "version": "...", "features": [] } ]
}
```

- `validation_status` on a feature is the **most conservative claim type** across **all signals** its predicate reads — indices, percentiles, and raw metrics alike. Resolve in two stages: (1) if any signal is `untested` or `unvalidated` (the FAIL tier), the feature fails the gate — a `validated` index mixed with an `unvalidated` raw percentile is `unvalidated`; (2) otherwise, every signal passes, and the feature is `validated` only if *all* its signals are `validated`, else `asserted`. Stage 2 is not a downgrade — it records that the feature's overall warrant is **descriptive** the moment any one signal is a present-tense description rather than a forecast.
- **Consequence: the flagship features are `asserted`, because they are *hybrid* diagnoses — and that is exactly right.** `toothpick` reads `load_index` (a present-tense structural fact → `asserted`, `validation-spec.md` §2.0/§2.1) and `bug_pressure_index` (a forecast → `validated`). Its overall claim type is `asserted` not because it is weak, but because "load-bearing but fragile" *is* partly a description (of load-bearingness) and partly a prediction (of fragility) — and a feature that contains a description cannot honestly present as a pure forecast. The `asserted` label names what kind of diagnosis it is, not how much you should doubt it. C5 voices it in the descriptive register, under the binding register constraint in §3 (A2 boundary): the load half may be stated as structural position, the fragility forecast comes only from the `validated` `bug_pressure_index`, and no propagation/consequence claim ("this will collapse," "changes ripple") is permitted until `blast_radius_index` is validated (`validation-spec.md` §2.3). A feature is `validated` only when every signal it reads is one of the two predictive indices — i.e. only when the *whole* claim is a forecast.
- The provenance chain is complete: `feature → predicate → evidence → substrate metric` and `feature → signal → validation_status → holdout report (or recorded §2.1 justification, for asserted signals)`.

## 6. Multi-profile semantics — layering, never unification

*Resolves system-spec open question #2.*

Running several profiles over one repo produces overlapping skeletons of the **same building**. The resolution is fixed:

> **Profiles are toggleable overlays over one shared skeleton geometry. The system never reconciles them into a single merged verdict.**

- One repo → one geometry (node positions, strata, massing are profile-independent and come from C4). Profiles change **which features are foregrounded and how they are styled**, not where the rooms are.
- Output carries a base layer plus named `overlays` (§5); the renderer toggles them. Two lenses may both flag the same node (a *Security* fortress that is also a *Maintainability* toothpick) — that co-location is shown, not averaged away.
- **Why not unify.** Collapsing lenses into one score reintroduces precisely the judgment call the whole architecture pushes downstream — "is security worse than maintainability here?" is a human weighting, not a metric fact. Unification would smuggle that weighting into C3 and break the diagnostic contract. Layering keeps every lens falsifiable on its own terms. (This mirrors the verdict-unification stance elsewhere on the platform.)

## 7. Open questions

1. **Archetype resolution.** How the per-node features and `summary` aggregates resolve to a single archetype label, and whether that label is itself gated (an archetype grounded only on `unvalidated` indices should be `decorative` too).
2. **Predicate threshold defaults.** The `p`/`q` cutoffs in conjunctive features (toothpick = `load ≥ p ∧ stress ≥ q`) need v0 defaults; they interact with the substrate's percentile distribution and should be set per-profile.
3. **Stability budget.** How much a small code change may move the skeleton before it counts as a genuine structural shift vs. jitter (system spec open question #3). This is the validation method for non-predictive features.
4. **Signal (C2) coupling.** Exactly which features may read `signal.json` and whether any become unavailable when C2 is skipped (C2 is optional in v0).
