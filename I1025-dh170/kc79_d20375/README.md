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
