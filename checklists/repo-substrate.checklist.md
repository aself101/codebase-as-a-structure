# Companion Checklist — repo-substrate (C1)

*Conformance checklist for `repo-substrate-spec.md` (v0.2). Every item is a testable contract derived from the spec; each cites its section. The substrate is the product — this list verifies it independent of any renderer.*

**Scope:** C1's own artifact (`substrate.json` + the markdown report). Seams to validation (`--truncate-at`) and to C3 (signal-name join) are verified in `system-integration.checklist.md`.

**Legend — contract class:** `[DET]` determinism · `[SCH]` schema shape · `[ALG]` computation · `[GATE]` degrade/refuse · `[BND]` substrate↔consumer boundary.
**Legend — verification:** `(golden)` byte-identical re-run · `(unit)` unit test · `(prop)` property test · `(fixture)` reference-repo run · `(review)` human recognition.

---

## A. Governing boundary (§1)

- [ ] `[BND]` Output contains **only** continuous bounded numbers (raw metrics, percentiles, indices) — `load_index: 0.92` is allowed. *(§1)* `(unit)`
- [ ] `[BND]` Output contains **no** discrete named claim — no feature (`"toothpick"`), archetype (`"cathedral"`), or quality grade (`"D"`). Naming is C3's job. *(§1)* `(unit)`
- [ ] `[DET]` Every index value is traceable to its versioned weights (a composite index is a small model, acceptable only because weights are inspectable). *(§1, §3)* `(golden)`

## B. Determinism & seed contract (§3)

- [ ] `[DET]` Output is a pure function of `(repo content@SHA, extractor_version, config incl. weights, toolchain_versions)`. *(§3)* `(golden)`
- [ ] `[DET]` `seed` = content hash of the resolved tree. *(§3)* `(unit)`
- [ ] `[DET]` `config_fingerprint` hashes the effective config: index weights, percentile settings, exclude globs, **and** `toolchain_versions`. *(§3)* `(golden)`
- [ ] `[DET]` `toolchain_versions` captures resolved versions of every value-affecting external tool (dep extractor, graph lib, history miner), hashed into the fingerprint and recorded verbatim in `repo`. *(§3)* `(unit)`
- [ ] `[DET]` Re-run on same SHA + versions + config is byte-identical except `extracted_at` (excluded from seed). *(§3)* `(golden)`
- [ ] `[DET]` Stable ordering throughout; floats rounded to 4 dp. *(§3)* `(unit)`

## C. Schema & node-set invariant (§4, §5)

- [ ] `[SCH]` `substrate.json` matches the v0.2 schema shape (`schema_version`, `extractor_version`, `seed`, `repo`, `summary`, `languages`, `nodes`, `edges`, `timeline`). *(§4)* `(unit)`
- [ ] `[ALG]` `nodes[]` is exactly the **post-exclude file inventory at HEAD** (or `--rev`/`--truncate-at`); a file deleted before HEAD has history but is **not** a node. *(§5)* `(unit)`
- [ ] `[ALG]` All Tier-1 raw metrics are emitted per node: `size_loc`, `age_days` (rename-followed first-touch), `last_touched_days`, `commit_count`, `churn_lines`, `fix_count`, `revert_count`, `author_count`, `fan_in`, `fan_out`, `is_test`, `has_sibling_test`, `introduced_idx`. *(§5)* `(unit)`
- [ ] `[SCH]` Raw metrics are always emitted even when percentiles/indices are `null`. *(§4)* `(unit)`

## D. Percentiles (§6.1)

- [ ] `[ALG]` A percentile is computed for **every** continuous metric — the full keyset incl. the three `_nonzero` variants (`fan_in_nonzero`, `fix_count_nonzero`, `revert_count_nonzero`), and `centrality`/`nesting_proxy` where defined. *(§6.1)* `(unit)`
- [ ] `[ALG]` Discrete signals (`is_test`, `has_sibling_test`) and bounded ratios (`fix_ratio`) are **not** percentiled — used directly. *(§6.1)* `(unit)`
- [ ] `[ALG]` Population = included source files after exclude globs; `exclude_tests_from_population` (default true) drops `is_test` files from the reference distribution but still measures them. *(§6.1)* `(unit)`
- [ ] `[ALG]` Method is empirical CDF with **average-rank ties**, range `[0,1]`. *(§6.1)* `(unit, prop)`
- [ ] `[GATE]` `population_size < N_min` (default 30) → `null` percentiles & indices, `percentiles_valid: false`, raw metrics kept; never fabricate ranks. *(§6.1)* `(unit)`
- [ ] `[ALG]` `_nonzero` variant ranks only among nonzero values; a floor file (`fan_in == 0`) has no `fan_in_nonzero` and contributes 0.0 to that input. *(§6.1)* `(unit)`

## E. Composite indices (§6.2)

- [ ] `[ALG]` Every index is a weighted combination of **normalized inputs** (percentiles or normalized discrete signals), never raw metrics; result lands in `[0,1]`. *(§6.2)* `(prop)`
- [ ] `[SCH]` Canonical index names are used; deprecated aliases (`volatility_index`, `staleness_index`, `test_reinforcement_index`) are not emitted. *(§6.2)* `(unit)`
- [ ] `[ALG]` `load_index` and `bug_pressure_index` consume the `_nonzero` inputs per the §6.2.1 formulas. *(§6.1, §6.2.1)* `(unit)`
- [ ] `[ALG]` v0 weights match §6.2.1 and live in config (feeding `config_fingerprint`); within-index weights sum to 1.0. *(§6.2.1)* `(unit)`
- [ ] `[ALG]` `reinforcement_index` is the documented exception — composed from normalized discrete test signals (1.0 sibling / 0.5 proximity / 0.0 none), still bounded. *(§6.2)* `(unit)`
- [ ] `[ALG]` Pinned input definitions honored: `centrality` = PageRank (damping 0.85, fixed iterations/tolerance); `nesting_proxy` = normalized max indent depth; `recent_commit_share` = timeline-relative (not wall-clock); test-proximity tiers per §6.2.2. *(§6.2.2)* `(unit)`
- [ ] `[DET]` Method choices in §6.2.2 are recorded in config and feed `config_fingerprint`. *(§6.2.2)* `(golden)`

## F. Graph fallback — quality, not just presence (§6.3)

- [ ] `[GATE]` Absent/empty graph → `graph_available: false`; `load_index` recomputed from non-graph inputs (weights removed & renormalized); every node `load_index_degraded: true`. *(§6.3)* `(unit)`
- [ ] `[ALG]` `graph_resolution_rate = resolved_in_repo_edges / (resolved_in_repo_edges + unresolved_imports)`, with external imports **excluded** from the denominator. *(§6.3, §8)* `(unit)`
- [ ] `[GATE]` Rate `< graph_quality_min` (default 0.80) → `graph_degraded: true` repo-wide + `load_index_degraded: true` per node, even with `graph_available: true`. *(§6.3)* `(unit)`
- [ ] `[ALG]` Rate is always reported (visible even above threshold); denominator-zero routes through the empty-graph path, not a `0.0` rate. *(§6.3)* `(unit)`
- [ ] `[GATE]` `load_index_degraded` rides with the value through every downstream artifact; degrading is not nulling. *(§6.3)* `(unit)`
- [ ] `[ALG]` Known residual documented: resolution rate catches non-resolution, **not** confident mis-resolution (deferred extractor-fidelity, §12 Q8). *(§6.3)* `(review)`

## G. Commit classification (§7)

- [ ] `[ALG]` Deterministic first-match cascade, recorded in `matched_rule`: conventional-prefix (`\b`, colon optional) → native-revert → merge (>1 parent) → subject-regex (`bug|hotfix|patch`→fix) → default. *(§7)* `(unit)`
- [ ] `[ALG]` No probabilistic classification; every `type` is traceable to a rule, matching `history_miner.py::classify_commit`. *(§7)* `(unit)`
- [ ] `[ALG]` Git-native reverts are labeled positive **via stage 1** (stage 2 is currently dead by design; spec describes option (a)). Any change here is decided against the holdout, not silently. *(§7 open item)* `(unit, review)`

## H. The substrate report (§9)

- [ ] `[SCH]` Deterministic markdown report names **no** building features; sorted top-K (K default 10) with contributing raw + derived values shown. *(§9)* `(golden)`
- [ ] `[SCH]` Five sections present: highest `load_index`, highest `change_pressure_index`, highest `bug_pressure_index`, high-load+low-reinforcement (`load ≥ p ∧ reinforcement ≤ q`), old+load-bearing+untouched (`neglect ≥ p ∧ load ≥ q`). *(§9)* `(golden)`
- [ ] `[ALG]` Threshold defaults `p = 0.90`, `q = 0.10` from config — the same cutoffs C3 starts from, so report and skeleton agree by default. *(§9)* `(unit)`
- [ ] `[review]` Sections 4 & 5 (toothpick / flooded-basement queries, unnamed) produce recognition on a known repo — the cheapest proof the signals bite. *(§9)* `(review)`

## I. Tooling & CLI (§8)

- [ ] `[ALG]` `HistoryMiner` honors a revision bound (`rev`/`to_commit`) — required before the holdout (build step 10); HEAD-only acceptable for steps 1–9. *(§8)* `(unit)`
- [ ] `[ALG]` Dependency edge contract: directed `import` `{from,to,kind}`, self-loops dropped, duplicates collapsed (fan_out = distinct deps), only resolved in-repo targets become edges, edges sorted by `(from,to)`. *(§8)* `(unit)`
- [ ] `[ALG]` `external_imports` and `unresolved_imports` counted **separately**; only in-repo failures feed the resolution rate. *(§8)* `(unit)`
- [ ] `[SCH]` CLI: `extract <repo> [--rev HEAD] [--truncate-at <sha>] [--config cfg.toml] -o substrate.json --report substrate-report.md`. *(§8)* `(unit)`
- [ ] `[DET]` All value-affecting config + `toolchain_versions` feed `config_fingerprint`. *(§8, §3)* `(golden)`

---

## Seams (verified in `system-integration.checklist.md`, not here)

- **Produces:** `substrate.json` consumed by C3 (signal-name join) and by validation (under `--truncate-at`); `seed` flows downstream to C4/C6.
- **`--truncate-at` is the validation seam:** the same pipeline truncated at a split SHA is what makes the holdout a real holdout (validation §7).
- **Deferred (on the page, not v0):** SZZ-style blame (truer defect label, validation §3.4.1); extractor mis-resolution fidelity (§12 Q8); `blast_radius_index` over `cochange_degree` (§5 Tier 2, validation §2.3).
