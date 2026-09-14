# Time-lapse — mcp-secure-server

*Trunk (first-parent) of 136 commits, HEAD `5348b3ef614d`; 12 frames (12 mapped, 0 skipped), geometry `layer`, ruleset maintainability 0.3.2 (profile maintainability), overlays: onboarding 0.3.0. Gate: `validation.json` at HEAD (substrate fingerprint `84bae11b50a7`, validated 2026-09-14T00:15:02+00:00) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank/mixed) | jitter churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | fd0cfbeb | 2025-12-10 | 1 | 39 | — | | | | | | |
| 1 | 455fe055 | 2025-12-14 | 14 | 112 | 13 | 89/24 | 13 (1.00) | 31+9 | 0+0 (0/0/0) | 0.000 / 0.000 | untested (below_pinned_k) |
| 2 | 5df62ef9 | 2025-12-18 | 27 | 179 | 13 | 63/1 | 13 (0.13) | 40+0 | 35+0 (25/10/0) | 0.075 / 0.000 | untested (below_pinned_k) |
| 3 | d8af9ef3 | 2025-12-20 | 39 | 181 | 12 | 2/0 | 26 (0.16) | 30+1 | 35+2 (14/23/0) | 0.135 / 0.014 | untested (below_pinned_k) |
| 4 | 58c6a4e5 | 2025-12-20 | 51 | 181 | 12 | 0/0 | 0 (0.00) | 0+0 | 0+0 (0/0/0) | 0.000 / 0.000 | untested (below_pinned_k) |
| 5 | a10c4abc | 2026-01-02 | 63 | 181 | 12 | 0/0 | 11 (0.07) | 18+0 | 17+0 (17/0/0) | 0.000 / 0.000 | untested (below_pinned_k) |
| 6 | d6172d2d | 2026-01-06 | 76 | 188 | 13 | 6/0 | 28 (0.17) | 30+0 | 62+0 (36/4/22) | 0.163 / 0.000 | untested (below_pinned_k) |
| 7 | 7f6381e0 | 2026-01-09 | 88 | 196 | 12 | 8/0 | 10 (0.06) | 9+1 | 32+1 (21/12/0) | 0.057 / 0.006 | untested (below_pinned_k) |
| 8 | f305a925 | 2026-01-10 | 100 | 197 | 12 | 1/0 | 18 (0.10) | 23+0 | 14+0 (11/3/0) | 0.017 / 0.000 | untested (below_pinned_k) |
| 9 | 8ca52ec6 | 2026-01-11 | 112 | 201 | 12 | 4/0 | 13 (0.07) | 9+1 | 11+6 (9/8/0) | 0.011 / 0.036 | untested (below_pinned_k) |
| 10 | f1473915 | 2026-04-08 | 125 | 202 | 13 | 1/0 | 10 (0.05) | 11+0 | 7+0 (6/1/0) | 0.005 / 0.000 | untested (below_pinned_k) |
| 11 | 5348b3ef | 2026-09-10 | 145 | 203 | 20 | 1/0 | 29 (0.16) | 26+4 | 9+4 (8/5/0) | 0.006 / 0.025 | untested (below_pinned_k) |

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals only — maintainability/dark_room, maintainability/lit_room — the skeleton reporting time), *rank* (features over rank-only signals, and every floor move of an untouched room: the percentile or the layer moved under a node nobody touched — jitter), and *mixed* (features over a clock and a rank signal together — maintainability/flooded_basement — whose rank component cannot be separated and which the budget therefore counts as jitter); *born/del* = structural change. The four together are the movement between frames. The budget (D-018, operand revised D-024) judges *jitter* = rank + mixed churn and strata moves over untouched rooms, only at K ≤ 50; beyond that it is `untested: beyond_pinned_k` and the numbers stand on their own.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | 243 | 0.36 |
| ripple (untouched nodes) | 235 | 0.35 |
| &nbsp;&nbsp;of which clock (time reported) | 147 | 0.22 |
| &nbsp;&nbsp;of which rank (jitter) | 66 | 0.10 |
| &nbsp;&nbsp;of which mixed (counted as jitter) | 22 | 0.03 |
| **jitter (rank + mixed)** | **88** | **0.13** at median K = 12 |
| structural (born + deleted) | 200 | 0.29 |
| **movement** | **678** | over 11 transitions, 144 commits |

Budget tally across transitions: untested:below_pinned_k × 11. **Budget reading: no verdict** — 0 of 11 transitions judged (coverage 0.00); a run the budget could not judge at all says nothing about stability (D-030).

## Feature counts per frame

| # | crack | dark_room | flooded_basement | foundation | hub | lit_room | onboarding/corridor | onboarding/foundation | onboarding/import_root | onboarding/leaf_utility | onboarding/package_entry | scaffolding | toothpick_wing |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 37 | 37 | 37 | 4 | 4 | 37 | 2 | 4 |  | 5 | 3 | 10 | 1 |
| 1 | 23 | 38 | 38 | 11 | 11 | 25 | 9 | 11 | 11 | 8 | 9 | 45 | 2 |
| 2 | 17 | 27 | 27 | 17 | 17 | 23 | 12 | 17 | 19 | 15 | 15 | 58 | 1 |
| 3 | 27 | 23 | 23 | 17 | 17 | 26 | 13 | 17 | 19 | 16 | 15 | 61 | 1 |
| 4 | 27 | 23 | 23 | 17 | 17 | 26 | 13 | 17 | 19 | 16 | 15 | 61 | 1 |
| 5 | 19 | 18 | 18 | 17 | 17 | 17 | 13 | 17 | 19 | 16 | 15 | 61 | 2 |
| 6 | 18 | 42 | 37 | 18 | 18 | 26 | 14 | 18 | 19 | 16 | 16 | 64 | 1 |
| 7 | 18 | 41 | 36 | 18 | 18 | 18 | 15 | 18 | 15 | 16 | 16 | 64 |  |
| 8 | 21 | 38 | 33 | 19 | 19 | 19 | 15 | 19 | 15 | 17 | 16 | 65 | 2 |
| 9 | 19 | 37 | 32 | 19 | 19 | 19 | 15 | 19 | 15 | 17 | 16 | 67 | 2 |
| 10 | 19 | 34 | 29 | 19 | 19 | 19 | 15 | 19 | 15 | 18 | 16 | 67 | 1 |
| 11 | 20 | 34 | 29 | 19 | 19 | 27 | 16 | 19 | 15 | 19 | 16 | 72 | 3 |

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
