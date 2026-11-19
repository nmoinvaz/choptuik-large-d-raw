# I980-rpi5: the inner selection, stage 4: level 5's approach radius at M = 9

Machine rpi5 (Raspberry Pi 5, Cortex-A76 x 4, 8 GB, aarch64), runner. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/980 (follows #974, #965).
Code: worktree `~/Source/choptuik-large-d-964` fast-forwarded to origin/main adc1f19e (`hier.py --approach=NU:XI`), venv `~/Source/venv-choptuik` (numba 0.68.1).
Started 2026-11-18 23:45 UTC, last run ended 2026-11-19 01:44 UTC (XI 0.095 and 0.105 side by side, then 0.112 and 0.125).

Runs: #974 run 1's command (`INNER_NB_RTOL=1e-13`, no `--floor`, `--verbose=2`) plus `--approach=5:XI`, XI in 0.095, 0.105, 0.112, 0.125, nice 10, 1 h cap each (`run_cap.py`),
two side by side, then the other two; logs `logs/hier_nb_M9_app5_<XI>_rpi5.log`:
`INNER_NB_RTOL=1e-13 python -u hier_nb.py 9 2.719219 1.000022 --x=0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168 --xi1=0.15 --pretune --fixA --schur --predict --procs 2 --h3=1e-4 --verbose=2 --approach=5:XI`
Check per log: `check_radii.py LOG XI` (the 'level radii' line shows r_5 at XI; `--mutate` must exit 1).
Scripts `run_cap.py`, `summarize_M9.py` are copied from `I974-rpi5/`.

Files: `logs/hier_nb_M9_app5_<XI>_rpi5.log` (the whole verbose=2 logs), their `.exit` files, `logs/run980_<XI>.driver.log`, `logs/M9_app5_summary.txt` (`summarize_app5.py`: every level-5 solve per XI),
`logs/check_radii.txt` (`check_radii.py`: r_5 at XI in each log's 'level radii' line, all four ok, `--mutate` exits 1), `launch.sh` (the command).

## Result: no XI takes level 5's first solve below 1e-6, and the polish solve ends at 42.5 for four of the five radii

Level 5's first solve at each approach radius (the 0.1188 row is #974 run 1, the default radius; all with `INNER_NB_RTOL=1e-13`, no `--floor`):

| XI | \|r_5\| at its end | approach solve stopped at \|g\| | polish solve stopped at \|g\| | residuals | seconds |
|---|---|---|---|---|---|
| 0.095 | 42.8 | 50.8 | no stop line | 2853 | 547 |
| 0.105 | **19.6** | no stop line | no stop line | 1027 | 181 |
| 0.112 | 42.5 | 16.6 | 42.5 | 2036 | 380 |
| 0.1188 (default) | 42.7 | 19.6 | 42.7 | 2150 | 407 |
| 0.125 | 42.5 | 23.0 | 42.5 | 1994 | 367 |

- The approach solve's |g| depends on XI (16.6 to 50.8, lowest at 0.112, highest at 0.095), but the first solve's end value does not: 42.5 to 42.8 at four radii. The polish radius is 0.15 for every XI ('level radii': r_5 XI -> 0.1500),
  so the polish solve starts from a different approach state each time and ends at the same |g|. XI 0.105 is the one run that ends lower (19.6); its first two solves are 19.6 and 11.9, and a later one has an approach solve at |g| 1.10 (the lowest of any run) and ends at 8.28.
- Later level-5 solves, the level-3 trials in each run: 0.095: 43.3, 179, 106, 72, 56, 50, 47; 0.105: 11.9, 8.28; 0.112: 43.3, 49.9, 8.61, then 9.9e4 to 1.5e5; 0.125: 42.7, 53.6, 51.2, 50.0, 49.4, 49.1, 48.9.
- Level 3: only 0.112 prints an iteration, `it 0 (lam 0.5)` at |r_3| 9.631e4 (2165 s, after a level-5 solve at 8.61), then the next trial's level-5 solves are at 1e5 and the run hits the 1 h cap at 3600 s. The others end with no accepted level-3 iteration:
  final |r_3| 5.2e5 (0.095, 3529 s), **9.3e4 (0.105, 1281 s)**, 5.3e5 (0.125, 3066 s); #974 run 1 (0.1188) had 5.2e5. None is near the 1e-6 bar, and r_1 is 1e9.
- The M = 9 zero solve (#980's "then") is not run: no XI worked.
- Not established: why the polish solve stops at 42.5. The K ratios of #974 (K[5,7]/K[7,7] 7e3, K[5,9]/K[9,9] 8e8) with level 7 at |r_7| 3e-8 to 4e-5 and level 9 at 2e-10 give a leakage into r_5 of at most about 0.3,
  far below 42.5, so a plain leakage of the converged harmonics 7 and 9 into r_5 does not explain it by that estimate (block maxima, an order of magnitude at best).

## Recommended tasks (one line each; the coordinator files them)

1. **M = 9 level 5, polish radius.** Add `hier.py --polish=NU:XI` (the polish radius of a level, as `--approach` is for the approach) and scan level 5's polish radius (0.15 now; harmonic 9's own polish radius is 0.1246) with the approach at 0.105 and 0.1188; acceptance: a pair at which level 5's first solve ends below 1e-6, or the table shows the polish stop |g| against it. Depends on #980.
2. **Level 5 at the first solve's start.** Print |r_5| at the start and after each trial of the first level-5 solve at verbose 2 (the approach solve's start and its stop, the polish solve's start and its stop), so that where 42.5 arises is in the log; the logs now show only stop lines, and XI 0.105's first solve ends with no stop line. Depends on #980.
