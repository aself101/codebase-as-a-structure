# Time-lapse — mcp-secure-server

*Trunk (first-parent) of 143 commits, HEAD `63f484757f8d`; 12 frames (12 mapped, 0 skipped), geometry `age`, ruleset maintainability 0.3.4 (profile maintainability), overlays: onboarding 0.3.1. Gate: `validation.json` at HEAD (substrate fingerprint `298696064105`, validated 2026-09-24T22:58:00+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank/mixed) | jitter churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | fd0cfbeb | 2025-12-10 | 1 | 39 | — | | | | | | |
| 1 | 9bc84b27 | 2025-12-14 | 15 | 137 | 14 | 31/24 | 13 (1.00) | 29+13 | 0+0 (0/0/0) | 0.000 / 0.000 | untested (below_pinned_k) |
| 2 | 37f0f52b | 2025-12-18 | 28 | 179 | 13 | 1/1 | 13 (0.30) | 29+12 | 8+19 (3/24/0) | 0.089 / 0.633 | untested (below_pinned_k) |
| 3 | dc823bf1 | 2025-12-20 | 41 | 181 | 13 | 2/0 | 11 (0.25) | 22+0 | 12+0 (4/8/0) | 0.143 / 0.000 | untested (below_pinned_k) |
| 4 | 95892a82 | 2025-12-20 | 54 | 181 | 13 | 0/0 | 0 (0.00) | 0+0 | 6+0 (0/6/0) | 0.083 / 0.000 | untested (below_pinned_k) |
| 5 | 8a5e6b27 | 2026-01-06 | 67 | 184 | 13 | 3/0 | 15 (0.33) | 24+0 | 7+0 (4/3/0) | 0.059 / 0.000 | untested (below_pinned_k) |
| 6 | 0e56d1da | 2026-01-07 | 79 | 188 | 12 | 2/0 | 11 (0.22) | 19+0 | 9+0 (5/4/0) | 0.077 / 0.000 | untested (below_pinned_k) |
| 7 | 906f93ef | 2026-01-09 | 92 | 196 | 13 | 8/1 | 11 (0.22) | 6+0 | 11+0 (8/3/0) | 0.064 / 0.000 | untested (below_pinned_k) |
| 8 | 701296bc | 2026-01-10 | 105 | 200 | 13 | 4/0 | 16 (0.28) | 11+0 | 5+0 (2/3/0) | 0.062 / 0.000 | untested (below_pinned_k) |
| 9 | cb13c32d | 2026-01-22 | 118 | 202 | 13 | 2/0 | 19 (0.31) | 19+0 | 6+0 (4/2/0) | 0.050 / 0.000 | untested (below_pinned_k) |
| 10 | 2cff5483 | 2026-06-11 | 131 | 202 | 13 | 0/0 | 7 (0.11) | 7+0 | 8+0 (8/0/0) | 0.000 / 0.000 | untested (below_pinned_k) |
| 11 | 63f48475 | 2026-09-24 | 169 | 206 | 38 | 3/0 | 33 (0.52) | 22+0 | 4+0 (3/0/1) | 0.043 / 0.000 | untested (touched_fraction_exceeds_floor) |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals only — maintainability/dark_room, maintainability/lit_room — the skeleton reporting time), *rank* (features over rank-only signals, and every floor move of an untouched room: the percentile or the layer moved under a node nobody touched — jitter), and *mixed* (features over a clock and a rank signal together — maintainability/flooded_basement — whose rank component cannot be separated and which the budget therefore counts as jitter); *born/del* = structural change. The four together are the movement between frames. The budget (D-018, operand revised D-024) judges *jitter* = rank + mixed churn and strata moves over untouched rooms, only at K ≤ 50; beyond that it is `untested: beyond_pinned_k` and the numbers stand on their own.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 213 | 0.55 |
| ripple (untouched nodes) | 95 | 0.24 |
| &nbsp;&nbsp;of which clock (time reported) | 41 | 0.11 |
| &nbsp;&nbsp;of which rank (jitter) | 53 | 0.14 |
| &nbsp;&nbsp;of which mixed (counted as jitter) | 1 | 0.00 |
| **jitter (rank + mixed)** | **54** | **0.14** at median K = 13 |
| structural (born + deleted) | 82 | 0.21 |
| **movement** | **390** | over 11 transitions, 168 commits |

Budget tally across transitions: untested:below_pinned_k × 10, untested:touched_fraction_exceeds_floor × 1. **Budget reading: no verdict** — 0 of 11 transitions judged (coverage 0.00); a run the budget could not judge at all says nothing about stability (D-030).

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/foundation | onboarding/leaf_utility | onboarding/package_entry | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 37 | 37 | 37 | 4 | 4 | 37 | 2 | 4 | 5 | 3 | 10 | 1 |
| 1 | 7 | 38 | 38 | 5 | 5 | 6 | 4 | 5 | 1 | 3 | 21 |  |
| 2 | 5 | 27 | 27 | 5 | 8 | 7 | 2 | 5 | 1 | 3 | 21 |  |
| 3 | 6 | 23 | 23 | 5 | 5 | 5 | 1 | 5 | 2 | 3 | 25 |  |
| 4 | 6 | 23 | 23 | 5 | 6 | 5 | 1 | 5 | 2 | 3 | 24 |  |
| 5 | 5 | 16 | 16 | 5 | 5 | 9 | 1 | 5 | 2 | 3 | 27 |  |
| 6 | 6 | 15 | 15 | 6 | 6 | 12 | 5 | 6 | 2 | 3 | 28 |  |
| 7 | 6 | 14 | 14 | 6 | 6 | 6 | 3 | 6 | 2 | 3 | 28 |  |
| 8 | 7 | 11 | 11 | 7 | 7 | 8 | 3 | 7 | 1 | 3 | 29 |  |
| 9 | 7 | 7 | 7 | 7 | 7 | 9 | 3 | 7 | 1 | 3 | 31 |  |
| 10 | 8 | 7 | 7 | 7 | 7 | 7 | 3 | 7 | 1 | 3 | 32 |  |
| 11 | 7 | 7 | 7 | 7 | 8 | 7 | 4 | 7 | 2 | 3 | 36 | 1 |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
