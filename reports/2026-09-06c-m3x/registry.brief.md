# uluops-registry-api — architect's brief

*Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `fd531406875f…`, facts `86544d3bba03…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page.*

The building holds 267 rooms in 3 wings: src at 230, scripts at 30, and a root shelf of 7. Across all profiles the rooms carry 352 diagnostic marks, and 39 rooms carry marks from more than one feature. One room is the declared package entry [package_entry ×1: src/index.ts].

Load concentrates in 27 rooms marked as foundation — a high-load hub, a position in the import graph, not a claim about what breaks — and the same 27 rooms are marked again under the onboarding overlay [foundation ×27; onboarding/foundation ×27: src/db/connection.ts, src/utils/logger.ts]. The list runs through configuration, database repositories, middleware, schemas, safety services and utilities [foundation ×27: src/config/index.ts, src/db/repository/base-repository.ts, src/middleware/auth.ts, src/services/safety/yaml-walker.ts].

27 rooms sit at high centrality [hub ×27: src/schemas/enums.ts, src/routes/v1/schemas.ts]. 13 rooms sit at high centrality with fan-out at or above the median [corridor ×13: src/config/database.ts, src/services/definition-renderer/index.ts]. 11 rooms have fan-in of 0 with high fan-out, sitting as import-graph roots, mostly in the scripts wing [import_root ×11: scripts/calibration-gate.ts, src/services/index.ts]. 20 rooms have fan-out of 0 with high fan-in, sitting as imported leaves [leaf_utility ×20: src/utils/uuid.ts, src/schemas/wdl/types.ts].

The age geometry splits the building. 27 rooms sit in the long-untouched band [dark_room ×27: src/db/migrations/001_create_definitions.ts, src/terminal/banner.ts] — dark_room is a long-untouched room, a timestamp position, not a claim about condition. 26 of the long-untouched rooms are still imported, marked flooded_basement — a long-untouched, still-imported room [flooded_basement ×26: src/utils/retry.ts, src/routes/v1/render.ts]. The migrations, the terminal wing and several utilities appear in both bands [dark_room ×27: src/db/migrations/016_add_fulltext_search_index.ts, src/terminal/styles.ts; flooded_basement ×26: src/utils/cycle-detection.ts].

At the other end of the same geometry, 40 rooms sit in the most recently touched band: controllers, repositories, route files, services [lit_room ×40: src/controllers/definition-controller.ts, src/db/repository/version-repository.ts, src/services/version-service.ts].

Reinforcement is the widest mark on the sheet: 133 rooms sit at or above the reinforcement threshold, spanning controllers, middleware, schemas, safety services and utilities [scaffolding ×133: src/middleware/error-handler.ts, src/schemas/fork/transforms.ts, src/services/safety/risk-calculator.ts, src/utils/circuit-breaker.ts].

27 decorative marks render but are not a diagnosis [crack ×27]; the position name is high edit-pressure node, and the rooms it fired on are not named here.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R3-number; 2: pass`
- brief_version: `0.2.1`
- effort: `high`
- facts_hash: `86544d3bba03ea00795d0bd9d55dc90c954336fb24d9eeeaa4d03916176a9f14`
- input_tokens: `10461`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `2016`
- relinted: `brief 0.2.1`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations.
