# mcp-secure-server — architect's brief

*The register below is rendered from the facts sheet by code and carries the inventory (D-039); the reading beneath it is model-written and linted. Register lint: **PASS on attempt 3**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `c4377f87c84e…`, facts `b338212acb80…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.6.0; a PASS is a pass under that grammar (D-035).*

## Register

*Rendered from the facts sheet by code (brief 0.6.0); every cell is a field, no cell is a sentence. 202 rooms in 3 wings ((root) 2 · cookbook 136 · src 64); 287 diagnostic marks across all profiles (196 in the base profile), one mark per feature per room; 24 decorative marks (crack, toothpick_wing); 91 rooms carry two or more diagnostic marks; gate `179d8acb7b0c`, 7 of 8 signals asserted, none validated. ◌ marks a decorative feature: excluded from the diagnosis.*

| feature | profile | position | rooms | by wing | dominant directory n / its rooms | relation to | predicate or reason |
|---|---|---|---|---|---|---|---|
| ◌ crack | maintainability | high edit-pressure node | 21 | (root) 1, src 20 | src/security/layers 4 / 9 | – | decorative — bug_pressure_index is unvalidated (D-015). |
| dark_room | maintainability | long-untouched room | 42 | cookbook 35, src 7 | cookbook/filesystem-server/src/tools 5 / 5 | ⊃ flooded_basement (5 outside it) | `last_touched_days >= p90` |
| flooded_basement | maintainability | long-untouched, still-imported room | 37 | cookbook 30, src 7 | cookbook/filesystem-server/src/tools 5 / 5 | ⊂ dark_room (5 of its rooms outside) | `last_touched_days >= p90 and load_index >= 0.10` |
| foundation | maintainability | high-load hub | 21 | cookbook 7, src 14 | src/types 3 / 6 | = foundation (same predicate, two profiles) | `load_index >= p90` |
| hub | maintainability | – | 22 | cookbook 12, src 10 | cookbook/image-gen-server/src/providers 6 / 6 | ⊃ corridor (4 outside it) | `centrality >= p90` |
| lit_room | maintainability | – | 21 | src 21 | src/security/utils 4 / 9 | – | `last_touched_days <= p10` |
| scaffolding | maintainability | test-imported room at or above the median reinforcement | 53 | cookbook 36, src 17 | src/security/utils 4 / 9 | – | `reinforcement_index >= 0.5` |
| ◌ toothpick_wing | maintainability | unreinforced high-load node with high edit pressure | 3 | src 3 | src/types 1 / 6 | – | decorative — bug_pressure_index is unvalidated on the pre-registered test set (D-015): its tuned weights assign zero to fix history and it does not beat busyness by the margin. The fragility half of this feature has no forecast to stand on; it renders as decorative, counted, and excluded from diagnostic claims until a reference repo validates the index. |
| corridor | onboarding | high-centrality, high-fan-out junction | 18 | cookbook 10, src 8 | cookbook/image-gen-server/src/providers 6 / 6 | ⊂ hub (4 of its rooms outside) | `centrality >= p90 and fan_out >= p50` |
| foundation | onboarding | high-load hub | 21 | cookbook 7, src 14 | src/types 3 / 6 | = foundation (same predicate, two profiles) | `load_index >= p90` |
| import_root | onboarding | import-graph root | 17 | cookbook 17 | cookbook/image-gen-server/src 3 / 4 | – | `fan_in == 0 and fan_out >= p75` |
| leaf_utility | onboarding | imported leaf | 19 | cookbook 13, src 6 | cookbook/nba-server/src/tools 4 / 6 | – | `fan_out == 0 and fan_in >= p75` |
| package_entry | onboarding | declared package entry | 16 | cookbook 13, src 3 | src/security/transport 1 / 8 | – | `is_package_entry == 1` |

## Reading

Three wings hold the 202 rooms: 136 in cookbook, 64 in src, 2 at the root. The cookbook wing takes all 17 rooms of import_root [import_root ×17: cookbook/nba-server/src/index.ts, cookbook/image-gen-server/src/index-debug.ts], and all 21 rooms of lit_room sit in src [lit_room ×21: src/security/presets.ts, src/security/layers/layer1-structure.ts]. scaffolding — a test-imported room at or above the median reinforcement — divides 36 in cookbook and 17 in src [scaffolding ×53: cookbook/kenpom-server/src/tools/team.ts, src/security/utils/response-validator.ts], and dark_room — a long-untouched room — sits 35 in cookbook and 7 in src [dark_room ×42: cookbook/database-server/src/utils/database.ts, src/types/messages.ts].

The graph marks fall on both sides. foundation — a high-load hub, a position in the import graph — takes 14 rooms in src and 7 in cookbook [foundation ×21: src/types/policies.ts, cookbook/monitoring-server/src/utils/alert-manager.ts]. hub takes 12 in cookbook and 10 in src [hub ×22: src/types/validation.ts]. corridor takes 10 in cookbook and 8 in src, and 6 of its 18 rooms sit in cookbook/image-gen-server/src/providers, a directory holding 6 of the building's 202 rooms [corridor ×18: cookbook/image-gen-server/src/providers/bfl.ts]. package_entry takes 13 in cookbook and 3 in src [package_entry ×16: src/security/transport/index.ts], leaf_utility 13 and 6 [leaf_utility ×19: cookbook/http-server/src/tools/echo.ts].

Three relations cut the count of distinct sets. flooded_basement — a long-untouched, still-imported room — nests inside dark_room: 37 of the 42 rooms, with 5 rooms outside it [flooded_basement ×37; dark_room ×42]. corridor nests inside hub the same way, 18 rooms with 4 outside [corridor ×18; hub ×22]. The two foundation rows are the same predicate read under two profiles, one set of 21 rooms [foundation ×21]. 91 rooms carry two or more diagnostic marks, out of 287 diagnostic marks over a base of 196.

24 decorative marks render but are not a diagnosis [crack ×21; toothpick_wing ×3]: crack — a high edit-pressure node — and toothpick_wing — an unreinforced high-load node with high edit pressure — both rest on bug_pressure_index, which is unvalidated (D-015), so their rooms are not named here.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `3`
- attempts_log: `1: R11-share, R13-inert, R13-inert; 2: R5-disclosure, R5-disclosure, R5-disclosure; 3: pass`
- brief_version: `0.6.0`
- effort: `high`
- facts_hash: `b338212acb80672d28f7f4326653cfc8c3edb7438e8cf3478313a2ac15d098f9`
- input_tokens: `13935`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `2977`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038).
