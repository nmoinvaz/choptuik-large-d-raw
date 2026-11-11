# I489-mac: crawlJ's D 242.3642 state re-noded to layouts ending at x = 0.8, their base polish and weakest directions

Machine: mac (Apple M5), a subagent of the coordinator, 2 threads under nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/489 (depends on #488 and #461).

Code: choptuik-large-d main a9b0885 plus `hp/renode_o.py` and `anm_run.py --save_base` (branch `wip/i489-subagent`,
84e4d7f), interpreter venv-314 (Python 3.14, its installed `hpkernel` built 2026-11-08).

Source state: `I461-win2/crawlJ/anm_pin3_D242.3642.npz` (nodes 0.3-0.7, eight parts, crawlJ's plan of 21 steps).

## Re-node, layout 1 (0.3, 0.4, 0.5, 0.6, 0.7, 0.8)

`renode_o.py RAW I461-win2/crawlJ/anm_pin3_D242.3642.npz I489-mac/renode_L1_<last>_D242.3642.npz --nodes
0.3,0.4,0.5,0.6,0.7,0.8 --last <last>`, logs `renode_L1_<last>.log`. The four old segments keep crawlJ's plan, and the
new one (0.7 to 0.8) is planned at 1e-32 (6 steps). The stored state's pinned max|F| on its own layout, with the held
offset at its own coefficients as the base polish forms it, is 7.99e-38, all in the held rows (crawlJ's polish of
crawlI's base started at 8.14e-38 for the same reason).

| start (`--last`) | node 0.8 from | its block's rows before, after | pinned max\|F\| of the start | largest block |
|---|---|---|---|---|
| f64 | `driver.renode`, beyond="horizon", summed in f64 | 6.12e-09 (not refined) | 6.12e-09 | 0.7 to 0.8 and horizon |
| horizon | the horizon series at u0 0.2, in eight parts | 6.12e-09, 0 | 1.62e-34 | horizon p, harmonics 1 and 3 |
| integrate | the Taylor steps from 0.7, in eight parts | 6.12e-09, 0 | 1.59e-34 | horizon p, harmonics 1 and 3 |

The horizon series and the Taylor steps differ at 0.8 by 4.4e-36 (p, m), 1.9e-36 (c) and 3e-39 (a). The control
(`--mutate sign`, `renode_L1_ctl_sign.*`) leaves the rows at 1.22e-08 and its check fails (exit 1), as it must.
The polish starts from the horizon start (`run_polish.sh`, `polish_L1.log`, `polish_L1/`).

## Base polish, layout 1: stopped inside its first Newton step

`run_polish.sh <worktree>/hp RAW I489-mac/renode_L1_horizon_D242.3642.npz polish_L1`: anm_run.py with crawlJ's
options, `--steps 0 --save_base 1`, 2 threads. It ran from 05:21:20 to 08:00:27 UTC (`exits.txt`: exit 143, SIGTERM,
wall 9547 s, 210 cpu-min) and was stopped at the coordinator's deadline. In that time it did not finish step 0, so the log
holds only its two header lines, `polish_L1/` is empty and no base was saved. newton_od prints a step only once a trial is
accepted or all nine trials (lam 1 to 1/256) are refused.

Where it was, from two stack samples (macOS `sample`, 07:25 and 08:00 UTC; the files were not kept):

- 07:25: `Solver.newton_o` building the octo-double Jacobian (`osolve::jacobian_o`, in `taylor_coeffs` and
  `horizon_series`). That is the start or a trial point.
- 08:00: `Solver.jacobian` and `Solver.residual` in double-double, i.e. `Reseeder.invert`, the re-seed projection's
  rung Newton. ElimO runs it only at points whose pinned quad-double max|F| exceeds 1e-15. The start's is 1.6e-34
  (computed afterwards from its four-part rounding with the same offset), so ElimO skips it there.

So at least one trial point of step 0 had max|F| above 1e-15, 19 or more orders above the start's 1.6e-34. That is
the signature of crawlK's first step at 0.3-0.7 (1.4e-35 to 2.3e-24, #488) and of the earlier 0.8 layouts
(notes/QUAD_DOUBLE.md 12.3, D 73: the first step raises |F| by 5-10 orders; 13.27, D 162.31: the polish stalls at
7.9e-18 with pivots down to 9e-20). Each trial here costs a full octo-double Jacobian and LU at L 897 plus, above the
switch, a projection with double-double Jacobians. With load 26-89 and swap nearly full, that held the run under one
step for 2.6 h. Layout 2 was not run (coordinator: one process only). `run_near_null.sh` was prepared and never run.
