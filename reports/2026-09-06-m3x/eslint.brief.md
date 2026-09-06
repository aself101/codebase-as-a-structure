# eslint — architect's brief

*Register lint: **FAILED (1 violation) on attempt 3**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `99af7dd3c201…`, facts `437dd628b8f9…`.*

473 rooms stand here. lib holds 388, docs 30, tools 22, messages 18, packages 8, the root 4, conf 2, bin 1. Across all profiles the survey records 896 diagnostic marks, 648 of them in the base profile, and 184 marks sit co-located with another. The widest single set covers 371 rooms [scaffolding ×371].

The heaviest load positions are marked by foundation — a high-load hub, a position in the import graph and nothing more — which fires on 48 rooms in the maintainability profile and on the same 48 in the onboarding overlay, among them conf/globals.js, lib/config/config.js, lib/rules/utils/ast-utils.js and lib/shared/traverser.js [foundation: conf/globals.js, lib/config/config.js, lib/rules/utils/ast-utils.js, lib/shared/traverser.js].

Centrality at or above p90 marks 50 rooms, including lib/api.js, lib/linter/linter.js, lib/rules/index.js and lib/shared/severity.js [hub: lib/api.js, lib/linter/linter.js, lib/rules/index.js, lib/shared/severity.js]. 22 of the overlay's rooms hold that centrality together with fan_out at or above p50 — the high-centrality, high-fan-out junction — among them lib/languages/js/source-code/source-code.js, lib/linter/code-path-analysis/code-path-analyzer.js and lib/rule-tester/rule-tester.js [corridor: lib/languages/js/source-code/source-code.js, lib/linter/code-path-analysis/code-path-analyzer.js, lib/rule-tester/rule-tester.js].

83 rooms carry last_touched_days at or above p90 — dark_room, a long-untouched room, a position in the age geometry — including lib/shared/text-table.js, lib/shared/ast-utils.js, messages/no-config-found.js and docs/src/assets/js/tabs.js [dark_room: lib/shared/text-table.js, lib/shared/ast-utils.js, messages/no-config-found.js, docs/src/assets/js/tabs.js].

48 rooms hold high neglect together with load_index at or above 0.10 — flooded_basement, a long-untouched, still-imported room, again a position and not a verdict — among them lib/rules/no-bitwise.js, lib/rules/semi.js, lib/rules/no-redeclare.js and lib/rules/utils/keywords.js [flooded_basement: lib/rules/no-bitwise.js, lib/rules/semi.js, lib/rules/no-redeclare.js, lib/rules/utils/keywords.js].

At the other end of the same geometry, 48 rooms sit at or below p10 on last_touched_days, including lib/cli.js, lib/options.js, lib/rules/quotes.js and tools/test-ecosystem/index.mjs [lit_room: lib/cli.js, lib/options.js, lib/rules/quotes.js, tools/test-ecosystem/index.mjs]. Reinforcement at or above 0.5 covers the largest set in the building, reaching lib/rules/no-magic-numbers.js and lib/services/parser-service.js among 371 rooms [scaffolding: lib/rules/no-magic-numbers.js, lib/services/parser-service.js].

The onboarding overlay reads edges. 19 rooms take no importers and hold fan_out at or above p75 — the import-graph root — among them bin/eslint.js, eslint.config.js and tools/update-eslint-all.js [import_root: bin/eslint.js, eslint.config.js, tools/update-eslint-all.js]. 148 rooms take no outward edges and hold fan_in at or above p75 — the imported leaf — including lib/shared/naming.js, lib/rules/no-octal.js and lib/rules/utils/lazy-loading-rule-map.js [leaf_utility: lib/shared/naming.js, lib/rules/no-octal.js, lib/rules/utils/lazy-loading-rule-map.js]. 11 rooms are declared package entries: lib/api.js, lib/unsupported-api.js and packages/js/src/index.js sit among them [package_entry: lib/api.js, lib/unsupported-api.js, packages/js/src/index.js].

49 decorative marks render but are not a diagnosis [crack ×48, toothpick_wing ×1]; crack names a high edit-pressure node and toothpick_wing an unreinforced high-load node with high edit pressure, both resting on bug_pressure_index, which is unvalidated, so neither enters the diagnosis and the rooms they touch are not named here.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `3`
- attempts_log: `1: R8-attribution, R8-attribution, R8-attribution, R8-attribution, R8-attribution, R2-provenance, R3-number, R3-number, R2-provenance; 2: R3-number, R3-number, R3-number, R2-provenance, R5-disclosure; 3: R2-provenance`
- brief_version: `0.2.0`
- effort: `high`
- facts_hash: `437dd628b8f975aac1847b48fe7a60afc5df036e1f674e227723a08ff13768a6`
- input_tokens: `21911`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `4151`
- stop_reason: `end_turn`

## Register lint

| rule | paragraph | detail | text |
|---|---|---|---|
| R2-provenance | 8 | paragraph carries no [feature: room] or [feature ×N] citation | 49 decorative marks render but are not a diagnosis [crack ×48, toothpick_wing ×1]; crack names a high edit-pressure node and toothpick_wing an unreinforced high |

**This brief failed the register lint and is not a diagnosis until it passes.**
