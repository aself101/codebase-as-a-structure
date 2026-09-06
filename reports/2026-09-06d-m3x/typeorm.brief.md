# typeorm — architect's brief

*Register lint: **PASS on attempt 1**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `2e1af3cc5da0…`, facts `ba1104f200df…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `?`. Brief 0.2.1; a PASS is a pass under that grammar (D-035).*

583 rooms stand across 7 wings: src holds 496, packages 69, docs 9, (root) 3, playground 3, extra 2, docker 1. The survey records 619 diagnostic marks across all profiles, 84 of them co-located on the same rooms. The widest single set is the reinforcement set, which lands on 164 rooms and reaches into every wing that carries source, including packages and src [scaffolding ×164: packages/codemod/src/cli/parse-args.ts, src/metadata/EntityMetadata.ts, src/util/StringUtils.ts].

Foundation — a high-load hub, a position in the import graph, not a claim about what breaks — fires on 59 rooms under the maintainability profile and on the same count under the onboarding overlay [foundation ×59; onboarding/foundation ×59]. The named rooms sit in src/metadata, src/decorator/relations, src/schema-builder/table and src/util, and two sit outside src entirely [foundation ×59: packages/codemod/src/transforms/ast-helpers.ts, packages/codemod/src/transforms/stats.ts, src/metadata/ColumnMetadata.ts, src/schema-builder/table/TableColumn.ts].

Centrality marks 60 rooms, concentrated in src/decorator/options, src/metadata-args and src/common [hub ×60: src/metadata-args/MetadataArgsStorage.ts, src/common/EntityTarget.ts, src/data-source/DataSource.ts]. Under the onboarding overlay, the high-centrality, high-fan-out junction sits on 37 rooms, among them the top-level index and the query-builder surface [corridor ×37: src/index.ts, src/query-builder/SelectQueryBuilder.ts, src/query-builder/WhereExpressionBuilder.ts].

Dark_room — a long-untouched room, a position on the age axis — covers 70 rooms, the bulk of them in src/error and src/metadata-args [dark_room ×70: src/error/TypeORMError.ts, src/error/MissingDriverError.ts, src/metadata-args/EmbeddedMetadataArgs.ts]. Flooded_basement — a long-untouched, still-imported room, again a position, not a claim about damage — also covers 70 rooms, including the option and type declarations in src/decorator/options and src/driver/types [flooded_basement ×70: src/decorator/options/ValueTransformer.ts, src/driver/types/ReplicationMode.ts, src/common/ObjectLiteral.ts].

At the recent end of the same axis, 60 rooms are marked, spread across src/driver, src/query-builder and the two eslint configurations [lit_room ×60: eslint.config.mjs, src/driver/postgres/PostgresQueryRunner.ts, src/query-builder/QueryBuilder.ts].

The onboarding overlay also fixes the edges of the graph. One import-graph root is recorded [import_root ×1: packages/codemod/src/index.ts]. 33 imported leaves sit mostly in src/driver/types and src/metadata/types [leaf_utility ×33: src/driver/types/ColumnTypes.ts, src/metadata/types/OnDeleteType.ts, src/util/VersionUtils.ts]. 6 rooms are declared package entries, in src and in both packages subtrees [package_entry ×6: src/cli.ts, src/index.ts, packages/legacy-naming-strategies/src/index.ts].

61 decorative marks render but are not a diagnosis [crack ×59; toothpick_wing ×2]. Crack names a high edit-pressure node and toothpick_wing an unreinforced high-load node with high edit pressure; both rest on an unvalidated index, and their rooms are not named here.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `1`
- attempts_log: `1: pass`
- brief_version: `0.2.1`
- effort: `high`
- facts_hash: `ba1104f200df0068cfdd6d0553856f23e30f17238c8323a9c760cf0b5f8446bf`
- input_tokens: `19112`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `2597`
- relinted: `brief 0.2.1`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations.
