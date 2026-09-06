"""Copy the time-lapse readings into reports/2026-09-05-phase1/ and write the cross-repo table."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "out" / "timelapse-b"
DST = ROOT / "reports" / "2026-09-05-phase1b"
DST.mkdir(parents=True, exist_ok=True)

rows = []
runs = sorted(p for p in SRC.iterdir() if (p / "frames.json").exists())
for run in runs:
    m = json.loads((run / "frames.json").read_text(encoding="utf-8"))
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

(DST / "phase1-reading.md").write_text(
    f"""# Phase 1 — time-lapse reading across the reference set under substrate 0.3.0 (D-021, D-022 addendum)

*2026-09-05. `substrate timelapse`, twelve evenly spaced first-parent checkpoints per repository, maintainability + onboarding overlay, `reports/2026-09-05-m1b/validation.json` at HEAD governing every frame, substrate config `config/tuned.toml` under substrate 0.3.0 (fingerprint `5f5554e36d4a`; age and recency fractional days, D-022). Supersedes `reports/2026-09-05-phase1/` where the numbers differ; the first reading is kept as the record of the instrument that found the artefact. Per-run reports, manifests, and scrubber pages sit beside this file as `<repo>.<geometry>.*`. Spec: `time-lapse-spec.md`.*

The question (D-020): over a repository's history, is the named structure structural change or the budget's jitter? Movement between adjacent frames decomposes into **edits** (feature changes and strata moves on rooms the intervening commits touched — the skeleton reporting the edit), **ripple** on rooms they did not touch, split into **clock** (clock-relative signals and age-geometry strata: the skeleton reporting time) and **rank** (the percentile or the dependency layer moved under an untouched room — jitter), and **structural** (rooms born or deleted). The rank share is the answer.

| repo | geometry | schedule | trunk | mapped/skipped | commits spanned | median K | movement | edits | clock | rank | mixed | **jitter** | structural | budget tally |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Readings (regenerated under the D-024 operand, judged against the ceilings pre-registered in D-024)

- **"Jitter is a few percent" is refuted for the young repositories and stands for the mature ones.** Pre-registered: a jitter share above 0.20 on any (repository, geometry), or above 0.10 on two repositories, refutes it. Observed: mcp-secure-server 0.32 / 0.19, uluops-registry-api 0.30 / 0.20 (age / layer); typeorm 0.12 / 0.08; eslint 0.05 / 0.05. Both conditions fire. The first reading's 2–7% was the one-sided classifier and the integer-day artefact together.
- **What the jitter is.** On the young repositories the rank column is dominated by floor moves of untouched rooms under age geometry: a population that grows by a fifth between frames re-ranks every age band, and a room keeps its floor by keeping its rank, not its age. That is movement of what did not itself change — jitter by D-018's definition — and it is caused by births, structural change propagating through in-repo percentiles (time-lapse §6.2; D-024, Nagarjuna TL-1). Under layer geometry the same repositories jitter at 0.19–0.20, the dependency-layer propagation D-018 noted. The mature repositories, whose populations grow by a few percent between frames, sit at 0.05–0.12.
- **The schedule is not averaging jitter away.** Pre-registered: every-5 exceeding twelve frames by more than 2× or 0.10 absolute refutes it. mcp-secure-server: 0.33 at every 5 against 0.32 at twelve frames. Stands.
- **Clock ripple** is now 0.03–0.23 and no longer the dominant non-edit movement anywhere; the tie artefact (D-022) and the age-strata reclassification account for the fall from the first reading's 0.44–0.61.
- **The budget at time-lapse K is `untested: beyond_pinned_k`** on every twelve-frame transition of every repository, by construction (K ≥ 12 > max_k = 10); only the every-5 run renders verdicts, and there the budget fired on the transitions where births re-ranked the bands. At K = 5 the adversarial ruleset could not make it fire (`reports/2026-09-05-m2b/adversarial-ruleset.md`); the ceiling's K is the open question (time-lapse §7 Q2).
- **The change sheets** (`<repo>.<geometry>.timelapse.html`, toggle "change sheet"; D-023) put the decomposition on the rooms, with each mark's evidence values in its tooltip; a room takes its strongest mark, rank > mixed > clock.

## What this decides

The phase's conclusion is restated with the corrected instrument. Over a **mature** repository's history the named structure is edits and births, with jitter at 5–12%: worth narrating on D-003's condition, as far as a mechanical test can say. Over a **young, fast-growing** repository the picture re-ranks by a fifth to a third between frames under self-relative calibration, and a narrative over it would be narrating the calibration as much as the building. That is a finding about in-repo percentiles on small growing populations, not about the repositories; corpus-relative calibration (Phase 3) is where it would change. Whether M3 is built, and for which class of repository, is a product judgment (D-020, D-024).
""",
    encoding="utf-8",
)
print(f"{len(runs)} runs → {DST}")
