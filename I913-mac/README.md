# I913-mac: sigdss's eta = 0.3 states at D 10.5 on the sigma-model kernel with the band solver, and the control

Machine: mac (Apple M5 Mac). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/913. Code: main e6a574c0
(worktree branch `wip/sa-913`), `matter/sigma_ms/run_eta.py --solver band`. The kernel module is the build of #652
(`I652-mac/README.md`), run with python 3.14 and `PYTHONPATH` at that build's site directory, one process with 2 threads
at nice 10. `run_i913.sh` ran the four starts in turn, each behind `gate.sh` (the 1-minute load at each start is in
`out/gate.log`: 11.6 to 30.7, all below 31). A converged run is followed by a run from its state with `--tol 1e-30`,
which takes one more Newton step if the residual is above that. Local paths are removed from the copies here.

## Result

All three eta = 0.3 starts at D 10.5, M = 32 converge, and to one solution:

| start | sigdss's Delta | iterations | max \|F\| | Delta | after one more Newton step: max \|F\|, Delta |
|---|---|---|---|---|---|
| `hi`: `I897-winb/walk2_hi_10.5.npy` | 1.1373236 | 2 resolved, 6 band | 2.49e-30 | 1.142980986472450205536279 | 1.05e-31, 1.142980986472450205537241 |
| `up`: `I907-winb/walk3_up_10.5.npy` | 1.1257430 | 4 resolved, 7 band, 1 Newton | 4.77e-29 | 1.142980986472450205537233 | 1.17e-31, 1.142980986472450205537250 |
| `march`: section 5's m03hi state, `solver/matter/data/sigdss_sol_m03hi_D10.5000_eta0.3000.npy` | 1.1391146 | 2 resolved, 6 band | 7.02e-30 | 1.142980986472450205528457 | 1.31e-31, 1.142980986472450205537226 |

After the extra step the three agree in Delta to 2.3e-23 (hi - up -8.5e-24, hi - march +1.5e-23, up - march
+2.3e-23), and before it to 8.8e-21. Their mean is 1.14298098647245020553724. The states agree to 2e-19 in c0 and
4e-17 elsewhere, except in the centre datum q (up to 1.1e-15), which the band leaves free. The constraint diagnostic is
8.2e-15.

Control, start B of #845 (eta = 1, D 10.475, sigdss 0.9934860) with the same code: converged in 10 iterations (2
resolved, 6 band, 2 Newton; 18 with #845's first version) at max |F| 1.11e-31, Delta 1.020104800025154887044190, which
is 2.7e-23 from #652's chain (1.020104800025154887044163). Its residual was already below 1e-30, so its second run took
no step.

## Against the f64 solver's numbers (matter/SIGMA_DSS.md sections 5 and 11)

| f64 number at eta = 0.3, D 10.5 | value | the kernel's 1.1429810 minus it |
|---|---|---|
| section 5's march value (m03hi, prior 1e-7; the seed here) | 1.1391146 | +0.0038664 |
| the m03up march value (prior 1e-8) | 1.112502 | +0.030479 |
| the m03hi walk's end (#897) | 1.1373236 | +0.0056574 |
| the m03up walk's end (#907) | 1.1257430 | +0.0172380 |
| Newton's estimate from the m03up end (#907) | 1.137754 | +0.005227 |
| the profile's minimum, sweep B (#910) | 1.136895 | +0.006086 |
| the profile's minimum, sweep A (#910, flat) | 1.133391 | +0.009590 |

The kernel is at M = 32 only. No other M was run here, so its own resolution error at D 10.5 is not measured.

## The band at eta = 0.3

As at eta = 1: 32 singular values below 1e-10 of the largest, 30 below 1e-11, 28 below 1e-12, then a gap to 1e-4
(33 below it). 89% of it lies in q, its largest Delta component is 0.09 to 0.12, and the reduced singular values run
from about 3e-10 to 1e-17. Newton's band step is 1.8 (hi), 6.9 (march) and 14 (up) long when the band steps begin.
Delta after each step, from `sm_records.jsonl`: hi 1.137325, 1.142489, 1.143175, 1.142944, 1.142981; up 1.125710,
1.141159, 1.143267, 1.142971, 1.142803, 1.142980, 1.142981; march 1.139116, 1.142908, 1.143175, 1.142947, 1.142981.
