# I1025-dh610/kc79_leg/D21.0: lambda_1 on win2's k_c 79 leg point D 21.0 (tag l1kc79Lw1025f), window 0.895 to 0.925 around the prediction 0.9082

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-24 00:29 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", and the hc ruling for points past D 20.90625)
lambda_1 on win2's k_c 79 leg at D 21.0: **predicted 0.9082 +-0.01** (the previous measured root 0.918970 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D21.000000.npy` and record `l1kc79Lw1025f.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). `tag.txt` names the tag.
- Grid centre 0.910 (the multiple of 0.005 nearest 0.9082; 0.905 lies 0.0032 away, 0.910 0.0018); the scan: 0.895, 0.900, 0.905, 0.910, 0.915, 0.920, 0.925 and a repeat of 0.910. The widening, if there is no robust change: low 0.890, 0.885, 0.880; high 0.930, 0.935, 0.940 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.0 0.910 0.9082` as the systemd user unit `i1025-leg-21_0` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.0 with both controls exit 1; all 8 processes print the record system; the repeat of 0.910 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.9082 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; the five earlier points passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (13%), two or more (7%). The change within 0.01 of 0.9082: 80%; within 0.005: 60%. The measured steps so far are -0.010169, -0.009717, -0.009793 and -0.009471 against the prediction's -0.0108 and the residuals +0.000120, +0.000951, +0.002234, +0.001041, +0.001370: I expect the root between 0.9083 and 0.9110 (60%).
- Each scan point takes 2200 to 4000 s (60%; the last point 2800 to 3423 s with the d19_k95 gap scan and the recount beside it); the point is done (no widening) within 75 min of the lane's start (70%).
- The state is on origin by 01:05 UTC (75%; win2's cadence 81.3 min, the last state 23:28:40 UTC).

## Status
- 2026-11-24 00:29 UTC: folder and README written; the unit `i1025-leg-21_0` waits for the state (expected about 00:50 UTC).

- 2026-11-24 00:46:15 UTC win2's commit 497efffe added the state (its commit time, 2026-11-23T16:46:15-08:00; `source_commit.txt`, tag l1kc79Lw1025f); 00:47:01 pinned; 00:47:04 lock taken, lane started; 00:47:05 selftests as wanted (0 0 1 1 0 0 1); 00:47:15 source check ACCEPTED and scan started (8 processes, nice 10); 01:22:55 the last process ended and the reading was written; 01:22:59 lane exit 0 (`exits_leg.txt`).

## Result (`summarize_leg.py 21.0 0.9082` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.895 | + | ++ (True) | + | -2323.53570203324 | 1651 |
| 0.900 | + | ++ (True) | + | -2324.3416186718364 | 1957 |
| 0.905 | + | ++ (True) | + | -2325.484061258967 | 1815 |
| 0.910 | - | -- (True) | - | -2327.768663594143 | 1715 |
| 0.910 | - | -- (True) | - | -2327.768663594143 | 2137 |
| 0.915 | - | -- (True) | - | -2325.9791618194995 | 1790 |
| 0.920 | - | -- (True) | - | -2325.7225453868386 | 1662 |
| 0.925 | - | -- (True) | - | -2325.715028374029 | 1902 |

scan points: 8 evaluations, seconds per point min 1651, median 1802, max 2137, sum 14629; outside 900 to 1900 s: [(0.9, 1957), (0.91, 2137), (0.925, 1902)]
win2's record at D 21.0: |F| 4.6401788196957317e-10, steps 2678, constraint 0.004719788472577341, Delta 1.1182445857206806, h 0.03125, seconds 4610
float64 sign differs from the hybrid at: []

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D21.0/scan 0.895 0.925
points 7 in 0.895-0.925; not noise-robust: none
hybrid signs: 0.895+ 0.900+ 0.905+ 0.910- 0.915- 0.920- 0.925-
float64 sign differs from the hybrid sign at: none
repeated points: [(0.91, 'agree')]
  robust change (0.905, 0.910), + to -, det-linear 0.909538, range [0.909234, 0.909538]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.895, - at 0.925
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D21.0/scan/scan_D21.0_all.jsonl: lambda [0.91]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.895+ 0.900+ 0.905+ 0.910- 0.915- 0.920- 0.925-
robust changes: 1
   change (0.905, 0.910), + to -, det-linear 0.909538, range [0.909234, 0.909538]
against the prediction 0.9082: change minus prediction +0.001338; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag f state and record at D 21.0 (record |F| 4.6401788197e-10, the state's 4.6429292105e-10, 2678 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system (|F| 4.6398734897e-10, 2678 steps).
- **One robust change in the window 0.895 to 0.925:** (0.905, 0.910), "+ to -", det-linear **0.909538**, estimator range [0.909234, 0.909538] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.895, - at 0.925). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.910** (p3 and p7) is bit-identical (hybrid -, ln|det| -2327.768663594143 in both; `repeat_check.py` PASS).
- **The float64 sign agrees with the hybrid at all 8 evaluations** (at D 20.875, 20.90625, 20.9375 and 20.96875 it differed at one or two grid points near the change; `../README.md` lists them).
- **Against the prediction 0.9082 (+-0.01, the previous root 0.918970 minus 0.0108):** +0.001338, within 0.01 (and within 0.005). No widening was needed.
- **Roots on the leg so far (det-linear, as measured):** 0.958120 (D 20.84375), 0.947951 (D 20.875), 0.938234 (D 20.90625), 0.928441 (D 20.9375), 0.918970 (D 20.96875), 0.909538 (D 21.0): steps -0.010169, -0.009717, -0.009793, -0.009471 and -0.009432 per 0.03125 in D, against the order's -0.0108.
- **Seconds per point:** 1651 to 2137 s (D 20.96875: 2800 to 3423 s). The load average, median over `scan/sampler.log`, was 14.14 (8 processes here, the #1081 pool's 5 and the recount's 2; D 20.96875: 15.05), peak RSS per process 1.60 to 1.74 GiB, MemAvailable at least 48.27 GiB. The load average does not explain the fall of about 40%; why is not tested.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (88%), 8 processes with the record system (90%), the repeat agrees (92%) | right |
| one robust change in the window (80%) | right |
| within 0.01 of 0.9082 (80%); within 0.005 (60%) | right (+0.001338) |
| the root between 0.9083 and 0.9110 (60%) | right (0.909538) |
| each scan point 2200 to 4000 s (60%) | WRONG (1651 to 2137 s, all eight below 2200 s) |
| the point done, no widening, within 75 min of the lane's start (70%) | right (36 min: 00:47:04 to 01:22:59) |
| the state on origin by 01:05 UTC (75%) | right (00:46:15 UTC, the commit time of 497efffe) |
