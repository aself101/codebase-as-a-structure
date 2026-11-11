"""The window page (window-page-spec.md, D-083): what differed between two commits.

A page about ONE pair of commits, rendered from one or two skeleton diffs of that pair (one
per geometry) and from nothing else — as the brief is rendered from one skeleton. Every
line is an event in that window: an unedited room whose predicate term changed outcome, a
row whose membership differs, a band that differs, the gate's budget arithmetic on the
pair. Nothing on it is a property of a room, a row, a ruleset or the repository; the page
adds no grade and quotes the gate's token as the gate's.

Two rules shape the code. (1) No fixed text names a mechanism: the page prints four
numbers and two comparisons per changed term and leaves "why" unsaid, because on the same
day this was written a cause was read off one side of a two-sided comparison three times
(D-082 F4, the first draft's two phrases, the clock line). (2) Each denominator names its
unit, and the words in `BANNED_WORDS` do not occur in fixed text. Both are held by tests.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .mapper.diff import CLOCK_SIGNALS
from .mapper.engine import _cmp
from .mapper.ruleset import parse_predicate

# 0.2.0 (the first seat, tracker run 73): the gate's token has a stated subject (the map, not
# the code); no "HEAD"; comparison cells are the arithmetic itself and read alone when pasted;
# "exited", not "left"; the features reading is stated once, bands per geometry; band lines
# carry their values; a clock term is glossed and its values carry their unit; a row's edited
# and unedited counts sit together; the crossings sentence says what it does not enumerate.
WINDOW_PAGE_VERSION = "0.2.0"

# words that turn an event into a property or a grade (spec §5); the gate's token and the
# room paths are quoted data, not fixed text, and are not scanned
BANNED_WORDS = ("stability", "stable", "unstable", "settled", "flicker", "verdict", "floor")
# words that name a mechanism (spec §11.1)
MECHANISM_WORDS = ("because", "due to", "moves with", "caused", "pushed", "evicted", "drift")

SCOPE_TEXT = (
    "One pair of commits. Each event below is between them. "
    "Another pair of commits reads differently."
)
ORIGIN_TEXT = {
    "gate": (
        "the pair the gate perturbs: the commit the gate was run at and the commit {k} timeline "
        "commits before it; chosen for the gate's test, not for this page"
    ),
    "caller": "a pair chosen by whoever ran this command",
}
ROOM_NOTE = "in no commit's recorded changes in the window"
UNDER_TABLE_TEXT = (
    "Each side's cutoff is computed over that commit's rooms that have a value, of "
    "{earlier} rooms earlier and {later} later, this room's included. The two comparisons "
    "are arithmetic on the four numbers beside them; neither names a cause. The rows column "
    "counts the rooms that entered and exited each row; it does not say which of them, if "
    "any, bears on the line it sits in."
)
CROSSINGS_LIMIT_TEXT = (
    "Only rooms that exited or entered a row are listed: a term that changed outcome while "
    "the room stayed in or out of its row is not on this page (the diff carries no evidence for it)."
)
SUBJECT_TEXT = (
    "What the gate's budget bounds: how far this tool's map differs between two commits for "
    "rooms that are in no commit's recorded changes. It is a check on the map. It is not a "
    "reading of the code, of the repository, or of any room named on this page."
)
CLOCK_GLOSS = (
    "A clock row's term is measured from the date of the snapshot, so every room's value on "
    "it differs between two commits made on different dates."
)
QUALIFIER_TEXT = (
    "A reading of this one window (mapper spec §7 Q3). This page does not read whether "
    "another window of this repository reads the same. The same number of crossings reads "
    "differently on a different number of rooms, so the token does not rank repositories."
)
NOT_COUNTED_CLOCK = "not counted in the gate's reading"
NOT_COUNTED_EXCLUDED = "excluded from the diagnosis; not counted in the gate's reading"
OPERAND_WORDS = {"features": "features", "floors": "bands"}
ATTRIBUTION_WORDS = {
    "band_only": "the same raw {raw} on both sides",
    "raw_depth_changed": "a different raw depth",
    "raw_value_changed": "a different raw value",
    "unknown": "raw value not recorded",
}
RAW_WORD = {"layer": "depth", "age": "value"}
NAMED_MAX = 3

REQUIRED = ("identity", "rooms", "per_decorative_feature", "degraded_marks")


class WindowError(ValueError):
    pass


def _num(v: Any) -> str:
    if v is None:
        return "not recorded"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, int):
        return str(v)
    return f"{float(v):.6g}"


def _named(rooms: list[str]) -> str:
    if not rooms:
        return "none"
    head = "; ".join(rooms[:NAMED_MAX])
    return head + (f"; and {len(rooms) - NAMED_MAX} more" if len(rooms) > NAMED_MAX else "")


def _plural(n: int, one: str, many: str | None = None) -> str:
    return f"{n} {one if n == 1 else (many or one + 's')}"


def _check_diff(d: dict[str, Any], name: str) -> None:
    missing = [k for k in REQUIRED if k not in d]
    if missing or "commit_count" not in (d.get("budget") or {}).get("window", {}):
        raise WindowError(
            f"{name}: written before D-083 (no {', '.join(missing) or 'budget.window.commit_count'}); "
            "regenerate it with `substrate skeleton-diff`"
        )
    ident = d["identity"]
    if ident["before"] != ident["after"]:
        diff = next(k for k in ident["before"] if ident["before"][k] != ident["after"].get(k))
        raise WindowError(
            f"{name}: the two sides were mapped under different {diff} "
            f"({ident['before'][diff]!r} vs {ident['after'][diff]!r}); their predicates may differ"
        )


SAME_WINDOW = (
    ("the pair of commits", lambda d: (d["before"]["repo"], d["after"]["repo"])),
    ("identity", lambda d: d["identity"]),
    ("commits_between", lambda d: d["commits_between"]),
    ("touched.nodes", lambda d: d["touched"]["nodes"]),
    ("rooms", lambda d: d["rooms"]),
    ("per_feature", lambda d: d["per_feature"]),
    ("per_decorative_feature", lambda d: d["per_decorative_feature"]),
    (
        "the budget's constants",
        lambda d: {k: v for k, v in d["budget"].items()
                   if k not in ("verdict", "reason", "operands", "fired", "window", "k")},
    ),
)


def _fixed_threshold(term: str) -> bool:
    return parse_predicate(term)[0].percentile is None


def _compare(value: Any, op: str, cutoff: Any) -> bool | None:
    if value is None or cutoff is None:
        return None
    return _cmp(float(value), op, float(cutoff))


def _rows(per_feature: dict[str, Any], touched: set[str], untouched_only_kinds: tuple[str, ...],
          profiles: list[str]) -> list[dict[str, Any]]:
    """One entry per predicate text among features of the given kinds (spec §11.9), a row's
    features named base profile first."""
    by_pred: dict[str, dict[str, Any]] = {}
    order = {p: i for i, p in enumerate(profiles)}
    for name in sorted(per_feature, key=lambda n: (order.get(n.split("/", 1)[0], len(order)), n)):
        pf = per_feature[name]
        if pf["kind"] not in untouched_only_kinds:
            continue
        profile, feature = name.split("/", 1)
        key = pf.get("predicate") or name
        row = by_pred.setdefault(key, {
            "predicate": pf.get("predicate"), "kind": pf["kind"], "members": [], "pf": pf,
        })
        row["members"].append({"feature": feature, "profile": profile})
    out = []
    for row in by_pred.values():
        pf = row.pop("pf")
        feats: dict[str, list[str]] = {}
        for m in row["members"]:
            feats.setdefault(m["feature"], []).append(m["profile"])
        label = " = ".join(f"{f} ({', '.join(ps)})" for f, ps in feats.items())
        added, removed = pf["added"], pf["removed"]
        out.append({
            **row,
            "label": label,
            "rooms_before": pf["rooms_before"],
            "rooms_after": pf["rooms_after"],
            "unedited_left": [n for n in removed if n in pf["untouched_affected_rooms"]],
            "unedited_entered": [n for n in added if n in pf["untouched_affected_rooms"]],
            "edited_entered": len([n for n in added if n in touched]),
            "edited_left": len([n for n in removed if n in touched]),
            "born_entered": pf["born_entered"],
            "deleted_left": pf["deleted_left"],
            "evidence": pf["transition_evidence"],
        })
    return out


def _row_words(row: dict[str, Any], direction: str) -> str:
    parts = []
    if row["edited_entered"]:
        parts.append(f"{_plural(row['edited_entered'], 'edited room')} entered")
    if row["edited_left"]:
        parts.append(f"{_plural(row['edited_left'], 'edited room')} exited")
    if row["born_entered"]:
        parts.append(f"{_plural(len(row['born_entered']), 'room')} only in the later commit entered")
    if row["deleted_left"]:
        parts.append(f"{_plural(len(row['deleted_left']), 'room')} only in the earlier commit exited")
    tail = f": {', '.join(parts)}" if parts else ""
    return f"{direction} {row['label']} ({row['rooms_before']} → {row['rooms_after']} rooms{tail})"


def _lines(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Spec §11.7. One line per (room, term) whose two outcomes are known and differ; the
    not-available and none-changed states are one line per room."""
    lines: dict[tuple[str, str], dict[str, Any]] = {}

    def put(room: str, term: str, row: dict[str, Any], direction: str, **fields: Any) -> None:
        line = lines.setdefault((room, term), {"room": room, "term": term, "rows": [], **fields})
        line["rows"].append({"label": row["label"], "direction": direction,
                             "words": _row_words(row, direction)})

    for row in rows:
        for direction, rooms in (("exited", row["unedited_left"]), ("entered", row["unedited_entered"])):
            for room in rooms:
                ev = row["evidence"].get(room) or {}
                before, after = ev.get("before") or {}, ev.get("after") or {}
                tb, ta = before.get("terms"), after.get("terms")
                if (before.get("availability") != "available" or after.get("availability") != "available"
                        or tb is None or ta is None or [x["term"] for x in tb] != [x["term"] for x in ta]):
                    put(room, "not available", row, direction, state="not_available")
                    continue
                changed = [(x, y) for x, y in zip(tb, ta)
                           if x["passed"] is not None and y["passed"] is not None and x["passed"] != y["passed"]]
                if not changed:
                    if any(x["passed"] is None or y["passed"] is None for x, y in zip(tb, ta)):
                        put(room, "not available", row, direction, state="not_available")
                    else:
                        put(room, "none changed outcome", row, direction, state="none_changed",
                            eligibility={side: {k: s.get(k) for k in
                                                ("diagnostic_eligible", "graph_degraded", "node_load_degraded")}
                                         for side, s in (("before", before), ("after", after))})
                    continue
                for x, y in changed:
                    fixed = _fixed_threshold(x["term"])
                    put(room, x["term"], row, direction, state="compared",
                        signal=x["signal"], operator=x["operator"],
                        term_kind="clock" if x["signal"] in CLOCK_SIGNALS else "rank",
                        fixed_threshold=fixed,
                        value_before=x["value"], value_after=y["value"],
                        cutoff_before=x["threshold"], cutoff_after=y["threshold"],
                        later_value_vs_earlier_cutoff=None if fixed else _compare(y["value"], x["operator"], x["threshold"]),
                        earlier_value_vs_later_cutoff=None if fixed else _compare(x["value"], x["operator"], y["threshold"]))
    return [lines[k] for k in sorted(lines)]


def window_facts(diffs: list[dict[str, Any]], names: list[str], origin: str = "caller",
                 page_file: str | None = None) -> dict[str, Any]:
    if origin not in ORIGIN_TEXT:
        raise WindowError(f"--origin must be one of {', '.join(ORIGIN_TEXT)}")
    if not 1 <= len(diffs) <= 2:
        raise WindowError("a window page reads one or two diffs (one per geometry)")
    for d, n in zip(diffs, names):
        _check_diff(d, n)
    if len(diffs) == 2:
        if diffs[0]["after"]["geometry"] == diffs[1]["after"]["geometry"]:
            raise WindowError(f"both diffs are of the {diffs[0]['after']['geometry']} geometry")
        for label, get in SAME_WINDOW:
            if get(diffs[0]) != get(diffs[1]):
                raise WindowError(f"{names[0]} and {names[1]} are not one window: {label} differs")
    d = diffs[0]
    touched = set(d["touched"]["nodes"])
    win = d["budget"]["window"]
    born, deleted = d["rooms"]["born"], d["rooms"]["deleted"]
    profiles = d["identity"]["after"].get("profiles") or []
    judged_rows = _rows(d["per_feature"], touched, ("rank", "mixed"), profiles)
    clock_rows = _rows(d["per_feature"], touched, ("clock",), profiles)
    k = d["budget"]["k"]

    def strip(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [{a: b for a, b in r.items() if a != "evidence"} for r in rows
                if r["unedited_left"] or r["unedited_entered"]]

    excluded = []
    for name in sorted(d["per_decorative_feature"]):
        pf = d["per_decorative_feature"][name]
        if not pf["untouched_affected_rooms"]:
            continue
        profile, feature = name.split("/", 1)
        excluded.append({
            "label": f"{feature} ({profile})", "predicate": pf["predicate"],
            "rooms_before": pf["rooms_before"], "rooms_after": pf["rooms_after"],
            # D-028 carried to this page: an excluded row's rooms are counted, never named —
            # naming them would hand a reader the salience the exclusion withholds
            "unedited_left": len([n for n in pf["removed"] if n in pf["untouched_affected_rooms"]]),
            "unedited_entered": len([n for n in pf["added"] if n in pf["untouched_affected_rooms"]]),
            "edited_entered": len([n for n in pf["added"] if n in touched]),
            "edited_left": len([n for n in pf["removed"] if n in touched]),
        })
    bands, readings = [], []
    for x in diffs:
        geom = x["after"]["geometry"]
        groups: dict[str, list[dict[str, Any]]] = {}
        for room, e in sorted(x["strata_evidence"].items()):
            if e["untouched"]:
                groups.setdefault(e["attribution"], []).append({
                    "room": room,
                    "band_before": e["before"]["band"], "band_after": e["after"]["band"],
                    "raw_before": e["before"]["raw"], "raw_after": e["after"]["raw"],
                })
        bands.append({"geometry": geom, "moved": sum(len(v) for v in groups.values()),
                      "of": x["untouched"]["n"], "groups": groups})
        b = x["budget"]
        readings.append({
            "geometry": geom, "token": b["verdict"], "reason": b["reason"],
            "fired": None if b["fired"] is None else [OPERAND_WORDS[o] for o in b["fired"]],
            "operands": b["operands"],
        })
    doc: dict[str, Any] = {
        "window_page_version": WINDOW_PAGE_VERSION,
        "page_file": page_file,
        "repo": d["after"]["repo"]["name"],
        "scope": "one window",
        "scope_text": SCOPE_TEXT,
        "origin": origin,
        "origin_text": ORIGIN_TEXT[origin].format(k=k),
        "window": {
            "before_sha": d["before"]["repo"]["head_sha"], "after_sha": d["after"]["repo"]["head_sha"],
            "commits_between": k,
            **{f: win.get(f) for f in ("before_ts", "after_ts", "first_ts", "last_ts", "commit_count")},
        },
        "rooms": {
            "common": d["common_nodes"], "only_later": born, "only_earlier": deleted,
            "edited": d["touched"]["n"], "unedited": d["untouched"]["n"],
            "edited_share": d["touched"]["frac"],
            "earlier": d["common_nodes"] + len(deleted), "later": d["common_nodes"] + len(born),
        },
        "crossings": _lines(judged_rows),
        "clock_rows": strip(clock_rows),
        "clock_crossings": _lines(clock_rows),
        "excluded_rows": excluded,
        "bands": bands,
        "gate_reading": readings,
        "qualifier_text": QUALIFIER_TEXT,
        "subject_text": SUBJECT_TEXT,
        "crossings_limit_text": CROSSINGS_LIMIT_TEXT,
        "not_reported": {"degraded_marks": d["degraded_marks"]},
        "identity": d["identity"]["after"],
        "sources": [{"file": n, "geometry": x["after"]["geometry"],
                     "before_skeleton_hash": x["before"]["skeleton_hash"],
                     "after_skeleton_hash": x["after"]["skeleton_hash"]} for x, n in zip(diffs, names)],
        "units": {
            "crossings": "(room, predicate term) pairs whose outcome differs between the two commits, among rooms in no commit's recorded changes that exited or entered a row; a term that changed outcome without a membership change is not enumerated",
            "gate_reading.operands.features": "(profile, feature, room) assignments of rank and mixed features",
            "gate_reading.operands.floors": "rooms (printed as bands)",
            "rooms.edited_share": "edited rooms / rooms in both commits",
        },
    }
    raw = json.dumps(doc, sort_keys=True, ensure_ascii=False, allow_nan=False).encode("utf-8")
    doc["facts_hash"] = hashlib.sha256(raw).hexdigest()
    return doc


def _date(ts: str | None) -> str:
    return ts if ts else "date not recorded"


DAY_SIGNALS = ("age_days", "last_touched_days", "blame_age_median")


def _unit(line: dict[str, Any]) -> str:
    return " days" if line.get("signal") in DAY_SIGNALS else ""


def _cell(line: dict[str, Any], value_key: str, cutoff_key: str, which: str) -> str:
    """The comparison as its own arithmetic, so a line pasted without its header still reads:
    `0.0128 >= 0.01285`: no. Never "passes"/"fails" (run 73: read as a check's status)."""
    if line.get("fixed_threshold"):
        return "fixed threshold"
    v = line.get(which)
    if v is None:
        return "not available"
    return f"`{_num(line[value_key])} {line['operator']} {_num(line[cutoff_key])}`: {'yes' if v else 'no'}"


TABLE_HEAD = [
    "| window | room | term | value, earlier → later | cutoff, earlier → later | later value against the earlier cutoff (arithmetic only) | earlier value against the later cutoff (arithmetic only) | rows (counts only) |",
    "|---|---|---|---|---|---|---|---|",
]


def _crossing_table(lines: list[dict[str, Any]], win: str) -> list[str]:
    out = list(TABLE_HEAD)
    for ln in lines:
        room = f"{ln['room']} ({ROOM_NOTE})"
        rows = "; ".join(r["words"] for r in ln["rows"])
        if ln["state"] == "not_available":
            out.append(f"| {win} | {room} | not available | not available | not available | not available | not available | {rows} |")
        elif ln["state"] == "none_changed":
            e = ln["eligibility"]
            sides = "; ".join(
                f"{word}: eligible {_flag(e[s]['diagnostic_eligible'])}, graph degraded {_flag(e[s]['graph_degraded'])}, room's load degraded {_flag(e[s]['node_load_degraded'])}"
                for word, s in (("earlier", "before"), ("later", "after")))
            out.append(f"| {win} | {room} | none changed outcome | {sides} | — | — | — | {rows} |")
        else:
            u = _unit(ln)
            cutoff = (f"fixed at {_num(ln['cutoff_before'])}{u}" if ln["fixed_threshold"]
                      else f"cutoff {_num(ln['cutoff_before'])} → {_num(ln['cutoff_after'])}{u}")
            out.append(
                f"| {win} | {room} | `{ln['term']}` | value {_num(ln['value_before'])} → {_num(ln['value_after'])}{u} | {cutoff} | "
                f"{_cell(ln, 'value_after', 'cutoff_before', 'later_value_vs_earlier_cutoff')} | "
                f"{_cell(ln, 'value_before', 'cutoff_after', 'earlier_value_vs_later_cutoff')} | {rows} |")
    return out


def _flag(v: Any) -> str:
    return "not recorded" if v is None else ("yes" if v else "no")


def _membership(row: dict[str, Any]) -> str:
    left, entered = row["unedited_left"], row["unedited_entered"]
    parts = [f"{len(left)} exited ({_named(left)}), {len(entered)} entered ({_named(entered)})"]
    other = f"edited rooms: {row['edited_entered']} entered, {row['edited_left']} exited"
    if row["born_entered"] or row["deleted_left"]:
        other += (f"; rooms only in one commit: {len(row['born_entered'])} entered, "
                  f"{len(row['deleted_left'])} exited")
    return (f"{row['rooms_before']} → {row['rooms_after']} rooms. Rooms {ROOM_NOTE}: {parts[0]}; {other}")


def render_window(f: dict[str, Any]) -> str:
    w, r = f["window"], f["rooms"]
    pair = f"{w['before_sha'][:8]}→{w['after_sha'][:8]}"
    out = [
        f"# {f['repo']} — one window: `{w['before_sha'][:12]}` → `{w['after_sha'][:12]}`",
        "",
        f"**{f['scope_text']}**",
        "",
        (f"The window: `{w['before_sha'][:12]}` ({_date(w['before_ts'])}) → `{w['after_sha'][:12]}` ({_date(w['after_ts'])}); "
        f"{f['origin_text']}. {_plural(w['commits_between'], 'commit')} in the window, the earliest at {_date(w['first_ts'])} "
        f"and the latest at {_date(w['last_ts'])}. {r['common']} rooms are in both commits, {len(r['only_later'])} only in the later "
        f"and {len(r['only_earlier'])} only in the earlier; {r['edited']} of the {r['common']} rooms in both are in some commit's "
        f"recorded changes ({r['edited_share']:.0%} of rooms in both), {r['unedited']} are in none."),
        "",
        "## Crossings",
        "",
    ]
    if f["crossings"]:
        intro = (f"{_plural(len(f['crossings']), 'crossing')}: one line per room and predicate term whose outcome differs between "
                 "the two commits, among rooms in no commit's recorded changes that exited or entered a row the gate's reading counts.")
        out += [intro, ""]
        out += _crossing_table(f["crossings"], pair)
        out += ["", UNDER_TABLE_TEXT.format(earlier=r["earlier"], later=r["later"]), "", f["crossings_limit_text"]]
    else:
        out += ["No room in no commit's recorded changes exited or entered a row the gate's reading counts.", "",
                f["crossings_limit_text"]]
    out += ["", "## Clock rows", "", CLOCK_GLOSS, ""]
    if f["clock_rows"]:
        for row in f["clock_rows"]:
            out.append(f"- **{row['label']}** — {_membership(row)}; {NOT_COUNTED_CLOCK}.")
        out += ["", f"Their crossings, {NOT_COUNTED_CLOCK}:", ""]
        out += _crossing_table(f["clock_crossings"], pair)
    else:
        out.append("No clock row's membership differs among rooms in no commit's recorded changes.")
    out += ["", "## Excluded rows (◌)", ""]
    if f["excluded_rows"]:
        for row in f["excluded_rows"]:
            out.append(
                f"- **◌ {row['label']}** — {row['rooms_before']} → {row['rooms_after']} rooms. Rooms {ROOM_NOTE}: "
                f"{row['unedited_left']} exited, {row['unedited_entered']} entered; edited rooms: "
                f"{row['edited_entered']} entered, {row['edited_left']} exited; "
                f"{NOT_COUNTED_EXCLUDED}. An excluded row's rooms are counted, not named, and no values or cutoffs are printed for it.")
    else:
        out.append("No excluded row's membership differs among rooms in no commit's recorded changes.")
    out += ["", "## Bands", ""]
    for b in f["bands"]:
        raw = RAW_WORD.get(b["geometry"], "value")
        if not b["moved"]:
            out.append(f"- Under the {b['geometry']} geometry, none of the {b['of']} rooms {ROOM_NOTE} changed band.")
            continue
        parts = []
        for attr in ("band_only", "raw_depth_changed", "raw_value_changed", "unknown"):
            rooms = b["groups"].get(attr)
            if rooms:
                named = _named([f"{x['room']}: band {_num(x['band_before'])} → {_num(x['band_after'])}, "
                                f"raw {raw} {_num(x['raw_before'])} → {_num(x['raw_after'])}" for x in rooms])
                parts.append(f"{len(rooms)} with {ATTRIBUTION_WORDS[attr].format(raw=raw)} ({named})")
        out.append(f"- Under the {b['geometry']} geometry, {b['moved']} of the {b['of']} rooms {ROOM_NOTE} changed band: "
                   + "; ".join(parts) + ".")
    out += ["", "## The gate's budget reading on this window", "", f["subject_text"], ""]
    ft = f["gate_reading"][0]["operands"]["features"]  # one window: the same under every geometry (SAME_WINDOW)
    cross = ("crossings not available" if ft["distinct_crossings"] is None
             else _plural(ft["distinct_crossings"], "crossing"))
    same = "the same under each geometry: " if len(f["gate_reading"]) > 1 else ""
    out.append(
        f"- features ({same}rows do not depend on it) — {ft['distinct_rooms']} of the {r['unedited']} rooms {ROOM_NOTE}, {cross}; "
        f"in the gate's unit, {ft['changes']} of {ft['denominator']} `(profile, feature, room)` assignments ({_over(ft, 'assignments')})."
    )
    for g in f["gate_reading"]:
        fl = g["operands"]["floors"]
        out.append(f"- bands, {g['geometry']} geometry — {fl['changes']} of {fl['denominator']} rooms {ROOM_NOTE} ({_over(fl, 'rooms')}).")
    for g in f["gate_reading"]:
        if g["token"] == "untested":
            out.append(f"- the gate's token, {g['geometry']} geometry — not judged by the gate: `{g['reason']}`.")
        else:
            on = f", on {' and '.join(g['fired'])}" if g["fired"] else ""
            out.append(f"- the gate's token, {g['geometry']} geometry — `{g['token']}`{on}.")
    out += ["", f["qualifier_text"], "", "## What this page does not report", ""]
    dm = f["not_reported"]["degraded_marks"]
    out.append(
        f"Marks that are neither diagnostic nor excluded ({dm['before']} in the earlier commit, {dm['after']} in the later); "
        "what differs for edited rooms beyond the counts beside each row; a term that changed outcome without the room "
        "exiting or entering its row; any pair of commits but this one."
    )
    i = f["identity"]
    out += ["", "## Provenance", ""]
    out.append(
        "; ".join(f"`{s['file']}` ({s['geometry']}: skeleton `{s['before_skeleton_hash'][:12]}…` → `{s['after_skeleton_hash'][:12]}…`)"
                  for s in f["sources"])
        + f". Ruleset {i['ruleset']['name']} {i['ruleset']['version']}"
        + "".join(f" + {o['name']} {o['version']}" for o in i["overlays"])
        + f", mapper {i['mapper_version']}, substrate config `{(i['substrate_config_fingerprint'] or '?')[:12]}`, "
        f"gate `{(i['validation_config_fingerprint'] or '?')[:12]}`. Window page {f['window_page_version']}, "
        f"facts `{f['facts_hash'][:12]}…`."
    )
    return "\n".join(out) + "\n"


def _over(op: dict[str, Any], unit: str) -> str:
    if op["fires_at"] is None:
        return f"no {unit} to read"
    return f"{op['fires_at']} or more of {op['denominator']} {unit} is over {op['ceiling']} by the gate's rule"


def run_window(diffs: list[dict[str, Any]], names: list[str], origin: str = "caller",
               page_file: str | None = None) -> dict[str, Any]:
    facts = window_facts(diffs, names, origin, page_file)
    return {"markdown": render_window(facts), "facts": facts}
