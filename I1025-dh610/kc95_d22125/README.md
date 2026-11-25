# I1025-dh610/kc95_d22125: macm3's k_c 87 b2 leg state at D 22.125 regridded to k_c 95, then a hybrid sign scan at lambda_1 0.475 to 0.505

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 62 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-25 03:06 UTC, before any run of this folder (the pin of the source state came first; no regrid, no scan). The k_c 95 roots are not yet physical. A root is identified by position; its orientation is printed as the reader prints it and is not interpreted here.

## Order (coordinator t5, hc, read at about 03:00 UTC 25 Nov), verbatim
"Coordinator (t5): next l = 1 lane (#1025), 8 threads, the quest's i1088a units first as before: k_c 95 at D 22.125, then at D 22.1875, from macm3's b2 states (tag l1kc87Lmacm3b2), same procedure as kc95_d2225. Windows: D 22.125 lambda 0.475 to 0.505 by 0.005 plus the repeat of 0.490 (k_c 87: 0.4908, '- to +'); D 22.1875 lambda 0.455 to 0.485 plus the repeat of 0.470 (k_c 87: 0.4735, '+ to -'). Report each root WITH its orientation as printed. The question is where k_c 95's orientation flips relative to k_c 87's near D 22.17 (at D 22.25 k_c 95 reads '- to +' where k_c 87 reads '+ to -'). Raw kc95_d22125/ and kc95_d221875/."

This folder is D 22.125 (the other is `../kc95_d221875/`); the two lanes run one at a time (8 threads), D 22.125 first. The order gives no prediction, so the prediction below (PRED 0.4848 for the reader's "against the prediction" line) is mine, registered before the run. macm3's own reading of this state (`I1025-macm3/kc87_leg_lambda/22.125/read_lower.txt`, macOS): one robust change, bracket (0.490, 0.495), "- to +" as printed, det-linear 0.491017, range [0.490646, 0.491017]; its float64 sign differed from the hybrid at 0.485, 0.500 and 0.505 (the coordinator's order quotes 0.4908, this file reads 0.491017); the file's window is 0.485 to 0.505. Orientations (as printed): macm3's k_c 87 at D 21.75 "- to +", D 22.125 "- to +", D 22.1875 "+ to -", D 22.25 "+ to -"; this lane's k_c 95 at D 21.75 "- to +" and at D 22.25 "- to +".

## Inputs (copies in `in/`; `in_blobs.txt` lists their blobs, `in_blobs_src.txt` the source's; the lane refuses any other blob)
| item | source | blob |
|---|---|---|
| macm3's k_c 87 D 22.125 state (commit 66ced7fd, 2026-11-24 14:40:56 -08:00 = 22:40:56 UTC) | I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.125000.npy | 9ff74e1f |
| its record file (rows up to D 22.125: \|F\| 3.959072914014199e-10, 2869 steps, psi-constraint 0.00679287146739289, Delta 1.1491514059231234, h 0.03125) | same folder, l1kc87Lmacm3b2.jsonl at that commit | f0e1b4e3 |
| the k_c 87 check; the k_c 95 check (3 changed lines, `kc95_syscheck_1025.diff`); the scanner, reader, repeat check, `leg_read.py` | as `../kc95_d2225/in/` | 6df5d960; d487e628; e089207a, 89309d3c, aaf598a9, 5cae2639 |
Code and environment as `../kc95_d2225/` (worktrees `~/Source/choptuik-large-d-1025g` 48c36355 and `-1025f` 505d8399, `~/Source/venv-i1058`). lambda_0(22.125) from `ell_delta.lam0_at` reads **2.1023628304** (the regrid's 7th argument; the lane stops if it reads otherwise).

## Commands (`lane_kc95.sh` in this folder, a copy of `../kc95_d2225/lane_kc95.sh` for this D; unit `i1025-kc95-22_125` via `start_kc95.sh`; `chain_kc95_22.sh` runs this lane and then the other)
1. Pins and selftests (wanted `0 0 0 1 1 0 0 1`), the source check (`kc87_syscheck_1025.py` exit 0, `--mutate=F` and `--mutate=steps` exit 1, `kc95_syscheck_1025.py` on the k_c 87 source exit 1).
2. Regrid in `solver/matter`, 8 threads, nice 10, `timeout 21600`: `ell_refine.py l1kc87Lmacm3b2 87 l1kc95dh610d22125 95 1 22.125 2.1023628304 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`; accepted only when `kc95_syscheck_1025.py` exits 0 on the result, both controls exit 1 and the k_c 87 check refuses it.
3. Scan (after ACCEPTED and a memory gate that waits, never stops): `d18_hybsign.py` at lambda 0.475, 0.480, 0.485, 0.490, 0.495, 0.500, 0.505 and a repeat of 0.490: 8 evaluations on 8 processes of 1 thread at nice 10, or on 4 processes (2 evaluations each: p0 0.475 and 0.490, p1 0.480 and 0.495, p2 0.485 and 0.500, p3 0.505 and the repeat of 0.490) when an i1088a unit is active at the start (the order: its units first); `watch_i1088a.sh` raises this lane's compute processes to nice 19 by exact pid while an i1088a unit is active; nothing is stopped.
4. Reading: `read_lower.py scan 0.475 0.505`, `repeat_check.py`, `leg_read.py read` against 0.4848 (bar 0.005). No robust change: reported as read, no widening.

## Acceptance (fixed before the run)
As `../kc95_d2225/`: the source accepted with controls 1 1 and the k_c 95 check refusing it; the regrid exits 0 inside 21600 s; the result accepted by `kc95_syscheck_1025.py` with both controls exit 1 and refused by the k_c 87 check; every scan process prints the record system and exits 0; the repeat agrees. A control that fires stops the work and I report it; no bar is loosened. Reported: steps, |F|, constraint, Delta of the regridded state beside macm3's k_c 87 record; every robust change by position (bracket, orientation **as printed**, det-linear, estimator range, a spread over interpolation choices and not an enclosure) beside macm3's k_c 87 root and orientation; the k_c step (k_c 95 minus k_c 87 root); seconds per point, load, RSS, MemAvailable; what the watcher did.

## Predictions, registered before the runs (mine, information)
Basis: the k_c step (k_c 95 root minus macm3's k_c 87 root) was +0.0018 at D 21.0 and +0.0039 at D 21.125 (the coordinator's earlier figures), -0.000991 at D 21.75 and -0.008252 at D 22.25 (this lane's `../kc95_d2175/`, `../kc95_d2225/`); a quadratic through the last three points (D 21.125, 21.75, 22.25) gives about -0.0062 at D 22.125 and -0.0072 at D 22.1875, so PRED = macm3's k_c 87 root plus that step (0.4848 and 0.4663). The Delta shift of the regrid was -1.027e-05 (D 21.75) and -2.030e-05 (D 22.25), -2.2e-06 at D 19.5 and 19.75.
- Source accepted with controls 1 1 and the k_c 95 check refusing it: 93%. Regrid exits 0 and is accepted: 85%.
- Steps about 3128 (the 87 to 95 ratio was 1.0903 at D 22.25; macm3's record has 2869): within 10: 60%; within 30: 90%. |F| below 1e-9: 95%.
- Delta shift: by linear interpolation in D between -1.027e-05 and -2.030e-05, -1.78e-05, so Delta about 1.149134 (the shift within 0.5e-5 of that: 60%; negative: 92%).
- Regrid wall 2800 to 4500 s (65%; 3066 s at D 19.75 and 3203 s at D 22.25, 9339 s at D 21.75); peak sampled RSS below 3 GiB (85%).
- Scan: every point noise-robust (75%); the repeat on another process than its original bit-identical (85%); exactly one robust change in the window (80%), none (10%), two or more (10%). The change within 0.005 of 0.4848 (65%); within 0.002 (35%); below macm3's k_c 87 root (85%); the step between -0.009 and -0.003 (60%). The bracket (0.480, 0.485) (45%). The printed orientation of the k_c 95 root is "- to +" (75%; at D 21.75 and D 22.25 it is "- to +" while macm3's k_c 87 reads "- to +" and "+ to -" there). The float64 sign agrees with the hybrid at all evaluations (25%). Each scan point 1800 to 3500 s (60%; the D 22.25 points took 1851 to 2077 s on 4 processes with the quest's build beside them); the scan done within 100 min of its start (65%).
- Timeline: the regrid done within 90 min of the lane's start (65%); the whole lane (regrid and scan) done within 3 h (60%).

## Regrid result (25 Nov, 03:07:15 to 04:34:32 UTC): ACCEPTED
`ell_refine.py` (8 threads, nice 10, raised to nice 19 at 03:07:43 UTC by the watcher because the quest's `i1088a-build2.service` was active) exited 0 after **5222 s** (the record's own 5219 s; predicted 2800 to 4500 s: no). Mean sampled CPU 758% (85 samples, `regrid/regrid_samples.csv`), about 39.6k CPU-seconds against 25.0k at D 22.25 (3203 s, 779%) and 23.8k at D 19.75: the same threads at nice 19 beside the quest's units (and, from 04:19, the two dd jobs) did more CPU time for the same work, which is what two hyperthreads on one core do; I have not measured it separately. Peak sampled RSS 2.55 GiB; 24 numpy RuntimeWarning lines in the log, as in the earlier regrids; no memory alert.
- Record `l1kc95dh610d22125.jsonl` (blob 64ecb047) and state `sol_l1kc95dh610d22125_D22.1250.npy` (blob 06c5082f, copied to `in/`; `in_blobs_regrid.txt`): k_c 95 at D 22.125, |F| 4.0627911135e-10, F_start 4.045e-05, **3132 steps** (macm3's k_c 87: 2869; ratio 1.0917, predicted about 3128), constraint 4.293e-03 (macm3's k_c 87: 6.793e-03, ratio 0.632), **Delta 1.1491338669** (macm3's k_c 87: 1.1491514059; shift **-1.7539e-05**; I predicted -1.78e-05 by interpolation in D, Delta about 1.149134).
- **Acceptance:** `kc95_syscheck_1025.py` exit 0 (the state's |F| equals the record's, `freeze_from` gives 3132 steps = the record's); `--mutate=F` exit 1, `--mutate=steps` exit 1; `kc87_syscheck_1025.py` on the k_c 95 result exits 1 (refuses). The source check and the selftests are in `exits_kc95.txt` and `regrid/source_*.txt`. Raw `ce4fce87`.
- **i1088a:** an i1088a unit was active at 04:34:36 UTC (`i1088a-rls300.service`), so the scan runs on 4 processes (8 evaluations, 2 each: p0 0.475 and 0.490, p1 0.480 and 0.495, p2 0.485 and 0.500, p3 0.505 and the repeat of 0.490), reniced to nice 19 by the watcher.

### Regrid predictions scorecard (registered before the run)
| prediction | result |
|---|---|
| source accepted with controls 1 1, the k_c 95 check refusing it (93%) | right |
| regrid exits 0 and is accepted (85%) | right |
| steps about 3128 (within 10: 60%; within 30: 90%) | right (3132) |
| \|F\| below 1e-9 (95%) | right (4.06e-10) |
| the Delta shift within 0.5e-5 of -1.78e-5 (60%); negative (92%) | right (-1.754e-05); right |
| regrid wall 2800 to 4500 s (65%) | WRONG (5222 s) |
| peak sampled RSS below 3 GiB (85%) | right (2.55 GiB) |
| the regrid done within 90 min of the lane's start (65%) | right (87.3 min) |

## Status
- 2026-11-25 03:06 UTC: folder, inputs (pinned: `in_blobs.txt`, `in_blobs_src.txt`, `source_commit.txt`), lane, watcher and README written before any run; `lane_kc95.sh dry` and the unit `i1025-kc95-chain22` (both lanes in turn) are started next.
- 2026-11-25 04:34 UTC: the regrid is ACCEPTED (03:07:15 to 04:34:32 UTC, 5222 s; result above, raw ce4fce87). The scan started 04:34:36 UTC on 4 processes (an i1088a unit was active), nice 19 by the watcher.
