# I1025-dh610/kc95_d22375: macm3's k_c 87 b2 leg state at D 22.375 regridded to k_c 95, then a WIDE hybrid sign scan at lambda_1 -0.10 to 0.50

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 62 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-25 06:16 UTC, before any run of this folder (the pin of the source state and the planted reading checks came first; no regrid, no scan). The k_c 95 roots are not yet physical. A root is identified by position; its orientation is printed as the reader prints it and is reported, not interpreted.

## Order (coordinator t5, hc, read at about 06:14 UTC 25 Nov), verbatim
"Coordinator (t5), #1025, second lane now (dh610 has ~9 threads idle): k_c 95 at D 22.375 from macm3's part b2 k_c 87 state (raw I1025-macm3 part b2, pin by blob; kc87 check accepts, controls 1 1, kc95 check refuses), the same regrid recipe as your D 22.1875 lane (nice 19 while i1088a runs, renice watcher keyed to this tag), then a WIDE scan: lambda -0.10 to 0.50 by 0.04 plus the repeat of 0.14, 4 processes. Report every robust change by position and printed orientation. Reason: k_c 87 has an extra root near 0.11 at D 22.25 that k_c 95 lacks there (win2, 0.08-0.18 all '-'); if it is the same feature shifted in D by resolution, it shows at k_c 95 at a larger D. Raw kc95_d22375/, README first with the predictions: one extra root below lambda_1 (orientation of lambda_1 '+ to -') if the feature has shifted in, else lambda_1 alone '- to +' near 0.40."

## Inputs (copies in `in/`; `in_blobs.txt` lists their blobs, `in_blobs_src.txt` the source's; the lane refuses any other blob and now also stops when `in_blobs_src.txt` is missing)
| item | source | blob |
|---|---|---|
| macm3's k_c 87 D 22.375 state (commit 79ae81f4, 2026-11-24 18:30:33 -08:00 = 2026-11-25 02:30:33 UTC) | I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.375000.npy | d7bfdaa2 |
| its record file (rows up to D 22.375: \|F\| 3.8444606037739405e-10, 2864 steps, psi-constraint 0.007785842472893882, Delta 1.1562474233720497, h 0.03125, 1756 s) | same folder, l1kc87Lmacm3b2.jsonl at that commit | 73589d63 |
| the k_c 87 check; the k_c 95 check (3 changed lines, `kc95_syscheck_1025.diff`); the scanner, reader, repeat check, `leg_read.py` (only its selftest is run here) | as `../kc95_d2225/in/` | 6df5d960; d487e628; e089207a, 89309d3c, aaf598a9, 5cae2639 |
Code and environment as `../kc95_d2225/`. lambda_0(22.375) from `ell_delta.lam0_at` reads **2.1014424345** (the regrid's 7th argument; the lane stops if it reads otherwise). macm3 has no reading of this D yet; its k_c 87 reading at D 22.25 is bracket (0.440, 0.445), 0.442516, "+ to -" as printed; this lane's k_c 95 at D 22.25 (`../kc95_d2225/`) is (0.430, 0.435), 0.434264, "- to +" as printed.

## Commands (`lane_kc95.sh`, a copy of `../kc95_d221875/lane_kc95.sh` rewritten for this D; unit `i1025-kc95-22_375` via `start_kc95.sh`)
1. Pins and selftests (wanted `0 0 0 1 1 0 0 1 0 1 0 1`: the eight of the earlier lanes, then `wide_read.py` selftest 0 and its `--mutate` 1, and `planted_wide.py` 0 and its `--mutate` 1), the source check (`kc87_syscheck_1025.py` exit 0, `--mutate=F` and `--mutate=steps` exit 1, `kc95_syscheck_1025.py` on the k_c 87 source exit 1).
2. Regrid in `solver/matter`, 8 threads, nice 10 (raised to nice 19 by `watch_i1088a.sh` while an i1088a unit is active), `timeout 21600`: `ell_refine.py l1kc87Lmacm3b2 87 l1kc95dh610d22375 95 1 22.375 2.1014424345 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`; accepted only when `kc95_syscheck_1025.py` exits 0 on the result, both controls exit 1 and the k_c 87 check refuses it.
3. Wide scan (after ACCEPTED and a memory gate that waits, never stops): `d18_hybsign.py` at lambda -0.10 to 0.50 by 0.04 (16 values) and a repeat of 0.14: 17 evaluations on 4 processes of 1 thread at nice 10 (nice 19 by the watcher while an i1088a unit is active): p0 -0.10, 0.06, 0.22, 0.38 and the repeat of 0.14; p1 -0.06, 0.10, 0.26, 0.42; p2 -0.02, 0.14, 0.30, 0.46; p3 0.02, 0.18, 0.34, 0.50.
4. Reading: `read_lower.py scan -0.10 0.50`, `repeat_check.py`, `wide_read.py` (every robust change by position and printed orientation; `leg_read.py`'s pattern cannot read negative numbers and is not used for the reading). **Planted truth before real data** (run now, `planted_wide.py` with the venv python, in `selftest_planted_wide*.log`): synthetic rows for det = (lambda + 0.04)(lambda - 0.11)(lambda - 0.40) on the same grid through the real reader: exactly the three planted brackets (-0.06, -0.02), (0.10, 0.14), (0.38, 0.42) with estimates inside them, the repeat agreeing; with the sign of 0.30 flipped (`--mutate`) the reader finds five changes and the script exits 1.

## Acceptance (fixed before the run)
As `../kc95_d2225/`: the source accepted with controls 1 1 and the k_c 95 check refusing it; the regrid exits 0 inside 21600 s; the result accepted by `kc95_syscheck_1025.py` with both controls exit 1 and refused by the k_c 87 check; every scan process prints the record system and exits 0; the repeat of 0.14 agrees. A control that fires stops the work and I report it; no bar is loosened. Reported: steps, |F|, constraint, Delta of the regridded state beside macm3's k_c 87 record; **every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure)**; changes touching a non-robust point (listed, not counted); ln|det| minima without a sign change; the edge signs; the float64 differences; seconds per point, load, RSS, MemAvailable; what the watcher did. The renice watcher's patterns are checked for this tag before the start (`watch_i1088a.sh` names `l1kc95dh610d22375` and `kc95dh610d22375` and nothing else).

## Threads and memory (stated before)
This lane: the regrid 8 threads, then 4 scan processes. Beside it: the D 22.1875 lane (`../kc95_d221875/`, a regrid since 06:12 UTC then 4 or 8 scan processes), the recount (2 busy), the quest's `i1088a-*` units (up to 10 threads) and the other agents' jobs: the coordinator counts about 9 idle threads; both lanes' compute processes are at nice 19 while a quest unit is active. One k_c 95 scan process peaked at 3.1 GiB, the regrid at 2.55 GiB; MemAvailable is about 45 GB now.

## Predictions, registered before the runs (mine, information)
Basis: k_c 87 roots at 22.125, 22.1875, 22.25: 0.491017, 0.473467, 0.442516 (steps -0.0175, -0.0310 per 0.0625 of D, growing); k_c 95: 0.491072 (22.125), 0.434264 (22.25); the coordinator expects lambda_1 near 0.40 at k_c 95, D 22.375; extrapolating the growing steps gives about 0.36 (0.34 to 0.39).
- Source accepted with controls 1 1 and the k_c 95 check refusing it: 93%. Regrid exits 0 and is accepted: 85%. Steps about 3122 (macm3's 2864 times 1.09: within 10: 55%; within 30: 88%); |F| below 1e-9: 95%; the Delta shift negative (92%) and about -2.4e-05 (the shifts were -1.027e-05 at D 21.75, -1.754e-05 at 22.125, -2.030e-05 at 22.25: within 0.6e-5: 55%). Regrid wall 4000 to 10000 s (65%; 5222 s at D 22.125 with the quest's units, 3203 s at D 22.25; this one runs beside another regrid); peak sampled RSS below 3 GiB (85%).
- Wide scan: at least 15 of the 17 points noise-robust (70%); the repeat of 0.14 on another process bit-identical (85%). Number of robust changes in -0.10 to 0.50: exactly one, lambda_1 alone (50%); exactly two (an extra root below lambda_1) (28%); three or more (12%); none (10%). The highest change (lambda_1) lies in (0.30, 0.42) (75%): bracket (0.34, 0.38) 35%, (0.30, 0.34) 25%, (0.38, 0.42) 15%. Printed orientation of lambda_1: "- to +" (65%), "+ to -" (30%). If there are two changes, the lower one lies in (0.06, 0.18) (60%), and then lambda_1 prints "+ to -" (60%), the coordinator's picture. The float64 sign agrees with the hybrid at all 17 evaluations (25%). Each scan point 1800 to 4000 s (60%; the wide window has no reason to cost more per point than a narrow one); the scan done (p0 runs 5 evaluations) within 6 h of its start (65%).
- Timeline: the regrid done within 3 h of the lane's start (65%).

## Regrid result (25 Nov, 06:17:03 to 08:21:08 UTC): ACCEPTED
`ell_refine.py` (8 threads, nice 10, raised to nice 19 at 06:18:05 UTC by the watcher while an `i1088a-*` unit was active) exited 0 after **7428 s** (the record's own 7425 s; predicted 4000 to 10000 s: yes). Mean sampled CPU 732% (122 samples, `regrid/regrid_samples.csv`), peak sampled RSS 2.56 GiB; 23 numpy RuntimeWarning lines in the log, as in the earlier regrids; no memory alert. It ran beside the D 22.1875 regrid (to 07:38) and the quest's units.
- Record `l1kc95dh610d22375.jsonl` (blob 0fac3b2b) and state `sol_l1kc95dh610d22375_D22.3750.npy` (blob e5c4682a, copied to `in/`; `in_blobs_regrid.txt`): k_c 95 at D 22.375, |F| 3.8917763591e-10, F_start 4.981e-05, **3128 steps** (macm3's k_c 87: 2864; ratio 1.0922; predicted about 3122), constraint 5.134e-03 (macm3's k_c 87: 7.786e-03, ratio 0.659), **Delta 1.1562229943** (macm3's k_c 87: 1.1562474234; shift **-2.443e-05**; predicted about -2.4e-05).
- **Acceptance:** `kc95_syscheck_1025.py` exit 0 (the state's |F| equals the record's, `freeze_from` gives 3128 steps = the record's); `--mutate=F` exit 1, `--mutate=steps` exit 1; `kc87_syscheck_1025.py` on the k_c 95 result exits 1 (refuses). Raw `d9cf426e`.
- **Wide scan:** started 08:21:13 UTC on 4 processes as ordered (17 evaluations; p0 has 5, so about 4 to 5 times one point's cost); the watcher reniced the 4 scan processes to nice 19 at 08:21:15 UTC (`i1088a-j2000m.service` active).

### Regrid predictions scorecard (registered before the run)
| prediction | result |
|---|---|
| source accepted with controls 1 1, the k_c 95 check refusing it (93%) | right |
| regrid exits 0 and is accepted (85%) | right |
| steps about 3122 (within 10: 55%; within 30: 88%) | right (3128: within 10) |
| \|F\| below 1e-9 (95%) | right (3.89e-10) |
| the Delta shift negative (92%) and about -2.4e-05, within 0.6e-5 (55%) | right (-2.443e-05); right |
| regrid wall 4000 to 10000 s (65%) | right (7428 s) |
| peak sampled RSS below 3 GiB (85%) | right (2.56 GiB) |
| the regrid done within 3 h of the lane's start (65%) | right (2 h 04 min) |

## Scan result (25 Nov, 08:21:13 to 14:00:57 UTC, 339.7 min, 4 processes; `summarize_kc95.py` > `summary_kc95.txt`)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| -0.100 | - | -- (True) | - | -2694.985353299071 | 5075 |
| -0.060 | - | -- (True) | - | -2698.555449560897 | 4298 |
| -0.020 | - | -- (True) | - | -2702.1361321958307 | 5042 |
| 0.020 | - | -- (True) | - | -2705.7289713217633 | 4578 |
| 0.060 | - | -- (True) | - | -2709.336206474374 | 3696 |
| 0.100 | - | -- (True) | - | -2712.961084059618 | 3780 |
| 0.140 | - | -- (True) | - | -2716.6084667883365 | 2670 |
| 0.140 | - | -- (True) | - | -2716.6084667883365 | 3839 |
| 0.180 | - | -- (True) | - | -2720.2860159051315 | 3911 |
| 0.220 | - | -- (True) | - | -2724.006745418366 | 3937 |
| 0.260 | - | -- (True) | - | -2727.795405917757 | 3636 |
| 0.300 | - | -- (True) | - | -2731.7086636828326 | 3626 |
| 0.340 | - | -- (True) | - | -2735.934694992649 | 3578 |
| 0.380 | + | ++ (True) | + | -2742.0397329270227 | 4997 |
| 0.420 | + | ++ (True) | + | -2742.7916978825333 | 4483 |
| 0.460 | + | ++ (True) | + | -2745.6283504717035 | 4838 |
| 0.500 | + | ++ (True) | + | -2748.7305673886635 | 4767 |

scan points: 17 evaluations, seconds per point min 2670, median 3937, max 5075, sum 70751; outside 1800 to 4000 s: [(-0.1, 5075), (-0.06, 4298), (-0.02, 5042), (0.02, 4578), (0.38, 4997), (0.42, 4483), (0.46, 4838), (0.5, 4767)]
the regridded record at D 22.375: |F| 3.891776359084224e-10, steps 3128, constraint 0.005134074026698804, Delta 1.1562229943027866, h None, seconds 7425
float64 sign differs from the hybrid at: []

```
=== read_lower.py /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc95_d22375/scan -0.10 0.50
points 16 in -0.100-0.500; not noise-robust: none
hybrid signs: -0.100- -0.060- -0.020- 0.020- 0.060- 0.100- 0.140- 0.180- 0.220- 0.260- 0.300- 0.340- 0.380+ 0.420+ 0.460+ 0.500+
float64 sign differs from the hybrid sign at: none
repeated points: [(0.14, 'agree')]
  robust change (0.340, 0.380), - to +, det-linear 0.379911, range [0.341204, 0.379911]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: - at -0.100, + at 0.500
read_lower exit 0
=== repeat_check.py (merged scan file)
repeat check /home/nathan/Source/choptuik-large-d-raw/I1025-dh610/kc95_d22375/scan/scan_D22.375_all.jsonl: lambda [0.14]: [2] evaluations each, agree -> PASS
repeat_check exit 0
```

- **All 4 processes exit 0 and printed the record system** (|F| 3.8933831162e-10 recomputed against the record's 3.8917763591e-10, steps 3128 = the record's); the pre-run checks passed (`selftest_exits.txt` 0 0 0 1 1 0 0 1 0 1 0 1, as the lane wanted). The scan ran on 4 processes (p0 -0.10, 0.06, 0.22, 0.38, then the repeat of 0.14; p1 -0.06, 0.10, 0.26, 0.42; p2 -0.02, 0.14, 0.30, 0.46; p3 0.02, 0.18, 0.34, 0.50) at nice 19 (the watcher's renice at 08:21:15 UTC, 4 pids, `i1088a_yield.txt`); process walls 4:30:06 (p1), 4:40:44 (p3), 4:49:13 (p2), 5:39:43 (p0).
- **One robust change in the window -0.10 to 0.50:** (0.340, 0.380), **"- to +" as the reader prints it**, det-linear **0.379911**, estimator range [0.341204, 0.379911] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.04, and the range fills the bracket, so the position inside it is not fixed by this scan). Edge signs differ (- at -0.10, + at 0.50). **No other change:** the hybrid sign is "-" at every point from -0.10 to 0.34 (in particular at 0.06, 0.10, 0.14 and 0.18, where k_c 87 has its extra root at D 22.25) and "+" at 0.38, 0.42, 0.46 and 0.50. No ln|det| minimum without a sign change; every point noise-robust (17 of 17); the float64 sign agrees with the hybrid at all 17.
- **The repeat of 0.14** (p2 and p0, two processes) is bit-identical (hybrid -, ln|det| -2716.6084667883365 in both; `repeat_check.py` PASS).
- **ln|det| (hybrid) along the grid:** the differences per 0.04 step are -3.57, -3.58, -3.59, -3.61, -3.62, -3.65 (to 0.14), -3.68, -3.72, -3.79 (to 0.26), -3.91 (0.26 to 0.30), -4.23 (0.30 to 0.34), **-6.11 (0.34 to 0.38, the bracket of the change)**, -0.75 (0.38 to 0.42), -2.84, -3.10. Printed as read; not interpreted here.
- **k_c 95 roots along D (det-linear; brackets as read; not corrected for the grid):** D 22.0 0.545920 (win2), D 22.25 0.434264 (mine, bracket (0.430, 0.435)), **D 22.375 0.379911 (mine, bracket (0.34, 0.38))**, D 22.5 0.339034 (win2, bracket (0.30, 0.34)). All four print "- to +". The coordinator's reason for this lane: macm3's k_c 87 has an extra root near 0.11 at D 22.25 that k_c 95 lacks there; **at D 22.375 k_c 95 shows no root near 0.11 either** (hybrid "-" at 0.06 to 0.18). macm3 has no k_c 87 reading at D 22.375 yet, so there is no k_c 87 root to put beside this one.
- **Seconds per point: 2670 to 5075 s** (median 3937), 4 processes at nice 19 beside the recount, the quest's units, my D 22.1875 scan (to 10:02), my k_c 103 D 22.125 regrid (from 10:09, 8 threads) and its scan (from 13:40): the points of the first round (-0.10, -0.06, -0.02, 0.02) took 4298 to 5075 s, the later ones 3578 to 4997 s, and the last one (p0's repeat of 0.14, from 13:16 to 14:00 UTC, beside only my k_c 103 scan, the recount and the quest's units) 2670 s. Load (1-minute, 677 samples 08:21 to 14:00 UTC): median 17.35, max 27.0, min 10.3; above 22 in 11 episodes of 30 s to 24 min (the longest 12:30 to 12:54 UTC), never for an hour (`load_alert.sh` silent, `load_alert.out` empty); peak RSS per process 3.04 to 3.10 GiB (`/usr/bin/time -v`); MemAvailable at least 42.48 GiB; no memory alert.

### Scan predictions scorecard (registered before the run)
| prediction | result |
|---|---|
| at least 15 of the 17 points noise-robust (70%) | right (17 of 17) |
| the repeat of 0.14 on another process bit-identical (85%) | right |
| exactly one robust change, lambda_1 alone (50%); exactly two (28%); three or more (12%); none (10%) | right (one) |
| the highest change in (0.30, 0.42) (75%): bracket (0.34, 0.38) 35%, (0.30, 0.34) 25%, (0.38, 0.42) 15% | right; right (bracket (0.340, 0.380)) |
| the printed orientation of lambda_1 "- to +" (65%), "+ to -" (30%) | right ("- to +") |
| if two changes: the lower in (0.06, 0.18) (60%), lambda_1 "+ to -" (60%) | not tested (one change) |
| the float64 sign agrees with the hybrid at all 17 evaluations (25%) | right (agrees at all 17) |
| each scan point 1800 to 4000 s (60%) | WRONG (2670 to 5075 s; 8 of 17 outside) |
| the scan done within 6 h of its start (65%) | right (5.66 h) |

## Status
- 2026-11-25 06:16 UTC: folder, pinned inputs, lane, wide reader with its planted-truth check, watcher (patterns checked) and README written before any run; the unit `i1025-kc95-22_375` is started next.
- 06:16:55 UTC: unit `i1025-kc95-22_375` started (selftests 0 0 0 1 1 0 0 1 0 1 0 1, source accepted with controls 1 1 and the k_c 95 check refusing it, regrid started 06:17:03 UTC at nice 10).
- 2026-11-25 06:18 UTC: a defect of mine, fixed: the watcher `watch_i1088a.sh` ended at once because `exits_kc95.txt` still held the line "STOP: in_blobs_src.txt is missing or empty" of my deliberate test of the new pin check (06:16:16 UTC), which its loop took for the lane's end; the regrid therefore ran at nice 10 until 06:18:05 UTC, when the corrected watcher (it counts only lines written after its own start; the old file kept as `watch_i1088a_stale_stop.sh`) raised it to nice 19 (`i1088a_yield.txt`; `i1088a-buildmob.service` is active). My first waiter had the same flaw and was replaced by a baseline-aware one. The same stale-line trap does not apply to `../kc95_d221875/` (no test STOP in its exits file).
- 2026-11-25 08:22 UTC: the regrid is ACCEPTED (06:17:03 to 08:21:08 UTC, 7428 s; result above, raw d9cf426e). The wide scan started 08:21:13 UTC on 4 processes, nice 19 by the watcher.
- 2026-11-25 14:10 UTC: the scan is done (08:21:13 to 14:00:57 UTC): one robust change in -0.10 to 0.50, bracket (0.340, 0.380) printed "- to +", det-linear 0.379911; no change near 0.11; result and scorecard above. This lane is finished.
