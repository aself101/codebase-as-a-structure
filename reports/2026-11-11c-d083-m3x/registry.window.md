# uluops-registry-api — one window: `368c01673360` → `e947c5b67542`

**One pair of commits. Each event below is between them. Another pair of commits reads differently.**

The window: `368c01673360` (2026-08-22T09:12:27-10:00) → `e947c5b67542` (2026-09-13T12:47:53-10:00); the pair the gate perturbs: HEAD and the commit 25 timeline commits before it; chosen for the gate's test, not for this page. 25 commits in the window, the earliest at 2026-08-22T13:30:09-10:00 and the latest at 2026-09-13T12:47:53-10:00. 206 rooms are in both commits, 0 only in the later and 0 only in the earlier; 38 of the 206 rooms in both are in some commit's recorded changes (18% of rooms in both), 168 are in none.

## Crossings

1 crossing: one line per room and predicate term whose outcome differs between the two commits, among rooms in no commit's recorded changes, on rows the gate's reading counts.

| window | room | term | value earlier → later | cutoff earlier → later | later value against the earlier cutoff | earlier value against the later cutoff | rows |
|---|---|---|---|---|---|---|---|
| 368c0167→e947c5b6 | src/schemas/validation/types.ts (in no commit's recorded changes in the window) | `reinforcement_index >= 0.5` | 0 → 0.6504 | fixed at 0.5 | fixed threshold | fixed threshold | entered scaffolding (maintainability) (130 → 133 rooms: 2 edited rooms entered) |

Each side's cutoff is computed over that commit's rooms that have a value, of 206 rooms earlier and 206 later, this room's included. The two comparisons are arithmetic on the four numbers beside them; neither names a cause.

## Clock rows

- **lit_room (maintainability)** — 36 → 21 rooms; 25 rooms in no commit's recorded changes in the window left (scripts/backfill-is-latest.ts; scripts/backfill-missing-risk-profiles.ts; scripts/backfill-risk-scalars.ts; and 22 more), 0 entered (none); not counted in the gate's reading.

Their crossings, not counted in the gate's reading:

| window | room | term | value earlier → later | cutoff earlier → later | later value against the earlier cutoff | earlier value against the later cutoff | rows |
|---|---|---|---|---|---|---|---|
| 368c0167→e947c5b6 | scripts/backfill-is-latest.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 6.0092 → 28.1588 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | scripts/backfill-missing-risk-profiles.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 6.0092 → 28.1588 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | scripts/backfill-risk-scalars.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 6.0092 → 28.1588 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | scripts/backfill-stale-risk-profiles.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 2.978 → 25.1276 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | scripts/calibration-gate.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 6.0092 → 28.1588 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | scripts/check-optionalauth-nonget.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 0.9013 → 23.0509 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | scripts/cron/deep-analysis.sh (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 6.0092 → 28.1588 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | scripts/cron/executions-retention.sh (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 6.0092 → 28.1588 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | scripts/cron/models-sync.sh (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 6.0092 → 28.1588 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | scripts/lineage-consistency-check.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 0.8556 → 23.0052 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | scripts/list-pre-a1-versions.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 6.0092 → 28.1588 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | scripts/requeue-deep-stale.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 2.9748 → 25.1244 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | src/config/index.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 6.0092 → 28.1588 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | src/middleware/index.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 6.0092 → 28.1588 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | src/middleware/rate-limit.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 6.0092 → 28.1588 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | src/routes/v1/analytics.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 5.9664 → 28.116 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | src/schemas/index.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 6.0092 → 28.1588 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | src/services/definition/mutations.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 0.8167 → 22.9663 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | src/services/safety/analyzer-version.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 2.978 → 25.1276 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | src/services/safety/deep-analysis-worker.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 2.978 → 25.1276 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | src/services/safety/definition-scanner.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 2.978 → 25.1276 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | src/services/safety/risk-calculator.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 2.978 → 25.1276 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | src/services/safety/types.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 3.7069 → 25.8565 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | src/services/validation/reference-validator.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 6.0092 → 28.1588 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |
| 368c0167→e947c5b6 | src/utils/errors.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 0.8167 → 22.9663 | 6.0092 → 20.126 | fails | passes | left lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms left) |

## Excluded rows (◌)

- **◌ crack (maintainability)** — 21 → 21 rooms; 6 rooms in no commit's recorded changes in the window left, 0 entered; excluded from the diagnosis; not counted in the gate's reading. An excluded row's rooms are counted, not named, and no values or cutoffs are printed for it.

## Bands

- Under the age geometry, 1 of the 168 rooms in no commit's recorded changes in the window changed band: 1 with a different raw value (scripts/list-pre-a1-versions.ts).
- Under the layer geometry, none of the 168 rooms in no commit's recorded changes in the window changed band.

## The gate's budget reading on this window

- age geometry — 1 room, 1 crossing (1 of 215 `(profile, feature, room)` assignments; 11 or more of 215 assignments is over 0.05 by the gate's rule); bands 1 of 168 rooms (9 or more of 168 rooms is over 0.05 by the gate's rule). The gate's token: `within_budget`.
- layer geometry — 1 room, 1 crossing (1 of 215 `(profile, feature, room)` assignments; 11 or more of 215 assignments is over 0.05 by the gate's rule); bands 0 of 168 rooms (9 or more of 168 rooms is over 0.05 by the gate's rule). The gate's token: `within_budget`.

A reading of this one window (mapper spec §7 Q3). This page does not read whether it is usual for this repository. The same number of crossings reads differently on a different number of rooms, so the token does not rank repositories.

## What this page does not report

Marks that are neither diagnostic nor excluded (0 in the earlier commit, 0 in the later); what differs for edited rooms beyond the counts in the rows column; any pair of commits but this one.

## Provenance

`registry.age.diff.json` (age: skeleton `fe26fad6aa94…` → `589718518a35…`); `registry.layer.diff.json` (layer: skeleton `a07687dbe79e…` → `f3a67ba39b13…`). Ruleset maintainability 0.3.4 + onboarding 0.3.1, mapper 0.11.1, substrate config `298696064105`, gate `942d86e90cfe`. Window page 0.1.0, facts `92d226e89099…`.
