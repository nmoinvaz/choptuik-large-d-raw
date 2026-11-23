# I1021-macm3: #1076's fu022mp run on macm3, fu021's guard-blocked points valued with the M = 3 inner solve in mpmath

Machine `macm3` (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1, arm64; runner macm3b). Issues https://github.com/nmoinvaz/choptuik-large-d/issues/1076 and https://github.com/nmoinvaz/choptuik-large-d/issues/1021.
Written 2026-11-23 02:14 UTC, after the run started at 02:13:42 UTC (the coordinator's order came first; this README is the runner's). The driver, its criteria and its checks are the coordinator's, `../I1021-mac/fu022mp/README.md`; this folder holds what the run writes.

## What is here

    I1021-macm3/
      README.md           this file
      fu022mp/            the driver's output (OUT of run_fu022mp.sh): logs/exits.txt (progress), logs/*.log, m3/ (the cache and the recount's files), rows_passN.jsonl
      runner/             the runner's own files: the launcher's output, the launcher pid, the session check

## The run (the coordinator's, hc 2026-11-23 about 02:10 UTC)

- Code: worktree `~/Source/choptuik-inner-mp` of choptuik-large-d, detached at **cc3c58e0ce4de673e77e36f6ed420a00a28cc657** ("value_mp: batch reads --points=, refuses a malformed list; valued needs |r_3| < 1e-8"), `git status --porcelain -- solver` empty.
- Raw clone `~/Source/choptuik-large-d-raw-749p` at origin/main 0f3e5ef915 (I1021-mac/fu022mp/CODE_COMMIT reads cc3c58e0..., run_fu022mp.sh takes 5 arguments, the last a label). The run writes into it; nothing is pulled or reset there while the run lasts. Pushes come from the separate worktree `~/Source/choptuik-large-d-raw-1076p`, with the run's files copied in.
- Python `~/Source/venv-macm3-1058b/bin/python`: 3.14.3, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0.
- Command, from the raw clone's root, in its own session (`launch_1070.py`: double fork and `setsid`, parent launchd, no controlling terminal) under `caffeinate -is`, output in the runner's private folder:

      bash I1021-mac/fu022mp/run_fu022mp.sh ~/Source/choptuik-inner-mp ~/Source/venv-macm3-1058b/bin/python "$PWD" 3 macm3

  3 processes for the valuing; the driver sets 1 thread per BLAS and nices the steps at 10; the recount uses `--procs=4`.
- Launcher pid 98824 (child pids in `runner/session_check_fu022mp.txt`: every chain ends at launchd, no claude, tty ??).
- Memory (the coordinator's correction of 2026-11-22): alerts only. My monitor posts the free memory to the coordinator when available memory is under 2 GiB, free memory under 8% or free disk under 3 GiB, and never stops, kills or signals a process. The driver's own stops (the preflight, a failed step, the cap of 16 h on the recount) apply.
- Reported to the coordinator and pushed here at each milestone: the preflight line, each pass's select line, the value step's last line and each row's |R|/sigma_mp and valued, the recount's exit and unresolved leaves, and prefix_keys' exit.

## Status

| time (UTC) | milestone |
|---|---|
| 02:13:42 | driver started (`logs/exits.txt`: start line, python versions); preflight `value_mp.py check1` running |
| 02:28 | preflight command 1, `value_mp.py check1 --n=1`: PASS at (2.5123456, 1.20654321), 870.0 s: |R_mp - R_f64| 1.824e-06 against the float64 sigma 3.893e-06, |v_mp - v_f64| 2.22e-16, sigma_mp 1.71e-24, |R|/sigma_mp 8.49e+26 |
| 02:50 | preflight command 2, `check1 --mutate=conv`: FAIL as it must, 1365.6 s (|R_mp - R_f64| 5.683e+10, |v_mp - v_f64| 7.43e-02). **Preflight line: `value_mp check1, check1 --mutate=conv exits: 0 1`** (the pass) |
| 02:50:58 | pass 1 select: 8 points without value in 17 unresolved leaves; 0 already run; 8 to run (the driver's README says the 16 sigma-guard leaves are named by 7 points); pass 1 value started, cache 3397 lines |
| 03:45 | pass 1 value, first three rows (valued True each): (3.5266034125, 0.21279321) |R|/sigma_mp 2.02e+19, 2129.2 s; (3.5529706, 0.41279321) 2.6e+19, 2408.1 s; (3.3185956, 0.22529321) 1.09e+20, 2809.4 s. Each point took 35 to 47 min (the driver's README: about 9 to 15 min); 5 points still to run on 3 processes |
| 04:35:01 | **pass 1 value exit 0: "valued 7 of 8 points (skipped 0)"**; 8 rows in `fu022mp/rows_pass1.jsonl`; the seven valued rows are appended to the cache (`fu022mp/m3/points_M3_r0.17.jsonl`: 3404 lines, was 3397). One row is `valued: false`: (3.9123456, 0.20654321), \|R\|/sigma_mp 0.4, 730.2 s. The value step took 1 h 44 min |
| 04:35:02 | **pass 1 recount exit 127: `nice: timeout: No such file or directory`** (`logs/recount_pass1.log`). The driver's recount command is `nice -n 10 timeout 16h python -u argcount.py ...`; macOS has no `timeout` (and no `gtimeout`) on this machine. The recount did not run; the driver left the pass loop. No unresolved-leaf count exists. **Stopped and reported; nothing changed.** |
| 04:35:02 | `prefix_keys.py` fu021 -> fu022mp: exit 0, criterion 4 read as prefix and keys: PASS (the first 3397 lines are fu021's; the 7 later records of old keys are valued `fu: "mp"` rows); `end` line |
| 04:37:24 | **recount of pass 1 by hand** (the coordinator's order: the driver's recount used `timeout`, which macOS lacks): the driver's `argcount.py` line argument for argument, with `capped_run.py 57600` (blob 11f0647b, kept in my I1025 runner folder, not copied into the code worktree) in place of `timeout 16h`, the venv python for both, from `~/Source/choptuik-inner-mp/solver/inner_stokes`, 1 thread per BLAS, nice 10, own session under caffeinate (`runner/hand_recount.sh`; `fu022mp/logs/hand_steps.txt` has the command, start, end and exit; the driver's `recount_pass1.log` and `exits.txt` are left as they are). Log `fu022mp/logs/recount_pass1_hand.log`; expected 1 to 3 h |
| 05:07:36 | **recount of pass 1 by hand: exit 0** (capped_run's: wall 1812 s = 30.2 min, no cap hit; argcount's own 1804 s); **unresolved leaves: 17** (len of the `unresolved` list in `fu022mp/m3/count_M3_fu022mp_pass1_r0.17.json`); 518 leaves after 169 splits, 3333 points, one zero (leaf_sum 1), boundary winding nan. The cache has 3440 lines (was 3404). Against fu021's pass 2 count (`runner/compare_fu021_pass2.txt`): the same 17 unresolved boxes (none new, none gone), the same 518 leaves and 169 splits, the same zero; no leaf changed `ok`, `W` or `depth`; 16 leaves' `minabs` fell (e.g. 717.05 to 103.13, 127865 to 5852.42). Pass 2 is the coordinator's by hand |
