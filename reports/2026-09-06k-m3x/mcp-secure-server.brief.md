# mcp-secure-server — architect's brief

*The register below is rendered from the facts sheet by code and carries the inventory (D-039); the reading beneath it is model-written and linted. Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `c4377f87c84e…`, facts `5c714bc205fe…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.7.0; a PASS is a pass under that grammar (D-035).*

## Register

*Rendered from the facts sheet by code (brief 0.7.0); every cell is a field, no cell is a sentence. 202 rooms in 3 wings ((root) 2 · cookbook 136 · src 64); 287 diagnostic marks across all profiles (196 in the base profile), one mark per feature per room — 21 of them fall on the same rooms twice because two profiles carry one predicate; the diagnostic features name 10 distinct sets of rooms; 24 decorative marks (crack, toothpick_wing); 91 rooms carry two or more diagnostic marks; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis. A position names where a room sits — in the import graph, on the clock, in the test graph — and is not a claim about its condition (D-004 Q3). The directory column is the immediate parent (non-recursive) holding the most of a feature's rooms, shown only when it holds a third or more of them; 'none' is a cell's own answer, not a gap.*

| feature | profile | position | rooms | by wing | largest parent directory n / rooms in it | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node | 21 | (root) 1, src 20 | none holds a third | none | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room | 42 | cookbook 35, src 7 | none holds a third | ⊃ flooded_basement (5 of these rooms outside it) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched, still-imported room | 37 | cookbook 30, src 7 | none holds a third | ⊂ dark_room (5 dark_room rooms outside this set) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load hub | 21 | cookbook 7, src 14 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | no consequence in the name | 22 | cookbook 12, src 10 | none holds a third | ⊃ corridor (4 of these rooms outside it) | `centrality >= p90` |
| lit_room | maintainability | no consequence in the name | 21 | src 21 | none holds a third | none | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room at or above the median reinforcement | 53 | cookbook 36, src 17 | none holds a third | none | `reinforcement_index >= 0.5` |
| ◌ toothpick_wing | maintainability | unreinforced high-load node with high edit pressure | 3 | src 3 | none holds a third | none | decorative — bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| corridor | onboarding | high-centrality, high-fan-out junction | 18 | cookbook 10, src 8 | cookbook/image-gen-server/src/providers 6 / 6 | ⊂ hub (4 hub rooms outside this set) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load hub | 21 | cookbook 7, src 14 | none holds a third | = foundation (same predicate, two profiles) | `load_index >= p90` |
| import_root | onboarding | import-graph root | 17 | cookbook 17 | none holds a third | none | `fan_in == 0 and fan_out >= p75` |
| leaf_utility | onboarding | imported leaf | 19 | cookbook 13, src 6 | none holds a third | none | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry | 16 | cookbook 13, src 3 | none holds a third | none | `is_package_entry == 1` |

## Reading

Three wings carry the rooms: cookbook, src, and a root holding. The import-graph roots stand in cookbook [import_root ×17: cookbook/http-server/src/index.ts, cookbook/nba-server/src/index.ts], and the declared package entries stand beside them and in src as well [package_entry ×16: cookbook/tool-policies-server/src/index.ts, src/security/transport/index.ts]. Recently touched rooms sit in src [lit_room ×21: src/security/presets.ts, src/security/layers/layer1-structure.ts], while scaffolding — a test-imported room at or above the median reinforcement — reaches both principal wings [scaffolding ×53: cookbook/kenpom-server/src/tools/ratings.ts, src/security/utils/response-validator.ts], as do the imported leaves [leaf_utility ×19: cookbook/nba-server/src/tools/live.ts, src/security/layers/contextual-config-builder.ts].

Two of the marks nest. flooded_basement — a long-untouched, still-imported room — names 37 rooms that sit within dark_room, a long-untouched room, and the load_index >= 0.10 conjunct leaves 5 rooms of dark_room outside it; these are two sets, not one [flooded_basement ×37: cookbook/database-server/src/utils/database.ts; dark_room ×42: cookbook/image-gen-server/src/index-minimal.ts]. corridor, a high-centrality, high-fan-out junction, names 18 rooms that sit within hub, with 4 rooms of hub left outside by the fan_out >= p50 conjunct [corridor ×18: cookbook/image-gen-server/src/providers/openai.ts; hub ×22: src/types/validation.ts].

The third relation is an identity: foundation — a high-load hub — carries the same predicate, load_index >= p90, under both profiles and names the same 21 rooms, so 21 marks land twice on one set [foundation ×21: src/types/policies.ts, cookbook/monitoring-server/src/utils/alert-manager.ts]. Counted with the identical pair once and each nesting twice, the diagnosis names 10 distinct sets of rooms, and 91 rooms carry two or more diagnostic marks [foundation ×21].

24 decorative marks render but are not a diagnosis [crack ×21; toothpick_wing ×3]: crack, a high edit-pressure node, and toothpick_wing, an unreinforced high-load node with high edit pressure, rest on bug_pressure_index, which is unvalidated.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R12-unit; 2: pass`
- brief_version: `0.7.0`
- effort: `high`
- facts_hash: `5c714bc205fea169338367f2e78ef9dd5017abe63b831814901ef33598a2a691`
- input_tokens: `14242`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `4394`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038); R16 the reading does not restate the register's by-wing and directory cells (D-040).
