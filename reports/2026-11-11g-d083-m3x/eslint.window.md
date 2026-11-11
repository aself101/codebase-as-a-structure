# eslint, as this tool maps it — one window: `5c8c2417b9ff` → `3f20a57c6293`

**One pair of commits. Each event below is between them. Another pair of commits may read differently; this page does not compare them.**

The window: `5c8c2417b9ff` (2026-08-24T18:17:49+00:00) → `3f20a57c6293` (2026-09-04T14:29:08+00:00); the pair the gate perturbs (the gate is a check on this tool's map, not on the repository): the commit the gate was run at and the commit 25 timeline commits before it; chosen for the gate's test, not for this page. 25 commits in the window, the earliest at 2026-08-24T18:17:49+00:00 and the latest at 2026-09-04T14:29:08+00:00. 461 rooms are in both commits, 1 only in the later and 0 only in the earlier; 16 of the 461 rooms in both are in some commit's recorded changes (3% of rooms in both), 445 are in none.

## Crossings

2 crossings: one line per room and predicate term whose outcome differs between the two commits, among rooms in no commit's recorded changes that exited or entered a row the gate counts.

A row's name is this tool's label for a position on its map, not a description of the code.

| window | room | term | value, earlier → later | cutoff, earlier → later | later value against the earlier cutoff (arithmetic only, not a cause) | earlier value against the later cutoff (arithmetic only, not a cause) | rows (the map's labels, not descriptions of the code; counts only) |
|---|---|---|---|---|---|---|---|
| 5c8c2417→3f20a57c | lib/cli-engine/hash.js (in no commit's recorded changes in the window) | `load_index >= p90` | value 0.7817 → 0.7889 | cutoff 0.7851 → 0.78847 | `0.7889 >= 0.7851`: yes | `0.7817 >= 0.78847`: no | entered the map's row `foundation` · high-load node (maintainability, onboarding) (47 → 47 rooms: this room entered, 1 room in no commit's recorded changes in the window exited) |
| 5c8c2417→3f20a57c | packages/js/src/index.js (in no commit's recorded changes in the window) | `load_index >= p90` | value 0.7851 → 0.7846 | cutoff 0.7851 → 0.78847 | `0.7846 >= 0.7851`: no | `0.7851 >= 0.78847`: no | exited the map's row `foundation` · high-load node (maintainability, onboarding) (47 → 47 rooms: this room exited, 1 room in no commit's recorded changes in the window entered) |

Each side's cutoff is computed over that commit's rooms that have a value, of 461 rooms earlier and 462 later, this room's included. The two comparisons are arithmetic on the four numbers beside them, as recorded; neither names a cause. The rows column counts the rooms that entered and exited each row; it does not say which of them, if any, bears on the line it sits in.

Only rooms that exited or entered a row are listed: a term that changed outcome while the room stayed in or out of its row is not on this page (the diff carries no evidence for it).

## Clock rows

A clock row's term is measured in days from the date of the snapshot, so its two sides are measured from two different dates. A clock row's rooms are counted, not named, and no values or cutoffs are printed for it. The two commits here are 10.84 days apart.

- **`lit_room` (maintainability)** — 50 → 47 rooms. Rooms in no commit's recorded changes in the window: 15 exited, 0 entered; edited rooms: 11 entered, 0 exited; rooms only in one commit: 1 entered, 0 exited; not in the gate's count.

## Excluded rows (◌)

- **◌ `crack` · high edit-pressure node (maintainability)** — 47 → 47 rooms. Rooms in no commit's recorded changes in the window: 1 exited, 0 entered; edited rooms: 1 entered, 0 exited; excluded from the diagnosis; not in the gate's count. An excluded row's rooms are counted, not named, and no values or cutoffs are printed for it.

## Bands

A band is a depth band of the map's geometry: a position in this tool's drawing, not a rating of a room.

- Under the age geometry, 1 of the 445 rooms in no commit's recorded changes in the window changed band: 1 with a different raw value (lib/rules/no-useless-concat.js: band 2 → 1, raw value 0.5996 → 0.6004).
- Under the layer geometry, none of the 445 rooms in no commit's recorded changes in the window changed band.

## What the gate counts on this window

What the gate counts on a window: for rooms in no commit's recorded changes, the rank and mixed rows they entered or exited, and the bands that differ. The clock rows and excluded rows above are not in its count. It is a check on this tool's map. It is not a reading of the code, of the repository, or of any room named on this page.

Counts of this one window (mapper spec §7 Q3). This page does not read whether another window of this repository counts the same. The same number of crossings is a different share of a different number of rooms, so these counts do not rank repositories. Whether the gate judged this window, the limit it judges against and its own word for it are in each diff's `budget` block and are not on this page.

- rows (the same under each geometry; rows do not depend on it) — 2 of the 445 rooms in no commit's recorded changes in the window, 2 crossings. In the gate's unit: 426 of those rooms hold, in one commit or the other, 748 `(profile, feature, room)` assignments on rank and mixed rows; 4 of those 748 assignments are in one commit and not the other.
- bands, age geometry — 1 of the 445 rooms in no commit's recorded changes in the window.
- bands, layer geometry — 0 of the 445 rooms in no commit's recorded changes in the window.

## What this page does not report

Marks that are neither diagnostic nor excluded (0 in the earlier commit, 0 in the later); what differs for edited rooms beyond the counts beside each row; which rooms entered or exited a clock row or an excluded row, and their values; a term that changed outcome without the room exiting or entering its row; any pair of commits but this one.

## Provenance

`eslint.age.diff.json` (age: skeleton `ab915a9bcd60…` → `dd889218caf9…`); `eslint.layer.diff.json` (layer: skeleton `da8d39a9600c…` → `49b05257c552…`). Ruleset maintainability 0.3.4 + onboarding 0.3.1, mapper 0.11.1, substrate config `298696064105`, gate `942d86e90cfe`. Window page 0.5.0, facts `303c4d3d4fac…`.
