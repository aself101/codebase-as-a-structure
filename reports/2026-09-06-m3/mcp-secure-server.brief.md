# mcp-secure-server — architect's brief

*Register lint: **FAILED (16 violations)**. Every claim below is licensed by an `asserted` signal and cites the feature and room it rests on; a claim voices a present structural position, never a consequence. Profile maintainability + onboarding, geometry age, skeleton `5aa582547012…`, facts `987906877c8e…`.*

The building has three wings. cookbook holds 136 rooms, src holds 64, and the root holds 2, out of a population of 202. The survey is drawn on the age geometry with an onboarding overlay, and 196 of the marks are diagnostic [scaffolding ×53, dark_room ×42, flooded_basement ×37].

Load lands in two clusters. foundation — a high-load hub, a position in the import graph, not a claim about what breaks — sits on 21 rooms, half of them the security core and half the cookbook utilities [feature: src/security/utils/validation-pipeline.ts, src/security/layers/validation-layer-base.ts, cookbook/monitoring-server/src/utils/alert-manager.ts]. hub, a centrality position, sits on 22 rooms, and the type declarations occupy that position as a block [feature: src/types/index.ts, src/types/layers.ts, src/types/policies.ts, src/types/server.ts, src/types/validation.ts].

Age reads across the cookbook wing. dark_room marks 42 rooms at or beyond the p90 last-touched threshold, nearly all of them cookbook tools, utils and vitest configs [feature: cookbook/api-wrapper-server/src/tools/weather.ts, cookbook/database-server/src/utils/database.ts, cookbook/filesystem-server/vitest.config.ts]. Seven of those rooms are in src [feature: src/security/layers/layer-utils/content/unicode.ts, src/security/utils/tool-registry.ts, src/types/messages.ts].

flooded_basement, which requires neglect at p90 together with load at or above 0.10, sits on 37 rooms and overlaps the dark set closely [feature: cookbook/filesystem-server/src/utils/path-validator.ts, cookbook/image-gen-server/src/providers/stability.ts, src/security/layers/layer2-validators/base64-css.ts]. The recently touched rooms are elsewhere: lit_room covers 21 rooms, every one of them under src/security or src/types [feature: src/security/layers/layer1-structure.ts, src/security/presets.ts, src/types/server.ts].

Reinforcement is the widest mark. scaffolding sits on 53 rooms spanning both wings, including cookbook tool handlers and the security pipeline [feature: cookbook/kenpom-server/src/tools/team.ts, cookbook/monitoring-server/src/utils/audit-logger.ts, src/security/utils/response-validator.ts, src/index.ts].

The onboarding overlay adds three positions. entrance — an import-graph root, fan-in zero with fan-out at or above p75 — sits on 17 rooms, all of them cookbook server and tool indexes [feature: cookbook/http-server/src/index.ts, cookbook/nba-server/src/tools/index.ts]. corridor, a high-centrality, high-fan-out junction, sits on 18 rooms, concentrated in the image-gen providers and the security config [feature: cookbook/image-gen-server/src/providers/index.ts, src/security/config/tool-policy-validation.ts]. leaf_utility, an imported leaf, sits on 19 rooms [feature: src/security/constants.ts, cookbook/nba-server/src/tools/live.ts, src/types/policies.ts].

47 rooms carry more than one mark. One room carries foundation, hub, corridor, scaffolding and lit_room together [feature: src/security/utils/error-sanitizer.ts], and another carries foundation, hub, corridor and leaf_utility [feature: src/types/policies.ts].

24 decorative marks render but are not a diagnosis [crack ×21, toothpick_wing ×3]. crack — a high edit-pressure node — sits on 21 rooms [feature: src/security/layers/layer3-behavior.ts, eslint.config.js], and toothpick_wing — an unreinforced high-load node with high edit pressure — sits on 3 [feature: src/security/config/tool-policies-config.ts, src/security/constants.ts, src/types/server.ts]. Both rest on an index the gate records as unvalidated (D-015), and neither enters any diagnosis here.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact [foundation ×21, scaffolding ×53, flooded_basement ×37].

## Provenance

- attempt: `2`
- brief_version: `0.1.0`
- effort: `high`
- facts_hash: `987906877c8ec5193cfc29f27077392d4f9637d2f429b57536317f875e0991ed`
- input_tokens: `10378`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3012`
- stop_reason: `end_turn`

## Register lint

| rule | paragraph | detail | text |
|---|---|---|---|
| R2-provenance | 1 | paragraph carries no [feature: room] or [feature ×N] citation | The building has three wings. cookbook holds 136 rooms, src holds 64, and the root holds 2, out of a population of 202. The survey is drawn on the age geometry  |
| R2-provenance | 2 | citation names a feature not in the skeleton: feature | Load lands in two clusters. foundation — a high-load hub, a position in the import graph, not a claim about what breaks — sits on 21 rooms, half of them the sec |
| R2-provenance | 2 | citation names a feature not in the skeleton: feature | Load lands in two clusters. foundation — a high-load hub, a position in the import graph, not a claim about what breaks — sits on 21 rooms, half of them the sec |
| R2-provenance | 3 | citation names a feature not in the skeleton: feature | Age reads across the cookbook wing. dark_room marks 42 rooms at or beyond the p90 last-touched threshold, nearly all of them cookbook tools, utils and vitest co |
| R2-provenance | 3 | citation names a feature not in the skeleton: feature | Age reads across the cookbook wing. dark_room marks 42 rooms at or beyond the p90 last-touched threshold, nearly all of them cookbook tools, utils and vitest co |
| R2-provenance | 4 | citation names a feature not in the skeleton: feature | flooded_basement, which requires neglect at p90 together with load at or above 0.10, sits on 37 rooms and overlaps the dark set closely [feature: cookbook/files |
| R2-provenance | 4 | citation names a feature not in the skeleton: feature | flooded_basement, which requires neglect at p90 together with load at or above 0.10, sits on 37 rooms and overlaps the dark set closely [feature: cookbook/files |
| R2-provenance | 5 | citation names a feature not in the skeleton: feature | Reinforcement is the widest mark. scaffolding sits on 53 rooms spanning both wings, including cookbook tool handlers and the security pipeline [feature: cookboo |
| R2-provenance | 6 | citation names a feature not in the skeleton: feature | The onboarding overlay adds three positions. entrance — an import-graph root, fan-in zero with fan-out at or above p75 — sits on 17 rooms, all of them cookbook  |
| R2-provenance | 6 | citation names a feature not in the skeleton: feature | The onboarding overlay adds three positions. entrance — an import-graph root, fan-in zero with fan-out at or above p75 — sits on 17 rooms, all of them cookbook  |
| R2-provenance | 6 | citation names a feature not in the skeleton: feature | The onboarding overlay adds three positions. entrance — an import-graph root, fan-in zero with fan-out at or above p75 — sits on 17 rooms, all of them cookbook  |
| R2-provenance | 7 | citation names a feature not in the skeleton: feature | 47 rooms carry more than one mark. One room carries foundation, hub, corridor, scaffolding and lit_room together [feature: src/security/utils/error-sanitizer.ts |
| R2-provenance | 7 | citation names a feature not in the skeleton: feature | 47 rooms carry more than one mark. One room carries foundation, hub, corridor, scaffolding and lit_room together [feature: src/security/utils/error-sanitizer.ts |
| R2-provenance | 8 | citation names a feature not in the skeleton: feature | 24 decorative marks render but are not a diagnosis [crack ×21, toothpick_wing ×3]. crack — a high edit-pressure node — sits on 21 rooms [feature: src/security/l |
| R2-provenance | 8 | citation names a feature not in the skeleton: feature | 24 decorative marks render but are not a diagnosis [crack ×21, toothpick_wing ×3]. crack — a high edit-pressure node — sits on 21 rooms [feature: src/security/l |
| R2-provenance | 9 | paragraph carries no [feature: room] or [feature ×N] citation | The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited,  |

**This brief failed the register lint and is not a diagnosis until it passes.**
