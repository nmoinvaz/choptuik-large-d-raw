# I525-win2: the chirp's hold-out test, sigma_3 and sigma_4's residual structure, and twelve half-unit states below D 216

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/525 (follows from #522).
Part 3 (runs): `run_i525.sh`, one `anm_run.py` chain of twelve steps of a = -0.5 from crawlG D 216.1312 (`--h_max -0.5 --steps 12 --a_grow 1`, 16 threads, worktree `D:\choptuik-i446g` at main 14dc386, Python only, venv-t126), each new state followed by `near_null_eq.py --plant=7 --threads=2` (worktree `D:\choptuik-i505` at 0cce81e), then the control `--mutate=rows_only` at one state. Exit codes in `exits.txt`.
Parts 1 and 2 (analysis only, venv-t177) run beside it. Results follow in this README.
