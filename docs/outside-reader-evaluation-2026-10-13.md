# Outside-reader exercise — facilitator protocol and evaluation

Status: prepared, not run. No reader has been selected or contacted. Do not send this
facilitator document to the participant. An independent human reader is still needed;
an AI persona run does not substitute for this exercise.

## Artifact manifest

Give the participant only the separate handout and these artifacts, in order:

- A: `reports/2026-09-24h-m3x/mcp-secure-server.brief.md`, brief 0.44.0,
  commit `5348b3ef614d0da5912a56ee11f86fc5888a916b`, age geometry.
  SHA-256 `efb9669c0d91f811479112d5f05f5d0bb0e0a9db5e698461c53808177e850deb`.
- B: reviewed D-080 `mcp-secure-server.layer.change.svg`, currently in the
  Codex task workspace's `stability-fixed-diagnostics/`, layer geometry,
  `4c99da71468c29bb285a3f0d3ad644ef8b4abe7d` to the same after commit.
  SHA-256 `363f99ba79bbe26cee190f9f2d7eea062c519cbe79a84765c0a6c1573e828dc0`.
- Facilitator evidence only: adjacent `mcp-secure-server.layer.diff.json`, SHA-256
  `a52b7e6d19cd0e9b876f265bd7c621e15587c599a9ed59c1525dce5c6b704df8`.

These are different geometry views of the same after revision, not the same skeleton.
The brief is an existing historical reading; the change sheet is fresh D-080 output.
Freeze these exact bytes before conducting the exercise. If they change, update the
manifest and evidence first. No computed-path artifact exists yet: do not show the
proposed D-081 spec as a working capability or explain it to the participant.

## Conduct

Record the reader's experience with code maintenance, familiarity with this repository,
prior exposure to these artifacts, date, rendering surface, artifact hashes and timing.
Prefer someone who did not author or previously review the project. Familiarity is a
recorded limitation, not a reason to erase inconvenient answers.

Give the handout without a tour, glossary, intended interpretation, or warning about
possible misconceptions. Preserve the artifacts' own text and disclosures. Observe
whether the reader discovers hovering/tooltips without prompting. Record rendering
failures separately from interpretation failures; the SVG's interactive title text needs
a surface that exposes it. If access assistance is necessary, record exactly what was
said and when. Do not explain the meaning of a feature or change while answers are
being collected.

Freeze Part A answers before showing B, and freeze Part B answers before asking for
supporting passages or revisions. Ask neutral follow-ups only: “Which part supported
that?” or “What remains unclear?” Capture spontaneous questions and time spent.
Do not mark answers right/wrong in front of the participant or guide a self-correction.

## Facilitator evidence key

Evaluate claims against the pinned artifacts, preserving each reader's words:

| Claim area | Supported evidence and limits |
|---|---|
| Brief population | 65 rooms; 264 source files; 61 test nodes; 138 excluded-kind nodes. They are different denominators. |
| Marks and sets | 88 diagnostic marks across profiles, 74 in base; repeated marks can name the same room/set. Seven excluded crack marks; 21 rooms occupy two or more distinct diagnostic sets. Marks are not independent defects. |
| Condition and priority | Features describe positions. No demonstrated bug, dead code, security failure, lack of test execution/coverage, severity ranking, or finished-versus-abandoned conclusion follows. A proposed investigation with an accurately stated reason is permissible. |
| Import/test graph | Resolved static import graph; computed loaders are not edges. A test-path importer is not evidence that a test executed. TypeScript import edges do not establish runtime causation. |
| Untouched jitter transition | 35 common untouched rooms; four changed rank/mixed (profile, feature, room) assignments divided by 35 jitter assignment-union members, 0.1142857. Two rooms lose these features. This denominator is not a count of all changed rooms or all untouched feature changes. |
| Other untouched feature changes | Four additional clock-only lit_room removals occur on structural-analysis.ts, text-decoding.ts, layer3-behavior.ts, and layer5-contextual-types.ts. Across all untouched features there are eight changed assignments / 46 assignment-union members, 0.1739130, affecting six rooms. Clock-only changes are reported separately from jitter; an answer observing them is supported. |
| Feature evidence | `src/types/index.ts` loses foundation in both profiles: load 0.8434 → 0.8429, cutoff 0.84085 → 0.84876. `src/index.ts` loses hub and corridor: centrality 0.0134 → 0.0128, cutoff 0.01285 → 0.01426; fan-out remains 2 at p50=2. These are both-side predicate observations, not proof of the cause of the raw change. |
| Layer strata | Four of 35 untouched rooms move floors. Config/index and content/helper-utils retain depth 2 while bands move 1 → 2. Semantic-policies depth 6 → 5, band 3 → 2; http-transport-manager depth 7 → 8, band 3 → 4. Two band-only moves and two raw-depth changes. |
| Budget | mcp remains over budget in age and layer feature comparisons; layer strata also exceeds the existing budget. This is a continuity-test result for the mapping, not a repository health score. D-080 exposes evidence without changing the verdict. |
| Unknowns | Missing/mismatched evidence is unavailable/unknown, not zero or a passing predicate. Eligibility and population floors are recorded separately from whether a predicate fires. No causal-edge attribution is asserted. |

## Coding and decision rule

Split answers into individual claims. Record the artifact passage/tooltip, claimed
inference, confidence, and one of: supported, unsupported, explicitly uncertain,
or not observed. A missing mention is not automatically a misunderstanding. For an
unsupported claim, distinguish a copied ambiguous label, inferred conclusion, and
rendering/access failure. Record initial claims and later self-corrections separately.

Pay particular attention to actionable unsupported condition claims, denominator
confusion, assignment-versus-room confusion, and raw-depth-versus-band movement.
Do not collapse these into one numerical comprehension score. Save a compact table:
`stage | verbatim claim | cited evidence | classification | uncertainty | revision`.
Use consented notes; any recording or publication requires a separate decision.

One reader is a case observation, not general validation or a new asserted signal.
A harmful unsupported first impression remains a finding even if corrected later.
After the exercise, propose a specific wording/display repair for each material
misreading, verify that it preserves the contracts, and repeat with a fresh reader
before claiming the repair improves first impressions. No verdict or improvement
is claimed until the exercise is actually conducted.

**Independent protocol review (2026-10-13).** Reviewer verified the manifest hashes,
neutral handout, frozen initial answers and absence of any claimed human run/outreach.
It identified an overbroad evidence-key statement: four assignment changes/two rooms
was the jitter subset, not every untouched feature. The key now names that subset
and separately records the four clock-only changes (all untouched: eight assignments,
six rooms). This repair changes the evaluation key, not the participant prompts.
