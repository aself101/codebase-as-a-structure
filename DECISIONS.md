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
