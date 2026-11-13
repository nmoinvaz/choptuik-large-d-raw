# I681-win: RT's K = 7 bounds against the K = 0 trend with 12 starts per state (rt_sigma.py, rough starts)

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/681 (the coordinator's message `1794569651229-0` on the `choptuik-large-d` channel; follows #671, raw `I671-win/` at 07961b4b, #643, `I643-win/` at 2927452a, #423 and #163). Worktree `choptuik-i423` (main 5135cdeb, `solver/rt/rt_sigma.py`), venv-t151 (Python 3.10, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0) through `rt_launch.py` and `resource.py` (copied from `I423-win/`; no repository file changes). BelowNormal. BLAS threads: two per run (the 32x121 matrices are 1.4 GiB, under the 3 GiB rule of AGENTS.md), three runs at a time = 6 busy threads.

## Plan, written before the runs (the issue's acceptance)

1. **Checks first**: `rt_sigma.py --planted` must exit 0 and `--planted --mutate=shift` must exit 1 (`logs/planted.log`, `logs/planted_mutate_shift.log`).
2. **Six runs**, `rt_sigma.py STATE --starts 12 --rough` on each of the six states of #671 / #643, read in place from the raw repository's origin/main checkout:

   | D | K = 7 root | K = 0 control (same start, rows dropped) |
   |---|---|---|
   | 40.020065 | `I671-win/solves/k7_D40_D40.0201_32x121.npz` | `I671-win/solves/k0_D40_mutnorows_D40.0201_32x121.npz` |
   | 50.007491 | `I163-mac/acc/a_32x121_D50.0075_32x121.npz` | `I163-mac/acc/a_32x121_mutnorows_D50.0075_32x121.npz` |
   | 54.996085 | `I671-win/solves/k7_D55_D54.9961_32x121.npz` | `I671-win/solves/k0_D55_mutnorows_D54.9961_32x121.npz` |

   The rough starts are the successive draws of one generator (`default_rng(163)`, `rt_sigma.py`), so the first three starts of a 12-start run are the three starts of #643 and #671; the other nine are new.
3. **The statistic, fixed here before the runs.** The bound of a run is the **median of its 12 rough bounds**, taken as the geometric mean of the 6th and 7th smallest. The best (smallest) is context, with the quartiles (Q1 = geometric mean of the 3rd and 4th smallest, Q3 = of the 9th and 10th) and the maximum; all 12 are in the table. R(D) = median(K = 7) / median(K = 0) at the same D.
4. **The window, fixed here before the runs.** The K = 7 bounds **follow the K = 0 trend** if R(40.020065) / R(50.007491) and R(54.996085) / R(50.007491) both lie in [1/3, 3], a factor 3. The noise of these ratios is estimated by a bootstrap: each state's 12 bounds are resampled with replacement (10000 times, fixed seed 681), medians and ratios recomputed, and the 2.5 and 97.5 percentiles are the 95% interval. The verdict is **FOLLOWS** if both point ratios and both intervals lie inside the window; **DOES NOT FOLLOW** if at least one point ratio lies outside and its own interval lies entirely outside; **UNDECIDED** otherwise (the sample cannot separate), with the intervals reported. The factor 3 is kept from #671 because with 12 starts the median's noise is smaller than the best-of-3's, which the bootstrap measures rather than assumes.
5. **Context, not criteria**: the best and the quartiles of each run; the class of the best start's x and the fraction of the 12 starts whose own x falls in each class (#423's rules, applied per start: *edge* if E >= 0.5 and E >= 3 C0, *centre in omega_4* if C4 >= 0.5 and C4 >= 3 E, else *mixed*); the number of starts that hit the 250-product cap and the solve residuals; and which root each state is (Delta_RT - Delta_hp from the solve's record).
6. **Controls beyond the planted check**: (a) the first three starts of each run must reproduce the per-start bounds of #643 / #671 (same draws, same state, same code) to within a factor 1.25, or the difference is reported; (b) the best of the first three starts must equal the best-of-3 of #671 / #643 (table of #671, 1.257e-34, 1.669e-34, 4.882e-34, 1.184e-34, 1.754e-34, 3.664e-35).
7. **A run that has not finished after 6 h** is reported with the starts it has printed; nothing is cut short before that.

## Summary

The planted check passes (exit 0, best bound 1.41e-21) and its `--mutate=shift` control fails (exit 1, 1.42e-19). All six runs finished with exit 0 and 12 starts each (72 starts); the first three starts of every run reproduce the per-start bounds of #643 and #671 to the printed digits (ratios 1.000).

**By the rule fixed before the runs the verdict is UNDECIDED.** The median of the 12 is the bound; R(D) = median(K = 7) / median(K = 0):

| D | K = 7 median | K = 0 control median | R(D) | R(D) / R(50.007) | 95% bootstrap interval | point inside [1/3, 3]? | interval |
|---|---|---|---|---|---|---|---|
| 40.020065 | 2.403e-34 | 2.463e-34 | 0.98 | **0.17** | 0.06 to 0.91 | **no** | straddles the lower edge |
| 50.007491 | 1.293e-33 | 2.199e-34 | 5.88 | 1 | | (reference) | |
| 54.996085 | 2.122e-34 | 2.983e-35 | 7.12 | 1.21 | 0.54 to 5.00 | yes | straddles the upper edge |

The point ratio at D 40.02 is outside the window and the other is inside, but neither interval lies on one side of an edge, so the rule gives neither FOLLOWS nor DOES NOT FOLLOW. The bootstrap half-width is about a factor of 4 on a ratio of four medians of 12; to bring the D 40.02 interval's upper end from 0.91 to 1/3 at the same point value (0.17) would take roughly 75 starts per state (the log half-width falls as 1/sqrt(n)), about six times this task.

**Context, as asked (the best of 12, not the statistic):** the best bounds are 1.26e-34 and 9.14e-35 at D 40.02, 3.82e-34 and 1.18e-34 at D 50.007, 7.97e-35 and 1.33e-35 at D 54.996 (K = 7 and K = 0), so R_best = 1.38, 3.22 and 5.98 and the ratios to R_best(50.007) are 0.43 and 1.86, both inside the window. Each rough bound is an upper bound on the smallest gain, so the best is the tightest bound and the median the typical one; the two statistics disagree about the window at D 40.02 (0.43 against 0.17) and agree at D 54.996.

What the 12 starts settle beyond the verdict:

- **D 40.02: the rows change nothing measurable.** The two medians agree (2.403e-34 and 2.463e-34, R = 0.98), the two roots coincide (Delta differs by 6.8e-18), the sorted bounds interleave, and in all 24 starts x is "mixed" (none centre in omega_4, none edge). At D 50.007 and 54.996 the K = 7 medians are 5.9 and 7.1 times the K = 0 ones.
- **The class moves with the rows at D 50.007 only.** Of the 12 starts' own x, "centre in omega_4" is 11 of 12 with the rows against 2 of 12 without at D 50.007; 12 of 12 for both at D 54.996; 0 of 12 for both at D 40.02.
- **R tracks how far the K = 7 root is from its control.** Delta(K = 7) - Delta(K = 0) is 6.8e-18 at D 40.02 (R = 0.98), 1.04e-12 at D 50.007 (R = 5.88) and 1.69e-10 at D 54.996 (R = 7.12). Three points and one start each, so a coincidence of the ordering cannot be excluded; it is an observation, not a result.
- **The spread of the starts is large everywhere** (max / min of the 12: 14.4 and 15.5 at D 40.02, 9.1 and 6.7 at D 50.007, 5.1 and 12.3 at D 54.996), which is what made the best-of-3 unstable in #671.

## Which root each run used

The runs read the states of #671 and #643; their Delta_RT - Delta_hp come from the solve records (`I671-win/solves/*.jsonl`, `I163-mac/acc/a_32x121*.jsonl`):

| run | state | Delta_RT - Delta_hp |
|---|---|---|
| K7_D40 | `I671-win/solves/k7_D40_D40.0201_32x121.npz` | +1.552e-15 |
| K0_D40 | `.../k0_D40_mutnorows_D40.0201_32x121.npz` | +1.545e-15 |
| K7_D50 | `I163-mac/acc/a_32x121_D50.0075_32x121.npz` | -1.855e-12 |
| K0_D50 | `.../a_32x121_mutnorows_D50.0075_32x121.npz` | -2.894e-12 (the same root as #145's `fol` 32x121 root, -2.9e-12) |
| K7_D55 | `I671-win/solves/k7_D55_D54.9961_32x121.npz` | **-3.840e-10** |
| K0_D55 | `.../k0_D55_mutnorows_D54.9961_32x121.npz` | **-5.529e-10** |

At D 54.996 neither is #145's root (+8.5e-12 from the 141 start) or its 101b root (+9.6e-13, `I145-mac/fol/from101b_32x121.jsonl`): four distinct roots of the same 32x121 grid are on record there (+8.5e-12, +9.6e-13, -3.84e-10, -5.53e-10). The K = 7 and K = 0 runs of D 54.996 therefore measure two different roots, both different from #423's.

## What ran

`run_681.py` (logs/run_681.log), BelowNormal, `rt_sigma.py STATE --starts 12 --rough`, venv-t151 through `rt_launch.py`, worktree `choptuik-i423` at main 5135cdeb, two BLAS threads, three runs at a time (K = 7 first):

| run | start (UTC) | end | wall |
|---|---|---|---|
| K7_D40 | 11:37:07 | 15:24:20 | 13633 s |
| K7_D50 | 11:37:07 | 14:40:56 | 11029 s |
| K7_D55 | 11:37:07 | 15:01:23 | 12256 s |
| K0_D50 | 15:01:23 | 15:54:48 | 3205 s |
| K0_D40 | 14:40:56 | 15:26:41 | 2745 s |
| K0_D55 | 15:24:20 | 16:21:01 | 3401 s |

(Each K = 0 run started when a K = 7 run freed a slot; `logs/run_681.log` has the lines.) No run exceeded the 6 h limit. Free memory was 15.2 GB at the 12:41 check.

## Results (`table_681.txt`)

| D | K | n starts | best | Q1 | **median (the bound)** | Q3 | max | max/min | starts at the 250 cap | worst residual | classes of the starts (edge / centre in w4 / mixed) | best start's class |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 40.020065 | K7 | 12 | 1.26e-34 | 1.42e-34 | **2.403e-34** | 6.17e-34 | 1.81e-33 | 14.4 | 12 of 12 | 4.3e-14 | 0 / 0 / 12 (of 12) | mixed |
| 40.020065 | K0 | 12 | 9.14e-35 | 1.50e-34 | **2.463e-34** | 6.51e-34 | 1.42e-33 | 15.5 | 0 of 12 | 2.5e-18 | 0 / 0 / 12 (of 12) | mixed |
| 50.007491 | K7 | 12 | 3.82e-34 | 5.08e-34 | **1.293e-33** | 1.79e-33 | 3.47e-33 | 9.1 | 5 of 12 | 5.6e-14 | 0 / 11 / 1 (of 12) | centre in w4 |
| 50.007491 | K0 | 12 | 1.18e-34 | 1.74e-34 | **2.199e-34** | 4.45e-34 | 7.98e-34 | 6.7 | 0 of 12 | 3.6e-19 | 0 / 2 / 10 (of 12) | mixed |
| 54.996085 | K7 | 12 | 7.97e-35 | 1.66e-34 | **2.122e-34** | 2.55e-34 | 4.10e-34 | 5.1 | 9 of 12 | 2.7e-13 | 0 / 12 / 0 (of 12) | centre in w4 |
| 54.996085 | K0 | 12 | 1.33e-35 | 1.77e-35 | **2.983e-35** | 5.49e-35 | 1.64e-34 | 12.3 | 0 of 12 | 3.9e-15 | 0 / 12 / 0 (of 12) | centre in w4 |

All bounds, sorted (per run):
  K7 D 40.020065: 1.26e-34, 1.26e-34, 1.30e-34, 1.56e-34, 1.61e-34, 2.19e-34, 2.64e-34, 3.67e-34, 4.88e-34, 7.80e-34, 9.92e-34, 1.81e-33
  K0 D 40.020065: 9.14e-35, 9.89e-35, 1.35e-34, 1.67e-34, 1.88e-34, 2.35e-34, 2.58e-34, 2.87e-34, 4.96e-34, 8.55e-34, 1.27e-33, 1.42e-33
  K7 D 50.007491: 3.82e-34, 4.34e-34, 4.88e-34, 5.28e-34, 5.60e-34, 1.27e-33, 1.32e-33, 1.35e-33, 1.51e-33, 2.12e-33, 2.94e-33, 3.47e-33
  K0 D 50.007491: 1.18e-34, 1.48e-34, 1.72e-34, 1.76e-34, 1.87e-34, 1.87e-34, 2.58e-34, 3.00e-34, 3.18e-34, 6.23e-34, 6.31e-34, 7.98e-34
  K7 D 54.996085: 7.97e-35, 1.52e-34, 1.57e-34, 1.75e-34, 1.85e-34, 2.10e-34, 2.14e-34, 2.16e-34, 2.42e-34, 2.69e-34, 3.36e-34, 4.10e-34
  K0 D 54.996085: 1.33e-35, 1.72e-35, 1.73e-35, 1.82e-35, 2.18e-35, 2.43e-35, 3.66e-35, 4.33e-35, 5.18e-35, 5.82e-35, 1.24e-34, 1.64e-34

R(D) = median(K = 7) / median(K = 0), and from the best:
  D 40.020065: median 2.403e-34 / 2.463e-34 = 0.98; best 1.257e-34 / 9.136e-35 = 1.38
  D 50.007491: median 1.293e-33 / 2.199e-34 = 5.88; best 3.816e-34 / 1.184e-34 = 3.22
  D 54.996085: median 2.122e-34 / 2.983e-35 = 7.12; best 7.966e-35 / 1.331e-35 = 5.98

The window of 3 on R(D)/R(50.007491), with the bootstrap 95% intervals:
  R(40.020065) / R(50.007491) = 0.17, interval 0.06 to 0.91: point OUTSIDE, interval straddles an edge
  R(54.996085) / R(50.007491) = 1.21, interval 0.54 to 5.00: point inside, interval straddles an edge
  VERDICT (rule of README.md): the K = 7 bounds UNDECIDED the K = 0 trend within a factor 3
  (best-of-12 ratios, context: R_best(40.020065) / R_best(50.007491) = 0.43, R_best(54.996085) / R_best(50.007491) = 1.86)

Control (a): the first three starts against the earlier 3-start runs (same draws, same state; within a factor 1.25):
  K7 D 40.020065: new 1.257e-34, 9.921e-34, 7.797e-34 / earlier 1.257e-34, 9.921e-34, 7.797e-34 = 1.000, 1.000, 1.000 -> reproduces; best of the first three 1.257e-34 against the earlier best-of-3 1.257e-34
  K0 D 40.020065: new 1.669e-34, 1.419e-33, 1.879e-34 / earlier 1.669e-34, 1.419e-33, 1.879e-34 = 1.000, 1.000, 1.000 -> reproduces; best of the first three 1.669e-34 against the earlier best-of-3 1.669e-34
  K7 D 50.007491: new 4.882e-34, 3.472e-33, 1.348e-33 / earlier 4.882e-34, 3.472e-33, 1.348e-33 = 1.000, 1.000, 1.000 -> reproduces; best of the first three 4.882e-34 against the earlier best-of-3 4.882e-34
  K0 D 50.007491: new 1.184e-34, 2.584e-34, 1.760e-34 / earlier 1.184e-34, 2.584e-34, 1.760e-34 = 1.000, 1.000, 1.000 -> reproduces; best of the first three 1.184e-34 against the earlier best-of-3 1.184e-34
  K7 D 54.996085: new 1.754e-34, 4.096e-34, 3.361e-34 / earlier 1.754e-34, 4.096e-34, 3.361e-34 = 1.000, 1.000, 1.000 -> reproduces; best of the first three 1.754e-34 against the earlier best-of-3 1.754e-34
  K0 D 54.996085: new 3.664e-35, 1.236e-34, 5.819e-35 / earlier 3.664e-35, 1.236e-34, 5.819e-35 = 1.000, 1.000, 1.000 -> reproduces; best of the first three 3.664e-35 against the earlier best-of-3 3.664e-35

The K = 7 starts hit the 250-product cap on 12 of 12 (D 40.02), 5 of 12 (D 50.007) and 9 of 12 (D 54.996) starts, the K = 0 starts on none, with worst residuals max|J x - v| of 4.3e-14, 5.6e-14 and 2.7e-13 for K = 7 and 2.5e-18, 3.6e-19 and 3.9e-15 for K = 0; a bound 1 / max|x| holds to a relative accuracy of that size, which is far below the spreads above. The classes counted per start use #423's rules.

## Controls

- **The planted check and its mutation**, above.
- **Control (a)**, the reproduction of #643 and #671: the first three starts of all six runs reproduce the earlier per-start bounds with ratios 1.000 (same generator, state and code; deterministic), and the best of the first three equals the earlier best-of-3 in all six.
- **The verdict code can fail**: `table_681.py --selftest` plants samples with a known ratio and gets FOLLOWS (same R at every D, narrow starts), DOES NOT FOLLOW (R(40) a factor 10 low, narrow starts) and UNDECIDED (R(40) a factor 4 low, starts spread by a factor of about 20), as expected.
- **Not run:** a second implementation of the bound, an SVD of J, other starts of the K = 7 roots (b), more than 12 starts, and the factor chosen after seeing the data.

## Discrepancies

None with #671 or #643 beyond the verdict itself: #671's best-of-3 said "does not follow", the median of 3 said "follows", and the median of 12 says "undecided" with the point estimate on the "does not follow" side at D 40.02 and the best-of-12 on the "follows" side. The statistic and the sample size, not the roots, are what these results disagree about.

## Recommended tasks (for the coordinator)

1. **Test whether R depends on the root rather than on D.** What: a K = 7 root and its K = 0 control at D 40.02 from start b, #145's 32x141 root (`I145-mac/fol/fol_32x141_D40.0201_32x141.npz`, resampled exactly, #163's options), and 12 rough starts each, the way `I671-win/run_671_solves.py` and #681 did. Why: at D 40.02 the K = 7 and K = 0 roots from start a coincide (Delta within 7e-18) and R = 0.98, while at D 50.007 and 54.996 they differ (1e-12 and 1.7e-10) and R is 6 to 7; a start-b pair at D 40.02 whose two roots differ would separate "the rows matter when the roots differ" from "the rows matter at D >= 50". Acceptance: Delta(K = 7) - Delta(K = 0) and R from the medians of 12, with the planted check repeated; the prediction (R about 6 if the roots differ, about 1 if they coincide) written before the runs. Depends on #681. About 5 h.
