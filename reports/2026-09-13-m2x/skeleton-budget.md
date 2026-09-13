# Skeleton-level stability budget — re-read under `115c4483645a` (2026-09-13)

*Procedure of D-018 with the D-024/D-026 operand: before = the gate's stability-perturbation substrate (HEAD minus the last K = 25 timeline commits), after = HEAD; maintainability + onboarding; gate `out/validation-k25d/validation.json`.*

| repo | geometry | K | common | born/del | touched | churn (all) | strata (all) | jitter churn | clock churn | strata (untouched) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| typeorm | age | 25 | 583 | 0/0 | 54 | 0.135 | 0.000 | 0.012 | 0.333 | 0.000 | within_budget |
| typeorm | layer | 25 | 583 | 0/0 | 54 | 0.135 | 0.000 | 0.012 | 0.333 | 0.000 | within_budget |
| mcp-secure-server | age | 25 | 202 | 1/0 | 29 | 0.103 | 0.000 | 0.000 | 0.208 | 0.000 | within_budget |
| mcp-secure-server | layer | 25 | 202 | 1/0 | 29 | 0.103 | 0.045 | 0.000 | 0.208 | 0.035 | within_budget |
| uluops-registry-api | age | 25 | 265 | 2/0 | 39 | 0.171 | 0.015 | 0.013 | 0.526 | 0.018 | within_budget |
| uluops-registry-api | layer | 25 | 265 | 2/0 | 39 | 0.171 | 0.087 | 0.013 | 0.526 | 0.088 | over_budget |
| eslint | age | 25 | 472 | 1/0 | 17 | 0.033 | 0.002 | 0.003 | 0.117 | 0.002 | within_budget |
| eslint | layer | 25 | 472 | 1/0 | 17 | 0.033 | 0.000 | 0.003 | 0.117 | 0.000 | within_budget |
