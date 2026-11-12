# I534-win: the second harmonic of ln sigma_1 and ln sigma_2 against the first, by window of D (analysis only)

Machine win (Surface Laptop 4, i7-1185G7), issue https://github.com/nmoinvaz/choptuik-large-d/issues/534 (moved from win2; the coordinator's message `choptuik-large-d/2026-11-12/134207Z-coordinator-1601.md`; recommended by win2 in #525's closing summary). Analysis only, one thread, venv-t151 (numpy 2.2.6, scipy 1.15.3, Python 3.10). The scripts read #533's code and #525's data from an up-to-date raw worktree (`I533-win2/period_p2_533.py`, its siblings in `I525-win2`, `I522-win2`, `I521-win2`, `I505-win2`), nothing is copied from it. Run from this folder with `PYTHONPATH=.`: `python second_harmonic_534.py --raw=<raw worktree> planted --scenario=S0|S0A|S0B|S1A|S1B|S2 --seeds=300`, `summarize FILES` (v1 rules), `summarize2 FILES` (v2 rules), `data --verdict=results_planted_534_v2.txt`, and `python posthoc_534.py --raw=<raw worktree>`.

## Method

The 51 equilibrated states D 210.13 to 237.13 of #505 to #525, ln sigma_1 and ln sigma_2 (`collect51()` of #533). The chirp of #533 (cubic trend in u = (D - 228) / 10, one sinusoid, period P0 + p1 x + p2 x^2, x = D - 228, `Fitter.fit_free`) is fitted to all 51 states and gives the phase phi(D). In each window the series is fitted by least squares as a quadratic in the window plus A1 cos phi + B1 sin phi + A2 cos 2 phi + B2 sin 2 phi with phi fixed. The ratio is rho = a2 / a1 (a_k = hypot(A_k, B_k)), the relative phase theta = delta2 - 2 delta1 (a_k cos(k phi + delta_k); unchanged if phi's origin moves). Errors: the delta method on the least-squares covariance, with a 1000-trial parametric bootstrap as a cross-check. Windows, by D and half open: D < 216 (12 states), 216 <= D < 228 (23 states), D >= 228 (16 states); the states between 227 and 228 belong to the middle window.

## Planted truth first (through the same code, the whole pipeline including the global chirp fit)

Fixed on the issue before the real series was read (comment 6825380215, edited afterwards only for its start time and one phrase): amplitude a1 = 0.11, noise 0.006, phi from P0 2.62, p1 +0.0165, p2 +0.0003, relative phase 1.0 rad, 300 seeds per scenario at the D of the data; S0 rho = 0, S1 rho = 0.066 in all windows (A calibrates, B tests), S2 rho = 0.03, 0.066, 0.12; rules R1 to R3 in the script's header and on the issue.

**First verdict (v1, `results_planted_534_v1.txt`): FAIL on one rule.** R1 on S0 (the interval rho_hat +- 2 SE must cover rho = 0 in at least 88% of seeds) gave 79%, 86% and 79%: rho_hat cannot be negative, so the interval misses 0 whenever the noise gives any second harmonic, and the delta-method SE is also too small in the 12-state window. Everything else passed (S1B coverage 88%, 95%, 94%; S2 91%, 96%, 91%; bias; Q size 5% on S1B and 1% on S0; power 52% on S2). The real series was not read.

**Change before reading it (v2, posted on the issue first, comment 6825466113):** only the S0 part of R1 is replaced, by a detection threshold z_crit(w) = the 95th percentile of z = rho_hat / SE on a fresh set S0A (300 new seeds), with a false-detection rate of at most 10% per window on a second fresh set S0B; R3b moves to S0B; all other thresholds and the S1/S2 results are unchanged. **Second verdict (`results_planted_534_v2.txt`): PASS.** z_crit 3.73, 2.48, 2.72 (D < 216, middle, D >= 228); false detections on S0B 2%, 7%, 3%; detection rates on S1B (rho 0.066) 39%, 93%, 70% and on S2 10%, 95%, 100%; Q critical value 7.91 (95th percentile on S1A), size 5% on S1B, 1% on S0B, power on S2 52% (just resolving). At the planted noise the 12-state window detects a ratio of 0.066 in only 39% of seeds.

Controls of the script (`control_guard_534.txt`): the `data` command refuses the v1 file (its VERDICT line says FAIL; exit 1), and a planted seed rerun reproduces its stored record.

## Results (`results_534.txt`, `results_534.json`; run after the v2 verdict)

Global chirp fits (the phase used): ln sigma_1 P0 2.616, p1 +0.0165, p2 +0.00031 (global rms 0.0060); ln sigma_2 P0 2.618, p1 +0.0178, p2 +0.00037 (0.0052), as in #533.

Phase of the p2 chirp (the main row):

| series | window | states | window rms | a1 | a2 | ratio rho +- SE | z (z_crit) | second harmonic | relative phase theta +- SE (rad) | bootstrap rho 16-50-84% |
|---|---|---|---|---|---|---|---|---|---|---|
| ln sigma_1 | D < 216 | 12 | 0.0018 | 0.1108 | 0.0079 | 0.072 +- 0.011 | 6.67 (3.73) | detected | +0.06 +- 0.14 | 0.062 0.073 0.083 |
| ln sigma_1 | 216 <= D < 228 | 23 | 0.0015 | 0.1097 | 0.0074 | 0.067 +- 0.005 | 14.49 (2.48) | detected | +0.02 +- 0.07 | 0.063 0.067 0.072 |
| ln sigma_1 | D >= 228 | 16 | 0.0011 | 0.1145 | 0.0069 | 0.060 +- 0.005 | 11.96 (2.72) | detected | -0.04 +- 0.08 | 0.055 0.060 0.066 |
| ln sigma_2 | D < 216 | 12 | 0.0009 | 0.1109 | 0.0073 | 0.066 +- 0.005 | 12.34 (3.73) | detected | -3.10 +- 0.08 | 0.060 0.066 0.071 |
| ln sigma_2 | 216 <= D < 228 | 23 | 0.0009 | 0.1111 | 0.0072 | 0.065 +- 0.003 | 24.03 (2.48) | detected | +3.05 +- 0.04 | 0.062 0.065 0.068 |
| ln sigma_2 | D >= 228 | 16 | 0.0006 | 0.1105 | 0.0072 | 0.065 +- 0.003 | 22.04 (2.72) | detected | -3.12 +- 0.04 | 0.063 0.065 0.068 |

**Do the windows agree within their errors? Yes, for both series.** Q = 1.59 for ln sigma_1 (inverse-variance mean ratio 0.065) and Q = 0.02 for ln sigma_2 (0.065), against the critical value 7.91 (5.73 when the test is calibrated at the data's own noise, post hoc below). The ratios fall slightly with D for ln sigma_1 (0.072, 0.067, 0.060), within their errors. The relative phase agrees across the windows to about 2 SE: ln sigma_1 is 0 within 0.14 (+0.06, +0.02, -0.04), ln sigma_2 is pi to about 2 SE (-3.10, +3.05, -3.12 are +3.18, +3.05, +3.16 modulo 2 pi, off pi by +0.04, -0.09, +0.02 against errors 0.08, 0.04, 0.04; the middle window is 2.2 SE away, and the largest pairwise difference between windows is 2.0 combined SE; this phase comparison is information, not a pre-registered rule). So the second harmonic is the same in all three windows: ratio about 0.065 (a2 about 0.0072 against a1 about 0.111), in phase with twice the first for ln sigma_1 and in antiphase for ln sigma_2.

Sensitivity, the phase of the p2 = 0 chirp (a cruder phase; window rms 0.0025 to 0.0034): ratios 0.070 +- 0.020 (not detected, z 3.56 against 3.73), 0.068 +- 0.008, 0.070 +- 0.012 for ln sigma_1 (Q 0.01) and 0.064 +- 0.015, 0.067 +- 0.008, 0.076 +- 0.016 for ln sigma_2 (Q 0.36), all detected for ln sigma_2; the agreement holds. Over all 51 states with a cubic trend (the cross-check with #525's by-product, 0.0074 against 0.112): a1 0.1113, a2 0.0075, ratio 0.067 +- 0.005 for ln sigma_1, and 0.1109, 0.0072, 0.065 +- 0.002 for ln sigma_2.

## Post hoc (not in the protocol, after the real series was read; `posthoc_534.py` -> `results_posthoc_534.txt`)

The windows' residual rms (0.0006 to 0.0018) is 3 to 10 times below the 0.006 that the planted test used as noise, because the residual of #522, #525 and #533 (0.005 to 0.006) is mostly the second harmonic itself: in each window, adding it takes the rms of the fit from 0.0047 to 0.0057 (first harmonic only) down to 0.0006 to 0.0018 (F test for the two added columns: p from 2.5e-13 to 3.2e-3).
Redoing the planted agreement test at noise 0.0015 (300 fresh seeds each): the Q critical value is 5.73 and the power on S2 (ratios 0.03, 0.066, 0.12) is 100%, so at the data's noise a change of that size would have been seen, and both observed Q (1.59 and 0.02) are below it.

## Caveats

- The phase is fixed from a global fit with one sinusoid; the sensitivity row shows how the ratio moves with a cruder phase (within the errors).
- Errors are white-noise errors (delta method, parametric bootstrap); the windows' residuals are small but not shown to be white.
- The planted test used noise 0.006, 3 to 10 times above the windows' own; its coverage, bias, detection thresholds and Q size are scale-free statements about the estimator, its power is not (hence the post hoc run).
- The first planted verdict failed and the rule was changed before the data were read, as above; the thresholds of the other rules were not touched.
