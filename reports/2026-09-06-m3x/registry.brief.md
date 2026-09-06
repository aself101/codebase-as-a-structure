# uluops-registry-api — architect's brief

*Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `b97b47e33344…`, facts `be1a6822641b…`.*

The building holds 267 rooms, distributed across the root wing at 7, scripts at 30, and src at 230. Geometry is drawn on age. One room, src/index.ts, stands as the declared package entry [package_entry: src/index.ts].

The survey records 353 diagnostic marks across all profiles, 281 of them in the base profile, and 39 rooms sit under more than one diagnostic feature. The widest single reading covers 133 rooms, reaching every wing of src — controllers, middleware, schemas, services, utils [scaffolding ×133].

Twenty-seven rooms carry foundation — a high-load hub, a position in the import graph, not a claim about what happens in them. Among them sit src/db/connection.ts, src/utils/logger.ts, src/utils/errors.ts, src/utils/singleton.ts, src/schemas/enums.ts and src/services/safety/yaml-walker.ts [foundation ×27]. A separately measured set of 27 rooms sits at high centrality, including src/config/database.ts, src/utils/request-context.ts, src/schemas/user/schema.ts and src/db/repository/base-repository.ts [hub ×27].

The onboarding overlay marks 13 rooms as high-centrality, high-fan-out junctions: src/config/database.ts, src/db/connection.ts, src/db/repository/base-repository.ts, src/db/repository/index.ts, src/middleware/auth.ts, src/routes/v1/schemas.ts, src/schemas/definition/schema.ts, src/schemas/enums.ts, src/schemas/model/schema.ts, src/schemas/reference/schema.ts, src/services/definition-renderer/index.ts, src/services/safety/definition-scanner.ts and src/utils/logger.ts [corridor ×13]. Eleven rooms are import-graph roots, zero fan-in with high fan-out, among them scripts/calibration-gate.ts, scripts/run-deep-analysis.ts, src/controllers/index.ts, src/schemas/index.ts and src/services/index.ts [import_root ×11]. Twenty rooms are imported leaves with no fan-out, including src/utils/uuid.ts, src/utils/hash.ts, src/utils/json.ts, src/terminal/styles.ts and src/schemas/wdl/types.ts [leaf_utility ×20].

Twenty-seven rooms carry dark_room — a long-untouched room, a position on the age axis. They cluster in src/db/migrations, from 001_create_definitions.ts through 016_add_fulltext_search_index.ts and 20260119222852_alter_hash_column_size.ts, and in src/terminal: banner.ts, index.ts, startup.ts, styles.ts and the sections rooms [dark_room ×27]. Twenty-seven rooms carry flooded_basement — a long-untouched, still-imported room. These include knexfile.ts, scripts/run-seed.ts, src/config/database.ts, the schemas rooms under fork, model, reference, validation and version, and src/utils/index.ts, src/utils/cycle-detection.ts and src/utils/singleton.ts [flooded_basement ×27].

Forty rooms sit at the recent end of the age axis: the controllers, src/db/repository/alias-repository.ts, lineage-repository.ts and version-repository.ts, src/services/definition/quota.ts, src/services/safety/publish-gate.ts, src/services/translation/translator.ts and src/index.ts among them [lit_room ×40].

27 decorative marks render but are not a diagnosis; the name stands on a high edit-pressure node, a position [crack ×27].

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R3-number, R3-number, R3-number, R1-consequence; 2: pass`
- brief_version: `0.2.0`
- effort: `high`
- facts_hash: `be1a6822641b092f512d35765638bae2cb68043f310a8b1496ff0dfbc24ada28`
- input_tokens: `10503`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `2896`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations.
