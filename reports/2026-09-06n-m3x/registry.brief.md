# uluops-registry-api — architect's brief

*The register below is rendered from the facts sheet by code and carries the inventory (D-039); the reading beneath it is model-written and linted. Register lint: **PASS on attempt 2**. What the lint checked: R1 consequence and forecast vocabulary refused outside a struck disclosure clause; R2 every citation resolves to a feature that fired on the rooms it names, with the count the skeleton records; R3 a number is on the facts sheet and sits in the sentence that cites its feature; R4 decorative features cited by count only, never as diagnosis, with their ungrounded signal named; R5 a consequence-implying name carries its position name where first used; R6 no whole-building label; R7 the diagnostic and decorative counts stated (met by the register); R8 a room named in a sentence is covered by a feature cited in that sentence; R9 features with the same or nested rooms named together (met by the register); R10 a directory named in a sentence contains a room cited in it; R11 no distributional adverb, ranking of marks, or span between rooms; R12 a number wears its unit; no ratio across units; R13 a nesting is not an identity; a shared predicate is one measurement, not two agreeing; R14 no 'validated' where no signal holds it; R15 a feature's largest directory named with its population (met by the register); R16 a feature's count in a minority wing or a directory is sayable only where that wing or directory is named; the largest wing's count is the register's; R17 a claim that a feature stands apart is checked against the register's relations. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `3d13dd5a0e47…`, facts `99fede89c59a…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.9.0; a PASS is a pass under that grammar (D-035).*

## Register

*Rendered from the facts sheet by code (brief 0.9.0); every cell is a field, no cell is a sentence. 267 rooms in 3 wings ((root) 7 · scripts 30 · src 230); 352 diagnostic marks across all profiles (280 in the base profile), one mark per feature per room — 27 of them fall on the same rooms twice (an identical pair counts each room twice): 27 where two profiles carry one predicate, 0 where two predicates draw one set because a conjunct excludes nothing; the diagnostic features name 10 distinct sets of rooms; 27 decorative marks (crack); 88 rooms carry two or more diagnostic marks; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis. A position names where a room sits — in the import graph, on the clock, in the test graph — and is not a claim about its condition (D-004 Q3). The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a third or more of them and the feature has six or more rooms; a parent that shares a wing's name is marked as the parent. Relations are drawn between sets of three or more rooms. A caveat is the ruleset's own warning about a predicate. Every cell that is not a number is a cell's own answer, not a gap.*

| feature | profile | position | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node | 27 | src 27 | none holds a third | none | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room | 27 | scripts 1, src 26 | src/db/migrations 11 / 55 | ⊃ flooded_basement (1 of these room outside it) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched, still-imported room | 26 | scripts 1, src 25 | src/db/migrations 11 / 55 | ⊂ dark_room (1 dark_room room outside this set) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load hub | 27 | src 27 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | no consequence word in the name (lexicon) | 27 | src 27 | none holds a third | ⊃ corridor (14 of these rooms outside it) | `centrality >= p90` |
| lit_room | maintainability | no consequence word in the name (lexicon) | 40 | src 40 | none holds a third | none | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room at or above the median reinforcement | 133 | src 133 | none holds a third | ⊃ corridor (120 of these rooms outside it) | `reinforcement_index >= 0.5` |
| corridor | onboarding | high-centrality, high-fan-out junction | 13 | src 13 | none holds a third | ⊂ hub (14 hub rooms outside this set); ⊂ scaffolding (120 scaffolding rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load hub | 27 | src 27 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| import_root | onboarding | import-graph root | 11 | scripts 8, src 3 | scripts (as parent, not the wing) 8 / 27 | none | `fan_in == 0 and fan_out >= p75` — caveat: reads no fan-in, not entrance (§5.5): a package entry that other rooms import cannot qualify, and one that nothing imports can |
| leaf_utility | onboarding | imported leaf | 20 | src 20 | src/utils 9 / 22 | none | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry | 1 | src 1 | too few rooms to place (1) | none | `is_package_entry == 1` |

## Reading

Three wings hold the rooms, and the scripts side is thin: 8 of the 11 import_root rooms — import_root is an import-graph root — sit in scripts [import_root ×11: scripts/calibration-gate.ts, scripts/backfill-references.ts]. Its caveat is on the sheet: the signal reads no fan-in, so a package entry that other rooms import cannot qualify and one that nothing imports can; the declared entry itself is a single room [package_entry: src/index.ts]. One dark_room room — a long-untouched room — sits in scripts [dark_room ×27: scripts/run-seed.ts], as does one flooded_basement room, a long-untouched, still-imported room [flooded_basement ×26: scripts/run-seed.ts].

The geometry is age at one end and reinforcement at the other. lit_room names 40 rooms [lit_room ×40: src/controllers/fork-controller.ts, src/services/definition/quota.ts]; scaffolding — a test-imported room at or above the median reinforcement — names 133 [scaffolding ×133: src/middleware/validate.ts, src/utils/logger.ts]; leaf_utility names 20 [leaf_utility ×20: src/utils/hash.ts, src/utils/json.ts].

Four relations bind the sets. flooded_basement sits within dark_room, and the added load_index >= 0.10 leaves 1 room outside, so these are two sets, not one [flooded_basement ×26; dark_room ×27]. maintainability/foundation and onboarding/foundation — foundation is a high-load hub — are the same predicate under two profiles, load_index >= p90 [foundation ×27; onboarding/foundation ×27]. corridor sits within hub with 14 hub rooms outside it, and separately within scaffolding with 120 rooms outside; each pair is two sets, counted twice [corridor ×13: src/db/repository/base-repository.ts; hub ×27; scaffolding ×133]. After the identical pair is counted once, the diagnosis names 10 distinct sets of rooms.

88 rooms carry two or more diagnostic marks; one of them is src/db/connection.ts, which is a corridor room, a foundation room and a hub room [corridor: src/db/connection.ts; foundation: src/db/connection.ts; hub: src/db/connection.ts].

27 decorative marks render but are not a diagnosis: crack — a high edit-pressure node — rests on bug_pressure_index, which is unvalidated [crack ×27].

The building is drawn as it is. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R13-inert; 2: pass`
- brief_version: `0.9.0`
- effort: `high`
- facts_hash: `99fede89c59aa12895f1aaf2581a2e6f4186c76517d648e5818f8ef8f15ce089`
- input_tokens: `13693`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `4391`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence and forecast vocabulary refused outside a struck disclosure clause, R2 every citation resolves to a feature that fired on the rooms it names, with the count the skeleton records, R3 a number is on the facts sheet and sits in the sentence that cites its feature, R4 decorative features cited by count only, never as diagnosis, with their ungrounded signal named, R5 a consequence-implying name carries its position name where first used, R6 no whole-building label, R7 the diagnostic and decorative counts stated (met by the register), R8 a room named in a sentence is covered by a feature cited in that sentence, R9 features with the same or nested rooms named together (met by the register), R10 a directory named in a sentence contains a room cited in it, R11 no distributional adverb, ranking of marks, or span between rooms, R12 a number wears its unit; no ratio across units, R13 a nesting is not an identity; a shared predicate is one measurement, not two agreeing, R14 no 'validated' where no signal holds it, R15 a feature's largest directory named with its population (met by the register), R16 a feature's count in a minority wing or a directory is sayable only where that wing or directory is named; the largest wing's count is the register's, R17 a claim that a feature stands apart is checked against the register's relations (D-027 through D-042).
