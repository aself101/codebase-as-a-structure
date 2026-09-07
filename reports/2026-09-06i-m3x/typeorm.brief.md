# typeorm — architect's brief

*The register below is rendered from the facts sheet by code and carries the inventory (D-039); the reading beneath it is model-written and linted. Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `e437a70f7562…`, facts `906e5d44c7dd…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.6.0; a PASS is a pass under that grammar (D-035).*

## Register

*Rendered from the facts sheet by code (brief 0.6.0); every cell is a field, no cell is a sentence. 583 rooms in 7 wings ((root) 3 · docker 1 · docs 9 · extra 2 · packages 69 · playground 3 · src 496); 619 diagnostic marks across all profiles (483 in the base profile), one mark per feature per room; 61 decorative marks (crack, toothpick_wing); 160 rooms carry two or more diagnostic marks; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis.*

| feature | profile | position | rooms | by wing | dominant directory n / its rooms | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node | 59 | (root) 1, src 58 | src/query-builder 7 / 28 | – | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room | 70 | src 70 | src/error 33 / 61 | = flooded_basement (load_index >= 0.10 excludes nothing) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched, still-imported room | 70 | src 70 | src/error 33 / 61 | = dark_room (load_index >= 0.10 excludes nothing) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load hub | 59 | packages 2, src 57 | src/schema-builder/table 7 / 7 | = foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | – | 60 | src 60 | src/metadata-args 6 / 22 | ⊃ corridor (23 outside it) | `centrality >= p90` |
| lit_room | maintainability | – | 60 | (root) 1, packages 2, src 57 | src/query-builder 5 / 28 | – | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room at or above the median reinforcement | 164 | packages 17, src 147 | src/error 15 / 61 | – | `reinforcement_index >= 0.5` |
| ◌ toothpick_wing | maintainability | unreinforced high-load node with high edit pressure | 2 | src 2 | src/query-builder 1 / 28 | – | decorative — bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| corridor | onboarding | high-centrality, high-fan-out junction | 37 | src 37 | src/metadata-args 4 / 22 | ⊂ hub (23 of its rooms outside) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load hub | 59 | packages 2, src 57 | src/schema-builder/table 7 / 7 | = foundation (same predicate, two profiles) | `load_index >= p90` |
| import_root | onboarding | import-graph root | 1 | packages 1 | packages/codemod/src 1 / 1 | ⊂ package_entry (5 of its rooms outside) | `fan_in == 0 and fan_out >= p75` |
| leaf_utility | onboarding | imported leaf | 33 | packages 4, src 29 | src/driver/types 8 / 12 | – | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry | 6 | packages 2, src 4 | src 4 / 5 | ⊃ import_root (5 outside it) | `is_package_entry == 1` |

## Reading

Seven wings: src holds 496 of the building's 583 rooms, packages 69, docs 9, (root) 3, playground 3, extra 2, docker 1. The heaviest set of marks is scaffolding — a test-imported room at or above the median reinforcement, a position, not a claim about what holds — with 147 of its 164 rooms in src and 17 in packages [scaffolding ×164: src/error/QueryFailedError.ts, packages/codemod/src/lib/colors.ts]. dark_room — a long-untouched room — fired on 70 rooms, all 70 in src, 33 of them in src/error, which holds 61 of the building's 583 rooms [dark_room ×70: src/error/TypeORMError.ts].

The load and centrality marks sit close together in the same wing. foundation — a high-load hub — carries 57 rooms in src and 2 in packages [foundation ×59: src/metadata/EntityMetadata.ts, packages/codemod/src/transforms/stats.ts]; hub carries 60, all in src [hub ×60: src/index.ts]; lit_room carries 57 in src, 2 in packages, 1 in (root) [lit_room ×60: eslint.config.mjs]; leaf_utility carries 29 in src and 4 in packages [leaf_utility ×33: src/driver/types/ColumnTypes.ts]. 160 rooms carry two or more diagnostic marks of the 619 drawn, 483 of them in the base profile [hub ×60: src/data-source/DataSource.ts].

Two relations reduce what is separately named. flooded_basement — a long-untouched, still-imported room — adds load_index >= 0.10 to dark_room and it excludes nothing on this repository: the 70 rooms are the same 70, with 33 in src/error, which holds 61 of the building's 583 rooms [dark_room ×70; flooded_basement ×70: src/error/QueryRunnerAlreadyReleasedError.ts]. foundation under maintainability and foundation under onboarding are the same predicate read under two profiles, one set of 59 rooms [foundation ×59: src/schema-builder/table/Table.ts].

Two further relations are nestings, not identities. corridor — a high-centrality, high-fan-out junction — sits within hub, and the extra conjunct fan_out >= p50 leaves 23 rooms outside it; these remain two measurements [corridor ×37: src/metadata-args/MetadataArgsStorage.ts; hub ×60: src/cache/QueryResultCache.ts]. import_root sits within package_entry with 5 rooms outside it: import_root fired on packages/codemod/src/index.ts, the 1 room in packages/codemod/src, which holds 1 of the building's 583 rooms, while 4 of package_entry's 6 sit in src, which holds 5 of the building's 583 rooms [import_root ×1: packages/codemod/src/index.ts; package_entry ×6: src/cli.ts].

61 decorative marks render but are not a diagnosis [crack ×59; toothpick_wing ×2]: crack — a high edit-pressure node — and toothpick_wing — an unreinforced high-load node with high edit pressure — rest on bug_pressure_index, which is unvalidated.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R2-provenance, R2-provenance, R13-inert, R13-inert; 2: pass`
- brief_version: `0.6.0`
- effort: `high`
- facts_hash: `906e5d44c7dd97febd7321df8757537853ebe7318ce938c3383a6e31f36e3234`
- input_tokens: `21854`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `7580`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038).
