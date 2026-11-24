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

## Result (`summarize_leg.py 21.40625 0.7770` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.760 | + | ++ (True) | + | -2273.709081663907 | 2392 |
| 0.765 | + | ++ (True) | - | -2274.453115954725 | 2399 |
| 0.770 | + | ++ (True) | + | -2275.4239830113147 | 2531 |
| 0.775 | + | ++ (True) | + | -2277.5105857788535 | 2523 |
| 0.775 | + | ++ (True) | + | -2277.5105857788535 | 2602 |
| 0.780 | - | -- (True) | - | -2276.6155908932888 | 2460 |
| 0.785 | - | -- (True) | + | -2276.1630373244066 | 2436 |
| 0.790 | - | -- (True) | - | -2276.089726865895 | 2230 |

scan points: 8 evaluations, seconds per point min 2230, median 2448, max 2602, sum 19573; outside 900 to 1900 s: [(0.76, 2392), (0.765, 2399), (0.77, 2531), (0.775, 2523), (0.775, 2602), (0.78, 2460), (0.785, 2436), (0.79, 2230)]
win2's record at D 21.40625: |F| 4.441325526387151e-10, steps 2642, constraint 0.0061941693797319146, Delta 1.129200176938387, h 0.03125, seconds 4398
float64 sign differs from the hybrid at: [0.765, 0.785]

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D21.40625/scan 0.760 0.790
points 7 in 0.760-0.790; not noise-robust: none
hybrid signs: 0.760+ 0.765+ 0.770+ 0.775+ 0.780- 0.785- 0.790-
float64 sign differs from the hybrid sign at: [(0.765, '+', '-'), (0.785, '-', '+')]
repeated points: [(0.775, 'agree')]
  robust change (0.775, 0.780), + to -, det-linear 0.776450, range [0.776024, 0.776450]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.760, - at 0.790
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D21.40625/scan/scan_D21.40625_all.jsonl: lambda [0.775]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.760+ 0.765+ 0.770+ 0.775+ 0.780- 0.785- 0.790-
robust changes: 1
   change (0.775, 0.780), + to -, det-linear 0.776450, range [0.776024, 0.776450]
against the prediction 0.777: change minus prediction -0.000550; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag g state and record at D 21.40625 (record |F| 4.4413255264e-10, 2642 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system. The state and record are of win2's commit 64a59f15 (2026-11-24 09:23:41 -08:00 = 17:23:41 UTC, 78.5 min after the D 21.375 state; the record's seconds 4398). The record's row: |F| 4.441325526387151e-10, steps 2642, Delta 1.129200176938387, constraint 0.0061941693797319146. This is the tag g leap's second-to-last state: its 12 h cap ends at 19:19:49 UTC (the coordinator, hc), so D 21.4375 (expected about 18:41 UTC) is the last g point and there is none at D 21.46875.
- **One robust change in the window 0.760 to 0.790:** (0.775, 0.780), "+ to -", det-linear **0.776450**, estimator range [0.776024, 0.776450] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.760, - at 0.790). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.775** is bit-identical (hybrid +, ln|det| -2277.5105857788535 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.765 (below the change) and at 0.785 (above it):** the float64 signs along the grid are + - + + - + -, four changes in float64 against one in the hybrid; the hybrid is read. At D 21.375 it differed at 0.785, below the change; at D 21.34375 at 0.815, above it.
- **Against the prediction 0.7770 (+-0.01, the previous root 0.787758 minus 0.0108):** -0.000550, within 0.01 and 0.005. No widening. The step from the previous root is -0.011308 (the last ones -0.010781 and -0.011010): the steps have grown in size at the last two points.
- **The same D at tag i:** the far scout's state of this D (win2 commit 07efddd1, 15:50:43 UTC; Delta i - g +1.2334e-05) is scanned with this window and rule (the coordinator's fifth order): `../../kc79_far/D21.40625/` (`i/`); the two roots are reported together. It was gated to start after this lane (thread arithmetic: this scan 8 + the k_c 95 regrid 8 + the recount 12 = 28 nominal).
- **Seconds per point: 2230 to 2602 s** (D 21.375: 1798 to 1879 s alone; the k_c 95 regrid, 8 threads at nice 10, ran beside this scan from 17:18 UTC). The load average, median over `scan/sampler.log` (87 samples, 17:25:26 to 18:08:36 UTC), was 17.1 (max 31.03), peak RSS per process 1.67 to 1.76 GiB (`/usr/bin/time -v`), MemAvailable at least 45.92 GiB. The lane ran 17:24:38 to 18:08:51 UTC, 44.2 min.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (91%), 8 processes with the record system (92%), the repeat agrees (92%) | right |
| one robust change in the window (84%) | right |
| within 0.01 of 0.7770 (90%); within 0.005 (80%) | right (-0.000550) |
| the root between 0.7760 and 0.7780 (60%) | right (0.776450) |
| the bracket is (0.775, 0.780) (65%) | right |
| the float64 sign agrees with the hybrid at all 8 evaluations (15%) | WRONG (differs at 0.765 and 0.785) |
| each scan point 1500 to 2600 s (65%) | WRONG (2230 to 2602 s: the repeat of 0.775 took 2602 s, 2 s above the bar; the other seven are inside) |
| the point done, no widening, within 60 min of the lane's start (70%) | right (44.2 min) |
| (unscored: the g state on origin about 17:15 to 17:30 UTC) | right (17:23:41 UTC) |

## Status
- 2026-11-24 16:41 UTC: folder and README written; the unit `i1025-leg-21_40625` is started next and waits for the state.
- 2026-11-24 18:09 UTC: lane done (17:24:38 to 18:08:51 UTC): result and scorecard above, parent row added. The next point is D 21.4375 (`../D21.4375/`), the last tag g point.
