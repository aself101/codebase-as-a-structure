# Time-lapse — typeorm

*Trunk (first-parent) of 3804 commits, HEAD `ac41823b9e27`; 12 frames (12 mapped, 0 skipped), geometry `age`, ruleset maintainability 0.2.0 (profile maintainability), overlays: onboarding 0.2.0. Gate: `validation.json` at HEAD (substrate fingerprint `179d8acb7b0c`, validated 2026-09-06T18:48:13+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank/mixed) | jitter churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 4309b8d8 | 2016-02-21 | 1 | 77 | — | | | | | | |
| 1 | 3c15b7e2 | 2016-12-07 | 551 | 332 | 550 | 285/29 | 47 (1.00) | 184+47 | 0+0 (0/0/0) | 0.000 / 0.000 | untested (beyond_pinned_k) |
| 2 | e381365f | 2017-07-10 | 1155 | 420 | 604 | 124/36 | 277 (0.94) | 292+156 | 40+16 (21/22/13) | 0.487 / 0.842 | untested (beyond_pinned_k) |
| 3 | 6cd98159 | 2017-10-18 | 1715 | 453 | 560 | 38/5 | 261 (0.63) | 212+48 | 92+32 (42/44/38) | 0.314 / 0.208 | untested (beyond_pinned_k) |
| 4 | 651e2ece | 2018-10-20 | 2972 | 522 | 1257 | 92/23 | 284 (0.66) | 162+112 | 157+63 (71/79/70) | 0.531 / 0.432 | untested (beyond_pinned_k) |
| 5 | 9b2ec889 | 2019-06-05 | 3951 | 547 | 979 | 25/0 | 165 (0.32) | 96+23 | 17+26 (11/30/2) | 0.024 / 0.073 | untested (beyond_pinned_k) |
| 6 | 2b378083 | 2020-09-15 | 4325 | 568 | 374 | 21/0 | 213 (0.39) | 106+17 | 26+21 (8/38/1) | 0.071 / 0.063 | untested (beyond_pinned_k) |
| 7 | 1de2e13c | 2021-07-11 | 4671 | 590 | 346 | 24/2 | 284 (0.50) | 118+28 | 35+15 (12/38/0) | 0.103 / 0.053 | untested (beyond_pinned_k) |
| 8 | e24cced8 | 2022-06-22 | 5017 | 637 | 346 | 64/17 | 573 (1.00) | 867+112 | 0+0 (0/0/0) | 0.000 / 0.000 | untested (beyond_pinned_k) |
| 9 | 8ebe7695 | 2024-01-26 | 5363 | 650 | 346 | 15/2 | 198 (0.31) | 289+8 | 33+18 (23/28/0) | 0.016 / 0.041 | untested (beyond_pinned_k) |
| 10 | 8a9a3765 | 2026-01-20 | 5719 | 683 | 356 | 40/7 | 288 (0.45) | 292+38 | 25+37 (12/50/0) | 0.026 / 0.104 | untested (beyond_pinned_k) |
| 11 | ac41823b | 2026-09-02 | 6065 | 583 | 346 | 80/180 | 402 (0.80) | 408+252 | 12+71 (3/80/0) | 0.064 / 0.703 | untested (beyond_pinned_k) |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals only — maintainability/dark_room, maintainability/lit_room — the skeleton reporting time), *rank* (features over rank-only signals, and every floor move of an untouched room: the percentile or the layer moved under a node nobody touched — jitter), and *mixed* (features over a clock and a rank signal together — maintainability/flooded_basement — whose rank component cannot be separated and which the budget therefore counts as jitter); *born/del* = structural change. The four together are the movement between frames. The budget (D-018, operand revised D-024) judges *jitter* = rank + mixed churn and strata moves over untouched rooms, only at K ≤ 50; beyond that it is `untested: beyond_pinned_k` and the numbers stand on their own.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 3867 | 0.68 |
| ripple (untouched nodes) | 736 | 0.13 |
| &nbsp;&nbsp;of which clock (time reported) | 203 | 0.04 |
| &nbsp;&nbsp;of which rank (jitter) | 409 | 0.07 |
| &nbsp;&nbsp;of which mixed (counted as jitter) | 124 | 0.02 |
| **jitter (rank + mixed)** | **533** | **0.09** at median K = 374 |
| structural (born + deleted) | 1109 | 0.19 |
| **movement** | **5712** | over 11 transitions, 6064 commits |

Budget tally across transitions: untested:beyond_pinned_k × 11. **Budget reading: no verdict** — 0 of 11 transitions judged (coverage 0.00); a run the budget could not judge at all says nothing about stability (D-030).

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/foundation | onboarding/import_root | onboarding/leaf_utility | onboarding/package_entry | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 77 | 77 | 77 | 8 | 8 | 77 | 4 | 8 | 5 | 9 |  |  | 8 |
| 1 | 34 | 35 | 35 | 34 | 34 | 91 | 21 | 34 | 9 | 22 | 1 | 64 | 5 |
| 2 | 42 | 82 | 82 | 42 | 42 | 48 | 26 | 42 | 20 | 26 | 1 | 91 | 6 |
| 3 | 46 | 60 | 60 | 46 | 48 | 46 | 26 | 46 | 19 | 34 | 2 | 99 | 6 |
| 4 | 53 | 95 | 95 | 53 | 53 | 53 | 31 | 53 | 19 | 32 | 1 | 121 | 5 |
| 5 | 55 | 91 | 89 | 55 | 56 | 59 | 33 | 55 | 19 | 31 | 2 | 133 | 4 |
| 6 | 57 | 88 | 87 | 57 | 57 | 60 | 34 | 57 | 19 | 34 | 2 | 152 | 5 |
| 7 | 60 | 82 | 81 | 59 | 61 | 59 | 36 | 59 | 11 | 25 | 2 | 159 | 3 |
| 8 | 64 | 475 | 475 | 64 | 66 | 68 | 38 | 64 | 11 | 31 | 4 | 157 | 5 |
| 9 | 65 | 371 | 371 | 65 | 65 | 67 | 39 | 65 | 11 | 32 | 4 | 166 | 4 |
| 10 | 69 | 259 | 259 | 69 | 70 | 69 | 40 | 69 | 13 | 31 | 5 | 164 | 6 |
| 11 | 59 | 70 | 70 | 59 | 60 | 60 | 37 | 59 | 1 | 33 | 6 | 164 | 2 |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
