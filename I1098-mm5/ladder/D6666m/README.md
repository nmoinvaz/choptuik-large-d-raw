# D6666m: D 6666's tail resumed, then its k* stage, on mm5 (#1098, part B of dh610's two stopped ladder runs)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098. Written 2026-11-28 03:38 UTC by the clock, before the run, on the coordinator's order of 2026-11-28 03:38 UTC (dh610 was stopped for a move; raw 37e499d20).

Script: raw `69da80285:I1098-mac-a/tools/mm5/d4628k_d6666r_mm5.sh`, blob **20038ad955423dae578db1c6338adde73ecd9eef** (checked after the copy into `ladder/tools3/`; read before it ran). Command, detached, one process, started 2026-11-28 03:39:12 UTC (pid 37188): `PYTHONPATH=$HOME/Source/fastmul7-site bash tools3/d4628k_d6666r_mm5.sh B` (10 threads).

**The environment fix, said first (the coordinator confirmed it at 03:40 UTC and corrected the script):** the script as launched, raw `69da80285`, blob **20038ad955423dae578db1c6338adde73ecd9eef**, calls `form_s.py release_ls` in part B without `PYTHONPATH=$SITE` (part A's `kstar_stage.sh` and `d8000tail_mm5.sh`'s `form_s.py` line set it). Without it `form_s.py` imports `hpkernel` from `~/venv-314/lib/python3.14/site-packages` (the 1ccd32ab build; checked: `import hpkernel` prints that path), not fastmul7's `~/Source/fastmul7-site/hpkernel`. The run was launched with `PYTHONPATH=$HOME/Source/fastmul7-site` in its environment (`ps eww` on the running python shows `PYTHONPATH=/Users/nathan/Source/fastmul7-site`, `HP_EXACT_RECIP=1`, `HP_HORIZON_RELAXED=1`), so it runs on fastmul7; the launched script's blob is unchanged. The coordinator's corrected script, raw `68735e257`, blob **847320bec341833470ec07928d7c4a3e70f544d6**, differs from the launched one in one comment and in that line (`PYTHONPATH=$SITE nice -n 10 timeout 16h $PY -u form_s.py release_ls ...`); the running B is not relaunched. Part A is the same under both blobs.

Resume: dh610 released h13 and took h15's outer step 0 (`release_ls_h15_D6666.0000_step.npz`; h15's outer 1 was not finished). `form_s.py release_ls` from that state, `--harm 15,17,19,21,23 --kmax 23 --jac_by 15:qq,17:qq,19:qq,21:qq,23:qq --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 10 --outer 8 --inner_chord 0` into `D6666m/tail`, under `timeout 16h`; then `kmax_rule.py`, then `kstar_stage.sh` (10 threads). The record joins dh610's `release_ls.jsonl` (h13, h15 outer 0) and this run's.

**Step labels (the coordinator confirmed at 03:55 UTC):** dh610's saved \`release_ls_h15_D6666.0000_step.npz\` is the state after its h15 outer step 0 (its record: F 2.963574201335112e-48 to F_new 4.327776599953002e-53, accepted, 12048.9 s). This run counts steps from its own start, so its "h15 outer 0" (first line of \`rls.log\`, started 03:39:13 UTC) is dh610's h15 outer 1, and the harmonics' outer numbers here are shifted by one against dh610's for h15 only. dh610's per-step wall times, for reference: D 6666 h13 outer 0 9273.4 s, h15 outer 0 12048.9 s.

Inputs, copied from raw origin by the script and blob-checked there (all from `I1098-dh610/ladder/D6666/tail/`):

| file | blob |
|---|---|
| `release_ls.jsonl` | 1f40daeec0a741d691cc9399001f42105b34efdb |
| `start.npz` | 292fe1f0f7d022dc3eac1370c81aebfcf4df3824 |
| `release_ls_h15_D6666.0000_step.npz` | a89b97885355fffd9dc103412e2493324d029655 |

Stop rules (the script's): `release_ls` under `timeout 16h`; the k* stage's own 3 h limit on its re-converge; a "job rc" other than 0 ends the part, which is reported and not rerun. Reported: release_ls's first lines and h15 outer 1's start within 20 min, then each harmonic's lines as they come. This folder is pushed at the end.
