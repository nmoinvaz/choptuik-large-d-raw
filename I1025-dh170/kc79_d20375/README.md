# I1025-dh170/kc79_d20375: #1025 k_c 79 at D 20.375 on Linux, regridded from leg 3's k_c 71 state; the roots in lambda 1.08 to 1.24

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 13:46:24 UTC, before any run of this folder. Raw origin/main when the inputs were taken: 249571b8.

## Order (the coordinator t5's hc, 23 Nov, after the D 20.5 result at raw 249571b8), quoted in part
"D 20.5 final accepted as read (raw 249571b8): one change at 1.087574, none in 1.09-1.24. Next, your recommendation (1), #1025: k_c 79 at D 20.375 on Linux from leg 3's k_c 71 D 20.375 state (raw I1025-win2/kc71_leap/states/, blob 90817a16, record file at c4c93318), as at D 20.5: kc71_syscheck on the source (controls exit 1); lam0 = lam0_at(20.375) in the README; ell_refine.py l1kc71Lw1025c 71 l1kc79dh170d20375 79 1 20.375 <lam0> --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (8 threads, nice 10); accept by kc79_syscheck (selftest 0, both controls exit 1). Then d18_hybsign at 1.08-1.24 by 0.02 plus a repeat of 1.16 (10 evals, 4 procs), read_lower. Written before (README): one robust change within 0.01 of 1.126 (midway on the line between 1.1653 at D 20.25 and 1.0876 at D 20.5); whether the D 20.25 discretization root (1.2035 at k_c 79) shows here is information. Raw I1025-dh170/kc79_d20375/, README first. Memory alerts only."
Roots are read by position, never by sign orientation (t5): "the root near lambda_1's line", "the rising root". lambda_0(20.375) = **2.1093568559** (`ell_delta.lam0_at(20.375, *ell_delta.lam0_table())[0]`, printed by the driver and checked against this number before the regrid).

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs and both drivers refuse any other blob)
| item | raw path | blob |
|---|---|---|
| leg 3's k_c 71 D 20.375 state (source), as named by t5 | I1025-win2/kc71_leap/states/sol_l1kc71Lw1025c_D20.375000.npy, commit c4c93318 | 90817a16 |
| its record file at commit c4c93318 ("leg 3 state D 20.375"): 6 rows, D 20.0625 to 20.375 (t5's "c4c93318" is that commit; the file's blob there is 123253fc) | I1025-win2/kc71_leap/states/l1kc71Lw1025c.jsonl, commit c4c93318 | 123253fc |
| the source check; the result check (the blobs of kc79_d20 and kc79_d205) | I1025-win2/kc71_leap/kc71_syscheck.py; I1025-win/kc79_d19/kc79_syscheck_1025.py | 4cd86cd4; 29dce7ea |
| the scanner, unmodified; its change finder | I1025-mac/d18/d18_hybsign.py; d185_scan_read.py | e089207a; 7c9d400f |
| reader (mine); `repeat_check.py` (dh610's) | I1025-dh170/lower_root/read_lower.py; I1025-dh610/kc71_d19125/in/repeat_check.py | 89309d3c; aaf598a9 |
| for the predictions: leg 3's record at commit 50ace0e9 (the D 20.5 row); my k_c 79 records at D 20 and D 20.5 (raw a6671e16 and 249571b8); the k_c 71 D 20 source row | I1025-win2/kc71_leap/states/l1kc71Lw1025c.jsonl; I1025-dh170/kc79_d20/l1kc79dh170d20.jsonl; I1025-dh170/kc79_d205/l1kc79dh170d205.jsonl; I1025-win2/kc79_d20/rec_k71_D20.0000.jsonl | e44df695; de8aa11b; 5406e21c; 3d22b88f |
Code: the worktree of `../kc79_d20` and `../kc79_d205`, unchanged: `~/Source/choptuik-large-d-1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_refine.py` 631e5801, `ell_delta.py` fde699f5), python `~/Source/choptuik-large-d-1058b/.venv` (3.14.10, multidouble 5.1.0, avx2). The source state is copied into the worktree's `solver/matter/data/` as `sol_l1kc71Lw1025c_D20.3750.npy` (blob checked). The drivers are `run_regrid.sh` and `run_scan.sh`, the kc79_d205 drivers with the tag, D, lambda_0, blobs and the lambda lists changed (`diff ../kc79_d205/run_regrid.sh run_regrid.sh`).

## Reference numbers (information, not a pass rule)
- **The source row, D 20.375** (record file above): |F| 4.8426726409e-10, 2469 steps, psi-constraint 4.8083996e-3, Delta 1.101837227594, F at the start 4.3592862e-5, h 0.0625, kappa 0.7, u0 0.04, Ks 30.
- **The same step at D 20 and D 20.5** (my regrids; ratios k_c 79 over the k_c 71 source): D 20: |F| 0.97339, steps 1.11376, constraint 0.57354, Delta k_c 79 minus source -9.8569e-6, wall 2389 s. D 20.5: |F| 0.96188, steps 1.11333, constraint 0.61743, Delta -2.2442e-5, wall 3112 s. Interpolated linearly in D to 20.375: |F| ratio 0.96476 (4.6720e-10), steps ratio 1.11344 (2749), constraint ratio 0.60646 (2.9161e-3), Delta minus source -1.9296e-5 (1.101817932), wall 2931 s.
- **The scans** (k_c 79, hybrid signs as printed): D 20 (kc79_d20, lambda 1.20 to 1.30): minus to 1.24, plus from 1.25, one change (1.24, 1.25), det-linear 1.246581 (Linux), 1.248340 (Windows). D 20.5 (kc79_d205, 1.00 to 1.24 by 0.03): minus at 1.00 to 1.06, plus at 1.09 to 1.24; one change (1.06, 1.09), det-linear 1.087574; none in 1.09 to 1.24.
- **D 20.25, k_c 79** (t5's comment 7098310980; I did not run it): two roots 1.165140 and 1.203492; t5 now calls the second "the D 20.25 discretization root". The first, continued linearly to D 20.5, is 1.087574 (found), midway 1.126 at D 20.375. The second, at -0.18 per unit D, would sit near 1.18 at D 20.375 (and near 1.16 at D 20.5, where none was found).

## Commands (systemd user units, so no terminal owns them)
**Regrid** (`run_regrid.sh`, unit `i1025-k79d20375r` under `systemd-inhibit`, 8 threads, nice 10; stops at the first failure; writes `steps.txt` and `VERDICT.txt`): in `solver/matter`,

    nice -n 10 timeout 21600 env OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8 ~/Source/choptuik-large-d-1058b/.venv/bin/python -u ell_refine.py \
      l1kc71Lw1025c 71 l1kc79dh170d20375 79 1 20.375 2.1093568559 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma

preceded by the pins, the worktree checks, the lambda_0 check, the two selftests and the source check.
**Scan** (`run_scan.sh`, unit `i1025-k79d20375s`, after VERDICT ACCEPTED): 4 processes of 1 thread at nice 10, `d18_hybsign.py` on the accepted state at D 20.375; lambda 1.08, 1.10, ..., 1.24 (9 values) and a repeat of 1.16 (10 evaluations): p0 1.08,1.16,1.24; p1 1.10,1.18 and the repeat 1.16 (on another process than the first 1.16); p2 1.12,1.20; p3 1.14,1.22. Three rounds, the third with two processes. Then `read_lower.py in/... scan 1.08 1.24`, its selftest and both mutations, and `repeat_check.py`.

## Acceptance (the order's, fixed before the run)
1. **Step 1, source.** `kc71_syscheck.py` accepts leg 3's k_c 71 D 20.375 state and record on this machine (|F| at most 1e-9, `freeze_from` gives 2469, |F| within 1%), both controls (`--mutate=F`, `--mutate=steps`) exit 1, and the k_c 79 check refuses the source (exit 1); both selftests exit 0. Otherwise no regrid.
2. **Step 2, regrid.** `ell_refine.py` exits 0 (the cap 21600 s is a stop); `kc79_syscheck_1025.py` accepts the result (k_c 79 at D 20.375, |F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%), both controls exit 1.
3. **Step 3, scan.** Each process prints the record system; `read_lower.py` selftest exit 0, mutations `shift` and `round2` exit 1; the repeat of 1.16 agrees (sign, ln|det| within 1e-6, noise signs, float64 sign). A stop at any step: I report and change nothing.

## Reading, fixed now (by position)
Every robust change (both neighbouring points noise-robust) with bracket, det-linear estimate and estimator range (the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure), orientation as printed (information); the edge signs; changes touching a non-robust point listed and not counted; every ln|det| minimum without a sign change flagged; the repeat's bits. On a grid of 0.02 a det-linear estimate is good to about the bracket (0.02), so "within 0.01 of 1.126" is read from the det-linear estimate lying in [1.116, 1.136], and the bracket is quoted beside it; the bracket (1.12, 1.14) is the one that contains 1.126. Parity: with two robust changes the two edge signs (1.08 and 1.24) are equal; unequal edge signs mean an odd number of changes, or one outside the window. Report: Delta, |F|, steps and psi-constraint of the regrid beside the interpolated numbers above; every root by position beside t5's 1.126 and the D 20.25 root's continuation (near 1.18).
**Written before the run (t5's):** one robust change within 0.01 of 1.126; whether the D 20.25 discretization root (1.2035 at k_c 79) shows here is information.

## Predictions, registered before the runs (mine, information)
- the source check passes with all four controls firing about 95%; the regrid exits 0 and is accepted with both controls firing about 85%; the regrid takes 2400 to 3400 s about 70% (interpolated 2931 s);
- steps between 2650 and 2850 about 65% (interpolated 2749); |F| within 5% of 4.6720e-10 about 80%; psi-constraint within 10% of 2.9161e-3 about 70%; Delta minus the source between -2.3e-5 and -1.4e-5 about 65% (interpolated -1.9296e-5);
- the scan: every point noise-robust about 70%; the repeat of 1.16 bit-identical about 90%; exactly one robust change in (1.08, 1.24) about 62%, two about 28%, none about 3%, three or more about 7%; given one change, its bracket is (1.12, 1.14) about 65%, and its det-linear estimate lies within 0.01 of 1.126 about 40%; a second change (the continuation of the D 20.25 root near 1.18) about 28%;
- the edge signs unequal about 62%; the float64 sign differs from the hybrid at more than half the points about 20%; the scan 1.9 to 2.4 h (two rounds of about 3200 s side by side and a third of about 1200 s with two processes) about 70%; peak RSS of a scan process below 3 GiB about 85%.

## Budget
The regrid: 8 threads at nice 10 (all of this machine). The scan: 4 processes of 1 thread at nice 10. Nothing else of mine runs. Memory: alert only (`alert.log` if MemAvailable falls below 2048 MiB; nothing is stopped for memory). Estimate: regrid about 50 min, scan about 2.1 h.

## Log
- 2026-11-23 13:46:24 UTC: folder, inputs, drivers and the reading prepared before any run. Selftests: `read_lower.py` exit 0, `shift` and `round2` exit 1, `repeat_check.py`, `kc79_syscheck_1025.py` and `kc71_syscheck.py` exit 0 (`selftest_exits_pre.txt`; the drivers run them again). Dry run of `run_regrid.sh`: the pins, the worktree checks and lambda_0(20.375) = 2.1093568559 pass (`dry_steps_regrid.txt`). The scan's lambda list was checked by a script: 10 evaluations, 1.16 twice on two processes.
- 2026-11-23 13:46:35 to 13:46:41 UTC: `run_regrid.sh` started as unit `i1025-k79d20375r`; **STEP 1** source check ACCEPTED at 13:46:41: leg 3's k_c 71 D 20.375 record |F| 4.8426726409e-10, 2469 steps, constraint 4.808e-3, Delta 1.101837227594 (3970 s on win2); this machine's state |F| 4.8425580358e-10 (-0.002% against the record, inside the 1% bar), `freeze_from` 2469 steps; `--mutate=F` and `--mutate=steps` exit 1; the k_c 79 check refuses the source (exit 1: "the record is not k_c 79 at D 20.375"); both selftests exit 0; lambda_0(20.375) recomputed 2.1093568559. The regrid started 13:46:41.
- 2026-11-23 13:46:41 to 14:38:14 UTC: **STEP 2 regrid** (`ell_refine.py`, 8 threads, nice 10, unit `i1025-k79d20375r`): exit 0, wall **3093 s** (the record's step 3091 s; interpolated 2931 s), peak RSS of `ell_refine` sampled 1.80 GiB (51 samples, one per 60 s), lowest MemAvailable 26.1 GiB, no memory alert. 14:38:18 **ACCEPTED**: `kc79_syscheck_1025.py` exit 0 (|F| in the record class, `freeze_from` 2746 steps = the record's), `--mutate=F` and `--mutate=steps` exit 1. State `sol_l1kc79dh170d20375_D20.3750.npy` blob 4ce09236, record `l1kc79dh170d20375.jsonl` blob bc2ece17.
- **The regrid beside the k_c 71 source and the interpolated numbers:** |F| **4.6591280965e-10** (source 4.8426726409e-10, ratio 0.96210; interpolated 4.6720e-10, -0.28%); steps **2746** (source 2469, ratio 1.1122; interpolated 2749); psi-constraint **2.9230109e-3** (source 4.8083996e-3, ratio 0.60790; interpolated 2.9161e-3, +0.24%); Delta **1.101818198689** (source 1.101837227594: k_c 79 minus the source **-1.9029e-5**; interpolated -1.9296e-5); F at the start 4.3324038e-5.
- 2026-11-23 14:38:30 UTC: **STEP 3 scan** started as unit `i1025-k79d20375s` (4 processes of 1 thread, nice 10, 10 evaluations); all four print the record system (|F| 4.6629294641e-10 against the record's 4.6591280965e-10, 2746 steps equal).
- 2026-11-23 14:39:22 UTC: step 2 logged (this entry).

## Result (written 2026-11-23 16:47:27 UTC)
Steps 1 and 2 as logged (ACCEPTED 13:46:41 and 14:38:18 UTC). **Step 3:** unit `i1025-k79d20375s` exit 0; processes p2, p3, p1, p0 exit 0 at 16:25:53, 16:26:29, 16:46:23 and 16:46:47 UTC; all four printed the record system (|F| 4.6629294641e-10 against the record's 4.6591280965e-10, 2746 steps equal); **10 of 10 evaluations noise-robust**; the repeat of 1.16 (the first on p0, the repeat last on p1) **bit-identical** (hybrid -1, ln|det| -2408.882104108996, float64 ln|det| -2409.1165637209997, noise [-1, -1]; `repeat_check.py` PASS); `read_lower.py` selftest exit 0, `--mutate=shift` and `--mutate=round2` exit 1; reader exit 0 (`read_lower.txt`). Seconds per point 3175 to 3310 in rounds 1 and 2 (four processes side by side) and 1209 and 1217 in round 3 (two processes); wall per process 1:47:23 to 2:08:17 by /usr/bin/time, the scan 2:08:18 (7698 s; 14:38:30 to 16:46:48); peak RSS 2.08 to 2.22 GiB; lowest MemAvailable 22.4 GiB (scan, 128 samples) and 26.1 GiB (regrid); no memory alert (`alert.log` does not exist).

**Hybrid signs, as printed, lambda 1.08 to 1.24: plus at 1.08, 1.10, 1.12; minus at 1.14, 1.16, 1.18, 1.20, 1.22, 1.24; edge signs plus and minus.** One robust change, none touching a non-robust point:
| position | bracket | orientation as printed | det-linear estimate | estimator range |
|---|---|---|---|---|
| **the change near 1.126, k_c 79, D 20.375, dh170 (Linux)** | (1.12, 1.14) | + to - | **1.122673** (0.0033 below 1.126) | [1.120276, 1.122673] |
The estimator range is the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure; on a grid of 0.02 the estimate is good to about the bracket. **There is no second change in 1.14 to 1.24**: the sign is minus at six consecutive points, and no ln|det| minimum without a sign change was found. ln|det|: 1.08 -2402.8497, 1.10 -2405.0145, 1.12 -2409.9575, 1.14 -2408.0886, 1.16 -2408.8821, 1.18 -2409.9585, 1.20 -2411.1259, 1.22 -2412.3219, 1.24 -2413.5285; the differences per 0.02 from 1.14 on are -0.7936, -1.0764, -1.1674, -1.1960, -1.2066 (no dip). The float64 sign differs from the hybrid at 1.12 only (float64 -, hybrid +; ln|det| -2406.9296 against -2409.9575). Parity: the edge signs are unequal, an odd number of changes in the window, which one change satisfies.
**The track of this root by position (k_c 79):** 1.165140 at D 20.25 (t5's), **1.122673** at D 20.375, 1.087574 at D 20.5 (kc79_d205): -0.3397 per unit D from D 20.25 to 20.375 and -0.2808 from D 20.375 to 20.5. The printed orientation is + to - at D 20.375 and - to + at D 20.5; it is information only (the roots are named by position). **The D 20.25 root at 1.2035** (t5: "discretization root", information): it does not show in 1.14 to 1.24 at D 20.375 (continued at -0.18 per unit D it would sit near 1.18) nor in 1.09 to 1.24 at D 20.5. **What the scan does not show:** a pair of changes closer together than 0.02 between two grid points of 1.14 to 1.24, or a root outside 1.08 to 1.24.

**The regrid beside the k_c 71 source and the interpolated numbers** (from D 20 and D 20.5):
| | dh170 k_c 79 | source k_c 71 | interpolated |
|---|---|---|---|
| |F| | 4.6591280965e-10 | 4.8426726409e-10 (ratio 0.96210) | 4.6720e-10 (-0.28%) |
| steps | 2746 | 2469 (ratio 1.1122) | 2749 |
| psi-constraint | 2.9230109e-3 | 4.8083996e-3 (ratio 0.60790) | 2.9161e-3 (+0.24%) |
| Delta | **1.101818198689** | 1.101837227594 (k_c 79 minus source **-1.9029e-5**) | -1.9296e-5 |

## Predictions against the result
| prediction | result |
|---|---|
| t5's, written before the run: one robust change within 0.01 of 1.126; the D 20.25 root (1.2035) showing is information | **yes**: one change, (1.12, 1.14), det-linear 1.122673 (0.0033 below 1.126); the 1.2035 root's continuation (near 1.18) does not show |
| mine: source check passes with all four controls firing (95%); regrid accepted with both controls firing (85%); regrid 2400 to 3400 s (70%) | yes; yes; yes, 3093 s (interpolated 2931 s) |
| steps 2650 to 2850 (65%); |F| within 5% of 4.6720e-10 (80%); psi-constraint within 10% of 2.9161e-3 (70%); Delta minus the source between -2.3e-5 and -1.4e-5 (65%) | yes, 2746; yes, -0.28%; yes, +0.24%; yes, -1.9029e-5 |
| every point noise-robust (70%); the repeat bit-identical (90%) | yes, 10 of 10; yes |
| exactly one robust change (62%; two 28%, none 3%, three or more 7%) | **one** |
| given one, the bracket (1.12, 1.14) (65%); the det-linear estimate within 0.01 of 1.126 (40%) | yes; yes |
| a second change, the D 20.25 root's continuation near 1.18 (28%) | no |
| the edge signs unequal (62%) | yes: plus at 1.08, minus at 1.24 |
| the float64 sign differs from the hybrid at more than half the points (20%) | no: 1 of 10 (1.12) |
| the scan 1.9 to 2.4 h (70%); peak RSS of a scan process below 3 GiB (85%) | yes, 2.14 h (the third round had two processes, 1209 and 1217 s per point); yes, 2.22 GiB. My ETA to t5 (16:45 UTC) was 2 min before the end |

## Log
- 2026-11-23 15:34 UTC: round 1 landed (1.08 to 1.14: plus, plus, plus, minus); 16:26: round 2 landed (partial reading, reported to t5: one change in (1.12, 1.14), none in 1.14 to 1.22; unchanged by round 3); 16:46:23 to 16:46:48 UTC: round 3 and the driver's reading finished.
- 2026-11-23 16:47:27 UTC: result written (this section).
