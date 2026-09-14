# Phase 1 — time-lapse reading across the reference set (D-021; gate `84bae11b50a7`)

*Generated 2026-09-14. `substrate timelapse`, twelve evenly spaced first-parent checkpoints per repository, maintainability + onboarding overlay; every frame governed by the gate at HEAD — substrate fingerprint `84bae11b50a7`, validation config `d42daadf3228`, validated 2026-09-14T00:15:02+00:00 — read from the manifests beside this file (D-035: the header states what the rows state, or it states nothing). Earlier readings (`reports/2026-09-05-phase1/`, `-phase1b/`, `2026-09-06-phase1x/`, `2026-09-06b-phase1x/`) are kept as the record of the instruments that produced them. Per-run reports, manifests, and scrubber pages sit beside this file as `<repo>.<geometry>.*`. Spec: `time-lapse-spec.md`.*

The question (D-020): over a repository's history, is the named structure structural change or the budget's jitter? Movement between adjacent frames decomposes into **edits** (feature changes and strata moves on rooms the intervening commits touched — the skeleton reporting the edit), **ripple** on rooms they did not touch, split into **clock** (clock-relative signals and age-geometry strata: the skeleton reporting time) and **rank** (the percentile or the dependency layer moved under an untouched room — jitter), and **structural** (rooms born or deleted). The rank share is the answer.

| repo | geometry | schedule | trunk | mapped/skipped | commits spanned | median K | movement | edits | clock | rank | mixed | **jitter** | structural | budget tally |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eslint | age | 12 frames | 8,677 | 11/1 | 9,400 | 789 | 4,360 | 0.81 | 0.03 | 0.03 | 0.02 | **0.05** | 0.11 | untested: beyond_pinned_k × 10 |
| eslint | layer | 12 frames | 8,677 | 11/1 | 9,400 | 789 | 4,054 | 0.81 | 0.03 | 0.02 | 0.03 | **0.05** | 0.12 | untested: beyond_pinned_k × 10 |
| mcp-secure-server | age | 12 frames | 136 | 12/0 | 144 | 12 | 824 | 0.31 | 0.18 | 0.25 | 0.03 | **0.27** | 0.24 | untested: below_pinned_k × 11 |
| mcp-secure-server | layer | 12 frames | 136 | 12/0 | 144 | 12 | 678 | 0.36 | 0.22 | 0.10 | 0.03 | **0.13** | 0.29 | untested: below_pinned_k × 11 |
| uluops-registry-api | age | 12 frames | 818 | 11/1 | 890 | 75 | 932 | 0.42 | 0.10 | 0.24 | 0.04 | **0.28** | 0.20 | untested: beyond_pinned_k × 10 |
| uluops-registry-api | layer | 12 frames | 818 | 11/1 | 890 | 75 | 801 | 0.46 | 0.11 | 0.14 | 0.05 | **0.20** | 0.23 | untested: beyond_pinned_k × 10 |
| typeorm | age | 12 frames | 3,804 | 12/0 | 6,064 | 374 | 5,657 | 0.68 | 0.04 | 0.07 | 0.02 | **0.09** | 0.19 | untested: beyond_pinned_k × 11 |
| typeorm | layer | 12 frames | 3,804 | 12/0 | 6,064 | 374 | 5,082 | 0.69 | 0.04 | 0.04 | 0.02 | **0.06** | 0.21 | untested: beyond_pinned_k × 11 |

## How to read it

- **The jitter share is the answer** to the phase's question, per (repository, geometry, schedule), and it is quoted with its median K because it is a joint value of repository and schedule (D-024, D-026).
- **Clock** is the skeleton reporting time; **edits** are the skeleton reporting edits; **structural** is births and deletions; only **rank + mixed** is jitter.
- **The budget's verdicts** are rendered only at 25 ≤ K ≤ 50 (D-026, D-032); on twelve-frame schedules almost every transition is `untested` by construction (`beyond_pinned_k` on the long histories, `below_pinned_k` on the short one), and the numbers stand on their own.
- The pre-registered ceilings of D-024 (jitter above 0.20 on any repository/geometry, or above 0.10 on two, refutes "a few percent") are judged in the decision log, not here; this file is the reading.
- Per-run pages beside this file carry the frames, the change sheets (D-023), and the per-transition tables.
