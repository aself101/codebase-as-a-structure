# mcp-secure-server — architect's brief

*Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `caf5cc9ff180…`, facts `0f283b667b97…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `?`. Brief 0.2.1; a PASS is a pass under that grammar (D-035).*

The building holds 202 rooms across 3 wings: cookbook at 136, src at 64, and the root at 2. Across all profiles 287 diagnostic marks land, and 49 of them sit co-located on rooms already carrying another mark. The widest single reading is scaffolding, on 53 rooms spread through both large wings [scaffolding ×53: cookbook/database-server/src/tools/query-users.ts, src/security/utils/validation-pipeline.ts].

The load-bearing positions read twice. foundation — a high-load hub, a position in the import graph, not a claim about what breaks — fires on 21 rooms under the maintainability profile and on 21 under the onboarding overlay [foundation ×21; onboarding/foundation ×21: src/types/index.ts, src/security/utils/error-sanitizer.ts, cookbook/monitoring-server/src/utils/alert-manager.ts].

Centrality marks a second, overlapping band. 22 rooms stand at the high-centrality end [hub ×22: src/types/validation.ts, cookbook/image-gen-server/src/providers/openai.ts], and 18 of the centrality readings also carry fan-out at or above the median, a high-centrality, high-fan-out junction [corridor ×18: cookbook/api-wrapper-server/src/utils/index.ts, src/security/config/tool-policy-validation.ts].

Age sits mostly in the cookbook wing. dark_room — a long-untouched room, a position on the last-touched axis — fires on 42 rooms [dark_room ×42: cookbook/nba-server/vitest.config.ts, src/types/messages.ts]. flooded_basement — a long-untouched, still-imported room, the same age position with load at or above 0.10 — fires on 37 [flooded_basement ×37: src/security/utils/tool-registry.ts, cookbook/filesystem-server/src/utils/path-validator.ts].

The recently touched end of the same axis is 21 rooms, and it sits almost entirely in src [lit_room ×21: src/security/presets.ts, src/security/layers/layer1-structure.ts].

The onboarding overlay marks the graph's edges. 17 rooms hold zero fan-in with fan-out at or above the 75th percentile, an import-graph root [import_root ×17: cookbook/image-gen-server/src/index-debug.ts]. 19 rooms hold the mirror position, zero fan-out with fan-in at or above the 75th percentile, an imported leaf [leaf_utility ×19: src/security/layers/contextual-config-builder.ts]. 16 rooms are declared package entries [package_entry ×16: cookbook/tool-policies-server/src/index.ts, src/security/transport/index.ts].

24 decorative marks render but are not a diagnosis: a high edit-pressure node and an unreinforced high-load node with high edit pressure, both resting on an unvalidated index [crack ×21; toothpick_wing ×3].

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R5-disclosure, R5-disclosure; 2: pass`
- brief_version: `0.2.1`
- effort: `high`
- facts_hash: `0f283b667b97892ec6e8acca74f402735961fbd645e444a2adac58b72e94dd0e`
- input_tokens: `11445`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `2996`
- relinted: `brief 0.2.1`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations.
