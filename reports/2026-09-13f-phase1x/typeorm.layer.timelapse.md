# Time-lapse — typeorm

*Trunk (first-parent) of 3804 commits, HEAD `ac41823b9e27`; 12 frames (12 mapped, 0 skipped), geometry `layer`, ruleset maintainability 0.3.2 (profile maintainability), overlays: onboarding 0.3.0. Gate: `validation.json` at HEAD (substrate fingerprint `84bae11b50a7`, validated 2026-09-14T00:15:02+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank/mixed) | jitter churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 4309b8d8 | 2016-02-21 | 1 | 77 | — | | | | | | |
| 1 | 3c15b7e2 | 2016-12-07 | 551 | 332 | 550 | 285/29 | 47 (1.00) | 184+26 | 0+0 (0/0/0) | 0.000 / 0.000 | untested (beyond_pinned_k) |
| 2 | e381365f | 2017-07-10 | 1155 | 420 | 604 | 118/36 | 277 (0.94) | 292+24 | 40+0 (21/6/13) | 0.487 / 0.000 | untested (beyond_pinned_k) |
| 3 | 6cd98159 | 2017-10-18 | 1715 | 453 | 560 | 38/5 | 258 (0.63) | 210+5 | 94+0 (42/14/38) | 0.329 / 0.000 | untested (beyond_pinned_k) |
| 4 | 651e2ece | 2018-10-20 | 2972 | 522 | 1257 | 92/22 | 282 (0.66) | 157+15 | 149+1 (68/15/67) | 0.516 / 0.007 | untested (beyond_pinned_k) |
| 5 | 9b2ec889 | 2019-06-05 | 3951 | 547 | 979 | 25/0 | 164 (0.32) | 95+5 | 13+0 (11/2/0) | 0.008 / 0.000 | untested (beyond_pinned_k) |
| 6 | 2b378083 | 2020-09-15 | 4325 | 568 | 374 | 20/0 | 211 (0.39) | 98+1 | 28+0 (8/20/0) | 0.078 / 0.000 | untested (beyond_pinned_k) |
| 7 | 1de2e13c | 2021-07-11 | 4671 | 590 | 346 | 24/2 | 283 (0.51) | 119+69 | 38+71 (11/98/0) | 0.123 / 0.256 | untested (beyond_pinned_k) |
| 8 | e24cced8 | 2022-06-22 | 5017 | 637 | 346 | 63/16 | 568 (1.00) | 865+25 | 0+0 (0/0/0) | 0.000 / 0.000 | untested (beyond_pinned_k) |
| 9 | 8ebe7695 | 2024-01-26 | 5363 | 650 | 346 | 15/2 | 195 (0.31) | 284+5 | 33+0 (23/10/0) | 0.016 / 0.000 | untested (beyond_pinned_k) |
| 10 | 8a9a3765 | 2026-01-20 | 5719 | 683 | 356 | 38/6 | 287 (0.45) | 287+8 | 27+0 (12/15/0) | 0.030 / 0.000 | untested (beyond_pinned_k) |
| 11 | ac41823b | 2026-09-02 | 6065 | 583 | 346 | 76/178 | 397 (0.80) | 410+299 | 12+3 (3/12/0) | 0.064 / 0.030 | untested (beyond_pinned_k) |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals only — maintainability/dark_room, maintainability/lit_room — the skeleton reporting time), *rank* (features over rank-only signals, and every floor move of an untouched room: the percentile or the layer moved under a node nobody touched — jitter), and *mixed* (features over a clock and a rank signal together — maintainability/flooded_basement — whose rank component cannot be separated and which the budget therefore counts as jitter); *born/del* = structural change. The four together are the movement between frames. The budget (D-018, operand revised D-024) judges *jitter* = rank + mixed churn and strata moves over untouched rooms, only at K ≤ 50; beyond that it is `untested: beyond_pinned_k` and the numbers stand on their own.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 3483 | 0.69 |
| ripple (untouched nodes) | 509 | 0.10 |
| &nbsp;&nbsp;of which clock (time reported) | 199 | 0.04 |
| &nbsp;&nbsp;of which rank (jitter) | 192 | 0.04 |
| &nbsp;&nbsp;of which mixed (counted as jitter) | 118 | 0.02 |
| **jitter (rank + mixed)** | **310** | **0.06** at median K = 374 |
| structural (born + deleted) | 1090 | 0.21 |
| **movement** | **5082** | over 11 transitions, 6064 commits |

Budget tally across transitions: untested:beyond_pinned_k × 11. **Budget reading: no verdict** — 0 of 11 transitions judged (coverage 0.00); a run the budget could not judge at all says nothing about stability (D-030).

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/foundation | onboarding/import_root | onboarding/leaf_utility | onboarding/package_entry | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 77 | 77 | 77 | 8 | 8 | 77 | 4 | 8 | 5 | 9 |  |  | 8 |
| 1 | 34 | 35 | 35 | 34 | 34 | 91 | 21 | 34 | 9 | 22 | 1 | 64 | 5 |
| 2 | 42 | 81 | 81 | 42 | 42 | 47 | 26 | 42 | 20 | 26 | 1 | 91 | 6 |
| 3 | 45 | 59 | 59 | 45 | 48 | 45 | 26 | 45 | 19 | 34 | 2 | 99 | 6 |
| 4 | 52 | 92 | 92 | 52 | 52 | 53 | 30 | 52 | 19 | 32 | 1 | 121 | 5 |
| 5 | 55 | 88 | 88 | 55 | 56 | 58 | 33 | 55 | 19 | 31 | 2 | 131 | 4 |
| 6 | 57 | 86 | 86 | 57 | 58 | 59 | 35 | 57 | 19 | 34 | 2 | 150 | 5 |
| 7 | 59 | 80 | 80 | 59 | 60 | 59 | 32 | 59 | 11 | 25 | 2 | 157 | 4 |
| 8 | 64 | 470 | 470 | 64 | 65 | 67 | 38 | 64 | 11 | 31 | 4 | 155 | 5 |
| 9 | 65 | 368 | 368 | 65 | 65 | 67 | 39 | 65 | 11 | 32 | 4 | 164 | 4 |
| 10 | 68 | 257 | 257 | 68 | 69 | 70 | 40 | 68 | 13 | 31 | 5 | 162 | 6 |
| 11 | 58 | 70 | 70 | 58 | 59 | 58 | 37 | 58 | 1 | 33 | 6 | 162 | 2 |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
