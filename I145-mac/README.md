# I145-mac: the RT prototype continued past D = 30 with the multiprecision solve, its Chebyshev N per D and cost growth

Machine: Apple M5 Mac, a subagent of the coordinator.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/145
Code: branch wip/i145 of nmoinvaz/choptuik-large-d, solver/rt/ (rt_run.py --solver mp with --start_prev, --pred_order,
--extras_off_path); the reading is a new section of notes/RT_FORMULATION.md there.

Start state: I105-mac/cont/cont_32x101_D30.0000_32x101.npz (raw commit 6c9d697), with the D = 28 and 29 states of the
same run as the predictor's history.

## Criteria, written before the runs

- Solver: rt_run.py --solver mp at 192 bits, Newton to max|F| < 1e-40 (as #105), N_t = 32, --max_products 250.
- N per D. The ladder is N = 81, 101, 121, 141, 161, ... (odd, steps of 20). At each check D, N(D) is the smallest N
  on the ladder with |Delta_N - Delta_{N+20}| < 1e-12, both converged. The continuation runs on the current N(D). It
  moves to N + 20, by resampling its last three states, once a check shows |Delta_N - Delta_{N+20}| >= 1e-13, one
  decade of margin, since the next check is 5 units of D away. The thresholds are not changed after the runs.
- Check D: the hp rows nearest 35, 40, 45, 50, 55, 60 (34.993266, 40.020065, 44.963411, 50.007491, 54.996085,
  60.001952, double-double, err 1e-16 to 2e-15) and past 60 the rows at 64.994829 (dd), 70 (pinned), 75, 80, 85, ...
  (chain_fit, err 3.9e-15 at 75 to 1.2e-12 at 100).
- Acceptance (issue #145): |Delta_RT - Delta_hp| < 1e-12 at the rows nearest 40, 50 and 60 on N(D), or the miss is
  reported. rt_grids.py on the N(D) and N(D) + 20 records with --tol 1e-12 exits 0, and with --mutate=shift exits 1.
- Control: --mutate=coef at D = 60.001952 from the unmutated state must move Delta by more than 1e-6 and exit 1.
- Continuation: steps of 1 in D with the quadratic predictor (--dD 1 --pred_order 2), which starts at the residual of
  #105's linear predictor at steps of 1/2 (1.8e-4 at D = 30 on 32x101, measured from #105's states). The check D are
  solved off the path (--extras_off_path).

## What ran

- `pilot/`: one step from D = 30 to 30.5 on 32x101 with #105's linear predictor (exit 1 only from the end check: hp has
  no row at 30.5).
- `run_cont.sh`, `cont/cont_32x101*`: the continuation on 32x101 from D = 30 (prev 28, 29).
- `cont/cont_32x121*`: the continuation on 32x121 from the same states resampled. Its start at D = 30 converged; its
  first step, to D = 31 from the quadratic predictor (max|F| 1.5e-4, the same as on 32x101), did not: the first Newton
  step was 6.6e-3 (halved to 3.3e-3), and after 4 steps and 3 rebuilds max|F| was still 3.6e-5 (exit 1). The protocol
  for the grid above the continuation's was then changed to the follower below. The criteria above are unchanged.
- `run_follow.sh`, `fol/fol_32x121*`: the follower. Each state the 32x101 continuation saves is resampled to 32x121 and
  re-solved there at the same D (rt_run.py --start STATE --grids 32x121), the check D first, otherwise the newest.
- The 32x101 run was restarted twice from its D = 33 state (same tag, appended): with the cubic predictor
  (`run_cont.sh ... 100 3`), and then with `--patient --it_max 20`, after #105's stall rule ended D = 34 unconverged at
  max|F| = 1.2e-26 (record with ok false). The follower's D = 32 solve stopped the same way at 1.5e-26 and was redone
  with --patient.
- A third restart, from D = 34 (prev 31-33): `--full_below 1e-10` let D = 34 converge, but at D = 35 a full step of
  3.4e-9 was halved to 1/128 for 8 steps while max|F| grew from 4.4e-19 to 2.2e-18. From 08:46 UTC the runs take every
  step below 1e-4 in full (`--full_below 1e-4`, `EXTRA=` without 34.993266, already done).
- `controls/planted*`: solver/rt/rt_mpsolve.py --selftest at the code of these runs (exit 0, error 6.9e-40).
- `fit/`: solver/rt/rt_cost_fit.py --planted and its mutations `rate`, `slope` (exit 0, 1, 1); solver/rt/rt_pred_check.py
  on #105's 32x101 states (`pred_check.log`, exit 0) and its `--mutate=order` (exit 1).
- `run_worker.sh`, `worker.stdout` (from 08:58 UTC, replacing `run_follow.sh`): one queue for the second process,
  32x121 re-solves of the continuation's states at the check D first, then 32x141 re-solves of the 32x121 states at the
  check D (`fol/fol_32x141*`), then 32x121 at the newest other D.
- `controls/nt_48x141*`: the 32x141 state at D = 40.020065 re-solved on 48x141 (time resolution). Delta moved by
  1.3e-20, so N_t = 32 is not what sets 32x141's Delta there.
- `controls/from101_32x141*`: 32x141 at D = 40.020065 re-solved from the 32x101 state (the follower started from the
  32x121 state). Both converge (max|F| 2.5e-47 and 5.4e-52), yet their Delta differ by 6.4e-15 and max|z1 - z2| is
  4.3e-16 (mostly mu and harmonic 0). So the 32x141 root there is not unique to that level.
- `run_roots.sh`, `controls/from121_32x101*`, `controls/from141_32x121*`: the same test for 32x101 (from the 32x121
  state) and 32x121 (from the 32x141 state). Both reproduce their first roots' Delta to all 20 printed digits.
- `run_worker2.sh`, `worker2.stdout` (from 10:20 UTC, replacing `run_worker.sh`): the queue with these root tests
  added at each check D (`fol/from121_32x101*`, `fol/from141_32x121*`). The 34.99 and 40.02 tests are marked done.
- `run_worker3.sh`, `worker3.stdout` (from 10:44 UTC, replacing `run_worker2.sh`, whose 32x141 solve at D 44.96 took
  9 min and landed 3.8e-12 from hp): 32x121 at each check D, then the root tests 32x121 -> 32x101
  (`fol/from121_32x101*`) and a second start for 32x121 from the 32x101 state at the integer D below the check D
  (`fol/fromint_32x121*`, rt_run.py --D_start), then 32x141 at the check D, then 32x121 at the newest D.
- `run_worker4.sh`, `run_worker4_start.sh`, `worker4.stdout` (from 10:56 UTC, replacing `run_worker3.sh`, whose rule 3
  started 32x121 a whole unit of D below the check D, from max|F| = 3.2e-3, and diverged; stopped by hand, its record
  in `fol/fromint_32x121*` has ok false): the second 32x121 start is the second 32x101 root (`fol/from101b_32x121*`) or
  the 32x141 root (`fol/from141_32x121*`).
- A fourth restart of the 32x101 run, from D = 53 (prev 50-52) at 11:21 UTC, with `NEWTON_TOL=1e-38` (rt_run.py
  --newton_tol; --patient then accepts a stall below 1e-32). The D = 54 step had bounced for 15 Newton steps between
  max|F| = 6e-35 and 1.2e-33 with max|dz| of 1e-18 to 3e-18 each, above the old acceptance of 1e-34, and was stopped
  by hand. A step of 3e-18 moves Delta by about 1e-17.
- A fifth restart, from D = 56 (prev 53-55) at 12:14 UTC, with `NEWTON_TOL=1e-36` (stalls accepted below 1e-30). The
  D = 57 step reached max|F| = 3.3e-35 at its seventh Newton step, then bounced for 7 steps between 1.2e-32 and 1.0e-31
  at max|dz| of 8e-18 to 1.2e-16, above the acceptance of 1e-32, and was stopped by hand. A step of 1e-16 moves Delta
  by about 1e-15.
- `run_roots_logs.sh`: rt_roots.py on each pair of roots (`controls/roots_*.log`). `fit/roots101_second.jsonl` joins
  the second 32x101 roots (`controls/` and `fol/from121_32x101.jsonl`) for rt_grids.py.
- `fol/from141_32x121*` at D = 54.996: 32x121 from the 32x141 root (itself 3.0e-7 off hp) wandered for 6 Newton steps,
  max|F| between 8e-25 and 8e-13 with steps up to 1.2e-7, and was stopped by hand at 12:21 UTC to free the slot for
  the coefficient mutation (`run_coef.sh`, `controls/coef_*`).
- `run_coef.sh`, `controls/coef_D54.9961*`: the coefficient mutation at D = 54.996085 (exit 1: 20 Newton steps,
  max|F| 4.0e-4 -> 1.5e-9, not converged, Delta 3.8e-2 from hp).
- `run_final60.sh`, `final60.stdout`: at D = 60.001952 it stops the continuation, then runs the coefficient mutation
  there (`controls/coef_D60.0020*`) beside the 32x121 re-solve, then the second 32x101 root.
