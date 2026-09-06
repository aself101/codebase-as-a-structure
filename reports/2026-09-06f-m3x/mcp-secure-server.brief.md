# mcp-secure-server — architect's brief

*Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named and cited; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `caf5cc9ff180…`, facts `1ff5b424769a…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.4.0; a PASS is a pass under that grammar (D-035).*

The building holds 202 rooms in three wings: 136 in cookbook, 64 in src, 2 at (root). Across all profiles it carries 287 diagnostic marks, 196 of them in the base profile; 91 rooms carry two or more diagnostic marks, and 49 rooms are marked in more than one profile. scaffolding fires on 53 rooms, 36 in cookbook and 17 in src [scaffolding ×53: cookbook/nba-server/src/tools/team.ts, src/security/utils/validation-pipeline.ts].

The geometry is age. dark_room — a long-untouched room, a position on the last-touch axis, not a claim about what happens there — fires on 42 rooms, 35 in cookbook and 7 in src [dark_room ×42: cookbook/database-server/src/tools/create-order.ts, src/types/messages.ts]. flooded_basement — a long-untouched, still-imported room, a position on the same axis crossed with load — fires on 37 rooms, 30 in cookbook and 7 in src [flooded_basement ×37: cookbook/filesystem-server/src/utils/path-validator.ts, src/security/utils/tool-registry.ts]. Those 37 rooms sit within the 42 dark_room rooms; the two marks fall on one set [flooded_basement ×37; dark_room ×42].

At the other end of the same axis, lit_room fires on 21 rooms, all 21 in src [lit_room ×21: src/security/layers/layer1-structure.ts, src/security/presets.ts].

foundation — a high-load hub, a position in the import graph, not a claim about what breaks — fires on 21 rooms, 14 in src and 7 in cookbook, and the maintainability and onboarding sets are the same 21 rooms [foundation ×21; onboarding/foundation ×21: src/types/policies.ts, cookbook/monitoring-server/src/utils/alert-manager.ts]. hub fires on 22 rooms, 12 in cookbook and 10 in src [hub ×22: cookbook/image-gen-server/src/providers/bfl.ts, src/security/config/tool-policy-validation.ts]. corridor — a high-centrality, high-fan-out junction — fires on 18 rooms, 10 in cookbook and 8 in src, 6 of them in cookbook/image-gen-server/src/providers [corridor ×18: cookbook/image-gen-server/src/providers/openai.ts, src/types/index.ts]. Those 18 rooms sit within the 22 hub rooms [corridor ×18; hub ×22].

The graph edges are marked directly. import_root — an import-graph root — fires on 17 rooms, all 17 in cookbook [import_root ×17: cookbook/http-server/src/index.ts, cookbook/multi-endpoint-server/src/tools/index.ts]. leaf_utility — an imported leaf — fires on 19 rooms, 13 in cookbook and 6 in src [leaf_utility ×19: cookbook/kenpom-server/src/tools/ratings.ts, src/security/layers/contextual-config-builder.ts]. package_entry — a declared package entry — fires on 16 rooms, 13 in cookbook and 3 in src [package_entry ×16: cookbook/tool-policies-server/src/index.ts, src/security/transport/index.ts].

24 decorative marks render but are not a diagnosis: crack — a high edit-pressure node — and toothpick_wing — an unreinforced high-load node with high edit pressure [crack ×21; toothpick_wing ×3].

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R11-share, R11-share; 2: pass`
- brief_version: `0.4.0`
- effort: `high`
- facts_hash: `1ff5b424769ac90b7575e9cd4088ef17a33df7041adef1ed309cf14314c9aa2d`
- input_tokens: `13335`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3460`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named and cited (D-036, D-037).
