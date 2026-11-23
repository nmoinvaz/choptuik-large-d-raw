# I1025-dh610/kc79_leg/D20.84375: lambda_1 on win2's k_c 79 leg point D 20.84375 (tag l1kc79Lw1025d), window 0.945 to 0.975 around the prediction 0.958

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-23 16:59 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45")
lambda_1 on win2's k_c 79 leg at D 20.84375: **predicted 0.958 +-0.01**; a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025d_D20.843750.npy` and record `l1kc79Lw1025d.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan).
- Grid centre 0.960 (the multiple of 0.005 nearest 0.958); the scan: 0.945, 0.950, 0.955, 0.960, 0.965, 0.970, 0.975 and a repeat of 0.960. The widening, if there is no robust change: low 0.940, 0.935, 0.930; high 0.980, 0.985, 0.990 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 20.84375 0.960 0.958` as the systemd user unit `i1025-leg-20_84375` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 20.84375 with both controls exit 1; all 8 processes print the record system; the repeat of 0.960 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.958 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; win2's states on this build: D 20.8125 passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (75%), none (17%), two or more (8%). The change within 0.01 of 0.958 (coordinator's reading): 55%; within 0.005: 35%.
- Each scan point takes 900 to 1900 s (65%); the point is done (no widening) within 45 min of the lane's start (70%).

## Status
- 2026-11-23 16:59 UTC: folder and README written; the unit waited for the state.
- 17:56 UTC: win2 pushed the state (commit 876aab69, `source_commit.txt`); 17:57:11 pins checked, selftests as wanted (0 0 1 1 0 0 1); 17:57:29 source check ACCEPTED, scan started; 18:28:02 scan done; 18:28:07 reading written, lane exit 0 (`exits_leg.txt`).

## Result (`summarize_leg.py 20.84375 0.958` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.945 | + | ++ (True) | + | -2342.9442587815265 | 1576 |
| 0.950 | + | ++ (True) | + | -2343.807275349622 | 1625 |
| 0.955 | + | ++ (True) | + | -2345.220979650325 | 1650 |
| 0.960 | - | -- (True) | - | -2345.7273501524696 | 1531 |
| 0.960 | - | -- (True) | - | -2345.7273501524696 | 1598 |
| 0.965 | - | -- (True) | - | -2344.9383178911608 | 1825 |
| 0.970 | - | -- (True) | - | -2344.777675905579 | 1742 |
| 0.975 | - | -- (True) | - | -2344.796622389299 | 1800 |

scan points: 8 evaluations, seconds per point min 1531, median 1638, max 1825, sum 13347; outside 900 to 1900 s: []
win2's record at D 20.84375: |F| 4.666490227259678e-10, steps 2694, constraint 0.004218466622892217, Delta 1.1140871985816614, h 0.03125, seconds 4730
float64 sign differs from the hybrid at: []

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D20.84375/scan 0.945 0.975
points 7 in 0.945-0.975; not noise-robust: none
hybrid signs: 0.945+ 0.950+ 0.955+ 0.960- 0.965- 0.970- 0.975-
float64 sign differs from the hybrid sign at: none
repeated points: [(0.96, 'agree')]
  robust change (0.955, 0.960), + to -, det-linear 0.958120, range [0.957532, 0.958120]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.945, - at 0.975
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D20.84375/scan/scan_D20.84375_all.jsonl: lambda [0.96]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.945+ 0.950+ 0.955+ 0.960- 0.965- 0.970- 0.975-
robust changes: 1
   change (0.955, 0.960), + to -, det-linear 0.958120, range [0.957532, 0.958120]
against the prediction 0.958: change minus prediction +0.000120; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's state and record at D 20.84375 (record |F| 4.6664902273e-10, the state's 4.6692553997e-10, 2694 steps = the record's), `--mutate=F` 1, `--mutate=steps` 1. All 8 processes printed the record system (|F| 4.6672965243e-10, 2694 steps).
- **One robust change in the window 0.945 to 0.975:** (0.955, 0.960), "+ to -", det-linear **0.958120**, estimator range [0.957532, 0.958120] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.945, - at 0.975). No ln|det| minimum without a sign change; every point noise-robust; the float64 sign equals the hybrid at all 8 evaluations.
- **The repeat of 0.960** (p3 and p7) is bit-identical (hybrid -, ln|det| -2345.7273501524696 in both; `repeat_check.py` PASS).
- **Against the coordinator's prediction 0.958 (+-0.01):** +0.000120, within 0.01. No widening was needed.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (88%), 8 processes with the record system (90%), the repeat agrees (92%) | right |
| one robust change in the window (75%) | right |
| within 0.01 of 0.958 (55%); within 0.005 (35%) | right (+0.000120) |
| each scan point 900 to 1900 s (65%) | right (1531 to 1825 s) |
| the point done within 45 min of the lane's start, no widening (70%) | right (31 min: 17:57:29 to 18:28:07) |
