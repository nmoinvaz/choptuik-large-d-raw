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
Delta was still falling by about 8.2e-06 per Jacobian when the arm stopped (jac 0 to 6: 1.027071, 1.027060, 1.027049,
1.027039, 1.027029, 1.027021, 1.027012, with |F| 5.9e-10 down to 3.8e-10), so it had not settled in Delta.

Arm b (D 9, kc 23, reg 0; 21:36:29 to 21:39:15 UTC, exit 0): |F| 3.735e-11 (from 1.130e-07), Delta 1.0270578345,
-2.55e-05 from the kernel and +1.53e-04 from the march, 1670 LM steps. Truncation reading at D 9: |Delta - kernel| is
2.55e-05 for kc 23 against 7.08e-05 for kc 15, a factor 2.78, short of 3, so it does not hold. Delta was still falling
(1.027077 at jac 0 to 1.027058 at jac 6, by 1.7e-06 per Jacobian at the end).

Arm c (D 10, kc 15, reg 0; 21:39:15 to 21:40:13 UTC, exit 0): |F| 2.498e-09 (from 7.647e-07), above the 1e-9 bar, so
it has not converged; Delta 1.0233007072, -1.37e-04 from the kernel's 1.02343724954 and -2.84e-03 from the march's
1.026141550, 1087 LM steps; readings: none. Delta was still falling by about 1.9e-05 per Jacobian when it stopped
(1.023417 at jac 0 to 1.023301 at jac 6, |F| 2.7e-09 down to 2.5e-09, smin/smax 2.2e-11).

Arm d (D 10, kc 15, reg 1e-8; 21:40:13 to 21:41:52 UTC, exit 0): |F| 2.328e-09 (from 7.647e-07), above the 1e-9 bar,
so it has not converged; Delta 1.0232112818, -2.26e-04 from the kernel and -2.93e-03 from the march's 1.026141550,
1086 LM steps. Prior reading at D 10: arm d is 2.93e-03 from the march, arm c 2.84e-03, so it does not hold. The
prior did not change the course: d's Delta and |F| follow c's (jac 6: 1.023300703 and 2.498e-09 against c's
1.023300707 and 2.498e-09), and Delta was still falling by about 1.7e-05 per Jacobian when it stopped.

Arm e (D 10, kc 23, reg 0; 21:41:52 to 21:44:37 UTC, exit 0): |F| 3.785e-10 (from 1.445e-07), Delta 1.0233713474,
-6.59e-05 from the kernel and -2.77e-03 from the march, 1665 LM steps; converged. Delta was still falling by about
8e-06 per Jacobian when it stopped (1.023427 at jac 0 to 1.023371 at jac 6).

## Result (2026-11-15 21:44 UTC, the five arms took 9 min 6 s in all)

| arm | D | kc | reg | seed \|F\| | \|F\| | Delta | Delta - kernel | Delta - march | LM steps | s | converged |
|---|---|---|---|---|---|---|---|---|---|---|---|
| a | 9 | 15 | 0 | 6.109e-07 | 3.839e-10 | 1.0270124764 | -7.084e-05 | +1.081e-04 | 1090 | 58 | yes |
| b | 9 | 23 | 0 | 1.130e-07 | 3.735e-11 | 1.0270578345 | -2.549e-05 | +1.534e-04 | 1670 | 165 | yes |
| c | 10 | 15 | 0 | 7.647e-07 | 2.498e-09 | 1.0233007072 | -1.365e-04 | -2.841e-03 | 1087 | 57 | no |
| d | 10 | 15 | 1e-08 | 7.647e-07 | 2.328e-09 | 1.0232112818 | -2.260e-04 | -2.930e-03 | 1086 | 99 | no |
| e | 10 | 23 | 0 | 1.445e-07 | 3.785e-10 | 1.0233713474 | -6.590e-05 | -2.770e-03 | 1665 | 165 | yes |

The kernel's Delta is 1.02708332095 at D 9 and 1.02343724954 at D 10, the march's 1.026904400 and 1.026141550.

| reading | D 9 | D 10 |
|---|---|---|
| converged (\|F\| <= 1e-9) | a yes (3.8e-10), b yes (3.7e-11) | c no (2.5e-09), d no (2.3e-09), e yes (3.8e-10) |
| same solution (within 1e-6 of the march) | no: a and b are 1.08e-04 and 1.53e-04 from it | none: no kc 15 arm converged, and e is 2.77e-03 from it |
| second solution (kc 15 converged, within 1e-5 of the kernel, 1e-4 or more from the march) | no: a is 7.1e-05 from the kernel | no: c and d did not converge (1.4e-04 and 2.3e-04 from the kernel) |
| truncation (kc 23 closer to the kernel by 3 or more) | no: 2.55e-05 against 7.08e-05, factor 2.78 | e against c: factor 2.07, no; e against d: factor 3.43, yes (neither c nor d converged, d has the prior and e has none) |
| prior (d within 1e-5 of the march, c not) | | no: d is 2.93e-03 from the march, c 2.84e-03 |

Also seen:
- All five arms stopped with Delta still falling steadily, by about 8.2e-06 (a), 1.7e-06 (b), 1.9e-05 (c), 1.7e-05 (d)
  and 8.2e-06 (e) per Jacobian, and |F| falling slowly with it; the logs do not say why they stopped. So each Delta is
  where the walk along the near-null band ended, not a fixed point.
- At D 9 the arms moved from the kernel's Delta toward the march's (by 7.1e-05 and 2.5e-05 of the 1.79e-04 between them).
  At D 10 they moved away from it, the kernel's Delta already being 2.70e-03 below the march's.
- Arm d did 12 Jacobians against the 7 of every other arm. At the same Jacobian their Delta and |F| agree (jac 6: 1.023300703 and 1.023300707),
  so the 9e-05 between c's and d's final Delta is the extra steps, not the prior.
- No check failed and no run crashed (every exit 0 in `exits_846.txt`).

Files: `selftest*.log`, `seed_D*_kc*.log` and `.npy` (the converted seeds), `log_i846?.txt`,
`sigdss_refine_i846?.jsonl` (the arm's record, fields as the solver writes them), `sigdss_sol_ref_i846?_D*.npy` (the
arm's final state), `exits_846.txt`, `run846a.sh` and `run846b.sh`.
