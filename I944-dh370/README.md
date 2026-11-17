# I944-dh370: order 160 from D 234.0, --od_weak_first 1 (three builds) and the default at --a0 0.125, none converged

Machine dh370 (Fedora 45, i7-8700, 12 threads). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/944

`run944.sh k160` and `a0125` (units `i944a`, `i944c`, `i944d`, `i944e`, each `RuntimeMaxSec=10800`, 12 threads at nice 10, one run at a time):
worktree `~/Source/choptuik-large-d-935`, its `.venv` (hpkernel with multidouble crate 4.8.2, unchanged by the moves below).
`anm_run.py` from `I903-dh610/chain_k160/anm_pin3_D234.0000.npz`, dh610's chain_k160 flags (`I903-dh610/run903c.sh`, with
`--od_strong 4`, `--ks 160 --keep_plan 1 --D_max 262`), `--steps 1 --od_weak_first 1` (runs 1 to 3) or `--steps 1 --a0 0.125` without the
option (run 4). The control is dh610's logged failure from
that base (a = 1 and 0.5 refused), not rerun.

## Runs

| run | hp (main) | multidouble Python package | outcome | files |
|---|---|---|---|---|
| 1 | d93f5b1b | a93e0896 (pre-fix) | stopped on the coordinator's order 16:51:26 UTC (4602 s), in its a = 0.25 attempt | `k160_weakfirst_d93f5b1b*` |
| 2 | 8c1857ce | a93e0896 (pre-fix) | stopped on the coordinator's order 16:53:05 UTC, 85 s in (the series) | `k160_weakfirst_old_pkg*` (log only) |
| 3 | c714694a | 482c6835 (installed by `pip install --force-reinstall --no-deps`, `pip_multidouble.log`) | killed by `RuntimeMaxSec` at 19:54:05 UTC (10800 s), in its a = 0.25 attempt, Newton iteration 9 | `k160_weakfirst*` |
| 4 | c714694a | 482c6835 | `--a0 0.125`, default corrector (no `--od_weak_first`); stopped on the coordinator's order 21:25:21 UTC (4865 s), in iteration 4, 4 accepted | `k160_a0125*` |

`exits_944.txt` has a start line per run and a line for each stop. Run 3's was written by hand: the wrapper died with the unit, so there
is no `anm_run exit` line (the unit's journal reads "Service reached runtime time limit", in the machine's local time, UTC-8).
Run 4's line in `exits_944.txt` has the trap's text "killed by SIGTERM (the unit limit)", and a hand-written line after it says it was the order.
The a93e0896 to 482c6835 change is `od_axpy` and `od_add_dd`, which the corrector's trials, projections and held offset call.

## Run 3 (`k160_weakfirst.log`)

Series 421 s, then the attempts of the step from D 234.0:

| attempt | what it did | octo-double max\|F\| at its end | wall |
|---|---|---|---|
| a = 1 | the start's projection failed ("rung u 0.3000 not converged at \|R\| 1.82e-05 after 8 steps"), prediction kept | not reached (the prediction's 1.1e+11) | 178 s |
| a = 0.5 | iteration 0: first trial to pass the test was lam 1/64 (ratio 0.984, bound 0.996; lam 1 to 1/32 failed their projections). Iteration 1 (full Newton): lam 1 to 1/64 failed (7.9e+09 down to 2.1e+06), lam 1/128 accepted (ratio 0.992). Then "lam at or below 0.04 twice in a row, stopping (stalled)" | 1.0e-24, not converged, state moved 9.2e-17 | 3149 s |
| a = 0.25 | re-seed ok (72 s), iterations below, the unit's limit hit in iteration 9 | 8.8e-26 after iteration 8 | to the limit |

a = 0.25, iterations (max\|F\| before to after, \|dz\| the Newton step's size before and after, lam the accepted fraction):

| it | max\|F\| | \|dz\| | lam | lam x \|dz\| before | wall (s) |
|---|---|---|---|---|---|
| 0 (weak directions left out) | 2.75e-36 to 7.10e-25 | 1.99e-26 to 1.49e-26 | 0.25 | 5.0e-27 | 853 |
| 1 | 7.10e-25 to 6.21e-25 | 6.79e-16 to 5.94e-16 | 0.125 | 8.5e-17 | 809 |
| 2 | 6.21e-25 to 5.43e-25 | 5.94e-16 to 5.20e-16 | 0.125 | 7.4e-17 | 811 |
| 3 | 5.43e-25 to 4.76e-25 | 5.20e-16 to 4.55e-16 | 0.125 | 6.5e-17 | 816 |
| 4 | 4.76e-25 to 4.16e-25 | 4.55e-16 to 3.98e-16 | 0.125 | 5.7e-17 | 824 |
| 5 | 4.16e-25 to 3.12e-25 | 3.98e-16 to 2.99e-16 | 0.25 | 9.9e-17 | 627 |
| 6 | 3.12e-25 to 2.34e-25 | 2.99e-16 to 2.24e-16 | 0.25 | 7.5e-17 | 638 |
| 7 | 2.34e-25 to 1.76e-25 | 2.24e-16 to 1.68e-16 | 0.25 | 5.6e-17 | 642 |
| 8 | 1.76e-25 to 8.80e-26 | 1.68e-16 to 8.40e-17 | 0.5 | 8.4e-17 | 452 |

Not read from the log: whether iteration 9 would have accepted lam 1. The step accepted at every iteration is between 5.6e-17 and
9.9e-17 long (last column), and iteration 9's full step is 8.4e-17, inside that range, so lam 1 is plausible, followed by the usual
quadratic convergence. That is an extrapolation from the table, untested. The corrector's cap is `--qd_it 20` iterations.

## Run 4 (`k160_a0125.log`), the default at --a0 0.125

Series 422 s, re-seed at a = 0.125 ok (73 s). The strong chord at iteration 0 is refused (max|F| 8.4e+07, theta inf), then the trials:
lam 1 to 1/8 failed their projections, lam 1/16 passes every iteration (ratio 0.9375, bound 0.984).

| it | max\|F\| | \|dz\| | lam | lam x \|dz\| before | wall (s) |
|---|---|---|---|---|---|
| 0 | 3.76e-36 to 4.48e-25 | 1.34e-15 to 1.26e-15 | 1/16 | 8.4e-17 | 1164 |
| 1 | 4.48e-25 to 1.92e-27 | 1.26e-15 to 1.18e-15 | 1/16 | 7.9e-17 | 1003 |
| 2 | 1.92e-27 to 2.62e-27 | 1.18e-15 to 1.10e-15 | 1/16 | 7.4e-17 | 993 |
| 3 | 2.62e-27 to 3.18e-27 | 1.10e-15 to 1.04e-15 | 1/16 | 6.9e-17 | 981 |

The first full step at each a, the prediction's distance to the root along the weak directions:

| a | \|dz\| of the first full step | run |
|---|---|---|
| 0.5 | 1.18e-14 | dh610's default iteration 0 (`I903-dh610/chain_k160.log`), and run 3's iteration 1 |
| 0.25 | 6.79e-16 | run 3, iteration 1 |
| 0.125 | 1.34e-15 | run 4, iteration 0 |

So the distance has a floor near 1e-15 (a 1/17 drop from 0.5 to 0.25, then a rise of 2 to 0.125), and the damped phase has to cover
it at about 8e-17 per iteration. A model of that phase (lam a power of 2, the observed cost per iteration of 1000, 810, 640 and 450 s
at lam 1/16, 1/8, 1/4 and 1/2) puts the full step inside the basin after 4.5 to 5.2 h; that is a model, not a measurement. Measured:
four iterations in 81 min, \|dz\| down 22%.

## Not run

The second stage (the same option from `chain_k160/anm_pin3_D225.0000.npz`, `--steps 1`, to compare with the chain's stored
`anm_pin3_D226.0000.npz`) is ordered only if the D 234.0 step converges. `agree944.py` (`NEW.npz STORED.npz [--mutate delta]`) is ready and
self-tested (`agree944_selftest.log`: D 226 against itself exit 0, `--mutate delta` exit 1), `run944.sh d225` is the run.

## Files

- `run944.sh`, `agree944.py`, `agree944_selftest.log`, `exits_944.txt`, `pip_multidouble.log`
- `k160_weakfirst.log`, `mem_k160_weakfirst.log` (used and free MB per minute), `k160_weakfirst/` (the jet `jet_pin3_D234.0000.npz` and the
  predictions at D 235.0, 234.5 and 234.25), and the same names with `_d93f5b1b` and `_old_pkg` for runs 1 and 2
- `k160_a0125.log`, `mem_k160_a0125.log`, `k160_a0125/` (the jet and the prediction at D 234.125), run 4
