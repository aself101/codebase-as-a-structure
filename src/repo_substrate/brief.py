"""M3 — the architect brief (C5) with the register lint (`architect-brief-spec.md`, D-027).

Three parts, in the order the anti-horoscope contract wants them:

1. `facts(skeleton, substrate)` — the deterministic facts sheet: everything the brief may
   say, and nothing else. Diagnostic features with their rooms, decorative features by
   count only, the gate's per-signal statuses, position-name disclosures for names that
   imply a consequence, the stance disclosure. A pure function of the skeleton.
2. `generate(facts, ...)` — one call to a model under the condemnation-surveyor stance with
   the register rules in the system prompt. The only non-deterministic step; its
   provenance (model served, request id, facts hash) is written into the brief.
3. `lint(text, facts)` — the deterministic hostile reader. Consequence vocabulary,
   provenance of every citation, numbers, decorative exclusion, disclosure, no building
   label. A brief that fails is written marked FAILED and never passes silently.

The lint is the product; the generator is replaceable (`--draft` lints a hand-written
brief with no model in the path).
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any

BRIEF_VERSION = "0.42.0"  # D-077: pooling stated as composition — the by-wing cell names a package scope of 30 or more rooms holding over twice or under half its share of a feature's rooms (mcp-secure-server: 27 of 27 lit rooms in the library, which holds 65 of 187); scope_composition on the sheet. D-075: a feature too small to place names up to three rooms in the parent cell (eslint toothpick_wing read as lib/cli.js); one imported room is not its own top room; the legend states the inputs a blend's tuning weighted zero (index_zeroed); a tie's lead parent is the first by path; the ◌ line pairs its names; a clock row's far boundary counts its disowned-commit rooms. D-074 (Alex: pair): a feature name the ruleset flags as implying a consequence is paired with its position name in the register's feature cell and the most-positions table ("dark_room · long-untouched room", "◌ crack (excluded) · high edit-pressure node"), so a pasted row carries the position. D-073: an import-graph row counts distinct importing files and the test files among them, the edge sum beside it and named as one (registry's foundation read "importers of these rooms: 466" on a graph of 456 files — 234 files, 91 test files); the top room is a third of the files; the via-importer clause names its most test-imported importer (typeorm toothpick_wing: src/index.ts, 1588). D-072: the stance states the system spec's case in the spec's words (one condition, the long-untouched position, counted) and labels the long-untouched ∩ high-load intersection as the page's own narrowing (D-070) — the eleventh control found the paraphrase credited to the spec named 6 of typeorm's 70; the most-positions table says how many of its rooms sit at the stance's case (eslint: 11 of 12, the eleventh skimmer); a position cell whose quantile word resolved to a value more than twice its nominal share reaches says what it resolved to (eslint: p75 on fan_out is 1, 270 of 467); the sheet carries term_reach and stance_case.untouched_count. D-071: the legend states every blend the page reads — its inputs as ranks and the tuned weights (mcp's `load_index >= p90 (here 0.77128)` had no expansion anywhere on the page; the expansion rule fired only in a relation cell that shares a signal); the under-a-third parent carries its tie (both readers of the tenth round found the D-070 branch dropped it — registry's lit_room three-way, mcp's package_entry sixteen-way), a tie past three partners counted not listed; the sheet's dominant_dir unit says the cell shows either way. D-070: a caveat case whose input file the tree does not declare says "nothing to read" instead of "0 of N here" (substrate 0.10.0: summary.blame_ignore_revs; the registry's clock rows); the population rule states what each excluded kind's convention reads (config = a tool-config basename at the package root — knexfile.ts is a room by it); the stance names the disclosure's case (long-untouched and high-load at once) and this page's rooms at it with size and importers; the largest parent is named with its count under a third too; a containee drawing one set is one entry; the tier gloss says non-blank lines and the parent header says whose rooms; an excluded row's feature cell says "(excluded)" beside ◌; an importer sum with a named top room states the share without it; the test-graph clause counts a row's own rooms on the unreinforced side; a clock far boundary states its commit breadth; the clock caveats say which way they cut (maintainability 0.3.3). D-069: a ranked term inside a conjunction states the population's tie at its cutoff (eslint: p75 on fan_in is 2 with 330 of 467 rooms at it — the rules' index+test constant); a tied clock row states the breadth of the commit the tie is (77 tied — one commit of 1060 files); an importer sum names the room holding a third or more of it; a far-boundary gap never renders in exponent notation; a test-graph row counts the rooms without a test importer that a test-imported room imports; the parent cell reads "33 of its 61"; the clock rows carry a caveat with a counted case (maintainability 0.3.2, substrate 0.9.0: last_touch_blame_ignored, last_touch_commit_files). D-068: the legend's cross-scope and package-name counts carry their test-file split; a wing's scopes are named where two or fewer hold the feature; the centrality illustration is this sheet's pair, not a literal; the test convention is stated from the substrate's effective config; a caveat's case count sits in the rooms column; "excluded" means one thing (◌ marks) and a kind the ruleset does not count says so; the reinforcement caveats name the run-time mechanism (maintainability 0.3.1). D-067: the population sentence counts the files a ruleset's kind exclusion removed (config / migration / placeholder — substrate 0.7.0's G1 flags; Alex's call). D-066: a ranked row states the next value beyond its cutoff and how many rooms sit there (a batch commit divides at the cutoff; the tie count closed one side); a by-wing count on a wing of many package scopes says how many scopes hold the feature; the population sentence says node_count is the files with a source extension, not the tree; the legend counts the imports that name this repository's own package; a caveat carries its case count beside the clause it counts (`{case}`). D-065: the legend states the resolver's alias state beside the unresolved count — how many tsconfig `paths` patterns it was handed, or that the tsconfig could not be read and why (the caveat the substrate had carried since 0.4.1 and the page never rendered; substrate 0.5.0 fixed the loader that made it fire). D-064: the unresolved imports are counted by kind (from test files; alias-shaped) so the test-graph cells they bias are said to be lower bounds; a set drawn twice says so in the rooms column; a tier lists one name per set. D-063: every ranked term states its cutoff (the corridor's median fan-out is 1 on registry); the tie count sits in the rooms column; two profiles on one predicate are one row; centrality is defined; column headers carry their own legend. D-062: instance counts where a general mechanism dominates (ties at the cutoff; importers from tests per import-graph row and per tier room; cross-scope edges); the note is a legend and loses its repetitions; one measurement is one matrix row; ◌ rows last. D-061: a row states its realized share and cutoff (ties broke "a tenth by construction"); the tier table is every room at the top count, by path, with size; the population rule, the resolver's limit and the tier gloss say what they are. D-060: the defence moves to the cell it defends (position first; a bold rule at the top of the note and over the tier table; ◌ = excluded); the page carries its snapshot, the tier names' meaning, a caveat's case count, a tier's unlisted rooms, a single-pNN row's share by construction. D-057: a feature that fired on nothing has a row; the marker's values are defined on the page and a derived index expands through its grounding; the import graph and the test graph are one edge set, said; ruleset versions in the header

# ---------------------------------------------------------------- 1. the facts sheet

STANCE = (
    "The diagnosis presupposes a maintenance norm — that the positions it marks are worth a "
    "visit — which the reader may reject; it is stated as an ought, not a fact (system spec, "
    "stance disclosure)."
)


def facts(skeleton: dict[str, Any], substrate: dict[str, Any] | None = None) -> dict[str, Any]:
    """The facts sheet: the closed set of things the brief may say."""
    nodes = {n["id"]: n for n in (substrate or {}).get("nodes", [])}
    groups: list[tuple[str, list[dict[str, Any]]]] = [
        (skeleton["profile"]["name"], skeleton["features"])
    ]
    for od in skeleton.get("overlays") or []:
        groups.append((od["profile"], od["features"]))
    feats: dict[str, dict[str, Any]] = {}
    # D-057 (eighteenth seating): rows come from the ruleset's roster, so a feature that fired on
    # no room has a row with 0 — toothpick_wing vanished from registry's page, and the ruleset's
    # own note says it is kept on the page so its absence is visible. Older skeletons carry no
    # roster; their rows are the fired set, as before.
    rosters: list[tuple[str, list[dict[str, Any]]]] = [(skeleton["profile"]["name"], list(skeleton["profile"].get("roster") or []))]
    for od in skeleton.get("overlays") or []:
        rosters.append((od["profile"], list(od.get("roster") or [])))
    for profile, flist in groups + rosters:
        for f in flist:
            key = f"{profile}/{f['feature']}"
            entry = feats.setdefault(
                key,
                {
                    "profile": profile,
                    "feature": f["feature"],
                    "predicate": f["predicate"],
                    "diagnostic": bool(f.get("diagnostic", not f["decorative"]) and not f["decorative"]),
                    "decorative": bool(f["decorative"]),
                    "decorative_reason": f.get("decorative_reason"),
                    "decorative_signal_reasons": dict(f.get("decorative_signal_reasons") or {}),  # D-054
                    "validation_status": f.get("validation_status"),
                    "name_implies_consequence": bool(f.get("name_implies_consequence")),
                    "position_name": f.get("position_name"),
                    "caveat": f.get("caveat"),  # D-041: a ruleset's own warning about a predicate
                    "caveat_case": f.get("caveat_case"),  # D-060
                    "extra_caveats": [dict(x) for x in (f.get("extra_caveats") or [])],  # D-069
                    "thresholds": dict(f.get("thresholds") or {}),  # D-061: the pNN cutoffs this population resolved to
                    "rooms": [],
                },
            )
            if f.get("node") is not None:
                entry["rooms"].append(f["node"])
    depth = int((skeleton.get("geometry") or {}).get("wing_depth", 1))

    def wing_of(nid: str) -> str:
        parts = nid.split("/")
        return "/".join(parts[:depth]) if len(parts) > depth else "(root)"

    def scope_of(nid: str) -> str:
        pkg = ((nodes.get(nid) or {}).get("metrics") or {}).get("package", "")
        return f"{pkg}/{ROOT_SCOPE}" if pkg else ROOT_SCOPE

    population_ids = set(skeleton["strata"]["by_node"])
    scope_sizes: dict[str, int] = {}
    for nid in population_ids:
        scope_sizes[scope_of(nid)] = scope_sizes.get(scope_of(nid), 0) + 1

    for e in feats.values():
        e["rooms"] = sorted(set(e["rooms"]))
        e["count"] = len(e["rooms"])
        # D-060: how many of the feature's rooms are the caveat's case (the control seating found
        # "can clear the floor" true of 12 of 26 flooded_basement rooms, and D-042 forbids the caveat
        # the number; the count is a field beside it)
        if e.get("caveat_case"):
            e["caveat_case_count"] = sum(1 for r in e["rooms"] if _case_holds(e["caveat_case"], (nodes.get(r) or {}).get("metrics") or {}))
        for ec in e.get("extra_caveats") or []:  # D-069: each extra caveat's case counted the same way
            ec["case_count"] = sum(1 for r in e["rooms"] if _case_holds(ec["case"], (nodes.get(r) or {}).get("metrics") or {})) if ec.get("case") else None
        # D-062 (the typeorm control): where a general mechanism dominates this repository's instance, the
        # page counts it — all 70 dark rooms sat at the p90 cutoff (one mass commit), and every one of
        # src/index.ts's 1374 importers was a test file, while the page said "ties" and "one edge set"
        e["at_cutoff"] = _rooms_at_cutoff(e, nodes)
        # D-066 (the cookbook control): 35 rooms tied at the p90 cutoff and 24 more 28 minutes younger —
        # the tie count closed the rank's discreteness on one side; the row states the other
        e["beyond_cutoff"] = _rooms_beyond_cutoff(e, nodes, population_ids)
        # D-069 (the rules maintainer): a ranked term inside a conjunction printed its cutoff and not the
        # tie at it — on eslint p75 on fan_in is 2 with 330 of 467 rooms at that value (the rules index
        # plus one test file), and p50 and p75 on fan_out both resolve to 1; the population's tie per term
        e["term_ties"] = _term_ties(e, nodes, population_ids)
        # D-072 (the eleventh skimmer): column one said "upper quartile" where eslint's p75 on fan_out
        # resolves to 1 and 270 of 467 rooms reach it; the rooms each ranked term admits alone
        e["term_reach"] = _term_reach(e, nodes, population_ids)
        # D-069: a tied clock row's tie is a commit; its breadth is on the substrate (last_touch_commit_files)
        e["tie_touch_files"] = _tie_touch_files(e, nodes)
        if nodes and _signals_read(e["predicate"]) & {"fan_in", "centrality"}:
            fi = sum(int(((nodes.get(r) or {}).get("metrics") or {}).get("fan_in", 0) or 0) for r in e["rooms"])
            tf = sum(int(((nodes.get(r) or {}).get("metrics") or {}).get("test_fan_in", 0) or 0) for r in e["rooms"])
            e["importers"] = {"total": fi, "from_tests": tf}
            # D-069 named the room holding a third of the sum; D-073: the sum is edges, and the page reads
            # files — distinct importing files, the test files among them, the top room by its files
            if substrate is not None:
                e["importers"].update(_importer_files(e["rooms"], nodes, substrate))
        # D-069 (the eighth skimmer): "test-imported 162" leaves the page as "412 untested" while the test
        # suite reaches src through a barrel; the rooms without a test importer that a test-imported room
        # imports are counted beside the count
        if nodes and _signals_read(e["predicate"]) & {"test_fan_in"} and substrate is not None:
            e["via_importer"] = _via_importer(e, nodes, population_ids, substrate)
        # D-036: the share of a mark per wing is on the sheet, so the prose can state a count
        # per wing instead of an adverb ("mostly", "concentrated") the sheet cannot carry
        bw: dict[str, int] = {}
        for r in e["rooms"]:
            bw[wing_of(r)] = bw.get(wing_of(r), 0) + 1
        e["by_wing"] = dict(sorted(bw.items()))
        # D-066 (the cookbook control): a wing of fourteen package scopes reads as one location; the
        # feature's rooms per scope travel, and the by-wing cell says how many of the wing's scopes hold it
        bs: dict[str, int] = {}
        wsc: dict[str, set[str]] = {}
        for r in e["rooms"]:
            bs[scope_of(r)] = bs.get(scope_of(r), 0) + 1
            wsc.setdefault(wing_of(r), set()).add(scope_of(r))
        e["by_scope"] = dict(sorted(bs.items()))
        e["by_wing_scopes"] = {w: len(v) for w, v in sorted(wsc.items())}
        # D-068: at two scopes or fewer the cell names them (D-066's breaks-if clause 3)
        wscn: dict[str, dict[str, int]] = {}
        for r in e["rooms"]:
            wscn.setdefault(wing_of(r), {})
            wscn[wing_of(r)][scope_of(r)] = wscn[wing_of(r)].get(scope_of(r), 0) + 1
        e["by_wing_scope_counts"] = {w: dict(sorted(v.items())) for w, v in sorted(wscn.items())}
        # D-077 (scope-calibration-spec.md): pooling's effect as composition, not a counterfactual
        e["scope_composition"] = _scope_composition(e["rooms"], scope_of, scope_sizes, len(population_ids))
        # D-037: the largest single directory in the set — the composition a two-room exemplar
        # list can hide (typeorm's dark_room is half src/error)
        bd: dict[str, int] = {}
        for r in e["rooms"]:
            d = r.rsplit("/", 1)[0] if "/" in r else "(root)"
            bd[d] = bd.get(d, 0) + 1
        # D-075 (the thirteenth control): the lead of a tie was the last by path while its partners were
        # listed first by path; the lead is the first by path, as the partners are
        top = min(bd.items(), key=lambda kv: (-kv[1], kv[0])) if bd else ("(root)", 0)
        tied = (
            sum(1 for v in bd.values() if v == top[1]) > 1
        )  # D-040: a silent tie-break is a claim
        # D-038: the directory's population is the denominator the share needs — on a monorepo
        # one directory can be two thirds of the building, and a share without it is the base rate
        def _parent_pop(d: str) -> int:
            return sum(
                1
                for nid in skeleton["strata"]["by_node"]
                if (nid.rsplit("/", 1)[0] if "/" in nid else "(root)") == d
            )

        pop = _parent_pop(top[0])
        # D-054 (fifteenth seating): "(tied)" named no partner — on eslint package_entry's cell
        # named packages/eslint-config-eslint 4 / 5 over lib 4 by name order, and the wing-named
        # parent the note promises to mark was the one left out. A tie names every partner with
        # its numbers (D-045 item 3: a directory the register names carries its numbers).
        tied_with = [
            {"dir": d, "n": n, "population": _parent_pop(d)}
            for d, n in sorted(bd.items())
            if n == top[1] and d != top[0]
        ]
        # D-040: `dir` is the room's immediate parent (non-recursive), `population` the rooms whose
        # parent it is; `holds_third` is R15's bar — below it the register prints no directory
        e["dominant_dir"] = {
            "dir": top[0],
            "n": top[1],
            "population": pop,
            "tied": tied,
            "tied_with": tied_with,
            "holds_third": bool(top[1] * DIRECTORY_SHARE >= len(e["rooms"])),
            # D-041: the size guard is its own field — a cell says the reason that is the reason
            "placeable": len(e["rooms"]) >= DIRECTORY_MIN_ROOMS,
        }
    wings: dict[str, int] = {}
    for nid in skeleton["strata"]["by_node"]:
        w = wing_of(nid)
        wings[w] = wings.get(w, 0) + 1
    # D-036: co-location across every profile (the base summary counts the base profile only)
    marks: dict[str, int] = {}
    for e in feats.values():
        if e["diagnostic"]:
            for r in e["rooms"]:
                marks[r] = marks.get(r, 0) + 1
    # D-052: co-location is counted in distinct sets, the unit the most-marked table uses — a room
    # under one predicate in two profiles carries two marks and is not co-located with anything
    co_located_all = co_located(feats.values())
    # D-048: the rooms carrying the most diagnostic marks, each with every diagnostic feature that
    # marks it — the one thing the register does not print and the reading is bound to say (R19)
    most_marked_rooms = most_marked(feats.values())
    # D-049: the rooms two diagnostic features share, for every pair — the register draws identity
    # and containment in the relation column; the matrix says how the other sets sit against
    # each other (four rooms are both import_root and package_entry on eslint: the caveat's live case)
    _dkeys = sorted(k for k, e in feats.items() if e["diagnostic"])
    shared_rooms = [
        {"a": a, "b": b, "shared": len(set(feats[a]["rooms"]) & set(feats[b]["rooms"]))}
        for i, a in enumerate(_dkeys)
        for b in _dkeys[i + 1 :]
    ]
    # D-049: the list is capped; the sheet says how many rooms carry the most so a page can say
    # whether the cap bit (twelve rooms tied at seven on eslint; five were listed). D-050: the most
    # is counted in distinct sets, and every row carries the rooms at its own count — the twelfth
    # seating found a fill row (one of eight at six, first by path) under a lead that said "all"
    rooms_at_most_sets = most_marked_rooms[0]["rooms_at_this_count"] if most_marked_rooms else 0
    # D-036: two diagnostic features whose room sets coincide, or nest, are one set of rooms;
    # the sheet says so and R9 makes the prose say so
    overlaps: list[dict[str, Any]] = []
    # D-041: a set of fewer than three rooms is inside anything that contains it; no relation is drawn
    # D-055 (sixteenth seating): unless the predicates guarantee it — toothpick_wing's two rooms on
    # typeorm were inside foundation and crack by conjunction and the cell said "too few rooms".
    # The floor exists for containment by accident; a containment by predicate is not one.
    diag = [
        (k, set(e["rooms"]))
        for k, e in sorted(feats.items())
        if len(e["rooms"]) >= 1  # D-044: decorative features too — the note promised every set
    ]
    for i, (ka, ra) in enumerate(diag):
        for kb, rb in diag[i + 1 :]:
            under = len(ra) < RELATION_MIN_ROOMS or len(rb) < RELATION_MIN_ROOMS
            if under:
                if ra < rb and _conjoins(feats[ka], feats[kb]):
                    overlaps.append(_flag(feats, _within(feats, ka, kb, ra, rb)))
                elif rb < ra and _conjoins(feats[kb], feats[ka]):
                    overlaps.append(_flag(feats, _within(feats, kb, ka, rb, ra)))
                continue
            if ra == rb:
                # D-037: when two predicates draw one set, the conjuncts one has and the other
                # lacks did no work on this repository; the sheet names them so the prose cannot
                # read the identity as two measurements agreeing
                sa = set(feats[ka]["predicate"].replace("∧", "and").split(" and "))
                sb = set(feats[kb]["predicate"].replace("∧", "and").split(" and "))
                inert = sorted(t.strip() for t in (sa ^ sb))
                overlaps.append(
                    _flag(
                        feats,
                        {
                            "a": ka,
                            "b": kb,
                            "relation": "identical",
                            "n": len(ra),
                            "inert_terms": inert,
                            # D-038: the same predicate under two profiles is one measurement, not two agreeing
                            "shared_predicate": not inert,
                        },
                    )
                )
            elif ra < rb:
                overlaps.append(_flag(feats, _within(feats, ka, kb, ra, rb)))
            elif rb < ra:
                overlaps.append(_flag(feats, _within(feats, kb, ka, rb, ra)))
    # D-040/D-044: the diagnosis's counts come from diagnostic pairs only; a decorative pair is drawn
    # in the register (the note promises every set of three or more rooms) and counted nowhere
    diag_overlaps = [o for o in overlaps if o.get("diagnostic")]
    # D-040: how many distinct sets of rooms the diagnosis names — identical pairs are one set,
    # nestings stay two; and how many of the all-profile marks fall on identical pairs twice
    # D-052: one computation — the sets themselves, the same identity the most-marked table
    # counts per room; n_diag minus the identical overlaps was floored at three rooms and would
    # have disagreed with the table on a triple or an under-floor twin
    n_diag = sum(1 for e in feats.values() if e["diagnostic"] and e["rooms"])
    identical = [o for o in diag_overlaps if o["relation"] == "identical"]
    distinct_room_sets = distinct_sets(feats.values())
    # D-044: this number counts rooms an identical pair marks twice, not marks — it was named as marks
    # D-047: distinct rooms — a room in two identical pairs is one room marked twice twice over,
    # not two rooms (typeorm: six rooms sit in both pairs; 129 summed, 123 distinct)
    _twice: set[str] = set()
    for o in identical:
        _twice |= set(feats[o["a"]]["rooms"])
    rooms_marked_twice = len(_twice)
    relation_counts = {
        "identical": sum(1 for o in overlaps if o["relation"] == "identical"),
        "within": sum(1 for o in overlaps if o["relation"] == "within"),
        "total": len(overlaps),
    }
    # D-042: a number with two causes is two numbers — a gloss that names one cause is false of the other
    _shared = {r for o in identical if o.get("shared_predicate") for r in feats[o["a"]]["rooms"]}
    _inert = {r for o in identical if not o.get("shared_predicate") for r in feats[o["a"]]["rooms"]}
    rooms_marked_twice_shared_predicate = len(_shared)
    rooms_marked_twice_inert_conjunct = len(_inert)
    rooms_in_both_kinds = len(_shared & _inert)
    gate_fp = skeleton.get("substrate_config_fingerprint")
    if not gate_fp:
        raise ValueError(
            "skeleton carries no substrate_config_fingerprint; the brief cannot name its gate (D-036)"
        )
    s = skeleton["summary"]
    # D-054 (fifteenth seating): D-053 counted package scopes over every substrate node — on eslint
    # 21 over 1481 nodes where the 473 rooms span 6 (the test files the population excludes carry
    # the other 15); the three other pages coincided. The count is over the population, and the
    # rooms per scope travel with it so the pooling the calibration sentence discloses has a size.
    by_package: dict[str, int] = {}
    for nid in skeleton["strata"]["by_node"]:
        # D-055 (sixteenth seating): "(root)" was the wing (3 rooms on typeorm) and the scope (502)
        # in one note; the scope's root is the repository's own manifest and is named as such
        pkg = ((nodes.get(nid) or {}).get("metrics") or {}).get("package", "")
        # D-056 (seventeenth seating): "cookbook 136" (the wing) and "cookbook 1" (the scope of
        # cookbook/package.json) sat in one paragraph; D-055 had renamed the root scope only. A
        # scope is named by its manifest path, which no wing name can equal.
        scope = f"{pkg}/{ROOT_SCOPE}" if pkg else ROOT_SCOPE
        by_package[scope] = by_package.get(scope, 0) + 1
    n_packages = len(by_package)
    scopes_by_wing: dict[str, set[str]] = {}
    for nid in skeleton["strata"]["by_node"]:
        scopes_by_wing.setdefault(wing_of(nid), set()).add(scope_of(nid))
    population = s["population"]
    doc = {
        "brief_version": BRIEF_VERSION,
        "repo": {"name": skeleton["repo"]["name"], "head_sha": skeleton["repo"]["head_sha"]},
        # D-060: the snapshot the clock positions are relative to — on the substrate and the sheet, never on the page until now
        "as_of": ((substrate or {}).get("repo") or {}).get("as_of"),
        # D-061 (the eslint control): what a room is and how the import graph was read — 1008 of
        # eslint's 1481 nodes are test files and not rooms; 20 imports did not resolve; neither was said
        "node_count": len(nodes) or None,
        "test_nodes": sum(1 for n in nodes.values() if (n.get("metrics") or {}).get("is_test")) if nodes else None,
        # the mapper's population rule (engine.map_skeleton): not a test file, and with computed indices
        "unindexed_nodes": sum(1 for n in nodes.values() if not (n.get("metrics") or {}).get("is_test") and (n.get("derived") or {}).get("indices") is None) if nodes else None,
        "unresolved_imports": ((substrate or {}).get("summary") or {}).get("unresolved_imports"),
        # D-062: edges whose ends sit in different package scopes — typeorm's packages/ trees share one edge with the core
        "cross_scope_edges": (
            sum(1 for ed in (substrate or {}).get("edges") or [] if ((nodes.get(ed.get("from")) or {}).get("metrics") or {}).get("package", "") != ((nodes.get(ed.get("to")) or {}).get("metrics") or {}).get("package", ""))
            if nodes and (substrate or {}).get("edges") is not None else None
        ),
        "edge_count": len((substrate or {}).get("edges") or []) if substrate else None,
        # D-068 (the codemod control): 214 of typeorm's 219 cross-scope edges are transform fixtures under
        # the test convention; the D-062 split applied to rows and the tier, not to the legend's counts
        "cross_scope_from_tests": (
            sum(1 for ed in (substrate or {}).get("edges") or [] if ((nodes.get(ed.get("from")) or {}).get("metrics") or {}).get("is_test") and ((nodes.get(ed.get("from")) or {}).get("metrics") or {}).get("package", "") != ((nodes.get(ed.get("to")) or {}).get("metrics") or {}).get("package", ""))
            if nodes and (substrate or {}).get("edges") is not None else None
        ),
        "package_name_from_tests": (
            sum(1 for x in ((substrate or {}).get("caveats") or {}).get("package_name_samples") or [] if ((nodes.get(x.get("from")) or {}).get("metrics") or {}).get("is_test"))
            if nodes and ((substrate or {}).get("caveats") or {}).get("package_name_samples") is not None else None
        ),
        "package_names": list(((substrate or {}).get("summary") or {}).get("package_names") or []),
        "test_globs": list((((substrate or {}).get("repo") or {}).get("effective_config") or {}).get("test_globs") or []),
        # D-070 (the ninth control, on the registry): the clock caveat's case read "0 of 34 here" on a tree
        # with no .git-blame-ignore-revs — a count of what an absent file says. The sheet carries whether
        # the convention file exists (substrate 0.10.0) so the page can say "nothing to read" instead of 0.
        "blame_ignore_revs": dict(((substrate or {}).get("summary") or {}).get("blame_ignore_revs") or {}) or None,
        # D-070: "config" on the page was a word and the instrument a regex the page did not print (the
        # registry's one root room, knexfile.ts, is a config by role and a room by the convention); the
        # kind conventions travel with the sheet so the population rule can state them
        "kind_conventions": {k: v for k, v in ((((substrate or {}).get("repo") or {}).get("effective_config") or {})).items() if k in ("config_file_regex", "migration_dir_regex", "placeholder_content_regex")},
        # D-071 (the tenth control, on mcp-secure-server): `load_index >= p90 (here 0.77128)` — a cutoff to
        # five places on a blend whose inputs and weights appeared nowhere on the page, because the legend
        # expands a blend only inside a relation cell that shares a signal and this page had none. The
        # blends any feature reads travel with the sheet, with the tuned weights they were computed under.
        "index_weights": _index_weights(feats, substrate),
        "index_zeroed": _index_zeroed(_index_weights(feats, substrate)),
        "centrality_illustration": _centrality_illustration(feats, nodes, population_ids),
        # D-064 (the security reviewer): 34 of mcp-secure-server's 34 unresolved imports are test files
        # importing src/security through a tsconfig alias — static, not run-time — so test_fan_in on
        # the rooms they aim at is a lower bound; the page had named run-time imports as the mechanism
        "unresolved_by_kind": _unresolved_by_kind(substrate, nodes),
        "external_imports": ((substrate or {}).get("summary") or {}).get("external_imports"),
        # D-065: the resolver's alias state — the substrate 0.4.1 caveat `tsconfig_malformed` fired on
        # mcp-secure-server (its own JSONC stripper read the `/*` in "@/*" as a comment) and the page
        # never said so; D-064 named the mechanism one layer too low. Stated beside the count it explains.
        "tsconfig_aliases": ((substrate or {}).get("summary") or {}).get("tsconfig_aliases"),
        "tsconfig_malformed": ((substrate or {}).get("caveats") or {}).get("tsconfig_malformed") if ((substrate or {}).get("summary") or {}).get("tsconfig_malformed") else None,
        "skeleton_hash": skeleton["skeleton_hash"],
        "profile": skeleton["profile"]["name"],
        "overlays": list(s.get("overlay_profiles") or []),
        # D-057: the ruleset versions the page's texts come from (the skeleton carried them; the sheet dropped them)
        "profile_versions": {skeleton["profile"]["name"]: skeleton["profile"].get("version"), **{od["profile"]: (od.get("ruleset") or {}).get("version") for od in skeleton.get("overlays") or []}},
        "geometry": skeleton["geometry"]["name"],
        # D-053: what a wing is, and how many package scopes the one population spans
        "wing_depth": int(skeleton["geometry"].get("wing_depth", 1)),
        "packages": n_packages,
        # D-056: an ordered list — the sheet is written with sorted keys, and a dict's "largest
        # first" was true of the render and false of the file the viewer would read
        "by_package": [{"scope": k, "rooms": v} for k, v in sorted(by_package.items(), key=lambda kv: (-kv[1], kv[0]))],
        "scopes_by_wing": {w: len(v) for w, v in sorted(scopes_by_wing.items())},  # D-066
        # D-067: the kinds the ruleset does not count as rooms, with the count each removed
        "excluded_kinds": list(s.get("excluded_kinds") or []),
        "excluded_by_kind": dict(s.get("excluded_by_kind") or {}),
        "package_name_imports": ((substrate or {}).get("summary") or {}).get("package_name_imports"),  # D-066
        "population": s["population"],
        "wings": dict(sorted(wings.items())),
        "wing_count": len(wings),
        "gate": dict(sorted(skeleton["gate"]["signals"].items())),
        "diagnostic_count": sum(e["count"] for e in feats.values() if e["diagnostic"]),
        "diagnostic_count_base": s["diagnostic_count"],
        "decorative": {
            "count": s["decorative_count"],
            # D-057: every decorative feature on the roster, fired or not, with its count
            "features": sorted({e["feature"] for e in feats.values() if e["decorative"]}),
            "counts": {e["feature"]: e["count"] for e in sorted(feats.values(), key=lambda e: e["feature"]) if e["decorative"]},
        },
        "co_located_rooms": co_located_all,
        "most_marked_rooms": most_marked_rooms,
        "rooms_at_most_sets": rooms_at_most_sets,
        # D-061: every room at the most positions, by path, with its size — the table the page
        # renders since 0.27.0 (the skimmer read a capped, count-ordered list as a leaderboard twice)
        "top_tier": top_tier([e for e in feats.values() if e["diagnostic"]], {r: (nodes.get(r) or {}).get("metrics") or {} for r in skeleton["strata"]["by_node"]}),
        "shared_rooms": shared_rooms,
        # D-046 addendum: the prose kept computing this to say "the N features name M sets"
        "diagnostic_features": n_diag,
        "distinct_room_sets": distinct_room_sets,
        "rooms_marked_twice": rooms_marked_twice,
        "rooms_marked_twice_shared_predicate": rooms_marked_twice_shared_predicate,
        "rooms_marked_twice_inert_conjunct": rooms_marked_twice_inert_conjunct,
        "rooms_in_both_kinds": rooms_in_both_kinds,
        "relation_counts": relation_counts,
        # D-037: every building-level number carries its unit; a count of rooms is not a count of marks
        "units": {
            "population": "rooms",
            "wings": "rooms",
            "diagnostic_count": "marks",
            "diagnostic_count_base": "marks",
            "decorative.count": "marks",
            "co_located_rooms": "rooms carrying two or more distinct diagnostic sets, across all profiles (a predicate under two profiles is one set)",
            "most_marked_rooms": f"the rooms carrying the most distinct diagnostic sets (at most {MOST_MARKED_ROOMS}; {MOST_MARKED_ORDER}), each with every diagnostic feature that marks it, profile-qualified where a feature is under two profiles; sets counts distinct room sets; marks counts one per feature per profile; rooms_at_this_count is the rooms under two or more sets carrying the row's sets count, and listed_at_this_count how many of them the list carries, the first by path",
            "rooms_at_most_sets": "rooms carrying that most; when it exceeds the rooms listed at it, the list is the first of them by path",
            "shared_rooms": "rooms both features of a pair mark, for every pair of diagnostic features; identity and containment are the relation column's",
            "diagnostic_features": "diagnostic features that fired (features, not marks or rooms)",
            "distinct_room_sets": "sets of rooms the diagnostic features name — the room sets themselves, so identical sets are one whatever their size; a nesting is two",
            "rooms_marked_twice": "rooms an identical pair of diagnostic features marks twice (each such room carries two marks)",
            "rooms_marked_twice_shared_predicate": "of those, rooms where two profiles carry one predicate",
            "rooms_marked_twice_inert_conjunct": "of those, rooms where two predicates draw one set because a conjunct excludes nothing",
            "rooms_in_both_kinds": "rooms counted under both causes (the two counts overlap by this many)",
            "relation_counts": "relations the register draws, by kind, over every feature with enough rooms, decorative included, and containments the predicates guarantee at any count",
            "dominant_dir": "the immediate parent directory (non-recursive) holding the most of a feature's rooms, with holds_third saying whether it holds a third or more (D-070: shown either way); tied_with names every other directory holding as many",
            "by_package": f"rooms of the population per package scope, each named by its manifest path (the nearest package.json above the room; {ROOT_SCOPE} is the repository's own), an ordered list, largest first",
            "feature.count": "rooms (one mark per room)",
        },
        "overlaps": overlaps,
        "calibration": (
            f"in-repo, self-relative (system spec §5.3)"
            + (f", {n_packages} package scopes pooled — per-package calibration is an open question of the mapper (architect-brief spec §5, mapper §7 Q7)" if n_packages > 1 else "")
            + "; one frame"
        ),
        "gate_fingerprint": gate_fp,
        "features": [feats[k] for k in sorted(feats)],
        "rooms": {
            nid: {
                "lines": nodes[nid]["metrics"]["size_loc"],
                "fan_in": nodes[nid]["metrics"].get("fan_in"),
                "fan_out": nodes[nid]["metrics"].get("fan_out"),
            }
            for nid in sorted(skeleton["strata"]["by_node"])
            if nid in nodes
        },
        "stance": STANCE,
        # D-070 (the ninth control): the stance was one generic sentence where the system spec names a
        # case — "a finished, correct, stable utility that nobody has touched" — and the registry's one
        # tier room (src/utils/singleton.ts, 34 lines, 18 importers, dark_room + flooded_basement) is it.
        # The page cannot judge "finished"; it can name the rooms at the case's positions — long-untouched
        # (dark_room) and high-load (foundation) at once — with the fields a reader would weigh.
        "stance_case": _stance_case(feats, nodes),
    }
    raw = json.dumps(doc, sort_keys=True, ensure_ascii=False).encode("utf-8")
    doc["facts_hash"] = hashlib.sha256(raw).hexdigest()
    return doc


# ---------------------------------------------------------------- 3. the register lint

# Words that voice a consequence or a forecast. An `asserted` signal licenses a present
# structural position and nothing else (validation §2.1.1); these words cross the line.
CONSEQUENCE_WORDS = {
    "break",
    "breaks",
    "breaking",
    "broke",
    "broken",
    "will",
    "would",
    "shall",
    "risk",
    "risks",
    "risky",
    "fragile",
    "brittle",
    "dangerous",
    "danger",
    "blast",
    "ripple",
    "ripples",
    "cascade",
    "cascades",
    "cascading",
    "fail",
    "fails",
    "failure",
    "failing",
    "likely",
    "unlikely",
    "predict",
    "predicts",
    "prediction",
    "expect",
    "expected",
    "cause",
    "causes",
    "caused",
    "collapse",
    "collapses",
    "crumble",
    "vulnerable",
    "vulnerability",
    "exposed",
    "threat",
    "threatens",
    "prone",
    "future",
    "soon",
    "eventually",
    "inevitably",
    "bound",
    "doomed",
    "hazard",
    "hazardous",
    "impact",
    "impacts",
    "consequence",
    "consequences",
    "propagate",
    "propagates",
    "regress",
    "regression",
    "bug",
    "bugs",
    "defect",
    "defects",
    "unsafe",
    "safe",
    "critical",
}
# Consequence voiced as a relation between sets, without a listed word (Hume C1, D-028).
CONSEQUENCE_PHRASES = [
    r"\bagainst that\b",
    r"\boffsets?\b",
    r"\bcompensat\w*",
    r"\bmakes? up for\b",
    r"\bin exchange\b",
    r"\bcounterbalanc\w*",
    r"\bif [^.]{0,60}\b(changed|touched|removed|moved)\b",
]
# The disclosure clause is struck from a sentence before R1 reads it — the clause is not an
# amnesty for the rest of the sentence (Wittgenstein, D-028).
DISCLOSURE_CLAUSES = [
    r"not a claim about [^.;,]*",  # "what breaks", "damage", "condition" — the clause, not a phrase (D-037)
    r"(denotes|names|is) (a )?(position|location|place)[^.;,]*",
    r"a (position|location|place) in the import graph[^.;,]*",
    r"(position|location), not [^.;,]*",
]
# Whole-building labels (D-019: no archetype in v0).
BUILDING_LABELS = {
    "cathedral",
    "shantytown",
    "shanty",
    "bunker",
    "ruin",
    "ruins",
    "fortress",
    "palace",
    "slum",
    "temple",
    "monolith",
    "mansion",
    "hovel",
    "castle",
    "warehouse",
    "barn",
    "skyscraper",
    "tenement",
    "tower block",
    "labyrinth",
    "maze",
}
# [feature: a, b] · [feature ×N] · [feature ×N: a, b] · [f ×N; g ×M] · [f ×N, g ×M] — one bracket
# may chain several clauses; the count and the rooms of each are checked (D-032 addendum)
# "are not a diagnosis", "enter no part of this diagnosis", "nothing confirmed … diagnosis":
# the disclosure sentence negates diagnosis in its own words (R4).
NEGATED_DIAGNOSIS = re.compile(
    r"\b(?:not|no|nothing|never|neither|nor|without|outside|apart from|excluded from|excluding)\b"
    r"[^.;]{0,60}\bdiagnos"
)
# D-036: distributional words the sheet cannot carry (it carries counts per wing instead)
DISTRIBUTION = re.compile(
    r"\b(?:mostly|most of|largely|predominantly|mainly|chiefly|concentrated in|the bulk|"
    r"spread across|scattered|throughout|every wing|all wings|all of the wings|reaches into every|"
    r"accordingly|in proportion|proportionally|correspondingly|as one would expect|"
    r"near these|nearby|close to|adjacent|"
    r"and others|the others|the rest|the remainder|others under|others in)\b"
)
# D-037: comparatives and superlatives set one mark against another; the register forbids it
# D-041: two rooms as the ends of a span the page does not order
SPAN = re.compile(r"\bfrom\s+[\w./@-]+/[\w./@-]+\s+(?:through|to)\s+[\w./@-]+/[\w./@-]+")
COMPARISON = re.compile(
    r"\b(?:widest|largest|biggest|broadest|narrowest|smallest|fewest|greatest|"
    r"wider than|larger than|bigger than|smaller than|fewer than|more than any|the most \w+ set)\b"
)
# D-037: a number followed by its unit noun ("160 of those marks", "70 rooms")
UNIT_USE = re.compile(
    r"\b(\d{1,7}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+"
    r"(?:of\s+(?:those|these|the|its|the\s+\w+)\s+)?(rooms?|marks?|findings?|features?|relations?|nestings?|identical pairs?)\b",
    re.IGNORECASE,
)
# signal names a decorative_reason may cite (R4b)
_SIGNAL_LIKE = {
    "bug_pressure_index",
    "change_pressure_index",
    "blast_radius_index",
    "load_index",
    "neglect_index",
    "reinforcement_index",
    "complexity_proxy_index",
    "recent_commit_share",
    "centrality",
    "fan_in",
}
# D-045 addendum: an inference from what a predicate reads to what its rooms are
INFERENCE = re.compile(
    r"\b(?:and so|so not|therefore|thus|hence|which makes|making them|so they are)\b"
)
# D-043: a negated property whose noun is another feature's position
NEGATED_PROPERTY = re.compile(
    r"\b(?:not|never|no)\s+(?:an?\s+|the\s+)?(entrance|entry|entries|hub|hubs|root|roots|leaf|leaves|reinforced)\b"
)
PROPERTY_ALIASES = {
    "entrance": "package_entry",
    "entry": "package_entry",
    "entries": "package_entry",
    "hub": "hub",
    "hubs": "hub",
    "root": "import_root",
    "roots": "import_root",
    "leaf": "leaf_utility",
    "leaves": "leaf_utility",
    "reinforced": "scaffolding",
}
# D-046 addendum: likeness words claim a shared distribution only where a place is named —
# "marks sit there and in the smaller wings alike" is a claim, "corridor is likewise nested
# inside hub" is a connective between two relation statements
LIKENESS = re.compile(r"\b(?:alike|likewise|similarly|in the same way)\b")
# D-041: constructions that deny a relation
NO_RELATION = re.compile(
    r"\b(?:unshared|stands? apart|stand alone|no overlap|shares? no rooms|independent of|unrelated|overlaps? nothing)\b"
)
# D-038: nouns that make a nesting an identity
IDENTITY_NOUN = re.compile(
    r"\b(?:the same (?:\d+ )?rooms|one set of rooms|identical|one finding|coincide)\b"
)
# a directory-like token: two or more path segments, not ending in a file extension
DIRECTORY = re.compile(r"(?<![\w/@.-])([A-Za-z0-9_@.-]+(?:/[A-Za-z0-9_@.-]+)+)(?![\w/])")
BRACKET = re.compile(r"\[([a-z_][^\]]*)\]")
CLAUSE = re.compile(r"^([a-z_]+(?:/[a-z_]+)?)\s*(?:×\s*(\d+))?\s*(?::\s*(.+))?$")


def _citations(text: str):
    """Yield (feature, count, rooms) for every clause of every bracket in ``text``.

    Clauses chain on ``;``. A comma chains too, but only between bare counts
    (``[crack ×21, toothpick_wing ×3]``) — inside ``[hub: a.ts, b.ts]`` the comma
    separates rooms. A clause that does not parse is yielded by its raw text so
    it resolves to nothing and R2 refuses it.
    """
    for b in BRACKET.finditer(text):
        body = b.group(1)
        parts = [c.strip() for c in body.split(";")]
        if len(parts) == 1 and "," in body and ":" not in body:
            cs = [c.strip() for c in body.split(",")]
            if all((m := CLAUSE.match(c)) and m.group(2) for c in cs):
                parts = cs
        for c in parts:
            m = CLAUSE.match(c)
            if m:
                yield m.group(1), m.group(2), (m.group(3) or "").strip() or None
            else:
                yield c, None, None


INTEGER = re.compile(r"(?<![\w./-])(\d{1,7})(?![\w./%-])")
WORD_NUMBERS = {
    w: i
    for i, w in enumerate(
        "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
        "fifteen sixteen seventeen eighteen nineteen twenty".split()
    )
}
WORD_NUMBERS.update(
    {
        w: 10 * (i + 3)
        for i, w in enumerate("thirty forty fifty sixty seventy eighty ninety".split())
    }
)
_NUM_WORD = "|".join(sorted(list(WORD_NUMBERS) + ["hundred", "thousand"], key=len, reverse=True))
# "two hundred sixty-seven", "one hundred and thirty-three", "twenty-one": one span, one value.
# An ordinal ("seventy-fifth percentile") is a rank, not a count, and is left alone.
SPELLED_NUMBER = re.compile(
    rf"\b((?:(?:{_NUM_WORD})(?:[\s-]+(?:and[\s-]+)?(?=(?:{_NUM_WORD})\b))?)+)"
    r"\b(?!-?(?:first|second|third|fifth|[a-z]+th)\b)",
    re.IGNORECASE,
)


def _spelled_numbers(text: str):
    """Yield (span, value) for every number written in words."""
    for m in SPELLED_NUMBER.finditer(text):
        span = m.group(1).strip(" -")
        total = cur = 0
        for w in re.split(r"[\s-]+", span.lower()):
            if w in WORD_NUMBERS:
                cur += WORD_NUMBERS[w]
            elif w == "hundred":
                cur = (cur or 1) * 100
            elif w == "thousand":
                total += (cur or 1) * 1000
                cur = 0
        yield span, total + cur


# a sentence may begin with a lowercase feature name ("flooded_basement sits inside …"): the split
# accepts any letter, or a bracket or backtick, after the terminal (D-042 addendum — one merged
# "sentence" let an identity noun for one pair fire R13 on the nestings beside it)
# D-048: a sentence may open with a digit — the prompt requires digits — and the lookahead
# admitted only letters, so "… 2 within. 254 rooms …" was one sentence to every per-sentence
# rule and a bracket warranting nothing passed R2b on the merged span
SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Za-z0-9_\[`])")


@dataclass
class Violation:
    rule: str
    paragraph: int
    text: str
    detail: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "rule": self.rule,
            "paragraph": self.paragraph,
            "text": self.text,
            "detail": self.detail,
        }


def _mentions(sentence: str, room: str) -> bool:
    """`src/index.ts` is not a mention of `packages/codemod/src/index.ts`: a room is named
    only as a whole path token."""
    return re.search(r"(?<![\w/.\-])" + re.escape(room) + r"(?![\w/.\-])", sentence) is not None


def _paragraphs(text: str) -> list[str]:
    body = text.split("\n## Provenance", 1)[0]
    return [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]


def lint(text: str, facts_doc: dict[str, Any], register: bool = False) -> list[Violation]:
    """The deterministic hostile reader. Returns the violations; empty means PASS."""
    out: list[Violation] = []
    by_feature = {f["feature"]: f for f in facts_doc["features"]}
    by_key = {f"{f['profile']}/{f['feature']}": f for f in facts_doc["features"]}
    allowed_numbers = set()
    allowed_numbers.add(facts_doc["population"])
    allowed_numbers.add(facts_doc["diagnostic_count"])
    allowed_numbers.add(facts_doc.get("diagnostic_count_base", facts_doc["diagnostic_count"]))
    allowed_numbers.add(facts_doc["decorative"]["count"])
    allowed_numbers.add(facts_doc["co_located_rooms"])
    for m in facts_doc.get("most_marked_rooms") or []:
        allowed_numbers.update((m["marks"], m.get("sets", 0), m.get("rooms_at_this_count", 0)))
    allowed_numbers.add(facts_doc.get("rooms_at_most_sets", 0))
    allowed_numbers.update(facts_doc["wings"].values())
    allowed_numbers.add(facts_doc.get("wing_count", len(facts_doc["wings"])))
    # D-039 addendum: "the same predicate under two profiles" — the profile count is a sheet fact
    allowed_numbers.add(1 + len(facts_doc.get("overlays") or []))
    allowed_numbers.add(facts_doc.get("distinct_room_sets", 0))
    allowed_numbers.add(facts_doc.get("diagnostic_features", 0))
    allowed_numbers.add(len(facts_doc.get("overlaps") or []))  # "three relations" (D-040 addendum)
    allowed_numbers.add(facts_doc.get("rooms_marked_twice", 0))
    allowed_numbers.add(facts_doc.get("rooms_marked_twice_shared_predicate", 0))
    allowed_numbers.add(facts_doc.get("rooms_marked_twice_inert_conjunct", 0))
    allowed_numbers.add(facts_doc.get("rooms_in_both_kinds", 0))
    allowed_numbers.update((facts_doc.get("relation_counts") or {}).values())
    # D-036 (hostile reading, run 17): a feature's numbers are admitted in the sentence that
    # cites the feature, not anywhere in the paragraph — "two sit outside src" passed because
    # 2 was some other feature's count
    feature_numbers: dict[str, set[int]] = {}
    for f in facts_doc["features"]:
        dd = f.get("dominant_dir") or {}
        nums = {
            f["count"],
            *f.get("by_wing", {}).values(),
            dd.get("n", f["count"]),
            dd.get("population", f["count"]),
        }
        feature_numbers[f["feature"]] = nums
        feature_numbers[f"{f['profile']}/{f['feature']}"] = nums
    for sr in facts_doc.get("shared_rooms") or []:
        for k in (sr["a"], sr["b"], sr["a"].split("/")[-1], sr["b"].split("/")[-1]):
            feature_numbers.setdefault(k, set()).add(sr["shared"])
    wing_names = set(facts_doc["wings"])
    # R18 (D-045): families of marks the sheet does not define, built from its own profile and record names
    _families = [
        facts_doc["profile"],
        *(facts_doc.get("overlays") or []),
        *[n for n, _ in _RECORDS],
        "graph",
        "age",
        "import-graph",
        "load",
        "recency",
    ]
    family_words = re.compile(
        r"\b(?:the\s+)?(?:"
        + "|".join(re.escape(x) for x in _families)
        + r")\s+(?:marks|features|positions|set|sets)\b"
    )
    largest_wing = (
        max(facts_doc["wings"], key=lambda w: (facts_doc["wings"][w], w))
        if facts_doc["wings"]
        else None
    )
    # D-037: unit classes for R12 — feature counts are both (one mark per room)
    rooms_only = (
        {facts_doc["population"], facts_doc["co_located_rooms"], facts_doc.get("rooms_at_most_sets", 0)}
        | {m.get("rooms_at_this_count", 0) for m in facts_doc.get("most_marked_rooms") or []}
        | set(facts_doc["wings"].values())
        # D-048: a directory's share and population are rooms — "which holds 61 rooms" was refused
        # as marks on typeorm because 61 was also a mark total
        | {
            v
            for f in facts_doc["features"]
            for v in ((f.get("dominant_dir") or {}).get("n"), (f.get("dominant_dir") or {}).get("population"))
            if v is not None
        }
    )
    marks_only = {
        *(m["marks"] for m in facts_doc.get("most_marked_rooms") or []),
        facts_doc["diagnostic_count"],
        facts_doc.get("diagnostic_count_base", 0),
        facts_doc["decorative"]["count"],
    }
    both = {f["count"] for f in facts_doc["features"]} | {
        v for f in facts_doc["features"] for v in f.get("by_wing", {}).values()
    }
    rooms_ok = both | rooms_only
    marks_ok = both | marks_only
    any_validated = any(v == "validated" for v in (facts_doc.get("gate") or {}).values())
    room_metrics = facts_doc.get("rooms", {})
    used_consequence_names: set[str] = set()
    first_use: dict[str, tuple[int, str]] = {}  # feature → (paragraph, paragraph text)
    room_ids = sorted(
        {r for f in facts_doc["features"] for r in f["rooms"]} | set(facts_doc.get("rooms", {})),
        key=len,
        reverse=True,
    )
    stance_key = facts_doc["stance"][:40].lower()
    for i, para in enumerate(_paragraphs(text), 1):
        if para.startswith(("#", "*Register lint")):
            continue
        low_para = para.lower()
        # the stance paragraph is the stance sentence, not any paragraph that quotes a phrase of it
        bare = BRACKET.sub("", low_para).strip()
        is_stance = bare.startswith(stance_key)
        is_disclosure = "decorative" in low_para and (
            "not a diagnosis" in low_para or "no diagnosis" in low_para
        )
        for f0 in facts_doc["features"]:
            if (
                f0["name_implies_consequence"]
                and f0["feature"] not in first_use
                and re.search(rf"\b{re.escape(f0['feature'])}\b", low_para)
            ):
                first_use[f0["feature"]] = (i, low_para)
        # R1 consequence vocabulary, per sentence. Bracket interiors are names, not claims,
        # and are stripped first; the disclosure clause is struck, not used as an amnesty.
        for sent in SENTENCE.split(para):
            bare_sent = BRACKET.sub("", sent)
            scan = BRACKET.sub("", sent).lower()
            for clause in DISCLOSURE_CLAUSES:
                scan = re.sub(clause, " ", scan)
            hits = sorted(w for w in CONSEQUENCE_WORDS if re.search(rf"\b{re.escape(w)}\b", scan))
            hits += [m.group(0) for pat in CONSEQUENCE_PHRASES for m in re.finditer(pat, scan)]
            if hits:
                out.append(
                    Violation(
                        "R1-consequence",
                        i,
                        sent[:160],
                        f"consequence/forecast vocabulary: {', '.join(hits)}",
                    )
                )
            # R6 building label
            labels = sorted(w for w in BUILDING_LABELS if re.search(rf"\b{re.escape(w)}\b", scan))
            if labels:
                out.append(
                    Violation(
                        "R6-archetype",
                        i,
                        sent[:160],
                        f"whole-building label: {', '.join(labels)} (D-019)",
                    )
                )
            # R2b (D-043, narrowed D-046): a citation warrants something in its sentence — the
            # feature named in prose, one of its rooms, or one of its numbers — or it is decoration.
            # Two forms warrant it otherwise: the decorative disclosure, whose whole discipline is to
            # cite by count and name no room (R4/R7), and a sentence continuing about a feature the
            # sentence before it named, where the subject is a pronoun.
            prev_sent = (
                SENTENCE.split(para)[max(0, SENTENCE.split(para).index(sent) - 1)]
                if sent in SENTENCE.split(para)
                else ""
            )
            dec_disclosure = bool(
                re.search(rf"\b{facts_doc['decorative']['count']}\b", bare_sent)
                and NEGATED_DIAGNOSIS.search(bare_sent.lower())
            )
            for cname, ccount, crooms in _citations(sent):
                cf = by_key.get(cname) or by_feature.get(cname)
                if not cf:
                    continue
                if dec_disclosure and cf["decorative"]:
                    continue
                named_in_prose = (
                    re.search(rf"\b{re.escape(cf['feature'])}\b", bare_sent) is not None
                )
                room_named = any(_mentions(bare_sent, r) for r in cf["rooms"])
                nums = {cf["count"], *cf.get("by_wing", {}).values()}
                number_used = any(re.search(rf"\b{n}\b", bare_sent) for n in nums)
                anaphora = bool(
                    prev_sent
                    and re.search(rf"\b{re.escape(cf['feature'])}\b", BRACKET.sub("", prev_sent))
                    and re.match(
                        r"\s*(?:it|its|it's|they|their|this|that|these|those)\b", bare_sent.lower()
                    )
                )
                if not (named_in_prose or room_named or number_used or anaphora):
                    out.append(
                        Violation(
                            "R2-provenance",
                            i,
                            sent[:160],
                            f"[{cname}] warrants nothing in this sentence: the feature, a room of it or its count must appear",
                        )
                    )
            # R8 attribution: a room named in a sentence is covered by a feature cited in it
            named = [rid for rid in room_ids if _mentions(sent, rid)]
            covered: set[str] = set()
            for cname, _c, _r in _citations(sent):
                cf = by_key.get(cname) or by_feature.get(cname)
                if cf:
                    covered.update(cf["rooms"])
            # R10 (D-036): a directory named in a sentence contains a room cited in it — R8 covered
            # rooms, and a distribution over four directories was asserted on the warrant of two
            for d in sorted(set(DIRECTORY.findall(BRACKET.sub("", sent)))):
                if d in room_ids or d in wing_names:
                    continue
                if not any(r.startswith(d + "/") for r in room_ids):
                    continue  # not a directory of this building; R2/R8 territory if it is a room
                if not any(r.startswith(d + "/") for r in covered):
                    out.append(
                        Violation(
                            "R10-prefix",
                            i,
                            sent[:160],
                            f"names the directory {d} but no room cited in the sentence sits in it",
                        )
                    )
            # R11 (D-036): a share is a number on the sheet (by_wing), not an adverb
            low_sent = bare_sent.lower().replace("across all profiles", "")
            for m in DISTRIBUTION.finditer(low_sent):
                out.append(
                    Violation(
                        "R11-share",
                        i,
                        sent[:160],
                        f"'{m.group(0)}' asserts a share the sheet does not carry; state the count per wing (by_wing)",
                    )
                )
            for m in SPAN.finditer(BRACKET.sub("", sent)):
                out.append(
                    Violation(
                        "R11-share",
                        i,
                        sent[:160],
                        f"'{m.group(0)[:60]}' presents two rooms as the ends of a span the page does not order (D-041)",
                    )
                )
            # D-046: R11 compares marks; a sentence that names no feature is comparing wings
            names_a_feature = any(
                re.search(rf"\b{re.escape(x['feature'])}\b", bare_sent)
                for x in facts_doc["features"]
            ) or any((by_key.get(c) or by_feature.get(c)) for c, _n, _r in _citations(sent))
            place_named = any(
                re.search(rf"(?<![\w/@.-]){re.escape(w)}(?![\w/])", bare_sent) for w in wing_names
            ) or any(
                (x.get("dominant_dir") or {}).get("dir")
                and re.search(
                    rf"(?<![\w/@.-]){re.escape(x['dominant_dir']['dir'])}(?![\w])", bare_sent
                )
                for x in facts_doc["features"]
            )
            if place_named:
                for m in LIKENESS.finditer(low_sent):
                    out.append(
                        Violation(
                            "R11-share",
                            i,
                            sent[:160],
                            f"'{m.group(0)}' claims a shared distribution the sheet does not carry; state the counts per wing",
                        )
                    )
            for m in COMPARISON.finditer(low_sent if names_a_feature else ""):
                # D-046 addendum: "the largest wing" compares wings, whatever else the sentence cites
                window = low_sent[max(0, m.start() - 30) : m.end() + 30]
                if re.search(r"\bwings?\b|\bdirector(?:y|ies)\b", window):
                    continue
                out.append(
                    Violation(
                        "R11-share",
                        i,
                        sent[:160],
                        f"'{m.group(0)}' sets one mark against another; a p90 set has its size by construction (D-037)",
                    )
                )
            # R12 (D-037): a number wears its unit — a count of rooms is not "N marks"
            for m in UNIT_USE.finditer(BRACKET.sub("", sent)):
                raw = m.group(1).lower()
                n = int(raw) if raw.isdigit() else WORD_NUMBERS.get(raw, -1)
                unit = m.group(2).lower().rstrip("s")
                if unit == "finding":
                    # D-038: "one finding, two marks" counts features — a unit the sheet does not carry
                    out.append(
                        Violation(
                            "R12-unit", i, sent[:160], "'findings' is not a unit on the facts sheet"
                        )
                    )
                    continue
                if unit == "feature":
                    continue  # a count of feature names; the names themselves are checked
                if unit in ("relation", "nesting", "identical pair"):
                    # D-044: a count of relations is a sheet number by kind, not a coincidence
                    rc = facts_doc.get("relation_counts") or {}
                    want = {
                        "relation": rc.get("total"),
                        "nesting": rc.get("within"),
                        "identical pair": rc.get("identical"),
                    }[unit]
                    if want is not None and n != want:
                        out.append(
                            Violation(
                                "R12-unit", i, sent[:160], f"{n} {unit}s: the register draws {want}"
                            )
                        )
                    continue
                if unit == "mark" and n <= 3 and n <= len(facts_doc["features"]):
                    continue  # "two marks on one set": a count of features wearing the word (D-038 addendum)
                if unit == "mark" and n in rooms_only and n not in marks_ok:
                    out.append(
                        Violation(
                            "R12-unit",
                            i,
                            sent[:160],
                            f"{n} counts rooms on the facts sheet, not marks",
                        )
                    )
                if unit == "room" and n in marks_only and n not in rooms_ok:
                    out.append(
                        Violation(
                            "R12-unit",
                            i,
                            sent[:160],
                            f"{n} counts marks on the facts sheet, not rooms",
                        )
                    )
            # R12 (D-040): a ratio across units — "N rooms … out of M marks"
            if re.search(
                r"\b\d+\s+rooms?\b[^.;]{0,60}\bout of\s+\d+\s+(?:diagnostic\s+)?marks?\b", low_sent
            ) or re.search(r"\b\d+\s+marks?\b[^.;]{0,60}\bout of\s+\d+\s+rooms?\b", low_sent):
                out.append(
                    Violation(
                        "R12-unit",
                        i,
                        sent[:160],
                        "a count of rooms is not a share of marks, nor marks of rooms",
                    )
                )
            # R17 (D-041): a prose claim of no relation is checked against the overlaps list —
            # the first sentence false against the sheet (fifth seating) said a nested feature stood apart
            if NO_RELATION.search(low_sent):
                related = {
                    x
                    for ov in facts_doc.get("overlaps") or []
                    for x in (ov["a"].split("/")[-1], ov["b"].split("/")[-1])
                }
                for name in related:
                    if re.search(rf"\b{re.escape(name)}\b", sent):
                        out.append(
                            Violation(
                                "R17-relation",
                                i,
                                sent[:160],
                                f"{name} is said to stand apart but the sheet lists it in a relation",
                            )
                        )
            # R17b (D-043): "not an entrance" said of rooms some of which another feature marks as
            # entries — the caveat paraphrased into a property of rooms (seventh seating)
            for m in NEGATED_PROPERTY.finditer(low_sent):
                target = PROPERTY_ALIASES.get(m.group(1))
                tf = by_feature.get(target) if target else None
                if not tf:
                    continue
                # D-045 addendum: a caveat is a limit on the predicate (D-042) and the page prints it,
                # so a sentence that quotes it and draws no inference to the rooms is the caveat
                # speaking, not a claim about rooms. The seventh seating's sentence inferred ("reading
                # no fan-in and so not an entrance"); these do not.
                quoted = any(
                    (cf or {}).get("caveat")
                    and sum(
                        1
                        for w in {t for t in re.findall(r"[a-z_]{4,}", cf["caveat"].lower())}
                        if re.search(rf"\b{re.escape(w)}\b", low_sent)
                    )
                    >= 3
                    for cf in (by_key.get(c) or by_feature.get(c) for c, _n, _r in _citations(sent))
                )
                if quoted and not INFERENCE.search(low_sent):
                    continue
                for cname, _c, _r in _citations(sent):
                    cf = by_key.get(cname) or by_feature.get(cname)
                    if cf and cf is not tf and set(cf["rooms"]) & set(tf["rooms"]):
                        out.append(
                            Violation(
                                "R17-relation",
                                i,
                                sent[:160],
                                f"'{m.group(0)}' is said of {cf['feature']} rooms, {len(set(cf['rooms']) & set(tf['rooms']))} of which {target} marks",
                            )
                        )
                        break
            # R18 (D-045): a family of marks no field defines — "the graph marks", "the onboarding
            # marks", "the age marks" — is refused; the reading names features, the register names
            # profiles and records. Built from the sheet's profile names and the record names.
            for m in family_words.finditer(low_sent):
                word = m.group(0).lower().replace("the ", "").split()[0]
                record = {
                    "graph": "import graph",
                    "import-graph": "import graph",
                    "age": "clock",
                    "recency": "clock",
                    "load": "import graph",
                    "test": "test graph",
                    "edit": "edit record",
                    "size": "size",
                }.get(word)
                cited_here = [
                    c
                    for c in (by_key.get(x) or by_feature.get(x) for x, _n, _r in _citations(sent))
                    if c
                ]
                # D-046 addendum: the family is defined when every feature the sentence cites reads
                # that record (record_of) or carries that profile — the sheet defines it after all
                if cited_here and all(
                    (record and record in record_of(c["predicate"])) or c["profile"] == word
                    for c in cited_here
                ):
                    continue
                out.append(
                    Violation(
                        "R18-family",
                        i,
                        sent[:160],
                        f"'{m.group(0)}' groups features into a family the sheet does not define; name the features",
                    )
                )
            # R16 (D-047): "N wings hold …:" followed by a list of fewer than N wings is a partial
            # enumeration presented as the whole; the building's wing counts are all sayable, so say all or none
            mw = re.search(rf"\b{facts_doc['wing_count']}\s+wings\b[^.;]*?:", low_sent)
            if mw:
                listed = sum(
                    1
                    for w in wing_names
                    if re.search(
                        rf"(?<![\w/@.-]){re.escape(w if w != '(root)' else 'root')}(?![\w/])",
                        low_sent,
                    )
                )
                if 0 < listed < facts_doc["wing_count"]:
                    out.append(
                        Violation(
                            "R16-restatement",
                            i,
                            sent[:160],
                            f"{facts_doc['wing_count']} wings announced and {listed} listed; name every wing with its rooms, or none",
                        )
                    )
            # R14 (D-037): "validated" names a status no signal holds in this gate
            if not any_validated and re.search(r"\bvalidated\b", low_sent):
                out.append(
                    Violation(
                        "R14-status",
                        i,
                        sent[:160],
                        "'validated' names a status no signal in this gate holds; every feature here rests on an asserted signal",
                    )
                )
            if named:
                for rid in named:
                    if rid not in covered:
                        out.append(
                            Violation(
                                "R8-attribution",
                                i,
                                sent[:160],
                                f"names {rid} but no feature cited in the sentence fired on it",
                            )
                        )
        # R2 provenance: citations resolve; every paragraph carries at least one
        cites = list(_citations(para))
        decorative_only = bool(cites) and all(
            (by_key.get(n) or by_feature.get(n) or {}).get("decorative") and c and not r
            for n, c, r in cites
        )
        # D-046 addendum: a paragraph that names no feature and no room and states only building-level
        # numbers is the building's shape (wings, population) — the register's, with nothing to cite
        building_only = (
            not any(
                re.search(rf"\b{re.escape(x['feature'])}\b", para) for x in facts_doc["features"]
            )
            and not any(_mentions(para, rid) for rid in room_ids)
            and INTEGER.findall(BRACKET.sub("", para))
            and all(int(n) in allowed_numbers for n in INTEGER.findall(BRACKET.sub("", para)))
        )
        if (
            not cites
            and not is_stance
            and not building_only
            and not (is_disclosure and decorative_only)
        ):
            out.append(
                Violation(
                    "R2-provenance",
                    i,
                    para[:160],
                    "paragraph carries no [feature: room] or [feature ×N] citation",
                )
            )
        for name, count, room in cites:
            if not count and not room:
                out.append(
                    Violation(
                        "R2-provenance", i, para[:160], f"[{name}] cites neither a room nor a count"
                    )
                )
                continue
            f = by_key.get(name) or by_feature.get(name)
            if f is None:
                out.append(
                    Violation(
                        "R2-provenance",
                        i,
                        para[:160],
                        f"citation names a feature not in the skeleton: {name}",
                    )
                )
                continue
            if f["decorative"] and room:
                out.append(
                    Violation(
                        "R4-decorative",
                        i,
                        para[:160],
                        f"a decorative feature is cited by count only; [{name}: …] singles out rooms it may not",
                    )
                )
            # A decorative feature is disclosed, not diagnosed, when the sentence that cites it
            # cites decorative features by count only and names no room — the wording is the
            # register's, the rule is the citation's (D-032 addendum; before, a phrase match).
            cite_sentences = [
                sent
                for sent in SENTENCE.split(para)
                if any(n == name for n, _c, _r in _citations(sent))
            ]
            disclosed_here = any(
                all(
                    (by_key.get(n) or by_feature.get(n) or {}).get("decorative") and c and not r
                    for n, c, r in _citations(sent)
                )
                and not any(_mentions(sent, rid) for rid in room_ids)
                and NEGATED_DIAGNOSIS.search(sent.lower())
                for sent in cite_sentences
            )
            if f["decorative"] and not disclosed_here:
                out.append(
                    Violation(
                        "R4-decorative",
                        i,
                        para[:160],
                        f"diagnostic claim cites a decorative feature: {name} (excluded from diagnosis, mapper §3)",
                    )
                )
            if room:
                for r in [x.strip() for x in room.split(",")]:
                    if r not in f["rooms"]:
                        out.append(
                            Violation("R2-provenance", i, para[:160], f"{name} did not fire on {r}")
                        )
            if count and int(count) != f["count"]:
                out.append(
                    Violation(
                        "R2-provenance",
                        i,
                        para[:160],
                        f"{name} ×{count}: the skeleton counts {f['count']}",
                    )
                )
            if f["name_implies_consequence"]:
                used_consequence_names.add(f["feature"])
        # R3 numbers — digits and number words alike; a room's own metrics are admitted only
        # in a paragraph that names the room (D-030: otherwise any small integer passes)
        for sent in SENTENCE.split(para):
            stripped = BRACKET.sub("", sent)
            # D-048: the sentence before this one, in this loop (the first loop's prev_sent is stale here)
            _sents = SENTENCE.split(para)
            prev_sent = _sents[_sents.index(sent) - 1] if sent in _sents and _sents.index(sent) else ""
            sent_allowed = set(allowed_numbers)
            for cname, _c, _r in _citations(sent):
                sent_allowed |= feature_numbers.get(cname, set())
            # D-038 addendum: the numbers of an overlap belong to the sentence that names its pair
            pair_numbers: set[int] = set()
            for ov in facts_doc.get("overlaps") or []:
                oa, ob = ov["a"].split("/")[-1], ov["b"].split("/")[-1]
                if re.search(rf"\b{re.escape(oa)}\b", sent) and re.search(
                    rf"\b{re.escape(ob)}\b", sent
                ):
                    pair_numbers |= {ov["n"], ov.get("n_outside", ov["n"])}
            sent_allowed |= pair_numbers
            if register:
                # R16 (D-040, rebuilt D-041): the register's by-wing and directory numbers are sayable
                # only in a sentence that names the wing or directory they belong to — a binding, not a
                # refusal, so the deflating number is always sayable and the bare restatement is not
                cited = [by_key.get(c) or by_feature.get(c) for c, _n, _r in _citations(sent)]
                bare = BRACKET.sub("", sent)
                # the entitlement is the union over every cited feature — a number one cited
                # feature owns is not refused because another cited feature also carries it
                entitled = set(allowed_numbers) | pair_numbers
                for cf in cited:
                    if not cf:
                        continue
                    entitled.add(cf["count"])
                    for w, v in cf.get("by_wing", {}).items():
                        wing_named = (
                            re.search(rf"(?<![\w/@.-]){re.escape(w)}(?![\w/])", bare) is not None
                            # D-047: "(root)" is written "the root" or "the root wing" in prose
                            or (
                                w == "(root)"
                                and re.search(r"\b(?:the\s+)?root(?:\s+wing|\s+level)?\b", bare)
                                is not None
                            )
                        )
                        if not wing_named:
                            continue
                        # D-045: a wing that holds all of a feature's rooms is that feature's register
                        # row, whether or not the number is in the prose — the citation carries it
                        # (S2: "import_root fires in the cookbook servers [×17]"); a feature of one or
                        # two rooms has no share to restate, its place is its room's name
                        if v == cf["count"] and cf["count"] >= RELATION_MIN_ROOMS:
                            out.append(
                                Violation(
                                    "R16-restatement",
                                    i,
                                    sent[:160],
                                    f"{cf['feature']}'s rooms all sit in {w}: that is its register row, not a reading — name its rooms or say nothing of the wing",
                                )
                            )
                            continue
                        # D-042: naming the largest wing costs nothing on a one-wing building, so its
                        # count stays the register's; a minority wing's count is the reading's to say
                        if w != largest_wing:
                            entitled.add(v)
                            # D-045: a located subset carries its total — "7 of the 42", never "7 in src"
                            if (
                                v < cf["count"]
                                and re.search(rf"\b{v}\b", bare)
                                and not re.search(rf"\b{cf['count']}\b", bare)
                            ):
                                out.append(
                                    Violation(
                                        "R16-restatement",
                                        i,
                                        sent[:160],
                                        f"{v} of {cf['feature']}'s rooms are placed in {w} without the {cf['count']} they are part of; say the total in the sentence",
                                    )
                                )
                    dd = cf.get("dominant_dir") or {}
                    # D-048: a directory is named, not a room inside it — "lib/config/default-config.js"
                    # does not name lib/config (the R19 sentence was refused for corridor's unplaced
                    # directory on eslint)
                    if dd and re.search(rf"(?<![\w/@.-]){re.escape(dd['dir'])}(?![\w/])", bare):
                        # D-046 addendum: a parent directory that shares a wing's name is sayable, but
                        # only as the parent — "the tools directory", "as parent", "not the wing" — since
                        # the wing and the directory hold different numbers of the feature's rooms
                        ambiguous = dd["dir"] in wing_names
                        marked = (
                            re.search(r"\bdirector(?:y|ies)\b|as parent|not the wing", bare)
                            is not None
                        )
                        if ambiguous and not marked:
                            if re.search(rf"\b{dd.get('n')}\b", bare) and dd.get("n") != cf.get(
                                "by_wing", {}
                            ).get(dd["dir"]):
                                out.append(
                                    Violation(
                                        "R16-restatement",
                                        i,
                                        sent[:160],
                                        f"{dd['dir']} names both a wing ({cf.get('by_wing', {}).get(dd['dir'])} of {cf['feature']}'s rooms) and their parent directory ({dd.get('n')}); say 'the {dd['dir']} directory' or name the wing's count",
                                    )
                                )
                        else:
                            entitled |= {dd.get("n"), dd.get("population")}
                            # D-045: a directory share carries its denominator in the same sentence, and
                            # a directory the register suppressed is named with both numbers or not at all
                            has_n = re.search(rf"\b{dd.get('n')}\b", bare) is not None
                            has_pop = re.search(rf"\b{dd.get('population')}\b", bare) is not None or (
                                # D-048: the population one sentence back, anchored on the directory's
                                # name — the split before a digit turned "which holds 22 rooms. 8 of
                                # the 27 … sit there" into two sentences, and a denominator a name
                                # anchors one sentence earlier is not a base rate
                                bool(prev_sent)
                                and re.search(
                                    rf"(?<![\w/@.-]){re.escape(dd['dir'])}(?![\w/])",
                                    BRACKET.sub("", prev_sent),
                                )
                                is not None
                                and re.search(
                                    rf"\b{dd.get('population')}\b", BRACKET.sub("", prev_sent)
                                )
                                is not None
                            )
                            if has_n != has_pop or (
                                not dd.get("holds_third") and not (has_n and has_pop)
                            ):
                                out.append(
                                    Violation(
                                        "R15-composition",
                                        i,
                                        sent[:160],
                                        f"{dd['dir']} is named for {cf['feature']} without both its share ({dd.get('n')}) and its rooms ({dd.get('population')}) in the sentence; a share carries its denominator",
                                    )
                                )
                for cf in cited:
                    if not cf:
                        continue
                    dd = cf.get("dominant_dir") or {}
                    for v in set(cf.get("by_wing", {}).values()) | {
                        dd.get("n"),
                        dd.get("population"),
                    }:
                        if v is None or v in entitled:
                            continue
                        sent_allowed.discard(v)
                        if re.search(rf"\b{v}\b", bare):
                            out.append(
                                Violation(
                                    "R16-restatement",
                                    i,
                                    sent[:160],
                                    (
                                        f"{v} is {cf['feature']}'s count in the largest wing ({largest_wing}), which is the register's; say a minority wing's count or leave it"
                                        if v == cf.get("by_wing", {}).get(largest_wing)
                                        else (
                                            f"{v} is {cf['feature']}'s count in a wing or directory this "
                                            f"sentence does not name (its wing counts are {cf.get('by_wing')}); "
                                            "name the place that holds it or leave the number to the register"
                                        )
                                    ),
                                )
                            )
            for rid in room_ids:
                if rid in room_metrics and _mentions(sent, rid):
                    sent_allowed.update(v for v in room_metrics[rid].values() if isinstance(v, int))
            for n in INTEGER.findall(stripped):
                if int(n) not in sent_allowed:
                    out.append(
                        Violation(
                            "R3-number",
                            i,
                            sent[:160],
                            f"number {n} is not in the facts sheet, or its feature is not cited in this sentence",
                        )
                    )
            for span, val in _spelled_numbers(stripped):
                if span.lower() == "one":
                    continue  # the determiner, not a measurement (D-032 addendum)
                if re.search(rf"\b{re.escape(span)}\s+or\s+more\b", stripped, re.IGNORECASE):
                    continue  # "two or more" is the sheet's own unit phrase for co_located_rooms (D-037)
                if val not in sent_allowed:
                    out.append(
                        Violation(
                            "R3-number",
                            i,
                            sent[:160],
                            f"number '{span}' ({val}) is not in the facts sheet, or its feature is not cited in this sentence",
                        )
                    )
    # R9 (D-036): two diagnostic features whose room sets coincide or nest are one set of rooms;
    # some sentence must name both features together (the sheet's `overlaps` says which)
    sentences_all = [snt for p in _paragraphs(text) for snt in SENTENCE.split(p)]
    for ov in facts_doc.get("overlaps") or []:
        if not ov.get("diagnostic", True):
            continue  # D-044: a decorative pair is the register's; prose never diagnoses it (R4)
        # D-039: with the register on the page the obligation to name the pair is met there; the
        # refusals (an identity noun on a nesting, two profiles read as agreeing) still bind the prose
        fa, fb = ov["a"].split("/")[-1], ov["b"].split("/")[-1]
        together = any(
            re.search(rf"\b{re.escape(fa)}\b", snt) and re.search(rf"\b{re.escape(fb)}\b", snt)
            for snt in sentences_all
        )
        if not together and not register:
            out.append(
                Violation(
                    "R9-overlap",
                    0,
                    "",
                    f"{ov['a']} and {ov['b']} mark {'the same' if ov['relation'] == 'identical' else 'nested'} rooms ({ov['n']}); no sentence names both",
                )
            )
        # R13 (D-037): an identity between predicates that differ is a conjunct that did no work,
        # and the sentence that names the pair says which
        pair_sents = [
            snt
            for snt in sentences_all
            if re.search(rf"\b{re.escape(fa)}\b", snt) and re.search(rf"\b{re.escape(fb)}\b", snt)
        ]
        if together and ov["relation"] == "within":
            # D-038: a nesting is not an identity — the sentence names the rooms outside and no identity noun
            n_out = ov.get("n_outside")
            asserts_identity = any(
                m
                for snt in pair_sents
                for m in IDENTITY_NOUN.finditer(snt.lower())
                # D-046 addendum: "two sets of rooms, not one finding" denies the identity
                if not re.search(
                    r"\b(?:not|never|rather than|instead of)\b[^.;]{0,20}$",
                    snt.lower()[: m.start()],
                )
            )
            if asserts_identity or not any(
                n_out is not None and re.search(rf"\b{n_out}\b", BRACKET.sub("", snt))
                for snt in pair_sents
            ):
                out.append(
                    Violation(
                        "R13-inert",
                        0,
                        "",
                        f"{ov['a']} sits within {ov['b']}: the sentence naming both states the {n_out} rooms outside and does not call them one set",
                    )
                )
        if together and ov["relation"] == "identical" and ov.get("shared_predicate"):
            # D-038: the same predicate under two profiles is one measurement; the sentence says so
            if not register and not any(
                re.search(r"\bpredicate\b", snt.lower()) for snt in pair_sents
            ):
                out.append(
                    Violation(
                        "R13-inert",
                        0,
                        "",
                        f"{ov['a']} and {ov['b']} carry the same predicate: the sentence naming both must say so, not read them as two measurements agreeing",
                    )
                )
        inert = ov.get("inert_terms") or []
        if together and ov["relation"] == "identical" and inert:
            sigs = sorted({re.split(r"\s*(?:>=|<=|==|>|<)\s*", t)[0].strip() for t in inert})
            said = any(
                re.search(rf"\b{re.escape(fa)}\b", snt)
                and re.search(rf"\b{re.escape(fb)}\b", snt)
                and all(re.search(rf"\b{re.escape(sig)}\b", snt) for sig in sigs)
                for snt in sentences_all
            )
            if not said and not register:
                out.append(
                    Violation(
                        "R13-inert",
                        0,
                        "",
                        f"{ov['a']} and {ov['b']} draw one set; the sentence naming both must say that {', '.join(sigs)} excludes nothing here",
                    )
                )
    # R15 (D-037): a feature whose rooms sit one third or more in one directory names that directory
    # in a sentence that cites the feature — and R10 then requires a cited room inside it, so the
    # exemplars cannot be drawn away from the set's composition
    for f in facts_doc["features"]:
        dd = f.get("dominant_dir") or {}
        if register or not f["diagnostic"] or not dd or f["count"] < 6 or dd["n"] * 3 < f["count"]:
            continue
        key, name = f"{f['profile']}/{f['feature']}", f["feature"]
        pop = dd.get("population")
        named_dir = any(
            any(c in (key, name) for c, _n, _r in _citations(snt))
            and re.search(rf"(?<![\w/@.-]){re.escape(dd['dir'])}(?![\w/])", snt)
            and (pop is None or re.search(rf"\b{pop}\b", BRACKET.sub("", snt)))
            for snt in sentences_all
        )
        if not named_dir:
            out.append(
                Violation(
                    "R15-composition",
                    0,
                    "",
                    f"{key}: {dd['n']} of its {f['count']} rooms sit in {dd['dir']}, which holds {pop} rooms; no sentence citing it names that directory with its population (D-038: a share carries its denominator)",
                )
            )
    # R4b (D-038): the decorative disclosure says why — the ungrounded signal from decorative_reason
    for f in facts_doc["features"]:
        if register or not f["decorative"]:
            continue
        reason = f.get("decorative_reason") or ""
        sigs = [w for w in re.findall(r"[a-z_]+", reason) if w in _SIGNAL_LIKE]
        if not sigs:
            continue
        key, name = f"{f['profile']}/{f['feature']}", f["feature"]
        cited = [
            snt for snt in sentences_all if any(c in (key, name) for c, _n, _r in _citations(snt))
        ]
        if cited and not any(
            re.search(rf"\b{re.escape(sig)}\b", snt) for snt in cited for sig in sigs
        ):
            out.append(
                Violation(
                    "R4-decorative",
                    0,
                    "",
                    f"{key} is decorative because {reason}; no sentence citing it names {', '.join(sigs)}",
                )
            )
    # R5 disclosure: a consequence-implying name carries its position name in the paragraph
    # where it is first used (a disclosure in paragraph 1 does not license paragraph 9)
    low_all = text.lower()
    used_consequence_names |= set(first_use)
    for feat in sorted(used_consequence_names):
        pos = (by_feature[feat].get("position_name") or "").lower()
        # tolerate plurals and hyphen/space variation: "high-load hub" ~ "high load hubs"
        words = [re.escape(w) for w in re.split(r"[\s-]+", pos) if w]
        pattern = r"[\s-]+".join(w + r"(?:s|es)?" for w in words) if words else None
        where = first_use.get(feat, (0, low_all))
        if pattern and not re.search(pattern, where[1]):
            out.append(
                Violation(
                    "R5-disclosure",
                    where[0],
                    feat,
                    f"'{feat}' is first used here without its position name ('{pos}') in the same paragraph (D-004 Q3)",
                )
            )
    # R7 decorative count must be stated when there are decorative features — met by the register
    # when the page carries one (D-039)
    dec_count = facts_doc["decorative"]["count"]
    prose_only = BRACKET.sub("", text)
    in_prose = {int(d) for d in INTEGER.findall(prose_only)} | {
        v for _, v in _spelled_numbers(prose_only)
    }
    stated = dec_count in in_prose
    diag = facts_doc["diagnostic_count"]
    if not register and diag not in in_prose:
        out.append(
            Violation(
                "R7-counts",
                0,
                "",
                f"the brief must state the diagnostic-mark count ({diag}, all profiles) beside the population",
            )
        )
    if not register and dec_count and not stated:
        out.append(
            Violation(
                "R7-decorative-count",
                0,
                "",
                f"the brief must state the decorative count ({facts_doc['decorative']['count']}) where a reader sees it (mapper §3)",
            )
        )
    return out


# ---------------------------------------------------------------- 2. the generator

# The model-written reading, its prompt (SYSTEM), its input message and the Anthropic generator
# lived here from D-027 to D-049. Eleven hostile seatings (tracker runs 17-28) found the reading
# reciting the register; everything it could add was a field. The page is rendered by code; the
# lint below stays for a hand-written draft (--draft). The prompt and generator are in the history
# at 0d8f5c0.


# ---------------------------------------------------------------- the run


NL = "\n"


# D-043: the note is generated from the same constants the renderer computes with
RELATION_MIN_ROOMS = 3  # a set of fewer rooms is inside anything that contains it (D-041)
MOST_MARKED_ROOMS = 5  # the sheet lists this many of the rooms carrying the most marks (D-048)
ROOT_SCOPE = "package.json"  # D-056: a scope is named by its manifest path — the root's is the bare file; "(root)" is the wing and no scope can share a wing's name
# D-055: the ordering the most-marked table uses, said once — the sheet's unit gloss kept "then marks"
# after D-054 dropped it from the key, and the lead said the opposite on the same page
MOST_MARKED_ORDER = "ordered by sets (a feature under two profiles, or two features drawing one set, is one set), then by path — marks (one per feature per profile) are shown and order nothing, since within a tier they differ only by the double count the register discounts"
DIRECTORY_MIN_ROOMS = 6  # below this no directory is placed (D-040)
DIRECTORY_SHARE = 3  # a directory is shown when it holds a third or more (R15)
# D-043: the record a predicate reads, named beside each position so the gloss covers every row.
# D-053: raw signals only — a blend's records are derived from the inputs config.ALLOWED_INPUTS
# declares for it (the fourteenth seating found bug_pressure_index filed under "edit record" while
# it reads recency, the clock, at 0.2; D-048 had fixed load_index alone, by hand)
_RECORDS: list[tuple[str, tuple[str, ...]]] = [
    ("import graph", ("fan_in", "fan_out", "centrality", "fan_in_nonzero")),
    # D-052: the declared entry is read from package.json (D-029), not from the import graph —
    # the thirteenth seating found "declared package entry (import graph)" on the register
    ("package manifest", ("is_package_entry",)),
    ("clock", ("age_days", "last_touched_days", "blame_age_median", "recent_commit_share")),
    ("test graph", ("test_fan_in", "reinforcement_index", "has_sibling_test")),
    ("edit record", ("commit_count", "churn_lines", "fix_count", "revert_count", "author_count")),
    ("size", ("size_loc", "nesting_proxy")),
]
# D-053: the raw signal each declared blend input is read from (derived.compute_indices)
_INPUT_SIGNAL: dict[str, str] = {
    "fan_in_nonzero": "fan_in",
    "inv_fan_out": "fan_out",
    "size_loc": "size_loc",
    "recency": "last_touched_days",
    "inv_recent_commit_share": "recent_commit_share",
    "fix_count_nonzero": "fix_count",
    "fix_ratio": "fix_count",
}


def records_of_signal(sig: str) -> list[str]:
    """D-053: the records a signal is read from — a raw signal's record, or every record of a
    blend's declared inputs (config.ALLOWED_INPUTS), so the lexicon cannot omit an input by hand."""
    from .config import ALLOWED_INPUTS

    if sig in ALLOWED_INPUTS:
        out: list[str] = []
        for inp in ALLOWED_INPUTS[sig]:
            for r in records_of_signal(_INPUT_SIGNAL.get(inp, inp)):
                if r not in out:
                    out.append(r)
        return [name for name, _ in _RECORDS if name in out]
    return [name for name, sigs in _RECORDS if sig in sigs]


def sets_per_room(features) -> dict[str, int]:
    """D-052: for every marked room, the number of distinct diagnostic room sets that contain it —
    one computation for the header's building count, the co-location count and the most-marked
    table, so no two cells can count sets two ways."""
    feats = [e for e in features if e["diagnostic"]]
    ids = {id(e): frozenset(e["rooms"]) for e in feats}
    rooms = {r for e in feats for r in e["rooms"]}
    return {r: len({ids[id(e)] for e in feats if r in ids[id(e)]}) for r in rooms}


def distinct_sets(features) -> int:
    """D-052: the number of distinct room sets the diagnostic features draw (an empty set is none)."""
    return len({frozenset(e["rooms"]) for e in features if e["diagnostic"] and e["rooms"]})


def co_located(features) -> int:
    """D-052: rooms under two or more distinct diagnostic sets."""
    return sum(1 for v in sets_per_room(features).values() if v >= 2)


def most_marked(features) -> list[dict[str, Any]]:
    """D-048: the rooms carrying the most diagnostic marks, each with every diagnostic feature that
    marks it. D-050: ordered by distinct sets (two features drawing one set of rooms, or one
    predicate under two profiles, mark a room once in this count — the unit the header uses for
    the building), then by marks, then by path; at most MOST_MARKED_ROOMS; each row carries the
    rooms at its own sets count. D-052: a room under one set is not listed (the floor is sets, as
    the co-location count is), and each row says how many rooms of its tier the list carries — the
    thirteenth seating found a tier of four listed as three under a lead that said "first by path"
    of every row. A feature under two profiles is named with its profile so names count marks."""
    feats = [e for e in features if e["diagnostic"]]
    twice = {e["feature"] for e in feats if sum(1 for x in feats if x["feature"] == e["feature"]) > 1}
    marks: dict[str, int] = {}
    for e in feats:
        for r in e["rooms"]:
            marks[r] = marks.get(r, 0) + 1
    set_ids = {id(e): frozenset(e["rooms"]) for e in feats}
    sets = sets_per_room(feats)
    at_count: dict[int, int] = {}
    for r, n in sets.items():
        if n >= 2:
            at_count[n] = at_count.get(n, 0) + 1
    # D-054 (fifteenth seating): within a tier of equal sets, marks differ only by the double count
    # the header discounts (a set under two profiles); on eslint's tier of 13 at six sets the marks
    # key was foundation's two profiles and nothing else. Sets, then path.
    top = [
        (r, n) for r, n in sorted(marks.items(), key=lambda kv: (-sets[kv[0]], kv[0])) if sets[r] >= 2
    ][:MOST_MARKED_ROOMS]
    listed: dict[int, int] = {}
    for r, _ in top:
        listed[sets[r]] = listed.get(sets[r], 0) + 1
    # D-060: the rooms a partly listed tier leaves out, by name — the control seating found the cut
    # room of a four-room tier was the one of a different kind, reachable only by recomputation
    shown = {r for r, _ in top}
    unlisted = {c: sorted(r for r, n in sets.items() if n == c and r not in shown) for c in at_count}
    return [
        {
            "room": r,
            "sets": sets[r],
            "marks": n,
            "rooms_at_this_count": at_count[sets[r]],
            "listed_at_this_count": listed[sets[r]],
            "unlisted": unlisted.get(sets[r], []),
            "features": sorted(
                (f"{e['profile']}/{e['feature']}" if e["feature"] in twice else e["feature"])
                for e in feats
                if r in set_ids[id(e)]
            ),
        }
        for r, n in top
    ]


def _case_holds(case: str, metrics: dict[str, Any]) -> bool:
    """D-060: a caveat_case is a conjunction of literal terms over raw metrics."""
    from .mapper.ruleset import parse_predicate

    for t in parse_predicate(case):
        v = metrics.get(t.signal)
        if v is None:
            return False
        x = float(v)
        ok = {"==": x == t.value, ">=": x >= t.value, "<=": x <= t.value, ">": x > t.value, "<": x < t.value, "!=": x != t.value}.get(t.op)
        if not ok:
            return False
    return True


def _unresolved_text(facts_doc: dict[str, Any]) -> str:
    """D-064: the unresolved imports by kind, and what they do to the test graph."""
    u = facts_doc.get("unresolved_by_kind")
    if not u or not u.get("sampled"):
        return ""
    n, t, a = u["sampled"], u["from_test_files"], u["alias_shaped"]
    of = "" if n == facts_doc.get("unresolved_imports") else f" (of {n} sampled)"
    kinds = []
    kinds.append(f"{'all ' if t == n else ''}{t} from test files" if t else "none from test files")
    if a:
        kinds.append(f"{'all ' if a == n else ''}{a} alias-shaped (a path the resolver should have placed in-repo)")
    tail = f"; test_fan_in on the rooms those {t} aim at is a lower bound" if t else ""
    return f" ({', '.join(kinds)}{of}{tail})"


def _alias_state_text(facts_doc: dict[str, Any]) -> str:
    """D-065: what the resolver was given for path aliases, said where the unresolved count is read.
    A malformed tsconfig is the substrate's caveat, rendered; an alias count is the positive fact
    (0.5.0 substrates carry it; an older sheet says nothing rather than guessing)."""
    bad = facts_doc.get("tsconfig_malformed")
    if bad:
        return f" The repository's tsconfig.json could not be read ({bad}), so no path alias reached the resolver and an alias-shaped import is unresolved for that reason."
    n = facts_doc.get("tsconfig_aliases")
    if n is None:
        return ""
    if n:
        return f" The resolver was given the {n} path-alias pattern{'s' if n != 1 else ''} tsconfig.json declares."
    return " No tsconfig.json path alias was read (none declared, or no tsconfig.json)."


# D-070: what each kind's regex reads, in words a reader can hold a file against; tested against the
# regexes on the sheet (`test_kind_convention_words_match_the_regexes`)
KIND_CONVENTION_WORDS = {
    "config": "a tool's configuration by basename — `*rc.*`, `*.config.*` or `*.conf.*` — at its package's root",
    "migration": "any file under a `migration/` or `migrations/` directory",
    "placeholder": "a file that is an empty export once comments are stripped",
}


def _kinds_rule_text(facts_doc: dict[str, Any]) -> str:
    """D-067: the ruleset's kind exclusion, in the population rule. D-070 (the ninth control): "config"
    was a word on the page and a regex in the instrument — the registry's one root room, knexfile.ts,
    is a config by role and a room by the convention; the rule states what each kind reads."""
    ks = facts_doc.get("excluded_kinds") or []
    if not ks:
        return ""
    conv = facts_doc.get("kind_conventions") or {}
    if conv:
        defs = "; ".join(f"{k}: {KIND_CONVENTION_WORDS.get(k, 'as the substrate reads it')}" for k in ks)
        return f", and not a {' or '.join(ks)} file (kinds the ruleset does not count as rooms, each read by a declared convention and nothing else — {defs})"
    return f", and not a {' or '.join(ks)} file (kinds the ruleset does not count as rooms)"


def _kinds_count_text(facts_doc: dict[str, Any]) -> str:
    """D-067: what the exclusion removed, counted per kind, beside the test-file count."""
    ebk = facts_doc.get("excluded_by_kind") or {}
    if not facts_doc.get("excluded_kinds"):
        return ""
    total = sum(ebk.values())
    if not total:
        return "; no file of a kind the ruleset does not count is in the tree"
    parts = ", ".join(f"{k} {v}" for k, v in ebk.items() if v)
    return f"; the {total} file{'s' if total != 1 else ''} of a kind the ruleset does not count ({parts}) {'are' if total != 1 else 'is'} in the graph and not a room"


def _package_name_text(facts_doc: dict[str, Any]) -> str:
    """D-066: the imports that name this repository's own package (a cookbook example under a
    `file:../..` manifest; a fixture importing "typeorm") — placed at the package's declared entry
    by substrate 0.6.0, and counted external before it. Said beside the external count they left."""
    n = facts_doc.get("package_name_imports")
    if not n:
        return ""
    names = facts_doc.get("package_names") or []
    named = f" ({', '.join(names)})" if names and len(names) <= 3 else (f" ({len(names)} names)" if names else "")
    return f" {n} import{'s' if n != 1 else ''} name a package this repository declares{named} and resolve to its entry{_from_tests_text(facts_doc.get('package_name_from_tests'), n)}."


def _from_tests_text(k: int | None, n: int | None) -> str:
    """D-068: the test-file split every import-graph count carries (D-062), on the legend's counts too."""
    if k is None or not n:
        return ""
    return f" ({'all ' if k == n else ''}{k} from test files)" if k else " (none from test files)"


def _wing_scopes_text(wing: str, n_feat: int, n_wing: int, counts: dict[str, int]) -> str:
    """D-068: a wing of more than one scope says how many hold the feature (D-066), and names them at
    two or fewer — "(in 1 of the wing's 2 scopes)" withheld the one word that located the rooms."""
    if n_wing <= 1:
        return ""
    if counts and len(counts) <= 2:
        if len(counts) == 1:
            return f" (all in {next(iter(counts))})"
        return " (" + ", ".join(f"{k} {v}" for k, v in counts.items()) + ")"
    return f" (in {n_feat} of the wing's {n_wing} scopes)"


# D-070: a case predicate whose input is a convention file the tree may not declare; the sheet says
# whether the file exists (substrate 0.10.0), and "0 of N here" becomes "nothing to read" when it does not
CASE_INPUT_FILES = {"last_touch_blame_ignored": ("blame_ignore_revs", ".git-blame-ignore-revs")}


def _case_count_text(case: str | None, n: int, m: int, facts_doc: dict[str, Any]) -> str:
    """D-070 (the ninth control, on the registry): the clock caveat's case read "0 of 34 here were last
    touched by a commit the repository's .git-blame-ignore-revs disowns" on a tree with no such file —
    a count of what an absent file says, beside a tie of 18 rooms at one 131-file commit. When the
    case's input file is absent the count says so instead of 0."""
    for sig, (field, fname) in CASE_INPUT_FILES.items():
        if case and sig in case:
            info = facts_doc.get(field)
            if isinstance(info, dict) and info.get("present") is False:
                return f"none of the {m} — the tree has no {fname} at this commit —"
    return f"{n} of {m} here"


def _case_label(caveat: str) -> str:
    """D-068: the clause a caveat's `{case}` count belongs to — the words after the placeholder up to
    the closing parenthesis ("have no importer", "are declared package entries")."""
    if "{case}" not in caveat:
        return ""
    tail = caveat.split("{case}", 1)[1]
    return tail.split(")", 1)[0].strip()


def _agree(n: int, label: str) -> str:
    """D-072 (the eleventh control's R5): "(1 have no importer)" — a case label's leading verb agrees with its count."""
    if n == 1:
        head, _, rest = label.partition(" ")
        head = {"have": "has", "are": "is", "were": "was"}.get(head, head)
        return f"{head} {rest}".strip()
    return label


def _test_convention_text(facts_doc: dict[str, Any]) -> str:
    """D-068: the term "the test convention" defined from the substrate's effective config (0.8.0)."""
    globs = facts_doc.get("test_globs") or []
    if not globs:
        return ""
    return f" (a path matching {', '.join(f'`{g}`' for g in globs)})"


def _centrality_illustration(feats: dict[str, Any], nodes: dict[str, Any], population_ids: set[str]) -> dict[str, Any] | None:
    """D-068: the legend illustrated "four well-placed importers can outrank thirteen" with the
    registry's D-063 pair as a literal on every page; the illustration is this sheet's own pair —
    the hub room with the fewest importers and the non-hub room with the most — or nothing."""
    from .mapper.ruleset import parse_predicate

    if not nodes:
        return None
    hub = None
    for e in feats.values():
        terms = parse_predicate(str(e.get("predicate") or ""))
        if len(terms) == 1 and terms[0].signal == "centrality" and terms[0].percentile is not None and not e.get("decorative"):
            hub = e
            break
    if hub is None or not hub["rooms"]:
        return None
    members = set(hub["rooms"])

    def fi(r: str) -> int:
        return int(((nodes.get(r) or {}).get("metrics") or {}).get("fan_in", 0) or 0)

    lo = min(sorted(members), key=fi)
    others = sorted(population_ids - members)
    if not others:
        return None
    hi = max(others, key=fi)
    if fi(lo) >= fi(hi):
        return None
    return {"hub_room": lo, "hub_fan_in": fi(lo), "other_room": hi, "other_fan_in": fi(hi), "feature": hub["feature"]}


def _centrality_illustration_text(facts_doc: dict[str, Any]) -> str:
    ill = facts_doc.get("centrality_illustration")
    if not ill:
        return ""
    return f", so a room with {ill['hub_fan_in']} well-placed importer{'s' if ill['hub_fan_in'] != 1 else ''} can outrank one with {ill['other_fan_in']} (here {ill['hub_room']} at {ill['hub_fan_in']} is a {ill['feature']} and {ill['other_room']} at {ill['other_fan_in']} is not)"


def _unresolved_by_kind(substrate: dict[str, Any] | None, nodes: dict[str, Any]) -> dict[str, int] | None:
    """D-064: the unresolved imports the substrate sampled, by the kind the page can state without
    resolving them itself — how many come from test files, and how many are alias-shaped (a
    specifier the resolver should have placed in-repo: `@/x`, `~/x`)."""
    if not substrate:
        return None
    samples = ((substrate.get("caveats") or {}).get("unresolved_import_samples")) or []
    if not samples:
        return {"sampled": 0, "from_test_files": 0, "alias_shaped": 0} if (substrate.get("summary") or {}).get("unresolved_imports") is not None else None
    from_tests = sum(1 for x in samples if ((nodes.get(x.get("from")) or {}).get("metrics") or {}).get("is_test"))
    alias = sum(1 for x in samples if str(x.get("specifier", "")).startswith(("@/", "~/", "#")))
    return {"sampled": len(samples), "from_test_files": from_tests, "alias_shaped": alias}


def _term_ties(e: dict[str, Any], nodes: dict[str, Any], population_ids: set[str]) -> dict[str, int]:
    """D-069: for every ranked term of a conjunctive predicate, how many of the population's rooms sit
    exactly at the value the rank resolved to."""
    from .mapper.ruleset import parse_predicate

    terms = parse_predicate(str(e.get("predicate") or ""))
    ranked = [t for t in terms if t.percentile is not None]
    if len(terms) < 2 or not ranked or not nodes:
        return {}
    out: dict[str, int] = {}
    for t in ranked:
        cut = (e.get("thresholds") or {}).get(t.render())
        if not isinstance(cut, (int, float)):
            continue
        n = 0
        for r in population_ids:
            node = nodes.get(r) or {}
            v = (node.get("metrics") or {}).get(t.signal)
            if v is None:
                v = ((node.get("derived") or {}).get("indices") or {}).get(t.signal)
            if isinstance(v, (int, float)) and abs(float(v) - float(cut)) < 1e-9:
                n += 1
        out[t.render()] = n
    return out


def _term_reach(e: dict[str, Any], nodes: dict[str, Any], population_ids: set[str]) -> dict[str, int]:
    """D-072: for every ranked term of a predicate, single or conjunctive, how many of the population's
    rooms satisfy that term alone at the value the rank resolved to."""
    import operator

    from .mapper.ruleset import parse_predicate

    ops = {">=": operator.ge, ">": operator.gt, "<=": operator.le, "<": operator.lt}
    out: dict[str, int] = {}
    if not nodes:
        return out
    for t in parse_predicate(str(e.get("predicate") or "")):
        cut = (e.get("thresholds") or {}).get(t.render())
        if t.percentile is None or t.op not in ops or not isinstance(cut, (int, float)):
            continue
        n = 0
        for r in population_ids:
            node = nodes.get(r) or {}
            v = (node.get("metrics") or {}).get(t.signal)
            if v is None:
                v = ((node.get("derived") or {}).get("indices") or {}).get(t.signal)
            if isinstance(v, (int, float)) and ops[t.op](float(v), float(cut)):
                n += 1
        out[t.render()] = n
    return out


def _quantile_reach_text(predicate: str, thresholds: dict[str, Any] | None, term_reach: dict[str, int] | None, population: int | None) -> str:
    """D-072: the position name's quantile word ("the upper quartile", "the median") is a share; where
    the rank resolved to a value more than twice that share of the population reaches, the position
    cell says what the word resolved to here. The word is the ruleset's and stays."""
    from .mapper.ruleset import parse_predicate

    if not term_reach or not population:
        return ""
    parts = []
    for t in parse_predicate(str(predicate or "")):
        n = term_reach.get(t.render())
        cut = (thresholds or {}).get(t.render())
        if t.percentile is None or n is None or not isinstance(cut, (int, float)):
            continue
        nominal = 100 - t.percentile if t.op in (">=", ">") else t.percentile
        share = 100.0 * n / population
        if share > 2 * nominal:
            parts.append(f"p{t.percentile} on {t.signal} resolves to {cut:g}, which {n} of {population} rooms reach ({share:.0f}%)")
    return (" — here " + "; ".join(parts)) if parts else ""


def _tie_touch_files(e: dict[str, Any], nodes: dict[str, Any]) -> int | None:
    """D-069: on a single-pNN clock row whose rooms tie at the cutoff, the breadth of the commit they
    share (substrate 0.9.0 `last_touch_commit_files`) — one value when the tie is one commit, else None."""
    from .mapper.ruleset import parse_predicate

    terms = parse_predicate(str(e.get("predicate") or ""))
    if len(terms) != 1 or terms[0].percentile is None or terms[0].signal != "last_touched_days" or not nodes:
        return None
    cut = (e.get("thresholds") or {}).get(str(e["predicate"]).strip())
    if not isinstance(cut, (int, float)) or (e.get("at_cutoff") or 0) < 2:
        return None
    vals = set()
    for r in e["rooms"]:
        m = (nodes.get(r) or {}).get("metrics") or {}
        v = m.get("last_touched_days")
        if isinstance(v, (int, float)) and abs(float(v) - float(cut)) < 1e-9:
            vals.add(m.get("last_touch_commit_files"))
    vals.discard(None)
    return next(iter(vals)) if len(vals) == 1 else None


# D-071: each blend input in words a reader can hold against the row's records; every input is a
# rank in this repository (derived.ecdf_percentiles), so the words say rank, not value
INDEX_INPUT_WORDS = {
    "fan_in_nonzero": "fan_in's rank among the rooms anything imports (0 for a room nothing imports)",
    "centrality": "centrality's rank",
    "inv_fan_out": "(1 − fan_out's rank)",
    "size_loc": "size's rank",
    "commit_count": "commit count's rank",
    "recency": "(1 − last_touched_days' rank)",
    "revert_count": "revert count's rank",
    "churn_lines": "churned lines' rank",
    "fix_count": "fix count's rank",
    "fix_count_nonzero": "fix count's rank among the rooms with a fix",
    "fix_ratio": "the share of commits that are fixes",
    "age_days": "age's rank",
    "last_touched_days": "last_touched_days' rank",
    "inv_recent_commit_share": "(1 − recent commit share)",
    "nesting_proxy": "nesting's rank",
    "fan_out": "fan_out's rank",
}


def _index_weights(feats: dict[str, Any], substrate: dict[str, Any] | None) -> dict[str, dict[str, float]]:
    """D-071: the tuned blends any feature on the page reads, keyed by index, from the substrate's
    effective config (the fingerprint's preimage, 0.8.0)."""
    from .mapper.ruleset import parse_predicate

    weights = ((((substrate or {}).get("repo") or {}).get("effective_config") or {}).get("weights") or {})
    out: dict[str, dict[str, float]] = {}
    for e in feats.values():
        for t in parse_predicate(str(e.get("predicate") or "")):
            if t.signal in weights:
                out[t.signal] = {k: float(v) for k, v in sorted(weights[t.signal].items(), key=lambda kv: (-kv[1], kv[0]))}
    return dict(sorted(out.items()))


def _index_zeroed(index_weights: dict[str, dict[str, float]]) -> dict[str, list[str]]:
    """D-075 (the thirteenth skimmer): bug_pressure_index's exclusion reason says its tuned weights give
    fix history zero, and the legend listed only the weighted inputs; the inputs a blend allows
    (config.ALLOWED_INPUTS) that the tuning weighted zero or dropped."""
    from .config import ALLOWED_INPUTS

    out: dict[str, list[str]] = {}
    for idx, w in index_weights.items():
        z = sorted(k for k in ALLOWED_INPUTS.get(idx, ()) if not w.get(k))
        if z:
            out[idx] = z
    return out


def _index_legend_lines(facts_doc: dict[str, Any]) -> str:
    """D-071: a legend line per blend the page reads — its inputs, in rank words, and the weights."""
    out = ""
    for idx, w in (facts_doc.get("index_weights") or {}).items():
        terms = " + ".join(f"{v:g} × {INDEX_INPUT_WORDS.get(k, k)}" for k, v in w.items())
        zeroed = (facts_doc.get("index_zeroed") or {}).get(idx) or []
        zero_text = f"; the tuning weighted 0: {', '.join(INDEX_INPUT_WORDS.get(k, k) for k in zeroed)}" if zeroed else ""
        out += f"- **{idx}** — a blend the ruleset reads as one signal, each input a rank in this repository's own population: {terms} (the tuned weights, D-009; the substrate's effective config){zero_text}." + NL
    return out


SCOPE_FLOOR = 30  # the mapper's population floor (D-034, engine.MIN_POPULATION): a scope below it is not named alone


def _scope_composition(rooms: list[str], scope_of: Any, scope_sizes: dict[str, int], population: int) -> list[dict[str, Any]]:
    """D-077 (scope-calibration-spec.md, reviewed): where the population pools package scopes, each scope of
    SCOPE_FLOOR or more rooms that holds over twice or under half its share of the population's rooms among
    a feature's rooms — the feature's count in it and its size. Pooling's effect stated as composition: a
    counterfactual count under a split population is quota arithmetic (the data-science review, run 65)."""
    if len(scope_sizes) < 2 or len(rooms) < DIRECTORY_MIN_ROOMS or not population:
        return []
    have: dict[str, int] = {}
    for r in rooms:
        have[scope_of(r)] = have.get(scope_of(r), 0) + 1
    out = []
    for sc, size in sorted(scope_sizes.items(), key=lambda kv: (-kv[1], kv[0])):
        if size < SCOPE_FLOOR:
            continue
        n = have.get(sc, 0)
        share, expected = n / len(rooms), size / population
        if share > 2 * expected or share < expected / 2:
            out.append({"scope": sc, "n": n, "scope_rooms": size})
    return out


def _scope_composition_text(comp: list[dict[str, Any]], count: int, population: int) -> str:
    """D-077: "; pooled scopes: 27 of these 27 in package.json, which holds 65 of the 187 rooms"."""
    if not comp:
        return ""
    return "; pooled scopes: " + "; ".join(f"{c['n']} of these {count} in {c['scope']}, which holds {c['scope_rooms']} of the {population} rooms" for c in comp)


def _stance_case_text(facts_doc: dict[str, Any]) -> str:
    """D-070: the case the system spec's disclosure names, with this page's rooms at it."""
    sc = facts_doc.get("stance_case")
    if not sc:
        return ""
    rooms = sc.get("rooms") or []
    # D-072 (the eleventh control): "long-untouched and high-load at once" sat inside the attribution to
    # the system spec, whose case is one condition; the narrowing is D-070's, and on typeorm it named 6
    # of the 70 long-untouched rooms. The spec's case in its words; the narrowing labelled as the page's
    n_u = sc.get("untouched_count")
    head = (
        " The norm's known false positive, in the system spec's words (stance disclosure): a finished, correct, stable utility that nobody has touched in three years. "
        f"The page cannot tell finished from abandoned; the case sits at the long-untouched position — here {sc['untouched']}"
        + (f", {n_u} room{'s' if n_u != 1 else ''}" if n_u is not None else "")
        + f". A narrowing that is this page's, not the spec's (D-070): the long-untouched rooms that are also high-load ({sc['loaded']}) — "
    )
    if not rooms:
        return head + "no long-untouched room is also high-load."
    listed = "; ".join(f"{r['room']} ({r['lines']} line{'s' if r['lines'] != 1 else ''}, {r['fan_in']} importer{'s' if r['fan_in'] != 1 else ''}, {r['test_fan_in']} from test files)" for r in rooms)
    return head + f"{len(rooms)} room{'s' if len(rooms) != 1 else ''} — {listed} — which the page places and does not judge."


def _stance_case(feats: dict[str, Any], nodes: dict[str, Any]) -> dict[str, Any] | None:
    """D-070: the rooms at the stance disclosure's named case — in a long-untouched set (not ◌)
    (a `last_touched_days >= pNN` predicate) and a high-load set (`load_index >= pNN`) at
    once — with size and importers. None when the sheet has no such pair of features."""
    from .mapper.ruleset import parse_predicate

    def single(e: dict[str, Any], sig: str) -> bool:
        terms = parse_predicate(str(e.get("predicate") or ""))
        return len(terms) == 1 and terms[0].signal == sig and terms[0].percentile is not None and terms[0].op in (">=", ">")

    untouched = [e for e in feats.values() if not e["decorative"] and single(e, "last_touched_days")]
    loaded = [e for e in feats.values() if not e["decorative"] and single(e, "load_index")]
    if not untouched or not loaded:
        return None
    u, l = untouched[0], loaded[0]
    rooms = sorted(set(u["rooms"]) & set(l["rooms"]))
    return {
        "untouched": u["feature"],
        "loaded": l["feature"],
        "untouched_count": len(u["rooms"]),
        "rooms": [
            {
                "room": r,
                "lines": ((nodes.get(r) or {}).get("metrics") or {}).get("size_loc"),
                "fan_in": ((nodes.get(r) or {}).get("metrics") or {}).get("fan_in"),
                "test_fan_in": ((nodes.get(r) or {}).get("metrics") or {}).get("test_fan_in"),
            }
            for r in rooms
        ],
    }


def _importer_files(rooms: list[str], nodes: dict[str, Any], substrate: dict[str, Any]) -> dict[str, Any]:
    """D-073 (the twelfth control): "importers of these rooms: 466" was Σ fan_in — import edges — on a page
    whose graph holds 456 files. The distinct files importing any of the rooms, the test files among them,
    and, where one room's importers are a third or more of those files, that room and the files without it."""
    R = set(rooms)
    by_room: dict[str, set[str]] = {}
    for ed in substrate.get("edges") or []:
        if ed["to"] in R:
            by_room.setdefault(ed["to"], set()).add(ed["from"])
    files = set().union(*by_room.values()) if by_room else set()

    def is_test(f: str) -> bool:
        return bool(((nodes.get(f) or {}).get("metrics") or {}).get("is_test"))

    out: dict[str, Any] = {"files": len(files), "test_files": sum(1 for f in files if is_test(f))}
    if files and len(by_room) > 1:  # D-075: one room imported is its own top room, and says nothing
        top = max(sorted(by_room), key=lambda r: len(by_room[r]))
        if len(by_room[top]) * 3 >= len(files):
            rest = files - by_room[top]
            out["top"] = {
                "room": top,
                "files": len(by_room[top]),
                "test_files": sum(1 for f in by_room[top] if is_test(f)),
                "rest": len(rest),
                "rest_tests": sum(1 for f in rest if is_test(f)),
            }
    return out


def _via_importer(e: dict[str, Any], nodes: dict[str, Any], population_ids: set[str], substrate: dict[str, Any]) -> dict[str, int]:
    """D-069: rooms with no test importer, and how many of those a room with one imports (one hop)."""
    importers: dict[str, set[str]] = {}
    for ed in substrate.get("edges") or []:
        importers.setdefault(ed["to"], set()).add(ed["from"])

    def tfi(r: str) -> int:
        return int(((nodes.get(r) or {}).get("metrics") or {}).get("test_fan_in", 0) or 0)

    none = [r for r in population_ids if tfi(r) == 0]
    via = sum(1 for r in none if any(tfi(i) > 0 for i in importers.get(r, ()) if i in population_ids))
    # D-070 (the parent's recount of the ninth skimmer): the clause was the population's complement on
    # every row reading test_fan_in — toothpick_wing read "1 (of the 95 rooms without a test importer,
    # 21 are imported by a room that has one)". A feature whose rooms are all without a test importer
    # (the unreinforced side) counts its own rooms; the test-imported side keeps the complement.
    own = [r for r in e["rooms"] if tfi(r) == 0]
    side = "own" if e["rooms"] and len(own) == len(e["rooms"]) else ("complement" if not own else "mixed")
    own_via = sum(1 for r in own if any(tfi(i) > 0 for i in importers.get(r, ()) if i in population_ids))
    out: dict[str, Any] = {"without": len(none), "reached": via, "side": side, "own_reached": own_via}
    # D-073 (the twelfth skimmer): typeorm's toothpick_wing read "0 from test files" beside "imported by a
    # room that has a test importer" without the room — src/index.ts, 1588 test importers, the barrel the
    # suite enters through; the most test-imported importer the clause counts is named
    reached_from = own if side == "own" else none
    cands = {i for r in reached_from for i in importers.get(r, ()) if i in population_ids and tfi(i) > 0}
    if cands:
        best = max(sorted(cands), key=tfi)
        out["via_room"] = {"room": best, "test_fan_in": tfi(best)}
    return out


def _paired(name: str, facts_doc: dict[str, Any]) -> str:
    """D-074: a consequence-implying feature name paired with its position name ("dark_room · long-untouched
    room"); a name without the flag, or without a position name, stands alone."""
    for f in facts_doc.get("features") or []:
        if f.get("feature") == name and f.get("name_implies_consequence") and f.get("position_name"):
            return f"{name} · {f['position_name']}"
    return name


def _paired_entry(entry: str, facts_doc: dict[str, Any]) -> str:
    """D-074: a most-positions entry ("foundation (2 profiles)") paired, its note kept after the position."""
    base, sep, note = entry.partition(" (")
    return _paired(base, facts_doc) + (f" ({note}" if sep else "")


def _via_room_text(v: dict[str, Any]) -> str:
    """D-073: the most test-imported importer the via-importer clause counts."""
    r = v.get("via_room")
    return f" — the most test-imported of them {r['room']}, {r['test_fan_in']} test importer{'s' if r['test_fan_in'] != 1 else ''}" if r else ""


def _gap(x: float, unit: str) -> str:
    """D-069: a gap in fixed notation — `.4g` rendered 4e-05 on eslint's crack row."""
    s = f"{x:.4g}"
    if "e" in s:
        s = f"{x:.6f}".rstrip("0").rstrip(".") or "0"
    return f"{s}{unit}"


def _rooms_at_cutoff(e: dict[str, Any], nodes: dict[str, Any]) -> int | None:
    """D-062: how many of a single-pNN feature's rooms sit exactly at the cutoff the population resolved to."""
    from .mapper.ruleset import parse_predicate

    terms = parse_predicate(str(e.get("predicate") or ""))
    if len(terms) != 1 or terms[0].percentile is None or not nodes:
        return None
    cut = (e.get("thresholds") or {}).get(str(e["predicate"]).strip())
    if not isinstance(cut, (int, float)):
        return None
    sig = terms[0].signal
    n = 0
    for r in e["rooms"]:
        node = nodes.get(r) or {}
        v = (node.get("metrics") or {}).get(sig)
        if v is None:
            v = ((node.get("derived") or {}).get("indices") or {}).get(sig)
        if isinstance(v, (int, float)) and abs(float(v) - float(cut)) < 1e-9:
            n += 1
    return n


def _rooms_beyond_cutoff(e: dict[str, Any], nodes: dict[str, Any], population_ids: set[str]) -> dict[str, Any] | None:
    """D-066: for a single-pNN feature, the nearest value on the far side of the cutoff among the
    population's rooms outside the set — how many rooms sit at it and how far it is from the cutoff.
    On mcp-secure-server the p90 clock cutoff fell inside one afternoon's commits: 35 rooms at the
    value, 24 more 0.0195 days under it, invisible to a tie count."""
    from .mapper.ruleset import parse_predicate

    terms = parse_predicate(str(e.get("predicate") or ""))
    if len(terms) != 1 or terms[0].percentile is None or not nodes:
        return None
    cut = (e.get("thresholds") or {}).get(str(e["predicate"]).strip())
    if not isinstance(cut, (int, float)):
        return None
    t = terms[0]
    above = t.op in (">=", ">")
    sig = t.signal
    members = set(e["rooms"])
    best: float | None = None
    n = 0
    for r in population_ids - members:
        node = nodes.get(r) or {}
        v = (node.get("metrics") or {}).get(sig)
        if v is None:
            v = ((node.get("derived") or {}).get("indices") or {}).get(sig)
        if not isinstance(v, (int, float)):
            continue
        v = float(v)
        if (above and v >= cut) or (not above and v <= cut):
            continue  # a non-member on the set's side (a null elsewhere); not the far side
        if best is None or (above and v > best) or (not above and v < best):
            best, n = v, 1
        elif abs(v - best) < 1e-9:
            n += 1
    if best is None:
        return None
    out: dict[str, Any] = {"value": best, "count": n, "gap": abs(float(cut) - best), "side": "below" if above else "above"}
    # D-075 (the thirteenth skimmer): eslint's cutoff tie carried its disowned-commit count and the 82
    # rooms 9 days under it did not, so the page could not say whether the far side is a chore too
    if sig == "last_touched_days":
        at = [r for r in population_ids - members if abs(float(((nodes.get(r) or {}).get("metrics") or {}).get(sig, float("nan"))) - best) < 1e-9]
        flags = [((nodes.get(r) or {}).get("metrics") or {}).get("last_touch_blame_ignored") for r in at]
        if any(v is not None for v in flags):
            out["blame_ignored"] = sum(1 for v in flags if v)
    # D-070 (the ninth skimmer, D-069's queue): on eslint the 82 rooms at the far value are one 300-file
    # chore; when the far value is a clock value and every room at it was last touched by a commit of one
    # breadth, the breadth is stated as the tie's is (tie_touch_files)
    if sig == "last_touched_days" and n >= 2:
        breadths = set()
        for r in population_ids - members:
            m = (nodes.get(r) or {}).get("metrics") or {}
            v = m.get("last_touched_days")
            if isinstance(v, (int, float)) and abs(float(v) - best) < 1e-9:
                breadths.add(m.get("last_touch_commit_files"))
        breadths.discard(None)
        if len(breadths) == 1:
            out["touch_files"] = next(iter(breadths))
    return out


def _share_by_construction(predicate: str, count: int | None = None, population: int | None = None, thresholds: dict[str, Any] | None = None, at_cutoff: int | None = None, beyond: dict[str, Any] | None = None, term_ties: dict[str, int] | None = None, blame_present: bool = False) -> str:
    """D-060 said a single-pNN row is "the top 10% … by construction"; D-061 (the eslint control):
    beside dark_room 83 of 473 — 80 rooms tie at the p90 cutoff. The rank fixes which rooms, not
    how many; the row states the share it realized and the cutoff this population resolved to."""
    from .mapper.ruleset import parse_predicate

    terms = parse_predicate(str(predicate or ""))
    ranked = [t for t in terms if t.percentile is not None]
    if len(terms) != 1 or terms[0].percentile is None:
        # D-063 (the registry control): a conjunctive row stated no cutoff, and on registry the
        # corridor's "at or above the median" fan-out resolves to 1; every ranked term says its value
        if not ranked:
            return ""
        parts = []
        for t in ranked:
            cut = (thresholds or {}).get(t.render())
            unit = " days" if t.signal.endswith("_days") else ""
            tie = (term_ties or {}).get(t.render())
            tie_text = f" ({tie} of {population} rooms at that value)" if tie and population else ""
            parts.append(f"p{t.percentile} on {t.signal} is {cut:g}{unit}{tie_text}" if isinstance(cut, (int, float)) else f"p{t.percentile} on {t.signal} unresolved")
        return " — here " + ", ".join(parts)
    t = terms[0]
    side = "at or above" if t.op in (">=", ">") else "at or below" if t.op in ("<=", "<") else None
    if side is None:
        return ""
    cut = (thresholds or {}).get(str(predicate).strip())
    unit = " days" if t.signal.endswith("_days") else ""
    cut_text = f"{cut:g}{unit}" if isinstance(cut, (int, float)) else "unresolved"
    if count is None or not population:
        return f" — rooms {side} this repository's p{t.percentile} on {t.signal} (here {cut_text})"
    share = 100.0 * count / population
    # D-062 counted the tie here; D-063 (the fourth skimmer): "83" travels and "80 at the cutoff value",
    # fourth in a run-on cell, does not — the tie count sits in the rooms column beside the number it qualifies
    text = f" — rooms {side} this repository's p{t.percentile} on {t.signal} (here {cut_text}): {count} of {population}, {share:.1f}%"
    if beyond:
        # D-066: the rank's other boundary — the next value beyond the cutoff and the rooms at it
        notes = []
        if beyond.get("touch_files"):
            notes.append(f"one commit of {beyond['touch_files']} files")
        if blame_present and beyond.get("blame_ignored") is not None:  # D-075: where the file exists, a zero answers the question
            k = beyond["blame_ignored"]
            notes.append(f"{k if k else 'none'} of them last touched by a commit the repository's .git-blame-ignore-revs disowns")
        paren = f" ({'; '.join(notes)})" if notes else ""
        text += f"; the next value {beyond['side']} the cutoff holds {beyond['count']} room{'s' if beyond['count'] != 1 else ''}{paren}, {_gap(beyond['gap'], unit)} {'under' if beyond['side'] == 'below' else 'over'} it"
    return text


def _signals_read(predicate: str) -> set[str]:
    """D-056: the raw signals a predicate reads, a blend expanded through its declared inputs
    (config.ALLOWED_INPUTS, _INPUT_SIGNAL) — the same walk records_of_signal makes for the record column."""
    from .config import ALLOWED_INPUTS
    from .validation.config import GROUNDING

    out: set[str] = set()
    for term in str(predicate or "").split(" and "):
        sig = term.strip().split(" ")[0]
        if not sig:
            continue
        if sig in ALLOWED_INPUTS:
            out |= {_INPUT_SIGNAL.get(i, i) for i in ALLOWED_INPUTS[sig]}
        elif (GROUNDING.get(sig) or {}).get("inputs"):
            # D-057: a derived index outside the tuned blends (reinforcement_index → test_fan_in)
            # expands through the grounding table, not by hand
            out |= {_INPUT_SIGNAL.get(i, i) for i in GROUNDING[sig]["inputs"]}
        else:
            out.add(sig)
    return out


def _conjoins(inner: dict[str, Any], outer: dict[str, Any]) -> bool:
    """D-053: a containment holds by predicate when the inner feature's predicate conjoins every
    term of the outer's — corridor ⊂ hub on every repository; toothpick_wing ⊂ lit_room on one.
    The fourteenth seating found five of six containments drawn like the one the repository decided."""
    terms = lambda p: {t.strip() for t in str(p or "").split(" and ")}  # noqa: E731
    return bool(terms(outer["predicate"])) and terms(outer["predicate"]) <= terms(inner["predicate"])


def _within(feats: dict[str, dict[str, Any]], inner: str, outer: str, ri: set[str], ro: set[str]) -> dict[str, Any]:
    """A containment overlap. D-053: by_predicate when the inner conjoins the outer's terms.
    D-056 (seventeenth seating): the silence of the marker had acquired a meaning — "independent"
    — the page never assigned; toothpick_wing ⊂ lit_room on mcp-secure-server is unmarked while
    bug_pressure_index reads recency, the clock lit_room reads. A containment not by predicate
    says which raw signals the two predicates read in common, or that there are none."""
    byp = _conjoins(feats[inner], feats[outer])
    shared = sorted(_signals_read(feats[inner]["predicate"]) & _signals_read(feats[outer]["predicate"])) if not byp else []
    return {"a": inner, "b": outer, "relation": "within", "n": len(ri), "n_outside": len(ro - ri), "by_predicate": byp, "shared_signals": shared}


def _flag(feats: dict[str, dict[str, Any]], ov: dict[str, Any]) -> dict[str, Any]:
    """D-044: an overlap says whether both its features are diagnostic; only those count."""
    ov["diagnostic"] = bool(feats[ov["a"]]["diagnostic"] and feats[ov["b"]]["diagnostic"])
    return ov


def record_of(predicate: str) -> str:
    """The records a predicate reads, in a fixed order — 'import graph and clock' for
    flooded_basement. A position is a place in these records and nothing else."""
    from .config import ALLOWED_INPUTS

    sigs = {sig for _, ss in _RECORDS for sig in ss} | set(ALLOWED_INPUTS)
    read = {r for sig in sigs if re.search(rf"\b{sig}\b", predicate) for r in records_of_signal(sig)}
    found = [name for name, _ in _RECORDS if name in read]
    return " and ".join(found) if found else "an unlisted record"


# D-042: the rules as the reader is told them — the header's checklist and the lint section both
# derive from this list, so the page cannot describe a rule the lint no longer applies
RULES: list[tuple[str, str]] = [
    ("R1", "consequence and forecast vocabulary refused outside a struck disclosure clause"),
    (
        "R2",
        "every citation resolves to a feature that fired on the rooms it names, with the count the skeleton records",
    ),
    ("R3", "a number is on the facts sheet and sits in the sentence that cites its feature"),
    (
        "R4",
        "decorative features cited by count only, never as diagnosis, with their ungrounded signal named",
    ),
    ("R5", "a consequence-implying name carries its position name where first used"),
    ("R6", "no whole-building label"),
    ("R7", "the diagnostic and decorative counts stated (met by the register)"),
    ("R8", "a room named in a sentence is covered by a feature cited in that sentence"),
    ("R9", "features with the same or nested rooms named together (met by the register)"),
    ("R10", "a directory named in a sentence contains a room cited in it"),
    ("R11", "no distributional adverb, ranking of marks, span or proximity between rooms"),
    (
        "R12",
        "a number wears its unit, a count of relations matches the register by kind; no ratio across units",
    ),
    (
        "R13",
        "a nesting is not an identity; a shared predicate is one measurement, not two agreeing",
    ),
    ("R14", "no 'validated' where no signal holds it"),
    ("R15", "a feature's largest directory named with its population (met by the register)"),
    (
        "R16",
        "a feature's count in a minority wing or a directory is sayable only where that wing or directory is named; the largest wing's count is the register's",
    ),
    (
        "R17",
        "a claim that a feature stands apart, or lacks a property another feature marks on its rooms, is checked against the register",
    ),
    (
        "R18",
        "no family of marks the sheet does not define (the graph marks, the onboarding marks); a family every cited feature's record reads is admitted",
    ),
]


def render_register(facts_doc: dict[str, Any]) -> str:
    """D-039: the register — one row per feature with fixed slots, rendered from the facts sheet
    by code. It states what three hostile readings found the prose could only overclaim: the
    unit, the wing counts, the dominant directory with its denominator, the relations between
    features (identical / within, with the rooms outside and the inert conjunct), the reason a
    decorative feature is excluded. The prose beneath it is the reading, not the inventory."""

    # D-050: a feature under two profiles is named with its profile everywhere it is named — the
    # matrix already did; the relation cell read "= foundation" on the foundation row
    _label = qualified_labels([f"{x['profile']}/{x['feature']}" for x in facts_doc["features"]])

    _dec = {f"{x['profile']}/{x['feature']}" for x in facts_doc["features"] if x["decorative"]}
    _rooms = {f"{x['profile']}/{x['feature']}": frozenset(x["rooms"]) for x in facts_doc["features"]}

    def plain(k: str) -> str:
        return _label.get(k, k.split("/")[-1])

    def short(k: str) -> str:
        # D-056: ◌ travels with the name — four relation cells named toothpick_wing without it
        return ("◌ " if k in _dec else "") + plain(k)

    def why_within(ov: dict[str, Any]) -> str:
        if ov.get("by_predicate"):
            return "by its predicate; "
        if "shared_signals" not in ov:
            return ""
        sh = ov["shared_signals"]
        # D-062: the cell carries its own correction — "no signal in common" read as independence 400 words from the note
        return (f"reads {', '.join(sh)} with it; " if sh else "no raw signal in common, one edge set read twice; ")

    def relations(key: str) -> str:
        out = []
        for ov in facts_doc.get("overlaps") or []:
            if key not in (ov["a"], ov["b"]):
                continue
            other = ov["b"] if ov["a"] == key else ov["a"]
            if ov["relation"] == "identical":
                if ov.get("shared_predicate"):
                    continue  # D-063: the row's profile cell says it
                elif ov.get("inert_terms"):
                    why = f"{', '.join(ov['inert_terms'])} excludes nothing"
                else:
                    why = ""
                out.append(f"= {short(other)}" + (f" ({why})" if why else ""))
            elif ov["a"] == key:
                # D-040: the remainder belongs to the superset — say whose rooms are outside;
                # D-053: a containment the predicates guarantee says so; D-056: containers that
                # are one set of rooms are one entry, named with every name that draws the set
                same = [o for o in facts_doc.get("overlaps") or [] if o["a"] == key and o["relation"] == "within" and _rooms.get(o["b"]) == _rooms.get(other)]
                if same and same[0] is not ov:
                    continue
                names = " = ".join(short(o["b"]) for o in (same or [ov]))
                out.append(
                    f"⊂ {names} ({why_within(ov)}{ov.get('n_outside')} {plain(other)} room{'s' if ov.get('n_outside') != 1 else ''} outside this set)"
                )
            else:
                # D-070 (the ninth control): scaffolding's cell listed maintainability/foundation and
                # onboarding/foundation as two containees with identical numbers while the register row
                # and the matrix treat them as one set; a containee drawing one set is one entry too
                # (two features drawing one set by different predicates keep their own entries — the
                # containment's reason is the pair's, not the set's)
                same = [o for o in facts_doc.get("overlaps") or [] if o["b"] == key and o["relation"] == "within" and _rooms.get(o["a"]) == _rooms.get(other) and why_within(o) == why_within(ov) and o.get("n_outside") == ov.get("n_outside")]
                if same and same[0] is not ov:
                    continue
                names = " = ".join(short(o["a"]) for o in (same or [ov]))
                out.append(
                    f"⊃ {names} ({why_within(ov)}{ov.get('n_outside')} of these rooms outside it)"
                )
        return "; ".join(out) or "no identity or containment"

    def relation_cell(f: dict[str, Any], key: str) -> str:
        # D-047: a set under the floor was not related to anything; the cell says that, not "none".
        # D-055: except where the predicates guarantee a containment — drawn at any count.
        # D-057: a feature that fired on nothing relates to nothing ("other" needs an antecedent)
        if f["count"] == 0:
            return "no rooms to relate (0)"
        if f["count"] < RELATION_MIN_ROOMS:
            drawn = relations(key)
            if drawn == "no identity or containment":
                return f"too few rooms to relate ({f['count']})"
            return f"{drawn}; too few rooms for any other relation ({f['count']})"
        return relations(key)

    rows = []
    # D-063 (the fourth skimmer): two identical rows under two profiles read as a generator bug; a
    # feature under two profiles with one predicate is one row whose profile cell names both
    _same = {}
    for ov in facts_doc.get("overlaps") or []:
        if ov["relation"] == "identical" and ov.get("shared_predicate"):
            _same.setdefault(ov["a"], []).append(ov["b"])
            _same.setdefault(ov["b"], []).append(ov["a"])
    _skip = set()
    for a, bs in _same.items():
        for b in bs:
            if b > a:
                _skip.add(b)

    def profile_cell(f: dict[str, Any]) -> str:
        k = f"{f['profile']}/{f['feature']}"
        others = sorted(x.split("/")[0] for x in _same.get(k, []))
        return f["profile"] if not others else " + ".join([f["profile"]] + others) + " (one predicate, two profiles)"

    # D-062 (the third skimmer): roster order put ◌ crack in the first row, the point of maximum attention; excluded rows render last
    for f in sorted(facts_doc["features"], key=lambda x: (bool(x["decorative"]),)):
        key = f"{f['profile']}/{f['feature']}"
        if key in _skip:
            continue
        sbw = facts_doc.get("scopes_by_wing") or {}
        fws = f.get("by_wing_scopes") or {}
        fwsc = f.get("by_wing_scope_counts") or {}
        bw = ", ".join(
            f"{k} {v}" + _wing_scopes_text(k, fws.get(k, 0), sbw.get(k, 1), fwsc.get(k) or {})
            for k, v in f.get("by_wing", {}).items()
        ) or "no wing (0)"
        bw += _scope_composition_text(f.get("scope_composition") or [], f["count"], facts_doc["population"])  # D-077
        # D-057: a zero row says so; D-066: a wing of many scopes says how many hold the feature; D-068: two or fewer are named
        dd = f.get("dominant_dir") or {}
        # D-041: every fallback says the reason that is the reason, and a directory that is also a
        # wing name is marked as the parent, not the wing
        if not dd or f["count"] == 0:
            dom = "no rooms"
        elif not dd.get("placeable", True):
            # D-075 (the thirteenth skimmer): eslint's one-room toothpick_wing never named its room, and
            # the via-importer clause's importer read as it; up to three rooms are named here
            dom = f"too few rooms to place ({f['count']})" + (": " + "; ".join(sorted(f["rooms"])) if f["count"] <= 3 else "")
        elif dd.get("holds_third"):
            as_parent = " (as parent, not the wing)" if dd["dir"] in facts_doc["wings"] else ""
            partners = ", ".join(
                f"{t['dir']}{' (as parent, not the wing)' if t['dir'] in facts_doc['wings'] else ''} {t['n']} of its {t['population']}"
                for t in dd.get("tied_with") or []
            )
            dom = f"{dd['dir']}{as_parent} {dd['n']} of its {dd['population']}" + (
                (f" (tied with {partners})" if partners else " (tied)") if dd.get("tied") else ""
            )
        else:
            # D-070 (the ninth control): "none holds a third" on five registry rows whose sheet said
            # src/utils held the most in each — a threshold read aloud where the field was; the parent
            # is named with its count and the threshold is said as what it is
            # D-071 (the tenth skimmer): the under-a-third parent rendered without its tie — lit_room's
            # "src/services/safety 3 of its 14" while the sheet tied it with analytics 3 of 6 and
            # definition 3 of 7; the tie renders on both branches
            as_parent = " (as parent, not the wing)" if dd.get("dir") in facts_doc["wings"] else ""
            tw = dd.get("tied_with") or []
            partners = ", ".join(
                f"{t['dir']}{' (as parent, not the wing)' if t['dir'] in facts_doc['wings'] else ''} {t['n']} of its {t['population']}"
                for t in tw
            )
            # (mcp's package_entry ties 16 parents at 1: past three partners the tie is counted, not listed)
            if len(tw) > 3:
                partners = f"{len(tw)} other parents, each holding {dd['n']}"
            tied = ((f" (tied with {partners})" if partners else " (tied)") if dd.get("tied") else "")
            dom = f"{dd['dir']}{as_parent} {dd['n']} of its {dd['population']}{tied} (under a third of the feature's rooms)" if dd.get("dir") else "none holds a third"
        if f["decorative"]:
            # D-055: the predicate is on the row — "the fragility half" of a reason was unresolvable
            # from a row that printed the reason and not the conjunction it is half of.
            # D-060: "decorative" read as cosmetic by the skimmer; the row says what the mark is
            what = f"`{f['predicate']}`" + _share_by_construction(f["predicate"], f["count"], facts_doc["population"], f.get("thresholds"), f.get("at_cutoff"), f.get("beyond_cutoff"), f.get("term_ties"), bool((facts_doc.get("blame_ignore_revs") or {}).get("present"))) + f" — ◌ excluded from the diagnosis: {f.get('decorative_reason') or ''}".rstrip()
        else:
            what = f"`{f['predicate']}`" + _share_by_construction(f["predicate"], f["count"], facts_doc["population"], f.get("thresholds"), f.get("at_cutoff"), f.get("beyond_cutoff"), f.get("term_ties"), bool((facts_doc.get("blame_ignore_revs") or {}).get("present")))
        if f.get("importers") and f["importers"]["total"]:
            # D-062: the import-graph positions are read from a graph that holds the test files; the row says how much of its importing is theirs
            imp = f["importers"]
            if "files" in imp:
                # D-073: files first, the edge sum beside it and said to be one
                nf = imp["files"]
                what += f" — imported by {nf} file{'s' if nf != 1 else ''}, {imp['test_files']} ({100.0 * imp['test_files'] / nf if nf else 0:.0f}%) of them test files ({imp['total']} import edges; a file importing several of these rooms is one file here)"
                if imp.get("top"):
                    t = imp["top"]
                    what += f" ({t['files']} of these files import {t['room']}, {t['test_files']} of them test files"
                    if t["rest"] > 0:
                        what += f"; without it {t['rest_tests']} of {t['rest']}, {100.0 * t['rest_tests'] / t['rest']:.0f}%"
                    what += ")"
            else:  # a sheet before 0.39.0 carries only the sum
                what += f" — importers of these rooms: {imp['total']}, {imp['from_tests']} ({100.0 * imp['from_tests'] / imp['total']:.0f}%) from test files"
        if f.get("caveat"):
            cav = str(f["caveat"])
            if f.get("caveat_case_count") is not None:
                # D-060: the case's magnitude is a field beside the caveat, never in it (D-042). D-066 (the
                # sixth skimmer): "(this case: 0 of 11 here)" after a two-clause caveat did not say which
                # clause it counted; a caveat places the count with `{case}`, beside the clause it counts
                n_of_m = _case_count_text(f.get("caveat_case"), f["caveat_case_count"], f["count"], facts_doc)
                cav = cav.replace("{case}", n_of_m) if "{case}" in cav else f"{cav} (this case: {n_of_m})"
            what += f" — caveat: {cav}"
            for ec in f.get("extra_caveats") or []:  # D-069: a second record, a second limit
                t = str(ec["text"])
                if ec.get("case_count") is not None:
                    n_of_m = _case_count_text(ec.get("case"), ec["case_count"], f["count"], facts_doc)
                    t = t.replace("{case}", n_of_m) if "{case}" in t else f"{t} (this case: {n_of_m})"
                what += f" — caveat: {t}"
        # D-070 (the ninth skimmer): in the columns a skimmer reads the glyph was the exclusion's only
        # carrier, and "crack 47" left the room as a diagnosis; the word travels with the glyph
        name = (f"◌ {f['feature']} (excluded)" if f["decorative"] else f["feature"])
        # D-074 (Alex: pair): the twelfth skimmer's CERTAIN drift — a pasted row carried the name and left
        # the register behind; a name the ruleset flags as implying a consequence travels with its position
        if f.get("name_implies_consequence") and f.get("position_name"):
            name += f" · {f['position_name']}"
        # D-041: the cell reads the field it claims to report; a consequence-implying name without a
        # position name is a ruleset defect and the page says so rather than denying it
        if f.get("position_name"):
            pos = f"{f['position_name']} ({record_of(f['predicate'])})" + _quantile_reach_text(f["predicate"], f.get("thresholds"), f.get("term_reach"), facts_doc.get("population"))
        elif f.get("name_implies_consequence"):
            pos = f"POSITION NAME MISSING (ruleset defect); a position in the {record_of(f['predicate'])}"
        else:
            # D-044: the note promises the record beside every position; the lexicon is why there is
            # no position name, the record is what the predicate reads — both are said
            pos = f"no consequence word in the name (lexicon); a position in the {record_of(f['predicate'])}"
        # D-060: the position is the first column — the skimmer reads column one and infers the rest
        # from the name, and the name is the column that carries the consequence word
        # D-063: the tie count travels with the count; two profiles on one predicate are one row
        tie = f" ({'all' if f.get('at_cutoff') == f['count'] else f.get('at_cutoff')} tied at the cutoff{f' — one commit of {f['tie_touch_files']} files' if f.get('tie_touch_files') else ''})" if (f.get("at_cutoff") or 0) > 1 else ""
        if f.get("via_importer") and f["via_importer"].get("without") and f["count"]:  # D-057: a zero row says only that
            v = f["via_importer"]
            # D-070: the clause is the complement on the test-imported side and the row's own rooms on the
            # unreinforced side (toothpick_wing had carried the population's complement beside a count of 1)
            if v.get("side") == "own":
                tie += f" ({v.get('own_reached', 0)} of these {f['count']} {'is' if f['count'] == 1 else 'are'} imported by a room that has a test importer{_via_room_text(v)})"
            elif v.get("side", "complement") == "complement":
                tie += f" (of the {v['without']} rooms without a test importer, {v['reached']} are imported by a room that has one{_via_room_text(v)})"
        # D-064 (the fifth skimmer): dark_room 70 and flooded_basement 70 summed to 140; a set drawn twice says so where the count is read
        twins = [ov["b"] if ov["a"] == key else ov["a"] for ov in facts_doc.get("overlaps") or [] if ov["relation"] == "identical" and not ov.get("shared_predicate") and key in (ov["a"], ov["b"])]
        if twins:
            tie += f" (the same rooms as {', '.join(plain(t) for t in twins)})"
        # D-068 (the seventh skimmer): every caveat count sat in the eighth column, which a rendered table
        # crushes; the case count travels with the count it qualifies, as the tie count does (D-063)
        if f.get("caveat_case_count") and f.get("caveat"):  # D-069: a zero case stays in the predicate cell ("0 of N here")
            lab = _case_label(str(f["caveat"]))
            if lab:
                tie += f" ({f['caveat_case_count']} {_agree(f['caveat_case_count'], lab)})"
        for ec in f.get("extra_caveats") or []:  # D-069
            if ec.get("case_count"):
                lab = _case_label(str(ec["text"]))
                if lab:
                    tie += f" ({ec['case_count']} {_agree(ec['case_count'], lab)})"
        rows.append(
            f"| {pos} | {name} | {profile_cell(f)} | {f['count']}{tie} | {bw} | {dom} | {relation_cell(f, key)} | {what} |"
        )
    wings = " · ".join(f"{k} {v}" for k, v in facts_doc["wings"].items())
    scopes = " · ".join(f"{e['scope']} {e['rooms']}" for e in (facts_doc.get("by_package") or []))  # D-054; D-056: a list
    gate = facts_doc.get("gate") or {}
    asserted = sum(1 for v in gate.values() if v == "asserted")
    # D-050: "none validated" was a literal beside a counted "asserted"; both are read from the gate
    validated = sum(1 for v in gate.values() if v == "validated")
    validated_text = "none validated" if validated == 0 else f"{validated} validated"
    base = facts_doc.get("diagnostic_count_base", facts_doc["diagnostic_count"])
    _dc = facts_doc["decorative"].get("counts") or {}
    dec = ", ".join(f"{n} {_dc[n]}" if n in _dc else n for n in facts_doc["decorative"]["features"]) or "none"
    fp = (facts_doc.get("gate_fingerprint") or "?")[:12]
    head = (
        "## Register"
        + NL
        + NL
        # D-060: the skimmer read the table and skipped the note whole; the one rule the page rests on
        # stands first, bold, outside the italic — and the calibration fact the numbers depend on beside it
        + "**A position names where a room sits in a record — the import graph, the clock, the test graph, the edit record, size — and is not a claim about the room's condition (D-004 Q3). "
        + f"Every pNN ranks this repository's own {facts_doc['population']} rooms, so a `>= p90` row holds a tenth of them — or more where rooms tie at the cutoff, and the rooms column says how many are tied; a single-rank row states its share, and every ranked term states the value its rank resolved to here — and no count on this page compares across repositories, or across snapshots of this one: a ranked row holds its share of whatever rooms the repository has, so working its rooms down moves the cutoff, not the count (D-073)."
        + (
            f" A room is a source file outside the test convention{_test_convention_text(facts_doc)} with computed signals{_kinds_rule_text(facts_doc)}: {facts_doc['population']} of the {facts_doc['node_count']} files with a source extension the substrate reads (manifests, documents and the rest of the tree are not counted); the {facts_doc['test_nodes']} test files are nodes of the import graph and not rooms{_kinds_count_text(facts_doc)}"
            + (f", and {facts_doc['unindexed_nodes']} file{'s' if facts_doc['unindexed_nodes'] != 1 else ''} with no computed signals {'are' if facts_doc['unindexed_nodes'] != 1 else 'is'} not a room either" if facts_doc.get("unindexed_nodes") else "")
            + "."
            if facts_doc.get("node_count") else ""
        )
        + "**"
        + NL
        + NL
        # D-062 (Rams): the note is a legend — one line per column or marker, the counts first — and no
        # longer repeats what the header, the cells or the column headers already say. D-043's rule
        # (a note sentence per renderer rule) generated one repetition per seating; the skimmer skipped
        # the paragraph whole (D-060, D-061). What remains defines what has no cell of its own.
        + f"*{facts_doc['population']} rooms in {facts_doc['wing_count']} wings ({wings}); {facts_doc['diagnostic_count']} diagnostic marks across all profiles "
        + f"({base} in the base profile), one mark per feature per room; identical pairs of diagnostic features mark {facts_doc.get('rooms_marked_twice', 0)} rooms twice ({facts_doc.get('rooms_marked_twice_shared_predicate', 0)} under one predicate in two profiles, {facts_doc.get('rooms_marked_twice_inert_conjunct', 0)} where two predicates draw one set because a conjunct excludes nothing, {facts_doc.get('rooms_in_both_kinds', 0)} under both); "
        + f"the diagnostic features name {facts_doc.get('distinct_room_sets', '?')} distinct sets of rooms; {facts_doc['decorative']['count']} excluded marks ◌ ({dec}); "
        + f"{facts_doc['co_located_rooms']} rooms carry two or more distinct diagnostic sets; gate `{fp}`, {asserted} of {len(gate)} signals asserted, {validated_text} — asserted is a description that held under the stability budget and the corroboration its grounding class requires (validation spec §2.4), validated a forecast confirmed by a temporal holdout (validation spec §3).*"
        + NL + NL
        + f"- **wing** — a directory at depth {facts_doc.get('wing_depth', 1)} of the tree (the ruleset's wing_depth), not a package"
        + (
            f"; the population spans {facts_doc.get('packages', 1)} package scopes, pooled (rooms per scope, largest first, each scope named by the manifest that holds it: {scopes}); pooled, a scope's share of a feature is not its own top tenth, and the by-wing cell names a scope of {SCOPE_FLOOR} or more rooms holding over twice or under half its share of the rooms (D-077)"
            + (f"; {facts_doc['cross_scope_edges']} of {facts_doc['edge_count']} imports cross a package scope{_from_tests_text(facts_doc.get('cross_scope_from_tests'), facts_doc['cross_scope_edges'])}" if facts_doc.get("cross_scope_edges") is not None else "")
            if (facts_doc.get("packages") or 1) > 1 else "; the population is one package scope (package.json)"
        )
        + "." + NL
        + "- **◌** — a feature excluded from the diagnosis (the ruleset's word is decorative): computed and counted, not claimed, because a signal it reads is unvalidated. 'Excluded' on this page means this and nothing else; a file kind the ruleset does not count as a room is said in those words." + NL
        + f"- **largest parent directory** — the immediate parent (non-recursive) holding the most of a feature's rooms, with how many of the parent's own rooms that is; the cell says when it holds under a {DIRECTORY_SHARE}rd of the feature's rooms, and a feature under {DIRECTORY_MIN_ROOMS} rooms is not placed; a parent that shares a wing's name is marked as the parent." + NL
        + f"- **relation to** — identity and containment, and only those, between features, diagnostic or decorative, with {RELATION_MIN_ROOMS} or more rooms — and a containment the predicates guarantee at any count; two sets that overlap without one containing the other are not related here, and 'no identity or containment' says exactly that. 'By its predicate': the inner predicate conjoins every term of the outer. Otherwise the cell says which raw signals the two predicates read in common (a blend or index expanded through its declared inputs), or 'no raw signal in common' — a signal, not an instrument." + NL
        + "- **the import graph and the test graph** — one edge set read twice: a test file is a node whose imports count in fan_in and centrality, and test_fan_in counts those importers alone; an import-graph row says how many distinct files import its rooms and how many of those are test files, with the import edges beside them (a file importing several of the rooms is one file and several edges). Centrality is PageRank over that graph: a room's rank rises with the rank of its importers, not only with their number" + _centrality_illustration_text(facts_doc) + "."
        + (f" The graph is resolved statically: {facts_doc['unresolved_imports']} imports in the tree did not resolve to a file{_unresolved_text(facts_doc)}, and {facts_doc['external_imports']} are external packages; an import the resolver did not place, or one computed at run time, is not an edge, so a room reached only that way reads as unimported there.{_alias_state_text(facts_doc)}{_package_name_text(facts_doc)}" if facts_doc.get("unresolved_imports") is not None else "")
        + NL
        + _index_legend_lines(facts_doc)
        + "- **caveat** — the ruleset's own limit on what a predicate reads, never a claim about this repository; the count in it ('N of M here') is this repository's, beside the clause it counts."
        + NL
        + NL
        + "| position (the record it reads) | feature | profile | rooms (tied at the cutoff) | by wing | largest parent directory (n of the parent's rooms) | relation to (= one set · ⊂ inside · ⊃ contains) | predicate (with the cutoffs resolved here); caveat, a limit on the predicate; or reason |"
        + NL
        + "|---|---|---|---|---|---|---|---|"
        + NL
    )
    return head + NL.join(rows) + NL + render_most_marked(facts_doc) + render_shared(facts_doc)


def qualified_labels(keys: list[str]) -> dict[str, str]:
    """D-050: the label a feature key prints under — the bare feature name, or profile/feature
    when the name is under two profiles, in every place a feature is named."""
    names = [k.split("/")[-1] for k in keys]
    return {k: (n if names.count(n) == 1 else k) for k, n in zip(keys, names)}


TOP_TIER_CAP = 25  # D-061: rooms of the top tier named before "and N more"


def _names_per_set(marking, twice: set[str]) -> list[str]:
    """D-064: features that draw one set of rooms are one name in a tier's feature list ('foundation (2 profiles)')."""
    groups: dict[frozenset, list[dict[str, Any]]] = {}
    for e in marking:
        groups.setdefault(frozenset(e["rooms"]), []).append(e)
    out = []
    for es in groups.values():
        names = sorted({e["feature"] for e in es})
        if len(names) == 1 and len(es) > 1:
            out.append(f"{names[0]} ({len(es)} profiles)")
        elif len(names) == 1:
            out.append(f"{es[0]['profile']}/{names[0]}" if names[0] in twice else names[0])
        else:
            out.append(" = ".join(names))
    return sorted(out)


def top_tier(features, room_metrics: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """D-061: every room under the most distinct diagnostic sets (two or more), by path, with its
    size and the features that mark it. A set, not a list ordered by anything a reader can take
    for severity."""
    feats = [e for e in features if e["diagnostic"]]
    twice = {e["feature"] for e in feats if sum(1 for x in feats if x["feature"] == e["feature"]) > 1}
    sets = sets_per_room(feats)
    most = max((n for n in sets.values() if n >= 2), default=0)
    rooms = sorted(r for r, n in sets.items() if n == most and most >= 2)
    return {
        "sets": most,
        "rooms": [
            {
                "room": r,
                "lines": (room_metrics.get(r) or {}).get("size_loc", (room_metrics.get(r) or {}).get("lines")),
                "fan_in": (room_metrics.get(r) or {}).get("fan_in"),
                "test_fan_in": (room_metrics.get(r) or {}).get("test_fan_in"),
                # D-064: one name per set — the heading said 6 and the cell listed 7 where foundation is two profiles of one predicate
                "features": _names_per_set([e for e in feats if r in set(e["rooms"])], twice),
            }
            for r in rooms
        ],
    }


def _unlisted(m: dict[str, Any]) -> str:
    """D-060: a partly listed tier names the rooms it leaves out (up to five), so the listed are not taken as the tier."""
    u = m.get("unlisted") or []
    if not u:
        return ""
    shown = ", ".join(u[:5])
    more = f" and {len(u) - 5} more" if len(u) > 5 else ""
    return f" (unlisted: {shown}{more})"


def render_most_marked(facts_doc: dict[str, Any]) -> str:
    """D-049: the rooms carrying the most, with the count of rooms at that most so a capped list is
    not a claim of completeness. D-050: the count is distinct sets. D-052: what the lead said of
    "a row below that count" was true of the list and false as a label on the second row of a
    tier; the cell now says it — "3 of 4" is three rows listed of four rooms at this count, the
    first by path — and the lead says only the ordering and the cap."""
    tier = facts_doc.get("top_tier")
    if tier is None:  # an older sheet without the field renders the capped list it carries (pre-0.27.0)
        return _render_most_marked_legacy(facts_doc)
    rooms = tier.get("rooms") or []
    most = tier.get("sets", 0)
    if not rooms:
        return NL + "### Rooms at the most positions" + NL + NL + "*No room carries two distinct diagnostic sets.*" + NL
    co = facts_doc.get("co_located_rooms")
    shown = rooms[:TOP_TIER_CAP]
    more = f"; the first {TOP_TIER_CAP} by path are listed and {len(rooms) - TOP_TIER_CAP} more are not" if len(rooms) > TOP_TIER_CAP else ""
    lead = (
        f"*Every room under the most distinct diagnostic sets ({most}), by path — {len(rooms)} room{'s' if len(rooms) != 1 else ''}{more}. "
        "A set is a distinct set of rooms a diagnostic feature draws (a feature under two profiles, or two features drawing one set, is one set). "
        + (f"Rooms at fewer positions are not listed; {co} rooms carry two or more distinct sets. " if co is not None else "")
        + "Size is the room's non-blank line count; importers is the room's fan_in, with the test files among them in parentheses.*"
    )
    def _imp(m: dict[str, Any]) -> str:
        if m.get("fan_in") is None:
            return "—"
        return f"{m['fan_in']} ({m.get('test_fan_in', 0)})"

    body = NL.join(f"| {m['room']} | {m.get('lines') if m.get('lines') is not None else '—'} | {_imp(m)} | {', '.join(_paired_entry(ft, facts_doc) for ft in m['features'])} |" for m in shown)
    # D-072 (the eleventh skimmer): 11 of eslint's 12 rooms here are the stance's case, and the stance
    # sat below the matrix where the skimmer had stopped; the count is said where the list is read
    at_case = ""
    sc = facts_doc.get("stance_case") or {}
    if sc.get("untouched"):
        n = sum(1 for m in rooms if any(ft.split(" ")[0] == sc["untouched"] for ft in m.get("features") or []))
        if n:
            who = (
                ("The one room here is" if n == 1 else f"All {n} rooms here are") if n == len(rooms)
                else f"{n} of these {len(rooms)} rooms {'is' if n == 1 else 'are'}"
            )
            at_case = (
                f"**{who} long-untouched ({sc['untouched']}) — "
                "the position at which the stance places the norm's known false positive (see Stance).**" + NL + NL
            )
    return (
        NL + f"### Rooms at the most positions ({most})" + NL + NL
        # D-060: the skimmer read a capped, count-ordered list as a leaderboard; D-061: the caption
        # over it was read and bounced, so the table is the whole top tier by path — a set, with size
        + "**Every room at the most positions, in path order — a set, not a ranking and not a severity (D-004 Q3).**" + NL + NL
        + at_case
        + lead + NL + NL
        # D-062 (Rams): the positions column was a constant already in the heading; (the typeorm control): importers, and how many are tests
        + "| room | lines | importers (from test files) | diagnostic features that mark it |" + NL + "|---|---|---|---|" + NL + body + NL
    )


def _render_most_marked_legacy(facts_doc: dict[str, Any]) -> str:
    """The capped, count-ordered list rendered from 0.19.0 to 0.26.0 (D-049 … D-060), kept for sheets without `top_tier`."""
    top = facts_doc.get("most_marked_rooms") or []
    if not top:
        return NL + "### Rooms at the most positions" + NL + NL + "*No room carries two distinct diagnostic sets.*" + NL
    most = top[0].get("sets", top[0]["marks"])
    at = facts_doc.get("rooms_at_most_sets", top[0].get("rooms_at_this_count", len(top)))
    lead = (
        f"*Rooms under two or more distinct diagnostic sets, {MOST_MARKED_ORDER}; at most {MOST_MARKED_ROOMS} are listed. "
        f"{at} room{'s' if at != 1 else ''} carr{'y' if at != 1 else 'ies'} the most ({most}). "
        "The listed column is rows listed of rooms at the row's sets count; where fewer are listed than carry the count, the listed are the first by path.*"
    )
    body = NL.join(
        f"| {m['room']} | {m.get('sets', m['marks'])} | {m['marks']} | {m.get('listed_at_this_count', '')} of {m.get('rooms_at_this_count', '')}{_unlisted(m)} | {', '.join(m['features'])} |"
        for m in top
    )
    return (
        NL + "### Rooms at the most positions" + NL + NL
        + "**A count of the positions a room sits at; the order is the count, then the path — not a ranking and not a severity (D-004 Q3).**" + NL + NL
        + lead + NL + NL
        + "| room | positions (distinct sets) | marks | listed of rooms at this count | diagnostic features that mark it |" + NL + "|---|---|---|---|---|" + NL + body + NL
    )


def render_shared(facts_doc: dict[str, Any]) -> str:
    """D-049: rooms each pair of diagnostic features shares, as a matrix; the diagonal is the
    feature's own count. Identity and containment are the relation column's; this is the rest."""
    pairs = facts_doc.get("shared_rooms") or []
    all_keys = sorted({k for sr in pairs for k in (sr["a"], sr["b"])})
    if not all_keys:
        return ""
    counts = {f"{f['profile']}/{f['feature']}": f["count"] for f in facts_doc["features"]}
    cell = {(sr["a"], sr["b"]): sr["shared"] for sr in pairs}
    cell.update({(b, a): n for (a, b), n in list(cell.items())})
    _label = qualified_labels(all_keys)
    # D-062 (Rams): two features drawing one set were two identical rows and columns — one measurement
    # shown as two agreeing (the reading R13 forbade in prose); they share one row, named with both names
    room_sets = {f"{f['profile']}/{f['feature']}": frozenset(f["rooms"]) for f in facts_doc["features"]}
    groups: dict[frozenset, list[str]] = {}
    for k in all_keys:
        groups.setdefault(room_sets.get(k) or frozenset([k]), []).append(k)  # an empty set is its own row
    keys = [ks[0] for ks in groups.values()]
    labels = [" = ".join(_label[k] for k in groups[room_sets.get(k) or frozenset([k])]) for k in keys]
    head = "| shared rooms | " + " | ".join(labels) + " |" + NL + "|---|" + "---|" * len(keys) + NL
    rows = NL.join(
        f"| {labels[i]} | "
        + " | ".join(
            f"**{counts.get(a, 0)}**" if a == b else str(cell.get((a, b), 0)) for b in keys
        )
        + " |"
        for i, a in enumerate(keys)
    )
    return (
        NL + "### Shared rooms" + NL + NL
        + "*Rooms both features mark, for every pair of diagnostic features (features drawing one set of rooms share one row, named with each name); the diagonal is the feature's own count. A shared count equal to the smaller of the two features' own counts is containment, and equal to both is identity; the relation column above draws those, and only between features with " + str(RELATION_MIN_ROOMS) + " or more rooms or where the predicates guarantee the containment — any other pair under that floor is read here and not there.*"
        + NL + NL + head + rows + NL
    )


def render_disclosure(facts_doc: dict[str, Any]) -> str:
    """D-049: the decorative disclosure, rendered from decorative_reason — the prompt's canonical
    sentence, now a fixed text tested against the fields it reads."""
    dec = [f for f in facts_doc["features"] if f["decorative"]]
    n = facts_doc["decorative"]["count"]
    if not dec:
        return "No excluded marks: every feature that fired rests on an asserted signal."
    sigs = sorted({w for f in dec for w in re.findall(r"[a-z_]+_index", f.get("decorative_reason") or "")})
    names = " and ".join(
        f"{f['feature']}" + (f" — {f['position_name']} —" if f.get("position_name") else "") for f in dec
    )
    # D-054 said the signal's reason once here; D-062 (Rams): that was its third copy — every ◌ row
    # carries it — and the section repeated three cells. One line: the names with counts, what ◌
    # means, which signal, and where the reason is. The heading stays as the ◌ legend the skimmer
    # (D-060) looked for below the table.
    listed = "; ".join(f"◌ {_paired(f['feature'], facts_doc)} {f['count']}" for f in dec)  # D-075: paired, as the row is
    where = f"the signal {'they read' if len(dec) != 1 else 'it reads'} ({', '.join(sigs)}) is unvalidated" if sigs else "a signal is unvalidated"
    return (
        f"{listed} — {n} mark{'s' if n != 1 else ''} computed and counted, excluded from the diagnosis: {where}; "
        "each row carries the reason."
    )


def _ver(facts_doc: dict[str, Any], profile: str) -> str:
    """D-057: the ruleset version beside the profile name — every caveat, position and reason on the page is a versioned text."""
    v = (facts_doc.get("profile_versions") or {}).get(profile)
    return f" {v}" if v else ""


def render_brief(
    text: str | None,
    facts_doc: dict[str, Any],
    violations: list[Violation],
    provenance: dict[str, Any],
) -> str:
    """D-049: header → register (with the most-marked rooms and the shared-rooms matrix) →
    decorative disclosure → stance → provenance, all rendered by code. A hand-written draft, if
    given, is appended as the reading with its lint section; nothing else on the page is prose."""
    draft = text is not None and text.strip() != ""
    fp = (facts_doc.get("gate_fingerprint") or "?")[:12]
    where = (
        f"Profile {facts_doc['profile']}{_ver(facts_doc, facts_doc['profile'])}"
        + (f" + {', '.join(o + _ver(facts_doc, o) for o in facts_doc['overlays'])}" if facts_doc["overlays"] else "")
        + f", geometry {facts_doc['geometry']}, skeleton `{facts_doc['skeleton_hash'][:12]}…`, facts `{facts_doc['facts_hash'][:12]}…`. "
        + (f"As of {str(facts_doc['as_of'])[:10]}, commit `{facts_doc['repo']['head_sha'][:12]}`. " if facts_doc.get("as_of") else f"Commit `{facts_doc['repo']['head_sha'][:12]}`. ")  # D-060: the clock's now
        + f"Calibration: {facts_doc.get('calibration', 'in-repo, self-relative')} — stability is the `substrate timelapse` run under gate `{fp}`, not this page. "
        f"Brief {facts_doc.get('brief_version', BRIEF_VERSION)}."
    )
    if draft:
        status = (
            "PASS"
            if not violations
            else f"FAILED ({len(violations)} violation{'s' if len(violations) != 1 else ''})"
        )
        head = (
            f"# {facts_doc['repo']['name']} — architect's brief\n\n"
            f"*The register below is rendered from the facts sheet by code; the reading beneath it is a hand-written draft, linted. "
            f"Register lint: **{status}**. What the lint checked: "
            + "; ".join(f"{rid} {desc}" for rid, desc in RULES)
            + ". What it cannot check: a consequence voiced without a listed word, a computed number that happens to match, a room's function inferred from its name. "
            + where
            + " A PASS is a pass under that grammar (D-035).*\n\n"
        )
    else:
        head = (
            f"# {facts_doc['repo']['name']} — architect's brief\n\n"
            f"*Rendered from the facts sheet by code; no model wrote any of it. "
            f"Every cell is a field, and every fixed text on the page has a test that asserts it against the sheet it is rendered from (`tests/test_brief.py`); the tests run on a fixture, not on this page. "
            + where
            + "*\n\n"
        )
    prov = (
        "\n## Provenance\n\n"
        + "\n".join(f"- {k}: `{v}`" for k, v in sorted(provenance.items()) if v is not None)
        + "\n"
    )
    page = (
        head
        + render_register(facts_doc)
        + "\n## Marks excluded from the diagnosis (◌)\n\n"
        + render_disclosure(facts_doc)
        + "\n\n## Stance\n\n"
        + facts_doc.get("stance", STANCE)
        + _stance_case_text(facts_doc)
        + "\n"
    )
    if draft:
        page += "\n## Reading (draft)\n\n" + (text or "").strip() + "\n"
    page += prov
    if draft:
        lint_md = "\n## Register lint\n\n"
        if violations:
            lint_md += (
                "| rule | paragraph | detail | text |\n|---|---|---|---|\n"
                + "\n".join(
                    f"| {v.rule} | {v.paragraph} | {v.detail.replace('|', '/')} | {v.text.replace('|', '/')} |"
                    for v in violations
                )
                + "\n\n**This draft failed the register lint and is not a diagnosis until it passes.**\n"
            )
        else:
            lint_md += (
                "No violations. Rules: "
                + ", ".join(f"{rid} {desc}" for rid, desc in RULES)
                + " (each rule is dated in DECISIONS.md).\n"
            )
        page += lint_md
    return page


def relint(
    markdown: str, skeleton: dict[str, Any], substrate: dict[str, Any] | None
) -> dict[str, Any]:
    """Re-judge the reading of an existing brief.md under the current lint, keeping its provenance.
    A page from before D-049 carries its reading under "## Reading"; a page since carries a draft
    under "## Reading (draft)" or no reading at all."""
    m = re.search(r"\n## Reading(?: \(draft\))?\n(.*?)(?=\n## |\Z)", markdown, re.DOTALL)
    prose = m.group(1).strip() if m else ""
    prov: dict[str, Any] = {}
    pm = re.search(r"## Provenance\n(.*?)(?:\n## |\Z)", markdown, re.DOTALL)
    if pm:
        for line in pm.group(1).splitlines():
            mm = re.match(r"- ([^:]+): `(.*)`", line.strip())
            if mm:
                prov[mm.group(1)] = mm.group(2)
    f = facts(skeleton, substrate)
    viols = lint(prose, f, register=True) if prose else []
    prov = {**prov, "relinted": f"brief {BRIEF_VERSION}", "facts_hash": f["facts_hash"]}
    return {
        "facts": f,
        "text": prose,
        "violations": [v.as_dict() for v in viols],
        "provenance": prov,
        "markdown": render_brief(prose, f, viols, prov),
        "passed": not viols,
    }


def run_brief(
    skeleton: dict[str, Any],
    substrate: dict[str, Any] | None,
    draft: str | None = None,
) -> dict[str, Any]:
    """Facts → rendered brief (D-049: by code, no model). A hand-written draft, if given, is
    linted and appended as the reading. Returns a dict with `facts`, `text`, `violations`,
    `provenance`, `markdown`, `passed`."""
    f = facts(skeleton, substrate)
    if draft is not None:
        text, prov = draft, {"generator": "draft", "facts_hash": f["facts_hash"], "brief_version": BRIEF_VERSION}
        viols = lint(text, f, register=True)
    else:
        text, prov, viols = None, {"generator": "code", "facts_hash": f["facts_hash"], "brief_version": BRIEF_VERSION}, []
    return {
        "facts": f,
        "text": text or "",
        "violations": [v.as_dict() for v in viols],
        "provenance": prov,
        "markdown": render_brief(text, f, viols, prov),
        "passed": not viols,
    }
