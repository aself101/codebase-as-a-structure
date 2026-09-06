# Can the budget fire? An adversarial ruleset at K = 5 (D-024)

*2026-09-05. `tests/fixtures/adversarial-dense.toml` — four features with thresholds placed in the dense part of their signals' distributions (`fan_in >= 2`, `size_loc >= 200`, `commit_count >= 3`, `load_index >= p50`). Same procedure as the D-018 reading: before = the M1b perturbation substrate (HEAD minus the last five timeline commits), after = HEAD, age geometry, substrate 0.3.0. The budget judges jitter over untouched rooms (D-024 operand). Popper's point: an instrument with no observed negative is not yet known to be an instrument.*

| repo | K | common | touched | jitter churn (untouched) | strata (untouched) | verdict | per feature (before, after, untouched changes) |
|---|---|---|---|---|---|---|---|
| typeorm | 5 | 583 | 7 | 0.000 | 0.000 | within_budget | {'medium_file': (96, 96, 0), 'mid_load': (292, 292, 0), 'three_commits': (500, 500, 0), 'two_importers': (372, 372, 0)} |
| mcp-secure-server | 5 | 202 | 14 | 0.000 | 0.000 | within_budget | {'medium_file': (38, 38, 0), 'mid_load': (101, 101, 0), 'three_commits': (52, 53, 0), 'two_importers': (88, 88, 0)} |
| uluops-registry-api | 5 | 267 | 0 | 0.000 | 0.000 | within_budget | {'medium_file': (58, 58, 0), 'mid_load': (134, 134, 0), 'three_commits': (154, 154, 0), 'two_importers': (148, 148, 0)} |
| eslint | 5 | 472 | 10 | 0.002 | 0.002 | within_budget | {'medium_file': (158, 159, 0), 'mid_load': (238, 237, 2), 'three_commits': (440, 440, 0), 'two_importers': (381, 382, 0)} |
