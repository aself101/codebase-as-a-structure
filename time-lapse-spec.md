# Time-lapse — the evolution of a skeleton (Phase 1)

*Phase 1 of codebase-as-structure (system spec §8, §10; D-020, D-021). The time-lapse replays a repository's history at checkpoints, produces a skeleton per checkpoint under the same gate and ruleset, measures the movement between adjacent skeletons with the stability budget, and renders the sequence. It exists to answer one question the single frame cannot: **is the named structure of a repository, over its history, structural change or the budget's jitter?** The answer decides whether M3 is built (D-003, D-020). Implemented in `src/repo_substrate/timelapse.py` as `substrate timelapse`.*

## 1. What it is, and what it is not

The time-lapse is a **consumer** of M1 and M2. It adds no signal, no feature, no geometry. Per checkpoint it runs C1 (extraction, truncated at the checkpoint), C3 (the mapper under the gate), and C6 (the cutaway), and between checkpoints it runs the skeleton diff (mapper §7 Q3, D-017/D-018). Its own contributions are the checkpoint schedule (§2), the per-frame bookkeeping (§3), the reading of the budget across frames (§4), and the report and page (§5).

It is not a validation run. `validation.json` is produced once, at HEAD, by the temporal-holdout protocol, and **governs every frame** (§3.2). The time-lapse does not re-derive which signals are `asserted` at each checkpoint; it asks what the structure that HEAD's gate licenses looked like earlier. That is a limitation, stated on the page (§6).

## 2. Checkpoints

- **The trunk.** Checkpoints are commits on the **first-parent line** from the root to HEAD (`git rev-list --first-parent --reverse HEAD`). Every checkpoint is therefore an ancestor of HEAD on the mainline, its truncated history is a prefix of HEAD's, and consecutive checkpoints are ordered by reachability, not by timestamp. A commit on a merged side branch is never a checkpoint: its reachable history is a strange subset of the mainline's and a frame built on it would not sit between its neighbours.
- **Spacing by commit count**, not wall time, for the reason the holdout split gives (validation §3.1): idle gaps distort a time split; a count split keeps every frame populated. Two schedules: `--frames N` picks `N` evenly spaced trunk indices, first and last inclusive; `--every K` walks back from HEAD in steps of `K`. HEAD is always the final frame.
- **The frame is truncated.** Each checkpoint's substrate is extracted with `truncate_at = sha`: inventory and history both stop there (C1 §8), and `as_of` is the checkpoint's last commit, so age and recency are measured against that clock, not HEAD's. The HEAD frame is truncated too, for uniform semantics; it differs from the `tip` document only in the `truncated_at` field.
- **Cache.** Frames are cached by `(repo, sha, trunc, config fingerprint)` in the validation cache (`validation/substrates.py`), so a re-run with a different schedule reuses every frame it has already seen, and the frames the M1 gate extracted (the split and the perturbation) are reused if the schedule lands on them.

## 3. Per frame

### 3.1 Pipeline

`cache.get(repo, sha, truncate=True)` → `map_skeleton(substrate, validation, ruleset, overlays, geometry)` → `render_cutaway`. The skeleton and the SVG are written per frame (`fNNN-<sha8>.skeleton.json`, `.cutaway.svg`); the substrate stays in the cache.

### 3.2 Gate and fingerprint

The mapper records the substrate's config fingerprint in the skeleton but does not compare it with the gate's (`mapper/engine.py`). The time-lapse does: a frame whose `repo.config_fingerprint` differs from `validation.substrate_config_fingerprint` is refused (`TimelapseError`), because a gate earned under one extractor configuration licenses nothing about substrates produced under another. This is the same rule as the cache's own fingerprint check, applied at the seam the cache does not see.

### 3.3 Skipped frames

A checkpoint whose population is below the substrate's `n_min` produces a substrate with `percentiles_valid: false` and no indices; the mapper would map it as an empty building. The time-lapse records such a frame as **skipped** with reason `population_below_n_min` and produces no skeleton for it. Skipped frames appear in the manifest and the report; they do not break the adjacency chain (the next mapped frame is diffed against the last mapped frame).

## 4. Between frames — the budget at K ≫ 5

Adjacent mapped frames are diffed with `skeleton_diff` (D-017, D-018): the later frame's renames map canonicalizes the earlier's names; the **touched set** is the union of `nodes_touched` over the commits present in the later frame's timeline and absent from the earlier's (`touched_between` — exact, since both timelines are available, unlike the CLI's single-substrate `touched_since`); `commits_between` is the size of that commit set.

The budget (D-018) was pinned at K = 5. Between checkpoints K is typically tens to hundreds of commits, and the reading changes in two ways that the report must state rather than hide:

- **The floors bite.** When the intervening commits touch more than half the common population, the verdict is `untested: touched_fraction_exceeds_floor`. This is the floor doing its job: with most rooms edited, the untouched population is too small and too selected to measure ripple. A schedule that produces mostly untested frames is too coarse for the budget; `--every K` with a smaller K is the remedy, at extraction cost.
- **Ripple accumulates.** Over K commits the untouched population absorbs K shifts of every percentile threshold and every layer depth. The untouched churn per frame is therefore *ripple accumulated over K*, not the per-edit ripple the budget bounds. An `over_budget` frame at K = 200 is a weaker finding than one at K = 5, and the report labels each frame with its K so the reader can weigh it.

What the time-lapse can say cleanly, per frame, is the **decomposition of movement**: how many feature changes and strata moves fell on touched nodes (the skeleton reporting edits), how many on untouched nodes (ripple), and how many nodes were born or deleted (structural change). Summed over the history these three numbers answer the phase's question without depending on the budget's K.

Ripple itself has two sources that the first registry reading forced apart. A node nobody edited can change through a **clock-relative** signal — `age_days`, `last_touched_days`, `blame_age_median`, `recent_commit_share`, and the two indices that carry one of them (`neglect_index`, `change_pressure_index`) — because the checkpoint's clock advanced: a lit room going dark because nobody visited is the skeleton reporting time, and age-geometry strata move the same way. Or it can change through a **rank-only** signal — `centrality`, `load_index`, `fan_in`, `fan_out`, `bug_pressure_index`, `reinforcement_index` — because the percentile or the dependency layer moved under it while others changed. Only the second is jitter. The time-lapse classifies each feature by its predicate's signals (`mapper/diff.py::classify_signals`, `CLOCK_SIGNALS`, pinned by test) as *clock* (clock-relative signals only), *rank* (none), or *mixed* (both — its rank component cannot be separated, so it is counted as jitter, the conservative side; D-024). Strata moves of untouched rooms are rank under both geometries: since D-022 a floor moves only because the population re-ranked around the room. The phase's question is answered by the **jitter share**, rank + mixed. The budget (D-018, operand revised D-024) judges jitter over untouched rooms and reports clock beside it; it is pinned at K = 5 and applied up to K = 10, and a transition beyond that is `untested: beyond_pinned_k` — the verdict token does not travel to a K it was not pinned at, the numbers do, labelled with their K. A jitter share is a joint value of repository, schedule K, geometry, and ruleset; the report table carries K with it.

**Pre-registered ceilings (D-024).** "Jitter is a few percent" is refuted by a jitter share above 0.20 on any (repository, geometry) at twelve frames, or above 0.10 on two or more repositories. "The schedule is not averaging jitter away" is refuted when the every-5 jitter share exceeds the twelve-frame share by more than 2× or by 0.10 absolute.

## 5. Outputs

All under one directory per run:

- `frames.json` — the manifest: schedule, gate reference (validation fingerprint and `validated_at`), ruleset and overlay versions, geometry, and per frame `{index, trunk_index, sha, as_of, commit_count, status (mapped|skipped), reason, population, feature_counts, diff: {commits_between, born, deleted, touched, untouched_churn, untouched_strata, touched_changes, budget_verdict, reason}}`.
- `fNNN-<sha8>.skeleton.json`, `fNNN-<sha8>.cutaway.svg`, `fNNN-<sha8>.diff.json` per mapped frame.
- `timelapse.html` — the frames inline with a scrubber (slider, previous/next, arrow keys), a caption per frame (date, commit count, population, budget verdict against the previous frame), and overlay toggles that apply to every frame. Frames are separate drawings; a room is not tweened between them (§6).
- `timelapse.md` — the report: the per-frame table, the decomposition totals (§4), the budget tally (`within / over / untested-by-reason`), and the limitations.

Byte-determinism: the manifest and the report contain no timestamps of their own; a re-run over the same cache produces identical files.

## 6. Limitations (on the page)

1. **HEAD's gate governs every frame.** A signal `asserted` at HEAD is treated as `asserted` throughout. Whether it would have passed the stability and corroboration bars at an earlier checkpoint is not tested. The honest reading of an early frame is "what HEAD's licensed structure looked like then," not "what was licensed then."
2. **Percentiles are per frame.** In-repo calibration re-ranks at every checkpoint, so `hub` in frame 3 means top-decile centrality *of frame 3's population*. A node that keeps its rank while the repository grows keeps its feature; one that keeps its raw value while others overtake it loses it. This is what self-relative calibration means, and the time-lapse is where it becomes visible.
3. **No tweening.** Rooms are laid out per frame by wing and stratum; a node that moves stratum jumps. Continuity of identity is carried by the diff (through renames), not by the picture. Animated layout is Phase 3 render work.
4. **Layer geometry drifts more than age geometry** (D-018): expect more strata movement under `--geometry layer`, for the reason given there.
5. **Trunk-only checkpoints** exclude side-branch states. The history a frame carries is nonetheless the full reachable history at that commit, side branches merged before it included.
6. **"Untouched" is the complement within what the extractor models.** An edit to a file that is not a room — a tsconfig path alias, a lockfile, a build config — can change which imports resolve and so move `fan_in` or a dependency layer on rooms that count as untouched; that movement lands in the jitter class (D-024, Nagarjuna SV-2). Unquantified.
7. **Movement sums four kinds of count** — feature flips, floor moves, births, deletions — that share a denominator by convention, not by unit. The shares are bookkeeping within that mixture (D-024, Nagarjuna SV-4).

## 7. Open questions

1. **Schedule.** Even spacing by count is the v0 default because it needs no judgment. A schedule keyed to structural events (release tags, large-`born` commits) would place frames where the building changes; it needs the time-lapse to exist first to find them.
2. **A ceiling per K, and per geometry** (D-018, D-024). The budget was pinned at K = 5, and at K = 5 nothing fires it — not the reference set, not a ruleset written to break it (`reports/2026-09-05-m2b/adversarial-ruleset.md`): five commits rarely move an untouched room's rank signal at all. The ceiling must be pinned at a K where it can fail, from every-K readings; and layer geometry's jitter runs above age's on every repository, so a per-geometry ceiling is the same question.
3. **Per-frame gate.** Re-running the asserted bar at each checkpoint (stability against K removed commits, corroboration on that frame's population) would replace limitation 1 with measurement. Cost is roughly one gate run per frame.
