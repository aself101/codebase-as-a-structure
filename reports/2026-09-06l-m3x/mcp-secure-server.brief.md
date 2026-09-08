# mcp-secure-server — architect's brief

*The register below is rendered from the facts sheet by code and carries the inventory (D-039); the reading beneath it is model-written and linted. Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `77f25ee8558c…`, facts `26f0f1eaa522…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.8.0; a PASS is a pass under that grammar (D-035).*

## Register

*Rendered from the facts sheet by code (brief 0.8.0); every cell is a field, no cell is a sentence. 202 rooms in 3 wings ((root) 2 · cookbook 136 · src 64); 287 diagnostic marks across all profiles (196 in the base profile), one mark per feature per room — 21 of them fall on the same rooms twice because two profiles carry one predicate; the diagnostic features name 10 distinct sets of rooms; 24 decorative marks (crack, toothpick_wing); 91 rooms carry two or more diagnostic marks; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis. A position names where a room sits — in the import graph, on the clock, in the test graph — and is not a claim about its condition (D-004 Q3). The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a third or more of them and the feature has six or more rooms; a parent that shares a wing's name is marked as the parent. Relations are drawn between sets of three or more rooms. A caveat is the ruleset's own warning about a predicate. Every cell that is not a number is a cell's own answer, not a gap.*

| feature | profile | position | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node | 21 | (root) 1, src 20 | none holds a third | none | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room | 42 | cookbook 35, src 7 | none holds a third | ⊃ flooded_basement (5 of these rooms outside it) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched, still-imported room | 37 | cookbook 30, src 7 | none holds a third | ⊂ dark_room (5 dark_room rooms outside this set) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load hub | 21 | cookbook 7, src 14 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | no consequence word in the name (lexicon) | 22 | cookbook 12, src 10 | none holds a third | ⊃ corridor (4 of these rooms outside it) | `centrality >= p90` |
| lit_room | maintainability | no consequence word in the name (lexicon) | 21 | src 21 | none holds a third | none | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room at or above the median reinforcement | 53 | cookbook 36, src 17 | none holds a third | none | `reinforcement_index >= 0.5` |
| ◌ toothpick_wing | maintainability | unreinforced high-load node with high edit pressure | 3 | src 3 | too few rooms to place (3) | none | decorative — bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| corridor | onboarding | high-centrality, high-fan-out junction | 18 | cookbook 10, src 8 | cookbook/image-gen-server/src/providers 6 / 6 | ⊂ hub (4 hub rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load hub | 21 | cookbook 7, src 14 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| import_root | onboarding | import-graph root | 17 | cookbook 17 | none holds a third | none | `fan_in == 0 and fan_out >= p75` — caveat: an import-graph root in a library is not its entrance (§5.5): the package's entry has fan-in and cannot qualify |
| leaf_utility | onboarding | imported leaf | 19 | cookbook 13, src 6 | none holds a third | none | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry | 16 | cookbook 13, src 3 | none holds a third | none | `is_package_entry == 1` |

## Reading

Three wings hold this building, and the marks fall unevenly across them. In cookbook the older material sits: 35 of the 42 dark_room rooms — the position is a long-untouched room — are in cookbook, among them cookbook/filesystem-server/src/tools/read-file.ts and cookbook/database-server/src/utils/database.ts [dark_room ×42: cookbook/filesystem-server/src/tools/read-file.ts, cookbook/database-server/src/utils/database.ts]. All 21 lit_room rooms are in src, including src/security/layers/layer1-structure.ts [lit_room ×21: src/security/layers/layer1-structure.ts]. scaffolding — a test-imported room at or above the median reinforcement — has 36 of its 53 rooms in cookbook, such as cookbook/kenpom-server/src/tools/team.ts [scaffolding ×53: cookbook/kenpom-server/src/tools/team.ts]. All 17 import_root rooms are in cookbook, e.g. cookbook/nba-server/src/index.ts, and the caveat on that mark is that an import-graph root in a library is not its entrance: the package's entry has fan-in and cannot qualify [import_root ×17: cookbook/nba-server/src/index.ts]. package_entry names declared entries, including src/security/transport/index.ts [package_entry ×16: src/security/transport/index.ts].

Two of the marks are nested inside others. flooded_basement — a long-untouched, still-imported room — lies within dark_room at 37 rooms; the added conjunct load_index >= 0.10 leaves 5 dark_room rooms outside it, so these are two sets, not one [flooded_basement ×37; dark_room ×42]. corridor lies within hub at 18 rooms, with 4 hub rooms outside the fan_out >= p50 conjunct; cookbook/image-gen-server/src/providers/openai.ts carries both [corridor ×18: cookbook/image-gen-server/src/providers/openai.ts; hub ×22: cookbook/image-gen-server/src/providers/openai.ts].

One pair is an identity. foundation — a high-load hub — is the same predicate under the maintainability and the onboarding profile, load_index >= p90, naming one set of 21 rooms twice, src/types/policies.ts among them [foundation ×21: src/types/policies.ts; onboarding/foundation ×21].

After that identity and the two nestings, the diagnosis names 10 distinct sets of rooms, and 91 rooms carry two or more diagnostic marks; src/security/utils/error-sanitizer.ts is one, held by scaffolding and by hub [scaffolding: src/security/utils/error-sanitizer.ts; hub: src/security/utils/error-sanitizer.ts].

24 decorative marks render but are not a diagnosis [crack ×21; toothpick_wing ×3]: crack, a high edit-pressure node, and toothpick_wing, an unreinforced high-load node with high edit pressure, rest on bug_pressure_index, which is unvalidated.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R2-provenance, R2-provenance; 2: pass`
- brief_version: `0.8.0`
- effort: `high`
- facts_hash: `26f0f1eaa5227c4f0b7313dadc9cab681106f52177936917f9a95988b9066fda`
- input_tokens: `14732`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `4052`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038); R16 a feature's by-wing or directory number is sayable only where the wing or directory is named (D-040, D-041), R17 a claim of no relation is checked against the overlaps (D-041).
