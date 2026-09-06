# Where eps and delta sit against the reference set

*Operands per (signal, repo): median |Δpercentile| against `stability_eps`, max |Δpercentile| against `stability_delta`, over the untouched population (validation §2.4.1). The D-026 rule: a ceiling sits where it can fail — between the reference set's median and p90 of its operand at the pinned K.*

## K = 25 — `out/validation-k25c/validation.json`

92 (signal, repo) readings reached the stability test: 44 own (null check — 0 read above 0.000), 48 coupled (the bars are placed over these).

| operand | threshold | reference-set median | p90 | max | fires on | verdict under the D-026 rule (letter) |
|---|---|---|---|---|---|---|
| eps over median \|Δ\| | 0.010 | 0.0000 | 0.0043 | 0.0162 | 3 of 48 | above p90 — cannot fail on this set |
| delta over the tail operand | 0.050 | 0.0010 | 0.0203 | 0.1195 | 2 of 48 | above p90 — cannot fail on this set |

| signal | ripple | repo | median \|Δ\| | p95 | max | operand | n | status |
|---|---|---|---|---|---|---|---|---|
| `neglect_index` | coupled | mcp-secure-server | 0.0080 | 0.1195 | 0.2394 | p95 | 179 | untested **fails** |
| `neglect_index` | coupled | uluops-registry-api | 0.0162 | 0.0645 | 0.2278 | p95 | 222 | untested **fails** |
| `recent_commit_share` | coupled | uluops-registry-api | 0.0090 | 0.0315 | 0.6329 | p95 | 222 | asserted |
| `neglect_index` | coupled | typeorm | 0.0103 | 0.0307 | 0.1014 | p95 | 529 | untested **fails** |
| `centrality` | coupled | mcp-secure-server | 0.0028 | 0.0251 | 0.0363 | p95 | 179 | asserted |
| `centrality` | coupled | uluops-registry-api | 0.0135 | 0.0203 | 0.2095 | p95 | 222 | asserted **fails** |
| `neglect_index` | coupled | eslint | 0.0043 | 0.0139 | 0.0674 | p95 | 455 | untested |
| `recent_commit_share` | coupled | eslint | 0.0033 | 0.0101 | 0.1165 | p95 | 455 | asserted |
| `recent_commit_share` | coupled | typeorm | 0.0028 | 0.0095 | 0.3563 | p95 | 529 | asserted |
| `load_index` | coupled | uluops-registry-api | 0.0034 | 0.0083 | 0.1034 | p95 | 222 | asserted |
| `load_index` | coupled | mcp-secure-server | 0.0016 | 0.0064 | 0.0967 | p95 | 179 | asserted |
| `complexity_proxy_index` | coupled | uluops-registry-api | 0.0032 | 0.0064 | 0.0071 | p95 | 222 | asserted |
| `complexity_proxy_index` | coupled | mcp-secure-server | 0.0021 | 0.0053 | 0.0088 | p95 | 179 | asserted |
| `test_fan_in` | coupled | uluops-registry-api | 0.0023 | 0.0045 | 0.4167 | p95 | 222 | asserted |
| `fan_in_nonzero` | coupled | uluops-registry-api | 0.0000 | 0.0039 | 0.1512 | p95 | 129 | asserted |
| `centrality` | coupled | typeorm | 0.0009 | 0.0038 | 0.2391 | p95 | 529 | asserted |
| `fan_in_nonzero` | coupled | mcp-secure-server | 0.0000 | 0.0037 | 0.1765 | p95 | 136 | asserted |
| `complexity_proxy_index` | coupled | typeorm | 0.0014 | 0.0031 | 0.0038 | p95 | 529 | asserted |
| `fan_in` | coupled | mcp-secure-server | 0.0000 | 0.0028 | 0.1341 | p95 | 179 | asserted |
| `fan_in` | coupled | uluops-registry-api | 0.0000 | 0.0023 | 0.0878 | p95 | 222 | asserted |
| `reinforcement_index` | coupled | uluops-registry-api | 0.0000 | 0.0017 | 0.6504 | p95 | 222 | asserted |
| `load_index` | coupled | eslint | 0.0012 | 0.0014 | 0.0115 | p95 | 455 | asserted |
| `load_index` | coupled | typeorm | 0.0004 | 0.0011 | 0.0749 | p95 | 529 | asserted |
| `centrality` | coupled | eslint | 0.0000 | 0.0011 | 0.0275 | p95 | 455 | asserted |
| `test_fan_in` | coupled | typeorm | 0.0009 | 0.0009 | 0.4282 | p95 | 529 | asserted |
| `reinforcement_index` | coupled | typeorm | 0.0000 | 0.0009 | 0.6098 | p95 | 529 | asserted |
| `complexity_proxy_index` | coupled | eslint | 0.0004 | 0.0008 | 0.0017 | p95 | 455 | asserted |
| `reinforcement_index` | coupled | eslint | 0.0006 | 0.0006 | 0.0027 | p95 | 455 | asserted |
| `age_days` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | asserted |
| `age_days` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | asserted |
| `age_days` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 222 | asserted |
| `age_days` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 455 | asserted |
| `author_count` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | asserted |
| `author_count` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | asserted |
| `author_count` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 222 | asserted **fails** |
| `author_count` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 455 | asserted |
| `blame_age_median` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | asserted |
| `blame_age_median` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | asserted |
| `blame_age_median` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 222 | asserted |
| `blame_age_median` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 454 | asserted |
| `churn_lines` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | asserted |
| `churn_lines` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | asserted |
| `churn_lines` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 222 | asserted |
| `churn_lines` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 455 | asserted |
| `cochange_degree` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | asserted |
| `cochange_degree` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | asserted |
| `cochange_degree` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 222 | asserted |
| `cochange_degree` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 455 | asserted |
| `commit_count` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | asserted |
| `commit_count` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | asserted |
| `commit_count` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 222 | asserted |
| `commit_count` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 455 | asserted |
| `fan_in` | coupled | typeorm | 0.0000 | 0.0000 | 0.0180 | p95 | 529 | asserted |
| `fan_in` | coupled | eslint | 0.0000 | 0.0000 | 0.0099 | p95 | 455 | asserted |
| `fan_in_nonzero` | coupled | typeorm | 0.0000 | 0.0000 | 0.0187 | p95 | 508 | asserted |
| `fan_in_nonzero` | coupled | eslint | 0.0000 | 0.0000 | 0.0114 | p95 | 396 | asserted |
| `fan_out` | coupled | typeorm | 0.0000 | 0.0000 | 0.0000 | p95 | 529 | asserted |
| `fan_out` | coupled | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | p95 | 179 | asserted |
| `fan_out` | coupled | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | p95 | 222 | asserted |
| `fan_out` | coupled | eslint | 0.0000 | 0.0000 | 0.0000 | p95 | 455 | asserted |
| `fix_count` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | asserted |
| `fix_count` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | asserted |
| `fix_count` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 222 | asserted |
| `fix_count` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 455 | asserted |
| `has_sibling_test` | coupled | typeorm | 0.0000 | 0.0000 | 0.0000 | p95 | 529 | asserted |
| `has_sibling_test` | coupled | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | p95 | 179 | asserted |
| `has_sibling_test` | coupled | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | p95 | 222 | asserted |
| `has_sibling_test` | coupled | eslint | 0.0000 | 0.0000 | 0.0000 | p95 | 455 | asserted |
| `is_package_entry` | coupled | typeorm | 0.0000 | 0.0000 | 0.0000 | p95 | 529 | asserted |
| `is_package_entry` | coupled | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | p95 | 179 | asserted |
| `is_package_entry` | coupled | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | p95 | 222 | asserted **fails** |
| `is_package_entry` | coupled | eslint | 0.0000 | 0.0000 | 0.0000 | p95 | 455 | asserted |
| `last_touched_days` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | asserted |
| `last_touched_days` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | asserted |
| `last_touched_days` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 222 | asserted |
| `last_touched_days` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 455 | asserted |
| `nesting_proxy` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | asserted |
| `nesting_proxy` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | asserted |
| `nesting_proxy` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 222 | asserted |
| `nesting_proxy` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 455 | asserted |
| `recent_commit_share` | coupled | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | p95 | 179 | asserted **fails** |
| `reinforcement_index` | coupled | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | p95 | 179 | asserted |
| `revert_count` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | untested |
| `revert_count` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | untested **fails** |
| `revert_count` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 222 | untested **fails** |
| `revert_count` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 455 | untested **fails** |
| `size_loc` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | asserted |
| `size_loc` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | asserted |
| `size_loc` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 222 | asserted |
| `size_loc` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 455 | asserted |
| `test_fan_in` | coupled | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | p95 | 179 | asserted |
| `test_fan_in` | coupled | eslint | 0.0000 | 0.0000 | 0.0044 | p95 | 455 | asserted |

