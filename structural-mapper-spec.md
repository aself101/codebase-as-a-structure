# Structural Mapper (C3) — Specification (v0.1 — the skeleton contracts, now built)

*Component 3 of codebase-as-structure. This is the **diagnosis**: it takes the substrate's continuous signals and produces discrete, named structural facts — which nodes are foundation, where the wings attach, where stress concentrates, what archetype the whole resolves to. C1 measures; C3 names. Everything visual downstream (C4/C5/C6) reads from C3's output and adds nothing the skeleton doesn't license.*

*This document pins the contracts the rest of the corpus depends on — the anti-horoscope gate, multi-profile semantics, graph-dependent gating, and the `skeleton.json` shape. As of 2026-09-04 (D-016) they are implemented in `src/repo_substrate/mapper/` and the first ruleset is `rulesets/maintainability.toml` (TOML rather than YAML: standard-library parse, no new dependency, same diffability). The ruleset grammar is a conjunction of `signal op value` terms with `pNN` percentile or absolute thresholds; no disjunction, no negation. A `decorative` rule must carry `decorative_reason` or the ruleset does not load. The archetype (§7 Q1) is emitted as `null` and not claimed in v0 (D-019: a corpus-relative claim, Phase 3). The skeleton-level stability budget (§7 Q3) is pinned at one room in twenty over the untouched population (D-018) and enforced by `substrate skeleton-diff`.*

*Input: `substrate.json` (`repo-substrate-spec.md`), optionally `signal.json` (C2), and a mapping profile. Output: `skeleton.json`. Determinism: deterministic given its versioned ruleset and profile.*

---

## 1. Governing principle

C3 is the **only** component allowed to emit a discrete, named structural claim. The substrate forbids it (`repo-substrate-spec.md` §1); C3 exists to do exactly that, under three disciplines that keep naming honest:

1. **Validation gate (anti-horoscope).** A name may rest on a signal only if that signal has earned it (§3).
2. **Provenance.** Every named feature carries the predicate and the substrate values that produced it, so "why is this a toothpick?" always resolves to numbers (§5).
3. **Determinism.** Given the same substrate, ruleset, and profile, the same skeleton — so two commits diff meaningfully (§2).

## 2. Scope & determinism

- **In scope (v0).** Apply a versioned `(feature → predicate over substrate)` ruleset under one profile to produce a typed feature set, each feature with evidence and validation status. *No archetype in v0* (D-019, §7 Q1): a whole-building label is a corpus-relative claim and is deferred to Phase 3 with the calibration it needs.
- **Determinism.** `skeleton.json` is a pure function of `(substrate.json, signal.json?, ruleset_version, profile_version)`. No randomness here — stochastic form is C4's job, seeded by the substrate's content hash. C3 is repeatable so the time-lapse (system spec §8) is continuous.
- **Out of scope.** Geometry, style, render (C4–C6); cross-repo corpus calibration (Phase 3).

## 3. The anti-horoscope gate (keystone contract)

This is the contract `validation-spec.md` §5 defines and C3 enforces. It is what makes the evocative metaphor a diagnosis rather than a horoscope.

> **A mapping rule may reference a *signal* in its predicate — a composite index, a percentile, or a raw metric — only if that signal's `validation_status` (from `validation.json`) is `validated` or `asserted` — OR the rule is explicitly tagged `decorative: true`.**

- **The gate is signal-level, not index-level.** A feature's predicate reads signals; *every* signal it reads is checked, whether or not an index sits in the path. This closes the leak where the v0-default percentile strategy (`fan_in` pctile ≥ p90) would otherwise bypass a gate scoped only to composite indices. Only the two predictive indices can be `validated` (they forecast); a bare percentile/raw signal is `asserted` when it carries a recorded recognition/stability grounding (`validation-spec.md` §2.2) — never `validated`, since it makes no forecast.
- An `unvalidated` or `untested` signal feeding a non-decorative feature is a **hard error** in ruleset validation: C3 refuses to emit the skeleton until the rule is either re-grounded on a validated/asserted signal or tagged decorative.
- `validated` (predicts where defects land, confirmed by the holdout) and `asserted` (describes a real present-tense structural fact, confirmed by the stability budget and cross-modal check of `validation-spec.md` §2.4) **both license a diagnostic feature.** They are two *kinds* of grounding, and `validated` is the stronger: the distinction rides through provenance so C5 speaks in the right **register** — a forecast for `validated`, a description for `asserted` — and so that a feature's overall claim is bounded by its weakest signal (§5). An `asserted` diagnosis is a real diagnosis of the present; it is not a forecast. *(Wording revised 2026-09-04, D-004 Q1: the June draft's "not two grades of one" was contradicted by this spec's own min-operator in §5.)*
- **The register constraint is binding, not stylistic (the A2 boundary, `validation-spec.md` §2.1.1).** A claim's grounding bounds what the brief may say from it. An `asserted` signal licenses only a *present structural* statement ("sits at a high-load position in the import graph"); it may **not** be voiced as a *consequence or forecast* ("will break much," "is fragile," "changes here ripple") — that is a prediction, and predictions may be voiced only from `validated` signals. A hybrid feature (below) draws its forecast strictly from its validated half and its structural description strictly from its asserted half; C5 may not transfer predictive force from one to the other. Propagation/consequence claims wait for `blast_radius_index` (`validation-spec.md` §2.3).
- A `decorative: true` feature is the genuinely different case: a signal with **neither** predictive validation **nor** a present-tense structural grounding — an evocative pattern the team likes but cannot tie to any confirmed fact. It still renders, but is **flagged unvalidated** in the skeleton and **excluded from diagnostic claims** in the C5 brief. This is the honest hatch for "this looks structural and we like it, but it rests on nothing we can confirm."
- **The hatch is audited, because it is the obvious deadline bypass** (tribunal A3/A6). A `decorative: true` rule must carry a `decorative_reason` string naming the ungrounded signal(s) and why the feature is kept; C3 refuses a decorative rule with no reason. The skeleton records `summary.decorative_count` and `summary.decorative_features[]`, and the C6 render and C5 brief must surface that count where a reader sees it — a building with eleven decorative features and two grounded ones announces itself. This does not make the hatch unabusable; it makes abuse visible in the artifact rather than in a config file. *(Added 2026-09-04.)*

The practical effect: the most diagnostically loaded features (toothpick, flooded basement) read `load_index` (a present-tense structural fact, `asserted`) *and* the pressure indices (`validated`). They are **hybrid diagnoses** — a confirmed description of load-bearingness joined to a confirmed prediction of fragility — and a feature that reaches *around* the indices to a raw percentile is held to the same standard. The skeleton records both kinds of grounding on its face.

## 4. Mapping model (carried from the system spec)

The full menu lives in the system spec §5 in summary; the canonical, authored version is the **ruleset** governed here. Three orthogonal axes:

- **Target ontology** — the building grammar (foundation, strata, wing, corridor, bridge, scaffolding, crack, toothpick, flooded basement, decay, fortress, tower, lighting, material). The multi-signal features (toothpick, flooded basement) are conjunctions over indices, not single metrics.
- **Predicate strategy** — absolute threshold, in-repo percentile (v0 default), composite index, graph-topological.
- **Calibration** — in-repo self-relative (v0 default); corpus-relative later.

A **mapping profile** (lens) selects which features are emphasized and with what weights — *Maintainability* foregrounds stress/decay/scaffolding, *Security* foregrounds fortress/entry/exposure, *Onboarding* foregrounds foundation/corridors/strata. Profiles and rulesets are both versioned, diffable text artifacts (TOML as built, D-016). **Geometry is not a profile property** (D-017): strata come from a map-time geometry choice over the substrate — `age` (era bands) or `layer` (dependency layering, the §5.1 primary definition) — and wings from directory depth; a profile may only decide overlays. Two profiles ship: `rulesets/maintainability.toml` and `rulesets/onboarding.toml`.

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
  "archetype": null,
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

- `validation_status` on a feature is the **most conservative claim type** across **all signals** its predicate reads — indices, percentiles, and raw metrics alike. Resolve in two stages: (1) if any signal is `untested` or `unvalidated` (the FAIL tier), the feature fails the gate — a `validated` index mixed with an `unvalidated` raw percentile is `unvalidated`; (2) otherwise, every signal passes, and the feature is `validated` only if *all* its signals are `validated`, else `asserted`. Stage 2 records that the feature's overall warrant is **descriptive** the moment any one signal is a present-tense description rather than a forecast — the feature is labeled by its more conservative claim type, which is the weaker grounding (`validation-spec.md` §1). This operator is the concrete form of the `validated > asserted` ordering; the June draft's prose denied that ordering while this line enforced it, and the prose was what changed (D-004).
- **Consequence: the flagship features are `asserted`, because they are *hybrid* diagnoses — and that is exactly right.** `toothpick` reads `load_index` (a present-tense structural fact → `asserted`, `validation-spec.md` §2.0/§2.1) and `bug_pressure_index` (a forecast → `validated`). Its overall claim type is `asserted` because "load-bearing but fragile" *is* partly a description (of load-bearingness) and partly a prediction (of fragility) — and a feature that contains a description cannot honestly present as a pure forecast. The `asserted` label names what kind of diagnosis it is and bounds what may be said from it. C5 voices it in the descriptive register, under the binding register constraint in §3 (A2 boundary): the load half may be stated as structural position, the fragility forecast comes only from the `validated` `bug_pressure_index`, and no propagation/consequence claim ("this will collapse," "changes ripple") is permitted until `blast_radius_index` is validated (`validation-spec.md` §2.3). A feature is `validated` only when every signal it reads is one of the two predictive indices — i.e. only when the *whole* claim is a forecast.
- The provenance chain is complete: `feature → predicate → evidence → substrate metric` and `feature → signal → validation_status → holdout report (or recorded §2.1 justification, for asserted signals)`.

## 6. Multi-profile semantics — layering, never unification

*Resolves system-spec open question #2.*

Running several profiles over one repo produces overlapping skeletons of the **same building**. The resolution is fixed:

> **Profiles are toggleable overlays over one shared skeleton geometry. The system never reconciles them into a single merged verdict.**

- One repo → one geometry (node positions, strata, massing are profile-independent and come from C4). Profiles change **which features are foregrounded and how they are styled**, not where the rooms are.
- Output carries a base layer plus named `overlays` (§5); the renderer toggles them (`substrate render --html`). Two lenses may both flag the same node (a *Security* fortress that is also a *Maintainability* toothpick) — that co-location is shown, not averaged away: `co_located_nodes` lists them and the cutaway draws one corner badge per overlay profile beside the base styling (D-017). *Built 2026-09-05; geometry is tested byte-identical with and without overlays.*
- **Why not unify.** Collapsing lenses into one score reintroduces precisely the judgment call the whole architecture pushes downstream — "is security worse than maintainability here?" is a human weighting, not a metric fact. Unification would smuggle that weighting into C3 and break the diagnostic contract. Layering keeps every lens falsifiable on its own terms. (This mirrors the verdict-unification stance elsewhere on the platform.)

## 7. Open questions

1. **Archetype resolution.** *Resolved — not claimed in v0 (D-019, 2026-09-05).* `archetype` is emitted as `null`; a ruleset carrying an `[archetype]` table is refused by `mapper/ruleset.py::load_ruleset`. A whole-building label ("cathedral," "shantytown") is a claim about this repository *relative to other buildings*, and v0 calibrates in-repo only (system spec §5.3): within one repo every distribution has a top decile, so no aggregate of per-node features can say what kind of building this is. It also has no second modality (validation §2.4.2) at the repo level, so it could never reach `asserted`, and a `decorative` one-word label on the banner is the horoscope the gate exists to refuse. Reopens with Phase 3 corpus calibration, where the reference class exists; the label will then be a repo-level feature under the same gate plus a repo-level stability check (does the label flip at K = 5?).
2. **Predicate threshold defaults.** The `p`/`q` cutoffs in conjunctive features (toothpick = `load ≥ p ∧ stress ≥ q`) need v0 defaults; they interact with the substrate's percentile distribution and should be set per-profile.
3. **Stability budget — skeleton level.** *Resolved (D-018, 2026-09-05).* Between two skeletons of one repository, **untouched feature churn ≤ 0.05 and untouched strata movement ≤ 0.05**, with the signal-level floors (≥ 30 untouched common nodes, ≤ 0.5 of the common population touched). "Untouched" means not edited by the commits between the two revisions, read from the after-substrate's timeline through its renames map — the same discipline as `validation-spec.md` §2.4.1: an edited node may change (the skeleton reporting the edit); an unedited node that changes moved by ripple, and ripple is what the budget bounds. Instrument and enforcement: `substrate skeleton-diff` / `mapper/diff.py::skeleton_diff` (`SKELETON_BUDGET`), which reports the whole-population and untouched-population numbers side by side and a verdict `within_budget | over_budget | untested(reason)`. Read at K = 5 on all four reference repos, both geometries: untouched churn 0.005–0.014, untouched strata 0–0.032 (`reports/2026-09-05-m2/skeleton-budget.md`). A skeleton over budget is a defect of the ruleset or geometry, not a finding about the repository. Layer geometry is the less stable geometry; a geometry-specific ceiling is a Phase 1 question.
4. **Signal (C2) coupling.** *Resolved — none in v0 (D-005).* C2 is removed from Phase 0; no v0 feature reads `signal.json`. Reopens with Phase 2.
5. **Position names over consequence names (D-004 Q3).** The ontology in §4 should prefer names that denote structural *position* ("hub," "junction," "strata") over names that import a *consequence* ("load-bearing wall," "toothpick") wherever the consequence adds nothing the signal can back. Where a consequence name is kept for legibility, the feature carries `name_implies_consequence: true` and C5 must disclose that the name denotes position (the C5 register lint, an M3 requirement). To be settled when the ruleset is authored.
