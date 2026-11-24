# I1025-dh170/kc71_d2128125: #1025 lambda_1 on win2's k_c 71 leg 6 at D 21.28125

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-24 04:08:54 UTC, before any run of this folder. Raw origin/main when the inputs were taken: 8f9b7159.

## Order (the coordinator t5's hc, 24 Nov), quoted in full
"Coordinator (t5): step 2 accepted (raw 8f9b7159), recorded as a k_c 71 scout value. Next, the same pipeline: leg 6's D 21.28125 state (win2 raw 2f39b042: state c1687fc0, record 7c4af06f, tag l1kc71Lw1025e; pin by blob; kc71_syscheck accept, controls exit 1): d18_hybsign at 0.795-0.825 by 0.005 plus a repeat of 0.810 (8 processes), read_lower. Written before (README first): one change within 0.01 of 0.8117 (winb's D 21.25 k_c 71 value 0.8217 - 0.32 x 0.03125). winb takes D 21.3125. Raw I1025-dh170/kc71_d2128125/."
Roots are read by position, never by sign orientation (t5). No regrid in this task.

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs and the drivers refuse any other blob)
| item | raw path | blob |
|---|---|---|
| win2's k_c 71 leg 6 state at D 21.28125 (tag `l1kc71Lw1025e`), commit 2f39b042 "leg 6 state D 21.28125"; the raw file `sol_l1kc71Lw1025e_D21.281250.npy` is also `_last.npy` (the same blob). Here it is `sol_l1kc71Lw1025e_D21.2812.npy` (ell_refine's `D{D:.4f}`) | I1025-win2/kc71_leap/states/sol_l1kc71Lw1025e_D21.281250.npy | c1687fc0 |
| its record file at that commit: 9 rows, D 21.03125 to 21.28125; the D 21.28125 row: |F| 4.458142231040e-10, 2384 steps, psi-constraint 8.75767e-3, Delta 1.125866383799, h 0.03125, F at the start 1.02318e-5, kappa 0.7, u0 0.04, Ks 30 | I1025-win2/kc71_leap/states/l1kc71Lw1025e.jsonl | 7c4af06f |
| the k_c 71 check; the k_c 79 check (it must refuse a k_c 71 state) | I1025-win2/kc71_leap/kc71_syscheck.py; I1025-win/kc79_d19/kc79_syscheck_1025.py | 4cd86cd4; 29dce7ea |
| the scanner, unmodified; its change finder | I1025-mac/d18/d18_hybsign.py; d185_scan_read.py | e089207a; 7c9d400f |
| reader (mine); `repeat_check.py` (dh610's) | I1025-dh170/lower_root/read_lower.py; I1025-dh610/kc71_d19125/in/repeat_check.py | 89309d3c; aaf598a9 |
Code: the worktree of the earlier tasks, unchanged: `~/Source/choptuik-large-d-1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's), python `~/Source/choptuik-large-d-1058b/.venv` (3.14.10, multidouble 5.1.0, avx2). `run_accept.sh` copies the state and record into the worktree's `solver/matter/data/` (blob checked), where the scan's code reads them. The drivers are those of `../kc71_scout`, made flat.

## Reference numbers (information, not a pass rule)
- **The k_c 71 root on leg 6 so far:** my D 21.0 (leg 4) 0.901815 (bracket (0.900, 0.905)); my D 21.21875 **0.832037** (bracket (0.830, 0.835), range [0.831557, 0.832037]); winb's D 21.25 (Windows, t5) **0.8217**. The slope between winb's D 21.25 and my D 21.21875 is -0.331 per unit D; mine from D 21.0 to 21.21875 is -0.319.
- **The two extrapolations to D 21.28125:** t5's 0.8217 - 0.32 x 0.03125 = **0.8117**; mine from my own point and my own slope: 0.832037 - 0.31899 x 0.0625 = **0.8121**. The window 0.795 to 0.825 is centered on 0.810.
- **Cost of a point:** 5963 to 5999 s with eight single-thread processes on this machine's 4 cores (the D 21.21875 scan); 4638 to 4830 s with seven (D 21.0).

## Commands (systemd user units, so no terminal owns them)
**Source check** (`run_accept.sh`, unit `i1025-k71d281a`, short): pins; selftests of `kc71_syscheck.py` and `kc79_syscheck_1025.py` (exit 0); `kc71_syscheck.py` accepts the state and record (exit 0; `--mutate=F` and `--mutate=steps` exit 1); `kc79_syscheck_1025.py` refuses them (exit 1); writes `VERDICT.txt`.
**Scan** (`run_scan.sh`, unit `i1025-k71d281s`, after VERDICT ACCEPTED): `d18_hybsign.py` on the accepted state at D 21.28125, lambda 0.795, 0.800, 0.805, 0.810, 0.815, 0.820, 0.825 and a repeat of 0.810, **one process of 1 thread per evaluation (8 processes, 8 threads, nice 10), one round**; the first 0.810 is process 3, the repeat process 7 (`stage.conf` has the lists, checked by a script). Then `read_lower.py in/... scan 0.795 0.825`, its selftest and both mutations, and `repeat_check.py`.

## Acceptance (fixed before the run)
1. **Source.** `kc71_syscheck.py` accepts the state and record on this machine (|F| at most 1e-9, `freeze_from` gives 2384, |F| within 1%), `--mutate=F` and `--mutate=steps` exit 1, both selftests exit 0, and `kc79_syscheck_1025.py` refuses the state (exit 1). Otherwise no scan.
2. **Scan.** Each process prints the record system; `read_lower.py` selftest exit 0, mutations `shift` and `round2` exit 1; the repeat of 0.810 agrees (sign, ln|det| within 1e-6, noise signs, float64 sign). A stop at any step: I report and change nothing.

## Reading, fixed now (by position)
Every robust change (both neighbouring points noise-robust) with bracket (0.005 wide), det-linear estimate and estimator range (the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure), orientation as printed (information); the edge signs; changes touching a non-robust point listed and not counted; every ln|det| minimum without a sign change flagged; the repeat's bits. **Written before (t5's):** one change within 0.01 of 0.8117, read on the det-linear estimate; the offset from 0.8117 and from my own extrapolation 0.8121 are both quoted.

## Predictions, registered before the runs (mine, information)
`kc71_syscheck.py` accepts the state on Linux with all four controls firing about 90%. Every point noise-robust about 75%; exactly one robust change in the window about 85% (none about 7%, two or more about 8%); its estimate within 0.01 of 0.8117 about 85%, within 0.005 about 65%, within 0.003 of my 0.8121 about 55%; edge signs unequal about 85%; the repeat of 0.810 bit-identical about 90%; the float64 sign differs from the hybrid at more than half the points about 25% (D 21.0: 0 of 7; D 21.21875: 3 of 8); the scan 1.5 to 1.9 h about 65% (D 21.21875: 1.67 h with the same eight processes); peak RSS of a scan process below 2 GiB about 90%.

## Budget
One round of 8 single-thread processes at nice 10 (all of this machine's threads); nothing else of mine runs. Memory: alert only (`alert.log` if MemAvailable falls below 2048 MiB; nothing is stopped for memory). Estimate: about 1.7 h in all (ends about 06:00 UTC).

## Log
- 2026-11-24 04:08:54 UTC: folder, inputs, drivers and the reading prepared before any run. Selftests: `read_lower.py` exit 0, `shift` and `round2` exit 1, `repeat_check.py`, `kc71_syscheck.py` and `kc79_syscheck_1025.py` exit 0 (`selftest_exits_pre.txt`; the drivers run them again). Dry run of `run_accept.sh`: the pins and the worktree checks pass (`dry_steps_accept.txt`). The drivers are those of `../kc71_scout` made flat; they were tested there on two scans.
- 2026-11-24 04:09:03 to 04:09:08 UTC: **first source-check run** (`run_accept.sh`, unit `i1025-k71d281a`): the checks passed (`kc71_syscheck.py` exit 0; `--mutate=F` and `--mutate=steps` exit 1; the k_c 79 check refuses, exit 1; both selftests exit 0) but the **driver stopped before the verdict** ("STOP: the worktree's l1kc71Lw1025e.jsonl differs from the pin", VERDICT REFUSED): the worktree's `solver/matter/data/l1kc71Lw1025e.jsonl` was the 7-row record of the previous task (blob c826dedc, the leg 6 D 21.21875 pin of `../kc71_scout/s2/in/`), not this task's 9-row record (7c4af06f). The guard did what it is for. Files of that run: `first_attempt_0409/`. I looked at the old file (blob c826dedc, 7 rows, nothing running on the worktree) and **moved it aside, not deleted**, to `data/l1kc71Lw1025e.jsonl.c826dedc_from_kc71_scout_s2`; its content is also in `../kc71_scout/s2/in/`. The old kc71_scout scans are finished and read; they do not read this file again.
- 2026-11-24 04:09:30 to 04:09:35 UTC: **source check, second run** (unit `i1025-k71d281a2`) **ACCEPTED** at 04:09:35: win2's k_c 71 leg 6 record |F| 4.4581422310e-10, 2384 steps, constraint 8.758e-3, Delta 1.125866383799 (3295 s on win2); this machine's state |F| 4.4565609972e-10 (-0.035% against the record, inside the 1% bar), `freeze_from` 2384 steps = the record's; `--mutate=F` and `--mutate=steps` exit 1; the k_c 79 check refuses the state (exit 1: "the record is not k_c 79 at D 21.2812 (kc 71, D 21.28125)"); both selftests exit 0; the state (c1687fc0) and record (7c4af06f) copied to this folder and to the worktree's `data/` (blob checked). 04:09:42 UTC: **the scan** started as unit `i1025-k71d281s` (8 processes of 1 thread, nice 10, lambda 0.795 to 0.825 and the repeat of 0.810); all eight print the record system (|F| 4.4557127862e-10 against the record's 4.4581422310e-10, 2384 steps equal), each at about 94% CPU.

## Result (written 2026-11-24 05:49:39 UTC)
**Source:** ACCEPTED 04:09:35 UTC on the second run (the first run stopped at the worktree-copy guard; both logged above). **Scan** (unit `i1025-k71d281s`, 8 processes of 1 thread, nice 10; 04:09:42 to 05:49:15 UTC, 5973 s): exit 0 for all eight (05:47:54 to 05:49:14 UTC); all printed the record system (|F| 4.4557127862e-10 against the record's 4.4581422310e-10, 2384 steps equal); **8 of 8 noise-robust**; the repeat of 0.810 (the first on process 3, the repeat on process 7) **bit-identical** (hybrid -1, ln|det| -1978.6416938123268, float64 ln|det| -1977.751542760501, noise [-1, -1]; `repeat_check.py` PASS); `read_lower.py` selftest exit 0, `--mutate=shift` and `--mutate=round2` exit 1; reader exit 0 (`read_lower.txt`). Seconds per point 5885 to 5967 (eight processes on this machine's 4 cores, one round); wall per process 1:38:11 to 1:39:32; peak RSS 1.41 to 1.49 GiB; lowest MemAvailable 19.8 GiB (99 samples); no memory alert (`alert.log` does not exist).

**Hybrid signs, as printed, lambda 0.795 to 0.825:** minus at 0.795, 0.800, 0.805, 0.810; plus at 0.815, 0.820, 0.825; edge signs minus and plus. **One robust change**, none touching a non-robust point, no ln|det| minimum without a sign change:
| root | bracket | orientation as printed | det-linear estimate | estimator range |
|---|---|---|---|---|
| **k_c 71, D 21.28125, dh170 (Linux)** | (0.810, 0.815) | - to + | **0.810978** | [0.810699, 0.810978] |
The float64 sign differs from the hybrid at 0.805 (float64 plus) and 0.815 (float64 minus): 2 of the 8 evaluations. ln|det|: 0.795 -1974.5783, 0.800 -1975.2958, 0.805 -1976.2578, 0.810 -1978.6417, 0.815 -1977.2274, 0.820 -1976.7869, 0.825 -1976.6912 (a dip at the root). The estimator range is the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure; the bracket is the 0.005 grid step.
**Against the two extrapolations:** t5's 0.8117 (winb's D 21.25 value 0.8217 - 0.32 x 0.03125): the estimate is **-0.000722** from it (t5's "within 0.01": **met**; within 0.005, my 65%: met); my own extrapolation 0.8121: **-0.001122** (within 0.003, my 55%: met).
**The k_c 71 track on leg 6 (position by D, Linux unless marked):** 0.901815 (D 21.0), 0.832037 (D 21.21875), winb's 0.8217 (D 21.25, Windows), **0.810978** (D 21.28125). Slope per unit D: -0.337 from D 21.21875 to 21.28125, -0.323 from D 21.0 to 21.28125, -0.343 from winb's D 21.25 point (a cross-build number) to this one.

## Predictions against the result
| prediction | result |
|---|---|
| t5's, written before the run: one change within 0.01 of 0.8117 | **met**: one change, 0.810978 (-0.000722) |
| mine: `kc71_syscheck.py` accepts with all four controls firing (90%) | yes (state |F| -0.035% of the record's, `freeze_from` 2384 = 2384); the first driver run stopped at a worktree-copy guard before its verdict, which the prediction did not cover |
| every point noise-robust (75%); exactly one robust change (85%) | yes, 8 of 8; yes |
| its estimate within 0.01 of 0.8117 (85%), within 0.005 (65%), within 0.003 of my 0.8121 (55%) | yes; yes; yes (-0.001122) |
| edge signs unequal (85%); the repeat of 0.810 bit-identical (90%) | yes; yes |
| the float64 sign differs from the hybrid at more than half the points (25%) | no: 2 of 8 |
| the scan 1.5 to 1.9 h (65%); peak RSS of a scan process below 2 GiB (90%) | yes, 1.66 h; yes, 1.49 GiB. My ETA to t5 (05:55 UTC) held (05:49:15) |

## Log
- 2026-11-24 05:47:54 to 05:49:15 UTC: the scan finished and was read. 2026-11-24 05:49:39 UTC: result written (this section). Nothing of mine is running on dh170.
