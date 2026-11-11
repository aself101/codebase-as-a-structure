# eslint — one window: `5c8c2417b9ff` → `3f20a57c6293`

**One pair of commits. Each event below is between them. Another pair of commits reads differently.**

The window: `5c8c2417b9ff` (2026-08-24T18:17:49+00:00) → `3f20a57c6293` (2026-09-04T14:29:08+00:00); the pair the gate perturbs: the commit the gate was run at and the commit 25 timeline commits before it; chosen for the gate's test, not for this page. 25 commits in the window, the earliest at 2026-08-24T18:17:49+00:00 and the latest at 2026-09-04T14:29:08+00:00. 461 rooms are in both commits, 1 only in the later and 0 only in the earlier; 16 of the 461 rooms in both are in some commit's recorded changes (3% of rooms in both), 445 are in none.

## Crossings

2 crossings: one line per room and predicate term whose outcome differs between the two commits, among rooms in no commit's recorded changes that exited or entered a row the gate counts.

| window | room | term | value, earlier → later | cutoff, earlier → later | later value against the earlier cutoff (arithmetic only) | earlier value against the later cutoff (arithmetic only) | rows (counts only) |
|---|---|---|---|---|---|---|---|
| 5c8c2417→3f20a57c | lib/cli-engine/hash.js (in no commit's recorded changes in the window) | `load_index >= p90` | value 0.7817 → 0.7889 | cutoff 0.7851 → 0.78847 | `0.7889 >= 0.7851`: yes | `0.7817 >= 0.78847`: no | entered the map's row foundation · high-load node (maintainability, onboarding) (47 → 47 rooms: this room entered, 1 room in no commit's recorded changes in the window exited) |
| 5c8c2417→3f20a57c | packages/js/src/index.js (in no commit's recorded changes in the window) | `load_index >= p90` | value 0.7851 → 0.7846 | cutoff 0.7851 → 0.78847 | `0.7846 >= 0.7851`: no | `0.7851 >= 0.78847`: no | exited the map's row foundation · high-load node (maintainability, onboarding) (47 → 47 rooms: this room exited, 1 room in no commit's recorded changes in the window entered) |

Each side's cutoff is computed over that commit's rooms that have a value, of 461 rooms earlier and 462 later, this room's included. The two comparisons are arithmetic on the four numbers beside them; neither names a cause. The rows column counts the rooms that entered and exited each row; it does not say which of them, if any, bears on the line it sits in.

Only rooms that exited or entered a row are listed: a term that changed outcome while the room stayed in or out of its row is not on this page (the diff carries no evidence for it).

## Clock rows

A clock row's term is measured in days from the date of the snapshot.

- **lit_room (maintainability)** — 50 → 47 rooms. Rooms in no commit's recorded changes in the window: 15 exited (docs/src/assets/js/css-vars-ponyfill@2.js; docs/src/assets/js/inert-polyfill.js; lib/rules/class-methods-use-this.js; and 12 more), 0 entered (none); edited rooms: 11 entered, 0 exited; rooms only in one commit: 1 entered, 0 exited; not in the gate's count.

Their crossings, not in the gate's count:

| window | room | term | value, earlier → later | cutoff, earlier → later | later value against the earlier cutoff (arithmetic only) | earlier value against the later cutoff (arithmetic only) | rows (counts only) |
|---|---|---|---|---|---|---|---|
| 5c8c2417→3f20a57c | docs/src/assets/js/css-vars-ponyfill@2.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 51.0454 → 61.8866 days | cutoff 51.0454 → 47.8085 days | `61.8866 <= 51.0454`: no | `51.0454 <= 47.8085`: no | exited the map's row lit_room (maintainability) (50 → 47 rooms: this room exited, 14 other rooms in no commit's recorded changes in the window exited, 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | docs/src/assets/js/inert-polyfill.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 51.0454 → 61.8866 days | cutoff 51.0454 → 47.8085 days | `61.8866 <= 51.0454`: no | `51.0454 <= 47.8085`: no | exited the map's row lit_room (maintainability) (50 → 47 rooms: this room exited, 14 other rooms in no commit's recorded changes in the window exited, 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/class-methods-use-this.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 37.3754 → 48.2166 days | cutoff 51.0454 → 47.8085 days | `48.2166 <= 51.0454`: yes | `37.3754 <= 47.8085`: yes | exited the map's row lit_room (maintainability) (50 → 47 rooms: this room exited, 14 other rooms in no commit's recorded changes in the window exited, 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/eqeqeq.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 49.8924 → 60.7336 days | cutoff 51.0454 → 47.8085 days | `60.7336 <= 51.0454`: no | `49.8924 <= 47.8085`: no | exited the map's row lit_room (maintainability) (50 → 47 rooms: this room exited, 14 other rooms in no commit's recorded changes in the window exited, 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/func-name-matching.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 51.0454 → 61.8866 days | cutoff 51.0454 → 47.8085 days | `61.8866 <= 51.0454`: no | `51.0454 <= 47.8085`: no | exited the map's row lit_room (maintainability) (50 → 47 rooms: this room exited, 14 other rooms in no commit's recorded changes in the window exited, 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/generator-star-spacing.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 51.0454 → 61.8866 days | cutoff 51.0454 → 47.8085 days | `61.8866 <= 51.0454`: no | `51.0454 <= 47.8085`: no | exited the map's row lit_room (maintainability) (50 → 47 rooms: this room exited, 14 other rooms in no commit's recorded changes in the window exited, 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/indent.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 51.0454 → 61.8866 days | cutoff 51.0454 → 47.8085 days | `61.8866 <= 51.0454`: no | `51.0454 <= 47.8085`: no | exited the map's row lit_room (maintainability) (50 → 47 rooms: this room exited, 14 other rooms in no commit's recorded changes in the window exited, 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/max-nested-callbacks.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 46.8307 → 57.6719 days | cutoff 51.0454 → 47.8085 days | `57.6719 <= 51.0454`: no | `46.8307 <= 47.8085`: yes | exited the map's row lit_room (maintainability) (50 → 47 rooms: this room exited, 14 other rooms in no commit's recorded changes in the window exited, 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/no-mixed-spaces-and-tabs.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 51.0454 → 61.8866 days | cutoff 51.0454 → 47.8085 days | `61.8866 <= 51.0454`: no | `51.0454 <= 47.8085`: no | exited the map's row lit_room (maintainability) (50 → 47 rooms: this room exited, 14 other rooms in no commit's recorded changes in the window exited, 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/no-promise-executor-return.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 51.0454 → 61.8866 days | cutoff 51.0454 → 47.8085 days | `61.8866 <= 51.0454`: no | `51.0454 <= 47.8085`: no | exited the map's row lit_room (maintainability) (50 → 47 rooms: this room exited, 14 other rooms in no commit's recorded changes in the window exited, 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/no-script-url.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 51.0454 → 61.8866 days | cutoff 51.0454 → 47.8085 days | `61.8866 <= 51.0454`: no | `51.0454 <= 47.8085`: no | exited the map's row lit_room (maintainability) (50 → 47 rooms: this room exited, 14 other rooms in no commit's recorded changes in the window exited, 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/no-shadow.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 51.0454 → 61.8866 days | cutoff 51.0454 → 47.8085 days | `61.8866 <= 51.0454`: no | `51.0454 <= 47.8085`: no | exited the map's row lit_room (maintainability) (50 → 47 rooms: this room exited, 14 other rooms in no commit's recorded changes in the window exited, 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/preserve-caught-error.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 38.5489 → 49.3901 days | cutoff 51.0454 → 47.8085 days | `49.3901 <= 51.0454`: yes | `38.5489 <= 47.8085`: yes | exited the map's row lit_room (maintainability) (50 → 47 rooms: this room exited, 14 other rooms in no commit's recorded changes in the window exited, 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/shared/serialization.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 38.1022 → 48.9434 days | cutoff 51.0454 → 47.8085 days | `48.9434 <= 51.0454`: yes | `38.1022 <= 47.8085`: yes | exited the map's row lit_room (maintainability) (50 → 47 rooms: this room exited, 14 other rooms in no commit's recorded changes in the window exited, 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | tools/config-rule.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | value 46.1184 → 56.9596 days | cutoff 51.0454 → 47.8085 days | `56.9596 <= 51.0454`: no | `46.1184 <= 47.8085`: yes | exited the map's row lit_room (maintainability) (50 → 47 rooms: this room exited, 14 other rooms in no commit's recorded changes in the window exited, 11 edited rooms entered, 1 room only in the later commit entered) |

Each side's cutoff is computed over that commit's rooms that have a value, of 461 rooms earlier and 462 later, this room's included. The two comparisons are arithmetic on the four numbers beside them; neither names a cause. The rows column counts the rooms that entered and exited each row; it does not say which of them, if any, bears on the line it sits in.

## Excluded rows (◌)

- **◌ crack · high edit-pressure node (maintainability)** — 47 → 47 rooms. Rooms in no commit's recorded changes in the window: 1 exited, 0 entered; edited rooms: 1 entered, 0 exited; excluded from the diagnosis; not in the gate's count. An excluded row's rooms are counted, not named, and no values or cutoffs are printed for it.

## Bands

A band is a depth band of the map's geometry: a position in this tool's drawing, not a rating of a room.

- Under the age geometry, 1 of the 445 rooms in no commit's recorded changes in the window changed band: 1 with a different raw value (lib/rules/no-useless-concat.js: band 2 → 1, raw value 0.5996 → 0.6004).
- Under the layer geometry, none of the 445 rooms in no commit's recorded changes in the window changed band.

## What the gate counts on this window

What the gate counts on a window: for rooms in no commit's recorded changes, the rank and mixed rows they entered or exited, and the bands that differ. The clock rows and excluded rows above are not in its count. It is a check on this tool's map. It is not a reading of the code, of the repository, or of any room named on this page.

- rows (the same under each geometry; rows do not depend on it) — 2 of the 445 rooms in no commit's recorded changes in the window, 2 crossings. In the gate's unit: 4 of the 748 `(profile, feature, room)` assignments that 426 of those rooms hold on rank and mixed rows. The gate's ceiling on the map is 0.05 of them.
- bands, age geometry — 1 of the 445 rooms in no commit's recorded changes in the window. The gate's ceiling on the map is 0.05 of them.
- bands, layer geometry — 0 of the 445 rooms in no commit's recorded changes in the window. The gate's ceiling on the map is 0.05 of them.

Counts of this one window (mapper spec §7 Q3). This page does not read whether another window of this repository counts the same. The same number of crossings is a different share of a different number of rooms, so these counts do not rank repositories. Whether the gate judged this window, and its own word for it, are in each diff's `budget` block and are not on this page.

## What this page does not report

Marks that are neither diagnostic nor excluded (0 in the earlier commit, 0 in the later); what differs for edited rooms beyond the counts beside each row; a term that changed outcome without the room exiting or entering its row; any pair of commits but this one.

## Provenance

`eslint.age.diff.json` (age: skeleton `ab915a9bcd60…` → `dd889218caf9…`); `eslint.layer.diff.json` (layer: skeleton `da8d39a9600c…` → `49b05257c552…`). Ruleset maintainability 0.3.4 + onboarding 0.3.1, mapper 0.11.1, substrate config `298696064105`, gate `942d86e90cfe`. Window page 0.3.0, facts `ca433e38e3a4…`.
