# I1025-dh170/kc71_scout: #1025 lambda_1 on win2's k_c 71 scout leg (leg 4's D 21.0 state, then leg 6's newest)

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-24 01:03:44 UTC, before any run of this folder. Raw origin/main when the inputs were taken: a2d42e42.

## Order (the coordinator t5's #1025 comment 7118664707 and hc, 24 Nov), quoted in part
"**Task for dh170: lambda_1 on the k_c 71 scout leg.** dh170's k_c 87 at D 20.90625 (raw a2d42e42) is 0.938363, +0.00013 from k_c 79. So k_c 79 resolves lambda_1 at the leg's far end (`ell1_best.csv`, main e3c78d20). win2's k_c 71 leg 6 runs ahead of the k_c 79 leap (D 21.15625 at 00:15, against 21.0). **Runs** (8 threads, nice 10; raw `I1025-dh170/kc71_scout/`, README first; the leg's states pinned by blob from raw `I1025-win2/kc71_leap/`; `kc71_syscheck` accepts each on Linux, controls exit 1): 1. **Calibration:** leg 4's D 21.0 state (tag l1kc71Lw1025c). `d18_hybsign` at 0.890-0.920 by 0.005 (7 points), `read_lower`. Compared with dh610's k_c 79 reading at D 21.0 (due ~01:50; I relay it), this measures the k_c 71 -> 79 step here. 2. **The scout point:** leg 6's newest state when step 1 ends (D 21.1875 or later). Seven points at 0.005 around the k_c 79 track's trend (lambda_1 ~ 0.908 - 0.30 (D - 21.0)) shifted by step 1's k_c step, plus a repeat of the middle point. **Written before:** k_c 71 - k_c 79 at D 21.0 is -0.003 +- 0.003 (at D 19 it was -0.0031); the scout point lies within 0.01 of the trend shifted by that step. **Estimate:** about 1.3 h per point at 4 processes, about 3 h in all."
Roots are read by position, never by sign orientation (t5). No regrid in this task: the states are win2's, pinned by blob, and accepted here by `kc71_syscheck.py`.

## Layout
`s1/` (calibration) and `s2/` (scout) are the two stages; each holds `in/` (pinned copies), `in_blobs.txt`, `stage.conf`, `steps.txt`, `VERDICT.txt` and the outputs. `run_accept.sh <stage>` (the check only; no regrid) and `run_scan.sh <stage>` are shared. `s2/` is created when step 1 ends, from leg 6's newest state at that time; its pins are logged here before its scan.

## Inputs of stage s1 (copies in `s1/in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs and the drivers refuse any other blob)
| item | raw path | blob |
|---|---|---|
| win2's k_c 71 leg 4 state at D 21.0 (tag `l1kc71Lw1025c`), commit 3f52168a "leg 4 ended at D 21.0, state D 21.0 and the final record file"; the raw file `sol_l1kc71Lw1025c_D21.000000.npy` is also `_D21.0000.npy` and `_last.npy` (the same blob) | I1025-win2/kc71_leap/states/sol_l1kc71Lw1025c_D21.000000.npy | b18381af |
| its record file at that commit: 20 rows, D 20.0625 to 21.0; the D 21.0 row: |F| 4.702802288437e-10, 2405 steps, psi-constraint 7.3207e-3, Delta 1.118296630104, h 0.03125, F at the start 1.0379e-5, kappa 0.7, u0 0.04, Ks 30 | I1025-win2/kc71_leap/states/l1kc71Lw1025c.jsonl | 2c985057 |
| the k_c 71 check (the check of every D 20.x task); the k_c 79 check (it must refuse a k_c 71 state) | I1025-win2/kc71_leap/kc71_syscheck.py; I1025-win/kc79_d19/kc79_syscheck_1025.py | 4cd86cd4; 29dce7ea |
| the scanner, unmodified; its change finder | I1025-mac/d18/d18_hybsign.py; d185_scan_read.py | e089207a; 7c9d400f |
| reader (mine); `repeat_check.py` (dh610's) | I1025-dh170/lower_root/read_lower.py; I1025-dh610/kc71_d19125/in/repeat_check.py | 89309d3c; aaf598a9 |
Code: the worktree of the earlier tasks, unchanged: `~/Source/choptuik-large-d-1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's), python `~/Source/choptuik-large-d-1058b/.venv` (3.14.10, multidouble 5.1.0, avx2). The state and record are copied into the worktree's `solver/matter/data/` (blob checked) by `run_accept.sh`, where the scan's code reads them.
**Leg 6** (for stage s2): tag `l1kc71Lw1025e`, raw `I1025-win2/kc71_leap/states/`, states D 21.03125, 21.0625, 21.09375, 21.125, 21.15625 at 23 Nov 16:14 (-0800) = 00:14 UTC (state blob fc671a6f, record aa9ba301 at commit cf1027e2); D 21.1875 or later is pinned when step 1 ends.

## Reference numbers (information, not a pass rule)
- **The k_c 71 to k_c 79 step on lambda_1 at D 19** (winb, Windows; t5): 1.536547 (k_c 71) and 1.539658 (k_c 79): **-0.0031**. At D 20.5 t5 gives the k_c 71 to k_c 79 step as 0.00013. **The k_c 79 and k_c 87 track** near the leg's far end: dh610's k_c 79 at D 20.90625 0.938234; my k_c 87 0.938363 (+0.000129); t5's trend for k_c 79: lambda_1 ~ 0.908 - 0.30 (D - 21.0). dh610's k_c 79 reading at D 21.0 is relayed by t5 (due about 01:50 UTC) and recorded here when it arrives.
- **Cost of a k_c 71 point:** not measured at D 21 here; my earlier k_c 71 scans used 4 threads per evaluation. A k_c 79 point took about 3250 s (D 20.5) and a k_c 87 point about 4700 s (D 20.9) with four single-thread processes side by side. With 7 or 8 single-thread processes on this machine's 4 cores each point runs about 1.4 times slower than with four.

## Commands (systemd user units, so no terminal owns them)
**Source check** (`run_accept.sh s1`, unit `i1025-k71s1a`, short): pins; selftests of `kc71_syscheck.py` and `kc79_syscheck_1025.py` (exit 0); `kc71_syscheck.py` accepts the state and record (exit 0; `--mutate=F` and `--mutate=steps` exit 1); `kc79_syscheck_1025.py` refuses them (exit 1); writes `s1/VERDICT.txt`.
**Scan** (`run_scan.sh s1`, unit `i1025-k71s1s`, after VERDICT ACCEPTED): `d18_hybsign.py` on the accepted state at D 21.0, lambda 0.890, 0.895, ..., 0.920 (7 points), **one process of 1 thread per point (7 processes, nice 10, 7 of the 8 threads)**, one round. The order has no repeat in step 1 (the repeat of step 2 is the run-to-run control). Then `read_lower.py in/... scan 0.890 0.920`, its selftest and both mutations.
**Step 2** (`run_accept.sh s2`, `run_scan.sh s2`, units `i1025-k71s2a`, `i1025-k71s2s`): the same on leg 6's newest state, **8 processes of 1 thread (8 threads)**, one round. **The grid rule fixed now:** c = 0.908 - 0.30 (D - 21.0) + s, with D the D of the pinned leg 6 state and s = (my step 1 det-linear estimate at D 21.0) - (dh610's k_c 79 det-linear estimate at D 21.0); m = c rounded to the nearest 0.005; the 7 values m-0.015, m-0.010, ..., m+0.015 and a repeat of m (8 evaluations; the repeat on another process than the first m); `read_lower.py scan m-0.015 m+0.015`. The lists are written to `s2/stage.conf` and logged below before the scan starts.

## Acceptance (the order's, fixed before the run; per stage)
1. **Source.** `kc71_syscheck.py` accepts the state and record on this machine (|F| at most 1e-9, `freeze_from` gives the record's steps, |F| within 1%), `--mutate=F` and `--mutate=steps` exit 1, both selftests exit 0, and `kc79_syscheck_1025.py` refuses the state (exit 1). Otherwise no scan.
2. **Scan.** Each process prints the record system; `read_lower.py` selftest exit 0, mutations `shift` and `round2` exit 1; in step 2 the repeat of m agrees (sign, ln|det| within 1e-6, noise signs, float64 sign). A stop at any step: I report and change nothing.

## Reading, fixed now (by position)
Every robust change (both neighbouring points noise-robust) with bracket (0.005 wide), det-linear estimate and estimator range (the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure), orientation as printed (information); the edge signs; changes touching a non-robust point listed and not counted; every ln|det| minimum without a sign change flagged; the repeat's bits. **Step 1:** the k_c 71 estimate at D 21.0 minus dh610's k_c 79 estimate at D 21.0 is the k_c step s, quoted with both brackets and ranges. **Step 2:** the scout estimate minus c (the trend shifted by s) is the scout's offset. **Written before (t5's):** s = -0.003 +- 0.003; the scout point within 0.01 of c.

## Predictions, registered before the runs (mine, information)
- **Step 1.** `kc71_syscheck.py` accepts leg 4's D 21.0 state on Linux with all four controls firing about 90%. Every point noise-robust about 70%; exactly one robust change in 0.890 to 0.920 about 85% (none about 8%, two or more about 7%), in (0.900, 0.905) about 40% and (0.905, 0.910) about 40%; s in [-0.006, 0.000] about 55% (t5's -0.003 +- 0.003), within 0.01 of zero about 85%; edge signs unequal about 85%; the float64 sign differs from the hybrid at more than half the points about 30%; the scan 0.7 to 1.4 h about 65% (t5: about 1.3 h per point at four processes); peak RSS of a scan process below 2.5 GiB about 85%.
- **Step 2.** The scout state is accepted with all controls firing about 90%; exactly one robust change in the window about 80%; its estimate within 0.01 of c about 75% (t5's), within 0.005 about 55%; the repeat of m bit-identical about 90%; every point noise-robust about 70%; the scan 0.8 to 1.7 h about 65%.

## Budget
One round of 7 (step 1) or 8 (step 2) single-thread processes at nice 10; nothing else of mine runs. Memory: alert only (`alert.log` if MemAvailable falls below 2048 MiB; nothing is stopped for memory). Estimate: step 1 about 1.0 h (ends about 02:15 UTC), step 2 about 1.2 h after it; about 2.5 h in all (t5: about 3 h).

## Log
- 2026-11-24 01:03:44 UTC: folder, inputs, drivers and the reading prepared before any run. Selftests: `read_lower.py` exit 0, `shift` and `round2` exit 1, `repeat_check.py`, `kc71_syscheck.py` and `kc79_syscheck_1025.py` exit 0 (`s1/selftest_exits_pre.txt`; the drivers run them again). Dry run of `run_accept.sh s1`: the pins and the worktree checks pass (`s1/dry_steps_accept.txt`). The drivers are those of `d19_lower` (accept) and `kc87_d2090625` (scan), made stage-based; the scan driver was tested there.
- 2026-11-24 01:03:58 to 01:04:03 UTC: **STEP 1 source check** (`run_accept.sh s1`, unit `i1025-k71s1a`) ACCEPTED at 01:04:03: win2's k_c 71 leg 4 record |F| 4.7028022884e-10, 2405 steps, constraint 7.321e-3, Delta 1.118296630104 (2897 s on win2); this machine's state |F| 4.7037820754e-10 (+0.021% against the record, inside the 1% bar), `freeze_from` 2405 steps = the record's; `--mutate=F` and `--mutate=steps` exit 1; the k_c 79 check refuses the state (exit 1: "the record is not k_c 79 at D 21 (kc 71, D 21.0)"); both selftests exit 0; the state and record copied to `s1/` and to the worktree's `data/` (blob checked). 01:04:10 UTC: **the step 1 scan** started as unit `i1025-k71s1s` (7 processes of 1 thread, nice 10, lambda 0.890 to 0.920 by 0.005, one point per process); all seven print the record system (|F| 4.7059833435e-10 against the record's 4.7028022884e-10, 2405 steps equal), each at about 98% CPU.
- 2026-11-24 01:23:16 UTC: **dh610's k_c 79 reading at D 21.0 received** (t5's hc, 01:22 UTC): one robust change, bracket (0.905, 0.910), det-linear **0.909538**, estimator range [0.909234, 0.909538]. For the step 2 rule fixed above: s = (my step 1 det-linear estimate) - 0.909538, and c = 0.908 - 0.30 (D - 21.0) + s with t5's trend constant 0.908 as written. (Anchoring the trend on dh610's 0.909538 instead of 0.908 would move c by +0.0015; both are logged with the lists; the window of 0.030 covers either.) Nothing else changes.

## Result of step 1 (calibration, written 2026-11-24 02:25:24 UTC)
**Source:** ACCEPTED 01:04:03 UTC (logged above). **Scan** (unit `i1025-k71s1s`, 7 processes of 1 thread, nice 10; 01:04:10 to 02:24:45 UTC, 4835 s): exit 0 for all seven (02:21:32 to 02:24:45 UTC); all printed the record system (|F| 4.7059833435e-10 against the record's 4.7028022884e-10, 2405 steps equal); **7 of 7 noise-robust**; `read_lower.py` selftest exit 0, `--mutate=shift` and `--mutate=round2` exit 1; reader exit 0 (`s1/read_lower.txt`); no repeat (the order has none). Seconds per point 4638 to 4830 (one round of seven processes on this machine's 4 cores); wall per process 1:17:22 to 1:20:34; peak RSS 1.39 to 1.49 GiB; lowest MemAvailable 20.9 GiB (80 samples); no memory alert (`alert.log` does not exist).

**Hybrid signs, as printed, lambda 0.890 to 0.920:** minus at 0.890, 0.895, 0.900; plus at 0.905, 0.910, 0.915, 0.920 (the float64 sign equals the hybrid at all 7). **One robust change**, none touching a non-robust point, no ln|det| minimum without a sign change:
| root | bracket | orientation as printed | det-linear estimate | estimator range |
|---|---|---|---|---|
| **k_c 71, D 21.0, dh170 (Linux)** | (0.900, 0.905) | - to + | **0.901815** | [0.901371, 0.901815] |
| k_c 79, D 21.0, dh610 (Linux) | (0.905, 0.910) | | **0.909538** | [0.909234, 0.909538] |
| **s = k_c 71 minus k_c 79 at D 21.0** | different 0.005 cells | | **-0.007723** | |
The estimator range is the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure; the bracket is the 0.005 grid step. ln|det|: 0.890 -2006.1858, 0.895 -2007.0941, 0.900 -2008.9213, 0.905 -2008.3593, 0.910 -2007.8148, 0.915 -2007.6886, 0.920 -2007.7089. **t5's written prediction (s = -0.003 +- 0.003, that is -0.006 to 0.000): not met**; s = -0.0077 is 0.0017 below the lower edge. At D 19 the step was -0.0031 (winb, Windows; t5), at D 20.5 0.00013 in the other direction (t5's figure for the k_c 71 to 79 step); the step here is larger than at both. Both estimates are from Linux builds (dh610's and mine).

## Predictions against the result (step 1)
| prediction | result |
|---|---|
| t5's, written before the run: s = -0.003 +- 0.003 | **not met**: -0.007723 |
| mine: `kc71_syscheck.py` accepts with all four controls firing (90%) | yes (state |F| +0.021% of the record's, `freeze_from` 2405 = 2405) |
| every point noise-robust (70%); exactly one robust change (85%), in (0.900, 0.905) (40%) | yes, 7 of 7; yes; yes |
| s in [-0.006, 0.000] (55%); within 0.01 of zero (85%) | **no**; yes |
| edge signs unequal (85%); the float64 sign differs from the hybrid at more than half the points (30%) | yes; no (0 of 7) |
| the scan 0.7 to 1.4 h (65%); peak RSS below 2.5 GiB (85%) | yes, 1.34 h; yes, 1.49 GiB. My ETA to t5 (02:15 to 02:30 UTC) held (02:24:45) |

## Stage s2 pins and lists, recorded before the step 2 check and scan (2026-11-24 02:26:07 UTC)
**Leg 6's newest state when step 1 ended (02:24:45 UTC): D 21.21875**, win2's commit 51f62d5a ("leg 6 state D 21.21875 (tag l1kc71Lw1025e)", 23 Nov 17:53 -0800 = 01:53 UTC), tag `l1kc71Lw1025e`: state `I1025-win2/kc71_leap/states/sol_l1kc71Lw1025e_D21.218750.npy` blob **ab4da272** (also `_last.npy`; here `s2/in/sol_l1kc71Lw1025e_D21.2188.npy`, ell_refine's `D{D:.4f}`), record `l1kc71Lw1025e.jsonl` blob **c826dedc** (7 rows, D 21.03125 to 21.21875; the D 21.21875 row: |F| 4.519145845379e-10, 2390 steps, psi-constraint 8.41924e-3, Delta 1.124176728865, F at the start 1.02624e-5, h 0.03125). The checks and scripts are those of `s1/in` (same blobs).
**The rule applied** (fixed above): s = 0.901815 - 0.909538 = **-0.007723** (my step 1 estimate minus dh610's k_c 79 estimate at D 21.0); c = 0.908 - 0.30 (21.21875 - 21.0) + s = 0.908 - 0.065625 - 0.007723 = **0.834652**; **m = 0.835** (anchored on dh610's 0.909538 instead of 0.908, c would be 0.836190 and m the same, 0.835). **Lists:** lambda 0.820, 0.825, 0.830, 0.835, 0.840, 0.845, 0.850 and a repeat of 0.835: 8 evaluations, **one single-thread process each (8 processes, 8 threads, nice 10, one round)**; the first 0.835 is process 3, the repeat process 7; window read `read_lower.py scan 0.820 0.850`. `s2/stage.conf` has them (checked by a script against the rule). **Predictions of step 2 stand as written above** (the scout within 0.01 of c = 0.834652: about 75%, within 0.005 about 55%). The k_c step I measured, -0.0077, is larger than t5's written -0.003 +- 0.003; the shifted trend uses the measured one, as the order says.
- 2026-11-24 02:26:11 to 02:26:16 UTC: **STEP 2 source check** (`run_accept.sh s2`, unit `i1025-k71s2a`) ACCEPTED at 02:26:16: win2's k_c 71 leg 6 record |F| 4.5191458454e-10, 2390 steps, constraint 8.419e-3, Delta 1.124176728865 (2450 s on win2); this machine's state |F| 4.5215381242e-10 (+0.053% against the record, inside the 1% bar), `freeze_from` 2390 steps = the record's; `--mutate=F` and `--mutate=steps` exit 1; the k_c 79 check refuses the state (exit 1: "the record is not k_c 79 at D 21.2188 (kc 71, D 21.21875)"); both selftests exit 0; the state and record copied to `s2/` and to the worktree's `data/` (blob checked). 02:26:23 UTC: **the step 2 scan** started as unit `i1025-k71s2s` (8 processes of 1 thread, nice 10, the lists above); all eight print the record system (|F| 4.5209699397e-10 against the record's 4.5191458454e-10, 2390 steps equal), each at about 94% CPU.

## Result of step 2 (the scout point, written 2026-11-24 04:06:56 UTC)
**Source:** ACCEPTED 02:26:16 UTC (logged above). **Scan** (unit `i1025-k71s2s`, 8 processes of 1 thread, nice 10; 02:26:23 to 04:06:27 UTC, 6004 s): exit 0 for all eight (04:05:52 to 04:06:27 UTC); all printed the record system (|F| 4.5209699397e-10 against the record's 4.5191458454e-10, 2390 steps equal); **8 of 8 noise-robust**; the repeat of 0.835 (the first on process 3, the repeat on process 7) **bit-identical** (hybrid +1, ln|det| -1984.3260648686567, float64 ln|det| -1983.248030561914, noise [1, 1]; `repeat_check.py` PASS); `read_lower.py` selftest exit 0, `--mutate=shift` and `--mutate=round2` exit 1; reader exit 0 (`s2/read_lower.txt`). Seconds per point 5963 to 5999 (eight processes on this machine's 4 cores, one round); wall per process 1:39:29 to 1:40:04; peak RSS 1.37 to 1.44 GiB; lowest MemAvailable 19.8 GiB (99 samples); no memory alert (`alert.log` does not exist).

**Hybrid signs, as printed, lambda 0.820 to 0.850:** minus at 0.820, 0.825, 0.830; plus at 0.835, 0.840, 0.845, 0.850. **One robust change**, none touching a non-robust point, no ln|det| minimum without a sign change:
| root | bracket | orientation as printed | det-linear estimate | estimator range |
|---|---|---|---|---|
| **k_c 71, D 21.21875, dh170 (Linux), the scout point** | (0.830, 0.835) | - to + | **0.832037** | [0.831557, 0.832037] |
The float64 sign differs from the hybrid at 0.835 and 0.845 (float64 reads minus there; 3 of the 8 evaluations, counting the repeat). ln|det|: 0.820 -1982.0705, 0.825 -1982.9681, 0.830 -1984.7005, 0.835 -1984.3261, 0.840 -1983.7506, 0.845 -1983.6190, 0.850 -1983.6386.
**Against the shifted trend:** c = 0.834652 (the k_c 79 trend 0.908 - 0.30 (D - 21.0), shifted by s = -0.007723). **The scout minus c is -0.002615**: inside t5's written 0.01 and inside my 0.005. Against the unshifted trend (0.842375) the scout is -0.010338 (just outside 0.01, which is why the shift matters). The measured k_c 71 slope from D 21.0 (0.901815) to D 21.21875 (0.832037) is **-0.31899 per unit D** (the trend's -0.30).

## Predictions against the result (step 2)
| prediction | result |
|---|---|
| t5's, written before the run: the scout point within 0.01 of the trend shifted by step 1's k_c step | **met**: -0.002615 from c = 0.834652 |
| mine: the scout state accepted by `kc71_syscheck.py` with all four controls firing (90%) | yes (state |F| +0.053% of the record's, `freeze_from` 2390 = 2390) |
| exactly one robust change in the window (80%); its estimate within 0.01 of c (75%), within 0.005 (55%) | yes; yes; yes (-0.002615) |
| the repeat of 0.835 bit-identical (90%); every point noise-robust (70%) | yes; yes, 8 of 8 |
| the scan 0.8 to 1.7 h (65%) | yes, 1.67 h (just inside; I expected 03:50 UTC and it ended 04:06:27, eight processes on four cores cost more CPU time per point than step 1's seven) |

## Task summary
| | k_c 71 (dh170, Linux) | k_c 79 (dh610, Linux) | k_c 71 minus k_c 79 |
|---|---|---|---|
| D 21.0 | 0.901815 (0.900, 0.905) | 0.909538 (0.905, 0.910) | **-0.007723** (t5 wrote -0.003 +- 0.003: not met) |
| D 21.21875 | **0.832037** (0.830, 0.835) | not scanned | the trend shifted by that step puts it at 0.834652: **-0.002615** (t5 wrote within 0.01: met) |
Information: the two Linux builds give the k_c 71 and k_c 79 roots at D 21.0; the k_c 71 root falls at -0.319 per unit D from D 21.0 to D 21.21875, a little steeper than the -0.30 of the k_c 79 trend. No raw output of this task lives outside this folder. Nothing of mine is running on dh170.

## Log
- 2026-11-24 02:26 UTC: step 2 scan started; 04:05:52 to 04:06:27 UTC: finished and read. 2026-11-24 04:06:56 UTC: result written (this section).
