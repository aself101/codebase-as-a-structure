# Skeleton-level stability budget — re-read under `179d8acb7b0c` (2026-09-06)

*Procedure of D-018 with the D-024/D-026 operand: before = the gate's stability-perturbation substrate (HEAD minus the last K = 5 timeline commits), after = HEAD; maintainability + onboarding; gate `out/validation-m1d/validation.json`.*

| repo | geometry | K | common | born/del | touched | churn (all) | strata (all) | jitter churn | clock churn | strata (untouched) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| typeorm | age | 5 | 583 | 0/0 | 7 | 0.018 | 0.000 | 0.000 | 0.047 | 0.000 | within_budget |
| typeorm | layer | 5 | 583 | 0/0 | 7 | 0.018 | 0.000 | 0.000 | 0.047 | 0.000 | within_budget |
| mcp-secure-server | age | 5 | 202 | 0/0 | 14 | 0.048 | 0.000 | 0.020 | 0.093 | 0.000 | within_budget |
| mcp-secure-server | layer | 5 | 202 | 0/0 | 14 | 0.048 | 0.040 | 0.020 | 0.093 | 0.032 | within_budget |
| uluops-registry-api | age | 5 | 267 | 0/0 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | within_budget |
| uluops-registry-api | layer | 5 | 267 | 0/0 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | within_budget |
| eslint | age | 5 | 472 | 1/0 | 10 | 0.018 | 0.002 | 0.003 | 0.048 | 0.002 | within_budget |
| eslint | layer | 5 | 472 | 1/0 | 10 | 0.018 | 0.000 | 0.003 | 0.048 | 0.000 | within_budget |
