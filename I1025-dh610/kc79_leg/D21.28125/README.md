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

## Result (`summarize_leg.py 21.28125 0.8204` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.805 | + | ++ (True) | + | -2289.227880269983 | 1875 |
| 0.810 | + | ++ (True) | + | -2290.007694203365 | 1807 |
| 0.815 | + | ++ (True) | + | -2291.0673896933095 | 1900 |
| 0.820 | + | ++ (True) | + | -2295.174628448419 | 1851 |
| 0.820 | + | ++ (True) | + | -2295.174628448419 | 1889 |
| 0.825 | - | -- (True) | - | -2291.874424566404 | 1800 |
| 0.830 | - | -- (True) | + | -2291.5478917082005 | 1871 |
| 0.835 | - | -- (True) | - | -2291.517722212665 | 1834 |

scan points: 8 evaluations, seconds per point min 1800, median 1861, max 1900, sum 14827; outside 900 to 1900 s: []
win2's record at D 21.28125: |F| 4.5267187993303683e-10, steps 2652, constraint 0.005713642093285211, Delta 1.1258083077444154, h 0.03125, seconds 4578
float64 sign differs from the hybrid at: [0.83]

```
=== read_lower.py D21.28125/scan 0.805 0.835
points 7 in 0.805-0.835; not noise-robust: none
hybrid signs: 0.805+ 0.810+ 0.815+ 0.820+ 0.825- 0.830- 0.835-
float64 sign differs from the hybrid sign at: [(0.83, '-', '+')]
repeated points: [(0.82, 'agree')]
  robust change (0.820, 0.825), + to -, det-linear 0.820178, range [0.820115, 0.820178]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.805, - at 0.835
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check D21.28125/scan/scan_D21.28125_all.jsonl: lambda [0.82]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.805+ 0.810+ 0.815+ 0.820+ 0.825- 0.830- 0.835-
robust changes: 1
   change (0.820, 0.825), + to -, det-linear 0.820178, range [0.820115, 0.820178]
against the prediction 0.8204: change minus prediction -0.000222; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag g state and record at D 21.28125 (record |F| 4.5267187993e-10, the state's 4.5326701826e-10, 2652 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system. The state and record are of win2's commit 6e781f4d (2026-11-24 04:42:19 -08:00 = 12:42:19 UTC, 79.5 min after the D 21.25 state; the record's seconds 4578). The g record's rows run on: |F| 4.564782766290151e-10, 4.5485512502509616e-10, 4.5267187993303683e-10, steps 2658, 2656, 2652, Delta 1.1241182782455752, 1.1249625860927213, 1.1258083077444154, constraint 0.005597282453435274 at D 21.25 and 0.005713642093285211 here.
- **One robust change in the window 0.805 to 0.835:** (0.820, 0.825), "+ to -", det-linear **0.820178**, estimator range [0.820115, 0.820178] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.805, - at 0.835). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.820** (p3 and p7) is bit-identical (hybrid +, ln|det| -2295.174628448419 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.830, above the change:** the float64 signs along the grid are + + + + - + -, so float64 alone would read three changes in the window. The hybrid is read (one change, in (0.820, 0.825)). At D 21.25 it differed at 0.835, 0.840 and 0.845, above the change; at D 21.21875 at 0.835 and 0.840, below the change; at D 21.1875 at 0.860.
- **Against the prediction 0.8204 (+-0.01, the previous root 0.831157 minus 0.0108):** -0.000222, within 0.01 (and within 0.005). No widening was needed. The residual against the registered predictions changes sign here, after falling from +0.000433 and +0.000257.
- **Roots on the leg so far (det-linear, as measured):** 0.958120 (D 20.84375), 0.947951 (D 20.875), 0.938234 (D 20.90625), 0.928441 (D 20.9375), 0.918970 (D 20.96875), 0.909538 (D 21.0), 0.900194 (D 21.03125), 0.891249 (D 21.0625), 0.881686 (D 21.09375), 0.872088 (D 21.125), 0.862190 (D 21.15625), 0.852069 (D 21.1875), 0.841733 (D 21.21875), 0.831157 (D 21.25), 0.820178 (D 21.28125): steps -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945, -0.009563, -0.009598, -0.009898, -0.010121, -0.010336, -0.010576 and -0.010979 per 0.03125 in D, against the order's -0.0108.
- **Seconds per point:** 1800 to 1900 s (D 21.25: 1802 to 1848 s). The load average, median over `scan/sampler.log` (63 samples), was 10.0 (max 10.34; 8 processes here at nice 5, and the recount's workers, restarted 12:01 UTC as i1076d, beside them), peak RSS per process 1.65 to 1.76 GiB (`/usr/bin/time -v`), MemAvailable at least 48.35 GiB.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (91%), 8 processes with the record system (92%), the repeat agrees (92%) | right |
| one robust change in the window (84%) | right |
| within 0.01 of 0.8204 (90%); within 0.005 (80%) | right (-0.000222) |
| the bracket is (0.820, 0.825) (60%) | right |
| the root between 0.8195 and 0.8215 (60%) | right (0.820178) |
| the float64 sign agrees with the hybrid at all 8 evaluations (20%) | WRONG (differs at 0.830) |
| each scan point 1500 to 2600 s (65%) | right (1800 to 1900 s) |
| the point done, no widening, within 60 min of the lane's start (70%) | right (31.9 min: 12:43:01 to 13:14:57) |
| the state on origin by 13:00 UTC (75%) | right (12:42:19 UTC, the commit time of 6e781f4d; interval 79.5 min) |

## Status
- 2026-11-24 11:55 UTC: folder and README written; the unit `i1025-leg-21_28125` is started next and waits for the state.
- 2026-11-24 13:16 UTC: lane done (12:43:01 to 13:14:57 UTC): result and scorecard above, parent row added. The next point is D 21.3125 (`../D21.3125/`).
