# I966-dh370: #961's two recommended checks and ks_chain3, the order-tied chain with the speed options

Machine: dh370 (Fedora 45, i7-8700, 12 threads, 31 GB), build and venv `~/Source/choptuik-large-d-961` at 40f4b4a5 (main add322ff plus #955).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/966 (posts of the chain on #903 with `ks_chain3` in the first line).

Start of ks_chain3: ks_chain2's base `I903-win2/ks_chain2/leg00_D232.0000_ks291/anm_pin3_D237.7132.npz` (raw 664b8f09, sha256 4ad949aa...dcfd00).

Files are added as the run goes: `run966.sh` (stages), `exits_966.txt`, `mem966.log`, the checks' logs, `ks_chain3/` (the chain).

## 2026-11-21 ~23:00 UTC: leg 14 stopped after the D 263.4862 save, leg 15 restarted with --h_max 0.045 (coordinator's hc)

- Stop: `stop966.sh i966u` at 22:58:35 UTC, TERM to `ks_chain.py` 1212412 then `anm_run.py` 1212413 (it had gone with the driver), unit `i966u` ended 22:58:36; step 25 was in its series (no corrector, no step 25 line in the log). Last accepted base: `ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D263.4862.npz` (D 263.486212892, 22:56:36 UTC; its plan is in the file's meta, 23 steps). The log at the stop: `leg14_anm_run_at_stop_2300.log`; leg 14's command line at the stop: `leg14_args_at_stop966.txt` (earlier copy `leg14_args966.txt`).
- Restart: `NOSTOP=1 bash restart966v.sh` (a --dry first with gates, and a mutant without the h_max change that aborts), unit `i966y` (`run966v.sh chainv`, stage `ks_chain3v`), 22:58:42 UTC, into `ks_chain3b/leg15_D263.4862_ks293/` (ks_chain.py 1446409, anm_run.py 1446410); the command line is `leg15_args966.txt`. Same order (ks 293) and build (code `~/Source/choptuik-large-d-966g` 299728b7, python and hpkernel `~/Source/choptuik-large-d-961/.venv`).
- Diff of leg 15's `anm_run.py` line against leg 14's (everything else equal): state `anm_pin3_D263.4862.npz` for `anm_pin3_D261.1415.npz`; `--h_max 0.045` for `--h_max 2`; `--base_polish 0` added; `--keep_plan 1` for `--keep_plan 0`; `--D_max 273.4862` for `271.1415`; the leg folder. The log's first lines: "the base keeps its stored plan (23 steps)", "base polish skipped (--base_polish 0): the stored state is the base", h_max 0.045.
- Why: step 24 (base D 263.4439) took three attempts and about 2.7 h (a 0.1693 skipped by the bar, a 0.0846 refused after 4840 s, a 0.0423 accepted); xfchecks needs two bases past D 263.5 and the cap is 04:18 UTC. Per-attempt table: `pause_step24_report_final.txt` (made by `pausepost966.py`).
