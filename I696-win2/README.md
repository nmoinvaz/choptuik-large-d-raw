# I696-win2: horizon series to ks 300 and 360 at D 245.14 and 253.80, base polishes (#696)

Machine win2 (Windows 11 desktop, 20 threads). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/696, commands in the coordinator's comment 6862225595.

Code: worktree `D:\choptuik-i696` at main 614211ab (`anm_run.py --ks K`), venv-i600 (the #600 fat build). Command: `run_696.sh` (per D, in order r130, r300, r360, p300; both D at once, 5 threads each).
Report: `compare_696.py` (`--selftest` plants the differences and mutates each control; it must pass before the real data is read).
Layout: `D245/` and `D253/` hold `<tag>/` (the run's output, `base_pin3_D*.npz`) and `<tag>.log`; `exits_696.txt` has the start and exit of every run.
