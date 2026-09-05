# Validation — Specification (v0)

*The falsifiable core of the project. This spec turns "the indices feel right" into "the indices predict where defects actually land," using nothing but git history. It is the gate that separates a **diagnostic** product from a horoscope with good art direction: no index is allowed to feed a named structural feature (C3) until it has either passed the protocol here or been explicitly marked decorative.*

*Consumes: `substrate.json` (see `repo-substrate-spec.md`) and, for the secondary corroboration test (§3A), a pinned snapshot of the platform's tracked issues. Produces: a per-signal `validation_status` verdict, an optional per-predictive-signal cross-source corroboration outcome (§3A), and a written holdout report. Referenced by: `repo-substrate-spec.md` §10, `structural-mapper-spec.md` §3 (anti-horoscope gate), and the system spec's anti-horoscope cross-cutting contract.*

---

## 1. Governing principle

The substrate claims only **"deterministic structural signals derived from repo history and static topology"** — never "architectural truth." Validity is established empirically and is allowed to fail. A failing result is not a bug; it is a finding that constrains C3. The whole point is that the test *can* come back negative and we will honor it.

Validation has a hard boundary: it can only falsify signals that make a **predictive claim about the future**. The protocol below validates exactly those (`validated`). Present-tense *descriptive* signals are confirmed on a different basis — stability and cross-modal corroboration (`asserted`, §2.1, operationalized in §2.4). That is a different **kind** of grounding, and, as currently operationalized, a **weaker** one: a `validated` signal's falsifier is a held-out forecast that can come back negative; an `asserted` signal's falsifier is a second present-tense measurement that can disagree. Both can fail; only the first fails against the future. The ordering matters for what a feature may claim (§2.1.1) and is the ordering the C3 min-operator encodes (`structural-mapper-spec.md` §5). *(Revised 2026-09-04, D-004: the earlier "not a weaker one" wording was withdrawn after the June 19 tribunal showed it was contradicted by the mapper's own operator and had no falsifier.)*

## 2. Scope — which signals this gates

`validation_status` is a property of **any signal that can feed a named feature** — a composite index, a bare percentile, or a raw metric — not of indices alone. This matters because the v0-default predicate strategy is the in-repo *percentile* (substrate §6.1), and several named features (flooded basement, foundation) can be written directly over percentiles with no index in the path. If status attached only to indices, such a feature would slip the gate (§5) entirely. So the rule is: **every signal a feature reads carries a status, and the holdout can confer `validated` only on the two predictive indices.** Every other signal is descriptive and is confirmed as `asserted` (§2.1) — a different kind of grounding, held to its own falsifier (§2.4).

### 2.0 The two falsifiable indices

| Index | Makes a future-predictive claim? | Validated here? |
|---|---|---|
| `bug_pressure_index` | Yes — "this file will keep accruing fix-activity" (a proxy for defects, §3.4.1) | **Primary target** |
| `change_pressure_index` | Yes — "this file is actively unstable" | **Primary target** |
| `load_index` | No — describes present topological position | No (see §2.1) |
| `neglect_index` | No — describes present age/abandonment | No (see §2.1) |
| `reinforcement_index` | No — describes present test support | No (see §2.1) |
| `complexity_proxy_index` | No — describes present intricacy | No (see §2.1) |

**This boundary is the spec's most important clarification.** The temporal holdout predicts future `fix` commits. Only the two pressure indices claim to do that. `load_index` is not wrong because it doesn't predict fixes — it was never a fix-predictor; it answers "what is load-bearing *now*." Holding `load_index` to a fix-prediction test would be a category error.

The two predictive indices now face **two** falsifiable tests: the temporal holdout (§3) and a secondary cross-source corroboration against tracked issues (§3A). Only the holdout confers `validated` in v0; corroboration strengthens or contests that verdict but never grants or revokes it.

### 2.1 How non-predictive indices earn their status

The four non-predictive indices describe **present-tense structural facts** — load-bearingness, neglect, test support, intricacy. They make no claim about the future, so the holdout has nothing to test. That is a **difference in kind, not a deficiency**: you do not falsify "this file is load-bearing *now*" with a fix-prediction test any more than you falsify a thermometer with a weather forecast. They are confirmed on a different basis:

- **Stability.** A small code change must not move the signal much. An unstable description is a bad description even when "correct." Operationalized as a numeric budget in §2.4.1.
- **Cross-modal corroboration.** The signal must agree with a second measurement of the *same present-tense property* taken from a modality that does not appear in its formula. Operationalized in §2.4.2. This replaces the "recognition" basis of earlier drafts: the June 19 tribunal showed that developer recognition of a list built from `fan_in` is assent to `fan_in`, not a test of it.
- **Recognition (recorded, not gating).** The developer's sealed blind ranking is reported beside the mechanical check (§2.4.3).

A signal confirmed this way carries `validation_status: "asserted"`. The two statuses are different epistemic claims:

- `validated` = "**predicts** where defects land, confirmed against held-out data." A claim about the future.
- `asserted` = "**describes** a real structural fact of the present, confirmed by stability and a second modality." A claim about what is.

`asserted` is empirically grounded — in measured topology and history — and it is not a failed `validated`, because a `kind: descriptive` signal was never eligible for the holdout (§3.8). But it is the weaker of the two groundings for the purpose of what a feature may *say*: an `asserted` signal licenses a description of the present and nothing more (§2.1.1). Provenance records which basis a signal rests on so C5 speaks in the right register.

#### 2.1.1 The line `asserted` may not cross (the descriptive/predictive boundary — referred to elsewhere as "the A2 boundary")

The thermometer analogy is only honest if the descriptive claim stays **synchronic** — about the present graph, not its counterfactual future. The danger is a word like "load-bearing," which colloquially means *"if this changed, much would break"* — a counterfactual about propagation, i.e. a prediction in descriptive clothing. If an `asserted` signal were allowed to carry that meaning, it would be an unfalsifiable forecast exempted from the holdout — the horoscope move, relocated above the gate. So the boundary is drawn explicitly:

- **What an `asserted` signal MAY claim:** a *present structural position*. `load_index` asserts **"occupies a high-centrality position in the current import graph"** — a fact about a graph that exists now, as synchronic as `fan_in = 40`. Nothing about what will happen.
- **What it MAY NOT claim:** a *consequence*. "Changing this will break much," "this will ripple," "this is fragile" are counterfactual/temporal claims. They are **predictions, not descriptions**, and may not be carried at the `asserted` tier. A consequence claim must be `validated` (it is testable — see §2.3) or it does not get made.

The test for which side a claim is on: *can it be wrong about the future?* "High centrality now" cannot — it is a measurement of the present. "Changes here break much" can — so it must earn its status through the holdout, not borrow the description's exemption.

### 2.2 Bare percentiles and raw metrics (closing the default-path leak)

A feature may also be written directly over a percentile (`fan_in` pctile ≥ p90) or a raw metric, bypassing the indices. These signals get a status by the same rule, with one hard ceiling:

- **They can never be `validated`.** Only the two predictive indices (§2.0) are falsifiable by the holdout. A bare percentile makes no future-predictive claim, so the holdout cannot confer `validated` on it.
- **They reach `asserted` only with a §2.1 justification.** A percentile/raw signal that a ruleset author wants to feed a *diagnostic* feature must carry the same intuition + stability backing as a non-predictive index, recorded against that signal. With it, the signal is `asserted`; without it, the signal is `untested` — **not** `unvalidated`. The vocabulary is precise (per §3.8): `unvalidated` means "ran the holdout and failed §3.7," which a bare percentile cannot do because the holdout never applies to it; a signal the protocol cannot test is `untested` (§4). The two are treated identically by the gate (both hard errors unless decorative), but conflating them would misreport *why* a signal is ungated.
- **Otherwise the feature must be `decorative`.** An ungrounded percentile feeding a non-decorative named feature is the same hard error as an `unvalidated` or `untested` index (§5).

The effect: routing a diagnosis through a raw percentile no longer dodges the gate. The default predicate strategy is held to the same standard as the composite indices — which is the whole point of the gate.

### 2.3 Promoting a description to a forecast — `blast_radius_index` (future)

The propagation/consequence claim that `asserted` may not smuggle (§2.1.1) is not forbidden — it is **deferred until it can be earned.** "Changes to this file ripple into others" is directly testable against history: the substrate already carries `cochange_degree` (repo-substrate §5.2 — files that change in the same commit), and the holdout can label whether edits to a high-`cochange` file co-occurred with edits elsewhere in the holdout window. A future **`blast_radius_index`** built on that signal would be a *third predictive index* (§2.0), validated like the other two — at which point the load-bearing-*consequence* claim graduates from forbidden-at-`asserted` to honestly `validated`. This is the resolution of the smuggled-prediction problem: don't exempt the forecast, **promote** it through the gate. Until `blast_radius_index` exists and passes, no feature may voice a propagation consequence as a diagnostic claim. (A future `blast_radius_index` is also corroborable by the §3A mechanism — co-change issues that span files supply a review-modality label for the same propagation claim.)

### 2.4 Operationalizing the `asserted` bar

*Resolves system-spec open question #3 and mapper open question #3 (the stability budget), and the June 19 tribunal's remediation items #5 and #6. Decision record: `DECISIONS.md` D-004.*

A `kind: descriptive` signal earns `asserted` only by passing **both** gates below on **≥ `M_asserted` reference repos** (config, default 2). Either alone is insufficient: stability alone certifies a constant (`load_index ≡ 0.5` never moves), and a correctness check alone certifies noise that happened to correlate once.

#### 2.4.1 Stability budget (robustness)

Recompute the substrate at HEAD with the last **K** commits removed (config `stability_perturbation_k`, default `5`) and measure, per node, each signal's percentile movement against the unperturbed run.

Pass iff `median(|Δpercentile|) ≤ stability_eps` (default `0.05`) **and** `max(|Δpercentile|) ≤ stability_delta` (default `0.15`) over the **untouched** population: nodes present in both runs and **not edited by any of the K removed commits** (D-008). A file those commits edited has its recency, churn, and co-change legitimately move — that is the signal reporting the edit, not instability. The budget measures whether editing *other* files moves *this* file's value. Nodes born inside the removed window are absent from the perturbed run and so excluded by construction. `p95(|Δ|)` is reported beside `max`. A signal that swings past budget on a small edit is `untested` with reason `unstable` — never `asserted`.

This proves the description is *stable*, not *correct*. That is why 2.4.2 is mandatory.

#### 2.4.2 Corroboration (correctness) — by grounding class

*Revised 2026-09-04 (D-008) after the first gate run. The June draft of this section paired every descriptive signal with a "different modality"; the run showed that for topological signals no such modality exists in v0, and that the one chosen (co-change for load) measured a different property. The bar is now set per class, recorded in `validation.json` as `grounding_class`.*

Every descriptive signal is placed in exactly one class. The pairing is fixed in the validation config and feeds the fingerprint.

| Class | What it covers | Correctness bar (beyond stability) | v0 members |
|---|---|---|---|
| **G1 measurement** | direct git or file facts whose instrument is git or the file itself and whose name is literal | none — the instrument is trusted; Popper's constant objection targets models, not measurements | `commit_count`, `churn_lines`, `fix_count`, `revert_count`, `author_count`, `last_touched_days`, `size_loc`, `nesting_proxy`, `cochange_degree`, `blame_age_median` |
| **G2 instrument-checked** | resolver-dependent facts, where the instrument can be wrong | τ-b vs an **independent second instrument measuring the same property**, bootstrap lower CI ≥ `tau_instrument` (default `0.60` — same property twice should agree strongly) | `fan_in`, `fan_in_nonzero`, `fan_out` ↔ `fan_in_alt` / `fan_out_alt` (a regex scanner with its own resolver, `repo-substrate-spec.md` §5); `has_sibling_test` ↔ `test_fan_in` (importers that are test files) |
| **G3 cross-modal** | a signal for which a **different modality** measures the same present-tense property | τ-b vs the counterpart, lower CI ≥ `tau_asserted` (default `0.30`) | `age_days`, `neglect_index` ↔ `blame_age_median` (median age of surviving lines) |
| **G4 derived** | fixed-weight blends and graph functions of asserted inputs | every input `asserted`; the composite's **name carries no claim beyond its inputs** (D-004 Q3) | `centrality` (from `fan_in`); `load_index`; `complexity_proxy_index`; `reinforcement_index` |

**Reported correlates.** A signal may declare correlates that are computed and printed but never gate: `load_index` ~ `cochange_degree` and `test_fan_in`; `neglect_index` ~ `cochange_degree`. On the first run `load_index` ~ co-change was τ 0.24 / 0.44 — informative (a foundation is imported by many and changed by few), not a correctness test.

**Why a second instrument for the load family, not a second modality.** The June 19 proposal specified blind, pre-registered rankings from three or more developers who know the repo. That removes confirmation bias but is unavailable to a single-developer project, and a gate that cannot run leaves the whole tier unreachable. D-004 then paired load with co-change; the run showed co-change is *change* coupling, which is conceptually a different property from import reach. There is no independent measurement of "load-bearing" in v0. So the substrate stops claiming one: `fan_in` is checked as a *measurement* (two instruments, one property — this can fail on alias-heavy and dynamic-import code, which is substrate open question #8 made measurable), and `load_index` is a named blend of checked measurements whose name is bounded by §2.1.1 and the C5 register lint. Lowering the τ floor until co-change passed was not considered.

**What each class can and cannot certify.** G1 certifies that git said so. G2 certifies that two independent readers of the source agree. G3 certifies that two different kinds of evidence agree. G4 certifies only that its parts are certified and its weights are fixed. None of them certifies that a *name* is apt; that is the register boundary's job.

#### 2.4.3 Recorded recognition (not gating)

The developer's sealed blind ranking (`blind/<repo>.md`, committed by hash before the first substrate run on that repo) is compared to each descriptive signal's top-K and reported as τ-b with `n` stated. At `n = 1` it carries no gate. It is the human sanity check the report shows beside the mechanical one, and the place a reviewer looks first when 2.4.2 passes on a repo the developer knows well.

#### 2.4.4 The gate

`asserted` ≝ passed 2.4.1 ∧ the 2.4.2 bar for the signal's class, on ≥ `M_asserted` repos; for G4, additionally every input is `asserted` overall (inputs are resolved first, in dependency order). The `validation.json` `grounding` block records the stability result, the corroboration result, the reported correlates, and the recognition comparison (§6.1). Failing yields `untested` with the specific reason (`unstable`, `corroboration_fail`, `input_not_asserted:<name>`, `too_few_pairs`), never a silent `asserted`.

**Known limit (on the page).** If on every reference repo the counterpart correlates with the signal so strongly that 2.4.2 cannot fail, it is not a falsifier and a third modality is needed. The holdout report (§6.2 section 4) prints the τ distribution across repos so this is checked, not assumed.

## 3. The temporal-holdout protocol (primary, falsifiable)

### 3.1 Split

- **Method.** Order the timeline chronologically. The first **80% of commits** form the **training window**; the final **20%** form the **holdout window**.
- **Why commit-count, not wall-time.** An 80%-of-time split is distorted by idle gaps — a repo dormant for a year then active produces a near-empty or overstuffed holdout. An 80%-of-commits split keeps both windows populated on bursty histories. (Alternative wall-time split is recorded as a config option but is not the default.)
- The split commit SHA is recorded in the report so the partition is reproducible.

### 3.2 Index computation

Compute all indices **using only commits in the training window** — the same `repo-substrate` pipeline, with history truncated at the split. No information from the holdout window may enter any index value. (This is the discipline that makes it a real holdout and not in-sample fitting.)

### 3.3 Eligible population

A file is **eligible for scoring** iff:
- it was introduced (rename-followed first touch) **before** the split, **and**
- it still exists at HEAD (not deleted before the holdout window ends).

Files **born in the holdout window** are excluded — they cannot be predicted from training-window signal. This exclusion is reported as a **coverage caveat** (`scored_files / total_files`), never hidden. A repo where most files are holdout-born yields low coverage and a correspondingly weak verdict.

### 3.4 Labeling

Deterministic, git-only:

> **A file is a positive iff it received ≥1 `fix`-type commit (`type ∈ {fix, revert}`, per substrate §7) within the holdout window.**

No manual labeling, no judgment call. The label is a pure function of the classified timeline.

#### 3.4.1 What this label is — a declared proxy, not ground truth

The label measures **fix-edit locality** — "this file was *edited by* a fix" — which is used as a proxy for **defect locality** — "this file *harbored* the defect." These are not the same thing, and the spec must not pretend they are:

- **The gap.** A fix routinely edits a file other than the one that held the bug: the caller rather than the callee, the test rather than the code, a config or an adjacent module. Cross-cutting bugs touch several files, only one of which is the root cause; a bug whose root cause is a *missing* file leaves no positive at the true site at all. So the label has irreducible noise, and for certain bug classes it is *systematically* off-site.
- **Why the proxy is nonetheless used in v0.** It is **git-only, deterministic, and unmanipulable** — no human labeling, no judgment call, fully reproducible (the §1 properties the whole gate depends on). And the indices it validates are *rankers*: the claim is "high-`bug_pressure` files attract fix-activity," for which fix-edit locality is a defensible, directly-measurable signal. Fix-edits are correlated with defect sites even when not identical to them.
- **What declaring it changes.** This is an **accepted v0 risk, on the page so a reviewer can challenge it** — not a hidden assumption. Two consequences follow and are owned explicitly: (1) the label noise **caps achievable AUC** — a `validated` verdict means "beats baselines at predicting fix-*activity*," which is what we can honestly measure, not "predicts defect *origin*"; the holdout report (§6.2) must state the verdict in those terms. (2) If a repo's fixes systematically land off-site (heavy indirection, DI, test-driven fix style), the proxy degrades — related to A-class assumptions about coupling visibility; a low coverage or a baseline the index barely beats is the warning sign.
- **The principled tightening (future).** Defect locality *is* recoverable from history without manual labeling, via **SZZ-style blame**: take each fix commit, `git blame` the lines it changed, and attribute the defect to the commit/file that last touched those lines. That relocates the positive from "where the fix landed" to "where the bug was introduced." It is deferred from v0 (blame across renames is fiddly and language-agnostic line attribution is noisy in its own right), but it is the documented path from the declared proxy to a truer label — the same "promote it when it can be earned" discipline as `blast_radius_index` (§2.3). Until then, `fix`-edit locality is the honest, named stand-in. A separately-derived, review-modality label *does* exist in the meantime — tracked issues (§3A) — but it is a **secondary corroboration** of the same predictive claim, **not** a stand-in for the holdout label and not a participant in conferring `validated`; it narrows the gap this note describes without closing it.

### 3.5 Baselines (the index must beat these)

A high AUC is meaningless if a trivial heuristic matches it. The index is compared against the **stronger** of two naive baselines:

- **Recency baseline.** Rank files by `(1 − last_touched_days_pctile)` — "recently touched files get fixed next."
- **Busyness baseline.** Rank files by training-window `commit_count` — "the file everyone keeps editing gets fixed next."

Busyness is usually the stronger adversary; both are computed and the index must beat whichever scores higher.

### 3.6 Metrics

Computed for each candidate index and each baseline, against the §3.4 labels:

- **precision@k** and **recall@k** for `k ∈ {10, 20, ⌈0.05 · |eligible population|⌉}`.
- **ROC-AUC** — overall ranking quality.
- **PR-AUC** — *the honest metric under imbalance.* Holdout positives are typically a small fraction of files; ROC-AUC can look healthy while the top-k is mostly false positives. PR-AUC is reported alongside and is part of the pass criterion.

### 3.7 Pass criteria (proposed defaults — tunable, versioned in config)

An index is `validated` iff, on **≥2 reference repos** (UluOps Registry and mcp-secure-server for v0):

1. `index_ROC_AUC ≥ best_baseline_ROC_AUC + 0.05`, **and**
2. `index_PR_AUC ≥ 1.20 × best_baseline_PR_AUC`, **and**
3. `eligible coverage (§3.3) ≥ 0.50` on that repo (else the repo's verdict is "insufficient coverage," not a pass or fail).

4. the **best baseline's PR-AUC ≥ `signal_floor_mult` × the positive base rate** (default `1.5×`) on that repo — else the repo's verdict is **`insufficient signal`** (§4), neither pass nor fail.

Both numeric thresholds (`0.05`, `1.20`) are config values that feed the report fingerprint, so a future tightening is itself versioned and auditable. They are deliberately modest for v0 — the bar is "demonstrably better than trivial," not "excellent."

**Why the margins are relative, and why clause 4 exists (the label-noise ceiling).** §3.4.1 concedes the fix-edit label is noisy, which caps the achievable AUC of *every* ranker — index and baseline alike. An absolute bar could therefore be unpassable on a noisy repo; a bar relative to the strongest baseline is not, because the ceiling compresses both sides. The one margin that does get harder under compression is the multiplicative PR-AUC clause: as PR-AUC approaches the base rate, `1.20×` of a near-noise number is still near noise and the comparison is meaningless. Clause 4 guards that: if even the best baseline cannot lift PR-AUC to 1.5× the base rate, the label carries too little signal on that repo to distinguish any ranker, and the repo is excluded from the verdict rather than counted as a fail. *(Added 2026-09-04; tribunal remediation item #8.)*

### 3.8 Verdict values

Each signal (index, percentile, or raw metric) ends with one of:

- `validated` — a predictive index that passed §3.7 on the reference set. A confirmed **forecast** — specifically of fix-*activity* (the declared §3.4.1 proxy), read in those terms, not of defect *origin*.
- `unvalidated` — a predictive index that ran the protocol and failed §3.7. **A real finding.** Per §5, this constrains C3.
- `asserted` — a present-tense **descriptive** signal (non-predictive index, percentile, or raw metric) that passed the stability budget and the cross-modal check (§2.4). A different kind of grounding from `validated`, and the weaker one for the purpose of what a feature may claim (§1, §2.1.1).
- `untested` — the protocol could not run (§4), or it does not apply to this signal (a descriptive signal with no recorded §2.1 grounding). Treated as ungated by the gate (§5).

**Legal status is constrained by `kind` — this is what stops a failed predictor laundering itself into `asserted`.** A signal's `kind` (`predictive` / `descriptive`) determines which statuses it may hold:

- A **`kind: predictive`** signal (the two pressure indices) may be **only** `validated`, `unvalidated`, or `untested`. It **may not** be `asserted` — a forecast does not get to relabel itself as a description to dodge the holdout it failed.
- A **`kind: descriptive`** signal may be only `asserted` or `untested`. It may not be `validated` (it makes no forecast the holdout can confirm).
- A `validation.json` entry that pairs `kind: predictive` with `status: asserted` (or `kind: descriptive` with `status: validated`) is **malformed**: the C3 gate (§5) and the validation loader **reject it as a hard error**, exactly as if the signal were `untested`. A signal's `kind` is fixed by what it measures (§2), not chosen per-run — flipping `kind` to change the legal status set is the same malformed input.

## 3A. Cross-source corroboration via tracked issues (secondary, falsifiable)

The temporal holdout (§3) is the project's primary falsifier, but it rests on one declared proxy: its label is **fix-*edit* locality**, not **defect locality** (§3.4.1), and for some bug classes that proxy is systematically off-site. The validation platform's own tracked issues carry a second signal — a `file_path` (and `failure_code`) naming the file a reviewer or cognitive-lens agent judged defective. That label is drawn from a *different modality* (review, not git). Running the two together turns a single-modality verdict into **cross-source corroboration**: agreement strengthens confidence in a `validated` result; disagreement is itself a finding.

The independence the corroboration *logic* needs is not modality difference but **error-source independence** — the two labels must not share a confound. This section establishes modality difference and treats error-source independence as an **open precondition** (§3A.13.0), not an achieved property.

This is corroboration in the strict sense — a second, **separately-derived** check on the same predictive claim — held to a deliberately secondary role. It **contests or strengthens** a `validated` result (the two pressure indices, §2.0); it does **not** falsify one (only the holdout does, §3) and it never **grants** a status (`validated` stays the holdout's to confer, `asserted` is out of scope here entirely — §3A.1, §3A.3).

### 3A.1 What this test does and does not establish

It tests the **same** predictive claim as §3 — "high-`bug_pressure` files attract defect activity" — against a separately-derived label. It is deliberately **secondary**:

- It can **strengthen or contest**, but it does **not** independently confer or revoke `validated`. The temporal holdout (§3) remains the sole grantor of that status, because the issue label carries biases the holdout does not (§3A.7) and a precondition that may not hold (§3A.13.0).
- A signal that **passes §3 but is contested here** stays `validated` but is reported with a `divergence` flag (§3A.8) — never silently clean. A divergence is a documented finding to investigate, not a number to average against the holdout (this mirrors the layering-not-unification stance, `structural-mapper-spec.md` §6).
- It never operates at the `asserted` tier. The two pressure indices are `kind: predictive` and may not be `asserted` (§3.8). The concurrent mode of §3A.3 produces a *recognition-grade description check*, not an `asserted` **status grant** — recognition is one of the two bases §2.1 already uses to confirm descriptive signals, and invoking it here changes no signal's status.
- Promotion of this test to a **co-equal falsifier** (one that can grant or revoke `validated` on its own) is deferred until the §3A.7 biases are controlled **and** the §3A.13.0 precondition is verified — the same "promote it when it can be earned" discipline as SZZ-blame (§3.4.1) and `blast_radius_index` (§2.3).

No new `validation_status` value is introduced; the §3.8 set is unchanged. Corroboration produces its own **outcome vocabulary** (§3A.10), which is distinct from `validation_status` and rides in a separate block and report section.

### 3A.2 The label

A per-file defect signal derived from tracked issues on a repo-backed project:

- **Eligible issues.** Issues with a **non-null, repo-relative `file_path`**, and an **affirmative, triaged defect status** — i.e. a status that positively means "confirmed defect," **not** merely the *absence* of a disqualifying label. Issues that are `false-positive`, `observation`, or **untriaged/open-unconfirmed** are excluded; an unreviewed issue must not enter the positive set by default (closes the "absence-of-disqualifier ⇒ positive" leak). Agent-discovered issues qualify; **user-submitted issues are excluded** — they routinely carry `file_path: null` and reflect a different selection process. The triaged-status predicate is recorded in the validation config and feeds the fingerprint (§3A.11).
- **Path normalization (mandatory, rename-aware).** Issue paths arrive mixed — some repo-relative (`src/middleware/error-handler.ts`), some absolute (`/home/<user>/<repo>/src/...`). Strip to repo-relative and map onto the substrate's node ids — the post-exclude HEAD inventory (`repo-substrate-spec.md` §5 node-set invariant). Mapping is **rename-followed**: a path logged before a rename is resolved to its HEAD node, so a positive is never silently attached to a *different* file that now occupies the old path. Two failure modes are reported, not hidden: issues whose file is **absent from the node set** (deleted before HEAD, or excluded by globs) are dropped as a **coverage caveat** (parallel to the §3.3 survivorship exclusion); issues whose path is **ambiguous after normalization** (absolute-path root cannot be resolved to exactly one node) are dropped as a **normalization caveat**. Both counts appear in the report.
- **Label form.** Two parallel encodings, both reported; the **primary endpoint is fixed in advance** (§3A.4) so the passing variant cannot be chosen post hoc:
  - **Binary** — a file is a positive iff it carries ≥1 eligible issue. Used for precision@k / PR-AUC, parallel to §3.4.
  - **Graded** — per-file eligible-issue count. Severity weighting (by `failureSeverityCode` `C/H/M/L/I`) is **secondary and reported-only**; the *primary* graded label is **unweighted**, pre-committed in config, so "optionally weighted" is no longer a researcher degree of freedom.

### 3A.3 Temporal discipline — the predictive/descriptive fork

The mode must match what the signal claims (the §2.1.1 boundary), so the test is run **predictively by default**:

- **Predictive (the honest test for a `validated` index).** Choose a substrate SHA `T`; compute the index from the **training history up to `T` only**; include only issues **first seen after `T`** (by `firstSeenRunId` timestamp). The index must then rank-predict where *future* issues land. This is a genuine forecast and is the only mode that can corroborate `validated`.
  - **Discovery-time ≠ manifestation-time caveat.** "First seen after `T`" is a clean control for *look-ahead leakage* only. It does **not** guarantee the defect *manifested* after `T`: a late agent run, or a newly deployed lens, can surface a defect that existed in training-window code. So a post-`T` issue set that spikes immediately after a new lens deployment is flagged (the report records lens-deployment events within the holdout window); it does not, on its own, invalidate the run, but it is a known contaminant of the forecast set.
- **Concurrent (descriptive, recognition-grade — not for status).** Issues seen at or around `T` test only whether the index *describes* present defect concentration — a recognition check (§2.1). It can corroborate a **descriptive reading** of the index's distribution, but it confers nothing: it neither grants `asserted` (the indices under test are predictive) nor `validated` (it is not a forecast). It is logged with `mode: "concurrent"` and excluded from any status reasoning.

The fork is the same line as §2.1.1: post-`T` issues = forecast = `validated`-grade evidence; concurrent issues = description = recognition-grade evidence. A corroboration run records which mode it used.

### 3A.4 Metrics, baselines, and the primary endpoint

Same metric family as §3.6, so the two tests report comparably — with tie-correction and a single declared primary endpoint:

- **Primary endpoint (declared in advance).** **Kendall τ-b** (tie-corrected) between the index ranking and the **unweighted graded** issue label. τ-b is mandated over τ-a / Spearman because the graded label is zero-inflated and heavily tied (most files have 0 issues, a few have 1, rarely 2+); plain τ-a / ρ are distorted by ties. The schema and the gate both read τ-b — no Spearman/Kendall split between report and pass rule.
- **Secondary endpoints (reported, not gated).** precision@k / PR-AUC against the binarized label, for `k` as in §3.6; severity-weighted τ-b. These contextualize but do not decide.
- **Baselines — including the `load_index` baseline.** Beyond the §3.5 recency and busyness baselines, the index is compared against a **`load_index`/centrality baseline**, for the reason in §3A.7. The headline number is `bug_pressure`'s **lift over the stronger of {busyness, `load_index`}**, not raw correlation. Picking the *stronger* baseline is conservative (it raises the bar), so this is baseline-hardening, not post-hoc baseline-shopping.
- **Margins are defined for the metrics actually used.** §3.7's margins (`+0.05` ROC-AUC, `1.20×` PR-AUC) are not defined for τ-b or precision@k, so this section states its own (tunable, versioned in the validation config exactly like §3.7):
  - τ-b: index τ-b **lower CI bound** (§3A.5) ≥ `τ_corr` (default `0.30`) **and** ≥ best-baseline τ-b **+ `τ_margin`** (default additive `+0.10`).
  - precision@k: index precision@k **lower CI bound** ≥ `pk_mult` × best-baseline precision@k (default multiplicative `1.20×`, mirroring §3.7's PR-AUC form).

All four threshold values (`τ_corr`, `τ_margin`, `pk_mult`, and the §3A.5 floors) feed the report fingerprint, so any future tightening is itself versioned and auditable.

### 3A.5 Uncertainty and the statistical floor (the n problem)

The issue corpus is small and sparse (§3A.13): per-file counts are low and `n_post_T_positives` can be in the low tens or single digits. A point estimate at that n is inside its own noise band, so **no pass/fail is emitted from a point estimate.**

- **Confidence intervals on every gated statistic.** τ-b and precision@k carry a **bootstrap CI over files** (resample the scored population); the **gate reads the lower CI bound**, never the point estimate (§3A.4). A point estimate that clears a threshold but whose lower bound does not → **not a pass**.
- **A null model for τ-b.** Significance against a **label-permutation null** (shuffle the issue label across the eligible population, recompute τ-b, repeat) is reported alongside the CI. A τ-b that is not distinguishable from the permutation null is reported as such regardless of its point value.
- **A numeric floor on the predictive positive set.** `n_post_T_positives < N_min_issue_positives` (config default `15`) → the repo's verdict is **`untested`** (§3A.9), mirroring §4's `N_min` and the zero-fix-commit refusal. This is the operational form of §3A.13's "treat a thin corpus as untested" — it is a number, not a judgment call. Note the floor is on the **post-`T` positive count**, not the total issue-file count: a repo with 40 lifetime issue-files but 6 post-`T` positives is below the floor.

### 3A.6 Pass criteria

Proposed pass criteria (tunable, versioned like §3.7). A predictive-mode corroboration run **corroborates** a signal iff, on **≥2 reference repos**:

1. `n_post_T_positives ≥ N_min_issue_positives` (§3A.5) on that repo — else that repo is `untested`, not a pass or fail, **and**
2. τ-b clears both the absolute floor and the baseline margin **on its lower CI bound** (§3A.4), **and**
3. precision@k clears the baseline multiplier **on its lower CI bound** (§3A.4), **and**
4. issue-file coverage (§3A.2) ≥ `0.50` on that repo — else "insufficient coverage" (§3A.9), parallel to §3.7 clause 3 and §4.

These bars are deliberately below the §3.7 holdout bars because the label is noisier; the CI-lower-bound discipline is what keeps "below the holdout bar" from collapsing into "passes on noise."

### 3A.7 The selection-bias confound, and the bounded claim it permits

The defining limitation, on the page so a reviewer can challenge it: tracked issues are produced by **running cognitive-lens agents (and human reviewers) over the code**, and those reviewers preferentially scrutinize central, important files. So issue density may correlate with centrality because that is **where people look**, not where defects are — the review-side analogue of the substrate's own busyness confound.

The `load_index` baseline (§3A.4) is the mitigation, and its reach must be stated honestly:

1. The `load_index` baseline is **mandatory, not optional** — corroboration counts only as lift *over* one measured channel of where-reviewers-look.
2. **But `load_index` is only one attention channel.** Review attention is also driven by busyness, recency, and complexity — and those signals live **inside `bug_pressure`** (§2.0, §3.5) while sitting **outside** the `load_index` baseline. The draft also concedes `bug_pressure` and `load_index` are themselves correlated. So lift over `load_index` removes centrality-driven attention but **not** churn- or complexity-driven attention.
3. **Therefore the claim is narrowed to what the baseline can support.** A positive predictive-mode result reads as:

   > **"`bug_pressure` adds ranking signal for tracked-issue location beyond busyness and centrality."**

   It does **not**, on the strength of a `load_index` baseline alone, read as "beyond review-attention" — that stronger claim requires controlling the **full attention surface** (busyness + complexity + recency jointly, or an externally measured attention signal such as PR-review file coverage or reviewer file-open telemetry). Controlling the full surface, or using a defect label drawn from outside the lens family entirely (incident post-mortems, CVE/advisory attributions), is **deferred** — the documented path to the stronger claim, on the same "promote it when earned" discipline. The §6.2 report must state results in the narrowed terms.

### 3A.8 The divergence criterion

"Divergence" is the section's headline contribution, so it is defined operationally rather than left to the schema field. Divergence between §3 and §3A is computed at **two levels**, and the schema records both:

- **Verdict-level (the gating definition).** A signal **diverges** when its §3 holdout verdict and its §3A predictive-mode corroboration verdict disagree on the same reference set — specifically when §3 confers `validated` but §3A returns `contested` (failed §3A.6) on **≥1 reference repo where the run was not `untested`/`insufficient-coverage`**, or the symmetric case. `divergence_with_holdout` (§3A.14) is set from this rule. Divergence **does not change `validation_status`** (§3A.1) — it raises a flag and a report entry.
- **Metric-level (early-warning, reported-only).** Per reference repo, a **sign disagreement** in rank correlation (holdout fix-label τ-b and issue-label τ-b point in opposite directions) or a precision@k gap beyond `divergence_margin` (config default `0.20`) is recorded as a metric-level divergence even when the verdict-level rule does not trip. This surfaces a brewing disagreement before it flips a verdict.

A run with both labels `untested` on a repo produces **no** divergence claim for that repo (you cannot disagree from two non-results).

### 3A.9 Degenerate cases — never silently pass

The protocol refuses to run rather than fabricate a verdict when (parallel to §4):

- **Zero eligible issues** — every issue on the repo is user-submitted, `false-positive`, `observation`, untriaged, or `file_path: null`. No positives, nothing to rank against; τ-b and precision@k are undefined → **`untested`** with reason `no_eligible_issues`.
- **Below the positive-set floor** — `n_post_T_positives < N_min_issue_positives` (§3A.5) → **`untested`** with reason `thin_corpus`.
- **Insufficient coverage** — issue-file coverage `< 0.50` on a reference repo → that repo's outcome is **`insufficient_coverage`** (§3A.6 clause 4); if true on *every* reference repo, the signal's corroboration outcome is `insufficient_coverage` overall.
- **Unpinned snapshot** — the issue snapshot is not frozen to a recorded as-of and id set (§3A.11) → the run is **refused** (not `untested`): a non-deterministic corroboration is not allowed to emit any verdict.

In all `untested`/`insufficient_coverage` cases the affected signal ships the outcome with an explicit reason and is **never rendered as corroborated** anywhere downstream.

### 3A.10 Corroboration outcomes — the verdict vocabulary

A §3A run emits a **corroboration outcome**, which is **not** a `validation_status` (the §3.8 set is unchanged) and must be enumerable so a consumer can distinguish "ran and disagreed" from "could not run":

- **`corroborated`** — predictive-mode run met §3A.6 on the reference set; agrees with the holdout.
- **`contested`** — predictive-mode run ran and **failed** §3A.6 on ≥1 non-degenerate reference repo. Pairs with `divergence_with_holdout: true` when §3 conferred `validated`. **Does not revoke `validated`** (§3A.1).
- **`insufficient_coverage`** — coverage `< 0.50` (§3A.9).
- **`untested`** — could not run (§3A.9: `no_eligible_issues`, `thin_corpus`, or concurrent-only data with no post-`T` positives).

The per-repo and overall outcomes both use this enum; the schema field is the enum string, **not** a boolean (a boolean cannot encode `insufficient_coverage`/`untested`, which would silently collapse "could not run" into "failed").

### 3A.11 Determinism and the issue snapshot

The verdict is a pure function of `(substrate at T, issue snapshot, validation config)`. Unlike git history, the **issue set drifts** — issues are added, resolved, and **re-triaged in place** — so a corroboration run **pins its snapshot**:

- It records the as-of timestamp and the set of contributing run/issue ids, **and hashes the snapshot *content*** — each contributing issue's `file_path`, triaged status, `firstSeenRunId`, and `failureSeverityCode` — into a `corroboration_fingerprint`. Hashing **content, not just ids**, is deliberate: an issue re-triaged in place (path edited, flipped to/from `false-positive`) changes the content hash even though its id is unchanged, so a verdict that moves because of a retroactive edit is always attributable. Hashing ids alone would let a re-triage silently change the verdict under a stable fingerprint — the exact failure this section exists to prevent.
- Re-running against the same pinned snapshot is byte-identical; a changed snapshot is a fingerprint change, mirroring `config_fingerprint` (`repo-substrate-spec.md` §3).

### 3A.12 Tooling

Parallel to §7. The issue snapshot is produced by a **named, recorded extraction** so two implementers fetch the same input:

- **Source.** The tracked-issue store of record (the validation platform's issue tracker / MCP). The validation config records the **tracker identifier, the project set, and the exact query** (the eligibility predicate of §3A.2 expressed as a filter: non-null `file_path`, triaged-defect status, agent-discovered, `firstSeenRunId` relative to `T`).
- **As-of mechanism.** The snapshot is taken at a recorded wall-clock as-of and the contributing ids are frozen (§3A.11); the extraction is **read-only** and re-runnable against the same as-of to reproduce the id+content set.
- **Stack.** Same as `repo-substrate` (Python 3.11+); reuses its `--truncate-at <split-sha>` mode for the index side and adds an issue-snapshot fetch + path-normalization step for the label side. No new extraction engine.

### 3A.13 Limits and open questions (on the page)

#### 3A.13.0 Blocking precondition — error-source independence (review this first)

The corroboration's entire value rests on the issue label being **derived separately** from the git label, not merely **expressed in a different modality**. There is a path by which that fails *one level beneath* the shared-prior limitation below: **if any issue-logging agent used git-derived signals — churn, recency, co-change — to decide *where to look*, then issue density is a downstream transform of the same git data the index is built on**, and agreement with `bug_pressure` is autocorrelation wearing review's clothing. The divergence flag would then never fire when it should.

This is **not** resolvable from the spec. It is a factual question for the **cognitive-lens agent owner**: *what inputs do the issue-logging agents consume to prioritize files?* Until answered:

- The word "independent" in this section means **modality-independent only**, not error-source-independent.
- A `corroborated` outcome is reported as **provisional on this precondition**.
- Co-equal-falsifier promotion (§3A.1) is blocked on a negative answer (agents do **not** consume git-derived targeting signals).

#### 3A.13.1 Other limits

- **"Closer to defect origin" is a claim, not a given.** This section does not assert the issue label sits nearer the defect than a fix-edit. A reviewer flags where a *symptom* surfaces, which carries the same caller/callee, test/code displacement §3.4.1 owns for fix-edits — it may be nearer or farther. The corroboration's value does **not** depend on the issue label being nearer; it depends on it being **separately derived** (§3A.13.0). Any "nearer-to-origin" benefit is upside, not a premise.
- **Same-org corpus.** The available issue corpus is all one org (the registry and mcp projects). A different *modality* (review vs git), **not** a different org, so it does **not** discharge the cross-org generalization question (§8.1). It narrows that gap; it does not close it.
- **Sparsity.** Most issues carry `timesSeen: 1` and per-file counts are low. The §3A.5 floor + CI discipline are the response; report the issue-file `n` and `n_post_T_positives` on every run.
- **Agent-produced label / shared prior.** If the same family of lenses that logged the issues also shaped the index design, the corroboration inherits a shared prior (the Hume habit objection, one layer up). Mitigate by drawing issues from agents/projects **not involved in tuning the indices** — separation of *operators*. Note this separates operators, **not** the lens family's defect concept; a fuller break uses labels from outside the lens family (incident post-mortems, CVEs), per §3A.7.
- **Two proxies, shared salience tilt.** §3's fix-edit label and §3A's issue label both tilt toward central/busy files, so "agreement strengthens" is partly the shared confound, not two independent confirmations. This is why agreement only *strengthens confidence* and never *confers status* (§3A.1).
- **Contests, does not falsify.** The holdout falsifies; this contests or strengthens. Treat a §3-vs-§3A divergence (§3A.8) as a finding to investigate, not an average to take.

#### 3A.13.2 New open questions (also listed in §8)

- The reference-issue-corpus: which projects, how the snapshot is frozen, the separation-of-duties rule (§3A.13.1), and the §3A.13.0 precondition.
- Calibration of `N_min_issue_positives`, `τ_corr`, `τ_margin`, `pk_mult`, and `divergence_margin` once real corroboration numbers exist (parallel to §8.2).
- Whether to retain pre-HEAD-deletion issues as positives in a variant (parallel to §8.4 survivorship).

### 3A.14 Schema and report

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

**Holdout report (§6.2).** Adds the "Cross-source corroboration" section described in §6.2.

## 4. Degenerate cases (never silently "pass")

The protocol must refuse to run rather than fabricate a verdict when:

- `population_size < N_min` (substrate §6.1) — the repo is too small to split meaningfully.
- The holdout window contains **zero** `fix`-type commits — no positives, nothing to predict; AUC is undefined.
- Eligible coverage `< 0.50` on every reference repo — the partition is dominated by holdout-born files.
- The best baseline's PR-AUC is below `signal_floor_mult` × the base rate on a repo (§3.7 clause 4) — the label is too close to noise to distinguish rankers; that repo is `insufficient signal`. If true on every reference repo, the index is `untested` with reason `insufficient_signal`.

In all four, affected indices ship with `validation_status: "untested"` and an explicit reason. **`untested` is never rendered as validated** anywhere downstream. A repo that cannot be validated does not get to claim its diagnosis is empirically grounded.

The corroboration test has its own parallel refuse-to-run list (§3A.9) — zero eligible issues, below the positive-set floor, insufficient coverage, unpinned snapshot — emitting the §3A.10 corroboration-outcome vocabulary rather than a `validation_status`. The same discipline holds across both: a test that cannot run never reports as if it passed.

## 5. Consequence — the anti-horoscope gate

This is the link that makes the whole architecture honest, enforced in C3 (`structural-mapper-spec.md` §3):

> **No *signal* — composite index, percentile, or raw metric — may feed a *named structural feature* unless its `validation_status` is `validated` or `asserted`, OR the mapping rule is explicitly tagged `decorative: true`.**

- The gate is **signal-level, not index-level.** This is deliberate: scoping it to indices would leave the default percentile predicate strategy (§2.2) ungated, and a fully diagnostic feature could be written in percentiles alone to slip the gate. Every signal in a feature's predicate is checked.
- An `unvalidated` or `untested` signal feeding a feature with no `decorative` tag is a **hard error** in C3's ruleset validation.
- **A `kind`/`status` mismatch is rejected before the gate even runs** (§3.8): a `kind: predictive` signal carrying `status: asserted` is malformed input, not a passing signal. This closes the relabel path — a predictive index that failed the holdout cannot re-enter as a description.
- A `decorative` feature renders with an "unvalidated" visual marker and is **excluded from diagnostic claims** in the C5 brief.
- **A `contested`/`divergence` corroboration (§3A) does not touch the gate.** Corroboration emits a separate outcome (§3A.10), never a `validation_status`, so a contested or divergent result leaves a signal's `validated` status — and therefore what the gate admits — unchanged. The divergence is a report-level finding (§3A.8, §6.2), not a gate input.
- The provenance chain therefore extends: `brief-claim → feature → predicate → signal → validation_status → holdout report`. "Why is this file a toothpick, and should I believe it?" resolves all the way down to a precision@k number on a named reference repo (for `validated` signals) or to a named, recorded intuition/stability justification (for `asserted` ones).

## 6. Outputs

### 6.1 `validation.json` (schema)

This is the interface the C3 anti-horoscope gate reads (`structural-mapper-spec.md` §3). The gate's lookup path is fixed: `validation.signals[<signal-name>].status`. Signals are **keyed by signal name** — the exact identifier used in `substrate.json` `derived` (an index name like `bug_pressure_index`, a percentile name like `fan_in_nonzero`, or a raw metric name). Every signal any ruleset references must have an entry; a missing key is treated as `untested`.

```json
{
  "schema_version": "0.1",
  "validation_version": "0.1.0",
  "validated_at": "<ISO8601, excluded from fingerprint>",
  "substrate_config_fingerprint": "<the config — incl. index weights — these verdicts validate>",
  "validation_config_fingerprint": "<sha256 of thresholds (§3.7) + reference-repo set>",
  "reference_repos": [
    { "name": "uluops-registry", "head_sha": "…", "split_sha": "…", "coverage": 0.72, "holdout_positives": 41 }
  ],
  "signals": {
    "bug_pressure_index": {
      "status": "validated",
      "kind": "predictive",
      "holdout": {
        "roc_auc": 0.78, "pr_auc": 0.41,
        "precision_at_k": { "10": 0.70, "20": 0.60, "p05": 0.55 },
        "recall_at_k":    { "10": 0.30, "20": 0.45, "p05": 0.50 },
        "baselines": {
          "recency":  { "roc_auc": 0.66, "pr_auc": 0.30 },
          "busyness": { "roc_auc": 0.71, "pr_auc": 0.33 }
        },
        "per_repo": [ { "name": "uluops-registry", "roc_auc": 0.80, "pr_auc": 0.43, "passed": true } ]
      }
    },
    "change_pressure_index": {
      "status": "unvalidated",
      "kind": "predictive",
      "holdout": {
        "roc_auc": 0.69, "pr_auc": 0.31,
        "precision_at_k": { "10": 0.40, "20": 0.40, "p05": 0.38 },
        "recall_at_k":    { "10": 0.17, "20": 0.30, "p05": 0.35 },
        "baselines": {
          "recency":  { "roc_auc": 0.66, "pr_auc": 0.30 },
          "busyness": { "roc_auc": 0.71, "pr_auc": 0.33 }
        },
        "per_repo": [
          { "name": "uluops-registry", "roc_auc": 0.69, "pr_auc": 0.31, "passed": false,
            "failed_clauses": ["roc_margin", "pr_auc_mult"], "best_baseline": "busyness" }
        ]
      }
    },
    "load_index": {
      "status": "asserted",
      "kind": "descriptive",
      "grounding": {
        "stability":   { "k": 5, "eps": 0.05, "delta": 0.15, "median_abs_delta": 0.02, "max_abs_delta": 0.09, "passed": true },
        "cross_modal": { "counterpart": "cochange_degree", "tau_b": 0.41, "tau_b_ci": [0.34, 0.48], "tau_floor": 0.30, "passed": true },
        "recognition": { "ref": "blind/uluops-registry-api.md", "sealed_sha": "…", "list": "load_bearing", "tau_b_top10": 0.33, "n": 1 },
        "repos_passed": ["uluops-registry-api", "mcp-secure-server"]
      }
    },
    "reinforcement_index": {
      "status": "untested",
      "kind": "descriptive",
      "reason": "no_counterpart",
      "grounding": {
        "stability":   { "k": 5, "eps": 0.05, "delta": 0.15, "median_abs_delta": 0.00, "max_abs_delta": 0.00, "passed": true },
        "cross_modal": { "counterpart": "line_coverage", "passed": null, "note": "no coverage report present in either reference repo" }
      }
    }
  }
}
```

- `status` ∈ {`validated`, `unvalidated`, `asserted`, `untested`} (§3.8). `kind` ∈ {`predictive`, `descriptive`} — records which basis the signal rests on (§2), so C3/C5 read the right register without re-deriving it. An `untested` entry carries a `reason` (`unstable`, `cross_modal_fail`, `no_counterpart`, `population_too_small`, `no_holdout_positives`, `insufficient_coverage`, `insufficient_signal`).
- **Predictive** signals carry a `holdout` block (the §3.6 metrics + §3.5 baselines + per-repo pass/fail with the failed clauses named). **Descriptive** signals carry a `grounding` block — the §2.4.1 `stability` result, the §2.4.2 `cross_modal` result, and the §2.4.3 `recognition` comparison — instead; never a `holdout` block.
- **Predictive** signals MAY *additionally* carry an `issue_corroboration` block (§3A.14) beside — never instead of — the `holdout` block. It records the §3A corroboration outcome, is keyed by the same signal name, and never alters the signal's `status`/`kind`. Its `outcome` enum (§3A.10) is distinct from `validation_status`.
- `validated_at` is excluded from both fingerprints so re-runs are byte-identical (mirrors substrate `extracted_at`).

### 6.2 The holdout report (human-readable)

Per the substrate's standing mandate, it **writes down where the indices lie**. Fixed section structure (parallel to the substrate report §9):
1. **Verdict table** — each predictive signal: status, ROC-AUC / PR-AUC vs. the stronger baseline, on each reference repo.
2. **Where it failed** — for every `unvalidated` signal: by how much, on which repo, against which baseline.
3. **Coverage caveats** — eligible-population coverage per repo (§3.3), and any `untested` signals with their reason (§4).
4. **Descriptive signals** — each descriptive signal with its stability numbers, its cross-modal τ-b and CI against the named counterpart, the recognition comparison against the sealed ranking, and the resulting status; plus the τ distribution across repos so the §2.4 known limit (a counterpart that cannot fail) is visible.
5. **Cross-source corroboration** (§3A) — per predictive signal: the corroboration `outcome` (§3A.10), τ-b with CI and permutation-p, lift over the `load_index` and busyness baselines (lower CI bound), coverage, `n_post_T_positives`, and **any divergence from the §3 verdict** (§3A.8). Results are stated in the §3A.7 narrowed terms ("adds ranking signal beyond busyness and centrality"), with the §3A.13.0 independence precondition status shown.

Those lies (section 2) are the documented input to the C3 spec's feature design.

## 7. Tooling & determinism

- Same stack as `repo-substrate` (Python 3.11+); reuses its pipeline with a `--truncate-at <split-sha>` mode rather than reimplementing extraction.
- The verdict is a pure function of `(reference repos at their SHAs, substrate config incl. weights, validation config incl. thresholds)`. Re-running reproduces the verdict byte-for-byte. Changing weights or thresholds changes the fingerprint — so "why did `bug_pressure_index` pass last month and fail now" always resolves to a weight diff, a threshold diff, or a new commit, never to nondeterminism.

## 8. Open questions

1. **Reference-repo set.** Two (Registry, mcp-secure-server) for v0. How many, and how diverse, before a `validated` verdict generalizes beyond them? Corpus calibration (system spec Phase 3) eventually subsumes this.
2. **Threshold defaults.** `+0.05` AUC and `1.20×` PR-AUC are first guesses. Tune once real holdout numbers exist — and record the tuning as a config diff.
3. **`fix` label fidelity.** The label inherits every limitation of substrate §7 classification (subject-only, squashed commits get one label). A mislabeled history weakens both the index and the test symmetrically; quantify how much.
4. **Survivorship.** Excluding deleted files (§3.3) drops files that were so bad they were removed — arguably the strongest positives. Consider a variant that labels "deleted in holdout after a fix" as positive.
5. **Corroboration independence precondition (blocking, §3A.13.0).** Does any issue-logging cognitive-lens agent use git-derived signals (churn, recency, co-change) to prioritize which files to examine? A positive answer collapses the §3A label's independence into autocorrelation with `bug_pressure`. This is a factual question for the cognitive-lens agent owner and **blocks** promotion of §3A to a co-equal falsifier until resolved.
6. **Corroboration reference-issue corpus (§3A.13.2).** Which projects supply issues, how the snapshot is frozen (§3A.11–§3A.12), and the separation-of-duties rule that keeps label-producing agents distinct from index-tuning agents (§3A.13.1).
7. **Corroboration threshold defaults.** `N_min_issue_positives` (15), `τ_corr` (0.30), `τ_margin` (+0.10), `pk_mult` (1.20×), and `divergence_margin` (0.20) are first guesses; tune once real corroboration numbers exist, recording each as a config diff (parallel to #2).
8. **Asserted-bar defaults (§2.4).** `stability_perturbation_k` (5), `stability_eps` (0.05), `stability_delta` (0.15), `tau_asserted` (0.30), `M_asserted` (2), and `signal_floor_mult` (1.5) are placeholders accepted under D-004 Q4; tune after the first real run.
9. **Cross-modal independence.** Whether `cochange_degree` and import topology are independent enough on real repos for §2.4.2 to be a falsifier. Answered by the τ distribution in the first holdout report; if it cannot fail, a third modality is required.
10. **Reference-repo set (revised).** Two same-org repos is near n=1 (tribunal A5). D-005 adds two public JS/TS repos; the chosen repos and their SHAs are recorded in `reference_repos` and in `DECISIONS.md` once cloned and sized.
