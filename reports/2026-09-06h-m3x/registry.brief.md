# uluops-registry-api — architect's brief

*Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `f25b7e76f18b…`, facts `b745843cac1f…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.5.0; a PASS is a pass under that grammar (D-035).*

The building holds 267 rooms in 3 wings: 230 in src, 30 in scripts, 7 at the root. Across all profiles 352 diagnostic marks land, 280 of them in the base profile, and 88 rooms carry two or more diagnostic marks. scaffolding — position name: test-imported room at or above the median reinforcement, a position, not a claim about what holds anything up — fires on 133 rooms, all 133 in src [scaffolding ×133: src/db/connection.ts, src/utils/logger.ts].

dark_room — position name: long-untouched room — fires on 27 rooms, 26 in src and 1 in scripts, with 11 of the 27 in src/db/migrations, a directory holding 55 rooms [dark_room ×27: src/db/migrations/001_create_definitions.ts, scripts/run-seed.ts]. flooded_basement — position name: long-untouched, still-imported room — fires on 26 rooms, 25 in src and 1 in scripts, and 11 of those 26 also sit in src/db/migrations, which holds 55 rooms [flooded_basement ×26: src/db/migrations/016_add_fulltext_search_index.ts, src/terminal/styles.ts]. flooded_basement nests within dark_room: 26 rooms shared, 1 room left outside by the added load_index conjunct [flooded_basement ×26; dark_room ×27].

foundation — position name: high-load hub — carries 27 rooms under the maintainability profile and 27 rooms under the onboarding profile; this is the same predicate under both profile names [foundation ×27; onboarding/foundation ×27]. Both name src/db/connection.ts and src/utils/hash.ts [foundation: src/db/connection.ts, src/utils/hash.ts].

hub fires on 27 rooms, all 27 in src [hub ×27: src/config/database.ts, src/schemas/enums.ts]. corridor — position name: high-centrality, high-fan-out junction — fires on 13 rooms, all 13 in src, and nests within hub, the fan-out conjunct leaving 14 hub rooms outside [corridor ×13; hub ×27]. corridor also nests within scaffolding, with 120 scaffolding rooms outside [corridor ×13; scaffolding ×133].

lit_room fires on 40 rooms, all 40 in src [lit_room ×40: src/controllers/user-controller.ts, src/services/definition/quota.ts]. package_entry — position name: declared package entry — fires on 1 room, that room being src/index.ts in the src directory, which holds 2 rooms [package_entry ×1: src/index.ts]. package_entry nests within lit_room, 39 lit_room rooms outside, and within scaffolding, 132 scaffolding rooms outside [package_entry ×1; lit_room ×40; scaffolding ×133].

import_root — position name: import-graph root — fires on 11 rooms, 8 in scripts and 3 in src, with 8 of the 11 in scripts, which holds 27 rooms [import_root ×11: scripts/calibration-gate.ts, src/services/index.ts]. leaf_utility — position name: imported leaf — fires on 20 rooms, all 20 in src, with 9 of the 20 in src/utils, which holds 22 rooms [leaf_utility ×20: src/utils/uuid.ts, src/schemas/wdl/types.ts].

27 decorative marks render but are not a diagnosis: crack, position name high edit-pressure node, rests on bug_pressure_index, which is unvalidated [crack ×27].

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R11-share, R3-number, R15-composition, R4-decorative; 2: pass`
- brief_version: `0.5.0`
- effort: `high`
- facts_hash: `b745843cac1f1f968cbbbecdc241a0113cbe8d8392c6ce5cb2055d8dfc189d53`
- input_tokens: `12872`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `4461`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038).
