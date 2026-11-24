# I1025-dh610/kc79_leg/D21.0625: lambda_1 on win2's k_c 79 leg point D 21.0625 (tag l1kc79Lw1025f), window 0.875 to 0.905 around the prediction 0.8894

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-24 02:52 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", and the hc ruling for points past D 20.90625)
lambda_1 on win2's k_c 79 leg at D 21.0625: **predicted 0.8894 +-0.01** (the previous measured root 0.900194 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D21.062500.npy` and record `l1kc79Lw1025f.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). `tag.txt` names the tag.
- Grid centre 0.890 (the multiple of 0.005 nearest 0.8894; 0.0006 away); the scan: 0.875, 0.880, 0.885, 0.890, 0.895, 0.900, 0.905 and a repeat of 0.890. The widening, if there is no robust change: low 0.870, 0.865, 0.860; high 0.910, 0.915, 0.920 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.0625 0.890 0.8894` as the systemd user unit `i1025-leg-21_0625` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.0625 with both controls exit 1; all 8 processes print the record system; the repeat of 0.890 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8894 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; the seven earlier points passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (13%), two or more (7%). The change within 0.01 of 0.8894: 80%; within 0.005: 62%. The measured steps so far are -0.010169, -0.009717, -0.009793, -0.009471, -0.009432 and -0.009344 against the prediction's -0.0108 and the residuals +0.000120, +0.000951, +0.002234, +0.001041, +0.001370, +0.001338, +0.001494: I expect the root between 0.8900 and 0.8925 (60%).
- The float64 sign agrees with the hybrid at all 8 evaluations (50%; it differed at 0.900 of the last point, agreed at all eight of the one before, and differed at one to two points in each of the five before that).
- Each scan point takes 1800 to 3500 s (60%; the last point 2356 to 2514 s beside the kc87_d21 regrid and the recount; this point's scan will run beside the kc87_d21 scan, 8 processes each, if that lane has reached its scan); the point is done (no widening) within 60 min of the lane's start (65%).
- The state is on origin by 03:45 UTC (80%; win2's cadence 77.6 to 80 min, the last state 02:06:19 UTC).

## Status
- 2026-11-24 02:52 UTC: folder and README written; the unit `i1025-leg-21_0625` is started next and waits for the state (expected about 03:25 UTC).
