# Skeleton-level stability budget — re-read under substrate 0.3.0 (D-022 addendum)

*2026-09-05. Same procedure as `reports/2026-09-05-m2/skeleton-budget.md` (D-018): before = the M1b gate's stability-perturbation substrate (HEAD with the last K = 5 timeline commits removed), after = HEAD; maintainability + onboarding overlay; gate `reports/2026-09-05-m1b/validation.json`, substrate fingerprint `5f5554e36d4a`. Age and recency are fractional days (D-022).*

| repo | geometry | commits | common | born/del | touched | churn (all) | strata (all) | churn (untouched) | strata (untouched) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| typeorm | age | 5 | 583 | 0/0 | 7 | 0.018 | 0.000 | 0.010 | 0.000 | within_budget |
| typeorm | layer | 5 | 583 | 0/0 | 7 | 0.018 | 0.000 | 0.010 | 0.000 | within_budget |
| mcp-secure-server | age | 5 | 202 | 0/0 | 14 | 0.051 | 0.000 | 0.038 | 0.000 | within_budget |
| mcp-secure-server | layer | 5 | 202 | 0/0 | 14 | 0.051 | 0.040 | 0.038 | 0.032 | within_budget |
| uluops-registry-api | age | 5 | 267 | 0/0 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | within_budget |
| uluops-registry-api | layer | 5 | 267 | 0/0 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | within_budget |
| eslint | age | 5 | 472 | 1/0 | 10 | 0.018 | 0.002 | 0.009 | 0.002 | within_budget |
| eslint | layer | 5 | 472 | 1/0 | 10 | 0.018 | 0.000 | 0.009 | 0.000 | within_budget |
