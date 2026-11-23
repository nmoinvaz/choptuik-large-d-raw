# I1079-macm3/m5/explore: EXPLORATORY start solves of #1080 at xi1 0.15 and 0.17, and x1's level 3 at 0.2 with --verbose=2 (not a reading)

**This folder is exploratory. It is not a reading of #1080 and decides nothing about persistence.** No walks: each run is one start solve, the first solve of `../walk1026.py`.

Machine: macm3 (Apple M3, 24 GB), session `choptuik-macm3-i1080`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1080 (the coordinator's order after the result of `../README.md`: the start solve at xi1 0.2 and 0.25 failed for both excited zeros, so the route at 0.2 cannot reach them and persistence is open).
Code and environment as in `../README.md`: main 59f36abc (no tracked changes), venv `~/Source/venv-macm3-i1080`, 2 processes per solve, nice 10, one BLAS thread per process, detached under `caffeinate -is`.

## What runs (`explore.sh`)

Each start solve is
```
hier_nb.py 5 A w --x=B3,C3 --fixA --schur --procs 2 --verbose=V --xi1=XI      (cwd solver/inner_stokes of main)
```
with A, w to 12 decimals and B3, C3 to 10, the same numbers and format as the walks' first solve (`explore_report.py args NAME`; x1, x2 from the box centres, the control from `../run1080.sh`).

| batch | xi1 | starts | --verbose |
|---|---|---|---|
| 1 | 0.15 | x1, x2, control, side by side | 1 |
| 2 | 0.17 | x1, x2, control, side by side | 1 |
| 3 | 0.2 | x1 | 2 |

Report per start: |r_1|, |r_3|, |r_5|, |F_5|/|F_3| (|F_ν/F_1| of the solve), and max|Y| if a log prints it (`explore_report.py report`; hier_nb.py's code has no such line, so it is expected to read "not printed"). The control is not a gate here. The reference at xi1 0.2 is `../logs/fix_*_xi0.2_01.log` (x1 |r_3| 2.1e5, x2 3.3e5, control 2.7e-8).

## Second order: two probes on x1's start (`explore2.sh`, still exploratory)

The coordinator's order after the first results: on x1's start solve at xi1 0.2 and at 0.17, (a) `--floor_max=1e-3` (run at `--verbose=2` so the stop reasons print; the verbose level changes no number) and (b) `--verbose=3` (prints every trial length). Logs `logs/start_x1_xi{0.2,0.17}_fm.log` and `_v3.log`, exits in `exits_explore2.txt`. Also asked: report max|Y| or |y(xi1)| if any log or hier's verbose output gives it (the coordinator's suspicion is float64's rounding floor, 1e-15 |Y|, as in #1021's guard-blocked cells). No walks.

## Files

| file | content |
|---|---|
| `explore.sh`, `explore2.sh`, `explore_report.py` | the driver, the log reader (`args`, `report`, `selftest`: its parse reproduces the main run's walk JSONs, and a log without its FIXED-A line reads as no result) |
| `logs/start_NAME_xiXI[_v2].log`, `exits_explore.txt` | one log per start (first line is the command), exits |
| `logs/report.md` | the table |

## Results

Run 2026-11-23 17:40:05 to 2026-11-23 17:40:21 UTC (16 s wall) under `caffeinate -is`, load 5.50 2.73 2.55 at the start (other work on the machine), no Traceback in any log, no sampler (the run is seconds long). Exits all 0. Seven start solves, no walks. The table is `logs/report.md`.

| start | xi1 | \|r1\| | \|r3\| | \|r5\| | \|F3\| | \|F5\| | \|F5\|/\|F3\| | max\|Y\| |
|---|---|---|---|---|---|---|---|---|
| control | 0.15 | 1.62e+02 | 1.0e-08 | 2.2e-10 | 0.0539 | 0.0030 | 0.0556 | not printed |
| control | 0.17 | 1.37e+02 | 6.0e-09 | 2.7e-10 | 0.0539 | 0.0030 | 0.0556 | not printed |
| x1 | 0.15 | 1.69e+09 | 1.3e+08 | 2.0e+05 | 0.2139 | 0.0653 | 0.3052 | not printed |
| x1 | 0.17 | 7.33e+06 | 9.9e+04 | 2.7e-03 | 0.2586 | 0.0860 | 0.3328 | not printed |
| x1 | 0.2_v2 | 7.88e+07 | 2.1e+05 | 1.9e-06 | 0.2525 | 0.0839 | 0.3321 | not printed |
| x2 | 0.15 | 1.11e+09 | 2.0e+07 | 3.2e+06 | 0.2769 | 0.0076 | 0.0275 | not printed |
| x2 | 0.17 | 3.97e+11 | 6.8e+07 | 4.7e+06 | 0.2769 | 0.0076 | 0.0276 | not printed |

- max|Y| is not printed by `hier_nb.py` at `--verbose` 1 or 2 (the code has no such line).
- The control's start solves converge at xi1 0.15 and 0.17 (|r_3| 1.0e-8 and 6.0e-9), as at 0.2 (2.7e-8).
- x1 and x2 do not converge at 0.15 or 0.17. x1 at 0.17: level 5 ends at 7.3e-4 to 2.7e-3 in its four solves, level 3 at 9.9e4. x2: level 5 does not move from its start at 0.15 and 0.17 (|r_5| 3.2e6 and 4.8e6 before and after), level 3 ends at 2.0e7 and 6.8e7.
- `--verbose=2` on x1 at 0.2 (`logs/start_x1_xi0.2_v2.log`, the same numbers as the verbose-1 start): level 5 ends at |r_5| 2.1e-6, 9.6e-7, 2.9e3 and 1.9e-6 in its four solves; the level-3 solve prints no iteration line and ends with "level 3 (top): stop at |r_3| 2.10e+05: a fresh Jacobian no longer halves |g|" after 142 residuals. That stop is the one `hier.py`'s `--floor_max` comment describes for M = 9 (#1007), and 2.1e5 is far above any noise floor. The log does not show the first step's trial lengths (`--verbose=3` does).
