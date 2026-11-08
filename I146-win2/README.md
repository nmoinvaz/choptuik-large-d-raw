# I146-win2: repeat-and-compare loop of win2's arithmetic, 4 h beside #82

Machine: win2 (Windows 11 Pro build 26300, ASRock Z890I Nova WiFi, BIOS 1.38 dated 2024-09-08, Intel Core Ultra 7 265K,
20 cores, AVX2, 2 x 48 GB DDR5 at 4800 MT/s). python-flint / FLINT: 0.9.0 FLINT 3.6.0 (venv choptuik-venv, Python 3.12.8).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/146

`run_i146.sh` is #140's launch in a loop: per round, three lemma 6a(5) copies on the 1e-18 sub-box, the rp = 0.081 control
(the issue #140's 0.079 is refused by the code) and three `amp_flint_par.py 1.10 15 750 640 --procs 1` copies, in parallel,
into `round<k>/`. Worktree `..\choptuik-i140` at origin/main d9fab0b, Normal priority, threads pinned to 1,
`PYTHONFAULTHANDLER=1`, beside #82's twelve processes. `compare_round.py` (with `compare.py`, #140's) runs after each round
against round 1, I140-win2 and I104-win2, appends to `rounds.csv`, and writes `round<k>/compare.txt`. An anomaly copies
that to `ALERT_round<k>.txt`. `driver.txt` has the round start and end times. A memory guard (`util_report.py --guard 15`,
`mem_guard.log`) kills this loop, and only this loop, if free memory falls under 15 GB.

## Result (loop ended 2026-11-08 11:52:32 UTC)

The loop ran from 07:44:38 to 11:52:32 UTC (247.9 min), 25 rounds of 7 processes (175 runs). Every process exited 0 and
every `compare_round.py` exited 0. All 25 rounds hash like round 1, I140-win2 and I104-win2 (`rounds.csv`):

| family | hash (16 hex) |
|---|---|
| lemma 6a(5) rho_6a JSON | 3fd0dba9e72ca8f6 |
| lemma 6a(5) stored B | 0eeb3ffce4507f76 |
| amplitude 1.10 K 15 J 750 640 bits | fd6b5ef2f90d4f55 |
| rp = 0.081 control (rho_6a JSON, must differ) | 1a507cd75a393f3f |

No ALERT file, no crash. The memory guard (15 GB free) never fired; the lowest free memory was 33.5 GB (480 samples at
30 s). P(no fault in 247.9 min) at the issue's rate of 2 process faults per 68 min is exp(-247.9/34) = 6.8e-4.
