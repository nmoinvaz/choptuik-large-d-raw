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

## Third order: the integrator tolerance (`explore3.sh`, still exploratory)

The coordinator's order after the second results: x1's start at xi1 0.2 with `--floor_max=1e-3` (`--verbose=2`), once with `INNER_NB_RTOL=1e-13` and once with `1e-11`, side by side. The default integrator tolerance is `rtol=1e-12`, `atol=1e-16` (`inner_nb.py` `integrate(..., rtol=1e-12, atol=1e-16)` and `jumps(rtol=1e-12)`; `inner_np.py` the same); `INNER_NB_RTOL` replaces rtol at every `integrate` call and leaves atol. The default's run is the earlier `logs/start_x1_xi0.2_fm.log` (same command, no override). Logs `logs/start_x1_xi0.2_fm_rtol{1e-13,1e-11}.log`, exits `exits_explore3.txt`, table from `rtol_floors.py`.

Reading, the coordinator's, with the thresholds fixed before the run: the stall unchanged with rtol means a float64 floor (the M = 5 route then needs extended precision); a stall that scales with rtol means integrator noise. Level 5 (12 top solves per run, so a range): *unchanged* when the 1e-13 and 1e-11 stall ranges both overlap the default's; *scales* when the 1e-11 range lies wholly above the default's and the 1e-13 range wholly below it; else *mixed*. Level 3 (one stall value): *unchanged* when both are within 3x of the default's 4.56e-4; *scales* when it falls 3x or more at 1e-13 and rises 3x or more at 1e-11; else *mixed*. `rtol_floors.py selftest` runs these two functions on synthetic ranges. K is each run's own table (its finite-difference Jacobian is computed at that rtol).

## Files

| file | content |
|---|---|
| `explore.sh`, `explore2.sh`, `explore3.sh`, `explore_report.py`, `rtol_floors.py`, `explore_probe_report.py`, `probe_floors.py` | the driver, the log reader (`args`, `report`, `selftest`: its parse reproduces the main run's walk JSONs, and a log without its FIXED-A line reads as no result) |
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

### Second order, results (still exploratory)

Run 2026-11-23 17:42:42 to 2026-11-23 17:42:52 UTC (10 s wall) under `caffeinate -is`, all exits 0, no Traceback. `logs/probe_report.md` (from `explore_probe_report.py`) and `logs/probe_floors.txt` (from `probe_floors.py`):

| probe | xi1 | \|r1\| | \|r3\| | \|r5\| | \|F5\|/\|F3\| |
|---|---|---|---|---|---|
| --floor_max=1e-3 (verbose 2) | 0.2 | 3.5e+05 | 4.6e-04 | 3.8e-06 | 0.3315 |
| --verbose=3 | 0.2 | 7.9e+07 | 2.1e+05 | 1.9e-06 | 0.3321 |
| --floor_max=1e-3 (verbose 2) | 0.17 | 7.1e+06 | 8.9e+04 | 6.0e-04 | 0.3329 |
| --verbose=3 | 0.17 | 7.3e+06 | 9.9e+04 | 2.7e-03 | 0.3328 |

xi1 0.2, verbose 3, level 3 trials:
    level 3 (top) it 0 trial lam 1: |r_3| 7.197e+05 against 3.813e+05: rejected
    level 3 (top) it 0 trial lam 0.5: |r_3| 2.101e+05 against 3.813e+05: accepted
xi1 0.2, floor_max, last level-3 iterate (B3, C3, B5, C5): (0.889367331, -0.003238748, 0.294548411, 0.011810894); start (B3, C3) was (0.8054175864, 0.0117800438)
xi1 0.17, verbose 3, level 3 trials:
    level 3 (top) it 0 trial lam 1: |r_3| 1.881e+05 against 3.963e+05: accepted
    level 3 (top) it 1 trial lam 1: |r_3| 9.921e+04 against 1.881e+05: accepted
xi1 0.17, floor_max, last level-3 iterate (B3, C3, B5, C5): (0.898744908, 0.011334493, 0.298759855, 0.016763472); start (B3, C3) was (0.8054175864, 0.0117800438)

xi1 0.2: K_1 1.15e+12  K_3 4.14e+10  K_5 4.78e+08  (max |d r_l / d x_nu| over nu = 3, 5)
  level 5: 12 top solves stopped at |r_5| 5.83e-07 to 3.76e-06; stop / K_5 = 1.2e-15 to 7.9e-15; reasons: a fresh Jacobian no longer halves |g|; every trial rejected with a fresh Jacobian (noise floor); maxit 15
  level 3: 1 top solves stopped at |r_3| 4.56e-04 to 4.56e-04; stop / K_3 = 1.1e-14 to 1.1e-14; reasons: a fresh Jacobian no longer halves |g|
  level 3 iterations: 2.10e+05, 2.41e+04, 7.92e+03, 1.28e+02, 2.35e+00, 7.05e-02, 1.53e-03, 5.97e-04 then the stop
xi1 0.17: K_1 1.83e+15  K_3 3.12e+13  K_5 2.07e+11  (max |d r_l / d x_nu| over nu = 3, 5)
  level 5: 6 top solves stopped at |r_5| 5.99e-04 to 1.69e-03; stop / K_5 = 2.9e-15 to 8.2e-15; reasons: every trial rejected with a fresh Jacobian (noise floor)
  level 3: 1 top solves stopped at |r_3| 8.88e+04 to 8.88e+04; stop / K_3 = 2.8e-09 to 2.8e-09; reasons: every trial rejected with a fresh Jacobian (noise floor)
  level 3 iterations: 1.21e+05, 8.88e+04 then the stop

- **max|Y| and |y(xi1)| are not printed** at `--verbose` 1, 2 or 3: no log in `logs/` or `../logs/` contains them (grep).
- **Why the verbose-1 start stopped at |r_3| 2.1e5:** the level-3 residual was 3.813e5 after the level-5 solve; the trial at lam 1 gave 7.197e5 (rejected), at lam 0.5 gave 2.101e5 (accepted), and with a fresh Jacobian that is not a halving (0.55), so the stop rule ended the solve (xi1 0.2, `_v3`). At xi1 0.17 the first trial (3.963e5 to 1.881e5) and the second (to 9.921e4) were accepted, and the second ended it the same way.
- **With `--floor_max=1e-3` at xi1 0.2 level 3 continues** from 2.1e5 through 2.4e4, 7.9e3, 1.3e2, 2.3, 7.1e-2, 1.5e-3, 6.0e-4 and stops at 4.56e-4 ("a fresh Jacobian no longer halves |g|", below floor_max), after 493 residuals in 5 s. Not under the 1e-6 bar: |r_3| 4.6e-4, |r_5| 3.8e-6. The start harmonics (B3, C3) = (0.8054, 0.0118) move to (0.8894, -0.0032), a change of 10% in B3, at fixed (A, w/w_inf).
- **At xi1 0.17** with `--floor_max` level 5 stops in all six top solves by "every trial rejected with a fresh Jacobian (noise floor)" at 6.0e-4 to 1.7e-3, and level 3 ends at 8.9e4 for the same reason.
- **Consistency with a float64 rounding floor** (not a test of the cause): the stop residual of level 5 divided by the level's sensitivity K_5 (the table `K by level` that `--verbose=2` prints) is 1.2e-15 to 7.9e-15 at xi1 0.2 and 2.9e-15 to 8.2e-15 at 0.17, while K_5 rises from 4.8e8 to 2.1e11 and the stall from 1e-6 to 1e-3. Level 3 at 0.2: 4.56e-4 / K_3 = 1.1e-14. Level 3 at 0.17 is not a clean case, since level 5 beneath it never converged. The ulp of float64 is 1.1e-16.
- Not run (the order ended here): `INNER_NB_RTOL=1e-13`, the integrator tolerance override `inner_nb.py` documents, would test whether the stall moves with the integrator's tolerance.
