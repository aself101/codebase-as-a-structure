# Stability budget on a small population — evidence for `stability-budget-spec.md` (2026-11-11)

Read-only readings from the pinned k25k caches (fingerprint `298696064105`); nothing here
changes a saved verdict.

- `operands_pinned.py` → `operands_pinned.md`: four operand variants on the four pinned
  comparisons. `uv run python reports/2026-11-11-stability/operands_pinned.py` from the
  repository root; reads `out/m2x-2026-11-11-d080/` and `out/cache/`.
- `operands_timelapse.py <walk dir>…` → `operands_timelapse.txt`: current operand against
  untouched-population cutoffs on each walk transition. It reads the walk's
  `f*.skeleton.json`, which are **not committed** (the walk output directories were in a
  session scratchpad, named `out-k25` and `out-k15` in the txt); regenerate them with the
  commands below to re-derive it.
- Walk diffs (committed): `mcp-every25/` and `mcp-every15/` (layer, from `5348b3ef614d`);
  `mcp-out-k25-age/` (age, same start); `mcp-out-k25-off12-layer/` and
  `mcp-out-k25-off12-age/` (from `f147391554ac`, twelve first-parent commits earlier).

Walk command, run against a clone of mcp-secure-server checked out at the start commit
(the live checkout has moved past the pin):

    uv run substrate timelapse <clone> --validation out/validation-k25k/validation.json \
      --ruleset rulesets/maintainability.toml --overlay rulesets/onboarding.toml \
      --geometry <layer|age> --every <25|15> --config config/tuned.toml -o <dir>
