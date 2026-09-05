# Time-lapse — typeorm

*Trunk (first-parent) of 3804 commits, HEAD `ac41823b9e27`; 12 frames (12 mapped, 0 skipped), geometry `layer`, ruleset maintainability 0.1.0 (profile maintainability), overlays: onboarding 0.1.0. Gate: `validation.json` at HEAD (substrate fingerprint `80b2a632f8b7`, validated 2026-09-05T02:50:14+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank) | untouched churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 4309b8d8 | 2016-02-21 | 1 | 77 | — | | | | | | |
| 1 | 3c15b7e2 | 2016-12-07 | 551 | 332 | 550 | 285/29 | 47 (1.00) | 174+16 | 0+0 (0/0) | 0.000 / 0.000 | untested (insufficient_untouched_population) |
| 2 | e381365f | 2017-07-10 | 1155 | 420 | 604 | 124/36 | 277 (0.94) | 279+17 | 28+0 (22/6) | 0.560 / 0.000 | untested (insufficient_untouched_population) |
| 3 | 6cd98159 | 2017-10-18 | 1715 | 453 | 560 | 38/5 | 261 (0.63) | 189+5 | 94+0 (82/12) | 0.450 / 0.000 | untested (touched_fraction_exceeds_floor) |
| 4 | 651e2ece | 2018-10-20 | 2972 | 522 | 1257 | 92/23 | 284 (0.66) | 163+12 | 127+1 (111/17) | 0.596 / 0.007 | untested (touched_fraction_exceeds_floor) |
| 5 | 9b2ec889 | 2019-06-05 | 3951 | 547 | 979 | 25/0 | 165 (0.32) | 97+5 | 25+0 (21/4) | 0.079 / 0.000 | over_budget |
| 6 | 2b378083 | 2020-09-15 | 4325 | 568 | 374 | 21/0 | 213 (0.39) | 115+1 | 35+0 (18/17) | 0.109 / 0.000 | over_budget |
| 7 | 1de2e13c | 2021-07-11 | 4671 | 590 | 346 | 24/2 | 284 (0.50) | 130+69 | 40+73 (17/96) | 0.134 / 0.259 | untested (touched_fraction_exceeds_floor) |
| 8 | e24cced8 | 2022-06-22 | 5017 | 637 | 346 | 64/17 | 573 (1.00) | 574+25 | 0+0 (0/0) | 0.000 / 0.000 | untested (insufficient_untouched_population) |
| 9 | 8ebe7695 | 2024-01-26 | 5363 | 650 | 346 | 15/2 | 198 (0.31) | 205+5 | 44+0 (34/10) | 0.062 / 0.000 | over_budget |
| 10 | 8a9a3765 | 2026-01-20 | 5719 | 683 | 356 | 40/7 | 288 (0.45) | 222+8 | 73+0 (60/13) | 0.124 / 0.000 | over_budget |
| 11 | ac41823b | 2026-09-02 | 6065 | 583 | 346 | 80/180 | 402 (0.80) | 313+285 | 41+3 (32/12) | 0.229 / 0.030 | untested (touched_fraction_exceeds_floor) |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals — maintainability/dark_room, maintainability/flooded_basement, maintainability/lit_room — and age-geometry strata: the skeleton reporting time) and *rank* (features over rank-only signals and layer strata: the percentile or the layer moved under a node nobody touched — jitter); *born/del* = structural change. The three together are the movement between frames.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 2909 | 0.63 |
| ripple (untouched nodes) | 584 | 0.13 |
| &nbsp;&nbsp;of which clock (time reported) | 397 | 0.09 |
| &nbsp;&nbsp;of which rank (jitter) | 187 | 0.04 |
| structural (born + deleted) | 1109 | 0.24 |
| **movement** | **4602** | over 11 transitions, 6064 commits |

Budget tally across transitions: over_budget × 4, untested:insufficient_untouched_population × 3, untested:touched_fraction_exceeds_floor × 4.

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/entrance | onboarding/foundation | onboarding/leaf_utility | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 77 | 77 | 77 | 8 | 8 | 77 | 4 | 5 | 8 | 9 |  | 8 |
| 1 | 34 | 35 | 34 | 34 | 34 | 92 | 21 | 9 | 34 | 22 | 64 | 5 |
| 2 | 42 | 82 | 46 | 42 | 42 | 53 | 26 | 20 | 42 | 26 | 91 | 6 |
| 3 | 47 | 60 | 46 | 46 | 48 | 47 | 26 | 19 | 46 | 34 | 99 | 6 |
| 4 | 53 | 96 | 53 | 53 | 53 | 53 | 31 | 19 | 53 | 32 | 121 | 6 |
| 5 | 55 | 92 | 53 | 55 | 56 | 59 | 33 | 19 | 55 | 31 | 133 | 4 |
| 6 | 57 | 89 | 58 | 57 | 57 | 73 | 34 | 19 | 57 | 34 | 152 | 5 |
| 7 | 60 | 83 | 58 | 59 | 61 | 64 | 36 | 11 | 59 | 25 | 159 | 3 |
| 8 | 64 | 475 | 64 | 64 | 66 | 68 | 38 | 11 | 64 | 31 | 157 | 5 |
| 9 | 66 | 371 | 65 | 65 | 65 | 91 | 39 | 11 | 65 | 32 | 166 | 4 |
| 10 | 69 | 259 | 69 | 69 | 70 | 109 | 40 | 13 | 69 | 31 | 164 | 6 |
| 11 | 59 | 70 | 59 | 59 | 60 | 63 | 37 | 1 | 59 | 33 | 164 | 2 |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
