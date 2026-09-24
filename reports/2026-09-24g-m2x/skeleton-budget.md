# Skeleton-level stability budget — re-read under `298696064105` (2026-09-24g)

*Procedure of D-018 with the D-024/D-026 operand: before = the gate's stability-perturbation substrate (HEAD minus the last K = 25 timeline commits), after = HEAD; maintainability + onboarding; gate `out/validation-k25k/validation.json`.*

| repo | geometry | K | common | born/del | touched | churn (all) | strata (all) | jitter churn | clock churn | strata (untouched) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| typeorm | age | 25 | 571 | 0/0 | 52 | 0.142 | 0.000 | 0.016 | 0.387 | 0.000 | within_budget |
| typeorm | layer | 25 | 571 | 0/0 | 52 | 0.142 | 0.000 | 0.016 | 0.387 | 0.000 | within_budget |
| mcp-secure-server | age | 25 | 64 | 1/0 | 29 | 0.258 | 0.000 | 0.114 | 0.364 | 0.000 | over_budget |
| mcp-secure-server | layer | 25 | 64 | 1/0 | 29 | 0.258 | 0.141 | 0.114 | 0.364 | 0.114 | over_budget |
| uluops-registry-api | age | 25 | 206 | 0/0 | 38 | 0.152 | 0.005 | 0.005 | 0.424 | 0.006 | within_budget |
| uluops-registry-api | layer | 25 | 206 | 0/0 | 38 | 0.152 | 0.000 | 0.005 | 0.424 | 0.000 | within_budget |
| eslint | age | 25 | 461 | 1/0 | 16 | 0.034 | 0.002 | 0.005 | 0.125 | 0.002 | within_budget |
| eslint | layer | 25 | 461 | 1/0 | 16 | 0.034 | 0.000 | 0.005 | 0.125 | 0.000 | within_budget |
