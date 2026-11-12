# I535-win2: twelve half-unit states below D 210 to test the period model

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/535 (follows from #525 and #533).
`run_i535.sh`: one `anm_run.py` chain of twelve steps of a = -0.5 from `I525-win2/down/anm_pin3_D210.1312.npz` (the last state of #525) to D 204.1312 (`--h_max -0.5 --steps 12 --a_grow 1 --a_hold 1`, 16 threads, worktree `D:\choptuik-i446g` at main 14dc386, Python only, venv-t126), each new state followed by `near_null_eq.py --plant=7 --threads=2` (worktree `D:\choptuik-i505` at 0cce81e), then the control `--mutate=rows_only` at D 207.1312. Exit codes in `exits.txt`.
Prediction under test, written on #533 before this run (comment 6813036441): the period of ln sigma_1 over D 204 to 209.6 is 2.404, bootstrap sd 0.021, to be within 0.1. Results follow in this README.
