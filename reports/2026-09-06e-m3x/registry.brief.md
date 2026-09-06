# uluops-registry-api — architect's brief

*Register lint: **PASS on attempt 3**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `e12154effd3d…`, facts `cde3c96ad400…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.3.0; a PASS is a pass under that grammar (D-035).*

The building holds 267 rooms in 3 wings. 230 of them sit in src, where src/index.ts is the declared package entry [package_entry: src/index.ts]; 30 sit in scripts, among them scripts/run-deep-analysis.ts [import_root ×11: scripts/run-deep-analysis.ts]; 7 more sit at the top level. Across all profiles 352 diagnostic marks land, and 88 rooms carry more than one.

27 rooms carry foundation — a high-load hub, a position in the import graph, not a claim about anything happening to them — and all 27 sit in src [foundation ×27: src/db/connection.ts, src/utils/logger.ts]. The 27 maintainability foundation rooms are the same 27 rooms as the onboarding foundation rooms [foundation ×27; onboarding/foundation ×27].

27 rooms sit at hub, all 27 in src [hub ×27: src/schemas/enums.ts, src/utils/errors.ts]. 13 rooms sit at corridor, a high-centrality, high-fan-out junction, all 13 in src [corridor ×13: src/config/database.ts, src/db/repository/index.ts]. The 13 corridor rooms are within the 27 hub rooms [corridor ×13; hub ×27], and the same 13 are within the 133 scaffolding rooms [corridor ×13; scaffolding ×133].

133 rooms carry scaffolding, all 133 in src [scaffolding ×133: src/middleware/error-handler.ts, src/services/safety/risk-calculator.ts, src/utils/circuit-breaker.ts].

27 rooms carry dark_room — a long-untouched room, a position in the edit record — with 26 of the 27 in src and 1 in scripts [dark_room ×27: src/db/migrations/001_create_definitions.ts, src/terminal/banner.ts, scripts/run-seed.ts]. 26 rooms carry flooded_basement — a long-untouched, still-imported room — 25 of them in src and 1 in scripts [flooded_basement ×26: src/utils/retry.ts, src/routes/v1/render.ts, scripts/run-seed.ts]. The 26 flooded_basement rooms are within the 27 dark_room rooms [flooded_basement ×26; dark_room ×27].

40 rooms carry lit_room, all 40 in src [lit_room ×40: src/controllers/user-controller.ts, src/services/definition/quota.ts]. The single package_entry room is within the 40 lit_room rooms and within the 133 scaffolding rooms [package_entry ×1; lit_room ×40; scaffolding ×133].

11 rooms sit at import_root, an import-graph root, 8 in scripts and 3 in src [import_root ×11: scripts/calibration-gate.ts, src/services/index.ts]. 20 rooms sit at leaf_utility, an imported leaf, all 20 in src [leaf_utility ×20: src/utils/json.ts, src/schemas/wdl/types.ts].

27 decorative marks render but are not a diagnosis [crack ×27]; crack names a high edit-pressure node, and its rooms are not listed here.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited, fixes should not concentrate — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `3`
- attempts_log: `1: R3-number; 2: R5-disclosure; 3: pass`
- brief_version: `0.3.0`
- effort: `high`
- facts_hash: `cde3c96ad4002d880af8e041fc317b690f7c2637ff57b5b8fe4b5bdca54762da`
- input_tokens: `11324`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3522`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb — shares are by_wing counts (D-036).
