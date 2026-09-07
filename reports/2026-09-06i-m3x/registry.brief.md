# uluops-registry-api — architect's brief

*The register below is rendered from the facts sheet by code and carries the inventory (D-039); the reading beneath it is model-written and linted. Register lint: **PASS on attempt 3**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `f25b7e76f18b…`, facts `929602dadc1c…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.6.0; a PASS is a pass under that grammar (D-035).*

## Register

*Rendered from the facts sheet by code (brief 0.6.0); every cell is a field, no cell is a sentence. 267 rooms in 3 wings ((root) 7 · scripts 30 · src 230); 352 diagnostic marks across all profiles (280 in the base profile), one mark per feature per room; 27 decorative marks (crack); 88 rooms carry two or more diagnostic marks; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis.*

| feature | profile | position | rooms | by wing | dominant directory n / its rooms | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node | 27 | src 27 | src/services/definition 4 / 7 | – | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room | 27 | scripts 1, src 26 | src/db/migrations 11 / 55 | ⊃ flooded_basement (1 outside it) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched, still-imported room | 26 | scripts 1, src 25 | src/db/migrations 11 / 55 | ⊂ dark_room (1 of its rooms outside) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load hub | 27 | src 27 | src/utils 8 / 22 | = foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | – | 27 | src 27 | src/utils 7 / 22 | ⊃ corridor (14 outside it) | `centrality >= p90` |
| lit_room | maintainability | – | 40 | src 40 | src/controllers 6 / 18 | ⊃ package_entry (39 outside it) | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room at or above the median reinforcement | 133 | src 133 | src/utils 20 / 22 | ⊃ corridor (120 outside it); ⊃ package_entry (132 outside it) | `reinforcement_index >= 0.5` |
| corridor | onboarding | high-centrality, high-fan-out junction | 13 | src 13 | src/db/repository 2 / 15 | ⊂ hub (14 of its rooms outside); ⊂ scaffolding (120 of its rooms outside) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load hub | 27 | src 27 | src/utils 8 / 22 | = foundation (same predicate, two profiles) | `load_index >= p90` |
| import_root | onboarding | import-graph root | 11 | scripts 8, src 3 | scripts 8 / 27 | – | `fan_in == 0 and fan_out >= p75` |
| leaf_utility | onboarding | imported leaf | 20 | src 20 | src/utils 9 / 22 | – | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry | 1 | src 1 | src 1 / 2 | ⊂ lit_room (39 of its rooms outside); ⊂ scaffolding (132 of its rooms outside) | `is_package_entry == 1` |

## Reading

The building stands in three wings: 230 of its 267 rooms sit in src, 30 in scripts, 7 at the root, and the marks sit almost wholly in src. scaffolding — a test-imported room at or above the median reinforcement, a position, not a claim about outcomes — fires on 133 rooms, all 133 in src [scaffolding ×133: src/utils/logger.ts, src/middleware/auth.ts]. dark_room — a long-untouched room — fires on 27 rooms, 26 in src and 1 in scripts, with 11 of them in src/db/migrations, which holds 55 of the building's rooms [dark_room ×27: src/db/migrations/001_create_definitions.ts, scripts/run-seed.ts]. import_root sits the other way round: 8 of its 11 rooms are in scripts, a directory of 27 rooms, and 3 in src [import_root ×11: scripts/calibration-gate.ts, src/services/index.ts].

Several of the marks are nestings rather than separate sets. flooded_basement — a long-untouched, still-imported room — covers 26 rooms lying within dark_room's 27, the added load_index >= 0.10 conjunct leaving 1 dark_room room outside; two sets, not one [flooded_basement ×26; dark_room ×27]. corridor's 13 rooms lie within hub's 27, 14 hub rooms falling outside the fan_out >= p50 conjunct [corridor ×13: src/db/connection.ts; hub ×27: src/schemas/fork/schema.ts]. Those same 13 corridor rooms lie within scaffolding, with 120 scaffolding rooms outside [corridor ×13; scaffolding ×133]. package_entry's single room lies within lit_room, 39 lit_room rooms outside [package_entry ×1: src/index.ts; lit_room ×40], and within scaffolding, 132 scaffolding rooms outside [package_entry ×1; scaffolding ×133]. Under maintainability and onboarding, foundation — a high-load hub — marks 27 rooms twice: the same predicate, load_index >= p90, read under two profiles, 8 of them in src/utils, which holds 22 rooms [foundation ×27: src/utils/hash.ts]. 88 rooms carry two or more diagnostic marks; leaf_utility puts 9 of its 20 in that same src/utils [leaf_utility ×20: src/utils/uuid.ts].

27 decorative marks render but are not a diagnosis [crack ×27]; crack — a high edit-pressure node — rests on bug_pressure_index, which is unvalidated (D-015).

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `3`
- attempts_log: `1: R2-provenance; 2: R13-inert, R13-inert, R13-inert, R13-inert, R13-inert; 3: pass`
- brief_version: `0.6.0`
- effort: `high`
- facts_hash: `929602dadc1c416528a1c0e92f7745f15e2df4ad2d2acb15a1857ad89c903587`
- input_tokens: `13103`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3590`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038).
