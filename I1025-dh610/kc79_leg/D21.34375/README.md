# I1025-dh610/kc79_leg/D21.34375: lambda_1 on win2's k_c 79 leg point D 21.34375 (tag l1kc79Lw1025g), window 0.785 to 0.815 around the prediction 0.7987

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots, and the tag switch to g of 2026-11-24 07:27 UTC with its authorization check). Written 2026-11-24 14:37 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical. **The same D is a shared D of win2's far scout (tag i, h 0.0625): `../../kc79_far/D21.34375/` compares the two states side by side and, by the coordinator's order of 24 Nov (hc), scans the tag i state with this window and this rule too; the two roots are reported together.**

## Order for this point (coordinator t5, #1025 comment of "17:45", the hc ruling for points past D 20.90625, and the hc ruling on the tag at win2's cap restart)
lambda_1 on win2's k_c 79 leg at D 21.34375: **predicted 0.7987 +-0.01** (the previous measured root 0.809549 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report. The state comes from win2's restarted k_c 79 leap under tag **l1kc79Lw1025g** (`tag.txt` is g, as at D 21.1875 to D 21.3125): its record file `l1kc79Lw1025g.jsonl` and states are its own.

## This point
- State `sol_l1kc79Lw1025g_D21.343750.npy` and record `l1kc79Lw1025g.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). The g states came 85.0, 81.3, 76.6, 79.5 and 77.6 min apart (records 4896, 4711, 4544, 4578 and 4584 s); the last landed at 13:59:53 UTC, so I expect this one about 15:15 to 15:25 UTC. The tag i state of this D is on origin since 14:34:00 UTC (win2 commit 9bb1884b).
- Grid centre 0.800 (the multiple of 0.005 nearest 0.7987; 0.0013 away; 0.795 lies 0.0037 away); the scan: 0.785, 0.790, 0.795, 0.800, 0.805, 0.810, 0.815 and a repeat of 0.800. The widening, if there is no robust change: low 0.780, 0.775, 0.770; high 0.820, 0.825, 0.830 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.34375 0.800 0.7987` as the systemd user unit `i1025-leg-21_34375` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`, scan at nice 5; every script reads `tag.txt`). The far lane's tag i scan of the same D starts after the comparison, beside this one (nominal threads: 8 + 8 + the recount's 12 = 28, nice 5, 8 and 10).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.34375 with both controls exit 1; all 8 processes print the record system; the repeat of 0.800 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- `fetch_point.sh` exits 2 and the lane stops when the g record has no row for D 21.34375 with kc 79 or a blob differs from the commit's.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.7987 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (91%), all 8 processes print the record system (92%), the repeat agrees (92%).
- One robust change in the window (84%), none (9%), two or more (7%). The change within 0.01 of 0.7987: 90%; within 0.005: 80%. The last steps are -0.010121, -0.010336, -0.010576, -0.010979 and -0.010629 against the prediction's -0.0108: the growth in their size stopped at the last point, so I expect a step of -0.0105 to -0.0110 and the root between 0.7975 and 0.8005 (60%). The bracket is (0.795, 0.800) (80%; it needs a step larger than 0.009549 in size, and the last eight were; (0.800, 0.805) needs a smaller one).
- The float64 sign agrees with the hybrid at all 8 evaluations (15%; it differed at 1 to 3 grid points in each of the last nine points, at 1 in the last two).
- Each scan point takes 1500 to 2600 s (60%; the last point 1802 to 1921 s; the far lane's tag i scan of this D runs beside this one, which raises it). The point is done (no widening) within 60 min of the lane's start (65%; the last 32 min).
- The state is on origin by 15:30 UTC (80%).

## Result (`summarize_leg.py 21.34375 0.7987` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.785 | + | ++ (True) | + | -2281.791622302807 | 4518 |
| 0.790 | + | ++ (True) | + | -2282.634517130593 | 4549 |
| 0.795 | + | ++ (True) | + | -2283.9166492174295 | 4497 |
| 0.800 | - | -- (True) | - | -2285.034941053603 | 4586 |
| 0.800 | - | -- (True) | - | -2285.034941053603 | 4611 |
| 0.805 | - | -- (True) | - | -2283.9991526138233 | 4430 |
| 0.810 | - | -- (True) | - | -2283.8119153279763 | 4597 |
| 0.815 | - | -- (True) | + | -2283.829836605837 | 4412 |

scan points: 8 evaluations, seconds per point min 4412, median 4534, max 4611, sum 36200; outside 900 to 1900 s: [(0.785, 4518), (0.79, 4549), (0.795, 4497), (0.8, 4586), (0.8, 4611), (0.805, 4430), (0.81, 4597), (0.815, 4412)]
win2's record at D 21.34375: |F| 4.484968788840308e-10, steps 2648, constraint 0.005950886267504929, Delta 1.1275035270998226, h 0.03125, seconds 2808
float64 sign differs from the hybrid at: [0.815]

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D21.34375/scan 0.785 0.815
points 7 in 0.785-0.815; not noise-robust: none
hybrid signs: 0.785+ 0.790+ 0.795+ 0.800- 0.805- 0.810- 0.815-
float64 sign differs from the hybrid sign at: [(0.815, '-', '+')]
repeated points: [(0.8, 'agree')]
  robust change (0.795, 0.800), + to -, det-linear 0.798768, range [0.798216, 0.798768]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.785, - at 0.815
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D21.34375/scan/scan_D21.34375_all.jsonl: lambda [0.8]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.785+ 0.790+ 0.795+ 0.800- 0.805- 0.810- 0.815-
robust changes: 1
   change (0.795, 0.800), + to -, det-linear 0.798768, range [0.798216, 0.798768]
against the prediction 0.7987: change minus prediction +0.000068; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag g state and record at D 21.34375 (record |F| 4.4849687888e-10, the state's 4.4900336580e-10, 2648 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system. The state and record are of win2's commit 451fee48 (2026-11-24 06:48:05 -08:00 = 14:48:05 UTC, **48.2 min** after the D 21.3125 state, record seconds 2808, against 4584 s there). The record's row: |F| 4.484968788840308e-10, steps 2648, Delta 1.1275035270998226, constraint 0.005950886267504929.
- **One robust change in the window 0.785 to 0.815:** (0.795, 0.800), "+ to -", det-linear **0.798768**, estimator range [0.798216, 0.798768] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.785, - at 0.815). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.800** is bit-identical (hybrid -, ln|det| -2285.034941053603 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.815, above the change** (float64 signs along the grid + + + - - - +: two changes in float64, one in the hybrid; the hybrid is read). At D 21.3125 it differed at 0.795, below the change; at D 21.28125 at 0.830.
- **Against the prediction 0.7987 (+-0.01, the previous root 0.809549 minus 0.0108):** +0.000068, within 0.01 and 0.005. No widening. The step from the previous root is -0.010781 (the last ones -0.010979, -0.010629).
- **The same D at tag i:** the far scout's state of this D (win2 commit 9bb1884b, 14:34:00 UTC) was scanned with the same window and rule: `../../kc79_far/D21.34375/` (`i/`, `roots_pair.txt`): root 0.798701, bracket (0.795, 0.800), so i - g = -0.000067 (the Delta entries differ by +4.1034e-06).
- **Seconds per point: 4412 to 4611 s, 2.4 times the 1802 to 1921 s of D 21.3125.** The tag i scan (8 processes, nice 8) ran beside this one from 14:49 to 16:03 UTC, and the recount's two workers beside both: the load average, median over `scan/sampler.log` (153 samples, 14:49:24 to 16:05:53 UTC), was 18.15 (max 28.91), peak RSS per process 1.64 to 1.76 GiB (`/usr/bin/time -v`), MemAvailable at least 38.62 GiB. The lane ran 14:48:40 to 16:06:15 UTC, 77.6 min, against 32 min alone.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (91%), 8 processes with the record system (92%), the repeat agrees (92%) | right |
| one robust change in the window (84%) | right |
| within 0.01 of 0.7987 (90%); within 0.005 (80%) | right (+0.000068) |
| the root between 0.7975 and 0.8005 (60%) | right (0.798768) |
| the bracket is (0.795, 0.800) (80%) | right |
| the float64 sign agrees with the hybrid at all 8 evaluations (15%) | WRONG (differs at 0.815) |
| each scan point 1500 to 2600 s (60%) | WRONG (4412 to 4611 s: the two scans and the recount shared 20 logical CPUs) |
| the point done, no widening, within 60 min of the lane's start (65%) | WRONG (77.6 min: 14:48:40 to 16:06:15) |
| the state on origin by 15:30 UTC (80%) | right (14:48:05 UTC; my unscored expectation 15:15 to 15:25 was WRONG) |

## Status
- 2026-11-24 14:37 UTC: folder and README written; the unit `i1025-leg-21_34375` is started next and waits for the state.
- 2026-11-24 16:07 UTC: lane done (14:48:40 to 16:06:15 UTC): result and scorecard above, parent row added. The next point is D 21.375 (`../D21.375/`).
