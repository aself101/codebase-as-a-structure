# eslint — architect's brief

*The register below is rendered from the facts sheet by code and carries the inventory (D-039); the reading beneath it is model-written and linted. Register lint: **PASS on attempt 1**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `f8bda106dcaa…`, facts `973d63713000…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.7.0; a PASS is a pass under that grammar (D-035).*

## Register

*Rendered from the facts sheet by code (brief 0.7.0); every cell is a field, no cell is a sentence. 473 rooms in 8 wings ((root) 4 · bin 1 · conf 2 · docs 30 · lib 388 · messages 18 · packages 8 · tools 22); 923 diagnostic marks across all profiles (675 in the base profile), one mark per feature per room — 48 of them fall on the same rooms twice because two profiles carry one predicate; the diagnostic features name 10 distinct sets of rooms; 49 decorative marks (crack, toothpick_wing); 254 rooms carry two or more diagnostic marks; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis. A position names where a room sits — in the import graph, on the clock, in the test graph — and is not a claim about its condition (D-004 Q3). The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a third or more of them; 'none' is a cell's own answer, not a gap.*

| feature | profile | position | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node | 48 | (root) 2, bin 1, lib 44, packages 1 | lib/rules 35 / 293 | none | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room | 83 | (root) 2, docs 22, lib 40, messages 11, packages 5, tools 3 | none holds a third | ⊃ flooded_basement (8 of these rooms outside it) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched, still-imported room | 75 | (root) 2, docs 18, lib 38, messages 11, packages 3, tools 3 | none holds a third | ⊂ dark_room (8 dark_room rooms outside this set) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load hub | 48 | conf 2, lib 45, tools 1 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | no consequence in the name | 50 | conf 2, docs 1, lib 46, packages 1 | none holds a third | ⊃ corridor (28 of these rooms outside it) | `centrality >= p90` |
| lit_room | maintainability | no consequence in the name | 48 | (root) 2, lib 40, messages 1, tools 5 | lib/rules 24 / 293 | none | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room at or above the median reinforcement | 371 | conf 2, docs 2, lib 360, packages 1, tools 6 | lib/rules 293 / 293 | none | `reinforcement_index >= 0.5` |
| ◌ toothpick_wing | maintainability | unreinforced high-load node with high edit pressure | 1 | lib 1 | none holds a third | none | decorative — bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| corridor | onboarding | high-centrality, high-fan-out junction | 22 | lib 21, packages 1 | none holds a third | ⊂ hub (28 hub rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load hub | 48 | conf 2, lib 45, tools 1 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| import_root | onboarding | import-graph root | 19 | (root) 2, bin 1, docs 3, lib 2, messages 2, packages 2, tools 7 | none holds a third | none | `fan_in == 0 and fan_out >= p75` |
| leaf_utility | onboarding | imported leaf | 148 | conf 2, docs 2, lib 139, messages 1, packages 2, tools 2 | lib/rules 98 / 293 | none | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry | 11 | bin 1, docs 1, lib 4, packages 5 | packages/eslint-config-eslint 4 / 5 (tied) | none | `is_package_entry == 1` |

## Reading

Eight wings stand over one. The lib wing holds 388 rooms, and the marks follow it: scaffolding — a test-imported room at or above the median reinforcement, a position, not a claim about what holds — falls on 371 rooms, among them lib/rules/no-var.js and lib/linter/vfile.js [scaffolding ×371: lib/rules/no-var.js, lib/linter/vfile.js].

The geometry here is age. dark_room — a long-untouched room — marks 83 rooms, reaching lib/shared/text-table.js and messages/plugin-missing.js, while lit_room marks 48, among them lib/rules/complexity.js and tools/test-ecosystem/index.mjs [dark_room ×83: lib/shared/text-table.js, messages/plugin-missing.js; lit_room ×48: lib/rules/complexity.js, tools/test-ecosystem/index.mjs].

The graph marks sit alongside. foundation — a high-load hub, a position in the import graph — marks 48 rooms including lib/config/flat-config-schema.js; hub marks 50, including lib/languages/js/source-code/source-code.js; leaf_utility marks 148, import_root 19 with tools/update-eslint-all.js among them, and package_entry 11, including packages/eslint-config-eslint/base.js [foundation ×48: lib/config/flat-config-schema.js; hub ×50: lib/languages/js/source-code/source-code.js; leaf_utility ×148; import_root ×19: tools/update-eslint-all.js; package_entry ×11: packages/eslint-config-eslint/base.js].

Three relations thin the count. flooded_basement — a long-untouched, still-imported room — nests within dark_room: adding load_index >= 0.10 leaves 75 rooms and removes 8, so these are two sets, not one [flooded_basement ×75; dark_room ×83]. corridor nests within hub, 22 rooms inside 50, with 28 rooms left outside by the fan_out >= p50 conjunct [corridor ×22; hub ×50]. The maintainability and onboarding foundation are the same predicate under two profiles, one set of 48 rooms carrying 48 marks twice over [foundation ×48; foundation ×48]. What the diagnosis names is 10 distinct sets of rooms.

254 rooms carry two or more diagnostic marks; lib/shared/traverser.js is one, standing under foundation and under hub [foundation ×48: lib/shared/traverser.js; hub ×50: lib/shared/traverser.js].

49 decorative marks render but are not a diagnosis: crack — a high edit-pressure node — and toothpick_wing — an unreinforced high-load node with high edit pressure — rest on bug_pressure_index, which is unvalidated [crack ×48; toothpick_wing ×1].

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `1`
- attempts_log: `1: pass`
- brief_version: `0.7.0`
- effort: `high`
- facts_hash: `973d63713000a7becfa310bb5fc1c613ba4decb1ee25322b7f576976c2030025`
- input_tokens: `25353`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3931`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038); R16 the reading does not restate the register's by-wing and directory cells (D-040).
