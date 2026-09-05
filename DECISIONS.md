# Decision log — codebase-as-structure

*Append-only. Each entry records a decision, the reasoning at the time, the assumptions it rests on, and what breaks if those assumptions change. Entries are never edited after the fact; a reversal is a new entry that cites the old one. This is the stratum a future reader digs through to learn why the artifact is shaped the way it is.*

*Format: `D-NNN · date · title` / Decision / Why / Assumes / Breaks if / Supersedes.*

---

## D-001 · 2026-09-04 · Claude runs point; Alex steps in for guidance, questions, and audit pipelines

**Decision.** Claude makes the core product decisions (features added, removed, modified; scope; sequencing; tooling) and executes. Alex provides occasional guidance, answers questions, and proposes audit pipelines. Decisions are logged here before or alongside the work they govern.

**Why.** Alex proposed it as an experiment in how far the project can be taken under delegated ownership. The project had stalled for eleven weeks on a single unsigned proposal; the cost of waiting exceeded the cost of a wrong call that can be reversed.

**Assumes.** Every decision is reversible by a later entry; nothing outward-facing (publishing, pushing to a remote, external services) is done without Alex's explicit go.

**Breaks if.** Alex wants decision rights back — he says so and this entry is superseded.

## D-002 · 2026-09-04 · Repository initialized; the June 20 corpus is the baseline commit

**Decision.** The project directory becomes a git repo. The first commit is the spec corpus exactly as found on 2026-09-04 (last modified 2026-06-20), including the tribunal report and the unsigned proposal.

**Why.** A project whose subject is git history was not itself under version control. Every later decision needs a diffable baseline to be attributable.

## D-003 · 2026-09-04 · "Completion" is defined in three milestones; M1 is the product

**Decision.**
- **M1 — repo-substrate, validated.** The C1 CLI emits `substrate.json` and the markdown report; the validation gate runs the temporal holdout on the reference set and emits `validation.json` and the holdout report; the C1, validation, and integration checklists are green. This is the standalone product the substrate spec already claims must be valuable even if the renderer never ships.
- **M2 — the diagnosis.** C3 built as a minimal authored ruleset with the anti-horoscope gate enforced, producing `skeleton.json`, plus a deterministic 2D cutaway render (C6) with C4 folded into it. No LLM in the path.
- **M3 — the narrative.** C5 architect brief under the adversarial lens, with the register lint. Optional; built only if M2 proves the skeleton is worth narrating.

**Why.** The system spec's six components span from a deterministic extractor to a diffusion renderer. Treating all six as one deliverable is how the project stalled. M1 is where every falsifiable claim lives; M2 is where the thesis (metaphor as faithful function of signal) gets its first real test; M3 is decoration until M2 exists.

**Assumes.** The substrate spec §1 framing — the substrate is the product — still holds.

**Breaks if.** Alex wants the render first. Then M2's cutaway gets pulled forward against unvalidated signals, which the anti-horoscope contract forbids; that would need a `decorative`-only render mode as a new decision.

## D-004 · 2026-09-04 · The asserted-tier proposal: adopted with one substitution

Resolves the four questions the June 19 proposal left open. Referenced by the tribunal as remediation items #5, #6, #9.

**Q1 — Walk back the parity claim.** *Adopted as proposed.* Keep "different kind," drop "not a weaker one / neither subsumes." The min-over-signals operator in the mapper stays; it was right. The six places in the live specs that assert parity are rewritten.

**Q2 — Blind pre-registered recognition as the `asserted` correctness bar.** *Adopted in principle, protocol substituted.* The proposal requires three or more developers who know the repo to rank files blind, on two or more repos. UluOps has one developer. As written, 2b cannot run, and a correctness gate that cannot run is `untested` forever, which makes the whole `asserted` tier unreachable. The substitute keeps what 2b was for (a falsifier a constant cannot pass, produced without seeing the metric's output) and drops the panel:

  - **2b′ — cross-modal corroboration of the description.** A descriptive signal earns its correctness half by rank-correlating (Kendall τ-b, lower CI bound ≥ a config floor, default `0.30`) with a measurement of the *same present-tense property* from a *different modality that is not in its formula*. For `load_index` (static import topology) the second modality is co-change coupling from history (`cochange_degree`, substrate §5.2 Tier 2, promoted to Tier 1 by this decision). For `neglect_index` it is blame-age of surviving lines. For `reinforcement_index` it is coverage data when present, else `untested`. For `complexity_proxy_index` it is real cyclomatic complexity on the languages where a parser is cheap. This is the §3A pattern (a second, separately-derived label) applied one tier down. It can return negative.
  - **2b″ — recorded n=1 blind ranking.** Alex produces a blind top-10 "load-bearing" and top-10 "I distrust this file" list per reference repo *before* seeing any substrate output; it is sealed (committed by hash before the run). It is reported as a recognition check, not gated, because n=1 cannot carry a gate.
  - Stability (2a) stays exactly as proposed and remains mandatory. `asserted` ≝ 2a ∧ 2b′.

**Q3 — Feature-name leak.** *Disclosure plus lint now; position-names in the C3 ontology.* The C5 brief must state that a name denotes structural position, not a breakage forecast, until `blast_radius_index` is validated. A deterministic post-hoc lint over the brief flags consequence vocabulary sourced from `asserted` signals. The C3 ontology prefers position names ("hub", "junction") where the consequence name adds nothing.

**Q4 — Numbers.** *Placeholders accepted* (ε=0.05, δ=0.15, K=5, τ≥0.30 for 2b′, M≥2). Tuned after the first real holdout, recorded as config diffs.

**Why the substitution.** The tribunal's deepest point was that recognition is confirmation-biased by construction. A human panel fixes the bias but is unavailable. A second modality that was not in the formula fixes the bias *and* is available. It is weaker than a panel in one way (both modalities are machine-derived from the same repo) and stronger in another (it is reproducible and cannot be flattered).

**Assumes.** `cochange_degree` is computable from the history miner without a new extraction engine (it is: pairwise co-occurrence over `nodes_touched`).

**Breaks if.** Co-change and import topology turn out to be so correlated on every repo that 2b′ cannot fail. Then it is not a falsifier and needs a third modality. The first holdout report will show the τ distribution and answer this.

**Supersedes.** The parity wording in validation §1, §2.1, §3.8; substrate §10; system §3; mapper §3.

## D-005 · 2026-09-04 · Scope cuts for M1

- **C2 (Narrative Reader) removed from v0 entirely**, not merely optional. Nothing in M1 or M2 reads `signal.json`. Mapper open question #4 closes as "no C2 coupling in v0."
- **C4 folds into C6.** For the 2D cutaway, massing is vertical strata plus feature placement; a separate `massing.json` artifact is ceremony. System open question #1 closes.
- **§3A corroboration stays specced but is not built in M1.** It is secondary by design, blocked on the independence precondition, and depends on a tracker corpus. Built after the holdout runs and only if the holdout leaves a `validated` signal for it to corroborate.
- **Reference set grows from two to four repos.** The two UluOps repos (registry-api, mcp-secure-server) are same-org, which the tribunal flagged as near n=1 generalization. Two public JS/TS repos with real fix history are added. Candidates chosen in a later entry once cloned and sized.

## D-006 · 2026-09-04 · Dependency extractor backend: dependency-cruiser, pinned

**Decision.** The v0 JS/TS `DependencyExtractor` shells out to `dependency-cruiser` (pinned exact version, recorded in `toolchain_versions`) and consumes its JSON output. The substrate owns the edge contract (self-loops dropped, duplicates collapsed, external vs unresolved split) over that output.

**Why.** It resolves `tsconfig` path aliases and reports unresolved modules distinctly from external packages, which is exactly the split substrate §6.3 needs and is the one piece a hand-rolled resolver would get wrong first. `tree-sitter` gives a parse, not a resolution; `madge` conflates unresolved with external. Cost: a Node toolchain dependency inside a Python project. Accepted, because the tool version is inside the fingerprint by construction.

**Assumes.** dependency-cruiser's output is deterministic for a fixed version and config. Verified by golden test before trust.

**Breaks if.** Alias-heavy repos produce confident mis-resolution (substrate open question #8). The spot-validation planned there is the check.

## D-007 · 2026-09-04 · Tracker reconciliation before building

**Decision.** The tracker project carries 50 open issues; roughly a dozen were resolved in the specs on June 19–20 without being closed. Each is closed with a note citing the spec section that resolved it before any new issues are logged. The tracker is the work queue only once it is true.

## D-008 · 2026-09-04 · Grounding classes for descriptive signals; the load family gets a second instrument, not a second modality

**Context.** The first run of the gate on `mcp-secure-server` and `uluops-registry-api` returned: `age_days` ↔ `blame_age_median` τ 0.77 / 0.78 (a genuine cross-modal confirmation); `neglect_index` ↔ blame τ 0.43 / 0.65; but the load family ↔ `cochange_degree` τ 0.24 / 0.44 with lower CI bounds below the 0.30 floor on the smaller repo, and `last_touched_days` ↔ blame τ 0.23 / 0.34. Several stability failures traced to the protocol counting files the removed commits had directly edited.

**Decision.**
1. **Stability compares only nodes untouched by the K removed commits.** A file edited in those commits has its recency, churn, and co-change legitimately move; that is the signal reporting the edit. The budget measures whether editing *other* files moves *this* file's value. `p95` is reported beside `max`.
2. **Descriptive signals are grounded by class**, recorded in `validation.json` as `grounding_class`:
   - **G1 measurement** — direct git or file facts (`commit_count`, `churn_lines`, `fix_count`, `revert_count`, `author_count`, `last_touched_days`, `size_loc`, `nesting_proxy`, `cochange_degree`, `blame_age_median`). Bar: stability. The instrument is git or the file; the metric's name is literal, so no meaning rides on the label. Popper's constant objection targets models, not measurements.
   - **G2 instrument-checked** — resolver-dependent facts checked against an independent second instrument measuring the *same property*: `fan_in`, `fan_in_nonzero`, `fan_out` ↔ `fan_in_alt` / `fan_out_alt` from a regex scanner with its own resolver (`altdeps.py`, no shared code with dependency-cruiser); `has_sibling_test` ↔ `test_fan_in` (importers that are test files). Bar: stability + τ-b lower CI ≥ `tau_instrument` = 0.60, set now, before the numbers are seen. Same property measured twice should agree strongly; a low τ means the instruments disagree on alias-heavy or dynamic-import code, which is substrate open question #8 made measurable.
   - **G3 cross-modal** — a different modality of the same property: `age_days`, `neglect_index` ↔ `blame_age_median`. Bar: stability + τ-b lower CI ≥ `tau_asserted` = 0.30.
   - **G4 derived** — fixed-weight blends and graph functions of asserted inputs: `centrality` (from `fan_in`), `load_index`, `complexity_proxy_index`, `reinforcement_index`. Bar: stability + every input asserted. The composite's name carries no claim beyond its inputs (D-004 Q3 handles the name); `cochange_degree` and `test_fan_in` are computed and **reported as correlates**, never gated.
3. `last_touched_days` moves from G3 to G1. Blame age measures how old the surviving text is; last-touched measures when the file was last edited. They are different properties, and the low τ was the counterpart being wrong, not the signal.

**Why.** D-004 asked for a counterpart "not in the formula" and named co-change for load. The run showed co-change is *change* coupling, and a foundation is precisely the file that is imported by many and changed by few, so the pairing was conceptually mismatched, not merely under-correlated. There is no independent measurement of "load-bearing" in v0 beyond the import graph; pretending otherwise would be the horoscope move in reverse. The honest position is that `load_index` is a named blend of independently checked measurements and claims nothing more. Lowering the τ floor until co-change passed was the deadline bypass the tribunal warned about and was not considered.

**Assumes.** The second scanner is genuinely independent (it is: separate module, no shared resolution code) and that τ ≥ 0.60 is the right agreement bar for two instruments on one property. Both are checked by the τ distribution in the report.

**Breaks if.** G4 is read as a loophole — a ruleset naming `load_index ≥ p90` "foundation" and C5 voicing "if this breaks, much falls." That is forbidden by §2.1.1 and D-004 Q3 regardless of G4; the register lint (M3) is the enforcement. **Flagged for audit**: this is the decision most worth a lens pass.

## D-009 · 2026-09-04 · Weight tuning is pre-registered: tune on two repos, verdict from the other two

**Context.** Both predictive indices failed the holdout on both small repos. `bug_pressure_index` ranked *below* the recency and busyness baselines (ROC −0.21 and −0.04). `change_pressure_index` beat the best baseline on ROC by +0.03 and +0.05 against a +0.05 margin, and on PR-AUC by ×1.69 and ×1.00 against ×1.20; it is, by construction, a blend of the two baselines and so cannot easily beat them by margin.

**Decision.** The §6.2.1 weights are tuned once, under this protocol, before any test-set number is seen:
- **Tuning set:** `uluops-registry-api` (956 commits, 132 holdout positives) and `eslint` (11,008 commits). One internal, one external, both with hundreds of positives.
- **Test set:** `typeorm` and `mcp-secure-server`. The `validated` verdict is computed **only** from the test set; tuning-set passes are reported but do not count. `min_repos` = 2 therefore means both test repos must pass.
- **Search:** a grid at 0.1 steps over each index's inputs (weights summing to 1), inputs for `bug_pressure_index` widened to {`fix_count` pctile, `fix_count_nonzero`, `revert_count`, `fix_ratio`, recency, `commit_count` pctile}. Objective: the **minimum** over tuning repos of (index ROC-AUC − best-baseline ROC-AUC), tie-broken by the minimum PR-AUC ratio. The minimum, not the mean, so one repo cannot carry the other.
- **Frozen** into `config/tuned.toml` and committed before the test set is run. The commit hash of the frozen config is recorded in the holdout report.
- The pass margins (+0.05, ×1.20) are **not** tuned. The interaction between the multiplicative PR margin and high base rates is noted in the report as a limitation, not adjusted away.

**Why.** The spec always said the weights are placeholders tuned against the holdout, held out not in sample. Tuning without pre-registration is the researcher-degrees-of-freedom leak the corroboration section already closes for its own thresholds; the same discipline applies here.

**Breaks if.** The tuned indices still fail the test set. Then the finding ships as `unvalidated`, the report says by how much, and C3 may not name a feature over either index. That outcome is acceptable; hiding it is not.

## D-010 · 2026-09-04 · The sealed recognition rankings are model-assisted priors, accepted as the n=1 substitute

**Context.** Alex had a separate Claude (Fable 5.1) session fill `blind/uluops-registry-api.md` and `blind/mcp-secure-server.md` from its session memory of those repos plus `git ls-files` (to make paths valid), and reviewed and endorsed the result. Each file states its own provenance: no `git log`, no `git blame`, no import tracing, no file contents, and no substrate output read. Substrate reports for both repos existed on disk in `out/` at the time; the provenance statements say they were not read, and the rankings contain items (`CHANGELOG.md`, `package.json`) that the substrate does not even emit, which is consistent with that.

**Decision.** Accept both files as the §2.4.3 recognition record, sealed at this commit, with the provenance carried into the holdout report verbatim: "n = 1, model-assisted, maintainer-endorsed." They remain non-gating, as §2.4.3 already requires. The next repos' rankings, if any, follow the same rule: provenance stated in the file, sealed before that repo's first gate run.

**Why.** The alternative was no recognition record at all. A model's priors endorsed by the maintainer are a weaker witness than the maintainer's own blind list, and a stronger one than nothing; since the record never gates, the cost of accepting it is bounded to the report's honesty, which the provenance note preserves. Section 5 ("the one structural fact") and section 6 ("where the metrics will lie") of each file are the more valuable content: they are pre-registered predictions about where the substrate will mislead, and the report should check them.

**Breaks if.** A future ranking is produced after reading substrate output. Then it is not a recognition check and must not be sealed; the file's own provenance line is the control.

## D-011 · 2026-09-04 · What the four-repo baseline and the second instrument found; reinforcement re-grounded on the import graph

**Context.** The first full run (four repos, placeholder weights) and the first review pass (python-validator, code-auditor, test-architect, software-architecture-expert-validator, popper-validator, circumvention-forecaster; tracker runs 4–9) landed together. Findings that changed the design:

1. **The second import instrument caught the primary one on its first outing.** On typeorm, `fan_in` ↔ `fan_in_alt` was τ 0.37 against 0.84–0.98 elsewhere. Cause: dependency-cruiser drops `import type` edges unless told to analyze pre-compilation dependencies; `src/data-source/DataSource.ts` had 9 importers on the primary instrument and 621 on the scanner. For a structural map a type import is a compile-time dependency, so `--ts-pre-compilation-deps` is now on, as a fingerprinted config value. This is substrate open question #8 (extractor mis-resolution) answered by measurement rather than spot-checking.
2. **Every substrate run now carries its own instrument-agreement check.** `summary.fan_in_instrument_tau` and `graph_instruments_disagree` (floor 0.60, config) are computed at extraction, and disagreement degrades the graph exactly as a low resolution rate does. The reference-set verdict is global; this makes the G2 check local to the repo being rendered, which is where C3 needs it.
3. **Reinforcement is re-grounded on the import graph.** `has_sibling_test` (path convention) disagreed with `test_fan_in` (a test imports the file) on three of four repos; on typeorm, whose tests are named by feature, the convention is simply wrong. `reinforcement_index` is now `0` when no test imports the file, else `0.5 + 0.5 · percentile among imported files`; its G2 counterpart is `test_fan_in_alt` from the independent scanner (Popper C-2B: the earlier pairing shared the primary resolver). `has_sibling_test` stays as a G1 measurement with a literal name and a declared heuristic, and is reported as a correlate.
4. **`fan_in_nonzero` is G4 over `fan_in`** (a monotone re-ranking, not a second measurement); the June-style lookup bug that made it permanently `too_few_pairs` is fixed.
5. **G1 carries declared heuristics and a degeneracy check** (Popper C-1). `fix_count`, `revert_count`, `author_count`, `nesting_proxy`, `blame_age_median`, `has_sibling_test` state their heuristic in the grounding table and the report; any signal with fewer than 3 distinct values across the population is `degenerate`, never `asserted`. The G1 membership is pinned by test to the spec table (circumvention A5).
6. **Stability has floors** (Popper C-5): `untested` (`insufficient_stability_population`) when fewer than 30 untouched nodes are compared or more than half the population was touched by the removed commits.
7. **A retirement criterion for corroboration pairs** (Popper C-2A): a G2/G3 pair whose bootstrap lower-CI τ is ≥ 0.85 on every reference repo is flagged `non_discriminating` in the report; an adversarial fixture is then required before it counts. On this run no pair trips it: `fan_in` τ ranges 0.37–0.98, `age_days` 0.38–0.78.
8. **Recognition leaves the verdict table** (Popper C-8) and lives in its own section with its provenance and non-gating status stated.

**Assumes.** The scanner is independent enough of dependency-cruiser to be a check on it (they share a JSONC parser for `tsconfig.json` and no resolution code).

**Breaks if.** A repo's tests reach the code only through runtime string paths or a bundler alias neither instrument resolves; then `reinforcement_index` reads zero for a well-tested repo and the `graph_instruments_disagree` flag is the only warning. On such a repo the gate withholds `asserted` rather than guessing, which is the intended failure.

## D-012 · 2026-09-04 · The gate's floors are validated, its inputs attested, and its preimages published

**Context.** The circumvention forecast found that D-008/D-009/D-010 had moved the June exploits out of the specification and into configuration and operator discipline, and that the report omitted exactly the knobs an operator under deadline would turn. The code audit found five reproducible correctness bugs, two of which (rename onto a reused path; case-insensitive blob reads) corrupt values the seed and fingerprint cannot see.

**Decision.** Each is fixed in code and, where the design changed, on the page:

- **`ValidationConfig.validate()`** range-checks every floor; the spec defaults are minimums — a config may tighten a bar, never loosen it below spec (A1, A8). The report prints every floor under "Gate configuration."
- **Tuning/test roles are in the artifact** (A3; Popper C-6; the architecture validator's DIVERGENT). `run` takes `--test-repo` and `--tuning-repo`; only test-role repos count; `reference_repos[].role` and `expected_role` (from the pre-registered D-009 sets, mismatch flagged) and `tuned_config_commit` are recorded.
- **Cache integrity** (A2; audit): atomic writes, a corrupt or foreign-fingerprint entry is a miss, `truncate` is in the key, and every scored document is attested by its seed and the sha256 of its bytes in `validation.json`.
- **Preimage published** (A7): `substrate_effective_config` — the weights, regexes, and toolchain the fingerprint hashes — is embedded verbatim beside the validation config.
- **Counterpart independence is tested** (A4): `METRIC_INSTRUMENT` maps every metric to the instrument that produced it; a test asserts every G2/G3 counterpart comes from a different instrument and is not one of the signal's own formula inputs. `WEIGHT_KEY_SIGNAL` maps weight keys to signals and a test asserts G4 input lists equal the formulas (A6).
- **The holdout label is derived from a frozen validation-side regex** (`label_subject_regex`, A9), re-classifying commit subjects rather than reading the substrate's feature-side `type`. Narrowing `fix_subject_regex` cannot move a label; the report shows both and flags a difference.
- **Sealed rankings carry their git identity** (A10): committed blob, working-tree blob, first-commit hash and time are recorded per repo; a mismatch is visible.
- **The substrate report is stamped UNGATED** (A12) until C3 exists: it consults no `validation.json` and says so in its second line.
- **Audit fixes:** rename-target alias breaking (fix counts no longer land on the old lineage); blobs read by SHA via `git cat-file --batch`, not by worktree path; the split index guarded against wraparound; NaN objectives and one-class holdouts are `degenerate`, never a false FAIL or a frozen weight; a `None` index is `index_unavailable`, never a score of zero; blame failures and unreadable files are counted as instrument faults, not absences; UTF-8 pinned on every subprocess and file call; timeouts on every subprocess; the worktree temp dir cannot leak; the one unsorted output list is sorted; `pyproject` and `__version__` agree.

**Not done, logged to the tracker:** an adversarial synthetic repo for G2 (alias-heavy, dynamic imports); the edge-dropout sweep that would show whether `centrality` inherits `fan_in`'s certification; the population-drift variant of the stability check; spec §4/§6.1 schema blocks rewritten to the emitted shape; the wall-time split option removed from §3.1; checklists re-derived.

**Why.** The circumvention pass's summary is the reason: "nothing here requires expertise, because the gate's floors are literals in files the operator owns." The fingerprint was the right detector and was correctly built over config-space; it covered no bytes on disk and published no preimage. Both are now covered. What remains social is the choice of reference repos, which is pre-registered and flagged, and the honesty of a blind-ranking's provenance line, which is now cross-checked against git.

## D-013 · 2026-09-04 · Standing rules from the first review cycle; the review roster as an experiment; the name

**Context.** Alex had a Claude Desktop session read the tracker runs side by side and write `docs/notes-for-fable.md`. Three of its seven points were already in the D-012 batch; the rest are adopted here.

**Rule 1 — a decision that closes an exploit names the code that enforces it.** In the decision itself. A decision that cannot name code has not closed anything; it has moved the exploit from the specification into configuration or discipline, which is exactly what the circumvention forecast found D-008/D-009/D-010 had done. D-012 follows this rule; every later decision must.

**Rule 2 — the review roster is recorded with its rationale, so the roster choice can be scored later.** Alex delegated lens selection, which makes each review cycle a dataset: a model-chosen validator roster against a real corpus, scorable by RAH for whether the picks were the reliable agents or the relevant-sounding ones. First cycle (tracker runs 4–9, workflow `m1-review`):

| Agent | Why chosen | Decision / score | Verdict on the choice |
|---|---|---|---|
| python-validator | mechanical hygiene | PASS 77 | correct, low information |
| code-auditor | runtime correctness; subprocess/worktree/NaN paths | UNSOUND 68 | **highest yield** — five reproduced bugs, two invisible to the fingerprint |
| test-architect | the golden test is what determinism rests on | IMPROVE 74 (auto-fail) | correct — mutation testing proved the verdict path was unguarded |
| software-architecture-expert-validator | four specs claim things about the code nobody had checked | IMPRECISE 74 | correct — caught networkx, toolchain roles, §6.1 shape drift |
| popper-validator | the June root finding was Popper's; closure test | UNCORROBORATED 87 | **correct** — predicted the `fan_in_nonzero` bug before the run confirmed it |
| circumvention-forecaster | the June highest-severity lens; scored 38 then | VULNERABLE 88 | **most informative number on the project** — the "exploits moved, didn't close" pattern |

Not chosen: Husserl (fulfillment audit fits M2, when there is a rendered experience), Hume (re-run at M2, when the stance becomes visible to a viewer), Wittgenstein (deferred to the C3 ruleset, where the naming lives).

Definition versions and token counts were not attached to runs 4–9 at save time; attaching them is a tracker follow-up, and future saves carry them.

**Rule 3 — a minimal consumer of `validation.json` exists from early M2.** Nobody shares a `validation.json`; the cutaway is the distribution mechanism for the measurement, and a consumer, even a throwaway one, is what makes the gate real (circumvention A12). M2 starts with a skeleton-schema sketch, strata plus one or two features, no C5.

**Rule 4 — the novelty claim is exact.** README states the prior art (CodeCity; CodeScene; Nagappan & Zimmermann; Google 2011) and claims only the temporal-holdout gate between metric and picture, citing only results the report has produced.

**Name (system-spec open question #5, substrate open question #9).** *Resolved.* The system is **codebase-as-structure** (the repository name, the parent spec, the tracker project). The standalone product — C1 plus the gate — is **repo-substrate** (the Python package and the CLI). Two names because they are two things: the second must be valuable even if the first never renders (`repo-substrate-spec.md` §1). No further naming work.

## D-014 · 2026-09-04 · The tuned weights are frozen; two gate corrections from the placeholder run

**Context.** The four-repo run under the D-011/D-012 gate (out/validation-placeholder) and the pre-registered tuning (config/tuning.json) landed together.

**Tuning outcome (D-009 protocol, tuning set = uluops-registry-api + eslint, grid step 0.1, objective = min-over-repos ΔROC then min PR ratio).**

| index | best weights found | min ΔROC (bar +0.05) | min PR ratio (bar ×1.20) | spec placeholder |
|---|---|---:|---:|---|
| `bug_pressure_index` | commit_count 0.5, recency 0.2, revert_count 0.3 | **+0.014** | **1.00** | ΔROC −0.041 / −0.119 |
| `change_pressure_index` | churn_lines 0.5, commit_count 0.2, recency 0.3 | **+0.030** | **1.00** | ΔROC +0.052 / +0.030 |

No weight vector in either grid reaches the pre-registered bar on the tuning set itself. The best `bug_pressure_index` drops `fix_count` and `fix_ratio` to zero weight: on these repos, historical fix concentration carries no forecast of future fix activity beyond busyness and recency. That is the substantive finding of M1 so far, and it is what the spec said the gate exists to find ("write down where the indices lie"). The weights are frozen in `config/tuned.toml` at this commit, before the test set is scored; the margins are not touched (D-009). The expected verdict on the test set is `unvalidated` for both, and if so C3 may not name a feature over either.

**Correction 1 — degeneracy is a modal-value share, not a distinct-value count.** The D-011 check marked `has_sibling_test` degenerate on every repo because it is binary. A two-valued signal with a real minority class is not a constant. `degenerate_max_modal_share` = 0.97 replaces `degenerate_min_distinct`; a constant (share 1.0) still fails. Enforced in `validation/asserted.py::run_stability`; floor validated in `ValidationConfig.validate()`.

**Correction 2 — the retirement criterion is satisfied by a committed fixture, and says so.** After the `import type` fix the two import instruments agree at τ 0.98–1.00 on every reference repo, which trips the D-011 criterion for `fan_in`, `fan_out`, `test_fan_in`. The criterion's purpose was to refuse a counterpart that *cannot* fail; `tests/test_instruments.py` shows these can (the scanner over-counts an import-shaped string; the primary drops type edges with the flag off; the fingerprint moves with the flag). The grounding table now records `adversarial_fixture` per G2 pair, `validation.json` carries `retirement_backed`, and the report prints the fixture name or "NO FIXTURE." A pair that trips the criterion without a fixture would be reported as such; none does. Enforced in `validation/config.py` (`GROUNDING`), `validation/gate.py::descriptive_verdict`, `validation/report.py`.

**Observed and left as is.** `neglect_index` is unstable on `mcp-secure-server` (max Δ 0.207, p95 0.025 — one node) and passes on the other three; the `max` clause is deliberately strict and the signal is `asserted` at M = 2. `has_sibling_test` under the corrected check is expected to be `asserted` (G1) with its heuristic declared; it feeds nothing.

**Breaks if.** The test-set verdict comes back `validated` for either index despite the tuning set failing the bar — that would be a sign the split leaked, and the first thing to check is `substrate_attestations` and the split SHAs.

## D-015 · 2026-09-04 · M1 verdict: both predictive indices `unvalidated`; twenty-one descriptive signals `asserted`; what C3 may name

**The test-set verdict** (out/validation, tuned config commit 24c087a, test repos typeorm and mcp-secure-server, tuning repos in-sample for the record):

| index | repo | role | ROC vs best baseline | PR-AUC ratio | passed |
|---|---|---|---:|---:|---|
| `bug_pressure_index` | typeorm | test | 0.770 vs 0.728 (+0.042) | ×1.06 | no |
| `bug_pressure_index` | mcp-secure-server | test | 0.828 vs 0.825 (+0.004) | ×1.55 | no |
| `change_pressure_index` | typeorm | test | 0.878 vs 0.728 (+0.150) | ×1.21 | **yes** |
| `change_pressure_index` | mcp-secure-server | test | 0.856 vs 0.825 (+0.031) | ×1.68 | no |

`bug_pressure_index`: **unvalidated**, 0 of 2. `change_pressure_index`: **unvalidated**, 1 of 2 (the bar is both test repos). Tuning-set rows fail the same clauses, as the tuning already showed.

**What the numbers say.** With the tuned weights `bug_pressure_index` rank-correlates with the baseline it must beat at τ 0.72–0.83: it *is* busyness plus recency with a revert term, which is what a grid search over a space that cannot beat busyness will find. The June concept — "historical fix concentration forecasts future fix activity" — is not supported on these four repos beyond what busyness already carries. `change_pressure_index` carries real signal on the large TypeScript repo (+0.150 ROC, the only clean pass in the whole run) and beats the baselines everywhere but never by the margin on the small one, whose holdout is 28 commits and 22 positives.

**Consequences, per the anti-horoscope contract (system spec §3, mapper §3).**
- C3 may not name a feature over `bug_pressure_index` or `change_pressure_index` except as `decorative: true` with a `decorative_reason`. The toothpick's fragility half and the crack/fault-line features have no validated forecast to rest on in v0.
- C3 may name features over the twenty-one `asserted` signals, in the descriptive register only (§2.1.1): `load_index`, `centrality`, `fan_in`, `fan_in_nonzero`, `fan_out`, `neglect_index`, `age_days`, `last_touched_days`, `blame_age_median`, `reinforcement_index`, `test_fan_in`, `has_sibling_test`, `complexity_proxy_index`, `nesting_proxy`, `size_loc`, `commit_count`, `churn_lines`, `fix_count`, `author_count`, `cochange_degree`, `recent_commit_share`. Foundation, strata, corridor (position), flooded basement (load-bearing ∧ neglected), scaffolding (reinforcement), and lighting/material (recency/age) are all reachable as descriptions.
- `revert_count` is `untested (degenerate)`: on every reference repo the modal value (zero) covers more than 97% of files. It stays a raw metric and feeds nothing named.
- The G2 pairs are `non_discriminating` on the reference set and fixture-backed (D-014); `age_days` and `neglect_index` ↔ blame are discriminating on their own (τ 0.38–0.78).

**What M1 delivered.** A substrate that is byte-identical on re-run, attested by seed and content hash, with every value-affecting choice in a published fingerprint preimage; a gate whose floors cannot be loosened below spec, whose labels are frozen on the validation side, whose test/tuning roles are in the artifact, and which returned a negative result on the first thing it was built to test. That is the product the substrate spec §1 said must be valuable even if nothing renders. **M1 is complete** in the sense the spec defines; the checklists' remaining unchecked items are the known deferrals (§3A corroboration, the population-drift stability variant, the edge-dropout sweep for `centrality`, a generic degradation flag for the non-graph indices).

**What changes for M2.** The ruleset is authored over `asserted` signals in the descriptive register. The recognition record for `load_index` on registry-api is overlap 0.40 / τ 0.44 against a model-assisted n=1 ranking — reported, not evidence. The cutaway's first consumer of `validation.json` (D-013 rule 3) is the next thing built.

**Breaks if.** A future reference repo with a long, fix-tagged history and a stable busyness profile lets `bug_pressure_index` clear the bar. Then the verdict moves, the report shows which repo moved it, and the toothpick's fragility half becomes voiceable. Nothing about the design has to change for that; only the evidence.

## D-016 · 2026-09-04 · M2 begins with the consumer: C3 as a gated ruleset engine, C6 as a deterministic SVG cutaway

**Decision.** M2's first deliverable is the thing D-013 rule 3 asked for — something downstream that reads `validation.json` — built as the real C3 rather than a throwaway, because the gate logic is small and the throwaway would have had to implement it anyway.

- **C3 (`repo_substrate/mapper/`).** A ruleset is a versioned **TOML** document (`rulesets/<profile>.toml`): a header and `[[feature]]` entries, each a conjunction of `signal op value` terms where `value` is `pNN` (a percentile of that signal across the population, resolved at map time) or an absolute number. No `or`, no `not`: a feature is a conjunction and a different feature is a different conjunction. The spec said YAML; TOML parses with the standard library and carries no new dependency, and both are versioned diffable text, which is the property the spec wanted. **The gate runs before any predicate is evaluated**: every signal a non-decorative feature reads must be `validated` or `asserted` in `validation.json`, a missing key is `untested`, and any violation refuses the whole skeleton (`GateError`). A `decorative` feature must carry `decorative_reason` or the ruleset does not load. Feature status is the min-operator of mapper §5. `graph_dependent` features degrade (emitted, flagged, not diagnostic) when the substrate's graph is degraded or the node's `load_index_degraded` is set. Every feature instance carries its predicate, the resolved thresholds, the evidence values, and each signal's status. `skeleton.json` records the substrate seed, both fingerprints, the ruleset name and version, a content hash of itself, and a `summary` with `diagnostic_count`, `decorative_count`, `degraded_count`, and `decorative_features`. The archetype is `null`: mapper §7 Q1 is unresolved and therefore not claimed.
- **The maintainability ruleset v0.1.0.** Six diagnostic features over `asserted` signals — `foundation` (load p90; `name_implies_consequence`, position name "high-load hub"), `hub` (centrality p90), `flooded_basement` (neglect p90 ∧ load ≥ 0.10, the substrate §9 query), `scaffolding` (reinforcement ≥ 0.5), `dark_room` / `lit_room` (last-touched p90 / p10) — and two **decorative** ones, `toothpick_wing` and `crack`, both over `bug_pressure_index`, each with a `decorative_reason` citing D-015. They are kept so that their absence from the diagnosis is visible on the picture rather than silent.
- **C6 (`repo_substrate/cutaway.py`), C4 folded in.** A deterministic SVG: wings are top-level directories (columns), strata are five `age_days` percentile bands with the oldest at the bottom, rooms are files with width ∝ √lines, material is age, lighting is recency, and features are overlays with distinct styles. The banner prints the diagnostic count, the decorative count in a warning colour, the degraded count, the gate's per-signal statuses, and every fingerprint. Decorative features are drawn dashed in a colour no diagnostic feature uses. Each room's tooltip carries its path, its raw numbers, and every feature that fired on it with its position name. No randomness: same skeleton and substrate, same bytes. The seed is recorded for the stochastic form grammar a later phase may add.
- **Geometry is profile-independent** (mapper §6): strata and wings come from the substrate; the ruleset only decides overlays. `overlays[]` is present and empty; the second profile is the next ruleset.

**First run, all four repos, over the D-015 verdict:** every non-decorative feature admitted; `crack` fires 22–59 times per repo and `toothpick_wing` 0–3 times, all decorative and counted; nothing degraded. On registry-api the toothpick never fires because every top-decile-load file is imported by a test.

**Assumes.** Five age bands and directory wings are an adequate first geometry. They are the cheapest geometry that makes the age-strata metaphor literal; a dependency-layering geometry (topological rank) is the alternative the system spec names and is deferred.

**Breaks if.** A reader takes `foundation` as a forecast. The feature carries `name_implies_consequence: true` and a position name, the banner says every feature denotes present position, and the tooltip prints the position name; the C5 lint (M3) is the last line. On this run no feature over a `validated` signal exists, so no forecast register is available to anything.

**Seen on the first pictures (D-016 addendum).** On `mcp-secure-server` the whole `cookbook` wing sits in the flooded-basement band — old, untouched, still imported — which is exactly what the sealed ranking's section 6 pre-registered ("cookbook/** will dominate … leaf consumers"). On `uluops-registry-api` the foundation outlines land on `src/utils/errors.ts`, `src/config/index.ts`, `src/db/connection.ts`, three of the ranking's top four load-bearing files, and the flooded basement is the bottom band of `src/utils`. Reported here as recognition, not evidence (n = 1, model-assisted); the pictures are in `reports/2026-09-04-m2/`.

## D-017 · 2026-09-05 · Overlays, two geometries, and a skeleton diff; geometry leaves the profile

**Decision.**
- **Overlays are implemented as mapper §6 specifies: layering, never unification.** `substrate map` takes one base ruleset and any number of `--overlay` rulesets. Each is gated on its own signals; each produces its own feature list and summary under `overlays[]`; duplicate profiles are refused. Geometry (strata, wings) is computed once from the substrate and is byte-identical whether or not overlays are present (tested). Nodes flagged by more than one profile are listed in `co_located_nodes` and counted — shown, never averaged. In the cutaway the base profile styles the room and each overlay adds a corner badge in its own hue; the HTML wrapper (`--html`) toggles overlay layers, and the base cannot be turned off because it is the building.
- **Geometry is a substrate property, chosen at map time, not a profile property.** `strata_signal` is removed from the ruleset. `--geometry age` (five `age_days` bands, oldest at the bottom) or `--geometry layer` (dependency layering: longest import path to a leaf over the SCC condensation, leaves at the bottom — the system spec §5.1's primary strata definition). The chosen geometry is recorded in `skeleton.json` and captioned on the picture. Cycles collapse to one layer; the condensation is Tarjan's SCC, iterative.
- **Second profile: onboarding v0.1.0** — `entrance` (fan_in 0 ∧ fan_out ≥ p75), `corridor` (centrality ≥ p90 ∧ fan_out ≥ p50), `foundation` (shared with maintainability, so co-location is visible), `leaf_utility` (fan_out 0 ∧ fan_in ≥ p75). All over asserted G2/G4 signals, all position names.
- **Skeleton diff** (`substrate skeleton-diff before after --renames <substrate>`): per (profile, feature) added/removed nodes and Jaccard over nodes present in both skeletons, a summary `feature_churn` (symmetric difference over union), and `strata_moved`. Born and deleted nodes are excluded from churn and counted separately — the same discipline as the signal-level budget (validation §2.4.1). This is the instrument for mapper §7 Q3; the budget number itself is not yet set. It is also the diff the Phase 1 time-lapse will consume.

**Why geometry left the profile.** If a profile could choose the strata, two lenses over one repo would draw two buildings, and mapper §6's whole point — the same room, marked twice — would be lost. A geometry is a way of drawing the substrate; a profile is a way of reading it.

**Assumes.** Corner badges at 7px read at the room sizes in use; on very small rooms (10px wide) two badges touch. Acceptable for v0.

**Breaks if.** A third overlay is added: corners run out at four. The badge scheme is a v0 encoding; a fifth profile needs a different mark.

**First skeleton-diff reading (D-017 addendum).** `uluops-registry-api`, age geometry, maintainability + onboarding, HEAD−5 commits → HEAD: 267 common nodes, 0 born, 0 deleted; `feature_churn` 0.012; 3 nodes changed stratum (1.1%); per feature, `dark_room` +1 and `flooded_basement` +2/−1 (Jaccard 0.96 and 0.90), everything else identical. Five commits moved about one percent of the named structure. A budget in the region of "≤ 5% feature churn and ≤ 3% strata movement per K = 5 commits" would pass this repo comfortably; it is not pinned until the other three repos are measured the same way.

**Predicate semantics (D-017 addendum).** The first layer-geometry render showed the onboarding `entrance` and `leaf_utility` features never firing: a bare metric name in a predicate resolved to its *percentile*, and an ECDF percentile is never 0, so `fan_out == 0` could not be true. Rule, now enforced in `mapper/engine.py::_node_value` and stated in the ruleset grammar: a predicate name denotes an index by its index name, otherwise the raw metric; `pNN` thresholds are ranked over those raw values; only `*_nonzero` names resolve to percentiles. Absolute thresholds therefore mean what they say on the signal's own scale, and percentile thresholds are unchanged in effect.

## D-018 · 2026-09-05 · Skeleton-level stability budget pinned; judged over the untouched population

**Decision.** Mapper §7 Q3 is resolved. Between two skeletons of one repository, **untouched feature churn ≤ 0.05 and untouched strata movement ≤ 0.05** — one room in twenty — with the floors of the signal-level budget carried over: at least 30 untouched common nodes, and no more than half of the common population touched. The budget is per comparison and per geometry; the caller chooses K and the diff records `commits_between`. Enforcement: `src/repo_substrate/mapper/diff.py::skeleton_diff` computes the split and emits `budget.verdict ∈ {within_budget, over_budget, untested}` with a reason; `SKELETON_BUDGET` holds the numbers; the CLI derives the touched set from the after-substrate's timeline (`touched_since`, commits after the before skeleton's `head_sha`, through the renames map) and reports `untested: touched_set_unavailable` when the two skeletons are not on one recorded line. Tests: `test_skeleton_budget_is_judged_over_the_untouched_population`, `test_skeleton_budget_floors_refuse_to_get_easier`, `test_touched_since_reads_the_after_timeline_through_renames`.

**Why the untouched population.** Same reasoning as D-008 for the signal budget. A node the intervening commits edited may legitimately change feature or stratum — that is the skeleton reporting the edit, and a time-lapse that hid it would be lying. A node they did not edit that changes anyway moved by ripple: a percentile threshold shifted under it, or a dependency's layer depth changed. Ripple is the jitter that makes adjacent frames flicker, and it is the only thing a *stability* budget should bound. The whole-population numbers stay in the output because they are what a reader sees.

**Why 0.05.** The four-repo reading (`reports/2026-09-05-m2/skeleton-budget.md`, K = 5, both geometries) puts untouched feature churn at 0.005–0.014 and untouched strata movement at 0–0.032. A ceiling fitted to the data would be no test; a ceiling far above it would never fail. 0.05 is above every reading, within a factor of two of the tightest (mcp-secure-server, layer, strata), and has a plain meaning on the picture: under a five-commit edit elsewhere, no more than one room in twenty may change its mark or its floor. A ruleset whose threshold sits in a dense part of a signal's distribution would exceed it at once; that is the failure it is built to catch.

**Assumes.** K = 5 is the perturbation the reference set was measured at; a budget claimed at K = 50 has not been measured. The touched set is what the extractor's timeline records as `nodes_touched`, so a file the extractor does not model (docs, lockfiles) cannot be "touched" — correct, since it is not a room either.

**Breaks if.** A geometry with finer strata (more than five bands) is added: strata movement scales with band count and the ceiling was read at five. Or a feature is written over a raw-count threshold near the mode of its distribution (`fan_in >= 2` on a repo where most files have fan_in 1 or 2): churn would be real and the budget would correctly refuse the ruleset, which is the point.

**Observed on the way (recorded, not gating).** Feature churn is geometry-invariant, as it must be. `uluops-registry-api`'s window touched no source node and the skeleton still moved 1.1%: the age signals are measured from HEAD's timestamp, so removing commits moves the clock — age geometry drifts under time alone. Layer geometry is the less stable geometry (longest-path depth propagates to every importer); whether it needs its own ceiling is deferred to Phase 1, where the time-lapse will read it at every checkpoint.

