# I611-mac: #611's continuation check on the Mac: the failure is the equations', not win's build

Machine: the M5 Mac (the coordinator), macOS 27. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/611
Code: choptuik-large-d main ff08351 to be8bfb1 (scan_qd.py unchanged in that range), hp's kernel the #523 build of
I523-mac/c3 (multishoot, exact projector), not win's build from before #523.

## Runs

| file | what | result |
|---|---|---|
| run_diag.sh, diag/diag_tan.stdout, diag/qd_diag_tan*.jsonl | win's `I611-win/diag.cmd`, tangent predictor: kf13_D50 state to D 50.017491, dD 0.01, --kfreeze 13, 3 threads | start converges (9.35e-57); the first step stops with `singular or non-finite pivot at column 0 (NaN)`, as on win |
| run_diag.sh, diag/diag_lag.stdout, diag/qd_diag_lag*.jsonl | the same with the Lagrange predictor (one point: the start itself) | first attempt at dD 0.01: \|F\| 4.40e+11, no trial step accepted; stopped by hand after it, at 20 min per attempt |
| run_diag2.sh, diag/diag_dd.stdout, diag/qd_diag_dd*.jsonl | tangent predictor from hp's own dd state `hp/data/states/up8_D50.0075.npz` instead of win's polish | start converges (9.82e-57, the same Delta); the same NaN pivot |
| diag/*_D50.007491.npz | the converged starts (save_q) | |

## The residual at nearby D (an inline script on the converged start, not a file here)

|F(z, D0 + dD)| at the converged z, the same Taylor segments, kfreeze 13:

| dD | 0 | 1e-10 | 1e-8 | 1e-6 | 1e-4 | 1e-3 | 1e-2 |
|---|---|---|---|---|---|---|---|
| max \|F\| | 1.4e-35 | 1.8e-7 | 1.8e-5 | 1.8e-3 | 0.29 | 8.1e4 | 4.4e11 |

Linear (row 766) to 1e-6, then like a high power of dD (rows 641-647: block 5 of 4M, field a). The double-double
residual (Solver.residual) gives the same values as residual_q at every dD, with and without the cut, and a fresh plan at
D0 + 1e-2 gives the same 4.4e11. So the sensitivity is in the discrete equations, not in either arithmetic, the plan or
win's build. The centre series converges (tail 1e-134 at kc 420, radius 0.61 to 0.69 at D 50, 54, 60).
