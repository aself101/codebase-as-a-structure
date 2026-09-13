# uluops-registry-api — architect's brief

*Rendered from the facts sheet by code; no model wrote any of it. The model-written reading was cut at D-049 after eleven hostile seatings found it reciting the register and everything it could add was a field. Every cell is a field, and every fixed text on the page has a test that asserts it against the sheet it is rendered from (`tests/test_brief.py`); the tests run on a fixture, not on this page. Profile maintainability 0.2.8 + onboarding 0.2.5, geometry age, skeleton `048edec68d69…`, facts `f15326e9fbb9…`. As of 2026-08-31, commit `f7414cc7bbec`. Calibration: in-repo, self-relative (system spec §5.3): every pNN ranks the 267 rooms as one population; one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is a `substrate timelapse` run under gate `179d8acb7b0c`; this page carries no stability value. Brief 0.27.0.*

## Register

**A position names where a room sits in a record — the import graph, the clock, the test graph, the edit record, size — and is not a claim about the room's condition (D-004 Q3). Every pNN ranks this repository's own 267 rooms, so a `>= p90` row holds a tenth of them — or more where rooms tie at the cutoff; each row states its share — and no count on this page compares across repositories. A room is a source file outside the test convention with computed signals: 267 of the tree's 456 files; the 189 test files are nodes of the import graph and not rooms.**

*Rendered from the facts sheet by code (brief 0.27.0); every cell is a field, a count, or a fixed text over them; no cell is written. 267 rooms in 3 wings ((root) 7 · scripts 30 · src 230); 352 diagnostic marks across all profiles (280 in the base profile), one mark per feature per room; identical pairs of diagnostic features mark 27 rooms twice (27 under one predicate in two profiles, 0 where two predicates draw one set because a conjunct excludes nothing, 0 under both); the diagnostic features name 10 distinct sets of rooms; 27 excluded marks ◌ (crack 27, toothpick_wing 0); 88 rooms carry two or more distinct diagnostic sets; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated — asserted is a description that held under the stability budget and the corroboration its grounding class requires (validation spec §2.4), validated a forecast confirmed by a temporal holdout (validation spec §3). A wing is a directory at depth 1 of the tree (the ruleset's wing_depth), not a package; the population spans 1 package scope (rooms per scope, largest first, each scope named by the manifest that holds it: package.json 267). ◌ marks an excluded feature (the ruleset's word is decorative): computed and counted, excluded from the diagnosis because a signal it reads is unvalidated. The record a position is read from is named beside it. The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a 3rd or more of them and the feature has 6 or more rooms; a parent that shares a wing's name is marked as the parent. The relation column draws identity and containment, and only those, between features, diagnostic or decorative, with 3 or more rooms — and a containment the predicates guarantee at any count; two sets that overlap without one containing the other are not related here, and 'no identity or containment' says exactly that. A containment says 'by its predicate' when the inner predicate conjoins every term of the outer; otherwise it says which raw signals the two predicates read in common, a blend or index expanded through its declared inputs, or 'no signal in common' — a signal, not an instrument: the import graph and the test graph are one edge set read twice, a test file is a node whose imports count in fan_in and centrality, and test_fan_in counts those importers alone. The import graph is resolved statically: 0 imports in the tree did not resolve to a file and 565 are external packages; an import computed at run time is not an edge, so a room loaded only that way reads as unimported. A feature that fired on no room keeps its row at 0. A caveat is the ruleset's own limit on what a predicate reads, never a claim about this repository. Every cell that is not a number is a cell's own answer, not a gap. The rooms at the most positions and the rooms each pair of diagnostic features shares follow the table.*

| position (the record it reads) | feature | profile | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate; caveat or reason |
|---|---|---|---|---|---|---|---|
| high edit-pressure node (clock and edit record) | ◌ crack | maintainability | 27 | src 27 | none holds a third | no identity or containment | `bug_pressure_index >= p90` — rooms at or above this repository's p90 on bug_pressure_index (here 0.75142): 27 of 267, 10.1% — ◌ excluded from the diagnosis: bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. |
| long-untouched room (clock) | dark_room | maintainability | 27 | scripts 1, src 26 | src/db/migrations 11 / 55 | ⊃ flooded_basement (by its predicate; 1 of these rooms outside it) | `last_touched_days >= p90` — rooms at or above this repository's p90 on last_touched_days (here 177.27 days): 27 of 267, 10.1% |
| long-untouched room above the load floor (import graph and clock and size) | flooded_basement | maintainability | 26 | scripts 1, src 25 | src/db/migrations 11 / 55 | ⊂ dark_room (by its predicate; 1 dark_room room outside this set) | `last_touched_days >= p90 and load_index >= 0.10` — caveat: reads a floor on the load blend, not an importer (D-048): a room that nothing imports can clear the floor on inverse fan-out and size alone (this case: 12 of 26 here) |
| high-load node (import graph and size) | foundation | maintainability | 27 | src 27 | none holds a third | = onboarding/foundation (same predicate, two profiles) | `load_index >= p90` — rooms at or above this repository's p90 on load_index (here 0.78956): 27 of 267, 10.1% |
| no consequence word in the name (lexicon); a position in the import graph | hub | maintainability | 27 | src 27 | none holds a third | ⊃ corridor (by its predicate; 14 of these rooms outside it) | `centrality >= p90` — rooms at or above this repository's p90 on centrality (here 0.00474): 27 of 267, 10.1% |
| no consequence word in the name (lexicon); a position in the clock | lit_room | maintainability | 40 | src 40 | none holds a third | no identity or containment | `last_touched_days <= p10` — rooms at or below this repository's p10 on last_touched_days (here 9.1099 days): 40 of 267, 15.0%; ties at the cutoff carry the row past a tenth |
| test-imported room (test graph) | scaffolding | maintainability | 133 | src 133 | none holds a third | ⊃ corridor (no signal in common; 120 of these rooms outside it) | `reinforcement_index >= 0.5` — caveat: reads whether any file under the test convention imports the room (test_fan_in > 0, D-011): the index is 0 with no test importer and 0.5 or more with one, so 0.5 is its floor, not a midpoint; a helper or fixture under the test paths counts as a test importer, and one import suffices |
| unreinforced high-load node with high edit pressure (import graph and clock and test graph and edit record and size) | ◌ toothpick_wing | maintainability | 0 | no wing (0) | no rooms | no rooms to relate (0) | `load_index >= p90 and bug_pressure_index >= p90 and reinforcement_index <= 0.0` — ◌ excluded from the diagnosis: bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| high-centrality junction with fan-out at or above the median (import graph) | corridor | onboarding | 13 | src 13 | none holds a third | ⊂ hub (by its predicate; 14 hub rooms outside this set); ⊂ scaffolding (no signal in common; 120 scaffolding rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| high-load node (import graph and size) | foundation | onboarding | 27 | src 27 | none holds a third | = maintainability/foundation (same predicate, two profiles) | `load_index >= p90` — rooms at or above this repository's p90 on load_index (here 0.78956): 27 of 267, 10.1% |
| import-graph root with fan-out at or above the upper quartile (import graph) | import_root | onboarding | 11 | scripts 8, src 3 | scripts (as parent, not the wing) 8 / 27 | no identity or containment | `fan_in == 0 and fan_out >= p75` — caveat: reads no fan-in, not entrance (D-029): a package entry that other rooms import cannot qualify, and one that nothing imports can (this case: 0 of 11 here) |
| imported leaf with fan-in at or above the upper quartile (import graph) | leaf_utility | onboarding | 20 | src 20 | src/utils 9 / 22 | no identity or containment | `fan_out == 0 and fan_in >= p75` |
| declared package entry (package manifest) | package_entry | onboarding | 1 | src 1 | too few rooms to place (1) | too few rooms to relate (1) | `is_package_entry == 1` |

### Rooms at the most positions (6)

**Every room at the most positions, in path order — a set, not a ranking and not a severity (D-004 Q3).**

*Every room under the most distinct diagnostic sets (6), by path — 2 rooms. A set is a distinct set of rooms a diagnostic feature draws (a feature under two profiles, or two features drawing one set, is one set). Rooms at fewer positions are not listed; 88 rooms carry two or more distinct sets. Size is the room's line count.*

| room | lines | positions (distinct sets) | diagnostic features that mark it |
|---|---|---|---|
| src/utils/async-handler.ts | 36 | 6 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |
| src/utils/singleton.ts | 34 | 6 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |

### Shared rooms

*Rooms both features mark, for every pair of diagnostic features (a feature under two profiles is two rows); the diagonal is the feature's own count. A shared count equal to the smaller of the two features' own counts is containment, and equal to both is identity; the relation column above draws those, and only between features with 3 or more rooms or where the predicates guarantee the containment — any other pair under that floor is read here and not there.*

| shared rooms | dark_room | flooded_basement | maintainability/foundation | hub | lit_room | scaffolding | corridor | onboarding/foundation | import_root | leaf_utility | package_entry |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dark_room | **27** | 26 | 3 | 3 | 0 | 6 | 0 | 3 | 0 | 4 | 0 |
| flooded_basement | 26 | **26** | 3 | 3 | 0 | 6 | 0 | 3 | 0 | 4 | 0 |
| maintainability/foundation | 3 | 3 | **27** | 20 | 5 | 26 | 9 | 27 | 0 | 13 | 0 |
| hub | 3 | 3 | 20 | **27** | 4 | 26 | 13 | 20 | 0 | 14 | 0 |
| lit_room | 0 | 0 | 5 | 4 | **40** | 35 | 3 | 5 | 0 | 2 | 1 |
| scaffolding | 6 | 6 | 26 | 26 | 35 | **133** | 13 | 26 | 0 | 19 | 1 |
| corridor | 0 | 0 | 9 | 13 | 3 | 13 | **13** | 9 | 0 | 0 | 0 |
| onboarding/foundation | 3 | 3 | 27 | 20 | 5 | 26 | 9 | **27** | 0 | 13 | 0 |
| import_root | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **11** | 0 | 0 |
| leaf_utility | 4 | 4 | 13 | 14 | 2 | 19 | 0 | 13 | 0 | **20** | 0 |
| package_entry | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | **1** |

## Excluded marks (◌)

27 excluded marks (◌) render but are not a diagnosis: crack — high edit-pressure node — rests on bug_pressure_index, which is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. toothpick_wing fired on no room.

## Stance

The diagnosis presupposes a maintenance norm — that the positions it marks are worth a visit — which the reader may reject; it is stated as an ought, not a fact (system spec, stance disclosure).

## Provenance

- brief_version: `0.27.0`
- facts_hash: `f15326e9fbb907829bfd82460418a91bdde10c24f738665b550b4ce52a39a08c`
- generator: `code`
