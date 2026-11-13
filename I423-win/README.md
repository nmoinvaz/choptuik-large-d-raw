# I423-win: the RT Jacobian's weakest directions against N, D and N_t (rt_sigma.py)

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/423 (the coordinator's message `1794543104322-0` on the `choptuik-large-d` channel and the commands in the issue's latest comment; follows #163, raw `I163-mac/`). Worktree `choptuik-i423` at main 5135cdeb (`solver/rt/rt_sigma.py`), venv-t151 (Python 3.10, numpy 2.2.6, python-flint 0.9.0, multidouble 0.1.0). Pure Python; `rt_launch.py` and `resource.py` of `I404-win/` supply the two names this interpreter lacks (`multidouble._dd_dot`, `math.fma`) without changing any file of the repository.

## Prediction, written before any run (the coordinator's, verbatim)

- (H) A copy of lambda_4's horizon branch: x concentrates at xi = +-1, the bound is seen with `--rough` starts more than with smooth ones, and it falls with D like the horizon exponent.
- (C) A centre direction: x concentrates in omega_4 near xi = 0, it is seen with smooth starts as well, and the bound does not follow the horizon exponent.

#163's measured bounds (9e-35 to 2e-33, omega_4 near xi = 0) favour (C). The runs decide.

## How the prediction is read, fixed here before the data

`rt_sigma.py` prints, per start, max|x|, the bound 1 / max|x| on the smallest gain, the solve's residual max|J x - v|, and for x / max|x| the mu entry and per field w1..w4 the maximum, the first four harmonics, and the column maxima at xi = +1, near 0 (the middle column) and -1. For each run (a state, a start kind) I take the best bound over its starts (the smallest) and the content of that start's x. Let F = the largest field entry of x/max|x| (over w1..w4), P_f, C_f, M_f the column maxima of field f at xi = +1, near 0, -1, relative to F. Then:

1. **Where x sits.** *Edge* when max_f max(P_f, M_f) >= 0.5 and exceeds 3 times max_f C_f. *Centre in omega_4* when C_w4 >= 0.5 and exceeds 3 times max_f max(P_f, M_f). *Mixed* otherwise. |mu| / max|x| is reported beside it.
2. **Smooth against rough.** *Seen by smooth* when the best smooth bound is within a factor 100 of the best rough bound on the same state; *seen only by rough* when the smooth bound is more than 100 times the rough one. (#163: 4.5e-18 against 1.5e-33 at D 50 on 32x101, a factor 3e15.)
3. **The D trend**, on the same grid width and N_t, from the rough bound: *horizon-like* when the bound falls by more than a factor 1000 from one of D 30, 40, 50 to the next (#163 estimated about six decades from D 40 to 50 at N 101 for a polynomial copy of lambda_4's branch, notes/RT_FORMULATION.md section 13); *not horizon-like* when it stays within a factor 10 either way; *in between* otherwise. The steps are D 30 to 40, 40 to 50 and 50 to 54.996085 on 32x121 (the one grid width present at all four D); for the last step, whose D interval is 4.989, the decades are scaled to a step of 10 in D (decades per unit D times 10). A D's verdict uses the step that ends at it (D 30 uses the step from 30 to 40). (This sentence on the steps was added at 04:16 UTC, when the pilot had printed only its header lines and no bound.)
4. **Verdict per D**: (H) when 1 is edge, 2 is seen only by rough, and 3 is horizon-like; (C) when 1 is centre in omega_4, 2 is seen by smooth, and 3 is not horizon-like; **neither** in every other case, with the three results named. The table reports 1, 2 and 3 for every (D, grid) so a reader can recombine them. A bound is an upper bound on the smallest gain, not an SVD; a bound that two starts reproduce within a factor 2.2 is taken as near the smallest singular value.

## Checks, run first

- `python rt_launch.py rt_sigma.py --planted` must exit 0 and `--planted --mutate=shift` must exit 1; both logs are kept in `logs/`.
- The pilot is D 40.020065 on the 32x79 state (no 32x81 state of that D exists, see below), smooth then rough, 3 starts each. Its wall time is reported; if one run takes over 2 h I stop and post.

## The states (all read from the raw repository at origin/main; none is regenerated)

The coordinator's list is D about 30, 40, 50 and 55 on 32x81 and 32x121, D 40 on 32x141 and one N_t = 48 grid. The raw repository has no 32x81 state at D 40, 50 or 55, so the nearest grid that exists is used and named in the table (the substitution is mine, not the coordinator's):

| D | requested | state used |
|---|---|---|
| 30.0000 | 32x81 | `I105-mac/cont/cont_32x81_D30.0000_32x81.npz` |
| 30.0000 | 32x121 | `I145-mac/cont/cont_32x121_D30.0000_32x121.npz` |
| 40.020065 | 32x81 (pilot) | `I106-mac/res/Nt_32x79_D40.0201_D40.0201_32x79.npz` (32x79) |
| 40.020065 | 32x121 | `I145-mac/fol/fol_32x121_D40.0201_32x121.npz` |
| 40.020065 | 32x141 | `I145-mac/fol/fol_32x141_D40.0201_32x141.npz` |
| 40.020065 | N_t = 48 | `I145-mac/controls/nt_48x141_D40.0201_48x141.npz` (48x141) |
| 50.007491 | 32x81 | `I145-mac/cont/cont_32x101_D50.0075_32x101.npz` (32x101) |
| 50.007491 | 32x121 | `I145-mac/fol/fol_32x121_D50.0075_32x121.npz` |
| 54.996085 | 32x81 | `I164-mac/roots/a101_32x85_D54.9961_32x85.npz` (32x85) |
| 54.996085 | 32x121 | `I145-mac/fol/fol_32x121_D54.9961_32x121.npz` |

Ten states, each run smooth and rough (3 starts), so 20 runs, three at a time (2 BLAS threads each, 6 busy threads at most, BelowNormal) after the pilot.

## Summary

All 20 runs finished (exit 0), the planted check passes and its `--mutate=shift` control fails (exit 1). **By the rules fixed above the verdict is "neither" at every D** (30, 40.02, 50.007, 54.996, read on 32x121), and the three parts of the prediction come out as follows.

| part | (H) says | (C) says | measured |
|---|---|---|---|
| where x sits (rough start) | at xi = +-1 | in omega_4 near xi = 0 | omega_4 near 0 on 32x121 at D 50 and 55, on 32x141 and 48x141 at D 40, 32x101 at D 50 (C4 = 1.00, edge content 0.1 to 0.3, |mu| 0.01 to 0.13); a mixed direction dominated by mu (|mu| = 0.6 to 1.0) at D 30 (N 81, 121), D 40 (N 79, 121) and D 55 (N 85) |
| smooth starts | do not see it | see it too | **do not see it anywhere**: smooth bound / rough bound = 8.5e14 to 7.2e15 at all ten states |
| D trend (rough bound, 32x121) | falls by more than 3 decades per 10 in D | does not follow the horizon exponent | -2.41 (D 30 to 40), -0.57 (40 to 50), -1.48 (50 to 55) decades per 10 in D |

So the location and the D trend at D 50 agree with (C), the failure of smooth starts agrees with (H), and the edge content and the size of the trend agree with neither. The bounds are 1.35e-31 (D 30), 5.2e-34 (D 40.02), 1.4e-34 (D 50.007) and 2.6e-35 (D 54.996) on 32x121.

## What ran

`run_423.py` (logs/run_423.log), BelowNormal, venv-t151 (Python 3.10, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0), worktree `choptuik-i423` at main 5135cdeb through `rt_launch.py`, 3 starts per run, `rt_sigma.py`'s defaults (192 bits, 250 products). Pilot D 40.020065 on 32x79 (smooth 240 s, rough 245 s, together, 4 BLAS threads). The other 16 runs of 32-wide states took 250 s (32x81) to 1237 s (32x141) each at 2 BLAS threads, three at a time (04:19:40 to 05:33:08 UTC). The N_t = 48 state needed one BLAS thread (below) and took 2079 s (smooth) and 2074 s (rough), run together (05:55:12 to 06:29:56 UTC). The states are the raw repository's own (table in the plan); none was regenerated.

**The 48x141 state crashes with more than one BLAS thread.** Five attempts at 2 BLAS threads died after printing the header (exit 3221225477 = 0xC0000005, `failed_attempt1_48x141/`, `failed_attempt2_48x141/`, `failed_attempt3_48x141/`; the third with Python's fault handler, an access violation in a native thread with no Python frame, the fifth a stepwise diagnostic that stopped in the LU step after the Jacobian had been built, 4.24 GiB in 208 s). `lu_size_test.py` reproduces it on a random matrix with the call of `LUdd` (`scipy.linalg.lu_factor(A.T, overwrite_a=True)` then `lu_solve`) at 2 BLAS threads: n = 20000 (2.98 GiB) factors in 76 s and solves to 8.0e-11, n = 23857 (4.24 GiB, more than 2^32 bytes) factors in 120 s and `lu_solve` dies with the access violation (`logs/lu_size_20000.log`, `logs/lu_size_23857.log`). With `OPENBLAS_NUM_THREADS=1` the real runs complete. So the crash belongs to multithreaded OpenBLAS in this scipy build above 4 GiB; I did not look into OpenBLAS itself, and the one-thread runs are the evidence that nothing else in `rt_sigma.py` is wrong at that size.

## Results (`table_423.txt`)

| state | D | grid | kind | bound (best of starts) | starts' spread | worst residual | products | x: mu | E (edge) | C0 (centre) | C4 (w4 centre) | class |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cont_32x81_D30.0000_32x81.npz | 30.000000 | 32x81 | rough | 2.539e-26 | 3.9 | 2.8e-28 | 34 | 0.57 | 1.00 | 0.90 | 0.90 | mixed |
| cont_32x81_D30.0000_32x81.npz | 30.000000 | 32x81 | smooth | 6.445e-11 | 3.0 | 2.3e-31 | 33 | 1.00 | 0.99 | 0.86 | 0.86 | mixed |
| cont_32x121_D30.0000_32x121.npz | 30.000000 | 32x121 | rough | 1.348e-31 | 1.6 | 7.3e-23 | 54 | 1.00 | 1.05 | 0.79 | 0.79 | mixed |
| cont_32x121_D30.0000_32x121.npz | 30.000000 | 32x121 | smooth | 1.147e-16 | 6.4 | 1.4e-36 | 54 | 0.03 | 0.80 | 1.00 | 1.00 | mixed |
| Nt_32x79_D40.0201_D40.0201_32x79.npz | 40.020065 | 32x79 | rough | 9.365e-31 | 1.7 | 1.2e-24 | 44 | 1.00 | 1.04 | 0.83 | 0.83 | mixed |
| Nt_32x79_D40.0201_D40.0201_32x79.npz | 40.020065 | 32x79 | smooth | 2.565e-15 | 3.2 | 7.9e-34 | 43 | 1.00 | 0.93 | 0.70 | 0.70 | mixed |
| fol_32x121_D40.0201_32x121.npz | 40.020065 | 32x121 | rough | 5.227e-34 | 3.7 | 1.1e-18 | 67 | 1.00 | 1.08 | 0.81 | 0.81 | mixed |
| fol_32x121_D40.0201_32x121.npz | 40.020065 | 32x121 | smooth | 5.804e-19 | 18.5 | 2.3e-34 | 67 | 1.00 | 1.11 | 0.67 | 0.67 | mixed |
| fol_32x141_D40.0201_32x141.npz | 40.020065 | 32x141 | rough | 2.993e-34 | 2.2 | 5.3e-19 | 75 | 0.07 | 0.20 | 1.00 | 1.00 | centre in w4 |
| fol_32x141_D40.0201_32x141.npz | 40.020065 | 32x141 | smooth | 8.333e-19 | 3.4 | 3.3e-35 | 75 | 0.14 | 0.30 | 1.00 | 1.00 | centre in w4 |
| nt_48x141_D40.0201_48x141.npz | 40.020065 | 48x141 | rough | 5.779e-35 | 2.6 | 9.8e-20 | 85 | 0.02 | 0.20 | 1.00 | 1.00 | centre in w4 |
| nt_48x141_D40.0201_48x141.npz | 40.020065 | 48x141 | smooth | 1.277e-19 | 7.6 | 4.3e-35 | 85 | 0.01 | 0.20 | 1.00 | 1.00 | centre in w4 |
| cont_32x101_D50.0075_32x101.npz | 50.007491 | 32x101 | rough | 1.510e-33 | 1.5 | 4.0e-21 | 66 | 0.13 | 0.30 | 1.00 | 1.00 | centre in w4 |
| cont_32x101_D50.0075_32x101.npz | 50.007491 | 32x101 | smooth | 1.397e-18 | 4.4 | 3.9e-36 | 66 | 0.52 | 0.40 | 1.00 | 1.00 | mixed |
| fol_32x121_D50.0075_32x121.npz | 50.007491 | 32x121 | rough | 1.404e-34 | 3.8 | 1.0e-18 | 76 | 0.08 | 0.30 | 1.00 | 1.00 | centre in w4 |
| fol_32x121_D50.0075_32x121.npz | 50.007491 | 32x121 | smooth | 1.736e-19 | 13.7 | 1.5e-31 | 76 | 0.06 | 0.30 | 1.00 | 1.00 | centre in w4 |
| a101_32x85_D54.9961_32x85.npz | 54.996085 | 32x85 | rough | 1.758e-33 | 1.6 | 5.7e-21 | 59 | 1.00 | 0.94 | 0.94 | 0.94 | mixed |
| a101_32x85_D54.9961_32x85.npz | 54.996085 | 32x85 | smooth | 1.270e-17 | 4.5 | 1.3e-32 | 59 | 1.00 | 0.94 | 0.94 | 0.94 | mixed |
| fol_32x121_D54.9961_32x121.npz | 54.996085 | 32x121 | rough | 2.559e-35 | 1.0 | 8.0e-19 | 80 | 0.01 | 0.20 | 1.00 | 1.00 | centre in w4 |
| fol_32x121_D54.9961_32x121.npz | 54.996085 | 32x121 | smooth | 1.376e-19 | 9.3 | 2.8e-32 | 80 | 0.03 | 0.10 | 1.00 | 1.00 | centre in w4 |

| state | rough bound | smooth bound | smooth / rough | seen by smooth (<= 100) |
|---|---|---|---|---|
| cont_32x81_D30.0000_32x81.npz | 2.539e-26 | 6.445e-11 | 2.54e+15 | no |
| cont_32x121_D30.0000_32x121.npz | 1.348e-31 | 1.147e-16 | 8.51e+14 | no |
| Nt_32x79_D40.0201_D40.0201_32x79.npz | 9.365e-31 | 2.565e-15 | 2.74e+15 | no |
| fol_32x121_D40.0201_32x121.npz | 5.227e-34 | 5.804e-19 | 1.11e+15 | no |
| fol_32x141_D40.0201_32x141.npz | 2.993e-34 | 8.333e-19 | 2.78e+15 | no |
| nt_48x141_D40.0201_48x141.npz | 5.779e-35 | 1.277e-19 | 2.21e+15 | no |
| cont_32x101_D50.0075_32x101.npz | 1.510e-33 | 1.397e-18 | 9.25e+14 | no |
| fol_32x121_D50.0075_32x121.npz | 1.404e-34 | 1.736e-19 | 1.24e+15 | no |
| a101_32x85_D54.9961_32x85.npz | 1.758e-33 | 1.270e-17 | 7.22e+15 | no |
| fol_32x121_D54.9961_32x121.npz | 2.559e-35 | 1.376e-19 | 5.38e+15 | no |

D trend on 32x121 (rough bound):
  D 30.000000 -> 40.020065: bound 1.348e-31 -> 5.227e-34, -2.41 decades per 10 in D, in between
  D 40.020065 -> 50.007491: bound 5.227e-34 -> 1.404e-34, -0.57 decades per 10 in D, not horizon-like
  D 50.007491 -> 54.996085: bound 1.404e-34 -> 2.559e-35, -1.48 decades per 10 in D, in between

Verdict per D (32x121 runs; trend from the step ending at D, D 30 from the step starting at it):
  D 30.000000: x mixed (rough start); smooth does not see it; trend in between (-2.41 decades per 10 in D) -> neither
  D 40.020065: x mixed (rough start); smooth does not see it; trend in between (-2.41 decades per 10 in D) -> neither
  D 50.007491: x centre in w4 (rough start); smooth does not see it; trend not horizon-like (-0.57 decades per 10 in D) -> neither
  D 54.996085: x centre in w4 (rough start); smooth does not see it; trend in between (-1.48 decades per 10 in D) -> neither

Rough bound against N at fixed D and N_t (decades between neighbouring N):
  D 30.0, N_t 32: N 81: 2.54e-26; N 121: 1.35e-31  (81->121: -5.27 decades)
  D 40.02, N_t 32: N 79: 9.37e-31; N 121: 5.23e-34; N 141: 2.99e-34  (79->121: -3.25, 121->141: -0.24 decades)
  D 40.02, N_t 48: N 141: 5.78e-35
  D 50.007, N_t 32: N 101: 1.51e-33; N 121: 1.40e-34  (101->121: -1.03 decades)
  D 54.996, N_t 32: N 85: 1.76e-33; N 121: 2.56e-35  (85->121: -1.84 decades)
N_t effect at D 40.02, N 141, rough: 2.993e-34 (N_t 32) -> 5.779e-35 (N_t 48), factor 0.193; class centre in w4 -> centre in w4
N_t effect at D 40.02, N 141, smooth: 8.333e-19 (N_t 32) -> 1.277e-19 (N_t 48), factor 0.153; class centre in w4 -> centre in w4

Columns: the bound is the best (smallest) of the 3 starts; "starts' spread" the largest bound over the smallest; E, C0, C4 as defined above for the best start's x, relative to its largest field entry; mu is |mu| / max|x|. The solve residuals of the rough starts are 2.8e-28 to 1.1e-18 relative to max|v| = 1, so the bounds 1 / max|x| hold to that relative accuracy.

## Controls

- **The check that can fail.** `logs/planted.log`: `rt_sigma.py --planted` exits 0 (best bound 1.41e-21 in [1e-22, 1e-20], largest other component 6.9e-19); `logs/planted_mutate_shift.log`: with `--mutate=shift` it exits 1 (best bound 1.42e-19, outside the window). `table_423.py --selftest` classifies three planted logs (edge, centre in omega_4, mixed) as expected.
- **A reproduction of #163.** The 32x101 state at D 50.007 is #163's (`I145-mac/cont/cont_32x101_D50.0075_32x101.npz`): rough bound 1.510e-33 here against 1.5e-33 on the Mac (`I163-mac/diag/sigma3_D50_101_rough.log`, RT_FORMULATION.md section 13), and smooth 1.4e-18 (best of 3) against 4.5e-18 (1 start). Same code on another machine and BLAS, not an independent method.
- **Starts agree.** The three rough starts of a run agree within a factor 1.0 to 3.9 (a factor 2.2 or less on 6 of the 10), the smooth ones within 3.0 to 18.5.
- **Not run:** a second implementation of the bound, an SVD of J (the bounds are upper bounds on the smallest gain, near it when the start is not nearly orthogonal to the weakest left vector), `--horizon K` states, and any N_t other than 32 and 48.

## What the numbers show, beyond the verdict

- **Against N at fixed D** (rough bound, decades between neighbouring N): D 30, 81 to 121, -5.27; D 40.02, 79 to 121, -3.25, then 121 to 141, -0.24; D 50.007, 101 to 121, -1.03; D 54.996, 85 to 121, -1.84. So the bound keeps falling with N, but from 121 to 141 at D 40.02 only by a factor 1.7.
- **Against N_t** (D 40.02, N 141): 32 to 48 lowers the rough bound from 2.99e-34 to 5.78e-35 (a factor 0.19) and the smooth one from 8.3e-19 to 1.3e-19 (0.15); x stays in omega_4 near xi = 0 (C4 = 1.00 in both).
- **The character of the weakest direction changes with N.** At D 40.02 it is dominated by mu (|mu| = 1.0) at N = 79 and 121, and sits in omega_4 near xi = 0 with |mu| 0.07 at N = 141 (0.02 at 48x141); at D 54.996 it is mu-dominated at N = 85 and in omega_4 at N = 121; at D 50.007 it is in omega_4 already at N = 101. The threshold N is not monotone in D at this resolution (between 121 and 141 at D 40, below 101 at D 50, between 85 and 121 at D 55).
- **Smooth starts reach a direction in the same place, much stronger.** At D 50.007 and 54.996 on 32x121 and at D 40.02 on N = 141 the best smooth start's x also has C4 = 1.00 (omega_4 near xi = 0) but its bound is 1e-19 to 1e-18, 10^15 times the rough one. So the weakest direction is not reached by smooth right-hand sides, as in #163, while the location is shared with a direction they do reach.

## Discrepancies

None with the text of #163. The coordinator's list of states is not what the raw repository holds (no 32x81 state at D 40, 50 or 55), which is why the grids differ; the table names every state.

## Recommended tasks (for the coordinator)

1. **The same bounds with `--horizon 7` states and the N_t = 48 grid at D 50.** What: `rt_sigma.py` on the K = 7 roots of `I163-mac/acc/` (32x121, D 50.007) and on a 48-wide state at D 50, rough starts, one BLAS thread above 4 GiB. Why: the rows exclude lambda_2's branch, and #163 found the weakest direction survives them at 4.9e-34; this run would show whether the rows change where x sits. Acceptance: the bound and the class per state, with the planted check and its control repeated. Depends on #423.
2. **Report the OpenBLAS crash above 4 GiB**, with `I423-win/lu_size_test.py` as the reproducer, to the maintainers of the scipy wheel in use, and add `OPENBLAS_NUM_THREADS=1` for matrices over 4 GiB to the RT notes. Not a task for the runners: a filed issue is a public action.


## Side task, 2026-11-13: facts for the OpenBLAS report (coordinator's message `1794551954544-0`)

Reproducer `lu_size_test.py N` (and `lu_size_test_steps.py`, the same with two progress prints): a random `N x N` float64 matrix, `scipy.linalg.lu_factor(A.T, overwrite_a=True, check_finite=False)` (the call of `LUdd`) and then `lu_solve` on `r = A.T @ x0`, which must return `x0` (the planted check; when it does not crash the error is 8.0e-11 for N = 20000 and 1.24e-10 for N = 23857). Windows 11 Pro `10.0.26200.9974`, i7-1185G7 (4 cores, 8 threads; threadpoolctl reports the SkylakeX kernels for every OpenBLAS here). Versions are in `logs/versions.txt`.

| stack | numpy / OpenBLAS in numpy | scipy / OpenBLAS in scipy (32-bit ints) | Python |
|---|---|---|---|
| old: `venv-t151` | 2.2.6 / 0.3.29 (ILP64) | 1.15.3 / 0.3.28 | 3.10.0 |
| new: throwaway `venv-blastest`, today's wheels from PyPI | 2.5.4 / 0.3.34.106.0 (ILP64) | 1.18.1 / 0.3.31.dev | 3.14.10 |

(Python 3.10 cannot install anything newer than numpy 2.2.6 and scipy 1.15.3, so the new stack is a Python 3.14.10 venv from the machine's nuget interpreter; a Python 3.10 venv with today's wheels resolves to the old versions.)

| stack | BLAS threads | N | matrix | result | log |
|---|---|---|---|---|---|
| old | 2 | 20000 | 2.98 GiB | passes (`lu_factor` 76 s, error 8.0e-11) | `lu_size_20000.log` |
| old | 2 | 21500 | 3.44 GiB | `lu_factor` done in 96 s, **`lu_solve` access violation** (0xC0000005, bash exit 139) | `lu_threshold_t151_21500.log` |
| old | 2 | 22300 | 3.71 GiB | `lu_factor` 105 s, **`lu_solve` access violation** | `lu_threshold_t151_22300.log` |
| old | 2 | 23100 | 3.98 GiB (under 2^32 bytes) | `lu_factor` 118 s, **`lu_solve` access violation** | `lu_threshold_t151_23100.log` |
| old | 2 | 23250 | 4.03 GiB | `lu_factor` 121 s, **`lu_solve` access violation** | `lu_threshold_t151_23250.log` |
| old | 2 | 23857 | 4.24 GiB | `lu_factor` 120 s, **`lu_solve` access violation** | `lu_size_23857.log` |
| old | **1** | 23857 | 4.24 GiB | **passes** (`lu_factor` 209 s, error 1.24e-10) | `lu_size_23857_1thread.log` |
| new | 2 | 20000 | 2.98 GiB | passes (`lu_factor` 68 s, error 8.0e-11) | `lu_threshold_latest_20000.log` |
| new | 2 | 23100 | 3.98 GiB | **dies inside `lu_factor`**, Windows exit code 0xC0000409 (fail-fast; run through PowerShell, `lu_threshold_latest_23100_rerun.log`; the first attempt through bash showed only "exit code 127") | `lu_threshold_latest_23100.log` |
| new | 2 | 23857 | 4.24 GiB | **dies inside `lu_factor`** (bash exit 139; the first run, `lu_size_23857_latest.log`, ended silently, the rerun with prints is `lu_size_23857_latest_steps.log`: last line "lu_factor starts") | `lu_size_23857_latest_steps.log` |
| new | **1** | 23857 | 4.24 GiB | **passes** (`lu_factor` 217 s, error 1.24e-10) | `lu_size_23857_latest_1thread.log` |

So: the crash is not at 4 GiB (3.44 GiB already crashes with scipy 1.15.3, 2.98 GiB does not; I did not bisect between), it needs more than one BLAS thread, and today's wheels crash as well, at a different place (inside `lu_factor` for scipy 1.18.1 against `lu_solve` for 1.15.3). Not tested: other Windows builds, other CPUs, a debug build of OpenBLAS, `OPENBLAS_CORETYPE=Haswell`, and N between 20000 and 21500. The throwaway venvs (`venv-blastest`, `venv-blastest310`) were sent to the Recycle Bin after the last test.


### Side task, second part (coordinator's message `1794554183629-0`): numpy's OpenBLAS 0.3.34 and the kernel family

A fresh Python 3.14.10 venv with today's wheels (numpy 2.5.4, scipy 1.18.1, threadpoolctl 3.8.0), two BLAS threads, BelowNormal, one test at a time beside #643; 13.8 GB free before the first. `np_solve_test.py` (numpy's own OpenBLAS, `np.linalg.solve(A, b)` with `b = A x0`, same generator and seed as `lu_size_test.py`), `lu_size_test_tp.py` (the LU reproducer with the threadpoolctl lines printed first). Windows exit codes come from PowerShell (`$p.ExitCode`); `OPENBLAS_CORETYPE` is set in the environment of the one process.

| test | threadpoolctl (numpy's OpenBLAS / scipy's OpenBLAS) | result | log |
|---|---|---|---|
| `np.linalg.solve`, N = 21500 (3.44 GiB) | 0.3.34.106.0 SkylakeX, pthreads, 2 threads / n.a. | **the solve finishes and is right** (92 s and 145 s in two runs, max abs error 1.26e-10) **and the process then dies at interpreter exit** with an access violation during garbage collection, no Python frame, exit code 0xC0000005 (both runs; `np_solve_21500.log`, `.err`) | `np_solve_21500.*` |
| `np.linalg.solve`, N = 20000 (2.98 GiB), the control | same | passes, exit 0 (81 s and 130 s, error 6.09e-11) | `np_solve_20000.*` |
| `lu_size_test.py`, N = 21500, default kernels | 0.3.34.106.0 SkylakeX / 0.3.31.dev SkylakeX, pthreads, 2 threads each | `lu_factor` done in 100 s, then **access violation** (0xC0000005) in a later Python call (`get_lapack_funcs`, called from `lu_solve`) | `lu_skylakex_21500.*` |
| the same, `OPENBLAS_CORETYPE=Haswell` | 0.3.34.106.0 **Haswell** / 0.3.31.dev **Haswell**, pthreads, 2 threads each | **passes**, `lu_factor` 136 s, error 1.61e-10, exit 0 | `lu_haswell_21500.*` |
| the same, N = 23857 (4.24 GiB), `OPENBLAS_CORETYPE=Haswell` | same | **passes**, `lu_factor` 170 s, error 8.56e-11, exit 0 | `lu_haswell_23857.*` |
| old stack (`venv-t151`: scipy 1.15.3, OpenBLAS 0.3.28), N = 23857, `OPENBLAS_CORETYPE=Haswell` | (not printed; the old venv has no threadpoolctl) | **passes**, `lu_factor` 187 s, error 8.56e-11, exit 0 | `lu_old_haswell_23857.*` |

Reading: with two threads the AVX-512 (SkylakeX) kernels corrupt memory on matrices of this size in both OpenBLAS 0.3.34 (numpy) and 0.3.31.dev (scipy), and in the old 0.3.28/0.3.29 pair, where it shows at once in `lu_solve`; in numpy's `solve` it shows only when the process exits, which is consistent with a write past an allocation (the answer is right, something else in the heap is not); I did not look for the cause. The Haswell (AVX2) kernels do not crash at either size or in either stack. So `OPENBLAS_CORETYPE=Haswell` is a workaround that keeps 2 BLAS threads above 4 GiB on this machine; I did not time it properly against one thread: the 1-thread LU of N = 23857 took 209 s and 217 s and the 2-thread Haswell ones 187 s and 170 s, but all of these ran beside other jobs, so the times are indicative only. Not tested: other CPUs, `OPENBLAS_CORETYPE=SkylakeX` with 1 thread (it passed by default at 1 thread), a debug build of OpenBLAS, and the old stack at N = 21500. The second throwaway venv (`venv-blastest`) was sent to the Recycle Bin after the last test.


### Side task, third part (coordinator's message `1794587330483-0`): the nightly wheels, a maintainer's suggestion on OpenMathLib/OpenBLAS#6252

The install was denied by the auto-mode classifier twice (16:29 and 16:35 UTC, texts in the message `1794587377513-0` and `1794587736639-0`), then allowed after Nathan's own message to the session; it ran once, unchanged: a Python 3.14.10 venv (the machine's nuget interpreter), `pip install --pre --upgrade --extra-index-url https://pypi.anaconda.org/scientific-python-nightly-wheels/simple numpy scipy threadpoolctl`. `logs/versions_nightly.txt` has the versions; the tests ran at two BLAS threads with the default kernels (`OPENBLAS_CORETYPE` unset), BelowNormal, one at a time beside #682, free memory 20 GB.

| package | version | OpenBLAS in it (threadpoolctl) |
|---|---|---|
| numpy | 2.6.0.dev0+git20261107.80049a0 | 0.3.34.237.2, 64-bit ints, SkylakeX, pthreads |
| scipy | 2.0.0.dev0+git20261108.c9073e6 | 0.3.34.237.2, 32-bit ints, SkylakeX, pthreads |
| threadpoolctl | 3.8.0 | |

| test (nightly wheels, 2 threads) | result | log |
|---|---|---|
| `np.linalg.solve`, N = 20000 (control) | passes, exit 0, 99 s, max abs error 6.09e-11 | `nightly_np_solve_20000.log` |
| `np.linalg.solve`, N = 21500 | **dies inside the solve**: access violation (0xC0000005), 17 s after the matrix-vector product, Python frame `numpy/linalg/_linalg.py` line 462 in `solve`. (The 0.3.34.106 wheel of part 2 finished the solve and died at exit.) | `nightly_np_solve_21500.*` |
| `lu_size_test.py`, N = 20000 (control) | passes, exit 0, `lu_factor` 92 s, error 8.0e-11 | `nightly_lu_20000.log` |
| `lu_size_test.py`, N = 21500 | `lu_factor` 97 s and `lu_solve` right (error 1.07e-10), "lu test done" printed, **then the process dies at exit** (0xC0000005, "Garbage-collecting", no Python frame) | `nightly_lu_21500.*` |
| `lu_size_test.py`, N = 23857 | **dies inside `lu_factor`** (0xC0000005, 163 s) | `nightly_lu_23857.*` |

So the nightly wheels, whose OpenBLAS is a build after 0.3.34 (0.3.34.237.2), crash as before: N = 20000 passes, 21500 and 23857 do not, in the same places as the wheels of part 2 (heap corruption that shows at exit for the LU at 21500, inside the factorization at 23857) except that `np.linalg.solve` at 21500 now dies inside the call. I did not check whether this build contains #6232 or #6235. The nightly venv was sent to the Recycle Bin after the last test.
