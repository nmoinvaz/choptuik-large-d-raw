# I105-mac: the RT prototype continued from D = 10 to 30 with a multiprecision Jacobian solve, and its planted tests

Machine: Apple M5 Mac, a subagent of the coordinator.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/105
Code: branch wip/i105 of nmoinvaz/choptuik-large-d, solver/rt/ (rt_mpsolve.py, rt_run.py --solver mp, rt_grids.py,
rt_mp_cost.py); the reading is section 9 of notes/RT_FORMULATION.md there.

- `planted*.log`, `planted.jsonl`: solver/rt/rt_mpsolve.py --selftest (kappa = 1e20 planted system).
  `planted_first_run.log` is the first design (GCR with f64 triangular solves), which crashed after one step with the
  true residual 1e-6 against GCR's 1e-18; the first record of `planted.jsonl` (no `inner` field) is the second design
  (GCR with the explicit f64 inverse), which failed. `planted.log` is the final design (flexible GMRES, the f64 LU
  applied by double-double triangular solves), `planted_mutate_*.log` its two mutations (exit 1), and
  `planted_variants.log` the other inner solvers and preconditioners.
- `pilot/`: rt_run.py --solver mp on 32x101. `d10_*` the D = 10 re-solve from I91-mac's 48x81 state, `pilot12_*` one
  Newton solve at D = 12 from it (`pilot12_32x101_norefresh.*` the first attempt without preconditioner rebuilds,
  stopped), `cont12_*` the continuation 10 to 12 in steps of 1/2. States are npz with zh, zl (double-double).
- `cont/`: the acceptance continuations D = 10 to 30 on 32x81 (exit 1: D = 20.04 and 29.98 miss 1e-10) and 32x101
  (exit 0), one jsonl record and one npz state per D, logs, stdout.
- `accept_grids.log`: solver/rt/rt_grids.py on the two continuations with --table and the resolution controls (exit 1).
- `controls/`: `coef_D*` the --mutate=coef runs at D = 15 and 29.98 from the 32x81 states (exit 1);
  `res_48x101_*`, `res_32x121_*` the 32x101 states re-solved on 48x101 and 32x121 at the three check D
  (`res_32x121_all.jsonl` their concatenation); `grids_121_101*.log` rt_grids.py on 32x121 against 32x101 (exit 0) and
  its --mutate=shift (exit 1); `planted_inplace*` the planted test of the in-place LU and its mutations; `mp_cost*`
  solver/rt/rt_mp_cost.py (`mp_cost_*` the first version, whose check against J64 was wrong; `mp_cost2_*` the
  backward-error check; `mp_cost3_*` with the dense-LU estimates, quoted in the note).
