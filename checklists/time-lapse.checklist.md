# Time-lapse checklist — `time-lapse-spec.md`

Testable contracts for Phase 1. Tags: `[NOW]` required for the phase; `[TL]` time-lapse-specific; `[DET]` determinism; `[HOR]` anti-horoscope; `[BUDGET]` D-018. Verification: `(unit)` · `(fixture)` reference-repo run · `(review)` human.

## A. Checkpoints (§2)

- [x] `[NOW][TL]` Checkpoints lie on the first-parent trunk; HEAD is always the last frame; `--frames N` is evenly spaced first-and-last inclusive, `--every K` walks back from HEAD. *(§2)* `(unit: test_choose_checkpoints_schedules)`
- [x] `[NOW][TL]` Each frame is extracted truncated at its checkpoint: inventory and history stop there, `as_of` is the checkpoint's clock; commit counts are monotone along the trunk. *(§2)* `(unit: test_timelapse_on_scripted_repo)`
- [x] `[NOW][DET]` Frames are cached by `(repo, sha, trunc, fingerprint)`; a re-run over the same cache produces byte-identical manifest and report. *(§2, §5)* `(unit: test_timelapse_is_deterministic_over_the_cache)`

## B. Per frame (§3)

- [x] `[NOW][HOR]` A frame whose substrate fingerprint differs from the gate's is refused, not mapped. *(§3.2)* `(unit: test_timelapse_refuses_a_frame_under_a_foreign_gate)`
- [x] `[NOW][TL]` A frame below `n_min` is recorded as `skipped: population_below_n_min`, produces no skeleton, and does not break the adjacency chain. *(§3.3)* `(unit: test_timelapse_on_scripted_repo; fixture: registry frame 0)`
- [x] `[NOW][HOR]` Every frame is mapped under the same `validation.json`, ruleset, overlays, and geometry; the manifest records all four. *(§3.1)* `(unit)`

## C. Between frames (§4)

- [x] `[NOW][BUDGET]` Adjacent mapped frames are diffed with the later frame's renames and the exact touched set (`touched_between`: commits in the later timeline absent from the earlier). *(§4)* `(unit)`
- [x] `[NOW][TL]` Movement decomposes into edits (touched), ripple (untouched), structural (born + deleted); shares sum to one. *(§4)* `(unit: test_timelapse_on_scripted_repo)`
- [x] `[NOW][TL]` Ripple splits into clock (clock-relative signals, age strata) and rank (rank-only signals, layer strata); a feature's kind follows its predicate's signals. *(§4)* `(unit: test_timelapse_on_scripted_repo)`
- [x] `[TL][BUDGET]` The report states the K of every transition and that the budget was pinned at K = 5. *(§4)* `(review: reports/2026-09-05-phase1/*.timelapse.md, 2026-09-05)`

## D. Outputs (§5)

- [x] `[NOW][TL]` `frames.json`, `timelapse.md`, `timelapse.html`, and per-frame skeleton / SVG / diff are written; the page carries every mapped frame and overlay toggles across frames. *(§5)* `(unit)`
- [x] `[TL]` Limitations §6 appear on the report. *(§6)* `(unit: test_timelapse_on_scripted_repo asserts the first; review for the rest)`

## E. Open (§7)

- [ ] `[TL]` Event-keyed schedule. *(§7 Q1)*
- [ ] `[TL][BUDGET]` Geometry-specific strata ceiling, read from the time-lapse. *(§7 Q2)*
- [ ] `[TL][HOR]` Per-frame gate. *(§7 Q3)*
