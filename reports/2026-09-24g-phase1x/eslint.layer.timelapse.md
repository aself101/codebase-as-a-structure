# Time-lapse — eslint

*Trunk (first-parent) of 8677 commits, HEAD `3f20a57c6293`; 12 frames (11 mapped, 1 skipped), geometry `layer`, ruleset maintainability 0.3.4 (profile maintainability), overlays: onboarding 0.3.1. Gate: `validation.json` at HEAD (substrate fingerprint `298696064105`, validated 2026-09-24T22:58:00+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank/mixed) | jitter churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | a658d7b0 | 2013-06-29 | 1 | 12 | skipped: population_below_n_min | | | | | | |
| 1 | fb6442e0 | 2014-11-11 | 1608 | 163 | — | | | | | | |
| 2 | 67e8f169 | 2015-08-27 | 3089 | 211 | 1481 | 58/10 | 147 (0.96) | 414+7 | 17+0 (7/5/5) | 0.303 / 0.000 | untested (beyond_pinned_k) |
| 3 | 61a3025f | 2016-03-28 | 4613 | 269 | 1524 | 64/6 | 165 (0.80) | 249+139 | 6+37 (2/41/0) | 0.035 / 0.925 | untested (beyond_pinned_k) |
| 4 | 9679daa8 | 2016-12-12 | 5487 | 307 | 874 | 37/0 | 269 (1.00) | 314+70 | 0+0 (0/0/0) | 0.000 / 0.000 | untested (beyond_pinned_k) |
| 5 | ea1b15d3 | 2018-01-09 | 6276 | 353 | 789 | 48/3 | 297 (0.98) | 521+47 | 3+0 (2/0/1) | 0.040 / 0.000 | untested (beyond_pinned_k) |
| 6 | 4c0b70b8 | 2019-08-31 | 7064 | 385 | 788 | 41/10 | 340 (1.00) | 502+30 | 2+0 (1/0/1) | 0.333 / 0.000 | untested (beyond_pinned_k) |
| 7 | d6c84af6 | 2021-02-10 | 7853 | 393 | 789 | 21/13 | 292 (0.79) | 196+22 | 119+0 (61/1/57) | 0.265 / 0.000 | untested (beyond_pinned_k) |
| 8 | c3ce5212 | 2022-11-04 | 8642 | 424 | 789 | 38/9 | 339 (0.89) | 172+7 | 47+0 (17/13/17) | 0.252 / 0.000 | untested (beyond_pinned_k) |
| 9 | b07d4278 | 2024-03-30 | 9431 | 447 | 789 | 33/18 | 345 (0.86) | 139+17 | 50+0 (25/9/16) | 0.210 / 0.000 | untested (beyond_pinned_k) |
| 10 | 677a2837 | 2025-06-10 | 10219 | 467 | 788 | 31/9 | 425 (1.00) | 223+8 | 0+0 (0/0/0) | 0.000 / 0.000 | untested (beyond_pinned_k) |
| 11 | 3f20a57c | 2026-09-04 | 11008 | 473 | 789 | 16/10 | 278 (0.62) | 162+11 | 30+0 (3/22/5) | 0.079 / 0.000 | untested (beyond_pinned_k) |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals only — maintainability/dark_room, maintainability/lit_room — the skeleton reporting time), *rank* (features over rank-only signals, and every floor move of an untouched room: the percentile or the layer moved under a node nobody touched — jitter), and *mixed* (features over a clock and a rank signal together — maintainability/flooded_basement — whose rank component cannot be separated and which the budget therefore counts as jitter); *born/del* = structural change. The four together are the movement between frames. The budget (D-018, operand revised D-024) judges *jitter* = rank + mixed churn and strata moves over untouched rooms, only at K ≤ 50; beyond that it is `untested: beyond_pinned_k` and the numbers stand on their own.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 3250 | 0.81 |
| ripple (untouched nodes) | 311 | 0.08 |
| &nbsp;&nbsp;of which clock (time reported) | 118 | 0.03 |
| &nbsp;&nbsp;of which rank (jitter) | 91 | 0.02 |
| &nbsp;&nbsp;of which mixed (counted as jitter) | 102 | 0.03 |
| **jitter (rank + mixed)** | **193** | **0.05** at median K = 789 |
| structural (born + deleted) | 475 | 0.12 |
| **movement** | **4036** | over 10 transitions, 9400 commits |

Budget tally across transitions: untested:beyond_pinned_k × 10. **Budget reading: no verdict** — 0 of 10 transitions judged (coverage 0.00); a run the budget could not judge at all says nothing about stability (D-030).

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/foundation | onboarding/import_root | onboarding/leaf_utility | onboarding/package_entry | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | 17 | 21 | 21 | 17 | 18 | 17 | 18 | 17 | 145 | 155 | 2 | 13 | 2 |
| 2 | 22 | 81 | 79 | 22 | 30 | 22 | 30 | 22 | 4 | 179 | 2 | 201 | 3 |
| 3 | 28 | 28 | 28 | 27 | 27 | 131 | 27 | 27 | 2 | 197 | 2 | 256 |  |
| 4 | 31 | 105 | 105 | 31 | 31 | 31 | 31 | 31 | 2 | 198 | 2 | 290 |  |
| 5 | 38 | 36 | 35 | 36 | 38 | 265 | 38 | 36 | 3 | 173 | 2 | 322 |  |
| 6 | 39 | 61 | 61 | 39 | 40 | 39 | 19 | 39 | 3 | 164 | 2 | 337 |  |
| 7 | 39 | 71 | 67 | 39 | 39 | 39 | 21 | 39 | 3 | 152 | 2 | 348 |  |
| 8 | 42 | 42 | 38 | 42 | 43 | 52 | 24 | 42 | 3 | 148 | 3 | 351 |  |
| 9 | 44 | 44 | 34 | 44 | 47 | 44 | 23 | 44 | 9 | 144 | 7 | 346 |  |
| 10 | 48 | 118 | 105 | 46 | 46 | 46 | 23 | 46 | 11 | 146 | 10 | 356 | 1 |
| 11 | 47 | 75 | 69 | 47 | 49 | 47 | 23 | 47 | 16 | 146 | 10 | 370 | 1 |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
