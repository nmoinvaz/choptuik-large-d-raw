# I1025-dh610/kc103_d225: win2's k_c 95 state at D 22.5 regridded to k_c 103, then a hybrid sign scan at lambda_1 0.26 to 0.42

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 62 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-25 14:05 UTC (the clock), before any run of this folder (the pins of the inputs and a syntax check of the lane came first; no regrid, no scan). The k_c 103 roots are not yet physical. A root is identified by position; its orientation is printed as the reader prints it and is not interpreted here.

## Order (coordinator t5, hc, read at about 14:05 UTC 25 Nov), verbatim
"Coordinator (t5), #1025, next lane: k_c 103 at D 22.5 from win2's accepted k_c 95 state (raw I1025-win2/kc95_d225, state blob 4bdcc567, record 3cdbdec1; kc95 check accepts, controls 1 1, kc87 and kc103 refuse), your k_c 103 recipe at nice 19 under i1088a, then a scan lambda 0.26 to 0.42 by 0.02 plus the repeat of 0.34, 4 procs. Register first: k_c 95's root 0.339 (bracket 0.30-0.34); a converged lambda_1 predicts 0.32 +- 0.04 at this grid. Raw kc103_d225/, README first."

The order gives the prediction 0.32 with bar 0.04 (**PRED 0.32**, bar 0.04, the reader's "against the prediction" line). Reading at this D: win2's k_c 95 root **0.339034**, bracket (0.300, 0.340), estimator range [0.300860, 0.339034], printed "- to +" (`I1025-win2/kc95_d225/read_lower.txt`; scan -0.10 to 0.50 by 0.04, 17 evaluations; one robust change; the float64 sign equal to the hybrid everywhere). Other k_c 95 roots, all printed "- to +": 0.545920 (D 22.0, win2), 0.434264 (D 22.25, mine), 0.379911 (D 22.375, mine, bracket (0.34, 0.38), `../kc95_d22375/`). The k_c 95 to 103 steps seen so far, as the coordinator gave them: -0.000062 (D 21.0, winb), +0.0034 (D 21.125), +0.0068 (D 21.75); my own k_c 103 scan at D 22.125 (`../kc103_d22125/`) is running and not read; dh370's k_c 103 at D 22.25 (`../../I1025-dh370/kc103_d2225/`) is not read either.

## Inputs (copies in `in/`; `in_blobs.txt` lists the scripts' blobs, `in_blobs_src.txt` the source's; the lane refuses any other blob)
| item | source | blob |
|---|---|---|
| win2's k_c 95 state at D 22.5 (regrid accepted by win2, 6599 s, 4 threads Windows; commit 8a958a291, 2026-11-24 23:41:10 -08:00 = 2026-11-25 07:41:10 UTC; |F| 3.813000485e-10, 3126 steps, constraint 5.592e-03, Delta 1.159795856212) | I1025-win2/kc95_d225/sol_l1kc95win2d225_D22.5000.npy | 4bdcc567 |
| its record (one row, tag l1kc95win2d225, kc 95, src l1kc87Lmacm3b2) | same folder, l1kc95win2d225.jsonl | 3cdbdec1 |
| the k_c 87, k_c 95 and k_c 103 checks (`kc103_syscheck_1025.diff`: 3 changed lines against the k_c 95 check), the scanner, reader, repeat check, `leg_read.py`, `d185_scan_read.py`, `d18c_read.py` | as `../kc103_d22125/in/` | 6df5d960; d487e628; 3ab58d16; e089207a, 89309d3c, aaf598a9, 5cae2639, 7c9d400f, 1383470f |
Code and environment as `../kc103_d22125/` (worktrees `~/Source/choptuik-large-d-1025g` 48c36355 and `-1025f` 505d8399; `~/Source/venv-i1058`). The regrid reads only the source state, which the lane copies into the worktree's `solver/matter/data/` after the pin. lambda_0(22.5) from `ell_delta.lam0_at` reads **2.1009889535** (the regrid's 7th argument; the lane stops if it reads otherwise). The source was built on Windows: the k_c 95 check recomputes its |F| here against the record's, within its 1% bar.

## Commands (`lane_kc103.sh` in this folder, derived from `../kc103_d22125/lane_kc103.sh`; unit `i1025-kc103-22_5` via `start_kc103.sh`; `watch_i1088a.sh` and `notify_kc103.sh` run beside it)
1. Pins and selftests (wanted `0 0 0 0 1 1 0 0 1`), the source check: `kc95_syscheck_1025.py` exit 0 on the source, `--mutate=F` and `--mutate=steps` exit 1, the k_c 87 check and the k_c 103 check exit 1 on it.
2. Regrid in `solver/matter`, 8 threads, nice 10, `timeout 43200` (the winb cap; the D 22.125 regrid took 12628 s): `ell_refine.py l1kc95win2d225 95 l1kc103dh610d225 103 1 22.5 2.1009889535 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`. Accepted only when `kc103_syscheck_1025.py` exits 0 on the result, both controls exit 1, and the k_c 95 and k_c 87 checks both refuse it.
3. Scan (after ACCEPTED and a memory gate that waits, never stops): `d18_hybsign.py` at lambda 0.26, 0.28, 0.30, 0.32, 0.34, 0.36, 0.38, 0.40, 0.42 and a repeat of 0.34: 10 evaluations on 4 processes of 1 thread at nice 10 (p0 0.34, 0.36, 0.40; p1 0.32, 0.28, 0.42; p2 0.30, 0.38; p3 the repeat of 0.34, 0.26), raised to nice 19 by `watch_i1088a.sh` by exact pid while an i1088a unit is active; nothing is stopped.
4. Reading: `read_lower.py scan 0.26 0.42`, `repeat_check.py`, `leg_read.py read` against 0.32 (bar 0.04). No robust change in the window: reported as read, no widening.

## Acceptance (fixed before the run)
The source accepted with controls 1 1 and refused by the k_c 87 and k_c 103 checks; the regrid exits 0 inside 43200 s; the result accepted by `kc103_syscheck_1025.py` with both controls exit 1 and refused by the k_c 95 and k_c 87 checks; every scan process prints the record system and exits 0; the repeat agrees. A control that fires stops the work and I report it; no bar is loosened. Reported: steps, |F|, constraint, Delta of the k_c 103 state beside win2's k_c 95 record; every robust change by position (bracket, orientation **as printed**, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside win2's k_c 95 root 0.339034; the k_c step (k_c 103 minus k_c 95 root, bracket-limited by the 0.04 grid of the k_c 95 reading); seconds per point, load, RSS, MemAvailable; what the watcher did.

## Predictions, registered before the runs (mine, information)
Basis: the coordinator's 0.32 +- 0.04 for a converged lambda_1; win2's k_c 95 root 0.339034 with a bracket (0.300, 0.340) of its own 0.04 grid (its estimator range is [0.300860, 0.339034], so the true k_c 95 position inside the bracket is open); the k_c 95 to 103 steps +0.0034 (D 21.125) and +0.0068 (D 21.75), -0.00006 (D 21.0). PRED stays the coordinator's 0.32; "met" means the det-linear root of the robust change nearest 0.32 lies in [0.28, 0.36].
- Source accepted with controls 1 1 and refused by the k_c 87 and k_c 103 checks: 90% (a Windows-built state checked here). Regrid exits 0 and is accepted: 85%.
- Steps about 3390 (win2's 3126 times the k_c 95 to 103 ratio 1.0846 of D 22.125): within 10: 40%; within 30: 80%. |F| below 1e-9: 95%.
- Delta(103) - Delta(95) negative (85%); smaller in magnitude than the k_c 87 to 95 shift at this D, -2.931e-05 (70%).
- Regrid wall 10000 to 20000 s (65%; 12628 s for the k_c 103 regrid at D 22.125 on 8 threads at nice 19 beside the quest's units and four scan processes of mine); peak sampled RSS below 3.5 GiB (80%).
- Scan: every point noise-robust (70%); the repeat on another process than its original bit-identical (85%); exactly one robust change in the window (70%), none (15%), two or more (15%). PRED met, i.e. the det-linear root in [0.28, 0.36] (60%); inside win2's k_c 95 bracket (0.30, 0.34) (40%); above 0.34 (30%); below 0.28 (10%). The bracket (0.32, 0.34) (20%), (0.30, 0.32) (20%), (0.34, 0.36) (15%), (0.28, 0.30) (12%). The printed orientation of the k_c 103 root is "- to +" (85%; every k_c 95 reading from D 22.0 to 22.5 prints it). The float64 sign agrees with the hybrid at all 10 evaluations (35%; it did at all 17 of win2's k_c 95 scan here and of mine at D 22.375, not at D 22.1875). Each scan point 3500 to 6500 s (60%); the scan done within 5 h of its start (60%).
- Timeline: the regrid done within 4.5 h of the lane's start (60%); the whole lane (regrid and scan) done within 9 h (55%).

## Regrid result (25 Nov, 14:06:16 to 17:04:05 UTC): ACCEPTED
`ell_refine.py` (8 threads, nice 10, raised to nice 19 at 14:06:28 UTC by the watcher while an `i1088a-*` unit was active) exited 0 after **10669 s** (the record's own 10666 s; predicted 10000 to 20000 s: right, 669 s inside the lower edge). Mean sampled CPU 713% (177 samples, `regrid/regrid_samples.csv`), about 76k CPU-seconds, against 83.5k for my k_c 103 regrid at D 22.125 (12628 s, 661%). Peak sampled RSS 2.98 GiB; 25 numpy RuntimeWarning lines in the log, as in the earlier regrids; no memory alert. It ran beside my k_c 103 D 22.125 scan (4 processes), the recount and the quest's units.
- Record `l1kc103dh610d225.jsonl` and state `sol_l1kc103dh610d225_D22.5000.npy` (both copied to `in/`): k_c 103 at D 22.5, |F| 3.8281691823e-10, F_start 2.396e-05, **3390 steps** (win2's k_c 95 state: 3126; ratio 1.0845, predicted about 3390), constraint 3.536e-03 (k_c 95: 5.592e-03, ratio 0.632), **Delta 1.159787618615** (win2's k_c 95: 1.159795856212; shift k_c 103 minus k_c 95 **-8.2376e-06**; the k_c 87 to 95 shift at this D was -2.931e-05).
- **Acceptance:** `kc103_syscheck_1025.py` exit 0 (the state's |F| equals the record's, `freeze_from` gives 3390 steps = the record's); `--mutate=F` exit 1, `--mutate=steps` exit 1; `kc95_syscheck_1025.py` and `kc87_syscheck_1025.py` on the k_c 103 result both exit 1 (refuse). The source check and the selftests are in `exits_kc103.txt` and `regrid/source_*.txt`.
- **Scan:** started 17:04:26 UTC on 4 processes (10 evaluations; p0 0.34, 0.36, 0.40; p1 0.32, 0.28, 0.42; p2 0.30, 0.38; p3 the repeat of 0.34, 0.26); the memory gate passed with no wait (MemAvailable 55.9 GB, load 16.3); the watcher reniced the processes to nice 19 while an `i1088a-*` unit is active.

### Regrid predictions scorecard (registered before the run)
| prediction | result |
|---|---|
| source accepted with controls 1 1, refused by the k_c 87 and k_c 103 checks (90%) | right |
| regrid exits 0 and is accepted (85%) | right |
| steps about 3390 (within 10: 40%; within 30: 80%) | right (3390, exact) |
| \|F\| below 1e-9 (95%) | right (3.83e-10) |
| Delta(103) - Delta(95) negative (85%); smaller in magnitude than 2.931e-05 (70%) | right (-8.24e-06); right |
| regrid wall 10000 to 20000 s (65%) | right (10669 s) |
| peak sampled RSS below 3.5 GiB (80%) | right (2.98 GiB) |
| the regrid done within 4.5 h of the lane's start (60%) | right (2.97 h: 14:05:59 to 17:04:21 UTC) |

## Scan result (25 Nov, 17:04:26 to 20:18:48 UTC, 194.4 min, 4 processes; `summarize_kc103.py` > `summary_kc103.txt`)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.260 | + | ++ (True) | + | -3032.33284849965 | 2638 |
| 0.280 | + | ++ (True) | + | -3034.782497259668 | 2649 |
| 0.300 | + | ++ (True) | + | -3037.9754392479367 | 3856 |
| 0.320 | - | -- (True) | - | -3039.3971209626507 | 3991 |
| 0.340 | - | -- (True) | - | -3040.342183713146 | 3954 |
| 0.340 | - | -- (True) | - | -3040.342183713146 | 4070 |
| 0.360 | - | -- (True) | - | -3041.768464173321 | 2646 |
| 0.380 | - | -- (True) | - | -3043.3529469840873 | 2666 |
| 0.400 | - | -- (True) | - | -3045.0174571780476 | 4217 |
| 0.420 | - | -- (True) | - | -3046.730566299375 | 5013 |

scan points: 10 evaluations, seconds per point min 2638, median 3905, max 5013, sum 35700; outside 3500 to 6500 s: [(0.26, 2638), (0.28, 2649), (0.36, 2646), (0.38, 2666)]
the regridded record at D 22.5: |F| 3.828169182320854e-10, steps 3390, constraint 0.003535552513596091, Delta 1.15978761861507, h None, seconds 10666
float64 sign differs from the hybrid at: []

```
hybrid signs: 0.260+ 0.280+ 0.300+ 0.320- 0.340- 0.360- 0.380- 0.400- 0.420-
robust changes: 1
   change (0.300, 0.320), + to -, det-linear 0.316112, range [0.301766, 0.316112]
against the prediction 0.32: change minus prediction -0.003888; within 0.04: True
```

- **All 4 processes exit 0 and printed the record system** (|F| 3.8281691823e-10 against the record's, steps 3390 = the record's); the pre-run checks passed (`selftest_exits.txt` 0 0 0 0 1 1 0 0 1). The scan ran on 4 processes (p0 0.34, 0.36, 0.40; p1 0.32, 0.28, 0.42; p2 0.30, 0.38; p3 the repeat of 0.34 and 0.26); process walls 1:48:47 (p2), 1:51:53 (p3), 3:00:22 (p0), 3:14:22 (p1).
- **One robust change in the window 0.26 to 0.42:** (0.300, 0.320), **"+ to -" as the reader prints it**, det-linear **0.316112**, estimator range [0.301766, 0.316112] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.02). Edge signs differ (+ at 0.26, - at 0.42). No ln|det| minimum without a sign change; every point noise-robust (10 of 10); the float64 sign equals the hybrid at all 10.
- **The repeat of 0.34** (p0 and p3, two processes) is bit-identical (hybrid -, ln|det| -3040.342183713146 in both; `repeat_check.py` PASS).
- **Beside win2's k_c 95 reading at this D** (`I1025-win2/kc95_d225/read_lower.txt`, scan -0.10 to 0.50 by 0.04, 16 points, one robust change, float64 sign equal to the hybrid everywhere), as printed:

| | grid | bracket | printed orientation | det-linear root | estimator range |
|---|---|---|---|---|---|
| win2 k_c 95 | 0.04 | (0.300, 0.340) | - to + | 0.339034 | [0.300860, 0.339034] |
| dh610 k_c 103 | 0.02 | (0.300, 0.320) | + to - | 0.316112 | [0.301766, 0.316112] |

  The k_c step (k_c 103 minus k_c 95 root) is **-0.022922** between the det-linear roots. The k_c 103 bracket (0.300, 0.320) lies inside win2's (0.300, 0.340) and the two estimator ranges overlap on [0.301766, 0.316112], so the grids leave the step between -0.04 and +0.02 (bracket-limited; its sign is not fixed by the signs at the shared grid points, as it was at D 22.125). The k_c 95 root is above 0.30 and below 0.34; the k_c 103 root is above 0.30 and below 0.32. **The printed orientations differ at this D** ("- to +" for k_c 95, "+ to -" for k_c 103), and so do the hybrid signs at all five grid points the two scans share: 0.26, 0.30, 0.34, 0.38, 0.42 read - - + + + for win2's k_c 95 and + + - - - for this k_c 103. I list this as printed and do not interpret it. The printed orientations at D 22.125 (all three "- to +") and the k_c steps at D 22.125 (-0.001176) are in `../kc103_d22125/`.
- **Seconds per point: 2638 to 5013 s** (median 3905), 4 processes of 1 thread at nice 19 (the watcher's renice at 17:04:49 UTC of the 4 pids, `i1088a_yield.txt`; from 17:44 UTC the per-thread watcher, the processes being 1-thread), beside my k_c 103 D 22.125 scan until 17:17 UTC, the recount until 17:55 UTC, then the #1076 one-box recounts, and the quest's units: 1-minute load median 13.52, max 20.52, min 4.35 over 387 samples 17:04:36 to 20:18:20 UTC (none above 22; `load_alert.out` empty, no alert); peak RSS per process 3.55 to 3.67 GiB (`/usr/bin/time -v`); MemAvailable at least 47.2 GiB; no memory alert.

### Scan predictions scorecard (registered before the run)
| prediction | result |
|---|---|
| every point noise-robust (70%) | right (10 of 10) |
| the repeat on another process bit-identical (85%) | right |
| exactly one robust change in the window (70%) | right |
| PRED met, the det-linear root in [0.28, 0.36] (60%) | right (0.316112, -0.003888 from 0.32) |
| inside win2's k_c 95 bracket (0.30, 0.34) (40%) | right |
| above 0.34 (30%); below 0.28 (10%) | WRONG; WRONG |
| the bracket (0.32, 0.34) (20%); (0.30, 0.32) (20%); (0.34, 0.36) (15%); (0.28, 0.30) (12%) | WRONG; right; WRONG; WRONG |
| the printed orientation of the k_c 103 root is "- to +" (85%) | WRONG (printed "+ to -") |
| the float64 sign agrees with the hybrid at all 10 evaluations (35%) | right |
| each scan point 3500 to 6500 s (60%) | WRONG (2638 to 5013 s; 4 of 10 below 3500 s) |
| the scan done within 5 h of its start (60%) | right (3.24 h) |
| the whole lane (regrid and scan) done within 9 h (55%) | right (6.21 h: 14:05:59 to 20:18:52 UTC) |

## Status
- 2026-11-25 14:05 UTC: folder, inputs (pinned: `in_blobs.txt`, `in_blobs_src.txt`, `source_commit.txt`), lane, watcher and README written before any run; `lane_kc103.sh dry` and the unit `i1025-kc103-22_5` are started next. Beside it: my k_c 103 D 22.125 scan (4 processes), the recount `i1076d` (1), the quest's `i1088a-*` units (not mine).
- 2026-11-25 17:05 UTC: regrid ACCEPTED (10669 s, 3390 steps, |F| 3.83e-10, Delta shift -8.24e-06 vs win2's k_c 95); the scan runs on 4 processes since 17:04:26 UTC. Scan result and scorecard are written when the last point is done.
- 2026-11-25 17:46 UTC, amendment (the coordinator's hc, dh370's finding: on Linux nice is per thread, `renice -p PID` moves only the main thread): this lane's `watch_i1088a.sh` raised nice on the main thread only. The regrid (8 threads, 14:06 to 17:04 UTC) therefore ran with its main thread at 19 and, by dh370's 4-thread test (19 10 10 10, reproduced here on a dummy), its worker threads at 10; I did not list its threads while it ran (the process is gone), so that is inferred from the mechanism, not observed. The scan's 4 processes are 1 thread each (`ps -L`: NLWP 1), so their nice 19 was right. Fix: `renice_threads.sh [--mutate] PID` (renices every tid below 19 by exact tid, prints the nice values before and after, exits 1 if a thread is left below 19; tested on 4-thread dummies at nice 10: plain `renice -p` gave 19 10 10 10, `--mutate` exit 1 with [19 10 10 10], the fix exit 0 with [19 19 19 19], the 1-thread scan pid exit 0) and `watch_i1088a.sh` now calls it for every matching pid whenever a thread is below 19 (the old script is kept as `watch_i1088a.sh.old_main_thread_only`; the new one started 17:44 UTC, the old one, pid 2018674, stopped by exact pid). Before and after for the running lane (17:44 UTC): scan pids 2056520 to 2056523, 1 thread each, nice 19 before and after. The recount (12 processes of 1 thread, nice 10 as ordered, not under the yield watcher) is unchanged.
- 2026-11-25 20:20 UTC: scan done (17:04:26 to 20:18:48 UTC). One robust change (0.300, 0.320), "+ to -" as printed, det-linear 0.316112; win2's k_c 95 reads "- to +" at 0.339034 (bracket (0.300, 0.340)); k_c 103 minus k_c 95 root -0.022922, bracket-limited. Scan result and both scorecards above.
