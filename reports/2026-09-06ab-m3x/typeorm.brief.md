# typeorm — architect's brief

*Rendered from the facts sheet by code; no model wrote any of it. The model-written reading was cut at D-049 after eleven hostile seatings found it reciting the register and everything it could add was a field. Every cell is a field, and every fixed text on the page is tested against the computation it labels (`tests/test_brief.py`). Profile maintainability + onboarding, geometry age, skeleton `61eb77132d34…`, facts `d40c05d4ce9e…`. Calibration: in-repo, self-relative (system spec §5.3): every pNN ranks the 583 rooms as one population, across 5 package scopes (package.json) pooled — per-package calibration is an open question of the mapper (architect-brief spec §5, mapper §7 Q7); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.24.0.*

## Register

*Rendered from the facts sheet by code (brief 0.24.0); every cell is a field, a count, or a fixed text over them; no cell is written. 583 rooms in 7 wings ((root) 3 · docker 1 · docs 9 · extra 2 · packages 69 · playground 3 · src 496); 619 diagnostic marks across all profiles (483 in the base profile), one mark per feature per room; identical pairs of diagnostic features mark 123 rooms twice (59 under one predicate in two profiles, 70 where two predicates draw one set because a conjunct excludes nothing, 6 under both); the diagnostic features name 9 distinct sets of rooms; 61 decorative marks (crack, toothpick_wing); 109 rooms carry two or more distinct diagnostic sets; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. A wing is a directory at depth 1 of the tree (the ruleset's wing_depth), not a package; the population spans 5 package scopes (rooms per scope, largest first, each scope named by the manifest that holds it: package.json 502 · packages/codemod/package.json 65 · docs/package.json 9 · packages/legacy-naming-strategies/package.json 4 · playground/package.json 3). ◌ marks a decorative feature: excluded from the diagnosis. A position names where a room sits in the record its predicate reads — the record is named beside each position — and is not a claim about its condition (D-004 Q3). The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a 3rd or more of them and the feature has 6 or more rooms; a parent that shares a wing's name is marked as the parent. The relation column draws identity and containment, and only those, between features, diagnostic or decorative, with 3 or more rooms — and a containment the predicates guarantee at any count; two sets that overlap without one containing the other are not related here, and 'no identity or containment' says exactly that. A caveat is the ruleset's own limit on what a predicate reads, never a claim about this repository. Every cell that is not a number is a cell's own answer, not a gap. The most-marked rooms and the rooms each pair of diagnostic features shares follow the table.*

| feature | profile | position | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate; caveat or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node (clock and edit record) | 59 | (root) 1, src 58 | none holds a third | ⊃ ◌ toothpick_wing (by its predicate; 57 of these rooms outside it) | `bug_pressure_index >= p90` — decorative: bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. |
| dark_room | maintainability | long-untouched room (clock) | 70 | src 70 | src/error 33 / 61 | = flooded_basement (load_index >= 0.10 excludes nothing) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched room above the load floor (import graph and clock and size) | 70 | src 70 | src/error 33 / 61 | = dark_room (load_index >= 0.10 excludes nothing) | `last_touched_days >= p90 and load_index >= 0.10` — caveat: reads a floor on the load blend, not an importer (D-048): a room that nothing imports can clear the floor on inverse fan-out and size alone |
| foundation | maintainability | high-load node (import graph and size) | 59 | packages 2, src 57 | none holds a third | ⊃ ◌ toothpick_wing (by its predicate; 57 of these rooms outside it); = onboarding/foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | no consequence word in the name (lexicon); a position in the import graph | 60 | src 60 | none holds a third | ⊃ corridor (by its predicate; 23 of these rooms outside it) | `centrality >= p90` |
| lit_room | maintainability | no consequence word in the name (lexicon); a position in the clock | 60 | (root) 1, packages 2, src 57 | none holds a third | no identity or containment | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room (test graph) | 164 | packages 17, src 147 | none holds a third | no identity or containment | `reinforcement_index >= 0.5` |
| ◌ toothpick_wing | maintainability | unreinforced high-load node with high edit pressure (import graph and clock and test graph and edit record and size) | 2 | src 2 | too few rooms to place (2) | ⊂ ◌ crack (by its predicate; 57 crack rooms outside this set); ⊂ maintainability/foundation = onboarding/foundation (by its predicate; 57 maintainability/foundation rooms outside this set); too few rooms for any other relation (2) | `load_index >= p90 and bug_pressure_index >= p90 and reinforcement_index <= 0.0` — decorative: bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| corridor | onboarding | high-centrality junction with fan-out at or above the median (import graph) | 37 | src 37 | none holds a third | ⊂ hub (by its predicate; 23 hub rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load node (import graph and size) | 59 | packages 2, src 57 | none holds a third | = maintainability/foundation (same predicate, two profiles); ⊃ ◌ toothpick_wing (by its predicate; 57 of these rooms outside it) | `load_index >= p90` |
| import_root | onboarding | import-graph root with fan-out at or above the upper quartile (import graph) | 1 | packages 1 | too few rooms to place (1) | too few rooms for any other relation (1) | `fan_in == 0 and fan_out >= p75` — caveat: reads no fan-in, not entrance (D-029): a package entry that other rooms import cannot qualify, and one that nothing imports can |
| leaf_utility | onboarding | imported leaf with fan-in at or above the upper quartile (import graph) | 33 | packages 4, src 29 | none holds a third | no identity or containment | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry (package manifest) | 6 | packages 2, src 4 | src (as parent, not the wing) 4 / 5 | no identity or containment | `is_package_entry == 1` |

### Most-marked rooms

*Rooms under two or more distinct diagnostic sets, ordered by sets (a feature under two profiles, or two features drawing one set, is one set), then by path — marks (one per feature per profile) are shown and order nothing, since within a tier they differ only by the double count the register discounts; at most 5 are listed. 1 room carries the most (6). The listed column is rows listed of rooms at the row's sets count; where fewer are listed than carry the count, the listed are the first by path.*

| room | distinct sets | marks | listed of rooms at this count | diagnostic features that mark it |
|---|---|---|---|---|
| src/index.ts | 6 | 7 | 1 of 1 | corridor, hub, lit_room, maintainability/foundation, onboarding/foundation, package_entry, scaffolding |
| src/common/ObjectLiteral.ts | 5 | 7 | 4 of 8 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |
| src/data-source/DataSource.ts | 5 | 6 | 4 of 8 | corridor, hub, lit_room, maintainability/foundation, onboarding/foundation, scaffolding |
| src/decorator/columns/PrimaryGeneratedColumn.ts | 5 | 6 | 4 of 8 | corridor, hub, lit_room, maintainability/foundation, onboarding/foundation, scaffolding |
| src/decorator/options/ValueTransformer.ts | 5 | 7 | 4 of 8 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |

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

## Decorative marks

61 decorative marks render but are not a diagnosis: crack — high edit-pressure node — and toothpick_wing — unreinforced high-load node with high edit pressure — rest on bug_pressure_index, which is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin.

## Stance

The diagnosis presupposes a maintenance norm — that the positions it marks are worth a visit — which the reader may reject; it is stated as an ought, not a fact (system spec, stance disclosure).

## Provenance

- brief_version: `0.24.0`
- facts_hash: `d40c05d4ce9ec4d2e1fabd8fc830c92922c3b9f98392560689b36450c5f68631`
- generator: `code`
