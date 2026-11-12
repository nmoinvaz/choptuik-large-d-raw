# I535-win2: twelve half-unit states below D 210 to test the period model

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/535 (follows from #525 and #533).
`run_i535.sh`: one `anm_run.py` chain of twelve steps of a = -0.5 from `I525-win2/down/anm_pin3_D210.1312.npz` (the last state of #525) to D 204.1312 (`--h_max -0.5 --steps 12 --a_grow 1 --a_hold 1`, 16 threads, worktree `D:\choptuik-i446g` at main 14dc386, Python only, venv-t126), each new state followed by `near_null_eq.py --plant=7 --threads=2` (worktree `D:\choptuik-i505` at 0cce81e), then the control `--mutate=rows_only` at D 207.1312. Exit codes in `exits.txt`.
Prediction under test, written on #533 before this run (comment 6813036441): the period of ln sigma_1 over D 204 to 209.6 is 2.404, bootstrap sd 0.021, to be within 0.1. Results follow in this README.

## Results (chain 2026-11-12 03:08:51 to 04:48:06 UTC, control to 04:52:05; analysis 04:53 to 04:58)

**The chain.** Twelve steps of a = -0.5 from `I525-win2/down/anm_pin3_D210.1312.npz` down to D 204.1312 (`run_i535.sh`, `down.log`, `down/`), every step accepted at its first attempt, none refused: a_max 3.406 to 3.414, the series 371 to 416 s, the corrector 47 to 51 s, the octo-double Newton in three steps to max|F| between 3.3e-92 and 2.0e-85, the state moved by 1.2e-35 to 6.2e-33 from the prediction. 8.3 min a step including the series, with #543 to #554 sharing the machine. Delta runs smoothly from 1.692765370940 (D 209.63) to 1.694065631517 (D 204.13). `near_null_eq.py --plant=7` (0cce81e) exited 0 at each of the twelve states, planted column scaling recovered to 6.1e-15 to 3.6e-13 (bound 1e-3), ||J_eq v_1|| / sigma_1 = 1.000000. The control `--mutate=rows_only` at D 207.1312 exited 1 (planted check FAIL), as it must.

Equilibrated sigma_1..4:

| D | sigma_1 | sigma_2 | sigma_3 | sigma_4 |
|---|---|---|---|---|
| 209.6312 | 6.7518e-46 | 2.2830e-45 | 2.5165e-42 | 2.0373e-40 |
| 209.1312 | 1.1009e-45 | 3.3792e-45 | 4.5147e-42 | 2.8537e-40 |
| 208.6312 | 1.5100e-45 | 5.9547e-45 | 8.2398e-42 | 3.9488e-40 |
| 208.1312 | 2.1388e-45 | 1.0012e-44 | 1.1411e-41 | 7.1087e-40 |
| 207.6312 | 3.4827e-45 | 1.4615e-44 | 1.5848e-41 | 1.2636e-39 |
| 207.1312 | 6.1320e-45 | 1.9541e-44 | 2.6670e-41 | 1.8180e-39 |
| 206.6312 | 9.4622e-45 | 2.9811e-44 | 4.9222e-41 | 2.3752e-39 |
| 206.1312 | 1.2618e-44 | 5.2163e-44 | 7.0873e-41 | 3.9472e-39 |
| 205.6312 | 1.8193e-44 | 8.4188e-44 | 9.3822e-41 | 7.1545e-39 |
| 205.1312 | 3.0143e-44 | 1.1769e-43 | 1.4967e-40 | 1.0765e-38 |
| 204.6312 | 5.2062e-44 | 1.5680e-43 | 2.7667e-40 | 1.3943e-38 |
| 204.1312 | 7.5096e-44 | 2.4887e-43 | 4.2618e-40 | 2.1599e-38 |

**(A) The periods in the twelve new states alone** (D 204.13 to 209.63, trend + one sinusoid, period scanned from 1.1, 1000-trial null test; the bracket is the spread of periods within one residual variance of the best, not a rigorous bound; `period_535.py` -> `results_period_535.txt`, selftest ok: a planted 2.404 passes the within-0.1 rule in 100% of 40 seeds, a planted 2.56 in 0%, a planted 2.334 also in 100%, so the rule cannot separate those two):

| series | trend | period | amplitude | rms | null fraction | #533's prediction | difference | distance to the linear drift / the constant period |
|---|---|---|---|---|---|---|---|---|
| sigma_1 | quadratic | 2.380 (2.370 to 2.395) | 0.111 +- 0.003 | 0.0046 | 0.0% | 2.404 | -0.024 | 0.046 / 0.180 |
| sigma_1 | line | 2.350 (2.320 to 2.385) | 0.103 +- 0.007 | 0.0129 | 0.0% | 2.404 | -0.054 | 0.016 / 0.210 |
| sigma_2 | quadratic | 2.385 (2.375 to 2.400) | 0.112 +- 0.003 | 0.0053 | 0.0% | 2.408 | -0.023 | 0.061 / 0.175 |
| sigma_2 | line | 2.410 (2.380 to 2.435) | 0.120 +- 0.007 | 0.0131 | 0.0% | 2.408 | +0.002 | 0.086 / 0.150 |
| sigma_3 | quadratic | 2.110 (2.095 to 2.120) | 0.131 +- 0.004 | 0.0073 | 0.0% | 2.103 | +0.007 | 0.018 / 0.070 |
| sigma_4 | quadratic | 2.120 (2.105 to 2.135) | 0.127 +- 0.005 | 0.0080 | 0.0% | 2.139 | -0.019 | 0.023 / 0.060 |

Acceptance (ln sigma_1, quadratic trend, within 0.1 of 2.404, null fraction below 1%): **passes**, 2.380 (2.370 to 2.395), null 0.0%, 0.024 below the prediction. The amplitudes are unchanged (0.111, 0.112, 0.131, 0.127). How much the one number says about the three models: the same local fit run on planted data in this layout (`bias_535.py` -> `results_bias_535.txt`, 200 seeds of noise 0.006) reads a planted period without bias and with sd 0.014, so the measured 2.380 is 1.7 sd below the p2 chirp's 2.404, 3.5 sd above the linear drift's 2.334 and 12.6 sd below the constant period's 2.560, for white noise only; with the line trend the fit reads 2.350, which is nearer the linear drift (0.016) than the p2 chirp (0.054). The local period alone favours the p2 chirp over the linear drift without deciding it; (B) decides more.

**(B) #533's model (cubic trend, fitted to the 51 states D >= 210.13) predicting the twelve new states, the whole of ln sigma, not only the period:**

| series | p2 chirp rms (max) | p2 = 0 chirp rms (max) | p1 = p2 = 0 rms (max) |
|---|---|---|---|
| sigma_1 | 0.0152 (0.0327) | 0.0239 (0.0611) | 0.0890 (0.1568) |
| sigma_2 | 0.0082 (0.0142) | 0.0258 (0.0527) | 0.0892 (0.1477) |
| sigma_3 | 0.0565 (0.0989) | 0.0588 (0.1106) | 0.0594 (0.1130) |
| sigma_4 | 0.0388 (0.0712) | 0.0352 (0.0686) | 0.0825 (0.1752) |

For sigma_1 and sigma_2 the p2 chirp predicts the new states 1.6 and 3.1 times better than the linear drift and 5.9 and 10.9 times better than the constant period: sigma_2 at 0.0082 meets the 0.014 of #525 and #533, sigma_1 at 0.0152 misses it by 9%. sigma_3 and sigma_4 are not predicted (0.057, 0.039), as in #533's hold-outs, which pointed at the polynomial trend.

**(C) The p2 chirp refitted to all 63 states D 204.13 to 237.13 (cubic trend):**

| series | p2 = 0: P0, p1 | rms | free: P0, p1, p2 | rms | period at D 206.8 / 228 / 237 | null fraction (i) / (ii) |
|---|---|---|---|---|---|---|
| sigma_1 | 2.615, +0.0121 | 0.0074 | 2.617, +0.0161, +0.00025 | 0.0059 | 2.389 / 2.617 / 2.782 | 0.0% / 0.0% |
| sigma_2 | 2.616, +0.0123 | 0.0075 | 2.619, +0.0171, +0.00030 | 0.0053 | 2.392 / 2.619 / 2.797 | 0.0% / 0.0% |
| sigma_3 | 2.197, +0.0042 | 0.0101 | 2.197, +0.0059, +0.00011 | 0.0096 | 2.121 / 2.197 / 2.259 | not run |
| sigma_4 | 2.198, +0.0043 | 0.0082 | 2.198, +0.0061, +0.00012 | 0.0075 | 2.121 / 2.198 / 2.263 | not run |

With the twelve states added, p2 for sigma_1 and sigma_2 moves from +0.00031 and +0.00037 to +0.00025 and +0.00030, stays at null 0.0%, and the residual stays at 0.0059 and 0.0053 over 63 states (0.0060 and 0.0052 over 51). The period at D 206.8 is 2.389 and 2.392, against the prediction 2.404 and 2.408.

### Summary of #535's acceptances

| acceptance | result |
|---|---|
| the measured sigma_1 period within 0.1 of the prediction written before the run | **passes**: 2.380 against 2.404 (-0.024), null 0.0% |
| all twelve steps accepted, or the first refusal reported | **all twelve accepted** at their first attempt |
| the planted check passes on each state, the rows_only control fails once | **passes** at all twelve (6.1e-15 to 3.6e-13, bound 1e-3), control exits 1 |
