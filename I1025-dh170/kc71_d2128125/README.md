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
