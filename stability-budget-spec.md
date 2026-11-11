# The skeleton stability budget on a small population — what the verdict measures, and who reads it

Status: **decided 2026-11-11 (D-082): Alex agreed A now, D next, E deferred, no B, no C. A is implemented; D is `event-statement-spec.md`, in draft.**
Drafted 2026-11-11 after the D-080 replay (tracker run 69); reviewed the same day by
measurement-validity-analyst (UNSUPPORTED) and data-science-analyst (QUALIFIED 61),
tracker run 70. This is the second text. §8 lists what the review changed, including
the draft's statements that were wrong; the draft is in git only as this file's first
commit, so the corrections are named here rather than left to a diff.

The mapper spec §7 Q3 (D-018, D-024, D-026) is the contract this document reads.
Nothing here changes a mark, a population, an operand, a ceiling or a saved verdict.

## 1. The question

`mcp-secure-server` has read `over_budget` on the skeleton stability budget, in both
geometries, since D-078 excluded its example directories and reduced its page from 187
rooms to 65. D-080 explained the reading and kept it. Still undecided:

1. Is the reading a statement about the ruleset and geometry on this repository, or
   about the instrument at this population size?
2. What does the verdict do?

## 2. The instrument as it stands

`SKELETON_BUDGET` (`src/repo_substrate/mapper/diff.py:45-53`) and the verdict ladder
(`diff.py:382-399`):

- two operands, either one over its ceiling gives `over_budget`:
  *features* — changed (profile, feature, room) assignments of rank and mixed features
  over untouched rooms, divided by the union of such assignments (`diff.py:377-379`);
  *floors* — untouched rooms whose floor moved, divided by untouched rooms;
- ceilings 0.05 on each;
- judged only when 25 ≤ K ≤ 50, touched ≤ half of the common rooms, untouched rooms ≥ 30,
  and the feature union ≥ 20 assignments; otherwise `untested` with a reason.

The pinned comparison (gate k25k, `4c99da71468c` → `5348b3ef614d`, K = 25):

| | common | touched | untouched | feature union | features | floors (layer) | verdict |
|---|---|---|---|---|---|---|---|
| mcp-secure-server | 64 | 29 (0.45) | 35 | 35 assignments, 23 rooms | 4 / 35 = 0.114 (2 rooms, 2 crossings) | 4 / 35 = 0.114 | over_budget |
| typeorm | 571 | 52 | 519 | 427, 235 rooms | 7 / 427 = 0.016 | 0.000 | within_budget |
| uluops-registry-api | 206 | 38 | 168 | 215, 125 rooms | 1 / 215 = 0.005 | 0.000 | within_budget |
| eslint | 461 | 16 | 445 | 748, 426 rooms | 4 / 748 = 0.005 | 0.000 | within_budget |

Source: `reports/2026-11-11-d080-m2x/*.diff.json`. Both reviewers re-derived the table.

## 3. Findings

Scripts, outputs, the walk diffs and the commands that made them are in
`reports/2026-11-11-stability/` (`README.md` there).

**F1. mcp is judged at the edge of every gate, and the same rooms give three answers.**
Untouched rooms 35 against a floor of 30; touched fraction 0.45 against 0.5; feature
union 35 against 20. The window `0ad173e90af2` → `5348b3ef614d` (K = 23) has the same
touched set, the same two feature rooms and the same four floor moves as the pinned
window (K = 25) and reads `untested: below_pinned_k`; the two commits between the
starts touch `package.json` and a file touched again later. The K = 33 window
containing both reads `untested: touched_fraction_exceeds_floor` at 0.508. K counts
commits, not edits.

**F2. The verdict fires at two rooms.** 0.05 of a 35-assignment union is 1.75
assignments; 0.05 of 35 untouched rooms is 1.75 rooms. The four changed assignments are
two threshold crossings: `src/types/index.ts` on `load_index >= p90` (foundation, one
predicate under two profiles), `src/index.ts` on `centrality >= p90` (hub, and corridor
which adds `fan_out >= p50`). Counted in rooms it is 2 / 35 = 0.057, still over. The
comment that introduced the union floor says "two rooms flipping is not a rate"
(`diff.py:43-44`, and the docstring of `test_budget_refuses_a_tiny_jitter_population`,
which overrides the floor to 10⁶ and so cannot see this); the floor it introduced, 20
assignments, and D-018's `min_untouched_n = 30` on the floors operand (1.5 rooms) both
admit exactly that. The mapper spec states the union floor as "twenty rooms"
(`structural-mapper-spec.md:108`); the code counts assignments.

**F3. The unit.** D-018 says "one room in twenty"; the feature operand counts
assignments, and correlated predicates count one crossing more than once. No verdict in
the pinned set changes under a per-predicate, per-crossing or per-room count
(`operands_pinned.md` column O1; run 70's room-unit recompute).

**F4. Two mechanisms, both inside what D-018 set out to bound.** From
`transition_evidence`: `src/types/index.ts` moved 0.8434 → 0.8429 on load and stayed
above the before-cutoff (0.84085); it left because the cutoff rose to 0.84876 when a
touched room entered — a threshold-only crossing. `src/index.ts` moved 0.0134 → 0.0128
on centrality, below the before-cutoff (0.01285); it leaves with the cutoff held. Its earlier
value (0.0134) is also below the later cutoff (0.01426), so it leaves with the value held
too: either move alone suffices, and neither is "the" cause (D-080). *(Run 71 corrected
this: the text first booked the room as a value case, which is one inequality of two.)* D-018 names "a
percentile threshold shifted under it" as ripple the budget bounds, and a coupled
signal's ripple is the same class (D-033). Under cutoffs resolved over the untouched
rooms alone the pinned mcp comparison reads 0 / 44 (`operands_pinned.md` column O3):
re-ordering among the unedited rooms accounts for none of it.

**F5. Alternative operands.** *Cutoffs over the untouched rooms* (the D-033 remedy
carried to the skeleton) reads at or below the current operand on all six windows at
K ≥ 25 and removes displacement by touched rooms, which D-018 counts. It is rejected as
the judged operand on that ground alone, and kept as a reported decomposition (F4).
*Cutoff held* is rejected for mixed features only: 28 of mcp's 32 changes under it are
`flooded_basement`, whose clock term moves with the checkpoint; on rank-only features it
reads 4 / 12 on mcp and 4 / 88 on eslint (run 70, reviewer's script).

**F6. D-026's calibration does not hold on this population, and its own breaks-if is
met for layer floors.** D-026 placed K so the ceiling sits between the reference set's
median and 90th percentile of the operand. The K study read K = 25 only on the registry
(mcp at K = 5 and 10, substrate 0.3.0, before the D-067 and D-078 exclusions); the
comment at `diff.py:38-41` attributes K = 10, 25, 50 and 100 readings to K = 25. Four
walks of mcp at `--every 25` under gate k25k, two geometries from two starting commits
twelve apart (nine windows; within a start they do not overlap, across starts they do):

| start | geometry | windows | features: median, over 0.05 | floors: median, over 0.05 | judged | over |
|---|---|---|---|---|---|---|
| `5348b3ef` | layer | 5 | 0.029, 2 | 0.114, 4 | 2 | 1 |
| `5348b3ef` | age | 5 | 0.029, 2 | 0.000, 1 | 2 | 0 |
| `f1473915` | layer | 4 | 0.067, 3 | 0.068, 3 | 2 | 1 |
| `f1473915` | age | 4 | 0.067, 3 | 0.000, 0 | 2 | 1 |

The floors refuse five of the nine windows. The rule for reading this was stated by the
measurement reviewer before the second start was run: a layer-floors median over the
ceiling at both starts meets D-026's breaks-if ("a reference repository whose K = 25
median exceeds 0.05 … then the pinned K must fall, or the rule is restated per growth
rate"). It is over at both. The features operand's median is under at one start and
over at the other. D-026 also read layer as the stable geometry (median 0.000
everywhere) and age floors as the unstable element; on the 65-room mcp it is the
reverse. Nine windows on one repository, most of them under the untouched floor, is
thin; it is enough to say the calibration was not read here and does not obviously
hold, not enough to place a new K.

**F7. No judged verdict reaches a reader.** The verdict is printed on change sheets
(`cutaway.py:459-466`), coloured on the time-lapse page (`scripts/build_timelapse_page.py`),
summarised by the time-lapse (`timelapse.py:267-304`, as "over if any transition is
over" — a fourth meaning nobody chose) and tabulated by `regenerate_readings.py`. The
brief's provenance line sends the reader to the time-lapse for stability
(`brief.py:3261`), and the twelve-frame time-lapse judges no transition on any of the
four repositories under the pinned K (`reports/2026-09-24g-phase1x/*.frames.json`:
`beyond_pinned_k` on three, `below_pinned_k` ×10 and one touched-fraction refusal on
mcp). The eight judged readings are in `reports/<tag>-m2x/skeleton-budget.md`, which no
page cites and whose rows carry no population or gate column: the D-078 row and the
row before it are two instruments printed as one series (186 common rooms under gate
`177c129be9b5`, 64 under `298696064105`, different rooms moving). That is how the
reading changed at D-078 and stood unread.

**F8. What the reader of the mcp page is not told.** In the pinned window 11 of the 35
unedited rooms changed a mark or a floor — 7 on the age-geometry page the brief is
rendered from, 4 more as layer floors, which the brief does not draw *(run 71: the text
first said all 11 were "something the page prints")*: 2 left a rank row, 4 left `lit_room`,
4 moved a layer floor, and the excluded `crack` row lost `src/security/index.ts` as well
as `src/index.ts`.

## 4. What the findings settle

Question 1. The reading is true of the picture: unedited rooms did change marks and
floors in that window (F4, F8), and the rule was applied correctly. What it does not
support is the inference the spec attaches to it. One window on 35 unedited rooms fires
at two rooms (F2), the same rooms give three answers by where the window starts (F1),
and the calibration that was to say whether a reading is typical or tail was never read
on this population and its breaks-if is met for one operand (F6). Whether mcp's reading
is a persistent property of these rulesets and this geometry on 65 rooms is
**undetermined**.

Question 2. Nothing acts on a judged verdict (F7).

## 5. Constraints carried from earlier decisions

- D-012: a config may tighten a bar, never loosen it. Raising a minimum floor tightens;
  `untested` is a refusal, not a pass. D-012 does not forbid a resolution floor. What
  argues against one is choosing its number after the one failure it would remove.
- D-026: a ceiling is placed where it can fail, and its breaks-if names what happens
  when a repository's K = 25 median exceeds it.
- D-077 (run 65): counts under a counterfactual split are quota arithmetic. An observed
  crossing in a recorded window is not that, but in a fixed-share row a leaver implies
  an entrant, and printed alone it reads as a fact about the leaver.
- D-078: the example exclusion stands. D-080: no causal edge for a raw-value change.
- The page's grammar (D-049 onward): counts with their denominators, no grades.

## 6. Options, as they stand after review

**A. Restate the meaning and carry the resolution on the datum.** Mapper spec §7 Q3
says one thing: *on one window at 25 ≤ K ≤ 50, more than 5% of the rank and mixed
assignments held by unedited rooms, or of the unedited rooms' floors, changed; it
describes this ruleset and geometry on this window and population; whether that is
typical or tail for the population is read separately and has not been read for
populations under about 200 rooms.* D-018's "defect" sentence stays with its date and
its K; the K study's reading of what firing means (self-relative percentile calibration
under growth) stays beside it. The "not a rate" sentence is withdrawn from the comment
and the test docstring, and the comment's K = 25 provenance corrected. The diff's budget
block gains, with no change to any verdict: which operand fired, the ceiling in whole
units for each operand (`ceil(0.05 × denominator)`), the count of distinct crossings,
and the window's two shas. `skeleton-budget.md` gains population and gate columns and a
series-break mark. D-026's breaks-if is logged as met for layer floors on mcp.

**B. A resolution floor.** Judge only when each ceiling is worth at least N whole rooms,
N derived in advance from the withdrawn sentence, applied to both operands and every
repository, with the list of historical verdicts it moves written down first. mcp would
be `untested` in essentially every window. Defensible if the token is meant to assert a
property; costs the one alarm unless D exists.

**C. Change the judged operand.** Rejected on construct grounds (F5).

**D. A reader on the page.** As a dated event statement, never a property of the row:
for the gate's own window, named by its two shas and dates, each rank or mixed row says
which unedited rooms left and which rooms entered, one count per predicate, with the
mechanism from D-080's evidence (cutoff moved; the room's own value moved); the floors
likewise; what prints when the window is refused is fixed in advance; whether clock
rows and excluded rows carry it is decided in D's own section. The provenance line
stops pointing at a run that judges nothing. D is a new measurement and needs its own
spec section, fixture case first, and a re-seat under D-075's rule.

**E. Re-read the calibration.** D-026's stated consequence when its breaks-if is met:
lower the pinned K for such populations or restate the rule per growth rate. Needs a K
study at the current substrate on all four repositories (the 2026-09-05 study predates
six substrate versions and both exclusions). The largest piece of work here, and it
calibrates a token that today has no reader.

**Recommendation: A now, D next as its own spec, E deferred until D gives the verdict a
reader; not B, not C.** A is true whatever else is decided and moves no verdict. D is
the precedent the project has set for every disclosed instability — the number goes in
the cell it qualifies — and it is the only option that would have caught the D-078
change the day it happened. E is what D-026 itself prescribes, and it is the honest
answer to "is the pin calibrated?"; doing it before anything reads the verdict would be
calibrating for nobody. B is where the reviewers and the draft disagree least clearly:
both reviewers say it is admissible and neither recommends it over carrying the
resolution on the datum.

One thing for Alex beyond the options: on the 65-room mcp the layer geometry's floors
are the unstable element and the age geometry's are still, the reverse of D-026 and of
the time-lapse spec's "layer where stability matters". Recorded, not acted on.

## 7. Questions put to the reviewers, and their answers

1. *Can one over_budget at K = 25 on 65 rooms be told from D-026's designed tail?* Both:
   no. The calibration never covered this population.
2. *Is D's per-row count D-077's quota arithmetic?* Both: not in kind (observed, not
   counterfactual); it inherits the fixed-share coupling and must print entrants.
3. *Does one window support a per-row statement?* Both: a dated event statement only.
4. *Must "the ceiling is under one room" produce `untested`?* Both: no; it is a
   resolution limit the token must carry. The draft's rejection of B misread D-012.
5. *Does A's interpretation match the instrument?* Both: partly; "tail" and "shrinks
   with size" were unsupported. They differ on "defect": the measurement reviewer would
   date-stamp or delete it, the data-science reviewer would keep the K study's reading
   of it. A keeps both sentences, dated.

## 8. Review (tracker run 70) and what it changed

measurement-validity-analyst 1.0.0, **UNSUPPORTED**: of ten claims about the token, one
supported (the rule was applied correctly), three qualified, five unsupported, one
undetermined. data-science-analyst 1.0.4, **QUALIFIED 61**: the table, F1, F2's
arithmetic, F3 and the core of F7 warranted; F6 and the grounds for rejecting B
unwarranted; A + D supportable with changes. Twenty issues filed, six convergent pairs.

Statements in the draft that were wrong, and are corrected above:

- *F6, "one over-budget reading is, by the budget's own calibration, not rare".* The
  calibration was never read on mcp at K = 25 nor on 65 rooms; the 53% was the registry,
  age geometry, either operand, unfloored. Replaced by the four walks and D-026's
  breaks-if. The draft's §4 clause "designed to be common" is withdrawn.
- *F4, "the four changed assignments are displacements".* Right for one room; the other
  crossed on its own value. The same error is in the D-080 replay addendum
  ("every untouched loss is a displacement by a touched room") and is corrected there.
- *F5's grounds against the untouched-cutoff operand.* The four "reads higher" cases
  were K = 15 windows, outside the instrument's range; "removes what D-018 says a reader
  sees" misquoted D-018, which says that of the whole-population numbers.
- *F5, "holding the cutoff measures the clock".* True of mixed features only.
- *F7, "the only code that reads the verdict is the time-lapse summary".* Three other
  places print it. The substance stood.
- *F8, 10 of 35.* 11: the excluded `crack` row lost a second unedited room.
- *§6 B, "a floor moved after a failure, which D-012 exists to refuse".* D-012 refuses
  loosening; a higher minimum tightens. The objection that survives is post-hoc choice.
- *F2, "one room alone is 0.057".* Only through hub and corridor sharing a term.

Checked by me against the tree before acting: the K = 23 window (the two commits between
the starts, from the after-substrate's timeline); the other verdict consumers; the
`crack` room and the direction of the four `lit_room` changes (all losses); that the
walks ran under fingerprint `298696064105`. Not re-derived by me: the reviewer's
rank-only cutoff-held figures.

Not done: no age or layer walk on the other three repositories; no K other than 25; the
walk skeletons are not committed (the diffs and the commands are).
