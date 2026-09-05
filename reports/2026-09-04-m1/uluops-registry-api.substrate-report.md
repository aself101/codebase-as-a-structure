# Substrate report — `uluops-registry-api` @ `f7414cc7bb`

*Deterministic sorted evidence over continuous signals. No feature is named here; naming is C3's job. Seed `c576e0759dc9…`, config fingerprint `80b2a632f8b7…`, as-of 2026-08-31.*

> **UNGATED.** This report consults no `validation.json`. Every number below is a measurement or a fixed-weight blend of measurements; none has passed the anti-horoscope gate, and nothing here is a diagnosis. Diagnostic claims come only from C3 over gated signals (`structural-mapper-spec.md` §3).

## Summary

| field | value |
|---|---:|
| `node_count` | 456 |
| `population_size` | 267 |
| `percentiles_valid` | yes |
| `orphan_nodes` | 0 |
| `graph_available` | yes |
| `graph_resolution_rate` | 1.00 |
| `fan_in_instrument_tau` | 0.99 |
| `graph_instruments_disagree` | no |
| `graph_degraded` | no |
| `external_imports` | 565 |
| `unresolved_imports` | 0 |
| `non_node_imports` | 1 |
| `blame_failed` | 0 |
| `alt_scanner_unreadable` | 0 |
| `tsconfig_malformed` | no |
| `total_loc` | 87134 |
| `repo_age_days` | 226 |
| `commit_count` | 956 |
| `author_count` | 2 |
| `authorship_gini` | 0.50 |
| `test_loc_ratio` | 0.55 |
| `dep_graph_density` | 0.01 |

## 1. Highest `load_index` (top 10)

| file | load | degraded | fan_in | centrality | fan_out | loc | cochange |
|---|---:|---:|---:|---:|---:|---:|---:|
| `src/utils/errors.ts` | 0.96 | no | 56 | 0.03 | 0 | 254 | 18 |
| `src/services/safety/types.ts` | 0.94 | no | 23 | 0.01 | 0 | 283 | 15 |
| `src/schemas/enums.ts` | 0.92 | no | 48 | 0.04 | 1 | 141 | 26 |
| `src/config/index.ts` | 0.92 | no | 15 | 0.04 | 0 | 157 | 33 |
| `src/db/connection.ts` | 0.91 | no | 45 | 0.02 | 3 | 383 | 34 |
| `src/utils/uuid.ts` | 0.91 | no | 36 | 0.02 | 0 | 81 | 1 |
| `src/middleware/auth.ts` | 0.91 | no | 29 | 0.01 | 2 | 393 | 66 |
| `src/routes/v1/schemas.ts` | 0.90 | no | 25 | 0.01 | 2 | 530 | 66 |
| `src/schemas/definition/provenance.ts` | 0.89 | no | 12 | 0.01 | 0 | 144 | 8 |
| `test/helpers/mock-knex.ts` | 0.88 | no | 11 | 0.00 | 0 | 384 | 36 |

## 2. Highest `change_pressure_index` (top 10)

| file | change | churn | commits | last_touched_d |
|---|---:|---:|---:|---:|
| `src/controllers/definition-controller.ts` | 0.99 | 2418 | 95 | 3 |
| `src/index.ts` | 0.99 | 1638 | 73 | 3 |
| `src/db/repository/definition-repository.ts` | 0.98 | 3377 | 87 | 7 |
| `src/services/analytics/analytics-service.ts` | 0.98 | 2424 | 64 | 7 |
| `test/unit/services/analytics/analytics-service.test.ts` | 0.97 | 1668 | 32 | 7 |
| `src/services/model/index.ts` | 0.96 | 2127 | 40 | 8 |
| `src/db/connection.ts` | 0.96 | 871 | 30 | 3 |
| `src/services/definition/lifecycle.ts` | 0.96 | 1086 | 31 | 7 |
| `src/routes/v1/definitions.ts` | 0.96 | 751 | 41 | 6 |
| `src/services/fork/index.ts` | 0.95 | 1065 | 35 | 7 |

## 3. Highest `bug_pressure_index` (top 10)

| file | bug | fixes | reverts | commits | reinforcement |
|---|---:|---:|---:|---:|---:|
| `src/controllers/definition-controller.ts` | 0.85 | 53 | 0 | 95 | 0.65 |
| `src/index.ts` | 0.85 | 43 | 0 | 73 | 0.94 |
| `src/db/repository/definition-repository.ts` | 0.84 | 51 | 0 | 87 | 0.91 |
| `src/routes/v1/definitions.ts` | 0.83 | 14 | 0 | 41 | 0.65 |
| `src/services/analytics/analytics-service.ts` | 0.83 | 43 | 0 | 64 | 0.94 |
| `src/db/connection.ts` | 0.83 | 17 | 0 | 30 | 0.99 |
| `src/services/fork/index.ts` | 0.82 | 16 | 0 | 35 | 0.85 |
| `test/unit/services/analytics/analytics-service.test.ts` | 0.82 | 22 | 0 | 32 | 0.00 |
| `src/routes/v1/schemas.ts` | 0.82 | 22 | 0 | 55 | 0.94 |
| `src/services/definition/lifecycle.ts` | 0.82 | 10 | 0 | 31 | 0.85 |

## 4. High load, low reinforcement — `load_index ≥ 0.9 ∧ reinforcement_index ≤ 0.1` (top 10 by load)

_(no nodes satisfy the predicate)_

## 5. Old, load-bearing, untouched — `neglect_index ≥ 0.9 ∧ load_index ≥ 0.1` (top 10 by neglect)

| file | neglect | load | age_d | last_touched_d | blame_age_d | fan_in |
|---|---:|---:|---:|---:|---:|---:|
| `scripts/run-seed.ts` | 0.99 | 0.12 | 226 | 226 | 226.31 | 0 |
| `src/utils/singleton.ts` | 0.99 | 0.86 | 226 | 226 | 226.31 | 18 |
| `test/unit/utils/singleton.test.ts` | 0.99 | 0.14 | 226 | 226 | 226.31 | 0 |
| `test/unit/config/index.test.ts` | 0.97 | 0.16 | 226 | 220 | 226.30 | 0 |
| `src/utils/async-handler.ts` | 0.96 | 0.85 | 226 | 196 | 226.31 | 16 |
| `src/db/migrations/001_create_definitions.ts` | 0.93 | 0.19 | 225 | 225 | 225.86 | 0 |
| `src/db/migrations/002_create_definition_versions.ts` | 0.93 | 0.17 | 225 | 225 | 225.86 | 0 |
| `src/db/migrations/003_create_definition_forks.ts` | 0.93 | 0.16 | 225 | 225 | 225.86 | 0 |
| `src/db/migrations/004_create_definition_references.ts` | 0.93 | 0.16 | 225 | 225 | 225.86 | 0 |
| `src/db/migrations/005_create_providers.ts` | 0.93 | 0.15 | 225 | 225 | 225.86 | 0 |

## Caveats

- none
