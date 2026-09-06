# mcp-secure-server — architect's brief

*Register lint: **FAILED (5 violations) on attempt 3**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `a2b20231bc10…`, facts `9443c104a585…`.*

The building holds 202 rooms. The cookbook wing holds 136, the src wing 64, and the root 2. Geometry is drawn by age; the profile is maintainability, with onboarding laid over it as an overlay. Across all profiles the survey records 287 diagnostic marks, and 49 rooms are co-located. Twenty-two rooms sit in the high-centrality band [hub ×22].

Twenty-one rooms carry foundation — a high-load hub, a position in the import graph and nothing more — and the same count repeats under the onboarding overlay [foundation ×21]. The mark sits on src/security/config/tool-policies.ts, src/security/layers/validation-layer-base.ts, src/security/utils/validation-pipeline.ts, src/types/index.ts and src/types/policies.ts, and reaches into the cookbook wing at cookbook/monitoring-server/src/utils/alert-manager.ts and cookbook/transaction-server/src/utils/index.ts [foundation: src/security/config/tool-policies.ts, src/security/layers/validation-layer-base.ts, src/security/utils/validation-pipeline.ts, src/types/index.ts, src/types/policies.ts, cookbook/monitoring-server/src/utils/alert-manager.ts, cookbook/transaction-server/src/utils/index.ts].

The centrality band takes in the whole image-gen provider row — cookbook/image-gen-server/src/providers/bfl.ts, google.ts, ideogram.ts, index.ts, openai.ts, stability.ts — along with src/types/validation.ts and src/security/config/tool-policy-validation.ts [hub: cookbook/image-gen-server/src/providers/bfl.ts, cookbook/image-gen-server/src/providers/google.ts, cookbook/image-gen-server/src/providers/ideogram.ts, cookbook/image-gen-server/src/providers/index.ts, cookbook/image-gen-server/src/providers/openai.ts, cookbook/image-gen-server/src/providers/stability.ts, src/types/validation.ts, src/security/config/tool-policy-validation.ts]. Eighteen rooms are marked corridor, a high-centrality, high-fan-out junction, among them src/security/layers/layer-utils/content/patterns/injection.ts and src/types/layers.ts [corridor ×18].

Forty-two rooms are dark_room — a long-untouched room — and they fall overwhelmingly in cookbook, including cookbook/filesystem-server/src/tools/read-file.ts, cookbook/database-server/src/utils/database.ts and every vitest.config.ts in that wing, with src/types/messages.ts and src/security/utils/tool-registry.ts on the src side [dark_room ×42; dark_room: cookbook/filesystem-server/src/tools/read-file.ts, cookbook/database-server/src/utils/database.ts, src/types/messages.ts, src/security/utils/tool-registry.ts]. Thirty-seven rooms are flooded_basement — a long-untouched, still-imported room — among them cookbook/api-wrapper-server/src/utils/http.ts, cookbook/filesystem-server/src/utils/path-validator.ts, src/security/layers/layer-utils/content/unicode.ts and src/security/layers/layer2-validators/base64-css.ts [flooded_basement ×37].

Twenty-one rooms are lit_room, all in src: src/security/presets.ts, src/security/layers/layer1-structure.ts, src/security/layers/builtin-validators.ts, src/security/utils/security-logger-types.ts and src/types/server.ts among them [lit_room: src/security/presets.ts, src/security/layers/layer1-structure.ts, src/security/layers/builtin-validators.ts, src/security/utils/security-logger-types.ts, src/types/server.ts]. Fifty-three rooms carry scaffolding, the largest set on the sheet, spanning cookbook/nba-server/src/tools/live.ts, cookbook/multi-endpoint-server/src/servers/admin-server.ts, src/index.ts and src/security/utils/response-validator.ts [scaffolding ×53].

Seventeen rooms are import_root, an import-graph root, including cookbook/image-gen-server/src/index-debug.ts and cookbook/advanced-validation-server/src/index.ts [import_root ×17]. Nineteen are leaf_utility, an imported leaf, including src/security/layers/contextual-config-builder.ts and cookbook/http-server/src/tools/echo.ts [leaf_utility ×19]. Sixteen are package_entry, a declared package entry, including src/security/transport/index.ts and cookbook/tool-policies-server/src/index.ts [package_entry ×16].

24 decorative marks render but are not a diagnosis [crack ×21, toothpick_wing ×3]. Each name carries a position only: crack, a high edit-pressure node; toothpick_wing, an unreinforced high-load node with high edit pressure.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `3`
- attempts_log: `1: R8-attribution, R8-attribution, R8-attribution, R8-attribution, R8-attribution, R8-attribution, R8-attribution, R2-provenance, R3-number, R3-number, R2-provenance; 2: R3-number, R3-number, R4-decorative; 3: R8-attribution, R8-attribution, R8-attribution, R8-attribution, R2-provenance`
- brief_version: `0.2.0`
- effort: `high`
- facts_hash: `9443c104a5857fe74b44bd9c8e015995d4761524dcf6897a6e1679d68b326264`
- input_tokens: `11397`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `4969`
- stop_reason: `end_turn`

## Register lint

| rule | paragraph | detail | text |
|---|---|---|---|
| R8-attribution | 4 | names cookbook/filesystem-server/src/tools/read-file.ts but no feature cited in the sentence fired on it | Forty-two rooms are dark_room — a long-untouched room — and they fall overwhelmingly in cookbook, including cookbook/filesystem-server/src/tools/read-file.ts, c |
| R8-attribution | 4 | names cookbook/database-server/src/utils/database.ts but no feature cited in the sentence fired on it | Forty-two rooms are dark_room — a long-untouched room — and they fall overwhelmingly in cookbook, including cookbook/filesystem-server/src/tools/read-file.ts, c |
| R8-attribution | 4 | names src/security/utils/tool-registry.ts but no feature cited in the sentence fired on it | Forty-two rooms are dark_room — a long-untouched room — and they fall overwhelmingly in cookbook, including cookbook/filesystem-server/src/tools/read-file.ts, c |
| R8-attribution | 4 | names src/types/messages.ts but no feature cited in the sentence fired on it | Forty-two rooms are dark_room — a long-untouched room — and they fall overwhelmingly in cookbook, including cookbook/filesystem-server/src/tools/read-file.ts, c |
| R2-provenance | 7 | paragraph carries no [feature: room] or [feature ×N] citation | 24 decorative marks render but are not a diagnosis [crack ×21, toothpick_wing ×3]. Each name carries a position only: crack, a high edit-pressure node; toothpic |

**This brief failed the register lint and is not a diagnosis until it passes.**
