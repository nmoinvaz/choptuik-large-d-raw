# D6666m: D 6666's tail resumed, then its k* stage, on mm5 (#1098, part B of dh610's two stopped ladder runs)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098. Written 2026-11-28 03:38 UTC by the clock, before the run, on the coordinator's order of 2026-11-28 03:38 UTC (dh610 was stopped for a move; raw 37e499d20).

Script: raw `69da80285:I1098-mac-a/tools/mm5/d4628k_d6666r_mm5.sh`, blob **20038ad955423dae578db1c6338adde73ecd9eef** (checked after the copy into `ladder/tools3/`; read before it ran). Command, detached, one process: `PYTHONPATH=$HOME/Source/fastmul7-site bash tools3/d4628k_d6666r_mm5.sh B` (10 threads).

**A deviation from the order's command, said first:** the script's part B calls `form_s.py release_ls` without `PYTHONPATH=$SITE` (part A's `kstar_stage.sh` and `d8000tail_mm5.sh`'s `form_s.py` line set it). Without it `form_s.py` imports `hpkernel` from `~/venv-314/lib/python3.14/site-packages` (the 1ccd32ab build, checked: `import hpkernel` prints that path), not fastmul7's `~/Source/fastmul7-site/hpkernel`. The order says the run is on fastmul7, so `PYTHONPATH` is set in the environment of the launch; the script's blob is unchanged. The kernel the run imports is recorded in `D6666m/tail/run.log`'s first line and the commit in its header.

Resume: dh610 released h13 and took h15's outer step 0 (`release_ls_h15_D6666.0000_step.npz`; h15's outer 1 was not finished). `form_s.py release_ls` from that state, `--harm 15,17,19,21,23 --kmax 23 --jac_by 15:qq,17:qq,19:qq,21:qq,23:qq --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 10 --outer 8 --inner_chord 0` into `D6666m/tail`, under `timeout 16h`; then `kmax_rule.py`, then `kstar_stage.sh` (10 threads). The record joins dh610's `release_ls.jsonl` (h13, h15 outer 0) and this run's.

Inputs, copied from raw origin by the script and blob-checked there (all from `I1098-dh610/ladder/D6666/tail/`):

| file | blob |
|---|---|
| `release_ls.jsonl` | 1f40daeec0a741d691cc9399001f42105b34efdb |
| `start.npz` | 292fe1f0f7d022dc3eac1370c81aebfcf4df3824 |
| `release_ls_h15_D6666.0000_step.npz` | a89b97885355fffd9dc103412e2493324d029655 |

Stop rules (the script's): `release_ls` under `timeout 16h`; the k* stage's own 3 h limit on its re-converge; a "job rc" other than 0 ends the part, which is reported and not rerun. Reported: release_ls's first lines and h15 outer 1's start within 20 min, then each harmonic's lines as they come. This folder is pushed at the end.
