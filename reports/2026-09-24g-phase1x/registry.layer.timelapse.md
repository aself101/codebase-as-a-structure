# Time-lapse — uluops-registry-api

*Trunk (first-parent) of 825 commits, HEAD `8d5f659a7ccf`; 12 frames (11 mapped, 1 skipped), geometry `layer`, ruleset maintainability 0.3.4 (profile maintainability), overlays: onboarding 0.3.1. Gate: `validation.json` at HEAD (substrate fingerprint `298696064105`, validated 2026-09-24T22:58:00+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank/mixed) | jitter churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 8e2fc8de | 2026-01-17 | 1 | 18 | skipped: population_below_n_min | | | | | | |
| 1 | 955dbb68 | 2026-01-23 | 76 | 117 | — | | | | | | |
| 2 | 72613cf3 | 2026-01-30 | 151 | 159 | 75 | 40/0 | 42 (0.40) | 18+11 | 9+10 (3/15/1) | 0.063 / 0.161 | untested (beyond_pinned_k) |
| 3 | 349a24a2 | 2026-02-23 | 226 | 174 | 75 | 19/8 | 60 (0.44) | 38+12 | 15+11 (9/17/0) | 0.067 / 0.145 | untested (beyond_pinned_k) |
| 4 | 1dcaa727 | 2026-04-01 | 349 | 189 | 123 | 8/2 | 120 (0.78) | 55+21 | 26+0 (12/3/11) | 0.311 / 0.000 | untested (beyond_pinned_k) |
| 5 | e42ea4a4 | 2026-04-07 | 424 | 201 | 75 | 15/6 | 40 (0.26) | 19+17 | 7+37 (4/39/1) | 0.023 / 0.322 | untested (beyond_pinned_k) |
| 6 | 921b78fd | 2026-04-18 | 498 | 203 | 74 | 3/4 | 59 (0.36) | 23+0 | 10+0 (5/4/1) | 0.045 / 0.000 | untested (beyond_pinned_k) |
| 7 | 89212fc2 | 2026-05-04 | 573 | 204 | 75 | 4/6 | 67 (0.41) | 23+0 | 10+0 (5/2/3) | 0.044 / 0.000 | untested (beyond_pinned_k) |
| 8 | 481c4749 | 2026-06-01 | 648 | 220 | 75 | 19/8 | 39 (0.25) | 25+10 | 13+7 (10/7/3) | 0.019 / 0.058 | untested (beyond_pinned_k) |
| 9 | 0883b2b7 | 2026-06-26 | 758 | 252 | 110 | 22/3 | 66 (0.38) | 43+6 | 57+0 (27/8/22) | 0.194 / 0.000 | untested (beyond_pinned_k) |
| 10 | 3d23dbc7 | 2026-08-03 | 848 | 263 | 90 | 9/2 | 66 (0.34) | 26+1 | 18+2 (7/13/0) | 0.062 / 0.016 | untested (beyond_pinned_k) |
| 11 | 8d5f659a | 2026-09-19 | 978 | 267 | 130 | 4/2 | 70 (0.35) | 46+1 | 20+0 (10/10/0) | 0.057 / 0.000 | untested (beyond_pinned_k) |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals only — maintainability/dark_room, maintainability/lit_room — the skeleton reporting time), *rank* (features over rank-only signals, and every floor move of an untouched room: the percentile or the layer moved under a node nobody touched — jitter), and *mixed* (features over a clock and a rank signal together — maintainability/flooded_basement — whose rank component cannot be separated and which the budget therefore counts as jitter); *born/del* = structural change. The four together are the movement between frames. The budget (D-018, operand revised D-024) judges *jitter* = rank + mixed churn and strata moves over untouched rooms, only at K ≤ 50; beyond that it is `untested: beyond_pinned_k` and the numbers stand on their own.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 395 | 0.48 |
| ripple (untouched nodes) | 252 | 0.30 |
| &nbsp;&nbsp;of which clock (time reported) | 92 | 0.11 |
| &nbsp;&nbsp;of which rank (jitter) | 118 | 0.14 |
| &nbsp;&nbsp;of which mixed (counted as jitter) | 42 | 0.05 |
| **jitter (rank + mixed)** | **160** | **0.19** at median K = 75 |
| structural (born + deleted) | 184 | 0.22 |
| **movement** | **831** | over 10 transitions, 902 commits |

Budget tally across transitions: untested:beyond_pinned_k × 10. **Budget reading: no verdict** — 0 of 10 transitions judged (coverage 0.00); a run the budget could not judge at all says nothing about stability (D-030).

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/foundation | onboarding/import_root | onboarding/leaf_utility | onboarding/package_entry | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | 11 | 21 | 20 | 11 | 11 | 11 | 1 | 11 | 4 | 11 | 1 | 71 |  |
| 2 | 16 | 19 | 19 | 15 | 16 | 17 | 2 | 15 | 4 | 15 | 1 | 95 | 1 |
| 3 | 16 | 17 | 17 | 16 | 16 | 16 | 2 | 16 | 4 | 15 | 1 | 93 | 1 |
| 4 | 17 | 17 | 16 | 17 | 17 | 17 | 2 | 17 | 5 | 12 | 1 | 101 | 1 |
| 5 | 17 | 17 | 15 | 17 | 17 | 18 | 2 | 17 | 5 | 12 | 1 | 110 | 1 |
| 6 | 18 | 17 | 15 | 17 | 17 | 19 | 2 | 17 | 4 | 11 | 1 | 112 | 1 |
| 7 | 18 | 17 | 16 | 17 | 18 | 19 | 3 | 17 | 4 | 13 | 1 | 111 | 1 |
| 8 | 18 | 18 | 17 | 18 | 18 | 23 | 3 | 18 | 6 | 16 | 1 | 114 | 1 |
| 9 | 20 | 38 | 37 | 20 | 22 | 21 | 5 | 20 | 8 | 19 | 1 | 123 | 1 |
| 10 | 21 | 38 | 37 | 21 | 21 | 21 | 6 | 21 | 10 | 16 | 1 | 129 | 1 |
| 11 | 21 | 34 | 33 | 21 | 21 | 28 | 8 | 21 | 10 | 16 | 1 | 133 |  |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
