# I1055-mac: PR #1055's plan-order measurements (Taylor order chosen by planned cost), on the Mac

Machine: the coordinator's M5 Mac, loaded (3 threads for the octo-double Jacobians). PR:
https://github.com/nmoinvaz/choptuik-large-d/pull/1055 (branch perf/plan-auto, head 476b8ae2), written by speed
subagent 3 on 2026-11-20. These are the printouts the PR's notes quote (notes/LOW_D_SPEEDUP.md and LARGE_D_WALL.md).

- `bench_*.txt`: the per-step cost of each Jacobian lane, the fit of the weight w in k^2 + w k.
- `plan_orders_*.txt`: steps and estimated cost per Taylor order on stored states (chain leg 10 at D 256.53 and
  256.85, low D at D 3.0475 M 320 and 3.044375 M 384, and D 73).
- `jac_o_plans_D256.5265.txt`: the octo-double Jacobian timed on the stored plan (order 36) and on the cheapest
  (order 14): medians 163.1 s and 133.1 s, 1.23x.
- `dump_nomod.py`: the `dump_ctx.py` variant with the kernel stubbed out, used to dump contexts without a build.
