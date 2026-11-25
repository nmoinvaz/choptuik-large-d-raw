# I1025-dh610/kc95_d221875: macm3's k_c 87 b2 leg state at D 22.1875 regridded to k_c 95, then a hybrid sign scan at lambda_1 0.455 to 0.485

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 62 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-25 03:06 UTC, before any run of this folder (the pin of the source state came first; no regrid, no scan). The k_c 95 roots are not yet physical. A root is identified by position; its orientation is printed as the reader prints it and is not interpreted here.

## Order (coordinator t5, hc, read at about 03:00 UTC 25 Nov), verbatim
"Coordinator (t5): next l = 1 lane (#1025), 8 threads, the quest's i1088a units first as before: k_c 95 at D 22.125, then at D 22.1875, from macm3's b2 states (tag l1kc87Lmacm3b2), same procedure as kc95_d2225. Windows: D 22.125 lambda 0.475 to 0.505 by 0.005 plus the repeat of 0.490 (k_c 87: 0.4908, '- to +'); D 22.1875 lambda 0.455 to 0.485 plus the repeat of 0.470 (k_c 87: 0.4735, '+ to -'). Report each root WITH its orientation as printed. The question is where k_c 95's orientation flips relative to k_c 87's near D 22.17 (at D 22.25 k_c 95 reads '- to +' where k_c 87 reads '+ to -'). Raw kc95_d22125/ and kc95_d221875/."

This folder is D 22.1875 (the other is `../kc95_d22125/`); the two lanes run one at a time (8 threads), D 22.125 first. The order gives no prediction, so the prediction below (PRED 0.4663 for the reader's "against the prediction" line) is mine, registered before the run. macm3's own reading of this state (`I1025-macm3/kc87_leg_lambda/22.1875/read_lower.txt`, macOS): one robust change, bracket (0.470, 0.475), "+ to -" as printed, det-linear 0.473467, range [0.472991, 0.473467]; its float64 sign differed from the hybrid at 0.475; the file's window is 0.455 to 0.475. Orientations (as printed): macm3's k_c 87 at D 21.75 "- to +", D 22.125 "- to +", D 22.1875 "+ to -", D 22.25 "+ to -"; this lane's k_c 95 at D 21.75 "- to +" and at D 22.25 "- to +".

## Inputs (copies in `in/`; `in_blobs.txt` lists their blobs, `in_blobs_src.txt` the source's; the lane refuses any other blob)
| item | source | blob |
|---|---|---|
| macm3's k_c 87 D 22.1875 state (commit 0ab2471c, 2026-11-24 15:38:48 -08:00 = 23:38:48 UTC) | I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.187500.npy | 8f56f515 |
| its record file (rows up to D 22.1875: \|F\| 3.923363163938017e-10, 2869 steps, psi-constraint 0.0070353243141629005, Delta 1.1509177741042835, h 0.03125) | same folder, l1kc87Lmacm3b2.jsonl at that commit | 3c1508ee |
| the k_c 87 check; the k_c 95 check (3 changed lines, `kc95_syscheck_1025.diff`); the scanner, reader, repeat check, `leg_read.py` | as `../kc95_d2225/in/` | 6df5d960; d487e628; e089207a, 89309d3c, aaf598a9, 5cae2639 |
Code and environment as `../kc95_d2225/` (worktrees `~/Source/choptuik-large-d-1025g` 48c36355 and `-1025f` 505d8399, `~/Source/venv-i1058`). lambda_0(22.1875) from `ell_delta.lam0_at` reads **2.1021310306** (the regrid's 7th argument; the lane stops if it reads otherwise).

## Commands (`lane_kc95.sh` in this folder, a copy of `../kc95_d2225/lane_kc95.sh` for this D; unit `i1025-kc95-22_1875` via `start_kc95.sh`; `chain_kc95_22.sh` runs this lane and then the other)
1. Pins and selftests (wanted `0 0 0 1 1 0 0 1`), the source check (`kc87_syscheck_1025.py` exit 0, `--mutate=F` and `--mutate=steps` exit 1, `kc95_syscheck_1025.py` on the k_c 87 source exit 1).
2. Regrid in `solver/matter`, 8 threads, nice 10, `timeout 21600`: `ell_refine.py l1kc87Lmacm3b2 87 l1kc95dh610d221875 95 1 22.1875 2.1021310306 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`; accepted only when `kc95_syscheck_1025.py` exits 0 on the result, both controls exit 1 and the k_c 87 check refuses it.
3. Scan (after ACCEPTED and a memory gate that waits, never stops): `d18_hybsign.py` at lambda 0.455, 0.460, 0.465, 0.470, 0.475, 0.480, 0.485 and a repeat of 0.470: 8 evaluations on 8 processes of 1 thread at nice 10, or on 4 processes (2 evaluations each: p0 0.455 and 0.470, p1 0.460 and 0.475, p2 0.465 and 0.480, p3 0.485 and the repeat of 0.470) when an i1088a unit is active at the start (the order: its units first); `watch_i1088a.sh` raises this lane's compute processes to nice 19 by exact pid while an i1088a unit is active; nothing is stopped.
4. Reading: `read_lower.py scan 0.455 0.485`, `repeat_check.py`, `leg_read.py read` against 0.4663 (bar 0.005). No robust change: reported as read, no widening.

## Acceptance (fixed before the run)
As `../kc95_d2225/`: the source accepted with controls 1 1 and the k_c 95 check refusing it; the regrid exits 0 inside 21600 s; the result accepted by `kc95_syscheck_1025.py` with both controls exit 1 and refused by the k_c 87 check; every scan process prints the record system and exits 0; the repeat agrees. A control that fires stops the work and I report it; no bar is loosened. Reported: steps, |F|, constraint, Delta of the regridded state beside macm3's k_c 87 record; every robust change by position (bracket, orientation **as printed**, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside macm3's k_c 87 root and orientation; the k_c step (k_c 95 minus k_c 87 root); seconds per point, load, RSS, MemAvailable; what the watcher did.

## Predictions, registered before the runs (mine, information)
Basis: the k_c step (k_c 95 root minus macm3's k_c 87 root) was +0.0018 at D 21.0 and +0.0039 at D 21.125 (the coordinator's earlier figures), -0.000991 at D 21.75 and -0.008252 at D 22.25 (this lane's `../kc95_d2175/`, `../kc95_d2225/`); a quadratic through the last three points (D 21.125, 21.75, 22.25) gives about -0.0062 at D 22.125 and -0.0072 at D 22.1875, so PRED = macm3's k_c 87 root plus that step (0.4848 and 0.4663). The Delta shift of the regrid was -1.027e-05 (D 21.75) and -2.030e-05 (D 22.25), -2.2e-06 at D 19.5 and 19.75.
- Source accepted with controls 1 1 and the k_c 95 check refusing it: 93%. Regrid exits 0 and is accepted: 85%.
- Steps about 3128 (the 87 to 95 ratio was 1.0903 at D 22.25; macm3's record has 2869): within 10: 60%; within 30: 90%. |F| below 1e-9: 95%.
- Delta shift: by linear interpolation in D between -1.027e-05 and -2.030e-05, -1.90e-05, so Delta about 1.150899 (the shift within 0.5e-5 of that: 60%; negative: 92%).
- Regrid wall 2800 to 4500 s (65%; 3066 s at D 19.75 and 3203 s at D 22.25, 9339 s at D 21.75); peak sampled RSS below 3 GiB (85%).
- Scan: every point noise-robust (75%); the repeat on another process than its original bit-identical (85%); exactly one robust change in the window (80%), none (10%), two or more (10%). The change within 0.005 of 0.4663 (65%); within 0.002 (35%); below macm3's k_c 87 root (85%); the step between -0.009 and -0.003 (60%). The bracket (0.465, 0.470) (45%). The printed orientation of the k_c 95 root is "- to +" (75%; at D 21.75 and D 22.25 it is "- to +" while macm3's k_c 87 reads "- to +" and "+ to -" there). The float64 sign agrees with the hybrid at all evaluations (25%). Each scan point 1800 to 3500 s (60%; the D 22.25 points took 1851 to 2077 s on 4 processes with the quest's build beside them); the scan done within 100 min of its start (65%).
- Timeline: the regrid done within 90 min of the lane's start (65%); the whole lane (regrid and scan) done within 3 h (60%).

## Regrid result (25 Nov, 06:12:03 to 07:38:50 UTC): ACCEPTED
`ell_refine.py` (8 threads, nice 10, raised to nice 19 by the watcher while an `i1088a-*` unit was active) exited 0 after **5196 s** (the record's own 5193 s; predicted 2800 to 4500 s: no). Mean sampled CPU 756% (85 samples, `regrid/regrid_samples.csv`); peak sampled RSS 1.86 GiB; 25 numpy RuntimeWarning lines in the log, as in the earlier regrids; no memory alert. It ran beside the D 22.375 regrid (from 06:17) and the quest's units, as the D 22.125 regrid (5222 s) did.
- Record `l1kc95dh610d221875.jsonl` (blob a0def3b7) and state `sol_l1kc95dh610d221875_D22.1875.npy` (blob 61f208a9, copied to `in/`; `in_blobs_regrid.txt`): k_c 95 at D 22.1875, |F| 4.0205479076e-10, F_start 4.263e-05, **3132 steps** (macm3's k_c 87: 2869; ratio 1.0917, predicted about 3128), constraint 4.494e-03 (macm3's k_c 87: 7.035e-03, ratio 0.639), **Delta 1.1508992846** (macm3's k_c 87: 1.1509177741; shift **-1.849e-05**; I predicted -1.90e-05, Delta about 1.150899).
- **Acceptance:** `kc95_syscheck_1025.py` exit 0 (the state's |F| equals the record's, `freeze_from` gives 3132 steps = the record's); `--mutate=F` exit 1, `--mutate=steps` exit 1; `kc87_syscheck_1025.py` on the k_c 95 result exits 1 (refuses). Raw `ce9f1702`.
- **i1088a:** `i1088a-j2000m.service` was active at 07:38:54 UTC, so the scan runs on 4 processes (8 evaluations, 2 each: p0 0.455 and 0.470, p1 0.460 and 0.475, p2 0.465 and 0.480, p3 0.485 and the repeat of 0.470), reniced to nice 19 at 07:39:09 UTC by the watcher (re-armed by the continuation session at 07:15 UTC, after the account switch).

### Regrid predictions scorecard (registered before the run)
| prediction | result |
|---|---|
| source accepted with controls 1 1, the k_c 95 check refusing it (93%) | right |
| regrid exits 0 and is accepted (85%) | right |
| steps about 3128 (within 10: 60%; within 30: 90%) | right (3132) |
| \|F\| below 1e-9 (95%) | right (4.02e-10) |
| the Delta shift within 0.5e-5 of -1.90e-05 (60%); negative (92%) | right (-1.849e-05); right |
| regrid wall 2800 to 4500 s (65%) | WRONG (5196 s) |
| peak sampled RSS below 3 GiB (85%) | right (1.86 GiB) |
| the regrid done within 90 min of the lane's start (65%) | right (86.8 min) |

## Scan result (25 Nov, 07:38:54 to 10:02:12 UTC, 143.3 min, 4 processes; `summarize_kc95.py` > `summary_kc95.txt`)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.455 | - | -- (True) | - | -2768.6441801085484 | 3310 |
| 0.460 | - | -- (True) | + | -2770.175264469934 | 3624 |
| 0.465 | + | ++ (True) | - | -2770.6149206298587 | 3534 |
| 0.470 | + | ++ (True) | + | -2769.9486633570154 | 4432 |
| 0.470 | + | ++ (True) | + | -2769.9486633570154 | 4583 |
| 0.475 | + | ++ (True) | + | -2769.8716046010877 | 4966 |
| 0.480 | + | ++ (True) | + | -2769.969051641245 | 4296 |
| 0.485 | + | ++ (True) | + | -2770.151675934942 | 3701 |

scan points: 8 evaluations, seconds per point min 3310, median 3998, max 4966, sum 32446; outside 1800 to 3500 s: [(0.46, 3624), (0.465, 3534), (0.47, 4432), (0.47, 4583), (0.475, 4966), (0.48, 4296), (0.485, 3701)]
the regridded record at D 22.1875: |F| 4.020547907630559e-10, steps 3132, constraint 0.004494247385818032, Delta 1.1508992846163095, h None, seconds 5193
float64 sign differs from the hybrid at: [0.46, 0.465]

```
hybrid signs: 0.455- 0.460- 0.465+ 0.470+ 0.475+ 0.480+ 0.485+
robust changes: 1
   change (0.460, 0.465), - to +, det-linear 0.463041, range [0.462294, 0.463041]
against the prediction 0.4663: change minus prediction -0.003259; within 0.005: True
```

- **All 4 processes exit 0 and printed the record system** (|F| 4.0218165377e-10 recomputed against the record's 4.0205479076e-10, steps 3132 = the record's); the pre-run checks passed (`selftest_exits.txt` 0 0 0 1 1 0 0 1). The scan ran on 4 processes (p0 0.455 and 0.470, p1 0.460 and 0.475, p2 0.465 and 0.480, p3 0.485 and the repeat of 0.470) because `i1088a-j2000m.service` was active at the start (and `i1088a-j2000b.service` at the end); process walls 2:10:37 to 2:23:17.
- **One robust change in the window 0.455 to 0.485:** (0.460, 0.465), **"- to +" as the reader prints it**, det-linear **0.463041**, estimator range [0.462294, 0.463041] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (- at 0.455, + at 0.485). No ln|det| minimum without a sign change; every point noise-robust (8 of 8).
- **The float64 sign differs from the hybrid at 0.460 and 0.465.** The float64 signs alone read - + - + + + + (0.455 to 0.485), which would be three changes (between 0.455 and 0.460, 0.460 and 0.465, 0.465 and 0.470); the hybrid, which the reader reads, gives one. Both noise tests agree with the hybrid at every point.
- **The repeat of 0.470** (p0 and p3, two processes) is bit-identical (hybrid +, ln|det| -2769.9486633570154 in both; `repeat_check.py` PASS).
- **Beside macm3's k_c 87 root at the same D** (0.473467, bracket (0.470, 0.475), range [0.472991, 0.473467], printed "+ to -"; macOS scan of its own state), this lane's k_c 95 root is:

| | bracket | printed orientation | det-linear root | estimator range |
|---|---|---|---|---|
| macm3 k_c 87 | (0.470, 0.475) | + to - | 0.473467 | [0.472991, 0.473467] |
| dh610 k_c 95 | (0.460, 0.465) | - to + | 0.463041 | [0.462294, 0.463041] |

  The k_c 95 root is **0.010426 below** macm3's k_c 87 root, the brackets differ and the two estimator ranges do not overlap. There is no robust change in this scan near 0.4735: the hybrid sign is + at 0.465 to 0.485. The k_c step (k_c 95 minus k_c 87 root) is therefore **-0.010426** at D 22.1875, against -0.000991 (D 21.75), +0.000055 (D 22.125) and -0.008252 (D 22.25). Against my prediction 0.4663: -0.003259, inside the bar 0.005.
- **The coordinator's question, the printed orientations side by side (as printed; not interpreted here):**

| D | k_c 87 (macm3) | k_c 95 (dh610) |
|---|---|---|
| 21.75 | - to + | - to + |
| 22.125 | - to + | - to + |
| 22.1875 | + to - | - to + |
| 22.25 | + to - | - to + |

  On this grid the k_c 95 root prints "- to +" at all four D, and k_c 87's printed orientation changes between D 22.125 and D 22.1875: the two agree as printed at D 21.75 and D 22.125, and differ at D 22.1875 and D 22.25.
- **Seconds per point: 3310 to 4966 s** (median 3998), 4 processes of 2 evaluations at nice 19 (the watcher's renice at 07:39:09 UTC, 4 pids, `i1088a_yield.txt`), beside the recount, the quest's units and the D 22.375 lane (its regrid from 06:17 to 08:21, its scan from 08:21): load median 13.73, max 28.84 (07:43, 9 samples above 22 between 07:41 and 07:45, then lower; far below the alert's hour), min 10.36 over 286 samples 07:39:04 to 10:02:11 UTC; peak RSS per process 3.00 to 3.14 GiB (`/usr/bin/time -v`); MemAvailable at least 42.17 GiB; no memory or load alert. The watcher's pattern was the fixed one, so this time the scan processes ran at nice 19 from the start.

### Scan predictions scorecard (registered before the run)
| prediction | result |
|---|---|
| every point noise-robust (75%) | right (8 of 8) |
| the repeat on another process bit-identical (85%) | right |
| exactly one robust change in the window (80%) | right |
| the change within 0.005 of 0.4663 (65%); within 0.002 (35%) | right (-0.003259); WRONG |
| below macm3's k_c 87 root, the step negative (85%) | right (-0.010426) |
| the step between -0.009 and -0.003 (60%) | WRONG (-0.010426) |
| the bracket (0.465, 0.470) (45%) | WRONG (it is (0.460, 0.465)) |
| the printed orientation of the k_c 95 root is "- to +" (75%) | right |
| the float64 sign agrees with the hybrid at all evaluations (25%) | WRONG (differs at 0.460 and 0.465) |
| each scan point 1800 to 3500 s (60%) | WRONG (3310 to 4966 s; 7 of 8 outside) |
| the scan done within 100 min of its start (65%) | WRONG (143.3 min) |
| the whole lane done within 3 h (60%) | WRONG (230.2 min: 06:12:03 to 10:02:12 UTC) |

## Status
- 2026-11-25 03:06 UTC: folder, inputs (pinned: `in_blobs.txt`, `in_blobs_src.txt`, `source_commit.txt`), lane, watcher and README written before any run; `lane_kc95.sh dry` and the unit `i1025-kc95-chain22` (both lanes in turn) are started next.
- 2026-11-25 07:40 UTC: the regrid is ACCEPTED (06:12:03 to 07:38:50 UTC, 5196 s; result above, raw ce9f1702). The scan started 07:38:54 UTC on 4 processes (an i1088a unit is active), nice 19 by the watcher.
- 2026-11-25 10:04 UTC: the scan is done (07:38:54 to 10:02:12 UTC): one robust change, bracket (0.460, 0.465) printed "- to +", det-linear 0.463041, 0.010426 below macm3's k_c 87 0.473467 (printed "+ to -"), -0.003259 against my prediction 0.4663; result and scorecard above. This lane is finished.
- 2026-11-25 17:47 UTC, amendment (the coordinator's hc, dh370's finding: on Linux nice is per thread, `renice -p PID` moves only the main thread): this lane's yield watcher raised only the main thread of its regrid (8 threads, 06:12:03 to 07:38:50 UTC) to nice 19, at 06:12:31 UTC (`i1088a_yield.txt`); by dh370's test its worker threads stayed at nice 10 (inferred from the mechanism, not observed: the process is gone). The scan's processes are 1 thread each, so their nice 19 was right. The fixed watcher and `renice_threads.sh` are in `../kc103_d225/`.
