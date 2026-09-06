# uluops-registry-api — architect's brief

*Register lint: **PASS**. Every claim below is licensed by an `asserted` signal and cites the feature and room it rests on; a claim voices a present structural position, never a consequence. Profile maintainability + onboarding, geometry age, skeleton `9196ea907438…`, facts `d90c412fdc3e…`.*

Three wings stand here: (root) with 7 rooms, scripts with 30, and src with 230 — 267 rooms in all, drawn on a geometry of age, read under a maintainability profile with an onboarding overlay. Twenty-seven of those rooms sit at or above the ninetieth percentile of centrality, and they cluster in configuration, connection, repository bases, schema files and small utilities [hub: src/config/index.ts, src/db/connection.ts, src/db/repository/base-repository.ts, src/schemas/enums.ts, src/utils/logger.ts, src/utils/singleton.ts].

Twenty-seven rooms meet the load_index predicate at the ninetieth percentile. Foundation here is a position name — a high-load hub, a place in the import graph, not a claim about what happens to it. The sheet carries the same 27 rooms twice, once under maintainability and once under the onboarding overlay [foundation ×27]. Thirteen rooms are junctions of high centrality and fan-out at or above the median, the corridor position [corridor: src/db/connection.ts, src/middleware/auth.ts, src/routes/v1/schemas.ts, src/services/safety/definition-scanner.ts, src/utils/logger.ts].

Age splits the plan. Twenty-seven rooms sit in the oldest decile by last touch — the numbered migrations, the whole terminal wing, and a handful of utilities [dark_room: src/db/migrations/001_create_definitions.ts, src/terminal/banner.ts, src/terminal/startup.ts, src/utils/retry.ts, src/utils/cycle-detection.ts]. Forty rooms sit in the newest decile, concentrated in controllers, the definition and analytics services, and the v1 routes [lit_room ×40].

Twenty-seven rooms carry a neglect_index in the top decile together with a load_index at or above 0.10: knexfile.ts, the seed runner, the database config, seven early migrations, and most of the schemas/*/types.ts files [flooded_basement: knexfile.ts, src/config/database.ts, src/schemas/reference/types.ts, src/schemas/version/types.ts, src/utils/index.ts].

One hundred and thirty-three rooms carry a reinforcement_index of 0.5 or above — the largest single marking in the building, spanning controllers, middleware, repositories, schemas, services and utils [scaffolding ×133]. Eleven rooms hold fan_in of zero with fan_out at or above the seventy-fifth percentile, the import-graph root position: eight in the scripts wing and the three barrel files at src/controllers/index.ts, src/schemas/index.ts and src/services/index.ts [entrance ×11]. Twenty rooms hold fan_out of zero with fan_in at or above the seventy-fifth percentile, the imported-leaf position [leaf_utility: src/utils/errors.ts, src/utils/hash.ts, src/utils/uuid.ts, src/services/safety/types.ts, src/schemas/wdl/types.ts]. Thirty-eight rooms are co-located, marked by more than one of these positions at once.

The diagnostic count is 281. Twenty-seven decorative marks — crack, whose position name is high edit-pressure node — render but are not a diagnosis, because bug_pressure_index is unvalidated [crack ×27].

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- brief_version: `0.1.0`
- effort: `high`
- facts_hash: `d90c412fdc3e6db9a940c823ad181b5132ce06529b14b6b2f07240b9ada1c099`
- input_tokens: `9860`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `2519`
- relinted: `brief 0.1.0`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary, R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features excluded from diagnosis, R5 position-name disclosure, R6 no whole-building label, R7 decorative count stated.
