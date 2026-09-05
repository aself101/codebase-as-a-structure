# Companion Checklist — System Integration (seams & cross-cutting invariants)

*Conformance checklist for the contracts that live in **no single component spec**: the inter-component seams and the system-level invariants from `codebase-as-structure-system-spec.md` §3. This is the layer, not the union — it does **not** re-list per-component items (those live in each component's own companion checklist). It verifies that the components, each correct on its own, compose correctly.*

**Why this exists separately:** the highest-stakes contracts — the anti-horoscope gate, the seed→every-stage determinism flow, the end-to-end provenance chain — are explicitly *system-level* (system spec §3). A per-component checklist structurally cannot verify that C1's hash reaches C6, or that `validation.json`'s keys join `substrate.json`'s. That's this file's whole job.

**Legend — contract class:** `[DET]` determinism flow · `[SEAM]` artifact handoff · `[HOR]` anti-horoscope · `[PROV]` provenance chain · `[VER]` versioning · `[LAYER]` multi-profile layering.
**Legend — verification:** `(golden)` byte-identical two-commit diff · `(e2e)` full-pipeline run · `(unit)` boundary unit test · `(review)` human.

---

## A. Determinism flow — the seed crosses every boundary (§3 determinism contract)

- [ ] `[DET]` The seed originates as C1's content hash of the resolved tree (`substrate.seed`) and is the **single** origin — no stage invents its own randomness. *(sys §3; substrate §3)* `(unit)`
- [ ] `[SEAM]` `skeleton.json.substrate_seed` equals `substrate.json.seed` verbatim. *(mapper §5)* `(unit)`
- [ ] `[DET]` The seed flows C1 → C4 (`massing.json`) → C6 (render); a full run on the same SHA + same component versions + same profile reproduces the same render. *(sys §3)* `(e2e, golden)`
- [ ] `[DET]` Two renders of two commits differ **only** by what actually changed in the substrate — a meaningful diff, not noise. *(sys §3, §8)* `(golden)`
- [ ] `[DET]` No stage reaches back upstream; data flow is strictly C1 → C3 → C4 → C5 → C6 with C2 as a side-input to C3. *(sys §3)* `(review)`

## B. Artifact handoff seams (§2 table, component I/O)

- [ ] `[SEAM]` **substrate → validation:** validation consumes `substrate.json` produced under `--truncate-at <split-sha>`; the truncated substrate sees only training-window history. *(validation §7; substrate §8)* `(unit)`
- [ ] `[SEAM]` **substrate ↔ validation key join:** every signal name in `validation.json.signals` is an exact identifier from `substrate.json.derived` (index, percentile, or raw metric name); a name the ruleset references but validation omits resolves to `untested`. *(validation §6.1)* `(unit)`
- [ ] `[SEAM]` **substrate → mapper:** every signal a C3 predicate reads exists in `substrate.json.derived` under the same name. *(mapper §3, §5)* `(unit)`
- [ ] `[SEAM]` **C2 → mapper (optional):** when `signal.json` is absent, no C3 feature that requires it is emitted as grounded; C2-dependent features degrade or omit, they do not silently render. *(mapper §7 Q4)* `(unit)`
- [ ] `[SEAM]` **mapper → C4:** geometry (node positions, strata, massing) is derived from the substrate and is **profile-independent**; profiles change foregrounding, not geometry. *(mapper §6)* `(unit)`
- [ ] `[SEAM]` **C5 → mapper:** every claim in `brief.md` references a `skeleton.json` feature id; a claim with no feature id is rejected. *(sys §3 provenance)* `(unit)`

## C. The anti-horoscope gate, end to end (§3 system invariant; validation §5; mapper §3)

- [ ] `[HOR]` No named feature in `skeleton.json` rests on a signal whose `validation_status` is `unvalidated`/`untested` unless the rule is `decorative: true`; otherwise C3 refuses to emit. *(mapper §3; validation §5)* `(unit)`
- [ ] `[HOR]` The gate is checked at **signal level** — every signal in a predicate, including bare percentiles and raw metrics, not just composite indices. *(sys §3; validation §5; mapper §3)* `(unit)`
- [ ] `[HOR]` A `kind`/`status` mismatch in `validation.json` is rejected **before** the gate runs — a failed predictor cannot relabel as `asserted` to slip through. *(validation §3.8; mapper §3)* `(unit)`
- [ ] `[HOR]` A feature's `validation_status` is the most conservative claim type across all signals it reads (any FAIL-tier signal → feature fails; all-pass but mixed → `asserted`). *(mapper §5)* `(unit)`
- [ ] `[HOR]` **Register binding crosses the C3→C5 seam:** C5 may voice a forecast only from a `validated` signal and only a present-structural statement from an `asserted` one; a hybrid feature draws forecast strictly from its validated half. *(mapper §3, §5; validation §2.1.1)* `(review)`
- [ ] `[HOR]` A `decorative: true` feature renders with an unvalidated marker and is excluded from diagnostic claims in the brief. *(validation §5; mapper §3)* `(unit, review)`
- [ ] `[HOR]` Graph-dependent features (foundation, corridor, bridge, tower) suppress or flag `degraded` when `graph_available: false`, `graph_degraded: true`, or node `load_index_degraded: true`. *(mapper §4.1; substrate §6.3)* `(unit)`
- [ ] `[HOR]` A `contested`/divergent §3A corroboration does **not** change any `validation_status` and therefore does not change what the gate admits — it is a report-level finding only. *(validation §3A.1, §3A.8, §5)* `(unit)`

## D. Provenance chain — resolves all the way down (§3 provenance)

- [ ] `[PROV]` Every `skeleton.json` feature carries an `evidence` block (the metric/index/topology values + the predicate). *(sys §3; mapper §5)* `(unit)`
- [ ] `[PROV]` The full chain resolves: `brief-claim → feature → predicate → evidence → substrate metric` **and** `feature → signal → validation_status → holdout report (or recorded recognition/stability grounding)`. *(sys §3; validation §5; mapper §5)* `(e2e)`
- [ ] `[PROV]` "Why is this file a toothpick, and should I believe it?" resolves to a precision@k number on a named reference repo (`validated`) or a named recognition/stability justification (`asserted`). *(validation §5)* `(review)`

## E. Versioning (§3 versioning; per-artifact)

- [ ] `[VER]` Each artifact records its `schema_version` and the producing component version. *(sys §3)* `(unit)`
- [ ] `[VER]` `skeleton.json` records `ruleset_version` and `profile{name,version}`; the render is reproducible/auditable from artifacts alone. *(sys §3; mapper §5)* `(unit)`
- [ ] `[VER]` `substrate.config_fingerprint` (incl. index weights + `toolchain_versions`) and `validation_config_fingerprint` are both recorded so a moved value resolves to a specific diff. *(substrate §3; validation §7)* `(golden)`
- [ ] `[VER]` `validation.json` records `substrate_config_fingerprint` — the exact substrate config its verdicts validate — so a verdict is never read against a substrate it didn't test. *(validation §6.1)* `(unit)`

## F. Multi-profile layering — never unification (§3; sys open Q2; mapper §6)

- [ ] `[LAYER]` Running several profiles yields overlapping skeletons of one shared geometry; the system never merges them into a single verdict. *(mapper §6; sys open Q2)* `(unit)`
- [ ] `[LAYER]` Co-located findings (a *Security* fortress that is also a *Maintainability* toothpick) are shown side-by-side, never averaged. *(mapper §6)* `(unit, review)`
- [ ] `[LAYER]` Output carries a base layer plus named `overlays`; the renderer toggles them. *(mapper §5, §6)* `(unit)`

---

## Seam-tracking (cross-references, not code items)

- **Open precondition (blocks §3A promotion, not the build):** the §3A.13.0 independence question — system spec §8 open question #5. Answer is owned by the cognitive-lens agent owner; track to closure before §3A becomes a co-equal falsifier.
- **Reserved seam rows (fill when their specs are authored):** C2 `signal.json` → C3 enrichment contract; C4 `massing.json` → C6 geometry; C5 `style.json` → C6 render. The integration view is intentionally complete-by-reservation ahead of those components.
- **Stability budget (shared open question):** how much a small code change may move the skeleton before it counts as a structural shift — system spec open Q3 / mapper §7 Q3 / validation §2.1 stability bar. One number, referenced by three specs; pin it once and verify all three read it.
