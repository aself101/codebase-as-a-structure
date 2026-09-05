"""The two import instruments must be able to disagree, or the G2 check is not a
falsifier (validation-spec §2.4.2 retirement criterion; Popper C-2A). This fixture is
built so the naive scanner over-counts (an import-shaped string inside a template
literal) and so `import type` edges exist (which the primary instrument only sees
with pre-compilation deps on). Requires the pinned dependency-cruiser; skipped when absent."""

from __future__ import annotations

from pathlib import Path

import pytest

from repo_substrate.assemble import ExtractOptions, extract
from repo_substrate.cli import TOOLS_DIR
from repo_substrate.config import SubstrateConfig
from repo_substrate.deps import DependencyCruiserExtractor

pytestmark = pytest.mark.skipif(
    not (TOOLS_DIR / "node_modules" / ".bin" / "depcruise").exists(),
    reason="dependency-cruiser not installed",
)


@pytest.fixture
def adversarial(make_repo):
    r = make_repo("adv")
    r.write(
        "tsconfig.json",
        '{"compilerOptions": {"baseUrl": ".", "paths": {"@lib/*": ["src/lib/*"]}}}\n',
    )
    r.write("src/lib/a.ts", "export const a = 1;\nexport type A = number;\n")
    r.write(
        "src/lib/b.ts", "import type { A } from './a';\nexport const b: A = 2;\n"
    )  # type-only import
    r.write("src/c.ts", "import { a } from '@lib/a';\nexport const c = a;\n")  # alias
    r.write(
        "src/lib/d.ts", "export const s = `import x from './a'`;\nexport const d = 4;\n"
    )  # looks like an import, is a string
    r.write("src/e.ts", "export * from './lib/b';\n")  # re-export
    for i in range(30):  # enough nodes to clear n_min
        r.write(f"src/pad/p{i}.ts", f"export const p{i} = {i};\n")
    r.commit("feat: adversarial fixture")
    r.write("src/lib/a.ts", "export const a = 11;\nexport type A = number;\n")
    r.commit("fix: bump a")
    return r


def _run(repo, tmp, pre_comp: bool) -> dict:
    cfg = SubstrateConfig(n_min=2, dep_ts_pre_compilation_deps=pre_comp)
    ex = DependencyCruiserExtractor(TOOLS_DIR, pre_comp)
    return extract(repo.path, cfg, ExtractOptions(scratch_dir=tmp, blame_workers=2), extractor=ex)


def _m(sub, path):
    return next(n for n in sub["nodes"] if n["id"] == path)["metrics"]


def test_instruments_can_disagree_and_type_imports_are_edges(adversarial, tmp_path):
    s = _run(adversarial, tmp_path, pre_comp=True)
    a = _m(s, "src/lib/a.ts")
    # primary (parser): b imports a (type-only, counted with pre-compilation deps) and c imports a via alias → 2
    assert a["fan_in"] == 2
    # scanner (regex): additionally counts the import-shaped string in d.ts → over-counts to 3
    assert a["fan_in_alt"] == 3
    assert s["summary"]["fan_in_instrument_tau"] is not None
    assert _m(s, "src/lib/b.ts")["fan_in"] == 1  # e.ts re-exports b


def test_without_pre_compilation_deps_type_imports_vanish(adversarial, tmp_path):
    """The typeorm finding (D-011) reproduced in miniature: with the flag off, b→a disappears."""
    s = _run(adversarial, tmp_path, pre_comp=False)
    assert _m(s, "src/lib/a.ts")["fan_in"] == 1
    assert _m(s, "src/lib/a.ts")["fan_in_alt"] == 3  # the scanner does not care about erasure


def test_fingerprint_moves_with_the_flag(adversarial, tmp_path):
    a = _run(adversarial, tmp_path, pre_comp=True)["repo"]["config_fingerprint"]
    b = _run(adversarial, tmp_path, pre_comp=False)["repo"]["config_fingerprint"]
    assert a != b
    Path(tmp_path).exists()
