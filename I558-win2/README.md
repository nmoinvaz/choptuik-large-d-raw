# I558-win2: twelve half-unit states below D 204 with a tighter pre-registered period bound

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/558 (follows from #535).
`run_i558.sh`: one `anm_run.py` chain of twelve steps of a = -0.5 from `I535-win2/down/anm_pin3_D204.1312.npz` (the last state of #535) to D 198.1312 (`--h_max -0.5 --steps 12 --a_grow 1 --a_hold 1`, 16 threads, worktree `D:\choptuik-i446g` at main 14dc386, Python only, venv-t126), each new state followed by `near_null_eq.py --plant=7 --threads=2` (worktree `D:\choptuik-i505` at 0cce81e), then the control `--mutate=rows_only` at D 201.1312. Exit codes in `exits.txt`.
Prediction under test, written on #558 before this run (comment 6815437477): the period of ln sigma_1 over D 198 to 203.6 is 2.365 (bootstrap sd 0.014; the linear drift 2.288, the constant period 2.520), to be within 0.05. Results follow in this README.
