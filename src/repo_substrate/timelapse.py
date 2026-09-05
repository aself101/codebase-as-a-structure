"""Phase 1 — the evolution time-lapse (system spec §8; `time-lapse-spec.md`; D-020, D-021).

A consumer of M1 and M2: per checkpoint on the first-parent trunk it runs extraction
(truncated at the checkpoint), the mapper under HEAD's gate, and the cutaway; between
adjacent mapped frames it runs the skeleton diff with the D-018 budget. It adds no signal,
no feature, no geometry. Its question is whether the named structure of a repository over
its history is structural change or the budget's jitter — the test M3 waits on (D-020).
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any

from .cutaway import render_change_sheet, render_cutaway
from .gitutil import run_git
from .mapper import Ruleset, map_skeleton
from .mapper.diff import skeleton_diff, touched_between
from .validation.substrates import SubstrateCache


class TimelapseError(ValueError):
    pass


# Signals measured against the checkpoint's clock (substrate spec §5, §7): a node nobody
# edited still moves on these because time passed or history lengthened. Movement on
# untouched nodes through these signals is the skeleton reporting time, not jitter
# (time-lapse §4). `recent_commit_share` is timeline-relative by commit count, which is a
# clock in commits rather than days; the two indices carry a clock input each.
CLOCK_SIGNALS = frozenset(
    {
        "age_days",
        "last_touched_days",
        "blame_age_median",
        "recent_commit_share",
        "neglect_index",
        "change_pressure_index",
    }
)


def feature_kinds(ruleset: Ruleset, overlays: tuple[Ruleset, ...]) -> dict[str, str]:
    """(profile/feature) → 'clock' if any signal the predicate reads is clock-relative, else 'rank'."""
    kinds: dict[str, str] = {}
    for rs in (ruleset, *overlays):
        for f in rs.features:
            kinds[f"{rs.profile}/{f.name}"] = (
                "clock" if any(s in CLOCK_SIGNALS for s in f.signals) else "rank"
            )
    return kinds


def trunk(repo: Path) -> list[str]:
    """First-parent line, root first (time-lapse §2)."""
    out = run_git(repo, "rev-list", "--first-parent", "--reverse", "HEAD")
    return [line.strip() for line in out.splitlines() if line.strip()]


def choose_checkpoints(n: int, frames: int | None = None, every: int | None = None) -> list[int]:
    """Trunk indices for the schedule: `frames` evenly spaced (first and last inclusive) or
    `every` K commits walking back from HEAD. HEAD (index n-1) is always the last frame."""
    if n <= 0:
        raise TimelapseError("empty trunk")
    if (frames is None) == (every is None):
        raise TimelapseError("choose exactly one of frames / every")
    if every is not None:
        if every < 1:
            raise TimelapseError("every must be >= 1")
        idx = list(range(n - 1, -1, -every))
        return sorted(set(idx))
    assert frames is not None
    if frames < 1:
        raise TimelapseError("frames must be >= 1")
    if frames == 1 or n == 1:
        return [n - 1]
    return sorted({round(i * (n - 1) / (frames - 1)) for i in range(frames)})


def _feature_counts(skeleton: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = dict(skeleton["summary"]["feature_counts"])
    for od in skeleton.get("overlays") or []:
        for name, c in od["summary"]["feature_counts"].items():
            counts[f"{od['profile']}/{name}"] = c
    return counts


def _diff_summary(d: dict[str, Any], kinds: dict[str, str], geometry: str) -> dict[str, Any]:
    touched_changes = sum(
        len(v["added"]) + len(v["removed"]) - v["untouched_changes"]
        for v in d["per_feature"].values()
    )
    untouched_changes = sum(v["untouched_changes"] for v in d["per_feature"].values())
    clock_feat = sum(
        v["untouched_changes"] for k, v in d["per_feature"].items() if kinds.get(k) == "clock"
    )
    strata_untouched = len(d["untouched"]["strata_moved"])
    clock_strata = strata_untouched if geometry == "age" else 0
    return {
        "ripple_clock": clock_feat + clock_strata,
        "ripple_rank": (untouched_changes - clock_feat) + (strata_untouched - clock_strata),
        "commits_between": d["commits_between"],
        "common_nodes": d["common_nodes"],
        "born": d["born"],
        "deleted": d["deleted"],
        "touched": d["touched"]["n"],
        "touched_frac": d["touched"]["frac"],
        "feature_churn": d["feature_churn"],
        "strata_moved_frac": d["strata_moved_frac"],
        "untouched_n": d["untouched"]["n"],
        "untouched_churn": d["untouched"]["feature_churn"],
        "untouched_strata_frac": d["untouched"]["strata_moved_frac"],
        # the decomposition of movement (time-lapse §4)
        "feature_changes_touched": touched_changes,
        "feature_changes_untouched": untouched_changes,
        "strata_moves_touched": len(d["strata_moved"]) - len(d["untouched"]["strata_moved"]),
        "strata_moves_untouched": len(d["untouched"]["strata_moved"]),
        "budget_verdict": d["budget"]["verdict"],
        "budget_reason": d["budget"]["reason"],
    }


def run_timelapse(
    repo: Path,
    cache: SubstrateCache,
    validation: dict[str, Any],
    ruleset: Ruleset,
    overlays: tuple[Ruleset, ...],
    geometry: str,
    checkpoints: list[int],
    out_dir: Path,
    schedule: dict[str, Any] | None = None,
    log=None,
) -> dict[str, Any]:
    repo = repo.resolve()
    line = trunk(repo)
    out_dir.mkdir(parents=True, exist_ok=True)
    gate_fp = validation.get("substrate_config_fingerprint")
    kinds = feature_kinds(ruleset, overlays)
    frames: list[dict[str, Any]] = []
    prev: tuple[dict[str, Any], dict[str, Any]] | None = None  # (substrate, skeleton)
    for i, ti in enumerate(checkpoints):
        if not 0 <= ti < len(line):
            raise TimelapseError(f"checkpoint index {ti} outside trunk of {len(line)}")
        sha = line[ti]
        sub = cache.get(repo, sha, truncate=True)
        if gate_fp and sub["repo"]["config_fingerprint"] != gate_fp:
            raise TimelapseError(
                f"frame {i} ({sha[:8]}): substrate fingerprint {sub['repo']['config_fingerprint'][:12]} "
                f"differs from the gate's {gate_fp[:12]}; the gate licenses nothing about it"
            )
        frame: dict[str, Any] = {
            "index": i,
            "trunk_index": ti,
            "sha": sha,
            "as_of": sub["repo"]["as_of"],
            "commit_count": sub["summary"]["commit_count"],
            "population": sub["summary"]["population_size"],
        }
        if not sub["summary"]["percentiles_valid"]:
            frame.update(status="skipped", reason="population_below_n_min")
            frames.append(frame)
            if log:
                log(f"frame {i} {sha[:8]}: skipped (population {frame['population']} below n_min)")
            continue
        skel = map_skeleton(sub, validation, ruleset, overlays, geometry)
        stem = f"f{i:03d}-{sha[:8]}"
        (out_dir / f"{stem}.skeleton.json").write_text(
            json.dumps(skel, indent=1, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        (out_dir / f"{stem}.cutaway.svg").write_text(render_cutaway(skel, sub), encoding="utf-8")
        frame.update(
            status="mapped",
            reason=None,
            stem=stem,
            skeleton_hash=skel["skeleton_hash"],
            feature_counts=_feature_counts(skel),
            diff=None,
        )
        if prev is not None:
            psub, pskel = prev
            ren = sub.get("renames", {})
            touched, between = touched_between(psub, sub, ren)
            d = skeleton_diff(pskel, skel, ren, touched, between)
            (out_dir / f"{stem}.diff.json").write_text(
                json.dumps(d, indent=1, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
                encoding="utf-8",
            )
            frame["diff"] = _diff_summary(d, kinds, geometry)
            (out_dir / f"{stem}.change.svg").write_text(
                render_change_sheet(pskel, skel, sub, d, kinds, psub), encoding="utf-8"
            )
            frame["change_stem"] = stem
        frames.append(frame)
        prev = (sub, skel)
        if log:
            dd = frame["diff"]
            log(
                f"frame {i} {sha[:8]}: {frame['as_of'][:10]} commits={frame['commit_count']} "
                f"population={frame['population']}"
                + (
                    f" | K={dd['commits_between']} born={dd['born']} del={dd['deleted']} "
                    f"untouched churn={dd['untouched_churn']:.3f} strata={dd['untouched_strata_frac']:.3f} "
                    f"ripple clock/rank={dd['ripple_clock']}/{dd['ripple_rank']} → {dd['budget_verdict']}"
                    + (f" ({dd['budget_reason']})" if dd["budget_reason"] else "")
                    if dd
                    else ""
                )
            )
    manifest = {
        "schema_version": "0.1",
        "repo": {"name": repo.name, "head_sha": line[-1], "trunk_length": len(line)},
        "schedule": schedule or {"checkpoints": checkpoints},
        "gate": {
            "substrate_config_fingerprint": gate_fp,
            "validation_config_fingerprint": validation.get("validation_config_fingerprint"),
            "validated_at": validation.get("validated_at"),
        },
        "ruleset": {"name": ruleset.name, "version": ruleset.version, "profile": ruleset.profile},
        "overlays": [
            {"name": o.name, "version": o.version, "profile": o.profile} for o in overlays
        ],
        "geometry": geometry,
        "feature_kinds": kinds,
        "frames": frames,
        "totals": _totals(frames),
    }
    (out_dir / "frames.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    (out_dir / "timelapse.md").write_text(render_report(manifest), encoding="utf-8")
    (out_dir / "timelapse.html").write_text(render_page(manifest, out_dir), encoding="utf-8")
    return manifest


def _totals(frames: list[dict[str, Any]]) -> dict[str, Any]:
    diffs = [f["diff"] for f in frames if f.get("diff")]
    tally: dict[str, int] = {}
    for d in diffs:
        key = d["budget_verdict"] + (f":{d['budget_reason']}" if d["budget_reason"] else "")
        tally[key] = tally.get(key, 0) + 1
    keys = (
        "born",
        "deleted",
        "feature_changes_touched",
        "feature_changes_untouched",
        "strata_moves_touched",
        "strata_moves_untouched",
        "ripple_clock",
        "ripple_rank",
        "commits_between",
    )
    sums = {k: sum(d[k] for d in diffs) for k in keys}
    moves = (
        sums["feature_changes_touched"]
        + sums["feature_changes_untouched"]
        + sums["strata_moves_touched"]
        + sums["strata_moves_untouched"]
        + sums["born"]
        + sums["deleted"]
    )
    return {
        "frames": len(frames),
        "mapped": sum(1 for f in frames if f["status"] == "mapped"),
        "skipped": sum(1 for f in frames if f["status"] == "skipped"),
        "transitions": len(diffs),
        "budget_tally": dict(sorted(tally.items())),
        **sums,
        "movement": moves,
        "ripple_share": (
            (sums["feature_changes_untouched"] + sums["strata_moves_untouched"]) / moves
            if moves
            else 0.0
        ),
        "ripple_clock_share": (sums["ripple_clock"] / moves if moves else 0.0),
        "ripple_rank_share": (sums["ripple_rank"] / moves if moves else 0.0),
        "edit_share": (
            (sums["feature_changes_touched"] + sums["strata_moves_touched"]) / moves
            if moves
            else 0.0
        ),
        "structural_share": ((sums["born"] + sums["deleted"]) / moves if moves else 0.0),
    }


def render_report(m: dict[str, Any]) -> str:
    t = m["totals"]
    r = m["repo"]
    rows = []
    for f in m["frames"]:
        d = f.get("diff")
        if f["status"] == "skipped":
            rows.append(
                f"| {f['index']} | {f['sha'][:8]} | {f['as_of'][:10]} | {f['commit_count']} | {f['population']} | skipped: {f['reason']} | | | | | | |"
            )
            continue
        if not d:
            rows.append(
                f"| {f['index']} | {f['sha'][:8]} | {f['as_of'][:10]} | {f['commit_count']} | {f['population']} | — | | | | | | |"
            )
            continue
        verdict = d["budget_verdict"] + (f" ({d['budget_reason']})" if d["budget_reason"] else "")
        rows.append(
            f"| {f['index']} | {f['sha'][:8]} | {f['as_of'][:10]} | {f['commit_count']} | {f['population']} | "
            f"{d['commits_between']} | {d['born']}/{d['deleted']} | {d['touched']} ({d['touched_frac']:.2f}) | "
            f"{d['feature_changes_touched']}+{d['strata_moves_touched']} | "
            f"{d['feature_changes_untouched']}+{d['strata_moves_untouched']} ({d['ripple_clock']}/{d['ripple_rank']}) | "
            f"{d['untouched_churn']:.3f} / {d['untouched_strata_frac']:.3f} | {verdict} |"
        )
    tally = ", ".join(f"{k} × {v}" for k, v in t["budget_tally"].items()) or "none"
    ov = ", ".join(f"{o['name']} {o['version']}" for o in m["overlays"]) or "none"
    counts_hdr = sorted({k for f in m["frames"] for k in (f.get("feature_counts") or {})})
    clock_feats = (
        ", ".join(sorted(k for k, v in m["feature_kinds"].items() if v == "clock")) or "none"
    )
    count_rows = []
    for f in m["frames"]:
        fc = f.get("feature_counts") or {}
        count_rows.append(
            f"| {f['index']} | " + " | ".join(str(fc.get(k, "")) for k in counts_hdr) + " |"
        )
    return f"""# Time-lapse — {r["name"]}

*Trunk (first-parent) of {r["trunk_length"]} commits, HEAD `{r["head_sha"][:12]}`; {t["frames"]} frames ({t["mapped"]} mapped, {t["skipped"]} skipped), geometry `{m["geometry"]}`, ruleset {m["ruleset"]["name"]} {m["ruleset"]["version"]} (profile {m["ruleset"]["profile"]}), overlays: {ov}. Gate: `validation.json` at HEAD (substrate fingerprint `{(m["gate"]["substrate_config_fingerprint"] or "")[:12]}`, validated {m["gate"]["validated_at"]}) governs every frame — see limitations. Budget: D-018, judged over the untouched population; K between frames is far above the K = 5 it was pinned at, so an over-budget frame here is ripple accumulated over K, not the per-edit reading. Spec: `time-lapse-spec.md`.*

## Frames

| # | sha | as of | commits | population | K | born/del | touched (frac) | edits (feat+strata) | ripple (feat+strata) (clock/rank) | untouched churn / strata | budget |
|---|---|---|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

*edits* = feature changes and strata moves on nodes the intervening commits edited (the skeleton reporting the edit); *ripple* = the same on nodes they did not edit, split into *clock* (features over clock-relative signals — {clock_feats} — and age-geometry strata: the skeleton reporting time) and *rank* (features over rank-only signals and layer strata: the percentile or the layer moved under a node nobody touched — jitter); *born/del* = structural change. The three together are the movement between frames.

## Decomposition of movement over the history

| | count | share |
|---|---|---|
| edits (touched nodes) | {t["feature_changes_touched"] + t["strata_moves_touched"]} | {t["edit_share"]:.2f} |
| ripple (untouched nodes) | {t["feature_changes_untouched"] + t["strata_moves_untouched"]} | {t["ripple_share"]:.2f} |
| &nbsp;&nbsp;of which clock (time reported) | {t["ripple_clock"]} | {t["ripple_clock_share"]:.2f} |
| &nbsp;&nbsp;of which rank (jitter) | {t["ripple_rank"]} | {t["ripple_rank_share"]:.2f} |
| structural (born + deleted) | {t["born"] + t["deleted"]} | {t["structural_share"]:.2f} |
| **movement** | **{t["movement"]}** | over {t["transitions"]} transitions, {t["commits_between"]} commits |

Budget tally across transitions: {tally}.

## Feature counts per frame

| # | {" | ".join(counts_hdr)} |
|---|{"---|" * len(counts_hdr)}
{chr(10).join(count_rows)}

## Limitations (time-lapse spec §6)

1. HEAD's gate governs every frame: an early frame shows what HEAD's licensed structure looked like then, not what was licensed then.
2. Percentiles are re-ranked per frame; a node keeps a percentile feature by keeping its rank, not its value.
3. Rooms are laid out per frame; no tweening. Identity across frames is carried by the diff through renames.
4. Checkpoints are trunk commits; the history each carries includes side branches merged before it.
"""


def render_page(m: dict[str, Any], out_dir: Path) -> str:
    """One page, every mapped frame's SVG inline, a scrubber, overlay toggles across frames."""
    name = escape(m["repo"]["name"])
    frames_html = []
    captions = []
    for f in m["frames"]:
        if f["status"] != "mapped":
            continue
        svg = (out_dir / f"{f['stem']}.cutaway.svg").read_text(encoding="utf-8")
        d = f.get("diff")
        cap = f"frame {f['index']} · {escape(f['sha'][:8])} · {escape(f['as_of'][:10])} · {f['commit_count']} commits · {f['population']} rooms"
        if d:
            cap += (
                f" · vs previous: K={d['commits_between']}, born {d['born']}, deleted {d['deleted']}, "
                f"ripple churn {d['untouched_churn']:.3f} / strata {d['untouched_strata_frac']:.3f} → {escape(d['budget_verdict'])}"
                + (f" ({escape(d['budget_reason'])})" if d["budget_reason"] else "")
            )
        captions.append(cap)
        frames_html.append(f'<div class="frame" hidden>{svg}</div>')
    toggles = "".join(
        f'<label><input type="checkbox" checked data-target="overlay-{i}"> {escape(o["profile"])} overlay</label>'
        for i, o in enumerate(m["overlays"])
    )
    n = len(frames_html)
    caps_json = json.dumps(captions, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{name} — time-lapse</title>
<style>
body{{margin:0;background:#e9e6df;color:#26221d;font-family:ui-monospace,Menlo,monospace;font-size:13px}}
.bar{{position:sticky;top:0;background:#faf8f3;border-bottom:1px solid #c9c2b4;padding:8px 16px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}}
.bar b{{font-weight:600}} label{{cursor:pointer}} button{{font:inherit}} input[type=range]{{width:min(420px,50vw)}}
.cap{{padding:6px 16px;color:#4a443b;background:#f3f0e9;border-bottom:1px solid #d8d2c5}}
.sheet{{overflow-x:auto;padding:8px}} .frame[hidden]{{display:none}}
</style></head><body>
<div class="bar"><b>{name}</b> <span>time-lapse · {n} frames · geometry {escape(m["geometry"])}</span>
<button id="prev">◀</button><input id="scrub" type="range" min="0" max="{max(n - 1, 0)}" value="{max(n - 1, 0)}"><button id="next">▶</button>
<span>base profile: {escape(m["ruleset"]["profile"])} (always on)</span>{toggles}</div>
<div class="cap" id="cap"></div>
<div class="sheet">{"".join(frames_html)}</div>
<script>
const caps = {caps_json};
const frames = Array.from(document.querySelectorAll('.frame'));
const scrub = document.getElementById('scrub');
function show(i) {{ i = Math.max(0, Math.min(frames.length - 1, i)); frames.forEach((f, j) => f.hidden = j !== i);
  scrub.value = i; document.getElementById('cap').textContent = caps[i] || ''; }}
scrub.addEventListener('input', () => show(+scrub.value));
document.getElementById('prev').addEventListener('click', () => show(+scrub.value - 1));
document.getElementById('next').addEventListener('click', () => show(+scrub.value + 1));
document.addEventListener('keydown', e => {{ if (e.key === 'ArrowLeft') show(+scrub.value - 1); if (e.key === 'ArrowRight') show(+scrub.value + 1); }});
document.querySelectorAll('input[data-target]').forEach(cb => cb.addEventListener('change', () => {{
  document.querySelectorAll('g[id="' + cb.dataset.target + '"]').forEach(g => g.style.display = cb.checked ? '' : 'none');
}}));
show(frames.length - 1);
</script></body></html>
"""
