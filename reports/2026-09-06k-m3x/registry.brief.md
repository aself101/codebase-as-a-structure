# uluops-registry-api — architect's brief

*The register below is rendered from the facts sheet by code and carries the inventory (D-039); the reading beneath it is model-written and linted. Register lint: **PASS on attempt 3**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `f25b7e76f18b…`, facts `89d22b06b7c4…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.7.0; a PASS is a pass under that grammar (D-035).*

## Register

*Rendered from the facts sheet by code (brief 0.7.0); every cell is a field, no cell is a sentence. 267 rooms in 3 wings ((root) 7 · scripts 30 · src 230); 352 diagnostic marks across all profiles (280 in the base profile), one mark per feature per room — 27 of them fall on the same rooms twice because two profiles carry one predicate; the diagnostic features name 10 distinct sets of rooms; 27 decorative marks (crack); 88 rooms carry two or more diagnostic marks; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis. A position names where a room sits — in the import graph, on the clock, in the test graph — and is not a claim about its condition (D-004 Q3). The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a third or more of them; 'none' is a cell's own answer, not a gap.*

| feature | profile | position | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node | 27 | src 27 | none holds a third | none | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room | 27 | scripts 1, src 26 | src/db/migrations 11 / 55 | ⊃ flooded_basement (1 of these rooms outside it) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched, still-imported room | 26 | scripts 1, src 25 | src/db/migrations 11 / 55 | ⊂ dark_room (1 dark_room rooms outside this set) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load hub | 27 | src 27 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | no consequence in the name | 27 | src 27 | none holds a third | ⊃ corridor (14 of these rooms outside it) | `centrality >= p90` |
| lit_room | maintainability | no consequence in the name | 40 | src 40 | none holds a third | ⊃ package_entry (39 of these rooms outside it) | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room at or above the median reinforcement | 133 | src 133 | none holds a third | ⊃ corridor (120 of these rooms outside it); ⊃ package_entry (132 of these rooms outside it) | `reinforcement_index >= 0.5` |
| corridor | onboarding | high-centrality, high-fan-out junction | 13 | src 13 | none holds a third | ⊂ hub (14 hub rooms outside this set); ⊂ scaffolding (120 scaffolding rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load hub | 27 | src 27 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| import_root | onboarding | import-graph root | 11 | scripts 8, src 3 | scripts 8 / 27 | none | `fan_in == 0 and fan_out >= p75` |
| leaf_utility | onboarding | imported leaf | 20 | src 20 | src/utils 9 / 22 | none | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry | 1 | src 1 | none holds a third | ⊂ lit_room (39 lit_room rooms outside this set); ⊂ scaffolding (132 scaffolding rooms outside this set) | `is_package_entry == 1` |

## Reading

Three wings stand: (root), scripts, and src. The src wing carries scaffolding — a test-imported room at or above the median reinforcement — at 133 rooms, from src/utils/logger.ts to src/middleware/auth.ts [scaffolding ×133: src/utils/logger.ts, src/middleware/auth.ts]. The scripts wing holds import-graph roots [import_root ×11: scripts/calibration-gate.ts, scripts/run-deep-analysis.ts], and dark_room — a long-untouched room — reaches there too, alongside its rooms under src/db/migrations [dark_room ×27: scripts/run-seed.ts, src/db/migrations/001_create_definitions.ts].

foundation — a high-load hub, a position in the import graph — fires under two profiles on one set of 27 rooms [foundation ×27: src/db/connection.ts, src/utils/uuid.ts]. That is the same predicate read twice, not two profiles agreeing, and 27 marks land a second time on rooms already marked [foundation ×27].

The remaining relations are nestings, and each names two sets, not one. corridor, a high-centrality high-fan-out junction, sits inside hub, its second conjunct removing 14 rooms [corridor ×13: src/db/connection.ts, src/utils/logger.ts; hub ×27]. corridor also sits inside scaffolding, with 120 rooms outside it [corridor ×13; scaffolding ×133]. flooded_basement — a long-untouched, still-imported room — sits inside dark_room, with 1 room outside [flooded_basement ×26: src/db/migrations/016_add_fulltext_search_index.ts; dark_room ×27]. package_entry sits inside lit_room with 39 rooms outside, and inside scaffolding with 132 outside [package_entry: src/index.ts; lit_room ×40; scaffolding ×133].

Counting the identical pair once and each nesting twice, the diagnosis names 10 distinct sets of rooms, and 88 rooms carry two or more diagnostic marks; the unshared positions stand apart, among them leaf_utility [leaf_utility ×20: src/utils/hash.ts, src/schemas/wdl/types.ts] and lit_room [lit_room ×40: src/controllers/user-controller.ts].

27 decorative marks render but are not a diagnosis [crack ×27]; crack, a high edit-pressure node, rests on bug_pressure_index, which is unvalidated.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `3`
- attempts_log: `1: R3-number; 2: R5-disclosure; 3: pass`
- brief_version: `0.7.0`
- effort: `high`
- facts_hash: `89d22b06b7c473005ee0c68b236177bf9f08516117dd45cc027148e070c3f207`
- input_tokens: `13254`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3895`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038); R16 the reading does not restate the register's by-wing and directory cells (D-040).
