# Companion Checklist — Validation Gate

*Conformance checklist for `validation-spec.md`. Every item is a testable contract derived from the spec; each cites the section it comes from. This list is a pure function of the spec — when the spec's `validation_config_fingerprint` or a §-number changes, re-derive the affected items.*

**Scope:** the offline validation gate only. Cross-component seams (substrate→validation key matching, the anti-horoscope gate as enforced in C3, fingerprint propagation) live in `system-integration.checklist.md` — this list stops at validation's own artifact boundary.

**Legend — contract class:** `[DET]` determinism · `[SCH]` schema shape · `[ALG]` computation · `[GATE]` refusal/degenerate/hard-error · `[HOR]` grounding/anti-horoscope · `[PROV]` provenance.
**Legend — verification:** `(golden)` byte-identical re-run · `(unit)` unit test · `(prop)` property test · `(fixture)` run on a reference repo · `(review)` human recognition.

---

## A. Governing principle & scope (§1, §2)

- [ ] `[HOR]` A failing verdict is emitted as a finding, never suppressed or retried into a pass — the protocol can return negative and that result ships. *(§1)* `(unit)`
- [ ] `[HOR]` Only signals making a **future-predictive** claim are eligible for `validated`; present-tense signals are routed to the descriptive basis. *(§1, §2.0)* `(unit)`
- [ ] `[SCH]` Every signal a feature can read carries a status — composite index, bare percentile, **and** raw metric — not indices alone. *(§2)* `(unit)`
- [ ] `[HOR]` Exactly two indices (`bug_pressure_index`, `change_pressure_index`) are accepted as holdout targets; the other four indices are rejected from the holdout as a category error. *(§2.0)* `(unit)`

## B. The descriptive/predictive boundary (§2.1, §2.1.1, §2.2, §2.3)

- [ ] `[HOR]` A `kind: descriptive` signal reaches `asserted` only by passing **both** the stability budget (§2.4.1) **and** the cross-modal check (§2.4.2) on ≥ `M_asserted` repos; failing either yields `untested` with a specific reason (`unstable`, `cross_modal_fail`, `no_counterpart`), never a silent `asserted`. *(§2.4.4, §6.1)* `(unit)`
- [ ] `[ALG]` Stability budget: substrate recomputed with the last K=5 commits removed; pass iff `median(|Δpctile|) ≤ 0.05` and `max(|Δpctile|) ≤ 0.15` over the eligible population, holdout-born nodes excluded. *(§2.4.1)* `(fixture)`
- [x] `[ALG]` Corroboration by grounding class (D-008/D-011): G2 second instrument (`fan_in`/`fan_out`/`test_fan_in` ↔ the independent scanner, lower CI ≥ 0.60), G3 cross-modal (`age_days`/`neglect_index` ↔ `blame_age_median`, lower CI ≥ 0.30), G4 every input asserted; the counterpart must come from a different instrument and not be one of the signal's own formula inputs. *(§2.4.2)* `(unit)` — tests/test_gate.py counterpart-independence and G4-inputs tests
- [x] `[GATE]` Degeneracy: a signal with < 3 distinct values is `degenerate`, never `asserted`; stability floors (`n ≥ 30`, excluded ≤ 0.5) yield `insufficient_stability_population`. *(§2.4.1, §2.4.2)* `(unit)` — tests/test_gate.py
- [x] `[HOR]` G1 membership is pinned to the spec table; a reclassification is a test failure. *(§2.4.2)* `(unit)` — tests/test_gate.py
- [x] `[GATE]` `ValidationConfig.validate()` rejects any floor loosened below the spec default (`m_asserted`, `min_repos`, τ floors, stability eps/delta, margins, `holdout_frac`). *(D-012)* `(unit)` — tests/test_gate.py
- [x] `[HOR]` D-009 roles in the artifact: only test-role repos count toward `validated`; tuning-only → `untested (no_test_repos)`; `role`, `expected_role`, `tuned_config_commit` recorded. *(D-009, D-012)* `(unit)` — tests/test_gate.py
- [x] `[DET]` Cache integrity: atomic writes; a corrupt or foreign-fingerprint entry is a miss; `truncate` in the key; seed + sha256 attestation per scored document in `validation.json`. *(D-012)* `(unit)` — tests/test_gate.py
- [x] `[HOR]` Holdout labels are re-derived from a frozen validation-side regex; narrowing the substrate's feature regex moves no label. *(§3.4, D-012)* `(unit)` — tests/test_gate.py
- [ ] `[HOR]` A constant signal passes stability and fails cross-modal — the gate cannot be satisfied by `load_index ≡ 0.5`. *(§2.4)* `(unit)`
- [ ] `[PROV]` The sealed blind ranking (`blind/<repo>.md`, committed by hash before the first run) is compared and reported as τ-b with `n` stated; it never gates. *(§2.4.3)* `(golden, review)`
- [ ] `[HOR]` The τ distribution across repos is printed in the report so a counterpart that cannot fail is visible. *(§2.4 known limit, §6.2)* `(golden)`
- [ ] `[HOR]` An `asserted` signal may carry only a **present structural position** claim; any consequence/forecast phrasing ("changes here break much") is rejected at this tier. *(§2.1.1)* `(unit, review)`
- [ ] `[SCH]` A bare percentile / raw metric can **never** be `validated` (the holdout does not apply); it is `asserted` (with grounding) or `untested`. *(§2.2)* `(unit)`
- [ ] `[SCH]` `untested` and `unvalidated` are distinct and not conflated: `unvalidated` = ran the holdout and failed §3.7; `untested` = holdout could not/does not apply. *(§2.2, §3.8)* `(unit)`
- [ ] `[HOR]` No feature voices a propagation/consequence claim until a future `blast_radius_index` exists and is `validated`. *(§2.3)* `(review)`

## C. Temporal-holdout protocol (§3.1–§3.6)

- [ ] `[ALG]` Split is **80% of commits** (chronological) training / final **20%** holdout — by commit-count, not wall-time (wall-time is a non-default config option). *(§3.1)* `(unit)`
- [ ] `[DET]` The split commit SHA is recorded in the report so the partition is reproducible. *(§3.1)* `(golden)`
- [ ] `[ALG]` Indices are computed from **training-window commits only**; no holdout-window information enters any index value (real holdout, not in-sample fit). *(§3.2)* `(unit)`
- [ ] `[ALG]` A file is eligible iff introduced (rename-followed first touch) **before** the split **and** still exists at HEAD; holdout-born files are excluded. *(§3.3)* `(unit)`
- [ ] `[SCH]` Excluded holdout-born files are reported as a coverage caveat (`scored_files / total_files`), never hidden. *(§3.3)* `(golden)`
- [ ] `[ALG]` Label is git-only and deterministic: a file is positive iff it received ≥1 commit of `type ∈ {fix, revert}` in the holdout window — no manual labeling. *(§3.4)* `(unit)`
- [ ] `[PROV]` The verdict is reported as predicting fix-**activity** (the declared §3.4.1 proxy), never defect **origin**. *(§3.4.1)* `(review)`
- [ ] `[ALG]` The index is compared against the **stronger** of recency and busyness baselines; both are computed. *(§3.5)* `(unit)`
- [ ] `[ALG]` Metrics computed for index and each baseline: precision@k & recall@k for `k ∈ {10, 20, ⌈0.05·|eligible|⌉}`, ROC-AUC, and PR-AUC. *(§3.6)* `(unit)`
- [ ] `[ALG]` PR-AUC is reported and is part of the pass criterion (not ROC-AUC alone). *(§3.6, §3.7)* `(unit)`

## D. Pass criteria & verdicts (§3.7, §3.8)

- [ ] `[GATE]` `validated` requires, on **≥2 reference repos**: ROC-AUC ≥ best-baseline + `0.05`, PR-AUC ≥ `1.20×` best-baseline, eligible coverage ≥ `0.50`, and best-baseline PR-AUC ≥ `1.5×` base rate on that repo (else `insufficient signal`). *(§3.7)* `(fixture)`
- [ ] `[DET]` Both thresholds (`0.05`, `1.20`) are config values feeding the report fingerprint. *(§3.7, §7)* `(golden)`
- [ ] `[SCH]` Verdict ∈ {`validated`, `unvalidated`, `asserted`, `untested`}, each emitted with the meaning fixed in §3.8. *(§3.8)* `(unit)`
- [ ] `[GATE]` A `kind: predictive` signal may hold **only** `validated`/`unvalidated`/`untested` — never `asserted`. *(§3.8)* `(unit)`
- [ ] `[GATE]` A `kind: descriptive` signal may hold **only** `asserted`/`untested` — never `validated`. *(§3.8)* `(unit)`
- [ ] `[GATE]` A `kind`/`status` mismatch entry is rejected as a **hard error** by the loader, identically to `untested`. *(§3.8)* `(unit)`

## E. Degenerate cases — never silently pass (§4)

- [ ] `[GATE]` `population_size < N_min` → affected indices ship `untested` with reason. *(§4)* `(unit)`
- [ ] `[GATE]` Holdout window with **zero** `fix`-type commits → `untested` (AUC undefined), not a pass. *(§4)* `(unit)`
- [ ] `[GATE]` Eligible coverage `< 0.50` on every reference repo → `untested`. *(§4)* `(fixture)`
- [ ] `[GATE]` `untested` is never rendered as `validated` anywhere downstream. *(§4)* `(unit)`

## F. Cross-source corroboration — §3A

- [ ] `[HOR]` Corroboration **strengthens or contests** a `validated` signal; it never grants or revokes `validated`, and never operates at the `asserted` tier. *(§3A, §3A.1)* `(unit)`
- [ ] `[ALG]` Eligible issues require a non-null repo-relative `file_path` **and an affirmative triaged-defect status** — absence of a disqualifier (untriaged/open) does **not** make a positive. *(§3A.2)* `(unit)`
- [ ] `[ALG]` User-submitted issues are excluded; agent-discovered eligible issues only. *(§3A.2)* `(unit)`
- [ ] `[ALG]` Path normalization is **rename-followed**; absent-from-node-set → coverage caveat, ambiguous-after-normalization → normalization caveat; both counts reported. *(§3A.2)* `(unit)`
- [ ] `[ALG]` Primary endpoint is **Kendall τ-b** (tie-corrected) on the **unweighted** graded label; severity-weighting is reported-only. Schema and gate read the same statistic. *(§3A.2, §3A.4)* `(unit)`
- [ ] `[ALG]` Predictive mode: index from history ≤ `T`, issues `firstSeen` after `T` only; concurrent mode logged as `mode: "concurrent"` and excluded from status reasoning. *(§3A.3)* `(unit)`
- [ ] `[ALG]` Lens-deployment events within the holdout window are recorded (discovery-time ≠ manifestation-time caveat). *(§3A.3)* `(golden)`
- [ ] `[ALG]` The `load_index`/centrality baseline is **mandatory**; the headline is lift over the stronger of {busyness, `load_index`}. *(§3A.4, §3A.7)* `(unit)`
- [ ] `[ALG]` Defined margins are applied: τ-b lower-CI ≥ `τ_corr` (0.30) **and** ≥ baseline τ-b + `τ_margin` (0.10); precision@k lower-CI ≥ `pk_mult`× baseline (1.20). *(§3A.4)* `(unit)`
- [ ] `[GATE]` **No pass/fail from a point estimate** — every gated statistic carries a bootstrap CI and the gate reads the **lower bound**. *(§3A.5)* `(unit)`
- [ ] `[ALG]` τ-b significance is reported against a label-permutation null. *(§3A.5)* `(unit)`
- [ ] `[GATE]` `n_post_T_positives < N_min_issue_positives` (default 15, on the **post-T** set) → `untested`/`thin_corpus`. *(§3A.5, §3A.9)* `(unit)`
- [ ] `[ALG]` Divergence is computed at verdict-level (sets `divergence_with_holdout`) and metric-level (sign disagreement / precision gap > `divergence_margin`); both recorded. *(§3A.8)* `(unit)`
- [ ] `[GATE]` §3A degenerate set enforced: `no_eligible_issues`, `thin_corpus`, `insufficient_coverage`, and **refuse** (not `untested`) on an unpinned snapshot. *(§3A.9)* `(unit)`
- [ ] `[SCH]` Corroboration `outcome` ∈ {`corroborated`, `contested`, `insufficient_coverage`, `untested`} as an enum **string**, never a boolean. *(§3A.10)* `(unit)`
- [ ] `[DET]` `corroboration_fingerprint` hashes issue snapshot **content** (`file_path`, status, `firstSeenRunId`, `failureSeverityCode`), not just ids — an in-place re-triage moves the fingerprint. *(§3A.11)* `(golden)`
- [ ] `[DET]` Snapshot extraction is read-only, pinned to a recorded as-of + id set, re-runnable to reproduce the id+content set. *(§3A.12)* `(golden)`
- [ ] `[HOR]` Results stated in the **narrowed claim** ("adds ranking signal beyond busyness and centrality"), not "beyond review-attention." *(§3A.7)* `(review)`
- [ ] `[HOR]` `precondition_independence` ∈ {`confirmed`,`provisional`,`failed`} recorded; `corroborated` is marked **provisional** until §3A.13.0 is answered. *(§3A.13.0, §3A.14)* `(review)`

## G. Outputs (§6, §3A.14)

- [ ] `[SCH]` `validation.json` is keyed by **signal name** at `validation.signals[<name>].status`; a missing key is treated as `untested`. *(§6.1)* `(unit)`
- [ ] `[SCH]` Predictive signals carry a `holdout` block; descriptive signals carry a `grounding` block instead — never both. *(§6.1)* `(unit)`
- [ ] `[SCH]` A predictive signal MAY additionally carry an `issue_corroboration` block beside (never instead of) `holdout`; it never alters `status`/`kind`. *(§6.1, §3A.14)* `(unit)`
- [ ] `[DET]` `validated_at` is excluded from both fingerprints; re-runs are byte-identical otherwise. *(§6.1, §7)* `(golden)`
- [ ] `[SCH]` The holdout report carries all five fixed sections: verdict table, where-it-failed, coverage caveats, descriptive signals, **cross-source corroboration**. *(§6.2)* `(golden)`
- [ ] `[PROV]` "Where it failed" records, for every `unvalidated` signal, by how much, on which repo, against which baseline. *(§6.2)* `(golden)`

## H. Tooling & determinism (§7)

- [ ] `[DET]` Reuses the `repo-substrate` pipeline via `--truncate-at <split-sha>` rather than reimplementing extraction. *(§7)* `(unit)`
- [ ] `[DET]` Verdict is a pure function of `(reference repos@SHAs, substrate config incl. weights, validation config incl. thresholds)`; re-run reproduces byte-for-byte. *(§7)* `(golden)`
- [ ] `[DET]` A weight or threshold change is a fingerprint change — a moved verdict always resolves to a diff, never to nondeterminism. *(§7)* `(golden)`

---

## Seams (verified in `system-integration.checklist.md`, not here)

- **Consumes:** `substrate.json` truncated at the split SHA (the `--truncate-at` contract is owned by the repo-substrate companion).
- **Produces:** `validation.json` whose signal-name keys must match `substrate.json` `derived` names exactly — the C3 anti-horoscope gate reads this join.
- **Open precondition that blocks promotion:** §3A.13.0 independence question (system spec §8 open question #5) — not a code item; an external answer from the cognitive-lens agent owner.
