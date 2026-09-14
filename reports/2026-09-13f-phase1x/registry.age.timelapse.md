# Time-lapse — uluops-registry-api

*Trunk (first-parent) of 818 commits, HEAD `e947c5b67542`; 12 frames (11 mapped, 1 skipped), geometry `age`, ruleset maintainability 0.3.2 (profile maintainability), overlays: onboarding 0.3.0. Gate: `validation.json` at HEAD (substrate fingerprint `84bae11b50a7`, validated 2026-09-14T00:15:02+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank/mixed) | jitter churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 8e2fc8de | 2026-01-17 | 1 | 18 | skipped: population_below_n_min | | | | | | |
| 1 | ad739b6f | 2026-01-23 | 75 | 117 | — | | | | | | |
| 2 | 50df43b7 | 2026-01-30 | 150 | 159 | 75 | 40/0 | 42 (0.40) | 19+31 | 9+28 (3/33/1) | 0.063 / 0.452 | untested (beyond_pinned_k) |
| 3 | ffb8768d | 2026-02-23 | 224 | 174 | 74 | 19/8 | 60 (0.44) | 38+13 | 15+16 (9/22/0) | 0.067 / 0.211 | untested (beyond_pinned_k) |
| 4 | e5a82fa7 | 2026-04-01 | 346 | 188 | 122 | 8/2 | 119 (0.78) | 58+15 | 27+9 (13/12/11) | 0.304 / 0.265 | untested (beyond_pinned_k) |
| 5 | 060834e8 | 2026-04-07 | 420 | 201 | 74 | 15/6 | 39 (0.25) | 11+3 | 6+24 (4/26/0) | 0.015 / 0.207 | untested (beyond_pinned_k) |
| 6 | fa2e09bd | 2026-04-14 | 495 | 203 | 75 | 3/4 | 61 (0.37) | 16+0 | 9+6 (4/10/1) | 0.045 / 0.057 | untested (beyond_pinned_k) |
| 7 | 89fe8d2b | 2026-05-04 | 569 | 204 | 74 | 4/6 | 66 (0.40) | 18+2 | 10+6 (5/8/3) | 0.043 / 0.062 | untested (beyond_pinned_k) |
| 8 | 773342d4 | 2026-05-31 | 643 | 219 | 74 | 19/8 | 41 (0.26) | 20+20 | 11+40 (8/40/3) | 0.019 / 0.339 | untested (beyond_pinned_k) |
| 9 | e0f182d5 | 2026-06-24 | 749 | 251 | 106 | 21/3 | 62 (0.35) | 30+13 | 57+29 (27/37/22) | 0.183 / 0.257 | untested (beyond_pinned_k) |
| 10 | 38253735 | 2026-07-31 | 840 | 263 | 91 | 10/2 | 69 (0.36) | 35+6 | 16+7 (6/17/0) | 0.060 / 0.056 | untested (beyond_pinned_k) |
| 11 | e947c5b6 | 2026-09-13 | 965 | 267 | 125 | 4/2 | 67 (0.33) | 45+2 | 21+7 (13/15/0) | 0.045 / 0.052 | untested (beyond_pinned_k) |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals only — maintainability/dark_room, maintainability/lit_room — the skeleton reporting time), *rank* (features over rank-only signals, and every floor move of an untouched room: the percentile or the layer moved under a node nobody touched — jitter), and *mixed* (features over a clock and a rank signal together — maintainability/flooded_basement — whose rank component cannot be separated and which the budget therefore counts as jitter); *born/del* = structural change. The four together are the movement between frames. The budget (D-018, operand revised D-024) judges *jitter* = rank + mixed churn and strata moves over untouched rooms, only at K ≤ 50; beyond that it is `untested: beyond_pinned_k` and the numbers stand on their own.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 395 | 0.42 |
| ripple (untouched nodes) | 353 | 0.38 |
| &nbsp;&nbsp;of which clock (time reported) | 92 | 0.10 |
| &nbsp;&nbsp;of which rank (jitter) | 220 | 0.24 |
| &nbsp;&nbsp;of which mixed (counted as jitter) | 41 | 0.04 |
| **jitter (rank + mixed)** | **261** | **0.28** at median K = 75 |
| structural (born + deleted) | 184 | 0.20 |
| **movement** | **932** | over 10 transitions, 890 commits |

Budget tally across transitions: untested:beyond_pinned_k × 10. **Budget reading: no verdict** — 0 of 10 transitions judged (coverage 0.00); a run the budget could not judge at all says nothing about stability (D-030).

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/foundation | onboarding/import_root | onboarding/leaf_utility | onboarding/package_entry | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | 11 | 21 | 20 | 11 | 11 | 11 | 1 | 11 | 4 | 11 | 1 | 71 |  |
| 2 | 16 | 19 | 19 | 15 | 16 | 15 | 2 | 15 | 4 | 15 | 1 | 95 | 1 |
| 3 | 16 | 17 | 17 | 16 | 16 | 16 | 2 | 16 | 4 | 15 | 1 | 93 | 1 |
| 4 | 17 | 18 | 16 | 17 | 17 | 18 | 2 | 17 | 5 | 12 | 1 | 101 | 1 |
| 5 | 17 | 17 | 15 | 17 | 17 | 17 | 2 | 17 | 5 | 12 | 1 | 110 | 1 |
| 6 | 17 | 17 | 15 | 17 | 17 | 18 | 2 | 17 | 4 | 11 | 1 | 112 | 1 |
| 7 | 17 | 17 | 16 | 17 | 18 | 17 | 3 | 17 | 4 | 13 | 1 | 111 | 1 |
| 8 | 18 | 18 | 17 | 18 | 18 | 21 | 3 | 18 | 6 | 16 | 1 | 113 | 1 |
| 9 | 21 | 40 | 39 | 20 | 20 | 21 | 4 | 20 | 8 | 18 | 1 | 122 | 1 |
| 10 | 21 | 38 | 37 | 21 | 21 | 22 | 6 | 21 | 10 | 16 | 1 | 129 | 1 |
| 11 | 21 | 34 | 33 | 21 | 21 | 21 | 8 | 21 | 10 | 16 | 1 | 133 |  |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
