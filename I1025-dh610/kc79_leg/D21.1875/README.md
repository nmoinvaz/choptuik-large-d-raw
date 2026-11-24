# I1025-dh610/kc79_leg/D21.1875: lambda_1 on win2's k_c 79 leg point D 21.1875 (tag l1kc79Lw1025g, the first point of the cap restart), window 0.835 to 0.865 around the prediction 0.8514

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots, and the tag switch to g of 2026-11-24 07:27 UTC with its authorization check). Written 2026-11-24 07:27 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", the hc ruling for points past D 20.90625, and the hc ruling on the tag at win2's cap restart)
lambda_1 on win2's k_c 79 leg at D 21.1875: **predicted 0.8514 +-0.01** (the previous measured root 0.862190 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report. The state comes from win2's restarted k_c 79 leap under tag **l1kc79Lw1025g** (`tag.txt` is g; the restart was checked against win2's README, `../README.md`): its record file `l1kc79Lw1025g.jsonl` and states are its own, started from the tag f states of D 21.125 and D 21.15625.

## This point
- State `sol_l1kc79Lw1025g_D21.187500.npy` and record `l1kc79Lw1025g.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). The first g state is expected about 08:35 UTC (the restart began at 07:19:49 UTC; a point takes win2 about 4500 s).
- Grid centre 0.850 (the multiple of 0.005 nearest 0.8514; 0.0014 away; 0.855 lies 0.0036 away); the scan: 0.835, 0.840, 0.845, 0.850, 0.855, 0.860, 0.865 and a repeat of 0.850. The widening, if there is no robust change: low 0.830, 0.825, 0.820; high 0.870, 0.875, 0.880 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 21.1875 0.850 0.8514` as the systemd user unit `i1025-leg-21_1875` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`; every script reads `tag.txt`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 21.1875 with both controls exit 1; all 8 processes print the record system; the repeat of 0.850 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Checks specific to the restart: `fetch_point.sh` exits 2 and the lane stops when the g record has no row for D 21.1875 with kc 79 or a blob differs from the commit's (the state's path names the tag, so a state not under tag g is never found). By hand, after the pins, I compare the g record's rows for D 21.125 and D 21.15625 (if it carries them) with tag f's by |F| and steps and report the result; that comparison does not gate the lane.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.8514 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (86%; the eleven earlier points passed, this is the first state of a restarted leap, as D 20.90625 was under tag f), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (13%), two or more (7%). The change within 0.01 of 0.8514: 83%; within 0.005: 70%. The measured steps so far are -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945, -0.009563, -0.009598 and -0.009898 against the prediction's -0.0108 and the residuals +0.000120, +0.000951, +0.002234, +0.001041, +0.001370, +0.001338, +0.001494, +0.001849, +0.001286, +0.001188, +0.000890: I expect the root between 0.8520 and 0.8545 (55%).
- The float64 sign agrees with the hybrid at all 8 evaluations (25%; it differed at 2 to 4 grid points in each of the last four points).
- Each scan point takes 1400 to 2300 s (65%; the last three points 1504 to 2574 s; this scan runs beside the recount only). The point is done (no widening) within 50 min of the lane's start (65%; the last 29 min).
- The state is on origin by 09:00 UTC (75%; win2's points take about 4500 s, the restart began 07:19:49 UTC).

## Result (`summarize_leg.py 21.1875 0.8514` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.835 | + | ++ (True) | + | -2300.63290851637 | 1529 |
| 0.840 | + | ++ (True) | + | -2301.3727119398804 | 1680 |
| 0.845 | + | ++ (True) | + | -2302.317336005788 | 1709 |
| 0.850 | + | ++ (True) | + | -2304.105352056101 | 1580 |
| 0.850 | + | ++ (True) | + | -2304.105352056101 | 1651 |
| 0.855 | - | -- (True) | - | -2303.7571574782423 | 1647 |
| 0.860 | - | -- (True) | + | -2303.231453777005 | 1524 |
| 0.865 | - | -- (True) | - | -2303.1467560334577 | 1575 |

scan points: 8 evaluations, seconds per point min 1524, median 1614, max 1709, sum 12895; outside 900 to 1900 s: []
win2's record at D 21.1875: |F| 4.578973943765308e-10, steps 2660, constraint 0.005369055634728287, Delta 1.1232751318410306, h 0.03125, seconds 4896
float64 sign differs from the hybrid at: [0.86]

```
=== read_lower.py .../D21.1875/scan 0.835 0.865
points 7 in 0.835-0.865; not noise-robust: none
hybrid signs: 0.835+ 0.840+ 0.845+ 0.850+ 0.855- 0.860- 0.865-
float64 sign differs from the hybrid sign at: [(0.86, '-', '+')]
repeated points: [(0.85, 'agree')]
  robust change (0.850, 0.855), + to -, det-linear 0.852069, range [0.851510, 0.852069]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.835, - at 0.865
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check .../D21.1875/scan/scan_D21.1875_all.jsonl: lambda [0.85]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.835+ 0.840+ 0.845+ 0.850+ 0.855- 0.860- 0.865-
robust changes: 1
   change (0.850, 0.855), + to -, det-linear 0.852069, range [0.851510, 0.852069]
against the prediction 0.8514: change minus prediction +0.000669; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag g state and record at D 21.1875 (record |F| 4.5789739438e-10, the state's 4.5775553374e-10, 2660 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system (|F| 4.5787142027e-10, 2660 steps). The state is blob 9d3351f6, the record blob e5cac323, both of win2's commit 0b106614 (2026-11-24 00:44:49 -08:00 = 08:44:49 UTC, 85 min after the restart began at 07:19:49 UTC; the record's seconds 4896).
- **The restart check by hand:** the tag g record `l1kc79Lw1025g.jsonl` holds one row, D 21.1875; it carries no rows for D 21.125 and D 21.15625, so there was nothing to compare with tag f's. The three points run continuously across the switch: |F| 4.605990614286346e-10 (D 21.125, f), 4.5897952881747886e-10 (D 21.15625, f), 4.578973943765308e-10 (D 21.1875, g); steps 2667, 2664, 2660; Delta 1.1215928048382566, 1.122433147959886, 1.1232751318410306.
- **One robust change in the window 0.835 to 0.865:** (0.850, 0.855), "+ to -", det-linear **0.852069**, estimator range [0.851510, 0.852069] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.835, - at 0.865). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.850** (p3 and p7) is bit-identical (hybrid +, ln|det| -2304.105352056101 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.860 only** (float64 + where the hybrid reads -): the float64 signs along the grid are + + + + - + -, which alone would read as three changes. The hybrid is read (one change). It differed at four evaluations at D 21.15625, two at D 21.125 and D 21.09375, three at D 21.0625.
- **Against the prediction 0.8514 (+-0.01, the previous root 0.862190 minus 0.0108):** +0.000669, within 0.01 (and within 0.005). No widening was needed.
- **Roots on the leg so far (det-linear, as measured):** 0.958120 (D 20.84375), 0.947951 (D 20.875), 0.938234 (D 20.90625), 0.928441 (D 20.9375), 0.918970 (D 20.96875), 0.909538 (D 21.0), 0.900194 (D 21.03125), 0.891249 (D 21.0625), 0.881686 (D 21.09375), 0.872088 (D 21.125), 0.862190 (D 21.15625), 0.852069 (D 21.1875, tag g): steps -0.010169, -0.009717, -0.009793, -0.009471, -0.009432, -0.009344, -0.008945, -0.009563, -0.009598, -0.009898 and -0.010121 per 0.03125 in D, against the order's -0.0108.
- **Seconds per point:** 1524 to 1709 s. The load average, median over `scan/sampler.log`, was 10.06 (max 11.07; 8 processes here and the recount's 2), peak RSS per process 1.64 to 1.82 GiB (`/usr/bin/time -v`), MemAvailable at least 48.42 GiB.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (86%), 8 processes with the record system (90%), the repeat agrees (92%) | right |
| one robust change in the window (80%) | right |
| within 0.01 of 0.8514 (83%); within 0.005 (70%) | right (+0.000669) |
| the root between 0.8520 and 0.8545 (55%) | right (0.852069; the range's low end 0.851510 lies below 0.8520) |
| the float64 sign agrees with the hybrid at all 8 evaluations (25%) | WRONG (differs at 0.860) |
| each scan point 1400 to 2300 s (65%) | right (1524 to 1709 s) |
| the point done, no widening, within 50 min of the lane's start (65%) | right (29 min: 08:45:54 to 09:14:49) |
| the state on origin by 09:00 UTC (75%) | right (08:44:49 UTC, the commit time of 0b106614; 85.0 min after the restart began) |

## Status
- 2026-11-24 07:27 UTC: folder and README written; the unit `i1025-leg-21_1875` is started next and waits for the state.
- 2026-11-24 09:17 UTC: lane done (08:45:54 to 09:14:49 UTC): result and scorecard above, parent row added. The next point is D 21.21875 (`../D21.21875/`).
