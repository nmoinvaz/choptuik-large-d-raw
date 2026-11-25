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

## Status
- 2026-11-25 14:05 UTC: folder, inputs (pinned: `in_blobs.txt`, `in_blobs_src.txt`, `source_commit.txt`), lane, watcher and README written before any run; `lane_kc103.sh dry` and the unit `i1025-kc103-22_5` are started next. Beside it: my k_c 103 D 22.125 scan (4 processes), the recount `i1076d` (1), the quest's `i1088a-*` units (not mine).
- 2026-11-25 17:05 UTC: regrid ACCEPTED (10669 s, 3390 steps, |F| 3.83e-10, Delta shift -8.24e-06 vs win2's k_c 95); the scan runs on 4 processes since 17:04:26 UTC. Scan result and scorecard are written when the last point is done.
