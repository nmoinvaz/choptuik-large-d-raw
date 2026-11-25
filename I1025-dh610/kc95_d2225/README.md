# I1025-dh610/kc95_d2225: macm3's k_c 87 b2 leg state at D 22.25 regridded to k_c 95, then a hybrid sign scan at lambda_1 0.430 to 0.455

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 62 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-25 01:03 UTC, before any run of this folder (the pin of the source state came first; no regrid, no scan). The k_c 95 roots are not yet physical. A root is identified by position, never by sign orientation (printed as the reader prints it, not compared across D or k_c).

## Order (coordinator t5, hc, read at about 01:00 UTC 25 Nov), verbatim
"Coordinator (t5): good table, thanks. Interim l = 1 task (#1025), 8 threads, beside the recount and leaving 10 threads for the quest's i1088a units when they come: k_c 95 at D 22.25 from macm3's b2 state (raw I1025-macm3/kc87_leg2/b2/, tag l1kc87Lmacm3b2; pin by blob, kc87_syscheck accepts it, controls 1 1). Regrid as your kc95_d2175 (8 threads, nice 10, 6 h cap; kc95_syscheck accepts, controls 1 1, the kc87 check refuses), then scan with 7 procs: lambda 0.430 to 0.455 by 0.005 plus the repeat of 0.440. PREDICTION: macm3's k_c 87 root 0.442516 minus 0.001 = 0.4415 (bar 0.005; D 21.75's step was -0.000991). Raw I1025-dh610/kc95_d2225/, README first. If an i1088a unit starts, let it have its threads first and drop your scan to 4 processes."

The folder is named `kc95_d2225` for D 22.25 (the order's name). The "drop to 4 processes" is read two ways, both built in: if an i1088a unit is active when the scan starts, it runs 4 processes (7 evaluations: p0 0.430 and 0.450, p1 0.435 and 0.455, p2 0.440, p3 0.445 and the repeat of 0.440, so the repeat is still on another process than its original); and while any i1088a unit is active, `watch_i1088a.sh` raises the nice value of this lane's own compute processes (the regrid's python, the scan's python) to 19 by exact pid, once per process, so the unit has its threads first (a running scan process cannot be cut to fewer processes without stopping it, and nothing is stopped). No i1088a unit is active at the time of writing.

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs, `in_blobs_src.txt` the source's; the lane refuses any other blob)
| item | source | blob |
|---|---|---|
| macm3's k_c 87 D 22.25 state (commit 36f4ffb9, 2026-11-24 16:11:40 -08:00 = 2026-11-25 00:11:40 UTC) | I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.250000.npy | 7caefe44 |
| its record file (rows up to D 22.25: \|F\| 3.8935427096813245e-10, 2869 steps, psi-constraint 0.00728177509841303, Delta 1.1526894087302582, h 0.03125, 1115 s) | same folder, l1kc87Lmacm3b2.jsonl at that commit | 40b37619 |
| the k_c 87 check; the k_c 95 check (3 changed lines, `kc95_syscheck_1025.diff`) | copies of ../kc95_d2175/in/ | 6df5d960; d487e628 |
| the scanner, xfkappa's, unmodified; its change finder `d18c_read.py` | I1025-mac/d18/ | e089207a; 7c9d400f, 1383470f |
| reader; `repeat_check.py`; `leg_read.py` | as ../kc95_d2175/in/ | 89309d3c; aaf598a9; 5cae2639 |
Code and environment as `../kc95_d2175/` (worktree `~/Source/choptuik-large-d-1025g` at 48c36355 for the regrid, `~/Source/choptuik-large-d-1025f` at 505d8399 for the scan, `~/Source/venv-i1058` 3.14.10). lambda_0(22.25) from `ell_delta.lam0_at` reads **2.1019003706** (the regrid's 7th argument; the lane stops if it reads otherwise). macm3's reading of this state (macOS, `I1025-macm3/kc87_leg_lambda/22.25/`): one robust change, bracket (0.440, 0.445), "+ to -" as printed, det-linear 0.442516, range [0.441911, 0.442516]; its float64 sign differed from the hybrid at 0.440. macm3's state is at h 0.03125 (the D 21.75 one was at h 0.0625).

## Commands (unit `i1025-kc95-22_25`, `lane_kc95.sh` via `start_kc95.sh`, a copy of `../kc95_d2175/lane_kc95.sh` for this D; it stops at the first failure and writes `exits_kc95.txt`, `regrid/VERDICT.txt`)
1. Pins and selftests (wanted `0 0 0 1 1 0 0 1`), then the source check: `kc87_syscheck_1025.py` exit 0 on the pinned state and record, `--mutate=F` and `--mutate=steps` exit 1, `kc95_syscheck_1025.py` on the k_c 87 source exit 1.
2. Regrid, in `solver/matter`, 8 threads, nice 10: `nice -n 10 timeout 21600 python -u ell_refine.py l1kc87Lmacm3b2 87 l1kc95dh610d2225 95 1 22.25 2.1019003706 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`. Accepted only when `kc95_syscheck_1025.py` exits 0 on the result, both controls exit 1, and `kc87_syscheck_1025.py` on the result exits 1.
3. Scan (after ACCEPTED and a memory gate: it waits, 6 h cap, for NP x 3.6 GB + 4 GB available; nothing is stopped for memory): `d18_hybsign.py` p0..p5 lambda 0.430, 0.435, 0.440, 0.445, 0.450, 0.455 and p6 the repeat of 0.440, 7 processes of 1 thread at nice 10 (4 when an i1088a unit is active at the start); every process must print the record system.
4. Reading: `read_lower.py scan 0.430 0.455`, `repeat_check.py`, `leg_read.py read` against 0.4415 (bar 0.005). No robust change: reported as read, no widening.

## Acceptance (fixed before the run)
As `../kc95_d2175/`: the source accepted with controls 1 1 and the k_c 95 check refusing it; the regrid exits 0 inside 21600 s; the result accepted by `kc95_syscheck_1025.py` with both controls exit 1 and refused by the k_c 87 check; every scan process prints the record system and exits 0; the repeat of 0.440 agrees. A control that fires stops the work and I report it; no bar is loosened. Reported: steps, |F|, constraint, Delta of the regridded state beside macm3's k_c 87 record; every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside 0.4415 (bar 0.005) and beside macm3's k_c 87 root 0.442516 (the k_c step, which D 21.75 showed is not a build effect); edge signs; seconds per point, load, RSS, MemAvailable; whether an i1088a unit ran and what the watcher did.

## Threads and memory (stated before)
The coordinator's count: the recount 2 busy threads, this lane 8, the quest's i1088a units up to 10: 20 logical CPUs (the recount's nominal 12 against the 20 is the earlier count; the busy 2 is what runs). The regrid takes 8 threads at nice 10 for about 2 to 3.5 h, then the scan 7 processes (or 4). One k_c 95 scan process peaked at 2.3 to 2.5 GiB at D 21.75, the regrid at 2.84 GiB; MemAvailable is 46 to 58 GB now.

## Predictions, registered before the runs (mine, information)
- Source accepted with controls 1 1 and the k_c 95 check refusing it: 93%. Regrid exits 0 and is accepted (both controls exit 1, the k_c 87 check refusing): 85%.
- Steps: the 87 to 95 ratio was 1.0911 (D 19.5), 1.0919 (D 19.75) and 1.0918 (D 21.75), so about 3133 steps for macm3's 2869 (within 10: 50%; within 30: 85%). |F| below 1e-9: 95%.
- Delta: the shift was -2.24e-6 (D 19.5), -2.22e-6 (D 19.75) and -1.027e-5 (D 21.75); extrapolated in D (a factor 4.6 over two units of D) it is about -1.5e-5 at D 22.25, so Delta about 1.152674 (the shift between -0.75e-5 and -3.0e-5: 60%; negative: 90%).
- Regrid wall 6000 to 12000 s (65%; 3066 s at D 19.75, 9339 s at D 21.75 at a mean of 737% CPU, which is about all 8 threads, so the load beside it was not the main cost; the machine is quieter now); peak sampled RSS below 3 GiB (85%).
- Scan: every point noise-robust (75%); the repeat on its own process bit-identical (85%); exactly one robust change in 0.430 to 0.455 (80%), none (10%), two or more (10%). The change within 0.005 of 0.4415 (85%); within 0.002 (60%); below macm3's 0.442516 (the step negative as at D 21.75: 80%); the step between -0.003 and 0 (70%). The bracket (0.440, 0.445) (65%), (0.435, 0.440) (25%). The float64 sign agrees with the hybrid at all evaluations (20%). Each scan point 3000 to 5500 s (55%; 7 to 8 procs of the kc95 scan took 7736 to 9925 s at D 21.75 beside another 8-process scan, and 2442 to 2770 s at D 19.75 on 4 processes; this one has the recount only, unless an i1088a unit runs); the scan done within 100 min of its start (60%).
- Timeline: the regrid done by 04:30 UTC (60%).

## Regrid result (25 Nov, 01:04:11 to 01:57:42 UTC): ACCEPTED
`ell_refine.py` (8 threads, nice 10, unit `i1025-kc95-22_25`) exited 0 after **3203 s** (the record's own 3203 s; predicted 6000 to 12000 s: no, it was faster). Mean sampled CPU 779% (52 samples, `regrid/regrid_samples.csv`), so it did about 25.0k CPU-seconds, the work of D 19.75's regrid (23.8k) and 0.36 of D 21.75's (68.8k): the 2.9 times of D 21.75 was not a trend in D, and its cause is still unmeasured. Peak sampled RSS 2.55 GiB; 22 numpy RuntimeWarning lines in the log, as in the earlier regrids; no memory alert.
- Record `l1kc95dh610d2225.jsonl` (blob e83e529e) and state `sol_l1kc95dh610d2225_D22.2500.npy` (blob d709a8c0, copied to `in/`; `in_blobs_regrid.txt`): k_c 95 at D 22.25, |F| 3.9737761418e-10, F_start 4.491e-05, **3128 steps** (macm3's k_c 87: 2869; ratio 1.0903, predicted about 3133), constraint 4.701e-03 (macm3's k_c 87: 7.282e-03, ratio 0.646), **Delta 1.1526691088** (macm3's k_c 87: 1.1526894087; shift **-2.030e-05**, 1.98 times the -1.027e-05 of D 21.75).
- **Acceptance:** `kc95_syscheck_1025.py` exit 0 (the state's |F| equals the record's, `freeze_from` gives 3128 steps = the record's); `--mutate=F` exit 1, `--mutate=steps` exit 1; `kc87_syscheck_1025.py` on the k_c 95 result exits 1 (refuses). The source check (macm3's state accepted by the k_c 87 check, both controls exit 1, the k_c 95 check refusing it) and the selftests (0 0 0 1 1 0 0 1) are in `exits_kc95.txt` and `regrid/source_*.txt`. Raw `bf976140`.
- **i1088a:** at the end of the regrid (01:57:46 UTC) the quest's unit `i1088a-build.service` (a build, `nice -n 10 timeout 3h ./build1088.sh`) was active, so by the coordinator's order the scan runs on 4 processes, and `watch_i1088a.sh` raised the 4 scan processes (pids 1859525, 1859528, 1859529, 1859530) to nice 19 at 01:58:10 UTC (`i1088a_yield.txt`); nothing was stopped.

### Regrid predictions scorecard (registered before the run)
| prediction | result |
|---|---|
| source accepted with controls 1 1, the k_c 95 check refusing it (93%) | right |
| regrid exits 0 and is accepted, k_c 87 check refusing the result (85%) | right |
| steps about 3133 (within 10: 50%; within 30: 85%) | right (3128) |
| \|F\| below 1e-9 (95%) | right (3.97e-10) |
| the Delta shift between -0.75e-5 and -3.0e-5 (60%); negative (90%) | right (-2.030e-05); right |
| regrid wall 6000 to 12000 s (65%) | WRONG (3203 s) |
| peak sampled RSS below 3 GiB (85%) | right (2.55 GiB) |
| the regrid done by 04:30 UTC (60%) | right (01:57:42 UTC) |

## Scan result (25 Nov, 01:57:46 to 03:03:37 UTC, 65.8 min, 4 processes; `summarize_kc95.py` > `summary_kc95.txt`)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.430 | - | -- (True) | - | -2760.0570242926374 | 2077 |
| 0.435 | + | ++ (True) | + | -2761.8133440277534 | 2074 |
| 0.440 | + | ++ (True) | + | -2760.499586019766 | 1868 |
| 0.440 | + | ++ (True) | + | -2760.499586019766 | 2069 |
| 0.445 | + | ++ (True) | + | -2760.3324960498508 | 2075 |
| 0.450 | + | ++ (True) | + | -2760.3943135265367 | 1862 |
| 0.455 | + | ++ (True) | + | -2760.55813497985 | 1851 |

scan points: 7 evaluations, seconds per point min 1851, median 2069, max 2077, sum 13876; outside 3000 to 5500 s: [(0.43, 2077), (0.435, 2074), (0.44, 1868), (0.44, 2069), (0.445, 2075), (0.45, 1862), (0.455, 1851)]
the regridded record at D 22.25: |F| 3.9737761418304846e-10, steps 3128, constraint 0.004701325487496441, Delta 1.1526691087985546, h None, seconds 3203
float64 sign differs from the hybrid at: []

```
hybrid signs: 0.430- 0.435+ 0.440+ 0.445+ 0.450+ 0.455+
robust changes: 1
   change (0.430, 0.435), - to +, det-linear 0.434264, range [0.434029, 0.434264]
against the prediction 0.4415: change minus prediction -0.007236; within 0.005: False
```

- **All 4 processes exit 0 and printed the record system** (|F| 3.9770752180e-10 recomputed against the record's 3.9737761418e-10, steps 3128 = the record's); the pre-run checks passed (`selftest_exits.txt` 0 0 0 1 1 0 0 1). The scan ran on 4 processes (p0 0.430 and 0.450, p1 0.435 and 0.455, p2 0.440, p3 0.445 and the repeat of 0.440) because the quest's `i1088a-build.service` was active at the start; `watch_i1088a.sh` raised the 4 processes to nice 19 at 01:58:10 UTC (`i1088a_yield.txt`, 5 lines: a second build unit appeared later); walls 1:05:27, 1:05:42, 1:05:46 and 34:32.
- **One robust change in the window 0.430 to 0.455:** (0.430, 0.435), **"- to +" as the reader prints it**, det-linear **0.434264**, estimator range [0.434029, 0.434264] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). The change sits in the lowest grid interval of the window: one point (0.430) lies below it. Edge signs differ (- at 0.430, + at 0.455). No ln|det| minimum without a sign change; every point noise-robust; the float64 sign agrees with the hybrid at all 7 evaluations.
- **The repeat of 0.440** (p2 and p3, two processes) is bit-identical (hybrid +, ln|det| -2760.499586019766 in both; `repeat_check.py` PASS).
- **Against the prediction 0.4415 (the coordinator's: macm3's k_c 87 root 0.442516 minus 0.001, bar 0.005):** -0.007236, **outside the bar** (the order has no widening; the change is in the window). **Beside macm3's k_c 87 root at the same D** (0.442516, bracket (0.440, 0.445), range [0.441911, 0.442516], orientation printed "+ to -", a macOS scan of its own state): the k_c 95 root is **0.008252 below it** (D 21.75: 0.000991 below; D 21.75 showed the builds agree, so this is the k_c step), and its printed orientation is "- to +", where macm3's k_c 87 prints "+ to -" at this D (at D 21.75 both print "- to +"). The orientations are listed as the reader prints them and are not interpreted here (the coordinator's question about where they flip is asked in the next lanes, `../kc95_d22125/` and `../kc95_d221875/`).
- **Seconds per point: 1851 to 2077 s** (median 2069), the machine quiet beside the recount and the quest's build (load median 6.28, max 10.8, min 5.04 over 131 samples 01:57:56 to 03:03:05 UTC), peak RSS per process 2.49 to 3.05 GiB (`/usr/bin/time -v`), MemAvailable at least 27.13 GiB (the build holds about 22 GB); no memory alert.

### Scan predictions scorecard (registered before the run)
| prediction | result |
|---|---|
| every point noise-robust (75%) | right (7 of 7) |
| the repeat on its own process bit-identical (85%) | right |
| exactly one robust change in 0.430 to 0.455 (80%) | right |
| the change within 0.005 of 0.4415 (85%); within 0.002 (60%) | WRONG (-0.007236); WRONG |
| below macm3's 0.442516, the step negative (80%) | right (-0.008252) |
| the step between -0.003 and 0 (70%) | WRONG (-0.008252) |
| the bracket (0.440, 0.445) (65%); (0.435, 0.440) (25%) | WRONG; WRONG (it is (0.430, 0.435)) |
| the float64 sign agrees with the hybrid at all evaluations (20%) | right (agrees at all 7) |
| each scan point 3000 to 5500 s (55%) | WRONG (1851 to 2077 s) |
| the scan done within 100 min of its start (60%) | right (65.8 min) |

## Status
- 2026-11-25 01:03 UTC: folder, inputs (pinned: `in_blobs.txt`, `in_blobs_src.txt`, `source_commit.txt`), lane, watcher and README written before any run; `lane_kc95.sh dry` is run next, then the unit and the watcher.
- 2026-11-25 01:58 UTC: the regrid is ACCEPTED (01:04:11 to 01:57:42 UTC, 3203 s; result above, raw bf976140). An i1088a unit was active: the scan started 01:57:46 UTC on 4 processes (nice 10, reniced to 19 by the watcher at 01:58:10 UTC).
- 2026-11-25 03:04 UTC: the scan is done (01:57:46 to 03:03:37 UTC): one robust change, bracket (0.430, 0.435) printed "- to +", det-linear 0.434264, -0.007236 against 0.4415 (outside the bar), 0.008252 below macm3's k_c 87 0.442516; result and scorecard above. This lane is finished.
