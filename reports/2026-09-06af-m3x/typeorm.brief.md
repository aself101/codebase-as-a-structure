# typeorm — architect's brief

*Rendered from the facts sheet by code; no model wrote any of it. The model-written reading was cut at D-049 after eleven hostile seatings found it reciting the register and everything it could add was a field. Every cell is a field, and every fixed text on the page has a test that asserts it against the sheet it is rendered from (`tests/test_brief.py`); the tests run on a fixture, not on this page. Profile maintainability 0.2.8 + onboarding 0.2.5, geometry age, skeleton `dad26b2cd18f…`, facts `4b9f90dbe9f3…`. As of 2026-09-02, commit `ac41823b9e27`. Calibration: in-repo, self-relative (system spec §5.3): every pNN ranks the 583 rooms as one population, across 5 package scopes (package.json) pooled — per-package calibration is an open question of the mapper (architect-brief spec §5, mapper §7 Q7); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is a `substrate timelapse` run under gate `179d8acb7b0c`; this page carries no stability value. Brief 0.27.0.*

## Register

**A position names where a room sits in a record — the import graph, the clock, the test graph, the edit record, size — and is not a claim about the room's condition (D-004 Q3). Every pNN ranks this repository's own 583 rooms, so a `>= p90` row holds a tenth of them — or more where rooms tie at the cutoff; each row states its share — and no count on this page compares across repositories. A room is a source file outside the test convention with computed signals: 583 of the tree's 3600 files; the 3017 test files are nodes of the import graph and not rooms.**

*Rendered from the facts sheet by code (brief 0.27.0); every cell is a field, a count, or a fixed text over them; no cell is written. 583 rooms in 7 wings ((root) 3 · docker 1 · docs 9 · extra 2 · packages 69 · playground 3 · src 496); 619 diagnostic marks across all profiles (483 in the base profile), one mark per feature per room; identical pairs of diagnostic features mark 123 rooms twice (59 under one predicate in two profiles, 70 where two predicates draw one set because a conjunct excludes nothing, 6 under both); the diagnostic features name 9 distinct sets of rooms; 61 excluded marks ◌ (crack 59, toothpick_wing 2); 109 rooms carry two or more distinct diagnostic sets; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated — asserted is a description that held under the stability budget and the corroboration its grounding class requires (validation spec §2.4), validated a forecast confirmed by a temporal holdout (validation spec §3). A wing is a directory at depth 1 of the tree (the ruleset's wing_depth), not a package; the population spans 5 package scopes (rooms per scope, largest first, each scope named by the manifest that holds it: package.json 502 · packages/codemod/package.json 65 · docs/package.json 9 · packages/legacy-naming-strategies/package.json 4 · playground/package.json 3). ◌ marks an excluded feature (the ruleset's word is decorative): computed and counted, excluded from the diagnosis because a signal it reads is unvalidated. The record a position is read from is named beside it. The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a 3rd or more of them and the feature has 6 or more rooms; a parent that shares a wing's name is marked as the parent. The relation column draws identity and containment, and only those, between features, diagnostic or decorative, with 3 or more rooms — and a containment the predicates guarantee at any count; two sets that overlap without one containing the other are not related here, and 'no identity or containment' says exactly that. A containment says 'by its predicate' when the inner predicate conjoins every term of the outer; otherwise it says which raw signals the two predicates read in common, a blend or index expanded through its declared inputs, or 'no signal in common' — a signal, not an instrument: the import graph and the test graph are one edge set read twice, a test file is a node whose imports count in fan_in and centrality, and test_fan_in counts those importers alone. The import graph is resolved statically: 8 imports in the tree did not resolve to a file and 2073 are external packages; an import computed at run time is not an edge, so a room loaded only that way reads as unimported. A feature that fired on no room keeps its row at 0. A caveat is the ruleset's own limit on what a predicate reads, never a claim about this repository. Every cell that is not a number is a cell's own answer, not a gap. The rooms at the most positions and the rooms each pair of diagnostic features shares follow the table.*

| position (the record it reads) | feature | profile | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate; caveat or reason |
|---|---|---|---|---|---|---|---|
| high edit-pressure node (clock and edit record) | ◌ crack | maintainability | 59 | (root) 1, src 58 | none holds a third | ⊃ ◌ toothpick_wing (by its predicate; 57 of these rooms outside it) | `bug_pressure_index >= p90` — rooms at or above this repository's p90 on bug_pressure_index (here 0.76204): 59 of 583, 10.1% — ◌ excluded from the diagnosis: bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. |
| long-untouched room (clock) | dark_room | maintainability | 70 | src 70 | src/error 33 / 61 | = flooded_basement (load_index >= 0.10 excludes nothing) | `last_touched_days >= p90` — rooms at or above this repository's p90 on last_touched_days (here 1629.71 days): 70 of 583, 12.0%; ties at the cutoff carry the row past a tenth |
| long-untouched room above the load floor (import graph and clock and size) | flooded_basement | maintainability | 70 | src 70 | src/error 33 / 61 | = dark_room (load_index >= 0.10 excludes nothing) | `last_touched_days >= p90 and load_index >= 0.10` — caveat: reads a floor on the load blend, not an importer (D-048): a room that nothing imports can clear the floor on inverse fan-out and size alone (this case: 1 of 70 here) |
| high-load node (import graph and size) | foundation | maintainability | 59 | packages 2, src 57 | none holds a third | ⊃ ◌ toothpick_wing (by its predicate; 57 of these rooms outside it); = onboarding/foundation (same predicate, two profiles) | `load_index >= p90` — rooms at or above this repository's p90 on load_index (here 0.8039): 59 of 583, 10.1% |
| no consequence word in the name (lexicon); a position in the import graph | hub | maintainability | 60 | src 60 | none holds a third | ⊃ corridor (by its predicate; 23 of these rooms outside it) | `centrality >= p90` — rooms at or above this repository's p90 on centrality (here 0.0022): 60 of 583, 10.3% |
| no consequence word in the name (lexicon); a position in the clock | lit_room | maintainability | 60 | (root) 1, packages 2, src 57 | none holds a third | no identity or containment | `last_touched_days <= p10` — rooms at or below this repository's p10 on last_touched_days (here 57.5427 days): 60 of 583, 10.3% |
| test-imported room (test graph) | scaffolding | maintainability | 164 | packages 17, src 147 | none holds a third | no identity or containment | `reinforcement_index >= 0.5` — caveat: reads whether any file under the test convention imports the room (test_fan_in > 0, D-011): the index is 0 with no test importer and 0.5 or more with one, so 0.5 is its floor, not a midpoint; a helper or fixture under the test paths counts as a test importer, and one import suffices |
| unreinforced high-load node with high edit pressure (import graph and clock and test graph and edit record and size) | ◌ toothpick_wing | maintainability | 2 | src 2 | too few rooms to place (2) | ⊂ ◌ crack (by its predicate; 57 crack rooms outside this set); ⊂ maintainability/foundation = onboarding/foundation (by its predicate; 57 maintainability/foundation rooms outside this set); too few rooms for any other relation (2) | `load_index >= p90 and bug_pressure_index >= p90 and reinforcement_index <= 0.0` — ◌ excluded from the diagnosis: bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| high-centrality junction with fan-out at or above the median (import graph) | corridor | onboarding | 37 | src 37 | none holds a third | ⊂ hub (by its predicate; 23 hub rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| high-load node (import graph and size) | foundation | onboarding | 59 | packages 2, src 57 | none holds a third | = maintainability/foundation (same predicate, two profiles); ⊃ ◌ toothpick_wing (by its predicate; 57 of these rooms outside it) | `load_index >= p90` — rooms at or above this repository's p90 on load_index (here 0.8039): 59 of 583, 10.1% |
| import-graph root with fan-out at or above the upper quartile (import graph) | import_root | onboarding | 1 | packages 1 | too few rooms to place (1) | too few rooms to relate (1) | `fan_in == 0 and fan_out >= p75` — caveat: reads no fan-in, not entrance (D-029): a package entry that other rooms import cannot qualify, and one that nothing imports can (this case: 1 of 1 here) |
| imported leaf with fan-in at or above the upper quartile (import graph) | leaf_utility | onboarding | 33 | packages 4, src 29 | none holds a third | no identity or containment | `fan_out == 0 and fan_in >= p75` |
| declared package entry (package manifest) | package_entry | onboarding | 6 | packages 2, src 4 | src (as parent, not the wing) 4 / 5 | no identity or containment | `is_package_entry == 1` |

### Rooms at the most positions (6)

**Every room at the most positions, in path order — a set, not a ranking and not a severity (D-004 Q3).**

*Every room under the most distinct diagnostic sets (6), by path — 1 room. A set is a distinct set of rooms a diagnostic feature draws (a feature under two profiles, or two features drawing one set, is one set). Rooms at fewer positions are not listed; 109 rooms carry two or more distinct sets. Size is the room's line count.*

| room | lines | positions (distinct sets) | diagnostic features that mark it |
|---|---|---|---|
| src/index.ts | 183 | 6 | corridor, hub, lit_room, maintainability/foundation, onboarding/foundation, package_entry, scaffolding |

### Shared rooms

*Rooms both features mark, for every pair of diagnostic features (a feature under two profiles is two rows); the diagonal is the feature's own count. A shared count equal to the smaller of the two features' own counts is containment, and equal to both is identity; the relation column above draws those, and only between features with 3 or more rooms or where the predicates guarantee the containment — any other pair under that floor is read here and not there.*

| shared rooms | dark_room | flooded_basement | maintainability/foundation | hub | lit_room | scaffolding | corridor | onboarding/foundation | import_root | leaf_utility | package_entry |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dark_room | **70** | 70 | 6 | 9 | 0 | 12 | 0 | 6 | 0 | 11 | 0 |
| flooded_basement | 70 | **70** | 6 | 9 | 0 | 12 | 0 | 6 | 0 | 11 | 0 |
| maintainability/foundation | 6 | 6 | **59** | 39 | 10 | 44 | 27 | 59 | 0 | 12 | 1 |
| hub | 9 | 9 | 39 | **60** | 10 | 30 | 37 | 39 | 0 | 12 | 1 |
| lit_room | 0 | 0 | 10 | 10 | **60** | 25 | 9 | 10 | 0 | 3 | 1 |
| scaffolding | 12 | 12 | 44 | 30 | 25 | **164** | 21 | 44 | 0 | 14 | 1 |
| corridor | 0 | 0 | 27 | 37 | 9 | 21 | **37** | 27 | 0 | 0 | 1 |
| onboarding/foundation | 6 | 6 | 59 | 39 | 10 | 44 | 27 | **59** | 0 | 12 | 1 |
| import_root | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **1** | 0 | 1 |
| leaf_utility | 11 | 11 | 12 | 12 | 3 | 14 | 0 | 12 | 0 | **33** | 0 |
| package_entry | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | **6** |

## Excluded marks (◌)

61 excluded marks (◌) render but are not a diagnosis: crack — high edit-pressure node — and toothpick_wing — unreinforced high-load node with high edit pressure — rest on bug_pressure_index, which is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin.

## Stance

The diagnosis presupposes a maintenance norm — that the positions it marks are worth a visit — which the reader may reject; it is stated as an ought, not a fact (system spec, stance disclosure).

## Provenance

- brief_version: `0.27.0`
- facts_hash: `4b9f90dbe9f3ba39c47ca9ca2f0b2d015c0fbe1224d1cb58464f0baef99ff8d2`
- generator: `code`
