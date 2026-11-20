# I1058-dh610: dh610's build of hp at main 8179068d (multishoot 4.1.0, multisolver 0.2.2, multidouble 5.1.0) and the four stored-reference checks

Machine: dh610 (Fedora 45, i7-12700, 20 threads, 62 GB), runner session claude-me2. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1058 (the coordinator's 20:18 UTC comment 7049678470 moves the target to main 8179068d).
Queued by the coordinator after #1043's two jobs, which ended at 21:54 UTC (I1054-dh610).

Steps (`run1058.sh`, one at a time at nice 10 from `hp/` of the worktree `~/Source/choptuik-large-d-1058`, detached at 8179068da460fe6be81312602e4c9987d17d73a3; `OMP_NUM_THREADS=1`, `CARGO_BUILD_JOBS=6`; systemd user unit `i1058`, alert-only memory log `memlog_1058.log`):
1. a new venv `~/Source/venv-i1058` (uv, Python 3.14, requirements.txt), `PIP_NO_CACHE_DIR=1 python -m pip uninstall -y multidouble`, `hp/build.sh` (fat LTO; its wall time and the unit's memory peak read from systemd right after it), pip's direct_url of the multidouble package (must name 8c4360ac; control: venv-i1050's, at 482c6835, read by the same test must not).
2. From `hp/`: `highm_check.py ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80` (exit 0), `scaled --compare=$RAW/T81/scaled_main.json` (0), `jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json` (0), the same `jets` with `--mutate=kappa` (1). Pass: 0 differing rows.
3. Also printed, not asked: whether this build's `Solver` has `set_exact_recip` and `plan_auto` (venv-i1054 has the first only, venv-i1056 neither).

Files: `common1058.sh`, `run1058.sh`, `summary_1058.txt`, `exits_1058.txt`, `venv.log`, `build1058.log`, `check_*.log`, `memlog_1058.log`.

## Result (20 Nov, 22:34 UTC): built, and the four checks pass

Unit `i1058`, 21:57:03 to 22:33:45 UTC, the machine otherwise idle (load 0.44 at the start). `hp/build.sh` at 8179068da460fe6be81312602e4c9987d17d73a3: exit 0, 1632 s (27.2 min; 21:57:04 to 22:24:16 UTC), the unit's memory peak 27 930 MiB (27.3 GiB; the peak of the venv step and the build, the checks stayed below it), `hpkernel avx2 multidouble avx2`, `_hpkernel` `.so` sha1 d068e2c96428, rustc 1.99.1, maturin 1.16.0, Python 3.14.10. pip's direct_url of multidouble 5.1.0 names 8c4360ac0be804d081faeea524e5c1c6e2fffaaa (the control, venv-i1050's package at 482c6835, read by the same test does not). Checks from `hp/`: `ref` exit 0 (PASS: 72 outputs bit-identical, 43 s), `scaled` exit 0 (PASS, its control fires, 369 s), `jets` exit 0 (PASS: 28 outputs bit-identical, 78 s), `jets --mutate=kappa` exit 1 (FAIL: 28 of 28 outputs differ, 79 s). Stored files sha1 a2c359d8145b, 2d938c93b3a0, ee008fc8d8c5. This build's `Solver` has `set_exact_recip` and `plan_auto` (venv-i1054: the first only; venv-i1056: neither). No memory alert. hp/src's last commit is 428b3ec2 (test modules, an ancestor of 14b2e4c4); hp/src, Cargo.toml, Cargo.lock, pyproject.toml and build.sh at 8179068d equal 14b2e4c4's (empty diff).
