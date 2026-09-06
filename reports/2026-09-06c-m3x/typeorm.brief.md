# typeorm — architect's brief

*Register lint: **PASS on attempt 1**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `5fab712a942a…`, facts `fe886e703e7c…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page.*

The building holds 583 rooms in seven wings: src carries 496, packages 69, docs 9, playground 3, (root) 3, extra 2, docker 1. Across all profiles 619 diagnostic marks land, and 84 of those sit co-located on rooms that already carry another mark. The widest single set is scaffolding, at 164 rooms, reaching from the codemod package through the decorators, drivers, metadata and util shelves [scaffolding ×164: packages/codemod/src/cli/parse-args.ts, src/metadata/EntityMetadata.ts, src/util/OrmUtils.ts].

The load-bearing set is foundation — a high-load hub, a position in the import graph, not a claim about what breaks — and it fires identically in both profiles at 59 rooms, gathered in the decorator, metadata, schema-builder table and util shelves [foundation ×59; onboarding/foundation ×59: src/metadata/ColumnMetadata.ts, src/schema-builder/table/Table.ts, src/index.ts].

Centrality marks 60 rooms, sitting largely on the same shelves: data-source, decorator options, metadata-args, query-runner [hub ×60: src/data-source/DataSource.ts, src/metadata-args/MetadataArgsStorage.ts, src/query-runner/QueryRunner.ts]. The onboarding overlay narrows to 37 junctions of high centrality and high fan-out [onboarding/corridor ×37: src/entity-manager/EntityManager.ts, src/query-builder/SelectQueryBuilder.ts, src/driver/Driver.ts].

Age geometry puts 70 rooms in dark_room — a long-untouched room, a position on the last-touched axis — concentrated almost entirely in the src/error shelf and the small option and type declarations beside it [dark_room ×70: src/error/TypeORMError.ts, src/metadata/types/TableTypes.ts, src/common/ObjectLiteral.ts]. The same count, 70, appears under flooded_basement — a long-untouched, still-imported room, a position combining last-touched with load — on the same shelves [flooded_basement ×70: src/error/QueryRunnerAlreadyReleasedError.ts, src/decorator/options/ValueTransformer.ts, src/subscriber/BroadcasterResult.ts].

At the other end of the same axis, 60 rooms are recently touched, spread across drivers, query-builder, repository and the two eslint configs [lit_room ×60: src/driver/postgres/PostgresDriver.ts, src/query-builder/QueryBuilder.ts, eslint.config.mjs].

The onboarding overlay also fixes the edges of the import graph. One room is an import-graph root with no fan-in [onboarding/import_root: packages/codemod/src/index.ts]. Thirty-three rooms are imported leaves with no fan-out, mostly type and option declarations [onboarding/leaf_utility ×33: src/driver/types/ColumnTypes.ts, src/common/DeepPartial.ts, src/util/VersionUtils.ts]. Six rooms are declared package entries [onboarding/package_entry ×6: src/cli.ts, packages/legacy-naming-strategies/src/index.ts, src/index.ts].

61 decorative marks render but are not a diagnosis [crack ×59; toothpick_wing ×2]. Crack names a high edit-pressure node and toothpick_wing an unreinforced high-load node with high edit pressure; both rest on bug_pressure_index, which the gate records as unvalidated, so neither enters the diagnosis and neither set of rooms is named here.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `1`
- attempts_log: `1: pass`
- brief_version: `0.2.1`
- effort: `high`
- facts_hash: `fe886e703e7ca2db24bbc209ccba7ff798bb07e9c46fc039edf252e437cf6f33`
- input_tokens: `19038`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `2738`
- relinted: `brief 0.2.1`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations.
