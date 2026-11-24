# I1025-dh610/kc79_leg/D21.34375: lambda_1 on win2's k_c 79 leg point D 21.34375 (tag l1kc79Lw1025g), window 0.785 to 0.815 around the prediction 0.7987

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots, and the tag switch to g of 2026-11-24 07:27 UTC with its authorization check). Written 2026-11-24 14:37 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical. **The same D is a shared D of win2's far scout (tag i, h 0.0625): `../../kc79_far/D21.34375/` compares the two states side by side and, by the coordinator's order of 24 Nov (hc), scans the tag i state with this window and this rule too; the two roots are reported together.**

## Order for this point (coordinator t5, #1025 comment of "17:45", the hc ruling for points past D 20.90625, and the hc ruling on the tag at win2's cap restart)
lambda_1 on win2's k_c 79 leg at D 21.34375: **predicted 0.7987 +-0.01** (the previous measured root 0.809549 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report. The state comes from win2's restarted k_c 79 leap under tag **l1kc79Lw1025g** (`tag.txt` is g, as at D 21.1875 to D 21.3125): its record file `l1kc79Lw1025g.jsonl` and states are its own.

## This point
- State `sol_l1kc79Lw1025g_D21.343750.npy` and record `l1kc79Lw1025g.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). The g states came 85.0, 81.3, 76.6, 79.5 and 77.6 min apart (records 4896, 4711, 4544, 4578 and 4584 s); the last landed at 13:59:53 UTC, so I expect this one about 15:15 to 15:25 UTC. The tag i state of this D is on origin since 14:34:00 UTC (win2 commit 9bb1884b).
- Grid centre 0.800 (the multiple of 0.005 nearest 0.7987; 0.0013 away; 0.795 lies 0.0037 away); the scan: 0.785, 0.790, 0.795, 0.800, 0.805, 0.810, 0.815 and a repeat of 0.800. The widening, if there is no robust change: low 0.780, 0.775, 0.770; high 0.820, 0.825, 0.830 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.34375 0.800 0.7987` as the systemd user unit `i1025-leg-21_34375` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`, scan at nice 5; every script reads `tag.txt`). The far lane's tag i scan of the same D starts after the comparison, beside this one (nominal threads: 8 + 8 + the recount's 12 = 28, nice 5, 8 and 10).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.34375 with both controls exit 1; all 8 processes print the record system; the repeat of 0.800 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- `fetch_point.sh` exits 2 and the lane stops when the g record has no row for D 21.34375 with kc 79 or a blob differs from the commit's.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.7987 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (91%), all 8 processes print the record system (92%), the repeat agrees (92%).
- One robust change in the window (84%), none (9%), two or more (7%). The change within 0.01 of 0.7987: 90%; within 0.005: 80%. The last steps are -0.010121, -0.010336, -0.010576, -0.010979 and -0.010629 against the prediction's -0.0108: the growth in their size stopped at the last point, so I expect a step of -0.0105 to -0.0110 and the root between 0.7975 and 0.8005 (60%). The bracket is (0.795, 0.800) (80%; it needs a step larger than 0.009549 in size, and the last eight were; (0.800, 0.805) needs a smaller one).
- The float64 sign agrees with the hybrid at all 8 evaluations (15%; it differed at 1 to 3 grid points in each of the last nine points, at 1 in the last two).
- Each scan point takes 1500 to 2600 s (60%; the last point 1802 to 1921 s; the far lane's tag i scan of this D runs beside this one, which raises it). The point is done (no widening) within 60 min of the lane's start (65%; the last 32 min).
- The state is on origin by 15:30 UTC (80%).

## Status
- 2026-11-24 14:37 UTC: folder and README written; the unit `i1025-leg-21_34375` is started next and waits for the state.
