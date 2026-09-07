# mcp-secure-server — architect's brief

*Register lint: **PASS on attempt 1**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `c4377f87c84e…`, facts `84490af05150…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.5.0; a PASS is a pass under that grammar (D-035).*

The building holds 202 rooms in 3 wings: 136 in cookbook, 64 in src, 2 at the root. Across all profiles 287 diagnostic marks land, 196 of them in the base profile, and 91 rooms carry two or more diagnostic marks. One set of 21 rooms carries the same predicate under two profiles, maintainability/foundation and onboarding/foundation — a high-load hub, a position in the import graph, not a claim about outcomes [foundation ×21; onboarding/foundation ×21].

The age geometry marks 42 rooms as dark_room — a long-untouched room — 35 of them in cookbook and 7 in src [dark_room ×42: cookbook/database-server/src/tools/create-order.ts, src/types/messages.ts]. flooded_basement — a long-untouched, still-imported room — nests within dark_room at 37 rooms, 30 in cookbook and 7 in src, the load_index conjunct removing 5 rooms from the larger set [flooded_basement ×37: cookbook/filesystem-server/src/utils/path-validator.ts, src/security/layers/layer2-validators/base64-css.ts].

On load and centrality, foundation sits at 21 rooms, 14 in src and 7 in cookbook [foundation ×21: src/security/utils/validation-pipeline.ts, cookbook/monitoring-server/src/utils/metrics-collector.ts]. hub covers 22 rooms, 12 in cookbook and 10 in src [hub ×22: cookbook/transaction-server/src/utils/mock-data.ts, src/types/validation.ts]. corridor nests within hub at 18 rooms, 10 in cookbook and 8 in src, the fan_out conjunct removing 4 rooms; 6 of the 18 sit in cookbook/image-gen-server/src/providers, which holds 6 of the building's 202 rooms [corridor ×18: cookbook/image-gen-server/src/providers/openai.ts].

lit_room stands at 21 rooms, all 21 in src [lit_room ×21: src/security/presets.ts, src/security/layers/layer1-structure.ts]. scaffolding — a test-imported room at or above the median reinforcement — stands at 53 rooms, 36 in cookbook and 17 in src [scaffolding ×53: cookbook/kenpom-server/src/tools/team.ts, src/security/utils/response-validator.ts].

At the graph edges, import_root sits on 17 rooms, all 17 in cookbook [import_root ×17: cookbook/multi-endpoint-server/src/index.ts, cookbook/image-gen-server/src/index-debug.ts]. leaf_utility sits on 19 rooms, 13 in cookbook and 6 in src [leaf_utility ×19: cookbook/http-server/src/tools/calculator.ts, src/security/layers/contextual-config-builder.ts]. package_entry sits on 16 rooms, 13 in cookbook and 3 in src [package_entry ×16: cookbook/tool-policies-server/src/index.ts, src/security/transport/index.ts].

24 decorative marks render but are not a diagnosis: crack — a high edit-pressure node — and toothpick_wing — an unreinforced high-load node with high edit pressure — rest on bug_pressure_index, which is unvalidated [crack ×21; toothpick_wing ×3].

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `1`
- attempts_log: `1: pass`
- brief_version: `0.5.0`
- effort: `high`
- facts_hash: `84490af05150f08cbda68a2d330c4b9e4bb56024d8cfec89100f3c54edfd3ef4`
- input_tokens: `13407`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `4450`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038).
