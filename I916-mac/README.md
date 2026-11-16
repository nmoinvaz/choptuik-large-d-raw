# I916-mac: the sigma-model kernel at eta = 0.3: the x direction at D 10.5, and the chain from D 9 to 11

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

## Part 2: the chain in D at M = 32 (`run_chain.sh`, `run_polish.sh`, `out/`)

`chain.py --eta 0.3` with `--solver band` for every point, from #913's solution at D 10.5: down to D 9 in steps of
0.0625 (`chain_down.txt`, 24 points), D 10.5 again from the secant through the chain's D 10.375 and 10.4375
(`chain_closure.txt`), up to D 11 (`chain_up.txt`, 8 points), and three points at sigdss's own D (`chain_x*.txt`:
10.475, 10.1, 9.759375). Then one more Newton step (`--tol 1e-30`, `polish_D*.txt`) at the six points that had
stopped between 1e-30 and 1e-28 (D 9.6875, 9.75, 9.8125, 10.1, 10.9375, 11). `gate.log` has the 1-minute load at
every start, 22 to 30.7.

No run failed and no step was halved. 30 of the 35 points took Newton's own short steps only (7 each, about 280 s).
The band solver's resolved and band steps ran at D 10.4375 and 10.375, which had zero-order seeds, and at D 10.875,
10.9375 and 11.

`out/chain_table.txt` is `matter/sigma_ms/chain_table.py <raw clone>` (csv in the repository,
`matter/sigma_ms/data/delta_D_eta0.3.csv`). Its three checks pass:

| check | result |
|---|---|
| every D converged, max \|F\| <= 1e-28 | 36 values of D (35 points and the closure), largest max \|F\| 2.03e-31 after the extra steps |
| closure at D 10.5 against #913's three states, to 1e-20 | largest difference 1.57e-23 (the chain's value is 7.2e-24 from #913's `hi` state) |
| smoothness: third and fourth differences each of one sign, largest fourth below 1% of largest second | 0.28%; the second derivative runs from -5.76e-3 at D 9.06 to -5.7e-4 at D 10.94 |

Its mutations `closure` (1e-19 added at D 10.5) and `kink` (1e-7 added at one grid point) each exit 1.

| D | Delta, kernel | sigdss's Delta (march, prior) | kernel minus sigdss |
|---|---|---|---|
| 9 | 1.164546055264371 | 1.1649451 (m03up, 1e-8) | -3.99e-4 |
| 9.759375 | 1.154489539614204 | 1.1549598 (m03up, 1e-8) | -4.70e-4 |
| 10 | 1.150875101002367 | 1.1545592 (m03up, 1e-8) | -3.68e-3 |
| 10.1 | 1.149332344023925 | 1.1517462 (m03hi, 1e-7) | -2.41e-3 |
| 10.25 | 1.146981042060820 | 1.1486373 (m03hi, 1e-7) | -1.66e-3 |
| 10.475 | 1.143384871611671 | 1.1400188 (m03hi, 1e-7) | +3.37e-3 |
| 10.5 | 1.142980986472450 | 1.1391146 (m03hi, 1e-7) | +3.87e-3 |
| 10.5 | | 1.1125022 (m03up, 1e-8) | +3.05e-2 |
| 10.5625 | 1.141968012549860 | 1.1187049 (m03up, 1e-8) | +2.33e-2 |
| 10.75 | 1.138904641730661 | 1.1299686 (m03hi, 1e-7) | +8.94e-3 |
| 11 | 1.134776574571409 | 1.1174614 (m03hi, 1e-7) | +1.73e-2 |

The kernel's Delta(D) falls smoothly, with slope -0.0116 at D 9 and -0.0166 at D 11. sigdss's values lie above the
kernel's curve from D 9 to 10.25 and below it from D 10.475 on: its offset is not uniform, and it changes sign
between D 10.25 and 10.475.
