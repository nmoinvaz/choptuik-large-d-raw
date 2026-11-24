# I1025-dh610/kc79_leg/D21.15625: lambda_1 on win2's k_c 79 leg point D 21.15625 (tag l1kc79Lw1025f), window 0.845 to 0.875 around the prediction 0.8613

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-24 06:10 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", and the hc ruling for points past D 20.90625)
lambda_1 on win2's k_c 79 leg at D 21.15625: **predicted 0.8613 +-0.01** (the previous measured root 0.872088 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D21.156250.npy` and record `l1kc79Lw1025f.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). `tag.txt` names the tag. win2's restarted leap under tag f is capped at 07:17:20 UTC; this state is expected before that (about 06:57 UTC). If the next state appears under tag g instead (win2's queued cap restart), the coordinator's ruling (`../README.md`, status of 2026-11-24 06:11 UTC) applies: `tag.txt` becomes g after the authorization check, and the switch is recorded in the parent README.
- Grid centre 0.860 (the multiple of 0.005 nearest 0.8613; 0.0013 away); the scan: 0.845, 0.850, 0.855, 0.860, 0.865, 0.870, 0.875 and a repeat of 0.860. The widening, if there is no robust change: low 0.840, 0.835, 0.830; high 0.880, 0.885, 0.890 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.15625 0.860 0.8613` as the systemd user unit `i1025-leg-21_15625` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.15625 with both controls exit 1; all 8 processes print the record system; the repeat of 0.860 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8613 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; the ten earlier points passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (13%), two or more (7%). The change within 0.01 of 0.8613: 83%; within 0.005: 70%. The measured steps so far are -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945, -0.009563 and -0.009598 against the prediction's -0.0108 and the residuals +0.000120, +0.000951, +0.002234, +0.001041, +0.001370, +0.001338, +0.001494, +0.001849, +0.001286, +0.001188: I expect the root between 0.8620 and 0.8645 (55%).
- The float64 sign agrees with the hybrid at all 8 evaluations (30%; it differed at 2 to 3 grid points in the last three points, at one in the one before that).
- Each scan point takes 1300 to 2300 s (60%; the last point 1504 to 1738 s at load 10, D 21.09375 2098 to 2574 s at load 14); this scan runs beside the recount only. The point is done (no widening) within 50 min of the lane's start (65%; the last 29 min).
- The state is on origin by 07:20 UTC (75%; win2's last three intervals 57.4, 77.5 and 78.1 min, the last state 05:39:26 UTC, so about 06:57 UTC; the cap at 07:17:20 UTC is the risk).

## Result (`summarize_leg.py 21.15625 0.8613` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.845 | + | ++ (True) | + | -2304.5727660963885 | 1684 |
| 0.850 | + | ++ (True) | + | -2305.310401161003 | 1616 |
| 0.855 | + | ++ (True) | + | -2306.248693826799 | 1674 |
| 0.860 | + | ++ (True) | - | -2307.9886742150366 | 1659 |
| 0.860 | + | ++ (True) | - | -2307.9886742150366 | 1681 |
| 0.865 | - | -- (True) | + | -2307.7390101687415 | 1697 |
| 0.870 | - | -- (True) | + | -2307.194223786326 | 1597 |
| 0.875 | - | -- (True) | - | -2307.1052778561434 | 1619 |

scan points: 8 evaluations, seconds per point min 1597, median 1666, max 1697, sum 13227; outside 900 to 1900 s: []
win2's record at D 21.15625: |F| 4.5897952881747886e-10, steps 2664, constraint 0.005257168144821403, Delta 1.122433147959886, h 0.03125, seconds 4475
float64 sign differs from the hybrid at: [0.86, 0.86, 0.865, 0.87]

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D21.15625/scan 0.845 0.875
points 7 in 0.845-0.875; not noise-robust: none
hybrid signs: 0.845+ 0.850+ 0.855+ 0.860+ 0.865- 0.870- 0.875-
float64 sign differs from the hybrid sign at: [(0.86, '+', '-'), (0.865, '-', '+'), (0.87, '-', '+')]
repeated points: [(0.86, 'agree')]
  robust change (0.860, 0.865), + to -, det-linear 0.862190, range [0.861612, 0.862190]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.845, - at 0.875
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check .../D21.15625/scan/scan_D21.15625_all.jsonl: lambda [0.86]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.845+ 0.850+ 0.855+ 0.860+ 0.865- 0.870- 0.875-
robust changes: 1
   change (0.860, 0.865), + to -, det-linear 0.862190, range [0.861612, 0.862190]
against the prediction 0.8613: change minus prediction +0.000890; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag f state and record at D 21.15625 (record |F| 4.5897952882e-10, the state's 4.5920742520e-10, 2664 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system (|F| 4.5890512643e-10, 2664 steps). This is the last point under tag f; its state is the second seed of win2's cap restart (tag g, blob ff2a8451).
- **One robust change in the window 0.845 to 0.875:** (0.860, 0.865), "+ to -", det-linear **0.862190**, estimator range [0.861612, 0.862190] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.845, - at 0.875). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.860** (p3 and p7) is bit-identical (hybrid +, ln|det| -2307.9886742150366 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.860 (both evaluations), 0.865 and 0.870:** the float64 signs along the grid are + + + - + + -, which alone would read as three changes. The hybrid is read (one change). It differed at two points at D 21.125 and at D 21.09375, at three at D 21.0625.
- **Against the prediction 0.8613 (+-0.01, the previous root 0.872088 minus 0.0108):** +0.000890, within 0.01 (and within 0.005). No widening was needed.
- **Roots on the leg so far (det-linear, as measured):** 0.958120 (D 20.84375), 0.947951 (D 20.875), 0.938234 (D 20.90625), 0.928441 (D 20.9375), 0.918970 (D 20.96875), 0.909538 (D 21.0), 0.900194 (D 21.03125), 0.891249 (D 21.0625), 0.881686 (D 21.09375), 0.872088 (D 21.125), 0.862190 (D 21.15625): steps -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945, -0.009563, -0.009598 and -0.009898 per 0.03125 in D, against the order's -0.0108.
- **Seconds per point:** 1597 to 1697 s (D 21.125: 1504 to 1738 s). The load average, median over `scan/sampler.log`, was 9.71 (max 12.13; 8 processes here and the recount's 2), peak RSS per process 1.68 to 1.82 GiB (`/usr/bin/time -v`), MemAvailable at least 48.36 GiB.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (88%), 8 processes with the record system (90%), the repeat agrees (92%) | right |
| one robust change in the window (80%) | right |
| within 0.01 of 0.8613 (83%); within 0.005 (70%) | right (+0.000890) |
| the root between 0.8620 and 0.8645 (55%) | right (0.862190) |
| the float64 sign agrees with the hybrid at all 8 evaluations (30%) | WRONG (differs at 0.860 twice, 0.865 and 0.870) |
| each scan point 1300 to 2300 s (60%) | right (1597 to 1697 s) |
| the point done, no widening, within 50 min of the lane's start (65%) | right (29 min: 06:57:18 to 07:25:59) |
| the state on origin by 07:20 UTC (75%) | right (06:56:16 UTC, the commit time of 11ebcd94; interval 76.8 min) |

## Status
- 2026-11-24 06:10 UTC: folder and README written; the unit `i1025-leg-21_15625` is started next and waits for the state.
- 2026-11-24 07:26 UTC: the lane ended (scan 06:57:35 to 07:25:59, 8 of 8 exit 0); Result and scorecard above, 7 of 8 right (float64 sign). The state was on origin at 06:56:16 UTC and pinned at 06:57:14. This is the last point under tag f.
