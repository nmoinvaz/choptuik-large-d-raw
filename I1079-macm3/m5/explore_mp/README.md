# I1079-macm3/m5/explore_mp: EXPLORATORY extended-precision M = 5 inner solves at the two excited zeros of #1080 (not a reading)

**This folder is exploratory. It is not a reading of #1080 and decides nothing about persistence.** One value per run, no walk.

Machine: macm3 (Apple M3, 24 GB), session `choptuik-macm3-i1080`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1080 (the coordinator's order after the integrator-tolerance results of `../explore/`: float64's rounding floor at level 5, so the M = 5 inner solve is done in extended precision).
Code: branch feat/inner-mp, commit 176daf53a6d2256acd8a31fb5d2f8de28cc371b5 (worktree `~/Source/choptuik-large-d-1080mp`, detached, no tracked changes; the commit message is "value_mp, zero_mp: M harmonics (#1080)"). The coordinator's note: the M = 3 path is bit-identical to the earlier one, and the M = 5 path was being checked on his Mac at the fundamental's M = 5 zero while these runs started. I did not rerun that check.
Environment: venv `~/Source/venv-macm3-1058b` (Python 3.14.3, mpmath 1.3.0 with its pure-Python backend: no gmpy2 in any macm3 venv, so these runs are slower than with it), 1 process per run, 3 runs side by side at nice 10, detached under `caffeinate -is`.

## What runs (`explore_mp.sh`)

```
python3 value_mp.py pointv A WF --M=5 --v=B3,C3,B5,C5       (cwd solver/inner_stokes of the worktree; default r1 0.17, dps 34 and 42, order 40 and 50, iters 8)
```
| run | A, WF | --v (B3, C3, B5, C5) |
|---|---|---|
| x1 | box centre of `../inputs/A_M_box_M3x1E2_h1e-12_w1e-13.json` (full decimal strings) | its B3, C3 and 0, 0 |
| x2 | box centre of `../inputs/A_M_box_M3x2E2_h1e-12_w1e-12.json` | its B3, C3 and 0, 0 |
| x1fm | x1's | 0.889367331, -0.003238748, 0.294548411, 0.011810894: the last level-3 iterate of the float64 `--floor_max=1e-3` start at xi1 0.2 (`../explore/logs/start_x1_xi0.2_fm.log`), to the 9 decimals hier prints; the 1e-11 run ends at the same values |

`mp_args.py NAME` prints the three arguments. Each run prints one JSON line when it ends (nothing before), so progress is the process's CPU time (`memlog_mp.log`, every 120 s). A solve may take an hour or more.

Per run the report (`report_mp.py report`, `logs/report.txt`) gives |r3| and |r5| after the solve (from `r_rest` = Re r_3, Im r_3, Re r_5, Im r_5), R_1 and sig, |R_1|/sig, valued, ymax, calls (at the two precisions), seconds, and the solved v. `valued` is value_mp's own test: |R_1| at least 10 sig, ymax at most 100, and every residual of the rest under 1e-8.

## Files

| file | content |
|---|---|
| `explore_mp.sh`, `mp_args.py`, `report_mp.py`, `memlog_mp.py` | the driver, the arguments, the report (selftest: its |r3|, |r5| split of `r_rest`; swapping the pairs must change it), the sampler |
| `logs/pointv_NAME.log`, `.time` | the command and the JSON line of a run; `/usr/bin/time -l` output (real, user, sys, maximum resident set size) |
| `exits_mp.txt`, `memlog_mp.log` | exits, load and memory |

## Results

(none yet)
