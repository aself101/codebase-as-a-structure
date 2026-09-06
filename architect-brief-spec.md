# Architect brief — C5 with the register lint (M3)

*Component 5 of codebase-as-structure, built 2026-09-06 as M3 (D-003, D-025, D-027). The brief is prose over `skeleton.json`: the building described by a condemnation surveyor, warts and all, in the **descriptive register only**. It is the one stage with a model in the path, and it is held to the anti-horoscope contract by a deterministic lint that runs after the model and refuses what the model may not say. Implemented in `src/repo_substrate/brief.py` as `substrate brief`.*

## 1. Contract

The brief may say what the skeleton says and nothing else. Concretely:

- **Register (validation §2.1.1, mapper §3).** Every feature in v0 rests on an `asserted` signal, which licenses a present structural position. The brief therefore speaks in the present tense about where rooms sit and what fires on them. It may not voice a consequence or a forecast — not "will break," not "fragile," not "changes here ripple." Those are predictions; none is licensed. When `blast_radius_index` or the pressure indices are `validated`, the register widens for them and only them.
- **Provenance (system-integration checklist, C5 → mapper seam).** Every paragraph cites the feature and room it rests on, in brackets: `[feature: path]`, `[feature: a, b]`, or `[feature ×N]`. A citation must resolve — the feature is in the skeleton, the room fired for it, the count is the skeleton's count. A paragraph with no citation is a violation.
- **Numbers.** Only numbers in the facts sheet: populations, wing sizes, feature counts, a room's lines, fan-in, fan-out. No estimates, no percentages.
- **Decorative features (mapper §3).** Excluded from diagnosis; their count is stated once where a reader sees it, with the feature names.
- **Disclosure (D-004 Q3).** A feature whose name implies a consequence (`name_implies_consequence`) is disclosed with its `position_name` — the grammar D-024 gave the flag is what the lint reads.
- **No label (D-019).** The building is not called a cathedral, a shantytown, or anything else. No archetype exists.
- **Stance (system spec, stance disclosure).** The brief carries the stance sentence: the diagnosis presupposes a maintenance norm the reader may reject.

## 2. Pipeline

1. **Facts sheet** — `facts(skeleton, substrate)`: a pure function of the skeleton (and the substrate's sizes). The closed set of sayable things: diagnostic features with their rooms, decorative features by count, wings and room counts, the gate's per-signal statuses, position names, the stance. Hashed; the hash is in the brief's provenance.
2. **Generation** — one call to a model (default `claude-opus-5`, adaptive thinking, effort high, server-side refusal fallback enabled) with the surveyor stance and the register rules as the system prompt and the facts sheet as the only material. Non-deterministic; the model served, request id, tokens, and attempt are written into the brief. If the first draft fails the lint, the violations are fed back once and the brief is regenerated (`--max-attempts`, default 2).
3. **Register lint** — `lint(text, facts)`: deterministic, seven rules (R1 consequence vocabulary per sentence, exempting disclosure sentences; R2 provenance of every citation and at least one per paragraph; R3 numbers; R4 decorative features not cited in diagnosis; R5 position-name disclosure; R6 whole-building label; R7 decorative count stated). Output: the violations table.
4. **The brief** — `brief.md`: header with the lint status, the prose, a provenance section, the lint section. A brief that fails is written **marked FAILED** and the command exits 1; it is not a diagnosis until it passes. `--draft` lints a hand-written brief with no model in the path; `--facts` writes the facts sheet beside the brief.

## 3. The adversarial lens (D-003's phrase)

The system spec asked for an "adversarially-framed Generator lens (a condemnation surveyor, not a realtor)." In v0 that is two things: the stance in the system prompt — the surveyor honours ugly facts — and the lint as the hostile reader, which is deterministic and therefore the part a reader can trust. A second model pass acting as hostile reader is not built (§5 Q1); the lint is what the anti-horoscope contract can enforce.

## 4. Limitations (on the page)

1. **The lint reads words, not meanings.** A consequence voiced without a listed word passes; a listed word in an innocent sense fails. The lexicon is in `brief.py::CONSEQUENCE_WORDS` and is the audit surface. False negatives are the risk that matters; the lexicon errs toward false positives.
2. **The model is not deterministic.** Two runs over one facts sheet produce two briefs. The facts hash and the lint status are what make a brief comparable; the prose is not.
3. **Scope (D-024, D-025).** On a young, fast-growing repository the skeleton re-ranks by a fifth to a third between frames; a brief over it narrates the calibration as much as the building. M3 is scoped to mature repositories; the brief states the skeleton hash it describes, and a time-lapse says how long that skeleton stood.
4. **The model sees the facts sheet without room metrics** (the `rooms` block is withheld to keep the prompt small); it may cite rooms but not their line counts unless a feature's count is the number. Metrics remain in the facts sheet for the lint.

## 5. Open questions

1. **A hostile-reader model pass.** A second call that tries to find an unsupported sentence, with its findings mapped to lint rules or struck. Would catch the meaning-level consequence claims §4.1 misses.
2. **Style/material directives** (`style.json`, system spec C5). Not built; the cutaway takes material from age and nothing from the brief.
3. **Widening the register.** When a predictive index is `validated`, the lint must admit consequence vocabulary sourced from that index and only that index — a per-signal lexicon, sourced from `validation.json`.
