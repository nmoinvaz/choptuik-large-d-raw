# I739-win: the full system past D 112.75 with the octo-double corrector, is #726's floor the quad-double precision

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/739 (the coordinator's messages `1794614449424-0` and `1794615586720-0` on the `choptuik-large-d` channel; recommended by #726, raw `I726-win/` 647cd9f5). Worktree `choptuik-i710` at main 5249c432, venv-t151 (Python 3.10), `OPENBLAS_NUM_THREADS=1`, BelowNormal, 4 threads. Start state `I726-win/L/anm_pin13_D112.7500.npz` (M = 32, quad-double, qd max|F| 4.7e-45). Flags as the issue gives them: #682's flags plus `--elim_switch 0 --corrector od --tol_od 1e-60 --reseed_o 3` (`run_739.py` lists them). Raw output to `I739-win/`.

## Plan, written before the runs (2026-11-14 00:20 UTC)

Runs, separate processes, each stopped at its own refusal (the driver kills the tree after an attempt that ends not converged, so no halvings run; the coordinator's message `1794615586720-0` confirms this and my reading of (c)):

1. **`ctl`, the control (a) and the cost probe**: the octo-double polish of the D 112.75 state alone, `--steps 0 --save_base 1`. Its Delta is compared with the quad-double state's: the difference is reported against the bar of 1e-30 (the issue's wording is "or the difference is reported", so a miss does not stop the task). Its time per Newton step at this D is the cost for A and B.
2. **`A` (b)**: one attempt a = 1/8 from the D 112.75 state to D 112.875, the attempt that stalled at 1.1e-44 in #726's quad-double run. Converged means octo-double max|F| of at most 1e-60 (the corrector's own "converged"). If it does not converge, I state the floor with each Newton step's max|F| from the log.
3. **`B` (c)**, only if A converged: one attempt a = 1/4 from the D 112.75 state to D 113, the attempt that stalled at 2.9e-44. Reported the same way. (112.875 + 1/4 would be D 113.125, so "a = 1/4 to D 113" is from D 112.75.)

**Expectation, written before the runs and not a criterion**: from #727 (with `--reseed_o 3` the octo-double floor is 1e-63 and below at D 99.875) and #713 on the Mac, I expect A to converge to 1e-60 in about 3 to 5 Newton steps, at roughly 100 to 150 s a step, and the stall of #726 to be the quad-double precision (the elimination pivots span 8e-20 to 9e14, a factor of 1e34, against quad-double's 1e-64). If A stalls at the quad-double level instead (1e-44 to 1e-43), the floor is not the precision and I report that. If A converges, I also report the Delta of the accepted D 112.875 state against the quad-double D 112.75 state's trend (the step's `dDelta`), and the first-step |F| of A and B against #726's.

**Not done**: any attempt past the first of a step, any state at another D, any change of the flags, the held states and `delta_all.csv` comparison of #726 (Delta_full - Delta_held at D 112.875 and D 113 is not asked here).

## Results (2026-11-14 01:02 UTC): the floor was the quad-double precision, both attempts converge in octo-double

`run_739.py ctl A` then `run_739.py B` (separate runs, each from `I726-win/L/anm_pin13_D112.7500.npz`, #682's flags with `--elim_switch 0 --corrector od --tol_od 1e-60 --reseed_o 3`, 4 threads, BelowNormal), all exit 0, none stopped by the driver: `ctl` 229 s, `A` 951 s, `B` 1213 s (B's first base-polish step took 176 s against 101 s in `ctl` and `A`, because I ran the table and compare scripts alongside it). Per-step tables are `table_739_out.md`, the Delta values `final_cmp_739.txt` (the exact sum of all eight parts), the times and the extra `extra_739_out.md`.

| acceptance | result |
|---|---|
| (a) control: octo-double polish of the D 112.75 state, Delta against the quad-double state's | **met**: 1 Newton step, max abs F 6.61e-48 to 2.45e-78 (converged, 2.5e-78), Delta difference -6.958e-46 against the bar 1e-30 |
| (b) the a = 1/8 attempt to D 112.875 converges to at most 1e-60, or its floor is stated | **converges** on its first attempt: max abs F 1.21e-35 (re-seeded prediction), 1.96e-22, 1.11e-40, 2.98e-47, 7.83e-89, accepted, 4 Newton steps |
| (c) the a = 1/4 attempt to D 113, reported the same way | **converges** on its first attempt: 1.86e-35, 7.59e-22, 3.53e-39, 4.30e-45, 7.25e-85, accepted, 4 Newton steps |

The same attempts from the same state, which stalled at 1.1e-44 (a = 1/8) and 2.9e-44 (a = 1/4) in #726's quad-double run, end 41 and 44 orders below those (7.3e-85 and 7.8e-89). The last Newton step is quadratic (4.30e-45 to 7.25e-85 in B, 2.98e-47 to 7.83e-89 in A), and the step before it already sits below the quad-double stall in both (3e-47 against 1.1e-44 in A, 4.3e-45 against 2.9e-44 in B), so the stall is not where the iteration runs out of descent: the octo-double iteration passes below it and then converges quadratically.

Accepted states, Delta as the exact sum of the eight parts, 40 digits: D 112.875 (`A/anm_pin13_D112.8750.npz`) 1.733737391603221302341174251654151455296, D 113 (`B/anm_pin13_D113.0000.npz`) 1.733640141567942734406710993193602081591. The refused quad-double iterates read 1.733737391603 and 1.733640141568 (12 digits, #726's log), equal at those digits. The quad-double stalled states were not saved, so their Delta error cannot be measured here; the per-step Delta changes at the quad-double stall were at most 4.4e-45.

**What this does not separate**: octo-double changes the corrector and, with `--reseed_o 3`, the projection together. #727's first pilot (octo-double corrector without `--reseed_o`, D 99.875) floored at the projection's quad-double level (2.74e-49), so at D 112 to 113 the quad-double projection alone may be a floor too. "The precision" here is the pipeline's, not one component's; no run with only one changed was made.

**Cost**: the octo-double attempts took 577 s (A) and 593 s (B) in the corrector, 5 evaluations each at 100 to 120 s a step, against 412 s and 495 s for the stalled quad-double attempts at the same a (and 686 s and 748 s for the two halvings), so about 1.2 to 1.4 times the price of an attempt that failed.

**Extra, not asked** (`extra_739.py`, read-only): Delta_full - Delta_held at D 113, which #726 did not reach, is +4.3655e-13 (held state `T138-win2/chain/anm_pin3_D113.0000.npz`), ratio 0.146 to delta_all.csv's err (3.0e-12, a spread over fit choices), and the ratio of the shift to D 112's is 1.037 (#726's successive ratios fell 1.055 to 1.039). The control, the same arithmetic at D 112 from #726's quad-double state, reproduces #726's +4.2096e-13.

Controls run: `run_739.py --selftest` (the stop rule fires only on a not-converged attempt after its summary line, not on a converged one or in the control), `cmp_739.py --selftest` (planted eight-part value returned to 40 digits, the two-part sum differs), `table_739.py --selftest` (planted lines parse, a not-converged ending reads NOT converged), and the D 112 control of the extra.
