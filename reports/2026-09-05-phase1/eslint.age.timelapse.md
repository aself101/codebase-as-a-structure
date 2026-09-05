# Time-lapse — eslint

*Trunk (first-parent) of 8677 commits, HEAD `3f20a57c6293`; 12 frames (11 mapped, 1 skipped), geometry `age`, ruleset maintainability 0.1.0 (profile maintainability), overlays: onboarding 0.1.0. Gate: `validation.json` at HEAD (substrate fingerprint `80b2a632f8b7`, validated 2026-09-05T02:50:14+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank) | untouched churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | a658d7b0 | 2013-06-29 | 1 | 12 | skipped: population_below_n_min | | | | | | |
| 1 | fb6442e0 | 2014-11-11 | 1608 | 163 | — | | | | | | |
| 2 | 67e8f169 | 2015-08-27 | 3089 | 211 | 1481 | 58/10 | 147 (0.96) | 367+86 | 16+4 (15/5) | 0.410 / 0.667 | untested (insufficient_untouched_population) |
| 3 | 61a3025f | 2016-03-28 | 4613 | 269 | 1524 | 64/6 | 165 (0.80) | 217+100 | 22+21 (39/4) | 0.162 / 0.525 | untested (touched_fraction_exceeds_floor) |
| 4 | 9679daa8 | 2016-12-12 | 5487 | 307 | 874 | 38/0 | 269 (1.00) | 264+71 | 0+0 (0/0) | 0.000 / 0.000 | untested (insufficient_untouched_population) |
| 5 | ea1b15d3 | 2018-01-09 | 6276 | 353 | 789 | 49/3 | 298 (0.98) | 458+89 | 4+5 (9/0) | 0.143 / 0.833 | untested (insufficient_untouched_population) |
| 6 | 4c0b70b8 | 2019-08-31 | 7064 | 385 | 788 | 42/10 | 342 (1.00) | 460+50 | 1+0 (1/0) | 0.333 / 0.000 | untested (insufficient_untouched_population) |
| 7 | d6c84af6 | 2021-02-10 | 7853 | 393 | 789 | 21/13 | 295 (0.79) | 197+19 | 93+2 (82/13) | 0.354 / 0.026 | untested (touched_fraction_exceeds_floor) |
| 8 | c3ce5212 | 2022-11-04 | 8642 | 424 | 789 | 40/9 | 342 (0.89) | 176+65 | 35+5 (29/11) | 0.259 / 0.119 | untested (touched_fraction_exceeds_floor) |
| 9 | b07d4278 | 2024-03-30 | 9431 | 447 | 789 | 42/19 | 347 (0.86) | 172+68 | 36+12 (39/9) | 0.257 / 0.207 | untested (touched_fraction_exceeds_floor) |
| 10 | 677a2837 | 2025-06-10 | 10219 | 467 | 788 | 32/12 | 434 (1.00) | 213+45 | 0+0 (0/0) | 0.000 / 0.000 | untested (insufficient_untouched_population) |
| 11 | 3f20a57c | 2026-09-04 | 11008 | 473 | 789 | 16/10 | 281 (0.61) | 161+15 | 56+12 (48/20) | 0.139 / 0.068 | untested (touched_fraction_exceeds_floor) |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals — maintainability/dark_room, maintainability/flooded_basement, maintainability/lit_room — and age-geometry strata: the skeleton reporting time) and *rank* (features over rank-only signals and layer strata: the percentile or the layer moved under a node nobody touched — jitter); *born/del* = structural change. The three together are the movement between frames.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 3293 | 0.80 |
| ripple (untouched nodes) | 324 | 0.08 |
| &nbsp;&nbsp;of which clock (time reported) | 262 | 0.06 |
| &nbsp;&nbsp;of which rank (jitter) | 62 | 0.02 |
| structural (born + deleted) | 494 | 0.12 |
| **movement** | **4111** | over 10 transitions, 9400 commits |

Budget tally across transitions: untested:insufficient_untouched_population × 5, untested:touched_fraction_exceeds_floor × 5.

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/entrance | onboarding/foundation | onboarding/leaf_utility | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | 17 | 21 | 17 | 17 | 18 | 18 | 18 | 145 | 17 | 155 | 13 | 2 |
| 2 | 22 | 81 | 20 | 22 | 30 | 23 | 30 | 4 | 22 | 179 | 201 | 3 |
| 3 | 28 | 28 | 27 | 27 | 27 | 131 | 27 | 2 | 27 | 197 | 256 |  |
| 4 | 31 | 107 | 31 | 31 | 31 | 31 | 31 | 2 | 31 | 198 | 290 |  |
| 5 | 38 | 36 | 34 | 36 | 38 | 265 | 38 | 3 | 36 | 173 | 322 |  |
| 6 | 39 | 61 | 39 | 39 | 40 | 39 | 40 | 3 | 39 | 164 | 337 |  |
| 7 | 41 | 71 | 40 | 40 | 45 | 40 | 22 | 3 | 40 | 152 | 348 |  |
| 8 | 44 | 43 | 42 | 43 | 43 | 53 | 24 | 3 | 43 | 148 | 351 |  |
| 9 | 45 | 46 | 45 | 45 | 48 | 47 | 24 | 10 | 45 | 147 | 348 |  |
| 10 | 49 | 129 | 47 | 47 | 53 | 47 | 26 | 14 | 47 | 149 | 357 | 1 |
| 11 | 48 | 83 | 48 | 48 | 50 | 48 | 22 | 19 | 48 | 148 | 371 | 1 |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
