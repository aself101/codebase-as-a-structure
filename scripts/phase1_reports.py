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
        f"{t['commits_between']:,} | {t['movement']:,} | {t['edit_share']:.2f} | {t['ripple_clock_share']:.2f} | "
        f"**{t['ripple_rank_share']:.2f}** | {t['structural_share']:.2f} | {tally} |"
    )

(DST / "phase1-reading.md").write_text(
    f"""# Phase 1 — time-lapse reading across the reference set under substrate 0.3.0 (D-021, D-022 addendum)

*2026-09-05. `substrate timelapse`, twelve evenly spaced first-parent checkpoints per repository, maintainability + onboarding overlay, `reports/2026-09-05-m1b/validation.json` at HEAD governing every frame, substrate config `config/tuned.toml` under substrate 0.3.0 (fingerprint `5f5554e36d4a`; age and recency fractional days, D-022). Supersedes `reports/2026-09-05-phase1/` where the numbers differ; the first reading is kept as the record of the instrument that found the artefact. Per-run reports, manifests, and scrubber pages sit beside this file as `<repo>.<geometry>.*`. Spec: `time-lapse-spec.md`.*

The question (D-020): over a repository's history, is the named structure structural change or the budget's jitter? Movement between adjacent frames decomposes into **edits** (feature changes and strata moves on rooms the intervening commits touched — the skeleton reporting the edit), **ripple** on rooms they did not touch, split into **clock** (clock-relative signals and age-geometry strata: the skeleton reporting time) and **rank** (the percentile or the dependency layer moved under an untouched room — jitter), and **structural** (rooms born or deleted). The rank share is the answer.

| repo | geometry | schedule | trunk | mapped/skipped | commits spanned | movement | edits | clock | **rank** | structural | budget tally |
|---|---|---|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Readings

- **Rank jitter is a small share of movement everywhere it can be measured:** 2–7% under age geometry, 3–16% under layer geometry, the layer maxima on the youngest repository, where strata moves on untouched rooms are dependency-layer propagation (D-018's observation, now measured over a history). The named structure over a history is overwhelmingly edits, time, and births.
- **The fine schedule agrees with the coarse one.** mcp-secure-server at every 5 commits: rank 10% against 7% at twelve frames; on the first reading (substrate 0.2.x) the registry at every 10 commits gave 5% against 5%. The twelve-frame schedule is not averaging jitter away (D-021 breaks-if, checked).
- **What substrate 0.3.0 removed was clock, not rank.** Against `reports/2026-09-05-phase1/`, mcp-secure-server's clock share fell 0.61 → 0.44 at twelve frames and its every-5 movement fell 1,649 → 1,054, almost all of it clock; the registry's clock share fell 0.37 → 0.33. Those were birth cohorts flipping floors and lights as integer-day ties broke (D-022). Rank shares rose by a point or two only because the denominator shrank.
- **Clock ripple remains the dominant non-edit movement on the young repositories** (33% on the registry, 44% on mcp-secure-server under age geometry): weeks pass between frames, and `lit_room` / `dark_room` / `flooded_basement` and the age bands move on rooms nobody touched because the checkpoint's clock advanced. That is the skeleton reporting time, and it is why D-018's single number does not transfer to K in the hundreds unchanged (time-lapse spec §4, §7 Q2).
- **The mature repositories are edits.** eslint: 80% of movement is on touched rooms; with ~790 commits between frames the intervening commits touch most of the population and the budget's floors refuse every transition — the floors working as designed on a schedule too coarse for them.
- **The change sheets** (`<repo>.<geometry>.timelapse.html`, toggle "change sheet"; D-023) put the decomposition on the rooms: a transition's births, edits, clock, and rank marks on the after frame's layout, deleted rooms dashed under each wing.

## What this decides

M3's condition (D-003: "built only if M2 proves the skeleton is worth narrating") is met in the sense the time-lapse can test: the structure that moves between frames is change and time, not jitter. Whether the *narrative* over it is worth building remains a product judgment, logged in D-021.
""",
    encoding="utf-8",
)
print(f"{len(runs)} runs → {DST}")
