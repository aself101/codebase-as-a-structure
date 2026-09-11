# mcp-secure-server — architect's brief

*Rendered from the facts sheet by code; no model wrote any of it. The model-written reading was cut at D-049 after eleven hostile seatings found it reciting the register and everything it could add was a field. Every cell is a field, and every fixed text on the page is tested against the computation it labels (`tests/test_brief.py`). Profile maintainability + onboarding, geometry age, skeleton `f476787515a5…`, facts `2f49d59d7f72…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.19.0.*

## Register

*Rendered from the facts sheet by code (brief 0.19.0); every cell is a field, a count, or a fixed text over them; no cell is written. 202 rooms in 3 wings ((root) 2 · cookbook 136 · src 64); 287 diagnostic marks across all profiles (196 in the base profile), one mark per feature per room; identical pairs of diagnostic features mark 21 rooms twice (21 under one predicate in two profiles, 0 where two predicates draw one set because a conjunct excludes nothing, 0 under both); the diagnostic features name 10 distinct sets of rooms; 24 decorative marks (crack, toothpick_wing); 91 rooms carry two or more diagnostic marks; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis. A position names where a room sits in the record its predicate reads — the record is named beside each position — and is not a claim about its condition (D-004 Q3). The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a 3rd or more of them and the feature has 6 or more rooms; a parent that shares a wing's name is marked as the parent. The relation column draws identity and containment, and only those, between features, diagnostic or decorative, with 3 or more rooms; two sets that overlap without one containing the other are not related here, and 'no identity or containment' says exactly that. A caveat is the ruleset's own limit on what a predicate reads, never a claim about this repository. Every cell that is not a number is a cell's own answer, not a gap. The most-marked rooms and the rooms each pair of diagnostic features shares follow the table.*

| feature | profile | position | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node (edit record) | 21 | (root) 1, src 20 | none holds a third | ⊃ toothpick_wing (18 of these rooms outside it) | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room (clock) | 42 | cookbook 35, src 7 | none holds a third | ⊃ flooded_basement (5 of these rooms outside it) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched room above the load floor (import graph and clock and size) | 37 | cookbook 30, src 7 | none holds a third | ⊂ dark_room (5 dark_room rooms outside this set) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load node (import graph and size) | 21 | cookbook 7, src 14 | none holds a third | ⊃ toothpick_wing (18 of these rooms outside it); = onboarding/foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | no consequence word in the name (lexicon); a position in the import graph | 22 | cookbook 12, src 10 | none holds a third | ⊃ corridor (4 of these rooms outside it) | `centrality >= p90` |
| lit_room | maintainability | no consequence word in the name (lexicon); a position in the clock | 21 | src 21 | none holds a third | ⊃ toothpick_wing (18 of these rooms outside it) | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room (test graph) | 53 | cookbook 36, src 17 | none holds a third | no identity or containment | `reinforcement_index >= 0.5` |
| ◌ toothpick_wing | maintainability | unreinforced high-load node with high edit pressure (import graph and test graph and edit record and size) | 3 | src 3 | too few rooms to place (3) | ⊂ crack (18 crack rooms outside this set); ⊂ maintainability/foundation (18 maintainability/foundation rooms outside this set); ⊂ lit_room (18 lit_room rooms outside this set); ⊂ onboarding/foundation (18 onboarding/foundation rooms outside this set) | decorative — bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| corridor | onboarding | high-centrality junction with fan-out at or above the median (import graph) | 18 | cookbook 10, src 8 | cookbook/image-gen-server/src/providers 6 / 6 | ⊂ hub (4 hub rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load node (import graph and size) | 21 | cookbook 7, src 14 | none holds a third | = maintainability/foundation (same predicate, two profiles); ⊃ toothpick_wing (18 of these rooms outside it) | `load_index >= p90` |
| import_root | onboarding | import-graph root with fan-out at or above the upper quartile (import graph) | 17 | cookbook 17 | none holds a third | no identity or containment | `fan_in == 0 and fan_out >= p75` — caveat: reads no fan-in, not entrance (D-029): a package entry that other rooms import cannot qualify, and one that nothing imports can |
| leaf_utility | onboarding | imported leaf with fan-in at or above the upper quartile (import graph) | 19 | cookbook 13, src 6 | none holds a third | no identity or containment | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry (import graph) | 16 | cookbook 13, src 3 | none holds a third | no identity or containment | `is_package_entry == 1` |

### Most-marked rooms

*Rooms ordered by the distinct diagnostic sets marking them (a feature under two profiles, or two features drawing one set, is one set), then by marks (one per feature per profile), then by path; the first 5 are listed. 1 room carries the most (6); all are listed; a row below that count is one of the rooms at its count, first by path, and its row says how many there are (rooms under two or more marks).*

| room | distinct sets | marks | rooms at this count | diagnostic features that mark it |
|---|---|---|---|---|
| cookbook/filesystem-server/src/utils/path-validator.ts | 6 | 7 | 1 | dark_room, flooded_basement, hub, leaf_utility, maintainability/foundation, onboarding/foundation, scaffolding |
| cookbook/filesystem-server/src/utils/index.ts | 5 | 6 | 3 | corridor, dark_room, flooded_basement, hub, maintainability/foundation, onboarding/foundation |
| src/security/utils/error-sanitizer.ts | 5 | 6 | 3 | corridor, hub, lit_room, maintainability/foundation, onboarding/foundation, scaffolding |
| cookbook/api-wrapper-server/src/utils/index.ts | 5 | 5 | 3 | corridor, dark_room, flooded_basement, hub, scaffolding |
| cookbook/transaction-server/src/utils/index.ts | 4 | 5 | 7 | corridor, hub, maintainability/foundation, onboarding/foundation, scaffolding |

### Shared rooms

*Rooms both features mark, for every pair of diagnostic features (a feature under two profiles is two rows); the diagonal is the feature's own count. A shared count equal to the smaller of the two features' own counts is containment, and equal to both is identity; the relation column above draws those, and only between features with 3 or more rooms — a pair under that floor is read here and not there.*

| shared rooms | dark_room | flooded_basement | maintainability/foundation | hub | lit_room | scaffolding | corridor | onboarding/foundation | import_root | leaf_utility | package_entry |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dark_room | **42** | 37 | 2 | 6 | 0 | 12 | 5 | 2 | 4 | 2 | 0 |
| flooded_basement | 37 | **37** | 2 | 6 | 0 | 12 | 5 | 2 | 0 | 2 | 0 |
| maintainability/foundation | 2 | 2 | **21** | 11 | 7 | 12 | 9 | 21 | 0 | 5 | 0 |
| hub | 6 | 6 | 11 | **22** | 5 | 4 | 18 | 11 | 0 | 2 | 0 |
| lit_room | 0 | 0 | 7 | 5 | **21** | 6 | 5 | 7 | 0 | 2 | 1 |
| scaffolding | 12 | 12 | 12 | 4 | 6 | **53** | 3 | 12 | 0 | 14 | 2 |
| corridor | 5 | 5 | 9 | 18 | 5 | 3 | **18** | 9 | 0 | 0 | 0 |
| onboarding/foundation | 2 | 2 | 21 | 11 | 7 | 12 | 9 | **21** | 0 | 5 | 0 |
| import_root | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **17** | 0 | 10 |
| leaf_utility | 2 | 2 | 5 | 2 | 2 | 14 | 0 | 5 | 0 | **19** | 0 |
| package_entry | 0 | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 10 | 0 | **16** |

## Decorative marks

24 decorative marks render but are not a diagnosis: crack — high edit-pressure node — and toothpick_wing — unreinforced high-load node with high edit pressure — rest on bug_pressure_index, which is unvalidated.

## Stance

The diagnosis presupposes a maintenance norm — that the positions it marks are worth a visit — which the reader may reject; it is stated as an ought, not a fact (system spec, stance disclosure).

## Provenance

- brief_version: `0.19.0`
- facts_hash: `2f49d59d7f72f8cee09da45abc586ee62ca161e980d0b1af5e23464b914fcb92`
- generator: `code`
