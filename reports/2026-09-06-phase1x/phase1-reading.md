# Phase 1 — time-lapse reading across the reference set under substrate 0.3.0 (D-021, D-022 addendum)

*2026-09-05. `substrate timelapse`, twelve evenly spaced first-parent checkpoints per repository, maintainability + onboarding overlay, `reports/2026-09-05-m1b/validation.json` at HEAD governing every frame, substrate config `config/tuned.toml` under substrate 0.3.0 (fingerprint `5f5554e36d4a`; age and recency fractional days, D-022). Supersedes `reports/2026-09-05-phase1/` where the numbers differ; the first reading is kept as the record of the instrument that found the artefact. Per-run reports, manifests, and scrubber pages sit beside this file as `<repo>.<geometry>.*`. Spec: `time-lapse-spec.md`.*

The question (D-020): over a repository's history, is the named structure structural change or the budget's jitter? Movement between adjacent frames decomposes into **edits** (feature changes and strata moves on rooms the intervening commits touched — the skeleton reporting the edit), **ripple** on rooms they did not touch, split into **clock** (clock-relative signals and age-geometry strata: the skeleton reporting time) and **rank** (the percentile or the dependency layer moved under an untouched room — jitter), and **structural** (rooms born or deleted). The rank share is the answer.

| repo | geometry | schedule | trunk | mapped/skipped | commits spanned | median K | movement | edits | clock | rank | mixed | **jitter** | structural | budget tally |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eslint | age | 12 frames | 8,677 | 11/1 | 9,400 | 789 | 4,401 | 0.81 | 0.03 | 0.03 | 0.02 | **0.05** | 0.11 | untested: beyond_pinned_k × 10 |
| eslint | layer | 12 frames | 8,677 | 11/1 | 9,400 | 789 | 4,094 | 0.80 | 0.03 | 0.02 | 0.02 | **0.05** | 0.12 | untested: beyond_pinned_k × 10 |
| mcp-secure-server | age | 12 frames | 134 | 12/0 | 138 | 12 | 870 | 0.27 | 0.19 | 0.27 | 0.03 | **0.30** | 0.24 | over_budget × 4, untested: touched_fraction_exceeds_floor × 1, within_budget × 6 |
| mcp-secure-server | layer | 12 frames | 134 | 12/0 | 138 | 12 | 704 | 0.31 | 0.23 | 0.12 | 0.04 | **0.16** | 0.30 | over_budget × 3, untested: touched_fraction_exceeds_floor × 1, within_budget × 7 |
| uluops-registry-api | age | 12 frames | 812 | 11/1 | 881 | 74 | 1,112 | 0.40 | 0.10 | 0.26 | 0.03 | **0.29** | 0.21 | untested: beyond_pinned_k × 10 |
| uluops-registry-api | layer | 12 frames | 812 | 11/1 | 881 | 74 | 931 | 0.44 | 0.11 | 0.16 | 0.03 | **0.19** | 0.25 | untested: beyond_pinned_k × 10 |
| typeorm | age | 12 frames | 3,804 | 12/0 | 6,064 | 374 | 5,157 | 0.63 | 0.04 | 0.08 | 0.04 | **0.12** | 0.22 | untested: beyond_pinned_k × 11 |
| typeorm | layer | 12 frames | 3,804 | 12/0 | 6,064 | 374 | 5,136 | 0.68 | 0.04 | 0.04 | 0.02 | **0.06** | 0.22 | untested: beyond_pinned_k × 11 |

## How to read it

- **The jitter share is the answer** to the phase's question, per (repository, geometry, schedule), and it is quoted with its median K because it is a joint value of repository and schedule (D-024, D-026).
- **Clock** is the skeleton reporting time; **edits** are the skeleton reporting edits; **structural** is births and deletions; only **rank + mixed** is jitter.
- **The budget's verdicts** are rendered only at K ≤ 50 (D-026); on twelve-frame schedules every transition is `untested: beyond_pinned_k` by construction, and the numbers stand on their own.
- The pre-registered ceilings of D-024 (jitter above 0.20 on any repository/geometry, or above 0.10 on two, refutes "a few percent") are judged in the decision log, not here; this file is the reading.
- Per-run pages beside this file carry the frames, the change sheets (D-023), and the per-transition tables.
