# mcp-secure-server — one window: `4c99da71468c` → `5348b3ef614d`

**One pair of commits. Each event below is between them. Another pair of commits reads differently.**

The window: `4c99da71468c` (2026-01-28T07:44:41-10:00) → `5348b3ef614d` (2026-09-10T18:57:42-10:00); the pair the gate perturbs: HEAD and the commit 25 timeline commits before it; chosen for the gate's test, not for this page. 25 commits in the window, the earliest at 2026-01-28T07:57:31-10:00 and the latest at 2026-09-10T18:57:42-10:00. 64 rooms are in both commits, 1 only in the later and 0 only in the earlier; 29 of the 64 rooms in both are in some commit's recorded changes (45% of rooms in both), 35 are in none.

## Crossings

2 crossings: one line per room and predicate term whose outcome differs between the two commits, among rooms in no commit's recorded changes, on rows the gate's reading counts.

| window | room | term | value earlier → later | cutoff earlier → later | later value against the earlier cutoff | earlier value against the later cutoff | rows |
|---|---|---|---|---|---|---|---|
| 4c99da71→5348b3ef | src/index.ts (in no commit's recorded changes in the window) | `centrality >= p90` | 0.0134 → 0.0128 | 0.01285 → 0.01426 | fails | fails | left hub (maintainability) (7 → 7 rooms: 2 edited rooms entered, 1 edited room left); left corridor (onboarding) (3 → 3 rooms: 1 edited room entered) |
| 4c99da71→5348b3ef | src/types/index.ts (in no commit's recorded changes in the window) | `load_index >= p90` | 0.8434 → 0.8429 | 0.84085 → 0.84876 | passes | fails | left foundation (maintainability, onboarding) (7 → 7 rooms: 1 edited room entered) |

Each side's cutoff is computed over that commit's rooms that have a value, of 64 rooms earlier and 65 later, this room's included. The two comparisons are arithmetic on the four numbers beside them; neither names a cause.

## Clock rows

- **lit_room (maintainability)** — 9 → 10 rooms; 4 rooms in no commit's recorded changes in the window left (src/security/layers/layer-utils/content/utils/structural-analysis.ts; src/security/layers/layer-utils/content/utils/text-decoding.ts; src/security/layers/layer3-behavior.ts; and 1 more), 0 entered (none); not counted in the gate's reading.

Their crossings, not counted in the gate's reading:

| window | room | term | value earlier → later | cutoff earlier → later | later value against the earlier cutoff | earlier value against the later cutoff | rows |
|---|---|---|---|---|---|---|---|
| 4c99da71→5348b3ef | src/security/layers/layer-utils/content/utils/structural-analysis.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 16.6122 → 242.08 | 16.643 → 0.0188 | fails | fails | left lit_room (maintainability) (9 → 10 rooms: 6 edited rooms entered, 1 edited room left) |
| 4c99da71→5348b3ef | src/security/layers/layer-utils/content/utils/text-decoding.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 16.6122 → 242.08 | 16.643 → 0.0188 | fails | fails | left lit_room (maintainability) (9 → 10 rooms: 6 edited rooms entered, 1 edited room left) |
| 4c99da71→5348b3ef | src/security/layers/layer3-behavior.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 16.643 → 242.11 | 16.643 → 0.0188 | fails | fails | left lit_room (maintainability) (9 → 10 rooms: 6 edited rooms entered, 1 edited room left) |
| 4c99da71→5348b3ef | src/security/layers/layer5-contextual-types.ts (in no commit's recorded changes in the window) | `last_touched_days <= p10` | 16.6351 → 242.102 | 16.643 → 0.0188 | fails | fails | left lit_room (maintainability) (9 → 10 rooms: 6 edited rooms entered, 1 edited room left) |

## Excluded rows (◌)

- **◌ crack (maintainability)** — 7 → 7 rooms; 2 rooms in no commit's recorded changes in the window left, 0 entered; excluded from the diagnosis; not counted in the gate's reading. An excluded row's rooms are counted, not named, and no values or cutoffs are printed for it.

## Bands

- Under the age geometry, none of the 35 rooms in no commit's recorded changes in the window changed band.
- Under the layer geometry, 4 of the 35 rooms in no commit's recorded changes in the window changed band: 2 with the same raw depth on both sides (src/security/config/index.ts; src/security/layers/layer-utils/content/helper-utils.ts); 2 with a different raw depth (src/security/layers/layer-utils/semantics/semantic-policies.ts; src/security/transport/http-transport-manager.ts).

## The gate's budget reading on this window

- age geometry — 2 rooms, 2 crossings (4 of 35 `(profile, feature, room)` assignments; 2 or more of 35 assignments is over 0.05 by the gate's rule); bands 0 of 35 rooms (2 or more of 35 rooms is over 0.05 by the gate's rule). The gate's token: `over_budget`, on features.
- layer geometry — 2 rooms, 2 crossings (4 of 35 `(profile, feature, room)` assignments; 2 or more of 35 assignments is over 0.05 by the gate's rule); bands 4 of 35 rooms (2 or more of 35 rooms is over 0.05 by the gate's rule). The gate's token: `over_budget`, on features and bands.

A reading of this one window (mapper spec §7 Q3). This page does not read whether it is usual for this repository. The same number of crossings reads differently on a different number of rooms, so the token does not rank repositories.

## What this page does not report

Marks that are neither diagnostic nor excluded (0 in the earlier commit, 0 in the later); what differs for edited rooms beyond the counts in the rows column; any pair of commits but this one.

## Provenance

`mcp-secure-server.age.diff.json` (age: skeleton `700b0ee35700…` → `38d867b47977…`); `mcp-secure-server.layer.diff.json` (layer: skeleton `2b03539d7171…` → `6f9eccea15e0…`). Ruleset maintainability 0.3.4 + onboarding 0.3.1, mapper 0.11.1, substrate config `298696064105`, gate `942d86e90cfe`. Window page 0.1.0, facts `1ce3a00068a0…`.
