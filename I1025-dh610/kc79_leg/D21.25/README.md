# I1025-dh610/kc79_leg/D21.25: lambda_1 on win2's k_c 79 leg point D 21.25 (tag l1kc79Lw1025g), window 0.815 to 0.845 around the prediction 0.8309

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots, and the tag switch to g of 2026-11-24 07:27 UTC with its authorization check). Written 2026-11-24 10:34 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", the hc ruling for points past D 20.90625, and the hc ruling on the tag at win2's cap restart)
lambda_1 on win2's k_c 79 leg at D 21.25: **predicted 0.8309 +-0.01** (the previous measured root 0.841733 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report. The state comes from win2's restarted k_c 79 leap under tag **l1kc79Lw1025g** (`tag.txt` is g, as at D 21.1875 and D 21.21875; the restart was checked against win2's README, `../README.md`): its record file `l1kc79Lw1025g.jsonl` and states are its own.

## This point
- State `sol_l1kc79Lw1025g_D21.250000.npy` and record `l1kc79Lw1025g.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). The g states came 85 min and 81.3 min apart (records 4896 s and 4711 s), so I expect this one about 11:28 UTC.
- Grid centre 0.830 (the multiple of 0.005 nearest 0.8309; 0.0009 away; 0.835 lies 0.0041 away); the scan: 0.815, 0.820, 0.825, 0.830, 0.835, 0.840, 0.845 and a repeat of 0.830. The widening, if there is no robust change: low 0.810, 0.805, 0.800; high 0.850, 0.855, 0.860 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.25 0.830 0.8309` as the systemd user unit `i1025-leg-21_25` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`; every script reads `tag.txt`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.25 with both controls exit 1; all 8 processes print the record system; the repeat of 0.830 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- `fetch_point.sh` exits 2 and the lane stops when the g record has no row for D 21.25 with kc 79 or a blob differs from the commit's.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8309 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (90%), all 8 processes print the record system (92%), the repeat agrees (92%).
- One robust change in the window (83%), none (10%), two or more (7%). The change within 0.01 of 0.8309: 88%; within 0.005: 78%. The bracket is (0.830, 0.835): 75%.
- The measured steps are -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945, -0.009563, -0.009598, -0.009898, -0.010121 and -0.010336 against the prediction's -0.0108; the residuals against the registered predictions are +0.000120, +0.000951, +0.002234, +0.001041, +0.001370, +0.001338, +0.001494, +0.001849, +0.001286, +0.001188, +0.000890, +0.000669 and +0.000433, falling over the last six, and the steps grow by about 0.0002 in size per point. I expect the root between 0.8300 and 0.8325 (65%).
- The float64 sign agrees with the hybrid at all 8 evaluations (25%; it differed at 1 to 4 grid points in each of the last six points).
- Each scan point takes 1300 to 2300 s (70%; the last point 1527 to 1603 s with the recount beside it). The point is done (no widening) within 50 min of the lane's start (70%; the last 27 min).
- The state is on origin by 11:50 UTC (75%).

## Status
- 2026-11-24 10:34 UTC: folder and README written; the unit `i1025-leg-21_25` is started next and waits for the state.
