# I1055-dh610: Linux checks of PR #1055 (--plan_auto, the Taylor order by the cost of planned steps) against main's build

Machine: dh610 (Fedora 45, i7-12700, 20 threads, 62 GB), runner session claude-me2. PR: https://github.com/nmoinvaz/choptuik-large-d/pull/1055 (branch `perf/plan-auto`, head 2928d458, rebased onto main 4ac62582).
Queued by the coordinator after the D 251.88 run of PR #1054. Nothing here is started until that run has ended and is posted.

The reference build is `~/Source/venv-i1056` (worktree `~/Source/choptuik-large-d-1056` at e208e136, multidouble 5.1.0 / multishoot 4.1.0 / multisolver 0.2.2); #1056 was merged by rebase, so main's `hp/src` and pins should equal e208e136.
The coordinator's check, `git diff --stat e208e136 4ac62582 -- hp/src hp/Cargo.toml hp/Cargo.lock hp/pyproject.toml`, was expected to be empty. It is not: it lists `hp/src/split_tests.rs` (+29 lines, a new `#[test]` `split_inputs_hash`).
`split_tests` is declared `#[cfg(test)]` in `hp/src/lib.rs`, so the release kernel is the same; `run1055.sh` records the diff and the declaration, and stops only if any other file differs.
The PR (against 4ac62582) adds `hp/src/plan_auto.rs`, `hp/src/lib.rs` (+1), `hp/src/python.rs` (+72, `Solver.plan_auto`, `kt`, `set_kt`), `hp/plan_auto_gain.py`, `hp/data/plan_auto/planted.txt`, `--plan_auto` in `anm_run.py`, `lowD_dd.py`, `lowD_highM.py`, and two notes.

Steps (the coordinator's; `run1055.sh`, one at a time at nice 10, each under timeout, from `hp/` of the worktree `~/Source/choptuik-large-d-1055`, `OMP_NUM_THREADS=1`):
1. a worktree at 2928d458, a new venv `~/Source/venv-i1055` (uv, Python 3.14), `PIP_NO_CACHE_DIR=1 python -m pip uninstall -y multidouble`, `hp/build.sh` (time, the unit's memory peak);
2. flag off: `highm_check.py ref --Ms=48,64,80`, `scaled` and `jets`, `--save=` with venv-i1056's python (`REF.json`, `SC.json`, `JETS.json`) and `--compare=` with venv-i1055's, and `jets --compare=JETS.json --mutate=kappa` (must fail). Pass: 0 differing rows;
3. the PR's own planted check `python3 plan_auto_gain.py planted --check data/plan_auto/planted.txt` and its control `--mutate n` (must exit 1), `plan_auto_gain.py selftest` (added, from the note's run 0), and `cargo test --profile release-dev --lib plan_auto -- --nocapture`
   (its tests include the controls `planted_steps_control_n` and `planted_choice_control_invert`).

## Files

| file | what |
|---|---|
| `common1055.sh`, `run1055.sh` | paths and the driver |
| `exits_1055.txt`, `summary_1055.txt`, `memlog_1055.log` | exits with times, the one-line result of every step, the alert-only memory log (no alert) |
| `build1055.log`, `venv.log` | the build (1565 s, unit memory peak 27 709 MiB), pip's direct_url of venv-i1055 (8c4360ac) |
| `REF.json`, `SC.json`, `JETS.json`, `JETS_inputs.npz` | the references saved with venv-i1056 (main's build) |
| `save_*.log`, `cmp_*.log` | the highm_check runs, flag off |
| `planted.log`, `planted_control_n.log`, `selftest.log`, `cargo_test_plan_auto.log` | the PR's planted truth and its control, the report's selftest, the Rust tests |

## Results (19:02 UTC, 20 Nov)

Every step passes: exits as expected, 0 differing rows in the three compares and the kappa control fails (28 of 28 differ), the planted check passes and its `--mutate n` control exits 1, `selftest` passes (12 of 12 faults fire), `cargo test plan_auto`: 5 passed, 3 ignored.
The unit ran 18:09:59 to 19:00:49 UTC (50 min 52 s, 1 h 8 min CPU), journal memory peak 27 GB, no memory alert.
