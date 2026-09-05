# Phase 1 — first time-lapse reading across the reference set (D-021)

*2026-09-05. `substrate timelapse`, twelve evenly spaced first-parent checkpoints per repository, maintainability + onboarding overlay, `reports/2026-09-04-m1/validation.json` at HEAD governing every frame, substrate config `config/tuned.toml` (fingerprint `80b2a632f8b7`). Per-run reports, manifests, and scrubber pages sit beside this file as `<repo>.<geometry>.*`. Spec: `time-lapse-spec.md`.*

The question (D-020): over a repository's history, is the named structure structural change or the budget's jitter? Movement between adjacent frames decomposes into **edits** (feature changes and strata moves on rooms the intervening commits touched — the skeleton reporting the edit), **ripple** on rooms they did not touch, split into **clock** (clock-relative signals and age-geometry strata: the skeleton reporting time) and **rank** (the percentile or the dependency layer moved under an untouched room — jitter), and **structural** (rooms born or deleted). The rank share is the answer.

| repo | geometry | trunk | mapped/skipped | commits spanned | movement | edits | clock | **rank** | structural | budget tally |
|---|---|---|---|---|---|---|---|---|---|---|
| eslint | age | 8,677 | 11/1 | 9,400 | 4,111 | 0.80 | 0.06 | **0.02** | 0.12 | untested: insufficient_untouched_population × 5, untested: touched_fraction_exceeds_floor × 5 |
| eslint | layer | 8,677 | 11/1 | 9,400 | 3,816 | 0.79 | 0.05 | **0.03** | 0.13 | untested: insufficient_untouched_population × 5, untested: touched_fraction_exceeds_floor × 5 |
| mcp-secure-server | age | 134 | 12/0 | 138 | 1,254 | 0.17 | 0.61 | **0.05** | 0.17 | over_budget × 8, untested: insufficient_untouched_population × 1, within_budget × 2 |
| mcp-secure-server | layer | 134 | 12/0 | 138 | 951 | 0.22 | 0.47 | **0.09** | 0.22 | over_budget × 7, untested: insufficient_untouched_population × 1, within_budget × 3 |
| uluops-registry-api | age | 812 | 11/1 | 881 | 1,286 | 0.40 | 0.37 | **0.05** | 0.18 | over_budget × 9, untested: touched_fraction_exceeds_floor × 1 |
| uluops-registry-api | layer | 812 | 11/1 | 881 | 1,032 | 0.44 | 0.19 | **0.15** | 0.23 | over_budget × 9, untested: touched_fraction_exceeds_floor × 1 |
| typeorm | age | 3,804 | 12/0 | 6,064 | 5,161 | 0.63 | 0.14 | **0.02** | 0.21 | over_budget × 4, untested: insufficient_untouched_population × 3, untested: touched_fraction_exceeds_floor × 4 |
| typeorm | layer | 3,804 | 12/0 | 6,064 | 4,602 | 0.63 | 0.09 | **0.04** | 0.24 | over_budget × 4, untested: insufficient_untouched_population × 3, untested: touched_fraction_exceeds_floor × 4 |

## Readings

- **Rank jitter is a small share of movement everywhere it can be measured:** 2–5% under age geometry, up to 15% under layer geometry on the youngest repository, where strata moves on untouched rooms are dependency-layer propagation (D-018's observation, now measured over a history). The named structure over a history is overwhelmingly edits, time, and births.
- **Clock ripple is the dominant non-edit movement on the young repositories** (37% on the registry, 61% on mcp-secure-server under age geometry). Weeks pass between frames, and `lit_room` / `dark_room` / `flooded_basement` / age strata move on rooms nobody touched because the checkpoint's clock advanced. That is the skeleton reporting time, not instability; but it is also why D-018's single number does not transfer to K in the hundreds unchanged (time-lapse spec §4, §7 Q2).
- **The mature repositories are edits.** eslint: 80% of movement is on touched rooms; with ~790 commits between frames, the intervening commits touch most of the population and the budget's floors refuse every transition (`insufficient_untouched_population` or `touched_fraction_exceeds_floor`) — the floors working as designed on a schedule too coarse for them.
- **The budget's verdicts at this K are not the K = 5 reading.** Over-budget transitions on the small repositories are ripple accumulated over 70–120 commits, most of it clock. A schedule with `--every 5` would produce the reading the budget was pinned for, at the cost of hundreds of extractions; that is the per-frame-gate question (§7 Q3), deferred.
- **What the pictures show** is on the scrubber pages: a foundation poured in the first frames and kept, wings bolted on at identifiable checkpoints, the flooded basement filling as the young repositories' first files go untouched. Recognition, n = 1, model-assisted; recorded, not evidence.

## What this decides

M3's condition (D-003: "built only if M2 proves the skeleton is worth narrating") is met in the sense the time-lapse can test: the structure that moves between frames is change and time, not jitter. Whether the *narrative* over it is worth building remains a product judgment, logged in D-021.
