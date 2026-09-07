# typeorm — architect's brief

*Register lint: **PASS on attempt 3**. What the lint checked: every paragraph cites a feature and a room it fired on, or a count the skeleton records; a room named in a sentence is covered by a feature cited in that sentence; consequence and forecast vocabulary is refused outside a struck disclosure clause; numbers come from the facts sheet and sit in the sentence that cites their feature; features with the same or nested rooms are named together; a directory named contains a cited room; no distributional adverb or ranking of marks; a number wears its unit; an identity between predicates names the conjunct that did no work; a feature's dominant directory is named with its population and cited; a nesting is not an identity and a shared predicate is one measurement; the decorative disclosure names its ungrounded signal; no 'validated' where no signal holds it; decorative features are cited by count only and never as diagnosis; a consequence-implying name carries its position name where first used; no whole-building label. What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. Profile maintainability + onboarding, geometry age, skeleton `e437a70f7562…`, facts `f3a952900fe4…`. Calibration: in-repo, self-relative (system spec §5.3); one frame — stability is read from a time-lapse, not from this page — the time-lapse for this skeleton is the one under gate `179d8acb7b0c`. Brief 0.5.0; a PASS is a pass under that grammar (D-035).*

The building holds 583 rooms in 7 wings: 496 in src, 69 in packages, 9 in docs, 3 in (root), 3 in playground, 2 in extra, 1 in docker. Across all profiles it carries 619 diagnostic marks, 483 of them in the base profile, and 160 rooms carry two or more diagnostic marks. 164 rooms carry scaffolding — a test-imported room at or above the median reinforcement, a position and nothing more — 147 of them in src and 17 in packages [scaffolding ×164: src/util/OrmUtils.ts, packages/codemod/src/lib/colors.ts].

70 rooms carry dark_room — a long-untouched room, a position in the age geometry — all 70 in src, with 33 in src/error, a directory of population 61, among them src/error/TypeORMError.ts [dark_room ×70: src/error/TypeORMError.ts].

flooded_basement — a long-untouched, still-imported room — adds load_index >= 0.10 to dark_room and it excludes nothing on this repository: the 70 rooms are the same 70 [flooded_basement ×70; dark_room ×70]. Those 70 all sit in src, 33 of them in src/error, population 61, including src/error/QueryRunnerAlreadyReleasedError.ts [flooded_basement ×70: src/error/QueryRunnerAlreadyReleasedError.ts].

foundation — a high-load hub, a position in the import graph — fires on 59 rooms, 57 in src and 2 in packages [foundation ×59: src/metadata/EntityMetadata.ts, packages/codemod/src/transforms/stats.ts]. The maintainability and onboarding readings of foundation are the same predicate under two profiles, the same 59 rooms [foundation ×59; onboarding/foundation ×59]. 60 rooms carry hub, all 60 in src [hub ×60: src/metadata-args/MetadataArgsStorage.ts].

corridor, a high-centrality, high-fan-out junction, nests within hub: its 37 rooms all sit in src, and the extra conjunct fan_out >= p50 removes 23 rooms of hub [corridor ×37: src/query-builder/WhereExpressionBuilder.ts; hub ×60]. 60 rooms carry lit_room, 57 in src, 2 in packages, 1 in (root) [lit_room ×60: src/driver/expo/ExpoDriver.ts, packages/codemod/eslint.config.mjs, eslint.config.mjs].

33 rooms carry leaf_utility, an imported leaf, 29 in src and 4 in packages [leaf_utility ×33: src/driver/types/UpsertType.ts, packages/codemod/src/transforms/todo.ts]. package_entry, a declared package entry, fires on 6 rooms, 4 in src — a directory of population 5 here — and 2 in packages [package_entry ×6: src/cli.ts, packages/legacy-naming-strategies/src/index.ts]. import_root, an import-graph root, nests within package_entry: 1 room in packages, and the conjunct fan_in == 0 and fan_out >= p75 removes 5 rooms of package_entry [import_root ×1: packages/codemod/src/index.ts; package_entry ×6].

61 decorative marks render but are not a diagnosis [crack ×59; toothpick_wing ×2]. crack — a high edit-pressure node — and toothpick_wing — an unreinforced high-load node with high edit pressure — rest on bug_pressure_index, which is unvalidated.

The building is drawn as it is, warts and all. The diagnosis presupposes a norm of health — load should be reinforced, old load-bearing code should be visited — and that norm is a maintenance stance the reader may reject, stated so it reads as an ought, not a fact.

## Provenance

- attempt: `3`
- attempts_log: `1: R15-composition; 2: R11-share, R12-unit, R12-unit; 3: pass`
- brief_version: `0.5.0`
- effort: `high`
- facts_hash: `f3a952900fe4d88c851b02a58725ead303b838234a4dd1e3ced48b3a128ac7de`
- input_tokens: `21609`
- model_requested: `claude-opus-5`
- model_served: `claude-opus-5`
- output_tokens: `3801`
- stop_reason: `end_turn`

## Register lint

No violations. Rules: R1 consequence vocabulary and phrases (citations stripped, disclosure clause struck), R2 provenance of every citation, R3 numbers from the facts sheet only, R4 decorative features cited by count only and never as diagnosis, R5 position-name disclosure at first use, R6 no whole-building label, R7 diagnostic and decorative counts stated, R8 rooms named in a sentence covered by that sentence's citations, R9 features with the same or nested rooms named together, R10 a directory named contains a cited room, R11 no distributional adverb or ranking between marks, R12 a number wears its unit, R13 an identity between differing predicates names the inert conjunct, R14 no 'validated' where no signal holds it, R15 a feature's dominant directory named with its population and cited; nestings state the rooms outside; shared predicates are named; the decorative disclosure names its ungrounded signal (D-036, D-037, D-038).
