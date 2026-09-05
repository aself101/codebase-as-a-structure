# Blind ranking — uluops-registry-api

*One file per reference repo. Fill this in BEFORE reading any substrate output, report, or validation result for this repo. Once you have seen output the ranking is worthless. Save as `blind/<repo-name>.md`; it will be committed by hash before the first substrate run so it is sealed.*

*Paths are repo-relative and must exist at the repo's current HEAD. Rank strictly (1 = strongest); ties are fine if you genuinely cannot separate two, write them on one line. Ten per list is the target; fewer is fine if you run out of conviction, do not pad.*

**Repo:** `uluops-registry-api`
**HEAD SHA at time of writing:** `f7414cc7bbec62ba80068af4b045667064d1d59e`
**Date:** 2026-09-04
**How well do you know this codebase right now?** (1 = barely, 5 = intimately) 3
**Have you seen any substrate output for this repo?** (must be "no") no

*Provenance of this fill: written by Claude (Fable 5.1) at Alex's request, from session-memory of prior work on this repo plus `git rev-parse HEAD` and `git ls-files` only. No `git log`, no `git blame`, no import tracing, no file contents were read. The listing was used solely to make paths valid. Treat the rankings as a model's priors, not the maintainer's.*

---

## 1. Load-bearing (present position)

*"If I picked one file and asked 'how much of the rest of the codebase reaches this, directly or through a chain?' which ten score highest?" This is about the import graph as it is today, not about what would break.*

1. `src/utils/errors.ts`
2. `src/utils/logger.ts`
3. `src/db/connection.ts`
4. `src/schemas/enums.ts`
5. `src/db/repository/base-repository.ts`
6. `src/config/index.ts`
7. `src/schemas/definition/types.ts`
8. `src/db/repository/definition-repository.ts`
9. `src/services/definition/index.ts`
10. `src/utils/uuid.ts`, `src/utils/index.ts` (tie — the barrel inflates whatever it re-exports; uuid is the binary-swap helper every repository needs)

## 2. Next to be fixed (prediction)

*"Over the next stretch of work, which ten files are most likely to receive a bug-fix or revert commit?" This is a forecast about fix activity, not about quality. A file can be well-written and still be where fixes land.*

1. `src/services/safety/signals.ts` — regex tuning and false-positive suppression is a permanent fix stream
2. `src/services/safety/definition-scanner.ts` — every `ANALYZER_VERSION` bump lands here and drags a backfill behind it
3. `src/services/translation/translator.ts` — factory 0.69.0 corpus retranslate is pending; render-gap fixes surface here
4. `src/services/definition/lifecycle.ts` — publish flow is where safety, translation, and lineage hooks all meet
5. `src/services/safety/deep-analysis-worker.ts` — ADR-013 activation hardening is fresh and will need follow-up
6. `src/middleware/auth.ts` — platform security audit run 21 has open items; registry-api is still on platform 1.27.0
7. `package.json` — pin bumps (factory, sdk-core minor-lock, tier-gate minor-lock) are fixes in this repo's dialect
8. `src/services/analytics/health.ts` — the `regressionRate` semantics change is the precedent; health factors keep moving
9. `src/controllers/definition-controller.ts` — largest controller, the batch-mechanical-fix target
10. `src/services/safety/publish-gate.ts` — calibration-gate threshold pressure

## 3. Unstable right now (present churn)

*"Which ten files are in active flux, being edited repeatedly, not settled?"*

1. `package.json`, `package-lock.json` (tie — the pin sweep)
2. `src/services/translation/translator.ts`
3. `scripts/retranslate-corpus.ts`
4. `src/services/safety/deep-analysis-worker.ts`
5. `src/services/safety/deep-analysis-queue.ts`
6. `src/controllers/deep-analysis-controller.ts`
7. `src/routes/v1/deep-analysis.ts`
8. `CHANGELOG.md`
9. `src/services/definition/lifecycle.ts`
10. `src/middleware/auth.ts`

## 4. Old, untouched, still depended on

*"Which ten files are the ones nobody has opened in a long time but the codebase still leans on?" The flooded basement.*

1. `src/utils/async-handler.ts` — every route is wrapped in it
2. `src/utils/hash.ts` — content identity; only the column-size migration ever touched its neighbourhood
3. `src/utils/cycle-detection.ts` — reference validation depends on it, nobody revisits it
4. `src/utils/fork-identity.ts`
5. `src/utils/singleton.ts`
6. `src/utils/retry.ts`, `src/utils/circuit-breaker.ts` (tie)
7. `src/middleware/correlation-id.ts`, `src/middleware/request-logger.ts` (tie)
8. `src/db/migrations/001_create_definitions.ts`, `src/db/migrations/002_create_definition_versions.ts` (tie — frozen by design, but they ARE the schema every query assumes)
9. `src/schemas/cdl/types.ts`, `src/schemas/wdl/types.ts` (tie — the non-ADL language schema copies, likely stale relative to the factory)
10. `src/db/seeds/utils.ts`

## 5. The one structural fact

The repo does not own its own substance: rendered `runtime_md` is stored at publish time from `@uluops/definition-factory`, so the load-bearing thing is an npm pin plus a stored column, not anything in `src/`. A map that draws only the in-repo import graph will show a well-shaped Express service and miss that its output is frozen by an external version number until someone retranslates the corpus.

## 6. Anything you expect the metrics to get wrong

*Optional. Files or regions where you predict the numbers will mislead (vendored code, generated files, a monorepo package that skews everything, a file that is huge but inert). This is not part of the ranking; it is a pre-registered list of where you expect the substrate to lie.*

- `src/db/migrations/*` — ~60 files, imported by nothing in `src/`, append-only churn. An import-graph metric scores them zero; a churn metric scores the directory high; both are wrong about what they mean.
- `scripts/backfill-*.ts` — one-shot scripts that are dead the day after they run but stay tracked; churn without ongoing dependence.
- `package-lock.json` — huge, churns on every pin bump, carries no structure.
- `docs/adr/*.md`, `plans/*.md` — zero imports, but they are the decision strata; a map that ignores prose misses the why.
- `src/schemas/CLAUDE.md`, `src/schemas/adl/CLAUDE.md` — agent instructions living inside the source tree, will be counted as documentation-of-code when they are instructions-to-a-tool.
- `src/services/safety/signals.ts` — a data table of regexes; large and frequently edited, low structural reach. Size and churn will overstate its centrality.
- Barrels (`src/utils/index.ts`, `src/services/index.ts`, `src/db/repository/index.ts`, `src/schemas/index.ts`, `src/middleware/index.ts`, `src/controllers/index.ts`) — inflate fan-in for whatever they re-export and will crowd the load-bearing list.
- `src/terminal/*` — startup banner; touched in cosmetic bursts, reached only from `src/index.ts`. Will look more central than it is.
- The dual-database architecture (ADR-003): the auth DB is shared with the platform and not modelled in this repo's migrations at all. Nothing in the file tree signals that half the schema lives elsewhere.
