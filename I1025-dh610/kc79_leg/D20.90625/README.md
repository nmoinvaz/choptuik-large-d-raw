# I1025-dh610/kc79_leg/D20.90625: lambda_1 on win2's k_c 79 leg point D 20.90625 (tag l1kc79Lw1025f, restarted leap; see Status), window 0.920 to 0.950 around the prediction 0.936

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-23 16:59 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45")
lambda_1 on win2's k_c 79 leg at D 20.90625: **predicted 0.936 +-0.01**; a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D20.906250.npy` and record `l1kc79Lw1025f.jsonl` (changed at 20:01 UTC from tag d, see Status) of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan).
- Grid centre 0.935 (the multiple of 0.005 nearest 0.936); the scan: 0.920, 0.925, 0.930, 0.935, 0.940, 0.945, 0.950 and a repeat of 0.935. The widening, if there is no robust change: low 0.915, 0.910, 0.905; high 0.955, 0.960, 0.965 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 20.90625 0.935 0.936` as the systemd user unit `i1025-leg-20_90625` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 20.90625 with both controls exit 1; all 8 processes print the record system; the repeat of 0.935 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.936 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; win2's states on this build: D 20.8125 passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (75%), none (17%), two or more (8%). The change within 0.01 of 0.936 (coordinator's reading): 45%; within 0.005: 25%.
- Each scan point takes 900 to 1900 s (65%); the point is done (no widening) within 45 min of the lane's start (70%).

## Status
- 2026-11-23 16:59 UTC: folder and README written; the unit waits for the state (expected about 20:35 UTC).
- 2026-11-23 20:01 UTC, before any run of this folder: win2's fold watch fired after D 20.875 and the coordinator ruled a restart of the leap from the D 20.84375 and D 20.875 states at h 0.03125 under a new tag l1kc79Lw1025f (`../../../I1025-win2/kc79_leap/README.md`, ruling quoted there; the restart's dry run passed 19:15 UTC). The state and record of this point therefore come under tag f. Changed: `tag.txt` of this folder (l1kc79Lw1025f), and `fetch_point.sh`, `lane_leg.sh`, `summarize_leg.py` of `..` read the tag from `D<D>/tag.txt` (d when the file is absent). Tested: the patched `fetch_point.sh` pins D 20.875 to the same two blobs as the run (2f6d6b8a, e443a587); a tag file naming a tag with no state exits 1; `summarize_leg.py` output for D 20.84375 and D 20.875 is byte-identical to `summary_leg.txt`. Nothing in the pins, the acceptance, the controls or the predictions of this README changed. The expected time of the state moves to about 20:40 UTC (the restarted leap's first new point, 80 min after about 19:20); if win2's files for tag f sit elsewhere than `states/`, the waiter will not find them and I look by hand.

- 2026-11-23 20:45:51 UTC win2 pushed the state (commit 8eb8aea0, `source_commit.txt`, tag l1kc79Lw1025f); 20:46:28 pins checked and pushed; 20:46:33 selftests as wanted (0 0 1 1 0 0 1); 20:47:05 source check ACCEPTED and scan started (8 processes, nice 10); 21:56:45 the last process ended; 21:56:50 reading written, lane exit 0 (`exits_leg.txt`).

## Result (`summarize_leg.py 20.90625 0.936` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.920 | + | ++ (True) | + | -2334.3204258883525 | 3050 |
| 0.925 | + | ++ (True) | + | -2335.018959345092 | 3104 |
| 0.930 | + | ++ (True) | - | -2335.882908548279 | 3756 |
| 0.935 | + | ++ (True) | - | -2337.2767070667555 | 3502 |
| 0.935 | + | ++ (True) | - | -2337.2767070667555 | 4171 |
| 0.940 | - | -- (True) | - | -2337.8813733323586 | 3935 |
| 0.945 | - | -- (True) | - | -2337.0648193870543 | 3744 |
| 0.950 | - | -- (True) | - | -2336.904864990097 | 3135 |

scan points: 8 evaluations, seconds per point min 3050, median 3623, max 4171, sum 28397; outside 900 to 1900 s: [(0.92, 3050), (0.925, 3104), (0.93, 3756), (0.935, 3502), (0.935, 4171), (0.94, 3935), (0.945, 3744), (0.95, 3135)]
win2's record at D 20.90625: |F| 4.6559593046216824e-10, steps 2687, constraint 0.004414739716036877, Delta 1.1157468265116242, h 0.03125, seconds 5031
float64 sign differs from the hybrid at: [0.93, 0.935, 0.935]

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D20.90625/scan 0.920 0.950
points 7 in 0.920-0.950; not noise-robust: none
hybrid signs: 0.920+ 0.925+ 0.930+ 0.935+ 0.940- 0.945- 0.950-
float64 sign differs from the hybrid sign at: [(0.93, '+', '-'), (0.935, '+', '-')]
repeated points: [(0.935, 'agree')]
  robust change (0.935, 0.940), + to -, det-linear 0.938234, range [0.937636, 0.938234]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.920, - at 0.950
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D20.90625/scan/scan_D20.90625_all.jsonl: lambda [0.935]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.920+ 0.925+ 0.930+ 0.935+ 0.940- 0.945- 0.950-
robust changes: 1
   change (0.935, 0.940), + to -, det-linear 0.938234, range [0.937636, 0.938234]
against the prediction 0.936: change minus prediction +0.002234; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag f state and record at D 20.90625 (record |F| 4.6559593046e-10, the state's 4.6613558364e-10, 2687 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system (|F| 4.6600517326e-10, 2687 steps).
- **One robust change in the window 0.920 to 0.950:** (0.935, 0.940), "+ to -", det-linear **0.938234**, estimator range [0.937636, 0.938234] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.920, - at 0.950). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.935** (p3 and p7) is bit-identical (hybrid +, ln|det| -2337.2767070667555 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.930 and at 0.935 (both evaluations):** float64 -, hybrid +, the hybrid's noise test robust at both. The hybrid sign is the one read. The two points lie 0.008 and 0.003 below the change.
- **Against the coordinator's prediction 0.936 (+-0.01):** +0.002234, within 0.01 (and within 0.005). No widening was needed.
- **Roots on the leg so far (det-linear, as measured):** 0.958120 (D 20.84375), 0.947951 (D 20.875), 0.938234 (D 20.90625): steps -0.010169 and -0.009717 per 0.03125 in D, against the order's -0.0108.
- **Seconds per point were longer again** (3050 to 4171 s here; 2021 to 2474 s at D 20.875, 1531 to 1825 s at D 20.84375). The load average does not explain it: the median over each scan's `scan/sampler.log` was 11.06 (D 20.84375, beside the recount), 19.03 (D 20.875, beside the d19_k95 regrid and the recount) and 16.11 here (beside the d19_k95 scan's 6 processes and the recount). The d19_k95 scan's processes (a larger system, 3575 steps) may compete for memory bandwidth; not tested.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (88%), 8 processes with the record system (90%), the repeat agrees (92%) | right |
| one robust change in the window (75%) | right |
| within 0.01 of 0.936 (45%); within 0.005 (25%) | right (+0.002234) |
| each scan point 900 to 1900 s (65%) | WRONG: all 8 evaluations took 3050 to 4171 s |
| the point done within 45 min of the lane's start, no widening (70%) | WRONG: 70 min (20:47:05 to 21:56:50) |
