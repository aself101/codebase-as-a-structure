# Substrate report — `typeorm` @ `ac41823b9e`

*Deterministic sorted evidence over continuous signals. No feature is named here; naming is C3's job. Seed `33fbe1cfaa1a…`, config fingerprint `80b2a632f8b7…`, as-of 2026-09-02.*

> **UNGATED.** This report consults no `validation.json`. Every number below is a measurement or a fixed-weight blend of measurements; none has passed the anti-horoscope gate, and nothing here is a diagnosis. Diagnostic claims come only from C3 over gated signals (`structural-mapper-spec.md` §3).

## Summary

| field | value |
|---|---:|
| `node_count` | 3600 |
| `population_size` | 583 |
| `percentiles_valid` | yes |
| `orphan_nodes` | 0 |
| `graph_available` | yes |
| `graph_resolution_rate` | 1.00 |
| `fan_in_instrument_tau` | 1.00 |
| `graph_instruments_disagree` | no |
| `graph_degraded` | no |
| `external_imports` | 2073 |
| `unresolved_imports` | 8 |
| `non_node_imports` | 7 |
| `blame_failed` | 0 |
| `alt_scanner_unreadable` | 0 |
| `tsconfig_malformed` | no |
| `total_loc` | 268779 |
| `repo_age_days` | 3846 |
| `commit_count` | 6065 |
| `author_count` | 1273 |
| `authorship_gini` | 0.72 |
| `test_loc_ratio` | 0.56 |
| `dep_graph_density` | 0.00 |

## 1. Highest `load_index` (top 10)

| file | load | degraded | fan_in | centrality | fan_out | loc | cochange |
|---|---:|---:|---:|---:|---:|---:|---:|
| `src/driver/types/ColumnTypes.ts` | 0.94 | no | 35 | 0.01 | 0 | 216 | 59 |
| `src/platform/PlatformTools.ts` | 0.93 | no | 57 | 0.01 | 1 | 214 | 65 |
| `packages/codemod/src/transforms/ast-helpers.ts` | 0.92 | no | 34 | 0.00 | 0 | 1333 | 10 |
| `test/utils/test-utils.ts` | 0.92 | no | 912 | 0.02 | 4 | 543 | 109 |
| `src/util/ObjectUtils.ts` | 0.91 | no | 40 | 0.01 | 1 | 85 | 3 |
| `src/error/TypeORMError.ts` | 0.90 | no | 71 | 0.01 | 0 | 15 | 0 |
| `src/decorator/columns/Column.ts` | 0.89 | no | 768 | 0.02 | 15 | 233 | 59 |
| `src/data-source/DataSource.ts` | 0.89 | no | 621 | 0.02 | 38 | 696 | 22 |
| `src/driver/DriverUtils.ts` | 0.89 | no | 91 | 0.00 | 3 | 255 | 40 |
| `src/decorator/columns/PrimaryGeneratedColumn.ts` | 0.88 | no | 494 | 0.01 | 7 | 118 | 12 |

## 2. Highest `change_pressure_index` (top 10)

| file | change | churn | commits | last_touched_d |
|---|---:|---:|---:|---:|
| `src/driver/postgres/PostgresQueryRunner.ts` | 0.99 | 16624 | 331 | 6 |
| `src/query-builder/SelectQueryBuilder.ts` | 0.99 | 12403 | 248 | 1 |
| `src/entity-manager/EntityManager.ts` | 0.99 | 8139 | 210 | 0 |
| `src/driver/postgres/PostgresDriver.ts` | 0.98 | 7477 | 292 | 7 |
| `src/driver/mysql/MysqlDriver.ts` | 0.98 | 6904 | 267 | 7 |
| `src/driver/cockroachdb/CockroachQueryRunner.ts` | 0.98 | 9617 | 99 | 6 |
| `src/query-builder/transformer/RawSqlResultsToEntityTransformer.ts` | 0.97 | 3537 | 119 | 5 |
| `src/query-builder/QueryBuilder.ts` | 0.97 | 15876 | 352 | 55 |
| `src/metadata/ColumnMetadata.ts` | 0.97 | 4236 | 185 | 41 |
| `src/query-builder/InsertQueryBuilder.ts` | 0.97 | 4728 | 139 | 41 |

## 3. Highest `bug_pressure_index` (top 10)

| file | bug | fixes | reverts | commits | reinforcement |
|---|---:|---:|---:|---:|---:|
| `src/query-builder/SelectQueryBuilder.ts` | 0.99 | 76 | 4 | 248 | 0.00 |
| `src/driver/postgres/PostgresQueryRunner.ts` | 0.99 | 80 | 2 | 331 | 0.76 |
| `src/driver/mysql/MysqlDriver.ts` | 0.99 | 47 | 3 | 267 | 0.82 |
| `src/driver/postgres/PostgresDriver.ts` | 0.99 | 46 | 2 | 292 | 0.91 |
| `src/entity-manager/EntityManager.ts` | 0.99 | 34 | 2 | 210 | 0.85 |
| `src/metadata/ColumnMetadata.ts` | 0.98 | 27 | 2 | 185 | 0.85 |
| `src/query-builder/transformer/RawSqlResultsToEntityTransformer.ts` | 0.98 | 22 | 2 | 119 | 0.00 |
| `src/query-builder/QueryBuilder.ts` | 0.97 | 44 | 1 | 352 | 0.61 |
| `src/query-builder/InsertQueryBuilder.ts` | 0.97 | 33 | 1 | 139 | 0.00 |
| `src/persistence/SubjectExecutor.ts` | 0.96 | 17 | 3 | 178 | 0.00 |

## 4. High load, low reinforcement — `load_index ≥ 0.9 ∧ reinforcement_index ≤ 0.1` (top 10 by load)

| file | load | degraded | fan_in | centrality | reinforcement | bug |
|---|---:|---:|---:|---:|---:|---:|
| `src/driver/types/ColumnTypes.ts` | 0.94 | no | 35 | 0.01 | 0.00 | 0.67 |

## 5. Old, load-bearing, untouched — `neglect_index ≥ 0.9 ∧ load_index ≥ 0.1` (top 10 by neglect)

| file | neglect | load | age_d | last_touched_d | blame_age_d | fan_in |
|---|---:|---:|---:|---:|---:|---:|
| `src/error/ConnectionNotFoundError.ts` | 0.95 | 0.21 | 3846 | 1629 | 3782.61 | 1 |
| `src/error/MetadataAlreadyExistsError.ts` | 0.95 | 0.23 | 3846 | 1629 | 1629.71 | 1 |
| `src/error/MetadataWithSuchNameAlreadyExistsError.ts` | 0.95 | 0.21 | 3846 | 1629 | 1629.71 | 1 |
| `src/error/MissingDriverError.ts` | 0.93 | 0.42 | 3780 | 1629 | 1895.29 | 2 |
| `src/error/ConnectionIsNotSetError.ts` | 0.92 | 0.59 | 3818 | 1629 | 3656.11 | 8 |
| `src/error/ColumnTypeUndefinedError.ts` | 0.92 | 0.65 | 3819 | 1629 | 3115.10 | 3 |
| `src/error/PrimaryColumnCannotBeNullableError.ts` | 0.92 | 0.52 | 3819 | 1629 | 1629.71 | 2 |
| `src/common/ObjectType.ts` | 0.91 | 0.75 | 3817 | 1629 | 3748.36 | 7 |

## Caveats

- **Unresolved in-repo imports** (first 8 of 8): `packages/codemod/test/transforms/v1/fixtures/connection-to-datasource/connection-to-datasource-no-typeorm-import.input.ts` → `./local-data-source`, `packages/codemod/test/transforms/v1/fixtures/connection-to-datasource/connection-to-datasource-no-typeorm-import.output.ts` → `./local-data-source`, `packages/codemod/test/transforms/v1/fixtures/relation-count/relation-count-no-typeorm-import.input.ts` → `./entity/Post`, `packages/codemod/test/transforms/v1/fixtures/relation-count/relation-count-no-typeorm-import.input.ts` → `./helpers/types`, `packages/codemod/test/transforms/v1/fixtures/relation-count/relation-count-no-typeorm-import.output.ts` → `./entity/Post`, `packages/codemod/test/transforms/v1/fixtures/relation-count/relation-count-no-typeorm-import.output.ts` → `./helpers/types`, `test/github-issues/4219/shim.ts` → `../../../../../extra/typeorm-class-transformer-shim`, `test/github-issues/4219/shim.ts` → `../../../../extra/typeorm-class-transformer-shim`
