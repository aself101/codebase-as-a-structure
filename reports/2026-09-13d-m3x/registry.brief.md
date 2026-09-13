# uluops-registry-api — architect's brief

*Rendered from the facts sheet by code; no model wrote any of it. Every cell is a field, and every fixed text on the page has a test that asserts it against the sheet it is rendered from (`tests/test_brief.py`); the tests run on a fixture, not on this page. Profile maintainability 0.3.1 + onboarding 0.3.0, geometry age, skeleton `7334b60b60c5…`, facts `31a9430bf8cf…`. As of 2026-09-13, commit `e947c5b67542`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is the `substrate timelapse` run under gate `e28401778e67`, not this page. Brief 0.34.0.*

## Register

**A position names where a room sits in a record — the import graph, the clock, the test graph, the edit record, size — and is not a claim about the room's condition (D-004 Q3). Every pNN ranks this repository's own 206 rooms, so a `>= p90` row holds a tenth of them — or more where rooms tie at the cutoff, and the rooms column says how many are tied; a single-rank row states its share, and every ranked term states the value its rank resolved to here — and no count on this page compares across repositories. A room is a source file outside the test convention (a path matching `**/*.test.*`, `**/*.spec.*`, `**/*_test.*`, `**/test_*.py`, `**/test/**`, `**/tests/**`, `**/__tests__/**`, `**/spec/**`, `**/__mocks__/**`) with computed signals, and not a config or migration or placeholder file (kinds the ruleset does not count as rooms): 206 of the 456 files with a source extension the substrate reads (manifests, documents and the rest of the tree are not counted); the 189 test files are nodes of the import graph and not rooms; the 61 files of a kind the ruleset does not count (config 6, migration 55) are in the graph and not a room.**

*206 rooms in 3 wings ((root) 1 · scripts 30 · src 175); 319 diagnostic marks across all profiles (263 in the base profile), one mark per feature per room; identical pairs of diagnostic features mark 21 rooms twice (21 under one predicate in two profiles, 0 where two predicates draw one set because a conjunct excludes nothing, 0 under both); the diagnostic features name 10 distinct sets of rooms; 21 excluded marks ◌ (crack 21, toothpick_wing 0); 76 rooms carry two or more distinct diagnostic sets; gate `e28401778e67`, 7 of 8 signals asserted, none validated — asserted is a description that held under the stability budget and the corroboration its grounding class requires (validation spec §2.4), validated a forecast confirmed by a temporal holdout (validation spec §3).*

- **wing** — a directory at depth 1 of the tree (the ruleset's wing_depth), not a package; the population is one package scope (package.json).
- **◌** — a feature excluded from the diagnosis (the ruleset's word is decorative): computed and counted, not claimed, because a signal it reads is unvalidated. 'Excluded' on this page means this and nothing else; a file kind the ruleset does not count as a room is said in those words.
- **largest parent directory** — the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a 3rd or more of them and the feature has 6 or more rooms; a parent that shares a wing's name is marked as the parent.
- **relation to** — identity and containment, and only those, between features, diagnostic or decorative, with 3 or more rooms — and a containment the predicates guarantee at any count; two sets that overlap without one containing the other are not related here, and 'no identity or containment' says exactly that. 'By its predicate': the inner predicate conjoins every term of the outer. Otherwise the cell says which raw signals the two predicates read in common (a blend or index expanded through its declared inputs), or 'no raw signal in common' — a signal, not an instrument.
- **the import graph and the test graph** — one edge set read twice: a test file is a node whose imports count in fan_in and centrality, and test_fan_in counts those importers alone; an import-graph row says how many of its rooms' importers are test files. Centrality is PageRank over that graph: a room's rank rises with the rank of its importers, not only with their number, so a room with 4 well-placed importers can outrank one with 16 (here src/config/database.ts at 4 is a hub and src/utils/async-handler.ts at 16 is not). The graph is resolved statically: 0 imports in the tree did not resolve to a file, and 565 are external packages; an import the resolver did not place, or one computed at run time, is not an edge, so a room reached only that way reads as unimported there. No tsconfig.json path alias was read (none declared, or no tsconfig.json).
- **caveat** — the ruleset's own limit on what a predicate reads, never a claim about this repository; the count in it ('N of M here') is this repository's, beside the clause it counts.

| position (the record it reads) | feature | profile | rooms (tied at the cutoff) | by wing | largest parent directory n / rooms in it | relation to (= one set · ⊂ inside · ⊃ contains) | predicate (with the cutoffs resolved here); caveat, a limit on the predicate; or reason |
|---|---|---|---|---|---|---|---|
| long-untouched room (clock) | dark_room | maintainability | 34 (18 tied at the cutoff) | scripts 1, src 33 | none holds a third | ⊃ flooded_basement (by its predicate; 1 of these rooms outside it) | `last_touched_days >= p90` — rooms at or above this repository's p90 on last_touched_days (here 189.792 days): 34 of 206, 16.5%; the next value below the cutoff holds 1 room, 1.664 days under it |
| long-untouched room above the load floor (import graph and clock and size) | flooded_basement | maintainability | 33 (1 have no importer) | scripts 1, src 32 | none holds a third | ⊂ dark_room (by its predicate; 1 dark_room room outside this set) | `last_touched_days >= p90 and load_index >= 0.10` — here p90 on last_touched_days is 189.792 days — importers of these rooms: 138, 25 (18%) from test files — caveat: reads a floor on the load blend, not an importer (D-048): a room that nothing imports can clear the floor on inverse fan-out and size alone (1 of 33 here have no importer) |
| high-load node (import graph and size) | foundation | maintainability + onboarding (one predicate, two profiles) | 21 | src 21 | none holds a third | ⊂ scaffolding (no raw signal in common, one edge set read twice; 112 scaffolding rooms outside this set) | `load_index >= p90` — rooms at or above this repository's p90 on load_index (here 0.8108): 21 of 206, 10.2%; the next value below the cutoff holds 1 room, 0.0002 under it — importers of these rooms: 466, 119 (26%) from test files |
| high-centrality node (import graph) | hub | maintainability | 21 | src 21 | none holds a third | ⊃ corridor (by its predicate; 13 of these rooms outside it) | `centrality >= p90` — rooms at or above this repository's p90 on centrality (here 0.00525): 21 of 206, 10.2%; the next value below the cutoff holds 1 room, 5e-05 under it — importers of these rooms: 434, 114 (26%) from test files |
| recently-touched room (clock) | lit_room | maintainability | 21 | src 21 | none holds a third | no identity or containment | `last_touched_days <= p10` — rooms at or below this repository's p10 on last_touched_days (here 20.126 days): 21 of 206, 10.2%; the next value above the cutoff holds 1 room, 0.04955 days over it |
| test-imported room (test graph) | scaffolding | maintainability | 133 | src 133 | none holds a third | ⊃ ◌ crack (no raw signal in common, one edge set read twice; 112 of these rooms outside it); ⊃ maintainability/foundation (no raw signal in common, one edge set read twice; 112 of these rooms outside it); ⊃ corridor (no raw signal in common, one edge set read twice; 125 of these rooms outside it); ⊃ onboarding/foundation (no raw signal in common, one edge set read twice; 112 of these rooms outside it) | `reinforcement_index >= 0.5` — caveat: reads whether any file under the test convention imports the room (test_fan_in > 0, D-011): the index is 0 with no test importer and 0.5 or more with one, so 0.5 is its floor, not a midpoint; a helper or fixture under the test paths counts as a test importer, and one import suffices; a room that tests reach only through a re-exporting barrel, or load by a path computed at run time, has no test importer of its own |
| high-centrality junction with fan-out at or above the median (import graph) | corridor | onboarding | 8 | src 8 | none holds a third | ⊂ hub (by its predicate; 13 hub rooms outside this set); ⊂ scaffolding (no raw signal in common, one edge set read twice; 125 scaffolding rooms outside this set) | `centrality >= p90 and fan_out >= p50` — here p90 on centrality is 0.00525, p50 on fan_out is 2 — importers of these rooms: 191, 44 (23%) from test files |
| import-graph root with fan-out at or above the upper quartile (import graph) | import_root | onboarding | 10 (0 are declared package entries) | scripts 7, src 3 | scripts (as parent, not the wing) 7 / 27 | no identity or containment | `fan_in == 0 and fan_out >= p75` — here p75 on fan_out is 5 — caveat: reads no fan-in, not entrance (D-029): a package entry that anything imports — a room or a test file — cannot qualify, and one that nothing imports can (0 of 10 here are declared package entries) |
| imported leaf with fan-in at or above the upper quartile (import graph) | leaf_utility | onboarding | 16 | src 16 | src/utils 9 / 22 | no identity or containment | `fan_out == 0 and fan_in >= p75` — here p75 on fan_in is 5 — importers of these rooms: 254, 76 (30%) from test files |
| declared package entry (package manifest) | package_entry | onboarding | 1 | src 1 | too few rooms to place (1) | too few rooms to relate (1) | `is_package_entry == 1` |
| high edit-pressure node (clock and edit record) | ◌ crack | maintainability | 21 | src 21 | none holds a third | ⊂ scaffolding (no raw signal in common, one edge set read twice; 112 scaffolding rooms outside this set) | `bug_pressure_index >= p90` — rooms at or above this repository's p90 on bug_pressure_index (here 0.77095): 21 of 206, 10.2%; the next value below the cutoff holds 1 room, 0.00205 under it — ◌ excluded from the diagnosis: bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. |
| unreinforced high-load node with high edit pressure (import graph and clock and test graph and edit record and size) | ◌ toothpick_wing | maintainability | 0 | no wing (0) | no rooms | no rooms to relate (0) | `load_index >= p90 and bug_pressure_index >= p90 and reinforcement_index <= 0.0` — here p90 on load_index unresolved, p90 on bug_pressure_index unresolved — ◌ excluded from the diagnosis: bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. — caveat: reads test_fan_in == 0 as the graph resolved it (D-011): a room whose tests import it through an alias the resolver did not place, or only through a re-exporting barrel, or only by a path computed at run time, reads as unreinforced |

### Rooms at the most positions (6)

**Every room at the most positions, in path order — a set, not a ranking and not a severity (D-004 Q3).**

*Every room under the most distinct diagnostic sets (6), by path — 1 room. A set is a distinct set of rooms a diagnostic feature draws (a feature under two profiles, or two features drawing one set, is one set). Rooms at fewer positions are not listed; 76 rooms carry two or more distinct sets. Size is the room's line count; importers is the room's fan_in, with the test files among them in parentheses.*

| room | lines | importers (from test files) | diagnostic features that mark it |
|---|---|---|---|
| src/utils/singleton.ts | 34 | 18 (1) | dark_room, flooded_basement, foundation (2 profiles), hub, leaf_utility, scaffolding |

### Shared rooms

*Rooms both features mark, for every pair of diagnostic features (features drawing one set of rooms share one row, named with each name); the diagonal is the feature's own count. A shared count equal to the smaller of the two features' own counts is containment, and equal to both is identity; the relation column above draws those, and only between features with 3 or more rooms or where the predicates guarantee the containment — any other pair under that floor is read here and not there.*

| shared rooms | dark_room | flooded_basement | maintainability/foundation = onboarding/foundation | hub | lit_room | scaffolding | corridor | import_root | leaf_utility | package_entry |
|---|---|---|---|---|---|---|---|---|---|---|
| dark_room | **34** | 33 | 2 | 2 | 0 | 16 | 0 | 0 | 4 | 0 |
| flooded_basement | 33 | **33** | 2 | 2 | 0 | 16 | 0 | 0 | 4 | 0 |
| maintainability/foundation = onboarding/foundation | 2 | 2 | **21** | 15 | 3 | 21 | 6 | 0 | 11 | 0 |
| hub | 2 | 2 | 15 | **21** | 2 | 20 | 8 | 0 | 10 | 0 |
| lit_room | 0 | 0 | 3 | 2 | **21** | 20 | 1 | 0 | 0 | 1 |
| scaffolding | 16 | 16 | 21 | 20 | 20 | **133** | 8 | 0 | 15 | 1 |
| corridor | 0 | 0 | 6 | 8 | 1 | 8 | **8** | 0 | 0 | 0 |
| import_root | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **10** | 0 | 0 |
| leaf_utility | 4 | 4 | 11 | 10 | 0 | 15 | 0 | 0 | **16** | 0 |
| package_entry | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | **1** |

## Marks excluded from the diagnosis (◌)

◌ crack 21 · ◌ toothpick_wing 0 — 21 marks computed and counted, excluded from the diagnosis: the signal they read (bug_pressure_index) is unvalidated; each row carries the reason.

## Stance

The diagnosis presupposes a maintenance norm — that the positions it marks are worth a visit — which the reader may reject; it is stated as an ought, not a fact (system spec, stance disclosure).

## Provenance

- brief_version: `0.34.0`
- facts_hash: `31a9430bf8cf4bccf85d7cec3199257b084b2858640b8080ca8d3074233a4dad`
- generator: `code`
