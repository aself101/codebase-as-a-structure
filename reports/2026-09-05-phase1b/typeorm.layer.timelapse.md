# Time-lapse — typeorm

*Trunk (first-parent) of 3804 commits, HEAD `ac41823b9e27`; 12 frames (12 mapped, 0 skipped), geometry `layer`, ruleset maintainability 0.1.0 (profile maintainability), overlays: onboarding 0.1.0. Gate: `validation.json` at HEAD (substrate fingerprint `5f5554e36d4a`, validated 2026-09-05T19:35:20+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank/mixed) | jitter churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 4309b8d8 | 2016-02-21 | 1 | 77 | — | | | | | | |
| 1 | 3c15b7e2 | 2016-12-07 | 551 | 332 | 550 | 285/29 | 47 (1.00) | 174+26 | 0+0 (0/0/0) | 0.000 / 0.000 | untested (beyond_pinned_k) |
| 2 | e381365f | 2017-07-10 | 1155 | 420 | 604 | 124/36 | 277 (0.94) | 272+24 | 28+0 (21/6/1) | 0.304 / 0.000 | untested (beyond_pinned_k) |
| 3 | 6cd98159 | 2017-10-18 | 1715 | 453 | 560 | 38/5 | 261 (0.63) | 188+5 | 94+0 (42/12/40) | 0.359 / 0.000 | untested (beyond_pinned_k) |
| 4 | 651e2ece | 2018-10-20 | 2972 | 522 | 1257 | 92/23 | 284 (0.66) | 162+15 | 126+1 (71/17/39) | 0.474 / 0.007 | untested (beyond_pinned_k) |
| 5 | 9b2ec889 | 2019-06-05 | 3951 | 547 | 979 | 25/0 | 165 (0.32) | 97+5 | 25+0 (11/4/10) | 0.066 / 0.000 | untested (beyond_pinned_k) |
| 6 | 2b378083 | 2020-09-15 | 4325 | 568 | 374 | 21/0 | 213 (0.39) | 106+1 | 32+0 (8/17/7) | 0.108 / 0.000 | untested (beyond_pinned_k) |
| 7 | 1de2e13c | 2021-07-11 | 4671 | 590 | 346 | 24/2 | 284 (0.50) | 116+69 | 40+73 (12/96/5) | 0.139 / 0.259 | untested (beyond_pinned_k) |
| 8 | e24cced8 | 2022-06-22 | 5017 | 637 | 346 | 64/17 | 573 (1.00) | 572+25 | 0+0 (0/0/0) | 0.000 / 0.000 | untested (beyond_pinned_k) |
| 9 | 8ebe7695 | 2024-01-26 | 5363 | 650 | 346 | 15/2 | 198 (0.31) | 197+5 | 44+0 (23/10/11) | 0.067 / 0.000 | untested (beyond_pinned_k) |
| 10 | 8a9a3765 | 2026-01-20 | 5719 | 683 | 356 | 40/7 | 288 (0.45) | 230+8 | 72+0 (12/13/47) | 0.189 / 0.000 | untested (beyond_pinned_k) |
| 11 | ac41823b | 2026-09-02 | 6065 | 583 | 346 | 80/180 | 402 (0.80) | 292+304 | 38+3 (3/12/26) | 0.340 / 0.030 | untested (beyond_pinned_k) |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals only — maintainability/dark_room, maintainability/lit_room — the skeleton reporting time), *rank* (features over rank-only signals, and every floor move of an untouched room: the percentile or the layer moved under a node nobody touched — jitter), and *mixed* (features over a clock and a rank signal together — maintainability/flooded_basement — whose rank component cannot be separated and which the budget therefore counts as jitter); *born/del* = structural change. The four together are the movement between frames. The budget (D-018, operand revised D-024) judges *jitter* = rank + mixed churn and strata moves over untouched rooms, only at K ≤ 10; beyond that it is `untested: beyond_pinned_k` and the numbers stand on their own.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 2893 | 0.63 |
| ripple (untouched nodes) | 576 | 0.13 |
| &nbsp;&nbsp;of which clock (time reported) | 203 | 0.04 |
| &nbsp;&nbsp;of which rank (jitter) | 187 | 0.04 |
| &nbsp;&nbsp;of which mixed (counted as jitter) | 186 | 0.04 |
| **jitter (rank + mixed)** | **373** | **0.08** at median K = 374 |
| structural (born + deleted) | 1109 | 0.24 |
| **movement** | **4578** | over 11 transitions, 6064 commits |

Budget tally across transitions: untested:beyond_pinned_k × 11.

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/entrance | onboarding/foundation | onboarding/leaf_utility | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 77 | 77 | 77 | 8 | 8 | 77 | 4 | 5 | 8 | 9 |  | 8 |
| 1 | 34 | 35 | 33 | 34 | 34 | 91 | 21 | 9 | 34 | 22 | 64 | 5 |
| 2 | 42 | 82 | 43 | 42 | 42 | 48 | 26 | 20 | 42 | 26 | 91 | 6 |
| 3 | 46 | 60 | 46 | 46 | 48 | 46 | 26 | 19 | 46 | 34 | 99 | 6 |
| 4 | 53 | 95 | 53 | 53 | 53 | 53 | 31 | 19 | 53 | 32 | 121 | 5 |
| 5 | 55 | 91 | 53 | 55 | 56 | 59 | 33 | 19 | 55 | 31 | 133 | 4 |
| 6 | 57 | 88 | 57 | 57 | 57 | 60 | 34 | 19 | 57 | 34 | 152 | 5 |
| 7 | 60 | 82 | 58 | 59 | 61 | 59 | 36 | 11 | 59 | 25 | 159 | 3 |
| 8 | 64 | 475 | 64 | 64 | 66 | 68 | 38 | 11 | 64 | 31 | 157 | 5 |
| 9 | 65 | 371 | 65 | 65 | 65 | 67 | 39 | 11 | 65 | 32 | 166 | 4 |
| 10 | 69 | 259 | 69 | 69 | 70 | 69 | 40 | 13 | 69 | 31 | 164 | 6 |
| 11 | 59 | 70 | 59 | 59 | 60 | 60 | 37 | 1 | 59 | 33 | 164 | 2 |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
