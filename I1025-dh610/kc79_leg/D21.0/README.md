# I1025-dh610/kc79_leg/D21.0: lambda_1 on win2's k_c 79 leg point D 21.0 (tag l1kc79Lw1025f), window 0.895 to 0.925 around the prediction 0.9082

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-24 00:29 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", and the hc ruling for points past D 20.90625)
lambda_1 on win2's k_c 79 leg at D 21.0: **predicted 0.9082 +-0.01** (the previous measured root 0.918970 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D21.000000.npy` and record `l1kc79Lw1025f.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). `tag.txt` names the tag.
- Grid centre 0.910 (the multiple of 0.005 nearest 0.9082; 0.905 lies 0.0032 away, 0.910 0.0018); the scan: 0.895, 0.900, 0.905, 0.910, 0.915, 0.920, 0.925 and a repeat of 0.910. The widening, if there is no robust change: low 0.890, 0.885, 0.880; high 0.930, 0.935, 0.940 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.0 0.910 0.9082` as the systemd user unit `i1025-leg-21_0` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.0 with both controls exit 1; all 8 processes print the record system; the repeat of 0.910 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.9082 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; the five earlier points passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (13%), two or more (7%). The change within 0.01 of 0.9082: 80%; within 0.005: 60%. The measured steps so far are -0.010169, -0.009717, -0.009793 and -0.009471 against the prediction's -0.0108 and the residuals +0.000120, +0.000951, +0.002234, +0.001041, +0.001370: I expect the root between 0.9083 and 0.9110 (60%).
- Each scan point takes 2200 to 4000 s (60%; the last point 2800 to 3423 s with the d19_k95 gap scan and the recount beside it); the point is done (no widening) within 75 min of the lane's start (70%).
- The state is on origin by 01:05 UTC (75%; win2's cadence 81.3 min, the last state 23:28:40 UTC).

## Status
- 2026-11-24 00:29 UTC: folder and README written; the unit `i1025-leg-21_0` waits for the state (expected about 00:50 UTC).
