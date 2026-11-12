# I404-win: the RT prototype on the N = 3 mod 4 grid ladder, 32x99 to 32x123, at D = 60.001952, 54.996085, 50.007491 and 40.020065

Machine win (Surface Laptop 4, i7-1185G7, 4 cores/8 threads, 31.8 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/404 (the coordinator's message `choptuik-large-d/2026-11-12/151101Z-coordinator-2c36.md`; recommended by #164's subagent; formerly #166).
Code: main f5f9eecb of nmoinvaz/choptuik-large-d, worktree `choptuik-i404` (`solver/rt/`, Python with python-flint 0.9.0 and multidouble's Python package with `dd_dot`, in venv-t151; nothing is built). The set-up is #164's (`I164-mac/README.md`): `rt_run.py --solver mp` (192 bits, N_t = 32).

Starts (the same files as #164, from `I145-mac`, copied unchanged; sha256 first 16 and size):

- a: `I145-mac/cont/cont_32x101_<D>_32x101.npz` (the 32x101 continuation's state): D 60.0020 4d4228bca5df6a23, D 54.9961 fd3170e8ac0340be, D 50.0075 f2f371033276c034, D 40.0201 18221618c647a967 (275656 bytes each).
- b: `I145-mac/fol/fol_32x121_<D>_32x121.npz` (the 32x121 root re-solved from a): D 60.0020 d536261c287d7fef, D 54.9961 782657c8d1dae592, D 50.0075 b5112fff7c82b272, D 40.0201 a6767a7dec01e91c (329416 bytes each).

Each is resampled to 32xN by `rt_run.py --start` and solved there at the same D.

## Criteria, written before the main runs (not changed afterwards)

- Solver and options, as #164 / #145 at D 55-60: `rt_run.py --start ST --grids 32xN --solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4 --newton_tol NTOL --out roots --tag <a101|b121>_32xN`, with NTOL = 1e-36 at D 60.001952, 1e-38 at D 54.996085 (#164's), and 1e-40 (rt_run.py's default, #145's own value up to D 53) at D 50.007491 and D 40.020065.
- Convergence: a root counts when its record has ok true, that is Newton reached max|F| below NTOL, or stalled within 1e6 of it under --patient. An unconverged solve may be restarted once from its saved last state with the same options (recorded here); if that does not converge either, the root counts as failing.
- Hp: the double-double rows of `hp/data/delta_all.csv` at D 60.001952 (up13), 54.996085 (up10), 50.007491 (up8) and 40.020065 (up7), Delta_q0 + Delta_q1, err 2e-15. Differences are taken in arb from the records' 30-digit Delta_str (`rt_grids.py`).
- Grids: N = 99, 103, 107, 111, 115, 119, 123 (all N = 3 mod 4), at each D from both starts: 14 solves per D. D 60.001952 first, then 54.996085, 50.007491, 40.020065. Four solves at once as separate processes, one thread each (BLAS threads 1), BelowNormal. The raw folder is pushed after each D, and the D 60 result is reported to the coordinator before going on.
- Definitions, per D and N: E(N) is the larger of the two roots' |Delta_RT - Delta_hp|; the spread s(N) = |Delta_a - Delta_b|; a grid passes when `rt_grids.py roots/a101_32xN.jsonl roots/b121_32xN.jsonl --D <D> --tol 1e-14` exits 0, that is both roots converged, both within 1e-14 of hp and their spread below 1e-14 (the hp rows carry err 2e-15, so 1e-14 is 5 times that).
- **Verdict at a D: the ladder falls to below 1e-14 when** some grid N* passes and E decreases strictly along the ladder up to N* (E(99) > E(103) > ... > E(N*)), or N* = 99 (it passes at the first rung; then the later grids are reported beside it). Otherwise the ladder **stops falling** at N_s, the first rung whose E is not below the previous rung's (E(N_{k+1}) >= E(N_k)) or the rung with the smallest E if E falls to the end: the report gives N_s, E(N_s), s(N_s) and the sign of Delta_RT - Delta_hp of each root along the ladder. The verdict of #404 per D is one of these two.
- Pair test: `rt_roots.py A.npz B.npz` (the planted check first, then the pair test of #164) on each pair of roots (a, b) at each N and D; the numbers (the roots' distance and B(e, e) / max|e|) are reported beside the verdict, outside it.
- Controls, once at D 60.001952, each must exit 1: `rt_grids.py --mutate=shift` on the best grid's two roots (2 tol added to one Delta) and `rt_roots.py --mutate=mid` on one pair of roots; the unmutated `rt_roots.py` planted check exits 0.
- Stop conditions: a Traceback, a solve past 4 h, or a failing restart (reported with its lines).

## What ran

The interpreter is Python 3.10.0 (venv-t151: python-flint 0.9.0, multidouble 0.1.0) on Windows where the RT code was written for Python 3.13 (the Mac) and SETUP.md asks for 3.14; the coordinator accepted a launcher that changes no repository file (agent-comms 162206Z). Four things in the code needed a stand-in here, found one run at a time (the logs of each failed launch are kept):

1. 15:14:36 UTC, `failed_attempt1/`: the first four solves died within 90 s with `AttributeError: module 'multidouble' has no attribute '_dd_dot'` (`rt_mpsolve.py` line 187; this multidouble has `dd_dot(xh, xl, yh, yl)`, the same arguments, as a wrapper of the same Rust function).
2. 15:17:45 UTC, `failed_attempt2/`: `AttributeError: module 'math' has no attribute 'fma'` (`rt_mpsolve._dd_div`, line 150; `math.fma` is Python 3.13 and later). `rt_launch.py` runs the repository's `rt_run.py` unchanged after aliasing `_dd_dot` and defining `math.fma` exactly with `fractions.Fraction` (one correct rounding); its selftest `selftest_rt_launch.txt`: against arb at 600 bits 0 of 20000 random cases differ, and the naive `x*y + z` differs in 10995 (the control).
3. 15:21:18 UTC (third launch), `failed_attempt3_resource/`: the first four solves (32x99 and 32x103, both starts) converged (4 Newton steps, final max|F| 4.9e-49, 1.3e-46, 7.3e-43, 1.4e-40, 11 to 14 min each) and died at the record step with `ModuleNotFoundError: No module named 'resource'` (`rt_run.py` `rss_peak_gb()`, a Unix module), before a record or a state was written. The stand-in `resource.py` (peak working set by ctypes `GetProcessMemoryInfo`, in KiB as `rt_run.py` expects; a 400 MB allocation raised it by 392 MB) was put beside the launcher at 15:44 UTC, and the solves already running (32x107, 32x111) found it when they ended.
4. `run_queue_404.py`'s skip rule first took rt_run's exit code 0 as "done"; `rt_run.py` exits 1 when |Delta_RT - Delta_hp| exceeds `--tol 1e-12`, which is the quantity under study, so the rule was changed to a converged record at the D in the jsonl (15:46 UTC, before it was used).

The four lost solves were rerun by a second queue (`run_queue_404.py D60.0020 --nproc 2 --grids 99,103`, 16:23:19 to 16:47:11 UTC, 660 to 751 s each). The first queue (14 jobs, four at once, one thread each, BelowNormal) ran 15:21:18 to 16:49:32 UTC (5294 s). Every one of the 14 records at D 60.001952 is `ok` on the first full run; no solve was restarted from a saved state. `fit/` holds the analysis (`analyze_404.py` -> `fit_analysis_D60.0020.txt`, `fit/verdict_32xN_D60.0020.log` from `rt_grids.py --tol 1e-14`, `fit/roots_32xN_D60.0020.log` from `rt_roots.py`, `run_fit_404.py`, `fit/summary_D60.0020.md`) and the controls.

## D 60.001952 (reported before going on)

Delta_RT - Delta_hp of the two roots on each grid, their spread, and the pair test (`rt_roots.py`; the planted checks pass for every pair), with the cost per solve (four at once):

| N | root a - hp | root b - hp | spread a - b | E(N) | max abs(z_b - z_a) | max abs(B(e,e)) / max abs(e) | Newton steps a, b | seconds a, b | peak GB a, b |
|---|---|---|---|---|---|---|---|---|---|
| 99 | -3.46e-13 | -1.80e-12 | +1.45e-12 | 1.80e-12 | 1.000e-13 | 6.7e-13 | 4, 4 | 654, 670 | 1.2, 1.21 |
| 103 | -4.04e-12 | -4.86e-11 | +4.46e-11 | 4.86e-11 | 3.302e-12 | 7.7e-12 | 4, 4 | 732, 743 | 1.29, 1.29 |
| 107 | +4.73e-12 | +1.30e-10 | -1.25e-10 | 1.30e-10 | 1.158e-11 | 1.5e-09 | 4, 4 | 905, 938 | 1.38, 1.38 |
| 111 | +2.57e-13 | -5.69e-10 | +5.70e-10 | 5.69e-10 | 3.935e-11 | 2.5e-10 | 4, 6 | 1030, 1737 | 1.47, 2.74 |
| 115 | +2.08e-11 | -7.62e-12 | +2.84e-11 | 2.08e-11 | 2.424e-12 | 1.5e-10 | 4, 4 | 1108, 1140 | 1.57, 1.58 |
| 119 | -8.60e-12 | -1.04e-11 | +1.77e-12 | 1.04e-11 | 1.606e-12 | 6.5e-10 | 4, 4 | 1146, 1077 | 1.67, 1.68 |
| 123 | -1.63e-07 | +2.27e-11 | -1.63e-07 | 1.63e-07 | 1.230e-08 | 7.9e-08 | 8, 4 | 2527, 1147 | 3.32, 1.78 |

**Verdict at D 60.001952: the ladder does not fall; it stops falling at N_s = 99** (the first rung): E(99) = 1.80e-12, spread 1.45e-12, both roots below hp (signs --), and E(103) = 4.86e-11 is larger. No grid passes `rt_grids.py --tol 1e-14` (nor 1e-12: root b of 32x99 is -1.80e-12). Beyond 99 the roots scatter between 1e-12 and 6e-10 with changing signs, and root a of 32x123 is at -1.63e-07: eight Newton steps with the residual bouncing between 1e-14 and 1e-28 (steps 2 to 6; two preconditioner rebuilds, 42 min, 3.3 GB), ending at max|F| 2.1e-38 on a root 1.2e-8 away from the other. For every N the pair test says the two roots are distinct (the residual rises between them: max|F(zm)| 1.7e-26 at 99 up to far above the roots' 1e-31 residuals), so the discrete system has a family of nearly degenerate roots, at residuals below 1e-30, spread over Delta by 1e-12 to 1e-7. #164's 32x95 (-6.4e-13, -5.9e-13), also N = 3 mod 4, lies at E = 6.4e-13, below this ladder's best.

**Against the Mac's #164 at 32x99** (a different machine, Python 3.13): start a -3.46e-13 here, -3.45e-13 there; start b -1.80e-12 here, -2.70e-13 there. The two starts-a roots agree to 1e-15, the starts-b roots differ by 1.5e-12, about the size of the root family's own spread at this N; rounding in the f64 preconditioner (and the exact `fma` I supply) can select another member of it.

**Controls at D 60.001952, on the best grid (32x99)** (`fit/control_*_32x99_D60.0020.log`): `rt_grids.py --mutate=shift` (2 tol added to root b's Delta) exits **1** at `--tol 1e-11`, where the unmutated check exits **0** (at 1e-14 or 1e-12 the grid fails by itself, so the mutation could not be told from it); `rt_roots.py --mutate=mid` exits **1** (its planted pair check gives relative error 2.0e11 and fails); `rt_roots.py --mutate=same` exits 1; the unmutated `rt_roots.py` planted checks pass (exit 0) for all seven pairs.

## D 54.996085 (queue 16:55:15 to 18:16:48 UTC, 4894 s; analysis 18:18 UTC)

All 14 solves converged on their first run (no restart, no crash; the launcher and the stand-in `resource.py` of the D 60 section were in place). Same table as above, `fit/summary_D54.9961.md`, `fit_analysis_D54.9961.txt`, `fit/verdict_32xN_D54.9961.log`, `fit/roots_32xN_D54.9961.log` (the planted checks pass for all seven pairs):

| N | root a - hp | root b - hp | spread a - b | E(N) | max abs(z_b - z_a) | max abs(B(e,e)) / max abs(e) | Newton steps a, b | seconds a, b | peak GB a, b |
|---|---|---|---|---|---|---|---|---|---|
| 99 | -3.75e-14 | -1.64e-14 | -2.11e-14 | 3.75e-14 | 1.660e-15 | 3.3e-14 | 4, 4 | 665, 685 | 1.2, 1.2 |
| 103 | -6.91e-14 | -7.49e-14 | +5.78e-15 | 7.49e-14 | 4.256e-16 | 9.5e-16 | 4, 4 | 734, 730 | 1.29, 1.28 |
| 107 | +5.44e-12 | -6.20e-13 | +6.06e-12 | 5.44e-12 | 4.388e-13 | 5.3e-13 | 4, 4 | 904, 886 | 1.37, 1.38 |
| 111 | +8.19e-14 | -6.93e-12 | +7.01e-12 | 6.93e-12 | 4.693e-13 | 5.2e-12 | 4, 4 | 980, 1009 | 1.47, 1.47 |
| 115 | -4.46e-11 | -8.53e-11 | +4.07e-11 | 8.53e-11 | 4.751e-12 | 1.6e-09 | 6, 4 | 1603, 1050 | 1.59, 1.56 |
| 119 | -9.89e-12 | -2.33e-10 | +2.23e-10 | 2.33e-10 | 1.688e-11 | 1.3e-10 | 4, 4 | 1162, 1153 | 1.67, 1.67 |
| 123 | +5.65e-11 | -1.21e-09 | +1.26e-09 | 1.21e-09 | 9.781e-11 | 1.3e-09 | 4, 8 | 1055, 1995 | 1.77, 3.3 |

**Verdict at D 54.996085: the ladder stops falling at N_s = 99**: E(99) = 3.75e-14, spread 2.11e-14, both roots below hp (signs --); E(103) = 7.49e-14 is larger and beyond it E grows to 1.21e-09. No grid passes `rt_grids.py --tol 1e-14` (the best, 32x99, is 3.75e-14 and 1.64e-14 from hp with a spread of 2.11e-14, a factor 2 to 4 above the bound). (At D 60.001952 the best grid was at 1.8e-12.)

**Pair test.** At N = 99 and 103 the two roots are not told apart: |z_b - z_a| is 1.7e-15 and 4.3e-16, and the pair test says the rise of the residual between them is "hidden by the residual floor", so at these N the two starts reach one root (the spreads 2.1e-14 and 5.8e-15 are the Delta uncertainty of that root at the residual floor, with hp's own error 2e-15). From N = 107 the two are distinct (the residual rises between them), |z_b - z_a| from 4.4e-13 (107) to 9.8e-11 (123): the degeneracy sets in between 103 and 107 at D 54.996, against already at 99 at D 60.

**Against the earlier results at this D.** #164 (the other family N = 3 mod 4 up to 97, both starts agreeing to 2e-14): 95 -5.46e-13, 97 +1.25e-13; here 99 is -3.75e-14 and -1.64e-14, so the ladder 95, 97, 99 is -5.5e-13, +1.3e-13, -3e-14 (not monotone in sign, falling in size), and 103 (-7e-14) does not continue the fall. #145's 32x101 (N = 1 mod 4) was -2.1e-14 at this D. Cost: 665 to 1162 s per solve for N 99 to 119 (four at once), up to 2002 s for the ones that needed 6 or 8 Newton steps (115a, 123b).

## D 50.007491 (queue 18:16:52 to 19:20:05 UTC, 3793 s; analysis 19:20 UTC)

All 14 solves converged on their first run (NTOL 1e-40; root b of 32x99 took 9 Newton steps and 1637 s, ending at max|F| 3.5e-38, a stall accepted within 1e6 of NTOL). Same table, `fit/summary_D50.0075.md`, `fit_analysis_D50.0075.txt`, `fit/verdict_32xN_D50.0075.log`, `fit/roots_32xN_D50.0075.log` (the planted checks pass for all seven pairs):

| N | root a - hp | root b - hp | spread a - b | E(N) | max abs(z_b - z_a) | max abs(B(e,e)) / max abs(e) | Newton steps a, b | seconds a, b | peak GB a, b |
|---|---|---|---|---|---|---|---|---|---|
| 99 | -2.33e-14 | -2.33e-14 | +1.12e-18 | 2.33e-14 | 8.455e-20 | 6.7e-19 | 4, 9 | 678, 1637 | 1.18, 1.19 |
| 103 | -2.95e-15 | -2.90e-15 | -4.86e-17 | 2.95e-15 | 2.863e-18 | 2.0e-16 | 4, 4 | 761, 748 | 1.27, 1.27 |
| 107 | -7.53e-15 | -7.39e-15 | -1.45e-16 | 7.53e-15 | 9.385e-18 | 1.5e-16 | 4, 4 | 859, 860 | 1.36, 1.36 |
| 111 | -5.97e-14 | -6.56e-14 | +5.89e-15 | 6.56e-14 | 7.528e-15 | 2.5e-12 | 4, 4 | 956, 1018 | 1.46, 1.46 |
| 115 | -3.08e-13 | +1.00e-14 | -3.18e-13 | 3.08e-13 | 2.386e-14 | 1.4e-13 | 4, 4 | 1092, 1115 | 1.56, 1.56 |
| 119 | -1.34e-12 | -2.62e-12 | +1.28e-12 | 2.62e-12 | 9.216e-14 | 1.3e-13 | 4, 4 | 1157, 985 | 1.66, 1.65 |
| 123 | -1.95e-12 | -3.31e-11 | +3.11e-11 | 3.31e-11 | 2.165e-12 | 5.5e-12 | 4, 4 | 1018, 1013 | 1.76, 1.75 |

**Verdict at D 50.007491: the ladder falls to below 1e-14 at N* = 103**: E(99) = 2.33e-14 > E(103) = 2.95e-15, and 32x103 passes `rt_grids.py --tol 1e-14` (both roots within 3e-15 of hp, spread 4.9e-17; hp's own error is 2e-15, so 32x103 equals hp within hp's error). 32x107 also passes (E = 7.53e-15, spread 1.5e-16) but E rises from 103 to 107, and from 111 on it grows steadily (6.56e-14, 3.08e-13, 2.62e-12, 3.31e-11): the ladder falls to N* = 103 and then rises again, so the window of N for which RT reproduces hp to 1e-14 at D 50 is 103 to 107.

**Pair test.** For N = 99, 103 and 107 the two starts reach one root to 1e-19 to 1e-17 (|z_b - z_a| 8.5e-20, 2.9e-18, 9.4e-18; the residual rise between them is "hidden by the residual floor"); from N = 111 the two roots are distinct (the residual rises between them), 7.5e-15 (111), 2.4e-14 (115), 9.2e-14 (119), 2.2e-12 (123) apart. So the degeneracy sets in between 107 and 111 at D 50.007, against between 103 and 107 at D 54.996 and at 99 or below at D 60.001952.

**Against the earlier results at this D.** #145's 32x101 (N = 1 mod 4, root a) was +3.3e-15; the neighbours of this ladder are 99 -2.3e-14, 103 -2.9e-15 and 107 -7.5e-15, all negative. Cost: 678 to 1157 s per solve (four at once), 1637 s for 99b (9 Newton steps).

## D 40.020065 (queue 19:20:05 to 20:14:28 UTC, 3263 s; analysis 20:15 UTC)

All 14 solves converged on their first run, 4 Newton steps each (NTOL 1e-40), no restart. Same table, `fit/summary_D40.0201.md`, `fit_analysis_D40.0201.txt`, `fit/verdict_32xN_D40.0201.log`, `fit/roots_32xN_D40.0201.log` (the planted checks pass for all seven pairs):

| N | root a - hp | root b - hp | spread a - b | E(N) | max abs(z_b - z_a) | max abs(B(e,e)) / max abs(e) | Newton steps a, b | seconds a, b | peak GB a, b |
|---|---|---|---|---|---|---|---|---|---|
| 99 | -8.22e-15 | -8.22e-15 | -1.58e-23 | 8.22e-15 | 1.199e-24 | 1.3e-23 | 4, 4 | 604, 607 | 1.16, 1.16 |
| 103 | +1.17e-15 | +1.17e-15 | +2.36e-21 | 1.17e-15 | 1.485e-22 | 2.0e-21 | 4, 4 | 674, 674 | 1.25, 1.25 |
| 107 | +1.54e-15 | +1.54e-15 | +1.09e-20 | 1.54e-15 | 7.836e-22 | 6.8e-20 | 4, 4 | 782, 759 | 1.34, 1.34 |
| 111 | +1.56e-15 | +1.56e-15 | +4.32e-21 | 1.56e-15 | 3.153e-22 | 1.2e-21 | 4, 4 | 894, 902 | 1.43, 1.43 |
| 115 | +1.55e-15 | +1.55e-15 | -8.13e-21 | 1.55e-15 | 6.543e-22 | 1.7e-20 | 4, 4 | 959, 922 | 1.53, 1.53 |
| 119 | +1.55e-15 | +1.55e-15 | +2.55e-20 | 1.55e-15 | 2.161e-21 | 9.2e-20 | 4, 4 | 1014, 1016 | 1.63, 1.63 |
| 123 | +1.54e-15 | +1.54e-15 | +3.18e-18 | 1.54e-15 | 3.126e-19 | 3.4e-17 | 4, 4 | 915, 914 | 1.73, 1.74 |

**Verdict at D 40.020065: the ladder falls to below 1e-14 at N* = 99, its first rung** (E(99) = 8.22e-15, spread 1.6e-23), and it **keeps converging**: all seven grids pass `rt_grids.py --tol 1e-14`. E settles on a plateau: from N = 107 to 123 Delta_RT - Delta_hp is +1.54e-15, +1.56e-15, +1.55e-15, +1.55e-15, +1.54e-15, constant to about 2e-17, and the two starts agree to 1e-18 to 1e-24. The plateau value (+1.55e-15) is the difference between the RT limit and hp's double-double row, inside hp's stated error 2e-15; it is not a failure of the grid to converge.

**Pair test.** For all seven grids the two roots are one root to 1e-24 to 3e-19 (|z_b - z_a| 1.2e-24 at 99, 1.5e-22 at 103, up to 3.1e-19 at 123; the pair test says "hidden by the residual floor" for every N): there is no degeneracy at D 40.020, up to 123.

**Against the earlier results at this D.** #145's 32x101 (N = 1 mod 4) was +3.5e-15, 2e-15 above this plateau (+1.55e-15), while the N = 3 mod 4 family sits on the plateau from 103 on (E(103) = 1.17e-15 is 4e-16 below it). Cost: 604 to 1016 s per solve (four at once), 4 Newton steps each.

## Across D: where the N = 3 mod 4 ladder converges

E(N), the larger of the two roots' |Delta_RT - Delta_hp| (the bold ones pass 1e-14), and the grid from which the two starts give two distinct roots:

| N | D 40.020065 | D 50.007491 | D 54.996085 | D 60.001952 |
|---|---|---|---|---|
| 99 | **8.22e-15** | 2.33e-14 | 3.75e-14 | 1.80e-12 |
| 103 | **1.17e-15** | **2.95e-15** | 7.49e-14 | 4.86e-11 |
| 107 | **1.54e-15** | **7.53e-15** | 5.44e-12 | 1.30e-10 |
| 111 | **1.56e-15** | 6.56e-14 | 6.93e-12 | 5.69e-10 |
| 115 | **1.55e-15** | 3.08e-13 | 8.53e-11 | 2.08e-11 |
| 119 | **1.55e-15** | 2.62e-12 | 2.33e-10 | 1.04e-11 |
| 123 | **1.54e-15** | 3.31e-11 | 1.21e-09 | 1.63e-07 |
| verdict | falls to below 1e-14 at 99 and stays (plateau +1.55e-15) | falls to below 1e-14 at 103; passes at 103 and 107 only | stops falling at 99 (3.75e-14) | stops falling at 99 (1.80e-12) |
| roots distinct from | none up to 123 | 111 | 107 | 99 |

The degeneracy of the discrete system, nearly degenerate roots at residuals below 1e-30 spread over Delta by 1e-12 to 1e-7, sets in at smaller N as D grows: not at all up to 123 at D 40, from 111 at D 50, from 107 at D 54.996, from 99 at D 60.002. The N = 3 mod 4 ladder converges (to hp's error) at D 40, for N 99 to 123; at D 50 only on N = 103 to 107; at D 54 and 60 it does not reach 1e-14.
