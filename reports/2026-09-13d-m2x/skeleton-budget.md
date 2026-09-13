# Skeleton-level stability budget — re-read under `e28401778e67` (2026-09-13d)

*Procedure of D-018 with the D-024/D-026 operand: before = the gate's stability-perturbation substrate (HEAD minus the last K = 25 timeline commits), after = HEAD; maintainability + onboarding; gate `out/validation-k25g/validation.json`.*

| repo | geometry | K | common | born/del | touched | churn (all) | strata (all) | jitter churn | clock churn | strata (untouched) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| typeorm | age | 25 | 574 | 0/0 | 52 | 0.146 | 0.000 | 0.016 | 0.402 | 0.000 | within_budget |
| typeorm | layer | 25 | 574 | 0/0 | 52 | 0.146 | 0.000 | 0.016 | 0.402 | 0.000 | within_budget |
| mcp-secure-server | age | 25 | 186 | 1/0 | 29 | 0.119 | 0.000 | 0.006 | 0.190 | 0.000 | within_budget |
| mcp-secure-server | layer | 25 | 186 | 1/0 | 29 | 0.119 | 0.043 | 0.006 | 0.190 | 0.025 | within_budget |
| uluops-registry-api | age | 25 | 206 | 0/0 | 38 | 0.152 | 0.005 | 0.005 | 0.424 | 0.006 | within_budget |
| uluops-registry-api | layer | 25 | 206 | 0/0 | 38 | 0.152 | 0.000 | 0.005 | 0.424 | 0.000 | within_budget |
| eslint | age | 25 | 466 | 1/0 | 16 | 0.033 | 0.002 | 0.005 | 0.121 | 0.002 | within_budget |
| eslint | layer | 25 | 466 | 1/0 | 16 | 0.033 | 0.000 | 0.005 | 0.121 | 0.000 | within_budget |
