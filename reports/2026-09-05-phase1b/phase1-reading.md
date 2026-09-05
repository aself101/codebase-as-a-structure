# Phase 1 — time-lapse reading across the reference set under substrate 0.3.0 (D-021, D-022 addendum)

*2026-09-05. `substrate timelapse`, twelve evenly spaced first-parent checkpoints per repository, maintainability + onboarding overlay, `reports/2026-09-05-m1b/validation.json` at HEAD governing every frame, substrate config `config/tuned.toml` under substrate 0.3.0 (fingerprint `5f5554e36d4a`; age and recency fractional days, D-022). Supersedes `reports/2026-09-05-phase1/` where the numbers differ; the first reading is kept as the record of the instrument that found the artefact. Per-run reports, manifests, and scrubber pages sit beside this file as `<repo>.<geometry>.*`. Spec: `time-lapse-spec.md`.*

The question (D-020): over a repository's history, is the named structure structural change or the budget's jitter? Movement between adjacent frames decomposes into **edits** (feature changes and strata moves on rooms the intervening commits touched — the skeleton reporting the edit), **ripple** on rooms they did not touch, split into **clock** (clock-relative signals and age-geometry strata: the skeleton reporting time) and **rank** (the percentile or the dependency layer moved under an untouched room — jitter), and **structural** (rooms born or deleted). The rank share is the answer.

| repo | geometry | schedule | trunk | mapped/skipped | commits spanned | movement | edits | clock | **rank** | structural | budget tally |
|---|---|---|---|---|---|---|---|---|---|---|---|
| eslint | age | 12 frames | 8,677 | 11/1 | 9,400 | 4,105 | 0.80 | 0.06 | **0.02** | 0.12 | untested: insufficient_untouched_population × 5, untested: touched_fraction_exceeds_floor × 5 |
| eslint | layer | 12 frames | 8,677 | 11/1 | 9,400 | 3,810 | 0.79 | 0.05 | **0.03** | 0.13 | untested: insufficient_untouched_population × 5, untested: touched_fraction_exceeds_floor × 5 |
| mcp-secure-server | age | 12 frames | 134 | 12/0 | 138 | 876 | 0.24 | 0.44 | **0.07** | 0.24 | over_budget × 7, untested: insufficient_untouched_population × 1, within_budget × 3 |
| mcp-secure-server | age | every 5 | 134 | 27/0 | 135 | 1,054 | 0.24 | 0.45 | **0.10** | 0.20 | over_budget × 10, untested: insufficient_untouched_population × 1, within_budget × 15 |
| mcp-secure-server | layer | 12 frames | 134 | 12/0 | 138 | 715 | 0.28 | 0.31 | **0.11** | 0.30 | over_budget × 7, untested: insufficient_untouched_population × 1, within_budget × 3 |
| uluops-registry-api | age | 12 frames | 812 | 11/1 | 881 | 1,129 | 0.40 | 0.33 | **0.06** | 0.21 | over_budget × 9, untested: touched_fraction_exceeds_floor × 1 |
| uluops-registry-api | layer | 12 frames | 812 | 11/1 | 881 | 934 | 0.43 | 0.16 | **0.16** | 0.25 | over_budget × 9, untested: touched_fraction_exceeds_floor × 1 |
| typeorm | age | 12 frames | 3,804 | 12/0 | 6,064 | 5,085 | 0.62 | 0.14 | **0.02** | 0.22 | over_budget × 4, untested: insufficient_untouched_population × 3, untested: touched_fraction_exceeds_floor × 4 |
| typeorm | layer | 12 frames | 3,804 | 12/0 | 6,064 | 4,539 | 0.63 | 0.09 | **0.04** | 0.24 | over_budget × 4, untested: insufficient_untouched_population × 3, untested: touched_fraction_exceeds_floor × 4 |

## Readings

- **Rank jitter is a small share of movement everywhere it can be measured:** 2–7% under age geometry, 3–16% under layer geometry, the layer maxima on the youngest repository, where strata moves on untouched rooms are dependency-layer propagation (D-018's observation, now measured over a history). The named structure over a history is overwhelmingly edits, time, and births.
- **The fine schedule agrees with the coarse one.** mcp-secure-server at every 5 commits: rank 10% against 7% at twelve frames; on the first reading (substrate 0.2.x) the registry at every 10 commits gave 5% against 5%. The twelve-frame schedule is not averaging jitter away (D-021 breaks-if, checked).
- **What substrate 0.3.0 removed was clock, not rank.** Against `reports/2026-09-05-phase1/`, mcp-secure-server's clock share fell 0.61 → 0.44 at twelve frames and its every-5 movement fell 1,649 → 1,054, almost all of it clock; the registry's clock share fell 0.37 → 0.33. Those were birth cohorts flipping floors and lights as integer-day ties broke (D-022). Rank shares rose by a point or two only because the denominator shrank.
- **Clock ripple remains the dominant non-edit movement on the young repositories** (33% on the registry, 44% on mcp-secure-server under age geometry): weeks pass between frames, and `lit_room` / `dark_room` / `flooded_basement` and the age bands move on rooms nobody touched because the checkpoint's clock advanced. That is the skeleton reporting time, and it is why D-018's single number does not transfer to K in the hundreds unchanged (time-lapse spec §4, §7 Q2).
- **The mature repositories are edits.** eslint: 80% of movement is on touched rooms; with ~790 commits between frames the intervening commits touch most of the population and the budget's floors refuse every transition — the floors working as designed on a schedule too coarse for them.
- **The change sheets** (`<repo>.<geometry>.timelapse.html`, toggle "change sheet"; D-023) put the decomposition on the rooms: a transition's births, edits, clock, and rank marks on the after frame's layout, deleted rooms dashed under each wing.

## What this decides

M3's condition (D-003: "built only if M2 proves the skeleton is worth narrating") is met in the sense the time-lapse can test: the structure that moves between frames is change and time, not jitter. Whether the *narrative* over it is worth building remains a product judgment, logged in D-021.
