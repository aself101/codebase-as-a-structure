# The stability window on the page — an event statement (D-082 option D)

Status: **reviewed (tracker run 71); the draft's form does not stand; where the statement lives is put to Alex (§10). Nothing implemented.** Proposed D-083. Written 2026-11-11.
Parent: `stability-budget-spec.md` (D-082), whose option D Alex accepted as "next, under
its own spec". The architect-brief spec §1 is the contract this changes. §9 holds the
review before any code.

## 1. What is being added, and what it is not

A section of the brief that states, for **one named pair of commits**, which rooms left
or entered each printed row without their own file being edited between the two, and
which unedited rooms moved a floor. It is an **event statement**: what differed between
two snapshots. It is not a property of a row, a room, a ruleset or the repository, it
is not a rate, and it grades nothing.

It exists because the page says nothing today about a reading the system computes and
nobody reads (D-082 F7, F8): on `mcp-secure-server`, between `4c99da71468c`
(2026-01-28) and `5348b3ef614d` (2026-09-10), 25 commits apart, 11 of the 35 unedited
rooms changed something the page prints.

Run 70's conditions on this measurement (measurement-validity-analyst F-9,
data-science-analyst Q2 and Q3) are requirements here, numbered R1–R7 in §4.

## 2. Current state (read from the tree)

- `substrate brief skeleton [substrate]` (`src/repo_substrate/cli.py:118-137`) builds a
  facts sheet from one skeleton and one substrate (`brief.py:39`, `facts`) and renders
  Register → rooms at the most positions → shared rooms → excluded marks → stance →
  provenance (`brief.py:3245`, `render_brief`). It takes no second snapshot.
- The provenance line ends "stability is the `substrate timelapse` run under gate …,
  not this page" (`brief.py:3261`). The twelve-frame time-lapse judges no transition on
  any reference repository (D-082 F7).
- `scripts/regenerate_readings.py` already writes, per repository and geometry, the
  diff of HEAD against the gate's stability perturbation (`reports/<tag>-m2x/
  <short>.<geometry>.diff.json`) before it writes the briefs (step 1, then step 3 at
  lines 222-245), from the age skeleton the brief also reads.
- That diff carries, per `profile/feature`: `kind`, `before`, `after`, `added`,
  `removed`, `untouched_affected_rooms`, and `transition_evidence` with both sides'
  term values, cutoffs and outcomes (D-080); `touched.nodes`; `strata_evidence` with
  `untouched` and `attribution` per moved room; and `budget` with `window`, `operands`,
  `fired`, `verdict`, `reason` (D-082). Decorative (◌) features are **not** in
  `per_feature`; their change is only a count (`untouched.decorative_changes`).
- The diff's `before.repo` and `after.repo` hold `head_sha` and `name`, no date. The
  after-substrate's `timeline` has an entry per commit with `sha` and `ts`
  (verified on the mcp cache: `4c99da71…` at `2026-01-28T07:44:41-10:00`).
- The register renders one predicate under two profiles as one row (D-063) and a
  feature's name with its position (D-074).

## 3. Inputs

`substrate brief skeleton substrate --stability <diff.json> [--stability <diff.json>]`.

- A diff is accepted only if its `after.repo.head_sha` equals the skeleton's and its
  `budget.window` is present (a diff written before D-082 is refused with that reason).
- The diff whose `after.skeleton_hash` equals the brief's skeleton hash is the **row
  source**: its `per_feature` is this page's rows. At most one. A diff of another
  geometry at the same pair of commits contributes its floors only. Any other
  combination — a different `before`, two row sources — is refused; nothing is merged
  by guess.
- With no `--stability`, the section is replaced by one sentence (§5, R6) and the page
  is otherwise unchanged.
- `regenerate_readings.py` passes both geometries' diffs for the pinned window.

## 4. Requirements

**R1. The window is named, with dates.** Both revisions (12 hex), each commit's date
from the after-substrate's `timeline[].ts`, and the commit count. "The last 25 commits"
never appears: on mcp that phrase covers seven months. If a date cannot be read the
cell says "date not recorded".

**R2. Entrants beside leavers, and the row's size on both sides.** For each row:
size before → after; unedited rooms that left; unedited rooms that entered; and how
many *edited* or *born* rooms entered and left (counted; named up to three, the page's
existing convention). A row that kept its size says so in the same clause, because in a
fixed-share row a leaver and an entrant are one event read twice.

**R3. One entry per predicate.** A predicate under two profiles is one row here, as in
the register. Two predicates that share a term stay two rows (hub, corridor); each
names the term that changed outcome, so the shared crossing is visible as shared.

**R4. The observation, not a cause.** For each unedited room that left or entered a
rank or mixed row: the term whose outcome changed, the room's value before → after, and
the cutoff before → after, from `transition_evidence`. Then one of two fixed phrases
derived from those four numbers alone: "its value would still clear the earlier
cutoff" or "its value crossed the earlier cutoff". No sentence says why a value or a
cutoff moved (D-080). When either side's evidence is unavailable the cell says
"evidence not available for this side" and no phrase is derived.

**R5. Floors per geometry supplied.** "Under the layer geometry 4 of 35 unedited rooms
moved a floor: 2 with the same dependency depth on both sides, 2 with a changed depth",
from `strata_evidence[].attribution`; rooms named up to three per group. A geometry not
supplied is not mentioned.

**R6. What prints when the window is refused or absent.** Events are observations and
print whenever a diff is supplied. The verdict clause reads the diff's own token:
judged (`within_budget`, or `over_budget` with the operands that fired, each with its
numerator, denominator and "over at n") or "not judged: <reason>" verbatim from the
ladder. With no diff: "No stability window was supplied to this page; it says nothing
about how its rows move between commits."

**R7. The scope sentence, fixed, in bold, first in the section:**
"**What changed between two commits, in rooms nobody edited between them. One window:
it is not a measure of how settled a row is, and another pair of commits reads
differently.**" The verdict clause follows the events, not the reverse, and carries
"a statement about this window (mapper spec §7 Q3)".

## 5. What the page gains

One section, after "Shared rooms" and before "Marks excluded from the diagnosis":

    ### Between two commits: rooms that moved without being edited

    **<R7>**

    Window: `4c99da71468c` (2026-01-28) → `5348b3ef614d` (2026-09-10), 25 commits;
    64 rooms in both, 29 edited, 35 not edited.

    | row | kind | rooms before → after | unedited rooms that left | unedited rooms that entered | edited or born rooms: entered · left |
    | foundation · high-load node | import graph and size | 7 → 7 (size kept) | src/types/index.ts — `load_index >= p90`: 0.8434 → 0.8429, cutoff 0.84085 → 0.84876; its value would still clear the earlier cutoff | none | 1 · 0 |
    | hub | import graph | 7 → 7 (size kept) | src/index.ts — `centrality >= p90`: 0.0134 → 0.0128, cutoff 0.01285 → 0.01426; its value crossed the earlier cutoff | none | 2 · 1 |
    | …

    Floors: under the layer geometry 4 of 35 … ; under the age geometry none of 35.

    This window's stability verdict (a statement about this window, mapper spec §7 Q3):
    over the ceiling on features, 4 of 35 assignments (over at 2), 2 distinct crossings …

Rows with no unedited change are not listed; a closing line counts them ("5 other rows
had no unedited room leave or enter"). The register's rows are **not** changed: no new
clause in its eighth column (D-068's finding about that column stands).

The provenance line's stability clause becomes "stability: the window above" or, with
no diff, "stability: no window supplied".

Sheet fields (`stability_window`): `before_sha`, `after_sha`, `before_ts`, `after_ts`,
`commits_between`, `common`, `edited`, `unedited`, `rows[]` (`names`, `profiles`,
`kind`, `predicate`, `before`, `after`, `left_unedited[]`, `entered_unedited[]` each
with `room`, `term`, `value_before`, `value_after`, `cutoff_before`, `cutoff_after`,
`clears_earlier_cutoff` (true | false | null), `entered_edited`, `left_edited`,
`entered_born`), `rows_unchanged`, `floors[]` (`geometry`, `moved`, `of`,
`same_raw`, `changed_raw`, `unknown`, `rooms[]`), `verdict`, `reason`, `fired`,
`operands`. Units recorded in the sheet's `units` block. Absent when no diff is given,
so a page without a window keeps its facts hash.

## 6. Decided here, with the reason

- **Clock rows are listed, marked "clock — not counted in the verdict".** `lit_room`
  lost four unedited rooms on mcp; the page prints that row and a reader sees it. For a
  clock row no value/cutoff phrase is derived beyond the numbers (the clock moves every
  value).
- **Excluded (◌) rows are listed, marked ◌ and "not counted in the verdict".** This
  needs the diff to carry decorative features' `added`/`removed`/`untouched_affected_rooms`
  the way it carries diagnostic ones (today only a count): an additive field
  `per_decorative_feature`, no operand touched.
- **A separate section, not a clause on each register row.** The register's rows state
  the snapshot; this states a difference between two. Mixing them puts a dated event in
  a cell that otherwise holds present-tense facts.

## 7. Not in scope

- Any change to the operand, the ceilings, the floors, K or a verdict.
- More than one window. "Left or joined in k of n windows" is the statement that could
  support a property reading (run 70); it needs a walk per repository and is option E's
  neighbour, not this.
- The time-lapse's `budget_reading` ("over if any transition is over",
  `timelapse.py:300-304`), a fourth meaning for the token. Recommended separately: drop
  the aggregate and print the tally it is derived from.

## 8. Tests and acceptance

Fixture case first (D-071): a two-snapshot fixture where (a) an unedited room leaves a
fixed-share row on the cutoff alone, (b) one leaves on its own value, (c) a row changes
size, (d) one predicate sits under two profiles, (e) two predicates share a term, (f) a
clock row and a ◌ row change, (g) evidence is missing on one side.

- every fixed sentence on the page is asserted against the sheet field it renders;
- R4's phrase is asserted against the four numbers, both ways, and absent under (g);
- a mismatched diff (other `after`, pre-D-082, two row sources) is refused, each with
  its reason; negative control: the same call succeeds with the matching diff;
- with no `--stability` the page's bytes outside the provenance clause equal today's;
- on the pinned mcp window the section names `src/types/index.ts` and `src/index.ts`
  with the D-080 numbers, 11 unedited rooms in all across rows and layer floors, and the
  verdict clause "over the ceiling on features … (over at 2)";
- brief 0.45.0; four pages regenerated; a re-seat (control on mcp-secure-server and a
  plain skimmer) under D-075's shape-change rule before the decision is closed.

## 9. Questions for the reviewers

1. Does the section, as specified, stay an event statement, or will its table be read
   as "rows that are unstable" regardless of R7?
2. Is R4's two-phrase classification an observation the four numbers support for every
   operator and for conjunctions, or does it smuggle a cause?
3. Is listing clock and ◌ rows (§6) a disclosure or noise that dilutes the two rooms
   the verdict counted?
4. Does naming the gate's own perturbation window give it an authority it has not
   earned — it was chosen as the gate's K = 25 cut, not as a reader's interval?
5. Is anything in §2 wrong about the code?

## 10. Review (tracker run 71) and the question it leaves

measurement-validity-analyst 1.0.0 (the run 70 instance, continued): **UNSUPPORTED** —
of twelve claims two supported, six qualified, three unsupported, one undetermined.
software-architecture-expert-validator 1.0.4: **DIVERGENT 56** (it notes its two scales
disagree at 56 and chose the harsher). adoption-drift-detector 2.2.2: **DRIFTED 44**
(it notes the verdict turns on rating five silent misreadings HIGH; at MEDIUM, 74).
Twenty-eight issues, six convergent clusters.

**What does not stand in §§1–9 above (kept as drafted; this list is the correction).**

- *R4's two phrases.* All three reviewers. For `src/index.ts` on hub the later value
  fails the earlier cutoff **and** the earlier value fails the later cutoff: either move
  alone suffices, and "its value crossed the earlier cutoff" books a cause. The phrases
  are also undefined for entrants, for `==` and fixed-value terms (no cutoff moves), for
  conjunctions with more than one changed term, for a clock term inside a mixed row, and
  for a membership change with no term changed. A reader takes the two phrases as real
  versus benign and bisects. Replacement: the four numbers, and both comparisons stated
  neutrally (later value against the earlier cutoff; earlier value against the later
  cutoff), or the numbers alone.
- *R2's inputs.* The diff's `per_feature` sets are over rooms present in both commits
  (`diff.py:349-350`); born rooms are in neither `added` nor `touched.nodes`. mcp's
  scaffolding is 31 → 35 in the diff and 31 → 36 in the skeletons. Row sizes and born or
  deleted rooms come from the two skeletons, or the diff gains the lists.
- *§1's "11 … the page prints".* 7 on the age page (2 rank, 4 clock, 1 excluded); the
  other 4 are layer floors the brief does not draw.
- *§5, "a page without a window keeps its facts hash", and §8, "bytes … equal
  today's".* `brief_version` is inside the hashed sheet; the bump changes every page.
- *One verdict clause.* Two geometries carry two tokens (age: features; layer: features
  and floors).
- *The row-major table.* Listing only rows that changed, with a count of the rest, is
  how a list of unstable rows is built; R7's caption does not travel with a pasted row,
  and the row carries no window. One line per crossing, the window in every line.
- *"over the ceiling … (over at 2)" and the word "stability".* Read as a budget overrun
  to fix, "2 over", and the one token on the page that looks comparable across
  repositories (eslint and mcp both read 2 crossings; one is within, one over). The
  clause must carry "has not been read for a repository this size" and lead with rooms
  and crossings.
- *Floors on the brief.* "Floor" already means a threshold on the page (six uses), and
  the brief draws no floors.
- *The heading.* "Moved without being edited" reads as renamed files.
- *The sheet field.* `stability_window.verdict` reaches an agent without its scope.
- *§2.* The stability clause is in the header sentence, not the Provenance section;
  D-074 pairs only names flagged `name_implies_consequence`.

**Where the reviewers differ.** Clock rows: the measurement reviewer supports listing
them given the calendar span; the drift reviewer would collapse them to one count line,
since an unedited room leaving `lit_room` is what unedited means.

**The contract finding, and the question.** The register's bold rule, asserted by a
test, says "no count on this page compares across repositories, or across snapshots of
this one" (`brief.py:2996`). The brief spec says the page "may say what the skeleton
says and nothing else" (§1), that its facts are "a pure function of the skeleton"
(§2.1), and that excluded features are cited by count only. This spec named that
contract and did not amend it. Two forms are open:

- **On the brief, reformed.** One line per crossing with the window in each line; no
  floors; the gate's reading renamed and qualified; the register's rule and three
  contract sentences amended to admit one dated window; the relint path and `facts`
  take a diff.
- **A page of its own, per window.** `<short>.window.md`, rendered from the two
  skeletons, the two substrates and the diffs: the crossings, both geometries' floors
  and readings each beside its own numbers. The brief stays a one-snapshot page; its
  header's stability clause names the window page and the pair of commits, or says no
  window was read.

Recommended: the page of its own. The one-snapshot rule is the brief's most-tested
property (thirteen unpointed rounds were read against it); every finding above about
floors, two verdicts, the relint path and the hash dissolves when the statement is not
on the brief; and a statement about a window is the natural subject of a page about a
window. What it costs: a pointer is weaker than a cell — D-082 argued "the number goes
in the cell it qualifies" — and the change sheet is a precedent for a two-snapshot
artifact nobody opened. The pointer therefore has to be specific (the pair, the dates,
the file) and the window page has to be regenerated and committed beside the brief.

Alex accepted D as "a reader on the page". Moving it off the page changes what was
accepted, so the choice goes back to him.
