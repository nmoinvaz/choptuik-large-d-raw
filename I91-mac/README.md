# I91-mac: logs and states of the Reiterer-Trubowitz formulation prototype (solver/rt/) and the Jacobian condition numbers of both formulations

Machine: Apple M5 Mac, a subagent of the coordinator.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/91
Code: branch wip/i91 of nmoinvaz/choptuik-large-d, solver/rt/; the reading is notes/RT_FORMULATION.md there.

- `rt_eqs_check*.log`: solver/rt/rt_eqs_check.py, plain (exit 0) and its two mutations (exit 1).
- `mu_check.log`: solver/rt/mu_check.py on the D = 4 states of T45-win (M 192, 160) and its mutation.
- `planted*.log`: solver/rt/rt_planted.py; `planted_first_run.log` and `planted_second_run.log` are the runs before
  its criteria were revised (the reason is in the script's docstring), `planted.log` the final run, and the
  mutation logs.
- `profiles/`: our hp states' p, m, a, c at Chebyshev points of [0, 1] (gg_to_rt.py profile), the input of the map.
- `D4/`, `cont/`: f64 runs of solver/rt/rt_run.py (resolution study at D = 4, continuation 4 to 10).
- `accept/`: the acceptance runs (rt_run.py --mp 160, plain and --mutate=coef), records, logs and RT states.
- `rt_kappa*.jsonl`: solver/rt/rt_cond.py (f64 condition numbers); `kappa_mp.jsonl`: solver/rt/rt_cond_mp.py (arb).
- `ours_kappa.jsonl`: hp/stall_margin.py on our D = 10 and 20.04 states (hp/data/states of the main checkout).
- `scan/`: solver/rt/rt_scan.py on a 16x21 grid (stopped at D = 6, Newton failed on that grid).
