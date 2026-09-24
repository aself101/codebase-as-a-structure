# Stance reading — per-repository applicability of the stance's known false positive

*Closes architect-brief spec §5 Q4 (opened at D-028, partly closed at D-070 and D-072). Drafted 2026-09-24 after the unpointed seating series closed (D-075), as the first of the three deferred items. Status: **withdrawn at D-076** — the measurement is sound as a count and does not measure what §3 interprets it as; nothing reaches the page. Kept as written, with the review in §9, as the record of a negative result.*

> **Withdrawal, 2026-09-24 (D-076).** A `data-science-analyst` review (tracker run 64) returned UNWARRANTED 50: the counts are right and have no leakage, but a low fix-touch rate for the longest-untouched rooms is predicted alike by *finished* rooms, by *neglected* ones (not being visited is what neglect is), and by the gate's own recency baseline (validation spec §3.5), so §3's last paragraph and §7's first clause claim a separation the comparison cannot make. The sections below are unchanged; §9 records what the review found and what a future attempt at §5 Q4 needs.

## 1. The question, as the record states it

The system spec discloses the diagnosis's stance: the maintenance norm presupposes that the positions it marks are worth a visit, and "a finished, correct, stable utility that nobody has touched in three years scores high on `neglect_index` and is not, by any reasonable reading, neglected" (`codebase-as-structure-system-spec.md:5`). D-028 found that on typeorm this abstract case is the concrete one — the long-untouched rooms are dominated by one-class error files — and opened a per-repository applicability note. §5 Q4 names two instruments for it: *the share of a feature's rooms that are single-class files*, and *the gate's per-repository corroboration numbers*.

What the page carries today (brief 0.41.0): the spec's case in its words, counted at the long-untouched position ("here dark_room, 70 rooms"), and the page's narrowing (long-untouched ∩ high-load, `stance_case` on the sheet, `brief.py::_stance_case`). Neither says whether, *on this repository*, the long-untouched position holds mostly finished rooms or mostly neglected ones. The eleventh-round skimmer (D-075, run 63) found the one high drift left standing: the Stance's list read as a work list.

## 2. What the two named instruments would and would not measure

**Single-class share.** A syntactic proxy: a file whose only top-level declaration is one class. The substrate has no such signal. The nearest precedent is `is_placeholder`, a content regex in the effective config (`config.py:155`, `inventory.py:57`), graded `untested` by the gate. A single-class regex over TypeScript and JavaScript would miss decorators, overloads and trailing re-exports, would be one more `untested` flag, and — the load-bearing objection — would measure *form*, not the thing the stance's case is about. typeorm's error classes are single-class and finished; so is an abandoned one-class adapter. The share would say how many rooms look like the case, not how many are it.

**The gate's corroboration numbers.** `validation.json` carries, per signal and per repository, a stability reading and a cross-modal corroboration (`signals.<name>.grounding.per_repo[]`: `stability`, `corroboration`). For `last_touched_days` these certify that the clock reads what git says — corroboration against `git log author_date`, passed on all four repositories. They say nothing about whether a long-untouched room is finished. They are about the instrument, not the norm. *As named in §5 Q4 this half measures the wrong thing, and this spec does not build it.*

## 3. The instrument that measures the question

The gate's temporal holdout already holds, per repository, the three things the question needs (`validation/holdout.py:65–122`, `split_and_eligible`):

- the eligible rooms at the split — introduced before it and alive at HEAD (§3.3 of the validation spec), with their metrics and percentiles *as of the split* (`SplitContext.nodes`);
- a label per room — whether a fix or revert commit, by the frozen label regex, touched it in the holdout window (`SplitContext.labels`; §3.4, the declared fix-*activity* proxy, never defect origin);
- the base rate over the eligible rooms (`stats.base_rate`).

**The stance reading** for a repository is then: of the rooms that sat at the long-untouched position at the split, how many received fix activity in the holdout window, against the base rate over all rooms. Three choices, each fixed by the feasibility run (§8):

- *The population is the page's, not the gate's.* The gate's eligible set includes test files (`holdout_include_tests = True`, `validation/config.py:305`) — on typeorm 2274 eligible nodes against the page's 574 rooms. The reading takes the eligible nodes that are rooms under the page's rule: `file_kind == "source"` and not a test (typeorm 417 at the split).
- *The position is resolved as the mapper resolves it.* `last_touched_days >= p90` over the raw values of that population, by the mapper's own `_resolve_thresholds` and `_node_value` (`mapper/engine.py:46, 119`) — not the substrate's percentile field, which ranks ties high and put 563 of eslint's 1219 eligible nodes at the top tenth in the first draft of the run.
- *Only the long-untouched position is read.* The page's narrowing (long-untouched ∩ `load_index` ≥ p90) holds 1 to 17 rooms at the four splits; an interval over three rooms says nothing, and the page will not print one.

A long-untouched set visited by fixes well under the base rate is a repository where the position held rooms the window's fix activity passed by — the pattern the stance's false positive predicts; a set visited at the base rate is one where the position did not separate them.

**Why this is not a verdict and grants nothing.** It is descriptive, one number per repository, read under the same proxy the holdout already declares. It does not change any signal's status, does not validate `neglect_index`, and does not license consequence vocabulary (architect-brief spec §1). It says, for one past window, how often the position the stance names was visited by fixes — which is the question §5 Q4 asks, stated as a count.

## 4. Contract

- **A derived artifact, pinned to the gate; the gate is not re-run.** `substrate stance-reading --validation <validation.json> --out <stance_reading.json>` reads, for each reference repository, the tip and split substrates the gate attested (`validation.json:substrate_attestations`), refuses any whose bytes' sha256 differs from the attestation, recomputes the split exactly as `split_and_eligible` does (`validation/holdout.py:65`; the split index, the frozen label regex, `canonical_resolver`), and writes per repository `{split_sha, n_holdout_commits, rooms, base_rate, untouched: {rooms, positives, rate, wilson95}}`, with the gate's `substrate_config_fingerprint` and `validation_config_fingerprint` copied in. It never opens the substrate cache through `SubstrateCache` — `_load_valid` deletes a file whose fingerprint differs from the caller's config (`validation/substrates.py:60`), and a derived command must not be able to delete the gate's evidence.
- **No verdict, no status.** The artifact carries counts and an interval. No signal's status changes; `validation.json` is not rewritten.
- **Sheet.** `substrate brief --stance-reading <stance_reading.json>`; `facts()` records the page's repository's entry as `stance_reading` (or `null`), and refuses an artifact whose substrate fingerprint differs from the substrate the page was rendered from.
- **Page (brief 0.42.0).** The Stance paragraph, after the spec's case and before the page's narrowing, one sentence of counts: "At the gate's holdout split (commit `844ad406f1`, 193 commits before this page's snapshot), 37 rooms sat at the long-untouched position; 3 of them (8%, 95% interval 3–21%) were touched by a commit whose subject marks a fix in the commits since, against 40% of all 194 rooms." The sentence names the proxy and the window and grades no room.
- **The work-list drift.** Answered by order: the reading stands before the room list.

## 5. What this does not do

- It does not classify a room as finished. No instrument on the page can; the sentence says how a position fared, not what any room is.
- It does not replace the Stance's room list or `stance_case`.
- It does not generalize across repositories: each page carries its own repository's reading (the register's rule: no count compares across repositories).
- It does not treat the holdout window as the future. The window is a past one; the sentence is in the past tense.

## 6. Limitations (to carry on the page's legend if built)

1. **The proxy.** Fix-activity by subject regex (`\b(bug|hotfix|patch)\b`), not defect origin (validation spec §3.4.1). A finished room touched by a mass rename labelled "patch" is a positive.
2. **Survivorship.** Eligibility requires the room to be alive at HEAD (§3.3). A long-untouched room deleted in the window drops out, and deletion is a visit the reading cannot see.
3. **The split is not the page.** The set at the split is not the page's dark_room set: rooms introduced after the split are absent, and a clock tie at a mass commit can put a different set at the cutoff (eslint's Prettier commit is after its split [VERIFY]).
4. **Small sets.** mcp-secure-server's window is 29 commits; its interval is wide (0 of 34, 0–10%), and the sentence prints it.
5. **The base rate is high where the window is long.** typeorm's window is 1213 commits and 71% of its rooms saw a fix-labelled commit in it — the subject regex catches broad commits; the reading is relative to that rate, not to zero.

## 7. Breaks if

The reading comes back at or near the base rate on every repository — then the position does not separate finished from visited rooms at this resolution, the sentence says so in its numbers, and the single-class instrument (§2) is the one left to try. Or a reader takes the rate as a forecast for the page's rooms — then the sentence's tense and window were not enough, and the reading moves to the legend beside the other gate statements.

## 8. Feasibility (2026-09-24, read-only, from the pinned gate's cache)

Computed from the attested cache files of gate `177c129be9b5` by a scratch script using the gate's and the mapper's own functions; the eligible counts and base rates over all nodes reproduce `holdout-report.md` exactly (typeorm 2274 / 0.446, eslint 1219 / 0.185), which checks the path. Over the page's population:

| repository | split | holdout commits | rooms | base rate | long-untouched at split | touched by a fix | rate (95% interval) |
|---|---|---:|---:|---:|---:|---:|---|
| typeorm | `fe7f328fd5` | 1213 | 417 | 0.710 | 43 | 20 | 0.465 (0.325–0.611) |
| mcp-secure-server | `654057ef9f` | 29 | 186 | 0.118 | 34 | 0 | 0.000 (0.000–0.102) |
| uluops-registry-api | `844ad406f1` | 193 | 194 | 0.402 | 37 | 3 | 0.081 (0.028–0.213) |
| eslint | `3398431574` | 2202 | 395 | 0.322 | 40 | 8 | 0.200 (0.105–0.348) |

On three repositories the interval sits below the base rate; on eslint it reaches it. §7's first clause does not fire.

## 9. Review and withdrawal (D-076)

Every number below was recomputed by the reviewer from the attested cache and the load-bearing ones re-checked here.

1. **The comparison cannot separate the hypotheses.** On registry 3 of the 37 long-untouched rooms were touched by any commit in the window, and on mcp-secure-server none of 34 — the low fix rate *is* the low visitation. Registry's three visits were all fixes (3 of 3), which if anything leans the other way. Against the other rooms rather than the whole (the base rate includes the set), and against the adjacent recency bands, the top decile is not distinct: typeorm's three oldest bands read 0.42 / 0.45 / 0.47.
2. **typeorm's reading is one codemod.** 18 of its 20 positives come from "fix: switch to type imports and exports whenever possible (#12044)", a `fix:`-prefixed commit touching 1362 files; it also carries the base rate (0.71; 0.30 without fix commits over 20 files). The label proxy's weakness (validation spec §3.4.1), concrete.
3. **The survival filter conditions on the future and discards the discriminating outcome.** Eligibility requires a room alive at HEAD; on typeorm 61 of the 80 rooms at the position at the split were deleted by HEAD (the `sample/sample10-mixed/` files), eslint 12 of 43. Deletion is the strongest abandonment signal the history holds, and the reading drops it.
4. **The Wilson interval assumes independent labels**, and labels cluster by commit (one commit supplied 90% of typeorm's positives); the printed 95% interval overstated precision badly.
5. **mcp-secure-server's position is 28 days** (27 of 34 rooms tied there) in a 29-commit window — degenerate; and ties put 19% of registry's rooms and 18% of mcp's at a "top tenth".

**What a future attempt at §5 Q4 needs.** The observables that bear on finished-versus-neglected are the *kind* of the visits a position receives (fix versus mechanical, among rooms touched at all) and *deletion*, computed from the split-time set before any survival filter; both need a mass-commit guard on the label, uncertainty resampled by commit, and a comparison against the other rooms and the adjacent recency band. On three of the four reference repositories both observables are small-n today (registry 3 visits, mcp 0), so the attempt is deferred until a reference repository offers enough visits to read, not built to print "too few to read" on every page.
