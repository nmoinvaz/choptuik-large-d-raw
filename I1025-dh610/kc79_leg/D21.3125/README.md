# I1025-dh610/kc79_leg/D21.3125: lambda_1 on win2's k_c 79 leg point D 21.3125 (tag l1kc79Lw1025g), window 0.795 to 0.825 around the prediction 0.8094

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots, and the tag switch to g of 2026-11-24 07:27 UTC with its authorization check). Written 2026-11-24 13:16 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical. This D is not a point of win2's far scout (tag i, h 0.0625: its D are 21.28125, 21.34375, ...), so the far lane has no part in it.

## Order for this point (coordinator t5, #1025 comment of "17:45", the hc ruling for points past D 20.90625, and the hc ruling on the tag at win2's cap restart)
lambda_1 on win2's k_c 79 leg at D 21.3125: **predicted 0.8094 +-0.01** (the previous measured root 0.820178 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report. The state comes from win2's restarted k_c 79 leap under tag **l1kc79Lw1025g** (`tag.txt` is g, as at D 21.1875 to D 21.28125): its record file `l1kc79Lw1025g.jsonl` and states are its own.

## This point
- State `sol_l1kc79Lw1025g_D21.312500.npy` and record `l1kc79Lw1025g.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). The g states came 85.0, 81.3, 76.6 and 79.5 min apart (records 4896, 4711, 4544 and 4578 s); the last landed at 12:42:19 UTC, so I expect this one about 13:58 to 14:08 UTC.
- Grid centre 0.810 (the multiple of 0.005 nearest 0.8094; 0.0006 away; 0.805 lies 0.0044 away); the scan: 0.795, 0.800, 0.805, 0.810, 0.815, 0.820, 0.825 and a repeat of 0.810. The widening, if there is no robust change: low 0.790, 0.785, 0.780; high 0.830, 0.835, 0.840 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.3125 0.810 0.8094` as the systemd user unit `i1025-leg-21_3125` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`, scan at nice 5; every script reads `tag.txt`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.3125 with both controls exit 1; all 8 processes print the record system; the repeat of 0.810 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- `fetch_point.sh` exits 2 and the lane stops when the g record has no row for D 21.3125 with kc 79 or a blob differs from the commit's.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8094 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (91%), all 8 processes print the record system (92%), the repeat agrees (92%).
- One robust change in the window (84%), none (9%), two or more (7%). The change within 0.01 of 0.8094: 90%; within 0.005: 80%. The measured steps are -0.009344, -0.008945, -0.009563, -0.009598, -0.009898, -0.010121, -0.010336, -0.010576 and -0.010979 (the last three steps grew in size by 0.000240 and 0.000403) against the prediction's -0.0108; the residuals against the registered predictions were +0.000433, +0.000257 and -0.000222, so the residual has crossed zero. If the step grows by 0.0003 to 0.0005 again, it is about -0.0113 to -0.0115 and the root about 0.8087 to 0.8090 (residual about -0.0005 to -0.0007); the root between 0.8075 and 0.8105 (60%). The bracket is (0.805, 0.810) (75%; it needs a step between -0.0102 and -0.0152; (0.810, 0.815) needs the step to fall back below 0.0102 in size, but the sizes have grown at every point since D 21.0625: 0.008945, 0.009563, 0.009598, 0.009898, 0.010121, 0.010336, 0.010576, 0.010979).
- The float64 sign agrees with the hybrid at all 8 evaluations (15%; it differed at 1 to 3 grid points in each of the last eight points, at 1 in the last).
- Each scan point takes 1500 to 2600 s (65%; the last point 1800 to 1900 s, with the recount's workers beside). The point is done (no widening) within 60 min of the lane's start (70%; the last 32 min).
- The state is on origin by 14:10 UTC (75%).

## Result (`summarize_leg.py 21.3125 0.8094` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.795 | + | ++ (True) | - | -2285.7013983531233 | 1921 |
| 0.800 | + | ++ (True) | + | -2286.5059895432037 | 1880 |
| 0.805 | + | ++ (True) | + | -2287.6459393782375 | 1871 |
| 0.810 | - | -- (True) | - | -2289.958189286981 | 1802 |
| 0.810 | - | -- (True) | - | -2289.958189286981 | 1847 |
| 0.815 | - | -- (True) | - | -2288.1468804965416 | 1821 |
| 0.820 | - | -- (True) | - | -2287.8888947301457 | 1888 |
| 0.825 | - | -- (True) | - | -2287.881183769819 | 1827 |

scan points: 8 evaluations, seconds per point min 1802, median 1859, max 1921, sum 14857; outside 900 to 1900 s: [(0.795, 1921)]
win2's record at D 21.3125: |F| 4.5111069749892923e-10, steps 2651, constraint 0.0058315057880221925, Delta 1.1266552092474795, h 0.03125, seconds 4584
float64 sign differs from the hybrid at: [0.795]

```
=== read_lower.py D21.3125/scan 0.795 0.825
points 7 in 0.795-0.825; not noise-robust: none
hybrid signs: 0.795+ 0.800+ 0.805+ 0.810- 0.815- 0.820- 0.825-
float64 sign differs from the hybrid sign at: [(0.795, '+', '-')]
repeated points: [(0.81, 'agree')]
  robust change (0.805, 0.810), + to -, det-linear 0.809549, range [0.809252, 0.809549]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.795, - at 0.825
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check D21.3125/scan/scan_D21.3125_all.jsonl: lambda [0.81]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.795+ 0.800+ 0.805+ 0.810- 0.815- 0.820- 0.825-
robust changes: 1
   change (0.805, 0.810), + to -, det-linear 0.809549, range [0.809252, 0.809549]
against the prediction 0.8094: change minus prediction +0.000149; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag g state and record at D 21.3125 (record |F| 4.5111069750e-10, the state's 4.5093447202e-10, 2651 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system. The state and record are of win2's commit 8503773d (2026-11-24 05:59:53 -08:00 = 13:59:53 UTC, 77.6 min after the D 21.28125 state; the record's seconds 4584). The g record's rows run on: |F| 4.5485512502509616e-10, 4.5267187993303683e-10, 4.5111069749892923e-10, steps 2656, 2652, 2651, Delta 1.1249625860927213, 1.1258083077444154, 1.1266552092474795, constraint 0.005713642093285211 at D 21.28125 and 0.0058315057880221925 here.
- **One robust change in the window 0.795 to 0.825:** (0.805, 0.810), "+ to -", det-linear **0.809549**, estimator range [0.809252, 0.809549] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.795, - at 0.825). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.810** (p3 and p7) is bit-identical (hybrid -, ln|det| -2289.958189286981 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.795, below the change:** the float64 signs along the grid are - + + - - - -, so float64 alone would read two changes, - to + in (0.795, 0.800) and + to - in (0.805, 0.810). The hybrid is read (one change, in (0.805, 0.810)). At D 21.28125 it differed at 0.830, above the change; at D 21.25 at 0.835, 0.840 and 0.845, above the change.
- **Against the prediction 0.8094 (+-0.01, the previous root 0.820178 minus 0.0108):** +0.000149, within 0.01 (and within 0.005). No widening was needed. The step is -0.010629 per 0.03125, smaller in size than the last (-0.010979): the growth in the step's size that I expected to continue (root about 0.8087 to 0.8090) did not; the root lies above that range, inside the registered range 0.8075 to 0.8105.
- **Roots on the leg so far (det-linear, as measured):** 0.958120 (D 20.84375), 0.947951 (D 20.875), 0.938234 (D 20.90625), 0.928441 (D 20.9375), 0.918970 (D 20.96875), 0.909538 (D 21.0), 0.900194 (D 21.03125), 0.891249 (D 21.0625), 0.881686 (D 21.09375), 0.872088 (D 21.125), 0.862190 (D 21.15625), 0.852069 (D 21.1875), 0.841733 (D 21.21875), 0.831157 (D 21.25), 0.820178 (D 21.28125), 0.809549 (D 21.3125): steps -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945, -0.009563, -0.009598, -0.009898, -0.010121, -0.010336, -0.010576, -0.010979 and -0.010629 per 0.03125 in D, against the order's -0.0108.
- **Seconds per point:** 1802 to 1921 s (D 21.28125: 1800 to 1900 s); the summary's bar of 900 to 1900 s lists 0.795 at 1921 s. The load average, median over `scan/sampler.log` (64 samples), was 10.0 (max 11.35; 8 processes here at nice 5, and the recount's workers beside them), peak RSS per process 1.61 to 1.76 GiB (`/usr/bin/time -v`), MemAvailable at least 48.11 GiB.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (91%), 8 processes with the record system (92%), the repeat agrees (92%) | right |
| one robust change in the window (84%) | right |
| within 0.01 of 0.8094 (90%); within 0.005 (80%) | right (+0.000149) |
| the bracket is (0.805, 0.810) (75%) | right |
| the root between 0.8075 and 0.8105 (60%) | right (0.809549) |
| the float64 sign agrees with the hybrid at all 8 evaluations (15%) | WRONG (differs at 0.795) |
| each scan point 1500 to 2600 s (65%) | right (1802 to 1921 s) |
| the point done, no widening, within 60 min of the lane's start (70%) | right (32.4 min: 14:01:04 to 14:33:26) |
| the state on origin by 14:10 UTC (75%) | right (13:59:53 UTC, the commit time of 8503773d; interval 77.6 min) |

## Status
- 2026-11-24 13:16 UTC: folder and README written; the unit `i1025-leg-21_3125` is started next and waits for the state.
- 2026-11-24 14:37 UTC: lane done (14:01:04 to 14:33:26 UTC): result and scorecard above, parent row added. The next point is D 21.34375 (`../D21.34375/`).
