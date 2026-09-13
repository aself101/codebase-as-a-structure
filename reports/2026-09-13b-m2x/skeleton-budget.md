# Skeleton-level stability budget — re-read under `661f93333b65` (2026-09-13b)

*Procedure of D-018 with the D-024/D-026 operand: before = the gate's stability-perturbation substrate (HEAD minus the last K = 25 timeline commits), after = HEAD; maintainability + onboarding; gate `out/validation-k25e/validation.json`.*

| repo | geometry | K | common | born/del | touched | churn (all) | strata (all) | jitter churn | clock churn | strata (untouched) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| typeorm | age | 25 | 583 | 0/0 | 54 | 0.138 | 0.000 | 0.016 | 0.333 | 0.000 | within_budget |
| typeorm | layer | 25 | 583 | 0/0 | 54 | 0.138 | 0.000 | 0.016 | 0.333 | 0.000 | within_budget |
| mcp-secure-server | age | 25 | 202 | 1/0 | 29 | 0.116 | 0.000 | 0.011 | 0.208 | 0.000 | within_budget |
| mcp-secure-server | layer | 25 | 202 | 1/0 | 29 | 0.116 | 0.025 | 0.011 | 0.208 | 0.029 | within_budget |
| uluops-registry-api | age | 25 | 266 | 1/0 | 39 | 0.174 | 0.008 | 0.013 | 0.534 | 0.009 | within_budget |
| uluops-registry-api | layer | 25 | 266 | 1/0 | 39 | 0.174 | 0.086 | 0.013 | 0.534 | 0.088 | over_budget |
| eslint | age | 25 | 472 | 1/0 | 17 | 0.029 | 0.002 | 0.000 | 0.117 | 0.002 | within_budget |
| eslint | layer | 25 | 472 | 1/0 | 17 | 0.029 | 0.000 | 0.000 | 0.117 | 0.000 | within_budget |
