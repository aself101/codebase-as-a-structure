# Holdout report — validation gate

*validation `0.3.0` · substrate fingerprint `661f93333b65…` · validation fingerprint `778f5cc1faf5…`. Verdicts are stated for fix-**activity** (the declared §3.4.1 proxy), never defect origin.*

## Gate configuration (every floor, so a loosened one is visible here)

- holdout: frac 0.2, ROC margin +0.05, PR-AUC ×1.2, coverage ≥ 0.5, signal floor ×1.5 base rate, **min test repos 2**
- asserted: K 25, **stability eps 0.01 / delta 0.05**, min compared 30, max excluded 0.5, max modal share 0.97, τ floors G3 0.3 / G2 0.6, retire 0.85, **m_asserted 3**
- label regex (frozen, validation side): `\b(bug|hotfix|patch)\b`; bootstrap 1000, permutation 1000, seed 20260904
- substrate weights validated (the fingerprint's preimage): `load_index` = {fan_in_nonzero: 0.5, centrality: 0.3, inv_fan_out: 0.1, size_loc: 0.1}; `change_pressure_index` = {churn_lines: 0.5, commit_count: 0.2, recency: 0.3}; `bug_pressure_index` = {commit_count: 0.5, recency: 0.2, revert_count: 0.3}; `neglect_index` = {age_days: 0.4, last_touched_days: 0.4, inv_recent_commit_share: 0.2}; `complexity_proxy_index` = {size_loc: 0.4, nesting_proxy: 0.4, fan_out: 0.2}
- substrate feature-side fix regex: `\b(bug|hotfix|patch)\b` (same as label regex)
- toolchain: dep_extractor=dependency-cruiser@18.2.0, git=git@2.53.0, history=pydriller@2.11, python=python@3.13.12, substrate=repo-substrate@0.6.0

## Reference repos

| repo | role | expected (D-009) | HEAD | commits | nodes | population | split | holdout commits | eligible | coverage | positives | base rate | fix-label rate | degenerate |
|---|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| `typeorm` | test | test | `ac41823b9e` | 6065 | 3600 | 583 | `fe7f328fd5` | 1213 | 2274 | 0.632 | 1014 | 0.446 | 0.328 | – |
| `mcp-secure-server` | test | test | `5348b3ef61` | 145 | 264 | 203 | `654057ef9f` | 29 | 258 | 0.977 | 36 | 0.140 | 0.414 | – |
| `uluops-registry-api` | tuning | tuning | `f4f6ebd23e` | 964 | 456 | 267 | `f95d9bf5d4` | 193 | 405 | 0.888 | 131 | 0.323 | 0.295 | – |
| `eslint` | tuning | tuning | `3f20a57c62` | 11008 | 1481 | 473 | `3398431574` | 2202 | 1219 | 0.823 | 225 | 0.185 | 0.134 | – |

**Substrate attestations** (cache file → seed, sha256 of the scored bytes):

- `eslint-3398431574b9-trunc-661f93333b65.substrate.json`: seed `1dc7cfaaec63…`, bytes `968347c9fe7b…`
- `eslint-3f20a57c6293-tip-661f93333b65.substrate.json`: seed `a50b92780e08…`, bytes `77b249defee3…`
- `eslint-5c8c2417b9ff-trunc-661f93333b65.substrate.json`: seed `284a5c2ea9e7…`, bytes `9fefb41e6126…`
- `mcp-secure-server-4c99da71468c-trunc-661f93333b65.substrate.json`: seed `8fee00040541…`, bytes `fcf06bbc2658…`
- `mcp-secure-server-5348b3ef614d-tip-661f93333b65.substrate.json`: seed `0f53b2d16c24…`, bytes `f2380116c94e…`
- `mcp-secure-server-654057ef9f62-trunc-661f93333b65.substrate.json`: seed `8fee00040541…`, bytes `7bc2568770e3…`
- `typeorm-ac41823b9e27-tip-661f93333b65.substrate.json`: seed `33fbe1cfaa1a…`, bytes `873017b0c9e8…`
- `typeorm-f5c6aa3bfe9c-trunc-661f93333b65.substrate.json`: seed `190672469654…`, bytes `ffc863fd0eb5…`
- `typeorm-fe7f328fd5b9-trunc-661f93333b65.substrate.json`: seed `df3baed073ea…`, bytes `f013d6098c79…`
- `uluops-registry-api-8319623b2b77-trunc-661f93333b65.substrate.json`: seed `94ba0e0d9be4…`, bytes `7a7eaeb1e705…`
- `uluops-registry-api-f4f6ebd23eb4-tip-661f93333b65.substrate.json`: seed `dc1e90d46248…`, bytes `99cfe6fc6189…`
- `uluops-registry-api-f95d9bf5d4ca-trunc-661f93333b65.substrate.json`: seed `ce12785c4a35…`, bytes `e318a3445fc7…`

## 1. Verdict table — predictive signals

*Verdicts count **test**-role repos only (D-009); tuning-role rows are in-sample and shown for the record. Tuned config commit: `24c087a123e5`.*

| signal | status | repo | role | ROC-AUC | best-baseline ROC | PR-AUC | best-baseline PR | base rate | p@10 | τ(index, baseline) | passed | failed clauses |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `bug_pressure_index` | **unvalidated** | `typeorm` | test | 0.770 | 0.728 (busyness) | 0.759 | 0.717 | 0.446 | 1.000 | 0.73 | no | roc_margin, pr_auc_mult |
| `bug_pressure_index` | **unvalidated** | `mcp-secure-server` | test | 0.804 | 0.839 (recency) | 0.497 | 0.436 | 0.140 | 0.700 | 0.73 | no | roc_margin, pr_auc_mult |
| `bug_pressure_index` | **unvalidated** | `uluops-registry-api` | tuning | 0.721 | 0.700 (busyness) | 0.572 | 0.574 | 0.323 | 0.800 | 0.83 | no | roc_margin, pr_auc_mult |
| `bug_pressure_index` | **unvalidated** | `eslint` | tuning | 0.791 | 0.777 (busyness) | 0.462 | 0.431 | 0.185 | 0.800 | 0.83 | no | roc_margin, pr_auc_mult |
| `change_pressure_index` | **unvalidated** | `typeorm` | test | 0.878 | 0.728 (busyness) | 0.868 | 0.717 | 0.446 | 1.000 | 0.55 | yes | – |
| `change_pressure_index` | **unvalidated** | `mcp-secure-server` | test | 0.831 | 0.839 (recency) | 0.530 | 0.436 | 0.140 | 0.800 | 0.53 | no | roc_margin |
| `change_pressure_index` | **unvalidated** | `uluops-registry-api` | tuning | 0.746 | 0.700 (busyness) | 0.567 | 0.574 | 0.323 | 0.800 | 0.63 | no | roc_margin, pr_auc_mult |
| `change_pressure_index` | **unvalidated** | `eslint` | tuning | 0.807 | 0.777 (busyness) | 0.492 | 0.431 | 0.185 | 1.000 | 0.69 | no | roc_margin, pr_auc_mult |

## 2. Where it failed

- **`bug_pressure_index`** — `unvalidated` (passed_on_0_of_2_test_repos_need_2).
  - `typeorm`: ROC-AUC 0.770 vs busyness 0.728 (Δ +0.042, need +0.05); PR-AUC 0.759 vs 0.717 (×1.06, need ×1.2); failed: roc_margin, pr_auc_mult.
  - `mcp-secure-server`: ROC-AUC 0.804 vs recency 0.839 (Δ -0.035, need +0.05); PR-AUC 0.497 vs 0.436 (×1.14, need ×1.2); failed: roc_margin, pr_auc_mult.
  - `uluops-registry-api`: ROC-AUC 0.721 vs busyness 0.700 (Δ +0.021, need +0.05); PR-AUC 0.572 vs 0.574 (×1.00, need ×1.2); failed: roc_margin, pr_auc_mult.
  - `eslint`: ROC-AUC 0.791 vs busyness 0.777 (Δ +0.014, need +0.05); PR-AUC 0.462 vs 0.431 (×1.07, need ×1.2); failed: roc_margin, pr_auc_mult.
- **`change_pressure_index`** — `unvalidated` (passed_on_1_of_2_test_repos_need_2).
  - `typeorm`: ROC-AUC 0.878 vs busyness 0.728 (Δ +0.150, need +0.05); PR-AUC 0.868 vs 0.717 (×1.21, need ×1.2); passed.
  - `mcp-secure-server`: ROC-AUC 0.831 vs recency 0.839 (Δ -0.008, need +0.05); PR-AUC 0.530 vs 0.436 (×1.22, need ×1.2); failed: roc_margin.
  - `uluops-registry-api`: ROC-AUC 0.746 vs busyness 0.700 (Δ +0.047, need +0.05); PR-AUC 0.567 vs 0.574 (×0.99, need ×1.2); failed: roc_margin, pr_auc_mult.
  - `eslint`: ROC-AUC 0.807 vs busyness 0.777 (Δ +0.030, need +0.05); PR-AUC 0.492 vs 0.431 (×1.14, need ×1.2); failed: roc_margin, pr_auc_mult.

## 3. Coverage caveats

- `typeorm`: coverage 0.632 (2274 of 3600 HEAD nodes eligible).
- `mcp-secure-server`: coverage 0.977 (258 of 264 HEAD nodes eligible).
- `uluops-registry-api`: coverage 0.888 (405 of 456 HEAD nodes eligible).
- `eslint`: coverage 0.823 (1219 of 1481 HEAD nodes eligible).
- `neglect_index`: untested — unstable.
- `recent_commit_share`: untested — degenerate.
- `revert_count`: untested — degenerate.

## 4. Descriptive signals (§2.4)

*Grounding classes: G1 measurement (stability only; instrument is git or the file), G2 second instrument (fan_in ↔ an independent scanner; floor τ ≥ 0.6), G3 cross-modal (a different modality; floor τ ≥ 0.3), G4 derived (stability + every input asserted; the name carries no claim beyond its inputs). Stability compares nodes untouched by the K removed commits.*

| signal | class | status | repo | reason | stability med / p95 / max Δ (n; tail operand) | distinct | stable | counterpart | n | τ-b | 95% CI | perm p | corroborated |
|---|---|---|---|---|---:|---:|---|---|---:|---:|---|---:|---|
| `age_days` | G3 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529; max) | 236 | yes | `blame_age_median` | 583 | 0.483 | [0.427, 0.535] | 0.001 | yes |
| `age_days` | G3 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (173; max) | 15 | yes | `blame_age_median` | 203 | 0.851 | [0.755, 0.934] | 0.001 | yes |
| `age_days` | G3 | **asserted** | `uluops-registry-api` | – | 0.000 / 0.000 / 0.000 (227; max) | 115 | yes | `blame_age_median` | 267 | 0.792 | [0.734, 0.848] | 0.001 | yes |
| `age_days` | G3 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.000 (455; max) | 382 | yes | `blame_age_median` | 472 | 0.378 | [0.316, 0.437] | 0.001 | yes |
| `author_count` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529; max) | 37 | yes | `git log` | – | – | – | – | yes |
| `author_count` | G1 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (173; max) | 2 | yes | `git log` | – | – | – | – | yes |
| `author_count` | G1 | **asserted** | `uluops-registry-api` | degenerate | 0.000 / 0.000 / 0.000 (227; max) | 1 | no | `git log` | – | – | – | – | yes |
| `author_count` | G1 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.000 (455; max) | 48 | yes | `git log` | – | – | – | – | yes |
| `blame_age_median` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529; max) | 218 | yes | `git blame -w` | – | – | – | – | yes |
| `blame_age_median` | G1 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (173; max) | 16 | yes | `git blame -w` | – | – | – | – | yes |
| `blame_age_median` | G1 | **asserted** | `uluops-registry-api` | – | 0.000 / 0.000 / 0.000 (227; max) | 140 | yes | `git blame -w` | – | – | – | – | yes |
| `blame_age_median` | G1 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.000 (454; max) | 310 | yes | `git blame -w` | – | – | – | – | yes |
| `centrality` | G4 | **asserted** | `typeorm` | – | 0.002 / 0.004 / 0.241 (529; p95) | 56 | yes | `–` | – | – | – | – | derived |
| `centrality` | G4 | **asserted** | `mcp-secure-server` | – | 0.003 / 0.032 / 0.072 (173; p95) | 54 | yes | `–` | – | – | – | – | derived |
| `centrality` | G4 | **asserted** | `uluops-registry-api` | unstable | 0.013 / 0.022 / 0.211 (227; p95) | 52 | no | `–` | – | – | – | – | derived |
| `centrality` | G4 | **asserted** | `eslint` | – | 0.000 / 0.001 / 0.036 (455; p95) | 41 | yes | `–` | – | – | – | – | derived |
| `churn_lines` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529; max) | 290 | yes | `git log --numstat` | – | – | – | – | yes |
| `churn_lines` | G1 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (173; max) | 123 | yes | `git log --numstat` | – | – | – | – | yes |
| `churn_lines` | G1 | **asserted** | `uluops-registry-api` | – | 0.000 / 0.000 / 0.000 (227; max) | 155 | yes | `git log --numstat` | – | – | – | – | yes |
| `churn_lines` | G1 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.000 (455; max) | 396 | yes | `git log --numstat` | – | – | – | – | yes |
| `cochange_degree` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529; max) | 76 | yes | `git log co-occurrence (§5)` | – | – | – | – | yes |
| `cochange_degree` | G1 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (173; max) | 9 | yes | `git log co-occurrence (§5)` | – | – | – | – | yes |
| `cochange_degree` | G1 | **asserted** | `uluops-registry-api` | – | 0.000 / 0.000 / 0.000 (227; max) | 31 | yes | `git log co-occurrence (§5)` | – | – | – | – | yes |
| `cochange_degree` | G1 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.000 (455; max) | 46 | yes | `git log co-occurrence (§5)` | – | – | – | – | yes |
| `commit_count` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529; max) | 77 | yes | `git log` | – | – | – | – | yes |
| `commit_count` | G1 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (173; max) | 9 | yes | `git log` | – | – | – | – | yes |
| `commit_count` | G1 | **asserted** | `uluops-registry-api` | – | 0.000 / 0.000 / 0.000 (227; max) | 27 | yes | `git log` | – | – | – | – | yes |
| `commit_count` | G1 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.000 (455; max) | 75 | yes | `git log` | – | – | – | – | yes |
| `complexity_proxy_index` | G4 | **asserted** | `typeorm` | – | 0.001 / 0.003 / 0.004 (529; p95) | 381 | yes | `–` | – | – | – | – | derived |
| `complexity_proxy_index` | G4 | **asserted** | `mcp-secure-server` | – | 0.004 / 0.009 / 0.012 (173; p95) | 152 | yes | `–` | – | – | – | – | derived |
| `complexity_proxy_index` | G4 | **asserted** | `uluops-registry-api` | – | 0.002 / 0.005 / 0.008 (227; p95) | 207 | yes | `–` | – | – | – | – | derived |
| `complexity_proxy_index` | G4 | **asserted** | `eslint` | – | 0.000 / 0.001 / 0.002 (455; p95) | 403 | yes | `–` | – | – | – | – | derived |
| `fan_in` | G2 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.018 (529; p95) | 49 | yes | `fan_in_alt` | 582 | 0.999 | [0.998, 1.000] | 0.001 | yes |
| `fan_in` | G2 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.020 (173; p95) | 12 | yes | `fan_in_alt` | 203 | 1.000 | [1.000, 1.000] | 0.001 | yes |
| `fan_in` | G2 | **asserted** | `uluops-registry-api` | – | 0.000 / 0.002 / 0.086 (227; p95) | 22 | yes | `fan_in_alt` | 261 | 0.995 | [0.991, 0.998] | 0.001 | yes |
| `fan_in` | G2 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.010 (455; p95) | 14 | yes | `fan_in_alt` | 472 | 0.992 | [0.980, 1.000] | 0.001 | yes |
| `fan_in_nonzero` | G4 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.019 (508; p95) | 48 | yes | `–` | – | – | – | – | derived |
| `fan_in_nonzero` | G4 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.002 / 0.027 (130; p95) | 11 | yes | `–` | – | – | – | – | derived |
| `fan_in_nonzero` | G4 | **asserted** | `uluops-registry-api` | – | 0.000 / 0.004 / 0.149 (131; p95) | 21 | yes | `–` | – | – | – | – | derived |
| `fan_in_nonzero` | G4 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.011 (397; p95) | 13 | yes | `–` | – | – | – | – | derived |
| `fan_out` | G2 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529; p95) | 32 | yes | `fan_out_alt` | 582 | 0.997 | [0.994, 0.999] | 0.001 | yes |
| `fan_out` | G2 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (173; p95) | 8 | yes | `fan_out_alt` | 203 | 1.000 | [1.000, 1.000] | 0.001 | yes |
| `fan_out` | G2 | **asserted** | `uluops-registry-api` | – | 0.000 / 0.000 / 0.000 (227; p95) | 14 | yes | `fan_out_alt` | 261 | 1.000 | [1.000, 1.000] | 0.001 | yes |
| `fan_out` | G2 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.000 (455; p95) | 9 | yes | `fan_out_alt` | 472 | 0.996 | [0.990, 1.000] | 0.001 | yes |
| `fix_count` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529; max) | 26 | yes | `git log` | – | – | – | – | yes |
| `fix_count` | G1 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (173; max) | 4 | yes | `git log` | – | – | – | – | yes |
| `fix_count` | G1 | **asserted** | `uluops-registry-api` | – | 0.000 / 0.000 / 0.000 (227; max) | 19 | yes | `git log` | – | – | – | – | yes |
| `fix_count` | G1 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.000 (455; max) | 26 | yes | `git log` | – | – | – | – | yes |
| `has_sibling_test` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529; p95) | 2 | yes | `path convention config (§6.2.2)` | – | – | – | – | yes |
| `has_sibling_test` | G1 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (173; p95) | 2 | yes | `path convention config (§6.2.2)` | – | – | – | – | yes |
| `has_sibling_test` | G1 | **asserted** | `uluops-registry-api` | – | 0.000 / 0.000 / 0.000 (227; p95) | 2 | yes | `path convention config (§6.2.2)` | – | – | – | – | yes |
| `has_sibling_test` | G1 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.000 (455; p95) | 2 | yes | `path convention config (§6.2.2)` | – | – | – | – | yes |
| `is_package_entry` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529; p95) | 2 | yes | `package.json main/module/browser/types/bin/exports` | – | – | – | – | yes |
| `is_package_entry` | G1 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (173; p95) | 2 | yes | `package.json main/module/browser/types/bin/exports` | – | – | – | – | yes |
| `is_package_entry` | G1 | **asserted** | `uluops-registry-api` | degenerate | 0.000 / 0.000 / 0.000 (227; p95) | 1 | no | `package.json main/module/browser/types/bin/exports` | – | – | – | – | yes |
| `is_package_entry` | G1 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.000 (455; p95) | 2 | yes | `package.json main/module/browser/types/bin/exports` | – | – | – | – | yes |
| `last_touched_days` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529; max) | 97 | yes | `git log author_date` | – | – | – | – | yes |
| `last_touched_days` | G1 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (173; max) | 32 | yes | `git log author_date` | – | – | – | – | yes |
| `last_touched_days` | G1 | **asserted** | `uluops-registry-api` | – | 0.000 / 0.000 / 0.000 (227; max) | 119 | yes | `git log author_date` | – | – | – | – | yes |
| `last_touched_days` | G1 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.000 (455; max) | 125 | yes | `git log author_date` | – | – | – | – | yes |
| `load_index` | G4 | **asserted** | `typeorm` | – | 0.001 / 0.001 / 0.070 (529; p95) | 452 | yes | `–` | – | – | – | – | derived |
| `load_index` | G4 | **asserted** | `mcp-secure-server` | – | 0.006 / 0.015 / 0.041 (173; p95) | 158 | yes | `–` | – | – | – | – | derived |
| `load_index` | G4 | **asserted** | `uluops-registry-api` | – | 0.004 / 0.009 / 0.102 (227; p95) | 202 | yes | `–` | – | – | – | – | derived |
| `load_index` | G4 | **asserted** | `eslint` | – | 0.001 / 0.001 / 0.012 (455; p95) | 379 | yes | `–` | – | – | – | – | derived |
| `neglect_index` | G3 | **untested** | `typeorm` | unstable | 0.010 / 0.031 / 0.101 (529; p95) | 411 | no | `blame_age_median` | 583 | 0.564 | [0.519, 0.602] | 0.001 | yes |
| `neglect_index` | G3 | **untested** | `mcp-secure-server` | unstable | 0.002 / 0.109 / 0.257 (173; p95) | 45 | no | `blame_age_median` | 203 | 0.611 | [0.525, 0.695] | 0.001 | yes |
| `neglect_index` | G3 | **untested** | `uluops-registry-api` | unstable | 0.014 / 0.055 / 0.219 (227; p95) | 185 | no | `blame_age_median` | 267 | 0.651 | [0.600, 0.697] | 0.001 | yes |
| `neglect_index` | G3 | **untested** | `eslint` | input_not_asserted:recent_commit_share | 0.004 / 0.014 / 0.067 (455; p95) | 416 | yes | `blame_age_median` | 472 | 0.373 | [0.320, 0.427] | 0.001 | yes |
| `nesting_proxy` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529; max) | 19 | yes | `indent counter (§6.2.2)` | – | – | – | – | yes |
| `nesting_proxy` | G1 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (173; max) | 9 | yes | `indent counter (§6.2.2)` | – | – | – | – | yes |
| `nesting_proxy` | G1 | **asserted** | `uluops-registry-api` | – | 0.000 / 0.000 / 0.000 (227; max) | 11 | yes | `indent counter (§6.2.2)` | – | – | – | – | yes |
| `nesting_proxy` | G1 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.000 (455; max) | 21 | yes | `indent counter (§6.2.2)` | – | – | – | – | yes |
| `recent_commit_share` | G1 | **untested** | `typeorm` | – | 0.003 / 0.009 / 0.356 (529; p95) | 130 | yes | `git log (timeline-relative window, §6.2.2)` | – | – | – | – | yes |
| `recent_commit_share` | G1 | **untested** | `mcp-secure-server` | degenerate | 0.043 / 0.451 / 0.488 (173; p95) | 1 | no | `git log (timeline-relative window, §6.2.2)` | – | – | – | – | yes |
| `recent_commit_share` | G1 | **untested** | `uluops-registry-api` | unstable | 0.011 / 0.046 / 0.634 (227; p95) | 30 | no | `git log (timeline-relative window, §6.2.2)` | – | – | – | – | yes |
| `recent_commit_share` | G1 | **untested** | `eslint` | – | 0.003 / 0.010 / 0.116 (455; p95) | 180 | yes | `git log (timeline-relative window, §6.2.2)` | – | – | – | – | yes |
| `reinforcement_index` | G4 | **asserted** | `typeorm` | – | 0.000 / 0.001 / 0.610 (529; p95) | 28 | yes | `–` | – | – | – | – | derived |
| `reinforcement_index` | G4 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.003 / 0.309 (173; p95) | 5 | yes | `–` | – | – | – | – | derived |
| `reinforcement_index` | G4 | **asserted** | `uluops-registry-api` | – | 0.000 / 0.002 / 0.650 (227; p95) | 12 | yes | `–` | – | – | – | – | derived |
| `reinforcement_index` | G4 | **asserted** | `eslint` | – | 0.001 / 0.001 / 0.003 (455; p95) | 8 | yes | `–` | – | – | – | – | derived |
| `revert_count` | G1 | **untested** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529; max) | 4 | yes | `git log` | – | – | – | – | yes |
| `revert_count` | G1 | **untested** | `mcp-secure-server` | degenerate | 0.000 / 0.000 / 0.000 (173; max) | 1 | no | `git log` | – | – | – | – | yes |
| `revert_count` | G1 | **untested** | `uluops-registry-api` | degenerate | 0.000 / 0.000 / 0.000 (227; max) | 1 | no | `git log` | – | – | – | – | yes |
| `revert_count` | G1 | **untested** | `eslint` | degenerate | 0.000 / 0.000 / 0.000 (455; max) | 3 | no | `git log` | – | – | – | – | yes |
| `size_loc` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529; max) | 194 | yes | `non-blank line count` | – | – | – | – | yes |
| `size_loc` | G1 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (173; max) | 121 | yes | `non-blank line count` | – | – | – | – | yes |
| `size_loc` | G1 | **asserted** | `uluops-registry-api` | – | 0.000 / 0.000 / 0.000 (227; max) | 144 | yes | `non-blank line count` | – | – | – | – | yes |
| `size_loc` | G1 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.000 (455; max) | 267 | yes | `non-blank line count` | – | – | – | – | yes |
| `test_fan_in` | G2 | **asserted** | `typeorm` | – | 0.001 / 0.001 / 0.428 (529; p95) | 28 | yes | `test_fan_in_alt` | 582 | 0.997 | [0.990, 1.000] | 0.001 | yes |
| `test_fan_in` | G2 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.006 / 0.188 (173; p95) | 5 | yes | `test_fan_in_alt` | 203 | 1.000 | [1.000, 1.000] | 0.001 | yes |
| `test_fan_in` | G2 | **asserted** | `uluops-registry-api` | – | 0.002 / 0.004 / 0.416 (227; p95) | 12 | yes | `test_fan_in_alt` | 261 | 0.986 | [0.976, 0.995] | 0.001 | yes |
| `test_fan_in` | G2 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.004 (455; p95) | 8 | yes | `test_fan_in_alt` | 472 | 0.992 | [0.978, 1.000] | 0.001 | yes |

**Declared heuristics inside G1 (bounded risks, not certifications):**

- `author_count`: author email, no mailmap (inflates on multi-email authors)
- `blame_age_median`: blame line attribution; no -M/-C
- `fix_count`: §7 subject classifier (regex over commit subjects; also the holdout label)
- `has_sibling_test`: filename adjacency; literal name, convention-dependent
- `is_package_entry`: built entry → source mapping (./index.js → src/index.ts, dir → index)
- `nesting_proxy`: indentation depth as a stand-in for nesting
- `revert_count`: §7 subject classifier

**Non-discriminating pairs (min lower-CI τ ≥ 0.85 on every repo — cannot fail, so not a falsifier; adversarial fixture required):** `fan_in (fixture-backed: tests/test_instruments.py)`, `fan_out (fixture-backed: tests/test_instruments.py)`, `test_fan_in (fixture-backed: tests/test_instruments.py)`

**τ distribution across repos (the §2.4 known limit — a counterpart that cannot fail is not a falsifier):**

- `age_days` ↔ `blame_age_median` (G3): 0.48, 0.85, 0.79, 0.38
- `fan_in` ↔ `fan_in_alt` (G2): 1.00, 1.00, 0.99, 0.99
- `fan_out` ↔ `fan_out_alt` (G2): 1.00, 1.00, 1.00, 1.00
- `neglect_index` ↔ `blame_age_median` (G3): 0.56, 0.61, 0.65, 0.37
- `test_fan_in` ↔ `test_fan_in_alt` (G2): 1.00, 1.00, 0.99, 0.99

**Reported correlates (never gating):**

- `centrality` ~ `cochange_degree` on `typeorm`: τ 0.13 [0.07, 0.20]
- `centrality` ~ `cochange_degree` on `mcp-secure-server`: τ 0.32 [0.21, 0.41]
- `centrality` ~ `cochange_degree` on `uluops-registry-api`: τ 0.39 [0.30, 0.46]
- `centrality` ~ `cochange_degree` on `eslint`: τ 0.05 [-0.04, 0.14]
- `load_index` ~ `cochange_degree` on `typeorm`: τ 0.19 [0.13, 0.25]
- `load_index` ~ `test_fan_in` on `typeorm`: τ 0.42 [0.38, 0.46]
- `load_index` ~ `cochange_degree` on `mcp-secure-server`: τ 0.34 [0.24, 0.42]
- `load_index` ~ `test_fan_in` on `mcp-secure-server`: τ 0.54 [0.47, 0.60]
- `load_index` ~ `cochange_degree` on `uluops-registry-api`: τ 0.39 [0.31, 0.46]
- `load_index` ~ `test_fan_in` on `uluops-registry-api`: τ 0.72 [0.69, 0.75]
- `load_index` ~ `cochange_degree` on `eslint`: τ 0.15 [0.07, 0.23]
- `load_index` ~ `test_fan_in` on `eslint`: τ 0.45 [0.37, 0.52]
- `neglect_index` ~ `cochange_degree` on `typeorm`: τ 0.11 [0.05, 0.16]
- `neglect_index` ~ `cochange_degree` on `mcp-secure-server`: τ -0.27 [-0.35, -0.18]
- `neglect_index` ~ `cochange_degree` on `uluops-registry-api`: τ -0.12 [-0.20, -0.04]
- `neglect_index` ~ `cochange_degree` on `eslint`: τ 0.10 [0.04, 0.15]
- `reinforcement_index` ~ `has_sibling_test` on `typeorm`: τ 0.20 [0.12, 0.27]
- `reinforcement_index` ~ `has_sibling_test` on `mcp-secure-server`: τ 0.50 [0.39, 0.60]
- `reinforcement_index` ~ `has_sibling_test` on `uluops-registry-api`: τ 0.56 [0.48, 0.66]
- `reinforcement_index` ~ `has_sibling_test` on `eslint`: τ 0.72 [0.60, 0.81]

## 5. Cross-source corroboration (§3A)

- Not run in M1 (D-005): §3A is built after the holdout leaves a `validated` signal to corroborate.

## 6. Recognition record (§2.4.3, D-010) — sealed rankings, n = 1, never gating

### `mcp-secure-server` — `blind/mcp-secure-server.md`

*Provenance of this fill: written by Claude (Fable 5.1) at Alex's request, from session-memory (chiefly: the per-tool policy requirement, the -32602 rejection, the 0.0.20-security vs ^0.0.6-security split across consumers, the five-layer pipeline, the self-contained cookbook) plus `git rev-parse HEAD`, `git ls-files`, and the root `package.json` name/version/dependency keys. No `git log`, no `git blame`, no import tracing, no source contents were read. Knowledge here is thinner than for registry-api; sections 3 and 4 in particular are guesses from the layer naming, not from having watched the repo move.*

| signal | source | ranked & present | overlap@10 | τ-b on ranked | items not in substrate |
|---|---|---:|---:|---:|---|
| `bug_pressure_index` | list 2 | 10 | 0.30 | -0.60 | – |
| `change_pressure_index` | list 3 | 9 | 0.30 | -0.17 | `CHANGELOG.md`, `README.md` |

> ## 5. The one structural fact
> 
> The library is a five-layer sequential validation pipeline wrapped around the MCP SDK transport, gated by a per-tool policy registry that rejects any unregistered tool at the protocol layer. Roughly two-thirds of the tracked files are not the library at all but twelve independent cookbook projects, each with its own `package.json` and lockfile, pointing back at the parent; a map that treats the repo as one package will draw the cookbook as the body and the library as an appendix.

> ## 6. Anything you expect the metrics to get wrong
> 
> 
> - `cookbook/**` — twelve self-contained example servers. They will dominate file count, line count, and churn while being leaf consumers with zero inbound edges from `src/`.
> - `cookbook/*/package-lock.json` (×11) plus `cookbook/package-lock.json` and the root lockfile — lockfile churn will register as activity.
> - `cookbook/tool-policies-server/tool-policies-server-1.0.0.tgz` — a checked-in tarball; any size or binary metric will spike on it.
> - `cookbook/test-data/*.txt`, `cookbook/filesystem-server/data/*`, `cookbook/filesystem-server/documents/**` — fixtures, not code.
> - `cookbook/image-gen-server/src/index-debug.ts`, `cookbook/image-gen-server/src/index-minimal.ts` — parallel variants of one entry point; a similarity or duplication metric will flag them as a problem when they are deliberate.
> - `src/security/layers/layer-utils/content/patterns/*.ts` — regex tables. Large and edited often, low structural reach; size and churn will overstate centrality.
> - Tests are `.js` under `test/` while `src/` is `.ts`. Any language-partitioned metric will split the repo in two and may under-count test coverage of the library.
> - `test/helpers/message-builders.js`, `test/setup/global-setup.js` — reached by every test, by nothing in `src/`; fan-in without being load-bearing for consumers.
> - `AGENTS.md` and `CLAUDE.md` — two agent-instruction files at the root; likely near-duplicates, and a doc metric will count them as documentation of the package.
> - The dependency edges that matter most are outbound from this repo: `ops-uluops-mcp` and `uluops-registry-mcp` pin `0.0.20-security`, `packages/-uluops-rah-mcp-server` pins `^0.0.6-security`. Nothing inside this repo's tree can show that its consumers sit on two incompatible policy shapes.

### `uluops-registry-api` — `blind/uluops-registry-api.md`

*Provenance of this fill: written by Claude (Fable 5.1) at Alex's request, from session-memory of prior work on this repo plus `git rev-parse HEAD` and `git ls-files` only. No `git log`, no `git blame`, no import tracing, no file contents were read. The listing was used solely to make paths valid. Treat the rankings as a model's priors, not the maintainer's.*

| signal | source | ranked & present | overlap@10 | τ-b on ranked | items not in substrate |
|---|---|---:|---:|---:|---|
| `bug_pressure_index` | list 2 | 9 | 0.10 | -0.28 | `package.json` |
| `change_pressure_index` | list 3 | 8 | 0.10 | 0.07 | `package.json`, `package-lock.json`, `CHANGELOG.md` |

> ## 5. The one structural fact
> 
> The repo does not own its own substance: rendered `runtime_md` is stored at publish time from `@uluops/definition-factory`, so the load-bearing thing is an npm pin plus a stored column, not anything in `src/`. A map that draws only the in-repo import graph will show a well-shaped Express service and miss that its output is frozen by an external version number until someone retranslates the corpus.

> ## 6. Anything you expect the metrics to get wrong
> 
> 
> - `src/db/migrations/*` — ~60 files, imported by nothing in `src/`, append-only churn. An import-graph metric scores them zero; a churn metric scores the directory high; both are wrong about what they mean.
> - `scripts/backfill-*.ts` — one-shot scripts that are dead the day after they run but stay tracked; churn without ongoing dependence.
> - `package-lock.json` — huge, churns on every pin bump, carries no structure.
> - `docs/adr/*.md`, `plans/*.md` — zero imports, but they are the decision strata; a map that ignores prose misses the why.
> - `src/schemas/CLAUDE.md`, `src/schemas/adl/CLAUDE.md` — agent instructions living inside the source tree, will be counted as documentation-of-code when they are instructions-to-a-tool.
> - `src/services/safety/signals.ts` — a data table of regexes; large and frequently edited, low structural reach. Size and churn will overstate its centrality.
> - Barrels (`src/utils/index.ts`, `src/services/index.ts`, `src/db/repository/index.ts`, `src/schemas/index.ts`, `src/middleware/index.ts`, `src/controllers/index.ts`) — inflate fan-in for whatever they re-export and will crowd the load-bearing list.
> - `src/terminal/*` — startup banner; touched in cosmetic bursts, reached only from `src/index.ts`. Will look more central than it is.
> - The dual-database architecture (ADR-003): the auth DB is shared with the platform and not modelled in this repo's migrations at all. Nothing in the file tree signals that half the schema lives elsewhere.
