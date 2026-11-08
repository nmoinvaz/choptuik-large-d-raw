# I121-win2: lemma 6b1(5) reproduced on win2

Machine: win2 (Windows 11 Pro build 26300, Intel Core Ultra 7 265K, 20 cores, AVX2, 95.6 GB RAM).
python-flint / FLINT: 0.9.0 FLINT 3.6.0 (venv choptuik-venv, Python 3.12.8, mpmath 1.3.0).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/121

Worktree `..\choptuik-i121` at origin/main 58b048c (contains c282ab8), run from `solver/proof/`, Normal priority, threads
pinned to 1, beside #82's twelve processes. `run_i121.sh` is the issue's cmd commands in bash order: the C1 ray, then the
five `rows` processes in parallel, then `check --json`, `check --drop=9,5` (must fail) and `mutate --j=0` (must certify
no disc). Each exit and wall time is in `exits.txt`. A memory guard (`util_report.py --guard 15`, `mem_guard.log`) kills
this chain, and only this chain, if free memory falls under 15 GB (the coordinator's rule for sharing the machine with #82).
`lemma6b1_runs_M5_cert/` is copied here at the end.

Results (exits in exits.txt):
- The C1 ray exited 0 in 588 s. Rows 0..17 are saved (366 discs), all `ok True`.
- `rows_b` (`--only=1,12,16`) died in row 1 at 06:35:29 UTC (exit 132, SIGILL as Git bash reports it, no traceback, no Windows
  event), which stopped the original chain at "rows failed" (07:17:03). Rows 1, 12 and 16 were rerun as three processes
  (`run_i121_retry_b.sh`, `rows_retry_row*.log`, `PYTHONFAULTHANDLER=1`), all exit 0. The original crashed log is
  `rows_b.log`. Then `run_i121_final.sh` ran the three last commands, as the chain would have.
- `check` exit 0: LEMMA 6b_1 CHECK: PASS (366 tiles glued, 1188 polar rectangles, 957 links). `check --drop=9,5` exit 3:
  FAIL (3 failures), as required. `mutate --j=0` exit 0: 0 of 38 discs certified.
- #121 was suspended from 07:02:01 to 07:05:13 UTC after a native fault in a #82 worker (suspended_pids.txt).
- `rows_table_vs_macm3.md` (from `rows_table_vs_macm3.py`) tabulates max Lam and max box radius per row against
  I38-macm3's, and `lemma6b1_runs_M5_cert/` is the run directory.
