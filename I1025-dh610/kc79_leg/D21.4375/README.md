# I1025-dh610/kc79_leg/D21.4375: lambda_1 on win2's k_c 79 leg point D 21.4375 (tag l1kc79Lw1025g), window 0.750 to 0.780 around the prediction 0.7656

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots, and the tag switch to g of 2026-11-24 07:27 UTC with its authorization check). Written 2026-11-24 18:10 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical. **This is tag g's last state:** its 12 h cap ends at 19:19:49 UTC and it is not restarted (the coordinator, hc, read at 17:50 UTC), so there is no g point at D 21.46875 and this lane ends here. The far scout (tag i) was stopped at 17:27 UTC (the coordinator): its D 21.4375 is not a state of it (its states are at D 21.28125, 21.34375, 21.40625 and 21.46875).

## Order for this point (coordinator t5, #1025 comment of "17:45", the hc ruling for points past D 20.90625, and the hc ruling on the tag at win2's cap restart)
lambda_1 on win2's k_c 79 leg at D 21.4375: **predicted 0.7656 +-0.01** (the previous measured root 0.776450 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report. The state comes from win2's restarted k_c 79 leap under tag **l1kc79Lw1025g** (`tag.txt` is g, as at D 21.1875 to D 21.40625).

## This point
- State `sol_l1kc79Lw1025g_D21.437500.npy` and record `l1kc79Lw1025g.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). The g states came 85.0, 81.3, 76.6, 79.5, 77.6, 48.2, 77.1 and 78.5 min apart (records 4896, 4711, 4544, 4578, 4584, 2808, 4448 and 4398 s); the last landed at 17:23:41 UTC, so I expect this one about 18:40 to 18:45 UTC (78 min after it gives 18:42), before the cap at 19:19:49 UTC.
- Grid centre 0.765 (the multiple of 0.005 nearest 0.7656; 0.0006 away; 0.770 lies 0.0044 away); the scan: 0.750, 0.755, 0.760, 0.765, 0.770, 0.775, 0.780 and a repeat of 0.765. The widening, if there is no robust change: low 0.745, 0.740, 0.735; high 0.785, 0.790, 0.795 (the side by `leg_read.py widen`).
- Commands: `bash start_point.sh 21.4375 0.765 0.7656` (unit `i1025-leg-21_4375`: waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`, scan at nice 5; every script reads `tag.txt`). Beside it: the recount (12 nominal) and the k_c 95 lane (`../../kc95_d2175/`: its regrid, or from about 18:30 its 7-process scan at nice 10), 12 + 8 + 7 or 8 = 27 or 28 nominal; the far lane's tag i scan of D 21.40625 (8, nice 8) may still run when this state lands (36 nominal for a while), which the coordinator's fifth order allowed by letting it start when the g lane of D 21.40625 ended.

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.4375 with both controls exit 1; all 8 processes print the record system; the repeat of 0.765 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- `fetch_point.sh` exits 2 and the lane stops when the g record has no row for D 21.4375 with kc 79 or a blob differs from the commit's.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.7656 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (91%), all 8 processes print the record system (92%), the repeat agrees (92%).
- One robust change in the window (84%), none (9%), two or more (7%). The change within 0.01 of 0.7656: 90%; within 0.005: 80%. The last steps are -0.010781, -0.011010 and -0.011308 against the prediction's -0.0108 (the residuals against the registered predictions +0.000068, -0.000242 and -0.000550 now drift one way, by about 0.0003 a point), so I expect a step of -0.0112 to -0.0120 and the root between 0.7645 and 0.7665 (55%). The bracket is (0.760, 0.765) (50%) or (0.765, 0.770) (40%): the root, if it sits as expected near 0.7650, is within 0.0005 of the grid point 0.765, and the point is on the line between the two brackets.
- The float64 sign agrees with the hybrid at all 8 evaluations (15%; it differed at 1 to 3 grid points in each of the last twelve points, at 2 in the last one).
- Each scan point takes 1700 to 3200 s (60%; D 21.375 took 1798 to 1879 s alone beside the recount, D 21.40625 took 2230 to 2602 s beside the k_c 95 regrid, D 21.34375 took 4412 to 4611 s beside the tag i scan). The point is done (no widening) within 75 min of the lane's start (65%).

## Result (`summarize_leg.py 21.4375 0.7656` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.750 | + | ++ (True) | + | -2270.2847205537014 | 3247 |
| 0.755 | + | ++ (True) | + | -2271.0742479886885 | 3367 |
| 0.760 | + | ++ (True) | + | -2272.179517382099 | 3056 |
| 0.765 | - | -- (True) | - | -2275.019958402657 | 3142 |
| 0.765 | - | -- (True) | - | -2275.019958402657 | 3612 |
| 0.770 | - | -- (True) | - | -2272.7645825367845 | 3128 |
| 0.775 | - | -- (True) | - | -2272.479129792504 | 3084 |
| 0.780 | - | -- (True) | - | -2272.457129337451 | 3585 |

scan points: 8 evaluations, seconds per point min 3056, median 3194, max 3612, sum 26221; outside 900 to 1900 s: [(0.75, 3247), (0.755, 3367), (0.76, 3056), (0.765, 3142), (0.765, 3612), (0.77, 3128), (0.775, 3084), (0.78, 3585)]
win2's record at D 21.4375: |F| 4.4106466847816965e-10, steps 2641, constraint 0.006318116475782323, Delta 1.1300506230709413, h 0.03125, seconds 4675
float64 sign differs from the hybrid at: []

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D21.4375/scan 0.750 0.780
points 7 in 0.750-0.780; not noise-robust: none
hybrid signs: 0.750+ 0.755+ 0.760+ 0.765- 0.770- 0.775- 0.780-
float64 sign differs from the hybrid sign at: none
repeated points: [(0.765, 'agree')]
  robust change (0.760, 0.765), + to -, det-linear 0.764724, range [0.764531, 0.764724]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.750, - at 0.780
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D21.4375/scan/scan_D21.4375_all.jsonl: lambda [0.765]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.750+ 0.755+ 0.760+ 0.765- 0.770- 0.775- 0.780-
robust changes: 1
   change (0.760, 0.765), + to -, det-linear 0.764724, range [0.764531, 0.764724]
against the prediction 0.7656: change minus prediction -0.000876; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag g state and record at D 21.4375 (record |F| 4.4106466848e-10, 2641 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system. The state and record are of win2's commit efb57790 (2026-11-24 10:39:50 -08:00 = 18:39:50 UTC, 76.2 min after the D 21.40625 state; the record's seconds 4675). The record's row: |F| 4.4106466847816965e-10, steps 2641, Delta 1.1300506230709413, constraint 0.006318116475782323. **This is the tag g leap's last state** (its 12 h cap ended at 19:19:49 UTC and it is not restarted: the coordinator, hc), so the leg lane has no further point.
- **One robust change in the window 0.750 to 0.780:** (0.760, 0.765), "+ to -", det-linear **0.764724**, estimator range [0.764531, 0.764724] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.750, - at 0.780). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.765** is bit-identical (hybrid -, ln|det| -2275.019958402657 in both; `repeat_check.py` PASS).
- **The float64 sign agrees with the hybrid at all 8 evaluations** (the first point since D 21.28125 where it does: it differed at one or two grid points at each of the last seven points).
- **Against the prediction 0.7656 (+-0.01, the previous root 0.776450 minus 0.0108):** -0.000876, within 0.01 and 0.005. No widening. The step from the previous root is -0.011726; the steps have grown in size at each of the last four points (-0.010781, -0.011010, -0.011308, -0.011726), and the residuals against the registered predictions (+0.000068, -0.000242, -0.000550, -0.000876) have drifted one way by about 0.0003 a point, as I expected.
- **Seconds per point: 3056 to 3612 s** (D 21.375: 1798 to 1879 s alone; the tag i scan of D 21.40625 at nice 8 ran beside this scan from 18:41 to 19:11 UTC, the k_c 95 regrid at nice 10 throughout, and the recount). The load average, median over `scan/sampler.log` (120 samples, 18:41:59 to 19:41:49 UTC), was 18.7 (max 26.94), peak RSS per process 1.66 to 1.74 GiB (`/usr/bin/time -v`), MemAvailable at least 44.69 GiB. The lane ran 18:41:00 to 19:42:16 UTC, 61.3 min. The load alert (alert only) did not fire.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (91%), 8 processes with the record system (92%), the repeat agrees (92%) | right |
| one robust change in the window (84%) | right |
| within 0.01 of 0.7656 (90%); within 0.005 (80%) | right (-0.000876) |
| the root between 0.7645 and 0.7665 (55%) | right (0.764724) |
| the bracket is (0.760, 0.765) (50%) | right |
| the float64 sign agrees with the hybrid at all 8 evaluations (15%) | right (agrees at all 8) |
| each scan point 1700 to 3200 s (60%) | WRONG (3056 to 3612 s; 4 of 8 inside) |
| the point done, no widening, within 75 min of the lane's start (65%) | right (61.3 min) |
| (unscored: the g state on origin about 18:40 to 18:45 UTC) | right (18:39:50 UTC, 10 s before the window) |

## Status
- 2026-11-24 18:10 UTC: folder and README written; the unit `i1025-leg-21_4375` is started next and waits for the state.
- 2026-11-24 19:42 UTC: lane done (18:41:00 to 19:42:16 UTC): result and scorecard above, parent row added. Tag g's last point: the leg lane has no further point.
