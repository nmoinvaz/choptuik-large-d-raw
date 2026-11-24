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

## Result (`summarize_leg.py 21.25 0.8309` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.815 | + | ++ (True) | + | -2293.1577794620903 | 1802 |
| 0.820 | + | ++ (True) | + | -2293.9165651643575 | 1841 |
| 0.825 | + | ++ (True) | + | -2294.914138581567 | 1835 |
| 0.830 | + | ++ (True) | + | -2297.220320331923 | 1845 |
| 0.830 | + | ++ (True) | + | -2297.220320331923 | 1848 |
| 0.835 | - | -- (True) | + | -2296.0194682245633 | 1811 |
| 0.840 | - | -- (True) | + | -2295.6092204302795 | 1842 |
| 0.845 | - | -- (True) | + | -2295.554158082009 | 1809 |

scan points: 8 evaluations, seconds per point min 1802, median 1838, max 1848, sum 14633; outside 900 to 1900 s: []
win2's record at D 21.25: |F| 4.5485512502509616e-10, steps 2656, constraint 0.005597282453435274, Delta 1.1249625860927213, h 0.03125, seconds 4544
float64 sign differs from the hybrid at: [0.835, 0.84, 0.845]

```
=== read_lower.py .../D21.25/scan 0.815 0.845
points 7 in 0.815-0.845; not noise-robust: none
hybrid signs: 0.815+ 0.820+ 0.825+ 0.830+ 0.835- 0.840- 0.845-
float64 sign differs from the hybrid sign at: [(0.835, '-', '+'), (0.84, '-', '+'), (0.845, '-', '+')]
repeated points: [(0.83, 'agree')]
  robust change (0.830, 0.835), + to -, det-linear 0.831157, range [0.830793, 0.831157]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.815, - at 0.845
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check .../D21.25/scan/scan_D21.25_all.jsonl: lambda [0.83]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.815+ 0.820+ 0.825+ 0.830+ 0.835- 0.840- 0.845-
robust changes: 1
   change (0.830, 0.835), + to -, det-linear 0.831157, range [0.830793, 0.831157]
against the prediction 0.8309: change minus prediction +0.000257; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag g state and record at D 21.25 (record |F| 4.5485512503e-10, the state's 4.5479735575e-10, 2656 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system. The state and record are of win2's commit e7a44b59 (2026-11-24 03:22:47 -08:00 = 11:22:47 UTC, 76.6 min after the D 21.21875 state; the record's seconds 4544). The g record's rows run on: |F| 4.578973943765308e-10, 4.564782766290151e-10, 4.5485512502509616e-10, steps 2660, 2658, 2656, Delta 1.1232751318410306, 1.1241182782455752, 1.1249625860927213.
- **One robust change in the window 0.815 to 0.845:** (0.830, 0.835), "+ to -", det-linear **0.831157**, estimator range [0.830793, 0.831157] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.815, - at 0.845). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.830** (p3 and p7) is bit-identical (hybrid +, ln|det| -2297.220320331923 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.835, 0.840 and 0.845, above the change:** the float64 signs along the grid are + + + + + + +, which alone would read no change in the window at all. The hybrid is read (one change, in (0.830, 0.835)). At D 21.21875 it differed at 0.835 and 0.840, below the change; at D 21.1875 at 0.860.
- **Against the prediction 0.8309 (+-0.01, the previous root 0.841733 minus 0.0108):** +0.000257, within 0.01 (and within 0.005). No widening was needed.
- **Roots on the leg so far (det-linear, as measured):** 0.958120 (D 20.84375), 0.947951 (D 20.875), 0.938234 (D 20.90625), 0.928441 (D 20.9375), 0.918970 (D 20.96875), 0.909538 (D 21.0), 0.900194 (D 21.03125), 0.891249 (D 21.0625), 0.881686 (D 21.09375), 0.872088 (D 21.125), 0.862190 (D 21.15625), 0.852069 (D 21.1875), 0.841733 (D 21.21875), 0.831157 (D 21.25): steps -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945, -0.009563, -0.009598, -0.009898, -0.010121, -0.010336 and -0.010576 per 0.03125 in D, against the order's -0.0108.
- **Seconds per point:** 1802 to 1848 s (D 21.21875: 1527 to 1603 s). The load average, median over `scan/sampler.log`, was 9.09 (max 9.42; 8 processes here at nice 5, and the recount's workers, started 11:13 UTC, beside them), peak RSS per process 1.65 to 1.82 GiB (`/usr/bin/time -v`), MemAvailable at least 48.92 GiB.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (90%), 8 processes with the record system (92%), the repeat agrees (92%) | right |
| one robust change in the window (83%) | right |
| within 0.01 of 0.8309 (88%); within 0.005 (78%) | right (+0.000257) |
| the bracket is (0.830, 0.835) (75%) | right |
| the root between 0.8300 and 0.8325 (65%) | right (0.831157) |
| the float64 sign agrees with the hybrid at all 8 evaluations (25%) | WRONG (differs at 0.835, 0.840 and 0.845) |
| each scan point 1300 to 2300 s (70%) | right (1802 to 1848 s) |
| the point done, no widening, within 50 min of the lane's start (70%) | right (31 min: 11:23:55 to 11:54:59) |
| the state on origin by 11:50 UTC (75%) | right (11:22:47 UTC, the commit time of e7a44b59; interval 76.6 min) |

## Status
- 2026-11-24 10:34 UTC: folder and README written; the unit `i1025-leg-21_25` is started next and waits for the state.
- 2026-11-24 11:55 UTC: lane done (11:23:55 to 11:54:59 UTC): result and scorecard above, parent row added. The next point is D 21.28125 (`../D21.28125/`).
