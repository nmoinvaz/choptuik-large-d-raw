# I558-win2: twelve half-unit states below D 204 with a tighter pre-registered period bound

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/558 (follows from #535).
`run_i558.sh`: one `anm_run.py` chain of twelve steps of a = -0.5 from `I535-win2/down/anm_pin3_D204.1312.npz` (the last state of #535) to D 198.1312 (`--h_max -0.5 --steps 12 --a_grow 1 --a_hold 1`, 16 threads, worktree `D:\choptuik-i446g` at main 14dc386, Python only, venv-t126), each new state followed by `near_null_eq.py --plant=7 --threads=2` (worktree `D:\choptuik-i505` at 0cce81e), then the control `--mutate=rows_only` at D 201.1312. Exit codes in `exits.txt`.
Prediction under test, written on #558 before this run (comment 6815437477): the period of ln sigma_1 over D 198 to 203.6 is 2.365 (bootstrap sd 0.014; the linear drift 2.288, the constant period 2.520), to be within 0.05. Results follow in this README.

## Results (chain 2026-11-12 05:39:41 to 07:19:04 UTC, control to 07:23:22; analysis 07:23 to 07:30)

**The chain.** Twelve steps of a = -0.5 from `I535-win2/down/anm_pin3_D204.1312.npz` down to D 198.1312 (`run_i558.sh`, `down.log`, `down/`), every step accepted at its first attempt, none refused: a_max 3.407 to 3.413, the series 373 to 454 s, the corrector 46 to 52 s, the octo-double Newton in three steps to max|F| between 1.5e-95 and 3.0e-86, the state moved by 6.0e-36 to 7.7e-34 from the prediction. 8.3 min a step including the series, with #558 to #572 and the analyses sharing the machine. Delta runs smoothly from 1.694187277376 (D 203.63) to 1.695565395434 (D 198.13). `near_null_eq.py --plant=7` (0cce81e) exited 0 at each of the twelve states, planted column scaling recovered to 1.6e-14 to 3.8e-12 (bound 1e-3). The control `--mutate=rows_only` at D 201.1312 exited 1 (planted check FAIL), as it must. (The first lines of `run_i558.sh` still carry comments copied from #535's script that name D 213.1312 and #525; the command lines are right.)

Equilibrated sigma_1..4:

| D | sigma_1 | sigma_2 | sigma_3 | sigma_4 |
|---|---|---|---|---|
| 203.6312 | 9.9154e-44 | 4.2884e-43 | 5.4956e-40 | 3.9513e-38 |
| 203.1312 | 1.4594e-43 | 6.5819e-43 | 8.2035e-40 | 6.1523e-38 |
| 202.6312 | 2.4579e-43 | 8.8081e-43 | 1.4633e-39 | 7.9080e-38 |
| 202.1312 | 4.0748e-43 | 1.1890e-42 | 2.3617e-39 | 1.1105e-37 |
| 201.6312 | 5.5210e-43 | 1.9544e-42 | 2.9915e-39 | 1.9867e-37 |
| 201.1312 | 7.3447e-43 | 3.2637e-42 | 4.2198e-39 | 3.2133e-37 |
| 200.6312 | 1.1151e-42 | 4.7510e-42 | 7.3034e-39 | 4.2473e-37 |
| 200.1312 | 1.8890e-42 | 6.1455e-42 | 1.2471e-38 | 5.6552e-37 |
| 199.6312 | 2.9230e-42 | 8.6376e-42 | 1.6135e-38 | 9.8438e-37 |
| 199.1312 | 3.7722e-42 | 1.4490e-41 | 2.1540e-38 | 1.6406e-36 |
| 198.6312 | 5.1113e-42 | 2.3037e-41 | 3.5104e-38 | 2.2034e-36 |
| 198.1312 | 8.0046e-42 | 3.1554e-41 | 6.0802e-38 | 2.7467e-36 |

**(A) The periods in the twelve new states alone** (D 198.13 to 203.63, trend + one sinusoid, period scanned from 1.1, 1000-trial null test; the bracket is the spread of periods within one residual variance of the best, not a rigorous bound; `period_558.py` -> `results_period_558.txt`, selftest ok: a planted 2.365 passes the within-0.05 rule in 100% of 40 seeds, a planted 2.288 and a planted 2.520 in 0%):

| series | trend | period | amplitude | rms | null fraction | prediction posted before the run | difference | distance to the linear drift / the constant period |
|---|---|---|---|---|---|---|---|---|
| sigma_1 | quadratic | 2.350 (2.335 to 2.360) | 0.110 +- 0.003 | 0.0051 | 0.0% | 2.365 | -0.015 | 0.062 / 0.170 |
| sigma_1 | line | 2.380 (2.350 to 2.410) | 0.119 +- 0.008 | 0.0147 | 0.0% | 2.365 | +0.015 | 0.092 / 0.140 |
| sigma_2 | quadratic | 2.355 (2.340 to 2.365) | 0.110 +- 0.004 | 0.0054 | 0.0% | 2.377 | -0.022 | 0.071 / 0.165 |
| sigma_3 | quadratic | 2.125 (2.110 to 2.140) | 0.129 +- 0.004 | 0.0073 | 0.0% | 2.118 | +0.007 | 0.042 / 0.045 |
| sigma_4 | quadratic | 2.105 (2.085 to 2.120) | 0.133 +- 0.006 | 0.0097 | 0.0% | 2.119 | -0.014 | 0.024 / 0.065 |

Acceptance (ln sigma_1, quadratic trend, within 0.05 of 2.365, null fraction below 1%): **passes**, 2.350 (2.335 to 2.360), null 0.0%, 0.015 below the prediction. The local fit reads a planted period without bias and with sd 0.014 in this layout (#535), so 2.350 is 1.1 sd from the p2 chirp's 2.365, 4.4 sd from the linear drift's 2.288 and 12 sd from the constant 2.520, for white noise only. Together with #535 (2.380 against 2.404) the measured period is 0.02 below the prediction in both. The amplitudes are unchanged (0.110, 0.110, 0.129, 0.133).

**(B) The 63-state model (cubic trend) predicting the twelve new states** (the whole of ln sigma):

| series | p2 chirp rms (max) | p2 = 0 chirp rms (max) | p1 = p2 = 0 rms (max) |
|---|---|---|---|
| sigma_1 | 0.0157 (0.0273) | 0.0300 (0.0529) | 0.1026 (0.1697) |
| sigma_2 | 0.0123 (0.0342) | 0.0391 (0.0961) | 0.1122 (0.2050) |
| sigma_3 | 0.0425 (0.0635) | 0.0496 (0.1056) | 0.0770 (0.1548) |
| sigma_4 | 0.0223 (0.0506) | 0.0261 (0.0444) | 0.0772 (0.1292) |

For sigma_1 and sigma_2 the p2 chirp predicts the new states 1.9 and 3.2 times better than the linear drift and 6.5 and 9.1 times better than the constant period; sigma_2 at 0.0123 meets the 0.014 of #533, sigma_1 at 0.0157 misses it by 12%.

**(C) The p2 chirp refitted to all 75 states D 198.13 to 237.13 (cubic trend):**

| series | p2 = 0: P0, p1 | rms | free: P0, p1, p2 | rms | period at D 200.9 / 228 / 237 | null fraction (i) / (ii) |
|---|---|---|---|---|---|---|
| sigma_1 | 2.607, +0.0107 | 0.0091 | 2.617, +0.0156, +0.00022 | 0.0061 | 2.356 / 2.617 / 2.775 | 0.0% / 0.0% |
| sigma_2 | 2.607, +0.0107 | 0.0097 | 2.619, +0.0166, +0.00026 | 0.0055 | 2.363 / 2.619 / 2.790 | 0.0% / 0.0% |
| sigma_3 | 2.194, +0.0036 | 0.0117 | 2.197, +0.0060, +0.00011 | 0.0106 | 2.117 / 2.197 / 2.260 | not run |
| sigma_4 | 2.195, +0.0038 | 0.0096 | 2.198, +0.0058, +0.00010 | 0.0085 | 2.112 / 2.198 / 2.258 | not run |

With the twelve states added, p2 for sigma_1 and sigma_2 moves from +0.00025 and +0.00030 (63 states) to +0.00022 and +0.00026, stays at null 0.0%, and the residual stays at 0.0061 and 0.0055 over 75 states.

### Summary of #558's acceptances

| acceptance | result |
|---|---|
| the measured sigma_1 period within 0.05 of the prediction written before the run | **passes**: 2.350 against 2.365 (-0.015), null 0.0% |
| all twelve steps accepted, or the first refusal reported | **all twelve accepted** at their first attempt |
| the planted checks pass, one rows_only control fails | **passes** at all twelve (1.6e-14 to 3.8e-12, bound 1e-3), control exits 1 |
