# Time-lapse — mcp-secure-server

*Trunk (first-parent) of 134 commits, HEAD `ecb30716b87e`; 27 frames (27 mapped, 0 skipped), geometry `age`, ruleset maintainability 0.1.0 (profile maintainability), overlays: onboarding 0.1.0. Gate: `validation.json` at HEAD (substrate fingerprint `5f5554e36d4a`, validated 2026-09-05T19:35:20+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank/mixed) | jitter churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 3a722916 | 2025-12-10 | 4 | 41 | — | | | | | | |
| 1 | c447ca84 | 2025-12-14 | 10 | 108 | 6 | 93/26 | 14 (0.93) | 24+14 | 0+1 (0/1/0) | 0.000 / 1.000 | untested (touched_fraction_exceeds_floor) |
| 2 | 9bc84b27 | 2025-12-14 | 15 | 137 | 5 | 29/0 | 21 (0.19) | 28+21 | 83+41 (43/50/31) | 0.360 / 0.471 | over_budget |
| 3 | 3216c6e4 | 2025-12-14 | 20 | 149 | 5 | 12/0 | 5 (0.04) | 3+0 | 25+0 (21/4/0) | 0.026 / 0.000 | within_budget |
| 4 | b927d4f9 | 2025-12-15 | 25 | 180 | 5 | 31/0 | 8 (0.05) | 13+7 | 31+61 (16/76/0) | 0.089 / 0.433 | over_budget |
| 5 | 7032d674 | 2025-12-18 | 30 | 179 | 5 | 0/1 | 8 (0.04) | 16+0 | 0+0 (0/0/0) | 0.000 / 0.000 | within_budget |
| 6 | 964dee76 | 2025-12-18 | 35 | 181 | 5 | 2/0 | 20 (0.11) | 17+0 | 32+4 (19/17/0) | 0.071 / 0.025 | over_budget |
| 7 | 3b9e4dd3 | 2025-12-20 | 40 | 181 | 5 | 0/0 | 6 (0.03) | 11+0 | 3+0 (0/3/0) | 0.015 / 0.000 | within_budget |
| 8 | 2f76b311 | 2025-12-20 | 45 | 181 | 5 | 0/0 | 0 (0.00) | 0+0 | 0+0 (0/0/0) | 0.000 / 0.000 | within_budget |
| 9 | 6f7ea8a2 | 2025-12-20 | 50 | 181 | 5 | 0/0 | 0 (0.00) | 0+0 | 0+0 (0/0/0) | 0.000 / 0.000 | within_budget |
| 10 | b9faeb23 | 2025-12-20 | 55 | 181 | 5 | 0/0 | 0 (0.00) | 0+0 | 0+0 (0/0/0) | 0.000 / 0.000 | within_budget |
| 11 | e913eb08 | 2025-12-29 | 60 | 181 | 5 | 0/0 | 8 (0.04) | 14+0 | 0+0 (0/0/0) | 0.000 / 0.000 | within_budget |
| 12 | d0610468 | 2026-01-02 | 65 | 181 | 5 | 0/0 | 7 (0.04) | 6+0 | 17+0 (17/0/0) | 0.000 / 0.000 | within_budget |
| 13 | 5b54ea72 | 2026-01-06 | 70 | 187 | 5 | 6/0 | 10 (0.06) | 7+0 | 96+0 (44/22/30) | 0.242 / 0.000 | over_budget |
| 14 | 134e712b | 2026-01-07 | 75 | 188 | 5 | 1/0 | 12 (0.06) | 10+0 | 9+0 (3/6/0) | 0.031 / 0.000 | within_budget |
| 15 | 04c53955 | 2026-01-08 | 80 | 188 | 5 | 0/0 | 18 (0.10) | 13+0 | 7+0 (7/0/0) | 0.000 / 0.000 | within_budget |
| 16 | 93b5451a | 2026-01-08 | 85 | 191 | 5 | 3/0 | 6 (0.03) | 8+0 | 12+62 (8/66/0) | 0.021 / 0.341 | over_budget |
| 17 | 0cde80da | 2026-01-09 | 90 | 196 | 5 | 5/0 | 6 (0.03) | 4+0 | 22+16 (14/24/0) | 0.039 / 0.086 | over_budget |
| 18 | 238267c5 | 2026-01-09 | 95 | 197 | 5 | 1/0 | 8 (0.04) | 11+0 | 9+0 (1/8/0) | 0.042 / 0.000 | within_budget |
| 19 | f305a925 | 2026-01-10 | 100 | 197 | 5 | 0/0 | 12 (0.06) | 12+0 | 13+0 (11/2/0) | 0.011 / 0.000 | within_budget |
| 20 | 701296bc | 2026-01-10 | 105 | 200 | 5 | 3/0 | 2 (0.01) | 0+0 | 7+0 (3/4/0) | 0.020 / 0.000 | within_budget |
| 21 | 5329e6a3 | 2026-01-11 | 110 | 201 | 5 | 1/0 | 4 (0.02) | 2+0 | 4+0 (0/4/0) | 0.020 / 0.000 | within_budget |
| 22 | 77a06562 | 2026-01-11 | 115 | 202 | 5 | 1/0 | 16 (0.08) | 8+0 | 10+0 (9/1/0) | 0.005 / 0.000 | within_budget |
| 23 | 4c99da71 | 2026-01-28 | 120 | 202 | 5 | 0/0 | 3 (0.01) | 9+0 | 2+0 (2/0/0) | 0.000 / 0.000 | within_budget |
| 24 | f1473915 | 2026-04-08 | 125 | 202 | 5 | 0/0 | 1 (0.00) | 0+0 | 0+0 (0/0/0) | 0.000 / 0.000 | within_budget |
| 25 | ccfcad6e | 2026-06-07 | 130 | 202 | 5 | 0/0 | 7 (0.03) | 5+0 | 2+0 (2/0/0) | 0.000 / 0.000 | within_budget |
| 26 | ecb30716 | 2026-08-24 | 139 | 202 | 9 | 0/0 | 16 (0.08) | 8+0 | 12+0 (11/1/0) | 0.006 / 0.000 | within_budget |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals only — maintainability/dark_room, maintainability/lit_room — the skeleton reporting time), *rank* (features over rank-only signals, and every floor move of an untouched room: the percentile or the layer moved under a node nobody touched — jitter), and *mixed* (features over a clock and a rank signal together — maintainability/flooded_basement — whose rank component cannot be separated and which the budget therefore counts as jitter); *born/del* = structural change. The four together are the movement between frames. The budget (D-018, operand revised D-024) judges *jitter* = rank + mixed churn and strata moves over untouched rooms, only at K ≤ 10; beyond that it is `untested: beyond_pinned_k` and the numbers stand on their own.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 271 | 0.25 |
| ripple (untouched nodes) | 581 | 0.54 |
| &nbsp;&nbsp;of which clock (time reported) | 231 | 0.22 |
| &nbsp;&nbsp;of which rank (jitter) | 289 | 0.27 |
| &nbsp;&nbsp;of which mixed (counted as jitter) | 61 | 0.06 |
| **jitter (rank + mixed)** | **350** | **0.33** at median K = 5 |
| structural (born + deleted) | 215 | 0.20 |
| **movement** | **1067** | over 26 transitions, 135 commits |

Budget tally across transitions: over_budget × 6, untested:touched_fraction_exceeds_floor × 1, within_budget × 19.

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/entrance | onboarding/foundation | onboarding/leaf_utility | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 24 | 15 | 15 | 5 | 5 | 26 | 3 |  | 5 | 5 | 10 |  |
| 1 | 16 | 40 | 11 | 11 | 11 | 64 | 8 | 9 | 11 | 10 | 35 | 1 |
| 2 | 23 | 40 | 42 | 14 | 14 | 25 | 12 | 11 | 14 | 10 | 37 | 2 |
| 3 | 30 | 39 | 41 | 15 | 15 | 17 | 13 | 12 | 15 | 12 | 41 | 2 |
| 4 | 36 | 34 | 36 | 18 | 18 | 19 | 15 | 17 | 18 | 30 | 48 | 2 |
| 5 | 18 | 29 | 30 | 18 | 18 | 26 | 15 | 17 | 18 | 30 | 48 | 2 |
| 6 | 25 | 27 | 28 | 19 | 19 | 22 | 16 | 17 | 19 | 31 | 49 | 2 |
| 7 | 28 | 24 | 25 | 19 | 19 | 27 | 16 | 17 | 19 | 32 | 51 | 1 |
| 8 | 28 | 24 | 25 | 19 | 19 | 27 | 16 | 17 | 19 | 32 | 51 | 1 |
| 9 | 28 | 24 | 25 | 19 | 19 | 27 | 16 | 17 | 19 | 32 | 51 | 1 |
| 10 | 28 | 24 | 25 | 19 | 19 | 27 | 16 | 17 | 19 | 32 | 51 | 1 |
| 11 | 19 | 20 | 21 | 19 | 19 | 33 | 16 | 17 | 19 | 32 | 51 | 1 |
| 12 | 21 | 19 | 19 | 19 | 19 | 19 | 16 | 17 | 19 | 32 | 51 | 2 |
| 13 | 21 | 52 | 47 | 19 | 20 | 19 | 17 | 17 | 19 | 16 | 51 | 2 |
| 14 | 19 | 51 | 46 | 19 | 19 | 20 | 16 | 17 | 19 | 16 | 52 | 2 |
| 15 | 19 | 51 | 46 | 19 | 19 | 26 | 16 | 17 | 19 | 16 | 52 | 2 |
| 16 | 20 | 50 | 45 | 20 | 20 | 25 | 17 | 17 | 20 | 16 | 52 | 2 |
| 17 | 20 | 50 | 45 | 20 | 20 | 20 | 17 | 17 | 20 | 16 | 52 | 1 |
| 18 | 21 | 47 | 42 | 20 | 20 | 25 | 17 | 17 | 20 | 16 | 52 | 2 |
| 19 | 22 | 46 | 41 | 20 | 20 | 20 | 17 | 17 | 20 | 17 | 53 | 3 |
| 20 | 22 | 46 | 41 | 20 | 20 | 20 | 17 | 17 | 20 | 17 | 53 | 3 |
| 21 | 23 | 46 | 41 | 21 | 21 | 23 | 18 | 17 | 21 | 17 | 53 | 3 |
| 22 | 21 | 45 | 40 | 21 | 21 | 21 | 18 | 17 | 21 | 18 | 53 | 2 |
| 23 | 21 | 42 | 37 | 21 | 21 | 22 | 18 | 17 | 21 | 18 | 53 | 2 |
| 24 | 21 | 42 | 37 | 21 | 21 | 22 | 18 | 17 | 21 | 18 | 53 | 2 |
| 25 | 21 | 42 | 37 | 21 | 21 | 25 | 18 | 17 | 21 | 18 | 53 | 2 |
| 26 | 21 | 42 | 37 | 21 | 22 | 21 | 18 | 17 | 21 | 19 | 53 | 3 |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
