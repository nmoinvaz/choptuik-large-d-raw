# I1025-dh610/kc79_leg/D21.0625: lambda_1 on win2's k_c 79 leg point D 21.0625 (tag l1kc79Lw1025f), window 0.875 to 0.905 around the prediction 0.8894

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-24 02:52 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", and the hc ruling for points past D 20.90625)
lambda_1 on win2's k_c 79 leg at D 21.0625: **predicted 0.8894 +-0.01** (the previous measured root 0.900194 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D21.062500.npy` and record `l1kc79Lw1025f.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). `tag.txt` names the tag.
- Grid centre 0.890 (the multiple of 0.005 nearest 0.8894; 0.0006 away); the scan: 0.875, 0.880, 0.885, 0.890, 0.895, 0.900, 0.905 and a repeat of 0.890. The widening, if there is no robust change: low 0.870, 0.865, 0.860; high 0.910, 0.915, 0.920 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.0625 0.890 0.8894` as the systemd user unit `i1025-leg-21_0625` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.0625 with both controls exit 1; all 8 processes print the record system; the repeat of 0.890 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8894 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; the seven earlier points passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (13%), two or more (7%). The change within 0.01 of 0.8894: 80%; within 0.005: 62%. The measured steps so far are -0.010169, -0.009717, -0.009793, -0.009471, -0.009432 and -0.009344 against the prediction's -0.0108 and the residuals +0.000120, +0.000951, +0.002234, +0.001041, +0.001370, +0.001338, +0.001494: I expect the root between 0.8900 and 0.8925 (60%).
- The float64 sign agrees with the hybrid at all 8 evaluations (50%; it differed at 0.900 of the last point, agreed at all eight of the one before, and differed at one to two points in each of the five before that).
- Each scan point takes 1800 to 3500 s (60%; the last point 2356 to 2514 s beside the kc87_d21 regrid and the recount; this point's scan will run beside the kc87_d21 scan, 8 processes each, if that lane has reached its scan); the point is done (no widening) within 60 min of the lane's start (65%).
- The state is on origin by 03:45 UTC (80%; win2's cadence 77.6 to 80 min, the last state 02:06:19 UTC).

## Result (`summarize_leg.py 21.0625 0.8894` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.875 | + | ++ (True) | + | -2316.0093511223113 | 3187 |
| 0.880 | + | ++ (True) | + | -2316.7677227694635 | 3111 |
| 0.885 | + | ++ (True) | + | -2317.761234732604 | 3341 |
| 0.890 | + | ++ (True) | + | -2319.9994471303226 | 3241 |
| 0.890 | + | ++ (True) | + | -2319.9994471303226 | 3281 |
| 0.895 | - | -- (True) | + | -2318.899878630826 | 2996 |
| 0.900 | - | -- (True) | + | -2318.4813009344107 | 3190 |
| 0.905 | - | -- (True) | + | -2318.424766639469 | 2984 |

scan points: 8 evaluations, seconds per point min 2984, median 3188, max 3341, sum 25331 (the summarizer's own 900 to 1900 s flag, written for the earlier points, lists all eight; the registered range for this point was 1800 to 3500 s)
win2's record at D 21.0625: |F| 4.6223106635316083e-10, steps 2670, constraint 0.004930364481203466, Delta 1.119915872658043, h 0.03125, seconds 3411
float64 sign differs from the hybrid at: [0.895, 0.9, 0.905]

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D21.0625/scan 0.875 0.905
points 7 in 0.875-0.905; not noise-robust: none
hybrid signs: 0.875+ 0.880+ 0.885+ 0.890+ 0.895- 0.900- 0.905-
float64 sign differs from the hybrid sign at: [(0.895, '-', '+'), (0.9, '-', '+'), (0.905, '-', '+')]
repeated points: [(0.89, 'agree')]
  robust change (0.890, 0.895), + to -, det-linear 0.891249, range [0.890860, 0.891249]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.875, - at 0.905
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check .../D21.0625/scan/scan_D21.0625_all.jsonl: lambda [0.89]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.875+ 0.880+ 0.885+ 0.890+ 0.895- 0.900- 0.905-
robust changes: 1
   change (0.890, 0.895), + to -, det-linear 0.891249, range [0.890860, 0.891249]
against the prediction 0.8894: change minus prediction +0.001849; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag f state and record at D 21.0625 (record |F| 4.6223106635e-10, the state's 4.6268985561e-10, 2670 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system (|F| 4.6256277471e-10, 2670 steps).
- **One robust change in the window 0.875 to 0.905:** (0.890, 0.895), "+ to -", det-linear **0.891249**, estimator range [0.890860, 0.891249] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.875, - at 0.905). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.890** (p3 and p7) is bit-identical (hybrid +, ln|det| -2319.9994471303226 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.895, 0.900 and 0.905** (float64 +, hybrid -): all three points above the change. A scan by the float64 sign alone would have shown no change in this window. The hybrid is read. At D 21.03125 it differed at 0.900 only, at D 21.0 at none.
- **Against the prediction 0.8894 (+-0.01, the previous root 0.900194 minus 0.0108):** +0.001849, within 0.01 (and within 0.005). No widening was needed.
- **Roots on the leg so far (det-linear, as measured):** 0.958120 (D 20.84375), 0.947951 (D 20.875), 0.938234 (D 20.90625), 0.928441 (D 20.9375), 0.918970 (D 20.96875), 0.909538 (D 21.0), 0.900194 (D 21.03125), 0.891249 (D 21.0625): steps -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344 and -0.008945 per 0.03125 in D, against the order's -0.0108. The last step is the smallest in size so far.
- **Seconds per point:** 2984 to 3341 s (D 21.03125: 2356 to 2514 s). The load average, median over `scan/sampler.log`, was 19.10 (max 22.83; 8 processes here, the kc87_d21 scan's 8 from 03:25:53 UTC, the regrid's 8 threads before that, and the recount's 2), peak RSS per process 1.59 to 1.76 GiB (`/usr/bin/time -v`), MemAvailable at least 45.24 GiB. The rise over D 21.03125 goes with the longer overlap with the kc87_d21 scan; that it is the cause is not tested.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (88%), 8 processes with the record system (90%), the repeat agrees (92%) | right |
| one robust change in the window (80%) | right |
| within 0.01 of 0.8894 (80%); within 0.005 (62%) | right (+0.001849) |
| the root between 0.8900 and 0.8925 (60%) | right (0.891249) |
| the float64 sign agrees with the hybrid at all 8 evaluations (50%) | WRONG (differs at 0.895, 0.900 and 0.905) |
| each scan point 1800 to 3500 s (60%) | right (2984 to 3341 s) |
| the point done, no widening, within 60 min of the lane's start (65%) | right (57 min: 03:04:47 to 04:01:19) |
| the state on origin by 03:45 UTC (80%) | right (03:03:45 UTC, the commit time of e1d85191; win2 cadence 57.4 min against 77 to 80 before) |

## Status
- 2026-11-24 02:52 UTC: folder and README written; the unit `i1025-leg-21_0625` is started next and waits for the state (expected about 03:25 UTC).
- 2026-11-24 04:01 UTC: the lane ended (scan 03:05:27 to 04:01:13, 8 of 8 exit 0); Result and scorecard above, 7 of 8 right (float64 sign). The state was on origin at 03:03:45 UTC and pinned at 03:04:43.
