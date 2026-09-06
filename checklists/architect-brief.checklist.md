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
