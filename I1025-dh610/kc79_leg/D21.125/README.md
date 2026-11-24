# I1025-dh610/kc79_leg/D21.125: lambda_1 on win2's k_c 79 leg point D 21.125 (tag l1kc79Lw1025f), window 0.855 to 0.885 around the prediction 0.8709

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-24 05:09 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", and the hc ruling for points past D 20.90625)
lambda_1 on win2's k_c 79 leg at D 21.125: **predicted 0.8709 +-0.01** (the previous measured root 0.881686 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D21.125000.npy` and record `l1kc79Lw1025f.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). `tag.txt` names the tag.
- Grid centre 0.870 (the multiple of 0.005 nearest 0.8709; 0.0009 away); the scan: 0.855, 0.860, 0.865, 0.870, 0.875, 0.880, 0.885 and a repeat of 0.870. The widening, if there is no robust change: low 0.850, 0.845, 0.840; high 0.890, 0.895, 0.900 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.125 0.870 0.8709` as the systemd user unit `i1025-leg-21_125` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.125 with both controls exit 1; all 8 processes print the record system; the repeat of 0.870 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8709 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; the nine earlier points passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (13%), two or more (7%). The change within 0.01 of 0.8709: 83%; within 0.005: 68%. The measured steps so far are -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945 and -0.009563 against the prediction's -0.0108 and the residuals +0.000120, +0.000951, +0.002234, +0.001041, +0.001370, +0.001338, +0.001494, +0.001849, +0.001286: I expect the root between 0.8715 and 0.8740 (55%).
- The float64 sign agrees with the hybrid at all 8 evaluations (30%; it differed at 2 to 3 grid points in the last two points, at one in the one before, at none in the one before that).
- Each scan point takes 1500 to 2800 s (60%; the last point 2098 to 2574 s with the kc87_d21 scan beside it for 24 of its 44 min, D 21.0 1651 to 2137 s with load 14); this scan runs beside the recount only. The point is done (no widening) within 55 min of the lane's start (65%; the last 44 min).
- The state is on origin by 05:50 UTC (80%; win2's last two intervals 57.4 and 77.5 min, the last state 04:21:18 UTC).

## Result (`summarize_leg.py 21.125 0.8709` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.855 | + | ++ (True) | + | -2308.512250322054 | 1504 |
| 0.860 | + | ++ (True) | + | -2309.25248190707 | 1727 |
| 0.865 | + | ++ (True) | - | -2310.1969074842277 | 1729 |
| 0.870 | + | ++ (True) | - | -2311.9783063508385 | 1543 |
| 0.870 | + | ++ (True) | - | -2311.9783063508385 | 1738 |
| 0.875 | - | -- (True) | - | -2311.645564577513 | 1614 |
| 0.880 | - | -- (True) | - | -2311.117799547639 | 1578 |
| 0.885 | - | -- (True) | - | -2311.03319738544 | 1538 |

scan points: 8 evaluations, seconds per point min 1504, median 1596, max 1738, sum 12971; outside 900 to 1900 s: []
win2's record at D 21.125: |F| 4.605990614286346e-10, steps 2667, constraint 0.0051467645113007585, Delta 1.1215928048382566, h 0.03125, seconds 4503
float64 sign differs from the hybrid at: [0.865, 0.87, 0.87]

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D21.125/scan 0.855 0.885
points 7 in 0.855-0.885; not noise-robust: none
hybrid signs: 0.855+ 0.860+ 0.865+ 0.870+ 0.875- 0.880- 0.885-
float64 sign differs from the hybrid sign at: [(0.865, '+', '-'), (0.87, '+', '-')]
repeated points: [(0.87, 'agree')]
  robust change (0.870, 0.875), + to -, det-linear 0.872088, range [0.871525, 0.872088]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.855, - at 0.885
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check .../D21.125/scan/scan_D21.125_all.jsonl: lambda [0.87]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.855+ 0.860+ 0.865+ 0.870+ 0.875- 0.880- 0.885-
robust changes: 1
   change (0.870, 0.875), + to -, det-linear 0.872088, range [0.871525, 0.872088]
against the prediction 0.8709: change minus prediction +0.001188; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag f state and record at D 21.125 (record |F| 4.6059906143e-10, 2667 steps = the state's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system (|F| 4.6074799409e-10, 2667 steps).
- **One robust change in the window 0.855 to 0.885:** (0.870, 0.875), "+ to -", det-linear **0.872088**, estimator range [0.871525, 0.872088] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.855, - at 0.885). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.870** (p3 and p7) is bit-identical (hybrid +, ln|det| -2311.9783063508385 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.865 and 0.870 (the latter in both evaluations; float64 -, hybrid +):** the float64 signs along the grid are + + - - - - -, which alone would put the change in (0.860, 0.865). The hybrid is read. It differed at 0.880 and 0.885 at D 21.09375, at three points at D 21.0625.
- **Against the prediction 0.8709 (+-0.01, the previous root 0.881686 minus 0.0108):** +0.001188, within 0.01 (and within 0.005). No widening was needed.
- **Roots on the leg so far (det-linear, as measured):** 0.958120 (D 20.84375), 0.947951 (D 20.875), 0.938234 (D 20.90625), 0.928441 (D 20.9375), 0.918970 (D 20.96875), 0.909538 (D 21.0), 0.900194 (D 21.03125), 0.891249 (D 21.0625), 0.881686 (D 21.09375), 0.872088 (D 21.125): steps -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945, -0.009563 and -0.009598 per 0.03125 in D, against the order's -0.0108.
- **Seconds per point:** 1504 to 1738 s (D 21.09375: 2098 to 2574 s). The load average, median over `scan/sampler.log`, was 9.98 (max 11.26; 8 processes here and the recount's 2, nothing else), peak RSS per process 1.62 to 1.76 GiB (`/usr/bin/time -v`), MemAvailable at least 48.42 GiB. The fall from D 21.09375 goes with the load falling from 14.3 to 10.0, as D 21.0's 1651 to 2137 s did at load 14; that it is the cause is not tested.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (88%), 8 processes with the record system (90%), the repeat agrees (92%) | right |
| one robust change in the window (80%) | right |
| within 0.01 of 0.8709 (83%); within 0.005 (68%) | right (+0.001188) |
| the root between 0.8715 and 0.8740 (55%) | right (0.872088) |
| the float64 sign agrees with the hybrid at all 8 evaluations (30%) | WRONG (differs at 0.865 and 0.870 twice) |
| each scan point 1500 to 2800 s (60%) | right (1504 to 1738 s; the smallest is 4 s above the floor) |
| the point done, no widening, within 55 min of the lane's start (65%) | right (29 min: 05:39:57 to 06:09:20) |
| the state on origin by 05:50 UTC (80%) | right (05:39:26 UTC, the commit time of e68865b2; interval 78.1 min) |

## Status
- 2026-11-24 05:09 UTC: folder and README written; the unit `i1025-leg-21_125` is started next and waits for the state.
- 2026-11-24 06:09 UTC: the lane ended (scan 05:40:13 to 06:09:17, 8 of 8 exit 0); Result and scorecard above, 7 of 8 right (float64 sign). The state was on origin at 05:39:26 UTC and pinned at 05:39:53.
