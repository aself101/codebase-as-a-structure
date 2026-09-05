# Substrate report — `mcp-secure-server` @ `ecb30716b8`

*Deterministic sorted evidence over continuous signals. No feature is named here; naming is C3's job. Seed `2c7db66a25f4…`, config fingerprint `80b2a632f8b7…`, as-of 2026-08-24.*

> **UNGATED.** This report consults no `validation.json`. Every number below is a measurement or a fixed-weight blend of measurements; none has passed the anti-horoscope gate, and nothing here is a diagnosis. Diagnostic claims come only from C3 over gated signals (`structural-mapper-spec.md` §3).

## Summary

| field | value |
|---|---:|
| `node_count` | 260 |
| `population_size` | 202 |
| `percentiles_valid` | yes |
| `orphan_nodes` | 0 |
| `graph_available` | yes |
| `graph_resolution_rate` | 0.92 |
| `fan_in_instrument_tau` | 1.00 |
| `graph_instruments_disagree` | no |
| `graph_degraded` | no |
| `external_imports` | 272 |
| `unresolved_imports` | 34 |
| `non_node_imports` | 0 |
| `blame_failed` | 0 |
| `alt_scanner_unreadable` | 0 |
| `tsconfig_malformed` | yes |
| `total_loc` | 41308 |
| `repo_age_days` | 256 |
| `commit_count` | 139 |
| `author_count` | 3 |
| `authorship_gini` | 0.44 |
| `test_loc_ratio` | 0.41 |
| `dep_graph_density` | 0.01 |

## 1. Highest `load_index` (top 10)

| file | load | degraded | fan_in | centrality | fan_out | loc | cochange |
|---|---:|---:|---:|---:|---:|---:|---:|
| `src/security/utils/error-sanitizer.ts` | 0.91 | no | 6 | 0.01 | 1 | 448 | 10 |
| `src/security/layers/validation-layer-base.ts` | 0.86 | no | 8 | 0.01 | 2 | 193 | 4 |
| `src/security/constants.ts` | 0.85 | no | 6 | 0.01 | 0 | 63 | 8 |
| `src/types/server.ts` | 0.85 | no | 6 | 0.01 | 6 | 164 | 21 |
| `src/types/index.ts` | 0.85 | no | 16 | 0.04 | 5 | 85 | 1 |
| `cookbook/image-gen-server/src/providers/index.ts` | 0.84 | no | 9 | 0.07 | 5 | 86 | 0 |
| `src/security/config/tool-policies-config.ts` | 0.84 | no | 4 | 0.03 | 2 | 301 | 14 |
| `cookbook/transaction-server/src/utils/index.ts` | 0.84 | no | 11 | 0.02 | 2 | 38 | 0 |
| `src/security/utils/security-logger.ts` | 0.83 | no | 5 | 0.01 | 3 | 491 | 5 |
| `src/security/config/tool-policies.ts` | 0.82 | no | 4 | 0.03 | 1 | 111 | 12 |

## 2. Highest `change_pressure_index` (top 10)

| file | change | churn | commits | last_touched_d |
|---|---:|---:|---:|---:|
| `src/security/utils/error-sanitizer.ts` | 1.00 | 1582 | 13 | 0 |
| `test/unit/utils/error-sanitizer.test.js` | 0.99 | 1143 | 10 | 0 |
| `src/security/mcp-secure-server.ts` | 0.98 | 1244 | 24 | 37 |
| `src/security/config/tool-policies-config.ts` | 0.98 | 1478 | 7 | 37 |
| `test/unit/server/secure-mcp-server.test.js` | 0.97 | 655 | 10 | 37 |
| `src/security/utils/security-logger.ts` | 0.96 | 1141 | 9 | 63 |
| `test/unit/layers/layer1-structure.test.js` | 0.95 | 502 | 5 | 37 |
| `src/security/transport/http-server.ts` | 0.95 | 903 | 11 | 224 |
| `test/unit/config/tool-policies-config.test.js` | 0.94 | 683 | 4 | 37 |
| `test/unit/layers/layer3-behavior.test.js` | 0.94 | 977 | 7 | 224 |

## 3. Highest `bug_pressure_index` (top 10)

| file | bug | fixes | reverts | commits | reinforcement |
|---|---:|---:|---:|---:|---:|
| `src/security/utils/error-sanitizer.ts` | 0.85 | 7 | 0 | 13 | 0.68 |
| `src/security/mcp-secure-server.ts` | 0.84 | 3 | 0 | 24 | 1.00 |
| `test/unit/utils/error-sanitizer.test.js` | 0.84 | 6 | 0 | 10 | 0.00 |
| `src/security/layers/layer-utils/content/patterns/path-traversal.ts` | 0.83 | 4 | 0 | 10 | 0.00 |
| `src/types/server.ts` | 0.83 | 2 | 0 | 10 | 0.00 |
| `test/unit/server/secure-mcp-server.test.js` | 0.83 | 1 | 0 | 10 | 0.00 |
| `src/security/config/tool-policies-config.ts` | 0.82 | 0 | 0 | 7 | 0.00 |
| `src/security/transport/http-server.ts` | 0.82 | 4 | 0 | 11 | 0.68 |
| `src/security/utils/security-logger.ts` | 0.82 | 3 | 0 | 9 | 0.68 |
| `src/index.ts` | 0.81 | 1 | 0 | 10 | 0.68 |

## 4. High load, low reinforcement — `load_index ≥ 0.9 ∧ reinforcement_index ≤ 0.1` (top 10 by load)

_(no nodes satisfy the predicate)_

## 5. Old, load-bearing, untouched — `neglect_index ≥ 0.9 ∧ load_index ≥ 0.1` (top 10 by neglect)

| file | neglect | load | age_d | last_touched_d | blame_age_d | fan_in |
|---|---:|---:|---:|---:|---:|---:|
| `src/security/layers/layer-utils/content/helper-utils.ts` | 0.95 | 0.72 | 256 | 256 | 256.63 | 4 |
| `src/security/layers/layer-utils/content/unicode.ts` | 0.95 | 0.68 | 256 | 256 | 256.63 | 2 |
| `src/security/layers/layer-utils/content/utils/index.ts` | 0.95 | 0.39 | 256 | 256 | 256.98 | 1 |
| `src/security/layers/layer-utils/semantics/semantic-quotas.ts` | 0.95 | 0.73 | 256 | 256 | 256.98 | 3 |
| `src/security/layers/layer2-validators/base64-css.ts` | 0.95 | 0.30 | 256 | 256 | 256.63 | 1 |
| `src/security/utils/tool-registry.ts` | 0.95 | 0.26 | 256 | 256 | 256.98 | 1 |
| `src/types/messages.ts` | 0.95 | 0.51 | 256 | 256 | 256.63 | 1 |
| `test/unit/integration/multi-layer-pipeline.test.js` | 0.95 | 0.21 | 256 | 256 | 256.98 | 0 |
| `test/unit/layers/base64-css.test.js` | 0.95 | 0.19 | 256 | 256 | 256.82 | 0 |
| `test/unit/utils/helper-utils.test.js` | 0.95 | 0.16 | 256 | 256 | 256.98 | 0 |

## Caveats

- **Unresolved in-repo imports** (first 34 of 34): `test/integration/validation-pipeline.e2e.test.ts` → `@/security/mcp-secure-server.js`, `test/integration/validation-pipeline.e2e.test.ts` → `@/security/utils/validation-pipeline.js`, `test/unit/config/tool-policies-config.test.js` → `@/security/config/tool-policies-config.js`, `test/unit/config/tool-policies-config.test.js` → `@/security/config/tool-policies.js`, `test/unit/config/tool-policies.test.js` → `@/security/config/pattern-categories.js`, `test/unit/config/tool-policies.test.js` → `@/security/config/tool-policies-config.js`, `test/unit/config/tool-policies.test.js` → `@/security/config/tool-policies.js`, `test/unit/integration/multi-layer-pipeline.test.js` → `@/security/layers/layer1-structure.js`, `test/unit/integration/multi-layer-pipeline.test.js` → `@/security/layers/layer2-content.js`, `test/unit/integration/multi-layer-pipeline.test.js` → `@/security/layers/layer3-behavior.js`
