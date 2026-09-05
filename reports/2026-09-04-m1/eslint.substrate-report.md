# Substrate report — `eslint` @ `3f20a57c62`

*Deterministic sorted evidence over continuous signals. No feature is named here; naming is C3's job. Seed `a50b92780e08…`, config fingerprint `80b2a632f8b7…`, as-of 2026-09-04.*

> **UNGATED.** This report consults no `validation.json`. Every number below is a measurement or a fixed-weight blend of measurements; none has passed the anti-horoscope gate, and nothing here is a diagnosis. Diagnostic claims come only from C3 over gated signals (`structural-mapper-spec.md` §3).

## Summary

| field | value |
|---|---:|
| `node_count` | 1481 |
| `population_size` | 473 |
| `percentiles_valid` | yes |
| `orphan_nodes` | 0 |
| `graph_available` | yes |
| `graph_resolution_rate` | 0.99 |
| `fan_in_instrument_tau` | 0.98 |
| `graph_instruments_disagree` | no |
| `graph_degraded` | no |
| `external_imports` | 490 |
| `unresolved_imports` | 20 |
| `non_node_imports` | 14 |
| `blame_failed` | 0 |
| `alt_scanner_unreadable` | 0 |
| `tsconfig_malformed` | no |
| `total_loc` | 504116 |
| `repo_age_days` | 4814 |
| `commit_count` | 11008 |
| `author_count` | 1275 |
| `authorship_gini` | 0.81 |
| `test_loc_ratio` | 0.81 |
| `dep_graph_density` | 0.00 |

## 1. Highest `load_index` (top 10)

| file | load | degraded | fan_in | centrality | fan_out | loc | cochange |
|---|---:|---:|---:|---:|---:|---:|---:|
| `lib/shared/traverser.js` | 0.92 | no | 7 | 0.01 | 0 | 177 | 0 |
| `lib/rules/utils/ast-utils.js` | 0.90 | no | 193 | 0.09 | 3 | 2673 | 97 |
| `lib/rule-tester/rule-tester.js` | 0.90 | no | 293 | 0.05 | 10 | 1800 | 63 |
| `lib/services/warning-service.js` | 0.89 | no | 8 | 0.00 | 0 | 78 | 5 |
| `lib/languages/js/source-code/token-store/utils.js` | 0.88 | no | 5 | 0.00 | 0 | 118 | 2 |
| `lib/config/flat-config-schema.js` | 0.88 | no | 4 | 0.00 | 1 | 523 | 22 |
| `lib/linter/source-code-fixer.js` | 0.88 | no | 4 | 0.00 | 0 | 132 | 0 |
| `lib/config/config.js` | 0.88 | no | 6 | 0.01 | 3 | 676 | 7 |
| `conf/globals.js` | 0.88 | no | 3 | 0.03 | 0 | 151 | 7 |
| `lib/shared/ast-utils.js` | 0.88 | no | 7 | 0.03 | 0 | 27 | 0 |

## 2. Highest `change_pressure_index` (top 10)

| file | change | churn | commits | last_touched_d |
|---|---:|---:|---:|---:|
| `lib/linter/linter.js` | 1.00 | 20407 | 458 | 0 |
| `tests/lib/linter/linter.js` | 0.99 | 92355 | 178 | 0 |
| `tests/lib/eslint/eslint.js` | 0.99 | 90652 | 116 | 0 |
| `tests/lib/languages/js/source-code/source-code.js` | 0.99 | 20984 | 83 | 0 |
| `tests/lib/rules/no-unused-vars.js` | 0.99 | 13440 | 130 | 0 |
| `lib/cli.js` | 0.98 | 4063 | 144 | 0 |
| `lib/languages/js/source-code/source-code.js` | 0.98 | 5254 | 101 | 0 |
| `lib/eslint/eslint.js` | 0.98 | 5824 | 73 | 0 |
| `Makefile.js` | 0.97 | 7771 | 320 | 37 |
| `lib/rules/utils/ast-utils.js` | 0.97 | 8546 | 129 | 37 |

## 3. Highest `bug_pressure_index` (top 10)

| file | bug | fixes | reverts | commits | reinforcement |
|---|---:|---:|---:|---:|---:|
| `lib/linter/linter.js` | 1.00 | 107 | 3 | 458 | 0.00 |
| `tests/lib/linter/linter.js` | 0.99 | 43 | 2 | 178 | 0.00 |
| `Makefile.js` | 0.98 | 22 | 2 | 320 | 0.00 |
| `lib/rules/utils/ast-utils.js` | 0.97 | 43 | 1 | 129 | 0.74 |
| `tests/lib/rules/utils/ast-utils.js` | 0.97 | 22 | 1 | 83 | 0.00 |
| `lib/rules/indent.js` | 0.97 | 69 | 1 | 193 | 0.74 |
| `eslint.config.js` | 0.94 | 4 | 1 | 51 | 0.00 |
| `tests/lib/rule-tester/rule-tester.js` | 0.93 | 29 | 1 | 119 | 0.00 |
| `packages/js/src/configs/eslint-recommended.js` | 0.92 | 8 | 1 | 361 | 0.00 |
| `lib/rule-tester/rule-tester.js` | 0.92 | 34 | 1 | 157 | 1.00 |

## 4. High load, low reinforcement — `load_index ≥ 0.9 ∧ reinforcement_index ≤ 0.1` (top 10 by load)

_(no nodes satisfy the predicate)_

## 5. Old, load-bearing, untouched — `neglect_index ≥ 0.9 ∧ load_index ≥ 0.1` (top 10 by neglect)

| file | neglect | load | age_d | last_touched_d | blame_age_d | fan_in |
|---|---:|---:|---:|---:|---:|---:|
| `tests/fixtures/formatters/simple.js` | 0.95 | 0.10 | 4784 | 4355 | 4784.33 | 0 |
| `tests/fixtures/rules/custom-rule.js` | 0.95 | 0.12 | 4778 | 1365 | 4778.81 | 1 |
| `tests/lib/rules/dot-notation.js` | 0.92 | 0.11 | 4793 | 533 | 2573.78 | 0 |
| `tests/fixtures/formatters/test/simple.js` | 0.92 | 0.10 | 4629 | 4355 | 4629.59 | 0 |

## Caveats

- **Unresolved in-repo imports** (first 20 of 20): `docs/src/assets/js/search.js` → `./algoliasearch.js`, `tests/bench/large.js` → `../data/ascii-identifier-data.js`, `tests/bench/large.js` → `../data/non-ascii-identifier-part-only.js`, `tests/bench/large.js` → `../data/non-ascii-identifier-start.js`, `tests/bench/large.js` → `./lex.js`, `tests/bench/large.js` → `./messages.js`, `tests/bench/large.js` → `./reg.js`, `tests/bench/large.js` → `./state.js`, `tests/bench/large.js` → `./style.js`, `tests/bench/large.js` → `./support/isBuffer`
