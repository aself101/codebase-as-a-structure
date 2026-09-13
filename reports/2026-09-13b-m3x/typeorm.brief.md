# typeorm — architect's brief

*Rendered from the facts sheet by code; no model wrote any of it. Every cell is a field, and every fixed text on the page has a test that asserts it against the sheet it is rendered from (`tests/test_brief.py`); the tests run on a fixture, not on this page. Profile maintainability 0.2.11 + onboarding 0.2.7, geometry age, skeleton `3ed1dede165f…`, facts `7d212ebe347d…`. As of 2026-09-02, commit `ac41823b9e27`. Calibration: in-repo, self-relative (system spec §5.3), 5 package scopes pooled — per-package calibration is an open question of the mapper (architect-brief spec §5, mapper §7 Q7); one frame — stability is the `substrate timelapse` run under gate `661f93333b65`, not this page. Brief 0.32.0.*

## Register

**A position names where a room sits in a record — the import graph, the clock, the test graph, the edit record, size — and is not a claim about the room's condition (D-004 Q3). Every pNN ranks this repository's own 583 rooms, so a `>= p90` row holds a tenth of them — or more where rooms tie at the cutoff, and the rooms column says how many are tied; a single-rank row states its share, and every ranked term states the value its rank resolved to here — and no count on this page compares across repositories. A room is a source file outside the test convention with computed signals: 583 of the 3600 files with a source extension the substrate reads (manifests, documents and the rest of the tree are not counted); the 3017 test files are nodes of the import graph and not rooms.**

*583 rooms in 7 wings ((root) 3 · docker 1 · docs 9 · extra 2 · packages 69 · playground 3 · src 496); 619 diagnostic marks across all profiles (483 in the base profile), one mark per feature per room; identical pairs of diagnostic features mark 123 rooms twice (59 under one predicate in two profiles, 70 where two predicates draw one set because a conjunct excludes nothing, 6 under both); the diagnostic features name 9 distinct sets of rooms; 61 excluded marks ◌ (crack 59, toothpick_wing 2); 109 rooms carry two or more distinct diagnostic sets; gate `661f93333b65`, 7 of 8 signals asserted, none validated — asserted is a description that held under the stability budget and the corroboration its grounding class requires (validation spec §2.4), validated a forecast confirmed by a temporal holdout (validation spec §3).*

- **wing** — a directory at depth 1 of the tree (the ruleset's wing_depth), not a package; the population spans 5 package scopes, pooled (rooms per scope, largest first, each scope named by the manifest that holds it: package.json 502 · packages/codemod/package.json 65 · docs/package.json 9 · packages/legacy-naming-strategies/package.json 4 · playground/package.json 3); 219 of 11907 imports cross a package scope.
- **◌** — an excluded feature (the ruleset's word is decorative): computed and counted, excluded from the diagnosis because a signal it reads is unvalidated.
- **largest parent directory** — the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a 3rd or more of them and the feature has 6 or more rooms; a parent that shares a wing's name is marked as the parent.
- **relation to** — identity and containment, and only those, between features, diagnostic or decorative, with 3 or more rooms — and a containment the predicates guarantee at any count; two sets that overlap without one containing the other are not related here, and 'no identity or containment' says exactly that. 'By its predicate': the inner predicate conjoins every term of the outer. Otherwise the cell says which raw signals the two predicates read in common (a blend or index expanded through its declared inputs), or 'no raw signal in common' — a signal, not an instrument.
- **the import graph and the test graph** — one edge set read twice: a test file is a node whose imports count in fan_in and centrality, and test_fan_in counts those importers alone; an import-graph row says how many of its rooms' importers are test files. Centrality is PageRank over that graph: a room's rank rises with the rank of its importers, not only with their number, so a room with four well-placed importers can outrank one with thirteen. The graph is resolved statically: 30 imports in the tree did not resolve to a file (29 from test files; test_fan_in on the rooms those 29 aim at is a lower bound), and 1823 are external packages; an import the resolver did not place, or one computed at run time, is not an edge, so a room reached only that way reads as unimported there. No tsconfig.json path alias was read (none declared, or no tsconfig.json). 228 imports name a package this repository declares and resolve to its entry.
- **caveat** — the ruleset's own limit on what a predicate reads, never a claim about this repository; the count in it ('N of M here') is this repository's, beside the clause it counts.

| position (the record it reads) | feature | profile | rooms (tied at the cutoff) | by wing | largest parent directory n / rooms in it | relation to (= one set · ⊂ inside · ⊃ contains) | predicate (with the cutoffs resolved here); caveat, a limit on the predicate; or reason |
|---|---|---|---|---|---|---|---|
| long-untouched room (clock) | dark_room | maintainability | 70 (all tied at the cutoff) (the same rooms as flooded_basement) | src 70 | src/error 33 / 61 | = flooded_basement (load_index >= 0.10 excludes nothing) | `last_touched_days >= p90` — rooms at or above this repository's p90 on last_touched_days (here 1629.71 days): 70 of 583, 12.0%; the next value below the cutoff holds 2 rooms, 5.894 days under it |
| long-untouched room above the load floor (import graph and clock and size) | flooded_basement | maintainability | 70 (the same rooms as dark_room) | src 70 | src/error 33 / 61 | = dark_room (load_index >= 0.10 excludes nothing) | `last_touched_days >= p90 and load_index >= 0.10` — here p90 on last_touched_days is 1629.71 days — importers of these rooms: 442, 18 (4%) from test files — caveat: reads a floor on the load blend, not an importer (D-048): a room that nothing imports can clear the floor on inverse fan-out and size alone (1 of 70 here have no importer) |
| high-load node (import graph and size) | foundation | maintainability + onboarding (one predicate, two profiles) | 59 | packages 2 (in 1 of the wing's 2 scopes), src 57 | none holds a third | ⊃ ◌ toothpick_wing (by its predicate; 57 of these rooms outside it) | `load_index >= p90` — rooms at or above this repository's p90 on load_index (here 0.8038): 59 of 583, 10.1%; the next value below the cutoff holds 1 room, 0.0044 under it — importers of these rooms: 6443, 5078 (79%) from test files |
| high-centrality node (import graph) | hub | maintainability | 60 (6 tied at the cutoff) | src 60 | none holds a third | ⊃ corridor (by its predicate; 23 of these rooms outside it) | `centrality >= p90` — rooms at or above this repository's p90 on centrality (here 0.0023): 60 of 583, 10.3%; the next value below the cutoff holds 3 rooms, 0.0001 under it — importers of these rooms: 5878, 4738 (81%) from test files |
| recently-touched room (clock) | lit_room | maintainability | 60 (5 tied at the cutoff) | (root) 1, packages 2 (in 1 of the wing's 2 scopes), src 57 | none holds a third | no identity or containment | `last_touched_days <= p10` — rooms at or below this repository's p10 on last_touched_days (here 57.5427 days): 60 of 583, 10.3%; the next value above the cutoff holds 3 rooms, 0.4406 days over it |
| test-imported room (test graph) | scaffolding | maintainability | 164 | packages 17 (in 2 of the wing's 2 scopes), src 147 | none holds a third | no identity or containment | `reinforcement_index >= 0.5` — caveat: reads whether any file under the test convention imports the room (test_fan_in > 0, D-011): the index is 0 with no test importer and 0.5 or more with one, so 0.5 is its floor, not a midpoint; a helper or fixture under the test paths counts as a test importer, and one import suffices; a room that tests reach only through a re-exporting barrel has no test importer of its own |
| high-centrality junction with fan-out at or above the median (import graph) | corridor | onboarding | 37 | src 37 | none holds a third | ⊂ hub (by its predicate; 23 hub rooms outside this set) | `centrality >= p90 and fan_out >= p50` — here p90 on centrality is 0.0023, p50 on fan_out is 2 — importers of these rooms: 5429, 4708 (87%) from test files |
| import-graph root with fan-out at or above the upper quartile (import graph) | import_root | onboarding | 1 | packages 1 (in 1 of the wing's 2 scopes) | too few rooms to place (1) | too few rooms to relate (1) | `fan_in == 0 and fan_out >= p75` — here p75 on fan_out is 4 — caveat: reads no fan-in, not entrance (D-029): a package entry that anything imports — a room or a test file — cannot qualify, and one that nothing imports can (1 of 1 here are declared package entries) |
| imported leaf with fan-in at or above the upper quartile (import graph) | leaf_utility | onboarding | 33 | packages 4 (in 1 of the wing's 2 scopes), src 29 | none holds a third | no identity or containment | `fan_out == 0 and fan_in >= p75` — here p75 on fan_in is 6 — importers of these rooms: 605, 29 (5%) from test files |
| declared package entry (package manifest) | package_entry | onboarding | 6 | packages 2 (in 2 of the wing's 2 scopes), src 4 | src (as parent, not the wing) 4 / 5 | no identity or containment | `is_package_entry == 1` |
| high edit-pressure node (clock and edit record) | ◌ crack | maintainability | 59 | (root) 1, src 58 | none holds a third | ⊃ ◌ toothpick_wing (by its predicate; 57 of these rooms outside it) | `bug_pressure_index >= p90` — rooms at or above this repository's p90 on bug_pressure_index (here 0.76204): 59 of 583, 10.1%; the next value below the cutoff holds 1 room, 0.00104 under it — ◌ excluded from the diagnosis: bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. |
| unreinforced high-load node with high edit pressure (import graph and clock and test graph and edit record and size) | ◌ toothpick_wing | maintainability | 2 | src 2 | too few rooms to place (2) | ⊂ ◌ crack (by its predicate; 57 crack rooms outside this set); ⊂ maintainability/foundation = onboarding/foundation (by its predicate; 57 maintainability/foundation rooms outside this set); too few rooms for any other relation (2) | `load_index >= p90 and bug_pressure_index >= p90 and reinforcement_index <= 0.0` — here p90 on load_index is 0.8038, p90 on bug_pressure_index is 0.76204 — ◌ excluded from the diagnosis: bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. — importers of these rooms: 38, 0 (0%) from test files — caveat: reads test_fan_in == 0 as the graph resolved it (D-011): a room whose tests import it through an alias the resolver did not place, or only through a re-exporting barrel, reads as unreinforced |

### Rooms at the most positions (6)

**Every room at the most positions, in path order — a set, not a ranking and not a severity (D-004 Q3).**

*Every room under the most distinct diagnostic sets (6), by path — 1 room. A set is a distinct set of rooms a diagnostic feature draws (a feature under two profiles, or two features drawing one set, is one set). Rooms at fewer positions are not listed; 109 rooms carry two or more distinct sets. Size is the room's line count; importers is the room's fan_in, with the test files among them in parentheses.*

| room | lines | importers (from test files) | diagnostic features that mark it |
|---|---|---|---|
| src/index.ts | 183 | 1592 (1588) | corridor, foundation (2 profiles), hub, lit_room, package_entry, scaffolding |

### Shared rooms

*Rooms both features mark, for every pair of diagnostic features (features drawing one set of rooms share one row, named with each name); the diagonal is the feature's own count. A shared count equal to the smaller of the two features' own counts is containment, and equal to both is identity; the relation column above draws those, and only between features with 3 or more rooms or where the predicates guarantee the containment — any other pair under that floor is read here and not there.*

| shared rooms | dark_room = flooded_basement | maintainability/foundation = onboarding/foundation | hub | lit_room | scaffolding | corridor | import_root | leaf_utility | package_entry |
|---|---|---|---|---|---|---|---|---|---|
| dark_room = flooded_basement | **70** | 6 | 9 | 0 | 12 | 0 | 0 | 11 | 0 |
| maintainability/foundation = onboarding/foundation | 6 | **59** | 39 | 10 | 44 | 27 | 0 | 12 | 1 |
| hub | 9 | 39 | **60** | 9 | 30 | 37 | 0 | 11 | 1 |
| lit_room | 0 | 10 | 9 | **60** | 25 | 8 | 0 | 3 | 1 |
| scaffolding | 12 | 44 | 30 | 25 | **164** | 22 | 0 | 14 | 1 |
| corridor | 0 | 27 | 37 | 8 | 22 | **37** | 0 | 0 | 1 |
| import_root | 0 | 0 | 0 | 0 | 0 | 0 | **1** | 0 | 1 |
| leaf_utility | 11 | 12 | 11 | 3 | 14 | 0 | 0 | **33** | 0 |
| package_entry | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | **6** |

## Excluded marks (◌)

◌ crack 59 · ◌ toothpick_wing 2 — 61 marks computed and counted, excluded from the diagnosis: the signal they read (bug_pressure_index) is unvalidated; each row carries the reason.

## Stance

The diagnosis presupposes a maintenance norm — that the positions it marks are worth a visit — which the reader may reject; it is stated as an ought, not a fact (system spec, stance disclosure).

## Provenance

- brief_version: `0.32.0`
- facts_hash: `7d212ebe347d3f988b47924e4f73dc6f340c03cc916ad843d28073055cb58eeb`
- generator: `code`
