# Example role — a declared kind a ruleset may exclude (D-078)

*Drafted 2026-09-24 after Alex's call at D-077/D-078: scopes with a declared example role are excludable from the population, the way D-067 made config, migration and placeholder files excludable. Status: **reviewed; revised and built at D-078** (substrate 0.11.0, brief 0.43.0). Follows `scope-calibration-spec.md` §9 item 2.*

> **Revision after review, 2026-09-24 (tracker run 66).** `foucault-analyst` (CONSTITUTIVE, split): "example" is defined in §1 as a relation — a consumer of the product — and inscribed in §2 as a word list; where the two agree (mcp's cookbook 14 of 14 subtrees import the product entry and none is imported back; typeorm's `playground/`) it is descriptive, and at the margins the word list makes the kind: eslint's `docs/_examples/` (5 rooms importing `lib/api.js`, outside eslint's published `files`) is a consumer the regex misses; typeorm's split-time frame loses 139 `sample/` files the regex matches; and — the load-bearing finding — excluded files leave the population and keep ranking it: 20 of `src/index.ts`'s 21 importers on mcp are cookbook files, and the blends rank against the 203-node substrate population, 136 of it cookbook. `software-architecture-expert-validator` (IMPRECISE 74): the mechanism corresponds; §2 misquoted its source (the re-rank changed foundation's membership on mcp, Jaccard 0.67, and crossed eslint's flooded_basement floor — "at most two rooms" was the "otherwise" case); "the page becomes the library's" is unqualified while the blend legend (`brief.py:2201`) and the population rule (`brief.py:2863`) would name two different populations; §5's grading is `m_asserted` = 3 across repositories, not per repository; `SPEC_G1` is not "the asserted set"; three allow-lists (`ruleset.py:316`, `brief.py:367`, `assemble.py:330`) and a dozen tests the spec did not name would fail the build. All re-checked here.
>
> **Revisions taken (D-078).** (1) The regex is the declared proxy for §1's relation, widened by an optional leading underscore: `(^|/)_?(examples?|samples?|demos?|cookbook|playground)/` — eslint's `docs/_examples/` is a consumer under the category Alex approved; and the relation is recorded beside the proxy: `summary.example_dirs` counts, per matched directory, its files, its imports into the rest of the repository, and the imports from the rest into it (mcp: 136 files, 20 in, 0 back). (2) The page says what the exclusion does not do: the importer clause names example importers, and the blend legend states its rank population ("each input a rank among this repository's N non-test files, M of them of kinds the ruleset does not count"). (3) The time-lapse limit is stated (a convention applied to past frames removes files that were rooms then). (4) Citations and the grading mechanism corrected; the touch points built. The sections below keep the draft's text where it was not wrong.

## 1. The decision this implements

A scope that is a consumer of the repository's product — mcp-secure-server's `cookbook/`: thirteen client servers under a private workspace-root manifest, 10 of the servers depending on the library by `file:../..` and the workspace root by `file:../` (11 of the 14 manifests; D-077 said "11 of 14 cookbook servers" — corrected at D-078), whose 20 cross-scope imports all enter at `src/index.ts`, and none of which the root's published `files` (`dist/`, docs) contains (verified at `5348b3ef614d`) — is not a room of the building. Today it is 122 of the page's 187 rooms and sets most of the cutoffs the library is ranked against (`scope-calibration-spec.md` §2; the composition clause, brief 0.42.0: the library, 65 of 187 rooms, holds 17 of 19 foundation and all 27 lit rooms). Alex chose exclusion by declared role over keeping the pooling and over per-product pages.

## 2. The convention (substrate 0.11.0)

- `file_kind` gains the value `example` (`inventory.py:37–60`), assigned by a declared directory convention: `SubstrateConfig.example_dir_regex = r"(^|/)(examples?|samples?|demos?|cookbook|playground)/"`, a path regex like `migration_dir_regex` (`config.py:153`), fingerprinted.
- Precedence: config > migration > placeholder > **example** > source. A tool configuration inside an example directory stays `config`; both are excluded by the shipped rulesets, so the order changes no population, only which count the file is reported under.
- A G1 flag `is_example` (`assemble.py:208–211`), entered in the grounding table beside `is_config` and `is_migration` (`validation/config.py:89–110`, `flag: true`, `ripple: own`, instrument "path regex (example_dir_regex)"), and in the spec's G1 membership `SPEC_G1` (`validation/config.py:243–263`; `tests/test_gate.py:308` holds the two equal).
- `summary.file_kinds` counts `example` with the others (`assemble.py:330`).
- **The substrate's own rank population does not change.** As with D-067's kinds, the substrate ranks every non-test node with history (`assemble.py:256–260`) and the mapper excludes; no index value moves. The architecture review measured the alternative (per-population re-rank): it changes foundation's membership on mcp (Jaccard 0.67), moves eslint's flooded_basement through its literal floor, and otherwise at most two rooms a feature (`scope-calibration-spec.md` revision note). The page states the rank population instead (§4).

**What the regex catches on the reference set** (rooms under the shipped rulesets, measured on the pinned tips): mcp-secure-server 122 (all `cookbook/`); typeorm 3 (`playground/`); uluops-registry-api 0; eslint 0.

## 3. The rulesets

`maintainability.toml` 0.3.4 and `onboarding.toml` 0.3.1 add `example` to `exclude_kinds` (`maintainability.toml:26`, `onboarding.toml:18`); an overlay must match its base (the population is one, D-067). The ruleset's version bumps because its population changes.

## 4. The page (brief 0.43.0)

- The population rule counts the example files the ruleset removed, in the sentence that already counts config, migration and placeholder files (`excluded_by_kind`), and `KIND_CONVENTION_WORDS` states the convention ("a file under a directory named examples, samples, demos, cookbook or playground").
- On mcp-secure-server the page becomes the library's: 65 rooms, one package scope, so the composition clause (D-077) no longer fires there; on typeorm it continues for `packages/codemod` (a second product, not an example).

## 5. The gate and the frames

- A new fingerprint: every cached substrate misses. The gate is re-run pinned (`--repo …/mcp-secure-server@5348b3ef614d --tuning-repo …/uluops-registry-api@e947c5b67542`; typeorm and eslint at their reference commits), the recipe in `docs/state-2026-09-13.md` §88. Expected: every existing signal's status, stability and holdout numbers identical (the substrate's values do not move); `is_example` graded — G1, and `untested` on any repository where it is a constant (registry and eslint have no example rooms, as `is_migration` was untested at D-067).
- The time-lapse frames are regenerated (a population change moves the skeleton on mcp-secure-server and typeorm).

## 6. What this does not do

- It does not exclude a scope by its manifest. The architecture review suggested manifest evidence (`private`, a `file:` dependency on an in-repo package, absence from the root's `files`) as corroboration; it is recorded here as a check a future version could add to the summary, not built — a directory convention is what D-067 used, and the manifest signals are uneven even on the one case (the workspace-root manifest is `private`, none of the thirteen servers is; three servers declare no dependency on the library at all).
- It does not decide per-product pages (D-077: named, not bundled).
- It does not touch typeorm's `packages/codemod`.

## 7. Limits (for the legend)

- A convention, not a detection: a library whose `examples/` directory is its documented, tested API surface loses those files as rooms; a consumer directory named otherwise stays in.
- `playground/` on typeorm is three files of a sample app; `sample/` directories deleted before HEAD are not rooms anyway.

## 8. Breaks if

A reference repository names its product code under one of the convention's words (a package called `demos` that is shipped) — then the regex is the ruleset's to narrow, as `config_file_regex` was narrowed to the package root; or the gate moves any existing verdict — then the substrate change was not value-neutral and is re-read before the pages are regenerated.
