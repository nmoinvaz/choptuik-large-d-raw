# I1025-dh170/kc79_d20: #1025 k_c 79 at D 20 on Linux, regridded from the k_c 71 source of win2's D 20 regrid, to measure the D 20 build spread (#1075's goal)

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 07:13:11 UTC, before any run of this folder. Raw origin/main when the inputs were taken: 8d19a03d.

## Order (the coordinator t5's #1025 comment 7094064956 and hc, 23 Nov), quoted in part
"**Why.** It measures the build spread at D 20 (#1075's goal; rpi5 was released). Windows gives lambda_1(20) = 1.248340 at k_c 79 and 1.247484 at k_c 87 (raw 9e520757). The build moved lambda_1 by 0.0032 at D 19.5 and 0.0136 at D 19.75. With the same source and the same command, the difference here is the build's. **Step 1:** pin the k_c 71 D 20 state and record that win2's I1025-win2/kc79_d20/ README names as its source (by blob), and win2's kc79_syscheck_1025.py. kc71_syscheck (or the k_c 79 check's refusal, as win2 did) accepts the source. Then ell_refine.py <that k_c 71 tag> 71 l1kc79dh170d20 79 1 20.0 2.1110019498 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (lambda_0 as win2 used), 8 threads, nice 10, a systemd-run --user unit. Accept by kc79_syscheck_1025.py (selftest 0, both controls exit 1). **Step 2:** d18_hybsign.py at 1.20 to 1.30 by 0.01 and a repeat of 1.25 (12 evaluations, 4 processes of 1 thread), then read_lower.py with its selftest and both mutations. **Report:** Delta, |F| and steps beside win2's k_c 79 D 20 regrid (Delta 1.092257255093, |F| 4.4105e-10, 2800 steps); every robust change by position, beside 1.248340. **Written before the run:** one robust change in (1.20, 1.30). Its distance from 1.248340 is the D 20 build spread; going by D 19.5 and 19.75 it lies between 0.003 and 0.03. Raw I1025-dh170/kc79_d20/, README first. Memory: alerts only. Estimate: regrid about 45 min, scan 3 rounds of about 80 min."
Roots are read by position, never by sign orientation (t5): "the root near lambda_1's line".

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs and both drivers refuse any other blob)
The source is the one win2's README (`I1025-win2/kc79_d20/README.md`) names: the leap's D 20 state of tag `l1kc71Lw1025b` (win2's `regrid79_d20.sh`: `sol_l1kc71Lw1025b_D20.000000.npy` and its `.4f` copy, which are the same blob) and its record line.
| item | raw path | blob |
|---|---|---|
| win2's k_c 71 D 20 state (source) | I1025-win2/kc71_leap/states/sol_l1kc71Lw1025b_D20.000000.npy (the `_D20.0000.npy` copy has the same blob) | 970fde73 |
| its record file, 11 rows to D 20.0; the D 20.0 row: |F| 4.5262043273e-10, 2514 steps, psi-constraint 3.6653e-3, Delta 1.0922691335, h 0.0625, kappa 0.7, u0 0.04, Ks 30 | I1025-win2/kc71_leap/states/l1kc71Lw1025b.jsonl | 8f86af85 |
| win2's single record line of that row (it equals the D 20 row of the file above, checked) | I1025-win2/kc79_d20/rec_k71_D20.0000.jsonl | 3d22b88f |
| win2's source check (the same blob in `kc79_d20/inputs/`) | I1025-win2/kc71_leap/kc71_syscheck.py | 4cd86cd4 |
| winb's result check (win2's copy in `kc79_d20/inputs/` is the same blob) | I1025-win/kc79_d19/kc79_syscheck_1025.py | 29dce7ea |
| the scanner, xfkappa's, unmodified; its change finder | I1025-mac/d18/d18_hybsign.py; d185_scan_read.py | e089207a; 7c9d400f |
| reader (mine); `repeat_check.py` (dh610's) | I1025-dh170/lower_root/read_lower.py; I1025-dh610/kc71_d19125/in/repeat_check.py | 89309d3c; aaf598a9 |
| for the comparison: win2's k_c 79 D 20 record, summary and reading | I1025-win2/kc79_d20/rec_k79_D20.0000.jsonl, summary_kc79.txt, read_lower_k79_D20.txt | d659667f, 79484f0c, 5832e968 |
Code: the worktree of `../kc79_d1975` and `../kc87_d1975`, unchanged: `~/Source/choptuik-large-d-1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_refine.py` 631e5801, `ell_delta.py` fde699f5), python `~/Source/choptuik-large-d-1058b/.venv` (3.14.10, multidouble 5.1.0, avx2). The source state is copied into the worktree's `solver/matter/data/` as `sol_l1kc71Lw1025b_D20.0000.npy`, the name `ell_refine.py` reads (`D:.4f`), and checked by blob. lambda_0(20) = 2.1110019498 = `ell_delta.lam0_at(20.0, *lam0_table())` (the driver recomputes it and refuses a different value; error 3.8e-7; unused with `--no-gamma`).

## win2's D 20 numbers (Windows), beside which mine are reported (information, not a pass rule)
- k_c 71 source record: |F| 4.5262043273e-10, 2514 steps, psi-constraint 3.6653e-3, Delta 1.0922691335.
- **win2's k_c 79 D 20 regrid** (8 threads of a Core Ultra 7 265K, 5273 s, raw 9e520757 and `I1025-win2/kc79_d20/`): |F| **4.4104844173e-10**, **2800** steps, psi-constraint 2.1021e-3, Delta **1.092257255093** (k_c 79 minus k_c 71 -1.1878e-5).
- **win2's scan** (lambda 1.20 to 1.32, 14 evaluations): hybrid minus from 1.20 to 1.24, plus from 1.25 to 1.32; one robust change in (1.24, 1.25), **det-linear 1.248340**, range [1.244440, 1.248340]; the repeat of 1.26 agrees; one ln|det| minimum without a change at 1.31 (depth 0.0356; outside my window).

## Commands (systemd user units, so no terminal owns them)
**Regrid** (`run_regrid.sh`, unit `i1025-k79d20r` under `systemd-inhibit`, 8 threads, nice 10; stops at the first failure; writes `steps.txt` and `VERDICT.txt`): in `solver/matter`,

    nice -n 10 timeout 21600 env OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8 ~/Source/choptuik-large-d-1058b/.venv/bin/python -u ell_refine.py \
      l1kc71Lw1025b 71 l1kc79dh170d20 79 1 20.0 2.1110019498 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma

preceded by the pins, the worktree checks, the lambda_0 check, the two selftests, and the source check.
**Scan** (`run_scan.sh`, unit `i1025-k79d20s`, after VERDICT ACCEPTED): 4 processes of 1 thread at nice 10, `d18_hybsign.py in/... STATE 20.0 LAMS scan/scan_D20_p<p>.jsonl`; lambda 1.20, 1.21, ..., 1.30 (11 values) and a repeat of 1.25: 12 evaluations; p0 1.20,1.24,1.28; p1 1.21,1.25,1.29; p2 1.22,1.26,1.30; p3 1.23,1.27 and the repeat 1.25 (on another process than the first 1.25), three rounds. The system check is each process's first line (anything but "the record system" is a stop). Then `read_lower.py` selftest, `shift`, `round2`, `read_lower.py scan 1.20 1.30` and `repeat_check.py`. Memory: alert only (both drivers write `alert.log` when MemAvailable is below 2 GiB, every 30 s; nothing is stopped or refused for memory).

## Acceptance (the order's, fixed before the run)
1. **Step 1, source.** `kc71_syscheck.py` accepts win2's k_c 71 D 20 state and record on this machine (|F| at most 1e-9, `freeze_from` gives 2514, |F| within 1%), both controls (`--mutate=F`, `--mutate=steps`) exit 1, and the k_c 79 check refuses the source (win2's rehearsal; exit 1); both selftests exit 0. Otherwise no regrid.
2. **Step 2, regrid.** `ell_refine.py` exits 0 (the cap 21600 s is a stop); `kc79_syscheck_1025.py` accepts the result (k_c 79 at D 20, |F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%), both controls exit 1.
3. **Step 3, scan.** Each process prints the record system; `read_lower.py` selftest exit 0, mutations `shift` and `round2` exit 1; the repeat of 1.25 agrees (sign, ln|det| within 1e-6, noise signs, float64 sign). A stop at any step: I report and change nothing.

## Reading, fixed now (by position)
Every robust change (both neighbouring points noise-robust) with bracket, det-linear estimate and estimator range (the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure), orientation as printed (information); the edge signs; changes touching a non-robust point listed and not counted; every ln|det| minimum without a sign change flagged; the repeat's bits. Report beside win2's: Delta, |F|, steps, psi-constraint of the regrid; each root's position beside 1.248340 (the difference is the D 20 build spread, mine minus win2's).
**Written before the run (t5's):** one robust change in (1.20, 1.30); its distance from 1.248340 lies between 0.003 and 0.03 (going by D 19.5 and 19.75).

## Predictions, registered before the runs (mine, information)
- the source check passes with all four controls firing about 95%; the regrid exits 0 and is accepted with both controls firing about 85%; the regrid takes 2200 to 3600 s about 65% (k_c 79 at D 19.75: 2410 s; win2 5273 s on Windows); steps equal to win2's 2800 about 45%, within 10 of it about 70%; |F| within 5% of win2's 4.4105e-10 about 80%; Delta within 1e-6 of win2's 1.092257255093 about 50% (the two k_c 87 regrids of D 19.75 differed by 1.4e-6 in Delta);
- the scan: every point noise-robust about 75%; the repeat of 1.25 bit-identical about 90%; exactly one robust change in (1.20, 1.30) about 85%;
- its distance from 1.248340: below 0.003 about 25%; 0.003 to 0.03 about 55%; above 0.03 about 10%; no change or two or more about 10%; its sign: Linux below win2's 1.248340 about 60% (the macOS root was above Linux's at D 19.75);
- the float64 sign differs from the hybrid at more than half the points about 40%; the scan 2.7 to 3.3 h (three rounds of about 3400 s side by side) about 65%; peak RSS of a scan process below 3 GiB about 85%.

## Budget
The regrid: 8 threads at nice 10 (all of this machine). The scan: 4 processes of 1 thread at nice 10. Nothing else of mine runs; load average 0.03 at 07:12 UTC, MemAvailable 28.5 GiB.

## Log
- 2026-11-23 07:13:11 UTC: folder, inputs, drivers and the reading prepared before any run. Selftests: `read_lower.py` exit 0, `shift` and `round2` exit 1, `repeat_check.py`, `kc79_syscheck_1025.py` and `kc71_syscheck.py` exit 0 (`selftest_exits_pre.txt`; the drivers run them again). Dry run of `run_regrid.sh`: the pins, the worktree checks and lambda_0(20) = 2.1110019498 pass (`dry_steps_regrid.txt`; its first try stopped on my own bug, `python -I` hid the cwd from the lambda_0 import, and was fixed before any run).
- 2026-11-23 07:13:22 to 07:13:27 UTC: `run_regrid.sh` started as unit `i1025-k79d20r`; **STEP 1** source check ACCEPTED at 07:13:27: win2's k_c 71 D 20 record |F| 4.5262043273e-10, 2514 steps; this machine's state |F| 4.5297951007e-10 (+0.08%, inside the 1% bar), `freeze_from` 2514 steps; `--mutate=F` and `--mutate=steps` exit 1; the k_c 79 check refuses the source (exit 1); both selftests exit 0; lambda_0(20) recomputed 2.1110019498. (My message to t5 said the state's |F| equalled the record's; the exact numbers are these.) The regrid started 07:13:27.
- 2026-11-23 07:13:27 to 07:53:16 UTC: **STEP 2 regrid** (`ell_refine.py`, 8 threads, nice 10, unit `i1025-k79d20r`): exit 0, wall 2389 s (the record's step 2387 s), peak RSS 1.08 GiB (sampled every 60 s, 39 samples), no memory alert. 07:53:21 **ACCEPTED**: `kc79_syscheck_1025.py` exit 0 (|F| in the record class, `freeze_from` 2800 steps = the record's), `--mutate=F` and `--mutate=steps` exit 1. State `sol_l1kc79dh170d20_D20.0000.npy` blob e258e176, record `l1kc79dh170d20.jsonl` blob de8aa11b.
- **The regrid beside win2's** (Windows, Core Ultra 7 265K, 8 threads, 5273 s; raw 9e520757 and `I1025-win2/kc79_d20/`): |F| **4.4057739182e-10** against 4.4104844173e-10 (ratio 0.99893); steps **2800** against 2800 (equal); psi-constraint **2.1021859e-3** against 2.1020999e-3 (+8.6e-8); Delta **1.092259276533** against **1.092257255093** (dh170 minus win2: **+2.021e-6**); F at the start 2.8185648415e-5 against 2.8185648415e-5. Both from the k_c 71 source (|F| 4.5262043273e-10, 2514 steps, constraint 3.6653e-3, Delta 1.092269133460): Delta k_c 79 minus the source is -9.857e-6 here and -1.188e-5 at win2.
- 2026-11-23 07:53:32 UTC: **STEP 3 scan** started as unit `i1025-k79d20s` (4 processes of 1 thread, nice 10, 12 evaluations); all four print the record system (|F| 4.4056529223e-10 against the record's 4.4057739182e-10, 2800 steps equal).
- 2026-11-23 07:54:17 UTC: step 2 logged (this entry).

## Result (written 2026-11-23 10:39:31 UTC)
Steps 1 and 2 as logged (ACCEPTED 07:13:27 and 07:53:21 UTC). **Step 3:** unit `i1025-k79d20s` exit 0; processes p3, p0, p1, p2 exit 0 at 10:38:24, 10:38:53, 10:38:58 and 10:38:59 UTC; all four printed the record system (|F| 4.4056529223e-10 against the record's 4.4057739182e-10, 2800 steps equal); **12 of 12 evaluations noise-robust**; the repeat of 1.25 (the first on p1, the repeat last on p3) **bit-identical** (hybrid +1, ln|det| -2452.015688737278, float64 ln|det| -2450.3944602494494, noise [1, 1]; `repeat_check.py` PASS); `read_lower.py` selftest exit 0, `--mutate=shift` and `--mutate=round2` exit 1; reader exit 0 (`read_lower.txt`). Seconds per point 3250 to 3379 (three rounds side by side), wall 2:44:51 to 2:45:27 by /usr/bin/time; peak RSS 2.15 to 2.21 GiB (2257408 to 2314264 kB); lowest MemAvailable 22616 MiB = 22.1 GiB over 165 samples during the scan and 26.9 GiB (27503 MiB, 39 samples) during the regrid; no memory alert (`alert.log` does not exist).

**Hybrid signs, as printed, lambda 1.20 to 1.30: minus from 1.20 to 1.24, plus from 1.25 to 1.30; edge signs minus and plus.** One robust change, none touching a non-robust point:
| position | bracket | orientation as printed | det-linear estimate | estimator range |
|---|---|---|---|---|
| **the root near lambda_1's line, k_c 79, D 20, dh170 (Linux)** | (1.24, 1.25) | - to + | **1.246581** | [1.242925, 1.246581] |
The estimator range is the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure. No ln|det| minimum without a sign change in 1.20 to 1.30 (win2's one at 1.31, depth 0.0356, is outside this window). The float64 sign differs from the hybrid at 2 of 12 evaluations (1.23, 1.24; plus where the hybrid is minus). ln|det|: 1.20 -2445.6955, 1.21 -2446.7549, 1.22 -2447.9214, 1.23 -2449.2952, 1.24 -2451.3607, 1.25 -2452.0157, 1.26 -2451.9524, 1.27 -2452.4727, 1.28 -2453.2192, 1.29 -2454.0640, 1.30 -2454.7718.

**The regrid beside win2's** (the same k_c 71 source, 970fde73 / 8f86af85; win2: Windows, Core Ultra 7 265K, 8 threads, 5273 s; dh170: Linux, i7-7700, 8 threads, 2389 s):
| | dh170 | win2 |
|---|---|---|
| |F| | 4.4057739182e-10 | 4.4104844173e-10 (ratio 0.99893) |
| steps | 2800 | 2800 |
| psi-constraint | 2.1021859e-3 | 2.1020999e-3 |
| Delta | **1.092259276533** | **1.092257255093** (dh170 minus win2: **+2.021e-6**) |
**The root near lambda_1's line at D 20, by position:** dh170 (Linux) **1.246581** [1.242925, 1.246581]; win2 (Windows) **1.248340** [1.244440, 1.248340]; both in the bracket (1.24, 1.25). **The D 20 build spread, Linux minus Windows, is -0.001759** (the det-linear estimates; both on the same source and the same command). It is below the 0.003 to 0.03 that t5 wrote before the run. Earlier build comparisons of this root: 0.0032 at D 19.5 (macm3 against dh610, k_c 87) and 0.0136 at D 19.75 (macOS against Linux, k_c 87); here Linux against Windows at k_c 79, a different pair.

## Predictions against the result
| prediction | result |
|---|---|
| t5's, written before the run: one robust change in (1.20, 1.30), 0.003 to 0.03 from 1.248340 | one change in (1.24, 1.25); **0.001759 from 1.248340, below the bracket** |
| mine: source check passes with all four controls firing (95%); regrid accepted with both controls firing (85%); regrid 2200 to 3600 s (65%); steps equal to 2800 (45%); |F| within 5% of win2's (80%) | yes; yes; yes, 2389 s; yes, equal; yes, 0.1% |
| Delta within 1e-6 of win2's 1.092257255093 (50%) | **no**: +2.021e-6 |
| scan: every point noise-robust (75%); the repeat bit-identical (90%); exactly one robust change (85%) | yes, 12 of 12; yes; yes |
| distance from 1.248340: below 0.003 about 25%, 0.003 to 0.03 about 55%, above 0.03 about 10%; Linux below win2's (60%) | below 0.003 (the 25% case): 0.001759; Linux below: yes |
| the float64 sign differs from the hybrid at more than half the points (40%) | **no**: 2 of 12 |
| the scan 2.7 to 3.3 h (65%); peak RSS of a scan process below 3 GiB (85%) | yes, 2.75 h (2:44:51 to 2:45:27 each); yes, 2.21 GiB. My ETA to t5 (10:40 UTC) was 1 min after the end (10:38:59) |

## Log
- 2026-11-23 08:50 UTC: round 1 landed (1.20 to 1.23, all minus); 09:45: round 2 landed (partial reading 1.246581, reported to t5 and unchanged by round 3); 10:38:24 to 10:38:59 UTC: round 3 and the driver's reading finished.
- 2026-11-23 10:39:31 UTC: result written (this section).
