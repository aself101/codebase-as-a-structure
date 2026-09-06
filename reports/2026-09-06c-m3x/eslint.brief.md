# eslint — architect's brief

*Register lint: **PASS on attempt 1**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `a34380cb0cb8…`, facts `7d4d580fff04…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page.*

The building holds 473 rooms across 8 wings: lib carries 388, docs 30, tools 22, messages 18, packages 8, the root 4, conf 2, and bin 1. Across all profiles 923 diagnostic marks land, and 184 rooms carry more than one. The largest single set is reinforcement, 371 rooms, seated mostly in the rule wing and the linter wing [scaffolding ×371: lib/rules/no-magic-numbers.js, lib/linter/source-code-traverser.js].

Foundation — a high-load hub, a position in the import graph, not a claim about what breaks — fires on 48 rooms in the maintainability profile and on the same count under the onboarding overlay [foundation ×48; onboarding/foundation ×48]. Those positions sit in conf, in the config wing, in the shared wing [foundation: conf/globals.js, lib/config/flat-config-schema.js, lib/shared/traverser.js].

Fifty rooms sit at or above the ninetieth percentile of centrality [hub ×50: lib/api.js, lib/linter/linter.js, lib/languages/js/source-code/source-code.js]. Twenty-two of the high-centrality junctions also carry fan-out at or above the median [corridor ×22: lib/rules/index.js, lib/eslint/eslint.js, lib/rule-tester/rule-tester.js].

Dark_room — a long-untouched room, a position on the age axis, not a claim about what breaks — marks 83 rooms, concentrated in the messages wing, the docs wing, and the token-store rooms [dark_room ×83: messages/no-config-found.js, docs/src/assets/js/themes.js, lib/languages/js/source-code/token-store/skip-cursor.js]. Flooded_basement — a long-untouched, still-imported room, again a position, not a claim about what breaks — marks 75 [flooded_basement ×75: lib/shared/text-table.js, lib/cli-engine/hash.js, messages/plugin-conflict.js].

At the other end of the same axis, 48 rooms sit at or below the tenth percentile of days since last touch, spread through the rule wing and the top of the tree [lit_room ×48: lib/cli.js, lib/options.js, lib/rules/no-unused-vars.js, Makefile.js].

The onboarding overlay places 19 rooms with zero fan-in and fan-out at or above the seventy-fifth percentile [import_root ×19: bin/eslint.js, tools/update-eslint-all.js, docs/.eleventy.js]. It places 148 rooms with zero fan-out and fan-in at or above the seventy-fifth percentile, the bulk of them in the rule wing and the shared wing [leaf_utility ×148: lib/shared/naming.js, lib/rules/utils/char-source.js, lib/rules/no-plusplus.js]. Eleven rooms are declared package entries [package_entry ×11: lib/unsupported-api.js, packages/eslint-config-eslint/base.js, lib/universal.js].

Forty-nine decorative marks render but are not a diagnosis: 48 high edit-pressure nodes and 1 unreinforced high-load node with high edit pressure [crack ×48; toothpick_wing ×1]. Both rest on an index the gate records as unvalidated, and neither enters the reading above.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `1`
- attempts_log: `1: pass`
- brief_version: `0.2.1`
- effort: `high`
- facts_hash: `7d4d580fff04400b2896a378c10602e42a5f2eb397c9d08a9c4d958b3a0f489b`
- input_tokens: `22261`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `2832`
- relinted: `brief 0.2.1`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations.
