# I1033-dh610: the tau-mapped grid at D 3.044375 (hp/tau_map_gain.py, run 5)

dh610 (Fedora 45, i7-12700, 20 threads, 62 GB), https://github.com/nmoinvaz/choptuik-large-d/issues/1033

Code: `perf/tau-map-lowd` at 32e5825d (worktree `~/Source/choptuik-1033`), `notes/LOW_D_SPEEDUP.md` "Step 5, the measurement", "Runs for a Linux runner": run 0, then run 5, then its report. Python: `~/Source/venv-ccc/bin/python` (3.14.10), whose hpkernel is the wheel built from `~/Source/choptuik-large-d-ccc` at hp 76fdcbc9 (perf/cauchy-cache-chunks, multidouble 4.9.0 from perf/dmat-apply-chunks 6dfd5b03, multishoot 3.3.0, multisolver 0.1.1; #1009); `hpkernel.__file__` is recorded in `exits_1033.txt` by the script. 8 threads at nice 10 beside #1003's K 49 and #1021's b21-25 rerun. Inputs from the raw repository at origin/main 5247895e (worktree `~/Source/choptuik-large-d-raw-1033`): `T100-win2/states/lowDhm_x0.000157-0.975_D3.0444_M384.npz` and `_M320.npz`, `I1033-win2/cost2.jsonl` (win2's c(M), so the cost rows compare this machine's calls with win2's c(M)).

| file | what it holds |
|---|---|
| `run1033_run5.sh` | the script: run 0 (selftest, eight controls), run 5 (solve), report; each step capped at 3 times its estimate by `timeout` on its own pid |
| `exits_1033.txt` | start, environment lines and each step's exit and wall seconds |
| `selftest.log`, `control_*.log` | run 0 |
| `report_control_delta.txt` | the report's control (`--mutate delta`, must exit 1) |
| `solve_D3.0444.jsonl`, `solve_D3.0444.log` | run 5's records (one per configuration) and log |
| `states/` | run 5's checkpoints and converged states (`tmap_*`) |
| `report_D3.0444.json`, `report_D3.0444.txt` | the report with `--ref` M 384, `--ref2` M 320 and `--cost` win2's cost2 |
| `memlog_1033.log`, `rss_1033.log` | alert-only memory log of the unit and the solve's RSS every 10 min |
