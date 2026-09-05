# repo-substrate — Specification (v0.2)

*A deterministic structural fingerprint of a git repository. Given only a repo, its history, and its dependency graph, it derives stable structural signals — load, change pressure, defect pressure, neglect, reinforcement — that reveal how the codebase is actually shaped. The substrate is the product. The codebase-as-structure renderer becomes one consumer of it, and the substrate must be valuable even if that renderer never ships.*

*Supersedes `truthful-extractor-spec.md` (v0.1). The system spec's Component 1 now points here.*

---

## 1. Governing principle

The substrate **emits continuous signals; it never emits a named feature.** This is the v0.1 boundary, redrawn for precision. v0.1 said "measures, does not interpret" — but a useful substrate needs normalized signals (percentiles, composite indices), and those are computations, not raw measurements. So the line is moved one notch and stated honestly:

- Allowed: raw measurements, repo-relative percentiles, and composite indices — anything that resolves to a **continuous, bounded number**. `load_index: 0.92` is fine.
- Forbidden: any **discrete, named structural claim** — a feature (`"toothpick"`), an archetype (`"cathedral"`), or a quality score (`"grade": "D"`). Naming features is the consumer's job (C3 under a profile).

Determinism is not the boundary — naming is. A composite index embeds weight choices and is therefore a small model, not a measurement; that is acceptable here only because the weights are a versioned, inspectable artifact (§3), so every index value remains fully traceable and regressable.

## 2. Scope

In scope for v0:
- One local git repository, one revision (default `HEAD`).
- Per-node raw metrics (node = file; directories are roll-up views over their files).
- A dependency edge set for one language family (JS/TS first — Open Question 2).
- A classified commit timeline.
- A `derived` block per node: repo-relative percentiles and composite indices (§6).
- Repo-level aggregates (raw inputs for downstream archetype classification — not done here).
- Two outputs: a JSON substrate and a deterministic markdown report (§9).

Out of scope for v0:
- No named features, archetypes, or quality scores (§1).
- No rendering, no metric→feature mapping (that is C3).
- No LLM (the optional narrative reader is a separate component).
- No cross-repo, no remote fetch, no multi-language dependency resolution.

## 3. Determinism and seed contract

- Output is a pure function of `(repo content at SHA, extractor_version, config, toolchain_versions)`, where `config` now includes the index weights.
- The **seed** is the content hash of the resolved tree; later stochastic stages consume it.
- The **config_fingerprint** is a hash of the effective config, including index weights, percentile settings, exclude globs, **and `toolchain_versions`** (see below). Two runs with different index weights produce different `derived` values and a different fingerprint — so "why did this file score 0.92 last month and 0.81 now" always resolves to a config/toolchain diff or a code change, never to nondeterminism.
- **`toolchain_versions` — external tools are inside the fingerprint, not outside it.** The substrate shells out to / links against tools whose *own* versions change the output: the dependency extractor (`madge` / `dependency-cruiser` / `tree-sitter` grammar), the graph library (`networkx`), and the history miner (`pydriller`). A silent `madge` upgrade that resolves imports differently would move `fan_in` → `load_index` with no code or config change — exactly the nondeterminism this contract forbids. So the **resolved versions of every value-affecting external tool are captured into `toolchain_versions`, hashed into `config_fingerprint`, and recorded verbatim in `repo` (§4)**. The capture format is pinned: each entry is `"<role>": "<package-name>@<version>"`, where the version string is exactly what the tool's own resolver reports — for a Node tool, the `version` field of its installed `package.json`; for a Python library, `importlib.metadata.version(name)`; for the git binary, the semver-looking token from `git --version`. No normalization beyond trimming: the string is hashed as reported, so two builds that report differently are different fingerprints, which is the intended behavior. The roles present in v0 are `history` (pydriller), `dep_extractor` (dependency-cruiser, D-006), `git`, `python` (the interpreter, `platform.python_version()`), and `substrate` (this package's own version, since its code is a value-affecting input too). There is no `graph` role: PageRank is in-package (§6.2.2). The independent scanner (`altdeps.py`) is part of the package and covered by the `substrate` role. Pinning PageRank's numerics (§6.2.2) is necessary but insufficient without this: it makes the *algorithm* deterministic, while this makes the *toolchain* attributable.
- Re-running on the same SHA with the same `extractor_version`, `config`, and `toolchain_versions` is byte-identical except `extracted_at` (excluded from the seed). A toolchain change is a *fingerprint* change, so a moved value is always attributable — never silent.
- Stable ordering throughout; floating-point values rounded to 4 dp.

## 4. Output schema (v0.2)

```json
{
  "schema_version": "0.2",
  "extractor_version": "0.2.0",
  "extracted_at": "<ISO8601, excluded from seed>",
  "seed": "<sha256 of resolved tree>",
  "repo": {
    "name": "string",
    "head_sha": "string",
    "branch": "string",
    "root_commit_sha": "string",
    "config_fingerprint": "<sha256 of effective config incl. index weights + toolchain_versions>",
    "as_of": "<ISO8601 author_date of the last commit in (ts, sha) order — the reference for every day count>",
    "truncated_at": "<sha or null: set when --truncate-at moved both inventory and history to this split>",
    "toolchain_versions": {
      "dep_extractor": "dependency-cruiser@18.2.0",
      "git": "git@2.53.0",
      "history": "pydriller@2.11",
      "python": "python@3.13.12",
      "substrate": "repo-substrate@0.2.2"
    }
  },
  "summary": {
    "node_count": 0,
    "population_size": 0,
    "percentiles_valid": true,
    "orphan_nodes": 0,
    "graph_available": true,
    "graph_resolution_rate": 0.0,
    "fan_in_instrument_tau": 0.0,
    "graph_instruments_disagree": false,
    "graph_degraded": false,
    "external_imports": 0,
    "unresolved_imports": 0,
    "non_node_imports": 0,
    "blame_failed": 0,
    "alt_scanner_unreadable": 0,
    "tsconfig_malformed": false,
    "total_loc": 0,
    "repo_age_days": 0,
    "commit_count": 0,
    "author_count": 0,
    "authorship_gini": 0.0,
    "test_loc_ratio": 0.0,
    "dep_graph_density": 0.0
  },
  "languages": { "<lang>": { "files": 0, "loc": 0 } },
  "nodes": [
    {
      "id": "src/registry/core.ts",
      "kind": "file",
      "lang": "ts",
      "metrics": { "<raw metrics, see 5>": 0 },
      "derived": {
        "percentiles": {
          "fan_in": 0.93, "fan_in_nonzero": 0.78,
          "churn_lines": 0.95, "fix_count": 0.89, "fix_count_nonzero": 0.71,
          "revert_count": 0.0, "revert_count_nonzero": null,
          "last_touched_days": 0.41
        },
        "indices": {
          "load_index": 0.91,
          "load_index_degraded": false,
          "change_pressure_index": 0.88,
          "bug_pressure_index": 0.82,
          "neglect_index": 0.17,
          "reinforcement_index": 0.0,
          "complexity_proxy_index": 0.74
        }
      }
    }
  ],
  "edges": [ { "from": "src/a.ts", "to": "src/b.ts", "kind": "import" } ],
  "timeline": [
    { "sha": "string", "ts": "ISO8601", "author": "string", "subject": "string",
      "type": "feat|fix|refactor|docs|chore|test|revert|merge|other",
      "matched_rule": "string", "nodes_touched": ["src/a.ts"], "added": 0, "deleted": 0 }
  ],
  "renames": { "<historical path>": "<successor path, one hop>" },
  "caveats": {
    "orphan_nodes": [], "unresolved_import_samples": [], "blame_failed": [],
    "alt_scanner_unreadable": [], "tsconfig_malformed": null
  }
}
```

Per-node `metrics` also carry, beyond the §5 catalog: `centrality` (§6.2.2), `fan_in_alt`, `fan_out_alt`, `test_fan_in`, `test_fan_in_alt` (§5 second-instrument metrics), `test_proximity`, `recent_commit_share` (§6.2.2), and `history_missing` (§5 orphans). `nodes_touched` in the timeline are recorded under the name current *at that commit*; a consumer joining timeline paths to nodes resolves through `renames`. `summary` fields added since the June draft: `fan_in_instrument_tau` and `graph_instruments_disagree` (the local G2 check, D-011), `non_node_imports` (§8's third kind of non-edge), `blame_failed`, `alt_scanner_unreadable`, `tsconfig_malformed` (instrument faults, distinct from absent measurements — 2026-09-04 audit).

When the percentile population is too small (§6.1), `derived.percentiles` and `derived.indices` are `null` per node and `summary.percentiles_valid` is `false`. Raw metrics are always emitted.

**`summary` field definitions** (each is a pure function of the substrate's own `nodes`, `edges`, and `timeline`; pinned 2026-09-04, tribunal "aggregates enumerated but not defined"):
- `node_count` — `len(nodes)`, the post-exclude HEAD inventory (§5).
- `population_size` — nodes in the percentile reference population: `node_count` minus `is_test` files (when `exclude_tests_from_population`) minus orphans (§5).
- `percentiles_valid` — `population_size ≥ N_min`.
- `orphan_nodes` — nodes with `metrics.history_missing: true` (§5).
- `graph_available` — at least one resolved in-repo edge exists.
- `graph_resolution_rate`, `graph_degraded`, `external_imports`, `unresolved_imports` — §6.3 and §8.
- `total_loc` — Σ `size_loc` over all nodes (tests included).
- `repo_age_days` — `(as_of − root commit author_date).days`.
- `commit_count` — `len(timeline)`, merges included.
- `author_count` — distinct author identities across the timeline (email, no mailmap — a known inflation, on the page).
- `authorship_gini` — Gini coefficient of non-merge commit counts per author, in `[0, 1]`; `0.0` when one author.
- `test_loc_ratio` — Σ `size_loc` over `is_test` nodes ÷ `total_loc`; `0.0` when `total_loc = 0`.
- `dep_graph_density` — `len(edges) ÷ (node_count × (node_count − 1))` over the directed graph; `0.0` when `node_count < 2`.
- `languages` (sibling block) — per detected language, `files` and `loc` over nodes; language is determined by extension via a pinned table in config.

## 5. Raw metric catalog

**Node-set invariant.** The substrate's `nodes[]` is exactly the **post-exclude file inventory at HEAD** (or at `--rev`/`--truncate-at`, §8) — the files that *exist* at the analyzed revision. History is then attached to those nodes. A file that was deleted before HEAD has history in the miner but is **not** a node: it is dropped (build order §11 step 3). This keeps `nodes[]` equal to the live inventory, and the percentile population (§6.1) equal to the live inventory *minus* `is_test` files and orphans; a phantom node would distort every percentile and the node count. *(Wording corrected 2026-09-04 — the June draft said "population equal to the live inventory," which contradicted §6.1's test exclusion; tribunal contradiction C2.)*

### Tier 1 (required)
`size_loc`, `age_days` (rename-followed first-touch), `last_touched_days`, `commit_count`, `churn_lines` (Σ added+deleted), `fix_count` (commits where `type ∈ {fix, revert}`), `revert_count`, `author_count`, `fan_in`, `fan_out`, `is_test`, `has_sibling_test`, `introduced_idx` (timeline position of introducing commit), and — promoted from Tier 2 on 2026-09-04 (D-004) because the `asserted` bar needs them as cross-modal counterparts — `cochange_degree` and `blame_age_median`.

Each carries a candidate structural signal (documentation of intent, not a mapping): `fan_in`→load-bearing; `churn_lines`→instability; `fix_count`→stress; `age_days`/`last_touched_days`→era/occupancy; `introduced_idx`→build phase; `has_sibling_test`→reinforcement; `cochange_degree`→hidden corridors (coupling not visible in imports).

**Pinned definitions for the two promoted metrics.** Both are *counterparts* (`validation-spec.md` §2.4.2): they must be computed from a modality that does not appear in the formula of the signal they check, so their definitions may not lean on the import graph or on commit timestamps respectively.
- **`cochange_degree`** — the number of *distinct other files* that appear together with this file in at least `cochange_min` commits (config, default `2`), counted over **non-merge** commits that touch at most `cochange_max_files` files (config, default `30`; bulk reformat and mass-rename commits are excluded because every file co-changes with every file in them and the signal collapses). Rename-followed: co-occurrence is recorded under canonical paths. Cost is quadratic in files-per-commit, bounded by the cap. It reads only `nodes_touched` from the timeline — no edges, no timestamps.
- **`blame_age_median`** — the median, over the file's non-blank lines at HEAD, of `(as_of − line's last-modified author_date)` in days, from `git blame -w` (whitespace-insensitive, rename-following via `-M -C` off by default to keep it cheap and deterministic). It measures how old the *surviving text* is, which is independent of when the file was last touched (a one-line edit yesterday moves `last_touched_days` to 0 and `blame_age_median` almost not at all). A file with zero non-blank lines has `null`. Cost is one blame per file; on the reference repos (≤ 700 source files) it is seconds, and it is cached by `(sha, path)`.

### Tier 2 (defer unless cheap)
`complexity` (cyclomatic, per-language parser), `public_surface_ratio` (exported vs. internal — the "no door" signal), `comment_density`. v0 uses a cheap nesting/LOC proxy for intricacy instead of real cyclomatic; real cyclomatic on JS/TS is wanted as the cross-modal counterpart for `complexity_proxy_index` and moves to Tier 1 when a pinned tool is chosen. `cochange_degree` is also the intended basis for a future **`blast_radius_index`** — the *validated* (predictive) signal that will eventually carry the change-propagation/consequence claim that descriptive signals are forbidden to smuggle (`validation-spec.md` §2.1.1, §2.3).

**Second-instrument metrics (D-008).** Two further Tier-1 metrics exist only so the validation gate can check resolver-dependent facts against an independent reading (`validation-spec.md` §2.4.2, class G2); they are emitted, never consumed by an index:
- **`fan_in_alt`, `fan_out_alt`** — in-repo import edges found by an independent regex scanner with its own resolver (`altdeps.py`): `import … from`, `export … from`, `require()`, and `import()` specifiers; relative paths resolved by extension and `index` probing; `tsconfig` `baseUrl`/`paths` aliases honored; bare specifiers ignored. Same edge contract as §8 (self-loops dropped, duplicates collapsed). It shares no code with the primary extractor, which is the point: where they disagree, the disagreement is the measurement of extractor fidelity (open question #8). `null` for non-JS/TS nodes.
- **`test_fan_in`** — the number of primary-graph importers of this node that are `is_test` files. A test that imports X reinforces X whatever the file is called; this is the import-graph reading of reinforcement, against which the path-convention reading (`has_sibling_test`) is checked.

**Orphan nodes.** A file that exists at HEAD but has no `FileHistory` cannot occur under a correct miner: every HEAD file was introduced by some commit on the traversed branch. It *can* occur under a miner defect (a rename-alias chain broken by path reuse, a submodule path, a file added by a commit outside the traversal). The substrate treats it as a **defect signal, not a data case**: the node is emitted with its static metrics (`size_loc`, `fan_in`, `fan_out`, `is_test`, `has_sibling_test`, `nesting_proxy`), every history-derived metric `null`, `metrics.history_missing: true`, and `summary.orphan_nodes` incremented. Orphans are **excluded from the percentile population** (a `null` cannot be ranked) and listed in the report's caveats section. A run with `orphan_nodes > 0` is a bug report against the miner, on the page rather than silently zero-filled. *(Added 2026-09-04; tribunal must-fix #2.)*

## 6. Derived signals

The substrate reveals truth in three layers of increasing synthesis: raw facts (§5), repo-relative position (§6.1), and composite pressure (§6.2). The first is measurement; the second is normalization; the third is a small, versioned model.

### 6.1 Percentiles

Repo-relative position — "how unusual is this file inside this repo?" — surfaces truth without interpretation.

- **Keyset (exhaustive).** A percentile is computed for **every continuous metric**, not only the ones shown in the §4 example. The complete `derived.percentiles` keyset is: `size_loc`, `age_days`, `last_touched_days`, `commit_count`, `churn_lines`, `fix_count`, `revert_count`, `author_count`, `fan_in`, `fan_out`, `cochange_degree`, `blame_age_median`, plus the three `_nonzero` variants (`fan_in_nonzero`, `fix_count_nonzero`, `revert_count_nonzero`). The §4 schema lists a representative subset; this is the authoritative set. Two **derived** inputs are also percentile-ranked where §6.2.2 defines them — `centrality` (graph PageRank) and `nesting_proxy` — so they appear in `derived.percentiles` too when available. Discrete signals (`is_test`, `has_sibling_test`) and bounded ratios (`fix_ratio` = `fix_count / commit_count`, already in `[0,1]`) are **not** percentiled — they are used directly. Every percentile an index formula (§6.2.1) references must appear here.
- **Population.** All included source files after exclude globs. A config flag (`exclude_tests_from_population`, default true) drops `is_test` files so test scaffolding does not skew the distribution. Test files are still measured; they are just not part of the reference population.
- **Method.** Empirical CDF with **average-rank ties**, so identical values share one percentile. Range `[0, 1]`.
- **N-floor.** If `population_size < N_min` (default 30, config), percentiles are not statistically meaningful: emit `null` percentiles and indices, set `percentiles_valid: false`, keep raw metrics. Never fabricate ranks for tiny repos.
- **Zero-spike.** Metrics with a large mass at the floor — `fan_in` (most files import nothing), `fix_count`, `revert_count` — give the whole floor cohort a single low percentile under average-rank. This is honest but lumpy, and it is precisely where the load and bug-pressure signals need resolution. **v0 ships the `_nonzero` variant** (resolved, was Open Q5): for `fan_in`, `fix_count`, and `revert_count`, also emit a percentile ranked only among nonzero values — `fan_in_nonzero`, `fix_count_nonzero`, `revert_count_nonzero`. The standard percentile is still emitted alongside. This is reclassified from "optional" to **near-load-bearing**: on import-sparse repos the plain `fan_in` percentile collapses most files to one floor value, which makes `load_index` mush. `load_index` and `bug_pressure_index` therefore consume the `_nonzero` inputs (§6.2). A file at the floor (`fan_in == 0`) has no `fan_in_nonzero` percentile; it is treated as 0.0 for that input, so floor files contribute zero load from this term rather than a spurious shared rank.

### 6.2 Composite indices

Each index is a weighted combination of **normalized inputs** — percentiles, or normalized discrete signals — **never raw metrics** (you cannot sum LOC and `fix_count`). All inputs are unit-free and bounded, so every index lands in `[0, 1]`. Weights live in config and feed `config_fingerprint`; the formulas below show inputs and intent, not final weights (those get tuned in §10).

Canonical names are **pinned** here; earlier drafts drifted (`volatility_index`, `staleness_index`, `test_reinforcement_index`) — those are deprecated aliases of the names below.

| Index | Signal | Normalized inputs |
|---|---|---|
| `load_index` | Load-bearingness | `fan_in_nonzero` pctile, centrality pctile (if graph available), `(1 − fan_out pctile)` light, `size_loc` pctile light |
| `change_pressure_index` | Active instability | `churn_lines` pctile, `commit_count` pctile, `(1 − last_touched_days pctile)` recency |
| `bug_pressure_index` | Historical defect pressure | `fix_count_nonzero` pctile, `revert_count` pctile, `fix_ratio` (= `fix_count / commit_count`, used as a raw `[0,1]` ratio — not percentiled) |
| `neglect_index` | Old, untouched, abandoned | `age_days` pctile, `last_touched_days` pctile, low recent-commit share |
| `reinforcement_index` | Test support | discrete: `has_sibling_test`, test proximity, `is_test`; later coverage |
| `complexity_proxy_index` | Internal intricacy (cheap) | `size_loc` pctile, nesting-depth proxy pctile, `fan_out` pctile, function count if easy |

`reinforcement_index` (**revised 2026-09-04, D-011**) is read from the import graph, not from file naming: `0.0` when no test file imports the node; otherwise `0.5 + 0.5 · percentile(test_fan_in)` among nodes that some test imports, so "one test touches it" and "the most-tested file in the repo" are distinguishable. When the graph is degraded (§6.3) it is `null` with `reinforcement_index_degraded: true`. The path-convention reading (`has_sibling_test`, `test_proximity`) is still emitted as a metric and reported as a correlate, but it is no longer an input: on the reference set it disagreed with the graph reading on three of four repos, and on a repo whose tests are named by feature rather than by module it is simply wrong. Its inputs are unit-free and bounded, so the "normalized inputs only" rule holds.

#### 6.2.1 Pinned v0 weights (placeholders — tuned per `validation-spec.md`)

These are concrete starting weights so the pipeline runs and the holdout has something to tune. They are **placeholders, not claims**: the two fix-predictive indices (`bug_pressure_index`, `change_pressure_index`) are tuned against the temporal-holdout loop (`validation-spec.md` §3); the other four are not falsifiable that way and keep these defaults unless intuition/stability work (`validation-spec.md` §2.1) revises them. Weights live in config and feed `config_fingerprint`, so any change is a versioned diff.

| Index | Weighted sum (inputs in `[0,1]`) |
|---|---|
| `load_index` | `0.5·fan_in_nonzero + 0.3·centrality + 0.1·(1 − fan_out) + 0.1·size_loc` |
| `change_pressure_index` | `0.4·churn_lines + 0.3·commit_count + 0.3·(1 − last_touched_days)` |
| `bug_pressure_index` | `0.5·fix_count_nonzero + 0.2·revert_count + 0.3·fix_ratio` |
| `neglect_index` | `0.4·age_days + 0.4·last_touched_days + 0.2·(1 − recent_commit_share)` |
| `reinforcement_index` | discrete: `1.0` direct sibling test / `0.5` test proximity / `0.0` none |
| `complexity_proxy_index` | `0.4·size_loc + 0.4·nesting_proxy + 0.2·fan_out` |

All names refer to the percentile of that metric unless noted. Weights within each index sum to 1.0 so the result lands in `[0, 1]`. When an input is unavailable (e.g. centrality with no graph — §6.3), its weight is removed and the remaining weights are renormalized to sum to 1.0, and a degradation flag is set.

#### 6.2.2 Pinned definitions for the non-obvious inputs

Four inputs above are not raw metrics and were previously underspecified; pinned here so every index value is deterministic and traceable. Like the weights (§6.2.1) these are **v0 defaults**, but unlike the weights they are *method* choices — changing one changes the metric's meaning, so each is recorded in config and feeds `config_fingerprint`.

- **`centrality`** (in `load_index`): **PageRank** over the directed import graph (edge `from → to` per §8), computed by an **in-package power iteration** (`graph.py`) that replicates networkx's pure-Python `_pagerank_python` semantics exactly and is tested against it: **`alpha = 0.85`, `max_iter = 100`, `tol = 1e-06`** (L1 convergence `err < N·tol`), uniform personalization, uniform dangling distribution (a file that imports nothing redistributes its mass evenly), unweighted edges, plain Python floats summed in sorted-node order. networkx is *not* a dependency: the numeric path must not depend on which sparse or BLAS backend a platform loads. *(Corrected 2026-09-04 — the June text named `networkx.pagerank` as the implementation, which the code never was; the architecture validator caught the divergence.)* All five settings are recorded in config and feed `config_fingerprint`. Values are rounded to 4 dp before ranking, which absorbs last-ulp differences across platforms. PageRank chosen over betweenness for stability under small graph changes (continuity matters for the time-lapse) and lower cost. Percentile-ranked like any metric. Absent graph → the §6.3 degraded path. Note that "present structural position" (`validation-spec.md` §2.1.1) means position *under this method with these parameters*; a different centrality would name a different position, and that is disclosed rather than hidden (tribunal A6).
- **`nesting_proxy`** (in `complexity_proxy_index`): **maximum indentation depth** of the file, language-agnostic — leading-whitespace runs normalized to a unit. Pinned edge cases: a tab counts as one level; the **modal indent width** is the most common positive leading-space count over lines whose leading whitespace is spaces only, ties broken toward the *smaller* width; if no line has leading spaces the width is `1`; a line's depth is `tabs + floor(spaces / width)`; lines inside a run with mixed tabs and spaces are counted as `tabs + floor(spaces / width)` too (no error); blank and whitespace-only lines are skipped; a file with no indented lines has `nesting_proxy = 0`; files over `nesting_max_bytes` (config, default 2 MiB) are `null` (treated as unavailable, weight renormalized). A cheap stand-in for cyclomatic complexity. Percentile-ranked.
- **`recent_commit_share`** (in `neglect_index`): timeline-relative, **not** wall-clock, so it is stable on re-run. Let the **recent window** be the last `recent_window_frac` of the timeline by commit count (config default `0.20`, mirroring the validation split). `recent_commit_share` = (this file's commits inside that window) / (this file's total commits). `neglect_index` uses `(1 − recent_commit_share)`: a file with no recent commits scores high neglect.
- **Test proximity** (a metric and correlate; no longer an index input as of D-011): `1.0` = a **name-matched** test — a test file whose stem (test suffix stripped) equals the module's stem and *either* whose mirrored directory equals the module's directory (`tests/lib/x.js` ↔ `lib/x.js`, `lib/__tests__/x.test.ts` ↔ `lib/x.ts`) *or* whose stem is unique among non-test modules (so `test/unit/utils/x.test.js` reaches `src/security/utils/x.ts` when exactly one module is named `x`); `0.5` = a test file's mirrored directory equals the module's directory, or a stem-matched test exists but the stem is ambiguous; `0.0` = neither. `has_sibling_test` ≝ `test_proximity == 1.0`. The test roots, suffixes, and globs live in config; the unique-stem rule is fixed. *(The June draft's "direct sibling" wording omitted the unique-stem rule; the architecture validator caught the divergence.)*

The substrate still never says `"feature": "toothpick"`. It says `load_index: 0.91, reinforcement_index: 0.0, has_sibling_test: false`, and leaves the naming to C3.

### 6.3 Graph fallback — quality, not just presence

`load_index` leans on `fan_in`/centrality, which require the dependency graph — the most failure-prone input (language pinned to JS/TS in v0, unresolved imports, missing extractor). The substrate must degrade honestly rather than silently. **A graph fails in two ways, and an absent graph is the easy one.** A *present but unreliable* graph — many imports unresolved, or a backend that drops a module pattern — is the dangerous case: it reads `graph_available: true` while `fan_in`/`centrality`/`load_index` are quietly wrong. So degradation triggers on **quality**, not just presence:

- **Absent or empty graph** → `summary.graph_available: false`; `load_index` recomputed from non-graph inputs only (`fan_out`, `size_loc`) with the `fan_in_nonzero`/centrality weights removed and renormalized (§6.2.1); every node sets `derived.indices.load_index_degraded: true`.
- **Present but low-quality graph** → degrade the *same way* even though `graph_available: true`. The substrate emits

  `summary.graph_resolution_rate = resolved_in_repo_edges / (resolved_in_repo_edges + unresolved_imports)`

  where `unresolved_imports` counts **only genuine in-repo resolution failures** — external/package imports are *excluded* (they are successful out-of-repo resolutions, counted in `summary.external_imports`, §8). So the rate measures "of the imports that *should* have resolved to an in-repo file, how many did," not "what fraction of imports are local" — a normal npm repo with mostly-external imports has a *high* resolution rate, not a low one. When the rate falls below `graph_quality_min` (config, default `0.80`), the graph is treated as unreliable: `summary.graph_degraded: true` is set repo-wide and every node sets `load_index_degraded: true`. The rate is always reported so reliability is visible even above the threshold. (Denominator-zero — a repo with no in-repo-looking imports at all — routes through the empty-graph `graph_available: false` path, not a `0.0` rate.)
- **A degraded `load_index` is never silently full-strength.** The `load_index_degraded` flag rides with the value through every downstream artifact (C3 suppresses graph-dependent features on it — see `structural-mapper-spec.md` §4.1), exactly as `percentiles_valid` does for the N-floor case. Degrading is deliberately *not* nulling: nulling would erase the partial signal `fan_out`/`size_loc` still carry.
- **Known residual — mis-resolution.** `graph_resolution_rate` catches the *volume of non-resolution* (imports the extractor couldn't place). It does **not** catch a confident *mis*-resolution — an import resolved to the *wrong* in-repo file (path-alias or re-export confusion), which produces a wrong edge with no unresolved count. That is a deferred **extractor-fidelity** concern: v0 reports resolution rate and degrades on it, but a high resolution rate is *not* a proof of correctness, and the dependency extractor's mapping should be spot-validated (a new extractor-fidelity open question, §12) before `load_index` rankings are trusted on alias-heavy repos. Stated here so the limit is on the page, not assumed away.

## 7. Commit-type classification

Deterministic rule cascade, first match wins, recorded in `matched_rule`:

1. **Conventional-commit prefix** (`/^(feat|fix|refactor|docs|test|chore|revert)\b/i`) → that type, `matched_rule: conventional-prefix`. Note the boundary is `\b`, not a required `:` — so a colon-less subject (`fix login bug`, `Revert "x"`) still matches. This is a deliberate loose reading (catches informal fix/feat subjects), and it has a consequence for stage 2 (below).
2. **Native-revert subject** (git's default `Revert "..."`, regex `/^revert[\s:"]/i`) → `revert`, `matched_rule: native-revert-subject`. *Intended* to run before merge detection so a reverted merge still classifies as `revert`. **AUDIT — currently subsumed:** because stage 1's `revert\b` is satisfied by any of `[\s:"]` (the `\b` lands before the space/colon/quote), every subject this stage could match is already caught at stage 1 and returned as `revert`/`conventional-prefix`. So in the current code `matched_rule: native-revert-subject` is emitted for *zero* commits — the `type` is correct either way, but the stage is dead. See the open item below.
3. **Merge detection** (>1 parent) → `merge`, `matched_rule: merge-parents`.
4. **Subject regex fallback** (`/\b(bug|hotfix|patch)\b/i` → `fix`) → `matched_rule: subject-regex`.
5. **Default** → `other`, `matched_rule: default`.

No probabilistic classification; every type is traceable to a rule. This cascade is authoritative and matches `history.py::classify_commit` in behavior. The validation gate re-runs the same cascade over holdout subjects with its own frozen fallback regex to derive labels (`validation-spec.md` §3.4). It matters beyond C1: validation labels (`validation-spec.md` §3.4) are a pure function of which commits land in `{fix, revert}`. Git-native reverts *are* labeled positive — but via stage 1, not stage 2; stage 2 changes no label.

**Open item (code, not spec).** The dead stage 2 reflects a latent choice. Either (a) drop the redundant `_NATIVE_REVERT` regex, since stage 1 already covers it, or (b) tighten stage 1 to require a conventional delimiter (`:`/`(`/`!`) so stage 2 becomes live and `native-revert-subject` is reachable. Option (b) is **not** label-neutral: it would reclassify colon-less `fix …`/`feat …` subjects out of `{fix}`, moving validation positives — so it must be decided against the holdout, not silently. Until then, this spec describes (a)'s behavior (stage 2 dead) as the truth of the code.

## 8. Tooling

- Python 3.11+.
- History mining: `pydriller` (per-commit modifications, rename-following, author/diff stats). The `HistoryMiner` protocol must honor a revision bound (`rev` / `to_commit`) — the `history_miner.py` `TODO(rev)` — because the validation gate runs the same pipeline truncated at a split SHA (see CLI below and `validation-spec.md` §7). HEAD-only is acceptable for substrate steps 1–9; the bound is required before the holdout (build order step 10).
- Graph metrics: `networkx` (or equivalent) for PageRank centrality (§6.2.2), run with fixed damping/tolerance for determinism.
- `repo.root_commit_sha` (§4) is produced by the assembler via a first-commit lookup (`git rev-list --max-parents=0 <rev>`); it is not part of `history_miner`'s per-file accounting.
- Dependency extraction behind a `DependencyExtractor` protocol; v0 ships JS/TS (shell out to `madge`/`dependency-cruiser` or parse imports with `tree-sitter`). The protocol's edge contract is pinned so `fan_in`/`fan_out` are well-defined:
  - An edge is a **directed** `import` from the importing file to the imported file: `{ from, to, kind: "import" }`.
  - **Self-loops dropped** (a file importing itself).
  - **Duplicates collapsed** — multiple imports of the same target from one file count as one edge (so `fan_out` is distinct-dependency count, not import-statement count).
  - **Only resolved, in-repo targets become edges**, and the two kinds of non-edge are counted **separately** — this distinction is load-bearing for §6.3:
    - **External imports** (a package / out-of-repo path the extractor *correctly* resolved as not-in-this-repo, e.g. `import "react"`) → counted in `summary.external_imports`. These are *successful* resolutions to an out-of-repo target; they are **not** a quality problem and are **excluded** from the resolution rate.
    - **Unresolved imports** (an import that looked in-repo/relative but the extractor *could not place* — a genuine resolution *failure*, e.g. a `tree-sitter` parse miss or an alias it couldn't follow) → counted in `summary.unresolved_imports`. These *are* the quality signal.
    - `summary.graph_resolution_rate` is computed from in-repo failures only (§6.3). Conflating external imports into the failure count would collapse the rate on every normal npm repo (where most imports are external) and falsely trip degradation — so the split is mandatory, not cosmetic.
  - Edges sorted by `(from, to)` for stable output.
- CLI: `extract <repo_path> [--rev HEAD] [--truncate-at <sha>] [--config cfg.toml] -o substrate.json --report substrate-report.md`. `--rev` selects the tip. `--truncate-at <sha>` **supersedes** `--rev`: both the inventory and the history are taken at `<sha>`, so the substrate sees only the training window and its node set is the tree at the split (a HEAD inventory with truncated history would make every holdout-born file an orphan). `repo.truncated_at` records the split.
  - **Three kinds of non-edge**, all counted: `external_imports` (bare specifiers, successful out-of-repo resolutions), `unresolved_imports` (in-repo-shaped specifiers the extractor could not place — the §6.3 quality signal), and `non_node_imports` (resolved to an in-repo path that is not a node: an excluded glob, or a non-source extension such as `.json`/`.css`). Only the second enters the resolution-rate denominator.
- Config: exclude globs, test-path patterns, sibling-test/name patterns, fix-subject regexes, `N_min`, `exclude_tests_from_population`, `recent_window_frac` (§6.2.2), `graph_quality_min` (§6.3, default 0.80), rounding precision, centrality method/params, and **index weights**. All config that affects a value feeds `config_fingerprint`; `toolchain_versions` (§3) does too.

## 9. The substrate report

A deterministic markdown report is the first "render" — not visual, but structurally revealing, and the cheapest possible proof that the signals bite. It is sorted evidence and names **no** building features.

Sections (each top-K, K config-default 10, with contributing raw + derived values shown for traceability):
1. Highest `load_index`
2. Highest `change_pressure_index`
3. Highest `bug_pressure_index`
4. High load + low reinforcement — `load_index ≥ p ∧ reinforcement_index ≤ q`
5. Old + load-bearing + untouched — `neglect_index ≥ p ∧ load_index ≥ q`

Threshold defaults (config): `p = 0.90`, `q = 0.10` (i.e. top-decile on the `≥` side, bottom-decile on the `≤` side). These are the same cutoffs C3 will start from for the corresponding conjunctive features; pinning them here means the report and the eventual skeleton agree by default.

Sections 4 and 5 are exactly the toothpick and flooded-basement queries, surfaced without naming them. On the §1/§2 boundary: a report section is a **sorted query over continuous signals** whose predicate is printed above the list; it emits no feature name, no archetype, and no grade, and it is not read by C3. That is what "no metric→feature mapping" means here — the substrate may *sort by a conjunction*, it may not *name the result*. The tribunal (contradiction C3) read §2 and §9 as in tension; this sentence is the resolution: the mapping C3 owns is the naming, not the query. If those lists do not make you wince in recognition on a repo you know, the signals are wrong — and you have learned it with zero render code written. (Recognition here is a smoke test for the developer, not the `asserted` grounding; that is `validation-spec.md` §2.4.)

## 10. Validation

The substrate claims only "deterministic structural signals derived from repo history and static topology" — never "architectural truth." **The full protocol now lives in `validation-spec.md`** (spun out so the gate is auditable on its own terms). Summary of the contract that spec defines:

- **Primary — temporal holdout (falsifiable).** Split the timeline (80% of commits training / 20% holdout), compute indices on the training window only, label files by whether they received a `fix`-type commit in the holdout, and test whether `bug_pressure_index` and `change_pressure_index` rank-predict the labels against recency/busyness baselines (precision@k, ROC-AUC, PR-AUC). Only those two indices make a future-predictive claim and so only they are falsifiable this way; the other four are present-tense descriptions, confirmed on a different basis — a stability budget and a cross-modal check (`asserted`, `validation-spec.md` §2.4) — a different kind of grounding, and the weaker one for the purpose of what a downstream feature may claim.
- **The pinned weights (§6.2.1) are tuned against this loop**, held-out, not in-sample.
- **The mandate stands: write down where the indices lie.** A failing index is a real finding, not a bug — it ships `validation_status: "unvalidated"` and, per the anti-horoscope gate (`validation-spec.md` §5), may not feed a named feature in C3 unless explicitly marked decorative. Build-order step 10 (§11) ends in that written report.

## 11. Build order (weekend)

1. Finalize the v0.2 schema shape.
2. File inventory + stable tree hashing (the seed). **This inventory is the node set** (§5 node-set invariant).
3. Git history metrics via pydriller (rename-following on). **Intersect with step 2**: `history_miner` accumulates a `FileHistory` for every path ever seen, including files deleted before HEAD; the assembler keys nodes off the step-2 HEAD inventory and **drops any `FileHistory` whose canonical path is absent at HEAD**. Keying nodes off `history_miner.files` directly would emit phantom nodes (no `size_loc`/`fan_in`) and inflate the percentile population.
4. JS/TS import edges (`DependencyExtractor` impl).
5. Percentiles, with the N-floor and tie rule (§6.1).
6. The 5–6 indices, weights from config (§6.2).
7. Emit `substrate.json`.
8. Emit the deterministic markdown report (§9).
9. Run against Registry + mcp-secure-server.
10. Run the temporal-holdout validation and **write down where it lies** — those lies are the input to the C3 spec.

## 12. Open questions

1. **Node granularity.** File primary (proposed), directory as roll-up. Revisit if file-level is too noisy on large repos.
2. **Dependency language priority.** JS/TS first (assumed). Flip to Python on request.
3. **Initial index weights.** *Resolved* — pinned in §6.2.1 as explicit placeholders; the holdout (`validation-spec.md`) is the tuner for the two predictive indices.
4. **`N_min` default.** *Resolved (confirm in practice)* — 30. Below it, percentiles and indices are `null` and validation is `untested`; revisit only if the smallest repo of interest is smaller.
5. **Zero-spike handling.** *Resolved* — ship the `_nonzero` variant in v0 for `fan_in`, `fix_count`, `revert_count` (§6.1); `load_index`/`bug_pressure_index` consume it.
6. **Percentile population.** *Resolved* — exclude `is_test` files from the reference population (`exclude_tests_from_population: true`); test files are still measured, just not part of the distribution they would otherwise skew.
7. **Vendored / generated / monorepo.** Default exclude set, and whether monorepos need per-package sub-extraction.
8. **Extractor fidelity (mis-resolution).** `graph_resolution_rate` (§6.3) catches *non*-resolution but not confident *mis*-resolution (an import resolved to the wrong in-repo file via path-alias / re-export). How is the extractor's mapping spot-validated, and on which repos, before `load_index` rankings are trusted? Carry until the JS/TS extractor is built and run against alias-heavy code.
9. **Project name.** Still TBD — `repo-substrate` is a working name for the standalone product.
10. **Orphan nodes.** *Resolved (2026-09-04)* — defect signal, emitted with `history_missing: true`, excluded from the population, counted in `summary.orphan_nodes` (§5).
11. **Cross-modal counterparts.** `cochange_degree` and `blame_age_median` are Tier 1 as of D-004 so the `asserted` bar can run. Whether their defaults (`cochange_min = 2`, `cochange_max_files = 30`, blame without `-M -C`) are right is answered by the first validation run; each is a config diff.
12. **Dependency extractor backend.** *Resolved (D-006)* — `dependency-cruiser`, pinned, behind the `DependencyExtractor` protocol.
