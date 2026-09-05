# Validation §3A — Cross-source corroboration via tracked issues (secondary, falsifiable)

> **Status: FOLDED IN — superseded by `validation-spec.md` §3A (2026-06-20).** This v2 draft, revised after a five-lens review pass (contradiction, circular-reasoning, experiment-design, assumption, gap), has been merged verbatim into `validation-spec.md` as §3A, with the cross-reference edits applied there (§2.0, §2.3, §3.4.1, §4, §5, §6.1, §6.2, §8). `validation-spec.md` is now the source of truth; this file is retained as the review-history record and must not be edited independently.
> The review's mechanical findings (missing degenerate-case handling, undefined divergence criterion, absent verdict vocabulary, no uncertainty quantification, metric mismatch, three internal contradictions) were resolved. Two findings were **not** silently resolved and are surfaced in the spec instead: the headline claim is **narrowed** (§3A.7) and the independence premise is promoted to a **blocking precondition** (§3A.13.0 / `validation-spec.md` §8 open question #5).

---

The temporal holdout (§3) is the project's primary falsifier, but it rests on one declared proxy: its label is **fix-*edit* locality**, not **defect locality** (§3.4.1), and for some bug classes that proxy is systematically off-site. The validation platform's own tracked issues carry a second signal — a `file_path` (and `failure_code`) naming the file a reviewer or cognitive-lens agent judged defective. That label is drawn from a *different modality* (review, not git). Running the two together turns a single-modality verdict into **cross-source corroboration**: agreement strengthens confidence in a `validated` result; disagreement is itself a finding.

The independence the corroboration *logic* needs is not modality difference but **error-source independence** — the two labels must not share a confound. This draft establishes modality difference and treats error-source independence as an **open precondition** (§3A.13.0), not an achieved property. Where this section earlier called the issue label "independent" and "closer to defect origin" as bare facts, both are now stated as claims with stated conditions for being true.

This is corroboration in the strict sense — a second, **separately-derived** check on the same predictive claim — held to a deliberately secondary role. It **contests or strengthens** a `validated` result (the two pressure indices, §2.0); it does **not** falsify one (only the holdout does, §3) and it never **grants** a status (`validated` stays the holdout's to confer, `asserted` is out of scope here entirely — §3A.1, §3A.3).

## 3A.1 What this test does and does not establish

It tests the **same** predictive claim as §3 — "high-`bug_pressure` files attract defect activity" — against a separately-derived label. It is deliberately **secondary**:

- It can **strengthen or contest**, but it does **not** independently confer or revoke `validated`. The temporal holdout (§3) remains the sole grantor of that status, because the issue label carries biases the holdout does not (§3A.7) and a precondition that may not hold (§3A.13.0).
- A signal that **passes §3 but is contested here** stays `validated` but is reported with a `divergence` flag (§3A.8) — never silently clean. A divergence is a documented finding to investigate, not a number to average against the holdout (this mirrors the layering-not-unification stance, `structural-mapper-spec.md` §6).
- It never operates at the `asserted` tier. The two pressure indices are `kind: predictive` and may not be `asserted` (parent §3.8). The concurrent mode of §3A.3 produces a *recognition-grade description check*, not an `asserted` **status grant** — recognition is one of the two bases the parent §2.1 already uses to confirm descriptive signals, and invoking it here changes no signal's status.
- Promotion of this test to a **co-equal falsifier** (one that can grant or revoke `validated` on its own) is deferred until the §3A.7 biases are controlled **and** the §3A.13.0 precondition is verified — the same "promote it when it can be earned" discipline as SZZ-blame (§3.4.1) and `blast_radius_index` (§2.3).

No new `validation_status` value is introduced; the §3.8 set is unchanged. Corroboration produces its own **outcome vocabulary** (§3A.10), which is distinct from `validation_status` and rides in a separate block and report section.

## 3A.2 The label

A per-file defect signal derived from tracked issues on a repo-backed project:

- **Eligible issues.** Issues with a **non-null, repo-relative `file_path`**, and an **affirmative, triaged defect status** — i.e. a status that positively means "confirmed defect," **not** merely the *absence* of a disqualifying label. Issues that are `false-positive`, `observation`, or **untriaged/open-unconfirmed** are excluded; an unreviewed issue must not enter the positive set by default (closes the "absence-of-disqualifier ⇒ positive" leak). Agent-discovered issues qualify; **user-submitted issues are excluded** — they routinely carry `file_path: null` and reflect a different selection process. The triaged-status predicate is recorded in the validation config and feeds the fingerprint (§3A.11).
- **Path normalization (mandatory, rename-aware).** Issue paths arrive mixed — some repo-relative (`src/middleware/error-handler.ts`), some absolute (`/home/<user>/<repo>/src/...`). Strip to repo-relative and map onto the substrate's node ids — the post-exclude HEAD inventory (`repo-substrate-spec.md` §5 node-set invariant). Mapping is **rename-followed**: a path logged before a rename is resolved to its HEAD node, so a positive is never silently attached to a *different* file that now occupies the old path. Two failure modes are reported, not hidden: issues whose file is **absent from the node set** (deleted before HEAD, or excluded by globs) are dropped as a **coverage caveat** (parallel to the §3.3 survivorship exclusion); issues whose path is **ambiguous after normalization** (absolute-path root cannot be resolved to exactly one node) are dropped as a **normalization caveat**. Both counts appear in the report.
- **Label form.** Two parallel encodings, both reported; the **primary endpoint is fixed in advance** (§3A.4) so the passing variant cannot be chosen post hoc:
  - **Binary** — a file is a positive iff it carries ≥1 eligible issue. Used for precision@k / PR-AUC, parallel to §3.4.
  - **Graded** — per-file eligible-issue count. Severity weighting (by `failureSeverityCode` `C/H/M/L/I`) is **secondary and reported-only**; the *primary* graded label is **unweighted**, pre-committed in config, so "optionally weighted" is no longer a researcher degree of freedom.

## 3A.3 Temporal discipline — the predictive/descriptive fork

The mode must match what the signal claims (the §2.1.1 boundary), so the test is run **predictively by default**:

- **Predictive (the honest test for a `validated` index).** Choose a substrate SHA `T`; compute the index from the **training history up to `T` only**; include only issues **first seen after `T`** (by `firstSeenRunId` timestamp). The index must then rank-predict where *future* issues land. This is a genuine forecast and is the only mode that can corroborate `validated`.
  - **Discovery-time ≠ manifestation-time caveat.** "First seen after `T`" is a clean control for *look-ahead leakage* only. It does **not** guarantee the defect *manifested* after `T`: a late agent run, or a newly deployed lens, can surface a defect that existed in training-window code. So a post-`T` issue set that spikes immediately after a new lens deployment is flagged (the report records lens-deployment events within the holdout window); it does not, on its own, invalidate the run, but it is a known contaminant of the forecast set.
- **Concurrent (descriptive, recognition-grade — not for status).** Issues seen at or around `T` test only whether the index *describes* present defect concentration — a recognition check (parent §2.1). It can corroborate a **descriptive reading** of the index's distribution, but it confers nothing: it neither grants `asserted` (the indices under test are predictive) nor `validated` (it is not a forecast). It is logged with `mode: "concurrent"` and excluded from any status reasoning.

The fork is the same line as §2.1.1: post-`T` issues = forecast = `validated`-grade evidence; concurrent issues = description = recognition-grade evidence. A corroboration run records which mode it used.

## 3A.4 Metrics, baselines, and the primary endpoint

Same metric family as §3.6, so the two tests report comparably — with tie-correction and a single declared primary endpoint:

- **Primary endpoint (declared in advance).** **Kendall τ-b** (tie-corrected) between the index ranking and the **unweighted graded** issue label. τ-b is mandated over τ-a / Spearman because the graded label is zero-inflated and heavily tied (most files have 0 issues, a few have 1, rarely 2+); plain τ-a / ρ are distorted by ties. The schema and the gate both read τ-b — no Spearman/Kendall split between report and pass rule.
- **Secondary endpoints (reported, not gated).** precision@k / PR-AUC against the binarized label, for `k` as in §3.6; severity-weighted τ-b. These contextualize but do not decide.
- **Baselines — including the `load_index` baseline.** Beyond the §3.5 recency and busyness baselines, the index is compared against a **`load_index`/centrality baseline**, for the reason in §3A.7. The headline number is `bug_pressure`'s **lift over the stronger of {busyness, `load_index`}**, not raw correlation. Picking the *stronger* baseline is conservative (it raises the bar), so this is baseline-hardening, not post-hoc baseline-shopping.
- **Margins are defined for the metrics actually used.** §3.7's margins (`+0.05` ROC-AUC, `1.20×` PR-AUC) are not defined for τ-b or precision@k, so this section states its own (tunable, versioned in the validation config exactly like §3.7):
  - τ-b: index τ-b **lower CI bound** (§3A.5) ≥ `τ_corr` (default `0.30`) **and** ≥ best-baseline τ-b **+ `τ_margin`** (default additive `+0.10`).
  - precision@k: index precision@k **lower CI bound** ≥ `pk_mult` × best-baseline precision@k (default multiplicative `1.20×`, mirroring §3.7's PR-AUC form).

All four threshold values (`τ_corr`, `τ_margin`, `pk_mult`, and the §3A.5 floors) feed the report fingerprint, so any future tightening is itself versioned and auditable.

## 3A.5 Uncertainty and the statistical floor (the n problem)

The issue corpus is small and sparse (§3A.13): per-file counts are low and `n_post_T_positives` can be in the low tens or single digits. A point estimate at that n is inside its own noise band, so **no pass/fail is emitted from a point estimate.**

- **Confidence intervals on every gated statistic.** τ-b and precision@k carry a **bootstrap CI over files** (resample the scored population); the **gate reads the lower CI bound**, never the point estimate (§3A.4). A point estimate that clears a threshold but whose lower bound does not → **not a pass**.
- **A null model for τ-b.** Significance against a **label-permutation null** (shuffle the issue label across the eligible population, recompute τ-b, repeat) is reported alongside the CI. A τ-b that is not distinguishable from the permutation null is reported as such regardless of its point value.
- **A numeric floor on the predictive positive set.** `n_post_T_positives < N_min_issue_positives` (config default `15`) → the repo's verdict is **`untested`** (§3A.9), mirroring parent §4's `N_min` and the zero-fix-commit refusal. This is the operational form of §3A.13's "treat a thin corpus as untested" — it is a number, not a judgment call. Note the floor is on the **post-`T` positive count**, not the total issue-file count: a repo with 40 lifetime issue-files but 6 post-`T` positives is below the floor.

## 3A.6 Pass criteria

Proposed pass criteria (tunable, versioned like §3.7). A predictive-mode corroboration run **corroborates** a signal iff, on **≥2 reference repos**:

1. `n_post_T_positives ≥ N_min_issue_positives` (§3A.5) on that repo — else that repo is `untested`, not a pass or fail, **and**
2. τ-b clears both the absolute floor and the baseline margin **on its lower CI bound** (§3A.4), **and**
3. precision@k clears the baseline multiplier **on its lower CI bound** (§3A.4), **and**
4. issue-file coverage (§3A.2) ≥ `0.50` on that repo — else "insufficient coverage" (§3A.9), parallel to §3.7 clause 3 and §4.

These bars are deliberately below the §3.7 holdout bars because the label is noisier; the CI-lower-bound discipline is what keeps "below the holdout bar" from collapsing into "passes on noise."

## 3A.7 The selection-bias confound, and the bounded claim it permits

The defining limitation, on the page so a reviewer can challenge it: tracked issues are produced by **running cognitive-lens agents (and human reviewers) over the code**, and those reviewers preferentially scrutinize central, important files. So issue density may correlate with centrality because that is **where people look**, not where defects are — the review-side analogue of the substrate's own busyness confound.

The `load_index` baseline (§3A.4) is the mitigation, and its reach must be stated honestly:

1. The `load_index` baseline is **mandatory, not optional** — corroboration counts only as lift *over* one measured channel of where-reviewers-look.
2. **But `load_index` is only one attention channel.** Review attention is also driven by busyness, recency, and complexity — and those signals live **inside `bug_pressure`** (parent §2.0, §3.5) while sitting **outside** the `load_index` baseline. The draft also concedes `bug_pressure` and `load_index` are themselves correlated. So lift over `load_index` removes centrality-driven attention but **not** churn- or complexity-driven attention.
3. **Therefore the claim is narrowed to what the baseline can support.** A positive predictive-mode result reads as:

   > **"`bug_pressure` adds ranking signal for tracked-issue location beyond busyness and centrality."**

   It does **not**, on the strength of a `load_index` baseline alone, read as "beyond review-attention" — that stronger claim requires controlling the **full attention surface** (busyness + complexity + recency jointly, or an externally measured attention signal such as PR-review file coverage or reviewer file-open telemetry). Controlling the full surface, or using a defect label drawn from outside the lens family entirely (incident post-mortems, CVE/advisory attributions), is **deferred** — the documented path to the stronger claim, on the same "promote it when earned" discipline. The §6.2 report must state results in the narrowed terms.

## 3A.8 The divergence criterion

"Divergence" is the section's headline contribution, so it is defined operationally rather than left to the schema field. Divergence between §3 and §3A is computed at **two levels**, and the schema records both:

- **Verdict-level (the gating definition).** A signal **diverges** when its §3 holdout verdict and its §3A predictive-mode corroboration verdict disagree on the same reference set — specifically when §3 confers `validated` but §3A returns `contested` (failed §3A.6) on **≥1 reference repo where the run was not `untested`/`insufficient-coverage`**, or the symmetric case. `divergence_with_holdout` (§3A.14) is set from this rule. Divergence **does not change `validation_status`** (§3A.1) — it raises a flag and a report entry.
- **Metric-level (early-warning, reported-only).** Per reference repo, a **sign disagreement** in rank correlation (holdout fix-label τ-b and issue-label τ-b point in opposite directions) or a precision@k gap beyond `divergence_margin` (config default `0.20`) is recorded as a metric-level divergence even when the verdict-level rule does not trip. This surfaces a brewing disagreement before it flips a verdict.

A run with both labels `untested` on a repo produces **no** divergence claim for that repo (you cannot disagree from two non-results).

## 3A.9 Degenerate cases — never silently pass

The protocol refuses to run rather than fabricate a verdict when (parallel to §4):

- **Zero eligible issues** — every issue on the repo is user-submitted, `false-positive`, `observation`, untriaged, or `file_path: null`. No positives, nothing to rank against; τ-b and precision@k are undefined → **`untested`** with reason `no_eligible_issues`.
- **Below the positive-set floor** — `n_post_T_positives < N_min_issue_positives` (§3A.5) → **`untested`** with reason `thin_corpus`.
- **Insufficient coverage** — issue-file coverage `< 0.50` on a reference repo → that repo's outcome is **`insufficient_coverage`** (§3A.6 clause 4); if true on *every* reference repo, the signal's corroboration outcome is `insufficient_coverage` overall.
- **Unpinned snapshot** — the issue snapshot is not frozen to a recorded as-of and id set (§3A.11) → the run is **refused** (not `untested`): a non-deterministic corroboration is not allowed to emit any verdict.

In all `untested`/`insufficient_coverage` cases the affected signal ships the outcome with an explicit reason and is **never rendered as corroborated** anywhere downstream.

## 3A.10 Corroboration outcomes — the verdict vocabulary

A §3A run emits a **corroboration outcome**, which is **not** a `validation_status` (the §3.8 set is unchanged) and must be enumerable so a consumer can distinguish "ran and disagreed" from "could not run":

- **`corroborated`** — predictive-mode run met §3A.6 on the reference set; agrees with the holdout.
- **`contested`** — predictive-mode run ran and **failed** §3A.6 on ≥1 non-degenerate reference repo. Pairs with `divergence_with_holdout: true` when §3 conferred `validated`. **Does not revoke `validated`** (§3A.1).
- **`insufficient_coverage`** — coverage `< 0.50` (§3A.9).
- **`untested`** — could not run (§3A.9: `no_eligible_issues`, `thin_corpus`, or concurrent-only data with no post-`T` positives).

The per-repo and overall outcomes both use this enum; the schema field is the enum string, **not** a boolean (a boolean cannot encode `insufficient_coverage`/`untested`, which would silently collapse "could not run" into "failed").

## 3A.11 Determinism and the issue snapshot

The verdict is a pure function of `(substrate at T, issue snapshot, validation config)`. Unlike git history, the **issue set drifts** — issues are added, resolved, and **re-triaged in place** — so a corroboration run **pins its snapshot**:

- It records the as-of timestamp and the set of contributing run/issue ids, **and hashes the snapshot *content*** — each contributing issue's `file_path`, triaged status, `firstSeenRunId`, and `failureSeverityCode` — into a `corroboration_fingerprint`. Hashing **content, not just ids**, is deliberate: an issue re-triaged in place (path edited, flipped to/from `false-positive`) changes the content hash even though its id is unchanged, so a verdict that moves because of a retroactive edit is always attributable. Hashing ids alone would let a re-triage silently change the verdict under a stable fingerprint — the exact failure this section exists to prevent.
- Re-running against the same pinned snapshot is byte-identical; a changed snapshot is a fingerprint change, mirroring `config_fingerprint` (`repo-substrate-spec.md` §3).

## 3A.12 Tooling

Parallel to §7. The issue snapshot is produced by a **named, recorded extraction** so two implementers fetch the same input:

- **Source.** The tracked-issue store of record (the validation platform's issue tracker / MCP). The validation config records the **tracker identifier, the project set, and the exact query** (the eligibility predicate of §3A.2 expressed as a filter: non-null `file_path`, triaged-defect status, agent-discovered, `firstSeenRunId` relative to `T`).
- **As-of mechanism.** The snapshot is taken at a recorded wall-clock as-of and the contributing ids are frozen (§3A.11); the extraction is **read-only** and re-runnable against the same as-of to reproduce the id+content set.
- **Stack.** Same as `repo-substrate` (Python 3.11+); reuses its `--truncate-at <split-sha>` mode for the index side and adds an issue-snapshot fetch + path-normalization step for the label side. No new extraction engine.

## 3A.13 Limits and open questions (on the page)

### 3A.13.0 Blocking precondition — error-source independence (review this first)

The corroboration's entire value rests on the issue label being **derived separately** from the git label, not merely **expressed in a different modality**. There is a path by which that fails *one level beneath* the shared-prior limitation below: **if any issue-logging agent used git-derived signals — churn, recency, co-change — to decide *where to look*, then issue density is a downstream transform of the same git data the index is built on**, and agreement with `bug_pressure` is autocorrelation wearing review's clothing. The divergence flag would then never fire when it should.

This is **not** resolvable from the spec. It is a factual question for the **cognitive-lens agent owner**: *what inputs do the issue-logging agents consume to prioritize files?* Until answered:

- The word "independent" in this section means **modality-independent only**, not error-source-independent.
- A `corroborated` outcome is reported as **provisional on this precondition**.
- Co-equal-falsifier promotion (§3A.1) is blocked on a negative answer (agents do **not** consume git-derived targeting signals).

### 3A.13.1 Other limits

- **"Closer to defect origin" is a claim, not a given.** This section no longer asserts the issue label sits nearer the defect than a fix-edit. A reviewer flags where a *symptom* surfaces, which carries the same caller/callee, test/code displacement §3.4.1 owns for fix-edits — it may be nearer or farther. The corroboration's value does **not** depend on the issue label being nearer; it depends on it being **separately derived** (§3A.13.0). Any "nearer-to-origin" benefit is upside, not a premise.
- **Same-org corpus.** The available issue corpus is all one org (the registry and mcp projects). A different *modality* (review vs git), **not** a different org, so it does **not** discharge the cross-org generalization question (§8.1; tribunal finding A5). It narrows that gap; it does not close it.
- **Sparsity.** Most issues carry `timesSeen: 1` and per-file counts are low. The §3A.5 floor + CI discipline are the response; report the issue-file `n` and `n_post_T_positives` on every run.
- **Agent-produced label / shared prior.** If the same family of lenses that logged the issues also shaped the index design, the corroboration inherits a shared prior (the Hume habit objection, one layer up). Mitigate by drawing issues from agents/projects **not involved in tuning the indices** — separation of *operators*. Note this separates operators, **not** the lens family's defect concept; a fuller break uses labels from outside the lens family (incident post-mortems, CVEs), per §3A.7.
- **Two proxies, shared salience tilt.** §3's fix-edit label and §3A's issue label both tilt toward central/busy files, so "agreement strengthens" is partly the shared confound, not two independent confirmations. This is why agreement only *strengthens confidence* and never *confers status* (§3A.1).
- **Contests, does not falsify.** The holdout falsifies; this contests or strengthens. Treat a §3-vs-§3A divergence (§3A.8) as a finding to investigate, not an average to take.

### 3A.13.2 New open questions to fold into §8

- The reference-issue-corpus: which projects, how the snapshot is frozen, the separation-of-duties rule (§3A.13.1), and the §3A.13.0 precondition.
- Calibration of `N_min_issue_positives`, `τ_corr`, `τ_margin`, `pk_mult`, and `divergence_margin` once real corroboration numbers exist (parallel to §8.2).
- Whether to retain pre-HEAD-deletion issues as positives in a variant (parallel to §8.4 survivorship).

## 3A.14 Schema and report

**`validation.json`.** A predictive signal MAY carry an `issue_corroboration` block beside its `holdout` block (never instead of it). The block is **not** a `validation_status` and never alters one:

```json
"bug_pressure_index": {
  "status": "validated",
  "kind": "predictive",
  "holdout": { "...": "see §6.1" },
  "issue_corroboration": {
    "mode": "predictive",
    "outcome": "corroborated",
    "claim_scope": "adds ranking signal beyond busyness and centrality",
    "precondition_independence": "provisional",
    "corroboration_fingerprint": "<sha256 of issue snapshot CONTENT + config>",
    "as_of": "<ISO8601 split point T>",
    "config": {
      "N_min_issue_positives": 15,
      "tau_corr": 0.30, "tau_margin": 0.10, "pk_mult": 1.20,
      "divergence_margin": 0.20,
      "primary_endpoint": "kendall_tau_b_unweighted",
      "triaged_status_predicate": "<recorded filter>"
    },
    "repos": [
      {
        "name": "uluops-registry-api",
        "outcome": "corroborated",
        "tau_b": 0.41, "tau_b_ci": [0.33, 0.49],
        "permutation_p": 0.004,
        "precision_at_k": { "10": 0.50 },
        "precision_at_k_ci": { "10": [0.24, 0.76] },
        "lift_over_load_index": 0.12, "lift_over_load_index_ci": [0.03, 0.21],
        "lift_over_busyness": 0.09,
        "n_issue_files": 23, "n_post_T_positives": 17,
        "coverage": 0.68,
        "dropped_absent": 4, "dropped_ambiguous": 1
      }
    ],
    "divergence_with_holdout": false,
    "divergence_detail": { "verdict_level": false, "metric_level_repos": [] },
    "note": "Beats the load_index and busyness baselines on lower CI bound on both repos; agrees with the holdout. Claim scoped to 'beyond busyness + centrality' (§3A.7); independence precondition (§3A.13.0) unconfirmed."
  }
}
```

- `outcome` ∈ {`corroborated`, `contested`, `insufficient_coverage`, `untested`} (§3A.10) — an enum string, never a boolean.
- Every gated statistic carries a CI; the gate reads the lower bound (§3A.5).
- `precondition_independence` ∈ {`confirmed`, `provisional`, `failed`} records the §3A.13.0 answer.

**Holdout report (§6.2).** Add a section: **"Cross-source corroboration"** — per predictive signal, the corroboration `outcome`, τ-b with CI and permutation-p, lift over the `load_index` and busyness baselines (lower CI bound), coverage, `n_post_T_positives`, and **any divergence from the §3 verdict**, stated in the §3A.7 narrowed terms ("adds ranking signal beyond busyness and centrality") with the §3A.13.0 precondition status shown.

---

## Cross-references to update when folding this in

- **§2.0** — note that the two predictive indices now face the holdout (falsifier) **and** this corroboration (a secondary, non-status check); only the holdout confers status in v0.
- **§2.3** — a future `blast_radius_index` is corroborable by this same mechanism (co-change issues that span files).
- **§3.4.1** — link forward, **without "substitute" language**: tracked issues are a separately-derived, secondary corroboration whose label sits in a different modality; they **narrow** the gap the SZZ note motivates but are **not** a stand-in for the holdout's defect label and do not participate in conferring `validated`.
- **§3.8** — unchanged; corroboration adds no `validation_status` value. Note that the corroboration **outcome** vocabulary (§3A.10) is a separate enum.
- **§4** — §3A.9 is the corroboration analogue of this section; cross-link the two "never silently pass" lists.
- **§5** — the gate is unaffected: a `divergence`/`contested` corroboration does not change a signal's `validation_status`, so it does not change what the gate admits; the flag is a report-level finding.
- **§6.1 / §6.2** — schema and report additions above.
- **§8** — add the open questions in §3A.13.2, **including the §3A.13.0 independence precondition** as a named blocker.
- **`repo-substrate-spec.md` §5 / §5.2** — path-to-node mapping reuses the node-set invariant and must be rename-followed (§3A.2); `cochange_degree` is the bridge to the `blast_radius` extension.
- **`structural-mapper-spec.md` §3** — unchanged; this only affects how confident we are in a `validated` signal, not how the gate reads it.
