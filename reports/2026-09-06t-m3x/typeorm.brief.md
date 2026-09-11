# typeorm — architect's brief

*The register below is rendered from the facts sheet by code and carries the inventory (D-039); the reading beneath it is model-written and linted. Register lint: **FAILED (2 violations) on attempt 3**. What the lint checked: R1 consequence and forecast vocabulary refused outside a struck disclosure clause; R2 every citation resolves to a feature that fired on the rooms it names, with the count the skeleton records; R3 a number is on the facts sheet and sits in the sentence that cites its feature; R4 decorative features cited by count only, never as diagnosis, with their ungrounded signal named; R5 a consequence-implying name carries its position name where first used; R6 no whole-building label; R7 the diagnostic and decorative counts stated (met by the register); R8 a room named in a sentence is covered by a feature cited in that sentence; R9 features with the same or nested rooms named together (met by the register); R10 a directory named in a sentence contains a room cited in it; R11 no distributional adverb, ranking of marks, span or proximity between rooms; R12 a number wears its unit, a count of relations matches the register by kind; no ratio across units; R13 a nesting is not an identity; a shared predicate is one measurement, not two agreeing; R14 no 'validated' where no signal holds it; R15 a feature's largest directory named with its population (met by the register); R16 a feature's count in a minority wing or a directory is sayable only where that wing or directory is named; the largest wing's count is the register's; R17 a claim that a feature stands apart, or lacks a property another feature marks on its rooms, is checked against the register; R18 no family of marks the sheet does not define (the graph marks, the onboarding marks); a family every cited feature's record reads is admitted. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `d8064b45d1c6…`, facts `40f321599211…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.16.0; a PASS is a pass under that grammar (D-035).*

## Register

*Rendered from the facts sheet by code (brief 0.16.0); every cell is a field, no cell is a sentence. 583 rooms in 7 wings ((root) 3 · docker 1 · docs 9 · extra 2 · packages 69 · playground 3 · src 496); 619 diagnostic marks across all profiles (483 in the base profile), one mark per feature per room; identical pairs of diagnostic features mark 123 rooms twice (59 under one predicate in two profiles, 70 where two predicates draw one set because a conjunct excludes nothing, 6 under both); the diagnostic features name 9 distinct sets of rooms; 61 decorative marks (crack, toothpick_wing); 160 rooms carry two or more diagnostic marks; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis. A position names where a room sits in the record its predicate reads — the record is named beside each position — and is not a claim about its condition (D-004 Q3). The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a 3rd or more of them and the feature has 6 or more rooms; a parent that shares a wing's name is marked as the parent. The relation column draws identity and containment, and only those, between features, diagnostic or decorative, with 3 or more rooms; two sets that overlap without one containing the other are not related here, and 'no identity or containment' says exactly that. A caveat is the ruleset's own limit on what a predicate reads, never a claim about this repository. Every cell that is not a number is a cell's own answer, not a gap.*

| feature | profile | position | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node (edit record) | 59 | (root) 1, src 58 | none holds a third | no identity or containment | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room (clock) | 70 | src 70 | src/error 33 / 61 | = flooded_basement (load_index >= 0.10 excludes nothing) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched, still-imported room (import graph and clock) | 70 | src 70 | src/error 33 / 61 | = dark_room (load_index >= 0.10 excludes nothing) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load hub (import graph) | 59 | packages 2, src 57 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | no consequence word in the name (lexicon); a position in the import graph | 60 | src 60 | none holds a third | ⊃ corridor (23 of these rooms outside it) | `centrality >= p90` |
| lit_room | maintainability | no consequence word in the name (lexicon); a position in the clock | 60 | (root) 1, packages 2, src 57 | none holds a third | no identity or containment | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room (test graph) | 164 | packages 17, src 147 | none holds a third | no identity or containment | `reinforcement_index >= 0.5` |
| ◌ toothpick_wing | maintainability | unreinforced high-load node with high edit pressure (import graph and test graph and edit record) | 2 | src 2 | too few rooms to place (2) | too few rooms to relate (2) | decorative — bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| corridor | onboarding | high-centrality, high-fan-out junction (import graph) | 37 | src 37 | none holds a third | ⊂ hub (23 hub rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load hub (import graph) | 59 | packages 2, src 57 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| import_root | onboarding | import-graph root (import graph) | 1 | packages 1 | too few rooms to place (1) | too few rooms to relate (1) | `fan_in == 0 and fan_out >= p75` — caveat: reads no fan-in, not entrance (§5.5): a package entry that other rooms import cannot qualify, and one that nothing imports can |
| leaf_utility | onboarding | imported leaf (import graph) | 33 | packages 4, src 29 | none holds a third | no identity or containment | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry (import graph) | 6 | packages 2, src 4 | src (as parent, not the wing) 4 / 5 | no identity or containment | `is_package_entry == 1` |

## Reading

Seven wings hold the building: src with 496 rooms, packages with 69, docs with 9, (root) with 3, playground with 3, extra with 2, docker with 1. 17 of the 164 scaffolding rooms sit in packages; scaffolding is a test-imported room, a position in the import graph [scaffolding ×164: packages/codemod/src/cli/parse-args.ts].

33 of the 70 dark_room rooms sit in the src/error directory, which holds 61 rooms [dark_room ×70: src/error/TypeORMError.ts]. flooded_basement — a long-untouched, still-imported room — adds load_index >= 0.10 to dark_room, a long-untouched room, and it excludes nothing on this repository: the 70 rooms are the same 70 [flooded_basement ×70; dark_room ×70].

foundation — a high-load hub — fires under both profiles on one predicate: the 59 rooms under maintainability and the 59 under onboarding are the same predicate under two profiles [foundation ×59; onboarding/foundation ×59]. 2 of those 59 rooms sit in packages, and 7 of the 59 sit in src/schema-builder/table, which holds 7 rooms [foundation: packages/codemod/src/transforms/stats.ts, src/schema-builder/table/Table.ts].

The 37 corridor rooms nest inside the 60 hub rooms; the added conjunct fan_out >= p50 removes 23 rooms from that set, and the two remain two sets [corridor ×37; hub ×60]. 6 of the 60 hub rooms sit in the src/metadata-args directory, which holds 22 rooms [hub: src/metadata-args/MetadataArgsStorage.ts].

8 of the 33 leaf_utility rooms sit in src/driver/types, which holds 12 rooms, and 4 of the 33 sit in packages [leaf_utility ×33: src/driver/types/ColumnTypes.ts, packages/codemod/src/lib/colors.ts]. 2 of the 6 package_entry rooms sit in packages [package_entry ×6: packages/legacy-naming-strategies/src/index.ts]. The import_root predicate reads no fan-in (§5.5): a package entry that other rooms import cannot qualify, and one that nothing imports can [import_root: packages/codemod/src/index.ts].

The 11 diagnostic features name 9 distinct sets of rooms, and the register draws 3 relations: 2 identical, 1 within. 160 rooms carry two or more diagnostic marks. 1 of the 60 lit_room rooms sits in (root), and 2 of those 60 sit in packages [lit_room ×60: eslint.config.mjs, packages/codemod/eslint.config.mjs].

crack — a high edit-pressure node — and toothpick_wing — an unreinforced high-load node with high edit pressure — rest on bug_pressure_index, which is unvalidated, and their 61 decorative marks render without being a diagnosis [crack ×59; toothpick_wing ×2].

The diagnosis presupposes a maintenance norm — that the positions it marks are worth a visit — which the reader may reject; it is stated as an ought, not a fact.

## Provenance

- attempt: `3`
- attempts_log: `1: R12-unit, R2-provenance; 2: R1-consequence, R5-disclosure, R5-disclosure; 3: R12-unit, R15-composition`
- brief_version: `0.16.0`
- effort: `high`
- facts_hash: `40f32159921147619a5c35b204ea5a76a53b141c4631139b757866530680cd30`
- input_tokens: `23390`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `5065`
- stop_reason: `end_turn`

## Register lint

| rule | paragraph | detail | text |
|---|---|---|---|
| R12-unit | 2 | 61 counts marks on the facts sheet, not rooms | 33 of the 70 dark_room rooms sit in the src/error directory, which holds 61 rooms [dark_room ×70: src/error/TypeORMError.ts]. |
| R15-composition | 4 | src/metadata-args is named for corridor without both its share (4) and its rooms (22) in the sentence; a share carries its denominator | The 37 corridor rooms nest inside the 60 hub rooms; the added conjunct fan_out >= p50 removes 23 rooms from that set, and the two remain two sets [corridor ×37; |

**This brief failed the register lint and is not a diagnosis until it passes.**
