# typeorm, as this tool maps it — one window: `f5c6aa3bfe9c` → `ac41823b9e27`

**One pair of commits. Each event below is between them. Another pair of commits may read differently; this page does not compare them.**

The window: `f5c6aa3bfe9c` (2026-07-08T17:43:11-04:00) → `ac41823b9e27` (2026-09-02T12:07:18+03:00); the pair the gate perturbs (the gate is a check on this tool's map, not on the repository): the commit the gate was run at and the commit 25 timeline commits before it; chosen for the gate's test, not for this page. 25 commits in the window, the earliest at 2026-07-09T18:22:01+02:00 and the latest at 2026-09-02T12:07:18+03:00. 571 rooms are in both commits, 0 only in the later and 0 only in the earlier; 52 of the 571 rooms in both are in some commit's recorded changes (9% of rooms in both), 519 are in none.

## Crossings

4 crossings: one line per room and predicate term whose outcome differs between the two commits, among rooms in no commit's recorded changes that exited or entered a row the gate counts.

A row's name is this tool's label for a position on its map, not a description of the code.

| window | room | term | value, earlier → later | cutoff, earlier → later | later value against the earlier cutoff (arithmetic only, not a cause) | earlier value against the later cutoff (arithmetic only, not a cause) | rows (the map's labels, not descriptions of the code; counts only) |
|---|---|---|---|---|---|---|---|
| f5c6aa3b→ac41823b | src/driver/types/ReplicationMode.ts (in no commit's recorded changes in the window) | `reinforcement_index >= 0.5` | value 0 → 0.6098 | fixed at 0.5 | fixed threshold | fixed threshold | entered the map's row `scaffolding` · test-imported room (maintainability) (161 → 162 rooms: this room entered) |
| f5c6aa3b→ac41823b | src/metadata-args/EntityListenerMetadataArgs.ts (in no commit's recorded changes in the window) | `load_index >= p90` | value 0.7998 → 0.7994 | cutoff 0.7998 → 0.8049 | `0.7994 >= 0.7998`: no | `0.7998 >= 0.8049`: no | exited the map's row `foundation` · high-load node (maintainability, onboarding) (58 → 58 rooms: this room exited, 1 room in no commit's recorded changes in the window entered) |
| f5c6aa3b→ac41823b | src/util/ApplyValueTransformers.ts (in no commit's recorded changes in the window) | `centrality >= p90` | value 0.0022 → 0.0023 | cutoff 0.0023 → 0.0023 | `0.0023 >= 0.0023`: yes | `0.0022 >= 0.0023`: no | entered the map's row `hub` (maintainability) (58 → 59 rooms: this room entered); entered the map's row `corridor` (onboarding) (36 → 37 rooms: this room entered) |
| f5c6aa3b→ac41823b | src/util/DateUtils.ts (in no commit's recorded changes in the window) | `load_index >= p90` | value 0.7471 → 0.8141 | cutoff 0.7998 → 0.8049 | `0.8141 >= 0.7998`: yes | `0.7471 >= 0.8049`: no | entered the map's row `foundation` · high-load node (maintainability, onboarding) (58 → 58 rooms: this room entered, 1 room in no commit's recorded changes in the window exited) |

Each side's cutoff is computed over that commit's rooms that have a value, of 571 rooms earlier and 571 later, this room's included. The two comparisons are arithmetic on the four numbers beside them, as recorded; neither names a cause. The rows column counts the rooms that entered and exited each row; it does not say which of them, if any, bears on the line it sits in.

Only rooms that exited or entered a row are listed: a term that changed outcome while the room stayed in or out of its row is not on this page (the diff carries no evidence for it).

## Clock rows

A clock row's term is measured in days from the date of the snapshot, so its two sides are measured from two different dates. A clock row's rooms are counted, not named, and no values or cutoffs are printed for it. The two commits here are 55.48 days apart.

- **`lit_room` (maintainability)** — 74 → 58 rooms. Rooms in no commit's recorded changes in the window: 48 exited, 0 entered; edited rooms: 32 entered, 0 exited; not in the gate's count.

## Excluded rows (◌)

- **◌ `crack` · high edit-pressure node (maintainability)** — 58 → 58 rooms. Rooms in no commit's recorded changes in the window: 6 exited, 0 entered; edited rooms: 6 entered, 0 exited; excluded from the diagnosis; not in the gate's count. An excluded row's rooms are counted, not named, and no values or cutoffs are printed for it.
- **◌ `toothpick_wing` · unreinforced high-load node with high edit pressure (maintainability)** — 4 → 2 rooms. Rooms in no commit's recorded changes in the window: 2 exited, 0 entered; edited rooms: 0 entered, 0 exited; excluded from the diagnosis; not in the gate's count. An excluded row's rooms are counted, not named, and no values or cutoffs are printed for it.

## Bands

A band is a depth band of the map's geometry: a position in this tool's drawing, not a rating of a room.

- Under the age geometry, none of the 519 rooms in no commit's recorded changes in the window changed band.
- Under the layer geometry, none of the 519 rooms in no commit's recorded changes in the window changed band.

## What the gate counts on this window

What the gate counts on a window: for rooms in no commit's recorded changes, the rank and mixed rows they entered or exited, and the bands that differ. The clock rows and excluded rows above are not in its count. It is a check on this tool's map. It is not a reading of the code, of the repository, or of any room named on this page.

Counts of this one window (mapper spec §7 Q3). This page does not read whether another window of this repository counts the same. The same number of crossings is a different share of a different number of rooms, so these counts do not rank repositories. Whether the gate judged this window, the limit it judges against and its own word for it are in each diff's `budget` block and are not on this page.

- rows (the same under each geometry; rows do not depend on it) — 4 of the 519 rooms in no commit's recorded changes in the window, 4 crossings. In the gate's unit: 235 of those rooms hold, in one commit or the other, 427 `(profile, feature, room)` assignments on rank and mixed rows; 7 of those 427 assignments are in one commit and not the other.
- bands, age geometry — 0 of the 519 rooms in no commit's recorded changes in the window.
- bands, layer geometry — 0 of the 519 rooms in no commit's recorded changes in the window.

## What this page does not report

Marks that are neither diagnostic nor excluded (0 in the earlier commit, 0 in the later); what differs for edited rooms beyond the counts beside each row; which rooms entered or exited a clock row or an excluded row, and their values; a term that changed outcome without the room exiting or entering its row; any pair of commits but this one.

## Provenance

`typeorm.age.diff.json` (age: skeleton `35dc6492c019…` → `e21ed35b9b2d…`); `typeorm.layer.diff.json` (layer: skeleton `b8414f31cd8b…` → `15f55b0222fa…`). Ruleset maintainability 0.3.4 + onboarding 0.3.1, mapper 0.11.1, substrate config `298696064105`, gate `942d86e90cfe`. Window page 0.5.0, facts `8c42257393c4…`.
