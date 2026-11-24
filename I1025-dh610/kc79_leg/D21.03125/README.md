# I1025-dh610/kc79_leg/D21.03125: lambda_1 on win2's k_c 79 leg point D 21.03125 (tag l1kc79Lw1025f), window 0.885 to 0.915 around the prediction 0.8987

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-24 01:24 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", and the hc ruling for points past D 20.90625)
lambda_1 on win2's k_c 79 leg at D 21.03125: **predicted 0.8987 +-0.01** (the previous measured root 0.909538 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D21.031250.npy` and record `l1kc79Lw1025f.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). `tag.txt` names the tag.
- Grid centre 0.900 (the multiple of 0.005 nearest 0.8987; 0.895 lies 0.0037 away, 0.900 0.0013); the scan: 0.885, 0.890, 0.895, 0.900, 0.905, 0.910, 0.915 and a repeat of 0.900. The widening, if there is no robust change: low 0.880, 0.875, 0.870; high 0.920, 0.925, 0.930 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.03125 0.900 0.8987` as the systemd user unit `i1025-leg-21_03125` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.03125 with both controls exit 1; all 8 processes print the record system; the repeat of 0.900 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8987 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; the six earlier points passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (13%), two or more (7%). The change within 0.01 of 0.8987: 80%; within 0.005: 62%. The measured steps so far are -0.010169, -0.009717, -0.009793, -0.009471 and -0.009432 against the prediction's -0.0108 and the residuals +0.000120, +0.000951, +0.002234, +0.001041, +0.001370, +0.001338: I expect the root between 0.8995 and 0.9020 (60%).
- Each scan point takes 1500 to 3500 s (60%; the last point 1651 to 2137 s with the #1081 pool of 5 and the recount beside it; the point before 2800 to 3423 s, and why they differ is not tested); the point is done (no widening) within 60 min of the lane's start (65%).
- The state is on origin by 02:20 UTC (75%; win2's cadence 77.6 min, the last state 00:46:15 UTC).

## Result (`summarize_leg.py 21.03125 0.8987` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.885 | + | ++ (True) | + | -2319.964460233125 | 2493 |
| 0.890 | + | ++ (True) | + | -2320.7454320999013 | 2464 |
| 0.895 | + | ++ (True) | + | -2321.80541181933 | 2472 |
| 0.900 | + | ++ (True) | - | -2325.829473750824 | 2356 |
| 0.900 | + | ++ (True) | - | -2325.829473750824 | 2514 |
| 0.905 | - | -- (True) | - | -2322.6193967513063 | 2433 |
| 0.910 | - | -- (True) | - | -2322.2927727722636 | 2435 |
| 0.915 | - | -- (True) | - | -2322.2630805692643 | 2448 |

scan points: 8 evaluations, seconds per point min 2356, median 2456, max 2514, sum 19615 (the summarizer's own 900 to 1900 s flag, written for the earlier points, lists all eight; the registered range for this point was 1500 to 3500 s)
win2's record at D 21.03125: |F| 4.63502744755702e-10, steps 2675, constraint 0.004824344185249075, Delta 1.119079283134851, h 0.03125, seconds 4566
float64 sign differs from the hybrid at: [0.9, 0.9]

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D21.03125/scan 0.885 0.915
points 7 in 0.885-0.915; not noise-robust: none
hybrid signs: 0.885+ 0.890+ 0.895+ 0.900+ 0.905- 0.910- 0.915-
float64 sign differs from the hybrid sign at: [(0.9, '+', '-')]
repeated points: [(0.9, 'agree')]
  robust change (0.900, 0.905), + to -, det-linear 0.900194, range [0.900125, 0.900194]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.885, - at 0.915
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check .../D21.03125/scan/scan_D21.03125_all.jsonl: lambda [0.9]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.885+ 0.890+ 0.895+ 0.900+ 0.905- 0.910- 0.915-
robust changes: 1
   change (0.900, 0.905), + to -, det-linear 0.900194, range [0.900125, 0.900194]
against the prediction 0.8987: change minus prediction +0.001494; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag f state and record at D 21.03125 (record |F| 4.6350274476e-10, the state's 4.6348451521e-10, 2675 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system (|F| 4.6351943997e-10, 2675 steps).
- **One robust change in the window 0.885 to 0.915:** (0.900, 0.905), "+ to -", det-linear **0.900194**, estimator range [0.900125, 0.900194] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.885, - at 0.915). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.900** (p3 and p7) is bit-identical (hybrid +, ln|det| -2325.829473750824 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.900, in both evaluations** (float64 -, hybrid +): float64 alone would put the change in (0.895, 0.900). The hybrid is read; at D 21.0 the two agreed at all eight.
- **Against the prediction 0.8987 (+-0.01, the previous root 0.909538 minus 0.0108):** +0.001494, within 0.01 (and within 0.005). No widening was needed.
- **Roots on the leg so far (det-linear, as measured):** 0.958120 (D 20.84375), 0.947951 (D 20.875), 0.938234 (D 20.90625), 0.928441 (D 20.9375), 0.918970 (D 20.96875), 0.909538 (D 21.0), 0.900194 (D 21.03125): steps -0.010169, -0.009717, -0.009793, -0.009471, -0.009432 and -0.009344 per 0.03125 in D, against the order's -0.0108.
- **Seconds per point:** 2356 to 2514 s (D 21.0: 1651 to 2137 s). The load average, median over `scan/sampler.log`, was 20.93 (max 22.36; 8 processes here, the kc87_d21 regrid's 8 threads and the recount's 2; D 21.0: 14.14), peak RSS per process 1.64 to 1.76 GiB (`/usr/bin/time -v`), MemAvailable at least 46.27 GiB. The rise over D 21.0 goes with the higher load; that it is the cause is not tested.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (88%), 8 processes with the record system (90%), the repeat agrees (92%) | right |
| one robust change in the window (80%) | right |
| within 0.01 of 0.8987 (80%); within 0.005 (62%) | right (+0.001494) |
| the root between 0.8995 and 0.9020 (60%) | right (0.900194) |
| each scan point 1500 to 3500 s (60%) | right (2356 to 2514 s) |
| the point done, no widening, within 60 min of the lane's start (65%) | right (42 min: 02:07:11 to 02:49:50) |
| the state on origin by 02:20 UTC (75%) | right (02:06:19 UTC, the commit time of e1098cc0) |

## Status
- 2026-11-24 01:24 UTC: folder and README written; the unit `i1025-leg-21_03125` waits for the state (expected about 02:05 UTC).
- 2026-11-24 02:49 UTC: the lane ended (scan 02:07:48 to 02:49:47, 8 of 8 exit 0); Result and scorecard above, 7 of 7 right. The state was on origin at 02:06:19 UTC and pinned at 02:07:07.
