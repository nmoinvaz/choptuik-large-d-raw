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
