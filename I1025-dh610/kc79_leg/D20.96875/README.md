# I1025-dh610/kc79_leg/D20.96875: lambda_1 on win2's k_c 79 leg point D 20.96875 (tag l1kc79Lw1025f), window 0.905 to 0.935 around the prediction 0.9176

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-23 23:15 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", and the hc ruling for points past D 20.90625)
lambda_1 on win2's k_c 79 leg at D 20.96875: **predicted 0.9176 +-0.01** (the previous measured root 0.928441 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D20.968750.npy` and record `l1kc79Lw1025f.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). `tag.txt` names the tag.
- Grid centre 0.920 (the multiple of 0.005 nearest 0.9176; 0.915 lies 0.0026 away, 0.920 0.0024); the scan: 0.905, 0.910, 0.915, 0.920, 0.925, 0.930, 0.935 and a repeat of 0.920. The widening, if there is no robust change: low 0.900, 0.895, 0.890; high 0.940, 0.945, 0.950 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 20.96875 0.920 0.9176` as the systemd user unit `i1025-leg-20_96875` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 20.96875 with both controls exit 1; all 8 processes print the record system; the repeat of 0.920 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.9176 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; the four earlier points on tag d and f passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (13%), two or more (7%). The change within 0.01 of 0.9176: 75%; within 0.005: 50%. The measured steps so far are -0.010169, -0.009717 and -0.009793 against the prediction's -0.0108 and the residuals +0.000120, +0.000951, +0.002234, +0.001041: I expect the root between 0.9180 and 0.9235 (60%).
- Each scan point takes 2500 to 4300 s (60%) while the d19_k95 scan (its last point) and the recount run, shorter when the recount runs alone (the earlier points: 1531 to 1825, 2021 to 2474, 3050 to 4171, 3148 to 3965 s); the point is done (no widening) within 75 min of the lane's start (60%).
- The state is on origin by 23:45 UTC (70%; win2's cadence 81.5 min, the last state 22:07:22 UTC).

## Status
- 2026-11-23 23:15 UTC: folder and README written; the unit `i1025-leg-20_96875` waits for the state (expected about 23:30 UTC).
