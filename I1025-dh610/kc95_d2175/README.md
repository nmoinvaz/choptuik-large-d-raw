# I1025-dh610/kc95_d2175: macm3's k_c 87 leg state at D 21.75 regridded to k_c 95, then a hybrid sign scan at lambda_1 0.640 to 0.665

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 62 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-24 17:17 UTC, before any run of this folder (the pins and the pin script's own fetch come first; no regrid, no scan). The k_c 95 roots are not yet physical. A root is identified by position, never by sign orientation (printed as the reader prints it, not compared across D or k_c).

## Order (coordinator t5, hc, 24 Nov, read at 17:14 UTC), verbatim
"Coordinator (t5) to dh610, #1025, a new lane now (your recount is in a serial stretch: load 1.3, 2 python busy): k_c 95 at D 21.75, the 87 -> 95 step where lambda_1 is 0.65, closer to the crossing (k_c steps so far: D 21.0 +0.0018, D 21.125 +0.0039; the 79 -> 87 step fell from 0.0055 at D 21.22 to 0.0038 at 21.375). Raw: I1025-dh610/kc95_d2175/ (README first, prediction before the scan). 1. Source: macm3's k_c 87 leg state at D 21.75 (raw I1025-macm3/kc87_leg2/b/, tag l1kc87Lmacm3b; its root 0.646846 is in kc87_leg_lambda/21.75). Pin by blob; kc87_syscheck accepts it (controls 1 1). 2. Regrid to k_c 95 with ell_refine.py exactly as your kc95_d1975 regrid (same worktree, venv), 8 threads, nice 10, timeout 6 h; acceptance by kc95_syscheck_1025.py (d487e628; controls 1 1, kc87 check refuses). 3. Scan with d18_hybsign.py, 8 processes, nice 10: lambda 0.640, 0.645, ..., 0.665 and a repeat of 0.650. PREDICTION: 0.646846 + 0.003 = 0.6498 (bar 0.005), the root nearest 0.6468 by position. Your kc79 lanes keep priority (nice 5/8); with the recount the nominal peak is 28 threads, as accepted before. Stop on: regrid not accepted, exception, no robust change (report, do not widen), a step over 6 h."

My reading of two details (reported to the coordinator): the grid 0.640 to 0.665 by 0.005 with a repeat of 0.650 is **7 evaluations**, so the scan runs 7 processes of 1 thread (one evaluation each; the repeat on its own process, so it tests another process, which the d1975 scan did not), not 8; "a step over 6 h" is the regrid's `timeout 21600` (exit 124 stops the lane).

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs, `in_blobs_src.txt` the source's; the lane refuses any other blob)
| item | source | blob |
|---|---|---|
| macm3's k_c 87 D 21.75 state (commit 660ad084, 2026-11-24 08:33:10 -08:00 = 16:33:10 UTC) | I1025-macm3/kc87_leg2/b/sol_l1kc87Lmacm3b_D21.750000.npy | f99f513b |
| its record file (rows up to D 21.75: |F| 4.2699503883635535e-10, 2887 steps, psi-constraint 0.005422677724131356, Delta 1.1386389254198963, h 0.0625, 785 s) | same folder, l1kc87Lmacm3b.jsonl at that commit | a4fb1525 |
| my k_c 87 check; the k_c 95 check (the k_c 87 check with 3 lines changed: the k_c test, its message, the selftest's planted record; `kc95_syscheck_1025.diff`) | copies of ../kc95_d1975/in/ | 6df5d960; d487e628 |
| the scanner, xfkappa's, unmodified; its change finder, `d18c_read.py` | I1025-mac/d18/ | e089207a; 7c9d400f, 1383470f |
| reader (dh170's); `repeat_check.py`; `leg_read.py` | I1025-dh170/lower_root/read_lower.py; I1025-dh610/kc71_d19125/in/; I1025-dh610/kc79_leg/in/ | 89309d3c; aaf598a9; 5cae2639 |
Code: worktree `~/Source/choptuik-large-d-1025g` at 48c36355 for the regrid (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_refine.py` blob 631e5801), worktree `~/Source/choptuik-large-d-1025f` at 505d8399 (clean) for the scan, python `~/Source/venv-i1058/bin/python` (3.14.10, multidouble avx2), as in `../kc95_d1975/`. lambda_0(21.75) from `ell_delta.lam0_at` reads **2.1037780803** (the regrid's 7th argument; the lane stops if it reads otherwise). macm3's reading of this state (macOS, `I1025-macm3/kc87_leg_lambda/21.75/`): one robust change, bracket (0.645, 0.650), "- to +" as printed, det-linear 0.646846, range [0.646292, 0.646846]; its float64 sign differed from the hybrid at 0.655.

## Commands (one systemd user unit `i1025-kc95-21_75` under `systemd-inhibit`, `lane_kc95.sh` via `start_kc95.sh`; it stops at the first failure, writes `exits_kc95.txt`, `regrid/steps`, `regrid/VERDICT.txt`)
1. **Pins and selftests**: blobs of `in/`, the rebuilt diff of the two checks (3 changed lines), the worktrees, lambda_0, then the selftests `kc87_syscheck` 0, `kc95_syscheck` 0, `read_lower` 0 with `--mutate=shift` 1 and `--mutate=round2` 1, `repeat_check` 0, `leg_read` 0 with `--mutate` 1 (wanted `0 0 0 1 1 0 0 1`).
2. **Source**: `kc87_syscheck_1025.py` exit 0 on the pinned state and record, `--mutate=F` and `--mutate=steps` exit 1 each, `kc95_syscheck_1025.py` on the k_c 87 source exit 1 (refuses).
3. **Regrid**, in `solver/matter` (cwd), 8 threads, nice 10:

       nice -n 10 timeout 21600 ~/Source/venv-i1058/bin/python -u ell_refine.py l1kc87Lmacm3b 87 l1kc95dh610d2175 95 1 21.75 2.1037780803 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma

   (OMP/OPENBLAS/MKL threads 8; the flags are `../kc95_d1975/`'s; only the source, tag, D and lambda_0 change). Accepted only when `kc95_syscheck_1025.py` exits 0 on the result, `--mutate=F` and `--mutate=steps` exit 1 each, and `kc87_syscheck_1025.py` on the result exits 1 (refuses).
4. **Scan** (after ACCEPTED and a memory gate: it waits, 6 h cap, until MemAvailable is at least 7 x 3.6 GB + 4 GB; nothing is stopped for memory): `d18_hybsign.py in/l1kc95dh610d2175.jsonl in/sol_l1kc95dh610d2175_D21.7500.npy 21.75 <lambda> scan/scan_D21.75_p<j>.jsonl`, p0..p5 lambda 0.640, 0.645, 0.650, 0.655, 0.660, 0.665 and p6 the repeat of 0.650, 7 processes of 1 thread at nice 10, cap 28800 s each; every process must print the record system.
5. **Reading**: `read_lower.py scan 0.640 0.665`, `repeat_check.py` on the merged rows, `leg_read.py read` against the prediction 0.6498 (bar 0.005). No robust change in the window: reported as read, no widening (the order).

## Acceptance (fixed before the run)
Source accepted with controls 1 1 and the k_c 95 check refusing it; the regrid exits 0 inside 21600 s; the result accepted by `kc95_syscheck_1025.py` with both controls exit 1 and refused by the k_c 87 check; every scan process prints the record system and exits 0; the repeat of 0.650 agrees (`repeat_check.py`: sign, ln|det| within 1e-6, noise signs, float64 sign). A control that fires stops the work and I report it; no bar is loosened. Reported: Delta, steps, |F|, constraint of the regridded state beside macm3's k_c 87 record; every robust change by position (bracket, orientation as printed, det-linear, estimator range, a spread over interpolation choices and not an enclosure; the bracket is the grid step 0.005) beside the prediction 0.6498 (bar 0.005) and beside macm3's k_c 87 root 0.646846 (the k_c 87 to 95 step); the edge signs; changes touching a non-robust point (listed, not counted); ln|det| minima without a sign change; the repeat; seconds per point; load, RSS and MemAvailable of both phases.

## Threads and memory (stated before)
The recount (unit i1076d) is 12 nominal threads (2 busy now, a serial stretch, load 1.3). The k_c 79 leg's scans take 8 (nice 5) and the far lane's paired scan of D 21.46875 takes 8 (nice 8, planned for about 19:10 to 19:50 UTC). This lane: the regrid 8 threads (nice 10) now, the scan 7 processes (nice 10) after it. Planned timeline: the regrid beside the leg's D 21.40625 scan (state expected about 17:22 UTC; 12 + 8 + 8 = 28 nominal, the figure accepted before); the scan from about 18:30 beside the leg's D 21.4375 scan (from about 18:39 UTC: 12 + 8 + 7 = 27) and then the far lane's paired scan (about 19:10: 12 + 8 + 7 = 27). The three scans and the recount together (12 + 8 + 8 + 7 = 35 nominal) happen only if a kc79 state arrives early, and the load alert (`../kc79_far/load_alert.sh`, alert only: load above 22 for an hour) watches. Memory: one k_c 95 scan process peaked at 3.14 to 3.33 GB at D 19.75, so 7 processes need about 23 GB beside the kc79 scans' 1.6 to 1.8 GiB each; the gate above waits, never stops.

## Predictions, registered before the runs (mine, information)
- Source accepted with controls 1 1 and the k_c 95 check refusing it: 93%. Regrid exits 0 and is accepted (both controls exit 1, the k_c 87 check refusing): 85%.
- Steps: the 87 to 95 step ratio was 1.0911 (D 19.5) and 1.0919 (D 19.75), so about 3153 steps for macm3's 2887 (within 10: 55%; within 30: 85%). |F| below 1e-9: 95%.
- Delta: the 87 to 95 shift was -2.2397e-6 (D 19.5) and -2.2168e-6 (D 19.75), so Delta about 1.1386367 (within 2e-6 of that: 75%; the shift negative: 85%).
- Regrid wall 2600 to 4800 s (70%; 3066 s at D 19.75 and 4293 s at D 19.5, with the kc79 scan's 8 processes beside it); peak sampled RSS below 3 GiB (85%).
- Scan: every point noise-robust (75%); the repeat on its own process bit-identical (85%); exactly one robust change in 0.640 to 0.665 (80%), none (10%), two or more (10%). The change within 0.005 of 0.6498 (the order's bar: 80%; within 0.003: 55%); above macm3's 0.646846 (the 87 to 95 step positive: 80%); the bracket (0.645, 0.650) (45%), (0.650, 0.655) (40%). The float64 sign agrees with the hybrid at all 7 evaluations (20%). Each scan point 2000 to 3300 s (55%; D 19.75 took 2442 to 2770 s with 4 processes, and the kc79 points slowed 2.4 times with two scans together); one process peak RSS 2.7 to 3.4 GiB (75%).
- Timeline: the regrid done by 18:45 UTC (60%); the scan done within 100 min of its start (65%).

## Regrid result (24 Nov, 17:18:03 to 19:53:52 UTC): ACCEPTED
`ell_refine.py` (8 threads, nice 10, unit `i1025-kc95-21_75`) exited 0 after **9339 s** (the record's own 9337 s; predicted 2600 to 4800 s: no). Mean sampled CPU 737% (154 samples, `regrid/regrid_samples.csv`; D 19.75's regrid: 776%), so the regrid did about 2.9 times the CPU work of D 19.75's (3066 s): the cause is unmeasured (its first evaluation was 8.8 times further from the solution: F_start 2.942e-05 here against 3.337e-06 there; the machine was loaded with two 8-process scans and the recount at nice 5 to 8 over this nice 10 for most of it). Peak sampled RSS 2.84 GiB; 25 numpy RuntimeWarning lines in the log, as in the earlier regrids; no memory alert.
- Record `l1kc95dh610d2175.jsonl` (blob 6bde1c86) and state `sol_l1kc95dh610d2175_D21.7500.npy` (blob ee18ab90, copied to `in/`; `in_blobs_regrid.txt`): k_c 95 at D 21.75, |F| 4.3937655374e-10, F_start 2.942e-05, **3152 steps** (macm3's k_c 87: 2887; ratio 1.0918, predicted about 3153), constraint 3.214e-03 (macm3's k_c 87: 5.4227e-03, ratio 0.593), **Delta 1.1386286581** (macm3's k_c 87: 1.1386389254; shift **-1.0267e-05**, 4.7 times the -2.2e-06 of D 19.5 and D 19.75).
- **Acceptance:** `kc95_syscheck_1025.py` exit 0 (the state's |F| equals the record's, `freeze_from` gives 3152 steps = the record's); `--mutate=F` exit 1, `--mutate=steps` exit 1; `kc87_syscheck_1025.py` on the k_c 95 result exits 1 (refuses). The source check (macm3's state accepted by the k_c 87 check, both controls exit 1, the k_c 95 check refusing it) and the selftests (0 0 0 1 1 0 0 1) are in `exits_kc95.txt` and `regrid/source_*.txt`. Raw `dc5a6edb`.

### Regrid predictions scorecard (registered before the run)
| prediction | result |
|---|---|
| source accepted with controls 1 1, the k_c 95 check refusing it (93%) | right |
| regrid exits 0 and is accepted, k_c 87 check refusing the result (85%) | right |
| steps about 3153 (within 10: 55%; within 30: 85%) | right (3152) |
| \|F\| below 1e-9 (95%) | right (4.39e-10) |
| Delta within 2e-6 of 1.1386367 (75%) | WRONG (1.1386286581, 8.1e-6 below it) |
| the Delta shift negative (85%) | right (-1.0267e-05, but 4.7 times the shift I had assumed) |
| regrid wall 2600 to 4800 s (70%) | WRONG (9339 s) |
| peak sampled RSS below 3 GiB (85%) | right (2.84 GiB) |
| the regrid done by 18:45 UTC (60%) | WRONG (19:53:52 UTC) |

## Scan result (24 Nov, 19:53:56 to 22:39:37 UTC, 165.7 min; `summarize_kc95.py` > `summary_kc95.txt`)
| lambda | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|
| 0.640 | - | -- (True) | + | -2838.8940248435065 | 8219 |
| 0.645 | - | -- (True) | - | -2841.5260114492503 | 8989 |
| 0.650 | + | ++ (True) | + | -2839.946788918143 | 8183 |
| 0.650 | + | ++ (True) | + | -2839.946788918143 | 9925 |
| 0.655 | + | ++ (True) | + | -2839.5934283266092 | 8533 |
| 0.660 | + | ++ (True) | - | -2839.5739700024424 | 7736 |
| 0.665 | + | ++ (True) | + | -2839.6837956179284 | 8440 |

scan points: 7 evaluations, seconds per point min 7736, median 8440, max 9925, sum 60025; outside 2000 to 3300 s: [(0.64, 8219), (0.645, 8989), (0.65, 8183), (0.65, 9925), (0.655, 8533), (0.66, 7736), (0.665, 8440)]
the regridded record at D 21.75: |F| 4.3937655373792033e-10, steps 3152, constraint 0.0032139850093208574, Delta 1.1386286581052725, h None, seconds 9337
float64 sign differs from the hybrid at: [0.64, 0.66]

```
hybrid signs: 0.640- 0.645- 0.650+ 0.655+ 0.660+ 0.665+
robust changes: 1
   change (0.645, 0.650), - to +, det-linear 0.645855, range [0.645557, 0.645855]
against the prediction 0.6498: change minus prediction -0.003945; within 0.005: True
```

- **All 7 processes exit 0 and printed the record system** (|F| 4.3980274601e-10 recomputed against the record's 4.3937655374e-10, steps 3152 = the record's); the pre-run checks passed (`selftest_exits.txt` 0 0 0 1 1 0 0 1; the source check and the regrid's acceptance above). Walls 2:09:04 to 2:45:36 (`scan/scan_p<j>.raw`, `/usr/bin/time -v`).
- **One robust change in the window 0.640 to 0.665:** (0.645, 0.650), "- to +" as the reader prints it, det-linear **0.645855**, estimator range [0.645557, 0.645855] (a spread over interpolation choices, not an enclosure; the bracket is the grid step 0.005). Edge signs differ (- at 0.640, + at 0.665). No ln|det| minimum without a sign change; every point noise-robust. The float64 sign differs from the hybrid at 0.640 (below the change) and 0.660 (above it); the hybrid is read.
- **The repeat of 0.650** (p2 and p6, two processes) is bit-identical (hybrid +, ln|det| -2839.946788918143 in both; `repeat_check.py` PASS).
- **Against the prediction 0.6498 (the coordinator's: macm3's k_c 87 root 0.646846 plus 0.003, bar 0.005):** -0.003945, within the bar (the root nearest 0.6468 by position is the only one in the window). **Beside macm3's k_c 87 root at the same D** (0.646846, bracket (0.645, 0.650), range [0.646292, 0.646846], a macOS scan of macm3's own k_c 87 state, `I1025-macm3/kc87_leg_lambda/21.75/`): the k_c 95 root is **0.000991 below it**, not 0.003 above; the two estimator ranges do not overlap (gap 0.000437). The comparison mixes two things: the k_c step (this state is that one regridded, the Delta shifted by -1.0267e-05) and the build (macOS scan against a Linux scan, two different scanners' windows and grids); a k_c 87 scan of the same state on this machine, which this lane does not do, would separate them.
- **Seconds per point: 7736 to 9925 s** (median 8440): 2.5 to 3 times the 2442 to 2770 s of D 19.75's scan at 4 processes. This scan (7 processes at nice 10) ran beside the k_c 87 chain of `../kc87_m3pts/` (8 processes at nice 8, and from 21:45 UTC at nice 15 by the coordinator's word) and the recount: 15 scan processes on 20 logical CPUs. The load average, median over `scan/sampler.log` (329 samples, 19:54:06 to 22:39:07 UTC), was 16.68 (max 18.72, min 10.53), peak RSS per process 2.32 to 2.53 GiB (`/usr/bin/time -v`), MemAvailable at least 34.58 GiB; no memory alert (no `MEMALERT_scan.txt`), the load alert (alert only) did not fire.

### Scan predictions scorecard (registered before the run)
| prediction | result |
|---|---|
| every point noise-robust (75%) | right (7 of 7) |
| the repeat on its own process bit-identical (85%) | right |
| exactly one robust change in 0.640 to 0.665 (80%) | right |
| the change within 0.005 of 0.6498 (80%); within 0.003 (55%) | right (-0.003945); WRONG |
| above macm3's 0.646846, the 87 to 95 step positive (80%) | WRONG (0.000991 below it) |
| the bracket (0.645, 0.650) (45%); (0.650, 0.655) (40%) | right; WRONG |
| the float64 sign agrees with the hybrid at all 7 evaluations (20%) | WRONG (differs at 0.640 and 0.660) |
| each scan point 2000 to 3300 s (55%) | WRONG (7736 to 9925 s) |
| one process peak RSS 2.7 to 3.4 GiB (75%) | WRONG (2.32 to 2.53 GiB) |
| the scan done within 100 min of its start (65%) | WRONG (165.7 min) |

## Status
- 2026-11-24 17:17 UTC: folder, inputs (pinned: `in_blobs.txt`, `in_blobs_src.txt`, `source_commit.txt`), lane and README written before any run; `lane_kc95.sh dry` (pins and selftests) is run next, then the unit.
- 2026-11-24 19:54 UTC: the regrid is ACCEPTED (17:18:03 to 19:53:52 UTC, 9339 s; result above, raw dc5a6edb). The scan (7 processes, nice 10) started 19:53:56 UTC beside the k_c 87 chain of `../kc87_m3pts/` (8) and the recount.
- 2026-11-24 22:40 UTC: the scan is done (19:53:56 to 22:39:37 UTC): one robust change, bracket (0.645, 0.650), det-linear 0.645855, -0.003945 against 0.6498; result and scorecard above. This lane is finished; the k_c 87 chain of `../kc87_m3pts/` is released from its hold.
