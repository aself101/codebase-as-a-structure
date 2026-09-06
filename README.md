# codebase-as-structure

*A single git repository rendered as a building you can read. The picture is diagnostic, not decorative: every visual feature is a function of a measured signal, and a feature may not render unless its signal has earned it.*

**Package:** `repo-substrate` (C1 + the validation gate). **Status (2026-09-04):** M1 complete (D-015). The substrate and the gate are built, reviewed by six lenses, hardened, and run: both predictive indices are `unvalidated` on the pre-registered test set; twenty-one descriptive signals are `asserted`. **M2 complete (2026-09-05, D-020):** C3 applies `rulesets/maintainability.toml` (+ `onboarding.toml` as an overlay) under the gate, the cutaway renders it in two geometries, `skeleton-diff` measures churn against a pinned budget (D-018), and no archetype is claimed (D-019); pictures and readings in `reports/2026-09-05-m2/`. **Phase 1 (2026-09-05, D-021–D-023):** `substrate timelapse` replays a repository at trunk checkpoints under HEAD's gate and draws a change sheet per transition; the time-lapse found an integer-day artefact in the age signals (D-022, substrate 0.3.0). **M3 (2026-09-06, D-027–D-028):** `substrate brief` writes the architect's brief with a model and holds it with a deterministic register lint; four reference briefs pass. **Since (D-029–D-032):** package facts and a declared-entry flag in the substrate (0.4.x), the budget pinned at K = 25 for signals and skeletons alike, `neglect_index` out of the ruleset, and three review cycles (tracker runs 12–14) whose fixes are named in the log. **D-033:** the signal-level stability budget re-ranks over the untouched population (own signals read 0.000 by construction — the class check), the tail operand follows the signal's ripple class, eps/delta sit where they fire (0.01 / 0.05), and `asserted` needs a majority of the reference set.

## What is new here, exactly

The building metaphor is not new. **CodeCity** (Wettel & Lanza, 2007) drew classes as buildings sized by metrics. **CodeScene** (Tornhill) visualizes churn × complexity hotspots from version history. **Nagappan & Zimmermann** (2005 onward) and Google's 2011 bug-prediction work established that churn and fix history predict where defects land. This project stands on all three and claims none of them.

The claim is narrower: a **temporal-holdout validation gate between the metric and the picture**. Each signal the substrate emits carries a `validation_status`. The two predictive indices earn `validated` only by beating recency and busyness baselines on a held-out window of commits, on repos they were not tuned on. Descriptive signals earn `asserted` only by a stability budget plus corroboration from an independent instrument or a different modality. A named structural feature — a foundation, a toothpick wing, a flooded basement — may rest only on signals that passed. Anything else renders as `decorative`, counted, and excluded from every diagnostic claim.

That claim is defensible only insofar as the gate can fail and the report shows it failing. So far it has. Under the pre-registered protocol (tune on two repos, verdict from the other two, margins untouched), `bug_pressure_index` failed both test repos and `change_pressure_index` passed one of two; the tuned bug-pressure weights assign zero to fix history, which is the finding. The report says by how much against which baseline. The second import instrument caught the primary one dropping `import type` edges on typeorm. Those are the results this README is allowed to cite, and no more.

## Layout

| Path | What |
|---|---|
| `codebase-as-structure-system-spec.md` | Parent spec: thesis, six components, cross-cutting contracts (determinism, provenance, the anti-horoscope gate) |
| `repo-substrate-spec.md` | C1: the substrate — per-file metrics, percentiles, composite indices, dependency edges, timeline |
| `validation-spec.md` | The gate: temporal holdout, the asserted bar (stability + grounding classes G1–G4), `validation.json` |
| `structural-mapper-spec.md` | C3: the ruleset that names features, under the gate; overlays, geometries, the skeleton diff and its budget |
| `time-lapse-spec.md` | Phase 1: a skeleton per trunk checkpoint under HEAD's gate, the budget between frames, a scrubber page |
| `architect-brief-spec.md` | M3 (C5): the surveyor's brief over a skeleton, descriptive register only, held by a deterministic register lint |
| `DECISIONS.md` | Append-only decision log, D-001 onward. Why the artifact is shaped this way |
| `checklists/` | Testable contracts per spec, each pointing at the test that covers it |
| `blind/` | Sealed recognition rankings per reference repo (n = 1, non-gating, provenance stated in-file) |
| `src/repo_substrate/` | The package: `substrate extract \| map \| render` and `substrate-validate run \| tune` |
| `rulesets/` | C3 rulesets (TOML): maintainability v0.1.0 (base) and onboarding v0.1.0 (overlay) |
| `tests/` | 107 tests incl. a scripted synthetic repository, verdict-path tests, and integrity checks |
| `docs/` | Review history: the June tribunal, the archived prototype, notes |

## Running it

```
uv sync && npm install
uv run substrate extract <repo> -o out/x.substrate.json --report out/x.report.md
uv run substrate-validate tune --repo <tuning-repo> --repo <tuning-repo> --out config/
uv run substrate-validate run --test-repo <a> --test-repo <b> --tuning-repo <c> --tuning-repo <d> \
    --config config/tuned.toml --out out/validation
uv run substrate map out/x.substrate.json --validation out/validation/validation.json \
    --ruleset rulesets/maintainability.toml --overlay rulesets/onboarding.toml \
    --geometry layer -o out/x.skeleton.json          # geometry: age | layer
uv run substrate render out/x.skeleton.json out/x.substrate.json -o out/x.cutaway.svg --html out/x.cutaway.html
uv run substrate skeleton-diff out/x.before.skeleton.json out/x.skeleton.json --renames out/x.substrate.json   # budget verdict over untouched nodes
uv run substrate timelapse <repo> --validation out/validation/validation.json --ruleset rulesets/maintainability.toml \
    --overlay rulesets/onboarding.toml --geometry age --frames 12 --config config/tuned.toml -o out/timelapse/x
uv run substrate brief out/x.skeleton.json out/x.substrate.json -o out/x.brief.md   # M3: model + register lint; --draft lints without a model
uv run pytest -q
```

The substrate report is stamped **UNGATED**: it consults no `validation.json` and makes no diagnosis. The holdout report is where the gate speaks.

## How work is done here

Decisions go in `DECISIONS.md` before or alongside the work they govern. Every review run is saved to the UluOps tracker project `codebase-as-structure`. A decision that closes an exploit names the code that enforces it, in the decision itself; a decision that cannot name code has not closed anything.
