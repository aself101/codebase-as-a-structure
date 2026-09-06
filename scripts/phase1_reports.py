"""Copy the time-lapse readings into reports/2026-09-05-phase1/ and write the cross-repo table."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import os

SRC = Path(os.environ.get("PHASE1_SRC", ROOT / "out" / "timelapse-b"))
DST = Path(os.environ.get("PHASE1_DST", ROOT / "reports" / "2026-09-05-phase1b"))
DST.mkdir(parents=True, exist_ok=True)

rows = []
runs = sorted(p for p in SRC.iterdir() if (p / "frames.json").exists())
gates: set[tuple] = set()
for run in runs:
    m = json.loads((run / "frames.json").read_text(encoding="utf-8"))
    gates.add(
        (
            m["gate"]["substrate_config_fingerprint"],
            m["gate"]["validation_config_fingerprint"],
            m["gate"].get("validated_at"),
        )
    )
    for name in ("frames.json", "timelapse.md", "timelapse.html"):
        shutil.copy(run / name, DST / f"{run.name}.{name}")
    t = m["totals"]
    tally = ", ".join(
        f"{k.replace('untested:', 'untested: ')} × {v}" for k, v in t["budget_tally"].items()
    )
    rows.append(
        f"| {m['repo']['name']} | {m['geometry']} | {'every ' + str(m['schedule'].get('every')) if m['schedule'].get('every') else str(m['schedule'].get('frames')) + ' frames'} | {m['repo']['trunk_length']:,} | {t['mapped']}/{t['skipped']} | "
        f"{t['commits_between']:,} | {t['k_median']} | {t['movement']:,} | {t['edit_share']:.2f} | {t['ripple_clock_share']:.2f} | "
        f"{t['ripple_rank_share']:.2f} | {t['ripple_mixed_share']:.2f} | **{t['jitter_share']:.2f}** | {t['structural_share']:.2f} | {tally} |"
    )

if len(gates) != 1:
    raise SystemExit(
        f"the runs under {SRC} were made under {len(gates)} different gates; one reading needs one gate"
    )
(gate_fp, val_fp, validated_at) = next(iter(gates))
generated = datetime.now(timezone.utc).strftime("%Y-%m-%d")
(DST / "phase1-reading.md").write_text(
    f"""# Phase 1 — time-lapse reading across the reference set (D-021; gate `{gate_fp[:12]}`)

*Generated {generated}. `substrate timelapse`, twelve evenly spaced first-parent checkpoints per repository, maintainability + onboarding overlay; every frame governed by the gate at HEAD — substrate fingerprint `{gate_fp[:12]}`, validation config `{val_fp[:12]}`, validated {validated_at} — read from the manifests beside this file (D-035: the header states what the rows state, or it states nothing). Earlier readings (`reports/2026-09-05-phase1/`, `-phase1b/`, `2026-09-06-phase1x/`, `2026-09-06b-phase1x/`) are kept as the record of the instruments that produced them. Per-run reports, manifests, and scrubber pages sit beside this file as `<repo>.<geometry>.*`. Spec: `time-lapse-spec.md`.*

The question (D-020): over a repository's history, is the named structure structural change or the budget's jitter? Movement between adjacent frames decomposes into **edits** (feature changes and strata moves on rooms the intervening commits touched — the skeleton reporting the edit), **ripple** on rooms they did not touch, split into **clock** (clock-relative signals and age-geometry strata: the skeleton reporting time) and **rank** (the percentile or the dependency layer moved under an untouched room — jitter), and **structural** (rooms born or deleted). The rank share is the answer.

| repo | geometry | schedule | trunk | mapped/skipped | commits spanned | median K | movement | edits | clock | rank | mixed | **jitter** | structural | budget tally |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## How to read it

- **The jitter share is the answer** to the phase's question, per (repository, geometry, schedule), and it is quoted with its median K because it is a joint value of repository and schedule (D-024, D-026).
- **Clock** is the skeleton reporting time; **edits** are the skeleton reporting edits; **structural** is births and deletions; only **rank + mixed** is jitter.
- **The budget's verdicts** are rendered only at 25 ≤ K ≤ 50 (D-026, D-032); on twelve-frame schedules almost every transition is `untested` by construction (`beyond_pinned_k` on the long histories, `below_pinned_k` on the short one), and the numbers stand on their own.
- The pre-registered ceilings of D-024 (jitter above 0.20 on any repository/geometry, or above 0.10 on two, refutes "a few percent") are judged in the decision log, not here; this file is the reading.
- Per-run pages beside this file carry the frames, the change sheets (D-023), and the per-transition tables.
""",
    encoding="utf-8",
)
print(f"{len(runs)} runs → {DST}")
