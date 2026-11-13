# I671-win: RT's weak direction with the K = 7 rows at D 40.02 and 54.996 (rt_sigma.py, rough and smooth starts)

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/671 (the coordinator's message `1794562038665-0` on the `choptuik-large-d` channel; follows #643, raw `I643-win/` at 2927452a, #423, `I423-win/`, and #163, `I163-mac/`). Worktree `choptuik-i423` (main 5135cdeb, `solver/rt`), venv-t151 (Python 3.10, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0) through `rt_launch.py` and `resource.py` (copied from `I423-win/`; no repository file changes). BelowNormal. BLAS threads: one for any matrix above 3 GiB (AGENTS.md, OpenBLAS pitfall; none of these is: 32x121 has L = 13665, 1.4 GiB), so the solves use one thread each (four at once) and the sigma runs two.

## Plan, written before the runs (the issue's acceptance)

1. **Checks first**: `rt_sigma.py --planted` must exit 0 and `--planted --mutate=shift` must exit 1 (`logs/planted.log`, `logs/planted_mutate_shift.log`).
2. **Four solves**, as #163's `run_one.sh` and `acc` queue did for D 50 (start a): from #145's 32x101 continuation states read in place from the raw repository's origin/main checkout, `I145-mac/cont/cont_32x101_D40.0201_32x101.npz` (D 40.020065) and `cont_32x101_D54.9961_32x101.npz` (D 54.996085), resampled exactly in xi (`--resample_mp`) to 32x121 and solved at their own D with `rt_run.py --solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4 --newton_tol NTOL` (NTOL 1e-40 at D 40.02, 1e-38 at D 54.996, #163's rule), once with `--horizon 7` (the K = 7 root) and once with `--horizon 7 --mutate=norows` (the same start and code with the rows dropped, K = 0: the control). A solve that does not end `ok` with max|F| <= 1e-36 is reported and its states are not measured.
3. **Eight sigma runs**: `rt_sigma.py STATE --starts 3` rough and smooth on each of the four states. D 50.007491 (start a) comes from #643 (`I643-win`): K = 7 rough 4.882e-34, smooth 2.698e-33; K = 0 control rough 1.184e-34, smooth 2.380e-19.
4. **Classification, #423's rules unchanged** (`I423-win/README.md`): the best bound of 3 starts; x's class (*edge* if E >= 0.5 and E >= 3 C0, *centre in omega_4* if C4 >= 0.5 and C4 >= 3 E, else *mixed*); *seen by smooth* if the smooth bound is within 100 of the rough one. The D trend of the K = 7 series is now **measured** from its own rough bounds at D 40.020065, 50.007491 and 54.996085 (start a, 32x121): decades per 10 in D between neighbours (the last step scaled to 10 in D), *horizon-like* if it falls by more than 3, *not horizon-like* within 1 either way, *in between* otherwise; a D's verdict uses the step that ends at it (D 40.02 uses the step from 40.02 to 50.007). Verdict per D: (H) = edge + seen only by rough + horizon-like; (C) = centre in omega_4 + seen by smooth + not horizon-like; **neither** otherwise, with the parts named.
5. **The factor, fixed here before any measurement.** Let R(D) = (rough bound of the K = 7 state) / (rough bound of its same-start K = 0 control), best of 3 starts each. R(50.007) = 4.12 (#643, start a; start b gave 7.82). **The K = 7 bounds follow the K = 0 trend within a factor 3 if R(40.020065) and R(54.996085) each lie within a factor 3 of R(50.007)**, that is between 1.37 and 12.4; otherwise they do not, and the verdict names which D and by how much. Factor 3 is chosen to exceed the start-to-start spread of R at D 50 (a factor 1.9) and to be small against the smooth/rough ratios that distinguish the cases (10^15 without rows, 4 to 8 with them). The same ratio against #423's K = 0 bounds (5.227e-34 at D 40.02, 2.559e-35 at D 54.996, the `fol` roots) is reported as a check on the controls, not as a criterion.
6. **Reproduction control**: the K = 0 controls here and #423's `fol` roots are different roots from the same family and the same start, so their rough bounds should agree within a factor 3 (at D 50: 1.184e-34 against 1.404e-34); a control outside that is reported.

## Amendment, 2026-11-13 10:01 UTC, before any sigma run of this task had printed a bound

Plan item 2 required each solve to end `ok` with max|F| <= 1e-36. The four solves ended: K = 7 at D 40.02 with max|F| **1.19e-36** (`ok` true; 5 steps, 1632 s), its K = 0 control 2.2e-40, K = 7 at D 54.996 1.3e-44, its control 3.1e-39. The K = 7 solve at D 40.02 misses the stated number by 19%. I measure it anyway, as a deviation I make after seeing this solve's F and before any sigma result: the 1e-36 was my own choice, meant to separate a converged solve from a cycling one, the solve's own record is `ok` (a stall within 1e6 times `newton_tol` 1e-40, #145's accepted stall, with `--patient`), and the state is stored in double-double, so `rt_sigma.py` evaluates it at about 1e-29 whatever its arb value (the K = 7 start a at D 50 reads 4.98e-29). It is flagged in the table and the summary.

## Summary

The planted check passes (exit 0) and its `--mutate=shift` control fails (exit 1). The four solves converged (one with a deviation from the plan, above) and all eight sigma runs finished with exit 0.

**By the factor fixed before the runs, the K = 7 bounds do not follow the K = 0 trend within a factor 3.** R(D), the rough K = 7 bound over the rough bound of its same-start K = 0 control:

| D | K = 7 rough bound | K = 0 control rough bound | R(D) | R(D) / R(50.007) | within a factor 3? |
|---|---|---|---|---|---|
| 40.020065 | 1.257e-34 | 1.669e-34 | **0.75** | **0.18** | **no** |
| 50.007491 (#643) | 4.882e-34 | 1.184e-34 | 4.12 | 1 | (reference) |
| 54.996085 | 1.754e-34 | 3.664e-35 | 4.79 | 1.16 | yes |

The miss is at D 40.02 alone, and it rests on one start. The three rough starts of the K = 7 run at D 40.02 give 1.26e-34, 7.80e-34 and 9.92e-34 (all three at the 250-product cap), a spread of 7.9, and the K = 0 control's give 1.67e-34, 1.88e-34 and 1.42e-33 (spread 8.5), so the best-of-3 statistic of the plan moves by a factor of several between draws, more than the factor 3 of the window (the 1.9 I chose the 3 from was the ratio between the R of #643's two starts a and b at D 50; the spread between the three starts inside one run there was 2.2 for the K = 0 control and 7.1 for the K = 7 run). **Post-hoc, added after the result above was seen and not the criterion**: with the median of the three starts instead of the best, R is 4.15, 7.66 and 5.78 at D 40.02, 50.007 and 54.996, and the ratios to R(50.007) are 0.54 and 0.75, within a factor 3 at both. So the pre-registered verdict is "does not follow", and a statistic less sensitive to a single draw would say "follows"; the data do not decide this at a factor of 3.

What does not depend on the choice of statistic: **smooth starts reach the weak direction with the rows at every D and never without them.** Smooth bound over rough bound: 3.34, 5.53 and 5.03 at D 40.02, 50.007 and 54.996 with the rows (K = 7), and 2.98e15, 2.01e15 and 1.53e15 without them (K = 0).

Classes and verdicts by #423's rules, with the D trend now measured from each series' own rough bounds (decades per 10 in D, D 40.02 to 50.007 and 50.007 to 54.996):

| series | D | x (rough start) | seen by smooth | trend ending at D | verdict |
|---|---|---|---|---|---|
| K = 7 | 40.020 | mixed (C4 1.00, E 0.70, mu 0.14) | yes (3.3) | +0.59, not horizon-like | **neither** |
| K = 7 | 50.007 | centre in omega_4 (E 0.30, mu 0.14) | yes (5.5) | +0.59, not horizon-like | **(C)** |
| K = 7 | 54.996 | centre in omega_4 (E 0.10, mu 0.01) | yes (5.0) | -0.89, not horizon-like | **(C)** |
| K = 0 control | 40.020 | mixed (mu 1.00) | no (3.0e15) | -0.15, not horizon-like | neither |
| K = 0 control | 50.007 | mixed (E 0.40, mu 0.34) | no (2.0e15) | -0.15, not horizon-like | neither |
| K = 0 control | 54.996 | centre in omega_4 (E 0.10, mu 0.03) | no (1.5e15) | -1.02, in between | neither |

So the K = 7 roots are (C) at two of the three D and "neither" at D 40.02, where the best start's x has an edge content of 0.70 against 1.00 in omega_4 near xi = 0 (the 3E rule makes it mixed); the K = 0 controls are "neither" at all three, because smooth starts do not see the direction. The K = 7 bound is not monotone in D (it rises by a factor 3.9 from D 40.02 to 50.007 and falls by a factor 2.8 to 54.996) while the K = 0 controls fall (0.71 and 0.31), but the rise is within the start-to-start spread. Neither series' trend is horizon-like by the plan's threshold of 3 decades per 10 in D.

## What ran

Checks: `logs/planted.log` (`rt_sigma.py --planted`: best bound 1.41e-21, exit 0) and `logs/planted_mutate_shift.log` (`--mutate=shift`: 1.42e-19, FAIL, exit 1).

**The four solves** (`run_671_solves.py`, `solves/`, `logs/k7_D40.log` etc.), `rt_run.py --solver mp` (192 bits) from #145's 32x101 states resampled exactly to 32x121, #163's options, one BLAS thread each, the four at once (09:28:56 to 10:00:09 UTC):

| state | start | newton max|F| at the end | Newton steps | seconds | Delta_RT - Delta_hp | note |
|---|---|---|---|---|---|---|
| K = 7, D 40.020065 | `cont_32x101_D40.0201` | **1.19e-36** | 5 | 1629 | +1.552e-15 | 19% above the plan's 1e-36 (amendment in the README), `ok` true |
| K = 0 control, D 40.020065 | same | 2.2e-40 | 4 | 1099 | +1.545e-15 | |
| K = 7, D 54.996085 | `cont_32x101_D54.9961` | 1.3e-44 | 5 | 1866 | -3.840e-10 | |
| K = 0 control, D 54.996085 | same | 3.1e-39 | 3 | 1003 | -5.529e-10 | |

At D 54.996 both states are roots 3.8e-10 and 5.5e-10 below hp's row on 32x121, not the +8.5e-12 of #145's `fol` 32x121 root at that D (the same grid has several nearly degenerate roots, #404); at D 40.02 all four agree with hp to 1.55e-15, the plateau of #404 and #610. rt_run.py exits 1 when |Delta_RT - Delta_hp| > 1e-12, which it did for both D 54.996 solves.

**The eight sigma runs** (`run_423.py` copied from `I423-win/`, log `logs/run_423.log`), BelowNormal, 3 starts each, two BLAS threads, three at a time (10:01:33 to 11:29:02 UTC); D 50.007 comes from `I643-win`. Peak resident memory of the solves 1.7 to 1.8 GB; 17.5 GB free at 11:18.

## Results (`table_671.txt`)

| D | K | kind | bound (best of 3) | starts' spread | worst residual | products | mu | E | C0 | C4 | class |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 40.020065 | K7 (K 7) | rough | 1.257e-34 | 7.9 | 1.6e-15 | 250 | 0.14 | 0.70 | 1.00 | 1.00 | mixed |
| 40.020065 | K7 (K 7) | smooth | 4.196e-34 | 4.8 | 3.8e-17 | 250 | 0.14 | 0.70 | 1.00 | 1.00 | mixed |
| 40.020065 | K0 (K 0) | rough | 1.669e-34 | 8.5 | 1.2e-18 | 67 | 1.00 | 0.96 | 0.96 | 0.96 | mixed |
| 40.020065 | K0 (K 0) | smooth | 4.974e-19 | 8.7 | 2.7e-34 | 67 | 1.00 | 1.11 | 0.89 | 0.89 | mixed |
| 50.007491 | K7 (K 7) | rough | 4.882e-34 | 7.1 | 4.9e-15 | 250 | 0.14 | 0.30 | 1.00 | 1.00 | centre in w4 |
| 50.007491 | K7 (K 7) | smooth | 2.698e-33 | 2.1 | 7.2e-17 | 175 | 0.16 | 0.30 | 1.00 | 1.00 | centre in w4 |
| 50.007491 | K0 (K 0) | rough | 1.184e-34 | 2.2 | 9.6e-20 | 76 | 0.34 | 0.40 | 1.00 | 1.00 | mixed |
| 50.007491 | K0 (K 0) | smooth | 2.380e-19 | 7.9 | 4.5e-31 | 76 | 0.33 | 0.40 | 1.00 | 1.00 | mixed |
| 54.996085 | K7 (K 7) | rough | 1.754e-34 | 2.3 | 9.0e-15 | 250 | 0.01 | 0.10 | 1.00 | 1.00 | centre in w4 |
| 54.996085 | K7 (K 7) | smooth | 8.831e-34 | 2.2 | 5.2e-17 | 162 | 0.03 | 0.09 | 1.00 | 1.00 | centre in w4 |
| 54.996085 | K0 (K 0) | rough | 3.664e-35 | 3.4 | 3.8e-15 | 88 | 0.03 | 0.10 | 1.00 | 1.00 | centre in w4 |
| 54.996085 | K0 (K 0) | smooth | 5.594e-20 | 17.9 | 1.0e-31 | 82 | 0.01 | 0.10 | 1.00 | 1.00 | centre in w4 |

R(D) = rough K = 7 bound / rough K = 0 control bound:
  D 40.020065: 1.257e-34 / 1.669e-34 = 0.75
  D 50.007491: 4.882e-34 / 1.184e-34 = 4.12
  D 54.996085: 1.754e-34 / 3.664e-35 = 4.79
  R(40.020065) / R(50.007491) = 0.18 -> OUTSIDE a factor 3
  R(54.996085) / R(50.007491) = 1.16 -> within a factor 3
  VERDICT on the trend: the K = 7 bounds DO NOT FOLLOW the K = 0 trend within a factor 3

D trend of the rough bounds (decades per 10 in D):
  K7: D 40.020065 -> 50.007491: 1.257e-34 -> 4.882e-34, +0.59 decades per 10 in D, not horizon-like
  K7: D 50.007491 -> 54.996085: 4.882e-34 -> 1.754e-34, -0.89 decades per 10 in D, not horizon-like
  K0: D 40.020065 -> 50.007491: 1.669e-34 -> 1.184e-34, -0.15 decades per 10 in D, not horizon-like
  K0: D 50.007491 -> 54.996085: 1.184e-34 -> 3.664e-35, -1.02 decades per 10 in D, in between
  (#423's K = 0 `fol` roots: 5.227e-34, 1.404e-34, 2.559e-35 = -0.57 and -1.48 decades per 10 in D)

Verdict per D by #423's rules with the measured trend of the same series:
  K7 D 40.020065: x mixed; smooth/rough 3.34e+00 (seen); trend not horizon-like (+0.59) -> neither
  K7 D 50.007491: x centre in w4; smooth/rough 5.53e+00 (seen); trend not horizon-like (+0.59) -> (C)
  K7 D 54.996085: x centre in w4; smooth/rough 5.03e+00 (seen); trend not horizon-like (-0.89) -> (C)
  K0 D 40.020065: x mixed; smooth/rough 2.98e+15 (not seen); trend not horizon-like (-0.15) -> neither
  K0 D 50.007491: x mixed; smooth/rough 2.01e+15 (not seen); trend not horizon-like (-0.15) -> neither
  K0 D 54.996085: x centre in w4; smooth/rough 1.53e+15 (not seen); trend in between (-1.02) -> neither

POST-HOC sensitivity, not the criterion: R from the median of the three rough starts instead of the best (the best-of-3 has a start-to-start spread of up to a factor 8):
  D 40.020065: K = 7 starts 1.26e-34, 7.80e-34, 9.92e-34 (median 7.80e-34); K = 0 starts 1.67e-34, 1.88e-34, 1.42e-33 (median 1.88e-34); R_median = 4.15
  D 50.007491: K = 7 starts 4.88e-34, 1.35e-33, 3.47e-33 (median 1.35e-33); K = 0 starts 1.18e-34, 1.76e-34, 2.58e-34 (median 1.76e-34); R_median = 7.66
  D 54.996085: K = 7 starts 1.75e-34, 3.36e-34, 4.10e-34 (median 3.36e-34); K = 0 starts 3.66e-35, 5.82e-35, 1.24e-34 (median 5.82e-35); R_median = 5.78
  R_median(40.020065) / R_median(50.007491) = 0.54 -> within a factor 3
  R_median(54.996085) / R_median(50.007491) = 0.75 -> within a factor 3

The K = 0 controls against #423's `fol` roots (rough bound; within a factor 3 expected):
  D 40.020065: 1.669e-34 against 5.227e-34: factor 0.32 -> OUTSIDE 3
  D 50.007491: 1.184e-34 against 1.404e-34: factor 0.84 -> within 3
  D 54.996085: 3.664e-35 against 2.559e-35: factor 1.43 -> within 3

The K = 7 rough starts hit the 250-product cap on 3 of 3 (D 40.02), 1 of 3 (D 50.007, from #643) and 1 of 3 (D 54.996) starts, with residuals max|J x - v| of 1.6e-15, 1.5e-15, 2.0e-16 (D 40.02) and 9.0e-15 (D 54.996); the bound 1 / max|x| holds to a relative accuracy of that size (the K = 0 runs end at 1e-18 or below, except the D 54.996 control at 3.8e-15, 88 products).

## Controls

- **The planted check and its mutation**, above.
- **K = 0 controls against #423's roots** (the `fol` 32x121 roots, same family and grid): the rough bounds agree within a factor 3 at D 50.007 (0.84) and D 54.996 (1.43) and miss it at D 40.02 (factor 0.32, against a start spread of 8.5 in the control itself). The D 54.996 control is a different root (5.5e-10 below hp) from #423's (+8.5e-12) and its bound still agrees within 1.43.
- **Not run:** a second implementation of the bound, an SVD of J, start b at D 40.02 and 54.996 (only start a was used, as #643's D 50 reference for R), more than 3 starts per run, and K = 7 at other D.

## Discrepancies

None with #643 or #423 beyond the above. The pre-registered statistic (the best of three) is less stable than I assumed when I chose the factor of 3, which the post-hoc median shows; I report the pre-registered verdict as the verdict and the median as the reason it is fragile.

## Recommended tasks (for the coordinator)

1. **Decide the K = 7 trend with more starts.** What: `rt_sigma.py --starts 12` rough on the K = 7 and K = 0 states at D 40.02 (the two `solves/` states), and the same at D 50.007 (`I163-mac/acc/a_32x121...` and `a_32x121_mutnorows...`) and D 54.996, so that the best, the median and a spread are all stable; about 5 h at three jobs at a time and the two-thread rates above, 12 starts at up to 250 products each. Why: the pre-registered verdict ("does not follow") rests on the best of 3 starts at D 40.02 and flips with the median; a larger sample would settle whether R(D) is constant in D. Acceptance: R(D) from the best and from the median of 12 starts at each D, with the factor 3 applied to both, and the starts' spread reported; the planted check and its control repeated. Depends on #671.
