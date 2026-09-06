# typeorm — architect's brief

*Register lint: **PASS on attempt 2**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named and cited; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `2e1af3cc5da0…`, facts `3323911e59e3…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.4.0; a PASS is a pass under that grammar (D-035).*

The building holds 583 rooms across 7 wings: 496 in src, 69 in packages, 9 in docs, 3 at the root, 3 in playground, 2 in extra, 1 in docker. 619 diagnostic marks land across all profiles, 483 of them in the base profile; 160 rooms carry two or more diagnostic marks across all profiles, and 84 rooms are marked in more than one profile. 164 rooms sit at or above the reinforcement threshold, 147 in src and 17 in packages [scaffolding ×164: src/util/OrmUtils.ts, packages/codemod/src/lib/colors.ts].

70 rooms hold the long-untouched position — dark_room is a long-untouched room, a position on last-touch age, not a claim about what happens inside one — and all 70 sit in src, with src/error the dominant directory [dark_room ×70: src/error/TypeORMError.ts, src/common/ObjectLiteral.ts]. The 70 flooded_basement rooms — a long-untouched, still-imported room, again a position — are the same 70 rooms as dark_room, all in src and dominated by the same directory, src/error [flooded_basement ×70: src/error/MissingDriverError.ts, src/metadata-args/CheckMetadataArgs.ts]. flooded_basement adds load_index >= 0.10 to dark_room and it excludes nothing on this repository: the 70 rooms are the same 70.

59 rooms hold the high-load hub position — foundation names a position in the import graph, not a claim about anything happening to it — 57 in src and 2 in packages [foundation ×59: src/metadata/EntityMetadata.ts, packages/codemod/src/transforms/stats.ts]. Those 59 rooms in the maintainability profile are the same 59 rooms as the onboarding reading [foundation ×59; onboarding/foundation ×59]. 60 rooms stand at the centrality threshold, all in src [hub ×60: src/metadata-args/MetadataArgsStorage.ts, src/index.ts]. The 37 rooms at the high-centrality, high-fan-out junction position sit within that set of 60 [corridor ×37: src/metadata-args/TableMetadataArgs.ts; hub ×60]. 60 rooms carry the recent-touch position, 57 in src, 2 in packages, 1 at the root [lit_room ×60: src/query-builder/QueryBuilder.ts, packages/codemod/src/transforms/v1/mongodb-types.ts, eslint.config.mjs].

One room holds the import-graph root position, in packages, in the directory packages/codemod/src [import_root ×1: packages/codemod/src/index.ts]. That single room sits within the 6 declared package entries, 4 of which sit in src [package_entry ×6: src/cli.ts, packages/legacy-naming-strategies/src/index.ts; import_root ×1]. 33 rooms hold the imported-leaf position, 29 in src and 4 in packages [leaf_utility ×33: src/driver/types/ColumnTypes.ts, packages/codemod/src/lib/colors.ts].

61 decorative marks render but are not a diagnosis [crack ×59; toothpick_wing ×2]; crack is a high edit-pressure node and toothpick_wing an unreinforced high-load node with high edit pressure, and neither rests on a confirmed signal.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `2`
- attempts_log: `1: R3-number, R3-number, R1-consequence, R5-disclosure, R5-disclosure; 2: pass`
- brief_version: `0.4.0`
- effort: `high`
- facts_hash: `3323911e59e3009758cccb918afd664f234db5152c9d9331a6dac0756a76c129`
- input_tokens: `21362`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `4591`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named and cited (D-036, D-037).
