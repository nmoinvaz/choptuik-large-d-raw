# I725-win: what Delta two converged full-system roots resolve at D 99.8, switch 0 against the default at a = 1/16

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/725 (the coordinator's message `1794604648017-0` on the `choptuik-large-d` channel; recommended by #710, raw `I710-win/` 978179f6). Worktree `choptuik-i710` at main 5249c432, venv-t151 (Python 3.10; hpkernel from before #523), quad-double, `OPENBLAS_NUM_THREADS=1`, BelowNormal, 4 threads, #682's flags (`--kfreeze 13 --N 24 --eps 1e-14 --D_max 400 --corrector qd --tol_qd 1e-44 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --save_pred 1 --a_grow 1.25 --a_hold 1 --lam_stall 0.04`). Raw output to `I725-win/`.

## Plan, written before the runs

The issue (verbatim): "The a = 1/16 step from `I682-win/cont3/anm_pin13_D99.7500.npz` with `--elim_switch 0`, to D 99.8125, and its Delta against `cont3/anm_pin13_D99.8125.npz`, which is the same step at the default switch. Then the same from D 99.8125 to 99.875, against `cont3/anm_pin13_D99.8750.npz`. Use #682's flags." Acceptance: "if both differences are below 1e-30, A1's 3e-26 belongs to the large step and is reported as a discrepancy. If both are at the 1e-26 scale, the bar was below what two converged roots resolve, and the report gives the floor." The coordinator's message adds the commands `--elim_switch 0 --h_max 0.0625 --a0 0.0625 --steps 1`, the second step from the new D 99.8125 state.

Choices fixed here (2026-11-13 21:18 UTC), before any run:

1. **Runs.** X1: start `I682-win/cont3/anm_pin13_D99.7500.npz`, `--elim_switch 0 --h_max 0.0625 --a0 0.0625 --steps 1`, to D 99.8125. X2: the same flags from `I725-win/X1/anm_pin13_D99.8125.npz`, to D 99.875. One after the other, `run_725.py X1 X2`. A step counts if its first attempt converges to qd max|F| of 1e-44 or less within 8 steps (the logs' qn lines and elim counts are reported); if the first attempt is refused and a halved one accepted, the Delta check is made only if the accepted D is the cont3 state's D.
2. **Delta**: the sum of the last entry of each of the four parts, in arb at 400 bits (as #710). X1 against `cont3/anm_pin13_D99.8125.npz`, X2 against `cont3/anm_pin13_D99.8750.npz`. X2's start is X1's state, so its difference carries X1's.
3. **Reading** of the two absolute differences d1 and d2: both below 1e-30 means "belongs to the large step" (the bar of #710 is met at a = 1/16); both between 1e-28 and 1e-24 means "the 1e-26 scale", and the floor reported is the larger of the two; anything else (one below and one above, or outside 1e-28 to 1e-24) is reported as it is and is neither of the issue's two outcomes. The state difference (leading-double agreement, max, median of the 769 entries) and each state's qd max|F| are context for the floor, as in #710.
4. **Not done**: any run beyond the two, and any change of the bar.

## Run record

`run_725.py X1 X2`, 4 threads, BelowNormal, one BLAS thread, both exit 0 (`logs/run_725.log`): X1 21:18:44 to 21:22:32 UTC (229 s), X2 21:22:32 to 21:26:25 UTC (233 s). `table_725.txt` is the output of `table_725.py` (its selftest passes: planted pairs read LARGE STEP, 1e-26 SCALE and NEITHER as they should, and a planted last-entry displacement of 1e-27 moves the reading from LARGE STEP to 1e-26 SCALE).

## Results

Both steps were accepted at their first attempt, in 3 corrector steps, with `u0q` 3 and `skipped` 0:

| run | a | D | qn 0 |F| (start to after the full step) | qn 1 | final qd max abs F | cont3's state at that D |
|---|---|---|---|---|---|---|
| X1 (from cont3 D 99.75) | 0.0625 | 99.8125 | 1.18e-35 to 9.14e-32 | 9.14e-32 to 2.35e-49 | 2.3e-49 | 4.4e-45 |
| X2 (from X1's state) | 0.0625 | 99.875 | 2.50e-35 to 4.31e-31 | 4.31e-31 to 4.09e-49 | 4.1e-49 | 3.9e-49 |

| | Delta (30 digits) | cont3's | abs diff | state difference (769 entries) |
|---|---|---|---|---|
| X1 at D 99.8125 | 1.74521191343852106839198616167 | 1.74521191343852106839198616167 | **5.670e-34** | max 2.2e-25, median 3.8e-28, same leading double in 769 of 769 |
| X2 at D 99.875 | 1.74515002816449925294435272784 | 1.74515002816449925294435289364 | **1.658e-25** | max 1.0e-17, median 1.6e-20, same leading double in 752 of 769 |

**Reading by README choice 3: NEITHER of the issue's two outcomes.** d1 = 5.670e-34 is below 1e-30 (the bar of #710 is met), d2 = 1.658e-25 is at the 1e-26 scale, so the two differences do not fall in one class. The first a = 1/16 step reproduces cont3's state to 5.7e-34 in Delta, the second does not.

**Context, from stored states only (no new run).** Three converged states exist at D 99.875: cont3's (qd max|F| 3.9e-49), #710's A1 (a = 1/8 from D 99.75, 6.2e-49) and this task's X2 (4.1e-49). Relative to cont3's, A1's Delta is +2.971e-26 and X2's is -1.658e-25, so the three span 1.955e-25 (A1 against X2), at |F| of 4e-49 to 6e-49. At D 99.8125 the two states (X1 and cont3's, whose |F| are 2.3e-49 and 4.4e-45) agree to 5.7e-34. So the floor in Delta at D 99.875 across these three paths is 1.96e-25, and at D 99.8125 two paths agree 11 orders better. I do not know why the agreement is different at the two D. If a weak direction of fixed gain set it, |F| of 4.4e-45 at D 99.8125 would permit a larger difference than the 5.7e-34 seen, so the simple reading of #710 (a weak direction with a gain near 5e-31 fixes what |F| resolves) does not explain both D by itself.

The bar of 1e-30 stays as it was.

## Recommended tasks (for the coordinator)

1. **Does the spread at D 99.875 shrink with a tighter polish?** What: for each of the three D 99.875 states (cont3's `anm_pin13_D99.8750.npz`, `I710-win/A1/...`, `I725-win/X2/...`), the base polish alone at `--tol_qd 1e-60 --qd_it 12 --steps 0` (check first that `--steps 0` stops after the base), and Delta of each polished state. Acceptance (can fail): the three Delta agree to 1e-30 (then the spread was unconverged weak-direction error at |F| of 1e-48) or stay about 2e-25 apart (then they are three distinct near-roots at this precision). Depends on #725. A few minutes per state at 4 threads.
2. **Measure the weak direction's gain at D 99.875.** What: the smallest singular value of the quad-double Newton matrix at `cont3/anm_pin13_D99.8750.npz` (inverse iteration through its LU) and the Delta component of that direction. Acceptance (can fail): sigma_min at most 5e-31 and the Delta component times |F| / sigma_min reproducing the 2e-25 spread (the weak direction explains it), or sigma_min above 1e-25 (it does not). Depends on #725.
