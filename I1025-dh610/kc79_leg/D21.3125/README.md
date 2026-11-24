# I1025-dh610/kc79_leg/D21.3125: lambda_1 on win2's k_c 79 leg point D 21.3125 (tag l1kc79Lw1025g), window 0.795 to 0.825 around the prediction 0.8094

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots, and the tag switch to g of 2026-11-24 07:27 UTC with its authorization check). Written 2026-11-24 13:16 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical. This D is not a point of win2's far scout (tag i, h 0.0625: its D are 21.28125, 21.34375, ...), so the far lane has no part in it.

## Order for this point (coordinator t5, #1025 comment of "17:45", the hc ruling for points past D 20.90625, and the hc ruling on the tag at win2's cap restart)
lambda_1 on win2's k_c 79 leg at D 21.3125: **predicted 0.8094 +-0.01** (the previous measured root 0.820178 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report. The state comes from win2's restarted k_c 79 leap under tag **l1kc79Lw1025g** (`tag.txt` is g, as at D 21.1875 to D 21.28125): its record file `l1kc79Lw1025g.jsonl` and states are its own.

## This point
- State `sol_l1kc79Lw1025g_D21.312500.npy` and record `l1kc79Lw1025g.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). The g states came 85.0, 81.3, 76.6 and 79.5 min apart (records 4896, 4711, 4544 and 4578 s); the last landed at 12:42:19 UTC, so I expect this one about 13:58 to 14:08 UTC.
- Grid centre 0.810 (the multiple of 0.005 nearest 0.8094; 0.0006 away; 0.805 lies 0.0044 away); the scan: 0.795, 0.800, 0.805, 0.810, 0.815, 0.820, 0.825 and a repeat of 0.810. The widening, if there is no robust change: low 0.790, 0.785, 0.780; high 0.830, 0.835, 0.840 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.3125 0.810 0.8094` as the systemd user unit `i1025-leg-21_3125` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`, scan at nice 5; every script reads `tag.txt`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.3125 with both controls exit 1; all 8 processes print the record system; the repeat of 0.810 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- `fetch_point.sh` exits 2 and the lane stops when the g record has no row for D 21.3125 with kc 79 or a blob differs from the commit's.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8094 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (91%), all 8 processes print the record system (92%), the repeat agrees (92%).
- One robust change in the window (84%), none (9%), two or more (7%). The change within 0.01 of 0.8094: 90%; within 0.005: 80%. The measured steps are -0.009344, -0.008945, -0.009563, -0.009598, -0.009898, -0.010121, -0.010336, -0.010576 and -0.010979 (the last three steps grew in size by 0.000240 and 0.000403) against the prediction's -0.0108; the residuals against the registered predictions were +0.000433, +0.000257 and -0.000222, so the residual has crossed zero. If the step grows by 0.0003 to 0.0005 again, it is about -0.0113 to -0.0115 and the root about 0.8087 to 0.8090 (residual about -0.0005 to -0.0007); the root between 0.8075 and 0.8105 (60%). The bracket is (0.805, 0.810) (75%; it needs a step between -0.0102 and -0.0152; (0.810, 0.815) needs the step to fall back below 0.0102 in size, but the sizes have grown at every point since D 21.0625: 0.008945, 0.009563, 0.009598, 0.009898, 0.010121, 0.010336, 0.010576, 0.010979).
- The float64 sign agrees with the hybrid at all 8 evaluations (15%; it differed at 1 to 3 grid points in each of the last eight points, at 1 in the last).
- Each scan point takes 1500 to 2600 s (65%; the last point 1800 to 1900 s, with the recount's workers beside). The point is done (no widening) within 60 min of the lane's start (70%; the last 32 min).
- The state is on origin by 14:10 UTC (75%).

## Status
- 2026-11-24 13:16 UTC: folder and README written; the unit `i1025-leg-21_3125` is started next and waits for the state.
