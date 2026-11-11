# mcp-secure-server, as this tool maps it — one window: `4c99da71468c` → `5348b3ef614d`

**One pair of commits. Each event below is between them. Another pair of commits may read differently; this page does not compare them.**

The window: `4c99da71468c` (2026-01-28T07:44:41-10:00) → `5348b3ef614d` (2026-09-10T18:57:42-10:00); the pair the gate perturbs: the commit the gate was run at and the commit 25 timeline commits before it; chosen for the gate's test, not for this page. 25 commits in the window, the earliest at 2026-01-28T07:57:31-10:00 and the latest at 2026-09-10T18:57:42-10:00. 64 rooms are in both commits, 1 only in the later and 0 only in the earlier; 29 of the 64 rooms in both are in some commit's recorded changes (45% of rooms in both), 35 are in none.

## Crossings

2 crossings: one line per room and predicate term whose outcome differs between the two commits, among rooms in no commit's recorded changes that exited or entered a row the gate counts.

A row's name is this tool's label for a position on its map, not a description of the code.

| window | room | term | value, earlier → later | cutoff, earlier → later | later value against the earlier cutoff (arithmetic only) | earlier value against the later cutoff (arithmetic only) | rows (counts only) |
|---|---|---|---|---|---|---|---|
| 4c99da71→5348b3ef | src/index.ts (in no commit's recorded changes in the window) | `centrality >= p90` | value 0.0134 → 0.0128 | cutoff 0.01285 → 0.01426 | `0.0128 >= 0.01285`: no | `0.0134 >= 0.01426`: no | exited the map's row hub (maintainability) (7 → 7 rooms: this room exited, 2 edited rooms entered, 1 edited room exited); exited the map's row corridor (onboarding) (3 → 3 rooms: this room exited, 1 edited room entered) |
| 4c99da71→5348b3ef | src/types/index.ts (in no commit's recorded changes in the window) | `load_index >= p90` | value 0.8434 → 0.8429 | cutoff 0.84085 → 0.84876 | `0.8429 >= 0.84085`: yes | `0.8434 >= 0.84876`: no | exited the map's row foundation · high-load node (maintainability, onboarding) (7 → 7 rooms: this room exited, 1 edited room entered) |

Each side's cutoff is computed over that commit's rooms that have a value, of 64 rooms earlier and 65 later, this room's included. The two comparisons are arithmetic on the four numbers beside them, as recorded; neither names a cause. The rows column counts the rooms that entered and exited each row; it does not say which of them, if any, bears on the line it sits in.

Only rooms that exited or entered a row are listed: a term that changed outcome while the room stayed in or out of its row is not on this page (the diff carries no evidence for it).

## Clock rows

A clock row's term is measured in days from the date of the snapshot, so the earlier side and the later side of a line are measured from two different dates and are not compared with each other. The two commits here are 225.47 days apart, and a room in no commit's recorded changes reads that many days more on the later side.

- **lit_room (maintainability)** — 9 → 10 rooms. Rooms in no commit's recorded changes in the window: 4 exited (src/security/layers/layer-utils/content/utils/structural-analysis.ts; src/security/layers/layer-utils/content/utils/text-decoding.ts; src/security/layers/layer3-behavior.ts; and 1 more), 0 entered (none); edited rooms: 6 entered, 1 exited; not in the gate's count.

Their crossings, not in the gate's count:

| window | room | term | value, earlier → later | cutoff, earlier → later | later value against the earlier cutoff (arithmetic only) | earlier value against the later cutoff (arithmetic only) | rows (counts only) |
|---|---|---|---|---|---|---|---|
| 4c99da71→5348b3ef | src/security/layers/layer-utils/content/utils/structural-analysis.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 16.6122 → 242.08 days | cutoff 16.643 → 0.0188 days | not compared across dates; later side alone: `242.08 <= 0.0188`: no | not compared across dates; earlier side alone: `16.6122 <= 16.643`: yes | exited the map's row lit_room (maintainability) (9 → 10 rooms: this room exited, 3 other rooms in no commit's recorded changes in the window exited, 6 edited rooms entered, 1 edited room exited) |
| 4c99da71→5348b3ef | src/security/layers/layer-utils/content/utils/text-decoding.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 16.6122 → 242.08 days | cutoff 16.643 → 0.0188 days | not compared across dates; later side alone: `242.08 <= 0.0188`: no | not compared across dates; earlier side alone: `16.6122 <= 16.643`: yes | exited the map's row lit_room (maintainability) (9 → 10 rooms: this room exited, 3 other rooms in no commit's recorded changes in the window exited, 6 edited rooms entered, 1 edited room exited) |
| 4c99da71→5348b3ef | src/security/layers/layer3-behavior.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 16.643 → 242.11 days | cutoff 16.643 → 0.0188 days | not compared across dates; later side alone: `242.11 <= 0.0188`: no | not compared across dates; earlier side alone: `16.643 <= 16.643`: yes | exited the map's row lit_room (maintainability) (9 → 10 rooms: this room exited, 3 other rooms in no commit's recorded changes in the window exited, 6 edited rooms entered, 1 edited room exited) |
| 4c99da71→5348b3ef | src/security/layers/layer5-contextual-types.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 16.6351 → 242.102 days | cutoff 16.643 → 0.0188 days | not compared across dates; later side alone: `242.102 <= 0.0188`: no | not compared across dates; earlier side alone: `16.6351 <= 16.643`: yes | exited the map's row lit_room (maintainability) (9 → 10 rooms: this room exited, 3 other rooms in no commit's recorded changes in the window exited, 6 edited rooms entered, 1 edited room exited) |

Each side's cutoff is computed over that commit's rooms that have a value, of 64 rooms earlier and 65 later, this room's included. The two comparisons are arithmetic on the four numbers beside them, as recorded; neither names a cause. The rows column counts the rooms that entered and exited each row; it does not say which of them, if any, bears on the line it sits in.

## Excluded rows (◌)

- **◌ crack · high edit-pressure node (maintainability)** — 7 → 7 rooms. Rooms in no commit's recorded changes in the window: 2 exited, 0 entered; edited rooms: 2 entered, 0 exited; excluded from the diagnosis; not in the gate's count. An excluded row's rooms are counted, not named, and no values or cutoffs are printed for it.

## Bands

A band is a depth band of the map's geometry: a position in this tool's drawing, not a rating of a room.

- Under the age geometry, none of the 35 rooms in no commit's recorded changes in the window changed band.
- Under the layer geometry, 4 of the 35 rooms in no commit's recorded changes in the window changed band: 2 with the same raw depth on both sides (src/security/config/index.ts: band 1 → 2, raw depth 2 → 2; src/security/layers/layer-utils/content/helper-utils.ts: band 1 → 2, raw depth 2 → 2); 2 with a different raw depth (src/security/layers/layer-utils/semantics/semantic-policies.ts: band 3 → 2, raw depth 6 → 5; src/security/transport/http-transport-manager.ts: band 3 → 4, raw depth 7 → 8).

## What the gate counts on this window

What the gate counts on a window: for rooms in no commit's recorded changes, the rank and mixed rows they entered or exited, and the bands that differ. The clock rows and excluded rows above are not in its count. It is a check on this tool's map. It is not a reading of the code, of the repository, or of any room named on this page.

- rows (the same under each geometry; rows do not depend on it) — 2 of the 35 rooms in no commit's recorded changes in the window, 2 crossings. In the gate's unit: 23 of those rooms hold, in one commit or the other, 35 `(profile, feature, room)` assignments on rank and mixed rows; 4 of those 35 are in one commit and not the other.
- bands, age geometry — 0 of the 35 rooms in no commit's recorded changes in the window.
- bands, layer geometry — 4 of the 35 rooms in no commit's recorded changes in the window.

Counts of this one window (mapper spec §7 Q3). This page does not read whether another window of this repository counts the same. The same number of crossings is a different share of a different number of rooms, so these counts do not rank repositories. Whether the gate judged this window, the limit it judges against and its own word for it are in each diff's `budget` block and are not on this page.

## What this page does not report

Marks that are neither diagnostic nor excluded (0 in the earlier commit, 0 in the later); what differs for edited rooms beyond the counts beside each row; a term that changed outcome without the room exiting or entering its row; any pair of commits but this one.

## Provenance

`mcp-secure-server.age.diff.json` (age: skeleton `700b0ee35700…` → `38d867b47977…`); `mcp-secure-server.layer.diff.json` (layer: skeleton `2b03539d7171…` → `6f9eccea15e0…`). Ruleset maintainability 0.3.4 + onboarding 0.3.1, mapper 0.11.1, substrate config `298696064105`, gate `942d86e90cfe`. Window page 0.4.0, facts `517b88caab8b…`.
