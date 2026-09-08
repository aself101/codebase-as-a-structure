# eslint — architect's brief

*The register below is rendered from the facts sheet by code and carries the inventory (D-039); the reading beneath it is model-written and linted. Register lint: **PASS on attempt 3**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `7719839821a7…`, facts `93db97b05aad…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.8.0; a PASS is a pass under that grammar (D-035).*

## Register

*Rendered from the facts sheet by code (brief 0.8.0); every cell is a field, no cell is a sentence. 473 rooms in 8 wings ((root) 4 · bin 1 · conf 2 · docs 30 · lib 388 · messages 18 · packages 8 · tools 22); 923 diagnostic marks across all profiles (675 in the base profile), one mark per feature per room — 48 of them fall on the same rooms twice because two profiles carry one predicate; the diagnostic features name 10 distinct sets of rooms; 49 decorative marks (crack, toothpick_wing); 254 rooms carry two or more diagnostic marks; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis. A position names where a room sits — in the import graph, on the clock, in the test graph — and is not a claim about its condition (D-004 Q3). The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a third or more of them and the feature has six or more rooms; a parent that shares a wing's name is marked as the parent. Relations are drawn between sets of three or more rooms. A caveat is the ruleset's own warning about a predicate. Every cell that is not a number is a cell's own answer, not a gap.*

| feature | profile | position | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node | 48 | (root) 2, bin 1, lib 44, packages 1 | lib/rules 35 / 293 | none | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room | 83 | (root) 2, docs 22, lib 40, messages 11, packages 5, tools 3 | none holds a third | ⊃ flooded_basement (8 of these rooms outside it) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched, still-imported room | 75 | (root) 2, docs 18, lib 38, messages 11, packages 3, tools 3 | none holds a third | ⊂ dark_room (8 dark_room rooms outside this set) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load hub | 48 | conf 2, lib 45, tools 1 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | no consequence word in the name (lexicon) | 50 | conf 2, docs 1, lib 46, packages 1 | none holds a third | ⊃ corridor (28 of these rooms outside it) | `centrality >= p90` |
| lit_room | maintainability | no consequence word in the name (lexicon) | 48 | (root) 2, lib 40, messages 1, tools 5 | lib/rules 24 / 293 | none | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room at or above the median reinforcement | 371 | conf 2, docs 2, lib 360, packages 1, tools 6 | lib/rules 293 / 293 | none | `reinforcement_index >= 0.5` |
| ◌ toothpick_wing | maintainability | unreinforced high-load node with high edit pressure | 1 | lib 1 | too few rooms to place (1) | none | decorative — bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| corridor | onboarding | high-centrality, high-fan-out junction | 22 | lib 21, packages 1 | none holds a third | ⊂ hub (28 hub rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load hub | 48 | conf 2, lib 45, tools 1 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| import_root | onboarding | import-graph root | 19 | (root) 2, bin 1, docs 3, lib 2, messages 2, packages 2, tools 7 | none holds a third | none | `fan_in == 0 and fan_out >= p75` — caveat: an import-graph root in a library is not its entrance (§5.5): the package's entry has fan-in and cannot qualify |
| leaf_utility | onboarding | imported leaf | 148 | conf 2, docs 2, lib 139, messages 1, packages 2, tools 2 | lib/rules 98 / 293 | none | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry | 11 | bin 1, docs 1, lib 4, packages 5 | packages/eslint-config-eslint 4 / 5 (tied) | none | `is_package_entry == 1` |

## Reading

The mass sits in lib. 360 of the 371 scaffolding rooms — a scaffolding room is a test-imported room at or above the median reinforcement, a position, not a verdict — are in that wing [scaffolding ×371: lib/rules/no-var.js, lib/linter/vfile.js], and 139 of the 148 leaf_utility rooms sit there too [leaf_utility ×148: lib/shared/traverser.js, lib/rules/no-tabs.js]. The load and centrality marks hold the same wing: 45 of the 48 foundation rooms — a foundation here is a high-load hub, a position in the import graph, not a claim about what happens to it — are in lib [foundation ×48: lib/shared/traverser.js, lib/linter/vfile.js], as are 46 of the 50 hub rooms [hub ×50: lib/api.js, lib/shared/naming.js].

The age marks reach the outer wings. 22 of the 83 dark_room rooms — a dark_room is a long-untouched room — sit in docs, and 11 of them sit in messages [dark_room ×83: docs/src/assets/js/themes.js, messages/plugin-missing.js]. Of the 48 lit_room rooms, 40 sit in lib and 5 in tools [lit_room ×48: lib/rules/quotes.js, tools/check-emfile-handling.js]. 7 of the 19 import_root rooms sit in tools [import_root ×19: tools/update-eslint-all.js, tools/check-rule-examples.js]; the sheet's caveat states that an import-graph root in a library is not its entrance — the package's entry has fan-in and cannot qualify. 5 of the 11 package_entry rooms sit in packages [package_entry ×11: packages/eslint-config-eslint/base.js].

Three relations tighten the count. The 75 flooded_basement rooms — long-untouched, still-imported rooms — lie within the dark_room rooms, and the added load term removes 8: two sets of rooms, two marks, not one [flooded_basement ×75; dark_room ×83]. The 22 corridor rooms lie within the hub rooms, with 28 hub rooms outside the fan-out term [corridor ×22; hub ×50]. maintainability/foundation and onboarding/foundation are the same predicate under two profiles, one set of 48 rooms carrying 48 marks twice over [foundation ×48]. The diagnosis therefore names 10 distinct sets of rooms, and 254 rooms carry two or more diagnostic marks.

49 decorative marks render but are not a diagnosis [crack ×48; toothpick_wing ×1]: crack — a high edit-pressure node — and toothpick_wing — an unreinforced high-load node with high edit pressure — rest on bug_pressure_index, which is unvalidated.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `3`
- attempts_log: `1: R13-inert, R13-inert; 2: R16-restatement, R16-restatement, R16-restatement, R3-number, R3-number, R12-unit, R5-disclosure, R5-disclosure; 3: pass`
- brief_version: `0.8.0`
- effort: `high`
- facts_hash: `93db97b05aadd1b93751778e0281d10f7c323058b253add4292d27cfaeb4d475`
- input_tokens: `26626`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `4280`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038); R16 a feature's by-wing or directory number is sayable only where the wing or directory is named (D-040, D-041), R17 a claim of no relation is checked against the overlaps (D-041).
