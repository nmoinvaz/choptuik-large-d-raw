# I1003-win2: the amplitude series at omega_inf, J 1500 half of #1003 (K 25 pilot, then K 49)

Machine win2 (runner win2b), 8 to 9 worker processes at BelowNormal, venv-i962 (python-flint 0.9.0, mpmath 1.3.0), code `D:\choptuik-i962\solver\inner_amp` at origin/main ec7cfea7.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1003 (the J 1250 half runs on dh610, raw `I1003-dh610/`).
RAW is the raw-data worktree `D:\choptuik-large-d-raw-743` (the live clone `D:\choptuik-large-d-raw` is never pulled).

Commands, from `solver/inner_amp`:

    1. pilot, 1 h cap:  python amp_flint_par.py 1.0 25 1500 1280 --procs 8 --fit phys --mf 6:12 --phys-prec 3840 --out RAW/I1003-win2/pilot_K25_J1500.json
       pass: sigma_0..sigma_12 equal scan45J1500/sigF_w1.0000_K45_J1500_p1280.json's sigma_str to 1e-19 relative (cmp1003.py)
    2. if it passes, 36 h cap:  the same with K 49, --procs 9, --out RAW/I1003-win2/sigF_w1.0000_K49_J1500_p1280.json

Glue (it chains the coordinator's commands and logs their starts and exits in `exits_1003.txt`; nothing here computes a result): `run1003p.sh` (pilot), `run1003k49.sh` (main run), `cmp1003.py`
(read-only: the pass check, with its own controls, `python -I cmp1003.py --selftest REF.json` and `python -I cmp1003.py PILOT.json REF.json 12`).
The JSON is written only at the end of a run, the log (`*.log`) prints each order's time as it goes.

## K 49 J 1500: final (2026-11-20 10:12:33 UTC)

`amp_flint_par.py 1.0 49 1500 1280 --procs 3 --fit phys --mf 6:12 --phys-prec 3840` (main 99363fe8, worktree D:/choptuik-i1003, venv-i962, BelowNormal) ended exit 0 at 10:12:33 UTC 20 Nov, wall 95297 s (26 h 28 min), no cap, the 72 h cap never reached. Final file `sigF_w1.0000_K49_J1500_p1280.json` (J 1500, K 49, 25 sigma values, prec 1280, `seconds` 95293.9; `sigma_err` is inf at every order, as in dh610's J 1250 file), log `sigF_w1.0000_K49_J1500_p1280.log`, per-order partials in `*.partial.json`. Closing checks: `cmp1003.py` against `solver/inner_amp/scan45J1500/sigF_w1.0000_K45_J1500_p1280.json`, N 22, PASS (its selftest control fails as required); sigma_23 and sigma_24 against dh610's `I1003-dh610/sigF_w1.0000_K49_J1250_p1280.json` (raw main 31c90c1a, blob 6ab2e721), read not recomputed: relative differences 6.8e-13 and 3.4e-12, bar 1e-8 (posted on #1003). Helper logs: `mem_1003.log` (tree peak 25.07 GiB at 07:08:57 UTC 20 Nov, lowest free 1.3 GiB at 07:04:54 UTC during win2-build's rustc peak), `orders_1003.log` (no line for order 49: the recorder ended with the python), `notify1003.log`.
- 2026-11-20 15:22:02 UTC: `memalert_win2.sh` (the alert-only machine watch, from 07:10:32 UTC; it never killed or stopped anything) stopped by win2b by exact pid (stop_memalert_at_build_end.sh, after its own log showed rustc under 1 GiB for 6 samples), to keep win2 quiet for #1040's timing check (the coordinator's hc ~14:25 UTC; win2-build agreed to let it run until its build ended). Last sample 15:21:39: free 56.4 GiB, commit 42.2 of 101.5 GiB. Nothing of win2b's runs on win2 now.
