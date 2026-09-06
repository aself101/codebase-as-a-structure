# The K study — jitter per transition at every K, and where the budget can fail (D-025, D-026)

*2026-09-05. `substrate timelapse --every K` on the four reference repositories, both geometries, maintainability + onboarding, gate `reports/2026-09-05-m1b/`, substrate 0.3.0. K = 5 and 10 on mcp-secure-server; 10, 25, 50 on uluops-registry-api; 50, 100 on typeorm; 100, 250 on eslint. Per transition: jitter churn (rank + mixed feature churn over untouched rooms, D-024) and untouched strata movement. Manifests and pages in `out/kstudy/` (not committed; rebuild with the commands in D-025).*

| repo | geometry | K | transitions | jitter share | jitter churn median / p90 / max | untouched strata median / p90 / max | share of transitions over 0.05 (either) |
|---|---|---|---|---|---|---|---|
| eslint | age | 100 | 86 | 0.16 | 0.028 / 0.125 / 1.000 | 0.030 / 0.133 / 0.667 | 0.43 |
| eslint | age | 250 | 34 | 0.16 | 0.062 / 0.312 / 1.000 | 0.068 / 0.286 / 0.647 | 0.85 |
| eslint | layer | 100 | 86 | 0.13 | 0.028 / 0.125 / 1.000 | 0.000 / 0.000 / 0.856 | 0.23 |
| eslint | layer | 250 | 34 | 0.14 | 0.062 / 0.312 / 1.000 | 0.000 / 0.000 / 0.885 | 0.62 |
| mcp-secure-server | age | 10 | 13 | 0.26 | 0.022 / 0.066 / 0.254 | 0.000 / 0.360 / 1.000 | 0.46 |
| mcp-secure-server | age | 5 | 26 | 0.33 | 0.008 / 0.089 / 0.360 | 0.000 / 0.433 / 1.000 | 0.27 |
| mcp-secure-server | layer | 10 | 13 | 0.16 | 0.022 / 0.066 / 0.254 | 0.000 / 0.033 / 0.044 | 0.23 |
| mcp-secure-server | layer | 5 | 26 | 0.21 | 0.008 / 0.089 / 0.360 | 0.000 / 0.013 / 0.043 | 0.15 |
| uluops-registry-api | age | 10 | 80 | 0.25 | 0.017 / 0.084 / 0.190 | 0.009 / 0.127 / 0.750 | 0.28 |
| uluops-registry-api | age | 25 | 32 | 0.28 | 0.034 / 0.143 / 0.211 | 0.043 / 0.249 / 0.706 | 0.53 |
| uluops-registry-api | age | 50 | 16 | 0.27 | 0.050 / 0.161 / 0.318 | 0.102 / 0.381 / 0.690 | 0.75 |
| uluops-registry-api | layer | 10 | 80 | 0.19 | 0.017 / 0.084 / 0.190 | 0.000 / 0.088 / 0.500 | 0.25 |
| uluops-registry-api | layer | 25 | 32 | 0.20 | 0.034 / 0.143 / 0.211 | 0.000 / 0.106 / 0.500 | 0.47 |
| uluops-registry-api | layer | 50 | 16 | 0.19 | 0.050 / 0.161 / 0.318 | 0.014 / 0.128 / 0.483 | 0.75 |
| typeorm | age | 100 | 38 | 0.16 | 0.049 / 0.342 / 0.395 | 0.028 / 0.372 / 1.000 | 0.53 |
| typeorm | age | 50 | 76 | 0.15 | 0.027 / 0.235 / 1.000 | 0.012 / 0.256 / 1.000 | 0.36 |
| typeorm | layer | 100 | 38 | 0.12 | 0.049 / 0.342 / 0.395 | 0.000 / 0.030 / 0.535 | 0.50 |
| typeorm | layer | 50 | 76 | 0.12 | 0.027 / 0.235 / 1.000 | 0.000 / 0.038 / 0.553 | 0.34 |

*Jitter share* is the D-024 share of all movement. *Jitter churn* and *untouched strata* are per-transition distributions. The last column is the share of transitions that exceed 0.05 on either.

## Readings

- **Jitter share is a property of the repository, not the schedule.** Within a repository it barely moves with K: registry 0.25 / 0.28 / 0.27 (age, K = 10 / 25 / 50), typeorm 0.15 / 0.16 (K = 50 / 100), eslint 0.16 / 0.16 (K = 100 / 250), mcp 0.33 / 0.26 (K = 5 / 10). Nagarjuna's SV-1 (D-024) is answered by measurement: the share can be quoted per repository, with K, and it will hold.
- **Jitter churn per transition grows with K at a rate set by growth.** Medians: registry 0.017 → 0.034 → 0.050 at K = 10 → 25 → 50; typeorm 0.027 → 0.049 at 50 → 100; eslint 0.028 → 0.062 at 100 → 250; mcp 0.008 → 0.022 at 5 → 10. The median crosses the 0.05 ceiling at roughly K ≈ 50 on the registry, ≈ 100 on typeorm, ≈ 200 on eslint, ≈ 25 on mcp — the faster a repository grows, the fewer commits it takes to re-rank a twentieth of its untouched rooms.
- **Where the ceiling can cut a tail.** At K = 5 nothing fires it (D-024). At K = 25 on the registry the ceiling sits between the median (0.034) and the 90th percentile (0.143), and 53% of transitions exceed it; at K = 10 on mcp between 0.022 and 0.066; at K = 50 on typeorm between 0.027 and 0.235; at K = 100 on eslint between 0.028 and 0.125. The ceiling separates typical from tail on every repository once K is in the tens, without being moved. That is the calibration rule D-026 adopts: **pin the budget at the K where 0.05 lies between the reference set's median and its 90th percentile**, which is K = 25, applied up to 50.
- **Age-geometry floors are the least stable element of the skeleton.** Untouched strata movement under age geometry: p90 0.13–0.43, medians up to 0.10 (registry, K = 50); under layer geometry: median 0.000 everywhere, p90 ≤ 0.13, with maxima of 0.5–0.9 at mass restructurings. Age bands are quantiles of `age_days`, and on a growing population they re-rank wholesale between frames; layer depth moves only when the graph does. A second, looser ceiling for age strata would be tuned to pass; the honest reading is that percentile age bands are not a stable floor on growing repositories, and that absolute-era bands (D-019's calibration argument applied to strata) are the design change — recorded as mapper §7 Q6, not built.
- **Degenerate transitions.** Two typeorm transitions at K = 50 report jitter churn 1.000 and 0.500 over unions of 2 and 10 rooms; two eslint transitions at K = 100 report 1.000 over unions of 145–192 rooms with 83 and 66 untouched — mass edits that touched most of the repository and re-ranked every room left. The first kind is refused by the new `min_jitter_union` floor (20); the second by the existing touched-fraction floor.

## What this decides

`SKELETON_BUDGET` is re-pinned at `pinned_k = 25`, `max_k = 50`, ceilings unchanged, `min_jitter_union = 20` (D-026). Under it the budget fires on a substantial share of transitions on every repository — it is an instrument that can fail — and what it fails on is a fact about self-relative calibration on growing populations: the maintainability ruleset's percentile features and the age geometry's quantile floors are not stable at K = 25 on a repository that grows by a tenth between frames. That is the finding; the ceiling is not tuned to hide it.

## Verdicts under the re-pinned budget (D-026 addendum)

*Regenerated from cache after D-026: `pinned_k = 25`, `max_k = 50`, `min_jitter_union = 20`. Runs at K > 50 are `untested: beyond_pinned_k` throughout and are not listed.*

| repo | geometry | K | transitions | judged | over | within | untested (reason × n) |
|---|---|---|---|---|---|---|---|
| mcp-secure-server | age | 10 | 13 | 12 | 5 | 7 | touched_fraction_exceeds_floor × 1 |
| mcp-secure-server | age | 5 | 26 | 25 | 6 | 19 | touched_fraction_exceeds_floor × 1 |
| mcp-secure-server | layer | 10 | 13 | 12 | 3 | 9 | touched_fraction_exceeds_floor × 1 |
| mcp-secure-server | layer | 5 | 26 | 25 | 4 | 21 | touched_fraction_exceeds_floor × 1 |
| uluops-registry-api | age | 10 | 80 | 78 | 21 | 57 | beyond_pinned_k × 1, touched_fraction_exceeds_floor × 1 |
| uluops-registry-api | age | 25 | 32 | 30 | 15 | 15 | beyond_pinned_k × 1, touched_fraction_exceeds_floor × 1 |
| uluops-registry-api | age | 50 | 16 | 10 | 8 | 2 | beyond_pinned_k × 5, insufficient_untouched_population × 1 |
| uluops-registry-api | layer | 10 | 80 | 78 | 19 | 59 | beyond_pinned_k × 1, touched_fraction_exceeds_floor × 1 |
| uluops-registry-api | layer | 25 | 32 | 30 | 13 | 17 | beyond_pinned_k × 1, touched_fraction_exceeds_floor × 1 |
| uluops-registry-api | layer | 50 | 16 | 10 | 7 | 3 | beyond_pinned_k × 5, insufficient_untouched_population × 1 |
| typeorm | age | 50 | 76 | 36 | 6 | 30 | beyond_pinned_k × 36, touched_fraction_exceeds_floor × 4 |
| typeorm | layer | 50 | 76 | 36 | 7 | 29 | beyond_pinned_k × 36, touched_fraction_exceeds_floor × 4 |

The budget now fails on a substantial share of the transitions it judges on every repository. What it fails on is stated above: percentile features and quantile age floors under growth.
