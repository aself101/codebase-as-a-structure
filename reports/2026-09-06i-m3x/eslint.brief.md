# eslint — architect's brief

*The register below is rendered from the facts sheet by code and carries the inventory (D-039); the reading beneath it is model-written and linted. Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `f8bda106dcaa…`, facts `dcc92dd66c8e…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.6.0; a PASS is a pass under that grammar (D-035).*

## Register

*Rendered from the facts sheet by code (brief 0.6.0); every cell is a field, no cell is a sentence. 473 rooms in 8 wings ((root) 4 · bin 1 · conf 2 · docs 30 · lib 388 · messages 18 · packages 8 · tools 22); 923 diagnostic marks across all profiles (675 in the base profile), one mark per feature per room; 49 decorative marks (crack, toothpick_wing); 254 rooms carry two or more diagnostic marks; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis.*

| feature | profile | position | rooms | by wing | dominant directory n / its rooms | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node | 48 | (root) 2, bin 1, lib 44, packages 1 | lib/rules 35 / 293 | – | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room | 83 | (root) 2, docs 22, lib 40, messages 11, packages 5, tools 3 | lib/shared 12 / 19 | ⊃ flooded_basement (8 outside it) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched, still-imported room | 75 | (root) 2, docs 18, lib 38, messages 11, packages 3, tools 3 | lib/shared 12 / 19 | ⊂ dark_room (8 of its rooms outside) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load hub | 48 | conf 2, lib 45, tools 1 | lib/shared 9 / 19 | = foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | – | 50 | conf 2, docs 1, lib 46, packages 1 | lib/shared 13 / 19 | ⊃ corridor (28 outside it) | `centrality >= p90` |
| lit_room | maintainability | – | 48 | (root) 2, lib 40, messages 1, tools 5 | lib/rules 24 / 293 | – | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room at or above the median reinforcement | 371 | conf 2, docs 2, lib 360, packages 1, tools 6 | lib/rules 293 / 293 | – | `reinforcement_index >= 0.5` |
| ◌ toothpick_wing | maintainability | unreinforced high-load node with high edit pressure | 1 | lib 1 | lib/eslint 1 / 4 | – | decorative — bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| corridor | onboarding | high-centrality, high-fan-out junction | 22 | lib 21, packages 1 | lib/config 4 / 5 | ⊂ hub (28 of its rooms outside) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load hub | 48 | conf 2, lib 45, tools 1 | lib/shared 9 / 19 | = foundation (same predicate, two profiles) | `load_index >= p90` |
| import_root | onboarding | import-graph root | 19 | (root) 2, bin 1, docs 3, lib 2, messages 2, packages 2, tools 7 | tools 5 / 13 | – | `fan_in == 0 and fan_out >= p75` |
| leaf_utility | onboarding | imported leaf | 148 | conf 2, docs 2, lib 139, messages 1, packages 2, tools 2 | lib/rules 98 / 293 | – | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry | 11 | bin 1, docs 1, lib 4, packages 5 | packages/eslint-config-eslint 4 / 5 | – | `is_package_entry == 1` |

## Reading

The building stands in 8 wings over 473 rooms, and one wing holds almost all of it: lib carries 388 rooms, then docs 30, tools 22, messages 18, packages 8, (root) 4, conf 2, bin 1. scaffolding — a test-imported room at or above the median reinforcement, a position, not a claim about what breaks — fires on 371 rooms, 360 of them in lib, and 293 of those sit in lib/rules, a directory holding 293 of the building's 473 rooms [scaffolding ×371: lib/rules/no-var.js, lib/rules/quotes.js].

The age marks fall differently. dark_room — a long-untouched room — sits on 83 rooms: 40 in lib, 22 in docs, 11 in messages, 5 in packages, 3 in tools, 2 at root, with 12 in lib/shared, which holds 19 rooms [dark_room ×83: lib/shared/traverser.js]. flooded_basement — a long-untouched, still-imported room — is a nesting inside that set, not the same set: its load_index term removes 8 of them, leaving 75, of which 38 are in lib and 11 in messages [flooded_basement ×75: messages/plugin-missing.js]. lit_room marks 48 rooms, 40 in lib, 24 of them in lib/rules [lit_room ×48: lib/rules/no-var.js].

The load and centrality marks name a smaller quarter. foundation — a high-load hub — appears under both profiles on 48 rooms under the same predicate, one set read twice, 45 in lib and 9 in lib/shared [foundation ×48: lib/shared/naming.js; onboarding/foundation ×48]. hub covers 50 rooms, 46 in lib, 13 in lib/shared [hub ×50: lib/shared/serialization.js]; corridor nests inside hub, with 28 rooms outside it, leaving 22, 4 of which sit in lib/config, a directory of 5 rooms [corridor ×22: lib/config/config.js].

At the graph's edges, leaf_utility holds 148 rooms, 139 in lib, 98 in lib/rules [leaf_utility ×148: lib/rules/no-bitwise.js]; import_root holds 19, with 5 in tools, which holds 13 rooms [import_root ×19: tools/update-eslint-all.js]; package_entry holds 11, 4 in packages/eslint-config-eslint, a directory of 5 [package_entry ×11: packages/eslint-config-eslint/base.js]. Of 923 diagnostic marks, 254 rooms carry two or more.

49 decorative marks render but are not a diagnosis [crack ×48; toothpick_wing ×1]: crack, a high edit-pressure node, and toothpick_wing, an unreinforced high-load node with high edit pressure, rest on bug_pressure_index, which is unvalidated.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R11-share; 2: pass`
- brief_version: `0.6.0`
- effort: `high`
- facts_hash: `dcc92dd66c8e55a1dbf547459732610eba4c138211f6cc1b955b315bb567f1e2`
- input_tokens: `25076`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3420`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038).
