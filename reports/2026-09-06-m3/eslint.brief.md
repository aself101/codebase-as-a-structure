# eslint — architect's brief

*Register lint: **PASS**. Every claim below is licensed by an `asserted` signal and cites the feature and room it rests on; a claim voices a present structural position, never a consequence. Profile maintainability + onboarding, geometry age, skeleton `b55497a3ac8c…`, facts `880f4d39e57f…`.*

The building holds 473 rooms in eight wings: 388 in lib, 30 in docs, 22 in tools, 18 in messages, 8 in packages, 4 at the root, 2 in conf, 1 in bin. The geometry is age; the profile is maintainability with an onboarding overlay. Nineteen rooms take imports from nowhere and hand out at fan_out at or above p75 — the build script, the binary, the docs generator, the release tooling, the worker and the universal entry [entrance: Makefile.js, bin/eslint.js, docs/.eleventy.js, tools/update-eslint-all.js, lib/eslint/worker.js, lib/universal.js].

Load concentrates in 48 rooms at load_index p90 or above — foundation, a high-load hub, a position in the import graph and not a verdict on behaviour. These sit in config schema, the rule index, the traverser, the timer, the globals table and the tooling that generates configs [foundation: lib/config/flat-config-schema.js, lib/rules/index.js, lib/shared/traverser.js, lib/linter/timing.js, conf/globals.js, tools/config-rule.js].

Fifty rooms stand at centrality p90 or above [hub: lib/linter/linter.js, lib/languages/js/source-code/source-code.js, lib/api.js, packages/js/src/index.js, lib/shared/severity.js]. Twenty-two of those also carry fan_out at or above p50, the junctions where traffic both arrives and departs [corridor: lib/linter/linter.js, lib/rule-tester/rule-tester.js, lib/config/flat-config-array.js, lib/languages/js/source-code/token-store/index.js]. At the other end of the graph, 148 rooms take fan_in at or above p75 with fan_out of zero [leaf_utility: lib/shared/flags.js, lib/rules/utils/char-source.js, lib/shared/relative-module-resolver.js, conf/ecma-version.js].

Reinforcement at 0.5 or above covers 371 rooms, most of the rule catalogue and much of the linter core [scaffolding: lib/rules/index.js, lib/linter/vfile.js, lib/services/parser-service.js].

By age, 83 rooms sit at last_touched_days p90 or above: the token-store cursors, the messages wing, the shared utilities, the docs asset scripts and two build files [dark_room: lib/languages/js/source-code/token-store/cursor.js, messages/plugin-missing.js, lib/shared/ajv.js, lib/shared/text-table.js, docs/src/assets/js/search.js, webpack.config.js]. Forty-eight rooms sit at p10 or below, in the CLI, the options table, several rules and the ecosystem tooling [lit_room: lib/cli.js, lib/options.js, lib/rules/no-unused-vars.js, tools/test-ecosystem/index.mjs, lib/languages/js/source-code/source-code.js].

Forty-eight rooms hold neglect_index at p90 or above together with load_index at 0.10 or above, nearly all of them single-purpose rules, plus the shared logger, the keyword table and a code-path segment [flooded_basement: lib/rules/camelcase.js, lib/rules/no-undef.js, lib/rules/semi.js, lib/shared/logging.js, lib/rules/utils/keywords.js, lib/linter/code-path-analysis/code-path-segment.js].

Marks overlap: 648 diagnostic marks land on the building, and 181 rooms carry more than one. The traverser alone sits at high load, at high centrality, at last_touched_days p90 or above, under reinforcement, and at the end of the import graph [foundation: lib/shared/traverser.js; hub: lib/shared/traverser.js; dark_room: lib/shared/traverser.js; scaffolding: lib/shared/traverser.js; leaf_utility: lib/shared/traverser.js].

Forty-nine decorative marks render but are not a diagnosis: crack — a high edit-pressure node, a position, not a verdict — and toothpick_wing — an unreinforced high-load node with high edit pressure, likewise a position [crack ×48; toothpick_wing: lib/eslint/eslint-helpers.js]. Both rest on bug_pressure_index, which is unvalidated; neither enters any diagnosis here.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- brief_version: `0.1.0`
- effort: `high`
- facts_hash: `880f4d39e57f9811617da1f15950fce17316195bd49b740adda583e841e58c5f`
- input_tokens: `20989`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3643`
- relinted: `brief 0.1.0`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary, R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features excluded from diagnosis, R5 position-name disclosure, R6 no whole-building label, R7 decorative count stated.
