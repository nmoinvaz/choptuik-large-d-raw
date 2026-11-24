# I1025-dh610/kc79_leg/D21.21875: lambda_1 on win2's k_c 79 leg point D 21.21875 (tag l1kc79Lw1025g), window 0.825 to 0.855 around the prediction 0.8413

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots, and the tag switch to g of 2026-11-24 07:27 UTC with its authorization check). Written 2026-11-24 09:16 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", the hc ruling for points past D 20.90625, and the hc ruling on the tag at win2's cap restart)
lambda_1 on win2's k_c 79 leg at D 21.21875: **predicted 0.8413 +-0.01** (the previous measured root 0.852069 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report. The state comes from win2's restarted k_c 79 leap under tag **l1kc79Lw1025g** (`tag.txt` is g, as at D 21.1875; the restart was checked against win2's README, `../README.md`): its record file `l1kc79Lw1025g.jsonl` and states are its own.

## This point
- State `sol_l1kc79Lw1025g_D21.218750.npy` and record `l1kc79Lw1025g.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). The first g state (D 21.1875) came 85 min after the restart began and its record says 4896 s, so I expect this one about 10:05 UTC (win2's points took 57 to 78 min under tag f).
- Grid centre 0.840 (the multiple of 0.005 nearest 0.8413; 0.0013 away; 0.845 lies 0.0037 away); the scan: 0.825, 0.830, 0.835, 0.840, 0.845, 0.850, 0.855 and a repeat of 0.840. The widening, if there is no robust change: low 0.820, 0.815, 0.810; high 0.860, 0.865, 0.870 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.21875 0.840 0.8413` as the systemd user unit `i1025-leg-21_21875` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`; every script reads `tag.txt`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.21875 with both controls exit 1; all 8 processes print the record system; the repeat of 0.840 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- `fetch_point.sh` exits 2 and the lane stops when the g record has no row for D 21.21875 with kc 79 or a blob differs from the commit's.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8413 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (82%), none (11%), two or more (7%). The change within 0.01 of 0.8413: 85%; within 0.005: 72%. The bracket is (0.840, 0.845): 80%.
- The measured steps so far are -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945, -0.009563, -0.009598, -0.009898 and -0.010121 against the prediction's -0.0108; the residuals against the registered predictions are +0.000120, +0.000951, +0.002234, +0.001041, +0.001370, +0.001338, +0.001494, +0.001849, +0.001286, +0.001188, +0.000890 and +0.000669, falling over the last five. I expect the root between 0.8410 and 0.8430 (60%).
- The float64 sign agrees with the hybrid at all 8 evaluations (25%; it differed at 1 to 4 grid points in each of the last five points).
- Each scan point takes 1300 to 2300 s (70%; the last point 1524 to 1709 s with the recount beside it). The point is done (no widening) within 50 min of the lane's start (70%; the last 29 min).
- The state is on origin by 10:30 UTC (75%).

## Result (`summarize_leg.py 21.21875 0.8413` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.825 | + | ++ (True) | + | -2297.094070155701 | 1576 |
| 0.830 | + | ++ (True) | + | -2297.84073598598 | 1527 |
| 0.835 | + | ++ (True) | - | -2298.8042659310718 | 1542 |
| 0.840 | + | ++ (True) | - | -2300.7464096105405 | 1591 |
| 0.840 | + | ++ (True) | - | -2300.7464096105405 | 1603 |
| 0.845 | - | -- (True) | - | -2300.112528923049 | 1547 |
| 0.850 | - | -- (True) | - | -2299.635058182109 | 1597 |
| 0.855 | - | -- (True) | - | -2299.56214077208 | 1543 |

scan points: 8 evaluations, seconds per point min 1527, median 1562, max 1603, sum 12526; outside 900 to 1900 s: []
win2's record at D 21.21875: |F| 4.564782766290151e-10, steps 2658, constraint 0.005482424492482856, Delta 1.1241182782455752, h 0.03125, seconds 4711
float64 sign differs from the hybrid at: [0.835, 0.84, 0.84]

```
=== read_lower.py .../D21.21875/scan 0.825 0.855
points 7 in 0.825-0.855; not noise-robust: none
hybrid signs: 0.825+ 0.830+ 0.835+ 0.840+ 0.845- 0.850- 0.855-
float64 sign differs from the hybrid sign at: [(0.835, '+', '-'), (0.84, '+', '-')]
repeated points: [(0.84, 'agree')]
  robust change (0.840, 0.845), + to -, det-linear 0.841733, range [0.841235, 0.841733]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.825, - at 0.855
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check .../D21.21875/scan/scan_D21.21875_all.jsonl: lambda [0.84]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.825+ 0.830+ 0.835+ 0.840+ 0.845- 0.850- 0.855-
robust changes: 1
   change (0.840, 0.845), + to -, det-linear 0.841733, range [0.841235, 0.841733]
against the prediction 0.8413: change minus prediction +0.000433; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag g state and record at D 21.21875 (record |F| 4.5647827663e-10, the state's 4.5653712486e-10, 2658 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system (|F| 4.5632156071e-10, 2658 steps). The state is blob 5d263c46, the record blob bf1b941f, both of win2's commit 2a8c4474 (2026-11-24 02:06:09 -08:00 = 10:06:09 UTC, 81.3 min after the D 21.1875 state; the record's seconds 4711). The g record now holds two rows (D 21.1875 and D 21.21875): |F| 4.578973943765308e-10 and 4.564782766290151e-10, steps 2660 and 2658, Delta 1.1232751318410306 and 1.1241182782455752.
- **One robust change in the window 0.825 to 0.855:** (0.840, 0.845), "+ to -", det-linear **0.841733**, estimator range [0.841235, 0.841733] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.825, - at 0.855). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.840** (p3 and p7) is bit-identical (hybrid +, ln|det| -2300.7464096105405 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.835 and 0.840 (0.840 twice), below the change:** the float64 signs along the grid are + + - - - - -, which alone would read the change in (0.830, 0.835), 0.010 below the hybrid's bracket. The hybrid is read (one change, in (0.840, 0.845)). At D 21.1875 it differed at 0.860 only, above the change; at D 21.15625 at 0.860, 0.865 and 0.870.
- **Against the prediction 0.8413 (+-0.01, the previous root 0.852069 minus 0.0108):** +0.000433, within 0.01 (and within 0.005). No widening was needed.
- **Roots on the leg so far (det-linear, as measured):** 0.958120 (D 20.84375), 0.947951 (D 20.875), 0.938234 (D 20.90625), 0.928441 (D 20.9375), 0.918970 (D 20.96875), 0.909538 (D 21.0), 0.900194 (D 21.03125), 0.891249 (D 21.0625), 0.881686 (D 21.09375), 0.872088 (D 21.125), 0.862190 (D 21.15625), 0.852069 (D 21.1875), 0.841733 (D 21.21875): steps -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945, -0.009563, -0.009598, -0.009898, -0.010121 and -0.010336 per 0.03125 in D, against the order's -0.0108.
- **Seconds per point:** 1527 to 1603 s. The load average, median over `scan/sampler.log`, was 9.05 (max 9.34; 8 processes here and the recount's 2), peak RSS per process 1.58 to 1.76 GiB (`/usr/bin/time -v`), MemAvailable at least 48.39 GiB.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (88%), 8 processes with the record system (90%), the repeat agrees (92%) | right |
| one robust change in the window (82%) | right |
| within 0.01 of 0.8413 (85%); within 0.005 (72%) | right (+0.000433) |
| the bracket is (0.840, 0.845) (80%) | right |
| the root between 0.8410 and 0.8430 (60%) | right (0.841733) |
| the float64 sign agrees with the hybrid at all 8 evaluations (25%) | WRONG (differs at 0.835 and 0.840 twice) |
| each scan point 1300 to 2300 s (70%) | right (1527 to 1603 s) |
| the point done, no widening, within 50 min of the lane's start (70%) | right (27 min: 10:06:38 to 10:33:35) |
| the state on origin by 10:30 UTC (75%) | right (10:06:09 UTC, the commit time of 2a8c4474; interval 81.3 min) |

## Status
- 2026-11-24 09:16 UTC: folder and README written; the unit `i1025-leg-21_21875` is started next and waits for the state.
- 2026-11-24 10:36 UTC: lane done (10:06:38 to 10:33:35 UTC): result and scorecard above, parent row added. The next point is D 21.25 (`../D21.25/`).
