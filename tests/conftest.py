"""Shared fixtures: a synthetic git repository builder with deterministic dates."""

from __future__ import annotations

import os
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from repo_substrate.assemble import ExtractOptions, extract
from repo_substrate.config import SubstrateConfig

T0 = datetime(2026, 1, 1, tzinfo=UTC)


class Repo:
    """Minimal scripted git repo. Every commit gets a strictly increasing author date so the
    (ts, sha) timeline order equals the scripted order."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.n = 0
        path.mkdir()
        self.git("init", "-q", "-b", "main")

    def git(self, *args: str, env: dict | None = None, check: bool = True) -> str:
        e = {
            **os.environ,
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": "t@x",
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@x",
            "LC_ALL": "C.UTF-8",
            **(env or {}),
        }
        return subprocess.run(
            ["git", "-C", str(self.path), *args],
            capture_output=True,
            text=True,
            check=check,
            env=e,
            encoding="utf-8",
        ).stdout

    def write(self, rel: str, text: str) -> None:
        p = self.path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def commit(self, msg: str, add_all: bool = True) -> str:
        self.n += 1
        when = (T0 + timedelta(days=self.n)).isoformat()
        if add_all:
            self.git("add", "-A")
        self.git(
            "commit",
            "-q",
            "--allow-empty",
            "-m",
            msg,
            env={"GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when},
        )
        return self.git("rev-parse", "HEAD").strip()

    def merge(self, branch: str, msg: str, extra: dict[str, str] | None = None) -> str:
        """Merge `branch` with --no-ff; files in `extra` are added inside the merge commit itself
        (the conflict-resolution shape that yields a HEAD file with no non-merge history)."""
        self.n += 1
        when = (T0 + timedelta(days=self.n)).isoformat()
        self.git("merge", "--no-ff", "--no-commit", branch, check=False)
        for rel, text in (extra or {}).items():
            self.write(rel, text)
        self.git("add", "-A")
        self.git(
            "commit", "-q", "-m", msg, env={"GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when}
        )
        return self.git("rev-parse", "HEAD").strip()


@pytest.fixture
def make_repo(tmp_path: Path):
    def _make(name: str = "repo") -> Repo:
        return Repo(tmp_path / name)

    return _make


@pytest.fixture
def small_cfg() -> SubstrateConfig:
    return SubstrateConfig(n_min=2)


def run_extract(repo: Repo, cfg: SubstrateConfig, tmp: Path, **kw) -> dict:
    return extract(
        repo.path, cfg, ExtractOptions(scratch_dir=tmp, blame_workers=2, **kw), extractor=None
    )


@pytest.fixture
def scripted_repo(make_repo) -> tuple[Repo, list[str]]:
    """12 commits, 6 source files under src/, one fix late in history, one rename, one deletion,
    one path-reuse-after-rename, and a merge that introduces a file only in the merge commit."""
    r = make_repo()
    shas = []
    for i in range(4):
        r.write(
            f"src/f{i}.js", f"const x{i} = require('./f{max(i - 1, 0)}');\nmodule.exports = x{i};\n"
        )
    shas.append(r.commit("feat: initial"))
    r.write("src/old.js", "module.exports = 1;\n")
    shas.append(r.commit("feat: add old"))
    r.git("mv", "src/old.js", "src/renamed.js")
    shas.append(r.commit("refactor: rename old -> renamed"))
    r.write("src/old.js", "// brand new file at a reused name\nmodule.exports = 2;\n")
    shas.append(r.commit("feat: reuse the name old.js"))
    r.write("src/old.js", "// fixed\nmodule.exports = 3;\n")
    shas.append(r.commit("fix: the new old.js"))
    r.write("src/f1.js", "const x1 = require('./f0');\nmodule.exports = x1 + 1;\n")
    shas.append(r.commit("fix: f1 off by one"))
    r.write("src/gone.js", "// temporary\n")
    shas.append(r.commit("chore: add temp"))
    (r.path / "src/gone.js").unlink()
    shas.append(r.commit("chore: remove temp"))
    # merge that adds a file only in the merge commit
    r.git("checkout", "-q", "-b", "side")
    r.write("src/side.js", "module.exports = 'side';\n")
    shas.append(r.commit("feat: side branch"))
    r.git("checkout", "-q", "main")
    r.write("src/f2.js", "const x2 = require('./f1');\nmodule.exports = x2 * 2;\n")
    shas.append(r.commit("chore: touch f2 on main"))
    shas.append(
        r.merge(
            "side", "Merge branch 'side'", extra={"src/merge_only.js": "// born in the merge\n"}
        )
    )
    r.write("src/f3.js", "const x3 = require('./f2');\nmodule.exports = x3 - 1;\n")
    shas.append(r.commit("fix: f3 latest"))
    return r, shas
