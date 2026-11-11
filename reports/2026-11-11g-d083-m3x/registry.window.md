# uluops-registry-api, as this tool maps it — one window: `368c01673360` → `e947c5b67542`

**One pair of commits. Each event below is between them. Another pair of commits may read differently; this page does not compare them.**

The window: `368c01673360` (2026-08-22T09:12:27-10:00) → `e947c5b67542` (2026-09-13T12:47:53-10:00); the pair the gate perturbs (the gate is a check on this tool's map, not on the repository): the commit the gate was run at and the commit 25 timeline commits before it; chosen for the gate's test, not for this page. 25 commits in the window, the earliest at 2026-08-22T13:30:09-10:00 and the latest at 2026-09-13T12:47:53-10:00. 206 rooms are in both commits, 0 only in the later and 0 only in the earlier; 38 of the 206 rooms in both are in some commit's recorded changes (18% of rooms in both), 168 are in none.

## Crossings

1 crossing: one line per room and predicate term whose outcome differs between the two commits, among rooms in no commit's recorded changes that exited or entered a row the gate counts.

A row's name is this tool's label for a position on its map, not a description of the code.

| window | room | term | value, earlier → later | cutoff, earlier → later | later value against the earlier cutoff (arithmetic only, not a cause) | earlier value against the later cutoff (arithmetic only, not a cause) | rows (the map's labels, not descriptions of the code; counts only) |
|---|---|---|---|---|---|---|---|
| 368c0167→e947c5b6 | src/schemas/validation/types.ts (in no commit's recorded changes in the window) | `reinforcement_index >= 0.5` | value 0 → 0.6504 | fixed at 0.5 | fixed threshold | fixed threshold | entered the map's row `scaffolding` · test-imported room (maintainability) (130 → 133 rooms: this room entered, 2 edited rooms entered) |

Each side's cutoff is computed over that commit's rooms that have a value, of 206 rooms earlier and 206 later, this room's included. The two comparisons are arithmetic on the four numbers beside them, as recorded; neither names a cause. The rows column counts the rooms that entered and exited each row; it does not say which of them, if any, bears on the line it sits in.

Only rooms that exited or entered a row are listed: a term that changed outcome while the room stayed in or out of its row is not on this page (the diff carries no evidence for it).

## Clock rows

A clock row's term is measured in days from the date of the snapshot, so its two sides are measured from two different dates. A clock row's rooms are counted, not named, and no values or cutoffs are printed for it. The two commits here are 22.15 days apart.

- **`lit_room` (maintainability)** — 36 → 21 rooms. Rooms in no commit's recorded changes in the window: 25 exited, 0 entered; edited rooms: 15 entered, 5 exited; not in the gate's count.

## Excluded rows (◌)

- **◌ `crack` · high edit-pressure node (maintainability)** — 21 → 21 rooms. Rooms in no commit's recorded changes in the window: 6 exited, 0 entered; edited rooms: 6 entered, 0 exited; excluded from the diagnosis; not in the gate's count. An excluded row's rooms are counted, not named, and no values or cutoffs are printed for it.

## Bands

A band is a depth band of the map's geometry: a position in this tool's drawing, not a rating of a room.

- Under the age geometry, 1 of the 168 rooms in no commit's recorded changes in the window changed band: 1 with a different raw value (scripts/list-pre-a1-versions.ts: band 4 → 3, raw value 0.1992 → 0.2022).
- Under the layer geometry, none of the 168 rooms in no commit's recorded changes in the window changed band.

## What the gate counts on this window

What the gate counts on a window: for rooms in no commit's recorded changes, the rank and mixed rows they entered or exited, and the bands that differ. The clock rows and excluded rows above are not in its count. It is a check on this tool's map. It is not a reading of the code, of the repository, or of any room named on this page.

Counts of this one window (mapper spec §7 Q3). This page does not read whether another window of this repository counts the same. The same number of crossings is a different share of a different number of rooms, so these counts do not rank repositories. Whether the gate judged this window, the limit it judges against and its own word for it are in each diff's `budget` block and are not on this page.

- rows (the same under each geometry; rows do not depend on it) — 1 of the 168 rooms in no commit's recorded changes in the window, 1 crossing. In the gate's unit: 125 of those rooms hold, in one commit or the other, 215 `(profile, feature, room)` assignments on rank and mixed rows; 1 of those 215 assignments are in one commit and not the other.
- bands, age geometry — 1 of the 168 rooms in no commit's recorded changes in the window.
- bands, layer geometry — 0 of the 168 rooms in no commit's recorded changes in the window.

## What this page does not report

Marks that are neither diagnostic nor excluded (0 in the earlier commit, 0 in the later); what differs for edited rooms beyond the counts beside each row; which rooms entered or exited a clock row or an excluded row, and their values; a term that changed outcome without the room exiting or entering its row; any pair of commits but this one.

## Provenance

`registry.age.diff.json` (age: skeleton `fe26fad6aa94…` → `589718518a35…`); `registry.layer.diff.json` (layer: skeleton `a07687dbe79e…` → `f3a67ba39b13…`). Ruleset maintainability 0.3.4 + onboarding 0.3.1, mapper 0.11.1, substrate config `298696064105`, gate `942d86e90cfe`. Window page 0.5.0, facts `08a2769e7dfb…`.
