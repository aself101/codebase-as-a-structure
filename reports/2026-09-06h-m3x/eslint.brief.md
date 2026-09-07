# eslint — architect's brief

*Register lint: **PASS on attempt 1**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `f8bda106dcaa…`, facts `b14d9b73170e…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.5.0; a PASS is a pass under that grammar (D-035).*

473 rooms stand in 8 wings: lib holds 388, docs 30, tools 22, messages 18, packages 8, the root 4, conf 2, bin 1. Across all profiles the building carries 923 diagnostic marks, 675 of them in the base profile, and 254 rooms carry two or more diagnostic marks. 371 rooms carry a scaffolding mark — a test-imported room at or above the median reinforcement, a position in the import graph, not a claim about what holds — with 360 in lib, 6 in tools, 2 in conf, 2 in docs and 1 in packages, and 293 of them sit in lib/rules, which holds 293 of the building's 473 rooms [scaffolding ×371: lib/rules/complexity.js, tools/eslint-fuzzer.js, conf/globals.js, docs/_examples/custom-rule-tutorial-code/enforce-foo-bar.js, packages/js/src/index.js].

83 rooms carry a dark_room mark — a long-untouched room, a position in the age geometry — 40 in lib, 22 in docs, 11 in messages, 5 in packages, 3 in tools, 2 at the root [dark_room ×83: lib/shared/traverser.js, docs/src/assets/js/main.js, messages/shared.js, packages/js/src/index.js, tools/commit-readme.sh, cypress.config.js].

flooded_basement — a long-untouched, still-imported room — is a nesting inside dark_room and not one set: 75 rooms carry both marks, and the added load_index >= 0.10 conjunct removes 8 rooms [flooded_basement ×75; dark_room ×83]. Of the 75, 38 sit in lib, 18 in docs, 11 in messages, 3 in packages, 3 in tools, 2 at the root [flooded_basement ×75: lib/shared/severity.js, docs/src/assets/js/tabs.js, messages/plugin-missing.js].

The 48 foundation rooms under the maintainability profile and the 48 under onboarding are the same predicate, load_index >= p90, read under two profiles; foundation names a high-load hub, a position, not a claim about what breaks. 45 sit in lib, 2 in conf, 1 in tools [foundation ×48; onboarding/foundation ×48: lib/shared/naming.js, conf/ecma-version.js, tools/config-rule.js].

50 rooms carry a hub mark, 46 in lib, 2 in conf, 1 in docs, 1 in packages [hub ×50: lib/linter/linter.js, conf/globals.js]. corridor, a high-centrality, high-fan-out junction, nests within hub: 22 rooms carry both, and the fan_out >= p50 conjunct leaves 28 hub rooms outside it; 21 of the 22 sit in lib, 1 in packages [corridor ×22; hub ×50: lib/config/config.js, packages/js/src/index.js].

48 rooms carry a lit_room mark, 40 in lib, 5 in tools, 2 at the root, 1 in messages, with 24 in lib/rules, which holds 293 of the 473 rooms [lit_room ×48: lib/rules/quotes.js, tools/check-emfile-handling.js, Makefile.js, messages/config-file-missing.js].

148 rooms are marked leaf_utility, an imported leaf: 139 in lib, 98 of them in lib/rules of 293 rooms, and 2 each in conf, docs, packages and tools, 1 in messages [leaf_utility ×148: lib/rules/no-octal.js, conf/globals.js, messages/shared.js]. 19 rooms are import-graph roots, 7 in tools, 3 in docs, 2 each in lib, messages, packages and the root, 1 in bin [import_root ×19: tools/update-eslint-all.js, bin/eslint.js]. 11 rooms are declared package entries, 4 of them in packages/eslint-config-eslint, which holds 5 rooms, plus 4 in lib, 1 in bin, 1 in docs [package_entry ×11: packages/eslint-config-eslint/base.js, lib/api.js].

49 decorative marks render but are not a diagnosis [crack ×48; toothpick_wing ×1]. crack — a high edit-pressure node — and toothpick_wing — an unreinforced high-load node with high edit pressure — rest on bug_pressure_index, which is unvalidated.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `1`
- attempts_log: `1: pass`
- brief_version: `0.5.0`
- effort: `high`
- facts_hash: `b14d9b73170ea4f23ccbedba0e50634f54f75b69cf8fcc6bb839064e334f0b0e`
- input_tokens: `24663`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `4709`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038).
