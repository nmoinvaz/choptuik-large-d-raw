# I1025-dh610/kc79_leg/D20.875: lambda_1 on win2's k_c 79 leg point D 20.875 (tag l1kc79Lw1025d), window 0.930 to 0.960 around the prediction 0.947

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-23 16:59 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45")
lambda_1 on win2's k_c 79 leg at D 20.875: **predicted 0.947 +-0.01**; a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025d_D20.875000.npy` and record `l1kc79Lw1025d.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan).
- Grid centre 0.945 (the multiple of 0.005 nearest 0.947); the scan: 0.930, 0.935, 0.940, 0.945, 0.950, 0.955, 0.960 and a repeat of 0.945. The widening, if there is no robust change: low 0.925, 0.920, 0.915; high 0.965, 0.970, 0.975 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 20.875 0.945 0.947` as the systemd user unit `i1025-leg-20_875` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 20.875 with both controls exit 1; all 8 processes print the record system; the repeat of 0.945 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.947 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; win2's states on this build: D 20.8125 passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (75%), none (17%), two or more (8%). The change within 0.01 of 0.947 (coordinator's reading): 50%; within 0.005: 30%.
- Each scan point takes 900 to 1900 s (65%); the point is done (no widening) within 45 min of the lane's start (70%).

## Status
- 2026-11-23 16:59 UTC: folder and README written; the unit waits for the state (expected about 19:15 UTC).

- 19:15:56 UTC: win2 pushed the state (commit 784040c7, `source_commit.txt`, with its fold-watch notice and the restart under tag l1kc79Lw1025f, below); 19:16:38 pins checked, 19:16:43 selftests as wanted (0 0 1 1 0 0 1); 19:17:17 source check ACCEPTED, scan started; 19:58:34 scan done; 19:58:38 reading written, lane exit 0 (`exits_leg.txt`).
- The state of this point is the leg point under the coordinator's ruling ("The D 20.875 state stands as the leg point (dh610 scans it now)", quoted in `../../I1025-win2/kc79_leap/README.md`): win2's fold watch fired after this point (n_null 72 -> 71, a mode entering the regular set), and its leap restarts from the D 20.84375 and D 20.875 states at h 0.03125 under the new tag l1kc79Lw1025f. The point after this one is therefore in tag f's files, not tag d's (see the parent README).

## Result (`summarize_leg.py 20.875 0.947` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.930 | + | ++ (True) | + | -2338.28360852358 | 2345 |
| 0.935 | + | ++ (True) | + | -2338.9853439726116 | 2162 |
| 0.940 | + | ++ (True) | + | -2339.861072722775 | 2021 |
| 0.945 | + | ++ (True) | - | -2341.3239672970544 | 2296 |
| 0.945 | + | ++ (True) | - | -2341.3239672970544 | 2435 |
| 0.950 | - | -- (True) | - | -2341.689053478801 | 2244 |
| 0.955 | - | -- (True) | - | -2340.9539623988658 | 2474 |
| 0.960 | - | -- (True) | - | -2340.8065308475234 | 2115 |

scan points: 8 evaluations, seconds per point min 2021, median 2270, max 2474, sum 18092; outside 900 to 1900 s: [(0.93, 2345), (0.935, 2162), (0.94, 2021), (0.945, 2296), (0.945, 2435), (0.95, 2244), (0.955, 2474), (0.96, 2115)]
win2's record at D 20.875: |F| 4.663164479998315e-10, steps 2689, constraint 0.004315887956416221, Delta 1.1149160696722138, h 0.03125, seconds 4612
float64 sign differs from the hybrid at: [0.945, 0.945]

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D20.875/scan 0.930 0.960
points 7 in 0.930-0.960; not noise-robust: none
hybrid signs: 0.930+ 0.935+ 0.940+ 0.945+ 0.950- 0.955- 0.960-
float64 sign differs from the hybrid sign at: [(0.945, '+', '-')]
repeated points: [(0.945, 'agree')]
  robust change (0.945, 0.950), + to -, det-linear 0.947951, range [0.947354, 0.947951]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.930, - at 0.960
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D20.875/scan/scan_D20.875_all.jsonl: lambda [0.945]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.930+ 0.935+ 0.940+ 0.945+ 0.950- 0.955- 0.960-
robust changes: 1
   change (0.945, 0.950), + to -, det-linear 0.947951, range [0.947354, 0.947951]
against the prediction 0.947: change minus prediction +0.000951; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's state and record at D 20.875 (record |F| 4.6631644800e-10, the state's 4.6614736747e-10, 2689 steps = the record's), `--mutate=F` 1, `--mutate=steps` 1 (`src/syscheck*.txt`). All 8 processes printed the record system (|F| 4.6644138846e-10, 2689 steps).
- **One robust change in the window 0.930 to 0.960:** (0.945, 0.950), "+ to -", det-linear **0.947951**, estimator range [0.947354, 0.947951] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.930, - at 0.960). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.945** (p3 and p7) is bit-identical (hybrid +, ln|det| -2341.3239672970544 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.945, in both evaluations** (float64 -, hybrid +; the hybrid's noise test is robust at that point). The hybrid sign is the one read; this point is the grid point beside the change (0.947951 lies 0.003 above it). No other point differs. At D 20.84375 no point differed.
- **Against the coordinator's prediction 0.947 (+-0.01):** +0.000951, within 0.01. No widening was needed.
- **Seconds per point were longer than at D 20.84375** (2021 to 2474 s here, 1531 to 1825 s there). This scan ran beside the d19_k95 regrid (8 threads, started 18:31 UTC) and the #1076 recount; the earlier scan ran beside the recount only. That is a likely cause, not tested.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (88%), 8 processes with the record system (90%), the repeat agrees (92%) | right |
| one robust change in the window (75%) | right |
| within 0.01 of 0.947 (50%); within 0.005 (30%) | right (+0.000951) |
| each scan point 900 to 1900 s (65%) | WRONG: all 8 evaluations took 2021 to 2474 s |
| the point done within 45 min of the lane's start, no widening (70%) | right (41 min: 19:16:42 to 19:58:38) |
