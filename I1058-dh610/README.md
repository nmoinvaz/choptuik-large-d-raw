# I1058-dh610: dh610's build of hp at main 8179068d (multishoot 4.1.0, multisolver 0.2.2, multidouble 5.1.0) and the four stored-reference checks

Machine: dh610 (Fedora 45, i7-12700, 20 threads, 62 GB), runner session claude-me2. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1058 (the coordinator's 20:18 UTC comment 7049678470 moves the target to main 8179068d).
Queued by the coordinator after #1043's two jobs, which ended at 21:54 UTC (I1054-dh610).

Steps (`run1058.sh`, one at a time at nice 10 from `hp/` of the worktree `~/Source/choptuik-large-d-1058`, detached at 8179068da460fe6be81312602e4c9987d17d73a3; `OMP_NUM_THREADS=1`, `CARGO_BUILD_JOBS=6`; systemd user unit `i1058`, alert-only memory log `memlog_1058.log`):
1. a new venv `~/Source/venv-i1058` (uv, Python 3.14, requirements.txt), `PIP_NO_CACHE_DIR=1 python -m pip uninstall -y multidouble`, `hp/build.sh` (fat LTO; its wall time and the unit's memory peak read from systemd right after it), pip's direct_url of the multidouble package (must name 8c4360ac; control: venv-i1050's, at 482c6835, read by the same test must not).
2. From `hp/`: `highm_check.py ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80` (exit 0), `scaled --compare=$RAW/T81/scaled_main.json` (0), `jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json` (0), the same `jets` with `--mutate=kappa` (1). Pass: 0 differing rows.
3. Also printed, not asked: whether this build's `Solver` has `set_exact_recip` and `plan_auto` (venv-i1054 has the first only, venv-i1056 neither).

Files: `common1058.sh`, `run1058.sh`, `summary_1058.txt`, `exits_1058.txt`, `venv.log`, `build1058.log`, `check_*.log`, `memlog_1058.log`.
