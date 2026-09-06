# eslint — architect's brief

*Register lint: **PASS**. Every claim below is licensed by an `asserted` signal and cites the feature and room it rests on; a claim voices a present structural position, never a consequence. Profile maintainability + onboarding, geometry age, skeleton `b55497a3ac8c…`, facts `880f4d39e57f…`.*

The building holds 473 rooms. The lib wing takes 388 of them; docs holds 30, tools 22, messages 18, packages 8, the root 4, conf 2, bin 1. The drawing is laid out on age. Nineteen rooms stand as import-graph roots, fan_in at zero and fan_out at or above p75 — the doors are Makefile.js, eslint.config.js, docs/.eleventy.js, lib/universal.js, tools/update-eslint-all.js and fourteen others [entrance ×19].

Fifty rooms sit at centrality p90 or above [hub ×50]. Forty-eight sit at load_index p90 or above — foundation, a high-load hub, a position in the import graph and not a claim about outcome [foundation ×48]. The two sets meet in lib/shared (assert.js, ast-utils.js, logging.js, naming.js, severity.js, string-utils.js, traverser.js), in lib/config (config.js, flat-config-array.js, flat-config-schema.js, default-config.js), and in lib/linter/index.js and lib/rules/utils/ast-utils.js. In total 181 rooms carry more than one diagnostic mark, out of 648 diagnostic marks placed.

Twenty-two rooms are high-centrality, high-fan-out junctions: centrality at p90 or above and fan_out at or above p50. lib/api.js, lib/linter/linter.js, lib/eslint/eslint.js, lib/rule-tester/rule-tester.js and lib/languages/js/source-code/source-code.js sit here [corridor ×22].

At the other end of the graph, 148 rooms are imported leaves — fan_out zero, fan_in at or above p75. Most are rule files (lib/rules/no-plusplus.js, lib/rules/no-octal.js, lib/rules/max-depth.js and their neighbours), joined by lib/shared/flags.js, lib/shared/naming.js and lib/rules/utils/keywords.js [leaf_utility ×148].

Reinforcement_index reaches 0.5 or above in 371 rooms, the largest single reading in the sheet, spanning the rule wing end to end and reaching lib/cli.js, lib/options.js, lib/linter/vfile.js and tools/eslint-fuzzer.js [scaffolding ×371].

On the age geometry, 83 rooms sit at last_touched_days p90 or above: the whole token-store cursor set, the messages wing (config-plugin-missing.js, plugin-conflict.js, whitespace-found.js and the rest), lib/shared/text-table.js, lib/universal.js, and most of docs/src [dark_room ×83]. Forty-eight rooms sit at p10 or below, among them Makefile.js, lib/cli.js, lib/config/config-loader.js, lib/rules/no-unused-vars.js and tools/test-ecosystem/index.mjs [lit_room ×48]. Six rooms hold both readings — lib/rules/utils/ast-utils.js, lib/eslint/eslint.js, lib/config/config.js among them — which is what happens when a room appears in both tails across profiles.

Forty-eight rooms carry neglect_index at p90 or above with load_index at 0.10 or above: lib/rules/no-redeclare.js, lib/rules/curly.js, lib/rules/semi.js, lib/rules/no-undef.js, lib/shared/logging.js, lib/rules/utils/keywords.js and lib/linter/code-path-analysis/code-path-segment.js among them [flooded_basement ×48].

49 decorative marks render but are not a diagnosis: 48 high edit-pressure nodes [crack ×48] and one unreinforced high-load node with high edit pressure at lib/eslint/eslint-helpers.js [toothpick_wing: lib/eslint/eslint-helpers.js]. Both rest on bug_pressure_index, which is unvalidated on the pre-registered test set (D-015); neither enters any diagnosis here.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `1`
- brief_version: `0.1.0`
- effort: `high`
- facts_hash: `880f4d39e57f9811617da1f15950fce17316195bd49b740adda583e841e58c5f`
- input_tokens: `20684`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `2564`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary, R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features excluded from diagnosis, R5 position-name disclosure, R6 no whole-building label, R7 decorative count stated.
