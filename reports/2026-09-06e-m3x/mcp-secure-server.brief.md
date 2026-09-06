# mcp-secure-server — architect's brief

*Register lint: **PASS on attempt 1**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `caf5cc9ff180…`, facts `7f438b2de0a4…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.3.0; a PASS is a pass under that grammar (D-035).*

The building holds 202 rooms in 3 wings: 136 in cookbook, 64 in src, 2 at the root. Across all profiles 287 diagnostic marks land, and 91 rooms carry more than one mark. Of the declared entries, 13 of 16 sit in cookbook and 3 in src [package_entry ×16: cookbook/transaction-server/src/index.ts, src/security/transport/index.ts].

Foundation — the position name is high-load hub, a coordinate in the import graph — fires on 21 rooms, 14 in src and 7 in cookbook [foundation ×21: src/types/index.ts, cookbook/monitoring-server/src/utils/metrics-collector.ts]. The 21 maintainability foundation rooms are the same 21 rooms as the onboarding foundation; two marks on one set of rooms are one finding [foundation ×21; onboarding/foundation ×21].

Centrality marks 22 rooms, 12 in cookbook and 10 in src [hub ×22: cookbook/image-gen-server/src/providers/index.ts, src/security/config/tool-policies.ts]. All 18 corridor rooms — the position name is high-centrality, high-fan-out junction — sit inside that hub set, 10 of them in cookbook and 8 in src [corridor ×18; hub ×22].

Dark_room — the position name is long-untouched room — covers 42 rooms, 35 in cookbook and 7 in src [dark_room ×42: cookbook/nba-server/src/utils/index.ts, src/types/messages.ts]. The 37 flooded_basement rooms — the position name is long-untouched, still-imported room — are all within the dark_room set, 30 of them in cookbook and 7 in src [flooded_basement ×37; dark_room ×42].

At the other end of the age geometry, 21 lit rooms sit entirely in src [lit_room ×21: src/security/presets.ts, src/security/layers/layer1-structure.ts].

Reinforcement carries the widest mark: 53 rooms, 36 in cookbook and 17 in src [scaffolding ×53: cookbook/kenpom-server/src/tools/team.ts, src/security/utils/response-validator.ts]. Two of the rooms named in the same sentence, src/security/utils/error-sanitizer.ts and cookbook/transaction-server/src/utils/index.ts, also stand in the foundation set [foundation ×21].

Seventeen import-graph roots sit in cookbook and none elsewhere [import_root ×17: cookbook/image-gen-server/src/index-debug.ts, cookbook/multi-endpoint-server/src/tools/index.ts]. Nineteen imported leaves divide 13 in cookbook and 6 in src [leaf_utility ×19: cookbook/http-server/src/tools/calculator.ts, src/security/layers/contextual-config-builder.ts].

24 decorative marks render but are not a diagnosis [crack ×21; toothpick_wing ×3]. Crack names a high edit-pressure node and toothpick_wing an unreinforced high-load node with high edit pressure; both rest on an index the gate lists as unvalidated, and neither enters any finding above.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `1`
- attempts_log: `1: pass`
- brief_version: `0.3.0`
- effort: `high`
- facts_hash: `7f438b2de0a4c224a22869214bb588f8b489284a5441e617273e615afdb08319`
- input_tokens: `12081`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `2779`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb — shares are by_wing counts (D-036).
