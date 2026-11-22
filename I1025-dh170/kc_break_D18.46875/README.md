# I1025-dh170/kc_break_D18.46875: #1025 bisecting the k_c break, the k_c 55 and k_c 63 states at D 18.46875 and their scans, lambda 1.62 to 1.80 at 0.01

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-22 06:48:32 UTC, before any run of this folder.
The first folder of this task, [../kc_break](../kc_break/README.md) (D 18.4375: k_c-stable), is the model for every script here.

## Order (the coordinator's hc, 22 Nov, after the D 18.4375 result), quoted
"Next task: your recommended task 2, the k_c test at D 18.46875, to bisect the break between D 18.4375 and 18.5. 1. Make the k_c 55 and k_c 63 states at D 18.46875 the way the D 18.4375 states were made (same tools, flags and acceptance check, including its controls), from the nearest accepted states. If a state does not converge or is not accepted, stop and report. 2. Then the two lanes as at D 18.4375 (d18_hybsign.py, lambda 1.62 to 1.80 at the same spacing, noise test, float64 sign, the 1.71 repeat), with the same fixed reading (each root matched within 0.01, unmatched changes, ln|det| minima), 8 h cap per lane. Post the commands, the window and the reading on #1025 before step 1 starts (raw I1025-dh170, new subfolder, README first). Keep your earlier thread budget and nice 10, and count t2d's i349 jobs against it. Report each state's time when it is accepted, and the result."

## Step 1: the states (`leap_kcbreak_dh170.sh 63` and `leap_kcbreak_dh170.sh 55`, side by side)
The D 18.4375 states are steps of `ell_leap.py` (blob 1eb873e4, the secant predictor through the two previous converged states, then lm with refrozen RK steps and a polish; flags `--tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold`; `kappa 0.7, u0 0.04, Ks 30` as the records; raw I1025-mac/d18/lane_d185L.sh, I1025-mac/leap_kc55_fold.log). Each lane runs, from `solver/matter` of the leap worktree `~/Source/choptuik-large-d-1025leap` (a new worktree at 505d8399, clean, the code of every earlier run; `ell_leap.py` writes into its `data/`):

    nice -n 10 python -u ell_leap.py l1kc63dh1025 1 63 sol_l1kc63Wm1025_D18.375000.npy 18.375 sol_l1kc63Wm1025_D18.437500.npy 18.4375 18.46875 0.03125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold
    nice -n 10 python -u ell_leap.py l1kc55dh1025 1 55 sol_l1kc55F1025_D18.375000.npy 18.375 sol_l1kc55F1025_D18.437500.npy 18.4375 18.46875 0.03125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold

- **Seeds** (the nearest accepted states below D 18.46875; the tool steps forward only, so D 18.5 cannot seed it): the Mac's leap states at D 18.375 and D 18.4375 for each k_c (blobs aa044592 and 16a17e5f for k_c 63, 6a1df3d6 and 2b886409 for k_c 55, taken from raw origin/main by `git cat-file blob` and checked against the tree). One step of h 0.03125 is half the seeds' spacing 0.0625, so the predictor extrapolates by half a seed spacing. A failed solve halves h once (to 0.015625, the tool's `--hmin`) and retries from the same seeds; a second failure ends the run with exit 1.
- **Acceptance** of a state, in this order: (1) the leap's own bars, |F| < 1e-8, psi-constraint <= 1e-2, no stop (the Mac's D 18.4375 states: |F| 2.7e-10 and constraint 1.8e-3 at k_c 63, 2.7e-10 and 2.8e-3 at k_c 55); (2) `accept_check.py` (new, 20 lines): the first lines of `d18_hybsign.py` alone, the state rebuilds its record row's discrete system, |F| within 1% of the record's and the same step count, which is the system check every scan starts with; the record row is the leap's own (a rebuild on this machine against a row the leap wrote on this machine). The scan repeats that check as its first line.
- **Controls of the acceptance, run first in each lane (a failure stops the lane):** the planted `ell_ddm.py selftest` PASS and `--mutate=slices` FAIL; `accept_check.py` on the Mac's D 18.4375 state with its own record row must exit 0 and with the D 18.5 row of the same record file must exit 3 ("NOT the record system"). Run now on both k_c, before the leaps (`ctl_accept.log`): all four as wanted (|F| 2.7869e-10 and 2.7110e-10 against 1.28e-3 for the planted mismatch). The bars `--fmax` and `--cmax` are the tool's; I do not mutate them (a mutated bar would cost two more solves, about the leap's time each).
- Caps: 3 h by exact pid for each leap (the Mac's leap steps from D 18.25 to D 18.5625 took 253 to 976 s with 4 threads), then the lane stops. The state, its record row and the log are copied into this folder and hashed; `pins_kc<k>.txt` holds the k_c, state blob and record blob the scan lane checks.

## Step 2: the scans (`lane_scan_dh170.sh 63` and `lane_scan_dh170.sh 55`, side by side, started only after both states are accepted)
Exactly as [../kc_break](../kc_break/README.md): the pins (state and record blobs from `pins_kc<k>.txt`, `d18_hybsign.py` e089207a, worktree `~/Source/choptuik-large-d-1025p4` at 505d8399 clean), the planted `ell_ddm.py selftest` and `--mutate=slices`, then `nice -n 10 /usr/bin/time -v python -u d18_hybsign.py REC STATE 18.46875 LAMS OUT`, 4 threads (OPENBLAS, OMP, MKL, VECLIB, RAYON = 4), an 8 h cap by exact pid, a memory sampler every 30 s (alert only). **The window:** lambda 1.71 first, then 1.62, 1.63, ..., 1.80 (19 points), then 1.71 last: 21 evaluations per lane. Each point: the hybrid sign (float64 blocks 0-11, dd block 12), the 1e-15 noise test on blocks 0-11 (2 seeds), the float64 sign beside it. `read_kcbreak.sh` after both lanes: `d18k2_read.py 18.46875 1.62 1.80 <k_c 55 scan> <k_c 63 scan>` (blob 52f31e53 with d185_scan_read 7c9d400f, d18c_read 1383470f, d18d_read 6b608903, unchanged; selftest 5 of 5 PASS and both mutations exit 1, `selftest_d18k2_read*.log`), then `repeat_check.py` (new) on each scan.
Where the roots should lie: k_c 63's first root, by the straight line between 1.692919 (D 18.4375) and 1.677209 (D 18.5), is 1.685064 at D 18.46875, in the bracket (1.68, 1.69). At D 18.4375 k_c 55's root was 1.695491 (+0.0026 from k_c 63's) and at D 18.5 k_c 55 has no root there (win2b's fine scan: a ln|det| minimum at 1.684 without a sign change).

## Reading, fixed now (the D 18.4375 reading, applied again)
The reader matches each k_c 63 robust change in 1.62 to 1.80 to the nearest robust k_c 55 change by det-linear estimate: within 0.01, **k_c-stable there**; else **k_c-dependent**. A k_c 55 change touching a non-robust point, or no robust k_c 63 change in the window, or a repeat that disagrees, gives no reading and the coordinator rules. Unmatched k_c 55 changes are listed. Every ln|det| minimum without a sign change, in either scan, gets the reader's dip fit (information). The float64 sign is reported beside the hybrid's (information). Each state reads its own signs and the signs are not compared.
**The branch verdict at D 18.46875** is read from the lambda_1 root, the k_c 63 change nearest 1.685 (the line above): k_c-stable there means **stable at D 18.46875** (the break lies in (18.46875, 18.5)); no k_c 55 change within 0.01 of it means **it breaks by D 18.46875** (in (18.4375, 18.46875)). Other k_c 63 changes (D 18.4375 had a second one at 1.791027) are matched the same way and reported; if one reads differently from the lambda_1 root the verdict is "mixed" and the coordinator rules. This choice of the lambda_1 root is mine: the coordinator's text says "each root matched within 0.01".

## Predictions, registered before the runs
- each leap reaches D 18.46875 in one step without halving h: k_c 63 about 90%, k_c 55 about 85%; both accepted by the checks above about 85%;
- Delta there, by the quadratic through the neighbours' Delta at D 18.4375 and D 18.5: k_c 63 1.0553016, k_c 55 1.0552647, each within 1e-5 about 90%; psi-constraint k_c 63 about 1.85e-3, k_c 55 about 2.86e-3 (each within 20% about 85%); |F| between 1e-11 and 1e-9 about 85%;
- seconds per leap, one process of 4 threads: 300 to 2400 s about 70%;
- scans: system check passes both about 95%; repeat check passes both about 90%; every point noise-robust: k_c 63 about 75%, k_c 55 about 70%;
- k_c 63: its lambda_1 root in (1.68, 1.69) about 70%; a second robust change in the window about 50%;
- the reading (the lambda_1 root; exclusive): stable about 45%; breaks with no k_c 55 root and a ln|det| minimum without a change about 30%; breaks with one k_c 55 change further than 0.01 about 10%; no reading (non-robust neighbour or other) about 15%;
- the float64 sign differs from the hybrid's at no more than 5 of 21 points: k_c 55 about 70%, k_c 63 about 30% (it was 11 of 21 at D 18.4375);
- wall of a scan: k_c 55 2.4 to 2.8 h and k_c 63 3.2 to 4.0 h about 65%; both inside the 8 h cap about 95%; max RSS below 2.5 GiB about 90%.

## Budget
Two processes of 4 threads each at nice 10 (as at D 18.4375), 8 threads on the 8 logical CPUs. The i349 jobs of t2d (`planted_dinf.py`, `reproduce_readme.py`) had ended when this was written (2026-11-22 06:48:32 UTC: no such process; load average 0.4). If they start again I count their threads against this and lower mine.

## Not done
No second route to the state (an interpolating predictor from D 18.4375 and D 18.5) and no mutated leap bar: a cross-check, not asked for. Cheap to add if the coordinator wants it.

## Log
- 2026-11-22 06:48:32 UTC: folder, scripts, controls and pins prepared; the commands, window and reading are fixed above before any run. Controls run: `ctl_accept.log` (4 of 4 as wanted), reader selftest PASS and both mutations FAIL, `repeat_check.py selftest` PASS.
- 2026-11-22 06:49:06 and 06:49:13 UTC: the two leaps started side by side (pids 1309918, 1310453), controls first: selftest PASS and mutate FAIL, accept_check exit 0 and 3, both k_c.
- 2026-11-22 07:21:25 UTC: **k_c 55 state accepted.** One step of ell_leap.py, h 0.03125, no halving; the leap's record row: |F| 2.6892152e-10 (F at the secant start 2.0e-5), 2153 steps, psi-constraint 2.8569e-3, Delta 1.0552647782 (the secant predictor 1.0552629), 1836 s in the step, 1926 s wall, max RSS 1.08 GiB. The rebuild by accept_check.py equals the record row to all printed digits. State `sol_l1kc55dh1025_D18.468750.npy` blob 567279bf, record `l1kc55dh1025.jsonl` blob 51a516f2.
- 2026-11-22 07:32:48 UTC: **k_c 63 state accepted.** One step, h 0.03125, no halving; |F| 2.7809094e-10 (secant start 2.0e-5), 2466 steps, psi-constraint 1.8442e-3, Delta 1.0553016757 (predictor 1.0552998), 2527 s in the step, 2619 s wall, max RSS 1.40 GiB. Rebuild equals the record row. State `sol_l1kc63dh1025_D18.468750.npy` blob 75a6b7d5, record `l1kc63dh1025.jsonl` blob c19b9501.
- 2026-11-22 07:33:17 and 07:33:20 UTC: the two scan lanes started (pins ok, planted selftest PASS and mutate FAIL, system check passes: k_c 63 |F| 2.7809094294e-10 against the record's, 2466 steps; k_c 55 2.6892152453e-10, 2153 steps), then `read_kcbreak.sh`. i349's `largeD_linear_poisson.py` (one thread, nice 19, started by t2d's agent) runs beside them; mine stay at 4 + 4 threads, nice 10, as at D 18.4375, which makes 9 threads on 8 CPUs with theirs yielding.
- 2026-11-22 07:33:53 UTC: results of step 1 written (this section).

## Step 1 against the predictions
| prediction | result |
|---|---|
| each leap reaches D 18.46875 in one step without halving (90%, 85%); both accepted (85%) | yes, yes; both accepted |
| Delta within 1e-5 of 1.0553016 (k_c 63) and 1.0552647 (k_c 55) (90%) | 1.0553016757 and 1.0552647782: 8e-8 each |
| psi-constraint within 20% of 1.85e-3 and 2.86e-3 (85%) | 1.844e-3 and 2.857e-3 |
| |F| between 1e-11 and 1e-9 (85%) | 2.78e-10 and 2.69e-10 |
| 300 to 2400 s per leap (70%) | k_c 55 1836 s yes; **k_c 63 2527 s no**, the two ran side by side (k_c 63's step ran 32 min beside k_c 55's) |

## Notes
- `accept_check.py`'s docstring was edited (one phrase) after its four controls (`ctl_accept.log`) ran and before the leaps; the code lines are unchanged. Its controls were repeated at the start of each leap lane (`ctl_leap_accept_kc*.log`: exit 0 and 3 as wanted).
- The record rows of both states are the leap's own, written on this machine; the Mac's D 18.4375 records were rebuilt here with |F| equal within 0.16%, and the new rows rebuild to the printed digits (same machine, same thread count).
- 2026-11-22 07:57 UTC: the terminal that owned both scan lanes and `read_kcbreak.sh` was closed (the coordinator: exit 129, SIGHUP) and all three died. Finished before that: k_c 63 one evaluation (lambda 1.71, 787 s), k_c 55 three (1.71, 1.62, 1.63, 504, 458 and 457 s); the evaluations in progress were lost. Their partial output (scan jsonl and raw, exits, time_pid, memlog, lane .out, selftest logs, the empty reader .out; 15 files) is kept in `killed_0757/`, nothing deleted. The two states were not touched.
- 2026-11-22 08:00:43 to 08:00:47 UTC: both lanes and the reader restarted from the start with the same scripts, arguments, threads (4 + 4) and nice 10, each as a systemd user unit (`i1025-kc63b`, `i1025-kc55b`, `i1025-readb`, started by `systemd-run --user --unit=... --working-directory=<this folder>`; the lanes under `systemd-inhibit --what=sleep`), so no terminal owns them. Both system checks again equal their records (k_c 63 |F| 2.7809094294e-10, 2466 steps; k_c 55 2.6892152453e-10, 2153), planted selftest PASS and mutate FAIL. 2026-11-22 08:01:25 UTC: this line written.

## Result of step 2 (written 2026-11-22 11:31:33 UTC)
Both lanes ran to the end in the rerun (units `i1025-kc55b`, `i1025-kc63b`, `i1025-readb`; the first run was killed at 07:57 UTC, see Log): 21 of 21 evaluations each, system check passed, every point noise-robust, the 1.71 repeats (first, middle, last) bit-identical in both scans (`repeat_check.py` PASS on both, the reader's own check on k_c 55 'agree'). Reader exit 0 at 11:30:31 UTC, output `kc_break_read.txt`.

| | k_c 55 | k_c 63 |
|---|---|---|
| started, ended (UTC), exit | 08:00:46, 10:41:08, 0 | 08:00:43, 11:30:18, 0 |
| wall | 9622 s (2:40:14 by /usr/bin/time) | 12575 s (3:29:29) |
| seconds per point | 400-579, mean 458 | 399-955, mean 598 (643-955 for the first 9 points beside the k_c 55 lane, about 400 after it ended) |
| max RSS, lowest MemAvailable | 1.08 GiB, 26.8 GiB | 1.42 GiB, 26.8 GiB |
| hybrid signs, 1.62 to 1.80 | -------++++++++---- (1.62-1.68 minus, 1.69-1.76 plus, 1.77-1.80 minus) | -------++++++++++++ (1.62-1.68 minus, 1.69-1.80 plus) |
| robust changes (det-linear estimate; estimator range = spread over the interpolation choices of d185_scan_read.changes, not an enclosure) | (1.68, 1.69): 1.687055 [1.686989, 1.687055]; (1.76, 1.77): 1.767385 [1.767385, 1.767820] | (1.68, 1.69): 1.684495 [1.684495, 1.684710]; none other |
| ln|det| minima without a sign change | none | none |
| float64 sign differs from the hybrid | 0 of 21 | 4 of 21 (plus from 1.65 to 1.68: a spurious change in (1.64, 1.65)) |

**Reading, as fixed: k_c-stable at D 18.46875.** The lambda_1 root (the k_c 63 change nearest 1.685): k_c 63 1.684495, k_c 55 1.687055 (+0.002560, within 0.01). The break therefore lies in (18.46875, 18.5). The estimator ranges leave the gap between +0.00228 and +0.00256. The signs are each state's own and are not compared.
- Unmatched k_c 55 change: 1.767385 (the second root family). k_c 63 has no change in 1.69 to 1.80 (plus throughout), so by the fixed reading (each k_c 63 root matched) nothing unmatched on the k_c 63 side; the pair of second roots, k_c 63 at 1.791027 and k_c 55 at 1.784813 at D 18.4375, are now at least 0.033 apart: k_c 55's moved down 0.0174, k_c 63's is not in the window (above 1.80 or gone). Information, outside the reading; the window cannot say which.
- The k_c 55 minus k_c 63 gap at the lambda_1 root: +0.002573 at D 18.4375, +0.002560 at D 18.46875 (det-linear estimates, 0.01 grid). k_c 63's root path: 1.692919 (D 18.4375), 1.684495 (D 18.46875, det-linear), 1.677209 (D 18.5, bisected root, comment 7070186508). At D 18.5 k_c 55 has no root there. So the k_c 55 root keeps its offset up to D 18.46875 and is gone at D 18.5.
- The 0.01 grid cannot exclude two more k_c 55 roots inside (1.68, 1.69): an odd count of changes shows one, not how many.

**Rerun against the killed run:** the killed run's four finished points (k_c 55: 1.71, 1.62, 1.63; k_c 63: 1.71, in `killed_0757/`) equal the rerun's, sign, ln|det|, float64 ln|det| and noise signs, bit for bit (checked on the jsonl).

## Step 2 against the predictions
| prediction | result |
|---|---|
| system check passes both (95%); repeat check passes both (90%) | yes; yes |
| every point noise-robust: k_c 63 (75%), k_c 55 (70%) | yes, yes |
| k_c 63's lambda_1 root in (1.68, 1.69) (70%) | yes, 1.684495 (the straight line gave 1.685064) |
| a second robust change in the window at k_c 63 (50%) | **no**: none; the second root left the window |
| reading: stable 45%, breaks with a minimum without a change 30%, breaks with a further change 10%, no reading 15% | stable |
| float64 differs at no more than 5 of 21: k_c 55 (70%), k_c 63 (30%) | k_c 55 yes (0); k_c 63 yes (4) |
| wall: k_c 55 2.4 to 2.8 h, k_c 63 3.2 to 4.0 h (65%); inside the 8 h cap (95%); RSS below 2.5 GiB (90%) | 2.67 h yes; 3.49 h yes; yes; 1.08 and 1.42 GiB yes |
- 2026-11-22 11:31:33 UTC: step 2 written (this section); the rerun's points equal the killed run's.
