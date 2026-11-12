# I522-win2: one drifting period or two? A chirp fit of the weak values, and half-unit states in D 216 to 227

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/522 (follows from #521).
Part 1: `chirp_522.py`, analysis only (venv-t177).
Part 2: eleven attempts of a = 0.5 from crawlG's unit states D 216.1312 to 226.1312 (`job_i522.sh`: crawlK's command with `--h_max 0.5 --steps 1 --threads 5`, worktree `D:\choptuik-i446g` at main 14dc386, Python only, venv-t126), four at a time, each followed by `near_null_eq.py --plant=7 --threads=2` (worktree `D:\choptuik-i505` at 0cce81e) on the new state; then the control `--mutate=rows_only` at one of them. Exit codes in `exits.txt`. Results follow in this README.

## Results (attempts 2026-11-11 23:29:15 to 2026-11-12 00:45:00 UTC; control to 00:48:48; analysis 00:49 to 00:53)

**Part 2, the states.** Eleven attempts of a = 0.5 exited 0 (`exits.txt`), each accepted at octo-double (3 Newton steps to |F| ~ 3e-82, moved 7.5e-37 to 1.9e-34). `near_null_eq.py --plant=7` exited 0 at each new state, with the planted column scaling recovered to 1.6e-15 to 8e-14 (bound 1e-3) and ||J_eq v_1|| / sigma_1 = 1.000000. The control `--mutate=rows_only` at D 221.6312 exited 1 (planted check 1.00e+00, FAIL, as it must; `eq_D221.6312_ctl_rows_only.log`).

Equilibrated sigma_1..4 of the eleven new states:

| D | sigma_1 | sigma_2 | sigma_3 | sigma_4 |
|---|---|---|---|---|
| 216.6312 | 1.0543e-48 | 3.3413e-48 | 3.0202e-45 | 2.0533e-43 |
| 217.6312 | 3.2064e-49 | 1.5624e-48 | 1.0951e-45 | 7.1690e-44 |
| 218.6312 | 1.3719e-49 | 5.0306e-49 | 3.5493e-46 | 2.7125e-44 |
| 219.6312 | 4.8054e-50 | 1.9465e-49 | 1.3936e-46 | 8.2801e-45 |
| 220.6312 | 1.6109e-50 | 7.6775e-50 | 3.9903e-47 | 3.3495e-45 |
| 221.6312 | 6.9647e-51 | 2.2871e-50 | 1.6550e-47 | 9.0962e-46 |
| 222.6312 | 1.9994e-51 | 1.0044e-50 | 4.2847e-48 | 3.8090e-46 |
| 223.6312 | 7.9847e-52 | 3.0755e-51 | 1.7932e-48 | 9.6258e-47 |
| 224.6312 | 2.7034e-52 | 1.0916e-51 | 4.4437e-49 | 3.9852e-47 |
| 225.6312 | 8.2443e-53 | 4.1649e-52 | 1.7606e-49 | 9.9722e-48 |
| 226.6312 | 3.4003e-53 | 1.1468e-52 | 4.4179e-50 | 3.7763e-48 |

**Part 2, the periods at half-unit spacing** (`halfunit_522.py` -> `results_halfunit_522.txt`; selftest ok: a planted 2.53 is recovered as 2.535 and a planted alias 1.654 as 1.650, both with null fraction 0.0%). 23 states D 216.13 to 227.13 at spacing 0.5, trend + one sinusoid, the period scanned from 1.1 (below the unit-spacing Nyquist period 2) in steps of 0.005, 1000-trial null test. The interval in brackets is the range of periods whose sum of squares is within one residual variance of the best, a spread over the scan and not a rigorous bound.

| series | unit spacing (#521) | its alias | half-unit, quadratic trend | difference | null fraction | verdict of the rule | half-unit, line trend (null fraction) |
|---|---|---|---|---|---|---|---|
| sigma_1 | 2.530 | 1.654 | 2.525 (2.520 to 2.530), rms 0.0071 | -0.005 | 0.0% | confirms | 2.470 (1.8%), rms 0.058 |
| sigma_2 | 2.525 | 1.656 | 2.525 (2.520 to 2.530), rms 0.0075 | -0.000 | 0.0% | confirms | 2.545 (0.0%), rms 0.059 |
| sigma_3 | 2.165 | 1.858 | 2.165 (2.160 to 2.165), rms 0.0065 | -0.000 | 0.0% | confirms | 2.145 (0.1%), rms 0.074 |
| sigma_4 | 2.155 | 1.866 | 2.160 (2.160 to 2.165), rms 0.0069 | +0.005 | 0.0% | confirms | 2.210 (3.2%), rms 0.076 |

The periods read from unit spacing in #521 are the real ones, not aliases: the half-unit data find them again to 0.005 with the scan open down to 1.1, and nothing near 1.65 to 1.87. The amplitudes are 0.110, 0.111, 0.129 and 0.127 (errors 0.002 to 0.003). With the line trend the residuals stay at 0.06 to 0.08 (the line cannot hold the curvature), so the quadratic trend is what the rule uses, as in #521; the line fits now find the same periods within 0.06 where #521's 12 unit states found nothing (null fractions 12.5% to 83% there, 0.0% to 3.2% here), because the fit has 23 points instead of 12.

**Part 1, the chirp fit** (`chirp_522.py`; selftest ok). Model: quadratic trend + one sinusoid with period P(D) = P0 + p1 (D - 228), P0 scanned 1.50 to 3.50 step 0.01 and p1 -0.12 to 0.12 step 0.002; null fractions from 1000 trials of a line + white noise, in two conventions (noise at the observed rms, noise at the rms of the quadratic trend alone), both 0.0% for every series. The p1 interval is the range of p1 whose best sum of squares is within one residual variance of the minimum, a spread over the grid and not a rigorous bound.

| series | states | P0 (D 228) | p1 per unit of D | P at D 216 | P at D 237 | amplitude | rms residual |
|---|---|---|---|---|---|---|---|
| sigma_1 | 28 (D 216 to 237, `results_chirp_522.txt`) | 2.62 | +0.014 | 2.45 | 2.75 | 0.1130 +- 0.0020 | 0.0062 |
| sigma_1 | 39 (with the 11 new, `results_chirp_522_with_half_units.txt`) | 2.62 | +0.016 (0.014 to 0.016) | 2.43 | 2.77 | 0.1126 +- 0.0017 | 0.0068 |
| sigma_2 | 28 | 2.62 | +0.016 | 2.43 | 2.77 | 0.1105 +- 0.0021 | 0.0065 |
| sigma_2 | 39 | 2.62 | +0.016 (0.016 to 0.016) | 2.43 | 2.77 | 0.1108 +- 0.0015 | 0.0061 |
| sigma_3 | 28 | 2.20 | +0.004 | 2.15 | 2.24 | 0.1211 +- 0.0055 | 0.0188 |
| sigma_3 | 39 | 2.20 | +0.004 (0.004 to 0.006) | 2.15 | 2.24 | 0.1238 +- 0.0041 | 0.0172 |
| sigma_4 | 28 | 2.20 | +0.008 | 2.10 | 2.27 | 0.1314 +- 0.0036 | 0.0119 |
| sigma_4 | 39 | 2.20 | +0.006 (0.006 to 0.008) | 2.13 | 2.25 | 0.1296 +- 0.0032 | 0.0135 |

Rule of #522 (the chirp fit reaches the residuals of the half fits, about 0.005, with a null fraction below 1%): for sigma_1 and sigma_2 it does, to within the half-unit low half's 0.007: one oscillation whose period grows by about 0.016 per unit of D (2.43 at D 216 to 2.77 at D 237, +14%) describes both halves, with a residual of 0.0068 and 0.0061 against 0.0795 and 0.0781 for the quadratic trend alone. For sigma_3 and sigma_4 it does not: the residual is 0.017 and 0.014, two to three times that of the half fits (0.0065 and 0.0069 in the low half), and adding the 11 new states did not bring it to that level (sigma_3 0.0188 to 0.0172, sigma_4 0.0119 to 0.0135). The chirp's period at the centre of each half agrees with the half's own fit to 0.031 or better (the tolerance of the script is 0.05) (`centres_522.py` -> `results_centres_522.txt`; its control `--mutate=p1zero`, the drift set to 0, exits 1, `results_centres_522_ctl_p1zero.txt`):

| series | chirp P at D 221.63 | low half fitted | chirp P at D 232.63 | high half fitted |
|---|---|---|---|---|
| sigma_1 | 2.518 | 2.525 | 2.694 | 2.715 |
| sigma_2 | 2.518 | 2.525 | 2.694 | 2.725 |
| sigma_3 | 2.175 | 2.165 | 2.219 | 2.230 |
| sigma_4 | 2.162 | 2.160 | 2.228 | 2.245 |

What this does not establish: why sigma_3 and sigma_4 leave 0.013 to 0.017 of residual under a linear period drift (an amplitude that changes with D, a second component, or a drift that is not linear are candidates, none tested here), and what sets the drift.
Software: numpy in venv-t177 (analysis); venv-t126 with its hpkernel build (the runs).
