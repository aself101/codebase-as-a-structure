"""End-to-end invariants on the scripted synthetic repository (conftest.scripted_repo):
determinism (repo-substrate-spec §3), the node-set invariant and orphans (§5),
rename following incl. path reuse (§5; 2026-09-04 audit), classification (§7),
and --truncate-at (§8). One invariant per test so a failure names what broke."""

from __future__ import annotations

import json

import pytest
from conftest import run_extract

from repo_substrate.config import IndexWeights, SubstrateConfig


@pytest.fixture
def sub(scripted_repo, small_cfg, tmp_path):
    repo, shas = scripted_repo
    return run_extract(repo, small_cfg, tmp_path), repo, shas


def _node(sub, path):
    return next(n for n in sub["nodes"] if n["id"] == path)


def test_rerun_is_byte_identical_modulo_extracted_at(scripted_repo, small_cfg, tmp_path):
    repo, _ = scripted_repo
    a = run_extract(repo, small_cfg, tmp_path)
    b = run_extract(repo, small_cfg, tmp_path)
    a.pop("extracted_at"); b.pop("extracted_at")
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_node_set_is_head_inventory(sub):
    s, _, _ = sub
    ids = {n["id"] for n in s["nodes"]}
    assert "src/gone.js" not in ids          # deleted before HEAD: history but not a node (§5)
    assert {"src/f0.js", "src/f1.js", "src/f2.js", "src/f3.js", "src/renamed.js", "src/old.js",
            "src/side.js", "src/merge_only.js"} <= ids


def test_merge_only_file_is_an_orphan_defect_signal(sub):
    s, _, _ = sub
    assert s["summary"]["orphan_nodes"] == 1
    assert s["caveats"]["orphan_nodes"] == ["src/merge_only.js"]
    n = _node(s, "src/merge_only.js")
    assert n["metrics"]["history_missing"] is True
    assert n["metrics"]["commit_count"] is None and n["metrics"]["size_loc"] == 1
    assert n["derived"]["indices"] is None   # excluded from the population, never indexed


def test_rename_followed_age_and_counts(sub):
    s, _, _ = sub
    renamed = _node(s, "src/renamed.js")
    assert renamed["metrics"]["commit_count"] == 2   # add + rename
    assert renamed["metrics"]["fix_count"] == 0
    assert renamed["metrics"]["introduced_idx"] == 1
    assert s["renames"] == {}                         # the alias for old.js was broken by the reuse below


def test_path_reuse_after_rename_starts_a_fresh_lineage(sub):
    """x→y then a new ADD at x must not inherit y's history (audit 2026-09-04)."""
    s, _, _ = sub
    old = _node(s, "src/old.js")
    assert old["metrics"]["commit_count"] == 2       # reuse add + fix
    assert old["metrics"]["fix_count"] == 1
    assert old["metrics"]["introduced_idx"] == 3
    renamed = _node(s, "src/renamed.js")
    assert renamed["metrics"]["fix_count"] == 0      # the fix did NOT land on the old lineage


def test_rename_onto_a_reused_name(make_repo, small_cfg, tmp_path):
    """x→y, then z→x, then a fix to the new x: reproduced by the audit as landing on y."""
    r = make_repo("reuse")
    r.write("x.js", "1\n"); r.commit("feat: x")
    r.git("mv", "x.js", "y.js"); r.commit("refactor: x -> y")
    r.write("z.js", "2\n"); r.commit("feat: z")
    r.git("mv", "z.js", "x.js"); r.commit("refactor: z -> x")
    r.write("x.js", "3\n"); r.commit("fix: new x")
    s = run_extract(r, small_cfg, tmp_path)
    y = _node(s, "y.js"); x = _node(s, "x.js")
    assert (y["metrics"]["commit_count"], y["metrics"]["fix_count"]) == (2, 0)
    assert (x["metrics"]["commit_count"], x["metrics"]["fix_count"]) == (3, 1)
    assert s["renames"] == {"z.js": "x.js"}          # the stale x→y alias was broken


def test_timeline_classification_and_order(sub):
    s, _, shas = sub
    types = [c["type"] for c in s["timeline"]]
    assert types == ["feat", "feat", "refactor", "feat", "fix", "fix", "chore", "chore", "feat", "chore", "merge", "fix"]
    assert [c["sha"] for c in s["timeline"]] == shas   # (ts, sha) order == scripted order
    assert s["repo"]["root_commit_sha"] == shas[0]


def test_graph_absent_degrades_load_and_reinforcement(sub):
    s, _, _ = sub
    assert s["summary"]["graph_available"] is False and s["summary"]["graph_degraded"] is True
    for n in s["nodes"]:
        idx = n["derived"]["indices"]
        if idx is None:
            continue
        assert idx["load_index_degraded"] is True
        assert idx["reinforcement_index"] is None and idx["reinforcement_index_degraded"] is True


def test_truncate_at_sees_only_training_window(scripted_repo, small_cfg, tmp_path):
    repo, shas = scripted_repo
    t = run_extract(repo, small_cfg, tmp_path, truncate_at=shas[6])   # just after "chore: add temp"
    assert t["repo"]["head_sha"] == shas[6] and t["repo"]["truncated_at"] == shas[6]
    assert t["summary"]["commit_count"] == 7
    assert "src/gone.js" in {n["id"] for n in t["nodes"]}          # alive at the split
    assert "src/side.js" not in {n["id"] for n in t["nodes"]}      # born after it


def test_config_validate_error_paths():
    with pytest.raises(ValueError, match="sum to"):
        SubstrateConfig(weights=IndexWeights(load_index={"fan_in_nonzero": 0.6, "centrality": 0.6})).validate()
    with pytest.raises(ValueError, match="unknown inputs"):
        SubstrateConfig(weights=IndexWeights(load_index={"fan_in_nonzero": 0.5, "bogus": 0.5})).validate()
    with pytest.raises(ValueError, match="n_min"):
        SubstrateConfig(n_min=1).validate()
    with pytest.raises(ValueError, match="recent_window_frac"):
        SubstrateConfig(recent_window_frac=1.5).validate()


def test_non_ascii_path_survives_c_locale(make_repo, small_cfg, tmp_path, monkeypatch):
    monkeypatch.setenv("LC_ALL", "C")
    monkeypatch.setenv("LANG", "C")
    r = make_repo("uni")
    r.write("src/café.js", "1\n"); r.commit("feat: café")
    r.write("src/b.js", "2\n"); r.commit("feat: b")
    s = run_extract(r, small_cfg, tmp_path)
    assert "src/café.js" in {n["id"] for n in s["nodes"]}
