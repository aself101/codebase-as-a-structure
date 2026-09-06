# eslint — architect's brief

*Register lint: **PASS on attempt 1**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `b55497a3ac8c…`, facts `f623f5867d5a…`.*

473 rooms stand in this building, drawn under the maintainability profile with an onboarding overlay, on a geometry of age. lib holds 388 of them, docs 30, tools 22, messages 18, packages 8, the root 4, conf 2, bin 1. Across all profiles 885 diagnostic marks fall, and 181 of those sit co-located on rooms already marked by another measurement. The widest single measurement is reinforcement: 371 rooms carry it, among them lib/linter/file-report.js, lib/unsupported-api.js, lib/services/parser-service.js and tools/eslint-fuzzer.js [scaffolding ×371].

Load concentrates. The foundation — a high-load hub, a position in the import graph read from the load index, not a claim about outcome — fires on 48 rooms in the maintainability profile, including conf/globals.js, lib/config/flat-config-schema.js, lib/shared/traverser.js and tools/config-rule.js, and on the same count again under the onboarding overlay [foundation ×48].

Centrality marks 50 rooms, among them lib/api.js, lib/linter/linter.js, lib/rules/index.js and lib/shared/serialization.js [hub ×50]. Twenty-two rooms sit at high centrality with fan-out at or above the median — a high-centrality, high-fan-out junction — including lib/eslint/eslint.js, lib/rule-tester/rule-tester.js, lib/languages/js/source-code/token-store/index.js and packages/js/src/index.js [corridor ×22].

The graph has 19 import-graph roots, rooms with no fan-in and fan-out at or above the seventy-fifth percentile: bin/eslint.js, docs/.eleventy.js, lib/eslint/worker.js, tools/update-eslint-all.js among them [entrance ×19]. At the other end, 148 imported leaves carry no fan-out and fan-in at or above the seventy-fifth percentile, including lib/shared/flags.js, lib/rules/utils/char-source.js, lib/linter/esquery.js and packages/eslint-config-eslint/base.js [leaf_utility ×148].

Age spreads unevenly. 83 rooms sit at or beyond the ninetieth percentile of days since last touch: messages/plugin-conflict.js, lib/shared/text-table.js, docs/src/assets/js/themes.js, tools/commit-readme.sh, and the token-store cursors [dark_room ×83]. 48 rooms sit at or below the tenth percentile of the same measure, among them lib/cli.js, lib/options.js, lib/rules/prefer-template.js and tools/test-ecosystem/index.mjs [lit_room ×48]. A further 48 rooms carry a neglect index at or above the ninetieth percentile together with a load index of at least 0.10: lib/rules/camelcase.js, lib/rules/no-ternary.js, lib/shared/logging.js, lib/linter/code-path-analysis/code-path-segment.js [flooded_basement ×48].

49 decorative marks render but are not a diagnosis [crack ×48, toothpick_wing ×1]. The first names a high edit-pressure node, the second an unreinforced high-load node with high edit pressure; both rest on bug_pressure_index, which the gate records as unvalidated, and neither enters any diagnosis here, nor are their rooms named.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `1`
- brief_version: `0.1.0`
- effort: `high`
- facts_hash: `f623f5867d5a0247ffc64f36d5cd0dd6c3175fd5ce5c8621991d593399e5dff5`
- input_tokens: `21031`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3050`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations.
