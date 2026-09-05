# Codebase-as-Structure — System Specification (high-level, v0)

*A system that renders a single codebase as an architectural structure — a building you can read. The structure is diagnostic, not aspirational: it shows what the codebase **is**, warts and all (the flooded basement, the load-bearing wing on toothpicks, the fortress with no door), never what it could be. This document is the parent spec; each numbered component can be split into its own standalone spec. Component 1 is `repo-substrate-spec.md` (which supersedes the v0.1 `truthful-extractor-spec.md`); Component 3 is `structural-mapper-spec.md` (DRAFT); the validation gate is `validation-spec.md`. Decisions that changed this corpus after its June 2026 review are logged in `DECISIONS.md`.*

**Stance disclosure.** "Diagnostic," "warts and all," and the condemnation-surveyor framing of C5 are a **chosen evaluative stance**, not the neutral content of "what the codebase is." A diagnosis presupposes a norm of health — here, roughly: load should be reinforced, old load-bearing code should be visited, fixes should not concentrate. Those are maintenance-oriented values. A finished, correct, stable utility that nobody has touched in three years scores high on `neglect_index` and is not, by any reasonable reading, neglected; the index name encodes the stance. The system commits to the stance because the product exists to surface maintenance pathologies, and it states the stance here so it reads as an *ought* the reader may reject, not as a fact the reader must accept. *(Added 2026-09-04, D-004 Part 4; the June 19 tribunal's Hume finding.)*

---

## 1. Thesis and principles

1. **Buildings and codebases are both load-bearing systems that accrete history.** The metaphor is principled, not decorative: every visual feature must be a faithful function of a real signal. A viewer should be able to *learn to read* the building.
2. **Deterministic skeleton, generative skin.** The load-bearing facts are derived deterministically. Art and narrative are layered on top, downstream and constrained.
3. **The model interprets; it never diagnoses.** Diagnosis is metric-derived and fixed. The LLM decides whether "flooded basement" reads as a crypt, a cistern, or weeping foundations — it cannot decide whether the basement is flooded.
4. **The codebase is the seed.** Stochastic layers are seeded by the repo's content hash, so randomness explores a space of valid buildings while staying reproducible.
5. **Observable, persistent, regressable.** Every artifact is versioned and every claim is traceable to evidence, so two renders of the same repo diff meaningfully and any change is attributable.

## 2. Architecture overview

Six components, each consuming the prior one's versioned artifact. Determinism class is the contract that matters most:

| # | Component | Determinism class | Input → Output artifact | Standalone spec |
|---|---|---|---|---|
| C1 | Truthful Extractor → **repo-substrate** | Deterministic | repo@SHA → `substrate.json` | `repo-substrate-spec.md` (supersedes `truthful-extractor-spec.md`) |
| C2 | Narrative Reader | Seeded / constrained (LLM, cached) | substrate + repo prose → `signal.json` | → own spec |
| C3 | Structural Mapper | Deterministic (given ruleset) | substrate (+signal) + profile → `skeleton.json` | `structural-mapper-spec.md` (DRAFT skeleton) |
| C4 | Form Grammar | Seeded-stochastic | skeleton + seed → `massing.json` | → own spec |
| C5 | Architect | Free interpretation (LLM, grounded) | skeleton (+massing) → `brief.md` + `style.json` | → own spec |
| C6 | Renderer | Deterministic (procedural) / free (diffusion) | massing + style → render | → own spec |
| — | **Validation** | Deterministic | substrate (truncated) → `validation.json` + holdout report | `validation-spec.md` |

C2 is **removed from v0** (D-005; it was "optional" in the June draft): nothing in Phase 0 reads `signal.json`, and the mapper's C2-coupling question closes as "none in v0." It returns in Phase 2, where the blueprint overlay (§9) needs it. C4 is likewise **folded into C6 for the 2D cutaway** (D-005, closing open question #1): massing for a cutaway is vertical strata plus feature placement, and a separate `massing.json` was ceremony. The table keeps both rows because the 3D and blueprint phases need them.

Validation is not a pipeline stage — it is an offline gate that runs the substrate against itself over a temporal holdout and assigns each **signal** (composite index, percentile, or raw metric) a `validation_status`. The two predictive indices can be `validated` (forecast confirmed by holdout); present-tense descriptive signals are `asserted` (description confirmed by a stability budget and a cross-modal check, `validation-spec.md` §2.4) — a different kind of grounding, and the weaker one for the purpose of what a feature may claim. That status is what the anti-horoscope contract (§3) enforces at C3.

## 3. Process, artifacts, and cross-cutting contracts

**Data flow.** A linear pipeline C1 → C3 → C4 → C5 → C6, with C2 as a side-input to C3. Each stage reads the prior artifact and emits its own; nothing reaches back upstream.

**Determinism contract (system-level).** The seed originates as C1's content hash of the resolved tree and flows into every stochastic stage. A full pipeline run on the same SHA, with the same component versions and the same mapping profile, reproduces the same render — modulo deliberate seed or profile changes. This is what makes renders across two commits a *meaningful diff* rather than noise.

**Provenance and traceability.** Every `skeleton.json` feature carries an `evidence` block: the metric/index/topology values and the predicate that produced it. Every claim in `brief.md` references a feature id. The chain brief-claim → feature → evidence → metric is complete, so "why is this file a toothpick?" always resolves to specific numbers. This is the spine that keeps the system diagnostic instead of decorative.

**Anti-horoscope contract (system-level invariant).** Provenance proves a claim isn't *fabricated*; it does not prove the underlying signal *means anything*. A signal can be perfectly traceable and still be noise. So a second invariant sits beside provenance: **no named structural feature may rest on a signal that has not earned it.** The invariant is *signal-level*, not index-level — it covers composite indices, percentiles, and raw metrics alike, because the v0-default predicate strategy is the in-repo percentile and a feature written directly over percentiles must not be able to slip the gate. Concretely — a C3 feature may reference a signal only if that signal's `validation_status` is `validated` (it *predicts* where defects land, confirmed by the temporal holdout, `validation-spec.md` — reachable only by the two predictive indices) or `asserted` (it *describes* a present-tense structural fact, confirmed by the stability budget and cross-modal check of `validation-spec.md` §2.4 — the grounding for non-predictive indices and for bare percentiles/raw metrics), unless the mapping rule is explicitly tagged `decorative: true`, in which case the feature renders but is excluded from diagnostic claims. `validated` and `asserted` are two **kinds** of grounding — a description is not a failed prediction — and both license a diagnosis, but they are not equal in corroboration: `validated` is the stronger, which is the ordering the C3 min-operator encodes, and the boundary below is where the difference bites. Only the genuinely ungrounded (`decorative`) is excluded from diagnosis altogether. A boundary keeps this honest: an `asserted` signal may claim only a *present structural position*, never a *consequence or forecast* ("changes here will break much") — that is a prediction and must be `validated`, not asserted (`validation-spec.md` §2.1.1). C5's narrative register is bound by the same line. The provenance chain therefore extends one link deeper: feature → signal → **validation_status** → holdout report (or recorded recognition/stability grounding). This contract is what authorizes the evocative metaphor; without it, a beautifully rendered cutaway is a horoscope with good art direction.

**Versioning.** Component versions, the mapping ruleset (§5.5), the mapping profile (§5.4), and the schema versions are all recorded in each artifact. Renders are reproducible and auditable from their artifacts alone.

## 4. Component summaries

**C1 — Truthful Extractor / repo-substrate** (specced — `repo-substrate-spec.md`, which supersedes the v0.1 `truthful-extractor-spec.md`). Pure measurement plus normalization: per-file metrics, repo-relative percentiles, composite indices, a dependency edge set, and a classified commit timeline. Emits continuous signals; names no feature.

**C2 — Narrative Reader** (LLM-as-reader). Turns irreducibly natural-language sources — commit bodies, READMEs, design docs — into structured signal: enriched commit intent, incident markers, and (for §9) an intended-structure extraction. Run cold and cached so it behaves near-deterministically. Optional in v0.

**C3 — Structural Mapper** (DRAFT skeleton — `structural-mapper-spec.md`). The diagnosis. Applies a versioned mapping ruleset under a chosen profile to derive the skeleton: which nodes are foundation, where the wings attach, where the stress concentrates, what archetype the whole resolves to. Deterministic given its ruleset. The canonical mapping model summarized in §5 below now lives, in authored form, in the C3 spec; §5 is kept as the system-level overview. C3 is also where the anti-horoscope gate (§3) and multi-profile layering (`structural-mapper-spec.md` §6; open question #2 in §11) are enforced.

**C4 — Form Grammar.** Turns the skeleton's facts into concrete geometry — many valid buildings satisfy one skeleton; the seed picks one. For the v0 cutaway this is light (vertical strata + feature placement); full 3D massing is later.

**C5 — Architect.** Generates the narrative brief and style/material/mood directives, grounded in the skeleton and run through an adversarially-framed Generator lens (a condemnation surveyor, not a realtor) so the model honors ugly facts instead of smoothing them. Cached/seeded for consistency.

**C6 — Renderer.** v0: a 2D cutaway elevation (chosen because a cutaway *exposes the diagnosis by construction* — the waterline, the toothpicks, the era-strata are all visible). Later: 3D procedural, then optionally diffusion for painterly stills.

## 5. Deriving meaning: structural mappings (C3 in depth)

> **Source-of-truth note.** This section is the system-level **overview of the mapping design space** — the menu of what *can* appear and how a metric *can* become a claim. The **authored, versioned ruleset** that actually selects and tunes these (the YAML `(feature → predicate)` set, the per-profile thresholds, and enforcement of the anti-horoscope gate §3 and graph-dependent gating) lives in `structural-mapper-spec.md`. When the two disagree, the C3 spec wins for rule mechanics; this section wins for intent and vocabulary.

The mapping problem is: given the substrate, produce structural facts. There are three orthogonal design axes — the **target ontology** (what we map *to*), the **predicate strategy** (how a metric becomes a structural claim), and the **calibration mode** (relative to what). A mapping is a set of `(feature → predicate over substrate)` rules; the axes below are the menu of options for building that set.

### 5.1 Target ontology — the building grammar

The vocabulary of structural features, each with an informal substrate signature. This is the menu of *what can appear* in a building.

| Feature | Signature (informal) |
|---|---|
| Foundation | High graph centrality ∧ high `fan_in` ∧ low recent churn |
| Strata / floors | Dependency-layering levels (topological rank) or directory depth |
| Wing / annex | A distinct dependency community introduced late in the timeline |
| Corridor | High-betweenness node/edge everything routes through (an interface) |
| Bridge | An edge connecting two otherwise-separate communities |
| Scaffolding | Test reinforcement present (`has_sibling_test`, coverage) |
| Crack / fault line | High stress index, concentrated in a region |
| Toothpick wing | Load-bearing ∧ fragile: high load index ∧ high stress index |
| Flooded basement | Load-bearing ∧ abandoned: high `fan_in` ∧ high `age_days` ∧ high `last_touched_days` |
| Decay / overgrowth | Old ∧ untouched ∧ low `fan_in` (dead-ish leaves) |
| Fortress / vault | Low `public_surface_ratio` ∧ high internal cohesion (no door) |
| Tower | Deep, cohesive, low-`fan_out` specialized subgraph |
| Lighting / occupancy | `last_touched_days` → lit vs. dark |
| Material / era | `age_days` → old stone vs. new glass |

Note that the most expressive features (toothpick, flooded basement) are **multi-signal** — they are conjunctions over derived indices, not single metrics. That observation drives the predicate strategy below.

### 5.2 Predicate strategies — the options

How a metric (or several) becomes a structural claim. These compose; a feature's predicate can mix strategies.

- **Absolute threshold.** Fixed cutoffs (`fan_in > 20`). Simplest, but brittle and non-transferable — a "high" value in one repo is unremarkable in another.
- **In-repo percentile.** Rank within this repo's own distribution (top-decile `fan_in`). Self-calibrating and transferable across repos. The proposed v0 default.
- **Composite index.** A weighted combination of metrics into a derived index, then thresholded/ranked. Captures the multi-signal features: a `load_index = f(centrality, fan_in, age)` and a `stress_index = f(fix_count, churn, complexity, ¬coverage)`; the toothpick is high on both. This is the cleanest way to express conjunctive features.
- **Graph-topological.** Read the dependency graph directly: centrality (PageRank / betweenness) → foundation and corridors; articulation points → load-bearing chokepoints; community detection → wings; inter-community edges → bridges; cycles → structural knots. Captures *relational* features that no per-node metric can.

### 5.3 Calibration modes

- **In-repo (self-relative).** Everything relative to this repo's own distribution. Needs no external data; honest about "this repo's worst," silent about "bad by global standards." v0 default.
- **Corpus-relative.** Calibrate against a benchmark corpus ("unusually under-tested versus the population"). More meaningful, requires aggregate data, and only aggregates ever leave a repo (privacy-preserving by construction). A later phase.

### 5.4 Mapping profiles (lenses)

A profile selects which features are emphasized, which predicate strategies and weights they use, and what gets foregrounded. The same substrate yields different skeletons under different profiles:

- *Maintainability* foregrounds stress, decay, scaffolding.
- *Security* foregrounds fortress/vault, entry points, and inbound exposure.
- *Onboarding* foregrounds foundation, corridors, and strata.

A profile is a versioned artifact. Running several profiles over one repo produces overlapping skeletons; reconciling or layering them is a system-level open question (§10).

### 5.5 The mapping ruleset as a versioned artifact

The full `(feature → predicate)` set is authored as a versioned definition (YAML), diffable and auditable. Because C3 is deterministic given its ruleset, changing the ruleset changes the skeleton predictably, and every resulting feature carries the predicate and values that produced it. The ruleset is the thing you tune in the validation loop, and it is the reason the diagnosis stays regressable.

## 6. Narrative and style (C5)

The architect reads the grounded skeleton and emits a brief plus style directives. Creative freedom is real but floats above fixed facts: form variation (seeded), material and era, the visual metaphor for a signal (decay as water, ice, sand, or rot), and the narrative genre (a surveyor's condemnation notice, an estate listing, an archaeologist's field notes). The adversarial lens framing is what prevents aspirational drift; the provenance requirement (every claim cites a feature) is what keeps it from becoming a horoscope.

## 7. Render (C6)

v0 ships the 2D cutaway elevation. The cutaway is not a compromise — it is the render idiom that most directly serves a *diagnostic* product, because strata, waterlines, and stress show up as geometry rather than needing annotation, and it diffs cleanly when the repo changes. 3D procedural and diffusion are deferred precisely because they trade legibility (and constraint-honoring) for painterliness.

## 8. Time dimension (forward-looking)

The schema already supports it: replay the timeline, re-run C3 at commit checkpoints, and animate the construction — foundation poured, floors raised, a wing bolted on, a fire (mass revert) and rebuild, a wing falling into overgrowth. This is the most emotionally resonant version and the strongest argument for keeping the skeleton *stable under small changes* (continuity), so the evolution is watchable rather than jittery.

## 9. Blueprint vs. as-built overlay (forward-looking)

If a spec or design doc exists, C2 extracts the *intended* structure and C3 renders the *as-built* against it. The **delta is itself diagnostic** — the load-bearing wing the spec promised that turned out a shack, the room never built, the unplanned annex. This stays inside "what is": it is what you said you'd build pinned beside what you built.

## 10. Phasing

- **Phase 0 (v0).** Split into milestones by D-003. **M1:** C1 + the validation gate run on the reference set — the substrate as standalone product. **M2:** a minimal C3 (in-repo percentile + a few topological predicates + the load/stress indices, gate enforced) + C6 static cutaway with C4 folded in; no LLM in the path. **M3 (optional):** C5 brief via adversarial lens with the register lint. C2 removed.
- **Phase 1.** Evolution time-lapse (§8).
- **Phase 2.** Blueprint vs. as-built overlay (§9), which pulls C2 onto the critical path.
- **Phase 3.** Corpus calibration (§5.3) and richer render (3D / diffusion).

## 11. System-level open questions

1. **C4/C6 boundary for the 2D cutaway.** *Resolved — folded (D-005).* For the cutaway, massing reduces to vertical strata + feature placement; C4 is not a distinct artifact in v0. It returns as its own component when 3D massing is built.
2. **Multi-profile reconciliation.** *Resolved — layering, never unification* (`structural-mapper-spec.md` §6). One repo yields one profile-independent geometry; profiles are toggleable overlays that change which features are foregrounded, never merged into a single verdict. Unification would smuggle a human weighting ("is security worse than maintainability here?") back into the deterministic core, breaking the diagnostic contract. Co-located findings (a *Security* fortress that is also a *Maintainability* toothpick) are shown, not averaged.
3. **Mapping stability.** *Resolved at the signal level (D-004; `validation-spec.md` §2.4.1).* The stability budget is a number: remove the last K=5 commits, and a signal's percentiles may move by at most a median of 0.05 and a max of 0.15. Paired with the cross-modal check (§2.4.2) it is the validation method for the non-predictive signals. The *skeleton-level* budget — how many features may appear or disappear between adjacent commits before the time-lapse reads as jitter — is pinned in `structural-mapper-spec.md` §7 Q3 (D-018): one room in twenty, over the nodes the intervening commits did not edit.
4. **Corpus privacy.** Confirm that corpus calibration only ever transmits aggregates, never definitions or source.
5. **Project name.** Still TBD.
