# uluops-registry-api — architect's brief

*Rendered from the facts sheet by code; no model wrote any of it. The model-written reading was cut at D-049 after eleven hostile seatings found it reciting the register and everything it could add was a field. Every cell is a field, and every fixed text on the page has a test that asserts it against the sheet it is rendered from (`tests/test_brief.py`); the tests run on a fixture, not on this page. Profile maintainability 0.2.8 + onboarding 0.2.5, geometry age, skeleton `048edec68d69…`, facts `b7930cca1d58…`. As of 2026-08-31, commit `f7414cc7bbec`. Calibration: in-repo, self-relative (system spec §5.3): every pNN ranks the 267 rooms as one population; one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is a `substrate timelapse` run under gate `179d8acb7b0c`; this page carries no stability value. Brief 0.26.0.*

## Register

**A position names where a room sits in a record — the import graph, the clock, the test graph, the edit record, size — and is not a claim about the room's condition (D-004 Q3). Every pNN ranks this repository's own 267 rooms, so a `>= p90` row holds about a tenth of them by construction, and no count on this page compares across repositories.**

*Rendered from the facts sheet by code (brief 0.26.0); every cell is a field, a count, or a fixed text over them; no cell is written. 267 rooms in 3 wings ((root) 7 · scripts 30 · src 230); 352 diagnostic marks across all profiles (280 in the base profile), one mark per feature per room; identical pairs of diagnostic features mark 27 rooms twice (27 under one predicate in two profiles, 0 where two predicates draw one set because a conjunct excludes nothing, 0 under both); the diagnostic features name 10 distinct sets of rooms; 27 excluded marks ◌ (crack 27, toothpick_wing 0); 88 rooms carry two or more distinct diagnostic sets; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated — asserted is a description confirmed by a stability budget and a cross-modal check, validated a forecast confirmed by a temporal holdout (system spec §3 and validation spec §3). A wing is a directory at depth 1 of the tree (the ruleset's wing_depth), not a package; the population spans 1 package scope (rooms per scope, largest first, each scope named by the manifest that holds it: package.json 267). ◌ marks an excluded feature (the ruleset's word is decorative): computed and counted, excluded from the diagnosis because a signal it reads is unvalidated. The record a position is read from is named beside it. The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a 3rd or more of them and the feature has 6 or more rooms; a parent that shares a wing's name is marked as the parent. The relation column draws identity and containment, and only those, between features, diagnostic or decorative, with 3 or more rooms — and a containment the predicates guarantee at any count; two sets that overlap without one containing the other are not related here, and 'no identity or containment' says exactly that. A containment says 'by its predicate' when the inner predicate conjoins every term of the outer; otherwise it says which raw signals the two predicates read in common, a blend or index expanded through its declared inputs, or 'no signal in common' — a signal, not an instrument: the import graph and the test graph are one edge set read twice, a test file is a node whose imports count in fan_in and centrality, and test_fan_in counts those importers alone. A feature that fired on no room keeps its row at 0. A caveat is the ruleset's own limit on what a predicate reads, never a claim about this repository. Every cell that is not a number is a cell's own answer, not a gap. The most-marked rooms and the rooms each pair of diagnostic features shares follow the table.*

| position (the record it reads) | feature | profile | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate; caveat or reason |
|---|---|---|---|---|---|---|---|
| high edit-pressure node (clock and edit record) | ◌ crack | maintainability | 27 | src 27 | none holds a third | no identity or containment | `bug_pressure_index >= p90` — ◌ excluded from the diagnosis: bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. |
| long-untouched room (clock) | dark_room | maintainability | 27 | scripts 1, src 26 | src/db/migrations 11 / 55 | ⊃ flooded_basement (by its predicate; 1 of these rooms outside it) | `last_touched_days >= p90` — the top 10% of rooms on this signal, by construction |
| long-untouched room above the load floor (import graph and clock and size) | flooded_basement | maintainability | 26 | scripts 1, src 25 | src/db/migrations 11 / 55 | ⊂ dark_room (by its predicate; 1 dark_room room outside this set) | `last_touched_days >= p90 and load_index >= 0.10` — caveat: reads a floor on the load blend, not an importer (D-048): a room that nothing imports can clear the floor on inverse fan-out and size alone (this case: 12 of 26 here) |
| high-load node (import graph and size) | foundation | maintainability | 27 | src 27 | none holds a third | = onboarding/foundation (same predicate, two profiles) | `load_index >= p90` — the top 10% of rooms on this signal, by construction |
| no consequence word in the name (lexicon); a position in the import graph | hub | maintainability | 27 | src 27 | none holds a third | ⊃ corridor (by its predicate; 14 of these rooms outside it) | `centrality >= p90` — the top 10% of rooms on this signal, by construction |
| no consequence word in the name (lexicon); a position in the clock | lit_room | maintainability | 40 | src 40 | none holds a third | no identity or containment | `last_touched_days <= p10` — the bottom 10% of rooms on this signal, by construction |
| test-imported room (test graph) | scaffolding | maintainability | 133 | src 133 | none holds a third | ⊃ corridor (no signal in common; 120 of these rooms outside it) | `reinforcement_index >= 0.5` — caveat: reads whether any file under the test convention imports the room (test_fan_in > 0, D-011): the index is 0 with no test importer and 0.5 or more with one, so 0.5 is its floor, not a midpoint; a helper or fixture under the test paths counts as a test importer, and one import suffices |
| unreinforced high-load node with high edit pressure (import graph and clock and test graph and edit record and size) | ◌ toothpick_wing | maintainability | 0 | no wing (0) | no rooms | no rooms to relate (0) | `load_index >= p90 and bug_pressure_index >= p90 and reinforcement_index <= 0.0` — ◌ excluded from the diagnosis: bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| high-centrality junction with fan-out at or above the median (import graph) | corridor | onboarding | 13 | src 13 | none holds a third | ⊂ hub (by its predicate; 14 hub rooms outside this set); ⊂ scaffolding (no signal in common; 120 scaffolding rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| high-load node (import graph and size) | foundation | onboarding | 27 | src 27 | none holds a third | = maintainability/foundation (same predicate, two profiles) | `load_index >= p90` — the top 10% of rooms on this signal, by construction |
| import-graph root with fan-out at or above the upper quartile (import graph) | import_root | onboarding | 11 | scripts 8, src 3 | scripts (as parent, not the wing) 8 / 27 | no identity or containment | `fan_in == 0 and fan_out >= p75` — caveat: reads no fan-in, not entrance (D-029): a package entry that other rooms import cannot qualify, and one that nothing imports can (this case: 0 of 11 here) |
| imported leaf with fan-in at or above the upper quartile (import graph) | leaf_utility | onboarding | 20 | src 20 | src/utils 9 / 22 | no identity or containment | `fan_out == 0 and fan_in >= p75` |
| declared package entry (package manifest) | package_entry | onboarding | 1 | src 1 | too few rooms to place (1) | too few rooms to relate (1) | `is_package_entry == 1` |

### Rooms at the most positions

**A count of the positions a room sits at; the order is the count, then the path — not a ranking and not a severity (D-004 Q3).**

*Rooms under two or more distinct diagnostic sets, ordered by sets (a feature under two profiles, or two features drawing one set, is one set), then by path — marks (one per feature per profile) are shown and order nothing, since within a tier they differ only by the double count the register discounts; at most 5 are listed. 2 rooms carry the most (6). The listed column is rows listed of rooms at the row's sets count; where fewer are listed than carry the count, the listed are the first by path.*

| room | positions (distinct sets) | marks | listed of rooms at this count | diagnostic features that mark it |
|---|---|---|---|---|
| src/utils/async-handler.ts | 6 | 7 | 2 of 2 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |
| src/utils/singleton.ts | 6 | 7 | 2 of 2 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |
| src/db/connection.ts | 5 | 6 | 3 of 4 (unlisted: src/terminal/styles.ts) | corridor, hub, lit_room, maintainability/foundation, onboarding/foundation, scaffolding |
| src/routes/v1/schemas.ts | 5 | 6 | 3 of 4 (unlisted: src/terminal/styles.ts) | corridor, hub, lit_room, maintainability/foundation, onboarding/foundation, scaffolding |
| src/schemas/enums.ts | 5 | 6 | 3 of 4 (unlisted: src/terminal/styles.ts) | corridor, hub, lit_room, maintainability/foundation, onboarding/foundation, scaffolding |

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

- brief_version: `0.26.0`
- facts_hash: `b7930cca1d58f15c8fcf8d864b6f023ae6f5e0974d8ab9c5d56817a19f7f3791`
- generator: `code`
