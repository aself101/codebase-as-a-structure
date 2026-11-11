# D-080 independent adversarial review — 2026-10-13

A fresh Codex reviewer (`/root/review_d080`), without the implementation author's
conversation history, examined the three D-080 contract sections, actual implementation
and test diffs, isolated synthetic inputs, and the attested four-repository snapshots.
This is a local review; no registry definition, paid API call, external reader, or tracker
run is claimed.

## Findings and disposition

1. **P2 — missing node eligibility metadata became false.** The original diagnostic
   helper defaulted an absent `load_index_degraded` flag to false and could assert
   graph-dependent eligibility. Repaired: missing relevant metadata remains unknown;
   known global/node degradation still settles eligibility false. The independent
   recheck also found a precedence case with missing signal status; known degradation
   now takes precedence over that unrelated absence.
2. **P2 — tooltips omitted required disclosures.** A ten-room reproduction printed
   eligibility true but omitted the recorded floor (`n=10`, `min=30`, `met=False`).
   Tooltips also omitted eligibility and per-term unknown reasons. Repaired: the
   recorded floor and reasons travel with both-side evidence. This does not change
   the mapper's existing eligibility or population-floor semantics.

Regressions: `test_missing_node_degradation_is_unknown_when_graph_dependent` and
`test_tooltip_discloses_unmet_floor_and_missing_term_reason` in
`tests/test_stability_evidence.py`.

## Independent coverage

The reviewer ran 19 initial focused tests and nine evidence tests on repair rechecks;
reproduced known/unknown degradation combinations, chained renames, seed/config
provenance refusal, and a compound predicate with outcomes `[None, True]`; checked
exact nested configuration serialization and observed raw-depth/band attribution;
and independently replayed all eight saved comparisons against HEAD's original diff.
Every pre-existing output field matched, including mcp's 4/35 over-budget result.
No new causal-edge overclaim was found. Final recheck: no blocking defects remain
from the review's coverage.

The author additionally reran the eight diagnostics after the final repair. Full-suite
and changed-file lint results are recorded in the D-080 decision-log addendum.
Limitations: no complete timelapse regeneration, outside-reader test, or general
security audit; targeted independent rechecks do not establish those outcomes.
