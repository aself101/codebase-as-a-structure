"""Unit tests for the validation gate's pure parts (validation-spec §3.6, §2.4, §3.8)."""

from __future__ import annotations

import pytest

from repo_substrate.validation.asserted import parse_blind_ranking
from repo_substrate.validation.config import GROUNDING, PREDICTIVE_SIGNALS
from repo_substrate.validation.stats import (
    average_precision,
    base_rate,
    bootstrap_ci,
    kendall_tau_b,
    permutation_p,
    precision_recall_at_k,
    roc_auc,
)
from repo_substrate.validation.tune import compositions


def test_roc_auc_and_ties():
    assert roc_auc([0.9, 0.8, 0.2, 0.1], [1, 1, 0, 0]) == pytest.approx(1.0)
    assert roc_auc([0.1, 0.2, 0.8, 0.9], [1, 1, 0, 0]) == pytest.approx(0.0)
    assert roc_auc([0.5, 0.5, 0.5, 0.5], [1, 0, 1, 0]) == pytest.approx(0.5)  # all tied → chance
    assert roc_auc([1, 2, 3], [0, 0, 0]) != roc_auc(
        [1, 2, 3], [0, 0, 0]
    )  # NaN when a class is empty


def test_average_precision_tie_grouping():
    # perfect ranking
    assert average_precision([0.9, 0.8, 0.1], [1, 1, 0]) == pytest.approx(1.0)
    # a tied block: positives in the block are credited at the block's end, so ordering inside cannot inflate
    ap = average_precision([0.5, 0.5, 0.1], [1, 0, 0])
    assert ap == pytest.approx(0.5)
    assert base_rate([1, 0, 0, 1]) == 0.5


def test_precision_at_k_tie_break_by_id():
    scores, labels, ids = [0.5, 0.5, 0.5], [1, 0, 0], ["b", "a", "c"]
    p, r = precision_recall_at_k(scores, labels, ids, 1)  # 'a' wins the tie → not the positive
    assert p == 0.0 and r == 0.0
    p, r = precision_recall_at_k(scores, labels, ids, 2)
    assert p == 0.5 and r == 1.0


def test_kendall_bootstrap_permutation_deterministic():
    x = [float(i) for i in range(40)]
    y = [float(i + (3 if i % 5 == 0 else 0)) for i in range(40)]
    t = kendall_tau_b(x, y)
    assert 0.8 < t <= 1.0
    lo1, hi1 = bootstrap_ci(x, y, kendall_tau_b, 200, seed=7)
    lo2, hi2 = bootstrap_ci(x, y, kendall_tau_b, 200, seed=7)
    assert (lo1, hi1) == (lo2, hi2) and lo1 <= t <= hi1
    assert permutation_p(x, y, kendall_tau_b, 200, seed=7) < 0.05


def test_parse_blind_ranking():
    text = """# x
## 1. Load-bearing
1. `src/a.ts`
2. src/b.ts — comment stays out of the path? no: keep whole line
3.
## 2. Next
1. `src/c.ts`
"""
    lists = parse_blind_ranking(text)
    assert lists[1][0] == "src/a.ts"
    assert lists[2] == ["src/c.ts"]
    assert len(lists[1]) == 2


def test_grounding_taxonomy_is_closed():
    assert set(PREDICTIVE_SIGNALS) == {"bug_pressure_index", "change_pressure_index"}
    for sig, g in GROUNDING.items():
        assert g["class"] in ("G1", "G2", "G3", "G4"), sig
        if g["class"] == "G4":
            for i in g["inputs"]:
                assert i in GROUNDING, (sig, i)
                assert GROUNDING[i]["class"] != "G4" or i != sig
        if g["class"] in ("G2", "G3"):
            assert g["counterpart"]


def test_compositions_grid_sums_to_one():
    grid = compositions(["a", "b", "c"], 0.5)
    assert len(grid) == 6
    for w in grid:
        assert sum(w.values()) == pytest.approx(1.0)
    assert {"a": 1.0, "b": 0.0, "c": 0.0} in grid
