# D4628m: D 4628's k* stage on mm5 (#1098, part A of dh610's two stopped ladder runs)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098. Written 2026-11-28 03:38 UTC by the clock, before the run, on the coordinator's order of 2026-11-28 03:38 UTC (dh610 was stopped for a move; raw 37e499d20).

Script: raw `69da80285:I1098-mac-a/tools/mm5/d4628k_d6666r_mm5.sh`, blob **20038ad955423dae578db1c6338adde73ecd9eef** (checked with `git hash-object --no-filters` after the copy into `ladder/tools3/`; read before it ran). Command, detached, one process: `bash tools3/d4628k_d6666r_mm5.sh A` (4 threads). It runs `kstar_stage.sh` (tools3 blob 6d29dfc0, checked by the script) on a copy of the tail's `release_ls.jsonl`, h15 and h23 states, into `D4628m/tail/kstar`, on mm5's fastmul7 (`~/Source/choptuik-fastmul7` at d40a9c62, `~/Source/fastmul7-site`, `~/venv-314`; `kstar_stage.sh` sets `PYTHONPATH=$SITE` itself).

Inputs, copied from raw origin by the script and blob-checked there (all from `I1098-dh610/ladder/D4628_x706/tail/`):

| file | blob |
|---|---|
| `release_ls.jsonl` | f4bff4b6cc07c0dbede34975814131fd425c3989 |
| `release_ls_h15_D4628.0000.npz` | c64ef01269c779d465e5a621829f9a41121009cd |
| `release_ls_h23_D4628.0000.npz` | 717aea659cf86342e977fd1f04ab4bedb6f77845 |

dh610 finished the tail to h23 and took the gain (1.186286e33, bound 8.8e-19, so a re-converge), and was stopped one hour into the re-converge. This run starts that re-converge again.

Stop rules (the script's): the k* stage's own 3 h limit on its re-converge; a "job rc" other than 0 ends the part, which is reported and not rerun. Reported: the k* line and the gain within 20 min, then the end (`kstar.json`). This folder is pushed at the end.

## Part A paused by the coordinator's order (noted 2026-11-28 04:38 UTC)

At 04:37 UTC the coordinator reported Nathan's order: every run on dh170, dh370 and mm5 is paused (SIGSTOP on mm5; nothing is resumed, restarted or rerun until told). Part A's re-converge (`form_s.py release_ls`, pid 40710, started 04:06:44 UTC; its last log line `h15 outer 0: target |F| 7.44e-52, harmonic-15 step 1.64e-25 (1530 s)`) is stopped (state T), with its `timeout 3h` (pid 40709) held by the hold guard (`hold_timeouts.log`, pid 40934), so the pause does not end the job. A paused run is not a failure. Nothing was changed.
