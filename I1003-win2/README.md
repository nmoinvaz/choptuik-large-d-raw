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
