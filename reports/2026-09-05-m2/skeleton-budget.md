# Skeleton-level stability budget — first full reading (D-018)

*2026-09-05. Instrument: `substrate skeleton-diff` (mapper §7 Q3, D-017), extended with the touched/untouched split. Before = the stability-perturbation substrate the M1 gate already cached (HEAD with the last K = 5 timeline commits removed, `validation.json` `perturbed_sha`); after = HEAD. Both mapped with `rulesets/maintainability.toml` + `--overlay rulesets/onboarding.toml` under `reports/2026-09-04-m1/validation.json`, substrate fingerprint `80b2a632f8b7`. Whole-population churn is what a reader of two adjacent pictures sees; untouched-population churn is ripple, and the budget is judged on it.*

| repo | geometry | commits | common | born/del | touched | churn (all) | strata (all) | churn (untouched) | strata (untouched) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| uluops-registry-api | age | 5 | 267 | 0/0 | 0 | 0.011 | 0.011 | 0.011 | 0.011 | within_budget |
| uluops-registry-api | layer | 5 | 267 | 0/0 | 0 | 0.011 | 0.000 | 0.011 | 0.000 | within_budget |
| mcp-secure-server | age | 5 | 202 | 0/0 | 14 | 0.022 | 0.000 | 0.014 | 0.000 | within_budget |
| mcp-secure-server | layer | 5 | 202 | 0/0 | 14 | 0.022 | 0.040 | 0.014 | 0.032 | within_budget |
| eslint | age | 5 | 472 | 1/0 | 10 | 0.018 | 0.002 | 0.009 | 0.002 | within_budget |
| eslint | layer | 5 | 472 | 1/0 | 10 | 0.018 | 0.000 | 0.009 | 0.000 | within_budget |
| typeorm | age | 5 | 583 | 0/0 | 7 | 0.013 | 0.000 | 0.005 | 0.000 | within_budget |
| typeorm | layer | 5 | 583 | 0/0 | 7 | 0.013 | 0.000 | 0.005 | 0.000 | within_budget |

**Budget (D-018):** untouched `feature_churn ≤ 0.05` and untouched `strata_moved_frac ≤ 0.05`, floors `min_untouched_n = 30` and `max_touched_frac = 0.5`; enforced in `src/repo_substrate/mapper/diff.py::skeleton_diff` (`SKELETON_BUDGET`).

**Readings.**
- Feature churn is identical across geometries on every repo, as it must be: features read signals, not strata.
- `uluops-registry-api`'s five commits touched no source node (CHANGELOG, package.json, lockfile only) and the skeleton still moved: `age_days` / `last_touched_days` are measured from HEAD's timestamp, so removing commits moves the clock. Age geometry moves under time alone; that is the signal reporting the passage of time, and it is within budget.
- The tightest margin is `mcp-secure-server` under the layer geometry (0.032 untouched strata): a change to one node's longest path to a leaf re-layers every importer above it, and a 139-commit repo with few layers has nowhere to absorb it. Layer geometry is the less stable of the two; whether it needs its own ceiling is a Phase 1 (time-lapse) question.
- Ripple in features is concentrated in percentile-threshold features (`lit_room`, `hub`, `flooded_basement`): a node sitting near p90 crosses it when the ECDF shifts under edits elsewhere. This is the jitter the budget exists to bound; at ≤ 0.014 it is far from it.
