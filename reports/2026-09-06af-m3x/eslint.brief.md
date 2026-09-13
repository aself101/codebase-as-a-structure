# eslint — architect's brief

*Rendered from the facts sheet by code; no model wrote any of it. The model-written reading was cut at D-049 after eleven hostile seatings found it reciting the register and everything it could add was a field. Every cell is a field, and every fixed text on the page has a test that asserts it against the sheet it is rendered from (`tests/test_brief.py`); the tests run on a fixture, not on this page. Profile maintainability 0.2.8 + onboarding 0.2.5, geometry age, skeleton `04a4c7a82a46…`, facts `2613794275bc…`. As of 2026-09-04, commit `3f20a57c6293`. Calibration: in-repo, self-relative (system spec §5.3): every pNN ranks the 473 rooms as one population, across 6 package scopes (package.json) pooled — per-package calibration is an open question of the mapper (architect-brief spec §5, mapper §7 Q7); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is a `substrate timelapse` run under gate `179d8acb7b0c`; this page carries no stability value. Brief 0.27.0.*

## Register

**A position names where a room sits in a record — the import graph, the clock, the test graph, the edit record, size — and is not a claim about the room's condition (D-004 Q3). Every pNN ranks this repository's own 473 rooms, so a `>= p90` row holds a tenth of them — or more where rooms tie at the cutoff; each row states its share — and no count on this page compares across repositories. A room is a source file outside the test convention with computed signals: 473 of the tree's 1481 files; the 1008 test files are nodes of the import graph and not rooms.**

*Rendered from the facts sheet by code (brief 0.27.0); every cell is a field, a count, or a fixed text over them; no cell is written. 473 rooms in 8 wings ((root) 4 · bin 1 · conf 2 · docs 30 · lib 388 · messages 18 · packages 8 · tools 22); 923 diagnostic marks across all profiles (675 in the base profile), one mark per feature per room; identical pairs of diagnostic features mark 48 rooms twice (48 under one predicate in two profiles, 0 where two predicates draw one set because a conjunct excludes nothing, 0 under both); the diagnostic features name 10 distinct sets of rooms; 49 excluded marks ◌ (crack 48, toothpick_wing 1); 254 rooms carry two or more distinct diagnostic sets; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated — asserted is a description that held under the stability budget and the corroboration its grounding class requires (validation spec §2.4), validated a forecast confirmed by a temporal holdout (validation spec §3). A wing is a directory at depth 1 of the tree (the ruleset's wing_depth), not a package; the population spans 6 package scopes (rooms per scope, largest first, each scope named by the manifest that holds it: package.json 435 · docs/package.json 24 · packages/eslint-config-eslint/package.json 5 · docs/_examples/custom-rule-tutorial-code/package.json 4 · packages/js/package.json 3 · docs/_examples/integration-tutorial-code/package.json 2). ◌ marks an excluded feature (the ruleset's word is decorative): computed and counted, excluded from the diagnosis because a signal it reads is unvalidated. The record a position is read from is named beside it. The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a 3rd or more of them and the feature has 6 or more rooms; a parent that shares a wing's name is marked as the parent. The relation column draws identity and containment, and only those, between features, diagnostic or decorative, with 3 or more rooms — and a containment the predicates guarantee at any count; two sets that overlap without one containing the other are not related here, and 'no identity or containment' says exactly that. A containment says 'by its predicate' when the inner predicate conjoins every term of the outer; otherwise it says which raw signals the two predicates read in common, a blend or index expanded through its declared inputs, or 'no signal in common' — a signal, not an instrument: the import graph and the test graph are one edge set read twice, a test file is a node whose imports count in fan_in and centrality, and test_fan_in counts those importers alone. The import graph is resolved statically: 20 imports in the tree did not resolve to a file and 490 are external packages; an import computed at run time is not an edge, so a room loaded only that way reads as unimported. A feature that fired on no room keeps its row at 0. A caveat is the ruleset's own limit on what a predicate reads, never a claim about this repository. Every cell that is not a number is a cell's own answer, not a gap. The rooms at the most positions and the rooms each pair of diagnostic features shares follow the table.*

| position (the record it reads) | feature | profile | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate; caveat or reason |
|---|---|---|---|---|---|---|---|
| high edit-pressure node (clock and edit record) | ◌ crack | maintainability | 48 | (root) 2, bin 1, lib 44, packages 1 | lib/rules 35 / 293 | ⊃ ◌ toothpick_wing (by its predicate; 47 of these rooms outside it) | `bug_pressure_index >= p90` — rooms at or above this repository's p90 on bug_pressure_index (here 0.72978): 48 of 473, 10.1% — ◌ excluded from the diagnosis: bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. |
| long-untouched room (clock) | dark_room | maintainability | 83 | (root) 2, docs 22, lib 40, messages 11, packages 5, tools 3 | none holds a third | ⊃ flooded_basement (by its predicate; 8 of these rooms outside it) | `last_touched_days >= p90` — rooms at or above this repository's p90 on last_touched_days (here 533.966 days): 83 of 473, 17.5%; ties at the cutoff carry the row past a tenth |
| long-untouched room above the load floor (import graph and clock and size) | flooded_basement | maintainability | 75 | (root) 2, docs 18, lib 38, messages 11, packages 3, tools 3 | none holds a third | ⊂ dark_room (by its predicate; 8 dark_room rooms outside this set) | `last_touched_days >= p90 and load_index >= 0.10` — caveat: reads a floor on the load blend, not an importer (D-048): a room that nothing imports can clear the floor on inverse fan-out and size alone (this case: 27 of 75 here) |
| high-load node (import graph and size) | foundation | maintainability | 48 | conf 2, lib 45, tools 1 | none holds a third | ⊃ ◌ toothpick_wing (by its predicate; 47 of these rooms outside it); = onboarding/foundation (same predicate, two profiles) | `load_index >= p90` — rooms at or above this repository's p90 on load_index (here 0.77078): 48 of 473, 10.1% |
| no consequence word in the name (lexicon); a position in the import graph | hub | maintainability | 50 | conf 2, docs 1, lib 46, packages 1 | none holds a third | ⊃ corridor (by its predicate; 28 of these rooms outside it) | `centrality >= p90` — rooms at or above this repository's p90 on centrality (here 0.0012): 50 of 473, 10.6% |
| no consequence word in the name (lexicon); a position in the clock | lit_room | maintainability | 48 | (root) 2, lib 40, messages 1, tools 5 | lib/rules 24 / 293 | no identity or containment | `last_touched_days <= p10` — rooms at or below this repository's p10 on last_touched_days (here 47.8538 days): 48 of 473, 10.1% |
| test-imported room (test graph) | scaffolding | maintainability | 371 | conf 2, docs 2, lib 360, packages 1, tools 6 | lib/rules 293 / 293 | no identity or containment | `reinforcement_index >= 0.5` — caveat: reads whether any file under the test convention imports the room (test_fan_in > 0, D-011): the index is 0 with no test importer and 0.5 or more with one, so 0.5 is its floor, not a midpoint; a helper or fixture under the test paths counts as a test importer, and one import suffices |
| unreinforced high-load node with high edit pressure (import graph and clock and test graph and edit record and size) | ◌ toothpick_wing | maintainability | 1 | lib 1 | too few rooms to place (1) | ⊂ ◌ crack (by its predicate; 47 crack rooms outside this set); ⊂ maintainability/foundation = onboarding/foundation (by its predicate; 47 maintainability/foundation rooms outside this set); too few rooms for any other relation (1) | `load_index >= p90 and bug_pressure_index >= p90 and reinforcement_index <= 0.0` — ◌ excluded from the diagnosis: bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| high-centrality junction with fan-out at or above the median (import graph) | corridor | onboarding | 22 | lib 21, packages 1 | none holds a third | ⊂ hub (by its predicate; 28 hub rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| high-load node (import graph and size) | foundation | onboarding | 48 | conf 2, lib 45, tools 1 | none holds a third | = maintainability/foundation (same predicate, two profiles); ⊃ ◌ toothpick_wing (by its predicate; 47 of these rooms outside it) | `load_index >= p90` — rooms at or above this repository's p90 on load_index (here 0.77078): 48 of 473, 10.1% |
| import-graph root with fan-out at or above the upper quartile (import graph) | import_root | onboarding | 19 | (root) 2, bin 1, docs 3, lib 2, messages 2, packages 2, tools 7 | none holds a third | no identity or containment | `fan_in == 0 and fan_out >= p75` — caveat: reads no fan-in, not entrance (D-029): a package entry that other rooms import cannot qualify, and one that nothing imports can (this case: 4 of 19 here) |
| imported leaf with fan-in at or above the upper quartile (import graph) | leaf_utility | onboarding | 148 | conf 2, docs 2, lib 139, messages 1, packages 2, tools 2 | lib/rules 98 / 293 | no identity or containment | `fan_out == 0 and fan_in >= p75` |
| declared package entry (package manifest) | package_entry | onboarding | 11 | bin 1, docs 1, lib 4, packages 5 | packages/eslint-config-eslint 4 / 5 (tied with lib (as parent, not the wing) 4 / 6) | no identity or containment | `is_package_entry == 1` |

### Rooms at the most positions (6)

**Every room at the most positions, in path order — a set, not a ranking and not a severity (D-004 Q3).**

*Every room under the most distinct diagnostic sets (6), by path — 13 rooms. A set is a distinct set of rooms a diagnostic feature draws (a feature under two profiles, or two features drawing one set, is one set). Rooms at fewer positions are not listed; 254 rooms carry two or more distinct sets. Size is the room's line count.*

| room | lines | positions (distinct sets) | diagnostic features that mark it |
|---|---|---|---|
| lib/config/default-config.js | 66 | 6 | corridor, dark_room, flooded_basement, hub, maintainability/foundation, onboarding/foundation, scaffolding |
| lib/languages/js/source-code/index.js | 5 | 6 | corridor, dark_room, flooded_basement, hub, maintainability/foundation, onboarding/foundation, scaffolding |
| lib/linter/code-path-analysis/code-path-segment.js | 228 | 6 | corridor, dark_room, flooded_basement, hub, maintainability/foundation, onboarding/foundation, scaffolding |
| lib/linter/index.js | 8 | 6 | corridor, dark_room, flooded_basement, hub, maintainability/foundation, onboarding/foundation, scaffolding |
| lib/rule-tester/index.js | 5 | 6 | corridor, dark_room, flooded_basement, hub, maintainability/foundation, onboarding/foundation, scaffolding |
| lib/rules/utils/regular-expressions.js | 50 | 6 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |
| lib/shared/ast-utils.js | 27 | 6 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |
| lib/shared/deep-merge-arrays.js | 52 | 6 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |
| lib/shared/logging.js | 33 | 6 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |
| lib/shared/severity.js | 45 | 6 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |
| lib/shared/string-utils.js | 47 | 6 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |
| lib/shared/traverser.js | 177 | 6 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |
| packages/js/src/index.js | 19 | 6 | corridor, dark_room, flooded_basement, hub, package_entry, scaffolding |

### Shared rooms

*Rooms both features mark, for every pair of diagnostic features (a feature under two profiles is two rows); the diagonal is the feature's own count. A shared count equal to the smaller of the two features' own counts is containment, and equal to both is identity; the relation column above draws those, and only between features with 3 or more rooms or where the predicates guarantee the containment — any other pair under that floor is read here and not there.*

| shared rooms | dark_room | flooded_basement | maintainability/foundation | hub | lit_room | scaffolding | corridor | onboarding/foundation | import_root | leaf_utility | package_entry |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dark_room | **83** | 75 | 17 | 21 | 0 | 23 | 8 | 17 | 4 | 21 | 6 |
| flooded_basement | 75 | **75** | 17 | 21 | 0 | 23 | 8 | 17 | 0 | 21 | 3 |
| maintainability/foundation | 17 | 17 | **48** | 36 | 9 | 42 | 15 | 48 | 0 | 26 | 1 |
| hub | 21 | 21 | 36 | **50** | 9 | 39 | 22 | 36 | 0 | 27 | 2 |
| lit_room | 0 | 0 | 9 | 9 | **48** | 37 | 7 | 9 | 3 | 6 | 0 |
| scaffolding | 23 | 23 | 42 | 39 | 37 | **371** | 18 | 42 | 0 | 135 | 4 |
| corridor | 8 | 8 | 15 | 22 | 7 | 18 | **22** | 15 | 0 | 0 | 2 |
| onboarding/foundation | 17 | 17 | 48 | 36 | 9 | 42 | 15 | **48** | 0 | 26 | 1 |
| import_root | 4 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | **19** | 0 | 4 |
| leaf_utility | 21 | 21 | 26 | 27 | 6 | 135 | 0 | 26 | 0 | **148** | 2 |
| package_entry | 6 | 3 | 1 | 2 | 0 | 4 | 2 | 1 | 4 | 2 | **11** |

## Excluded marks (◌)

49 excluded marks (◌) render but are not a diagnosis: crack — high edit-pressure node — and toothpick_wing — unreinforced high-load node with high edit pressure — rest on bug_pressure_index, which is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin.

## Stance

The diagnosis presupposes a maintenance norm — that the positions it marks are worth a visit — which the reader may reject; it is stated as an ought, not a fact (system spec, stance disclosure).

## Provenance

- brief_version: `0.27.0`
- facts_hash: `2613794275bcea9c460842339d3a992f69c2b44e27ccb80074736ba7b74b1ca0`
- generator: `code`
