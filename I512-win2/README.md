# I512-win2: the spread of ln|det M| at D 30 over rounding realisations

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, AVX2), issue https://github.com/nmoinvaz/choptuik-large-d/issues/512 (after #509), the harness of #485 and #509: worktree `D:\choptuik-bisect2` at e043be2 (today's tree), venv `venv-bisect2`.
Check points as in #509 (October's D 30.0688 M 48 state, lambda = 4.267 + 0.974 i and 3.94364216362105 + 1.1900607986722187 i).

## Method

`patch_shiftnoise.py` (effective diff `shiftnoise_on_e043be2.patch`) adds to `dtau_c` of today's `modecount_cx`: `set_shift_noise(rel, seed)`, which adds hi x rel x u to the lo part of every element of the shift's output (re and im, 8 lanes), u uniform in [-1, 1) from a hash of the seed and the bits of the element's inputs (so it does not depend on thread scheduling and differs for every seed), and `set_shift_old(flag)`, the shift in its old `DotAcc` form. Defaults change nothing.
`shift_noise.py` (log `shift_noise.log`, values `shift_noise.json`): per point the baseline (today's value), control A (rel 0 with a seed gives the baseline to the bit), control B (the old form, the fixed known change, must give #509's first-order prediction to 1e-3), then seeds 1..30 at rel 1e-30, and a linearity check.
`shift_noise_scan.py` (`shift_noise_scan.log`, `.json`): seeds 1..10 at rel 1e-34, 1e-32, 1e-31, 1e-29, 1e-28, 1e-26, 1e-24.

## Results (2026-11-11 21:26 to 21:57 UTC)

Control A: passed at both points (baseline -940.4586634376807 and -965.1149263918375, today's; rel 0 with seed 17 the same).
Control B: the old form changes ln|det| by -8.108600e-09 (prediction -8.108163e-09, ratio 1.000054) and +1.670060e-08 (prediction +1.670138e-08, ratio 0.999953): passed.

The 30 values at rel 1e-30, change of ln|det| from the baseline (seeds 1 to 30):
point 1: -1.740e-08 -4.185e-08 +6.045e-08 +9.191e-08 +4.049e-08 -3.640e-08 +3.669e-08 +5.540e-08 -3.087e-08 +1.098e-08 -7.243e-09 +2.134e-08 -5.501e-09 +7.055e-09 +2.976e-08 +1.831e-08 +3.507e-08 +4.573e-08 +6.763e-08 +4.852e-08 +2.897e-08 -1.970e-08 -3.849e-08 +6.028e-08 +3.543e-08 +3.770e-08 -1.519e-08 +3.667e-08 -1.578e-08 -6.315e-10
point 2: +2.310e-08 +1.884e-08 +1.896e-08 +2.523e-08 +3.360e-08 +1.053e-08 +4.307e-09 +3.268e-08 +3.174e-08 +4.498e-08 +1.700e-08 +2.107e-08 +3.198e-08 +3.235e-08 +6.473e-09 +1.776e-09 +5.600e-08 +1.233e-08 +1.089e-08 +5.705e-08 +7.310e-09 +1.003e-08 +4.118e-08 +7.034e-09 +1.954e-08 +3.361e-08 +1.445e-09 +2.666e-08 -3.239e-09 +2.585e-08

| | point 1 | point 2 |
|---|---|---|
| mean | +1.798e-08 (standard error 6.4e-09) | +2.201e-08 (2.8e-09) |
| sample standard deviation | 3.514e-08 | 1.556e-08 |
| min, max | -4.185e-08, +9.191e-08 | -3.239e-09, +5.705e-08 |
| range | 1.338e-07 | 6.029e-08 |
| the old form's change (#509) | -8.1e-09 | +1.67e-08 |

Spread against the size of the change (seeds 1..10 per rel, sample std of the change of ln|det|):

| rel | point 1 | point 2 |
|---|---|---|
| 1e-34 | 2.1e-09 | 1.6e-09 |
| 1e-32 | 3.16e-08 | 1.44e-08 |
| 1e-31 | 1.89e-08 | 1.17e-08 |
| 1e-30 (30 seeds) | 3.51e-08 | 1.56e-08 |
| 1e-29 | 8.30e-08 | 1.03e-07 |
| 1e-28 | 7.80e-07 | 9.54e-07 |
| 1e-26 | 7.96e-05 | 9.56e-05 |
| 1e-24 | 7.97e-03 | 9.56e-03 |

Above rel 1e-29 the std is proportional to rel (std / rel = 7.8e21 to 8.3e21 at point 1, 9.5e21 to 10.3e21 at point 2; the same seed at 1e-24 and 1e-26 gives a ratio of 100.005 +- 0.5 and 100.08 +- 0.8 over the ten seeds): the first-order regime, in which the change is the random-sign sum of the 8e21-per-unit sensitivity. Below rel 1e-30 the spread stops following rel and sits at 1.2e-08 to 3.2e-08: the floor set by the roundings downstream, which a perturbation of any size re-rolls.

## Checks that failed, reported

1. `shift_noise.py`'s linearity check (the change at rel 1e-29 over the change at rel 1e-30 for the same seeds must be 10 +- 20%) failed: 7.17, 1.02, 0.86, 1.03, -3.96 at point 1. The premise was wrong: at 1e-30 the first-order term (8e21 x 1e-30 = 8e-09) is below the rounding floor (about 3e-08), so the response is not linear there. The scan replaces it: the same-seed ratio between 1e-24 and 1e-26 is 100.
2. `shift_noise_scan.py`'s control (rel 1e-34 changes nothing) failed: the std is 2.1e-09 and 1.6e-09. Also a wrong premise: the added hi x 1e-34 is representable when the element's lo part is small, so it changes the element and re-rolls the roundings downstream. The scan reports it as FAILED; the reading of the 1e-34 row is "a perturbation four orders below the double-double precision still gives a spread of 2e-09".
Both are in the logs (`controls: FAILED`, `control (rel 1e-34 changes nothing): FAILED`).
