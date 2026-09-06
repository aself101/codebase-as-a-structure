# mcp-secure-server — architect's brief

*Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `5aa582547012…`, facts `e8d92650c4e1…`.*

The building holds 202 rooms across three wings: 136 in cookbook, 64 in src, 2 at the root. Across all profiles, 271 diagnostic marks land, 47 of them co-located on rooms carrying more than one. Every import-graph root sits in the cookbook wing — cookbook/nba-server/src/index.ts, cookbook/transaction-server/src/index.ts, cookbook/http-server/src/index.ts, cookbook/multi-endpoint-server/src/tools/index.ts among them [entrance ×17].

Twenty-one rooms occupy the position the facts sheet calls a high-load hub — a measured position in the import graph, not a verdict about anything downstream. They sit on both sides of the building: cookbook/monitoring-server/src/utils/alert-manager.ts, cookbook/image-gen-server/src/tools/generate.ts, src/security/layers/validation-layer-base.ts, src/security/utils/validation-pipeline.ts, src/types/index.ts, src/types/policies.ts [foundation ×21].

Centrality gathers in the type and provider rooms. src/types/index.ts, src/types/validation.ts, src/types/layers.ts, cookbook/image-gen-server/src/providers/openai.ts and cookbook/image-gen-server/src/providers/bfl.ts hold the hub position [hub ×22]. The high-centrality, high-fan-out junction lands on a narrower set, including src/security/config/tool-policy-validation.ts, src/security/layers/layer-utils/content/patterns/injection.ts and cookbook/transaction-server/src/utils/index.ts [corridor ×18].

At the other end of the graph sit the imported leaves, fan-out zero and fan-in at or above the third quartile: src/security/layers/contextual-config-builder.ts, src/security/layers/layer-utils/semantics/glob-utils.ts, cookbook/kenpom-server/src/tools/ratings.ts, cookbook/nba-server/src/tools/live.ts [leaf_utility ×19].

Forty-two rooms carry last-touch ages at or above the ninetieth percentile, nearly all of them in cookbook — cookbook/api-wrapper-server/src/tools/weather.ts, cookbook/filesystem-server/src/tools/read-file.ts, cookbook/database-server/src/utils/database.ts — with src/types/messages.ts and src/security/utils/tool-registry.ts among the src rooms [dark_room ×42]. Thirty-seven rooms sit where neglect at that percentile meets a load index of at least 0.10, including cookbook/filesystem-server/src/utils/path-validator.ts, cookbook/image-gen-server/src/providers/stability.ts, src/security/layers/layer-utils/content/unicode.ts and src/security/layers/layer2-validators/base64-css.ts [flooded_basement ×37].

The most recently touched rooms cluster in src: src/security/presets.ts, src/security/layers/layer1-structure.ts, src/security/layers/builtin-validators.ts, src/security/utils/security-logger-types.ts, src/types/server.ts [lit_room ×21]. Fifty-three rooms carry a reinforcement index of 0.5 or higher, spread across both wings — cookbook/monitoring-server/src/utils/audit-logger.ts, cookbook/kenpom-server/src/tools/team.ts, cookbook/multi-endpoint-server/src/servers/admin-server.ts, src/security/utils/response-validator.ts, src/security/layers/layer-utils/content/canonicalize.ts [scaffolding ×53].

Twenty-four decorative marks render but are not a diagnosis [crack ×21, toothpick_wing ×3]. Crack sits at the position named high edit-pressure node; toothpick_wing sits at the position named unreinforced high-load node with high edit pressure. Both rest on bug_pressure_index, which the gate records as unvalidated, so neither carries a diagnostic claim here and the rooms they mark go unnamed.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- brief_version: `0.1.0`
- effort: `high`
- facts_hash: `e8d92650c4e104e4384d14fee2f88024fa3ca32f1dc91710e183316cbd384ec5`
- input_tokens: `10654`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3299`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations.
