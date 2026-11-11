# I522-win2: one drifting period or two? A chirp fit of the weak values, and half-unit states in D 216 to 227

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/522 (follows from #521).
Part 1: `chirp_522.py`, analysis only (venv-t177).
Part 2: eleven attempts of a = 0.5 from crawlG's unit states D 216.1312 to 226.1312 (`job_i522.sh`: crawlK's command with `--h_max 0.5 --steps 1 --threads 5`, worktree `D:\choptuik-i446g` at main 14dc386, Python only, venv-t126), four at a time, each followed by `near_null_eq.py --plant=7 --threads=2` (worktree `D:\choptuik-i505` at 0cce81e) on the new state; then the control `--mutate=rows_only` at one of them. Exit codes in `exits.txt`. Results follow in this README.
