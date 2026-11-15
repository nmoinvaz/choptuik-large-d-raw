# I846-winb: sigdss seeded from the sigma_ms kernel's chain at D 9 and 10, eta = 1

Machine: winb (Surface Laptop 4, Windows 11, Python 3.14.10, numpy 2.5.4, scipy 1.18.1). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/846. Code: main 5063422d (`matter/sigma_ms/to_sigdss.py`,
`solver/matter/sigdss_run.py`), worktree `choptuik-i846`. Inputs: `I652-mac/out/sm_eta1_D9_M32.npz` and
`sm_eta1_D10_M32.npz` (raw 5a3d24b4), read from raw main 86399a4b. One process at a time, below-normal priority,
`OPENBLAS_NUM_THREADS=4`. The launchers are `run846a.sh` (selftests and seeds) and `run846b.sh` (the five refine arms);
`exits_846.txt` has each step's exit code and UTC time.

## Stage 1: the converter (2026-11-15 21:35 UTC)

| step | exit | result |
|---|---|---|
| `--selftest` | 0 | round trip 2.12e-16 (bar 1e-12), PASS |
| `--selftest --mutate=shift` | 1 | 1.11e-2, FAIL as it must |
| `--selftest --mutate=parity` | 1 | 4.52e-1, FAIL as it must |
| seed D 9, kc 15 | 0 | sigdss \|F\| 6.109e-07 (Mac 6.1e-7) |
| seed D 9, kc 23 | 0 | sigdss \|F\| 1.130e-07 (Mac 1.1e-7) |
| seed D 10, kc 15 | 0 | sigdss \|F\| 7.647e-07 (Mac 7.6e-7) |
| seed D 10, kc 23 | 0 | sigdss \|F\| 1.445e-07 (no Mac value) |

All four are below the bar of 1e-5.

## Stage 2: the five refine arms
Arm a (D 9, kc 15, reg 0; 21:35:31 to 21:36:29 UTC, exit 0): |F| 3.839e-10 (from 6.109e-07), Delta 1.0270124764,
-7.08e-05 from the kernel's 1.02708332095 and +1.08e-04 from the march's 1.026904400, 1090 LM steps; readings: none.
Delta was still falling by about 1e-5 per Jacobian when the arm stopped (jac 0 to 6: 1.027071, 1.027060, 1.027049,
1.027039, 1.027029, 1.027021, 1.027012, with |F| 5.9e-10 down to 3.8e-10), so it had not settled in Delta.
(arms b to e follow)
