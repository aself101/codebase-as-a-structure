# typeorm — architect's brief

*Register lint: **PASS**. Every claim below is licensed by an `asserted` signal and cites the feature and room it rests on; a claim voices a present structural position, never a consequence. Profile maintainability + onboarding, geometry age, skeleton `5c122943226d…`, facts `31cc018c7fb6…`.*

The building holds 583 rooms in seven wings: src at 496, packages at 69, docs at 9, (root) and playground at 3 each, extra at 2, docker at 1. The packages wing carries the only import-graph root recorded, a room with fan_in of zero and fan_out at or above p75 [entrance: packages/codemod/src/index.ts].

Fifty-nine rooms register as foundation — a high-load hub, a position in the import graph, not a claim about what breaks. They sit in the metadata layer, the decorator set, the schema-builder tables and the driver interfaces, with src/data-source/DataSource.ts, src/metadata/EntityMetadata.ts and src/index.ts among them. The same 59 rooms register under both the maintainability profile and the onboarding overlay [foundation ×59].

Sixty rooms sit at or above p90 centrality [hub ×60]. Thirty-seven of those also carry fan_out at or above p50, making them high-centrality, high-fan-out junctions; src/data-source/DataSource.ts, src/entity-manager/EntityManager.ts, src/query-builder/SelectQueryBuilder.ts and src/metadata-args/MetadataArgsStorage.ts stand among them [corridor ×37].

Seventy rooms carry last_touched_days at or above p90 [dark_room ×70]. The dense cluster is the error directory and the metadata-args and option types — src/error/TypeORMError.ts, src/error/TransactionNotStartedError.ts, src/metadata-args/EmbeddedMetadataArgs.ts. Sixty rooms sit at the other end, last_touched_days at or below p10, and these are the drivers, query builders and repositories [lit_room ×60]. Some rooms hold both readings at once, among them src/metadata/ColumnMetadata.ts and src/index.ts [dark_room: src/common/ObjectLiteral.ts].

Fifty-nine rooms carry neglect_index at or above p90 together with load_index at or above 0.10 [flooded_basement ×59]; the error classes and metadata-args files fill most of that list, alongside src/cli.ts and src/entity-schema/EntitySchema.ts. Against that, 164 rooms hold reinforcement_index at or above 0.5, spread across packages/codemod, the decorator set, the util directory and the schema-builder tables [scaffolding ×164].

Thirty-three rooms are imported leaves — fan_out of zero, fan_in at or above p75 — mostly type aliases and small option shapes such as src/driver/types/ColumnTypes.ts and src/metadata/types/OnDeleteType.ts [leaf_utility ×33].

Eighty-four rooms are co-located: they answer to more than one diagnostic reading at once. src/data-source/DataSource.ts sits as high-load hub, hub, corridor, lit_room and reinforced room together; src/common/ObjectLiteral.ts sits as high-load hub, hub, dark_room, flooded_basement and imported leaf [foundation: src/data-source/DataSource.ts, src/common/ObjectLiteral.ts].

61 decorative marks render but are not a diagnosis. Fifty-nine of them are crack — a high edit-pressure node — and two are toothpick_wing — an unreinforced high-load node with high edit pressure, at src/driver/mongodb/typings.ts and src/query-builder/SelectQueryBuilder.ts. Both rest on bug_pressure_index, which the gate records as unvalidated, so neither enters the diagnosis [crack ×59, toothpick_wing ×2].

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact [foundation ×59, scaffolding ×164].

## Provenance

- attempt: `2`
- brief_version: `0.1.0`
- effort: `high`
- facts_hash: `31cc018c7fb62a1969ea88144799d4a12bbc43107ecba1834cc8ee8a2b3f9246`
- input_tokens: `18276`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `2450`
- relinted: `brief 0.1.0`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary, R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features excluded from diagnosis, R5 position-name disclosure, R6 no whole-building label, R7 decorative count stated.
