# Skeleton-level stability budget — re-read under `298696064105` (2026-11-11d-d083)

*Procedure of D-018 with the D-024/D-026 operand: before = the gate's stability-perturbation substrate (HEAD minus the last K = 25 timeline commits), after = HEAD; maintainability + onboarding; gate `out/validation-k25k/validation.json`.*

*Reading a row (mapper spec §7 Q3, D-082): the verdict is a statement about one window — more than 5% of the rank and mixed assignments held by unedited rooms, or of the unedited rooms' floors, changed. "over at n" is the smallest count that exceeds the ceiling on that denominator. Rows are one series with another tag's table only where the gate, the ruleset versions (maintainability 0.3.4, onboarding 0.3.1) and the rooms column all match; the last column marks a row whose population differs from the most recent earlier table for the same pair of commits.*

| repo | geometry | K | rooms | excluded kinds | common | born/del | touched | untouched | churn (all) | strata (all) | jitter: assignments | clock churn | floors: untouched rooms | verdict (operand over) | series |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| typeorm | age | 25 | 571 | config 6, example 3, migration 3 | 571 | 0/0 | 52 | 519 | 0.142 | 0.000 | 7/427 = 0.016 (over at 22) | 0.387 | 0/519 = 0.000 (over at 26) | within_budget | continues 2026-11-11c-d083 |
| typeorm | layer | 25 | 571 | config 6, example 3, migration 3 | 571 | 0/0 | 52 | 519 | 0.142 | 0.000 | 7/427 = 0.016 (over at 22) | 0.387 | 0/519 = 0.000 (over at 26) | within_budget | continues 2026-11-11c-d083 |
| mcp-secure-server | age | 25 | 65 | config 14, example 122, placeholder 2 | 64 | 1/0 | 29 | 35 | 0.258 | 0.000 | 4/35 = 0.114 (over at 2) | 0.364 | 0/35 = 0.000 (over at 2) | over_budget (features) | continues 2026-11-11c-d083 |
| mcp-secure-server | layer | 25 | 65 | config 14, example 122, placeholder 2 | 64 | 1/0 | 29 | 35 | 0.258 | 0.141 | 4/35 = 0.114 (over at 2) | 0.364 | 4/35 = 0.114 (over at 2) | over_budget (features, floors) | continues 2026-11-11c-d083 |
| uluops-registry-api | age | 25 | 206 | config 6, migration 55 | 206 | 0/0 | 38 | 168 | 0.152 | 0.005 | 1/215 = 0.005 (over at 11) | 0.424 | 1/168 = 0.006 (over at 9) | within_budget | continues 2026-11-11c-d083 |
| uluops-registry-api | layer | 25 | 206 | config 6, migration 55 | 206 | 0/0 | 38 | 168 | 0.152 | 0.000 | 1/215 = 0.005 (over at 11) | 0.424 | 0/168 = 0.000 (over at 9) | within_budget | continues 2026-11-11c-d083 |
| eslint | age | 25 | 462 | config 5, example 5, placeholder 1 | 461 | 1/0 | 16 | 445 | 0.034 | 0.002 | 4/748 = 0.005 (over at 38) | 0.125 | 1/445 = 0.002 (over at 23) | within_budget | continues 2026-11-11c-d083 |
| eslint | layer | 25 | 462 | config 5, example 5, placeholder 1 | 461 | 1/0 | 16 | 445 | 0.034 | 0.000 | 4/748 = 0.005 (over at 38) | 0.125 | 0/445 = 0.000 (over at 23) | within_budget | continues 2026-11-11c-d083 |
