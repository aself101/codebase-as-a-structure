# Architect brief checklist — `architect-brief-spec.md`

Tags: `[NOW]` required for M3; `[HOR]` anti-horoscope; `[PROV]` provenance; `[DET]` determinism. Verification: `(unit)` · `(fixture)` real brief · `(review)` human.

- [x] `[NOW][DET]` The facts sheet is a pure function of the skeleton (+ substrate sizes) and is hashed. *(§2.1)* `(unit: test_facts_sheet_is_the_closed_set)`
- [x] `[NOW][HOR]` R1: consequence vocabulary is a violation except in a disclosure sentence. *(§1)* `(unit: test_lint_catches_each_register_breach)`
- [x] `[NOW][PROV]` R2: every paragraph cites; every citation resolves to a feature and a room that fired, or the skeleton's count. *(§1)* `(unit)`
- [x] `[NOW][HOR]` R3: numbers come from the facts sheet only. *(§1)* `(unit)`
- [x] `[NOW][HOR]` R4/R7: decorative features are never cited in diagnosis; their count is stated. *(§1)* `(unit)`
- [x] `[NOW][HOR]` R5: a consequence-implying name is disclosed with its position name. *(§1, D-004 Q3, D-024)* `(unit)`
- [x] `[NOW][HOR]` R6: no whole-building label. *(§1, D-019)* `(unit)`
- [x] `[NOW][PROV]` R8: a room named in a sentence is covered by a feature cited in that sentence that fired on it. *(§1, D-028)* `(unit: test_lint_catches_each_register_breach)`
- [x] `[NOW][HOR]` The disclosure clause is struck, not an amnesty; citations are stripped before R1; consequence phrases refused. *(§1, D-028)* `(unit)`
- [x] `[NOW][HOR]` A failing brief is written marked FAILED, exit 1; the violations are fed back once. *(§2.4)* `(unit: test_run_brief_regenerates_once_and_marks_failure)`
- [x] `[NOW][PROV]` Provenance (model served, request id, attempt, facts hash, skeleton hash) is on the page. *(§2.2)* `(unit)`
- [x] `[NOW][HOR]` Real briefs over the four reference skeletons pass the lint. *(§2)* `(fixture: reports/2026-09-06-m3/, 2026-09-06, second attempt on each)`
- [ ] `[HOR]` Hostile-reader model pass. *(§5 Q1)*
- [ ] `[HOR]` Per-signal lexicon widening when an index is validated. *(§5 Q3)*

## D-083 the window page and the brief's pointer (window-page-spec.md)

- [x] The brief's header names the window page (pair, earlier date, file) or says none was rendered; no count crosses (`test_the_brief_points_at_the_window_page_and_takes_no_count_from_it`, `test_register_*` clause assertion in `tests/test_brief.py`).
- [x] A sheet about another commit or another skeleton is refused (`test_the_brief_refuses_a_sheet_about_another_commit_or_another_skeleton`).
- [x] The diff carries true row sizes, rooms only one commit has, excluded rows without evidence, both sides' identity, and window times over the commits counted (`test_row_sizes_count_rooms_only_one_commit_has`, `test_excluded_rows_are_carried_outside_per_feature_and_without_evidence`, `test_identity_records_*`, `test_window_times_*`).
- [x] A crossing prints four numbers and two comparisons and no cause, for leavers and entrants; one predicate under two profiles is one row; a shared term is one line (`test_cutoff_passed_it_and_own_value_fell_*`, `test_an_entrant_*`, `test_one_predicate_under_two_profiles_*`).
- [x] Fixed-value terms, null outcomes, no-term-changed and a missing side each have a fixed form (`test_a_fixed_value_term_*`, `test_a_null_outcome_*`, `test_membership_change_with_no_term_change_and_a_missing_side`).
- [x] Clock rows get the same numbers and comparisons; excluded rows are counted and not named (`test_clock_rows_*`, `test_excluded_rows_are_counted_and_their_rooms_not_named`).
- [x] Two geometries are two readings; `floors` prints as bands; an unjudged window quotes the ladder's reason (`test_two_geometries_*`, `test_the_operand_named_floors_is_printed_as_bands`).
- [x] The window is in every crossing line; no property word and no mechanism word in fixed text (`test_the_window_is_in_every_crossing_line_*`, `test_no_property_word_and_no_mechanism_word_in_the_fixed_text`).
- [x] Refusals: same geometry twice, not one window, pre-D-083 diff, sides mapped differently, more than two (`test_refusals_each_with_its_reason`).
- [x] The gate's token, its reason and what fired are on neither the page nor the sheet (`test_the_gates_own_word_is_not_on_the_page_or_the_sheet`); a flagged name travels with its position (`test_a_flagged_name_travels_with_its_position_and_an_unflagged_one_is_bare`); band lines carry values (`test_band_lines_carry_the_band_and_raw_values_of_each_named_room`).
- [ ] The seat on the rendered mcp window page (spec §11.12): two run, both failed in part (runs 73, 74); a third owed on 0.3.0.
