# Time-lapse — mcp-secure-server

*Trunk (first-parent) of 134 commits, HEAD `ecb30716b87e`; 12 frames (12 mapped, 0 skipped), geometry `age`, ruleset maintainability 0.1.0 (profile maintainability), overlays: onboarding 0.1.0. Gate: `validation.json` at HEAD (substrate fingerprint `5f5554e36d4a`, validated 2026-09-05T19:35:20+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank) | untouched churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | fd0cfbeb | 2025-12-10 | 1 | 39 | — | | | | | | |
| 1 | 455fe055 | 2025-12-14 | 14 | 112 | 13 | 97/24 | 14 (0.93) | 28+1 | 1+1 (2/0) | 0.333 / 1.000 | untested (insufficient_untouched_population) |
| 2 | d3e32dbe | 2025-12-15 | 26 | 180 | 12 | 68/0 | 8 (0.07) | 10+7 | 65+90 (139/16) | 0.314 / 0.865 | over_budget |
| 3 | c40e182c | 2025-12-20 | 38 | 181 | 12 | 2/1 | 31 (0.17) | 43+0 | 22+4 (16/10) | 0.109 / 0.027 | over_budget |
| 4 | 6f7ea8a2 | 2025-12-20 | 50 | 181 | 12 | 0/0 | 1 (0.01) | 0+0 | 0+0 (0/0) | 0.000 / 0.000 | within_budget |
| 5 | 96933e1b | 2026-01-02 | 62 | 181 | 12 | 0/0 | 11 (0.06) | 18+0 | 15+0 (15/0) | 0.067 / 0.000 | over_budget |
| 6 | 134e712b | 2026-01-07 | 75 | 188 | 13 | 7/0 | 15 (0.08) | 18+0 | 100+0 (77/23) | 0.376 / 0.000 | over_budget |
| 7 | 99d792bd | 2026-01-09 | 87 | 195 | 12 | 7/0 | 23 (0.12) | 19+7 | 20+71 (85/6) | 0.083 / 0.430 | over_budget |
| 8 | 20408558 | 2026-01-09 | 99 | 197 | 12 | 2/0 | 17 (0.09) | 26+0 | 28+0 (22/6) | 0.112 / 0.000 | over_budget |
| 9 | 3f55fd47 | 2026-01-11 | 111 | 201 | 12 | 4/0 | 14 (0.07) | 12+0 | 9+0 (7/2) | 0.036 / 0.000 | within_budget |
| 10 | 3f6fd83d | 2026-04-04 | 123 | 202 | 12 | 1/0 | 13 (0.06) | 11+0 | 10+0 (9/1) | 0.040 / 0.000 | within_budget |
| 11 | ecb30716 | 2026-08-24 | 139 | 202 | 16 | 0/0 | 18 (0.09) | 13+0 | 14+0 (13/1) | 0.059 / 0.000 | over_budget |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals — maintainability/dark_room, maintainability/flooded_basement, maintainability/lit_room — and age-geometry strata: the skeleton reporting time) and *rank* (features over rank-only signals and layer strata: the percentile or the layer moved under a node nobody touched — jitter); *born/del* = structural change. The three together are the movement between frames.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 213 | 0.24 |
| ripple (untouched nodes) | 450 | 0.51 |
| &nbsp;&nbsp;of which clock (time reported) | 385 | 0.44 |
| &nbsp;&nbsp;of which rank (jitter) | 65 | 0.07 |
| structural (born + deleted) | 213 | 0.24 |
| **movement** | **876** | over 11 transitions, 138 commits |

Budget tally across transitions: over_budget × 7, untested:insufficient_untouched_population × 1, within_budget × 3.

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/entrance | onboarding/foundation | onboarding/leaf_utility | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 39 | 39 | 39 | 4 | 4 | 39 | 2 |  | 4 | 5 | 10 | 1 |
| 1 | 23 | 40 | 12 | 12 | 12 | 25 | 10 | 10 | 12 | 10 | 35 | 2 |
| 2 | 37 | 34 | 36 | 18 | 18 | 19 | 15 | 17 | 18 | 30 | 48 | 2 |
| 3 | 28 | 24 | 25 | 19 | 19 | 27 | 16 | 17 | 19 | 32 | 51 | 1 |
| 4 | 28 | 24 | 25 | 19 | 19 | 27 | 16 | 17 | 19 | 32 | 51 | 1 |
| 5 | 20 | 19 | 20 | 19 | 19 | 20 | 16 | 17 | 19 | 32 | 51 | 2 |
| 6 | 19 | 51 | 46 | 19 | 19 | 20 | 16 | 17 | 19 | 16 | 52 | 2 |
| 7 | 21 | 50 | 45 | 20 | 20 | 30 | 17 | 17 | 20 | 16 | 52 | 2 |
| 8 | 22 | 47 | 42 | 20 | 20 | 22 | 17 | 17 | 20 | 17 | 53 | 3 |
| 9 | 21 | 45 | 40 | 21 | 21 | 25 | 18 | 17 | 21 | 17 | 53 | 3 |
| 10 | 21 | 42 | 37 | 21 | 21 | 22 | 18 | 17 | 21 | 18 | 53 | 2 |
| 11 | 21 | 42 | 37 | 21 | 22 | 21 | 18 | 17 | 21 | 19 | 53 | 3 |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
