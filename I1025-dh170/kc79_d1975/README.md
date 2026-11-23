# I1025-dh170/kc79_d1975: #1025 k_c 79 at D 19.75, win2's k_c 71 D 19.75 state regridded to k_c 79, then a hybrid sign scan lambda 1.27 to 1.38 (extending lambda_1's line)

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-22 22:21:22 UTC, before any run of this folder. Raw origin/main when the inputs were taken: f0a08198.

## Order (the coordinator t5's hc, 22 Nov), quoted in part
"#1025, k_c 79 at D 19.75, extending lambda_1's line: (1) win2's kc71_syscheck.py on its k_c 71 D 19.75 state (raw I1025-win2/kc71_leap/states/sol_l1kc71Lw1025b_D19.750000.npy with its line in states/l1kc71Lw1025b.jsonl, f51bcdd6 or later; pin the blobs); (2) regrid to k_c 79 with ell_refine.py as dh370 did at D 19.5 (its README in I1025-dh370/kc79_d195; lam0 from ell_delta.lam0_at(19.75)), accepted only by kc79_syscheck_1025.py and both controls, 8 threads, nice 10, a systemd unit; (3) scan lambda 1.27 to 1.38 at 0.01 (12 values) plus a repeat of 1.32, 4 processes of 1 thread, read_lower.py. The line (1.5397, 1.5058, 1.4700, 1.4316, 1.3976 at D 19 to 19.5) puts lambda_1 near 1.325 (information, not a pass rule). Raw folder I1025-dh170/kc79_d1975/, README first. Read by position. Post on #1025, send me each step's verdict."
Roots are read by position, never by sign orientation (t5, same day): "the root near lambda_1's line" and "the rising root".

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs and `run_regrid.sh`, `run_scan.sh` refuse any other blob)
| item | raw path | blob |
|---|---|---|
| k_c 71 D 19.75 state (win2's leg 2) | I1025-win2/kc71_leap/states/sol_l1kc71Lw1025b_D19.750000.npy | ab514df3 |
| its record, 9 rows D 19.375 to 19.875 (f51bcdd6 is an ancestor of the raw head used); the D 19.75 row: |F| 4.0732333920e-10, 2552 steps, psi-constraint 3.0243e-3, Delta 1.0860122540, h 0.0625, kappa 0.7, u0 0.04, Ks 30 | I1025-win2/kc71_leap/states/l1kc71Lw1025b.jsonl | ee94e902 |
| win2's source check | I1025-win2/kc71_leap/kc71_syscheck.py | 4cd86cd4 |
| winb's result check (named kc79_syscheck.py in its docstring) | I1025-win/kc79_d19/kc79_syscheck_1025.py | 29dce7ea |
| the scanner, xfkappa's, unmodified | I1025-mac/d18/d18_hybsign.py | e089207a |
| change finder (xfkappa's) | I1025-mac/d18/d185_scan_read.py | 7c9d400f |
| reader (mine); `repeat_check.py` (dh610's) | I1025-dh170/lower_root/read_lower.py; I1025-dh610/kc71_d19125/in/repeat_check.py | 89309d3c; aaf598a9 |
| for the comparison: dh370's D 19.5 reading and steps; macm3's D 19.25 reading | I1025-dh370/kc79_d195/read_lower.txt, steps.txt; I1025-macm3/kc79_d1925/read_lower.txt | 4e9bbe30, bdb59510; cf3608e7 |
Code: worktree `~/Source/choptuik-large-d-1025k79` (new, detached at **48c36355**, as dh370's `choptuik-large-d-1025`): `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's (checked by the driver), `ell_refine.py` blob 631e5801, `ell_delta.py` fde699f5. Python `~/Source/choptuik-large-d-1058b/.venv` (3.14.10, multidouble 5.1.0, avx2). The source state is copied into the worktree's `solver/matter/data/` as `sol_l1kc71Lw1025b_D19.7500.npy`, the name `ell_refine.py` reads (`D:.4f`), and checked by blob.

## Commands (systemd user units, so no terminal owns them)
**Regrid** (`run_regrid.sh`, unit `i1025-k79r` under `systemd-inhibit`, 8 threads, nice 10; stops at the first failure, writes `steps.txt` and `VERDICT.txt`): the D 19.5 command with D, the output tag and lambda_0 changed:

    cd ~/Source/choptuik-large-d-1025k79/solver/matter && nice -n 10 timeout 21600 env OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8 \
      ~/Source/choptuik-large-d-1058b/.venv/bin/python -u ell_refine.py l1kc71Lw1025b 71 l1kc79dh170d1975 79 1 19.75 2.1120935738 \
      --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma

lambda_0(19.75) = 2.1120935738107143 from `ell_delta.lam0_at(D, *ell_delta.lam0_table())`, which here reproduces winb's 2.1181259879 at D 18.5 and 2.1156378446 at D 19 and dh370's 2.1132623525 at D 19.5 (its error estimate grows with D, 1.07e-5 here against 6.2e-7 at D 19.5; `--no-gamma` does not use the lambda_0 argument, as dh370 noted).
**Scan** (`run_scan.sh`, unit `i1025-k79s`, after VERDICT ACCEPTED): 4 processes of 1 thread at nice 10, `d18_hybsign.py in/... STATE 19.75 LAMS scan/scan_D19.75_p<p>.jsonl`; lambda 1.27, 1.28, ..., 1.38 (12 values) and a repeat of 1.32: 13 evaluations, split by index mod 4: p0 1.27, 1.31, 1.35 and the repeat 1.32; p1 1.28, 1.32, 1.36; p2 1.29, 1.33, 1.37; p3 1.30, 1.34, 1.38 (the repeat is on another process than the first 1.32). The system check is each process's first line (anything but "the record system" is a stop).

## Acceptance (fixed before the run, as at D 19.125 and D 19.5)
1. **Step 1, source.** `kc71_syscheck.py` accepts the k_c 71 D 19.75 state and record on this machine (the record's |F| at most 1e-9, `freeze_from` gives the record's step count, |F| within 1%), both controls (`--mutate=F`, `--mutate=steps`) exit 1, and both selftests (`kc71_syscheck.py`, `kc79_syscheck_1025.py`) exit 0. Otherwise no regrid; I report.
2. **Step 2, regrid.** `ell_refine.py` exits 0 (the cap 21600 s is a stop); `kc79_syscheck_1025.py` accepts the regridded record and state (k_c 79 at D 19.75, |F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%) and both controls exit 1.
3. **Step 3, scan.** Each process prints the record system; `read_lower.py` selftest exits 0 and its mutations `shift` and `round2` exit 1; the repeat of 1.32 agrees (sign, ln|det| within 1e-6, noise signs, float64 sign). A stop at any step: I report and do not go on.

## Reading, fixed now (by position)
Every robust change (both neighbouring points noise-robust) with bracket, det-linear estimate and estimator range (the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure), orientation as printed (information, not used to identify a root); the edge signs; changes touching a non-robust point listed and not counted; every ln|det| minimum without a sign change flagged; the repeat. A change in the window is "the root near lambda_1's line" if its position fits the k_c 79 track, else reported by position only.

## Beside which the k_c 79 reading is reported (information, not a pass rule)
The k_c 79 root near lambda_1's line at D 19, 19.125, 19.25, 19.375, 19.5: **1.539658** (winb, `I1025-win/kc79_d19`), **1.505784** (dh370, `kc79_d19125`), **1.469975** (macm3, raw cc30e59c, det-linear in (1.46, 1.47)), **1.4316** (t5's list, macm3), **1.397565** (dh370, `kc79_d195`, range [1.396781, 1.397565]); the slopes -0.2710, -0.2865, -0.307 and -0.2723 per unit D put it at **1.3296 to 1.3209 at D 19.75**, inside the window 1.27 to 1.38; t5: near 1.325. The rising root of k_c 79 (1.4002 at D 19.125, my `../kc79_d19125low`; t5's line from it to macm3's 1.4698 at D 19.375) is above the window at D 19.75.

## Cost, written before the run
dh370's regrids: 2576 s (D 19.125) and 2240 s (D 19.5) on 6 threads, peak RSS 1.47 GB; I expect 2000 to 3500 s on 8 threads of this i7-7700. dh370's scan points took 1971 to 2068 s on 4 processes of 1 thread; 13 evaluations on 4 processes are 4 rounds for p0: about 2.3 h. Total about 3 to 4 h.

## Predictions, registered before the runs (mine, information)
- the source check passes with both controls firing about 95%; the regrid exits 0 about 90% and is accepted with both controls firing about 85% (the source |F| 4.07e-10 is higher than at D 19.5, 3.50e-10, and the bar is 1e-9); the regrid takes 2000 to 3500 s about 65%;
- the scan: every point noise-robust about 75%; the repeat of 1.32 agrees about 90%; the window shows exactly one robust change about 65%, within 0.02 of 1.325 about 60% of the runs (so about 40% overall), none about 15%, two or more about 15%, other 5%;
- the float64 sign differs from the hybrid at more than half the points about 50% (as at D 19.5: opposite at every point); a lane of 4 rounds takes 2 to 2.8 h about 60%; peak RSS below 2.5 GiB about 90%.

## Budget
The regrid: 8 threads at nice 10 (all of this machine). The scan: 4 processes of 1 thread at nice 10. Nothing else of mine runs; no other job on dh170 at 22:18 UTC (load average 0.2).

## Log
- 2026-11-22 22:21:22 UTC: folder, inputs, drivers, worktree and the reading prepared before any run. Reader selftest exit 0, `shift` and `round2` exit 1, `repeat_check.py` exit 0 (`selftest_exits_pre.txt`; the drivers run them again). Dry run of `run_regrid.sh`: pins and worktree checks pass (`dry_steps_regrid.txt`).
- 2026-11-22 22:21:35 to 22:21:39 UTC: `run_regrid.sh` started as unit `i1025-k79r`; STEP 1 (source check) ACCEPTED at 22:21:39 (record |F| 4.0732333920e-10, 2552 steps; this machine's state |F| 4.0720551300e-10, freeze_from 2552; both controls exit 1); the regrid started at 22:21:39 UTC. (The Budget line's typo, 'dh370... on dh170', is fixed.)
- 2026-11-22 22:21:39 to 23:01:49 UTC: **STEP 2 regrid** (`ell_refine.py`, 8 threads, nice 10, unit `i1025-k79r`): exit 0, wall 2410 s (the record's step 2408 s), peak RSS 1.81 GiB (sampled every 60 s, 40 samples). The state: |F| 4.0158668855e-10 (F at the start 2.104e-5), 2839 steps, psi-constraint 1.652e-3, Delta 1.0860054437 (the k_c 71 source's 1.0860122540). 23:01:54 UTC **ACCEPTED** by `kc79_syscheck_1025.py` (|F| in the record class and the step count comes back: 2839 = 2839); controls: `--mutate=F` (record |F| x 1.5) exit 1, `--mutate=steps` (steps + 1) exit 1. State `sol_l1kc79dh170d1975_D19.7500.npy` blob f2ad34b5, record `l1kc79dh170d1975.jsonl` blob 0508163e.
- 2026-11-22 23:02:14 UTC: **STEP 3 scan** started as unit `i1025-k79s` (4 processes of 1 thread, nice 10, 13 evaluations); all four print the record system (|F| 4.0206992553e-10 against the record's 4.0158668855e-10, 2839 steps equal).
- 2026-11-22 23:02:49 UTC: step 2 logged (this entry).

## Result (written 2026-11-23 02:53:16 UTC; the scan ended at 02:05:32 UTC during an outage of the home network, 01:00 to 02:50 UTC, that cut my session from the API; every run was a systemd user unit and kept going; I read and checked the results after the outage)
**Steps 1 and 2:** step 1 ACCEPTED 22:21:39 UTC, regrid exit 0 in 2410 s, ACCEPTED 23:01:54 UTC (see the Log). **Step 3:** unit `i1025-k79s` exit 0; processes p3, p2, p1 exit 0 at 01:50:11, 01:50:19, 01:50:23 UTC and p0 at 02:05:31; all four printed the record system (|F| 4.0206992553e-10 against the record's 4.0158668855e-10, 2839 steps equal); **13 of 13 evaluations noise-robust**; the repeat of 1.32 (the first on p1, the repeat last on p0) bit-identical (ln|det| -2478.947320280177, sign, noise, float64; `repeat_check.py` PASS); `read_lower.py` selftest exit 0, `--mutate=shift` and `--mutate=round2` exit 1; reader exit 0 (`read_lower.txt`). Seconds per point 3326 to 3412 side by side (three rounds), 904 for p0's last point alone; wall 2:47:57 to 2:48:09 (p1, p2, p3) and 3:03:17 (p0) by /usr/bin/time; peak RSS 2.19 to 2.22 GiB (2296464 to 2331252 kB); no ALERT file (this driver has no sampler).

**Hybrid signs, as printed, lambda 1.27 to 1.38: plus from 1.27 to 1.32, minus from 1.33 to 1.38; edge signs plus and minus.** One robust change, none touching a non-robust point:
| position | bracket | orientation as printed | det-linear estimate | estimator range |
|---|---|---|---|---|
| **the root near lambda_1's line, k_c 79, D 19.75** | (1.32, 1.33) | + to - | **1.326378** | [1.324044, 1.326378] |
The estimator range is the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure. No ln|det| minimum without a sign change (ln|det| falls to -2479.513 at 1.33, beside the change, rises to -2479.032 at 1.34 and falls slowly to -2480.105 at 1.38). The float64 sign differs from the hybrid at 4 of 13 evaluations (1.30, 1.32 twice, 1.33).

**By position, the track of the k_c 79 root near lambda_1's line** (D: lambda): 19: 1.539658 (winb); 19.125: 1.505784 (dh370); 19.25: 1.469975 (macm3); 19.375: 1.4316 (t5's list); 19.5: 1.397565 (dh370); **19.75: 1.326378 (here)**. The step from D 19.5 is -0.071187 in 0.25 D, **-0.2847 per unit D**; the earlier slopes are -0.2710, -0.2865, -0.307 and -0.2723. The extrapolations of the README (1.3209 to 1.3296; t5's 1.325) bracket it: the estimate is 0.0014 above 1.325. The rising root (1.4002 at D 19.125, 1.4698 at D 19.375, t5's line) is above this window, and the window holds no other change.

## Predictions against the result
| prediction | result |
|---|---|
| source check passes with both controls firing (95%); regrid exits 0 (90%); accepted with both controls firing (85%); regrid 2000 to 3500 s (65%) | yes; yes; yes; yes, 2410 s |
| scan: every point noise-robust (75%); the repeat of 1.32 agrees (90%) | yes, 13 of 13; yes, bit-identical |
| exactly one robust change in the window (65%), within 0.02 of 1.325 (about 60% of those) | one, 0.0014 above 1.325 |
| the float64 sign differs from the hybrid at more than half the points (50%) | **no**: 4 of 13 |
| a lane of 4 rounds takes 2 to 2.8 h (60%); peak RSS below 2.5 GiB (90%) | **no**: p0 3.05 h (3 rounds beside the others at 3330 to 3410 s, then one point alone, 904 s; dh370's points took 1971 to 2068 s on its 6-core machine); the ETA I sent t5 (02:48) was 43 min later than the end (02:05); yes, 2.22 GiB |

## Log
- 2026-11-22 22:21:35 to 23:01:54 UTC: steps 1 and 2 (see above and `steps.txt`); 23:02:14 the scan started (unit `i1025-k79s`).
- 2026-11-23 00:55 UTC: after rounds 1 and 2 (8 of 13) I ran the same reader on a scratch copy outside this folder: one change in (1.32, 1.33), 1.326378; the final reading above is unchanged by rounds 3 and 4.
- 2026-11-23 01:50 to 02:05 UTC: the scan finished and the driver ran the reader (steps.txt), while my session was cut off from the API (the network outage). 02:52 UTC: I read the logs and wrote this section.
- 2026-11-23 02:53:16 UTC: result written (this section).
