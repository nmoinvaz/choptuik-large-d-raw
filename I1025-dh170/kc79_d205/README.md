# I1025-dh170/kc79_d205: #1025 k_c 79 at D 20.5 on Linux, regridded from leg 3's k_c 71 state; the roots in lambda 1.00 to 1.24

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 10:43:25 UTC, before any run of this folder. Raw origin/main when the inputs were taken: a6671e16.

## Order (the coordinator t5's #1025 comment 7098310980 and hc, 23 Nov), quoted in part
"D 20 is read on two builds: Linux 1.246581 (dh170, raw a6671e16) and Windows 1.248340 and 1.247484 at k_c 79 and 87. One regrid fixes lambda_1 to about ±0.003 past D 19.5. D 20.25 at k_c 79 has two roots, 1.165140 and 1.203492, and win2's k_c 87 scan (about 12:00) decides which is lambda_1. This task extends the march meanwhile. **Step 1:** pin leg 3's k_c 71 D 20.5 state and record (raw `I1025-win2/kc71_leap/states/`, 50ace0e9: `sol_l1kc71Lw1025c_D20.500000.npy` blob 63399965, `l1kc71Lw1025c.jsonl` blob e44df695). `kc71_syscheck` accepts the source (both controls exit 1). lambda_0 = `ell_delta.lam0_at(20.5, *lam0_table())`, printed in the README. Then `ell_refine.py l1kc71Lw1025c 71 l1kc79dh170d205 79 1 20.5 <lambda_0> --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, 8 threads, nice 10, as a `systemd-run --user` unit. Accept by `kc79_syscheck_1025.py` (selftest 0, both controls exit 1). **Step 2:** `d18_hybsign.py` at 1.00 to 1.24 by 0.03 (9 values) and a repeat of 1.12 (10 evaluations, 4 processes of 1 thread), then `read_lower.py` with its selftest and both mutations. **Written before the run:** two robust changes. One near 1.08 (1.1651 continued at -0.33 per unit D) and one near 1.16 (1.2035 continued at -0.18 per unit D), each within about 0.03, the grid's resolution. **Report:** Delta, |F| and steps; every robust change by position. Raw `I1025-dh170/kc79_d205/`, README first. Memory: alerts only."
Roots are read by position, never by sign orientation (t5): "the root near lambda_1's line", "the rising root". lambda_0(20.5) = **2.1088217835** (`ell_delta.lam0_at(20.5, *ell_delta.lam0_table())[0]`, printed by the driver and checked against this number before the regrid).

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs and both drivers refuse any other blob)
| item | raw path | blob |
|---|---|---|
| leg 3's k_c 71 D 20.5 state (source); the `_D20.5000.npy` copy there is the same blob | I1025-win2/kc71_leap/states/sol_l1kc71Lw1025c_D20.500000.npy, commit 50ace0e9 | 63399965 |
| its record file at commit 50ace0e9: 8 rows, D 20.0625 to 20.5 (the current file on origin/main, blob 09b7ea78, has 10 rows to 20.625 and is not used) | I1025-win2/kc71_leap/states/l1kc71Lw1025c.jsonl, commit 50ace0e9 | e44df695 |
| the source check; the result check (the blobs of kc79_d20) | I1025-win2/kc71_leap/kc71_syscheck.py; I1025-win/kc79_d19/kc79_syscheck_1025.py | 4cd86cd4; 29dce7ea |
| the scanner, unmodified; its change finder | I1025-mac/d18/d18_hybsign.py; d185_scan_read.py | e089207a; 7c9d400f |
| reader (mine); `repeat_check.py` (dh610's) | I1025-dh170/lower_root/read_lower.py; I1025-dh610/kc71_d19125/in/repeat_check.py | 89309d3c; aaf598a9 |
| for the predictions: my k_c 79 D 20 record (kc79_d20, raw a6671e16) and the k_c 71 D 20 source row | I1025-dh170/kc79_d20/l1kc79dh170d20.jsonl; I1025-win2/kc79_d20/rec_k71_D20.0000.jsonl | de8aa11b; 3d22b88f |
Code: the worktree of `../kc79_d20`, unchanged: `~/Source/choptuik-large-d-1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_refine.py` 631e5801, `ell_delta.py` fde699f5), python `~/Source/choptuik-large-d-1058b/.venv` (3.14.10, multidouble 5.1.0, avx2). The source state is copied into the worktree's `solver/matter/data/` as `sol_l1kc71Lw1025c_D20.5000.npy` (blob checked). The drivers are `run_regrid.sh` and `run_scan.sh`, the kc79_d20 drivers with the tag, D, lambda_0, blobs and the lambda lists changed (the diff is `diff ../kc79_d20/run_regrid.sh run_regrid.sh`).

## Reference numbers (information, not a pass rule)
- **The source row, D 20.5** (record file above): |F| 4.8617065437e-10, 2453 steps, psi-constraint 5.2446740e-3, Delta 1.105077888484, F at the start 4.3165409880e-5, h 0.0625, kappa 0.7, u0 0.04, Ks 30.
- **D 20, the same step** (kc79_d20): source |F| 4.5262043273e-10, 2514 steps, constraint 3.6652833e-3, Delta 1.092269133460; my k_c 79 regrid |F| 4.4057739182e-10, 2800 steps, constraint 2.1021859e-3, Delta 1.092259276533 (2389 s). Ratios k_c 79 over the source: |F| 0.97339, steps 1.1138, constraint 0.57354; Delta k_c 79 minus the source -9.8569e-6. Applied to the D 20.5 source: |F| 4.7323e-10, 2732 steps, constraint 3.0080e-3, Delta 1.105068032.
- **The scan at D 20** (kc79_d20, hybrid signs as printed): minus from 1.20 to 1.24, plus from 1.25 to 1.30; one robust change (1.24, 1.25), det-linear 1.246581.
- **D 20.25, k_c 79** (t5's comment; I did not run it): two roots 1.165140 and 1.203492. Continued to D 20.5 at -0.33 and -0.18 per unit D: 1.0826 and 1.1585 (t5 writes "near 1.08" and "near 1.16").

## Commands (systemd user units, so no terminal owns them)
**Regrid** (`run_regrid.sh`, unit `i1025-k79d205r` under `systemd-inhibit`, 8 threads, nice 10; stops at the first failure; writes `steps.txt` and `VERDICT.txt`): in `solver/matter`,

    nice -n 10 timeout 21600 env OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8 ~/Source/choptuik-large-d-1058b/.venv/bin/python -u ell_refine.py \
      l1kc71Lw1025c 71 l1kc79dh170d205 79 1 20.5 2.1088217835 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma

preceded by the pins, the worktree checks, the lambda_0 check, the two selftests and the source check.
**Scan** (`run_scan.sh`, unit `i1025-k79d205s`, after VERDICT ACCEPTED): 4 processes of 1 thread at nice 10, `d18_hybsign.py` on the accepted state at D 20.5; lambda 1.00, 1.03, ..., 1.24 (9 values) and a repeat of 1.12 (10 evaluations): p0 1.00,1.12,1.24; p1 1.03,1.15 and the repeat 1.12 (on another process than the first 1.12); p2 1.06,1.18; p3 1.09,1.21. Three rounds, the third with two processes. Then `read_lower.py in/... scan 1.00 1.24`, its selftest and both mutations, and `repeat_check.py`.

## Acceptance (the order's, fixed before the run)
1. **Step 1, source.** `kc71_syscheck.py` accepts leg 3's k_c 71 D 20.5 state and record on this machine (|F| at most 1e-9, `freeze_from` gives 2453, |F| within 1%), both controls (`--mutate=F`, `--mutate=steps`) exit 1, and the k_c 79 check refuses the source (exit 1); both selftests exit 0. Otherwise no regrid.
2. **Step 2, regrid.** `ell_refine.py` exits 0 (the cap 21600 s is a stop); `kc79_syscheck_1025.py` accepts the result (k_c 79 at D 20.5, |F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%), both controls exit 1.
3. **Step 3, scan.** Each process prints the record system; `read_lower.py` selftest exit 0, mutations `shift` and `round2` exit 1; the repeat of 1.12 agrees (sign, ln|det| within 1e-6, noise signs, float64 sign). A stop at any step: I report and change nothing.

## Reading, fixed now (by position)
Every robust change (both neighbouring points noise-robust) with bracket, det-linear estimate and estimator range (the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure), orientation as printed (information); the edge signs; changes touching a non-robust point listed and not counted; every ln|det| minimum without a sign change flagged; the repeat's bits. On a grid of 0.03 a det-linear estimate is good to about the bracket, so a position is quoted with its bracket. Parity: with two robust changes the two edge signs (1.00 and 1.24) are equal; unequal edge signs mean an odd number of changes, or one outside the window. Report: Delta, |F|, steps and psi-constraint of the regrid beside the D 20 numbers above; every root by position beside t5's 1.08 and 1.16.
**Written before the run (t5's):** two robust changes, one near 1.08 and one near 1.16, each within about 0.03.

## Predictions, registered before the runs (mine, information)
- the source check passes with all four controls firing about 95%; the regrid exits 0 and is accepted with both controls firing about 85%; the regrid takes 2000 to 3000 s about 70% (D 20: 2389 s);
- steps between 2600 and 2900 about 65% (the D 20 ratio gives 2732); |F| within 10% of 4.7323e-10 about 75%; psi-constraint within 15% of 3.0080e-3 about 70%; Delta minus the source between -1.5e-5 and -5e-6 about 65% (D 20: -9.857e-6);
- the scan: every point noise-robust about 70%; the repeat of 1.12 bit-identical about 90%; exactly two robust changes in (1.00, 1.24) about 60%, one about 18%, none about 7%, three or more about 15%; with two, the lower in (1.05, 1.11) and the upper in (1.13, 1.19) about 70% (about 40% overall);
- the edge signs equal about 65%; the float64 sign differs from the hybrid at more than half the points about 25%; the scan 2.4 to 3.1 h (two rounds of about 3300 s side by side and a shorter third) about 65%; peak RSS of a scan process below 3 GiB about 85%.

## Budget
The regrid: 8 threads at nice 10 (all of this machine). The scan: 4 processes of 1 thread at nice 10. Nothing else of mine runs. Memory: alert only (`alert.log` if MemAvailable falls below 2048 MiB; nothing is stopped for memory). Estimate: regrid about 40 min, scan about 2.7 h.

## Log
- 2026-11-23 10:43:25 UTC: folder, inputs, drivers and the reading prepared before any run. Selftests: `read_lower.py` exit 0, `shift` and `round2` exit 1, `repeat_check.py`, `kc79_syscheck_1025.py` and `kc71_syscheck.py` exit 0 (`selftest_exits_pre.txt`; the drivers run them again). Dry run of `run_regrid.sh`: the pins, the worktree checks and lambda_0(20.5) = 2.1088217835 pass (`dry_steps_regrid.txt`). The scan's lambda list was checked by a script: 10 evaluations, 1.12 twice on two processes.
- 2026-11-23 10:43:35 to 10:43:40 UTC: `run_regrid.sh` started as unit `i1025-k79d205r`; **STEP 1** source check ACCEPTED at 10:43:40: leg 3's k_c 71 D 20.5 record |F| 4.8617065437e-10, 2453 steps, constraint 5.245e-3, Delta 1.105077888484 (2725 s on win2); this machine's state |F| 4.8612559089e-10 (-0.009% against the record, inside the 1% bar), `freeze_from` 2453 steps; `--mutate=F` and `--mutate=steps` exit 1; the k_c 79 check refuses the source (exit 1: "the record is not k_c 79 at D 20.5"); both selftests exit 0; lambda_0(20.5) recomputed 2.1088217835. The regrid started 10:43:40.
- 2026-11-23 10:43:40 to 11:35:32 UTC: **STEP 2 regrid** (`ell_refine.py`, 8 threads, nice 10, unit `i1025-k79d205r`): exit 0, wall **3112 s** (the record's step 3109 s; D 20 took 2389 s), peak RSS of `ell_refine` sampled 1.14 GiB (51 samples, one per 60 s), lowest MemAvailable 26.8 GiB, no memory alert. 11:35:37 **ACCEPTED**: `kc79_syscheck_1025.py` exit 0 (|F| in the record class, `freeze_from` 2731 steps = the record's), `--mutate=F` and `--mutate=steps` exit 1. State `sol_l1kc79dh170d205_D20.5000.npy` blob 30a92b78, record `l1kc79dh170d205.jsonl` blob 5406e21c.
- **The regrid beside the k_c 71 source and the D 20 ratios:** |F| **4.6763736498e-10** (source 4.8617065437e-10, ratio 0.96188; the D 20 ratio 0.97339 gave 4.7323e-10, -1.18%); steps **2731** (source 2453, ratio 1.1133; the D 20 ratio 1.1138 gave 2732); psi-constraint **3.2382273e-3** (source 5.2446740e-3, ratio 0.61743; the D 20 ratio 0.57354 gave 3.0080e-3, +7.65%); Delta **1.105055446478** (source 1.105077888484: k_c 79 minus the source **-2.2442e-5**; D 20: -9.857e-6); F at the start 4.9820694e-5.
- 2026-11-23 11:35:51 UTC: **STEP 3 scan** started as unit `i1025-k79d205s` (4 processes of 1 thread, nice 10, 10 evaluations); all four print the record system (|F| 4.6786148313e-10 against the record's 4.6763736498e-10, 2731 steps equal).
- 2026-11-23 11:36:43 UTC: step 2 logged (this entry).

## Result (written 2026-11-23 13:43:57 UTC)
Steps 1 and 2 as logged (ACCEPTED 10:43:40 and 11:35:37 UTC). **Step 3:** unit `i1025-k79d205s` exit 0; processes p2, p3, p1, p0 exit 0 at 13:22:31, 13:22:51, 13:42:54 and 13:43:02 UTC; all four printed the record system (|F| 4.6786148313e-10 against the record's 4.6763736498e-10, 2731 steps equal); **10 of 10 evaluations noise-robust**; the repeat of 1.12 (the first on p0, the repeat last on p1) **bit-identical** (hybrid +1, ln|det| -2391.4860573718984, float64 ln|det| -2391.237076265184, noise [1, 1]; `repeat_check.py` PASS); `read_lower.py` selftest exit 0, `--mutate=shift` and `--mutate=round2` exit 1; reader exit 0 (`read_lower.txt`). Seconds per point 3159 to 3262 in rounds 1 and 2 (four processes side by side) and 1207 and 1217 in round 3 (two processes); wall per process 1:46:39 to 2:07:11 by /usr/bin/time, the scan 2:07:12 (11:35:51 to 13:43:03); peak RSS 2.11 to 2.23 GiB; lowest MemAvailable 22.1 GiB (scan, 127 samples) and 26.8 GiB (regrid); no memory alert (`alert.log` does not exist).

**Hybrid signs, as printed, lambda 1.00 to 1.24: minus at 1.00, 1.03, 1.06; plus at 1.09, 1.12, 1.15, 1.18, 1.21, 1.24; edge signs minus and plus; the float64 sign equals the hybrid at all 10 evaluations.** One robust change, none touching a non-robust point:
| position | bracket | orientation as printed | det-linear estimate | estimator range |
|---|---|---|---|---|
| **the change near 1.08, k_c 79, D 20.5, dh170 (Linux)** | (1.06, 1.09) | - to + | **1.087574** | [1.062870, 1.087574] |
The estimator range is the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure; on a grid of 0.03 the estimate is good to about the bracket. **There is no second change in 1.09 to 1.24**: the sign is plus at six consecutive points, and no ln|det| minimum without a sign change was found. ln|det|: 1.00 -2382.4046, 1.03 -2385.0181, 1.06 -2388.1449, 1.09 -2390.5755, 1.12 -2391.4861, 1.15 -2393.0830, 1.18 -2394.8791, 1.21 -2396.7901, 1.24 -2398.8077; the differences per 0.03 from 1.09 on are -0.9106, -1.5969, -1.7961, -1.9110, -2.0176 (no dip). Parity: the edge signs are unequal, an odd number of changes in the window, which one change satisfies.
**What the scan does not show:** whether a pair of changes closer together than 0.03 lies between two grid points of 1.09 to 1.24 (equal signs, a dip that falls between points), or whether the root that t5 puts at 1.203492 at D 20.25 lies outside 1.00 to 1.24. A root moving at -0.18 per unit D would sit near 1.16; none is there.

**The regrid beside the k_c 71 source and the D 20 ratios** (source: leg 3's record row; D 20 ratios from kc79_d20):
| | dh170 k_c 79 | source k_c 71 | the D 20 ratios gave |
|---|---|---|---|
| |F| | 4.6763736498e-10 | 4.8617065437e-10 (ratio 0.96188) | 4.7323e-10 |
| steps | 2731 | 2453 (ratio 1.1133) | 2732 |
| psi-constraint | 3.2382273e-3 | 5.2446740e-3 (ratio 0.61743) | 3.0080e-3 |
| Delta | **1.105055446478** | 1.105077888484 (k_c 79 minus source **-2.2442e-5**) | -9.857e-6 |

## Predictions against the result
| prediction | result |
|---|---|
| t5's, written before the run: two robust changes, near 1.08 and near 1.16, each within about 0.03 | **the first is there**: (1.06, 1.09), 1.087574 (0.0076 above 1.08); **the second is not**: sign plus at 1.09 to 1.24, no dip |
| mine: source check passes with all four controls firing (95%); regrid accepted with both controls firing (85%) | yes; yes |
| the regrid takes 2000 to 3000 s (70%) | **no**: 3112 s (D 20: 2389 s) |
| steps between 2600 and 2900 (65%); |F| within 10% of 4.7323e-10 (75%); psi-constraint within 15% of 3.0080e-3 (70%) | yes, 2731; yes, -1.18%; yes, +7.65% |
| Delta minus the source between -1.5e-5 and -5e-6 (65%) | **no**: -2.2442e-5 |
| every point noise-robust (70%); the repeat bit-identical (90%) | yes, 10 of 10; yes |
| exactly two robust changes (60%), one (18%), none (7%), three or more (15%) | **one** (the 18% case) |
| the edge signs equal (65%) | **no**: minus at 1.00, plus at 1.24 (consistent with one change) |
| the float64 sign differs from the hybrid at more than half the points (25%) | no: 0 of 10 |
| the scan 2.4 to 3.1 h (65%) | **no**: 2.12 h (the third round had two processes, 1207 and 1217 s per point); peak RSS below 3 GiB (85%): yes, 2.23 GiB. My ETA to t5 (14:20 UTC) was 37 min after the end |

## Log
- 2026-11-23 12:30 UTC: round 1 landed (1.00 to 1.09: minus, minus, minus, plus); 13:22: round 2 landed (partial reading, reported to t5: one change in (1.06, 1.09), none near 1.16; unchanged by round 3); 13:42:54 to 13:43:03 UTC: round 3 and the driver's reading finished.
- 2026-11-23 13:43:57 UTC: result written (this section).
