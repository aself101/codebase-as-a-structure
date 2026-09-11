# eslint — architect's brief

*Rendered from the facts sheet by code; no model wrote any of it. The model-written reading was cut at D-049 after eleven hostile seatings found it reciting the register and everything it could add was a field. Every cell is a field, and every fixed text on the page is tested against the computation it labels (`tests/test_brief.py`). Profile maintainability + onboarding, geometry age, skeleton `9491c37335d3…`, facts `283862b57e4c…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.18.0.*

## Register

*Rendered from the facts sheet by code (brief 0.18.0); every cell is a field, no cell is a sentence. 473 rooms in 8 wings ((root) 4 · bin 1 · conf 2 · docs 30 · lib 388 · messages 18 · packages 8 · tools 22); 923 diagnostic marks across all profiles (675 in the base profile), one mark per feature per room; identical pairs of diagnostic features mark 48 rooms twice (48 under one predicate in two profiles, 0 where two predicates draw one set because a conjunct excludes nothing, 0 under both); the diagnostic features name 10 distinct sets of rooms; 49 decorative marks (crack, toothpick_wing); 254 rooms carry two or more diagnostic marks; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis. A position names where a room sits in the record its predicate reads — the record is named beside each position — and is not a claim about its condition (D-004 Q3). The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a 3rd or more of them and the feature has 6 or more rooms; a parent that shares a wing's name is marked as the parent. The relation column draws identity and containment, and only those, between features, diagnostic or decorative, with 3 or more rooms; two sets that overlap without one containing the other are not related here, and 'no identity or containment' says exactly that. A caveat is the ruleset's own limit on what a predicate reads, never a claim about this repository. Every cell that is not a number is a cell's own answer, not a gap. The most-marked rooms and the rooms each pair of diagnostic features shares follow the table.*

| feature | profile | position | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node (edit record) | 48 | (root) 2, bin 1, lib 44, packages 1 | lib/rules 35 / 293 | no identity or containment | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room (clock) | 83 | (root) 2, docs 22, lib 40, messages 11, packages 5, tools 3 | none holds a third | ⊃ flooded_basement (8 of these rooms outside it) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched room above the load floor (import graph and clock and size) | 75 | (root) 2, docs 18, lib 38, messages 11, packages 3, tools 3 | none holds a third | ⊂ dark_room (8 dark_room rooms outside this set) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load node (import graph and size) | 48 | conf 2, lib 45, tools 1 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | no consequence word in the name (lexicon); a position in the import graph | 50 | conf 2, docs 1, lib 46, packages 1 | none holds a third | ⊃ corridor (28 of these rooms outside it) | `centrality >= p90` |
| lit_room | maintainability | no consequence word in the name (lexicon); a position in the clock | 48 | (root) 2, lib 40, messages 1, tools 5 | lib/rules 24 / 293 | no identity or containment | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room (test graph) | 371 | conf 2, docs 2, lib 360, packages 1, tools 6 | lib/rules 293 / 293 | no identity or containment | `reinforcement_index >= 0.5` |
| ◌ toothpick_wing | maintainability | unreinforced high-load node with high edit pressure (import graph and test graph and edit record and size) | 1 | lib 1 | too few rooms to place (1) | too few rooms to relate (1) | decorative — bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| corridor | onboarding | high-centrality junction with fan-out at or above the median (import graph) | 22 | lib 21, packages 1 | none holds a third | ⊂ hub (28 hub rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load node (import graph and size) | 48 | conf 2, lib 45, tools 1 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| import_root | onboarding | import-graph root (import graph) | 19 | (root) 2, bin 1, docs 3, lib 2, messages 2, packages 2, tools 7 | none holds a third | no identity or containment | `fan_in == 0 and fan_out >= p75` — caveat: reads no fan-in, not entrance (§5.5): a package entry that other rooms import cannot qualify, and one that nothing imports can |
| leaf_utility | onboarding | imported leaf (import graph) | 148 | conf 2, docs 2, lib 139, messages 1, packages 2, tools 2 | lib/rules 98 / 293 | no identity or containment | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry (import graph) | 11 | bin 1, docs 1, lib 4, packages 5 | packages/eslint-config-eslint 4 / 5 (tied) | no identity or containment | `is_package_entry == 1` |

### Most-marked rooms

*12 rooms carry the most diagnostic marks (7, one per feature per profile); the first 5 by path are listed.*

| room | marks | diagnostic features that mark it |
|---|---|---|
| lib/config/default-config.js | 7 | corridor, dark_room, flooded_basement, foundation, hub, scaffolding |
| lib/languages/js/source-code/index.js | 7 | corridor, dark_room, flooded_basement, foundation, hub, scaffolding |
| lib/linter/code-path-analysis/code-path-segment.js | 7 | corridor, dark_room, flooded_basement, foundation, hub, scaffolding |
| lib/linter/index.js | 7 | corridor, dark_room, flooded_basement, foundation, hub, scaffolding |
| lib/rule-tester/index.js | 7 | corridor, dark_room, flooded_basement, foundation, hub, scaffolding |

### Shared rooms

*Rooms both features mark, for every pair of diagnostic features (a feature under two profiles is two rows); the diagonal is the feature's own count. A shared count is not a relation: identity and containment are drawn in the relation column above, and only those.*

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

## Decorative marks

49 decorative marks render but are not a diagnosis: crack — high edit-pressure node — and toothpick_wing — unreinforced high-load node with high edit pressure — rest on bug_pressure_index, which is unvalidated.

## Stance

The diagnosis presupposes a maintenance norm — that the positions it marks are worth a visit — which the reader may reject; it is stated as an ought, not a fact (system spec, stance disclosure).

## Provenance

- brief_version: `0.18.0`
- facts_hash: `283862b57e4ccdfd6671a0fabc3795ce735fd74728bb84fb5429aeffd29852ca`
- generator: `code`
