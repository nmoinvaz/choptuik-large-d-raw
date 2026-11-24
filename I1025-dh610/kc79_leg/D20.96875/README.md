# I1025-dh610/kc79_leg/D20.96875: lambda_1 on win2's k_c 79 leg point D 20.96875 (tag l1kc79Lw1025f), window 0.905 to 0.935 around the prediction 0.9176

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Parent folder `../README.md` (order, method, pins, pilots). Written 2026-11-23 23:15 UTC, before the state of this point is on origin and before any run of this folder. The k_c 79 roots are not yet physical.

## Order for this point (coordinator t5, #1025 comment of "17:45", and the hc ruling for points past D 20.90625)
lambda_1 on win2's k_c 79 leg at D 20.96875: **predicted 0.9176 +-0.01** (the previous measured root 0.928441 minus 0.0108); a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point; no change in the window: widen once by 0.015 and report.

## This point
- State `sol_l1kc79Lw1025f_D20.968750.npy` and record `l1kc79Lw1025f.jsonl` of `I1025-win2/kc79_leap/states/`: pinned by blob when the state is on origin (`in_blobs.txt`, `source_commit.txt`, pushed before the scan). `tag.txt` names the tag.
- Grid centre 0.920 (the multiple of 0.005 nearest 0.9176; 0.915 lies 0.0026 away, 0.920 0.0024); the scan: 0.905, 0.910, 0.915, 0.920, 0.925, 0.930, 0.935 and a repeat of 0.920. The widening, if there is no robust change: low 0.900, 0.895, 0.890; high 0.940, 0.945, 0.950 (the side by `leg_read.py widen`).
- Commands: `bash wait_and_run.sh 20.96875 0.920 0.9176` as the systemd user unit `i1025-leg-20_96875` (waits for the state, pins, pushes the pins, takes the lock, runs `lane_leg.sh`).

## Acceptance (fixed before the run)
- `kc79_syscheck_1025.py` accepts the state at D 20.96875 with both controls exit 1; all 8 processes print the record system; the repeat of 0.920 agrees (`repeat_check.py`); `read_lower.py`, `leg_read.py` and `repeat_check.py` selftests as wanted. A failing control or check stops the lane and I report it.
- Reported: every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the prediction 0.9176 (bar 0.01); the edge signs; the repeat; the seconds per point; the widening if it ran.

## Predictions, registered before the run (mine, information)
- The source is accepted (88%; the four earlier points on tag d and f passed), all 8 processes print the record system (90%), the repeat agrees (92%).
- One robust change in the window (80%), none (13%), two or more (7%). The change within 0.01 of 0.9176: 75%; within 0.005: 50%. The measured steps so far are -0.010169, -0.009717 and -0.009793 against the prediction's -0.0108 and the residuals +0.000120, +0.000951, +0.002234, +0.001041: I expect the root between 0.9180 and 0.9235 (60%).
- Each scan point takes 2500 to 4300 s (60%) while the d19_k95 scan (its last point) and the recount run, shorter when the recount runs alone (the earlier points: 1531 to 1825, 2021 to 2474, 3050 to 4171, 3148 to 3965 s); the point is done (no widening) within 75 min of the lane's start (60%).
- The state is on origin by 23:45 UTC (70%; win2's cadence 81.5 min, the last state 22:07:22 UTC).

## Status
- 2026-11-23 23:15 UTC: folder and README written; the unit `i1025-leg-20_96875` waits for the state (expected about 23:30 UTC).

- 2026-11-23 23:28:40 UTC win2's commit 1954135e added the state (its commit time, 15:28:40-08:00; `source_commit.txt`, tag l1kc79Lw1025f); 23:28:58 pinned; 23:29:02 lock taken, lane started; 23:29:03 selftests as wanted (0 0 1 1 0 0 1); 23:29:31 source check ACCEPTED and scan started (8 processes, nice 10); 00:26:41 the last process ended; 00:26:42 reading written; 00:26:46 lane exit 0 (`exits_leg.txt`).

## Result (`summarize_leg.py 20.96875 0.9176` > `summary_leg.txt` prints the table from the files)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.905 | + | ++ (True) | + | -2327.4983859340095 | 3144 |
| 0.910 | + | ++ (True) | + | -2328.3302804100163 | 2928 |
| 0.915 | + | ++ (True) | + | -2329.570984202691 | 2800 |
| 0.920 | - | -- (True) | + | -2330.9205303933077 | 3141 |
| 0.920 | - | -- (True) | + | -2330.9205303933077 | 3370 |
| 0.925 | - | -- (True) | - | -2329.757954241734 | 2926 |
| 0.930 | - | -- (True) | - | -2329.5528730566407 | 3414 |
| 0.935 | - | -- (True) | - | -2329.5625598028323 | 3423 |

scan points: 8 evaluations, seconds per point min 2800, median 3142, max 3423, sum 25146; outside 900 to 1900 s: [(0.905, 3144), (0.91, 2928), (0.915, 2800), (0.92, 3141), (0.92, 3370), (0.925, 2926), (0.93, 3414), (0.935, 3423)]
win2's record at D 20.96875: |F| 4.647310528405076e-10, steps 2681, constraint 0.004616671557448626, Delta 1.1174107429384874, h 0.03125, seconds 4715
float64 sign differs from the hybrid at: [0.92, 0.92]

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D20.96875/scan 0.905 0.935
points 7 in 0.905-0.935; not noise-robust: none
hybrid signs: 0.905+ 0.910+ 0.915+ 0.920- 0.925- 0.930- 0.935-
float64 sign differs from the hybrid sign at: [(0.92, '-', '+')]
repeated points: [(0.92, 'agree')]
  robust change (0.915, 0.920), + to -, det-linear 0.918970, range [0.918464, 0.918970]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.905, - at 0.935
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc79_leg/D20.96875/scan/scan_D20.96875_all.jsonl: lambda [0.92]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

```
hybrid signs: 0.905+ 0.910+ 0.915+ 0.920- 0.925- 0.930- 0.935-
robust changes: 1
   change (0.915, 0.920), + to -, det-linear 0.918970, range [0.918464, 0.918970]
against the prediction 0.9176: change minus prediction +0.001370; within 0.01: True
```

- **Source accepted:** `kc79_syscheck_1025.py` exit 0 on win2's tag f state and record at D 20.96875 (record |F| 4.6473105284e-10, the state's 4.6458803875e-10, 2681 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (`src/syscheck*.txt`). All 8 processes printed the record system (|F| 4.6469981664e-10, 2681 steps).
- **One robust change in the window 0.905 to 0.935:** (0.915, 0.920), "+ to -", det-linear **0.918970**, estimator range [0.918464, 0.918970] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (+ at 0.905, - at 0.935). No ln|det| minimum without a sign change; every point noise-robust. The orientation is as the reader prints it.
- **The repeat of 0.920** (p3 and p7) is bit-identical (hybrid -, ln|det| -2330.9205303933077 in both; `repeat_check.py` PASS).
- **The float64 sign differs from the hybrid at 0.920, in both evaluations** (float64 +, hybrid -, noise test robust). The hybrid sign is the one read. That point is the upper edge of the bracket, 0.001 above the change; read by float64 the change would lie in (0.920, 0.925).
- **Against the prediction 0.9176 (+-0.01, the previous root 0.928441 minus 0.0108):** +0.001370, within 0.01 (and within 0.005). No widening was needed.
- **Roots on the leg so far (det-linear, as measured):** 0.958120 (D 20.84375), 0.947951 (D 20.875), 0.938234 (D 20.90625), 0.928441 (D 20.9375), 0.918970 (D 20.96875): steps -0.010169, -0.009717, -0.009793 and -0.009471 per 0.03125 in D, against the order's -0.0108.
- **Seconds per point:** 2800 to 3423 s (D 20.9375: 3148 to 3965 s). The load average, median over `scan/sampler.log`, was 15.05 (8 processes here, the d19_k95 gap scan's 5 and the recount's 2; D 20.9375: 16.24). Peak RSS per process (`/usr/bin/time -v`) 1.63 to 1.82 GiB; MemAvailable at least 40.09 GiB. Why the seconds fell a little is not tested.

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| source accepted (88%), 8 processes with the record system (90%), the repeat agrees (92%) | right |
| one robust change in the window (80%) | right |
| within 0.01 of 0.9176 (75%); within 0.005 (50%) | right (+0.001370) |
| the root between 0.9180 and 0.9235 (60%) | right (0.918970) |
| each scan point 2500 to 4300 s (60%) | right (2800 to 3423 s) |
| the point done, no widening, within 75 min of the lane's start (60%) | right (58 min: 23:29:02 to 00:26:46) |
| the state on origin by 23:45 UTC (70%) | right (23:28:40 UTC, the commit time of 1954135e) |

All seven registered predictions came true.
