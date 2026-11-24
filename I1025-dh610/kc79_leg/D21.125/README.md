# I1025-dh610/kc79_leg/D21.125: lambda_1 on win2's k_c 79 leg point D 21.125 (tag l1kc79Lw1025f), window 0.855 to 0.885 around the prediction 0.8709

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-24 05:09 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", and the hc ruling for points past D 20.90625)
lambda_1 on win2's k_c 79 leg at D 21.125: **predicted 0.8709 +-0.01** (the previous measured root 0.881686 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D21.125000.npy` and record `l1kc79Lw1025f.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). `tag.txt` names the tag.
- Grid centre 0.870 (the multiple of 0.005 nearest 0.8709; 0.0009 away); the scan: 0.855, 0.860, 0.865, 0.870, 0.875, 0.880, 0.885 and a repeat of 0.870. The widening, if there is no robust change: low 0.850, 0.845, 0.840; high 0.890, 0.895, 0.900 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.125 0.870 0.8709` as the systemd user unit `i1025-leg-21_125` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.125 with both controls exit 1; all 8 processes print the record system; the repeat of 0.870 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8709 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; the nine earlier points passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (13%), two or more (7%). The change within 0.01 of 0.8709: 83%; within 0.005: 68%. The measured steps so far are -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945 and -0.009563 against the prediction's -0.0108 and the residuals +0.000120, +0.000951, +0.002234, +0.001041, +0.001370, +0.001338, +0.001494, +0.001849, +0.001286: I expect the root between 0.8715 and 0.8740 (55%).
- The float64 sign agrees with the hybrid at all 8 evaluations (30%; it differed at 2 to 3 grid points in the last two points, at one in the one before, at none in the one before that).
- Each scan point takes 1500 to 2800 s (60%; the last point 2098 to 2574 s with the kc87_d21 scan beside it for 24 of its 44 min, D 21.0 1651 to 2137 s with load 14); this scan runs beside the recount only. The point is done (no widening) within 55 min of the lane's start (65%; the last 44 min).
- The state is on origin by 05:50 UTC (80%; win2's last two intervals 57.4 and 77.5 min, the last state 04:21:18 UTC).

## Status
- 2026-11-24 05:09 UTC: folder and README written; the unit `i1025-leg-21_125` is started next and waits for the state.
