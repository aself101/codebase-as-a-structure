# Blind ranking — <repo name>

*One file per reference repo. Fill this in BEFORE reading any substrate output, report, or validation result for this repo. Once you have seen output the ranking is worthless. Save as `blind/<repo-name>.md`; it will be committed by hash before the first substrate run so it is sealed.*

*Paths are repo-relative and must exist at the repo's current HEAD. Rank strictly (1 = strongest); ties are fine if you genuinely cannot separate two, write them on one line. Ten per list is the target; fewer is fine if you run out of conviction, do not pad.*

**Repo:** `<name>`
**HEAD SHA at time of writing:** `<git rev-parse HEAD>`
**Date:**
**How well do you know this codebase right now?** (1 = barely, 5 = intimately)
**Have you seen any substrate output for this repo?** (must be "no")

---

## 1. Load-bearing (present position)

*"If I picked one file and asked 'how much of the rest of the codebase reaches this, directly or through a chain?' which ten score highest?" This is about the import graph as it is today, not about what would break.*

1.
2.
3.
4.
5.
6.
7.
8.
9.
10.

## 2. Next to be fixed (prediction)

*"Over the next stretch of work, which ten files are most likely to receive a bug-fix or revert commit?" This is a forecast about fix activity, not about quality. A file can be well-written and still be where fixes land.*

1.
2.
3.
4.
5.
6.
7.
8.
9.
10.

## 3. Unstable right now (present churn)

*"Which ten files are in active flux, being edited repeatedly, not settled?"*

1.
2.
3.
4.
5.
6.
7.
8.
9.
10.

## 4. Old, untouched, still depended on

*"Which ten files are the ones nobody has opened in a long time but the codebase still leans on?" The flooded basement.*

1.
2.
3.
4.
5.
6.
7.
8.
9.
10.

## 5. The one structural fact

*In one or two sentences: what is the single structural truth about this repo that a good map would have to show, and would be wrong if it missed?*

## 6. Anything you expect the metrics to get wrong

*Optional. Files or regions where you predict the numbers will mislead (vendored code, generated files, a monorepo package that skews everything, a file that is huge but inert). This is not part of the ranking; it is a pre-registered list of where you expect the substrate to lie.*
