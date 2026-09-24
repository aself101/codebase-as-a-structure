# Time-lapse — typeorm

*Trunk (first-parent) of 3804 commits, HEAD `ac41823b9e27`; 12 frames (12 mapped, 0 skipped), geometry `layer`, ruleset maintainability 0.3.4 (profile maintainability), overlays: onboarding 0.3.1. Gate: `validation.json` at HEAD (substrate fingerprint `298696064105`, validated 2026-09-24T22:58:00+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank/mixed) | jitter churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 4309b8d8 | 2016-02-21 | 1 | 77 | — | | | | | | |
| 1 | 3c15b7e2 | 2016-12-07 | 551 | 332 | 550 | 168/29 | 35 (1.00) | 131+28 | 0+0 (0/0/0) | 0.000 / 0.000 | untested (beyond_pinned_k) |
| 2 | e381365f | 2017-07-10 | 1155 | 420 | 604 | 105/36 | 153 (0.92) | 174+31 | 38+1 (20/7/12) | 0.667 / 0.071 | untested (beyond_pinned_k) |
| 3 | 6cd98159 | 2017-10-18 | 1715 | 453 | 560 | 38/5 | 138 (0.52) | 90+6 | 64+4 (29/14/25) | 0.307 / 0.031 | untested (beyond_pinned_k) |
| 4 | 651e2ece | 2018-10-20 | 2972 | 522 | 1257 | 92/17 | 231 (0.80) | 141+16 | 47+1 (21/7/20) | 0.413 / 0.018 | untested (beyond_pinned_k) |
| 5 | 9b2ec889 | 2019-06-05 | 3951 | 547 | 979 | 25/0 | 161 (0.42) | 83+5 | 31+0 (16/6/9) | 0.109 / 0.000 | untested (beyond_pinned_k) |
| 6 | 2b378083 | 2020-09-15 | 4325 | 568 | 374 | 20/0 | 207 (0.51) | 87+1 | 38+0 (14/17/7) | 0.166 / 0.000 | untested (beyond_pinned_k) |
| 7 | 1de2e13c | 2021-07-11 | 4671 | 590 | 346 | 24/2 | 280 (0.66) | 107+56 | 54+15 (23/32/14) | 0.252 / 0.105 | untested (beyond_pinned_k) |
| 8 | e24cced8 | 2022-06-22 | 5017 | 637 | 346 | 62/14 | 433 (1.00) | 717+27 | 0+0 (0/0/0) | 0.000 / 0.000 | untested (beyond_pinned_k) |
| 9 | 8ebe7695 | 2024-01-26 | 5363 | 650 | 346 | 15/2 | 192 (0.39) | 268+5 | 34+0 (23/11/0) | 0.024 / 0.000 | untested (beyond_pinned_k) |
| 10 | 8a9a3765 | 2026-01-20 | 5719 | 683 | 356 | 18/6 | 192 (0.38) | 150+8 | 21+0 (9/12/0) | 0.029 / 0.000 | untested (beyond_pinned_k) |
| 11 | ac41823b | 2026-09-02 | 6065 | 583 | 346 | 76/25 | 394 (0.80) | 372+81 | 13+1 (2/12/0) | 0.082 / 0.010 | untested (beyond_pinned_k) |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals only — maintainability/dark_room, maintainability/lit_room — the skeleton reporting time), *rank* (features over rank-only signals, and every floor move of an untouched room: the percentile or the layer moved under a node nobody touched — jitter), and *mixed* (features over a clock and a rank signal together — maintainability/flooded_basement — whose rank component cannot be separated and which the budget therefore counts as jitter); *born/del* = structural change. The four together are the movement between frames. The budget (D-018, operand revised D-024) judges *jitter* = rank + mixed churn and strata moves over untouched rooms, only at K ≤ 50; beyond that it is `untested: beyond_pinned_k` and the numbers stand on their own.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 2584 | 0.69 |
| ripple (untouched nodes) | 362 | 0.10 |
| &nbsp;&nbsp;of which clock (time reported) | 157 | 0.04 |
| &nbsp;&nbsp;of which rank (jitter) | 118 | 0.03 |
| &nbsp;&nbsp;of which mixed (counted as jitter) | 87 | 0.02 |
| **jitter (rank + mixed)** | **205** | **0.06** at median K = 374 |
| structural (born + deleted) | 779 | 0.21 |
| **movement** | **3725** | over 11 transitions, 6064 commits |

Budget tally across transitions: untested:beyond_pinned_k × 11. **Budget reading: no verdict** — 0 of 11 transitions judged (coverage 0.00); a run the budget could not judge at all says nothing about stability (D-030).

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/foundation | onboarding/import_root | onboarding/leaf_utility | onboarding/package_entry | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 65 | 65 | 65 | 7 | 7 | 65 | 5 | 7 | 4 | 6 |  |  | 7 |
| 1 | 21 | 22 | 22 | 21 | 21 | 91 | 13 | 21 | 1 | 19 | 1 | 44 | 3 |
| 2 | 28 | 28 | 28 | 28 | 28 | 29 | 17 | 28 | 1 | 17 | 1 | 71 | 3 |
| 3 | 31 | 42 | 42 | 31 | 31 | 31 | 19 | 31 | 1 | 17 | 2 | 79 | 4 |
| 4 | 38 | 38 | 38 | 38 | 38 | 38 | 25 | 38 | 1 | 27 | 1 | 101 | 4 |
| 5 | 42 | 43 | 43 | 41 | 43 | 45 | 26 | 41 | 1 | 20 | 2 | 111 | 2 |
| 6 | 43 | 43 | 43 | 43 | 44 | 47 | 27 | 43 | 1 | 18 | 2 | 130 | 4 |
| 7 | 45 | 47 | 46 | 45 | 46 | 57 | 29 | 45 | 1 | 18 | 2 | 137 | 3 |
| 8 | 50 | 366 | 366 | 50 | 52 | 55 | 32 | 50 | 1 | 21 | 4 | 135 | 4 |
| 9 | 51 | 266 | 266 | 51 | 53 | 51 | 35 | 51 | 1 | 23 | 4 | 144 | 2 |
| 10 | 52 | 219 | 219 | 52 | 53 | 52 | 33 | 52 | 1 | 23 | 4 | 142 | 3 |
| 11 | 58 | 70 | 70 | 58 | 59 | 58 | 37 | 58 | 1 | 33 | 6 | 162 | 2 |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
