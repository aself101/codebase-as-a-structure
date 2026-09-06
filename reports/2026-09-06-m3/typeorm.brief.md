# typeorm — architect's brief

*Register lint: **FAILED (3 violations)**. Every claim below is licensed by an `asserted` signal and cites the feature and room it rests on; a claim voices a present structural position, never a consequence. Profile maintainability + onboarding, geometry age, skeleton `5c122943226d…`, facts `31cc018c7fb6…`.*

The census is 583 rooms. `src` holds 496, `packages` 69, `docs` 9, `(root)` and `playground` 3 each, `extra` 2, `docker` 1. Exactly one room has no importer and a fan-out at or above the 75th percentile — the import-graph root [entrance: packages/codemod/src/index.ts]. The survey rests on 472 diagnostic marks and 84 co-located ones; the geometry is age, with an onboarding overlay laid over the maintainability profile [corridor ×37].

The widest mark is scaffolding, at reinforcement_index of 0.5 or more, standing on 164 rooms: the decorator set, the error classes, the schema-builder tables, and the utility drawer [scaffolding ×164]. It reaches the largest rooms in the building as well [scaffolding: src/data-source/DataSource.ts, src/metadata/EntityMetadata.ts, src/query-builder/QueryBuilder.ts].

Load concentrates. foundation — a high-load hub, a position in the import graph, not a statement about what a room contains — covers 59 rooms, and the same 59 under both the maintainability and onboarding profiles [foundation ×59]. hub, at centrality in the top decile, covers 60 [hub ×60]. The two overlap on the metadata core and the public surface [foundation: src/index.ts, src/metadata/ColumnMetadata.ts, src/metadata/EntityMetadata.ts, src/entity-manager/EntityManager.ts]. Of the high-centrality rooms, 37 also carry fan-out at or above the median and are marked as high-centrality, high-fan-out junctions [corridor ×37], while 33 rooms have fan_out of zero and fan_in in the top quartile — imported leaves, mostly the type and option declarations [leaf_utility: src/driver/types/ColumnTypes.ts, src/common/ObjectLiteral.ts, src/error/TypeORMError.ts].

Age splits the floor. 70 rooms sit in the oldest decile by last touch, densest in `src/error`, `src/metadata-args`, and the option types [dark_room ×70]. 60 rooms sit in the newest decile, densest in the drivers, the query builders, and the repository layer [lit_room ×60]. Some rooms carry high load and old paint together [dark_room: src/decorator/options/ValueTransformer.ts, src/metadata/types/DeferrableType.ts, src/error/TypeORMError.ts]; others carry high load and recent touch [lit_room: src/data-source/DataSource.ts, src/query-builder/SelectQueryBuilder.ts, src/util/OrmUtils.ts].

Where neglect_index sits in the top decile and load_index is at or above 0.10, the mark is flooded_basement — 59 rooms, again weighted to `src/error`, the listener decorators, and the metadata-args set [flooded_basement ×59], and reaching the CLI entry and the schema-builder interface [flooded_basement: src/cli.ts, src/schema-builder/SchemaBuilder.ts, src/entity-schema/EntitySchema.ts].

61 decorative marks render but are not a diagnosis: crack — a high edit-pressure node — on 59 rooms [crack ×59], and toothpick_wing — an unreinforced high-load node with high edit pressure — on 2 [toothpick_wing: src/driver/mongodb/typings.ts, src/query-builder/SelectQueryBuilder.ts]. Both rest on bug_pressure_index, which the gate lists as unvalidated; neither enters the diagnosis.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact [foundation ×59; scaffolding ×164].

## Provenance

- attempt: `2`
- brief_version: `0.1.0`
- effort: `high`
- facts_hash: `31cc018c7fb62a1969ea88144799d4a12bbc43107ecba1834cc8ee8a2b3f9246`
- input_tokens: `18774`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `2604`
- stop_reason: `end_turn`

## Register lint

| rule | paragraph | detail | text |
|---|---|---|---|
| R4-decorative | 6 | diagnostic claim cites a decorative feature: crack (excluded from diagnosis, mapper §3) | 61 decorative marks render but are not a diagnosis: crack — a high edit-pressure node — on 59 rooms [crack ×59], and toothpick_wing — an unreinforced high-load  |
| R4-decorative | 6 | diagnostic claim cites a decorative feature: toothpick_wing (excluded from diagnosis, mapper §3) | 61 decorative marks render but are not a diagnosis: crack — a high edit-pressure node — on 59 rooms [crack ×59], and toothpick_wing — an unreinforced high-load  |
| R2-provenance | 7 | paragraph carries no [feature: room] or [feature ×N] citation | The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited,  |

**This brief failed the register lint and is not a diagnosis until it passes.**
