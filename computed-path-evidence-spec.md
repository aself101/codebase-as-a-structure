# Computed-path load evidence — proposed D-081

Status: draft for review, **not implemented**. This adds a source-evidence record, not
an import edge, runtime trace, reinforcement signal, dead-code verdict, or new mapping
population. The first acceptance case is ESLint's message loader.

## 1. The pending question and current evidence

D-072/D-073 deferred a counted record for `messages/*.js` rather than explaining every
zero importer by a runtime-load caveat. Tracker run 59
(`e657ecca-4d73-4399-a756-4a63158884c9`) leaves issue
`5095c7e7-1523-4df2-a7e0-f4a68cdf03f2` deferred. The older runtime/DI-coupling
issue `4c0eddae-95a1-487a-a0b6-5846a701764a` is also deferred; this proposal does
not claim to close it. The alias-loader failure (D-065), self-package resolution
(D-066), example-role choice (D-078), and PageRank-cycle disclosure (D-079) are
already resolved and are not reopened here.

At the local reference checkout and attested gate revision
`3f20a57c6293371b6193d3fb6746c2b7b2ac2689` (clean tracked tree):

- `bin/eslint.js:107`, in `getErrorMessage`, calls
  ``require(`../messages/${error.messageTemplate}.js`)`` after checking that the
  property is a string, inside a try/catch. It is conditional; errors fall back to
  the stack/message. Neither execution nor successful loading was observed.
- The pinned inventory contains **18** direct `messages/*.js` files: **17** have
  static `fan_in == 0`; `messages/shared.js` has two static importers, from
  `invalid-rule-options.js` and `invalid-rule-severity.js`. It exports a helper
  object, not the template function the CLI later invokes. It still matches the
  lexical envelope and must not be silently removed from the candidate set.
- The current diagnostic flooded-basement set contains **11** of these files:
  **10** without a static importer, plus `shared.js`. These are snapshot-specific
  descriptive intersections, not newly computed features or dead-code claims.
- Literal property assignments include `file-not-found` (eslint-helpers.js:88),
  `config-plugin-missing` (config.js:103), and several other identifiers. They are
  examples of producers, not a closed dataflow proof: third-party errors can
  supply a string, and the call site does not forbid separators or traversal.

Other current runtime-loader cases are `import(optionsURL)`
(`lib/eslint/eslint-helpers.js:990`), `import(pathToFileURL(formatterPath))`
(`lib/eslint/eslint.js:1273`), `import(fileURL.href)`
(`lib/config/config-loader.js:185`), and `jiti.import(fileURL.href)` at line 169.
The first three have opaque computed targets under this proposal; the custom jiti
method is outside native-call recognition. No target set is guessed for them.

## 2. Narrow method

Use the already pinned TypeScript parser (5.9.2) to read source bytes at the analyzed
git revision. Do not execute modules, project build steps, imports, or tests to collect
this evidence. Comments and string literals containing call-shaped text are not calls.
For direct `require(...)`, check lexical scopes for a shadowing binding; record a
shadowed/uncertain site as excluded/unknown, not a native loader. No lexical shadow
found is a syntactic observation, not proof against monkey-patching at runtime. Native
`import(...)` is recognized as syntax. Custom member loaders are out of initial scope.

Initial candidate rule: a relative template-literal argument with one hole, a fixed
prefix ending in `/`, and a fixed `.js` suffix. Resolve the fixed directory lexically
from the source file's directory using POSIX repository paths. Enumerate direct child
`.js` paths in the **pinned substrate inventory**. The suffix denotes that exact source
filename; do not map built JS back to TS, resolve packages/aliases, follow filesystem
symlinks, or infer implicit extensions/index files in this rule. Existing static
resolution owns those cases. A literal argument remains the existing static backend's
responsibility and must not acquire a duplicate candidate relation.

The first rule's candidate set is a **direct-file envelope**, not the set of all possible
runtime targets. An unrestricted hole may contain subdirectories or traversal and may
name another file, a missing file, or a module that throws. Report runtime target
coverage as unknown even when the supported syntax scan is complete. Do not turn
known producer strings into resolved edges without a separate dataflow design.

Bare expressions, multiple holes, suffixless paths, unsupported languages/shapes,
parse errors, ambiguous/shadowed bindings, oversized files and prefixes escaping the
repository produce explicit coverage/refusal records. They are never an empty proof
of no runtime coupling. Proposed parse limit: 2 MiB per file, in the method fingerprint.
No candidate-name cap is proposed; the inventory is finite and the record retains its
complete direct-child set in sorted order.

## 3. Deterministic side artifact

Proposed output: `computed-load-evidence.json`, separate from `substrate.json`. Bind
it to the substrate's revision, seed, config fingerprint and SHA-256 of its exact bytes;
refuse a mismatched attachment. Older attested substrates remain immutable. Record an
independent evidence-method fingerprint over parser version, recognizer/rule versions,
path semantics, scope policy and resource limits. No metric/config fingerprint changes
in this evidence-only phase. A timestamp, if present, is excluded from content hashing.

Fields:

- `schema_version`, `method_fingerprint`, `substrate_binding`, and deterministic
  `coverage` counts with file-level refused/unsupported reasons.
- Per site: source path, git blob OID, call span (`start_utf16`, `end_utf16`,
  one-based line and UTF-16 column), loader syntax, binding-check result, argument-source
  SHA-256, recognizer ID, cooked fixed literal segments, hole count and hole AST kind.
  No full expression/source text is emitted by default.
- Recognition/site status: the complete mutually exclusive taxonomy in §7.1;
  target relation is always `candidate_only` for
  an enumerated computed envelope. This is categorical evidence, not a probability
  or a numeric confidence score.
- Per candidate: inventory node ID, `is_test`, and declared `file_kind`; candidates
  are sorted and deduplicated within the site. They are not appended to `edges`.
- `candidate_scope = direct_inventory_children`,
  `runtime_target_coverage = unknown`, and
  `execution_observed = false`. These disclosures travel with any display/export.

Source order is path, then call offset; targets sort by exact repository path. Source
spans use the parser's UTF-16 units explicitly (not mislabeled UTF-8 byte offsets).
Hash raw source bytes separately; Unicode and CRLF fixtures must pin both concepts.
Repeated sites do not double-count a candidate file in a per-feature intersection.
No scalar count of records is a count of importers or executed loads.

## 4. Exclusions, graph and gate

The existing inventory's include/exclude conventions define the candidate universe;
non-inventoried or generated/build targets remain outside it and are disclosed as a
limit. Tests and example files that are inventory nodes may carry evidence. Role
exclusion from a profile does not erase graph nodes or evidence (D-078). For profile
counts, intersect candidate IDs with that exact skeleton's room/feature sets. Count
source/test/example categories disjointly where shown: tests first, examples outside
the test convention second; never repeat D-079's overlapping counts.

Import edges, fan-in/out, test fan-in, PageRank, indices, graph-quality denominators,
gate statuses, populations, feature membership and stability verdicts remain byte-for-
byte/value-for-value as they were without this side artifact. A candidate is neither
a resolved import nor an unresolved-import failure and enters neither counter.
There is no new asserted/validated signal in this phase. Promotion to graph edges or
reinforcement requires a separate reviewed contract, new extractor/fingerprint,
independent resolution validation and the normal gate re-run.

Permitted display: “10 of this row's files have no resolved static importer and match
a computed-load candidate envelope at bin/eslint.js:107; the call may not execute
and its target values are not established.” The displayed number must be recomputed
from the attached artifact and current skeleton, never copied from this spec. Forbidden:
“10 runtime-loaded files,” “reinforced by the CLI,” “not dead,” “safe to keep,” or a
causal explanation of their rank. No artifact means unknown, not zero. Partial scan
results may be shown only as observed candidates with their incomplete coverage; zero
never means no runtime loading.

## 5. Fixtures and acceptance checks

1. The pinned ESLint call yields the 18 direct inventory candidates, including
   shared.js; shows 17 static-fan-in-zero candidates and the present 10/11 row
   intersection when paired with the pinned skeleton. Opaque native imports are
   recorded without target guesses; jiti is stated out of scope.
2. Positive template fixture; comment/string decoys; shadowed require; literal
   static require; duplicate sites; empty candidate directory; missing target;
   multiple holes; basename/suffix mismatch; traversal/subdirectory-valued hole;
   prefix escaping root; excluded build/test/example files; parser failure and
   oversized source. These guard the candidate/actual-load distinction.
3. Unicode/CRLF span/hash fixture, deterministic ordering, repeated-run identical
   content, parser/rule fingerprint changes, and rejection of wrong revision,
   seed, configuration or substrate-byte attestation.
4. Assert zero changes to static edges, all existing metrics and graph quality,
   gate tables, both skeleton geometries and all eight D-080 stability operands.
5. Verify every displayed intersection/count from its site/candidate IDs; duplicate
   routes and overlapping file roles cannot inflate file counts. Missing/partial
   coverage cannot produce a claim of absence.

## 6. Review and decision boundary

This is a proposed record of source syntax and candidate namespaces. It is not a
solution to runtime reachability, dependency injection, event buses or dead-code
identification. Independent spec review must challenge the direct-file boundary,
require binding assumptions, confidence wording, count units, refusal/coverage states
and whether each promised invariant can be tested before implementation.

Implementation awaits a decision after this review. A future graph-promotion design
or a broader candidate/dataflow rule is a separate decision, not bundled here.

## 7. Independent review closure — operational policies

The independent source/spec review confirmed the pinned observations and candidate-only
boundaries, and required four contract repairs. The following policies are part of the
method fingerprint; acceptance fixtures must exercise each. No implementation is authorized
by recording this revision.

### 7.1 Source denominator and status taxonomy

The source universe is every pinned substrate node whose `lang` is `js` or `ts`,
including test/example nodes even when a mapping profile excludes their role. Read its
blob from the analyzed git revision, not the live worktree. Regular blob modes 100644
and 100755 may be analyzed. Symlinks/non-regular blobs remain in this denominator
with `refused/non_regular_blob`; no link is followed. Nodes in other languages are
`out_of_scope/unsupported_language`, outside the source denominator. Inventory
exclusions are inherited, not rescanned and then counted as missing.

Every source-universe file has exactly one outcome: `analyzed`, or `refused` with
`non_regular_blob`, `blob_unavailable`, `invalid_utf8`, `oversized_source`, or
`parse_error`. `source_files = analyzed_files + refused_files`; count files, not sites.
A parsed file with opaque sites is analyzed, not refused. Coverage is
`complete_for_supported_syntax` only if every source-universe file was analyzed;
otherwise `partial` (or `unavailable` if none could be analyzed). Even complete
syntax coverage leaves runtime target coverage unknown.

Count recognized syntax sites separately: direct identifier calls named `require`
and native `import(...)`. Every such site receives exactly one outcome:
`static_literal_delegated` (existing backend owns it), `supported_envelope`,
`opaque_target` (bare computed expression/URL-producing call),
`excluded_shadowed_binding`, `uncertain_binding`, or `unsupported_shape`.
Unsupported-shape reasons include `multiple_holes`, `unsupported_suffix`,
`nonrelative_prefix`, `prefix_escapes_repository`, and `invalid_cooked_segment`.
Custom member loaders are outside this site denominator. Syntax-site counts are not
counts of native loader executions, runtime dependencies, or candidate files.

### 7.2 Decoding, spans and hash preimages

Decode raw blob bytes as strict UTF-8. Refuse invalid bytes; do not replace them. Retain
a leading BOM as U+FEFF and retain CRLF; the parser treats the BOM as trivia, but
its code unit remains part of source-offset/column accounting. Resolve fixed template
segments from their **cooked values**, including JS escape processing. Escaped
`mess\u0061ges` and `\u002ejs` therefore select the same envelope as `messages`
and `.js`; their raw argument hashes differ. Invalid escapes/parse diagnostics refuse
the file. Refuse a cooked path segment containing an unpaired surrogate or a NUL;
do not repair it or apply host filesystem/case/Unicode normalization.

Both call and argument spans are half-open `[start_utf16, end_utf16)`, using the
parser's `getStart(sourceFile)` (excluding leading trivia) and `getEnd()`. The one-based
line/UTF-16 column identify the call start. `argument_source_sha256` hashes the raw
UTF-8 bytes of the argument expression only, including its delimiters, excluding
leading trivia and the surrounding call. Convert those UTF-16 endpoints to original
byte positions explicitly; never slice UTF-8 bytes using UTF-16 offsets. Source blob
OID and raw blob SHA-256 include BOM/CRLF unchanged.

Canonical method/content-hash JSON uses UTF-8, no insignificant whitespace, sorted
object keys by UTF-8 byte order, and standard required JSON string escapes without
ASCII-escaping other Unicode or normalizing it. Paths also sort by UTF-8 byte order,
then numeric call offset. Hash inputs contain only integers, strings, booleans, null,
arrays and objects; no floating/non-finite values. The method hash covers exactly
`method_config` (parser package/version, recognizer IDs/versions, source/binding/path
policies and limits). The content hash covers the complete artifact except
`content_hash` and optional `created_at`; method fingerprint and substrate binding
remain included. Pretty printing is outside both preimages.

### 7.3 Binding policy

For identifier `require`, inspect the whole containing scope chain before classifying
the site, regardless of declaration order. Source value bindings include parameters,
imports that introduce values, destructuring names, catch parameters, function/class
declarations, function-scoped `var`, and block/module `let`/`const`. Hoisting and
TDZ do not make a declaration invisible. Type-only TS declarations do not introduce
a runtime value; unsupported binding constructs are `uncertain_binding`. A found
source value binding named require is excluded by this rule, without claiming its
runtime value is necessarily different from the Node loader.

A containing `with` object environment, or a syntactically direct call named `eval`
in the containing function/program scope or an ancestor scope, makes resolution
uncertain. Inspect all of that scope, even later statements or conditional calls;
this conservative rule does not execute or analyze eval strings. An eval in an
unrelated sibling function does not taint another scope. Report `with_environment`
or `direct_eval_environment`; distinguish these from a found binding. The assumed
ambient CommonJS require is disclosed as an assumption, not a runtime proof.

Fixtures must cover parameters, imports, nested/destructured/catch bindings,
function/var hoisting, declarations after the call, TDZ, type-only declarations,
with/direct eval, and sibling-scope eval. Uncertain sites have no inferred candidates.

### 7.4 Display provenance

Before any displayed feature intersection, require the skeleton's repository revision,
`substrate_seed`, and `substrate_config_fingerprint` to match the artifact binding,
and require the bound substrate's byte SHA-256 to match the attached substrate.
Reject a mismatch as unavailable evidence; never compute a plausible path intersection
anyway. Record the particular skeleton hash/profile and evidence content hash with
derived display counts, so counts cannot be reused across another profile/population.
Add wrong-snapshot, wrong-seed/fingerprint and stale-profile display fixtures.

These revisions define reproducibility and refusal, not a broader candidate rule,
closed runtime target set, or graph promotion.

**Independent recheck (2026-10-13).** The fresh reviewer confirmed all four
contract repairs in §7 and found no remaining blocking ambiguity in its review
coverage. It verified the pinned ESLint observations against source and retained
the candidate-only/graph/gate boundaries. The editorial status list in §3 now points
to the authoritative §7.1 taxonomy. This is spec review evidence, not implementation
validation; no evidence extractor, artifact, graph promotion or new gate run exists.
