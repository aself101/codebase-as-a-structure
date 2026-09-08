# typeorm — architect's brief

*The register below is rendered from the facts sheet by code and carries the inventory (D-039); the reading beneath it is model-written and linted. Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `c0c610c3cac3…`, facts `05d08f991a1b…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.8.0; a PASS is a pass under that grammar (D-035).*

## Register

*Rendered from the facts sheet by code (brief 0.8.0); every cell is a field, no cell is a sentence. 583 rooms in 7 wings ((root) 3 · docker 1 · docs 9 · extra 2 · packages 69 · playground 3 · src 496); 619 diagnostic marks across all profiles (483 in the base profile), one mark per feature per room — 129 of them fall on the same rooms twice because two profiles carry one predicate; the diagnostic features name 9 distinct sets of rooms; 61 decorative marks (crack, toothpick_wing); 160 rooms carry two or more diagnostic marks; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis. A position names where a room sits — in the import graph, on the clock, in the test graph — and is not a claim about its condition (D-004 Q3). The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a third or more of them and the feature has six or more rooms; a parent that shares a wing's name is marked as the parent. Relations are drawn between sets of three or more rooms. A caveat is the ruleset's own warning about a predicate. Every cell that is not a number is a cell's own answer, not a gap.*

| feature | profile | position | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node | 59 | (root) 1, src 58 | none holds a third | none | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room | 70 | src 70 | src/error 33 / 61 | = flooded_basement (load_index >= 0.10 excludes nothing) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched, still-imported room | 70 | src 70 | src/error 33 / 61 | = dark_room (load_index >= 0.10 excludes nothing) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load hub | 59 | packages 2, src 57 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | no consequence word in the name (lexicon) | 60 | src 60 | none holds a third | ⊃ corridor (23 of these rooms outside it) | `centrality >= p90` |
| lit_room | maintainability | no consequence word in the name (lexicon) | 60 | (root) 1, packages 2, src 57 | none holds a third | none | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room at or above the median reinforcement | 164 | packages 17, src 147 | none holds a third | none | `reinforcement_index >= 0.5` |
| ◌ toothpick_wing | maintainability | unreinforced high-load node with high edit pressure | 2 | src 2 | too few rooms to place (2) | none | decorative — bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| corridor | onboarding | high-centrality, high-fan-out junction | 37 | src 37 | none holds a third | ⊂ hub (23 hub rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load hub | 59 | packages 2, src 57 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| import_root | onboarding | import-graph root | 1 | packages 1 | too few rooms to place (1) | none | `fan_in == 0 and fan_out >= p75` — caveat: an import-graph root in a library is not its entrance (§5.5): the package's entry has fan-in and cannot qualify |
| leaf_utility | onboarding | imported leaf | 33 | packages 4, src 29 | none holds a third | none | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry | 6 | packages 2, src 4 | src (as parent, not the wing) 4 / 5 | none | `is_package_entry == 1` |

## Reading

Seven wings hold 583 rooms. src holds 496 of them, and the diagnostic marks sit inside it accordingly: all 70 dark_room rooms — dark_room is a long-untouched room, a position under the age geometry, not a claim about what happens in it — are src rooms [dark_room ×70: src/error/TypeORMError.ts, src/subscriber/BroadcasterResult.ts]. scaffolding — a test-imported room at or above the median reinforcement — names 147 rooms in src and 17 in packages [scaffolding ×164: src/util/OrmUtils.ts, packages/codemod/src/cli/parse-args.ts].

The packages wing holds 69 rooms. The single import_root room sits there [import_root: packages/codemod/src/index.ts], and the register's caveat holds that an import-graph root in a library is not its entrance: the package's entry has fan-in and cannot qualify. package_entry names 4 rooms in src and 2 in packages [package_entry ×6: src/cli.ts, packages/codemod/src/index.ts]; leaf_utility names 29 in src and 4 in packages [leaf_utility ×33: src/driver/types/ReplicationMode.ts, packages/codemod/src/lib/colors.ts]; lit_room names 57 in src, 2 in packages and 1 in (root) [lit_room ×60: src/query-builder/QueryBuilder.ts, packages/codemod/eslint.config.mjs, eslint.config.mjs].

flooded_basement — a long-untouched, still-imported room — adds load_index >= 0.10 to dark_room, and it excludes nothing on this repository: the 70 rooms are the same 70 [flooded_basement ×70; dark_room ×70]. foundation — a high-load hub — stands under the maintainability profile and under the onboarding overlay on one set of 59 rooms; that is the same predicate read twice, not two positions [foundation ×59; foundation ×59]. corridor — a high-centrality, high-fan-out junction — sits within hub, its added fan_out >= p50 conjunct removing 23 hub rooms; two sets, two measurements [corridor ×37; hub ×60]. Counting each identical pair once and the nesting twice, the diagnosis names 9 distinct sets of rooms, 160 rooms carry two or more diagnostic marks, and 129 marks land on rooms already marked because one predicate is carried under two profiles [foundation ×59].

61 decorative marks render but are not a diagnosis [crack ×59; toothpick_wing ×2]: crack — a high edit-pressure node — and toothpick_wing — an unreinforced high-load node with high edit pressure — rest on bug_pressure_index, which is unvalidated.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R10-prefix; 2: pass`
- brief_version: `0.8.0`
- effort: `high`
- facts_hash: `05d08f991a1bf109caca1a341c0612a8a306dca607cabdfd56f3b3e63b2eeac7`
- input_tokens: `22403`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `5881`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038); R16 a feature's by-wing or directory number is sayable only where the wing or directory is named (D-040, D-041), R17 a claim of no relation is checked against the overlaps (D-041).
