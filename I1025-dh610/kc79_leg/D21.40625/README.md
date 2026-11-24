# I1025-dh610/kc79_leg/D21.40625: lambda_1 on win2's k_c 79 leg point D 21.40625 (tag l1kc79Lw1025g), window 0.760 to 0.790 around the prediction 0.7770

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots, and the tag switch to g of 2026-11-24 07:27 UTC with its authorization check). Written 2026-11-24 16:41 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical. **The same D is a shared D of win2's far scout (tag i, h 0.0625; its state is on origin since 15:50:43 UTC, win2 commit 07efddd1): `../../kc79_far/D21.40625/` compares the two states side by side and does not scan the tag i state (the coordinator's order of 24 Nov: only D 21.34375 is scanned at both tags).**

## Order for this point (coordinator t5, #1025 comment of "17:45", the hc ruling for points past D 20.90625, and the hc ruling on the tag at win2's cap restart)
lambda_1 on win2's k_c 79 leg at D 21.40625: **predicted 0.7770 +-0.01** (the previous measured root 0.787758 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report. The state comes from win2's restarted k_c 79 leap under tag **l1kc79Lw1025g** (`tag.txt` is g, as at D 21.1875 to D 21.375).

## This point
- State `sol_l1kc79Lw1025g_D21.406250.npy` and record `l1kc79Lw1025g.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). The g states came 85.0, 81.3, 76.6, 79.5, 77.6, 48.2 and 77.1 min apart (records 4896, 4711, 4544, 4578, 4584, 2808 and 4448 s); the last landed at 16:05:09 UTC, so I expect this one about 17:15 to 17:30 UTC (77 min after it gives 17:22; the short 48 min of D 21.34375 would give 16:53).
- Grid centre 0.775 (the multiple of 0.005 nearest 0.7770; 0.0020 away; 0.780 lies 0.0030 away); the scan: 0.760, 0.765, 0.770, 0.775, 0.780, 0.785, 0.790 and a repeat of 0.775. The widening, if there is no robust change: low 0.755, 0.750, 0.745; high 0.795, 0.800, 0.805 (the side by `leg_read.py widen`).
- Commands: `bash start_point.sh 21.40625 0.775 0.7770` (unit `i1025-leg-21_40625`: waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`, scan at nice 5; every script reads `tag.txt`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.40625 with both controls exit 1; all 8 processes print the record system; the repeat of 0.775 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- `fetch_point.sh` exits 2 and the lane stops when the g record has no row for D 21.40625 with kc 79 or a blob differs from the commit's.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.7770 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (91%), all 8 processes print the record system (92%), the repeat agrees (92%).
- One robust change in the window (84%), none (9%), two or more (7%). The change within 0.01 of 0.7770: 90%; within 0.005: 80%. The last steps are -0.010576, -0.010979, -0.010629, -0.010781 and -0.011010 against the prediction's -0.0108 (the residuals against the registered predictions -0.000222, +0.000149, +0.000068 and -0.000242 are small and change sign), so I expect a step of -0.0105 to -0.0115 and the root between 0.7760 and 0.7780 (60%). The bracket is (0.775, 0.780) (65%; the root, if it sits as expected near 0.7770, is 0.0020 from 0.775 and 0.0030 from 0.780; (0.770, 0.775) needs a step beyond -0.012758 in size, larger than all seventeen so far).
- The float64 sign agrees with the hybrid at all 8 evaluations (15%; it differed at 1 to 3 grid points in each of the last eleven points, at 1 in the last four).
- Each scan point takes 1500 to 2600 s (65%; D 21.375 took 1798 to 1879 s alone beside the recount; the far lane runs no scan here). The point is done (no widening) within 60 min of the lane's start (70%; 31.7 min).

## Status
- 2026-11-24 16:41 UTC: folder and README written; the unit `i1025-leg-21_40625` is started next and waits for the state.
