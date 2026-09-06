# typeorm — architect's brief

*Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `e1576a9568f1…`, facts `f0f4c2512c5f…`.*

The building holds 583 rooms. The src wing carries 496 of them; packages carries 69, docs 9, the root 3, playground 3, extra 2, docker 1. Across all profiles 608 diagnostic marks land, and 85 rooms carry more than one mark. Six declared package entries sit at the edges of these wings [package_entry: packages/codemod/src/index.ts, packages/legacy-naming-strategies/src/index.ts, src/cli-ts-node-commonjs.ts, src/cli-ts-node-esm.ts, src/cli.ts, src/index.ts].

The load measure fires on 59 rooms — foundation, a high-load hub, a position in the import graph, not a claim about what breaks — including src/metadata/EntityMetadata.ts, src/query-builder/SelectQueryBuilder.ts, src/platform/PlatformTools.ts, src/util/OrmUtils.ts and packages/codemod/src/transforms/ast-helpers.ts [foundation ×59].

Centrality at or above p90 marks 60 rooms, among them src/data-source/DataSource.ts, src/metadata-args/MetadataArgsStorage.ts, src/entity-schema/EntitySchema.ts and src/subscriber/event/BaseEvent.ts [hub ×60]. Of the high-centrality rooms, 37 also sit at or above median fan-out — a high-centrality, high-fan-out junction — including src/index.ts, src/entity-manager/EntityManager.ts, src/driver/Driver.ts and src/metadata-args/MetadataArgsStorage.ts [corridor ×37].

Reinforcement at or above 0.5 registers on 164 rooms, reaching from packages/codemod/src/cli/parse-args.ts and packages/legacy-naming-strategies/src/naming-strategy-v03.ts into src/error/QueryFailedError.ts, src/util/RandomGenerator.ts and src/subscriber/event/UpdateEvent.ts [scaffolding ×164].

Seventy rooms sit in the top decile of days since last touch — dark_room, a long-untouched room, a position on the age axis — among them src/error/TransactionNotStartedError.ts, src/metadata/types/TableTypes.ts, src/decorator/options/ColumnEnumOptions.ts and src/find-options/EqualOperator.ts [dark_room ×70]. Sixty rooms sit in the bottom decile of the same measure, including src/driver/postgres/PostgresQueryRunner.ts, src/repository/Repository.ts, src/cache/DbQueryResultCache.ts, src/metadata/UniqueMetadata.ts and eslint.config.mjs [lit_room ×60].

Fifty-nine rooms hold both a neglect index at or above p90 and a load index at or above 0.10 — flooded_basement, a long-untouched, still-imported room — among them src/cli.ts, src/entity-schema/EntitySchema.ts, src/metadata-args/TableMetadataArgs.ts, src/decorator/listeners/AfterLoad.ts and src/schema-builder/SchemaBuilder.ts [flooded_basement ×59].

At the graph's edges, one room has fan-in of zero with fan-out at or above p75 — an import-graph root [import_root: packages/codemod/src/index.ts]. Thirty-three rooms have fan-out of zero with fan-in at or above p75 — an imported leaf — including src/driver/Query.ts, src/common/DeepPartial.ts, src/util/Uint8ArrayUtils.ts and src/driver/types/UpsertType.ts [leaf_utility ×33].

61 decorative marks render but are not a diagnosis [crack ×59] and [toothpick_wing ×2]; crack names a high edit-pressure node and toothpick_wing an unreinforced high-load node with high edit pressure, both resting on an index the gate records as unvalidated, and neither is used here.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R3-number, R3-number, R8-attribution, R8-attribution, R8-attribution, R8-attribution, R8-attribution, R8-attribution, R8-attribution, R8-attribution, R8-attribution, R2-provenance, R2-provenance; 2: pass`
- brief_version: `0.2.0`
- effort: `high`
- facts_hash: `f0f4c2512c5f971b9fcfee3116adbbc4454b0f570fc7f3ea6402585240a39627`
- input_tokens: `20175`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `4132`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations.
