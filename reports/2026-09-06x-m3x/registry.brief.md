# uluops-registry-api — architect's brief

*Rendered from the facts sheet by code; no model wrote any of it. The model-written reading was cut at D-049 after eleven hostile seatings found it reciting the register and everything it could add was a field. Every cell is a field, and every fixed text on the page is tested against the computation it labels (`tests/test_brief.py`). Profile maintainability + onboarding, geometry age, skeleton `8be45cb6b80b…`, facts `71879ade7d1e…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.20.0.*

## Register

*Rendered from the facts sheet by code (brief 0.20.0); every cell is a field, a count, or a fixed text over them; no cell is written. 267 rooms in 3 wings ((root) 7 · scripts 30 · src 230); 352 diagnostic marks across all profiles (280 in the base profile), one mark per feature per room; identical pairs of diagnostic features mark 27 rooms twice (27 under one predicate in two profiles, 0 where two predicates draw one set because a conjunct excludes nothing, 0 under both); the diagnostic features name 10 distinct sets of rooms; 27 decorative marks (crack); 88 rooms carry two or more distinct diagnostic sets; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis. A position names where a room sits in the record its predicate reads — the record is named beside each position — and is not a claim about its condition (D-004 Q3). The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a 3rd or more of them and the feature has 6 or more rooms; a parent that shares a wing's name is marked as the parent. The relation column draws identity and containment, and only those, between features, diagnostic or decorative, with 3 or more rooms; two sets that overlap without one containing the other are not related here, and 'no identity or containment' says exactly that. A caveat is the ruleset's own limit on what a predicate reads, never a claim about this repository. Every cell that is not a number is a cell's own answer, not a gap. The most-marked rooms and the rooms each pair of diagnostic features shares follow the table.*

| feature | profile | position | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node (edit record) | 27 | src 27 | none holds a third | no identity or containment | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room (clock) | 27 | scripts 1, src 26 | src/db/migrations 11 / 55 | ⊃ flooded_basement (1 of these room outside it) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched room above the load floor (import graph and clock and size) | 26 | scripts 1, src 25 | src/db/migrations 11 / 55 | ⊂ dark_room (1 dark_room room outside this set) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load node (import graph and size) | 27 | src 27 | none holds a third | = onboarding/foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | no consequence word in the name (lexicon); a position in the import graph | 27 | src 27 | none holds a third | ⊃ corridor (14 of these rooms outside it) | `centrality >= p90` |
| lit_room | maintainability | no consequence word in the name (lexicon); a position in the clock | 40 | src 40 | none holds a third | no identity or containment | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room (test graph) | 133 | src 133 | none holds a third | ⊃ corridor (120 of these rooms outside it) | `reinforcement_index >= 0.5` |
| corridor | onboarding | high-centrality junction with fan-out at or above the median (import graph) | 13 | src 13 | none holds a third | ⊂ hub (14 hub rooms outside this set); ⊂ scaffolding (120 scaffolding rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load node (import graph and size) | 27 | src 27 | none holds a third | = maintainability/foundation (same predicate, two profiles) | `load_index >= p90` |
| import_root | onboarding | import-graph root with fan-out at or above the upper quartile (import graph) | 11 | scripts 8, src 3 | scripts (as parent, not the wing) 8 / 27 | no identity or containment | `fan_in == 0 and fan_out >= p75` — caveat: reads no fan-in, not entrance (D-029): a package entry that other rooms import cannot qualify, and one that nothing imports can |
| leaf_utility | onboarding | imported leaf with fan-in at or above the upper quartile (import graph) | 20 | src 20 | src/utils 9 / 22 | no identity or containment | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry (package manifest) | 1 | src 1 | too few rooms to place (1) | too few rooms to relate (1) | `is_package_entry == 1` |

### Most-marked rooms

*Rooms under two or more distinct diagnostic sets, ordered by sets (a feature under two profiles, or two features drawing one set, is one set), then by marks (one per feature per profile), then by path; at most 5 are listed. 2 rooms carry the most (6). The listed column is rows listed of rooms at the row's sets count; where fewer are listed than carry the count, the listed are the first by path.*

| room | distinct sets | marks | listed of rooms at this count | diagnostic features that mark it |
|---|---|---|---|---|
| src/utils/async-handler.ts | 6 | 7 | 2 of 2 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |
| src/utils/singleton.ts | 6 | 7 | 2 of 2 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |
| src/db/connection.ts | 5 | 6 | 3 of 4 | corridor, hub, lit_room, maintainability/foundation, onboarding/foundation, scaffolding |
| src/routes/v1/schemas.ts | 5 | 6 | 3 of 4 | corridor, hub, lit_room, maintainability/foundation, onboarding/foundation, scaffolding |
| src/schemas/enums.ts | 5 | 6 | 3 of 4 | corridor, hub, lit_room, maintainability/foundation, onboarding/foundation, scaffolding |

### Shared rooms

*Rooms both features mark, for every pair of diagnostic features (a feature under two profiles is two rows); the diagonal is the feature's own count. A shared count equal to the smaller of the two features' own counts is containment, and equal to both is identity; the relation column above draws those, and only between features with 3 or more rooms — a pair under that floor is read here and not there.*

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

## Decorative marks

27 decorative marks render but are not a diagnosis: crack — high edit-pressure node — rest on bug_pressure_index, which is unvalidated.

## Stance

The diagnosis presupposes a maintenance norm — that the positions it marks are worth a visit — which the reader may reject; it is stated as an ought, not a fact (system spec, stance disclosure).

## Provenance

- brief_version: `0.20.0`
- facts_hash: `71879ade7d1efabe716e2649dd54c5572447ca5e7e188ddbe7f7399e7d04899c`
- generator: `code`
