# I105-mac: the RT prototype continued from D = 10 to 30 with a multiprecision Jacobian solve, and its planted tests

Machine: Apple M5 Mac, a subagent of the coordinator.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/105
Code: branch wip/i105 of nmoinvaz/choptuik-large-d, solver/rt/ (rt_mpsolve.py, rt_run.py); the reading is the
section "Past D = 10: a multiprecision Jacobian solve" of notes/RT_FORMULATION.md there.

- `planted*.log`, `planted.jsonl`: solver/rt/rt_mpsolve.py --selftest (kappa = 1e20 planted system).
  `planted_first_run.log` is the first design (GCR with f64 triangular solves), which crashed after one step with the
  true residual 1e-6 against GCR's 1e-18; the first record of `planted.jsonl` (no `inner` field) is the second design
  (GCR with the explicit f64 inverse), which failed. `planted.log` is the final design (flexible GMRES, the f64 LU
  applied by double-double triangular solves), `planted_mutate_*.log` its two mutations (exit 1), and
  `planted_variants.log` the other inner solvers and preconditioners.
