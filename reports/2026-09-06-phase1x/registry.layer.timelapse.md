# Time-lapse — uluops-registry-api

*Trunk (first-parent) of 812 commits, HEAD `f7414cc7bbec`; 12 frames (11 mapped, 1 skipped), geometry `layer`, ruleset maintainability 0.2.0 (profile maintainability), overlays: onboarding 0.2.0. Gate: `validation.json` at HEAD (substrate fingerprint `179d8acb7b0c`, validated 2026-09-06T18:44:06+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank/mixed) | jitter churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 8e2fc8de | 2026-01-17 | 1 | 18 | skipped: population_below_n_min | | | | | | |
| 1 | ad739b6f | 2026-01-23 | 75 | 117 | — | | | | | | |
| 2 | 79f2801b | 2026-01-30 | 148 | 159 | 73 | 42/0 | 39 (0.33) | 18+7 | 39+0 (21/6/12) | 0.168 / 0.000 | untested (beyond_pinned_k) |
| 3 | 54ff7c77 | 2026-02-23 | 222 | 174 | 74 | 23/8 | 61 (0.40) | 43+10 | 25+1 (11/14/1) | 0.130 / 0.011 | untested (beyond_pinned_k) |
| 4 | f93a24c5 | 2026-03-31 | 344 | 188 | 122 | 16/2 | 123 (0.72) | 65+20 | 21+0 (10/2/9) | 0.208 / 0.000 | untested (beyond_pinned_k) |
| 5 | 53439c5c | 2026-04-07 | 418 | 200 | 74 | 18/6 | 39 (0.21) | 15+4 | 8+17 (6/19/0) | 0.014 / 0.119 | untested (beyond_pinned_k) |
| 6 | b325d940 | 2026-04-14 | 491 | 202 | 73 | 6/4 | 58 (0.30) | 17+1 | 11+0 (6/5/0) | 0.036 / 0.000 | untested (beyond_pinned_k) |
| 7 | 2ed60d62 | 2026-05-04 | 565 | 204 | 74 | 9/7 | 71 (0.36) | 27+0 | 12+0 (6/6/0) | 0.046 / 0.000 | untested (beyond_pinned_k) |
| 8 | ca0cb8ee | 2026-05-31 | 639 | 218 | 74 | 22/8 | 46 (0.23) | 21+6 | 9+13 (7/14/1) | 0.012 / 0.087 | untested (beyond_pinned_k) |
| 9 | d8ea567f | 2026-06-24 | 744 | 249 | 105 | 34/3 | 65 (0.30) | 46+7 | 23+15 (8/27/3) | 0.093 / 0.100 | untested (beyond_pinned_k) |
| 10 | 22aab5c2 | 2026-07-29 | 833 | 262 | 89 | 15/2 | 70 (0.28) | 42+8 | 28+22 (15/31/4) | 0.077 / 0.124 | untested (beyond_pinned_k) |
| 11 | f7414cc7 | 2026-08-31 | 956 | 267 | 123 | 7/2 | 76 (0.29) | 47+5 | 26+18 (17/26/1) | 0.048 / 0.098 | untested (beyond_pinned_k) |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals only — maintainability/dark_room, maintainability/lit_room — the skeleton reporting time), *rank* (features over rank-only signals, and every floor move of an untouched room: the percentile or the layer moved under a node nobody touched — jitter), and *mixed* (features over a clock and a rank signal together — maintainability/flooded_basement — whose rank component cannot be separated and which the budget therefore counts as jitter); *born/del* = structural change. The four together are the movement between frames. The budget (D-018, operand revised D-024) judges *jitter* = rank + mixed churn and strata moves over untouched rooms, only at K ≤ 50; beyond that it is `untested: beyond_pinned_k` and the numbers stand on their own.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 409 | 0.44 |
| ripple (untouched nodes) | 288 | 0.31 |
| &nbsp;&nbsp;of which clock (time reported) | 107 | 0.11 |
| &nbsp;&nbsp;of which rank (jitter) | 150 | 0.16 |
| &nbsp;&nbsp;of which mixed (counted as jitter) | 31 | 0.03 |
| **jitter (rank + mixed)** | **181** | **0.19** at median K = 74 |
| structural (born + deleted) | 234 | 0.25 |
| **movement** | **931** | over 10 transitions, 881 commits |

Budget tally across transitions: untested:beyond_pinned_k × 10. **Budget reading: no verdict** — 0 of 10 transitions judged (coverage 0.00); a run the budget could not judge at all says nothing about stability (D-030).

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/foundation | onboarding/import_root | onboarding/leaf_utility | onboarding/package_entry | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | 15 | 17 | 16 | 12 | 12 | 14 | 4 | 12 | 4 | 14 | 1 | 71 |  |
| 2 | 16 | 27 | 26 | 16 | 16 | 19 | 2 | 16 | 4 | 17 | 1 | 95 | 1 |
| 3 | 18 | 25 | 25 | 18 | 18 | 18 | 8 | 18 | 4 | 15 | 1 | 93 | 1 |
| 4 | 20 | 23 | 22 | 19 | 19 | 20 | 10 | 19 | 5 | 12 | 1 | 101 | 1 |
| 5 | 20 | 23 | 22 | 20 | 20 | 22 | 11 | 20 | 5 | 12 | 1 | 110 | 1 |
| 6 | 21 | 23 | 22 | 21 | 21 | 21 | 11 | 21 | 5 | 11 | 1 | 112 | 1 |
| 7 | 21 | 21 | 20 | 21 | 21 | 21 | 3 | 21 | 5 | 13 | 1 | 111 | 1 |
| 8 | 22 | 22 | 21 | 22 | 23 | 22 | 4 | 22 | 7 | 16 | 1 | 113 | 1 |
| 9 | 25 | 25 | 24 | 25 | 26 | 27 | 15 | 25 | 10 | 18 | 1 | 120 | 1 |
| 10 | 27 | 27 | 26 | 27 | 27 | 32 | 14 | 27 | 10 | 20 | 1 | 129 | 1 |
| 11 | 27 | 27 | 26 | 27 | 27 | 40 | 13 | 27 | 11 | 20 | 1 | 133 |  |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
