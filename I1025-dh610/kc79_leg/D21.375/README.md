# I1025-dh610/kc79_leg/D21.375: lambda_1 on win2's k_c 79 leg point D 21.375 (tag l1kc79Lw1025g), window 0.775 to 0.805 around the prediction 0.7880

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots, and the tag switch to g of 2026-11-24 07:27 UTC with its authorization check). Written 2026-11-24 16:08 UTC, after the state landed on origin (win2 commit 8eae0ea6, 2026-11-24 08:05:09 -08:00 = 16:05:09 UTC) and before it is pinned and before any run of this folder. The k_c 79 roots are not yet physical. D 21.375 is not a shared D of the far scout (its states are at h 0.0625: 21.28125, 21.34375, 21.40625).

## Order for this point (coordinator t5, #1025 comment of "17:45", the hc ruling for points past D 20.90625, and the hc ruling on the tag at win2's cap restart)
lambda_1 on win2's k_c 79 leg at D 21.375: **predicted 0.7880 +-0.01** (the previous measured root 0.798768 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report. The state comes from win2's restarted k_c 79 leap under tag **l1kc79Lw1025g** (`tag.txt` is g, as at D 21.1875 to D 21.34375).

## This point
- State `sol_l1kc79Lw1025g_D21.375000.npy` and record `l1kc79Lw1025g.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). The g states came 85.0, 81.3, 76.6, 79.5, 77.6, 48.2 and 77.1 min apart; this one's record row: |F| 4.469901080569173e-10, steps 2646, constraint 0.006071772417823825, Delta 1.1283515960867552, h 0.03125, 4448 s.
- Grid centre 0.790 (the multiple of 0.005 nearest 0.7880; 0.0020 away; 0.785 lies 0.0030 away); the scan: 0.775, 0.780, 0.785, 0.790, 0.795, 0.800, 0.805 and a repeat of 0.790. The widening, if there is no robust change: low 0.770, 0.765, 0.760; high 0.810, 0.815, 0.820 (the side by `leg_read.py widen`).
- Commands: `bash start_point.sh 21.375 0.790 0.7880` (unit `i1025-leg-21_375`: pins, pushes the pins, takes the lock, runs `lane_leg.sh`, scan at nice 5; every script reads `tag.txt`). The far lane has no scan running (its next lambda_1 scans start at D 21.53125), so this point runs beside the recount only (8 + 12 nominal threads), as D 21.25 to 21.3125 did.

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.375 with both controls exit 1; all 8 processes print the record system; the repeat of 0.790 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- `fetch_point.sh` exits 2 and the lane stops when the g record has no row for D 21.375 with kc 79 or a blob differs from the commit's.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.7880 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (91%), all 8 processes print the record system (92%), the repeat agrees (92%).
- One robust change in the window (84%), none (9%), two or more (7%). The change within 0.01 of 0.7880: 90%; within 0.005: 80%. The last steps are -0.010336, -0.010576, -0.010979, -0.010629 and -0.010781 against the prediction's -0.0108 (the residuals against the registered predictions +0.000433, +0.000257, -0.000222, +0.000149 and +0.000068 have changed sign twice and are small), so I expect a step of -0.0105 to -0.0110 and the root between 0.7870 and 0.7890 (60%). The bracket is (0.785, 0.790) (80%; it needs a step between -0.008768 and -0.013768, and the last fourteen were all inside that).
- The float64 sign agrees with the hybrid at all 8 evaluations (15%; it differed at 1 to 3 grid points in each of the last ten points, at 1 in the last three).
- Each scan point takes 1500 to 2600 s (65%; D 21.3125 took 1802 to 1921 s alone beside the recount; D 21.34375 took 4412 to 4611 s beside the tag i scan). The point is done (no widening) within 60 min of the lane's start (70%; 32 min alone).

## Status
- 2026-11-24 16:08 UTC: folder and README written; `start_point.sh 21.375 0.790 0.7880` is run next.
