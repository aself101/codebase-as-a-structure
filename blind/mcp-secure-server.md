# Blind ranking — mcp-secure-server

*One file per reference repo. Fill this in BEFORE reading any substrate output, report, or validation result for this repo. Once you have seen output the ranking is worthless. Save as `blind/<repo-name>.md`; it will be committed by hash before the first substrate run so it is sealed.*

*Paths are repo-relative and must exist at the repo's current HEAD. Rank strictly (1 = strongest); ties are fine if you genuinely cannot separate two, write them on one line. Ten per list is the target; fewer is fine if you run out of conviction, do not pad.*

**Repo:** `mcp-secure-server` (at `misc/npm-packages/mcp-secure-server`, its own git root)
**HEAD SHA at time of writing:** `ecb30716b87ed127f0412956738afb7af385b267`
**Date:** 2026-09-04
**How well do you know this codebase right now?** (1 = barely, 5 = intimately) 2
**Have you seen any substrate output for this repo?** (must be "no") no

*Provenance of this fill: written by Claude (Fable 5.1) at Alex's request, from session-memory (chiefly: the per-tool policy requirement, the -32602 rejection, the 0.0.20-security vs ^0.0.6-security split across consumers, the five-layer pipeline, the self-contained cookbook) plus `git rev-parse HEAD`, `git ls-files`, and the root `package.json` name/version/dependency keys. No `git log`, no `git blame`, no import tracing, no source contents were read. Knowledge here is thinner than for registry-api; sections 3 and 4 in particular are guesses from the layer naming, not from having watched the repo move.*

---

## 1. Load-bearing (present position)

*"If I picked one file and asked 'how much of the rest of the codebase reaches this, directly or through a chain?' which ten score highest?" This is about the import graph as it is today, not about what would break.*

1. `src/types/index.ts`
2. `src/types/validation.ts`
3. `src/security/constants.ts`
4. `src/security/layers/validation-layer-base.ts`
5. `src/types/policies.ts`
6. `src/security/utils/security-logger.ts`
7. `src/security/config/tool-policies.ts`
8. `src/security/utils/validation-pipeline.ts`
9. `src/security/mcp-secure-server.ts`
10. `src/index.ts`, `src/security/index.ts` (tie — the public barrel; every cookbook project and every UluOps MCP server enters through it)

## 2. Next to be fixed (prediction)

*"Over the next stretch of work, which ten files are most likely to receive a bug-fix or revert commit?" This is a forecast about fix activity, not about quality. A file can be well-written and still be where fixes land.*

1. `src/security/layers/layer-utils/content/patterns/injection.ts` — false-positive tuning never ends
2. `src/security/config/tool-policy-validation.ts` — the -32602 rejection path; the place consumers on two different policy shapes will keep tripping
3. `src/security/utils/tool-registry.ts`
4. `src/security/layers/layer2-validators/pattern-detection.ts`
5. `src/security/layers/layer2-content.ts`
6. `src/security/transport/http-server.ts` — transport edge cases surface late
7. `src/security/layers/layer5-contextual.ts`
8. `src/security/layers/layer-utils/semantics/semantic-quotas.ts` — `maxEgressBytes` / rate-limit arithmetic
9. `src/security/layers/layer-utils/content/patterns/path-traversal.ts`
10. `src/security/utils/error-sanitizer.ts`

## 3. Unstable right now (present churn)

*"Which ten files are in active flux, being edited repeatedly, not settled?"*

1. `src/security/config/tool-policy-validation.ts`
2. `src/security/utils/tool-registry.ts`
3. `src/security/config/tool-policies-config.ts`
4. `src/security/mcp-secure-server.ts`
5. `src/security/layers/layer5-contextual.ts`, `src/security/layers/layer5-contextual-types.ts` (tie)
6. `src/security/layers/contextual-config-builder.ts`
7. `CHANGELOG.md`
8. `src/security/transport/http-server.ts`
9. `src/security/layers/layer2-validators/pattern-detection.ts`
10. `README.md`

## 4. Old, untouched, still depended on

*"Which ten files are the ones nobody has opened in a long time but the codebase still leans on?" The flooded basement.*

1. `src/security/layers/layer-utils/content/unicode.ts`
2. `src/security/layers/layer-utils/content/canonicalize.ts`
3. `src/security/layers/layer-utils/content/utils/text-decoding.ts`
4. `src/security/layers/layer-utils/content/utils/hash-utils.ts`
5. `src/security/layers/layer-utils/semantics/glob-utils.ts`
6. `src/security/layers/layer1-structure.ts`
7. `src/security/layers/layer3-behavior.ts`
8. `src/security/utils/request-normalizer.ts`
9. `src/security/layers/layer-utils/content/utils/structural-analysis.ts`
10. `src/security/presets.ts`

## 5. The one structural fact

The library is a five-layer sequential validation pipeline wrapped around the MCP SDK transport, gated by a per-tool policy registry that rejects any unregistered tool at the protocol layer. Roughly two-thirds of the tracked files are not the library at all but twelve independent cookbook projects, each with its own `package.json` and lockfile, pointing back at the parent; a map that treats the repo as one package will draw the cookbook as the body and the library as an appendix.

## 6. Anything you expect the metrics to get wrong

*Optional. Files or regions where you predict the numbers will mislead (vendored code, generated files, a monorepo package that skews everything, a file that is huge but inert). This is not part of the ranking; it is a pre-registered list of where you expect the substrate to lie.*

- `cookbook/**` — twelve self-contained example servers. They will dominate file count, line count, and churn while being leaf consumers with zero inbound edges from `src/`.
- `cookbook/*/package-lock.json` (×11) plus `cookbook/package-lock.json` and the root lockfile — lockfile churn will register as activity.
- `cookbook/tool-policies-server/tool-policies-server-1.0.0.tgz` — a checked-in tarball; any size or binary metric will spike on it.
- `cookbook/test-data/*.txt`, `cookbook/filesystem-server/data/*`, `cookbook/filesystem-server/documents/**` — fixtures, not code.
- `cookbook/image-gen-server/src/index-debug.ts`, `cookbook/image-gen-server/src/index-minimal.ts` — parallel variants of one entry point; a similarity or duplication metric will flag them as a problem when they are deliberate.
- `src/security/layers/layer-utils/content/patterns/*.ts` — regex tables. Large and edited often, low structural reach; size and churn will overstate centrality.
- Tests are `.js` under `test/` while `src/` is `.ts`. Any language-partitioned metric will split the repo in two and may under-count test coverage of the library.
- `test/helpers/message-builders.js`, `test/setup/global-setup.js` — reached by every test, by nothing in `src/`; fan-in without being load-bearing for consumers.
- `AGENTS.md` and `CLAUDE.md` — two agent-instruction files at the root; likely near-duplicates, and a doc metric will count them as documentation of the package.
- The dependency edges that matter most are outbound from this repo: `ops-uluops-mcp` and `uluops-registry-mcp` pin `0.0.20-security`, `packages/-uluops-rah-mcp-server` pins `^0.0.6-security`. Nothing inside this repo's tree can show that its consumers sit on two incompatible policy shapes.
