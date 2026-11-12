# I602-win: where ln sigma_1's H2 hold-out miss of #601 comes from, the trend's degree against the waveform (analysis only)

Machine win (Surface Laptop 4, i7-1185G7), issue https://github.com/nmoinvaz/choptuik-large-d/issues/602 (recommended by win in #601; the coordinator's message `choptuik-large-d/2026-11-12/142212Z-coordinator-b298.md`). Analysis only, one thread, venv-t151 (numpy 2.2.6, scipy 1.15.3, Python 3.10). `trend_degree_602.py` imports `holdout2_601.py` (a copy of I601-win's, in this folder) and #533's code from an up-to-date raw worktree (`I533-win2/period_p2_533.py` and its siblings); nothing is copied from it. Run from this folder without `-I` (the copy must be importable): `python trend_degree_602.py --raw=<raw worktree> planted --scenario=T0|T1 --seeds=100`, `summarize FILES`, `data --verdict=results_planted_602_v1.txt`.

## Method

Ln sigma_1 (ln sigma_2 as information), #601's two-harmonic chirp (period P0 + p1 x + p2 x^2, x = D - 228, waveform A1 cos phi + B1 sin phi + A2 cos 2 phi + B2 sin 2 phi) with a polynomial trend of degree d = 2, 3, 4 in u = (D - 228) / 10, and #601's hold-outs: H1 fits D <= 232.7 (42 states) and predicts D 233.13 to 237.13 (9); H2 fits D >= 214 (43) and predicts D 210.13 to 213.63 (8). Variant (a): the whole fit (trend and oscillation) from the training states extrapolated. Variant (b): the oscillation alone extrapolated from the training fit, with the trend (degree d) refitted to all 51 states of (y - oscillation) afterwards (it leaks the trend: it says how much of the miss is the trend's). Diagnostic R: the residual rms of the 2-harmonic cubic fit to all 51 states over D < 214 divided by that over D >= 214 (a low-D excess the model does not carry).

## Planted truth first (the whole pipeline, 100 seeds per scenario, noise 0.003, fixed on the issue before the real series was read: comment 6826350097)

a1 0.11, rho 0.065, theta 0, phi from P0 2.62, p1 +0.0165, p2 +0.0003, trend 0.3 - 1.1 u + 0.15 u^2 - 0.09 u^3. T0: that trend alone (control). T1: that trend plus g(D) = 0.05 exp(-(D - 210) / 3), structure at the low-D end (0.050 at D 210, 0.013 at D 214, not a polynomial). The amplitude 0.05 was chosen on planted data only (8 seeds at 0.03, 0.06, 0.10, 0.15) so that the cubic variant (a) misses H2 by about #601's observed 0.0146; an earlier draft used 0.03 and a mean-residual diagnostic, both dropped on those planted runs before the rules were posted.

**Verdict (`results_planted_602_v1.txt`): PASS, all six rules.** C1 (T0): (a) cubic meets 0.014 in 97% (H1) and 100% (H2) of seeds, (b) cubic in 100% and 100%. S1 (T1): the median H2 rms of (a) cubic is 0.0153 (in [0.012, 0.017]). S2: (a) cubic H2 exceeds 0.014 in 65% of seeds (at least 35%). S3: the median H2 rms of (b) cubic is 0.0051, 66% below (a)'s. S4: 47% of the T1 seeds have R above T0's 90th percentile (1.30; medians T0 0.87, T1 1.26), at least 40%. S5: median rho_hat 0.066. Medians of the rms in the table below the results. Control of the script (`control_guard_602.txt`): the `data` command refuses a verdict file that does not say PASS (exit 1).

| scenario | degree | (a) H1 share <= 0.014 (median) | (a) H2 | (b) H1 | (b) H2 |
|---|---|---|---|---|---|
| T0 | 3 | 97% (0.0061) | 100% (0.0054) | 100% (0.0040) | 100% (0.0041) |
| T0 | 4 | 76% (0.0095) | 86% (0.0074) | 99% (0.0038) | 100% (0.0040) |
| T1 | 3 | 32% (0.0162) | 35% (0.0153) | 100% (0.0046) | 100% (0.0051) |
| T1 | 4 | 50% (0.0140) | 72% (0.0106) | 100% (0.0039) | 100% (0.0037) |

(Degree 2 fails every cell in both scenarios, as the planted trend is cubic: (a) 0.16 to 0.19, (b) 0.05 to 0.06.)

## Results on the real series (`results_602.txt`, `results_602.json`; run after the verdict)

The 2-harmonic cubic fit over all 51 states: ln sigma_1 P0 2.616, p1 +0.0160, p2 +0.00027, rho 0.068, rms 0.0027.

**ln sigma_1** (rms (max) of the prediction error; the bound is 0.014):

| trend degree | (a) H1 | (a) H2 | (a) both <= 0.014 | (b) H1 | (b) H2 | (b) both <= 0.014 |
|---|---|---|---|---|---|---|
| 2 | 0.0282 (0.0433) | 0.0170 (0.0253) | no | 0.0091 (0.0165) | 0.0072 (0.0121) | yes |
| 3 | 0.0094 (0.0157) | **0.0146** (0.0242) | no | 0.0040 (0.0063) | 0.0048 (0.0088) | yes |
| 4 | 0.0141 (0.0297) | 0.0280 (0.0432) | no | 0.0044 (0.0066) | 0.0024 (0.0050) | yes |

**Variants for which H2 and H1 are both at most 0.014: for (a) none; for (b) all three degrees (2, 3, 4).** Variant (a) is nearest at degree 3 (H1 0.0094, H2 0.0146); degree 2 misses both (0.0282, 0.0170), degree 4 misses H2 widely (0.0280) and H1 by 0.0001 (0.0141).

**The pre-registered statement: (b) cubic meets H2 (0.0048) while (a) cubic does not (0.0146): the trend's extrapolation is the cause of the miss, not the oscillation.** Once the trend is refitted to all 51 states, the oscillation extrapolated from the training fit (chirp and two harmonics) predicts both hold-outs to 0.0024 to 0.0091 at every degree.

The diagnostic R of the real fit is 0.89, below T0's 90th percentile 1.30: no low-D excess is flagged in the residuals (E, the mean residual over D < 213, is -0.0021).

**Post hoc, after the data were read (outside the protocol): where the real values sit in the planted distributions.** The observed (a) cubic H2 0.0146 is reached or exceeded in 58% of the T1 seeds (median 0.0153) and in 0% of the T0 seeds (median 0.0054, maximum below it); the observed (b) cubic H2 0.0048 is typical of both (36% of T0, 66% of T1). So the size of the miss is that of a planted trend problem and not of noise. But the residual profile is not that of T1: R = 0.89 or lower occurs in 6% of the T1 seeds and in 54% of the T0 seeds, so the real fit's residuals do not carry a localized low-D excess like the planted exponential (the diagnostic has only 47% power on T1, so this argues against that shape, not against every trend problem). Together: the trend polynomial trained on part of the range extrapolates badly, at every degree, while the full-range trend is well described by a quadratic or cubic.

**ln sigma_2 (information, not asked):** 2-harmonic cubic fit rms 0.0011, R 0.79, no excess flagged. (a): degree 2 fails (0.0242, 0.0199), degree 3 meets both (0.0027, 0.0070), degree 4 meets both at the edge (0.0134, 0.0122); (b): all three degrees meet both (0.0066/0.0076, 0.0025/0.0046, 0.0035/0.0031).

## Caveats

- Variant (b) is not a prediction: it uses the test states to fix the trend. It shows that the oscillation is not the cause; it does not give a trend form that extrapolates.
- The planted structure is one shape (an exponential rise to D 210); the diagnostic R detects it in 47% of seeds. The real cause is established as the trend's extrapolation, not its shape.
- Planted noise 0.003, as in #601 (ln sigma_1's own global 2-harmonic rms is 0.0027).
- A degree of the trend from 2 to 4 only; no non-polynomial trend was tried.
