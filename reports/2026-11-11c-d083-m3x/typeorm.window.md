# typeorm — one window: `f5c6aa3bfe9c` → `ac41823b9e27`

**One pair of commits. Each event below is between them. Another pair of commits reads differently.**

The window: `f5c6aa3bfe9c` (2026-07-08T17:43:11-04:00) → `ac41823b9e27` (2026-09-02T12:07:18+03:00); the pair the gate perturbs: HEAD and the commit 25 timeline commits before it; chosen for the gate's test, not for this page. 25 commits in the window, the earliest at 2026-07-09T18:22:01+02:00 and the latest at 2026-09-02T12:07:18+03:00. 571 rooms are in both commits, 0 only in the later and 0 only in the earlier; 52 of the 571 rooms in both are in some commit's recorded changes (9% of rooms in both), 519 are in none.

## Crossings

4 crossings: one line per room and predicate term whose outcome differs between the two commits, among rooms in no commit's recorded changes, on rows the gate's reading counts.

| window | room | term | value earlier → later | cutoff earlier → later | later value against the earlier cutoff | earlier value against the later cutoff | rows |
|---|---|---|---|---|---|---|---|
| f5c6aa3b→ac41823b | src/driver/types/ReplicationMode.ts (in no commit's recorded changes in the window) | `reinforcement_index >= 0.5` | 0 → 0.6098 | fixed at 0.5 | fixed threshold | fixed threshold | entered scaffolding (maintainability) (161 → 162 rooms) |
| f5c6aa3b→ac41823b | src/metadata-args/EntityListenerMetadataArgs.ts (in no commit's recorded changes in the window) | `load_index >= p90` | 0.7998 → 0.7994 | 0.7998 → 0.8049 | fails | fails | left foundation (maintainability, onboarding) (58 → 58 rooms) |
| f5c6aa3b→ac41823b | src/util/ApplyValueTransformers.ts (in no commit's recorded changes in the window) | `centrality >= p90` | 0.0022 → 0.0023 | 0.0023 → 0.0023 | passes | fails | entered hub (maintainability) (58 → 59 rooms); entered corridor (onboarding) (36 → 37 rooms) |
| f5c6aa3b→ac41823b | src/util/DateUtils.ts (in no commit's recorded changes in the window) | `load_index >= p90` | 0.7471 → 0.8141 | 0.7998 → 0.8049 | passes | fails | entered foundation (maintainability, onboarding) (58 → 58 rooms) |

Each side's cutoff is computed over that commit's rooms that have a value, of 571 rooms earlier and 571 later, this room's included. The two comparisons are arithmetic on the four numbers beside them; neither names a cause.

## Clock rows

- **lit_room (maintainability)** — 74 → 58 rooms; 48 rooms in no commit's recorded changes in the window left (gulpfile.ts; packages/codemod/src/transforms/ast-helpers.ts; packages/codemod/src/transforms/v1/column-readonly.ts; and 45 more), 0 entered (none); not counted in the gate's reading.

Their crossings, not counted in the gate's reading:

| window | room | term | value earlier → later | cutoff earlier → later | later value against the earlier cutoff | earlier value against the later cutoff | rows |
|---|---|---|---|---|---|---|---|
| f5c6aa3b→ac41823b | gulpfile.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 2.5082 → 57.9833 | 76.5585 → 57.5427 | passes | passes | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | packages/codemod/src/transforms/ast-helpers.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 74.9295 → 130.405 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | packages/codemod/src/transforms/v1/column-readonly.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 74.9295 → 130.405 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | packages/codemod/src/transforms/v1/column-width-zerofill.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 74.9295 → 130.405 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | packages/codemod/src/transforms/v1/connection-to-datasource.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5025 → 131.978 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | packages/codemod/src/transforms/v1/datasource-sqlite-options.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 74.9295 → 130.405 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | packages/legacy-naming-strategies/src/index.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 64.6508 → 120.126 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | packages/legacy-naming-strategies/src/legacy-oracle-naming-strategy.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 64.6508 → 120.126 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | packages/legacy-naming-strategies/src/naming-strategy-v03.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 64.6508 → 120.126 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/driver/aurora-mysql/AuroraMysqlQueryRunner.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5585 → 132.034 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/driver/aurora-postgres/AuroraPostgresQueryRunner.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5585 → 132.034 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/driver/capacitor/CapacitorQueryRunner.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5585 → 132.034 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/driver/cordova/CordovaQueryRunner.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5585 → 132.034 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/driver/expo/ExpoQueryRunner.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5585 → 132.034 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/driver/mongodb/typings.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 20.2385 → 75.7136 | 76.5585 → 57.5427 | passes | passes | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/driver/mysql/MysqlQueryRunner.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 75.3291 → 130.804 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/driver/nativescript/NativescriptQueryRunner.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5585 → 132.034 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/driver/react-native/ReactNativeQueryRunner.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5585 → 132.034 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/driver/sap/SapQueryRunner.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 75.3291 → 130.804 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/driver/spanner/SpannerQueryRunner.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5585 → 132.034 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/driver/sqlserver/SqlServerQueryRunner.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 51.1611 → 106.636 | 76.5585 → 57.5427 | fails | passes | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/driver/types/InvalidFindOptionsWhereBehavior.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 26.1697 → 81.6448 | 76.5585 → 57.5427 | fails | passes | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/error/AlreadyHasActiveConnectionError.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 28.1232 → 83.5983 | 76.5585 → 57.5427 | fails | passes | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/error/NamedPlaceholdersNotSupportedError.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5585 → 132.034 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/error/QueryFailedError.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5585 → 132.034 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/error/index.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5585 → 132.034 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/find-options/operator/JsonContains.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 54.4752 → 109.95 | 76.5585 → 57.5427 | fails | passes | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/logger/DebugLogger.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5585 → 132.034 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/metadata-builder/ClosureJunctionEntityMetadataBuilder.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 14.0983 → 69.5734 | 76.5585 → 57.5427 | passes | passes | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/metadata/types/ClosureTreeOptions.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 14.0983 → 69.5734 | 76.5585 → 57.5427 | passes | passes | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/naming-strategy/DefaultNamingStrategy.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 64.6508 → 120.126 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/naming-strategy/NamingStrategyInterface.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 64.6508 → 120.126 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/persistence/EntityPersistExecutor.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 64.5648 → 120.04 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/persistence/SubjectChangedColumnsComputer.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 59.3295 → 114.805 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/persistence/SubjectDatabaseEntityLoader.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 64.5648 → 120.04 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/persistence/SubjectExecutor.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 35.1767 → 90.6518 | 76.5585 → 57.5427 | fails | passes | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/query-builder/JoinAttribute.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 20.1615 → 75.6366 | 76.5585 → 57.5427 | passes | passes | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/query-builder/QueryExpressionMap.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 54.498 → 109.973 | 76.5585 → 57.5427 | fails | passes | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/query-builder/SoftDeleteQueryBuilder.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 58.1279 → 113.603 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/query-builder/relation-id/RelationIdLoader.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 64.5648 → 120.04 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/query-builder/transformer/DocumentToEntityTransformer.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 20.2385 → 75.7136 | 76.5585 → 57.5427 | passes | passes | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/query-runner/BaseQueryRunner.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 75.3291 → 130.804 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/query-runner/QueryRunner.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5585 → 132.034 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/repository/TreeRepository.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 14.0983 → 69.5734 | 76.5585 → 57.5427 | passes | passes | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/subscriber/Broadcaster.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5585 → 132.034 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/subscriber/event/QueryEvent.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 76.5585 → 132.034 | 76.5585 → 57.5427 | fails | fails | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/util/RandomGenerator.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 2.5082 → 57.9833 | 76.5585 → 57.5427 | passes | passes | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |
| f5c6aa3b→ac41823b | src/util/StringUtils.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 2.5082 → 57.9833 | 76.5585 → 57.5427 | passes | passes | left lit_room (maintainability) (74 → 58 rooms: 32 edited rooms entered) |

## Excluded rows (◌)

- **◌ crack (maintainability)** — 58 → 58 rooms; 6 rooms in no commit's recorded changes in the window left, 0 entered; excluded from the diagnosis; not counted in the gate's reading. An excluded row's rooms are counted, not named, and no values or cutoffs are printed for it.
- **◌ toothpick_wing (maintainability)** — 4 → 2 rooms; 2 rooms in no commit's recorded changes in the window left, 0 entered; excluded from the diagnosis; not counted in the gate's reading. An excluded row's rooms are counted, not named, and no values or cutoffs are printed for it.

## Bands

- Under the age geometry, none of the 519 rooms in no commit's recorded changes in the window changed band.
- Under the layer geometry, none of the 519 rooms in no commit's recorded changes in the window changed band.

## The gate's budget reading on this window

- age geometry — 4 rooms, 4 crossings (7 of 427 `(profile, feature, room)` assignments; 22 or more of 427 assignments is over 0.05 by the gate's rule); bands 0 of 519 rooms (26 or more of 519 rooms is over 0.05 by the gate's rule). The gate's token: `within_budget`.
- layer geometry — 4 rooms, 4 crossings (7 of 427 `(profile, feature, room)` assignments; 22 or more of 427 assignments is over 0.05 by the gate's rule); bands 0 of 519 rooms (26 or more of 519 rooms is over 0.05 by the gate's rule). The gate's token: `within_budget`.

A reading of this one window (mapper spec §7 Q3). This page does not read whether it is usual for this repository. The same number of crossings reads differently on a different number of rooms, so the token does not rank repositories.

## What this page does not report

Marks that are neither diagnostic nor excluded (0 in the earlier commit, 0 in the later); what differs for edited rooms beyond the counts in the rows column; any pair of commits but this one.

## Provenance

`typeorm.age.diff.json` (age: skeleton `35dc6492c019…` → `e21ed35b9b2d…`); `typeorm.layer.diff.json` (layer: skeleton `b8414f31cd8b…` → `15f55b0222fa…`). Ruleset maintainability 0.3.4 + onboarding 0.3.1, mapper 0.11.1, substrate config `298696064105`, gate `942d86e90cfe`. Window page 0.1.0, facts `2a6a93e51aaf…`.
