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
