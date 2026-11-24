# I1025-dh610/kc79_leg/D21.03125: lambda_1 on win2's k_c 79 leg point D 21.03125 (tag l1kc79Lw1025f), window 0.885 to 0.915 around the prediction 0.8987

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-24 01:24 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", and the hc ruling for points past D 20.90625)
lambda_1 on win2's k_c 79 leg at D 21.03125: **predicted 0.8987 +-0.01** (the previous measured root 0.909538 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D21.031250.npy` and record `l1kc79Lw1025f.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). `tag.txt` names the tag.
- Grid centre 0.900 (the multiple of 0.005 nearest 0.8987; 0.895 lies 0.0037 away, 0.900 0.0013); the scan: 0.885, 0.890, 0.895, 0.900, 0.905, 0.910, 0.915 and a repeat of 0.900. The widening, if there is no robust change: low 0.880, 0.875, 0.870; high 0.920, 0.925, 0.930 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.03125 0.900 0.8987` as the systemd user unit `i1025-leg-21_03125` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.03125 with both controls exit 1; all 8 processes print the record system; the repeat of 0.900 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8987 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; the six earlier points passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (13%), two or more (7%). The change within 0.01 of 0.8987: 80%; within 0.005: 62%. The measured steps so far are -0.010169, -0.009717, -0.009793, -0.009471 and -0.009432 against the prediction's -0.0108 and the residuals +0.000120, +0.000951, +0.002234, +0.001041, +0.001370, +0.001338: I expect the root between 0.8995 and 0.9020 (60%).
- Each scan point takes 1500 to 3500 s (60%; the last point 1651 to 2137 s with the #1081 pool of 5 and the recount beside it; the point before 2800 to 3423 s, and why they differ is not tested); the point is done (no widening) within 60 min of the lane's start (65%).
- The state is on origin by 02:20 UTC (75%; win2's cadence 77.6 min, the last state 00:46:15 UTC).

## Status
- 2026-11-24 01:24 UTC: folder and README written; the unit `i1025-leg-21_03125` waits for the state (expected about 02:05 UTC).
