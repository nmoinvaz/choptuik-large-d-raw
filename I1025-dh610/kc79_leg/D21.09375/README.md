# I1025-dh610/kc79_leg/D21.09375: lambda_1 on win2's k_c 79 leg point D 21.09375 (tag l1kc79Lw1025f), window 0.865 to 0.895 around the prediction 0.8804

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-24 04:02 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", and the hc ruling for points past D 20.90625)
lambda_1 on win2's k_c 79 leg at D 21.09375: **predicted 0.8804 +-0.01** (the previous measured root 0.891249 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D21.093750.npy` and record `l1kc79Lw1025f.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). `tag.txt` names the tag.
- Grid centre 0.880 (the multiple of 0.005 nearest 0.8804; 0.0004 away); the scan: 0.865, 0.870, 0.875, 0.880, 0.885, 0.890, 0.895 and a repeat of 0.880. The widening, if there is no robust change: low 0.860, 0.855, 0.850; high 0.900, 0.905, 0.910 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.09375 0.880 0.8804` as the systemd user unit `i1025-leg-21_09375` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.09375 with both controls exit 1; all 8 processes print the record system; the repeat of 0.880 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8804 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; the eight earlier points passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (13%), two or more (7%). The change within 0.01 of 0.8804: 82%; within 0.005: 65%. The measured steps so far are -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344 and -0.008945 against the prediction's -0.0108 and the residuals +0.000120, +0.000951, +0.002234, +0.001041, +0.001370, +0.001338, +0.001494, +0.001849: I expect the root between 0.8810 and 0.8835 (55%).
- The float64 sign agrees with the hybrid at all 8 evaluations (35%; it differed at three points of the last point, at one of the one before, at none of the one before that).
- Each scan point takes 2000 to 3800 s (60%; the last point 2984 to 3341 s, 2356 to 2514 s the point before); the scan runs beside the kc87_d21 scan (8 processes each) and the recount until the kc87_d21 scan ends. The point is done (no widening) within 70 min of the lane's start (65%; the last 57 min).
- The state is on origin by 04:45 UTC (80%; win2's last interval 57.4 min, those before 77 to 80 min; the last state 03:03:45 UTC).

## Result (`summarize_leg.py 21.09375 0.8804` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.865 | + | ++ (True) | + | -2312.0616646886115 | 2574 |
| 0.870 | + | ++ (True) | + | -2312.810858376313 | 2119 |
| 0.875 | + | ++ (True) | + | -2313.778685498677 | 2290 |
| 0.880 | + | ++ (True) | - | -2315.7472487914342 | 2098 |
| 0.880 | + | ++ (True) | - | -2315.7472487914342 | 2303 |
| 0.885 | - | -- (True) | + | -2315.0717713209083 | 2286 |
| 0.890 | - | -- (True) | - | -2314.6020787440857 | 2506 |
| 0.895 | - | -- (True) | - | -2314.5321731689546 | 2308 |

scan points: 8 evaluations, seconds per point min 2098, median 2296, max 2574, sum 18484 (the summarizer's own 900 to 1900 s flag, written for the earlier points, lists all eight; the registered range for this point was 2000 to 3800 s)
win2's record at D 21.09375: |F| 4.617751780667425e-10, steps 2671, constraint 0.005037829143111499, Delta 1.1207536326395737, h 0.03125, seconds 4503
float64 sign differs from the hybrid at: [0.88, 0.88, 0.885]

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D21.09375/scan 0.865 0.895
points 7 in 0.865-0.895; not noise-robust: none
hybrid signs: 0.865+ 0.870+ 0.875+ 0.880+ 0.885- 0.890- 0.895-
float64 sign differs from the hybrid sign at: [(0.88, '+', '-'), (0.885, '-', '+')]
repeated points: [(0.88, 'agree')]
  robust change (0.880, 0.885), + to -, det-linear 0.881686, range [0.881196, 0.881686]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.865, - at 0.895
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check .../D21.09375/scan/scan_D21.09375_all.jsonl: lambda [0.88]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.865+ 0.870+ 0.875+ 0.880+ 0.885- 0.890- 0.895-
robust changes: 1
   change (0.880, 0.885), + to -, det-linear 0.881686, range [0.881196, 0.881686]
against the prediction 0.8804: change minus prediction +0.001286; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag f state and record at D 21.09375 (record |F| 4.6177517807e-10, the state's 4.6166568384e-10, 2671 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system (|F| 4.6180138100e-10, 2671 steps).
- **One robust change in the window 0.865 to 0.895:** (0.880, 0.885), "+ to -", det-linear **0.881686**, estimator range [0.881196, 0.881686] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.865, - at 0.895). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.880** (p3 and p7) is bit-identical (hybrid +, ln|det| -2315.7472487914342 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.880 (both evaluations; float64 -, hybrid +) and at 0.885 (float64 +, hybrid -)**, one point on each side of the change: the float64 signs along the grid are + + + - + - -, which alone would read as three changes. The hybrid is read (one change). At D 21.0625 it differed at three points above the change, at D 21.03125 at 0.900 only.
- **Against the prediction 0.8804 (+-0.01, the previous root 0.891249 minus 0.0108):** +0.001286, within 0.01 (and within 0.005). No widening was needed.
- **Roots on the leg so far (det-linear, as measured):** 0.958120 (D 20.84375), 0.947951 (D 20.875), 0.938234 (D 20.90625), 0.928441 (D 20.9375), 0.918970 (D 20.96875), 0.909538 (D 21.0), 0.900194 (D 21.03125), 0.891249 (D 21.0625), 0.881686 (D 21.09375): steps -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945 and -0.009563 per 0.03125 in D, against the order's -0.0108.
- **Seconds per point:** 2098 to 2574 s (D 21.0625: 2984 to 3341 s). The load average, median over `scan/sampler.log`, was 14.30 (max 22.62; 8 processes here, the kc87_d21 scan's 8 until 04:46:49 UTC, the recount's 2), peak RSS per process 1.58 to 1.82 GiB (`/usr/bin/time -v`), MemAvailable at least 45.08 GiB. The fall from D 21.0625 goes with the end of the overlap with the kc87_d21 scan; that it is the cause is not tested.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (88%), 8 processes with the record system (90%), the repeat agrees (92%) | right |
| one robust change in the window (80%) | right |
| within 0.01 of 0.8804 (82%); within 0.005 (65%) | right (+0.001286) |
| the root between 0.8810 and 0.8835 (55%) | right (0.881686) |
| the float64 sign agrees with the hybrid at all 8 evaluations (35%) | WRONG (differs at 0.880 twice and 0.885) |
| each scan point 2000 to 3800 s (60%) | right (2098 to 2574 s) |
| the point done, no widening, within 70 min of the lane's start (65%) | right (44 min: 04:22:28 to 05:06:21) |
| the state on origin by 04:45 UTC (80%) | right (04:21:18 UTC, the commit time of 5109c7ba; interval 77.5 min) |

## Status
- 2026-11-24 04:02 UTC: folder and README written; the unit `i1025-leg-21_09375` is started next and waits for the state.
- 2026-11-24 05:06 UTC: the lane ended (scan 04:23:14 to 05:06:17, 8 of 8 exit 0); Result and scorecard above, 7 of 8 right (float64 sign). The state was on origin at 04:21:18 UTC and pinned at 04:22:25.
