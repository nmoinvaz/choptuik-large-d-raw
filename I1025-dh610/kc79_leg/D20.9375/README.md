# I1025-dh610/kc79_leg/D20.9375: lambda_1 on win2's k_c 79 leg point D 20.9375 (tag l1kc79Lw1025f), window 0.910 to 0.940 around the prediction 0.9274

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-23 21:59 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", and the hc ruling for points past D 20.90625)
lambda_1 on win2's k_c 79 leg at D 20.9375: **predicted 0.9274 +-0.01** (the previous measured root 0.938234 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D20.937500.npy` and record `l1kc79Lw1025f.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). `tag.txt` names the tag.
- Grid centre 0.925 (the multiple of 0.005 nearest 0.9274); the scan: 0.910, 0.915, 0.920, 0.925, 0.930, 0.935, 0.940 and a repeat of 0.925. The widening, if there is no robust change: low 0.905, 0.900, 0.895; high 0.945, 0.950, 0.955 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 20.9375 0.925 0.9274` as the systemd user unit `i1025-leg-20_9375` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 20.9375 with both controls exit 1; all 8 processes print the record system; the repeat of 0.925 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.9274 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; the three earlier points passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (78%), none (14%), two or more (8%). The change within 0.01 of 0.9274 (the coordinator's reading): 70%; within 0.005: 45%. The measured steps so far are -0.010169 and -0.009717, against the prediction's -0.0108, and the residuals +0.000120, +0.000951, +0.002234 grow: I expect the root between 0.9275 and 0.9320 (60%).
- Each scan point takes 2500 to 4300 s (60%) while the d19_k95 scan runs and the recount (its round 2 ends about 22:35 to 23:20 UTC), shorter after (the earlier points: 1531 to 1825, 2021 to 2474, 3050 to 4171 s); the point is done (no widening) within 75 min of the lane's start (60%).
- The state is on origin by 22:30 UTC (70%; win2's cadence 84 min, the last state 20:45:51 UTC).

## Status
- 2026-11-23 21:59 UTC: folder and README written; the unit `i1025-leg-20_9375` waits for the state (expected about 22:10 UTC).

- 2026-11-23 22:07:22 UTC win2 pushed the state (commit e145364c, `source_commit.txt`, tag l1kc79Lw1025f); 22:07:40 pins checked and pushed; 22:07:45 selftests as wanted (0 0 1 1 0 0 1); 22:08:16 source check ACCEPTED and scan started (8 processes, nice 10); 23:14:28 the last process ended; 23:14:32 reading written, lane exit 0 (`exits_leg.txt`).

## Result (`summarize_leg.py 20.9375 0.9274` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.910 | + | ++ (True) | + | -2330.7619281685497 | 3965 |
| 0.915 | + | ++ (True) | + | -2331.4588831648193 | 3950 |
| 0.920 | + | ++ (True) | + | -2332.3152160747873 | 3935 |
| 0.925 | + | ++ (True) | - | -2333.663817036468 | 3148 |
| 0.925 | + | ++ (True) | - | -2333.663817036468 | 3791 |
| 0.930 | - | -- (True) | - | -2334.4555586897363 | 3925 |
| 0.935 | - | -- (True) | - | -2333.567381660108 | 3865 |
| 0.940 | - | -- (True) | - | -2333.3980357452033 | 3819 |

scan points: 8 evaluations, seconds per point min 3148, median 3895, max 3965, sum 30398; outside 900 to 1900 s: [(0.91, 3965), (0.915, 3950), (0.92, 3935), (0.925, 3148), (0.925, 3791), (0.93, 3925), (0.935, 3865), (0.94, 3819)]
win2's record at D 20.9375: |F| 4.6526639601251245e-10, steps 2683, constraint 0.004514982917733106, Delta 1.1165778406212568, h 0.03125, seconds 4824
float64 sign differs from the hybrid at: [0.925, 0.925]

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D20.9375/scan 0.910 0.940
points 7 in 0.910-0.940; not noise-robust: none
hybrid signs: 0.910+ 0.915+ 0.920+ 0.925+ 0.930- 0.935- 0.940-
float64 sign differs from the hybrid sign at: [(0.925, '+', '-')]
repeated points: [(0.925, 'agree')]
  robust change (0.925, 0.930), + to -, det-linear 0.928441, range [0.927851, 0.928441]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.910, - at 0.940
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D20.9375/scan/scan_D20.9375_all.jsonl: lambda [0.925]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.910+ 0.915+ 0.920+ 0.925+ 0.930- 0.935- 0.940-
robust changes: 1
   change (0.925, 0.930), + to -, det-linear 0.928441, range [0.927851, 0.928441]
against the prediction 0.9274: change minus prediction +0.001041; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag f state and record at D 20.9375 (record |F| 4.6526639601e-10, the state's 4.6517239980e-10, 2683 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system (|F| 4.6527154465e-10, 2683 steps).
- **One robust change in the window 0.910 to 0.940:** (0.925, 0.930), "+ to -", det-linear **0.928441**, estimator range [0.927851, 0.928441] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.910, - at 0.940). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.925** (p3 and p7) is bit-identical (hybrid +, ln|det| -2333.663817036468 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.925, in both evaluations** (float64 -, hybrid +, noise test robust). The hybrid sign is the one read. That point lies 0.003 below the change.
- **Against the prediction 0.9274 (+-0.01, the previous root 0.938234 minus 0.0108):** +0.001041, within 0.01 (and within 0.005). No widening was needed.
- **Roots on the leg so far (det-linear, as measured):** 0.958120 (D 20.84375), 0.947951 (D 20.875), 0.938234 (D 20.90625), 0.928441 (D 20.9375): steps -0.010169, -0.009717 and -0.009793 per 0.03125 in D, against the order's -0.0108.
- **Seconds per point:** 3148 to 3965 s (D 20.90625: 3050 to 4171). The load average, median over `scan/sampler.log`, was 16.24 (8 processes here, the d19_k95 scan's 6 and the recount's 2).

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (88%), 8 processes with the record system (90%), the repeat agrees (92%) | right |
| one robust change in the window (78%) | right |
| within 0.01 of 0.9274 (70%); within 0.005 (45%) | right (+0.001041) |
| the root between 0.9275 and 0.9320 (60%) | right (0.928441) |
| each scan point 2500 to 4300 s (60%) | right (3148 to 3965 s) |
| the point done, no widening, within 75 min of the lane's start (60%) | right (66 min: 22:08:16 to 23:14:32) |
| the state on origin by 22:30 UTC (70%) | right (22:07:22) |
