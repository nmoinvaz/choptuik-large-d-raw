# I1084-mac: value_mp's Newton solve at its rounding floor, old code (6b807830) against the floor stop (wip/value-mp-floor)

Machine: mac (Apple M5, 10 cores, 32 GB, macOS 27.0.1); Python 3.14.7, mpmath 1.3.0 (python backend).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1084

Inputs: #1076's cache `I1021-dh610/fu022mp_m3mp/m3/points_M3_r0.17.jsonl` at raw 110637ab (points p1 line 3763,
p2 line 3828, p3 line 3792; each start F_3 from the latest earlier float64 record of the key), and #1080's M = 5 centre
(A 2.726475885672135, wf 1.0156030949093042). The brief's log of that centre (`old_m5_progress.log`) does not record
its start; a first new-code attempt from (0.1444194785, 0.0110874259, 0, 0) gave max|r| 9.2e8 at its first call
(the log: 3.6e-5) and was stopped (`runs/new_m5_wrongstart.*`). Old and new were then both run from the log's solved
v rounded to 10 digits, v0 = 0.1461732092, 0.01423943566, 0.008040315601, 0.001389551001 (`tools/run_m5.sh`).
All runs at nice 10, one process at a time.

Files:
- `tools/`: `probe.py` (the old code under logging wrappers: every residual call, every linear solve, and at each
  Jacobian refresh the step the previous Jacobian would take, with its bits compared), `drive.py` (the new code with
  each solve's trace), `summarize_probe.py`, `compare_rows.py`, `pick_points.py`, the chain scripts.
- `runs/probe_p*.jsonl|out|err`: old code on p1-p3 (`value_point(..., iters=12)` as argcount calls it).
- `runs/new_*.out|err`: new code on p1-p3 and the M = 5 centre (`pointv ... --iters=8` as the old log's run).
- `runs/check_*.log`: `value_mp_floor_check.py` and its controls; `runs/zero_selftest*.log`.
- `old/`: value_mp.py and inner_mp.py at 6b807830 as run.

Results: see the issue's closing comment (and `results.txt`).
