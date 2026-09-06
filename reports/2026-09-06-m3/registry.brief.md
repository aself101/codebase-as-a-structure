# uluops-registry-api — architect's brief

*Register lint: **FAILED (2 violations)**. Every claim below is licensed by an `asserted` signal and cites the feature and room it rests on; a claim voices a present structural position, never a consequence. Profile maintainability + onboarding, geometry age, skeleton `9196ea907438…`, facts `d90c412fdc3e…`.*

The building holds 267 rooms across three wings: 230 in src, 30 in scripts, 7 at the root. The scripts wing is entered from outside — eight of the eleven import-graph roots stand there, alongside three barrels, src/controllers/index.ts, src/schemas/index.ts, src/services/index.ts [entrance ×11]. Geometry is drawn on age; the overlay is onboarding. 281 diagnostic marks land, 38 of them co-located.

Load gathers in a named set. The foundation — a high-load hub, a position in the import graph, and nothing beyond that — sits on 27 rooms, chiefly src/config/index.ts, src/db/connection.ts, src/db/repository/base-repository.ts, src/middleware/auth.ts, src/utils/errors.ts and src/utils/logger.ts [foundation: src/config/index.ts, src/db/connection.ts, src/db/repository/base-repository.ts]. The same 27 rooms carry the mark again under the onboarding overlay [foundation ×27].

Centrality traces nearly the same floor plan. The hub position covers 27 rooms and shares src/config/index.ts, src/db/connection.ts, src/db/repository/base-repository.ts, src/middleware/auth.ts, src/routes/v1/schemas.ts, src/schemas/enums.ts, src/terminal/styles.ts and src/utils/singleton.ts with the load set [hub ×27]. Thirteen of those are high-centrality, high-fan-out junctions, including src/config/database.ts, src/db/repository/index.ts and src/services/safety/definition-scanner.ts [corridor ×13]. Twenty rooms are imported leaves with no outward edges, among them src/utils/hash.ts, src/utils/uuid.ts, src/utils/json.ts and src/services/safety/types.ts [leaf_utility ×20].

Age splits the plan. Forty rooms sit in the most recently touched band — the controllers floor, src/routes/v1/definitions.ts, src/services/definition/lifecycle.ts, src/services/definition/queries.ts, src/db/repository/definition-repository.ts [lit_room ×40]. Twenty-seven sit in the least recently touched band: twelve migrations from 001_create_definitions.ts through 20260119222852_alter_hash_column_size.ts, the entire src/terminal floor, and utilities including src/utils/retry.ts and src/utils/cycle-detection.ts [dark_room ×27]. Twenty-seven rooms hold both neglect at or above p90 and load at or above 0.10, among them knexfile.ts, src/config/database.ts, the same early migrations, the src/schemas type and index files, src/utils/async-handler.ts and src/utils/singleton.ts [flooded_basement ×27].

Reinforcement is the widest mark: 133 rooms at or above 0.5, covering every controller, every repository, the whole middleware floor, the schemas wing, the safety services and most of src/utils [scaffolding ×133]. src/db/connection.ts, src/middleware/auth.ts, src/routes/v1/schemas.ts and src/schemas/enums.ts hold reinforcement together with load and centrality [scaffolding: src/db/connection.ts, src/middleware/auth.ts, src/routes/v1/schemas.ts]. Rooms in the least-touched band that carry no reinforcement include src/terminal/banner.ts, src/terminal/startup.ts and src/db/migrations/016_add_fulltext_search_index.ts [dark_room: src/terminal/banner.ts, src/terminal/startup.ts, src/db/migrations/016_add_fulltext_search_index.ts].

Twenty-seven decorative marks — crack, a high edit-pressure node — render but are not a diagnosis; bug_pressure_index is unvalidated [crack ×27].

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact [foundation ×27, scaffolding ×133].

## Provenance

- attempt: `2`
- brief_version: `0.1.0`
- effort: `high`
- facts_hash: `d90c412fdc3e6db9a940c823ad181b5132ce06529b14b6b2f07240b9ada1c099`
- input_tokens: `10971`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `1996`
- stop_reason: `end_turn`

## Register lint

| rule | paragraph | detail | text |
|---|---|---|---|
| R4-decorative | 6 | diagnostic claim cites a decorative feature: crack (excluded from diagnosis, mapper §3) | Twenty-seven decorative marks — crack, a high edit-pressure node — render but are not a diagnosis; bug_pressure_index is unvalidated [crack ×27]. |
| R2-provenance | 7 | paragraph carries no [feature: room] or [feature ×N] citation | The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited,  |

**This brief failed the register lint and is not a diagnosis until it passes.**
