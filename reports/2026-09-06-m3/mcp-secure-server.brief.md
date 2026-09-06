# mcp-secure-server — architect's brief

*Register lint: **PASS**. Every claim below is licensed by an `asserted` signal and cites the feature and room it rests on; a claim voices a present structural position, never a consequence. Profile maintainability + onboarding, geometry age, skeleton `5aa582547012…`, facts `987906877c8e…`.*

The building holds 202 rooms in three wings: 136 in cookbook, 64 in src, 2 at the root. Seventeen rooms sit as import-graph roots — nothing imports them and their fan-out stands at or above the 75th percentile — and every one of them is a cookbook entry file or a tools index [entrance: cookbook/database-server/src/index.ts, cookbook/image-gen-server/src/index.ts, cookbook/nba-server/src/tools/index.ts]. Sixteen of the seventeen are named index or index-variant [entrance ×17].

Twenty-two rooms sit at or above the 90th percentile of centrality [hub ×22]. Eighteen of those also carry fan-out at or above the median, making them high-centrality, high-fan-out junctions [corridor ×18]. The junctions cluster in two places: the image-gen provider set and the src type and policy files [corridor: cookbook/image-gen-server/src/providers/index.ts, src/types/index.ts, src/security/config/tool-policies.ts].

Twenty-one rooms sit at or above the 90th percentile of load index — the position name is high-load hub, a position in the import graph, not a claim about what breaks [foundation ×21]. Seven sit in cookbook, fourteen in src, and the src set concentrates on the security utilities and the shared type declarations [foundation: src/security/utils/error-sanitizer.ts, src/security/utils/security-logger.ts, src/types/policies.ts].

Forty-two rooms carry last-touched days at or above the 90th percentile [dark_room ×42]; thirty-five of them are cookbook rooms, including every vitest config in that wing [dark_room: cookbook/nba-server/vitest.config.ts, cookbook/kenpom-server/vitest.config.ts]. Twenty-one rooms sit at or below the 10th percentile of last-touched days, and all twenty-one are in src, under security and types [lit_room ×21].

Thirty-seven rooms hold neglect index at or above the 90th percentile together with load index at or above 0.10 [flooded_basement ×37]. The overlap with the untouched set is close to total; the src members are the content and semantics helpers and the tool registry [flooded_basement: src/security/utils/tool-registry.ts, src/security/layers/layer-utils/content/unicode.ts].

Fifty-three rooms carry a reinforcement index of 0.5 or higher [scaffolding ×53]. Nineteen rooms have zero fan-out and fan-in at or above the 75th percentile — imported leaves, terminal in the graph [leaf_utility ×19]. Several leaves are also high-load hubs [foundation: cookbook/monitoring-server/src/utils/alert-manager.ts, cookbook/monitoring-server/src/utils/metrics-collector.ts, src/security/constants.ts].

Forty-seven rooms are co-located across more than one of these positions, and 196 marks in total are diagnostic [hub: src/security/config/tool-policies-config.ts, src/types/server.ts, src/security/utils/error-sanitizer.ts].

24 decorative marks render but are not a diagnosis: 21 high edit-pressure nodes [crack ×21] and 3 unreinforced high-load nodes with high edit pressure [toothpick_wing ×3]. Both rest on bug_pressure_index, which the gate records as unvalidated; neither is used in any reading above.

The stance is disclosed here rather than assumed [foundation ×21]. The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- brief_version: `0.1.0`
- effort: `high`
- facts_hash: `987906877c8ec5193cfc29f27077392d4f9637d2f429b57536317f875e0991ed`
- input_tokens: `10349`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `2373`
- relinted: `brief 0.1.0`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary, R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features excluded from diagnosis, R5 position-name disclosure, R6 no whole-building label, R7 decorative count stated.
