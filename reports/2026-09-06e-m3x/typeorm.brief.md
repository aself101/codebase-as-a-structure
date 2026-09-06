# typeorm — architect's brief

*Register lint: **PASS on attempt 1**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `2e1af3cc5da0…`, facts `05e6a06edf43…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.3.0; a PASS is a pass under that grammar (D-035).*

The building holds 583 rooms in 7 wings: 496 in src, 69 in packages, 9 in docs, 3 in (root), 3 in playground, 2 in extra, 1 in docker. Across all profiles 619 diagnostic marks land on it, and 160 of those marks are co-located. The widest single set is scaffolding, 164 rooms, of which 147 sit in src and 17 in packages [scaffolding ×164: src/util/OrmUtils.ts, packages/codemod/src/lib/colors.ts].

The load positions are named foundation — the position name is high-load hub, a location in the import graph and not a claim about damage. There are 59 of them, 57 in src and 2 in packages [foundation ×59: src/metadata/EntityMetadata.ts, packages/codemod/src/transforms/ast-helpers.ts]. The 59 foundation rooms in the maintainability profile are the same 59 rooms as the onboarding foundation set [foundation ×59; onboarding/foundation ×59].

Centrality marks 60 hub rooms, all 60 in src [hub ×60: src/index.ts, src/data-source/DataSource.ts]. The 37 corridor rooms — the position name is high-centrality, high-fan-out junction — sit within the 60 hub rooms [corridor ×37; hub ×60], and all 37 are in src [corridor ×37: src/metadata-args/MetadataArgsStorage.ts, src/query-builder/WhereExpressionBuilder.ts].

Age marks two sets that coincide. dark_room — the position name is long-untouched room — covers 70 rooms, all 70 in src [dark_room ×70: src/error/TypeORMError.ts, src/common/ObjectLiteral.ts]. The 70 flooded_basement rooms — the position name is long-untouched, still-imported room — are the same 70 rooms as dark_room [flooded_basement ×70; dark_room ×70].

At the other end of the same axis, lit_room marks 60 rooms: 57 in src, 2 in packages, 1 in (root) [lit_room ×60: src/query-builder/QueryBuilder.ts, packages/codemod/src/transforms/v1/mongodb-types.ts, eslint.config.mjs].

The onboarding overlay adds three edge positions. package_entry marks 6 declared entries, 4 in src and 2 in packages [package_entry ×6: src/cli.ts, packages/legacy-naming-strategies/src/index.ts]. The single import_root room, an import-graph root, sits in packages and lies within the package_entry set [import_root ×1: packages/codemod/src/index.ts; package_entry ×6]. leaf_utility, the imported-leaf position, marks 33 rooms, 29 in src and 4 in packages [leaf_utility ×33: src/driver/types/ColumnTypes.ts, packages/codemod/src/transforms/todo.ts].

61 decorative marks render but are not a diagnosis [crack ×59; toothpick_wing ×2]. crack carries the position name high edit-pressure node; toothpick_wing carries the position name unreinforced high-load node with high edit pressure. Neither rests on a validated measure and neither enters the findings above.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `1`
- attempts_log: `1: pass`
- brief_version: `0.3.0`
- effort: `high`
- facts_hash: `05e6a06edf433523e142df27e9caf6682a0df062102993d32f118e038ccad953`
- input_tokens: `19948`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3693`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb — shares are by_wing counts (D-036).
