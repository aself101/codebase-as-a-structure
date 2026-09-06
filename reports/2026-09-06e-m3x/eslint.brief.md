# eslint — architect's brief

*Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `865b9a71c08a…`, facts `cf6dea7f25a4…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.3.0; a PASS is a pass under that grammar (D-035).*

The building holds 473 rooms in 8 wings: 388 in lib, 30 in docs, 22 in tools, 18 in messages, 8 in packages, 4 at (root), 2 in conf, 1 in bin. Across all profiles 923 diagnostic marks land on it, and 254 rooms carry more than one mark. The widest single set is scaffolding at 371 rooms — 360 in lib, 6 in tools, 2 in conf, 2 in docs, 1 in packages [scaffolding ×371: lib/rules/index.js, lib/linter/vfile.js, tools/config-rule.js].

Load sits in one wing. The foundation set — the position name is high-load hub, a spot in the import graph and nothing more — covers 48 rooms, 45 in lib, 2 in conf, 1 in tools [foundation ×48: lib/config/flat-config-schema.js, lib/rules/utils/ast-utils.js, conf/globals.js]. The 48 foundation rooms of the maintainability profile are the same 48 rooms as onboarding's foundation [foundation ×48; onboarding/foundation ×48].

Centrality lands nearby. 50 rooms carry the hub mark, 46 in lib, 2 in conf, 1 in docs, 1 in packages [hub ×50: lib/linter/linter.js, lib/shared/traverser.js, packages/js/src/index.js]. The 22 corridor rooms — a high-centrality, high-fan-out junction — sit within the hub set, 21 of them in lib and 1 in packages [corridor ×22; hub ×50].

Age is the second axis. 83 rooms are dark_room — the position name is long-untouched room — with 40 in lib, 22 in docs, 11 in messages, 5 in packages, 3 in tools, 2 at (root) [dark_room ×83: docs/src/assets/js/themes.js, messages/plugin-conflict.js, lib/shared/text-table.js]. The 75 flooded_basement rooms — a long-untouched, still-imported room — sit within that same dark_room set, 38 in lib, 18 in docs, 11 in messages, 3 in packages, 3 in tools, 2 at (root) [flooded_basement ×75; dark_room ×83]. At the other end of the same axis, 48 rooms are lit_room, 40 in lib, 5 in tools, 2 at (root), 1 in messages [lit_room ×48: lib/cli.js, tools/check-emfile-handling.js, Makefile.js].

The graph's edges are marked at both ends. 148 rooms are leaf_utility — an imported leaf — with 139 in lib, 2 in conf, 2 in docs, 2 in packages, 2 in tools, 1 in messages [leaf_utility ×148: lib/shared/flags.js, conf/ecma-version.js, tools/test-ecosystem/data.mjs]. 19 rooms are import_root, 7 in tools, 3 in docs, 2 at (root), 2 in lib, 2 in messages, 2 in packages, 1 in bin [import_root ×19: tools/update-eslint-all.js, docs/.eleventy.js, bin/eslint.js]. 11 rooms are package_entry, 5 in packages, 4 in lib, 1 in bin, 1 in docs [package_entry ×11: lib/api.js, packages/eslint-config-eslint/base.js].

49 decorative marks render but are not a diagnosis [crack ×48; toothpick_wing ×1]; crack names a high edit-pressure node and toothpick_wing an unreinforced high-load node with high edit pressure, and neither position is used here.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate in few rooms — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R8-attribution, R2-provenance; 2: pass`
- brief_version: `0.3.0`
- effort: `high`
- facts_hash: `cf6dea7f25a41bada7771c0e9fb80415f2e581944ae616e73511d476629123cd`
- input_tokens: `23672`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3084`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb — shares are by_wing counts (D-036).
