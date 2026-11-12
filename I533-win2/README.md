# I533-win2: a nonlinear period drift for sigma_1 and sigma_2 over D 210 to 237, with both hold-outs

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/533 (follows from #525). Analysis only, one thread, venv-t177.
`period_p2_533.py`: the chirp with P(D) = P0 + p1 x + p2 x^2 (x = D - 228) and a cubic trend on the 51 states D 210.13 to 237.13 of #505 to #525, planted truth first (`results_selftest_533.txt`), the null test of p2, the residual, both hold-outs with the p1 = p2 = 0 control, and the prediction of sigma_1's period over D 204 to 209.6 for #535. Results follow in this README.

## Results (2026-11-12 02:50 to 02:57 UTC)

Planted truth first (`results_selftest_533.txt`, 300 null trials per case): a planted p2 = +0.0004 (P0 2.63, p1 +0.0185, amplitude 0.11, cubic trend, noise 0.006) is recovered as +0.00040 with rms 0.0047 and null fraction 0.0% in both conventions; a planted p2 = 0 (P0 2.60, p1 +0.014) gives +0.00008 with null fractions 40.3% and 32.3%, not claimed. Selftest ok.

The data: the 51 equilibrated states D 210.13 to 237.13 (the 39 of #522 and the 12 of #525). The chirp phase is 2 pi times the integral of 1 / P(D), P(D) = P0 + p1 x + p2 x^2, x = D - 228; the linear parameters by least squares, (P0, p1, p2) by Nelder-Mead from the grid best of the p2 = 0 chirp and from p2 = +-0.0005. Null fraction: 500 trials of (the p2 = 0 fit + white noise), the whole fit repeated in each, at the noise of (i) the free fit's residual rms and (ii) the p2 = 0 fit's.

**Fits to the 51 states, cubic trend** (`period_p2_533.py` -> `results_533.txt`):

| series | p2 = 0: P0, p1 | rms | free: P0, p1, p2 | rms | period at D 213 / 228 / 237 | null fraction (i) / (ii) |
|---|---|---|---|---|---|---|
| ln sigma_1 | 2.620, +0.0135 | 0.0066 | 2.616, +0.0165, +0.00031 | 0.0060 | 2.437 / 2.616 / 2.789 | 0.0% / 0.2% |
| ln sigma_2 | 2.622, +0.0141 | 0.0063 | 2.618, +0.0178, +0.00037 | 0.0052 | 2.435 / 2.618 / 2.807 | 0.0% / 0.0% |
| ln sigma_3 | 2.199, +0.0051 | 0.0078 | 2.199, +0.0056, +0.00005 | 0.0078 | 2.126 / 2.199 / 2.253 | not run |
| ln sigma_4 | 2.199, +0.0048 | 0.0068 | 2.196, +0.0066, +0.00019 | 0.0062 | 2.139 / 2.196 / 2.271 | not run |

p2 is significant for sigma_1 and sigma_2 and the residual with it is 0.0060 and 0.0052, below the 0.0065 asked. For sigma_3 it is not needed (rms unchanged), for sigma_4 it helps a little (0.0068 -> 0.0062). With the quadratic trend (also in `results_533.txt`) the residual stays at 0.0077 and 0.0071 for sigma_1 and sigma_2 and 0.025 and 0.022 for sigma_3 and sigma_4.

**Hold-outs, cubic trend.** H1 fits D <= 232.7 (42 states) and predicts the 9 states D 233.13 to 237.13; H2 fits D >= 214 (43 states) and predicts the 8 states D 210.13 to 213.63. Prediction rms (max); the controls are the p2 = 0 chirp and the constant period (p1 = p2 = 0):

| series | hold-out | p2 chirp | p2 = 0 chirp | p1 = p2 = 0 | meets 0.014 |
|---|---|---|---|---|---|
| ln sigma_1 | H1 | 0.0079 (0.0162) | 0.0177 (0.0398) | 0.0891 (0.1741) | yes |
| ln sigma_1 | H2 | **0.0173** (0.0300) | 0.0208 (0.0428) | 0.1046 (0.1831) | **no** |
| ln sigma_2 | H1 | 0.0082 (0.0134) | 0.0157 (0.0314) | 0.0966 (0.1854) | yes |
| ln sigma_2 | H2 | 0.0119 (0.0198) | 0.0137 (0.0197) | 0.0943 (0.1632) | yes |
| ln sigma_3 | H1 | 0.0308 (0.0536) | 0.0306 (0.0524) | 0.0625 (0.1234) | no |
| ln sigma_3 | H2 | 0.0404 (0.0649) | 0.0406 (0.0671) | 0.0552 (0.1206) | no |
| ln sigma_4 | H1 | 0.0167 (0.0251) | 0.0192 (0.0435) | 0.0614 (0.1191) | no |
| ln sigma_4 | H2 | 0.0201 (0.0358) | 0.0235 (0.0436) | 0.0564 (0.1074) | no |

Acceptance for sigma_1 and sigma_2, both hold-outs at most 0.014: **fails**, on sigma_1's H2 (0.0173). The three other entries meet it (0.0079, 0.0082, 0.0119), and p2 improves on the p2 = 0 chirp in each of the four cases (0.0177 -> 0.0079, 0.0157 -> 0.0082, 0.0208 -> 0.0173, 0.0137 -> 0.0119). The constant period is 6 to 12 times worse for sigma_1 and sigma_2 and 1.4 to 3.7 times worse for sigma_3 and sigma_4.

**Follow-up, a quartic trend** (`quartic_533.py` -> `results_quartic_533.txt`, not an acceptance): the 51-state residuals fall to 0.0059, 0.0052, 0.0061, 0.0057 for sigma_1..4, but the hold-outs do not follow: sigma_2 (0.0085, 0.0120) and sigma_4 (0.0068, 0.0107) meet 0.014 in both, sigma_1 (0.0230, 0.0407) and sigma_3 (0.0430, 0.0259) miss by more than with the cubic trend. The polynomial trend extrapolated over 4.5 to 6 units is what limits the hold-outs, and which degree extrapolates well differs by series.

**Prediction for #535** (the period over D 204 to 209.6, its centre D 206.8, from the cubic-trend fit to all 51 states; the spread is a parametric bootstrap of 200 trials with the free fit as the truth and white noise at its rms, which counts the noise and not the model):

| series | p2 chirp | bootstrap sd | p2 = 0 chirp | p1 = p2 = 0 |
|---|---|---|---|---|
| ln sigma_1 | 2.404 | 0.021 | 2.334 | 2.560 |
| ln sigma_2 | 2.408 | 0.019 | 2.324 | 2.560 |
| ln sigma_3 | 2.103 | 0.019 | 2.092 | 2.180 |
| ln sigma_4 | 2.139 | 0.015 | 2.097 | 2.180 |
