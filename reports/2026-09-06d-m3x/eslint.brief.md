# eslint — architect's brief

*Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `865b9a71c08a…`, facts `ef402ceaba8a…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `?`. Brief 0.2.1; a PASS is a pass under that grammar (D-035).*

The building holds 473 rooms across 8 wings: lib at 388, docs at 30, tools at 22, messages at 18, packages at 8, (root) at 4, conf at 2, bin at 1. Across all profiles 923 diagnostic marks land, and 184 of those sit co-located on rooms carrying more than one mark. The widest single mark is reinforcement, which covers 371 rooms [scaffolding ×371].

Reinforcement runs the length of the lib wing and reaches the tools and packages wings as well [scaffolding ×371: lib/rules/index.js, lib/linter/vfile.js, tools/config-rule.js]. It also stands on two rooms in the conf wing [scaffolding: conf/ecma-version.js, conf/globals.js].

Load concentrates on 48 rooms, and the same 48 register under the onboarding overlay — foundation here is a high-load hub, a position in the import graph, not a claim about what happens to it [foundation ×48; onboarding/foundation ×48]. The set includes rooms in lib/shared, lib/linter, and the tools wing [foundation ×48: lib/shared/traverser.js, lib/linter/source-code-fixer.js, tools/config-rule.js].

Centrality marks 50 rooms [hub ×50: lib/api.js, lib/linter/linter.js, lib/shared/serialization.js]. A narrower onboarding mark, the high-centrality, high-fan-out junction, sits on 22 [corridor ×22: lib/languages/js/source-code/token-store/index.js, lib/rule-tester/rule-tester.js].

Age marks 83 rooms — dark_room names a long-untouched room, a timestamp position, not a claim about condition [dark_room ×83: docs/src/assets/js/themes.js, lib/shared/text-table.js, messages/plugin-conflict.js]. Of the age readings, 75 rooms carry the narrower mark: flooded_basement names a long-untouched, still-imported room, again a position, and it stands across the messages wing and the token-store rooms [flooded_basement ×75: messages/file-not-found.js, lib/languages/js/source-code/token-store/skip-cursor.js, lib/shared/directives.js].

At the other end of the timestamp range, 48 rooms are recently touched [lit_room ×48: lib/cli.js, lib/rules/quotes.js, tools/test-ecosystem/index.mjs].

The onboarding overlay draws the graph's edges. 19 rooms sit as import-graph roots with no fan-in [import_root ×19: bin/eslint.js, docs/.eleventy.js, tools/update-eslint-all.js]. 148 sit as imported leaves with no fan-out [leaf_utility ×148: lib/shared/flags.js, lib/rules/no-with.js, packages/eslint-config-eslint/base.js]. 11 rooms are declared package entries [package_entry ×11: lib/api.js, lib/unsupported-api.js, packages/js/src/index.js].

49 decorative marks render but are not a diagnosis: crack — a high edit-pressure node — accounts for 48, and toothpick_wing — an unreinforced high-load node with high edit pressure — accounts for 1 [crack ×48; toothpick_wing ×1]. Both rest on an index the gate records as unvalidated, so neither enters the diagnosis and neither set of rooms is named here.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R5-disclosure, R5-disclosure; 2: pass`
- brief_version: `0.2.1`
- effort: `high`
- facts_hash: `ef402ceaba8a4cd0d93cd34f030329cdd4a2e140ed6a36637b9943ab5021ab49`
- input_tokens: `22471`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `2545`
- relinted: `brief 0.2.1`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations.
