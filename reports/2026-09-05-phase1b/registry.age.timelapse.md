# Time-lapse — uluops-registry-api

*Trunk (first-parent) of 812 commits, HEAD `f7414cc7bbec`; 12 frames (11 mapped, 1 skipped), geometry `age`, ruleset maintainability 0.1.0 (profile maintainability), overlays: onboarding 0.1.0. Gate: `validation.json` at HEAD (substrate fingerprint `5f5554e36d4a`, validated 2026-09-05T19:35:20+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank) | untouched churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 8e2fc8de | 2026-01-17 | 1 | 18 | skipped: population_below_n_min | | | | | | |
| 1 | ad739b6f | 2026-01-23 | 75 | 117 | — | | | | | | |
| 2 | 79f2801b | 2026-01-30 | 148 | 159 | 73 | 42/0 | 39 (0.33) | 18+28 | 28+42 (64/6) | 0.212 / 0.538 | over_budget |
| 3 | 54ff7c77 | 2026-02-23 | 222 | 174 | 74 | 23/8 | 61 (0.40) | 42+14 | 36+17 (40/13) | 0.248 / 0.189 | over_budget |
| 4 | f93a24c5 | 2026-03-31 | 344 | 188 | 122 | 16/2 | 123 (0.72) | 65+16 | 16+9 (23/2) | 0.225 / 0.184 | untested (touched_fraction_exceeds_floor) |
| 5 | 53439c5c | 2026-04-07 | 418 | 200 | 74 | 18/6 | 39 (0.21) | 16+3 | 11+26 (35/2) | 0.064 / 0.182 | over_budget |
| 6 | b325d940 | 2026-04-14 | 491 | 202 | 73 | 6/4 | 58 (0.30) | 17+0 | 11+9 (15/5) | 0.067 / 0.065 | over_budget |
| 7 | 2ed60d62 | 2026-05-04 | 565 | 204 | 74 | 9/7 | 71 (0.36) | 28+2 | 30+11 (35/6) | 0.175 / 0.089 | over_budget |
| 8 | ca0cb8ee | 2026-05-31 | 639 | 218 | 74 | 22/8 | 46 (0.23) | 23+22 | 8+43 (50/1) | 0.040 / 0.287 | over_budget |
| 9 | d8ea567f | 2026-06-24 | 744 | 249 | 105 | 34/3 | 65 (0.30) | 47+12 | 21+48 (57/12) | 0.107 / 0.320 | over_budget |
| 10 | 22aab5c2 | 2026-07-29 | 833 | 262 | 89 | 15/2 | 70 (0.28) | 43+6 | 26+14 (31/9) | 0.124 / 0.079 | over_budget |
| 11 | f7414cc7 | 2026-08-31 | 956 | 267 | 123 | 7/2 | 76 (0.29) | 48+3 | 26+10 (28/8) | 0.113 / 0.054 | over_budget |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals — maintainability/dark_room, maintainability/flooded_basement, maintainability/lit_room — and age-geometry strata: the skeleton reporting time) and *rank* (features over rank-only signals and layer strata: the percentile or the layer moved under a node nobody touched — jitter); *born/del* = structural change. The three together are the movement between frames.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 453 | 0.40 |
| ripple (untouched nodes) | 442 | 0.39 |
| &nbsp;&nbsp;of which clock (time reported) | 378 | 0.33 |
| &nbsp;&nbsp;of which rank (jitter) | 64 | 0.06 |
| structural (born + deleted) | 234 | 0.21 |
| **movement** | **1129** | over 10 transitions, 881 commits |

Budget tally across transitions: over_budget × 9, untested:touched_fraction_exceeds_floor × 1.

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/entrance | onboarding/foundation | onboarding/leaf_utility | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | 15 | 17 | 16 | 12 | 12 | 14 | 4 | 4 | 12 | 14 | 71 |  |
| 2 | 16 | 27 | 15 | 16 | 16 | 19 | 2 | 4 | 16 | 17 | 95 | 1 |
| 3 | 18 | 25 | 26 | 18 | 18 | 18 | 8 | 4 | 18 | 15 | 93 | 1 |
| 4 | 20 | 23 | 18 | 19 | 19 | 20 | 10 | 5 | 19 | 12 | 101 | 1 |
| 5 | 20 | 23 | 20 | 20 | 20 | 22 | 11 | 5 | 20 | 12 | 110 | 1 |
| 6 | 21 | 23 | 20 | 21 | 21 | 21 | 11 | 5 | 21 | 11 | 112 | 1 |
| 7 | 21 | 21 | 31 | 21 | 21 | 21 | 3 | 5 | 21 | 13 | 111 | 1 |
| 8 | 22 | 22 | 29 | 22 | 23 | 22 | 4 | 7 | 22 | 16 | 113 | 1 |
| 9 | 25 | 25 | 29 | 25 | 26 | 27 | 15 | 10 | 25 | 18 | 120 | 1 |
| 10 | 27 | 27 | 28 | 27 | 27 | 32 | 14 | 10 | 27 | 20 | 129 | 1 |
| 11 | 27 | 27 | 27 | 27 | 27 | 40 | 13 | 11 | 27 | 20 | 133 |  |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
