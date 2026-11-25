# I1025-dh610/kc103_d22125: my k_c 95 state at D 22.125 regridded to k_c 103, then a hybrid sign scan at lambda_1 0.470 to 0.510

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 62 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-25 10:07 UTC (the clock), before any run of this folder (the pins of the inputs and a syntax check of the lane came first; no regrid, no scan). The k_c 103 roots are not yet physical. A root is identified by position; its orientation is printed as the reader prints it and is not interpreted here.

## Order (coordinator t5, hc, read at about 10:05 UTC 25 Nov), verbatim
"Coordinator (t5), #1025, next lane for your freed threads: k_c 103 at D 22.125 from your accepted k_c 95 state (tag l1kc95dh610d22125; kc95 check accepts, controls 1 1, kc87 and kc103 refuse; result: kc103_syscheck_1025.py 3ab58d16 accepts, kc95 refuses), the regrid recipe of winb's k_c 103 runs, nice 19 under i1088a units, then a scan 0.470 to 0.510 by 0.005 plus the repeat of 0.490, 4 procs. Register first: k_c 87 0.4908 and k_c 95 0.491072 differ by +0.0003, so converged F predicts 0.491 +- 0.005; the k_c 103 steps at D 21.125 (+0.0034) and D 21.75 (+0.0068) say it may move more. Raw kc103_d22125/, README first."

The order gives the prediction 0.491 with bar 0.005 (**PRED 0.491**, the reader's "against the prediction" line). Readings at this D (all printed "- to +"): macm3's k_c 87 root 0.491017, bracket (0.490, 0.495), range [0.490646, 0.491017] (`I1025-macm3/kc87_leg_lambda/22.125/`, macOS; the order's 0.4908 is its rounding of the window reading); my k_c 95 root **0.491072**, bracket (0.490, 0.495), range [0.490684, 0.491072] (`../kc95_d22125/read_lower.txt`, scan 0.475 to 0.505; float64 sign equal to the hybrid at all 7 points; k_c step 87 to 95 +0.000055). The k_c 95 to 103 steps of the other runners, as the order gives them: -0.000062 (D 21.0, winb), +0.0034 (D 21.125), +0.0068 (D 21.75). dh370 runs k_c 103 at D 22.25 and 0.04 spacing from my k_c 95 state there (`../../I1025-dh370/kc103_d2225/`), not read yet.

## Inputs (copies in `in/`; `in_blobs.txt` lists the scripts' blobs, `in_blobs_src.txt` the source's; the lane refuses any other blob)
| item | source | blob |
|---|---|---|
| my k_c 95 state at D 22.125 (accepted 2026-11-25 04:34:32 UTC; |F| 4.0627911135e-10, 3132 steps, constraint 4.293e-03, Delta 1.1491338669, 5219 s) | I1025-dh610/kc95_d22125/in/sol_l1kc95dh610d22125_D22.1250.npy (raw commit ce4fce87f; `source_commit.txt`) | 06c5082f |
| its record (one row, tag l1kc95dh610d22125, kc 95, src l1kc87Lmacm3b2) | same folder, l1kc95dh610d22125.jsonl | 64ecb047 |
| the k_c 95 check (3 changed lines against the k_c 87 check) and the k_c 87 check | as `../kc95_d22125/in/` | d487e628; 6df5d960 |
| the k_c 103 check `kc103_syscheck_1025.py` (dh170's, from `I1025-dh170/kc103_d21125/in/`; 3 changed lines against the k_c 95 check, `kc103_syscheck_1025.diff`) | origin/main of the raw repository | 3ab58d16 |
| the scanner, reader, repeat check, `leg_read.py`, `d185_scan_read.py`, `d18c_read.py` | as `../kc95_d22125/in/` | e089207a, 89309d3c, aaf598a9, 5cae2639, 7c9d400f, 1383470f |
Code and environment as `../kc95_d221875/` (worktrees `~/Source/choptuik-large-d-1025g` 48c36355, which holds the source state and record in `solver/matter/data/` from the k_c 95 regrid, and `-1025f` 505d8399; `~/Source/venv-i1058`). lambda_0(22.125) from `ell_delta.lam0_at` reads **2.1023628304** (the regrid's 7th argument; the lane stops if it reads otherwise).

## Commands (`lane_kc103.sh` in this folder, derived from `../kc95_d221875/lane_kc95.sh`; unit `i1025-kc103-22_125` via `start_kc103.sh`; `watch_i1088a.sh` and `notify_kc103.sh` run beside it)
1. Pins and selftests (wanted `0 0 0 0 1 1 0 0 1`: the k_c 87, k_c 95 and k_c 103 checks, `read_lower.py` with its two mutations, `repeat_check.py`, `leg_read.py` with its mutation), the source check: `kc95_syscheck_1025.py` exit 0 on the source, `--mutate=F` and `--mutate=steps` exit 1, the k_c 87 check and the k_c 103 check exit 1 on it.
2. Regrid in `solver/matter`, 8 threads, nice 10, `timeout 21600`: `ell_refine.py l1kc95dh610d22125 95 l1kc103dh610d22125 103 1 22.125 2.1023628304 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma` (the recipe of winb's and dh170's k_c 103 runs). Accepted only when `kc103_syscheck_1025.py` exits 0 on the result, both controls exit 1, and the k_c 95 check and the k_c 87 check both refuse it.
3. Scan (after ACCEPTED and a memory gate that waits, never stops): `d18_hybsign.py` at lambda 0.470, 0.475, 0.480, 0.485, 0.490, 0.495, 0.500, 0.505, 0.510 and a repeat of 0.490: 10 evaluations on 4 processes of 1 thread at nice 10 (p0 0.490, 0.480, 0.470; p1 0.495, 0.485, 0.510; p2 0.500, 0.475; p3 the repeat of 0.490, 0.505), raised to nice 19 by `watch_i1088a.sh` by exact pid while an i1088a unit is active; nothing is stopped.
4. Reading: `read_lower.py scan 0.470 0.510`, `repeat_check.py`, `leg_read.py read` against 0.491 (bar 0.005). No robust change in the window: reported as read, no widening.

## Acceptance (fixed before the run)
The source accepted with controls 1 1 and refused by the k_c 87 and k_c 103 checks; the regrid exits 0 inside 21600 s; the result accepted by `kc103_syscheck_1025.py` with both controls exit 1 and refused by the k_c 95 and k_c 87 checks; every scan process prints the record system and exits 0; the repeat agrees. A control that fires stops the work and I report it; no bar is loosened. Reported: steps, |F|, constraint, Delta of the k_c 103 state beside my k_c 95 record; every robust change by position (bracket, orientation **as printed**, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside the k_c 95 root 0.491072 and macm3's k_c 87 root 0.491017; the k_c step (k_c 103 minus k_c 95 root); seconds per point, load, RSS, MemAvailable; what the watcher did.

## Predictions, registered before the runs (mine, information)
Basis: the coordinator's 0.491 +- 0.005 (k_c 87 and k_c 95 agree to +0.0001 here, against -0.0010 at D 21.75 and +0.0039 at D 21.125 for the k_c step 87 to 95), and the k_c 95 to 103 steps +0.0034 (D 21.125) and +0.0068 (D 21.75), -0.00006 (D 21.0): the step has been positive and grew with D at the two D where it was measured above 21.0, so I put more weight above 0.491 than below. PRED stays the coordinator's 0.491; "met" means the det-linear root of the robust change nearest 0.491 lies in [0.486, 0.496].
- Source accepted with controls 1 1 and refused by the k_c 87 and k_c 103 checks: 93%. Regrid exits 0 and is accepted: 85%.
- Steps about 3395 (the k_c 95 to 103 ratio was 1.0842 at D 21.125 and 1.0839 at D 21.0; my record has 3132): within 10: 40%; within 30: 80%. |F| below 1e-9: 95%.
- Delta(103) - Delta(95): negative (85%); smaller in magnitude than the 87 to 95 shift of -1.754e-05 at this D (65%).
- Regrid wall 5500 to 9000 s (65%; my k_c 95 regrids took 5196 to 7428 s on 8 threads at nice 19 beside the quest's units, and the k_c 95 to 103 step cost 1.25 to 1.32 times the 87 to 95 one in the winb and dh170 runs); peak sampled RSS below 3.5 GiB (75%; 2.56 GiB at k_c 95, D 22.375).
- Scan: every point noise-robust (70%); the repeat on another process than its original bit-identical (85%); exactly one robust change in the window (75%), none (12%), two or more (13%). The change within 0.005 of 0.491, i.e. PRED met (50%); within 0.002 (20%); above 0.496 (30%); below 0.486 (10%); the step (k_c 103 minus k_c 95 root) positive (65%). The bracket (0.490, 0.495) (25%); (0.495, 0.500) (25%); (0.485, 0.490) (15%). The printed orientation of the k_c 103 root is "- to +" (85%; both earlier readings at this D print it). The float64 sign agrees with the hybrid at all evaluations (30%; it did at all 7 of my k_c 95 scan here, not at D 22.1875). Each scan point 3500 to 6500 s (60%; the D 22.1875 k_c 95 points took 3310 to 4966 s at nice 19 beside the quest's units); the scan done within 5 h of its start (60%).
- Timeline: the regrid done within 2.5 h of the lane's start (70%); the whole lane (regrid and scan) done within 8 h (60%).

## Regrid result (25 Nov, 10:09:35 to 13:40:03 UTC): ACCEPTED
`ell_refine.py` (8 threads, nice 10, raised to nice 19 at 10:09:48 UTC by the watcher while `i1088a-j2000b.service` was active) exited 0 after **12628 s** (the record's own 12625 s; predicted 5500 to 9000 s: no). Mean sampled CPU 661% (210 samples, `regrid/regrid_samples.csv`), about 83.5k CPU-seconds against 39.6k for my k_c 95 regrid at this D (5222 s, 758%): 2.1 times the CPU work for the step from 3132 to 3397 steps, where the winb and dh170 runs saw 1.25 to 1.32 times at D 21.0 and 21.125. Peak sampled RSS 2.98 GiB; 27 numpy RuntimeWarning lines in the log, as in the earlier regrids; no memory alert. It ran beside the D 22.375 wide scan (4 processes), the recount and the quest's units.
- Record `l1kc103dh610d22125.jsonl` (blob 1e903b8b) and state `sol_l1kc103dh610d22125_D22.1250.npy` (blob 7c8d7ad2, copied to `in/`; `in_blobs_regrid.txt`): k_c 103 at D 22.125, |F| 4.1351140279e-10, F_start 1.751e-05, **3397 steps** (my k_c 95: 3132; ratio 1.0846, predicted about 3395), constraint 2.677e-03 (k_c 95: 4.293e-03, ratio 0.624), **Delta 1.1491293754** (k_c 95: 1.1491338669; shift k_c 103 minus k_c 95 **-4.4915e-06**; the k_c 87 to 95 shift was -1.7539e-05).
- **Acceptance:** `kc103_syscheck_1025.py` exit 0 (the state's |F| equals the record's, `freeze_from` gives 3397 steps = the record's); `--mutate=F` exit 1, `--mutate=steps` exit 1; `kc95_syscheck_1025.py` and `kc87_syscheck_1025.py` on the k_c 103 result both exit 1 (refuse). The source check and the selftests are in `exits_kc103.txt` and `regrid/source_*.txt`.
- **Scan:** started 13:40:30 UTC on 4 processes (10 evaluations; p0 0.490, 0.480, 0.470; p1 0.495, 0.485, 0.510; p2 0.500, 0.475; p3 the repeat of 0.490, 0.505); the watcher reniced the 4 processes to nice 19 at 13:40:57 UTC (the scan runs 27 s at nice 10 first: the watcher polls every 30 s).

### Regrid predictions scorecard (registered before the run)
| prediction | result |
|---|---|
| source accepted with controls 1 1, refused by the k_c 87 and k_c 103 checks (93%) | right |
| regrid exits 0 and is accepted (85%) | right |
| steps about 3395 (within 10: 40%; within 30: 80%) | right (3397, within 10) |
| \|F\| below 1e-9 (95%) | right (4.14e-10) |
| Delta(103) - Delta(95) negative (85%); smaller in magnitude than 1.754e-05 (65%) | right (-4.49e-06); right |
| regrid wall 5500 to 9000 s (65%) | WRONG (12628 s) |
| peak sampled RSS below 3.5 GiB (75%) | right (2.98 GiB) |
| the regrid done within 2.5 h of the lane's start (70%) | WRONG (3.52 h: 10:08:49 to 13:40:03 UTC) |

## Scan result (25 Nov, 13:40:30 to 17:17:42 UTC, 217.2 min, 4 processes; `summarize_kc103.py` > `summary_kc103.txt`)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.470 | - | -- (True) | - | -3105.795339859036 | 3853 |
| 0.475 | - | -- (True) | - | -3106.558623431753 | 4127 |
| 0.480 | - | -- (True) | - | -3107.4424187887776 | 4213 |
| 0.485 | - | -- (True) | + | -3108.6250963380644 | 4288 |
| 0.490 | + | ++ (True) | - | -3112.479673623191 | 4451 |
| 0.490 | + | ++ (True) | - | -3112.479673623191 | 4539 |
| 0.495 | + | ++ (True) | + | -3109.5046048667373 | 4528 |
| 0.500 | + | ++ (True) | + | -3109.3000033988346 | 4567 |
| 0.505 | + | ++ (True) | + | -3109.372399630725 | 3997 |
| 0.510 | + | ++ (True) | + | -3109.5598065181575 | 4211 |

scan points: 10 evaluations, seconds per point min 3853, median 4250, max 4567, sum 42774; outside 3500 to 6500 s: []
the regridded record at D 22.125: |F| 4.135114027900697e-10, steps 3397, constraint 0.002677338499874125, Delta 1.1491293753694207, h None, seconds 12625
float64 sign differs from the hybrid at: [0.485, 0.49, 0.49]

```
hybrid signs: 0.470- 0.475- 0.480- 0.485- 0.490+ 0.495+ 0.500+ 0.505+ 0.510+
robust changes: 1
   change (0.485, 0.490), - to +, det-linear 0.489896, range [0.489754, 0.489896]
against the prediction 0.491: change minus prediction -0.001104; within 0.005: True
```

- **All 4 processes exit 0 and printed the record system** (|F| 4.1358706522e-10 recomputed against the record's 4.1351140279e-10, steps 3397 = the record's); the pre-run checks passed (`selftest_exits.txt` 0 0 0 0 1 1 0 0 1). The scan ran on 4 processes (p0 0.490, 0.480, 0.470; p1 0.495, 0.485, 0.510; p2 0.500, 0.475; p3 the repeat of 0.490 and 0.505); process walls 2:20:52 (p3), 2:25:03 (p2), 3:30:16 (p0), 3:37:11 (p1).
- **One robust change in the window 0.470 to 0.510:** (0.485, 0.490), **"- to +" as the reader prints it**, det-linear **0.489896**, estimator range [0.489754, 0.489896] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (- at 0.470, + at 0.510). No ln|det| minimum without a sign change (the ln|det| at 0.490, -3112.48, lies 3.9 below its 0.485 neighbor and 3.0 below its 0.495 neighbor, with the sign change just below it); every point noise-robust (10 of 10).
- **The float64 sign differs from the hybrid at 0.485 and 0.490** (both evaluations of 0.490). The float64 signs alone read - - - + - + + + + (0.470 to 0.510), which would be three changes (between 0.480 and 0.485, 0.485 and 0.490, 0.490 and 0.495); the hybrid, which the reader reads, gives one. Both noise tests agree with the hybrid at every point.
- **The repeat of 0.490** (p0 and p3, two processes) is bit-identical (hybrid +, ln|det| -3112.479673623191 in both; `repeat_check.py` PASS).
- **The three readings at this D, side by side (as printed; the k_c 87 and k_c 95 rows are earlier results):**

| | bracket | printed orientation | det-linear root | estimator range |
|---|---|---|---|---|
| macm3 k_c 87 (`I1025-macm3/kc87_leg_lambda/22.125/`) | (0.490, 0.495) | - to + | 0.491017 | [0.490646, 0.491017] |
| dh610 k_c 95 (`../kc95_d22125/`) | (0.490, 0.495) | - to + | 0.491072 | [0.490684, 0.491072] |
| dh610 k_c 103 (this folder) | (0.485, 0.490) | - to + | 0.489896 | [0.489754, 0.489896] |

  The k_c step (k_c 103 minus k_c 95 root) is **-0.001176** (det-linear roots; the estimator ranges do not overlap, gap 0.000788), against +0.000055 for the step 87 to 95 here and -0.000062 (D 21.0), +0.0034 (D 21.125), +0.0068 (D 21.75) for 95 to 103 elsewhere. The sign of this step is fixed by the grid: at the shared point 0.490 the k_c 95 hybrid sign is - (before its root) and the k_c 103 hybrid sign is + (after its root), both noise-robust and repeated bit-identically in their own scans, so the k_c 103 root lies below 0.490 and the k_c 95 root above it, one robust change each; the hybrid's call at 0.490 for k_c 103 is the one the float64 sign disagrees with. Its size is bracket-limited (between 0 and 0.01 by the brackets; the det-linear estimate is -0.001176). Against the coordinator's prediction 0.491 (bar 0.005): -0.001104, met.
- **The three printed orientations at this D are equal ("- to +"); not interpreted here.**
- **Seconds per point: 3853 to 4567 s** (median 4250), 4 processes at nice 19 (the watcher's renice at 13:40:57 UTC, 4 pids, `i1088a_yield.txt`), beside my k_c 103 D 22.5 lane (its regrid 14:06 to 17:04 on 8 threads, then its scan), the recount and the quest's units: 1-minute load median 14.80, max 25.01, min 11.03 over 433 samples 13:40:40 to 17:17:20 UTC (32 samples above 22, scattered between 14:09 and 16:33, none sustained; `load_alert.out` empty, no alert); peak RSS per process 3.63 to 3.71 GiB (`/usr/bin/time -v`); MemAvailable at least 20.6 GiB; no memory alert.

### Scan predictions scorecard (registered before the run)
| prediction | result |
|---|---|
| every point noise-robust (70%) | right (10 of 10) |
| the repeat on another process bit-identical (85%) | right |
| exactly one robust change in the window (75%) | right |
| the change within 0.005 of 0.491, PRED met (50%); within 0.002 (20%) | right (-0.001104); right |
| above 0.496 (30%); below 0.486 (10%) | WRONG (0.489896); WRONG |
| the step (k_c 103 minus k_c 95 root) positive (65%) | WRONG (-0.001176) |
| the bracket (0.490, 0.495) (25%); (0.495, 0.500) (25%); (0.485, 0.490) (15%) | WRONG; WRONG; right |
| the printed orientation of the k_c 103 root is "- to +" (85%) | right |
| the float64 sign agrees with the hybrid at all evaluations (30%) | WRONG (differs at 0.485 and both 0.490) |
| each scan point 3500 to 6500 s (60%) | right (3853 to 4567 s) |
| the scan done within 5 h of its start (60%) | right (3.62 h) |

### Timeline prediction (the regrid's half is in its scorecard above: WRONG, 3.52 h)
| prediction | result |
|---|---|
| the whole lane (regrid and scan) done within 8 h (60%) | right (7.15 h: 10:08:49 to 17:17:47 UTC) |

## Status
- 2026-11-25 10:07 UTC: folder, inputs (pinned: `in_blobs.txt`, `in_blobs_src.txt`, `source_commit.txt`), lane, watcher and README written before any run; `lane_kc103.sh dry` and the unit `i1025-kc103-22_125` are started next. Beside it: the D 22.375 wide scan (4 processes), the recount `i1076d` (1), the quest's `i1088a-*` units (not mine).
- 2026-11-25 13:42 UTC: the regrid is ACCEPTED (10:09:35 to 13:40:03 UTC, 12628 s; result above). The scan started 13:40:30 UTC on 4 processes, nice 19 by the watcher.
- 2026-11-25 17:20 UTC: scan done (13:40:30 to 17:17:42 UTC). One robust change (0.485, 0.490), "- to +", det-linear 0.489896; k_c 103 minus k_c 95 root -0.001176. Scan result and both scorecards above.
