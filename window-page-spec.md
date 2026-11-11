# The window page — what differed between two commits, on a page of its own

Status: **built 2026-11-11 (§12); re-checked (run 72, §11); open until the seat has run.** D-083.
Supersedes the form in `event-statement-spec.md`, whose §10 (tracker run 71) lists what
fell and why. Alex chose the separate page the same day. Parent: `stability-budget-spec.md`
(D-082). §11 holds the re-check before any code.

## 1. What it is

A page about **one pair of commits**: which unedited rooms had a predicate term change
outcome between them, which clock and excluded rows changed membership, which unedited
rooms changed band, and what the gate's budget arithmetic reads on that pair. Every
line is an event in that window. Nothing on it is a property of a room, a row, a
ruleset or the repository; nothing on it is graded; no count on it is offered for
comparison with another repository or another window.

The brief stays a page about one snapshot. Its rule "no count on this page compares
across repositories, or across snapshots of this one" (`brief.py:2996`) and the brief
spec's §1 and §2.1 are untouched. The brief gains a pointer and nothing else (§7).

## 2. Architecture

The window page is a pure function of one or two **skeleton diffs** of the same pair of
commits (one per geometry), as the brief is a pure function of a skeleton. Everything
the page prints is a field of a diff; the diff gains the fields it lacks (§3). No
skeleton or substrate is read at render time, so a page cannot disagree with the diff
it cites.

    substrate skeleton-diff A B --renames SB --before-substrate SA -o D.json   (exists; gains fields)
    substrate window D.age.json [D.layer.json] --origin gate|caller -o W.md --facts W.facts.json   (new)
    substrate brief SK SB --window W.facts.json -o brief.md                     (gains --window)

`scripts/regenerate_readings.py` runs them in that order: diffs (step 1, exists), window
pages into `reports/<tag>-m3x/<short>.window.md` beside the brief, then briefs.

## 3. What the diff gains (additive; no existing leaf, operand or verdict changes)

Read against `mapper/diff.py::skeleton_diff` as of commit 828d20e.

| field | content | why |
|---|---|---|
| `identity` | `ruleset` and each overlay as `{name, version}`, both skeletons' `mapper_version`, `substrate_config_fingerprint` | two diffs can be checked to come from one ruleset and gate; today a diff records none of it |
| `rooms.born`, `rooms.deleted` | names (after-names; before-names for deleted) | today only counts (`born`, `deleted`) |
| `per_feature[*].rooms_before`, `.rooms_after` | the row's size in each skeleton, all rooms | `before`/`after` are over rooms present in both commits (`diff.py:349-350`): mcp scaffolding 31 → 35 there, 31 → 36 in the skeletons |
| `per_feature[*].born_entered`, `.deleted_left` | names | born rooms are in neither `added` nor `touched.nodes` |
| `per_feature[*].predicate` | the roster's predicate text | to merge one predicate under two profiles without the brief's `overlaps` |
| `per_decorative_feature` | per excluded feature: `kind`, `predicate`, `rooms_before`, `rooms_after`, `added`, `removed`, `untouched_affected_rooms`, `born_entered`, `deleted_left`. **No `transition_evidence`.** | today a count only (`untouched.decorative_changes`). Kept outside `per_feature` so the operand, the crossings and the time-lapse ripple counts cannot move |
| `budget.window.before_ts`, `.after_ts`, `.first_ts`, `.last_ts` | the two endpoint commits' timestamps, and the earliest and latest timestamp over the commits in the after-timeline and not the before-timeline, each as recorded with its UTC offset; null when no after-substrate is supplied or an entry has no `ts` | endpoint dates do not bound a window when a commit is merged late and authored early (`touched_between` is by reachability) |

Marks that are neither diagnostic nor excluded (degraded: a graph-dependent feature on a
degraded graph, `engine.py:201-204`) are in neither set and stay unreported; the page
says so with the count of such marks in each skeleton (`degraded_marks`, additive).

## 4. The command

`substrate window DIFF [DIFF] --origin gate|caller -o page.md [--facts sheet.json]`

Refused, each with its reason: a diff without §3's fields; two diffs of one geometry;
two diffs whose pair of commits, `identity`, `touched.nodes` or `per_feature` membership
differ (features do not depend on geometry: `_apply` runs apart from `compute_strata`,
`engine.py:287-300`; a difference means the two diffs are not one window); more than
two diffs.

`--origin gate` prints: "the pair the gate perturbs: HEAD and the commit K timeline
commits before it; chosen for the gate's stability test, not for this page".
`--origin caller` (the default) prints: "a pair chosen by whoever ran this command".
`regenerate_readings.py` passes `gate`.

## 5. The page

Wording rules for every fixed text: each denominator names its unit; the words
"stability", "stable", "unstable", "settled", "flicker" and "verdict" do not occur; the
gate's token is quoted in code font as a token. A test holds the list.

**Title.** `<repo> — one window: <before 12 hex> → <after 12 hex>`

**Scope, bold, first.** "**One pair of commits. Each line below is one event between
them, in a room nobody edited between them. Another pair of commits reads
differently.**"

**The window.** The pair; `--origin`'s sentence; first and last commit timestamps in the
window with offsets (and the two endpoints' when they differ from those); K commits;
rooms in both commits, born, deleted; edited n of the rooms in both (share); unedited n.

**5.1 Crossings.** One line per (room, term) among unedited rooms of rank and mixed
rows, where the term's outcome differs between the two sides. The row is the last
column.

| column | content |
|---|---|
| window | `<before 8 hex>→<after 8 hex>`, in every line |
| room | the path, with "(not edited in the window)" |
| term | the term text, e.g. `centrality >= p90` |
| value | earlier → later |
| cutoff | earlier → later; for a fixed-value term "fixed at 0.5" |
| later value against the earlier cutoff | `passes` or `fails`, by the term's own operator (`_cmp`) |
| earlier value against the later cutoff | `passes` or `fails` |
| rows | in words: "left hub (7 → 7 rooms: 2 edited rooms entered, 1 edited room left); left corridor (3 → 3 rooms: 1 edited room entered)". One predicate under two profiles is one row name with both profiles; sizes are `rooms_before → rooms_after` |

Cells that are not derived, each a fixed text: a fixed-value term has no second
comparison ("fixed threshold"); a clock term inside a mixed row prints its numbers and
"not compared: a clock term moves with the checkpoint"; a side whose evidence is
unavailable, or a term whose value, cutoff or outcome is null, prints "not available";
a room whose membership changed with no term changing outcome is one line with term
"none changed outcome" and the two sides' `diagnostic_eligible` values.

Under the table, fixed: "A percentile cutoff is computed from every room's value, this
room's included. The two comparisons are arithmetic on the four numbers beside them;
neither names a cause."

**5.2 Clock rows.** One line per clock row with a change among unedited rooms: the row,
`rooms_before → rooms_after`, how many unedited rooms left and entered, named up to
three, and "a clock row's membership moves with the checkpoint; not counted in the
gate's reading". (Run 71's reviewers differed on listing these; this is the count line
one asked for with the names the other allowed, outside the crossings table.)

**5.3 Excluded rows (◌).** One line per excluded row with a change among unedited
rooms: ◌ and the row name first, sizes, rooms named up to three, "excluded from the
diagnosis; not counted in the gate's reading". No values, cutoffs or comparisons: the
signal is unvalidated and the diff carries no evidence for it.

**5.4 Bands, per geometry supplied.** "Under the layer geometry, 4 of 35 unedited rooms
changed band: 2 with the same raw depth on both sides, 2 with a different raw depth."
Under age: "raw value". An `unknown` attribution prints as "raw value not recorded".
Rooms are filtered on `strata_evidence[].untouched` and named up to three per group. The
page says "band", never "floor".

**5.5 The gate's budget reading on this window, per geometry supplied**, each beside its
own numbers and never merged:

> age geometry — 2 unedited rooms, 2 crossings (4 of 35 `(profile, feature, room)`
> assignments; the 5% ceiling is exceeded at 2 assignments); bands 0 of 35 unedited rooms
> (exceeded at 2 rooms). The gate's token: `over_budget`, on features.

or "not judged: `<reason>`" with the ladder's reason verbatim. Then, fixed, after the
last geometry: "A reading of this one window (mapper spec §7 Q3). Whether it is usual
for a repository of N rooms has not been read (D-082). The same number of crossings
reads differently on a different number of rooms, so the token does not rank
repositories."

**5.6 What this page does not report.** Degraded marks (with the two counts); edited
rooms' changes beyond the counts in the rows column; any window but this one.

**Provenance.** Each diff's file name, both skeleton hashes, `identity`, the window page
version, the sheet's hash.

## 6. The sheet

`window_reading` (never `stability_window`): `scope` ("one window"), `scope_text` (the
bold sentence), `origin`, `origin_text`, `window` (shas, the four timestamps, K),
`rooms` (common, born, deleted, edited, unedited, edited_share), `crossings[]` (`room`,
`term`, `signal`, `operator`, `term_kind` rank|clock, `fixed_threshold`,
`value_before`, `value_after`, `cutoff_before`, `cutoff_after`,
`later_value_vs_earlier_cutoff`, `earlier_value_vs_later_cutoff` (each
true|false|null), `not_derived_reason`, `rows[]` with `names`, `profiles`, `direction`
left|entered, `rooms_before`, `rooms_after`, `edited_entered`, `edited_left`,
`born_entered`, `deleted_left`), `clock_rows[]`, `excluded_rows[]`, `bands[]` per
geometry, `gate_reading[]` per geometry (`geometry`, `token`, `reason`, `fired`,
`operands`, `distinct_rooms`, `distinct_crossings`, `qualifier_text`),
`not_reported`, `units`, `identity`, `window_page_version`, `facts_hash`.

## 7. The brief's pointer

`substrate brief SK [SB] --window W.facts.json`; the relint path takes the same option.
Refused if the sheet's after-commit is not the skeleton's. The header sentence's clause
(`brief.py:3261`, "stability is the `substrate timelapse` run under gate …, not this
page") becomes:

- with a sheet: "what differed between `<before>` (<date>) and this commit is on the
  window page `<file name>`, not this page";
- without: "no window page was rendered with this brief; it says nothing about how its
  rows differ between commits".

The sheet gains `window_ref` (`file`, `before_sha`, `after_sha`, `before_ts`,
`after_ts`) or null. No count crosses to the brief. Brief 0.45.0; every page's facts
hash and header change with the version, as on every bump. `test_brief.py:1923`
(the old clause) is rewritten for both cases.

## 8. Tests — fixture first (D-071)

A purpose-built two-snapshot fixture built in the test from synthetic substrates with
timelines (the pinned mcp fixture has stripped skeletons and no substrates, and `out/`
is ignored), under a test ruleset with an overlay, holding: (a) an unedited room whose
later value passes the earlier cutoff and whose earlier value fails the later; (b) one
failing both; (c) an entrant; (d) one predicate under two profiles; (e) two predicates
sharing a term; (f) a fixed-value term changing outcome; (g) a mixed row whose clock
term changes; (h) a clock row and an excluded row changing; (i) a born room entering a
row and a deleted room leaving one; (j) evidence missing on one side; (k) a commit
whose timestamp precedes the before-commit's.

- diff: every pre-existing leaf of the eight pinned comparisons is unchanged after §3
  (regenerated and compared, as at D-080 and D-082); `rooms_after` equals the after
  skeleton's fired count for every feature, born rooms included (negative control: the
  old `after` does not);
- page: every fixed text asserted against the sheet field it renders; each §5.1 cell
  state reached by a fixture case; (a) and (b) print different comparison cells and
  **the same** absence of any cause word; the word list of §5 is absent from the page;
  the window is in every crossing line;
- two geometries: two readings, each beside its numbers; a mismatched second diff is
  refused, with the matching one accepted as the negative control;
- brief: both clauses; a sheet for another commit refused;
- on the pinned mcp window (from `out/`, run by hand and recorded, not a unit test):
  two crossing lines (`src/types/index.ts` on `load_index >= p90`: passes / fails;
  `src/index.ts` on `centrality >= p90`: fails / fails, rows hub and corridor), one
  clock line (lit_room, 4), one excluded line (◌ crack, 2 rooms), bands 0 of 35 under
  age and 4 of 35 under layer, readings `over_budget` on features (age) and on
  features and bands (layer).

Then a seat on the rendered mcp window page: a plain skimmer and a hostile reader,
unpointed, before D-083 closes.

## 9. Not in scope

More than one window per page; any operand, ceiling, floor, K or token change; the
time-lapse's "over if any" aggregate (`timelapse.py:300-304`); a window page in the
time-lapse's scrubber.

## 10. Questions for the re-check

1. Is §3's table right about what `skeleton_diff` has at hand to compute each field,
   and is each addition outside every path that feeds an operand or the crossings?
2. Do §5.1's two comparison columns, with the not-derived states, cover every case the
   predicate grammar and the evidence can produce, with no cause implied?
3. Does anything on the page as specified still grade, rank or assert a property?
4. Is §4's refusal list sufficient for two diffs to be one window?

## 11. Re-check

*(appended; no code before it)*

Tracker run 72. measurement-validity-analyst: **UNSUPPORTED** on two fixed sentences,
with its nine run-71 findings resolved (13 claims: 8 supported, 2 qualified, 2
unsupported, 1 undetermined pending the seat). software-architecture-expert-validator:
**IMPRECISE 72** (from DIVERGENT 56): the contract collisions are gone, five of §3's
seven fields are computable as written, every addition is outside the operand paths;
four text defects. Where a section above and a line below disagree, the line below is
the contract.

1. **Clock terms are compared like every other term** (§5.1, §5.2). "Not compared: a
   clock term moves with the checkpoint" and "a clock row's membership moves with the
   checkpoint" are withdrawn: on mcp `lit_room`'s four unedited rooms went 16.61 → 242.08
   days while the cutoff fell 16.643 → 0.0188 as edited rooms reset, and either move
   alone evicts them. The sentences named half a cause — the third time in one day that
   a mechanism was written from one side of a two-sided comparison (D-082 F4, the first
   R4, this). §5.2 becomes: a count line per clock row, then the row's crossings in a
   table with §5.1's columns, headed "not counted in the gate's reading". No fixed text
   on the page names a mechanism; a test holds that against a word list ("because",
   "due to", "moves with", "caused", "pushed", "evicted", "drift").
2. **§5.5's qualifier** reads: "A reading of this one window (mapper spec §7 Q3). This
   page does not read whether it is usual for this repository. The same number of
   crossings reads differently on a different number of rooms, so the token does not
   rank repositories." The arithmetic clause reads "2 or more of 35 assignments is over
   0.05 by the gate's rule". §1's "nothing on it is graded" becomes "the page adds no
   grade; the gate's token is quoted as the gate's".
3. **The commit set is passed in, once.** `skeleton_diff` gains `window_commits`
   (`[{sha, ts}]`), supplied by the same call that computes `touched` and
   `commits_between` (`touched_since` on the CLI path, `touched_between` in the
   time-lapse; each gains a sibling returning the entries it counted). First and last
   are the minimum and maximum over parsed instants, printed as recorded. Null when the
   caller passes none or an entry has no `ts`.
4. **`identity`** records, for each side, the ruleset and each overlay as
   `{name, version}` and `mapper_version`, and for the pair
   `substrate_config_fingerprint` and `validation_config_fingerprint`. `substrate window`
   refuses a diff whose two sides differ in any of them (the predicates may differ), and
   two diffs whose identities differ.
5. **Two diffs are one window when** the pair of commits, `identity`, `commits_between`,
   `touched.nodes`, `rooms`, the whole of `per_feature` (evidence included) and
   `per_decorative_feature`, and the budget's constants are equal. Anything else is
   refused with the first differing field named.
6. **Words.** `--origin gate` prints "the pair the gate perturbs: HEAD and the commit K
   timeline commits before it; chosen for the gate's test, not for this page". The
   operand named `floors` in the diff is printed as "bands"; the token (`over_budget`,
   `within_budget`) is quoted. Rooms are "in no commit's recorded changes in the
   window", not "not edited"; the bold sentence reads "**One pair of commits. Each event
   below is between them. Another pair of commits reads differently.**" Born and
   deleted print as "only in the later commit" and "only in the earlier commit" (a file
   that changes kind leaves the room population without being deleted).
7. **Crossing lines** exist only for rooms that left or entered a row (the diff carries
   evidence for no others). Per room and row: if either side's evidence is unavailable,
   or the two sides' term lists differ, one line with term "not available". Otherwise
   one line per term whose two outcomes are both known and differ. If none differs: when
   any outcome is null, one line "not available"; else one line "none changed outcome"
   with each side's `diagnostic_eligible`, `graph_degraded` and `node_load_degraded`
   (null printed as "not recorded"). Lines for the same (room, term) from several rows
   are one line whose rows cell lists them.
8. **The sentence under the table**: "Each side's cutoff is computed over that commit's
   rooms that have a value (N earlier, M later), this room's included. The two
   comparisons are arithmetic on the four numbers beside them; neither names a cause."
9. **Rows merge** on predicate text: one entry naming every feature that has it, each
   with its profile ("foundation (maintainability, onboarding)").
10. **The brief's pointer** is also refused when the sheet's skeleton hash for the
    brief's geometry is not the brief's.
11. **Fixture case (j)** is a per-term null on one side, not an omitted substrate; an
    unavailable side is a second, separate diff.
12. **The seat's rule, written before it runs.** Readers: a plain skimmer on the whole
    mcp window page; a hostile reader on the whole page; a third reader given one
    crossing line pasted alone. The page fails if any reader (i) attributes a cause to a
    line, (ii) uses a property word of a room, a row or the repository (unstable,
    drifting, settling, degraded, fragile), or (iii) calls the gate's token a defect to
    fix. The three readers share a model family: agreement among them is one
    observation. Skimmer: "In two sentences, what does this page tell you about
    `src/index.ts` and about the hub row?" then "Is anything on this page a problem
    someone should fix?" Pasted line: "What does this line say?" Hostile reader: "Quote
    the sentence someone could cite as a claim about this repository, or a row, beyond
    these two commits."
13. **Excluded rows are counted, never named** (found while building, not by a reviewer):
    the brief spec's §1 cites excluded features "by count only — naming their rooms would
    hand a reader the salience the exclusion withholds" (D-028). §5.3 above named up to
    three rooms; the page and the sheet now carry the two counts and no path.

## 12. As built (2026-11-11)

`src/repo_substrate/window.py` (window page 0.1.0), `substrate window`, the diff's
additive fields (`mapper/diff.py`), `substrate brief --window` (brief 0.45.0), and the
window step in `scripts/regenerate_readings.py`. Tests: `tests/test_window.py` (21, on a
two-snapshot fixture built in the test). All eight pinned diffs regenerated under tag
`2026-11-11c-d083`: no pre-existing leaf differs from `2026-11-11b-d082`. The four briefs
differ from the `2026-09-24h` pages in the header sentence, the version and the facts
hash, and in nothing else.

The pinned mcp window page reads as §8 predicted, with one difference: the excluded line
gives counts (2 rooms left `crack`) and no names. Across the four pages every cell state
but two is reached on real data (compared with both comparisons; fixed threshold on the
registry and typeorm); "not available" and "none changed outcome" are reached by the
fixture only. typeorm's clock table is 48 lines, the longest thing on any of the pages.

Open until the seat (§11.12) has run.
