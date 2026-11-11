# eslint — one window: `5c8c2417b9ff` → `3f20a57c6293`

**One pair of commits. Each event below is between them. Another pair of commits reads differently.**

The window: `5c8c2417b9ff` (2026-08-24T18:17:49+00:00) → `3f20a57c6293` (2026-09-04T14:29:08+00:00); the pair the gate perturbs: HEAD and the commit 25 timeline commits before it; chosen for the gate's test, not for this page. 25 commits in the window, the earliest at 2026-08-24T18:17:49+00:00 and the latest at 2026-09-04T14:29:08+00:00. 461 rooms are in both commits, 1 only in the later and 0 only in the earlier; 16 of the 461 rooms in both are in some commit's recorded changes (3% of rooms in both), 445 are in none.

## Crossings

2 crossings: one line per room and predicate term whose outcome differs between the two commits, among rooms in no commit's recorded changes, on rows the gate's reading counts.

| window | room | term | value earlier → later | cutoff earlier → later | later value against the earlier cutoff | earlier value against the later cutoff | rows |
|---|---|---|---|---|---|---|---|
| 5c8c2417→3f20a57c | lib/cli-engine/hash.js (in no commit's recorded changes in the window) | `load_index >= p90` | 0.7817 → 0.7889 | 0.7851 → 0.78847 | passes | fails | entered foundation (maintainability, onboarding) (47 → 47 rooms) |
| 5c8c2417→3f20a57c | packages/js/src/index.js (in no commit's recorded changes in the window) | `load_index >= p90` | 0.7851 → 0.7846 | 0.7851 → 0.78847 | fails | fails | left foundation (maintainability, onboarding) (47 → 47 rooms) |

Each side's cutoff is computed over that commit's rooms that have a value, of 461 rooms earlier and 462 later, this room's included. The two comparisons are arithmetic on the four numbers beside them; neither names a cause.

## Clock rows

- **lit_room (maintainability)** — 50 → 47 rooms; 15 rooms in no commit's recorded changes in the window left (docs/src/assets/js/css-vars-ponyfill@2.js; docs/src/assets/js/inert-polyfill.js; lib/rules/class-methods-use-this.js; and 12 more), 0 entered (none); not counted in the gate's reading.

Their crossings, not counted in the gate's reading:

| window | room | term | value earlier → later | cutoff earlier → later | later value against the earlier cutoff | earlier value against the later cutoff | rows |
|---|---|---|---|---|---|---|---|
| 5c8c2417→3f20a57c | docs/src/assets/js/css-vars-ponyfill@2.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 51.0454 → 61.8866 | 51.0454 → 47.8085 | fails | fails | left lit_room (maintainability) (50 → 47 rooms: 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | docs/src/assets/js/inert-polyfill.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 51.0454 → 61.8866 | 51.0454 → 47.8085 | fails | fails | left lit_room (maintainability) (50 → 47 rooms: 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/class-methods-use-this.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 37.3754 → 48.2166 | 51.0454 → 47.8085 | passes | passes | left lit_room (maintainability) (50 → 47 rooms: 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/eqeqeq.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 49.8924 → 60.7336 | 51.0454 → 47.8085 | fails | fails | left lit_room (maintainability) (50 → 47 rooms: 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/func-name-matching.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 51.0454 → 61.8866 | 51.0454 → 47.8085 | fails | fails | left lit_room (maintainability) (50 → 47 rooms: 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/generator-star-spacing.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 51.0454 → 61.8866 | 51.0454 → 47.8085 | fails | fails | left lit_room (maintainability) (50 → 47 rooms: 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/indent.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 51.0454 → 61.8866 | 51.0454 → 47.8085 | fails | fails | left lit_room (maintainability) (50 → 47 rooms: 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/max-nested-callbacks.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 46.8307 → 57.6719 | 51.0454 → 47.8085 | fails | passes | left lit_room (maintainability) (50 → 47 rooms: 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/no-mixed-spaces-and-tabs.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 51.0454 → 61.8866 | 51.0454 → 47.8085 | fails | fails | left lit_room (maintainability) (50 → 47 rooms: 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/no-promise-executor-return.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 51.0454 → 61.8866 | 51.0454 → 47.8085 | fails | fails | left lit_room (maintainability) (50 → 47 rooms: 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/no-script-url.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 51.0454 → 61.8866 | 51.0454 → 47.8085 | fails | fails | left lit_room (maintainability) (50 → 47 rooms: 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/no-shadow.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 51.0454 → 61.8866 | 51.0454 → 47.8085 | fails | fails | left lit_room (maintainability) (50 → 47 rooms: 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/rules/preserve-caught-error.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 38.5489 → 49.3901 | 51.0454 → 47.8085 | passes | passes | left lit_room (maintainability) (50 → 47 rooms: 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | lib/shared/serialization.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 38.1022 → 48.9434 | 51.0454 → 47.8085 | passes | passes | left lit_room (maintainability) (50 → 47 rooms: 11 edited rooms entered, 1 room only in the later commit entered) |
| 5c8c2417→3f20a57c | tools/config-rule.js (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 46.1184 → 56.9596 | 51.0454 → 47.8085 | fails | passes | left lit_room (maintainability) (50 → 47 rooms: 11 edited rooms entered, 1 room only in the later commit entered) |

## Excluded rows (◌)

- **◌ crack (maintainability)** — 47 → 47 rooms; 1 room in no commit's recorded changes in the window left, 0 entered; excluded from the diagnosis; not counted in the gate's reading. An excluded row's rooms are counted, not named, and no values or cutoffs are printed for it.

## Bands

- Under the age geometry, 1 of the 445 rooms in no commit's recorded changes in the window changed band: 1 with a different raw value (lib/rules/no-useless-concat.js).
- Under the layer geometry, none of the 445 rooms in no commit's recorded changes in the window changed band.

## The gate's budget reading on this window

- age geometry — 2 rooms, 2 crossings (4 of 748 `(profile, feature, room)` assignments; 38 or more of 748 assignments is over 0.05 by the gate's rule); bands 1 of 445 rooms (23 or more of 445 rooms is over 0.05 by the gate's rule). The gate's token: `within_budget`.
- layer geometry — 2 rooms, 2 crossings (4 of 748 `(profile, feature, room)` assignments; 38 or more of 748 assignments is over 0.05 by the gate's rule); bands 0 of 445 rooms (23 or more of 445 rooms is over 0.05 by the gate's rule). The gate's token: `within_budget`.

A reading of this one window (mapper spec §7 Q3). This page does not read whether it is usual for this repository. The same number of crossings reads differently on a different number of rooms, so the token does not rank repositories.

## What this page does not report

Marks that are neither diagnostic nor excluded (0 in the earlier commit, 0 in the later); what differs for edited rooms beyond the counts in the rows column; any pair of commits but this one.

## Provenance

`eslint.age.diff.json` (age: skeleton `ab915a9bcd60…` → `dd889218caf9…`); `eslint.layer.diff.json` (layer: skeleton `da8d39a9600c…` → `49b05257c552…`). Ruleset maintainability 0.3.4 + onboarding 0.3.1, mapper 0.11.1, substrate config `298696064105`, gate `942d86e90cfe`. Window page 0.1.0, facts `c7c0e4be6697…`.
