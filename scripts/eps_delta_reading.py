"""Read where the signal-level stability thresholds sit against the reference set (D-026 rule, D-033).

    uv run python scripts/eps_delta_reading.py out/validation-k25/validation.json [reports/2026-09-06-m1c/validation.json ...]

For every validation.json given: pool the per-(signal, repo) stability readings — median |Δ| (the eps
operand) and max |Δ| (the delta operand), p95 beside — over every signal that reached the stability test,
and report the reference-set median and p90 of each operand next to the threshold. D-026's rule: a
ceiling must sit between the reference set's median and p90 of the operand at the pinned K, or it
cannot fail (above p90) or cannot pass (below the median). Prints a markdown reading.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from statistics import median


def q(xs: list[float], p: float) -> float:
    xs = sorted(xs)
    if not xs:
        return float("nan")
    i = min(len(xs) - 1, max(0, round(p * (len(xs) - 1))))
    return xs[i]


def read(path: Path) -> dict:
    v = json.loads(path.read_text())
    k = v["validation_config"]["stability_perturbation_k"]
    eps, delta = v["validation_config"]["stability_eps"], v["validation_config"]["stability_delta"]
    rows = []
    for sig, rec in sorted(v["signals"].items()):
        for r in (rec.get("grounding") or {}).get("per_repo", []):
            st = r.get("stability") or {}
            if st.get("median_abs_delta") is None:
                continue
            rows.append(
                (
                    sig,
                    r["name"],
                    st["median_abs_delta"],
                    st.get("p95_abs_delta"),
                    st["max_abs_delta"],
                    st.get("n_compared") or st.get("n"),
                    rec["status"],
                    st.get("passed"),
                    st.get("ripple", "own"),
                    st.get("operand", "max"),
                )
            )
    return {"k": k, "eps": eps, "delta": delta, "rows": rows, "path": str(path)}


def render(d: dict) -> str:
    rows = d["rows"]
    own = [r for r in rows if r[8] == "own"]
    coupled = [r for r in rows if r[8] == "coupled"]
    # D-033: the own signals are the instrument's null check; the bars are placed over the
    # coupled readings, each on its own tail operand (p95), the median operand beside.
    placed = coupled if coupled else rows
    meds = [r[2] for r in placed]
    tails = [(r[3] if r[9] == "p95" else r[4]) for r in placed]
    out = [f"## K = {d['k']} — `{d['path']}`", ""]
    nz = [r for r in own if r[4] > 0]
    out.append(
        f"{len(rows)} (signal, repo) readings reached the stability test: {len(own)} own (null check — "
        f"{len(nz)} read above 0.000{': ' + ', '.join(f'{r[0]}@{r[1]}' for r in nz) if nz else ''}), {len(coupled)} coupled (the bars are placed over these)."
    )
    out.append("")
    out.append(
        "| operand | threshold | reference-set median | p90 | max | verdict under the D-026 rule |"
    )
    out.append("|---|---|---|---|---|---|")
    for name, thr, xs in (
        ("eps over median \\|Δ\\|", d["eps"], meds),
        ("delta over the tail operand", d["delta"], tails),
    ):
        m, p90, mx = median(xs), q(xs, 0.9), max(xs)
        if thr > p90:
            verdict = "above p90 — cannot fail on this set"
        elif thr < m:
            verdict = "below the median — cannot pass on this set"
        else:
            verdict = "between median and p90 — can fail"
        out.append(f"| {name} | {thr:.3f} | {m:.4f} | {p90:.4f} | {mx:.4f} | {verdict} |")
    out.append("")
    out.append("| signal | ripple | repo | median \\|Δ\\| | p95 | max | operand | n | status |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    for sig, repo, med, p95, mx, n, status, passed, ripple, operand in sorted(
        rows, key=lambda r: -(r[3] if r[9] == "p95" else r[4])
    ):
        flag = "" if passed else " **fails**"
        out.append(
            f"| `{sig}` | {ripple} | {repo} | {med:.4f} | {p95 if p95 is None else f'{p95:.4f}'} | {mx:.4f} | {operand} | {n} | {status}{flag} |"
        )
    out.append("")
    return "\n".join(out)


def main() -> int:
    docs = [read(Path(p)) for p in sys.argv[1:]]
    print("# Where eps and delta sit against the reference set\n")
    print(
        "*Operands per (signal, repo): median |Δpercentile| against `stability_eps`, max |Δpercentile| against `stability_delta`, over the untouched population (validation §2.4.1). The D-026 rule: a ceiling sits where it can fail — between the reference set's median and p90 of its operand at the pinned K.*\n"
    )
    for d in docs:
        print(render(d))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
