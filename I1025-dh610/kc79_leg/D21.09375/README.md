# I1025-dh610/kc79_leg/D21.09375: lambda_1 on win2's k_c 79 leg point D 21.09375 (tag l1kc79Lw1025f), window 0.865 to 0.895 around the prediction 0.8804

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-24 04:02 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", and the hc ruling for points past D 20.90625)
lambda_1 on win2's k_c 79 leg at D 21.09375: **predicted 0.8804 +-0.01** (the previous measured root 0.891249 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D21.093750.npy` and record `l1kc79Lw1025f.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). `tag.txt` names the tag.
- Grid centre 0.880 (the multiple of 0.005 nearest 0.8804; 0.0004 away); the scan: 0.865, 0.870, 0.875, 0.880, 0.885, 0.890, 0.895 and a repeat of 0.880. The widening, if there is no robust change: low 0.860, 0.855, 0.850; high 0.900, 0.905, 0.910 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.09375 0.880 0.8804` as the systemd user unit `i1025-leg-21_09375` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.09375 with both controls exit 1; all 8 processes print the record system; the repeat of 0.880 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8804 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; the eight earlier points passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (13%), two or more (7%). The change within 0.01 of 0.8804: 82%; within 0.005: 65%. The measured steps so far are -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344 and -0.008945 against the prediction's -0.0108 and the residuals +0.000120, +0.000951, +0.002234, +0.001041, +0.001370, +0.001338, +0.001494, +0.001849: I expect the root between 0.8810 and 0.8835 (55%).
- The float64 sign agrees with the hybrid at all 8 evaluations (35%; it differed at three points of the last point, at one of the one before, at none of the one before that).
- Each scan point takes 2000 to 3800 s (60%; the last point 2984 to 3341 s, 2356 to 2514 s the point before); the scan runs beside the kc87_d21 scan (8 processes each) and the recount until the kc87_d21 scan ends. The point is done (no widening) within 70 min of the lane's start (65%; the last 57 min).
- The state is on origin by 04:45 UTC (80%; win2's last interval 57.4 min, those before 77 to 80 min; the last state 03:03:45 UTC).

## Status
- 2026-11-24 04:02 UTC: folder and README written; the unit `i1025-leg-21_09375` is started next and waits for the state.
