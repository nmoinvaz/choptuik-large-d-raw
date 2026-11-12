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
