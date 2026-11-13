# I726-win: the full system from D 104.5 to 120 with `--elim_switch 0`, and the held fit's error past D 100

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/726 (the coordinator's message `1794604648017-0` on the `choptuik-large-d` channel; recommended by #710, raw `I710-win/` 978179f6, whose run C gave the start `I710-win/C/anm_pin13_D104.5078.npz`; follows #682, raw `I682-win/` 0e9206ac). Worktree `choptuik-i710` at main 5249c432, venv-t151 (Python 3.10; hpkernel from before #523, so the rounded freeze projector as in #642), quad-double, `OPENBLAS_NUM_THREADS=1`, BelowNormal, 4 threads, #682's flags (`--kfreeze 13 --N 24 --eps 1e-14 --D_max 400 --corrector qd --tol_qd 1e-44 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --save_pred 1 --a_grow 1.25 --a_hold 1 --lam_stall 0.04`) with `--elim_switch 0`. Raw output to `I726-win/`.

## Plan, written before the run (2026-11-13 21:28 UTC)

The issue's acceptance (each can fail): (1) each step converges to qd max|F| of at most 1e-44, or the three-refusal stop fires and its history is posted; (2) Delta_full - Delta_held at each integer D from 105 to 120, against the held states `T138-win2/chain/anm_pin3_D<D>.0000.npz`, with its ratio to `delta_all.csv`'s err (as in #682).

Choices fixed here:

1. **Runs.** `run_726.py S1 L`: S1 is one step `--h_max 0.4921875 --a0 0.4921875 --steps 1` from `I710-win/C/anm_pin13_D104.5078.npz` (104.5078125 + 0.4921875 = 105 exactly); L is `--h_max 1.0 --a0 1.0 --steps 15` from `I726-win/S1/anm_pin13_D105.0000.npz`, to D 120 if every step is taken at a = 1. 4 threads, BelowNormal, one BLAS thread. The stop rule is anm_run's own (three refused attempts in a row at one D, after which the run ends and its step history is posted).
2. **Converged** means the corrector says converged and its qd max|F| is at most 1e-44 (`table_726.py` checks the bar itself, and its selftest has a planted attempt at 2e-44 that must read NOT converged). A refused attempt that anm_run halves and then accepts is reported with both attempts.
3. **Delta_full - Delta_held** is read as in #682: the sum of the last entry of each of the four parts, in arb at 400 bits, of the full state minus the held state at the same integer D, and the ratio to the `chain_fit` row of `delta_all.csv` (kind "fits d10"; that err is a spread over fit choices, not an enclosure). A D that is not reached is listed as not reached. The held states exist on the stage checkout for D 100 to 121 at least.
4. **Expectation, written before the run and not a criterion**: from #682 the shift grows with successive ratios falling from 1.08 (D 99 to 100) toward 1, and its ratio to the err stays near 0.19 (the value from D 97 to 100). A break of that pattern is reported as it is.
5. **Not done**: any step past D 120, any change of the flags, and the Delta floor of #725 is not applied (it is 1e-25 against shifts of 1e-13).

## Results (2026-11-13 23:13 UTC)

`run_726.py S1 L` exited 0: S1 236 s, L 6073 s (4 threads, BelowNormal, one BLAS thread). L ended by anm_run's own stop at D 112.75, "no convergence after three halvings". The rule is `for attempt in range(4)` (`hp/anm_run.py` line 808), so it needs four refused attempts at one D, the first and three halvings, not three in a row as the plan said. Ten states are accepted (S1 to D 105, L to D 112 in seven steps at a = 1, then D 112.5 and D 112.75) and six attempts are refused. The full per-attempt table and the Delta table are `table_726_out.md` (`table_726.py`, selftest passed, its planted 2e-44 attempt reads NOT converged).

Acceptance 1 holds: every accepted step has qd max|F| at most 7.0e-45, and the stop fired with its history in the table. Acceptance 2 holds for D 105 to 112 below, and D 113 to 120 are not reached.

| D | Delta_full - Delta_held | err of delta_all.csv (chain_fit, a spread over fit choices) | ratio |
|---|---|---|---|
| 105 | +3.0518e-13 | 1.8e-12 | 0.170 |
| 106 | +3.2207e-13 | 2.0e-12 | 0.161 |
| 107 | +3.3893e-13 | 2.1e-12 | 0.161 |
| 108 | +3.5571e-13 | 2.3e-12 | 0.155 |
| 109 | +3.7236e-13 | 2.4e-12 | 0.155 |
| 110 | +3.8881e-13 | 2.6e-12 | 0.150 |
| 111 | +4.0503e-13 | 2.7e-12 | 0.150 |
| 112 | +4.2096e-13 | 2.9e-12 | 0.145 |

The expectation fixed before the run held in one respect and failed in another. The successive ratios of the shift fall toward 1 as expected (1.055, 1.052, 1.050, 1.047, 1.044, 1.042, 1.039). Its ratio to the err does not stay near 0.19: it falls from 0.170 to 0.145, because the err grows faster (1.8e-12 to 2.9e-12) than the shift (3.05e-13 to 4.21e-13). These are not enclosures. The Delta floor of #725 (1e-25) is far below the shifts.

Refused attempts (qd max|F| after the corrector's own stop, "no trial step accepted"):

| from D | a | to D | qd steps | qd max abs F |
|---|---|---|---|---|
| 112 | 1 | 113 | 7 | 3.5e-43 |
| 112.5 | 0.5 | 113 | 6 | 9.3e-44 |
| 112.75 | 1/4 | 113 | 8 | 2.9e-44 |
| 112.75 | 1/8 | 112.875 | 5 | 1.1e-44 |
| 112.75 | 1/16 | 112.8125 | 9 | 7.8e-44 |
| 112.75 | 1/32 | 112.78125 | 7 | 6.6e-44 |

The stalled |F| is flat in a (2.9e-44, 1.1e-44, 7.8e-44, 6.6e-44 over a factor 8) while the first full step's |F| falls with a (1.05e-21 to 1.7e-23), so the floor is not the step's quadratic error. The last Newton steps of the stalled attempts change Delta by 2e-46 to 4e-45. The elimination pivots span 8e-20 to 9e14 (a factor 1e34). Whether the quad-double precision sets the floor is not tested here (the octo-double corrector would test it, M = 32 here).

The series behind the predictor, per step (norm of the last term z_N; order ratio 5 is `ratios_2_5[3]`):

| step | D | a_max | order ratio 5 | z_N |
|---|---|---|---|---|
| 0 | 105 | 4.690 | 105.9 | 5.00e-33 |
| 1 | 106 | 5.091 | 109.6 | 7.47e-34 |
| 2 | 107 | 4.236 | 98.5 | 5.05e-32 |
| 3 | 108 | 3.952 | 64.9 | 2.46e-31 |
| 4 | 109 | 4.073 | 59.9 | 1.21e-31 |
| 5 | 110 | 3.888 | 34.5 | 3.46e-31 |
| 6 | 111 | 3.643 | 27.4 | 1.53e-30 |
| 7 | 112 | 3.337 | 8.0 | 1.14e-29 |
| 8 | 112.5 | 3.526 | 18.3 | 3.17e-30 |
| 9 | 112.75 | 3.442 | 11.9 | 5.50e-30 |

Files: `S1/` and `L/` (states `anm_pin13_D*.npz`, predictions `pred_pin13_D*.npz`, `anm_run.jsonl`), `logs/` (S1.log, L.log, run_726.log, exits), `table_726.py`, `table_726_out.md`, `run_726.py`. The last accepted state is `L/anm_pin13_D112.7500.npz`.
