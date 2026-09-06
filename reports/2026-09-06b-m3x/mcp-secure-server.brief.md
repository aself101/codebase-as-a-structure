# mcp-secure-server — architect's brief

*Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `517fdc42e7cb…`, facts `986b1e4009f2…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page.*

The building holds 202 rooms across three wings: cookbook with 136, src with 64, and a root wing of 2. Across all profiles 287 diagnostic marks land on it, and 49 rooms carry more than one mark at once [scaffolding ×53; hub ×22]. The geometry is drawn by age; one overlay, onboarding, sits over the maintainability profile.

Centrality gathers in two places. Twenty-two rooms stand at or above the ninetieth percentile of centrality [hub ×22: src/types/index.ts, src/types/policies.ts, cookbook/image-gen-server/src/providers/index.ts]. Eighteen of the junctions combine that centrality with fan-out at or above the median [corridor ×18: cookbook/api-wrapper-server/src/utils/index.ts, src/security/config/tool-policy-validation.ts, src/types/layers.ts].

Load concentrates on twenty-one rooms under both profiles — foundation, a high-load hub, is a position in the import graph and not a claim about behaviour [foundation ×21; onboarding/foundation ×21]. Those positions include src/security/utils/validation-pipeline.ts, src/security/layers/validation-layer-base.ts, and cookbook/monitoring-server/src/utils/alert-manager.ts [foundation ×21].

Age sits mostly in the cookbook wing. Forty-two rooms fall at or above the ninetieth percentile of days since last touch — dark_room names a long-untouched room [dark_room ×42: cookbook/nba-server/src/tools/index.ts, src/types/messages.ts, src/security/utils/tool-registry.ts].

Thirty-seven of the aged rooms also carry a load index of at least 0.10 — flooded_basement names a long-untouched, still-imported room [flooded_basement ×37: cookbook/database-server/src/utils/database.ts, cookbook/filesystem-server/src/utils/path-validator.ts, src/security/layers/layer2-validators/base64-css.ts].

The recent end of the age geometry sits entirely inside src. Twenty-one rooms fall at or below the tenth percentile of days since last touch [lit_room ×21: src/security/presets.ts, src/security/layers/layer1-structure.ts, src/security/utils/security-logger-types.ts].

Reinforcement at or above 0.5 is recorded on fifty-three rooms, spread over both large wings [scaffolding ×53: cookbook/kenpom-server/src/tools/ratings.ts, cookbook/multi-endpoint-server/src/servers/admin-server.ts, src/security/utils/response-validator.ts].

The onboarding overlay marks the edges of the import graph. Seventeen rooms have fan-in of zero with fan-out at or above the seventy-fifth percentile [import_root ×17: cookbook/image-gen-server/src/index-debug.ts, cookbook/multi-endpoint-server/src/tools/index.ts]. Nineteen have fan-out of zero with fan-in at or above the seventy-fifth percentile [leaf_utility ×19: src/security/layers/contextual-config-builder.ts, cookbook/http-server/src/tools/echo.ts]. Sixteen are declared package entries [package_entry ×16: src/index.ts, src/security/transport/index.ts, cookbook/tool-policies-server/src/index.ts].

Twenty-four decorative marks render but are not a diagnosis: crack, a high edit-pressure node, and toothpick_wing, an unreinforced high-load node with high edit pressure, both rest on an unvalidated index and are excluded from every claim above [crack ×21; toothpick_wing ×3].

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R5-disclosure, R5-disclosure, R5-disclosure, R5-disclosure; 2: pass`
- brief_version: `0.2.1`
- effort: `high`
- facts_hash: `986b1e4009f25250b706d1a14526e59ef0974547093f2a3360d54d825c011867`
- input_tokens: `11514`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3363`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations.
