# Truthful Extractor — v0 Specification

> ## ⚠️ SUPERSEDED
> **This document (v0.1) is superseded by `repo-substrate-spec.md` (v0.2).** It is retained for history only — do not implement from it. The successor moved the measure/interpret boundary one notch (continuous derived signals — percentiles, composite indices — are now in scope; named features remain out), pinned the index weights, added the `_nonzero` percentile and graph-absent handling, and spun the validation protocol out to `validation-spec.md`. The system spec's Component 1 points at the successor. Where this v0.1 text and the successor disagree, **the successor wins** in all cases.

*Component 1 of the codebase-as-structure project (working name TBD). This component measures; it does not interpret. Its sole job is to turn one git repository at one commit into a reproducible, structured description of its measurable properties — the substrate every later layer reads from.*

---

## 1. Governing principle

The extractor emits **substrate, not diagnosis**. Every field is a fact derived by a pure function from git history or static source. No field names a building feature, assigns an archetype, or scores quality. Interpretation lives strictly downstream. If a value in the output could only have come from a judgment call, it does not belong here.

This is the layer that makes the whole pipeline *regressable*: two runs on the same commit produce the same numbers, so any change in a later render is attributable to either a code change or a deliberate seed/lens change — never to extractor nondeterminism.

## 2. Scope

In scope for v0:
- One local git repository, one revision (default `HEAD`).
- Per-node metrics (node = file; directories are aggregation views over their files).
- A dependency edge set for **one** language family (see Open Question 2).
- A commit timeline with deterministic commit-type classification.
- Repo-level aggregate features (raw inputs for the *separate* archetype classifier — component 2).
- A single JSON document as output.

Explicitly **out** of scope for v0:
- No LLM anywhere in this component.
- No archetype label, no quality score, no building/structural vocabulary.
- No rendering, no metric→feature mapping (that is the next spec).
- No cross-repo, no remote fetch, no multi-language dependency resolution.

## 3. Determinism contract

- The output is a pure function of `(repo content at commit SHA, extractor_version, config)`.
- The **seed** is the content hash of the resolved tree (recorded in output). Later stochastic layers consume this seed.
- Re-running on the same SHA with the same `extractor_version` and config yields byte-identical output **except** `extracted_at`, which is excluded from the content hash.
- All ordering is stable: nodes sorted by path, edges by `(from, to)`, timeline by `(timestamp, sha)`.
- Floating-point aggregates are rounded to a fixed precision (proposed: 4 dp) to keep hashes stable across platforms.

## 4. Output schema (v0.1)

```json
{
  "schema_version": "0.1",
  "extractor_version": "0.1.0",
  "extracted_at": "<ISO8601, excluded from seed>",
  "seed": "<sha256 of resolved tree>",
  "repo": {
    "name": "string",
    "head_sha": "string",
    "branch": "string",
    "root_commit_sha": "string",
    "config_fingerprint": "<sha256 of effective config>"
  },
  "summary": { "<repo-level aggregates, see 5.3>": 0 },
  "languages": { "<lang>": { "files": 0, "loc": 0 } },
  "nodes": [
    {
      "id": "src/registry/health.ts",
      "kind": "file",
      "lang": "ts",
      "metrics": { "<per-node metrics, see 5.1>": 0 }
    }
  ],
  "edges": [
    { "from": "src/a.ts", "to": "src/b.ts", "kind": "import" }
  ],
  "timeline": [
    {
      "sha": "string",
      "ts": "ISO8601",
      "author": "string",
      "subject": "string",
      "type": "feat|fix|refactor|docs|chore|test|revert|merge|other",
      "matched_rule": "string",
      "nodes_touched": ["src/a.ts"],
      "added": 0,
      "deleted": 0
    }
  ]
}
```

Directory-level aggregates are not stored as nodes in v0; they are computed on demand by rolling per-file metrics up the path tree. This gives level-of-detail (file → dir → repo) for free without duplicating data.

## 5. Metric catalog

Each metric lists its derivation and the **candidate structural signal(s)** it might feed. The candidate column is documentation of intent, *not* a mapping — it exists so the next component (deterministic metric→feature options) has a starting map. Nothing here commits to a rendering.

### 5.1 Per-node, Tier 1 (required for v0)

| Metric | Derivation | Candidate structural signal |
|---|---|---|
| `size_loc` | Non-blank line count | Footprint / room volume |
| `age_days` | Days since first commit to touch the file (rename-followed) | Material & era (old stone vs. new glass) |
| `last_touched_days` | Days since most recent commit to touch it | Occupancy / lighting (lit vs. dark) |
| `commit_count` | # commits touching the file over history | Traffic / wear |
| `churn_lines` | Σ(added + deleted) across history | Instability / structural fatigue |
| `fix_count` | # touching commits whose `type == fix` or `revert` | Cracks / stress concentration |
| `author_count` | Distinct authors who touched it | Provenance; low count = single-builder wing |
| `fan_in` | Inbound import edges | Load-bearing-ness (foundation candidates) |
| `fan_out` | Outbound import edges | Dependence on others / propping |
| `is_test` | Path/name matches test convention | (excluded from non-test aggregates) |
| `has_sibling_test` | A test file maps to this module | Scaffolding / reinforcement present |
| `introduced_idx` | Index of introducing commit in the timeline | Build phase: original core vs. later annex |

### 5.2 Per-node, Tier 2 (defer unless cheap)

| Metric | Derivation | Candidate structural signal |
|---|---|---|
| `complexity` | Cyclomatic (per-language parser) | Internal intricacy |
| `public_surface_ratio` | Exported vs. internal symbols | "Fortress with no door" |
| `comment_density` | Comment lines / LOC | Signage / blueprint adherence |
| `cochange_degree` | # files that frequently change in the same commit | Hidden corridors / coupling not visible in imports |

`complexity` and `public_surface_ratio` are the two most valuable Tier-2 metrics but both require real parsing; keep them out of v0 and use a cheap language-agnostic proxy for intricacy if needed (max nesting depth or `size_loc`).

### 5.3 Repo-level aggregates, Tier 1 (raw features for the classifier)

`node_count`, `total_loc`, `repo_age_days`, `commit_count`, `commit_cadence` (commits-per-month series), `author_count`, `authorship_gini` (concentration), `test_loc_ratio`, `language_breakdown`, `dep_graph_density` (edges / possible edges).

These are emitted raw. v0 assigns **no archetype** — the cathedral-vs-Howl's-castle call is component 2's job and reads only from `summary`.

## 6. Commit-type classification

Deterministic rule cascade, first match wins, recorded in `matched_rule`:
1. Conventional-commit prefix (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `revert:`).
2. Merge detection (>1 parent → `merge`).
3. Subject regex fallback (e.g. `/\b(bug|hotfix|patch)\b/i` → `fix`).
4. Default → `other`.

No probabilistic classification in v0 — every commit type is traceable to a rule. (An LLM-as-reader pass can enrich this later, but stays optional and cached.)

## 7. Tooling

- **Language:** Python 3.11+.
- **History mining:** `pydriller` — purpose-built for per-commit modification mining, rename-following, and author/diff stats. Avoids hand-parsing `git log --numstat`.
- **Dependency extraction:** behind a `DependencyExtractor` protocol so language support is swappable. v0 ships one implementation (see Open Question 2). For JS/TS, shell out to `madge`/`dependency-cruiser` or parse imports with `tree-sitter`; for Python, `ast` + import resolution.
- **CLI:** `extract <repo_path> [--rev HEAD] [--config cfg.toml] -o out.json`.
- **Config:** exclude globs (vendored/generated/`node_modules`), test-path patterns, fix-subject regexes, rounding precision.

## 8. Validation plan ("see what it says")

Run against a known repo (proposed: UluOps Registry) and check that the substrate surfaces the warts *without* being told what a wart is:
1. Highest-`fan_in` nodes should be recognizable core modules.
2. The toothpick candidates — high `fan_in` ∧ high `fix_count` ∧ no `has_sibling_test` — should be files you already distrust.
3. Flooded-basement candidates — high `fan_in` ∧ high `age_days` ∧ high `last_touched_days` (load-bearing but untouched) — should match your gut.
4. `introduced_idx` distribution should reveal whether the repo was front-loaded (spec-first) or accreted (organic).

If these four eyeball checks fail, the metric set is wrong before any rendering question is even on the table. That is the cheapest possible place to find out.

## 9. Open questions (carry, do not resolve yet)

1. **Node granularity.** File as the primary node (proposed) vs. directory/package. File keeps it simple and rolls up cleanly; revisit if file-level is too noisy for large repos.
2. **Dependency language priority.** Which language's import graph ships first? `fan_in`/`fan_out` fidelity depends entirely on this. Assumption: JS/TS first (largest share of the stack). Flip to Python-first on request.
3. **Complexity proxy.** Cheap language-agnostic proxy now (nesting depth / LOC) vs. wait for real cyclomatic per-language. Affects whether "intricacy" is trustworthy in v0.
4. **Vendored / generated / monorepo packages.** Exclusion is config-driven, but the default exclude set needs deciding, and monorepos may need per-package sub-extraction.
5. **Rename following.** pydriller can follow renames so `age_days`/`churn` aren't reset by a move. This materially affects truthfulness (a 3-year-old file renamed last week should not read as new) and should be on by default — confirm.
