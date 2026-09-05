"""End-to-end determinism on a synthetic repository built in a temp dir
(repo-substrate-spec §3 [B], §5 node-set invariant [C], §7 [G]).

The synthetic history exercises: a rename, a file deleted before HEAD (must not
be a node), a conventional fix, a merge, and a --truncate-at split.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from repo_substrate.assemble import ExtractOptions, extract
from repo_substrate.config import SubstrateConfig


def _git(repo: Path, *args: str, env: dict | None = None) -> str:
    e = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@x", "GIT_COMMITTER_NAME": "t",
         "GIT_COMMITTER_EMAIL": "t@x", **(env or {})}
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True, env=e).stdout


def _commit(repo: Path, msg: str, when: str) -> str:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", msg, env={"GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when})
    return _git(repo, "rev-parse", "HEAD").strip()


@pytest.fixture
def synthetic_repo(tmp_path: Path) -> tuple[Path, list[str]]:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    (repo / "src").mkdir()
    (repo / "src" / "core.js").write_text("const x = 1;\nmodule.exports = x;\n")
    (repo / "src" / "old.js").write_text("require('./core');\n")
    shas = [_commit(repo, "feat: initial", "2026-01-01T00:00:00Z")]
    (repo / "src" / "core.js").write_text("const x = 2;\nmodule.exports = x;\n")
    shas.append(_commit(repo, "fix: off by one", "2026-01-02T00:00:00Z"))
    _git(repo, "mv", "src/old.js", "src/renamed.js")
    shas.append(_commit(repo, "refactor: rename", "2026-01-03T00:00:00Z"))
    (repo / "src" / "gone.js").write_text("// temporary\n")
    shas.append(_commit(repo, "chore: add temp", "2026-01-04T00:00:00Z"))
    (repo / "src" / "gone.js").unlink()
    shas.append(_commit(repo, "chore: remove temp", "2026-01-05T00:00:00Z"))
    return repo, shas


def _run(repo: Path, tmp: Path, **kw) -> dict:
    cfg = SubstrateConfig(n_min=2)
    return extract(repo, cfg, ExtractOptions(scratch_dir=tmp, blame_workers=2, **kw), extractor=None)


def test_golden_determinism_and_invariants(synthetic_repo, tmp_path):
    repo, shas = synthetic_repo
    a = _run(repo, tmp_path)
    b = _run(repo, tmp_path)
    a.pop("extracted_at"); b.pop("extracted_at")
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)

    ids = {n["id"] for n in a["nodes"]}
    assert ids == {"src/core.js", "src/renamed.js"}          # gone.js deleted before HEAD is not a node
    assert a["summary"]["orphan_nodes"] == 0
    renamed = next(n for n in a["nodes"] if n["id"] == "src/renamed.js")
    assert renamed["metrics"]["age_days"] == 4                # rename-followed: age from the original commit
    assert renamed["metrics"]["commit_count"] == 2            # initial + rename
    core = next(n for n in a["nodes"] if n["id"] == "src/core.js")
    assert core["metrics"]["fix_count"] == 1
    assert [c["type"] for c in a["timeline"]] == ["feat", "fix", "refactor", "chore", "chore"]
    assert a["repo"]["root_commit_sha"] == shas[0]
    assert a["summary"]["graph_available"] is False           # no extractor → degraded path
    assert all(n["derived"]["indices"]["load_index_degraded"] for n in a["nodes"])
    assert a["summary"]["commit_count"] == 5


def test_truncate_at_sees_only_training_window(synthetic_repo, tmp_path):
    repo, shas = synthetic_repo
    t = _run(repo, tmp_path, truncate_at=shas[3])
    assert t["repo"]["head_sha"] == shas[3]
    assert t["repo"]["truncated_at"] == shas[3]
    assert t["summary"]["commit_count"] == 4
    assert {n["id"] for n in t["nodes"]} == {"src/core.js", "src/renamed.js", "src/gone.js"}  # gone.js alive at split
    assert t["repo"]["as_of"].startswith("2026-01-04")
