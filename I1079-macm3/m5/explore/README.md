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

## Files

| file | content |
|---|---|
| `explore.sh`, `explore_report.py` | the driver, the log reader (`args`, `report`, `selftest`: its parse reproduces the main run's walk JSONs, and a log without its FIXED-A line reads as no result) |
| `logs/start_NAME_xiXI[_v2].log`, `exits_explore.txt` | one log per start (first line is the command), exits |
| `logs/report.md` | the table |

## Results

(none yet)
