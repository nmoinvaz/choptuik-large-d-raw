# I916-mac: the sigma-model kernel at eta = 0.3: the x direction at D 10.5, and the chain from D 9 to 11 (in progress)

Machine: mac (Apple M5 Mac). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/916. Code: branch `wip/sa-916`
on main 90fcfe24. The kernel module is the build of #652 (`I652-mac/README.md`), run with python 3.14 and `PYTHONPATH`
at that build's site directory, one process with 2 threads at nice 10, every run behind `gate.sh` (1-minute load below
31 at its start). Local paths are removed from the copies here.

## Part 1: the x direction at D 10.5, M = 32 (`xcheck.py`, `out/xcheck.txt`, `out/xcheck_fixed.txt`, `out/xcheck.json`)

Each variant starts from #913's M = 32 state (`I913-mac/out/sm_hi_D10.5_polish_M32.npz`), plans its Taylor steps, and
takes Newton steps with the exact Jacobian. The 27-node state is that state carried to the new nodes by `renode.py`
(`seeds/`): its max |F| on the 27-node system is 1.20e-31 before any step.

| variant | Taylor steps | max \|F\|, before and after each Newton step | Delta minus the base's |
|---|---|---|---|
| base: 21 nodes, plan tolerance 1e-32 | 123 | 1.05e-31, 1.66e-31 | 0 (Delta 1.142980986472450205537211484) |
| 27 nodes (0.04, 0.13, 0.2, 0.35, 0.45, 0.55 added) | 124 | 1.20e-31, 1.66e-31 | +9.5e-31 |
| plan tolerance 1e-28, re-planned after each step | 96 | 4.30e-29, 3.53e-29, 3.01e-29, 4.11e-29 | +3.6e-23 |
| plan tolerance 1e-28, the plan kept | 96 | 4.30e-29, 1.49e-30, 1.23e-30, 1.76e-30 | +4.7e-24 |
| plan tolerance 1e-24, re-planned (an extra) | 83 | 2.5e-25, 6.0e-19, 2.9e-25, 2.8e-25 | +2.1e-23 |
| plan tolerance 1e-24, the plan kept (an extra) | 83 | 2.5e-25, 2.7e-25, 1.9e-25, 2.9e-25 | -1.1e-21 |

The base's own Newton step moves Delta by -2.7e-23 from the mean of #913's three M = 32 states, which is the level
to which the band lets a converged state fix Delta. So the node set changes Delta by 9.5e-31, and a plan tolerance
10^4 times looser by no more than that level. With the looser tolerance the residual does not reach 1e-30: it stays
at the plan's own error, 1.2e-30 to 4e-29 at 1e-28.

## Part 2: the chain (`run_chain.sh`), running
