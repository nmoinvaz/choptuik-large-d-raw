# I1025-dh610/kc79_leg/D21.28125: lambda_1 on win2's k_c 79 leg point D 21.28125 (tag l1kc79Lw1025g), window 0.805 to 0.835 around the prediction 0.8204

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots, and the tag switch to g of 2026-11-24 07:27 UTC with its authorization check). Written 2026-11-24 11:55 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical. **The same D is also a point of win2's far scout (tag i, h 0.0625): `../../kc79_far/D21.28125/`, scanned by the second lane.**

## Order for this point (coordinator t5, #1025 comment of "17:45", the hc ruling for points past D 20.90625, and the hc ruling on the tag at win2's cap restart)
lambda_1 on win2's k_c 79 leg at D 21.28125: **predicted 0.8204 +-0.01** (the previous measured root 0.831157 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report. The state comes from win2's restarted k_c 79 leap under tag **l1kc79Lw1025g** (`tag.txt` is g, as at D 21.1875 to D 21.25): its record file `l1kc79Lw1025g.jsonl` and states are its own.

## This point
- State `sol_l1kc79Lw1025g_D21.281250.npy` and record `l1kc79Lw1025g.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). The g states came 85.0, 81.3 and 76.6 min apart (records 4896, 4711 and 4544 s); win2's far scout now runs beside the leap, so I expect this one about 12:40 to 12:55 UTC.
- Grid centre 0.820 (the multiple of 0.005 nearest 0.8204; 0.0004 away; 0.825 lies 0.0046 away); the scan: 0.805, 0.810, 0.815, 0.820, 0.825, 0.830, 0.835 and a repeat of 0.820. The widening, if there is no robust change: low 0.800, 0.795, 0.790; high 0.840, 0.845, 0.850 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.28125 0.820 0.8204` as the systemd user unit `i1025-leg-21_28125` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`, scan at nice 5; every script reads `tag.txt`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.28125 with both controls exit 1; all 8 processes print the record system; the repeat of 0.820 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- `fetch_point.sh` exits 2 and the lane stops when the g record has no row for D 21.28125 with kc 79 or a blob differs from the commit's.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8204 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (91%), all 8 processes print the record system (92%), the repeat agrees (92%).
- One robust change in the window (84%), none (9%), two or more (7%). The change within 0.01 of 0.8204: 90%; within 0.005: 80%. The measured steps are -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945, -0.009563, -0.009598, -0.009898, -0.010121, -0.010336 and -0.010576 against the prediction's -0.0108, growing by about 0.00024 in size per point; the residuals against the registered predictions are +0.000120, +0.000951, +0.002234, +0.001041, +0.001370, +0.001338, +0.001494, +0.001849, +0.001286, +0.001188, +0.000890, +0.000669, +0.000433 and +0.000257, falling by about 0.00018 a point, so I expect a residual near 0 and the root between 0.8195 and 0.8215 (60%). The bracket is (0.820, 0.825) (60%; the root, if it sits as expected near 0.8203, is 0.0003 from the grid point 0.820, so (0.815, 0.820) is the other likely bracket).
- The float64 sign agrees with the hybrid at all 8 evaluations (20%; it differed at 1 to 3 grid points in each of the last seven points).
- Each scan point takes 1500 to 2600 s (65%; the last point 1802 to 1848 s; the far lane may scan beside this one, which would raise it). The point is done (no widening) within 60 min of the lane's start (70%; the last 31 min).
- The state is on origin by 13:00 UTC (75%).

## Status
- 2026-11-24 11:55 UTC: folder and README written; the unit `i1025-leg-21_28125` is started next and waits for the state.
