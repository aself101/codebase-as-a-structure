# Holdout report — validation gate

*validation `0.3.0` · substrate fingerprint `179d8acb7b0c…` · validation fingerprint `a9eaac785fb6…`. Verdicts are stated for fix-**activity** (the declared §3.4.1 proxy), never defect origin.*

## Gate configuration (every floor, so a loosened one is visible here)

- holdout: frac 0.2, ROC margin +0.05, PR-AUC ×1.2, coverage ≥ 0.5, signal floor ×1.5 base rate, **min test repos 2**
- asserted: K 25, **stability eps 0.05 / delta 0.15**, min compared 30, max excluded 0.5, max modal share 0.97, τ floors G3 0.3 / G2 0.6, retire 0.85, **m_asserted 2**
- label regex (frozen, validation side): `\b(bug|hotfix|patch)\b`; bootstrap 1000, permutation 1000, seed 20260904
- substrate weights validated (the fingerprint's preimage): `load_index` = {fan_in_nonzero: 0.5, centrality: 0.3, inv_fan_out: 0.1, size_loc: 0.1}; `change_pressure_index` = {churn_lines: 0.5, commit_count: 0.2, recency: 0.3}; `bug_pressure_index` = {commit_count: 0.5, recency: 0.2, revert_count: 0.3}; `neglect_index` = {age_days: 0.4, last_touched_days: 0.4, inv_recent_commit_share: 0.2}; `complexity_proxy_index` = {size_loc: 0.4, nesting_proxy: 0.4, fan_out: 0.2}
- substrate feature-side fix regex: `\b(bug|hotfix|patch)\b` (same as label regex)
- toolchain: dep_extractor=dependency-cruiser@18.2.0, git=git@2.53.0, history=pydriller@2.11, python=python@3.13.12, substrate=repo-substrate@0.4.1

## Reference repos

| repo | role | expected (D-009) | HEAD | commits | nodes | population | split | holdout commits | eligible | coverage | positives | base rate | fix-label rate | degenerate |
|---|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| `typeorm` | test | test | `ac41823b9e` | 6065 | 3600 | 583 | `fe7f328fd5` | 1213 | 2274 | 0.632 | 1014 | 0.446 | 0.328 | – |
| `mcp-secure-server` | test | test | `ecb30716b8` | 139 | 260 | 202 | `3f55fd476d` | 28 | 257 | 0.988 | 22 | 0.086 | 0.464 | – |
| `uluops-registry-api` | tuning | tuning | `f7414cc7bb` | 956 | 456 | 267 | `417d4387a0` | 192 | 403 | 0.884 | 132 | 0.328 | 0.312 | – |
| `eslint` | tuning | tuning | `3f20a57c62` | 11008 | 1481 | 473 | `3398431574` | 2202 | 1219 | 0.823 | 225 | 0.185 | 0.134 | – |

**Substrate attestations** (cache file → seed, sha256 of the scored bytes):

- `eslint-3398431574b9-trunc-179d8acb7b0c.substrate.json`: seed `1dc7cfaaec63…`, bytes `17969318ad52…`
- `eslint-3f20a57c6293-tip-179d8acb7b0c.substrate.json`: seed `a50b92780e08…`, bytes `265d9ea22c90…`
- `eslint-5c8c2417b9ff-trunc-179d8acb7b0c.substrate.json`: seed `284a5c2ea9e7…`, bytes `920209db16a6…`
- `mcp-secure-server-205ab1b4ffff-trunc-179d8acb7b0c.substrate.json`: seed `645081de9b36…`, bytes `462e91bd1691…`
- `mcp-secure-server-3f55fd476ded-trunc-179d8acb7b0c.substrate.json`: seed `5fad71a46159…`, bytes `8c0cd4e44510…`
- `mcp-secure-server-ecb30716b87e-tip-179d8acb7b0c.substrate.json`: seed `2c7db66a25f4…`, bytes `e9e162a7ec87…`
- `typeorm-ac41823b9e27-tip-179d8acb7b0c.substrate.json`: seed `33fbe1cfaa1a…`, bytes `86bbc8fbf86d…`
- `typeorm-f5c6aa3bfe9c-trunc-179d8acb7b0c.substrate.json`: seed `190672469654…`, bytes `b8051e3cf3f4…`
- `typeorm-fe7f328fd5b9-trunc-179d8acb7b0c.substrate.json`: seed `df3baed073ea…`, bytes `fbb3065ccae1…`
- `uluops-registry-api-417d4387a048-trunc-179d8acb7b0c.substrate.json`: seed `f564280e55a8…`, bytes `26824b1e979c…`
- `uluops-registry-api-6aba3f0c0996-trunc-179d8acb7b0c.substrate.json`: seed `e5c3fecb1f4b…`, bytes `127879a44012…`
- `uluops-registry-api-f7414cc7bbec-tip-179d8acb7b0c.substrate.json`: seed `c576e0759dc9…`, bytes `84d20541af6d…`

## 1. Verdict table — predictive signals

*Verdicts count **test**-role repos only (D-009); tuning-role rows are in-sample and shown for the record. Tuned config commit: `24c087a123e5`.*

| signal | status | repo | role | ROC-AUC | best-baseline ROC | PR-AUC | best-baseline PR | base rate | p@10 | τ(index, baseline) | passed | failed clauses |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `bug_pressure_index` | **unvalidated** | `typeorm` | test | 0.770 | 0.728 (busyness) | 0.759 | 0.717 | 0.446 | 1.000 | 0.73 | no | roc_margin, pr_auc_mult |
| `bug_pressure_index` | **unvalidated** | `mcp-secure-server` | test | 0.828 | 0.821 (recency) | 0.387 | 0.257 | 0.086 | 0.400 | 0.74 | no | roc_margin |
| `bug_pressure_index` | **unvalidated** | `uluops-registry-api` | tuning | 0.721 | 0.697 (busyness) | 0.584 | 0.585 | 0.328 | 1.000 | 0.82 | no | roc_margin, pr_auc_mult |
| `bug_pressure_index` | **unvalidated** | `eslint` | tuning | 0.791 | 0.777 (busyness) | 0.462 | 0.431 | 0.185 | 0.800 | 0.83 | no | roc_margin, pr_auc_mult |
| `change_pressure_index` | **unvalidated** | `typeorm` | test | 0.878 | 0.728 (busyness) | 0.868 | 0.717 | 0.446 | 1.000 | 0.55 | yes | – |
| `change_pressure_index` | **unvalidated** | `mcp-secure-server` | test | 0.854 | 0.821 (recency) | 0.424 | 0.257 | 0.086 | 0.600 | 0.53 | no | roc_margin |
| `change_pressure_index` | **unvalidated** | `uluops-registry-api` | tuning | 0.749 | 0.697 (busyness) | 0.583 | 0.585 | 0.328 | 0.900 | 0.62 | no | pr_auc_mult |
| `change_pressure_index` | **unvalidated** | `eslint` | tuning | 0.807 | 0.777 (busyness) | 0.492 | 0.431 | 0.185 | 1.000 | 0.69 | no | roc_margin, pr_auc_mult |

## 2. Where it failed

- **`bug_pressure_index`** — `unvalidated` (passed_on_0_of_2_test_repos_need_2).
  - `typeorm`: ROC-AUC 0.770 vs busyness 0.728 (Δ +0.042, need +0.05); PR-AUC 0.759 vs 0.717 (×1.06, need ×1.2); failed: roc_margin, pr_auc_mult.
  - `mcp-secure-server`: ROC-AUC 0.828 vs recency 0.821 (Δ +0.006, need +0.05); PR-AUC 0.387 vs 0.257 (×1.50, need ×1.2); failed: roc_margin.
  - `uluops-registry-api`: ROC-AUC 0.721 vs busyness 0.697 (Δ +0.025, need +0.05); PR-AUC 0.584 vs 0.585 (×1.00, need ×1.2); failed: roc_margin, pr_auc_mult.
  - `eslint`: ROC-AUC 0.791 vs busyness 0.777 (Δ +0.014, need +0.05); PR-AUC 0.462 vs 0.431 (×1.07, need ×1.2); failed: roc_margin, pr_auc_mult.
- **`change_pressure_index`** — `unvalidated` (passed_on_1_of_2_test_repos_need_2).
  - `typeorm`: ROC-AUC 0.878 vs busyness 0.728 (Δ +0.150, need +0.05); PR-AUC 0.868 vs 0.717 (×1.21, need ×1.2); passed.
  - `mcp-secure-server`: ROC-AUC 0.854 vs recency 0.821 (Δ +0.032, need +0.05); PR-AUC 0.424 vs 0.257 (×1.65, need ×1.2); failed: roc_margin.
  - `uluops-registry-api`: ROC-AUC 0.749 vs busyness 0.697 (Δ +0.052, need +0.05); PR-AUC 0.583 vs 0.585 (×1.00, need ×1.2); failed: pr_auc_mult.
  - `eslint`: ROC-AUC 0.807 vs busyness 0.777 (Δ +0.030, need +0.05); PR-AUC 0.492 vs 0.431 (×1.14, need ×1.2); failed: roc_margin, pr_auc_mult.

## 3. Coverage caveats

- `typeorm`: coverage 0.632 (2274 of 3600 HEAD nodes eligible).
- `mcp-secure-server`: coverage 0.988 (257 of 260 HEAD nodes eligible).
- `uluops-registry-api`: coverage 0.884 (403 of 456 HEAD nodes eligible).
- `eslint`: coverage 0.823 (1219 of 1481 HEAD nodes eligible).
- `neglect_index`: untested — unstable.
- `recent_commit_share`: untested — degenerate.
- `revert_count`: untested — degenerate.

## 4. Descriptive signals (§2.4)

*Grounding classes: G1 measurement (stability only; instrument is git or the file), G2 second instrument (fan_in ↔ an independent scanner; floor τ ≥ 0.6), G3 cross-modal (a different modality; floor τ ≥ 0.3), G4 derived (stability + every input asserted; the name carries no claim beyond its inputs). Stability compares nodes untouched by the K removed commits.*

| signal | class | status | repo | reason | stability med / p95 / max Δ (n) | distinct | stable | counterpart | n | τ-b | 95% CI | perm p | corroborated |
|---|---|---|---|---|---:|---:|---|---|---:|---:|---|---:|---|
| `age_days` | G3 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529) | 236 | yes | `blame_age_median` | 583 | 0.483 | [0.427, 0.535] | 0.001 | yes |
| `age_days` | G3 | **asserted** | `mcp-secure-server` | – | 0.002 / 0.005 / 0.005 (179) | 17 | yes | `blame_age_median` | 202 | 0.883 | [0.791, 0.953] | 0.001 | yes |
| `age_days` | G3 | **asserted** | `uluops-registry-api` | – | 0.006 / 0.011 / 0.011 (222) | 112 | yes | `blame_age_median` | 267 | 0.793 | [0.735, 0.848] | 0.001 | yes |
| `age_days` | G3 | **asserted** | `eslint` | – | 0.001 / 0.002 / 0.002 (455) | 382 | yes | `blame_age_median` | 472 | 0.378 | [0.316, 0.437] | 0.001 | yes |
| `author_count` | G1 | **asserted** | `typeorm` | – | 0.002 / 0.004 / 0.004 (529) | 37 | yes | `git log` | – | – | – | – | yes |
| `author_count` | G1 | **asserted** | `mcp-secure-server` | – | 0.007 / 0.007 / 0.007 (179) | 2 | yes | `git log` | – | – | – | – | yes |
| `author_count` | G1 | **asserted** | `uluops-registry-api` | degenerate | 0.000 / 0.000 / 0.000 (222) | 1 | no | `git log` | – | – | – | – | yes |
| `author_count` | G1 | **asserted** | `eslint` | – | 0.001 / 0.002 / 0.002 (455) | 48 | yes | `git log` | – | – | – | – | yes |
| `blame_age_median` | G1 | **asserted** | `typeorm` | – | 0.004 / 0.009 / 0.009 (529) | 218 | yes | `git blame -w` | – | – | – | – | yes |
| `blame_age_median` | G1 | **asserted** | `mcp-secure-server` | – | 0.007 / 0.009 / 0.014 (179) | 18 | yes | `git blame -w` | – | – | – | – | yes |
| `blame_age_median` | G1 | **asserted** | `uluops-registry-api` | – | 0.012 / 0.023 / 0.024 (222) | 137 | yes | `git blame -w` | – | – | – | – | yes |
| `blame_age_median` | G1 | **asserted** | `eslint` | – | 0.001 / 0.002 / 0.002 (454) | 310 | yes | `git blame -w` | – | – | – | – | yes |
| `centrality` | G4 | **asserted** | `typeorm` | unstable | 0.001 / 0.003 / 0.232 (529) | 55 | no | `–` | – | – | – | – | derived |
| `centrality` | G4 | **asserted** | `mcp-secure-server` | – | 0.004 / 0.024 / 0.046 (179) | 50 | yes | `–` | – | – | – | – | derived |
| `centrality` | G4 | **asserted** | `uluops-registry-api` | unstable | 0.010 / 0.020 / 0.187 (222) | 51 | no | `–` | – | – | – | – | derived |
| `centrality` | G4 | **asserted** | `eslint` | – | 0.002 / 0.002 / 0.029 (455) | 38 | yes | `–` | – | – | – | – | derived |
| `churn_lines` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.003 / 0.005 (529) | 290 | yes | `git log --numstat` | – | – | – | – | yes |
| `churn_lines` | G1 | **asserted** | `mcp-secure-server` | – | 0.002 / 0.009 / 0.015 (179) | 128 | yes | `git log --numstat` | – | – | – | – | yes |
| `churn_lines` | G1 | **asserted** | `uluops-registry-api` | – | 0.002 / 0.010 / 0.014 (222) | 151 | yes | `git log --numstat` | – | – | – | – | yes |
| `churn_lines` | G1 | **asserted** | `eslint` | – | 0.001 / 0.002 / 0.002 (455) | 396 | yes | `git log --numstat` | – | – | – | – | yes |
| `cochange_degree` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.001 (529) | 76 | yes | `git log co-occurrence (§5)` | – | – | – | – | yes |
| `cochange_degree` | G1 | **asserted** | `mcp-secure-server` | – | 0.007 / 0.034 / 0.044 (179) | 10 | yes | `git log co-occurrence (§5)` | – | – | – | – | yes |
| `cochange_degree` | G1 | **asserted** | `uluops-registry-api` | – | 0.001 / 0.011 / 0.011 (222) | 30 | yes | `git log co-occurrence (§5)` | – | – | – | – | yes |
| `cochange_degree` | G1 | **asserted** | `eslint` | – | 0.001 / 0.002 / 0.002 (455) | 46 | yes | `git log co-occurrence (§5)` | – | – | – | – | yes |
| `commit_count` | G1 | **asserted** | `typeorm` | – | 0.002 / 0.006 / 0.006 (529) | 77 | yes | `git log` | – | – | – | – | yes |
| `commit_count` | G1 | **asserted** | `mcp-secure-server` | – | 0.011 / 0.021 / 0.022 (179) | 10 | yes | `git log` | – | – | – | – | yes |
| `commit_count` | G1 | **asserted** | `uluops-registry-api` | – | 0.001 / 0.006 / 0.007 (222) | 26 | yes | `git log` | – | – | – | – | yes |
| `commit_count` | G1 | **asserted** | `eslint` | – | 0.001 / 0.002 / 0.002 (455) | 75 | yes | `git log` | – | – | – | – | yes |
| `complexity_proxy_index` | G4 | **asserted** | `typeorm` | – | 0.001 / 0.003 / 0.004 (529) | 378 | yes | `–` | – | – | – | – | derived |
| `complexity_proxy_index` | G4 | **asserted** | `mcp-secure-server` | – | 0.002 / 0.005 / 0.009 (179) | 153 | yes | `–` | – | – | – | – | derived |
| `complexity_proxy_index` | G4 | **asserted** | `uluops-registry-api` | – | 0.003 / 0.006 / 0.007 (222) | 203 | yes | `–` | – | – | – | – | derived |
| `complexity_proxy_index` | G4 | **asserted** | `eslint` | – | 0.000 / 0.001 / 0.002 (455) | 399 | yes | `–` | – | – | – | – | derived |
| `fan_in` | G2 | **asserted** | `typeorm` | – | 0.000 / 0.001 / 0.019 (529) | 49 | yes | `fan_in_alt` | 582 | 0.999 | [0.998, 1.000] | 0.001 | yes |
| `fan_in` | G2 | **asserted** | `mcp-secure-server` | – | 0.001 / 0.004 / 0.130 (179) | 10 | yes | `fan_in_alt` | 202 | 1.000 | [1.000, 1.000] | 0.001 | yes |
| `fan_in` | G2 | **asserted** | `uluops-registry-api` | – | 0.004 / 0.005 / 0.107 (222) | 21 | yes | `fan_in_alt` | 261 | 0.995 | [0.991, 0.998] | 0.001 | yes |
| `fan_in` | G2 | **asserted** | `eslint` | – | 0.001 / 0.001 / 0.011 (455) | 13 | yes | `fan_in_alt` | 472 | 0.981 | [0.944, 1.000] | 0.001 | yes |
| `fan_in_nonzero` | G4 | **asserted** | `typeorm` | – | 0.000 / 0.001 / 0.020 (508) | 48 | yes | `–` | – | – | – | – | derived |
| `fan_in_nonzero` | G4 | **asserted** | `mcp-secure-server` | unstable | 0.002 / 0.005 / 0.166 (136) | 9 | no | `–` | – | – | – | – | derived |
| `fan_in_nonzero` | G4 | **asserted** | `uluops-registry-api` | unstable | 0.003 / 0.003 / 0.164 (129) | 20 | no | `–` | – | – | – | – | derived |
| `fan_in_nonzero` | G4 | **asserted** | `eslint` | – | 0.001 / 0.001 / 0.012 (396) | 12 | yes | `–` | – | – | – | – | derived |
| `fan_out` | G2 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529) | 32 | yes | `fan_out_alt` | 582 | 1.000 | [1.000, 1.000] | 0.001 | yes |
| `fan_out` | G2 | **asserted** | `mcp-secure-server` | – | 0.002 / 0.006 / 0.006 (179) | 8 | yes | `fan_out_alt` | 202 | 1.000 | [1.000, 1.000] | 0.001 | yes |
| `fan_out` | G2 | **asserted** | `uluops-registry-api` | – | 0.004 / 0.006 / 0.006 (222) | 13 | yes | `fan_out_alt` | 261 | 1.000 | [1.000, 1.000] | 0.001 | yes |
| `fan_out` | G2 | **asserted** | `eslint` | – | 0.001 / 0.001 / 0.001 (455) | 9 | yes | `fan_out_alt` | 472 | 0.996 | [0.990, 1.000] | 0.001 | yes |
| `fix_count` | G1 | **asserted** | `typeorm` | – | 0.002 / 0.003 / 0.003 (529) | 26 | yes | `git log` | – | – | – | – | yes |
| `fix_count` | G1 | **asserted** | `mcp-secure-server` | – | 0.019 / 0.027 / 0.027 (179) | 4 | yes | `git log` | – | – | – | – | yes |
| `fix_count` | G1 | **asserted** | `uluops-registry-api` | – | 0.009 / 0.013 / 0.014 (222) | 18 | yes | `git log` | – | – | – | – | yes |
| `fix_count` | G1 | **asserted** | `eslint` | – | 0.001 / 0.005 / 0.005 (455) | 26 | yes | `git log` | – | – | – | – | yes |
| `has_sibling_test` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529) | 2 | yes | `path convention config (§6.2.2)` | – | – | – | – | yes |
| `has_sibling_test` | G1 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (179) | 2 | yes | `path convention config (§6.2.2)` | – | – | – | – | yes |
| `has_sibling_test` | G1 | **asserted** | `uluops-registry-api` | – | 0.000 / 0.000 / 0.000 (222) | 2 | yes | `path convention config (§6.2.2)` | – | – | – | – | yes |
| `has_sibling_test` | G1 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.000 (455) | 2 | yes | `path convention config (§6.2.2)` | – | – | – | – | yes |
| `is_package_entry` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529) | 2 | yes | `package.json main/module/browser/types/bin/exports` | – | – | – | – | yes |
| `is_package_entry` | G1 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (179) | 2 | yes | `package.json main/module/browser/types/bin/exports` | – | – | – | – | yes |
| `is_package_entry` | G1 | **asserted** | `uluops-registry-api` | degenerate | 0.000 / 0.000 / 0.000 (222) | 1 | no | `package.json main/module/browser/types/bin/exports` | – | – | – | – | yes |
| `is_package_entry` | G1 | **asserted** | `eslint` | – | 0.000 / 0.000 / 0.000 (455) | 2 | yes | `package.json main/module/browser/types/bin/exports` | – | – | – | – | yes |
| `last_touched_days` | G1 | **asserted** | `typeorm` | – | 0.026 / 0.073 / 0.091 (529) | 97 | yes | `git log author_date` | – | – | – | – | yes |
| `last_touched_days` | G1 | **asserted** | `mcp-secure-server` | – | 0.017 / 0.089 / 0.111 (179) | 32 | yes | `git log author_date` | – | – | – | – | yes |
| `last_touched_days` | G1 | **asserted** | `uluops-registry-api` | unstable | 0.032 / 0.145 / 0.163 (222) | 116 | no | `git log author_date` | – | – | – | – | yes |
| `last_touched_days` | G1 | **asserted** | `eslint` | – | 0.009 / 0.030 / 0.038 (455) | 125 | yes | `git log author_date` | – | – | – | – | yes |
| `load_index` | G4 | **asserted** | `typeorm` | – | 0.000 / 0.001 / 0.075 (529) | 449 | yes | `–` | – | – | – | – | derived |
| `load_index` | G4 | **asserted** | `mcp-secure-server` | – | 0.002 / 0.006 / 0.097 (179) | 161 | yes | `–` | – | – | – | – | derived |
| `load_index` | G4 | **asserted** | `uluops-registry-api` | – | 0.003 / 0.008 / 0.103 (222) | 197 | yes | `–` | – | – | – | – | derived |
| `load_index` | G4 | **asserted** | `eslint` | – | 0.001 / 0.001 / 0.011 (455) | 381 | yes | `–` | – | – | – | – | derived |
| `neglect_index` | G3 | **untested** | `typeorm` | input_not_asserted:recent_commit_share | 0.010 / 0.031 / 0.101 (529) | 411 | yes | `blame_age_median` | 583 | 0.564 | [0.519, 0.602] | 0.001 | yes |
| `neglect_index` | G3 | **untested** | `mcp-secure-server` | unstable | 0.008 / 0.119 / 0.239 (179) | 49 | no | `blame_age_median` | 202 | 0.593 | [0.508, 0.685] | 0.001 | yes |
| `neglect_index` | G3 | **untested** | `uluops-registry-api` | unstable | 0.016 / 0.064 / 0.228 (222) | 179 | no | `blame_age_median` | 267 | 0.653 | [0.603, 0.700] | 0.001 | yes |
| `neglect_index` | G3 | **untested** | `eslint` | input_not_asserted:recent_commit_share | 0.004 / 0.014 / 0.067 (455) | 416 | yes | `blame_age_median` | 472 | 0.373 | [0.320, 0.427] | 0.001 | yes |
| `nesting_proxy` | G1 | **asserted** | `typeorm` | – | 0.003 / 0.008 / 0.008 (529) | 19 | yes | `indent counter (§6.2.2)` | – | – | – | – | yes |
| `nesting_proxy` | G1 | **asserted** | `mcp-secure-server` | – | 0.005 / 0.007 / 0.007 (179) | 10 | yes | `indent counter (§6.2.2)` | – | – | – | – | yes |
| `nesting_proxy` | G1 | **asserted** | `uluops-registry-api` | – | 0.006 / 0.008 / 0.009 (222) | 11 | yes | `indent counter (§6.2.2)` | – | – | – | – | yes |
| `nesting_proxy` | G1 | **asserted** | `eslint` | – | 0.000 / 0.002 / 0.002 (455) | 21 | yes | `indent counter (§6.2.2)` | – | – | – | – | yes |
| `recent_commit_share` | G1 | **untested** | `typeorm` | unstable | 0.000 / 0.000 / 0.500 (529) | 130 | no | `git log (timeline-relative window, §6.2.2)` | – | – | – | – | yes |
| `recent_commit_share` | G1 | **untested** | `mcp-secure-server` | degenerate | 0.000 / 0.000 / 0.000 (179) | 5 | no | `git log (timeline-relative window, §6.2.2)` | – | – | – | – | yes |
| `recent_commit_share` | G1 | **untested** | `uluops-registry-api` | unstable | 0.000 / 0.043 / 1.000 (222) | 26 | no | `git log (timeline-relative window, §6.2.2)` | – | – | – | – | yes |
| `recent_commit_share` | G1 | **untested** | `eslint` | unstable | 0.000 / 0.022 / 0.333 (455) | 180 | no | `git log (timeline-relative window, §6.2.2)` | – | – | – | – | yes |
| `reinforcement_index` | G4 | **asserted** | `typeorm` | unstable | 0.000 / 0.001 / 0.610 (529) | 28 | no | `–` | – | – | – | – | derived |
| `reinforcement_index` | G4 | **asserted** | `mcp-secure-server` | – | 0.000 / 0.000 / 0.000 (179) | 4 | yes | `–` | – | – | – | – | derived |
| `reinforcement_index` | G4 | **asserted** | `uluops-registry-api` | unstable | 0.000 / 0.002 / 0.650 (222) | 11 | no | `–` | – | – | – | – | derived |
| `reinforcement_index` | G4 | **asserted** | `eslint` | – | 0.001 / 0.001 / 0.003 (455) | 7 | yes | `–` | – | – | – | – | derived |
| `revert_count` | G1 | **untested** | `typeorm` | – | 0.000 / 0.000 / 0.000 (529) | 4 | yes | `git log` | – | – | – | – | yes |
| `revert_count` | G1 | **untested** | `mcp-secure-server` | degenerate | 0.000 / 0.000 / 0.000 (179) | 1 | no | `git log` | – | – | – | – | yes |
| `revert_count` | G1 | **untested** | `uluops-registry-api` | degenerate | 0.000 / 0.000 / 0.000 (222) | 1 | no | `git log` | – | – | – | – | yes |
| `revert_count` | G1 | **untested** | `eslint` | degenerate | 0.000 / 0.000 / 0.000 (455) | 3 | no | `git log` | – | – | – | – | yes |
| `size_loc` | G1 | **asserted** | `typeorm` | – | 0.000 / 0.003 / 0.008 (529) | 194 | yes | `non-blank line count` | – | – | – | – | yes |
| `size_loc` | G1 | **asserted** | `mcp-secure-server` | – | 0.002 / 0.006 / 0.015 (179) | 127 | yes | `non-blank line count` | – | – | – | – | yes |
| `size_loc` | G1 | **asserted** | `uluops-registry-api` | – | 0.005 / 0.011 / 0.013 (222) | 140 | yes | `non-blank line count` | – | – | – | – | yes |
| `size_loc` | G1 | **asserted** | `eslint` | – | 0.001 / 0.002 / 0.004 (455) | 267 | yes | `non-blank line count` | – | – | – | – | yes |
| `test_fan_in` | G2 | **asserted** | `typeorm` | unstable | 0.001 / 0.001 / 0.419 (529) | 28 | no | `test_fan_in_alt` | 582 | 0.997 | [0.990, 1.000] | 0.001 | yes |
| `test_fan_in` | G2 | **asserted** | `mcp-secure-server` | – | 0.001 / 0.001 / 0.001 (179) | 4 | yes | `test_fan_in_alt` | 202 | 1.000 | [1.000, 1.000] | 0.001 | yes |
| `test_fan_in` | G2 | **asserted** | `uluops-registry-api` | unstable | 0.003 / 0.004 / 0.396 (222) | 11 | no | `test_fan_in_alt` | 261 | 0.986 | [0.976, 0.995] | 0.001 | yes |
| `test_fan_in` | G2 | **asserted** | `eslint` | – | 0.002 / 0.002 / 0.004 (455) | 7 | yes | `test_fan_in_alt` | 472 | 0.975 | [0.932, 1.000] | 0.001 | yes |

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

- `age_days` ↔ `blame_age_median` (G3): 0.48, 0.88, 0.79, 0.38
- `fan_in` ↔ `fan_in_alt` (G2): 1.00, 1.00, 0.99, 0.98
- `fan_out` ↔ `fan_out_alt` (G2): 1.00, 1.00, 1.00, 1.00
- `neglect_index` ↔ `blame_age_median` (G3): 0.56, 0.59, 0.65, 0.37
- `test_fan_in` ↔ `test_fan_in_alt` (G2): 1.00, 1.00, 0.99, 0.98

**Reported correlates (never gating):**

- `centrality` ~ `cochange_degree` on `typeorm`: τ 0.13 [0.07, 0.19]
- `centrality` ~ `cochange_degree` on `mcp-secure-server`: τ 0.19 [0.08, 0.30]
- `centrality` ~ `cochange_degree` on `uluops-registry-api`: τ 0.38 [0.30, 0.46]
- `centrality` ~ `cochange_degree` on `eslint`: τ 0.05 [-0.04, 0.14]
- `load_index` ~ `cochange_degree` on `typeorm`: τ 0.19 [0.13, 0.25]
- `load_index` ~ `test_fan_in` on `typeorm`: τ 0.42 [0.38, 0.46]
- `load_index` ~ `cochange_degree` on `mcp-secure-server`: τ 0.24 [0.13, 0.34]
- `load_index` ~ `test_fan_in` on `mcp-secure-server`: τ 0.47 [0.40, 0.54]
- `load_index` ~ `cochange_degree` on `uluops-registry-api`: τ 0.39 [0.31, 0.46]
- `load_index` ~ `test_fan_in` on `uluops-registry-api`: τ 0.72 [0.69, 0.75]
- `load_index` ~ `cochange_degree` on `eslint`: τ 0.15 [0.07, 0.23]
- `load_index` ~ `test_fan_in` on `eslint`: τ 0.46 [0.38, 0.53]
- `neglect_index` ~ `cochange_degree` on `typeorm`: τ 0.11 [0.05, 0.16]
- `neglect_index` ~ `cochange_degree` on `mcp-secure-server`: τ -0.24 [-0.32, -0.15]
- `neglect_index` ~ `cochange_degree` on `uluops-registry-api`: τ -0.12 [-0.20, -0.04]
- `neglect_index` ~ `cochange_degree` on `eslint`: τ 0.10 [0.04, 0.15]
- `reinforcement_index` ~ `has_sibling_test` on `typeorm`: τ 0.20 [0.12, 0.27]
- `reinforcement_index` ~ `has_sibling_test` on `mcp-secure-server`: τ 0.17 [0.03, 0.31]
- `reinforcement_index` ~ `has_sibling_test` on `uluops-registry-api`: τ 0.56 [0.48, 0.66]
- `reinforcement_index` ~ `has_sibling_test` on `eslint`: τ 0.72 [0.61, 0.81]

## 5. Cross-source corroboration (§3A)

- Not run in M1 (D-005): §3A is built after the holdout leaves a `validated` signal to corroborate.

## 6. Recognition record (§2.4.3, D-010) — sealed rankings, n = 1, never gating

### `mcp-secure-server` — `blind/mcp-secure-server.md`

*Provenance of this fill: written by Claude (Fable 5.1) at Alex's request, from session-memory (chiefly: the per-tool policy requirement, the -32602 rejection, the 0.0.20-security vs ^0.0.6-security split across consumers, the five-layer pipeline, the self-contained cookbook) plus `git rev-parse HEAD`, `git ls-files`, and the root `package.json` name/version/dependency keys. No `git log`, no `git blame`, no import tracing, no source contents were read. Knowledge here is thinner than for registry-api; sections 3 and 4 in particular are guesses from the layer naming, not from having watched the repo move.*

| signal | source | ranked & present | overlap@10 | τ-b on ranked | items not in substrate |
|---|---|---:|---:|---:|---|
| `bug_pressure_index` | list 2 | 10 | 0.30 | -0.56 | – |
| `change_pressure_index` | list 3 | 9 | 0.30 | -0.06 | `CHANGELOG.md`, `README.md` |

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
| `bug_pressure_index` | list 2 | 9 | 0.20 | -0.33 | `package.json` |
| `change_pressure_index` | list 3 | 8 | 0.10 | 0.00 | `package.json`, `package-lock.json`, `CHANGELOG.md` |

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
