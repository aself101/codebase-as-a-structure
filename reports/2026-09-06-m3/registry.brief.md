# uluops-registry-api — architect's brief

*Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `9196ea907438…`, facts `3357ba2f3537…`.*

The building holds 267 rooms in three wings: 7 in (root), 30 in scripts, 230 in src. The geometry is age; the profile is maintainability, with an onboarding overlay. Across all profiles 352 diagnostic marks land, and 38 marks sit co-located on rooms already marked by another feature. The root wing is not empty of marks: knexfile.ts carries one, and so does scripts/run-seed.ts [flooded_basement: knexfile.ts, scripts/run-seed.ts].

Twenty-seven rooms sit at high load. The name is disclosed with its position: foundation — a high-load hub, a position in the import graph, not a claim about damage. The set includes src/db/connection.ts, src/db/repository/base-repository.ts, src/utils/logger.ts, src/utils/errors.ts and src/schemas/enums.ts [foundation ×27]. The same 27 positions are drawn again under the onboarding overlay, on the same predicate [foundation ×27].

Centrality marks a further 27 rooms, among them src/config/database.ts, src/schemas/definition/provenance.ts, src/services/safety/yaml-walker.ts and src/utils/request-context.ts [hub ×27]. Thirteen of the central rooms also carry fan-out at or above the median — the position is a high-centrality, high-fan-out junction — including src/db/repository/index.ts, src/middleware/auth.ts, src/routes/v1/schemas.ts and src/services/definition-renderer/index.ts [corridor ×13].

Eleven rooms have no inbound imports and high fan-out, the import-graph root position; eight of these sit in scripts, with src/controllers/index.ts, src/schemas/index.ts and src/services/index.ts in src [entrance: scripts/backfill-fork-parents.ts, scripts/backfill-references.ts, scripts/calibration-gate.ts, scripts/run-deep-analysis.ts, src/controllers/index.ts, src/schemas/index.ts, src/services/index.ts]. At the other end of the graph, 20 rooms import nothing and are imported often — the imported-leaf position — among them src/utils/hash.ts, src/utils/uuid.ts, src/utils/json.ts and src/terminal/styles.ts [leaf_utility ×20].

Age separates the plan. Twenty-seven rooms sit in the oldest decile by last touch: the whole run of src/db/migrations/001_create_definitions.ts through src/db/migrations/007_create_model_aliases.ts, the src/terminal wing including src/terminal/banner.ts and src/terminal/startup.ts, and src/utils/retry.ts [dark_room ×27]. Forty rooms sit in the newest decile, including src/controllers/definition-controller.ts, src/db/repository/lineage-repository.ts, src/index.ts, src/services/definition/queries.ts and src/services/translation/translator.ts [lit_room ×40].

Twenty-seven rooms carry high neglect together with load at or above 0.10: knexfile.ts, src/config/database.ts, the migrations 001 through 007, and the schema clusters src/schemas/reference/schema.ts, src/schemas/reference/types.ts, src/schemas/validation/types.ts and src/schemas/version/types.ts [flooded_basement ×27].

Reinforcement at or above 0.5 is the widest mark on the plan: 133 rooms, spanning every controller from src/controllers/analytics-controller.ts to src/controllers/webhook-controller.ts, the whole of src/middleware including src/middleware/error-handler.ts and src/middleware/tier-gate.ts, the repository floor at src/db/repository/definition-repository.ts, and the src/services/safety rooms src/services/safety/decode.ts and src/services/safety/section-classifier.ts [scaffolding ×133].

27 decorative marks render but are not a diagnosis [crack ×27]; the position is a high edit-pressure node, and the name is disclosed as a position only, not a claim about damage.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- brief_version: `0.1.0`
- effort: `high`
- facts_hash: `3357ba2f353773fa1b511eda08b59b84c6a19052f38a5355b4cda99d748404f5`
- input_tokens: `10024`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3362`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations.
