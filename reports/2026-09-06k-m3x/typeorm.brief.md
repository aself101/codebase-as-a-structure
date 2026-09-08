# typeorm — architect's brief

*The register below is rendered from the facts sheet by code and carries the inventory (D-039); the reading beneath it is model-written and linted. Register lint: **PASS on attempt 3**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `e437a70f7562…`, facts `6ac1624b9e11…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.7.0; a PASS is a pass under that grammar (D-035).*

## Register

*Rendered from the facts sheet by code (brief 0.7.0); every cell is a field, no cell is a sentence. 583 rooms in 7 wings ((root) 3 · docker 1 · docs 9 · extra 2 · packages 69 · playground 3 · src 496); 619 diagnostic marks across all profiles (483 in the base profile), one mark per feature per room — 129 of them fall on the same rooms twice because two profiles carry one predicate; the diagnostic features name 9 distinct sets of rooms; 61 decorative marks (crack, toothpick_wing); 160 rooms carry two or more diagnostic marks; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis. A position names where a room sits — in the import graph, on the clock, in the test graph — and is not a claim about its condition (D-004 Q3). The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a third or more of them; 'none' is a cell's own answer, not a gap.*

| feature | profile | position | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node | 59 | (root) 1, src 58 | none holds a third | none | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room | 70 | src 70 | src/error 33 / 61 | = flooded_basement (load_index >= 0.10 excludes nothing) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched, still-imported room | 70 | src 70 | src/error 33 / 61 | = dark_room (load_index >= 0.10 excludes nothing) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load hub | 59 | packages 2, src 57 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | no consequence in the name | 60 | src 60 | none holds a third | ⊃ corridor (23 of these rooms outside it) | `centrality >= p90` |
| lit_room | maintainability | no consequence in the name | 60 | (root) 1, packages 2, src 57 | none holds a third | none | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room at or above the median reinforcement | 164 | packages 17, src 147 | none holds a third | none | `reinforcement_index >= 0.5` |
| ◌ toothpick_wing | maintainability | unreinforced high-load node with high edit pressure | 2 | src 2 | none holds a third | none | decorative — bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| corridor | onboarding | high-centrality, high-fan-out junction | 37 | src 37 | none holds a third | ⊂ hub (23 hub rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load hub | 59 | packages 2, src 57 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| import_root | onboarding | import-graph root | 1 | packages 1 | none holds a third | ⊂ package_entry (5 package_entry rooms outside this set) | `fan_in == 0 and fan_out >= p75` |
| leaf_utility | onboarding | imported leaf | 33 | packages 4, src 29 | none holds a third | none | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry | 6 | packages 2, src 4 | src 4 / 5 | ⊃ import_root (5 of these rooms outside it) | `is_package_entry == 1` |

## Reading

Seven wings. Of 583 rooms, 496 sit in src, and that wing is where the load positions stand: src/metadata/EntityMetadata.ts and src/schema-builder/table/Table.ts both carry foundation — a high-load hub, a position in the import graph, not a verdict on the room [foundation ×59: src/metadata/EntityMetadata.ts, src/schema-builder/table/Table.ts]. The packages wing holds 69 rooms and the marks reach it: packages/legacy-naming-strategies/src/naming-strategy-v03.ts carries scaffolding — a test-imported room at or above the median reinforcement [scaffolding ×164: packages/legacy-naming-strategies/src/naming-strategy-v03.ts, src/util/StringUtils.ts]. Another 33 rooms carry leaf_utility, an imported leaf, src/driver/types/ColumnTypes.ts among them [leaf_utility ×33: src/driver/types/ColumnTypes.ts].

The geometry is age, and it lands twice on one set of rooms. flooded_basement — a long-untouched, still-imported room — adds load_index >= 0.10 to dark_room, a long-untouched room, and it excludes nothing on this repository: the 70 rooms are the same 70, src/error/TypeORMError.ts and src/common/ObjectLiteral.ts among them [dark_room ×70; flooded_basement ×70: src/error/TypeORMError.ts, src/common/ObjectLiteral.ts]. The same signal at its low end names 60 rooms under lit_room, including src/query-builder/QueryBuilder.ts [lit_room ×60: src/query-builder/QueryBuilder.ts].

foundation stands under maintainability and under onboarding as the same predicate on 59 rooms, src/data-source/DataSource.ts among them [foundation ×59: src/data-source/DataSource.ts]. onboarding/corridor, a high-centrality, high-fan-out junction, sits within maintainability/hub: 37 rooms carry corridor, and 23 hub rooms lie outside that extra conjunct — a nesting of two sets, with src/metadata-args/MetadataArgsStorage.ts in both [corridor ×37: src/metadata-args/MetadataArgsStorage.ts; hub ×60]. onboarding/import_root nests inside onboarding/package_entry the same way: packages/codemod/src/index.ts holds the import-graph root, and 5 package_entry rooms lie outside it, src/cli.ts among them [import_root ×1: packages/codemod/src/index.ts; package_entry ×6: src/cli.ts]. Counted with each identical pair as one set and each nesting as two, the diagnosis names 9 distinct sets of rooms, and 160 rooms carry two or more diagnostic marks [hub ×60].

61 decorative marks render but are not a diagnosis: crack — a high edit-pressure node — and toothpick_wing — an unreinforced high-load node with high edit pressure — rest on bug_pressure_index, which is unvalidated [crack ×59; toothpick_wing ×2].

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `3`
- attempts_log: `1: R11-share, R5-disclosure, R5-disclosure; 2: R11-share, R13-inert, R13-inert; 3: pass`
- brief_version: `0.7.0`
- effort: `high`
- facts_hash: `6ac1624b9e11ec4cf3dbd7bb544bf6a67901c710ea524a55ff08f5e1d49b8f08`
- input_tokens: `22240`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `6425`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038); R16 the reading does not restate the register's by-wing and directory cells (D-040).
