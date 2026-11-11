# uluops-registry-api — one window: `368c01673360` → `e947c5b67542`

**One pair of commits. Each event below is between them. Another pair of commits reads differently.**

The window: `368c01673360` (2026-08-22T09:12:27-10:00) → `e947c5b67542` (2026-09-13T12:47:53-10:00); the pair the gate perturbs: the commit the gate was run at and the commit 25 timeline commits before it; chosen for the gate's test, not for this page. 25 commits in the window, the earliest at 2026-08-22T13:30:09-10:00 and the latest at 2026-09-13T12:47:53-10:00. 206 rooms are in both commits, 0 only in the later and 0 only in the earlier; 38 of the 206 rooms in both are in some commit's recorded changes (18% of rooms in both), 168 are in none.

## Crossings

1 crossing: one line per room and predicate term whose outcome differs between the two commits, among rooms in no commit's recorded changes that exited or entered a row the gate's reading counts.

| window | room | term | value, earlier → later | cutoff, earlier → later | later value against the earlier cutoff (arithmetic only) | earlier value against the later cutoff (arithmetic only) | rows (counts only) |
|---|---|---|---|---|---|---|---|
| 368c0167→e947c5b6 | src/schemas/validation/types.ts (in no commit's recorded changes in the window) | `reinforcement_index >= 0.5` | value 0 → 0.6504 | fixed at 0.5 | fixed threshold | fixed threshold | entered scaffolding (maintainability) (130 → 133 rooms: 2 edited rooms entered) |

Each side's cutoff is computed over that commit's rooms that have a value, of 206 rooms earlier and 206 later, this room's included. The two comparisons are arithmetic on the four numbers beside them; neither names a cause. The rows column counts the rooms that entered and exited each row; it does not say which of them, if any, bears on the line it sits in.

Only rooms that exited or entered a row are listed: a term that changed outcome while the room stayed in or out of its row is not on this page (the diff carries no evidence for it).

## Clock rows

A clock row's term is measured from the date of the snapshot, so every room's value on it differs between two commits made on different dates.

- **lit_room (maintainability)** — 36 → 21 rooms. Rooms in no commit's recorded changes in the window: 25 exited (scripts/backfill-is-latest.ts; scripts/backfill-missing-risk-profiles.ts; scripts/backfill-risk-scalars.ts; and 22 more), 0 entered (none); edited rooms: 15 entered, 5 exited; not counted in the gate's reading.

Their crossings, not counted in the gate's reading:

| window | room | term | value, earlier → later | cutoff, earlier → later | later value against the earlier cutoff (arithmetic only) | earlier value against the later cutoff (arithmetic only) | rows (counts only) |
|---|---|---|---|---|---|---|---|
| 368c0167→e947c5b6 | scripts/backfill-is-latest.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 6.0092 → 28.1588 days | cutoff 6.0092 → 20.126 days | `28.1588 <= 6.0092`: no | `6.0092 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | scripts/backfill-missing-risk-profiles.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 6.0092 → 28.1588 days | cutoff 6.0092 → 20.126 days | `28.1588 <= 6.0092`: no | `6.0092 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | scripts/backfill-risk-scalars.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 6.0092 → 28.1588 days | cutoff 6.0092 → 20.126 days | `28.1588 <= 6.0092`: no | `6.0092 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | scripts/backfill-stale-risk-profiles.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 2.978 → 25.1276 days | cutoff 6.0092 → 20.126 days | `25.1276 <= 6.0092`: no | `2.978 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | scripts/calibration-gate.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 6.0092 → 28.1588 days | cutoff 6.0092 → 20.126 days | `28.1588 <= 6.0092`: no | `6.0092 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | scripts/check-optionalauth-nonget.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 0.9013 → 23.0509 days | cutoff 6.0092 → 20.126 days | `23.0509 <= 6.0092`: no | `0.9013 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | scripts/cron/deep-analysis.sh (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 6.0092 → 28.1588 days | cutoff 6.0092 → 20.126 days | `28.1588 <= 6.0092`: no | `6.0092 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | scripts/cron/executions-retention.sh (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 6.0092 → 28.1588 days | cutoff 6.0092 → 20.126 days | `28.1588 <= 6.0092`: no | `6.0092 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | scripts/cron/models-sync.sh (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 6.0092 → 28.1588 days | cutoff 6.0092 → 20.126 days | `28.1588 <= 6.0092`: no | `6.0092 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | scripts/lineage-consistency-check.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 0.8556 → 23.0052 days | cutoff 6.0092 → 20.126 days | `23.0052 <= 6.0092`: no | `0.8556 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | scripts/list-pre-a1-versions.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 6.0092 → 28.1588 days | cutoff 6.0092 → 20.126 days | `28.1588 <= 6.0092`: no | `6.0092 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | scripts/requeue-deep-stale.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 2.9748 → 25.1244 days | cutoff 6.0092 → 20.126 days | `25.1244 <= 6.0092`: no | `2.9748 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | src/config/index.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 6.0092 → 28.1588 days | cutoff 6.0092 → 20.126 days | `28.1588 <= 6.0092`: no | `6.0092 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | src/middleware/index.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 6.0092 → 28.1588 days | cutoff 6.0092 → 20.126 days | `28.1588 <= 6.0092`: no | `6.0092 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | src/middleware/rate-limit.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 6.0092 → 28.1588 days | cutoff 6.0092 → 20.126 days | `28.1588 <= 6.0092`: no | `6.0092 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | src/routes/v1/analytics.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 5.9664 → 28.116 days | cutoff 6.0092 → 20.126 days | `28.116 <= 6.0092`: no | `5.9664 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | src/schemas/index.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 6.0092 → 28.1588 days | cutoff 6.0092 → 20.126 days | `28.1588 <= 6.0092`: no | `6.0092 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | src/services/definition/mutations.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 0.8167 → 22.9663 days | cutoff 6.0092 → 20.126 days | `22.9663 <= 6.0092`: no | `0.8167 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | src/services/safety/analyzer-version.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 2.978 → 25.1276 days | cutoff 6.0092 → 20.126 days | `25.1276 <= 6.0092`: no | `2.978 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | src/services/safety/deep-analysis-worker.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 2.978 → 25.1276 days | cutoff 6.0092 → 20.126 days | `25.1276 <= 6.0092`: no | `2.978 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | src/services/safety/definition-scanner.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 2.978 → 25.1276 days | cutoff 6.0092 → 20.126 days | `25.1276 <= 6.0092`: no | `2.978 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | src/services/safety/risk-calculator.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 2.978 → 25.1276 days | cutoff 6.0092 → 20.126 days | `25.1276 <= 6.0092`: no | `2.978 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | src/services/safety/types.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 3.7069 → 25.8565 days | cutoff 6.0092 → 20.126 days | `25.8565 <= 6.0092`: no | `3.7069 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | src/services/validation/reference-validator.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 6.0092 → 28.1588 days | cutoff 6.0092 → 20.126 days | `28.1588 <= 6.0092`: no | `6.0092 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |
| 368c0167→e947c5b6 | src/utils/errors.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 0.8167 → 22.9663 days | cutoff 6.0092 → 20.126 days | `22.9663 <= 6.0092`: no | `0.8167 <= 20.126`: yes | exited lit_room (maintainability) (36 → 21 rooms: 15 edited rooms entered, 5 edited rooms exited) |

## Excluded rows (◌)

- **◌ crack (maintainability)** — 21 → 21 rooms. Rooms in no commit's recorded changes in the window: 6 exited, 0 entered; edited rooms: 6 entered, 0 exited; excluded from the diagnosis; not counted in the gate's reading. An excluded row's rooms are counted, not named, and no values or cutoffs are printed for it.

## Bands

- Under the age geometry, 1 of the 168 rooms in no commit's recorded changes in the window changed band: 1 with a different raw value (scripts/list-pre-a1-versions.ts: band 4 → 3, raw value 0.1992 → 0.2022).
- Under the layer geometry, none of the 168 rooms in no commit's recorded changes in the window changed band.

## The gate's budget reading on this window

What the gate's budget bounds: how far this tool's map differs between two commits for rooms that are in no commit's recorded changes. It is a check on the map. It is not a reading of the code, of the repository, or of any room named on this page.

- features (the same under each geometry: rows do not depend on it) — 1 of the 168 rooms in no commit's recorded changes in the window, 1 crossing; in the gate's unit, 1 of 215 `(profile, feature, room)` assignments (11 or more of 215 assignments is over 0.05 by the gate's rule).
- bands, age geometry — 1 of 168 rooms in no commit's recorded changes in the window (9 or more of 168 rooms is over 0.05 by the gate's rule).
- bands, layer geometry — 0 of 168 rooms in no commit's recorded changes in the window (9 or more of 168 rooms is over 0.05 by the gate's rule).
- the gate's token, age geometry — `within_budget`.
- the gate's token, layer geometry — `within_budget`.

A reading of this one window (mapper spec §7 Q3). This page does not read whether another window of this repository reads the same. The same number of crossings reads differently on a different number of rooms, so the token does not rank repositories.

## What this page does not report

Marks that are neither diagnostic nor excluded (0 in the earlier commit, 0 in the later); what differs for edited rooms beyond the counts beside each row; a term that changed outcome without the room exiting or entering its row; any pair of commits but this one.

## Provenance

`registry.age.diff.json` (age: skeleton `fe26fad6aa94…` → `589718518a35…`); `registry.layer.diff.json` (layer: skeleton `a07687dbe79e…` → `f3a67ba39b13…`). Ruleset maintainability 0.3.4 + onboarding 0.3.1, mapper 0.11.1, substrate config `298696064105`, gate `942d86e90cfe`. Window page 0.2.0, facts `e4f80f98f6f0…`.
