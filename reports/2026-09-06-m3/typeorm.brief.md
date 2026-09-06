# typeorm — architect's brief

*Register lint: **PASS on attempt 1**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `5c122943226d…`, facts `56b699e9ca81…`.*

583 rooms stand across seven wings: src holds 496, packages 69, docs 9, (root) 3, playground 3, extra 2, docker 1. Across all profiles 602 diagnostic marks land on this population, and 84 rooms carry more than one mark. One room sits with no inbound imports and fan-out at or above p75 — packages/codemod/src/index.ts, an import-graph root [entrance: packages/codemod/src/index.ts].

Sixty rooms sit at centrality at or above p90. Among them src/data-source/DataSource.ts, src/metadata/EntityMetadata.ts, src/index.ts, src/entity-manager/EntityManager.ts and src/query-runner/QueryRunner.ts [hub: src/data-source/DataSource.ts, src/metadata/EntityMetadata.ts, src/index.ts, src/entity-manager/EntityManager.ts, src/query-runner/QueryRunner.ts]. Thirty-seven rooms hold that centrality together with fan-out at or above p50 — a high-centrality, high-fan-out junction — including src/metadata-args/MetadataArgsStorage.ts, src/query-builder/WhereExpressionBuilder.ts, src/util/InstanceChecker.ts and src/error/index.ts [corridor: src/metadata-args/MetadataArgsStorage.ts, src/query-builder/WhereExpressionBuilder.ts, src/util/InstanceChecker.ts, src/error/index.ts].

Fifty-nine rooms register load_index at or above p90 — foundation, a high-load hub, a position in the import graph and nothing more — and the same set registers under both the maintainability and the onboarding profile: src/util/OrmUtils.ts, src/platform/PlatformTools.ts, src/query-builder/SelectQueryBuilder.ts, src/driver/types/ColumnTypes.ts and packages/codemod/src/transforms/ast-helpers.ts among them [foundation ×59].

The largest diagnostic set is reinforcement_index at or above 0.5, on 164 rooms: src/error/QueryFailedError.ts, src/util/RandomGenerator.ts, src/schema-builder/table/TableForeignKey.ts, src/subscriber/event/InsertEvent.ts, packages/legacy-naming-strategies/src/naming-strategy-v03.ts and packages/codemod/src/cli/parse-args.ts sit inside it [scaffolding ×164].

Seventy rooms sit at last_touched_days at or above p90 — src/common/MixedList.ts, src/error/TypeORMError.ts, src/metadata-args/CheckMetadataArgs.ts, src/metadata/types/TableTypes.ts, src/query-builder/SelectQuery.ts [dark_room: src/common/MixedList.ts, src/error/TypeORMError.ts, src/metadata-args/CheckMetadataArgs.ts, src/metadata/types/TableTypes.ts, src/query-builder/SelectQuery.ts]. Fifty-nine rooms hold neglect_index at or above p90 with load_index at or above 0.10, including src/cli.ts, src/entity-schema/EntitySchema.ts, src/metadata-args/TableMetadataArgs.ts and src/schema-builder/SchemaBuilder.ts [flooded_basement: src/cli.ts, src/entity-schema/EntitySchema.ts, src/metadata-args/TableMetadataArgs.ts, src/schema-builder/SchemaBuilder.ts].

At the other end of the age geometry, sixty rooms show last_touched_days at or below p10: eslint.config.mjs, src/driver/postgres/PostgresQueryRunner.ts, src/repository/Repository.ts, src/metadata/UniqueMetadata.ts, src/util/VersionUtils.ts [lit_room: eslint.config.mjs, src/driver/postgres/PostgresQueryRunner.ts, src/repository/Repository.ts, src/metadata/UniqueMetadata.ts, src/util/VersionUtils.ts].

Thirty-three rooms are imported leaves — fan-out zero, fan-in at or above p75 — among them src/driver/Query.ts, src/driver/types/UpsertType.ts, src/repository/SaveOptions.ts, src/subscriber/BroadcasterResult.ts and packages/codemod/src/transforms/todo.ts [leaf_utility: src/driver/Query.ts, src/driver/types/UpsertType.ts, src/repository/SaveOptions.ts, src/subscriber/BroadcasterResult.ts, packages/codemod/src/transforms/todo.ts].

61 decorative marks render but are not a diagnosis: the high edit-pressure node, and the unreinforced high-load node with high edit pressure, both resting on an unvalidated index [crack ×59, toothpick_wing ×2].

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `1`
- brief_version: `0.1.0`
- effort: `high`
- facts_hash: `56b699e9ca812c135451db48a4f881e7a7d1fabb08d47168ac62708750b4725d`
- input_tokens: `18349`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3643`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations.
