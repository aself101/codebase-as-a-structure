# Scope calibration — ranking a pooled monorepo (structural-mapper spec §7 Q7)

*Drafted 2026-09-24, the second of the three items deferred at D-075. Status: **reviewed and decided at D-077** — option 1 rebuilt as composition (brief 0.42.0); the identity question reframed as role exclusion and brought to Alex; options 2 and 3 demoted and dropped.*

> **Revision after review, 2026-09-24 (D-077; tracker run 65).** Two specialist reviews read this draft before any code. `data-science-analyst` (UNWARRANTED 52): the §2 table's arithmetic reproduces, but "kept k, added m" under the mixed rule is quota arithmetic — for a single-term pNN the split and pooled sets nest within each part, so kept = Σ min(pooled, mixed) per part, a function of the composition table and nothing more; option 1's cell would print it as a pooling effect, and its added clock rooms are one-commit tie blocks carrying re-anchored names (typeorm's codemod "long-untouched" rooms are 159 days old against the page's 1630). `software-architecture-expert-analyst` (STRAINED 73): the package scope is the wrong partition — mcp-secure-server's root publishes only `dist/`, 11 of its 14 cookbook servers depend on it by `file:../..`, and all 20 cross-scope imports run cookbook → `src/index.ts` (verified at `5348b3ef614d`); the cookbook is a set of client programs outside the building, and the missing option is exclusion by declared role in D-067's grammar. Both measured what §2 left as an adjective: re-ranking the substrate's inputs per scope changes membership, not counts, on mcp (foundation Jaccard 0.67), moves eslint's flooded_basement through its literal `load_index >= 0.10` floor (so §2's "literal thresholds do not move" holds only for the mapper-only rule), and otherwise moves at most two rooms a feature — "understates" is withdrawn. §3's "hid" (typeorm) and "the diagnosis" (mcp, which quoted the decorative crack) overreach and are withdrawn; the defensible reading is composition: the library, 65 of 187 rooms, holds 17 of 19 foundation rooms and all 27 lit rooms, and the cookbook all 15 import roots. Options 2 and 3 also omitted the time-lapse: a mixed rule flips a scope from pooled to split in the frame it crosses 30 rooms. The sections below are kept as drafted; §9 records the outcome.

## 1. The question as the record states it

Every pNN ranks one repository's rooms as one population (system spec §5.3, "in-repo, self-relative … v0 default"; D-019), across every `package.json` scope the population spans (`mapper/engine.py:276–286`: the population is every non-test node with indices outside the ruleset's excluded kinds; `_apply` resolves each pNN over all of it, `engine.py:169–186`). The page states the pooling and the rooms per scope (D-053, D-054) and calls per-package calibration open (structural-mapper spec §7 Q7). The mapper spec records why it stayed open: a per-scope population falls under the population floor (30 rooms, D-034, `engine.py:45`) on every scope but the root on eslint and mcp-secure-server, and "a mixed rule (pool below the floor, split above it) is a calibration mode §5.3 does not have."

Nothing has measured how much the pooling moves.

## 2. The measurement (read-only, 2026-09-24)

The mapper's own `_apply` run twice per repository over the pinned gate's tip substrates (`177c129be9b5`) and both rulesets: once over the pooled population as today, once under the mixed rule — each scope of 30 or more rooms ranked as its own population, every smaller scope pooled into one remainder. Counts are rooms per feature.

| repository | scopes (rooms) | split under the mixed rule | largest movement (pooled → kept of them, added) |
|---|---|---|---|
| uluops-registry-api | 1 (206) | none — one scope | no feature moves |
| eslint | 6 (467) | root 432; remainder 35 | corridor 23 → 23 kept, 4 added; foundation, lit_room, crack 44–45 of 47 kept |
| typeorm | 5 (574) | root 497, `packages/codemod` 63; remainder 14 | dark_room / flooded_basement 70 → 70 kept, **19 added**; lit_room 52 of 58 kept, 15 added; hub 51 of 59 |
| mcp-secure-server | 15 (187) | root 65; remainder 122 (fourteen `cookbook/` scopes, the largest 17) | foundation **9 of 19 kept**, 11 added; crack **7 of 20**, 15 added; lit_room **10 of 27**, 15 added; toothpick_wing 0 of 3 |

Features read through a flag or a literal threshold (`package_entry`, `scaffolding`'s `reinforcement_index >= 0.5`) do not move, as they should not.

**A limit on the measurement itself.** The mixed rule above moves only the mapper's cutoffs. The blends the rulesets read (`load_index`, `bug_pressure_index`, and the rest) are computed in the substrate as ranks over the whole repository's nodes — one population of every non-test node with history, no scope split (`assemble.py:256–266`, `derived.py:63` `compute_percentiles`; the ECDF inputs of every index). Under the mixed rule a room in the root scope would still carry a `load_index` built from ranks against the cookbook. The table understates what a full per-scope calibration would move on mcp-secure-server, and is exact only for features that read raw metrics (`last_touched_days`, `centrality`, `fan_out`, `fan_in`).

## 3. What the numbers say

On two of the four reference repositories the pooling is immaterial (registry has one scope; eslint's remainder is 35 of 467 rooms and moves at most four rooms a feature). On typeorm it is moderate and one-directional where it matters: ranked against its own clock, `packages/codemod` contributes 19 long-untouched rooms the pooled ranking hid behind the ORM's older files. On mcp-secure-server it is the diagnosis: 122 of 187 rooms are fourteen example servers, and for foundation, crack and lit_room more than half of the rooms the page names would not be named if the library were ranked against itself.

## 4. Options

1. **State the movement; change no calibration.** The sheet carries, per feature, the count kept and added under the mixed rule; the row's rooms cell says so where the movement is material ("19 (ranked by scope: 9 of these kept, 11 others)"). The page's established move (D-062: where a general mechanism dominates this repository's instance, the page counts it). Mapper untouched; the sheet computes the counterfactual with `_apply`. Floor: say it only where a scope splits.
2. **Adopt the mixed rule in the mapper.** A calibration mode "per package scope where a scope holds 30 or more rooms, pooled below" (§5.3 gains a mode). Cheap to build; the half measure §2 names — the indices stay pooled ranks.
3. **Adopt the mixed rule through the substrate.** Per-scope ranks for every derived input, then the mapper's mixed rule. The whole measure; a substrate schema change, a re-tune question (the D-009 weights were tuned on pooled ranks), and a gate re-run whose stability tests would now rank scopes of 30–60 rooms.
4. **Keep pooling, stated as it is.** What the page does today.

## 5. Recommendation and ownership

**Option 1 now; options 2 and 3 are Alex's.** Option 1 is a descriptive field in the page's existing grammar and moves no position; it makes the pooling's effect as visible as its size already is. Options 2 and 3 change what the building *is* — D-019 and §5.3 take the repository as the unit; a per-scope calibration takes the package — and that is an identity decision, brought as options, not settled in a fix branch. The numbers in §2 are the case for deciding it: on mcp-secure-server the answer changes the page.

## 6. Limits of option 1 (for the legend, if built)

- The counterfactual is the mapper-only mixed rule; the footnote in §2 goes with it ("the blends' inputs stay ranked against the whole repository").
- The remainder is itself a pool of unrelated scopes (mcp's fourteen example servers ranked together); the mixed rule splits only what the floor allows.
- A reader may take "ranked by scope: 9 kept" as the page conceding the other 10 are wrong. They are positions under a different population, not errors under this one.

## 7. Breaks if

The review finds the mixed-rule counterfactual misleading as a single number — then option 1 prints the scope split's cutoffs rather than kept counts, or nothing; or a reader of option 1's cell takes the counterfactual as the page's diagnosis — then it moves to the legend as one line per page.

## 9. Outcome (D-077)

1. **Built (brief 0.42.0):** the composition clause — the by-wing cell names each package scope of 30 or more rooms holding over twice or under half its share of the population's rooms among a feature's rooms: "pooled scopes: 27 of these 27 in package.json, which holds 65 of the 187 rooms". No counterfactual population, no mapper change; `scope_composition` on the sheet; the legend says a pooled scope's share of a feature is not its own top tenth.
2. **To Alex:** the question is not the calibration unit but the room definition — whether a scope with a declared *example* role (a consumer of the repository's product: a `cookbook/` of client servers depending on the library by `file:`) is a room at all, recorded as a flag from a declared convention and excluded by the ruleset as D-067 excluded config and migration files. One population, one calibration mode, no floor cliff, stable over time; on mcp it ranks the library's 65 rooms alone. typeorm's `packages/codemod` is a second product, not an example, and stays pooled and stated.
3. **Demoted:** option 2 (a floor cliff, a calibration mode that changes across time-lapse frames, tie artifacts in 30–60-room scopes, a remainder pool that is no population). **Dropped:** option 3 (at most two rooms a feature on the reference set, against a substrate schema change, a re-tune and a gate re-run).
4. The measurement scripts are the reviewers' and this session's scratch; the numbers are recorded here and in the reviews (run 65).
