# Skeleton-level stability budget — re-read under `179d8acb7b0c` (2026-09-06b)

*Procedure of D-018 with the D-024/D-026 operand: before = the gate's stability-perturbation substrate (HEAD minus the last K = 25 timeline commits), after = HEAD; maintainability + onboarding; gate `out/validation-k25/validation.json`.*

| repo | geometry | K | common | born/del | touched | churn (all) | strata (all) | jitter churn | clock churn | strata (untouched) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| typeorm | age | 25 | 583 | 0/0 | 54 | 0.135 | 0.000 | 0.012 | 0.333 | 0.000 | within_budget |
| typeorm | layer | 25 | 583 | 0/0 | 54 | 0.135 | 0.000 | 0.012 | 0.333 | 0.000 | within_budget |
| mcp-secure-server | age | 25 | 201 | 1/0 | 22 | 0.129 | 0.000 | 0.011 | 0.263 | 0.000 | within_budget |
| mcp-secure-server | layer | 25 | 201 | 1/0 | 22 | 0.129 | 0.025 | 0.011 | 0.263 | 0.011 | within_budget |
| uluops-registry-api | age | 25 | 264 | 3/0 | 42 | 0.171 | 0.015 | 0.013 | 0.491 | 0.018 | within_budget |
| uluops-registry-api | layer | 25 | 264 | 3/0 | 42 | 0.171 | 0.087 | 0.013 | 0.491 | 0.090 | over_budget |
| eslint | age | 25 | 472 | 1/0 | 17 | 0.033 | 0.002 | 0.003 | 0.117 | 0.002 | within_budget |
| eslint | layer | 25 | 472 | 1/0 | 17 | 0.033 | 0.000 | 0.003 | 0.117 | 0.000 | within_budget |
