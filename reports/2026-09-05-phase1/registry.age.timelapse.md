# Time-lapse — uluops-registry-api

*Trunk (first-parent) of 812 commits, HEAD `f7414cc7bbec`; 12 frames (11 mapped, 1 skipped), geometry `age`, ruleset maintainability 0.1.0 (profile maintainability), overlays: onboarding 0.1.0. Gate: `validation.json` at HEAD (substrate fingerprint `80b2a632f8b7`, validated 2026-09-05T02:50:14+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank) | untouched churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 8e2fc8de | 2026-01-17 | 1 | 18 | skipped: population_below_n_min | | | | | | |
| 1 | ad739b6f | 2026-01-23 | 75 | 117 | — | | | | | | |
| 2 | 79f2801b | 2026-01-30 | 148 | 159 | 73 | 42/0 | 39 (0.33) | 27+27 | 35+32 (61/6) | 0.243 / 0.410 | over_budget |
| 3 | 54ff7c77 | 2026-02-23 | 222 | 174 | 74 | 23/8 | 61 (0.40) | 42+24 | 30+31 (48/13) | 0.200 / 0.344 | over_budget |
| 4 | f93a24c5 | 2026-03-31 | 344 | 188 | 122 | 16/2 | 123 (0.72) | 69+8 | 15+10 (23/2) | 0.208 / 0.204 | untested (touched_fraction_exceeds_floor) |
| 5 | 53439c5c | 2026-04-07 | 418 | 200 | 74 | 18/6 | 39 (0.21) | 19+1 | 16+24 (38/2) | 0.090 / 0.168 | over_budget |
| 6 | b325d940 | 2026-04-14 | 491 | 202 | 73 | 6/4 | 58 (0.30) | 20+3 | 34+32 (61/5) | 0.180 / 0.232 | over_budget |
| 7 | 2ed60d62 | 2026-05-04 | 565 | 204 | 74 | 9/7 | 71 (0.36) | 41+7 | 14+37 (45/6) | 0.083 / 0.298 | over_budget |
| 8 | ca0cb8ee | 2026-05-31 | 639 | 218 | 74 | 22/8 | 46 (0.23) | 28+19 | 24+26 (49/1) | 0.111 / 0.173 | over_budget |
| 9 | d8ea567f | 2026-06-24 | 744 | 249 | 105 | 34/3 | 65 (0.30) | 61+16 | 29+49 (66/12) | 0.143 / 0.327 | over_budget |
| 10 | 22aab5c2 | 2026-07-29 | 833 | 262 | 89 | 15/2 | 70 (0.28) | 40+11 | 35+22 (48/9) | 0.160 / 0.124 | over_budget |
| 11 | f7414cc7 | 2026-08-31 | 956 | 267 | 123 | 7/2 | 76 (0.29) | 48+3 | 31+12 (35/8) | 0.132 / 0.065 | over_budget |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals — maintainability/dark_room, maintainability/flooded_basement, maintainability/lit_room — and age-geometry strata: the skeleton reporting time) and *rank* (features over rank-only signals and layer strata: the percentile or the layer moved under a node nobody touched — jitter); *born/del* = structural change. The three together are the movement between frames.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 514 | 0.40 |
| ripple (untouched nodes) | 538 | 0.42 |
| &nbsp;&nbsp;of which clock (time reported) | 474 | 0.37 |
| &nbsp;&nbsp;of which rank (jitter) | 64 | 0.05 |
| structural (born + deleted) | 234 | 0.18 |
| **movement** | **1286** | over 10 transitions, 881 commits |

Budget tally across transitions: over_budget × 9, untested:touched_fraction_exceeds_floor × 1.

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/entrance | onboarding/foundation | onboarding/leaf_utility | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | 12 | 30 | 11 | 12 | 12 | 15 | 4 | 4 | 12 | 14 | 71 |  |
| 2 | 16 | 27 | 27 | 16 | 16 | 31 | 2 | 4 | 16 | 17 | 95 | 1 |
| 3 | 18 | 26 | 27 | 18 | 18 | 18 | 8 | 4 | 18 | 15 | 93 | 1 |
| 4 | 19 | 24 | 18 | 19 | 19 | 26 | 10 | 5 | 19 | 12 | 101 | 1 |
| 5 | 20 | 25 | 20 | 20 | 20 | 42 | 11 | 5 | 20 | 12 | 110 | 1 |
| 6 | 21 | 24 | 36 | 21 | 21 | 23 | 11 | 5 | 21 | 11 | 112 | 1 |
| 7 | 21 | 21 | 29 | 21 | 21 | 40 | 3 | 5 | 21 | 13 | 111 | 1 |
| 8 | 22 | 22 | 27 | 22 | 23 | 31 | 4 | 7 | 22 | 16 | 113 | 1 |
| 9 | 25 | 26 | 29 | 25 | 26 | 46 | 15 | 10 | 25 | 18 | 120 | 1 |
| 10 | 27 | 27 | 28 | 27 | 27 | 32 | 14 | 10 | 27 | 20 | 129 | 1 |
| 11 | 27 | 28 | 28 | 27 | 27 | 40 | 13 | 11 | 27 | 20 | 133 |  |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
