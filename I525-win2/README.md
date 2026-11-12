# I525-win2: the chirp's hold-out test, sigma_3 and sigma_4's residual structure, and twelve half-unit states below D 216

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/525 (follows from #522).
Part 3 (runs): `run_i525.sh`, one `anm_run.py` chain of twelve steps of a = -0.5 from crawlG D 216.1312 (`--h_max -0.5 --steps 12 --a_grow 1`, 16 threads, worktree `D:\choptuik-i446g` at main 14dc386, Python only, venv-t126), each new state followed by `near_null_eq.py --plant=7 --threads=2` (worktree `D:\choptuik-i505` at 0cce81e), then the control `--mutate=rows_only` at one state. Exit codes in `exits.txt`.
Parts 1 and 2 (analysis only, venv-t177) run beside it. Results follow in this README.

## Results

### Part 1, the hold-out (`holdout_525.py` -> `results_holdout_525.txt`; selftest `results_holdout_525_selftest.txt` ok)

The chirp of #522 (quadratic trend + one sinusoid, period P(D) = P0 + p1 (D - 228), P0 1.50 to 3.50 step 0.01, p1 -0.12 to 0.12 step 0.002) fitted to the 30 states with D <= 232.63 and used to predict the 9 states D 233.13 to 237.13. (a) is everything extrapolated, the acceptance; (b) extrapolates the oscillation only and refits the trend to all 39 states afterwards (it leaks the trend). The control is the same fit with p1 = 0.

| series | chirp P0, p1 (training) | in-sample rms | prediction rms (max) (a) | (b) | p1 = 0: P | in-sample rms | prediction rms (max) (a) | (b) |
|---|---|---|---|---|---|---|---|---|
| ln sigma_1 | 2.61, +0.014 | 0.0062 | 0.0222 (0.0472) | 0.0132 | 2.56 | 0.0131 | 0.0667 (0.1385) | 0.0528 |
| ln sigma_2 | 2.62, +0.016 | 0.0054 | 0.0152 (0.0245) | 0.0073 | 2.56 | 0.0140 | 0.0546 (0.1048) | 0.0525 |
| ln sigma_3 | 2.20, +0.006 | 0.0103 | 0.0765 (0.1290) | 0.0194 | 2.18 | 0.0117 | 0.0768 (0.1374) | 0.0346 |
| ln sigma_4 | 2.20, +0.006 | 0.0075 | 0.0564 (0.0991) | 0.0169 | 2.18 | 0.0112 | 0.0697 (0.1547) | 0.0370 |

Acceptance (the issue's, sigma_1 and sigma_2 at most 2 x 0.007 = 0.014): **fails** for both, 0.0222 and 0.0152. The control predicts 3 to 4 times worse (0.0667, 0.0546), so the drift is needed, as the issue's control reads. The limit is not met by the true model every time: in the planted selftest (a planted chirp P0 2.62, p1 +0.016, amplitude 0.11, noise 0.007, 200 seeds at the D of the data) the chirp's prediction rms has median 0.0107 and 90th percentile 0.0156, and 82% of seeds are at most 0.014, against 0.0565 median for the p1 = 0 control (0% at most 0.014). A parametric bootstrap with the training fit as the truth (500 trials, noise at its in-sample rms x sqrt(n / (n - 7))) puts the observed errors at the upper tail of what the true model gives:

| series | noise | observed | trials: median | trials: 90th percentile | share at or above the observed |
|---|---|---|---|---|---|
| ln sigma_1 | 0.0070 | 0.0222 | 0.0104 | 0.0160 | 1.0% |
| ln sigma_2 | 0.0062 | 0.0152 | 0.0092 | 0.0146 | 8.0% |
| ln sigma_3 | 0.0118 | 0.0765 | 0.0181 | 0.0287 | 0.0% |
| ln sigma_4 | 0.0086 | 0.0564 | 0.0133 | 0.0222 | 0.0% |

The oscillation alone extrapolates better than the whole (b: 0.0132, 0.0073 for sigma_1 and sigma_2), so the quadratic trend extrapolated over 4.5 units is part of the miss.

Follow-up with a cubic trend (`holdout_cubic_525.py` -> `results_holdout_cubic_525.txt`, selftest ok: a planted chirp with a cubic term, degree 3 median 0.0138 against 0.0818 for degree 2 and 0.0340 for the p1 = 0 control). It is not the acceptance, and the choice of the cubic came from the full 39 states, test states included (the training states alone prefer it clearly for sigma_3 and sigma_4, in-sample rms 0.0103 -> 0.0052 and 0.0075 -> 0.0057, and hardly for sigma_1 and sigma_2, 0.0062 -> 0.0058 and 0.0054 -> 0.0053):

| series | trend | chirp P0, p1 | in-sample rms | prediction rms (max) | p1 = 0 prediction rms (max) |
|---|---|---|---|---|---|
| ln sigma_1 | degree 3 | 2.61, +0.014 | 0.0058 | 0.0121 (0.0164) | 0.0718 (0.1494) |
| ln sigma_2 | degree 3 | 2.62, +0.016 | 0.0053 | 0.0082 (0.0127) | 0.0822 (0.1721) |
| ln sigma_3 | degree 3 | 2.20, +0.006 | 0.0052 | 0.0149 (0.0258) | 0.0310 (0.0473) |
| ln sigma_4 | degree 3 | 2.20, +0.006 | 0.0057 | 0.0100 (0.0185) | 0.0328 (0.0552) |

### Part 2, what is left in sigma_3 and sigma_4 (`residual_525.py` -> `results_residual_525.txt`, selftest `results_residual_525_selftest.txt` ok on four planted cases; `trend_525.py` -> `results_trend_525.txt`, selftest ok)

Fits on the 39 states, all with the chirp; 300 null trials of (the baseline fit + white noise), the scan of each extended model repeated in every trial, null fractions in the two noise conventions of #522 (the larger is quoted). M1 is an amplitude linear in D, M2h the chirp's second harmonic, M2s a second sinusoid of its own constant period (scanned 1.1 to 15).

| series | baseline rms | M1 | M2h | M2s (P2) | cubic trend | quartic trend |
|---|---|---|---|---|---|---|
| ln sigma_3 | 0.0172 | 0.0170 (null 73%) | 0.0155 (4.7%) | 0.0081 (0.0%), P2 15.00 | 0.0059 (0.0%) | 0.0059 (0.0%) |
| ln sigma_4 | 0.0135 | 0.0131 (51%) | 0.0128 (24%) | 0.0081 (0.3%), P2 15.00 | 0.0060 (0.0%) | 0.0059 (0.0%) |
| ln sigma_1 | 0.0068 | 0.0063 (19%) | 0.0043 (0.0%) | 0.0047 (0.3%), P2 1.30 | 0.0059 (0.7%) | 0.0058 (1.7%) |
| ln sigma_2 | 0.0061 | 0.0060 (64%) | 0.0032 (0.0%) | 0.0038 (0.3%), P2 1.30 | 0.0058 (8.7%) | 0.0058 (14.7%) |

Acceptance (residual at most 0.008 with a null fraction below 1%): no extension of the oscillation meets it for sigma_3 and sigma_4. M1 and M2h do not reduce the residual (M1 amplitudes change by -5% and +10% across the range). M2s reaches 0.0081 and 0.0081, just over the limit, and only with P2 = 15.00, the edge of its scan: a slow term and not a second oscillation. **A cubic trend meets it**: rms 0.0059 and 0.0060, null fractions 0.0%, with the chirp unchanged (P0 2.20, p1 +0.006) and the u^3 coefficient (u = (D - 228) / 10) -0.087 and -0.065; the quartic term adds nothing (+0.002, -0.009). So the leftover of sigma_3 and sigma_4 after the chirp is the quadratic trend's shortcoming, and the model that did not reach the limit is the oscillatory ones (M1, M2h, M2s).

By-products for sigma_1 and sigma_2 (not asked): their second harmonic is significant (M2h rms 0.0043 and 0.0032, null 0.0%, second-harmonic amplitude 0.0074 for both against first 0.112 and 0.110), the waveform is not a pure sinusoid at the 7% level; a cubic trend helps sigma_1 slightly (0.0068 -> 0.0059, null 0.7%) and sigma_2 not.
In the planted case T2 (an amplitude slope) M2s also reached 0.0069, so a second sinusoid of nearby period can imitate an amplitude change; here M1 did nothing, so that does not arise.

### Part 3, twelve half-unit states below D 216 (`run_i525.sh`, `exits.txt`, `down.log`, `down/`, `eq_D2*`; analysis `below216_525.py` -> `results_below216_525.txt`, selftest `results_below216_525_selftest.txt` ok)

One `anm_run.py` chain of twelve steps of a = -0.5 from crawlG D 216.1312 (`--h_max -0.5 --steps 12 --a_grow 1 --a_hold 1`, 16 threads, main 14dc386), 01:01:39 to 02:33:27 UTC. A first launch (00:59:52 to 01:00:52) was stopped by me with taskkill a minute in, before any step finished, to relaunch with a longer tool timeout; its leftovers are `aborted_launch1_*`. The negative step was accepted at its first attempt in every one of the twelve steps (no halving), a_max 3.40 to 3.42, the series 361 to 379 s, the corrector 46 to 49 s, the octo-double Newton in three steps to max|F| between 1.2e-91 and 1.5e-85, the state moved by 1.5e-36 to 1.9e-34 from the prediction. `near_null_eq.py --plant=7` (0cce81e) exited 0 at each of the twelve states, planted check 1.2e-14 to 2.6e-13 (bound 1e-3), ||J_eq v_1|| / sigma_1 = 1.000000. The control `--mutate=rows_only` at D 213.1312 exited 1 (planted check FAIL, as it must).

Cross-check of the chain itself: D 215.1312 reached by two steps of -0.5 down from crawlG D 216.1312 equals crawlB2's D 215.1312 (reached by +0.1 from I19-win2's D 215.0312) to 2.0e-20 relative, Delta differing by 8.5e-21 (`compare_215_525.py` -> `results_compare_215_525.txt`; the control against D 215.6312 differs by 1.3e-4 relative and exits 1). Delta of the twelve states runs smoothly from 1.691421678979 (D 215.63) to 1.692650500593 (D 210.13).

Equilibrated sigma_1..4:

| D | sigma_1 | sigma_2 | sigma_3 | sigma_4 |
|---|---|---|---|---|
| 215.6312 | 2.2879e-48 | 1.0640e-47 | 8.1342e-45 | 5.8313e-43 |
| 215.1312 | 3.6588e-48 | 1.7339e-47 | 1.5917e-44 | 8.1847e-43 |
| 214.6312 | 6.5825e-48 | 2.4860e-47 | 2.4223e-44 | 1.4586e-42 |
| 214.1312 | 1.1648e-47 | 3.6038e-47 | 3.4100e-44 | 2.7867e-42 |
| 213.6312 | 1.7013e-47 | 6.2737e-47 | 5.7393e-44 | 4.4073e-42 |
| 213.1312 | 2.4134e-47 | 1.1231e-46 | 1.1181e-43 | 6.0405e-42 |
| 212.6312 | 3.8338e-47 | 1.7695e-46 | 1.8154e-43 | 9.7779e-42 |
| 212.1312 | 6.8547e-47 | 2.4726e-46 | 2.4724e-43 | 1.8781e-41 |
| 211.6312 | 1.1759e-46 | 3.6044e-46 | 3.8883e-43 | 3.1136e-41 |
| 211.1312 | 1.6667e-46 | 6.3191e-46 | 7.3164e-43 | 4.2704e-41 |
| 210.6312 | 2.3577e-46 | 1.1002e-45 | 1.2671e-42 | 6.3037e-41 |
| 210.1312 | 3.7874e-46 | 1.6728e-45 | 1.7103e-42 | 1.1849e-40 |

**(A) The periods in the twelve new states alone** (D 210.13 to 215.63, trend + one sinusoid, period scanned from 1.1 to the D range over 1.5 in steps of 0.005, 1000-trial null test; the bracket is the spread of periods within one residual variance of the best, not a rigorous bound; "chirp" is the extrapolation P0 + p1 (212.8 - 228) of #522's 39-state fit with its quadratic trend, "low half" the D 216 to 227 period of #522):

| series | trend | period | amplitude | rms | null fraction | chirp | low half |
|---|---|---|---|---|---|---|---|
| sigma_1 | quadratic | 2.440 (2.425 to 2.455) | 0.111 +- 0.004 | 0.0059 | 0.0% | 2.377 | 2.525 |
| sigma_1 | line | 2.455 (2.425 to 2.490) | 0.119 +- 0.007 | 0.0139 | 0.0% | 2.377 | 2.525 |
| sigma_2 | quadratic | 2.425 (2.415 to 2.440) | 0.111 +- 0.003 | 0.0049 | 0.0% | 2.377 | 2.525 |
| sigma_2 | line | 2.400 (2.360 to 2.440) | 0.102 +- 0.008 | 0.0143 | 0.0% | 2.377 | 2.525 |
| sigma_3 | quadratic | 2.130 (2.125 to 2.140) | 0.131 +- 0.003 | 0.0050 | 0.0% | 2.139 | 2.165 |
| sigma_3 | line | 2.080 (2.055 to 2.100) | 0.127 +- 0.009 | 0.0165 | 0.0% | 2.139 | 2.165 |
| sigma_4 | quadratic | 2.140 (2.135 to 2.145) | 0.130 +- 0.003 | 0.0044 | 0.0% | 2.109 | 2.160 |
| sigma_4 | line | 2.180 (2.160 to 2.200) | 0.135 +- 0.008 | 0.0139 | 0.0% | 2.109 | 2.160 |

Acceptance (ln sigma_1, quadratic trend: within 0.1 of the chirp's 2.377 with the interval below 2.525 and null fraction below 1%): **passes**, 2.440 (2.425 to 2.455), null 0.0%. The period has kept shortening below D 216 (2.525 -> 2.440 for sigma_1, 2.165 -> 2.130 for sigma_3), as the chirp says. It is 0.063 above the linear chirp's extrapolation for sigma_1 and 0.048 for sigma_2 (0.031 for sigma_4, -0.009 for sigma_3), several times the fit intervals, so the drift is slowing towards low D and is not exactly linear: sigma_1's local period is 2.440 at D 212.8, 2.525 at D 221.6 and 2.715 at D 232.6 (D 228 to 237, #521), a slope of 0.0097 per unit of D below D 221.6 and 0.0173 above. The amplitudes stay at 0.111, 0.111, 0.131 and 0.130, as at D 216 and above. The planted selftest of the rule: a planted 2.38 meets it in 100% of 40 seeds, a planted 2.525 in 0%.

**(B) The chirp fitted to the 39 states D >= 216.13, extrapolated down to the twelve new states** ((a) is the pure extrapolation, (b) extrapolates the oscillation only and refits the trend to all 51 states):

| series | trend | chirp P0, p1 | prediction rms (a) | (b) | p1 = 0: prediction rms (a) | (b) |
|---|---|---|---|---|---|---|
| sigma_1 | degree 2 | 2.62, +0.016 | 0.0357 | 0.0230 | 0.0762 | 0.0699 |
| sigma_1 | degree 3 | 2.62, +0.016 | 0.0244 | 0.0231 | 0.0767 | 0.0705 |
| sigma_2 | degree 2 | 2.62, +0.016 | 0.0338 | 0.0221 | 0.0760 | 0.0722 |
| sigma_2 | degree 3 | 2.62, +0.016 | 0.0225 | 0.0213 | 0.0776 | 0.0714 |
| sigma_3 | degree 2 | 2.20, +0.004 | 0.1172 | 0.0227 | 0.1234 | 0.0457 |
| sigma_3 | degree 3 | 2.20, +0.006 | 0.0513 | 0.0145 | 0.0596 | 0.0446 |
| sigma_4 | degree 2 | 2.20, +0.006 | 0.1073 | 0.0221 | 0.1171 | 0.0496 |
| sigma_4 | degree 3 | 2.20, +0.006 | 0.0238 | 0.0157 | 0.0508 | 0.0420 |

The chirp extrapolates 2 to 3 times better than the constant period for sigma_1 and sigma_2 (and the oscillation alone, (b), 0.021 to 0.023 against 0.070 to 0.072), but not to the 0.014 of the hold-out limit, and the extrapolation here is over 6 units against 4.5 above.

**(C) The chirp refitted to all 51 states D 210.13 to 237.13:**

| series | trend | P0 (D 228) | p1 | period at D 213 | rms residual |
|---|---|---|---|---|---|
| sigma_1 | degree 2 | 2.62 | +0.014 | 2.410 | 0.0087 |
| sigma_1 | degree 3 | 2.62 | +0.014 | 2.410 | 0.0069 |
| sigma_2 | degree 2 | 2.62 | +0.014 | 2.410 | 0.0077 |
| sigma_2 | degree 3 | 2.62 | +0.014 | 2.410 | 0.0064 |
| sigma_3 | degree 2 | 2.20 | +0.004 | 2.140 | 0.0254 |
| sigma_3 | degree 3 | 2.20 | +0.006 | 2.110 | 0.0091 |
| sigma_4 | degree 2 | 2.20 | +0.006 | 2.110 | 0.0223 |
| sigma_4 | degree 3 | 2.20 | +0.004 | 2.140 | 0.0085 |

One linear-drift chirp with a cubic trend describes ln sigma_1 and ln sigma_2 over D 210 to 237 to 0.0069 and 0.0064, and ln sigma_3 and ln sigma_4 to 0.0091 and 0.0085 (above the 0.006 of the 39 states, so the cubic trend and the linear drift are stretched over the longer range).

### Summary of #525's three acceptances

| part | acceptance | result |
|---|---|---|
| 1 hold-out | sigma_1, sigma_2 prediction rms at most 0.014, p1 = 0 control reported | **fails**: 0.0222, 0.0152; the control 0.0667, 0.0546 is 3 to 4 times worse; with a cubic trend (a follow-up, not the acceptance) 0.0121, 0.0082 |
| 2 residual of sigma_3, sigma_4 | residual at most 0.008 with null below 1%, or name the model that did not | **a cubic trend meets it** (0.0059, 0.0060, null 0.0%); an amplitude slope, a second harmonic and a second sinusoid (P2 at the scan edge) do not (0.0170 / 0.0131, 0.0155 / 0.0128, 0.0081 / 0.0081) |
| 3 states below D 216 | sigma_1's period within 0.1 of 2.38, excluding 2.525 | **passes**: 2.440 (2.425 to 2.455), null 0.0%; all twelve negative steps accepted, no refusal |

Software: numpy and mpmath in venv-t177 (analysis, compare); venv-t126 with its hpkernel build (the runs).
