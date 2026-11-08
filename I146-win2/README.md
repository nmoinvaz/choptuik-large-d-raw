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
