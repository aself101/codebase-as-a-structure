# Where eps and delta sit against the reference set

*Operands per (signal, repo): median |Δpercentile| against `stability_eps`, max |Δpercentile| against `stability_delta`, over the untouched population (validation §2.4.1). The D-026 rule: a ceiling sits where it can fail — between the reference set's median and p90 of its operand at the pinned K.*

## K = 25 — `out/validation-k25/validation.json`

92 (signal, repo) readings reached the stability test: 92 own (null check — 75 read above 0.000: age_days@mcp-secure-server, age_days@uluops-registry-api, age_days@eslint, author_count@typeorm, author_count@mcp-secure-server, author_count@eslint, blame_age_median@typeorm, blame_age_median@mcp-secure-server, blame_age_median@uluops-registry-api, blame_age_median@eslint, centrality@typeorm, centrality@mcp-secure-server, centrality@uluops-registry-api, centrality@eslint, churn_lines@typeorm, churn_lines@mcp-secure-server, churn_lines@uluops-registry-api, churn_lines@eslint, cochange_degree@typeorm, cochange_degree@mcp-secure-server, cochange_degree@uluops-registry-api, cochange_degree@eslint, commit_count@typeorm, commit_count@mcp-secure-server, commit_count@uluops-registry-api, commit_count@eslint, complexity_proxy_index@typeorm, complexity_proxy_index@mcp-secure-server, complexity_proxy_index@uluops-registry-api, complexity_proxy_index@eslint, fan_in@typeorm, fan_in@mcp-secure-server, fan_in@uluops-registry-api, fan_in@eslint, fan_in_nonzero@typeorm, fan_in_nonzero@mcp-secure-server, fan_in_nonzero@uluops-registry-api, fan_in_nonzero@eslint, fan_out@mcp-secure-server, fan_out@uluops-registry-api, fan_out@eslint, fix_count@typeorm, fix_count@mcp-secure-server, fix_count@uluops-registry-api, fix_count@eslint, last_touched_days@typeorm, last_touched_days@mcp-secure-server, last_touched_days@uluops-registry-api, last_touched_days@eslint, load_index@typeorm, load_index@mcp-secure-server, load_index@uluops-registry-api, load_index@eslint, neglect_index@typeorm, neglect_index@mcp-secure-server, neglect_index@uluops-registry-api, neglect_index@eslint, nesting_proxy@typeorm, nesting_proxy@mcp-secure-server, nesting_proxy@uluops-registry-api, nesting_proxy@eslint, recent_commit_share@typeorm, recent_commit_share@uluops-registry-api, recent_commit_share@eslint, reinforcement_index@typeorm, reinforcement_index@uluops-registry-api, reinforcement_index@eslint, size_loc@typeorm, size_loc@mcp-secure-server, size_loc@uluops-registry-api, size_loc@eslint, test_fan_in@typeorm, test_fan_in@mcp-secure-server, test_fan_in@uluops-registry-api, test_fan_in@eslint), 0 coupled (the bars are placed over these).

| operand | threshold | reference-set median | p90 | max | fires on | verdict under the D-026 rule (letter) |
|---|---|---|---|---|---|
| eps over median \|Δ\| | 0.050 | 0.0012 | 0.0095 | 0.0322 | 0 of 92 | above p90 — cannot fail on this set |
| delta over the tail operand | 0.150 | 0.0082 | 0.2278 | 1.0000 | 14 of 92 | between median and p90 — can fail |

| signal | ripple | repo | median \|Δ\| | p95 | max | operand | n | status |
|---|---|---|---|---|---|---|---|---|
| `recent_commit_share` | own | uluops-registry-api | 0.0000 | 0.0431 | 1.0000 | max | 222 | untested **fails** |
| `reinforcement_index` | own | uluops-registry-api | 0.0000 | 0.0017 | 0.6504 | max | 222 | asserted **fails** |
| `reinforcement_index` | own | typeorm | 0.0000 | 0.0009 | 0.6098 | max | 529 | asserted **fails** |
| `recent_commit_share` | own | typeorm | 0.0000 | 0.0000 | 0.5000 | max | 529 | untested **fails** |
| `test_fan_in` | own | typeorm | 0.0009 | 0.0009 | 0.4193 | max | 529 | asserted **fails** |
| `test_fan_in` | own | uluops-registry-api | 0.0029 | 0.0036 | 0.3960 | max | 222 | asserted **fails** |
| `recent_commit_share` | own | eslint | 0.0000 | 0.0225 | 0.3333 | max | 455 | untested **fails** |
| `neglect_index` | own | mcp-secure-server | 0.0080 | 0.1195 | 0.2394 | max | 179 | untested **fails** |
| `centrality` | own | typeorm | 0.0009 | 0.0026 | 0.2324 | max | 529 | asserted **fails** |
| `neglect_index` | own | uluops-registry-api | 0.0162 | 0.0645 | 0.2278 | max | 222 | untested **fails** |
| `centrality` | own | uluops-registry-api | 0.0097 | 0.0200 | 0.1869 | max | 222 | asserted **fails** |
| `fan_in_nonzero` | own | mcp-secure-server | 0.0017 | 0.0046 | 0.1663 | max | 136 | asserted **fails** |
| `fan_in_nonzero` | own | uluops-registry-api | 0.0030 | 0.0030 | 0.1637 | max | 129 | asserted **fails** |
| `last_touched_days` | own | uluops-registry-api | 0.0322 | 0.1451 | 0.1628 | max | 222 | asserted **fails** |
| `fan_in` | own | mcp-secure-server | 0.0006 | 0.0039 | 0.1305 | max | 179 | asserted |
| `last_touched_days` | own | mcp-secure-server | 0.0173 | 0.0892 | 0.1114 | max | 179 | asserted |
| `fan_in` | own | uluops-registry-api | 0.0036 | 0.0048 | 0.1071 | max | 222 | asserted |
| `load_index` | own | uluops-registry-api | 0.0034 | 0.0083 | 0.1034 | max | 222 | asserted |
| `neglect_index` | own | typeorm | 0.0103 | 0.0307 | 0.1014 | max | 529 | untested |
| `load_index` | own | mcp-secure-server | 0.0016 | 0.0064 | 0.0967 | max | 179 | asserted |
| `last_touched_days` | own | typeorm | 0.0258 | 0.0727 | 0.0909 | max | 529 | asserted |
| `load_index` | own | typeorm | 0.0004 | 0.0011 | 0.0749 | max | 529 | asserted |
| `neglect_index` | own | eslint | 0.0043 | 0.0139 | 0.0674 | max | 455 | untested |
| `centrality` | own | mcp-secure-server | 0.0043 | 0.0245 | 0.0460 | max | 179 | asserted |
| `cochange_degree` | own | mcp-secure-server | 0.0071 | 0.0344 | 0.0442 | max | 179 | asserted |
| `last_touched_days` | own | eslint | 0.0095 | 0.0305 | 0.0381 | max | 455 | asserted |
| `centrality` | own | eslint | 0.0022 | 0.0022 | 0.0289 | max | 455 | asserted |
| `fix_count` | own | mcp-secure-server | 0.0194 | 0.0267 | 0.0267 | max | 179 | asserted |
| `blame_age_median` | own | uluops-registry-api | 0.0115 | 0.0232 | 0.0237 | max | 222 | asserted |
| `commit_count` | own | mcp-secure-server | 0.0113 | 0.0213 | 0.0217 | max | 179 | asserted |
| `fan_in_nonzero` | own | typeorm | 0.0000 | 0.0009 | 0.0197 | max | 508 | asserted |
| `fan_in` | own | typeorm | 0.0000 | 0.0009 | 0.0189 | max | 529 | asserted |
| `churn_lines` | own | mcp-secure-server | 0.0017 | 0.0092 | 0.0148 | max | 179 | asserted |
| `size_loc` | own | mcp-secure-server | 0.0019 | 0.0059 | 0.0148 | max | 179 | asserted |
| `blame_age_median` | own | mcp-secure-server | 0.0067 | 0.0095 | 0.0144 | max | 179 | asserted |
| `fix_count` | own | uluops-registry-api | 0.0094 | 0.0128 | 0.0142 | max | 222 | asserted |
| `churn_lines` | own | uluops-registry-api | 0.0021 | 0.0100 | 0.0140 | max | 222 | asserted |
| `size_loc` | own | uluops-registry-api | 0.0050 | 0.0107 | 0.0130 | max | 222 | asserted |
| `fan_in_nonzero` | own | eslint | 0.0012 | 0.0012 | 0.0123 | max | 396 | asserted |
| `load_index` | own | eslint | 0.0012 | 0.0014 | 0.0115 | max | 455 | asserted |
| `age_days` | own | uluops-registry-api | 0.0060 | 0.0107 | 0.0112 | max | 222 | asserted |
| `cochange_degree` | own | uluops-registry-api | 0.0012 | 0.0105 | 0.0112 | max | 222 | asserted |
| `fan_in` | own | eslint | 0.0011 | 0.0011 | 0.0106 | max | 455 | asserted |
| `nesting_proxy` | own | uluops-registry-api | 0.0063 | 0.0083 | 0.0089 | max | 222 | asserted |
| `complexity_proxy_index` | own | mcp-secure-server | 0.0021 | 0.0053 | 0.0088 | max | 179 | asserted |
| `blame_age_median` | own | typeorm | 0.0043 | 0.0086 | 0.0086 | max | 529 | asserted |
| `nesting_proxy` | own | typeorm | 0.0034 | 0.0077 | 0.0077 | max | 529 | asserted |
| `size_loc` | own | typeorm | 0.0000 | 0.0034 | 0.0077 | max | 529 | asserted |
| `commit_count` | own | uluops-registry-api | 0.0014 | 0.0058 | 0.0074 | max | 222 | asserted |
| `complexity_proxy_index` | own | uluops-registry-api | 0.0032 | 0.0064 | 0.0071 | max | 222 | asserted |
| `author_count` | own | mcp-secure-server | 0.0069 | 0.0069 | 0.0069 | max | 179 | asserted |
| `nesting_proxy` | own | mcp-secure-server | 0.0048 | 0.0067 | 0.0067 | max | 179 | asserted |
| `fan_out` | own | uluops-registry-api | 0.0037 | 0.0063 | 0.0063 | max | 222 | asserted |
| `fan_out` | own | mcp-secure-server | 0.0019 | 0.0061 | 0.0061 | max | 179 | asserted |
| `commit_count` | own | typeorm | 0.0017 | 0.0060 | 0.0060 | max | 529 | asserted |
| `churn_lines` | own | typeorm | 0.0000 | 0.0034 | 0.0051 | max | 529 | asserted |
| `age_days` | own | mcp-secure-server | 0.0018 | 0.0047 | 0.0049 | max | 179 | asserted |
| `fix_count` | own | eslint | 0.0007 | 0.0045 | 0.0045 | max | 455 | asserted |
| `author_count` | own | typeorm | 0.0017 | 0.0043 | 0.0043 | max | 529 | asserted |
| `test_fan_in` | own | eslint | 0.0023 | 0.0023 | 0.0042 | max | 455 | asserted |
| `complexity_proxy_index` | own | typeorm | 0.0014 | 0.0031 | 0.0038 | max | 529 | asserted |
| `size_loc` | own | eslint | 0.0005 | 0.0020 | 0.0036 | max | 455 | asserted |
| `fix_count` | own | typeorm | 0.0017 | 0.0026 | 0.0035 | max | 529 | asserted |
| `reinforcement_index` | own | eslint | 0.0006 | 0.0006 | 0.0027 | max | 455 | asserted |
| `blame_age_median` | own | eslint | 0.0012 | 0.0021 | 0.0023 | max | 454 | asserted |
| `age_days` | own | eslint | 0.0011 | 0.0020 | 0.0021 | max | 455 | asserted |
| `author_count` | own | eslint | 0.0010 | 0.0020 | 0.0021 | max | 455 | asserted |
| `cochange_degree` | own | eslint | 0.0008 | 0.0016 | 0.0021 | max | 455 | asserted |
| `commit_count` | own | eslint | 0.0008 | 0.0019 | 0.0020 | max | 455 | asserted |
| `churn_lines` | own | eslint | 0.0006 | 0.0016 | 0.0018 | max | 455 | asserted |
| `complexity_proxy_index` | own | eslint | 0.0004 | 0.0008 | 0.0017 | max | 455 | asserted |
| `nesting_proxy` | own | eslint | 0.0004 | 0.0015 | 0.0015 | max | 455 | asserted |
| `cochange_degree` | own | typeorm | 0.0000 | 0.0000 | 0.0009 | max | 529 | asserted |
| `test_fan_in` | own | mcp-secure-server | 0.0007 | 0.0009 | 0.0009 | max | 179 | asserted |
| `fan_out` | own | eslint | 0.0006 | 0.0008 | 0.0008 | max | 455 | asserted |
| `age_days` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | asserted |
| `author_count` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 222 | asserted **fails** |
| `fan_out` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | asserted |
| `has_sibling_test` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | asserted |
| `has_sibling_test` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | asserted |
| `has_sibling_test` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 222 | asserted |
| `has_sibling_test` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 455 | asserted |
| `is_package_entry` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | asserted |
| `is_package_entry` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | asserted |
| `is_package_entry` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 222 | asserted **fails** |
| `is_package_entry` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 455 | asserted |
| `recent_commit_share` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | untested **fails** |
| `reinforcement_index` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | asserted |
| `revert_count` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 529 | untested |
| `revert_count` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 179 | untested **fails** |
| `revert_count` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 222 | untested **fails** |
| `revert_count` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 455 | untested **fails** |

## K = 5 — `reports/2026-09-06-m1c/validation.json`

92 (signal, repo) readings reached the stability test: 92 own (null check — 48 read above 0.000: age_days@eslint, author_count@typeorm, author_count@eslint, blame_age_median@mcp-secure-server, blame_age_median@eslint, centrality@mcp-secure-server, centrality@eslint, churn_lines@typeorm, churn_lines@mcp-secure-server, churn_lines@eslint, cochange_degree@mcp-secure-server, cochange_degree@eslint, commit_count@typeorm, commit_count@mcp-secure-server, commit_count@eslint, complexity_proxy_index@typeorm, complexity_proxy_index@mcp-secure-server, complexity_proxy_index@eslint, fan_in@mcp-secure-server, fan_in@eslint, fan_in_nonzero@mcp-secure-server, fan_in_nonzero@eslint, fan_out@mcp-secure-server, fan_out@eslint, fix_count@typeorm, fix_count@eslint, last_touched_days@typeorm, last_touched_days@mcp-secure-server, last_touched_days@eslint, load_index@typeorm, load_index@mcp-secure-server, load_index@eslint, neglect_index@typeorm, neglect_index@mcp-secure-server, neglect_index@uluops-registry-api, neglect_index@eslint, nesting_proxy@typeorm, nesting_proxy@mcp-secure-server, nesting_proxy@eslint, recent_commit_share@typeorm, recent_commit_share@mcp-secure-server, recent_commit_share@uluops-registry-api, recent_commit_share@eslint, reinforcement_index@eslint, size_loc@typeorm, size_loc@mcp-secure-server, size_loc@eslint, test_fan_in@eslint), 0 coupled (the bars are placed over these).

| operand | threshold | reference-set median | p90 | max | fires on | verdict under the D-026 rule (letter) |
|---|---|---|---|---|---|
| eps over median \|Δ\| | 0.050 | 0.0000 | 0.0011 | 0.0050 | 0 of 92 | above p90 — cannot fail on this set |
| delta over the tail operand | 0.150 | 0.0008 | 0.0289 | 1.0000 | 3 of 92 | above p90 — cannot fail on this set |

| signal | ripple | repo | median \|Δ\| | p95 | max | operand | n | status |
|---|---|---|---|---|---|---|---|---|
| `recent_commit_share` | own | mcp-secure-server | 0.0000 | 0.0000 | 1.0000 | max | 188 | asserted **fails** |
| `recent_commit_share` | own | typeorm | 0.0000 | 0.0000 | 0.5000 | max | 576 | asserted **fails** |
| `neglect_index` | own | mcp-secure-server | 0.0000 | 0.0258 | 0.2079 | max | 188 | asserted **fails** |
| `recent_commit_share` | own | eslint | 0.0000 | 0.0000 | 0.1250 | max | 462 | asserted |
| `neglect_index` | own | typeorm | 0.0007 | 0.0038 | 0.1000 | max | 576 | asserted |
| `last_touched_days` | own | mcp-secure-server | 0.0000 | 0.0297 | 0.0643 | max | 188 | asserted |
| `recent_commit_share` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0400 | max | 267 | asserted |
| `centrality` | own | mcp-secure-server | 0.0000 | 0.0222 | 0.0322 | max | 188 | asserted |
| `cochange_degree` | own | mcp-secure-server | 0.0050 | 0.0247 | 0.0297 | max | 188 | asserted |
| `centrality` | own | eslint | 0.0022 | 0.0022 | 0.0289 | max | 462 | asserted |
| `neglect_index` | own | eslint | 0.0010 | 0.0087 | 0.0289 | max | 462 | asserted |
| `last_touched_days` | own | eslint | 0.0011 | 0.0168 | 0.0233 | max | 462 | asserted |
| `commit_count` | own | mcp-secure-server | 0.0000 | 0.0123 | 0.0149 | max | 188 | asserted |
| `fan_in_nonzero` | own | eslint | 0.0012 | 0.0012 | 0.0123 | max | 402 | asserted |
| `last_touched_days` | own | typeorm | 0.0017 | 0.0094 | 0.0121 | max | 576 | asserted |
| `load_index` | own | eslint | 0.0012 | 0.0014 | 0.0115 | max | 462 | asserted |
| `fan_in` | own | eslint | 0.0011 | 0.0011 | 0.0106 | max | 462 | asserted |
| `churn_lines` | own | mcp-secure-server | 0.0000 | 0.0074 | 0.0099 | max | 188 | asserted |
| `size_loc` | own | mcp-secure-server | 0.0000 | 0.0050 | 0.0099 | max | 188 | asserted |
| `load_index` | own | mcp-secure-server | 0.0005 | 0.0067 | 0.0099 | max | 188 | asserted |
| `neglect_index` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0080 | max | 267 | asserted |
| `nesting_proxy` | own | mcp-secure-server | 0.0025 | 0.0075 | 0.0075 | max | 188 | asserted |
| `complexity_proxy_index` | own | mcp-secure-server | 0.0010 | 0.0040 | 0.0070 | max | 188 | asserted |
| `blame_age_median` | own | mcp-secure-server | 0.0000 | 0.0025 | 0.0050 | max | 188 | asserted |
| `fix_count` | own | eslint | 0.0003 | 0.0045 | 0.0045 | max | 462 | asserted |
| `test_fan_in` | own | eslint | 0.0023 | 0.0023 | 0.0042 | max | 462 | asserted |
| `fan_in_nonzero` | own | mcp-secure-server | 0.0000 | 0.0031 | 0.0031 | max | 145 | asserted |
| `size_loc` | own | eslint | 0.0005 | 0.0014 | 0.0029 | max | 462 | asserted |
| `reinforcement_index` | own | eslint | 0.0006 | 0.0006 | 0.0027 | max | 462 | asserted |
| `fan_in` | own | mcp-secure-server | 0.0000 | 0.0016 | 0.0025 | max | 188 | asserted |
| `fan_out` | own | mcp-secure-server | 0.0000 | 0.0025 | 0.0025 | max | 188 | asserted |
| `age_days` | own | eslint | 0.0010 | 0.0020 | 0.0021 | max | 462 | asserted |
| `blame_age_median` | own | eslint | 0.0011 | 0.0020 | 0.0021 | max | 461 | asserted |
| `cochange_degree` | own | eslint | 0.0008 | 0.0016 | 0.0021 | max | 462 | asserted |
| `author_count` | own | eslint | 0.0009 | 0.0020 | 0.0020 | max | 462 | asserted |
| `commit_count` | own | eslint | 0.0009 | 0.0019 | 0.0020 | max | 462 | asserted |
| `churn_lines` | own | typeorm | 0.0000 | 0.0017 | 0.0018 | max | 576 | asserted |
| `commit_count` | own | typeorm | 0.0000 | 0.0018 | 0.0018 | max | 576 | asserted |
| `size_loc` | own | typeorm | 0.0000 | 0.0017 | 0.0017 | max | 576 | asserted |
| `churn_lines` | own | eslint | 0.0006 | 0.0016 | 0.0017 | max | 462 | asserted |
| `complexity_proxy_index` | own | eslint | 0.0003 | 0.0007 | 0.0012 | max | 462 | asserted |
| `complexity_proxy_index` | own | typeorm | 0.0000 | 0.0004 | 0.0011 | max | 576 | asserted |
| `author_count` | own | typeorm | 0.0000 | 0.0009 | 0.0009 | max | 576 | asserted |
| `fix_count` | own | typeorm | 0.0000 | 0.0009 | 0.0009 | max | 576 | asserted |
| `nesting_proxy` | own | typeorm | 0.0000 | 0.0009 | 0.0009 | max | 576 | asserted |
| `fan_out` | own | eslint | 0.0006 | 0.0008 | 0.0008 | max | 462 | asserted |
| `nesting_proxy` | own | eslint | 0.0004 | 0.0008 | 0.0008 | max | 462 | asserted |
| `load_index` | own | typeorm | 0.0000 | 0.0001 | 0.0002 | max | 576 | asserted |
| `age_days` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 576 | asserted |
| `age_days` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 188 | asserted |
| `age_days` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `author_count` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 188 | asserted |
| `author_count` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted **fails** |
| `blame_age_median` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 576 | asserted |
| `blame_age_median` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `centrality` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 576 | asserted |
| `centrality` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `churn_lines` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `cochange_degree` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 576 | asserted |
| `cochange_degree` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `commit_count` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `complexity_proxy_index` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `fan_in` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 576 | asserted |
| `fan_in` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `fan_in_nonzero` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 553 | asserted |
| `fan_in_nonzero` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 168 | asserted |
| `fan_out` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 576 | asserted |
| `fan_out` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `fix_count` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 188 | asserted |
| `fix_count` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `has_sibling_test` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 576 | asserted |
| `has_sibling_test` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 188 | asserted |
| `has_sibling_test` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `has_sibling_test` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 462 | asserted |
| `is_package_entry` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 576 | asserted |
| `is_package_entry` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 188 | asserted |
| `is_package_entry` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `is_package_entry` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 462 | asserted |
| `last_touched_days` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `load_index` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `nesting_proxy` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `reinforcement_index` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 576 | asserted |
| `reinforcement_index` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 188 | asserted |
| `reinforcement_index` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `revert_count` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 576 | untested |
| `revert_count` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 188 | untested **fails** |
| `revert_count` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | untested **fails** |
| `revert_count` | own | eslint | 0.0000 | 0.0000 | 0.0000 | max | 462 | untested **fails** |
| `size_loc` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |
| `test_fan_in` | own | typeorm | 0.0000 | 0.0000 | 0.0000 | max | 576 | asserted |
| `test_fan_in` | own | mcp-secure-server | 0.0000 | 0.0000 | 0.0000 | max | 188 | asserted |
| `test_fan_in` | own | uluops-registry-api | 0.0000 | 0.0000 | 0.0000 | max | 267 | asserted |

