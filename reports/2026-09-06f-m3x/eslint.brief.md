# eslint — architect's brief

*Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named and cited; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `865b9a71c08a…`, facts `6cc074beec25…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.4.0; a PASS is a pass under that grammar (D-035).*

The building holds 473 rooms in 8 wings: 388 in lib, 30 in docs, 22 in tools, 18 in messages, 8 in packages, 4 at (root), 2 in conf, 1 in bin. Across all profiles 923 diagnostic marks land, 675 of them in the base summary; 254 rooms carry two or more diagnostic marks, and 184 rooms are marked in more than one profile. The reinforcement set puts 360 rooms in lib, of which 293 sit in lib/rules — lib/rules/indent.js among them — with 2 in conf, 2 in docs, 1 in packages and 6 in tools [scaffolding ×371: lib/rules/indent.js].

The 83 dark_room rooms — dark_room names a long-untouched room, a position in the edit record — sit 40 in lib, 22 in docs, 11 in messages, 5 in packages, 3 in tools and 2 at (root), among them lib/shared/text-table.js and docs/src/assets/js/themes.js [dark_room ×83: lib/shared/text-table.js, docs/src/assets/js/themes.js]. The 75 flooded_basement rooms — flooded_basement names a long-untouched, still-imported room — sit within the 83 dark_room rooms: two marks on one set of rooms are one finding [flooded_basement ×75; dark_room ×83].

The 48 foundation rooms — foundation names a high-load hub, a position in the import graph — sit 45 in lib, 2 in conf and 1 in tools, among them lib/shared/traverser.js [foundation ×48: lib/shared/traverser.js]. The maintainability set and the onboarding set are the same 48 rooms [foundation ×48; onboarding/foundation ×48].

The 50 hub rooms sit 46 in lib, 2 in conf, 1 in docs and 1 in packages, among them lib/linter/esquery.js [hub ×50: lib/linter/esquery.js]. The 22 corridor rooms — corridor names a high-centrality, high-fan-out junction — sit 21 in lib and 1 in packages, and they sit within hub: one finding, two marks [corridor ×22: lib/config/flat-config-array.js; hub ×50].

The 48 lit_room rooms sit 40 in lib, 5 in tools, 2 at (root) and 1 in messages, with 24 of them in lib/rules, among them lib/rules/complexity.js [lit_room ×48: lib/rules/complexity.js]. The 148 leaf_utility rooms — the position is imported leaf — sit 139 in lib, 2 in conf, 2 in docs, 2 in packages, 2 in tools and 1 in messages, with 98 in lib/rules, among them lib/rules/no-bitwise.js [leaf_utility ×148: lib/rules/no-bitwise.js].

The 19 import_root rooms — the position is import-graph root — sit 7 in tools, 3 in docs, 2 at (root), 2 in lib, 2 in messages, 2 in packages and 1 in bin [import_root ×19: tools/update-eslint-all.js]. The 11 package_entry rooms — the position is declared package entry — sit 5 in packages, 4 in lib, 1 in docs and 1 in bin, with 4 in packages/eslint-config-eslint, among them packages/eslint-config-eslint/base.js [package_entry ×11: packages/eslint-config-eslint/base.js].

49 decorative marks render but are not a diagnosis: crack, whose position is high edit-pressure node, and toothpick_wing, whose position is unreinforced high-load node with high edit pressure [crack ×48; toothpick_wing ×1].

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R3-number, R3-number, R3-number, R5-disclosure, R5-disclosure; 2: pass`
- brief_version: `0.4.0`
- effort: `high`
- facts_hash: `6cc074beec25fc3c7ae666d620d0170972bce58be51dbf5f1070c9c3c2135cc1`
- input_tokens: `24735`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `4718`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named and cited (D-036, D-037).
