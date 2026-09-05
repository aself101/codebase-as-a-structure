"""Phase 1 time-lapse (time-lapse-spec.md, D-021) on the scripted repository."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from repo_substrate.mapper import load_ruleset
from repo_substrate.timelapse import TimelapseError, choose_checkpoints, run_timelapse, trunk
from repo_substrate.validation.substrates import SubstrateCache

RULESET = Path(__file__).resolve().parents[1] / "rulesets" / "maintainability.toml"
ONBOARDING = RULESET.parent / "onboarding.toml"


def _validation(cache: SubstrateCache, *rulesets) -> dict:
    return {
        "validation_config_fingerprint": "v" * 64,
        "substrate_config_fingerprint": cache.fingerprint,
        "validated_at": "2026-09-05T00:00:00+00:00",
        "signals": {
            s: {"status": "asserted"} for rs in rulesets for f in rs.features for s in f.signals
        },
    }


def test_choose_checkpoints_schedules():
    assert choose_checkpoints(10, frames=4) == [0, 3, 6, 9]
    assert choose_checkpoints(10, frames=1) == [9]
    assert choose_checkpoints(10, frames=50) == list(range(10))  # never more than the trunk
    assert choose_checkpoints(10, every=4) == [1, 5, 9]  # HEAD always last
    assert choose_checkpoints(1, frames=3) == [0]
    with pytest.raises(TimelapseError):
        choose_checkpoints(10)
    with pytest.raises(TimelapseError):
        choose_checkpoints(10, frames=2, every=2)
    with pytest.raises(TimelapseError):
        choose_checkpoints(0, frames=2)


def test_timelapse_on_scripted_repo(scripted_repo, small_cfg, tmp_path):
    repo, _ = scripted_repo
    line = trunk(repo.path)
    assert line[-1] == repo.git("rev-parse", "HEAD").strip()
    cache = SubstrateCache(tmp_path / "cache", small_cfg, None, tmp_path, 2)
    base, ov = load_ruleset(RULESET), load_ruleset(ONBOARDING)
    val = _validation(cache, base, ov)
    cps = choose_checkpoints(len(line), frames=3)
    out = tmp_path / "tl"
    m = run_timelapse(repo.path, cache, val, base, (ov,), "age", cps, out, {"frames": 3})
    frames = m["frames"]
    assert [f["trunk_index"] for f in frames] == cps
    assert frames[-1]["sha"] == line[-1] and frames[-1]["status"] == "mapped"
    mapped = [f for f in frames if f["status"] == "mapped"]
    assert mapped and mapped[0]["diff"] is None
    # every later mapped frame is diffed against the previous mapped frame, skipped frames or not
    for f in mapped[1:]:
        d = f["diff"]
        assert d["commits_between"] >= 1 and d["budget_verdict"] in (
            "within_budget",
            "over_budget",
            "untested",
        )
        assert (out / f"{f['stem']}.diff.json").exists()
        assert f["change_stem"] == f["stem"] and (out / f"{f['stem']}.change.svg").exists()
    for f in mapped:
        assert (out / f"{f['stem']}.skeleton.json").exists()
        assert (out / f"{f['stem']}.cutaway.svg").read_text(encoding="utf-8").startswith("<svg")
        assert f["as_of"] <= frames[-1]["as_of"]
    # commit counts grow along the trunk: each frame's history is a prefix of the next's
    counts = [f["commit_count"] for f in frames]
    assert counts == sorted(counts)
    t = m["totals"]
    assert t["frames"] == len(cps) and t["mapped"] + t["skipped"] == t["frames"]
    assert (
        abs(
            t["edit_share"]
            + t["ripple_share"]
            + t["structural_share"]
            - (1.0 if t["movement"] else 0.0)
        )
        < 1e-9
    )
    # outputs: manifest, report, page — and the page carries every mapped frame and the overlay toggle
    manifest = json.loads((out / "frames.json").read_text(encoding="utf-8"))
    assert manifest["gate"]["substrate_config_fingerprint"] == cache.fingerprint
    page = (out / "timelapse.html").read_text(encoding="utf-8")
    assert page.count('class="frame"') == len(mapped) and 'data-target="overlay-0"' in page
    report = (out / "timelapse.md").read_text(encoding="utf-8")
    assert "Decomposition of movement" in report and "HEAD's gate governs every frame" in report


def test_timelapse_is_deterministic_over_the_cache(scripted_repo, small_cfg, tmp_path):
    repo, _ = scripted_repo
    cache = SubstrateCache(tmp_path / "cache", small_cfg, None, tmp_path, 2)
    base = load_ruleset(RULESET)
    val = _validation(cache, base)
    cps = choose_checkpoints(len(trunk(repo.path)), every=4)
    a = run_timelapse(repo.path, cache, val, base, (), "layer", cps, tmp_path / "a")
    b = run_timelapse(repo.path, cache, val, base, (), "layer", cps, tmp_path / "b")
    assert a == b
    assert (tmp_path / "a" / "timelapse.md").read_bytes() == (
        tmp_path / "b" / "timelapse.md"
    ).read_bytes()


def test_timelapse_refuses_a_frame_under_a_foreign_gate(scripted_repo, small_cfg, tmp_path):
    repo, _ = scripted_repo
    cache = SubstrateCache(tmp_path / "cache", small_cfg, None, tmp_path, 2)
    base = load_ruleset(RULESET)
    val = {**_validation(cache, base), "substrate_config_fingerprint": "f" * 64}
    with pytest.raises(TimelapseError, match="fingerprint"):
        run_timelapse(
            repo.path, cache, val, base, (), "age", [len(trunk(repo.path)) - 1], tmp_path / "x"
        )
