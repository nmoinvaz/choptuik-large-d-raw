# I1025-win2b/kc55: the hybrid sign scan at D 18.5, k_c 55, and which roots are k_c-stable (win2b)

Machine win2 (Windows 11, Intel Core Ultra 7 265K, 20 cores). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025

Written before the run, 2026-11-21 18:41 UTC by `date -u`.

## Order

The coordinator (hc, about 18:36 UTC 21 Nov): a root rising 8.4 per unit D is unlikely to be physical, and step counts change between these states, so the next question is which roots are k_c-stable. Scan D 18.5 at k_c 55 on the Mac's state raw `I1025-mac/out/sol_l1kc55F1025_D18.500000.npy` (its record line from `I1025-mac/out/l1kc55F1025.jsonl`, with the system check first), lambda 1.55 to 2.40 at 0.01, with the same script, noise test and float64 sign, two processes with one point repeated as the check, 4 threads each, BelowNormal, 8 h caps. Window and reading go into this README first, raw `I1025-win2b/kc55`. Post on #1025.

Reading (the coordinator's, fixed before the run): compare with k_c 63 at D 18.5 (one root at 1.6772 in 1.55 to 2.10; xfkappa's 2.10 to 2.40 scan is running). **A root at both k_c within 0.01 is k_c-stable. A root at one k_c only depends on the discretization.**

## Inputs (raw origin/main bef17e78, taken by `git show`, checked with `git hash-object --no-filters`; `in/pins.txt`, `in/pins_check.log`)

| item | raw path | blob |
|---|---|---|
| scanner | `I1025-mac/d18/d18_hybsign.py` | e089207a61fbd98614716abd309571cbc4888db2 |
| state | `I1025-mac/out/sol_l1kc55F1025_D18.500000.npy` (29048 bytes; the same blob as `sol_l1kc55F1025_D18.5000.npy`) | 04e93d6b0989ffc82ed3b05967de984fee590760 |
| record | `I1025-mac/out/l1kc55F1025.jsonl` (47 lines; one D 18.5 line, line 12: k_c 55, F 2.6618688406954084e-10, 2149 steps, kappa 0.7, u0 0.04, Ks 30, h 0.0625) | 0fb77df8281d634e6ecf2d3b2038e3706df3c960 |
| the lane script quoted below | `I1025-mac/d18/lane_d185S.sh` | a019238b1dfbd91c7f258ea64d617c1edd2e9cb6 |
| reader | `I1025-win/d18mid/read_d18mid_1025.py` (winb) | 017ae1dabfb3d07d50ff2d885ad1f6af5db7bbca |
| xfkappa's k_c 63 scans: D 18 (control of the reader), D 18.5 (1.55 to 1.90, the k_c 63 reference) | `I1025-mac/d18/d18_scan_1025.jsonl`, `d185_scan_1025.jsonl` | ac80e9d5bd9c42b1ff10eea65d26258b3314021f, 90540dafdae9ff4093240cdc79d3ef8cc0506000 |

Code: worktree `D:/choptuik-1025p4` at 505d8399, clean (`P4_WT_MATTER`; the driver checks that `dss_ell.py`, `ell_ddm.py` and `ddnp.py` equal 505d8399), PY `C:/Users/nathan/Source/venv-md510` (multidouble 5.1.0), BelowNormal, 4 BLAS and rayon threads per process. The state is the Mac's, taken as it is; whether it is the record's system is the scanner's own first check (below).

## The scan command, quoted

`d18_hybsign.py` docstring: `usage (venv-1025dd): d18_hybsign.py STUB.jsonl STATE.npy D LAMS OUT.jsonl   (LAMS comma-separated)`. It takes the record line at D from the first file (the record's jsonl works as it is), **rebuilds the record's discrete system and checks it first** (|F| within 1% of the record's F and equal steps, else it prints "NOT the record system" and exits 3, before any lambda), and at each lambda prints the hybrid sign and ln|det| (`p4_hybrid.py`'s `sd()`, unchanged) with its 1e-15 noise test on blocks 0 to 11 (2 seeds) and the plain float64 sign beside it. Each point is independent, so a split changes nothing per point.

xfkappa's D 18.5 scan at k_c 63 in `lane_d185S.sh` (blob a019238b):

```
L=$($PY -c 'print(",".join(f"{1.55 + 0.01 * i:.2f}" for i in range(36)))')
timeout 21600 nice -n 10 $PY -u $Q/d18_hybsign.py $REC $ST 18.5 $L $SCAN < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d185_scan.log
```

Mine, per process (`kc55_driver.sh`): `python -u in/d18_hybsign.py in/l1kc55F1025.jsonl in/sol_l1kc55F1025_D18.500000.npy 18.5 <LAMS> <OUT>`, the same environment as my earlier scans (`OPENBLAS_NUM_THREADS` and the others 4, `P4_WT_MATTER`). Differences from the quoted lines, outside the computation: venv-md510, no `nice` (BelowNormal by the launcher), no `timeout` (an exact-pid cap with a command-line check), and the warning filter applied to a copy of the raw log after the run. **The system check is the first line of each process's log; if it says "NOT the record system" the process exits 3, the driver stops, and nothing is read.**

## Window and lambda lists, fixed before the run

Window: lambda 1.55 to 2.40 at 0.01, 86 points. At k_c 63 the Mac's scan covers 1.55 to 1.90 (one robust change, minus-to-plus in (1.67, 1.68), det-linear estimate 1.677016, estimator range [1.677016, 1.677225]) and, by the coordinator, 1.55 to 2.10 holds the one root 1.6772; xfkappa's k_c 63 scan of 2.10 to 2.40 is running.

| process | lambda, in this order | evaluations |
|---|---|---|
| A | 1.97, then 1.55, 1.56, ..., 1.96 | 43 |
| B | 1.97 again, then 1.98, 1.99, ..., 2.40 | 44 |

The repeated point (1.97, first in both) makes 87 evaluations for 86 distinct points. Caps 28800 s (8 h) each by the exact pid of the root process (`taskkill /T /F /PID`) after a check that its command line contains `d18_hybsign.py`; a cap is not retried.

## Reading, fixed now (`kc55_compare.py`; the pinned reader prints the changes and minima)

Definitions. A **k_c 55 root** is a robust change of the hybrid sign: two consecutive points of different hybrid sign, both passing their 1e-15 noise test; it lies in its bracket (a, b), b - a = 0.01. A k_c 63 root r and a k_c 55 root are **within 0.01** when the k_c 55 root is in the band [r - 0.01, r + 0.01]. The bracket is all this scan gives, so, for each k_c 55 root in the k_c 63 coverage:

- bracket inside the band of a k_c 63 root: **STABLE**;
- bracket outside the band of every k_c 63 root: **k_c 55 ONLY** (depends on the discretization);
- otherwise (the bracket straddles a band edge): **UNDETERMINED at the 0.01 step**, reported and not decided (a hybrid root search in the bracket would decide it, and is the coordinator's to order).

For each k_c 63 root: a robust k_c 55 bracket inside its band: **MATCHED**; no k_c 55 change (robust or not) touching the band: **k_c 63 ONLY**; otherwise UNDETERMINED. The k_c 63 roots are: 1.6772 over the coverage 1.55 to 2.10 (the coordinator's figure). A k_c 55 change above 2.10 is **not compared** until xfkappa's 2.10 to 2.40 k_c 63 scan is in; then `kc55_compare.py` is rerun with `--cov63 1.55,2.40 --r63 <roots>` and its result posted. A change that touches a non-robust point is listed and not counted. The orientation of each change is printed as the scan gives it and is **not used** by the rule; **all orientation readings wait for xfkappa's sign-convention check.** The ln|det| local minima without a change (near-misses) and the float64 sign are reported as the pinned reader prints them; nothing else is read.

## Repeat check, fixed now

At the repeated lambda 1.97 the two records (A's and B's) must have the same hybrid sign and ln|det| equal to 1e-6 (`merge_scan.py`; the gate, the same bar as the other scans). The merged 86-point scan is written, and the reader and comparison run, only if this check passes, the two files share exactly the point 1.97, every record is at D 18.5 and every lambda from 1.55 to 2.40 is present. The result is written into this README after the run.

## Controls, before the run

`plant_checks_kc55.py`, 27 cases (`plant_checks_kc55.log`, rerun by the driver as `plant_checks_kc55_run.log`; the driver does not start the scan unless it passes): `merge_scan.py` merges equal repeats and fails on a ln|det| difference of 1e-3, a flipped repeat sign, no repeated point, a second point in both files, a missing lambda and records at another D, and writes no merged file then; `kc55_compare.py` on planted 86-point scans gives STABLE and MATCHED for a change in (1.67, 1.68), UNDETERMINED for (1.66, 1.67), k_c 55 ONLY and k_c 63 ONLY for (1.69, 1.70), k_c 63 ONLY for no change, "not compared" above the coverage, k_c 55 ONLY and STABLE and MATCHED with a widened coverage and a second k_c 63 root, "not counted" and UNDETERMINED for a change with a non-robust point, and "outside the window" for a k_c 63 root outside it; the pinned reader gives winb's quoted readings on xfkappa's D 18 and D 18.5 scans, and the comparison on the k_c 63 D 18.5 scan itself calls its own change STABLE against 1.6772. All 27 pass. (A first run of the controls had 2 cases wrong, through my own planted case "repeat sign differs", which gave the repeat the sign it already had; I corrected the planted case, not a script, and reran.)

## Run

`kc55_driver.sh` (launcher `launch_kc55.ps1`, BelowNormal): checks the pins, the worktree and the record line (one D 18.5 line, F and steps), runs the planted controls, starts the two processes and the passive sampler (`samples.csv`, a sample every 60 s, only the processes whose command line holds this folder's `d18_hybsign.py` path), then merges, reads and compares. Blobs of the new scripts (mine): `merge_scan.py` 378ccc17, `kc55_compare.py` e63ab7d6, `plant_checks_kc55.py` 41ef7d22, `kc55_driver.sh` 836eba29, the sampler `sample_kc55.ps1` 9437f3ef. Output: `scanA.jsonl`, `scanB.jsonl`, `scan_merged.jsonl`, `scanA_raw.log`, `scanB_raw.log`, `scanA.log`, `scanB.log`, `merge.log`, `reading.log`, `compare.log`, `rc_A`, `rc_B`, and one line per event in `../exits_1025.txt` (prefix `1025 kc55`); the last lines are `1025 kc55 reading: ...`, `1025 kc55 compare: ...` and `1025 kc55 done`.

Estimate: not known at k_c 55. At k_c 63 a point took 425 to 530 s with two processes running; k_c 55 is a smaller system, so 43 to 44 points are expected in about 3 to 6 h.

## Log

(appended below as the run goes)
- 2026-11-21 18:41:25 UTC: both scan processes started (A root pid 29936, B root pid 24624; the driver's pre-checks, including the 27 planted controls, passed at 18:41:23). **System check, first line of each log: "the record system" on both**: |F| 2.6646072378e-10 against the record's 2.6618688407e-10 (0.10%), steps 2149 against 2149.
- 2026-11-21 21:35 UTC (3 h progress post, comment 7069589234): 66 of 86 distinct points done (A 33 evaluations, B 34), 274 to 429 s a point (mean 308 s), no point fails its noise test. Interim signs, not read: minus at 1.55 to 1.86 (no change, which covers the whole band of the k_c 63 root 1.6772), plus at 1.97 to 2.21, minus at 2.22 to 2.30 (a robust plus-to-minus change in (2.21, 2.22)); A still has 1.87 to 1.96 and B 2.31 to 2.40. The formal reading is made on the merged scan after the repeat check.
- 2026-11-21 18:41:25 to 22:23:49 UTC: A ended 22:19:05 (exit 0, 13060 s) and B 22:23:47 (exit 0, 13342 s), neither capped; 262 to 429 s a point (mean 303 s). The sampler (`samples.csv`) was ended by its exact pid at 22:23:48. Merge, reading and comparison by the driver at 22:23:49 (`merge.log`, `reading.log`, `compare.log`).

## Result (22:25 UTC, by `date -u`)

**Repeat check (lambda 1.97, first in both halves): PASS.** Hybrid sign +1 in A and B; ln|det| -1597.118812893949 in both, difference 0.000e+00 (bar 1e-6); noise robust in both; float64 sign +1 in both; 288 s and 291 s. The merged 86-point scan was written (`scan_merged.jsonl`).

**Reading (the pinned reader, `reading.log`):**

- every point is noise robust (none fails its 1e-15 noise test);
- hybrid signs: minus at 1.55 to 1.87 (33 points), plus at 1.88 to 2.21 (34), minus at 2.22 to 2.40 (19);
- **two robust changes: (1.87, 1.88) minus-to-plus and (2.21, 2.22) plus-to-minus** (the reader's gap line, centre to centre 0.340, carries its fixed D 18 reference text 0.0325 and is not a k_c comparison);
- ln|det| local minima: at 1.87 (ln -1602.160580) beside a change; at 2.21 (ln -1594.539028) beside a change; **at 1.68 (ln -1605.631561) WITHOUT a change**;
- the float64 sign differs from the hybrid's at 1 of 86 points (1.88; information).

**Comparison with k_c 63 at D 18.5 (`kc55_compare.py`, the rule fixed before the run).**

First run, as the driver did it (k_c 63 coverage 1.55 to 2.10, root 1.6772; `compare.log`): (1.87, 1.88) **k_c 55 ONLY**; (2.21, 2.22) not compared (above the coverage); k_c 63 root 1.6772: **k_c 63 ONLY**.

xfkappa's k_c 63 scan of 2.10 to 2.40 came in meanwhile (#1025 comment 7067627814, 18:56 UTC; raw `I1025-mac/d18/d185_scanup_1025.jsonl` blob 9f3e31e5, and `d185_scanhi_1025.jsonl` blob 496f4b63 for 1.90 to 2.10, both taken at raw origin/main 65c4f990 and kept in `in/`). I read the raw files myself: with the Mac's 1.55 to 1.90 scan (blob 90540daf) the three give 86 points over 1.55 to 2.40 at the same state, all noise robust, and the pinned reader finds **one robust change, (1.67, 1.68) minus-to-plus**, plus at every point from 1.68 to 2.40 (`in/kc63_d185_merged_1.55-2.40.jsonl`, `kc63_d185_reading.log`). That is the "rerun with --cov63 1.55,2.40" the README fixed. Second run (`compare_cov240.log`, coverage 1.55 to 2.40, root 1.6772):

| k_c 55 or k_c 63 root | bracket or value | verdict by the rule |
|---|---|---|
| k_c 55, minus-to-plus | (1.87, 1.88) | k_c 55 ONLY (outside the band 1.6672 to 1.6872 of the only k_c 63 root) |
| k_c 55, plus-to-minus | (2.21, 2.22) | k_c 55 ONLY (k_c 63 has no root in 1.55 to 2.40 apart from 1.6772) |
| k_c 63, minus-to-plus | 1.6772 (bracket (1.67, 1.68)) | k_c 63 ONLY (no k_c 55 change, robust or not, touches 1.6672 to 1.6872) |

**By the letter: no root of D 18.5 in 1.55 to 2.40 is k_c-stable** (none at both k_c within 0.01); each of the three depends on the discretization.

**A fact beside the rule, not part of it:** the k_c 55 scan has a ln|det| local minimum at 1.68 WITHOUT a change, at the place of the k_c 63 root. ln|det| at 1.66, 1.67, 1.68, 1.69, 1.70: k_c 55 -1604.311, -1604.975, **-1605.632**, -1605.513, -1604.727 (sign minus at all five); k_c 63 -1901.001, -1901.777, **-1902.632**, -1901.013, -1900.337 (minus, minus, plus, plus, plus). Both have their minimum at 1.68; at k_c 55 the sign does not change. A step of 0.01 cannot tell a near miss from two roots inside one step or a double root. Nothing is read from this; a finer k_c 55 scan around 1.66 to 1.70 would decide it, and is the coordinator's to order.

**cpu and memory (`samples.csv`, a sample every 60 s, 218 samples 18:41:25 to 22:23:12 UTC; my processes only).** The two python children (pids 30920 and 36440; the roots are launcher stubs): peak working set 0.80 GiB and private 1.30 GiB each; 18787 and 19220 cpu-s in 13060 and 13342 s; BelowNormal throughout; together at most 1.30 GiB working set and 2.45 GiB private in one sample. Machine: cpu mean 36.9% (1 s samples), max 53.7%; commit 46.4 to 56.8 of 101.5 GiB; free physical at least 44.7 GiB.

---

# Part 2: the finer scan, lambda 1.660 to 1.700 at 0.002 (win2b)

Written before the run, 2026-11-21 22:30 UTC by `date -u`. Part 1 above (lambda 1.55 to 2.40 at 0.01) is done; its files are unchanged, and the files of this part have the prefix `fine_`.

## Order

The coordinator (hc, about 22:26 UTC 21 Nov, after Part 1's result, "yes to the finer scan"): k_c 55 at D 18.5, the same state and record, lambda 1.660 to 1.700 at 0.002 (21 points), with the same script, noise test and float64 sign. Two processes, with 1.680 run in both as the check, 4 threads each, BelowNormal, 8 h caps. Window and reading go into this README first, raw `I1025-win2b/kc55`. Post on #1025.

Reading (the coordinator's, fixed before the run): **two robust changes inside the window mean a close pair at k_c 55 where k_c 63 has one root at 1.6772, and report the pair's positions and gap. No change, with the ln|det| minimum resolved, means a near miss: k_c 55 has no root there.**

## Inputs

The same as Part 1 (`in/pins.txt`, all blobs checked again by the driver before the start): scanner `d18_hybsign.py` e089207a, state `sol_l1kc55F1025_D18.500000.npy` 04e93d6b, record `l1kc55F1025.jsonl` 0fb77df8 (one D 18.5 line: F 2.6618688406954084e-10, 2149 steps). The system check is the script's own first line (the record system, else exit 3 and the driver stops). Worktree `D:/choptuik-1025p4` at 505d8399, venv-md510, 4 BLAS and rayon threads per process, BelowNormal. Plus Part 1's 0.01 scan `scan_merged.jsonl` (blob 24179d07661c86d192d397e39688fe6365a05ddf), for the overlap comparison and the endpoint signs.

winb's pinned reader prints lambda to two decimals, which a 0.002 grid cannot use, and `merge_scan.py` has the step 0.01 in it. New scripts of this part (mine; blobs): `merge_fine.py` e42b2c19 (the same logic and bar as `merge_scan.py`, step and three decimals as arguments), `read_fine.py` fe01f2e5 (the pinned reader's definitions with the step as a parameter, lambda to three decimals, and the fixed reading below), `plant_checks_fine.py` 9d816ad8, `fine_driver.sh` f9548b7b (launcher `launch_fine.ps1`), the sampler `sample_kc55.ps1` 9437f3ef (unchanged).

## Window and lambda lists, fixed before the run

Window: lambda 1.660 to 1.700 at 0.002, 21 points. It holds the 0.01 scan's points 1.66, 1.68 and 1.70 (sign minus at all three) and the whole band of the k_c 63 root 1.6772 (bracket (1.67, 1.68), bisected 1.6772091); the 0.01 scan's ln|det| minimum at k_c 55 is at 1.68.

| process | lambda, in this order | evaluations |
|---|---|---|
| A | 1.680, then 1.660, 1.662, ..., 1.678 | 11 |
| B | 1.680 again, then 1.682, 1.684, ..., 1.700 | 11 |

The repeated point (1.680, first in both) makes 22 evaluations for 21 distinct points. Caps 28800 s (8 h) each by the exact pid of the root process (`taskkill /T /F /PID`) after a check that its command line contains `d18_hybsign.py`; a cap is not retried.

## Reading, fixed now (`read_fine.py`)

Definitions as in the pinned reader: a point is robust if the hybrid's sign survives its 1e-15 noise test (2 seeds); a change is two consecutive points of different hybrid sign, robust if both are; orientation minus-to-plus or plus-to-minus; a ln|det| local minimum is an interior point below both neighbours', "beside a change" if a neighbour's sign differs, else "WITHOUT a change"; a point at the window's end below its only neighbour is "at the scan edge". Then, the coordinator's reading:

- **two robust changes inside the window**: a close pair at k_c 55 where k_c 63 has one root. Report the pair's positions (the two brackets, 0.002 wide, with the det-linear estimate of each root as information: the line through the bracket's det = sign exp(ln), xfkappa's estimator, which gives 1.677016 on the k_c 63 scan) and the gap (between the brackets, the two extremes, and centre to centre);
- **no robust change, with the ln|det| minimum resolved** (an interior local minimum WITHOUT a change, below both neighbours): a near miss; k_c 55 has no root there;
- no change with the minimum at the window's edge: reported as "minimum not resolved" (not a near miss by the reading);
- any other count of robust changes (1, 3, 4, ...): reported as OTHER, not covered by the fixed reading. The 0.01 scan had sign minus at 1.66 and at 1.70, so an odd number of changes between them is impossible; the reader checks this window's endpoint signs against them (`--ends -,-`) and prints INCONSISTENT if they differ;
- a change that touches a non-robust point is listed and not counted;
- the float64 sign and the orientation are reported as printed; orientation readings wait for xfkappa's sign-convention check.

A step of 0.002 cannot exclude two roots closer together than 0.002; that is stated with the result, not read.

## Repeat check, fixed now

At the repeated lambda 1.680 the two records (A's and B's) must have the same hybrid sign and ln|det| equal to 1e-6 (`merge_fine.py`; the gate). The merged 21-point scan is written, and the reader run, only if this check passes, the two files share exactly the point 1.680, every record is at D 18.5 and all 21 lambda are present. In addition `merge_fine.py` compares every point the 0.01 scan also holds (1.660, 1.680, 1.700) with that scan's record, sign and ln|det| to 1e-6, and prints AGREES or DIFFERS for each (information, not a gate). The results are written into this README after the run.

## Controls, before the run

`plant_checks_fine.py`, 28 cases (`plant_checks_fine.log`, rerun by the driver as `plant_checks_fine_run.log`; the driver does not start the scan unless it passes): `merge_fine.py` merges equal repeats, reports a prior value that agrees and ones that differ, fails on a ln|det| difference of 1e-3, a flipped repeat sign, no repeated point, a second point in both files, a missing lambda and records at another D, and writes no merged file then; `read_fine.py` on planted 21-point scans reports a pair with its positions and gap (the planted pair gives brackets (1.674, 1.676) and (1.682, 1.684), gap 0.006 to 0.010, centre to centre 0.0080), a near miss with the minimum's depth for a V at 1.680, "minimum not resolved" for a minimum at the edge, OTHER for one change (with INCONSISTENT endpoints) and for four, OTHER with a non-robust change not counted, and a grid gap; and it agrees with winb's pinned reader on three real 0.01 scans (the k_c 55 and k_c 63 D 18.5 scans and xfkappa's D 18 scan: the same changes and the same minima) and gives xfkappa's det-linear estimate 1.677016 on the k_c 63 scan. All 28 pass first time.

## Run

`fine_driver.sh` (launcher `launch_fine.ps1`, BelowNormal): checks the pins, the worktree, the record line and the 0.01 scan's blob, runs the planted controls, starts the two processes and the passive sampler (`fine_samples.csv`, a sample every 60 s, only my `d18_hybsign.py` processes), then merges and reads. Output: `fine_scanA.jsonl`, `fine_scanB.jsonl`, `fine_scan_merged.jsonl`, `fine_scanA_raw.log`, `fine_scanB_raw.log`, `fine_scanA.log`, `fine_scanB.log`, `fine_merge.log`, `fine_reading.log`, `fine_rc_A`, `fine_rc_B`, and one line per event in `../exits_1025.txt` (prefix `1025 kc55fine`); the last lines are `1025 kc55fine reading: ...` and `1025 kc55fine done`.

Estimate: Part 1 took 262 to 429 s a point (mean 303 s) with two processes running; 11 evaluations per process take about 55 to 80 minutes.

## Log (Part 2)

(appended below as the run goes)
- 2026-11-21 22:31:22 UTC: both scan processes started (A root pid 32696, B root pid 34144; the driver's pre-checks, including the 28 planted controls, passed at 22:31:21). **System check, first line of each log: "the record system" on both**: |F| 2.6646072378e-10 against the record's 2.6618688407e-10 (0.10%), steps 2149 against 2149.
- 2026-11-21 22:31:22 to 23:21:40 UTC: B ended 23:21:31 (exit 0, 3009 s) and A 23:21:40 (exit 0, 3018 s), neither capped; 264 to 282 s a point (mean 273 s). The sampler (`fine_samples.csv`) was ended by its exact pid at 23:21:41. Merge and reading by the driver at 23:21:44 (`fine_merge.log`, `fine_reading.log`).

## Result (Part 2, 23:23 UTC by `date -u`)

**Repeat check (lambda 1.680, first in both halves): PASS.** Hybrid sign -1 in A and B; ln|det| -1605.631560677098 in both, difference 0.000e+00 (bar 1e-6); noise robust in both; float64 sign -1 in both; 280 s and 280 s. **Comparison with the 0.01 scan (information): AGREES at all five shared points** (1.660, 1.670, 1.680, 1.690, 1.700: sign minus, ln|det| equal to the last digit). The merged 21-point scan was written (`fine_scan_merged.jsonl`).

**Reading (`read_fine.py`, as fixed before the run):**

- every point is noise robust, and the hybrid sign is minus at all 21 points: **no change** (the endpoint signs, minus at 1.660 and at 1.700, are consistent with the 0.01 scan);
- one ln|det| local minimum, **at 1.684 (ln -1605.721024), interior and WITHOUT a change**, below its neighbours by 0.0225 (1.682) and 0.0258 (1.686): **resolved**;
- **FINE READING: NEAR MISS.** No robust change and a resolved minimum: k_c 55 has no root there, by the coordinator's reading;
- the float64 sign equals the hybrid's at all 21 points (information);
- no pair: no two changes, so no positions or gap to report.

The ln|det| over the window falls from -1604.3106 at 1.660 to -1605.7210 at 1.684 and rises to -1604.7270 at 1.700; the differences between consecutive points run smoothly from -0.1211 to -0.1460 (at 1.670 to 1.672), through -0.0225 and +0.0258 at the minimum, to +0.1661 (at 1.696 to 1.698), with no jump. The 0.01 scan's minimum at 1.68 (ln -1605.632) was a grid point beside the true minimum, 1.684.

**Information, beside the reading, not part of it** (`fine_dip_fit.py`, `fine_dip_fit.log`; a model fit, not a root search; the script first recovers two planted truths): the 21 ln|det| values are fitted to a + ln((l - l0)^2 + e^2) + b (l - l0) + c (l - l0)^2 (a pair of complex roots l0 +- i e times a smooth factor) with l0 = 1.68434 and e = 0.01275, max residual 2.3e-4, rms 1.0e-4, while a quartic polynomial leaves 3.9e-2 and a quadratic 0.21. Within that model the roots are off the real axis by 0.0128, and l0 is 0.0071 above the k_c 63 root 1.6772091. A step of 0.002 cannot exclude two real roots closer together than 0.002; the smooth, shallow minimum shows no sign of one.

**cpu and memory (`fine_samples.csv`, a sample every 60 s, 50 samples 22:31:22 to 23:21:29 UTC; my processes only).** The two python children (pids 26000 and 34952; the roots are launcher stubs): peak working set 0.69 and 0.70 GiB, private 1.11 and 1.27 GiB; 4235 and 4233 cpu-s in about 3010 s; BelowNormal throughout; together at most 1.19 GiB working set and 2.37 GiB private in one sample. Machine: cpu mean 31.1% (1 s samples), max 46.3%; commit 50.3 to 54.0 of 101.5 GiB; free physical at least 49.4 GiB.

---

# Part 3: the k_c test at D 18.25, lambda 1.30 to 2.40 at 0.02 (win2b)

Written before the run, 2026-11-21 23:28 UTC by `date -u`. Parts 1 and 2 above (D 18.5) are done; their files are unchanged, and the files of this part have the prefix `d1825_`.

## Order

The coordinator (hc, about 23:25 UTC 21 Nov, after Part 2's near miss): the k_c test at D 18.25, completing the set (xfkappa D 17.75, winb D 18, win2b D 18.5, win2 k_c 71 at D 18.5). Scan the Mac's k_c 55 state raw `I1025-mac/out/sol_l1kc55F1025_D18.250000.npy` (its record line, system check first) over 1.30 to 2.40 at 0.02 (56 points), with the same script, noise test and float64 sign. Two processes with one point repeated as the check, 4 threads each, BelowNormal, 8 h caps. Window and reading go into this README first, raw `I1025-win2b/kc55`. Post on #1025.

Reading (the coordinator's, fixed before the run): compare with k_c 63 at D 18.25 (xfkappa, comment 7070296128: 1.3885, 1.7425, 2.3187). **Each k_c 55 change within 0.02 of a k_c 63 root counts as stable; the rest are k_c-dependent. Report any ln|det| minimum without a change, with the dip fit.**

## Inputs (raw origin/main b247f0e8, taken by `git show`, checked with `git hash-object --no-filters`; `in/pins_d1825.txt`, `in/pins_d1825_state.txt`)

The same as Part 1 (scanner `d18_hybsign.py` e089207a, record `l1kc55F1025.jsonl` 0fb77df8, winb's reader 017ae1da) and the new state: `I1025-mac/out/sol_l1kc55F1025_D18.250000.npy` (29048 bytes), blob cbaffca8ea07b6079ae436dfd7fcd9b1a9f57143. The record has one D 18.25 line (line 8: k_c 55, F 2.777068169891278e-10, 2190 steps, kappa 0.7, u0 0.04, Ks 30, h 0.0625). **The system check is the script's own first line** (|F| within 1% of the record's F and equal steps, else "NOT the record system", exit 3, before any lambda; the driver then stops and nothing is read). Worktree `D:/choptuik-1025p4` at 505d8399, venv-md510, 4 BLAS and rayon threads per process, BelowNormal.

The k_c 63 side is xfkappa's comment 7070296128: D 18.25's map over 1.20 to 2.60 on one state (93 merged points), three roots with their estimator ranges: 1.388522 to 1.388581, 1.742506 to 1.742860, 2.318523 to 2.318888 (hybrid, provisional, no dd check); the signs run plus at 1.20, then minus, plus, minus across the three roots, and minus at 2.60, so the roots are plus-to-minus, minus-to-plus, plus-to-minus. The coordinator's figures 1.3885, 1.7425, 2.3187 are used.

## Window and lambda lists, fixed before the run

Window: lambda 1.30 to 2.40 at 0.02, 56 points. It holds the three k_c 63 roots (1.3885, 1.7425, 2.3187, all inside) and is inside the k_c 63 map (1.20 to 2.60).

| process | lambda, in this order | evaluations |
|---|---|---|
| A | 1.86, then 1.30, 1.32, ..., 1.84 | 29 |
| B | 1.86 again, then 1.88, 1.90, ..., 2.40 | 28 |

The repeated point (1.86, first in both; no k_c 63 root is near it) makes 57 evaluations for 56 distinct points. Caps 28800 s (8 h) each by the exact pid of the root process (`taskkill /T /F /PID`) after a check that its command line contains `d18_hybsign.py`; a cap is not retried.

## Reading, fixed now (`kc_compare2.py`, `read_fine.py`, `dip_fit2.py`)

*(Amended by the coordinator before any result, recorded 2026-11-21 23:33 UTC: the rule compares the k_c 55 change's det-linear estimate with the k_c 63 root; the bracket-distance rule below stays as information. See "Amendment 1" at the end of this part.)*

A **k_c 55 change** is two consecutive points of different hybrid sign, both passing their 1e-15 noise test (robust); it lies in its bracket (a, b), b - a = 0.02. **"Within 0.02 of a k_c 63 root r"** is read as: the distance from r to the bracket [a, b] is at most 0.02 (0 if r is inside). That is the coordinator's two-class rule:

- a k_c 55 change within 0.02 of a k_c 63 root: **STABLE**;
- a k_c 55 change farther than 0.02 from every k_c 63 root: **k_c-DEPENDENT (k_c 55 only)**;
- a k_c 63 root with no robust k_c 55 change within 0.02: **k_c-DEPENDENT (k_c 63 only)**.

The bracket is as wide as the band, so each STABLE change is also marked **wholly inside** the band [r - 0.02, r + 0.02] (the k_c 55 root is certainly within 0.02 of r) or **straddling the band edge** (the root may be up to 0.04 from r); both count as stable by the rule, and the two counts are printed. (At D 18.5 the band was 0.01 and the rule stricter, with an UNDETERMINED class; here the coordinator's rule is the one stated above.) A change that touches a non-robust point is listed and not counted, and a k_c 63 root with only such a change near it is UNDETERMINED; a k_c 55 change outside the k_c 63 coverage (1.20 to 2.60) would be not compared. The orientation of each change is printed beside its k_c 63 match as information; **the rule does not use orientation, and all orientation readings wait for xfkappa's sign-convention check.**

**Every ln|det| local minimum without a change** (the pinned reader's definition: an interior point below both neighbours', the hybrid sign the same on both sides) is reported by `read_fine.py` and fitted by `dip_fit2.py` with the dip model of Part 2's `fine_dip_fit.py` (ln|det| = a + ln((l - l0)^2 + e^2) + b (l - l0) + c (l - l0)^2, a complex pair l0 +- i e times a smooth factor), over the 11 points around the minimum, with the 1-sigma uncertainties from the Jacobian and a quartic and a quadratic polynomial over the same points. At a step of 0.02 the fit is coarse: it is flagged NOT RESOLVED when |e| is below half a step or its uncertainty exceeds |e|. The fit is information, a model and not a root search. The line "FINE READING" that `read_fine.py` prints is Part 2's rule and is not used here.

## Repeat check, fixed now

At the repeated lambda 1.86 the two records (A's and B's) must have the same hybrid sign and ln|det| equal to 1e-6 (`merge_fine.py`, step 0.02; the gate). The merged 56-point scan is written, and the reading run, only if this check passes, the two files share exactly the point 1.86, every record is at D 18.25 and all 56 lambda are present. The result is written into this README after the run.

## Controls, before the run

`plant_checks_d1825.py`, 26 cases (`plant_checks_d1825.log`, rerun by the driver as `plant_checks_d1825_run.log`; the driver does not start the scan unless it passes): `kc_compare2.py` on planted 56-point scans with the three k_c 63 roots gives STABLE (wholly inside) and MATCHED for brackets over all three roots, STABLE marked "straddles the band edge" for a bracket 0.0085 from a root, k_c-DEPENDENT (k_c 55 only) for a bracket 0.1025 from the nearest root and k_c-DEPENDENT (k_c 63 only) for a root with no change near it (and for all three with no change at all), "not counted" and UNDETERMINED for a change with a non-robust point, "not compared" above a narrower coverage, and the orientation the same or the opposite; `merge_fine.py` at step 0.02 merges an equal repeat (no prior scan) and fails on a ln|det| difference of 1e-3 and on a missing lambda; `read_fine.py` at step 0.02 prints the changes with two-decimal brackets; `dip_fit2.py` recovers a resolved planted pair (e = 0.06) and an unresolved one is flagged NOT RESOLVED (e = 0.004), finds a planted smooth complex-pair dip without a change (l0 and e recovered) and finds none beside a change. All 26 pass; a first run had 2 cases wrong, both my planted cases (a planted parabola for the dip fit and a V placed where no change was), which I corrected before the run, not a script.

## Run

`d1825_driver.sh` (launcher `launch_d1825.ps1`, BelowNormal): checks the pins, the worktree and the record line, runs the planted controls, starts the two processes and the passive sampler (`d1825_samples.csv`, a sample every 60 s, only my `d18_hybsign.py` processes), then merges and reads. Blobs of the new scripts (mine): `kc_compare2.py` a7289a19, `dip_fit2.py` 8a876f65, `plant_checks_d1825.py` c98856e2, `d1825_driver.sh` 68969ab8; `merge_fine.py` e42b2c19, `read_fine.py` fe01f2e5 and the sampler 9437f3ef as in Part 2. Output: `d1825_scanA.jsonl`, `d1825_scanB.jsonl`, `d1825_scan_merged.jsonl`, `d1825_scanA_raw.log`, `d1825_scanB_raw.log`, `d1825_scanA.log`, `d1825_scanB.log`, `d1825_merge.log`, `d1825_reading.log`, `d1825_compare.log`, `d1825_dipfit.log`, `d1825_rc_A`, `d1825_rc_B`, and one line per event in `../exits_1025.txt` (prefix `1025 kc55d1825`); the last lines are `1025 kc55d1825 reading: ...`, `compare: ...`, `dip fit: ...` and `done`.

Estimate: Part 1 took 262 to 429 s a point at D 18.5 with two processes running; 28 to 29 evaluations per process take about 2.5 to 3.5 h. The 3 h progress post is due if it is still running then.

## Log (Part 3)

(appended below as the run goes)
- 2026-11-21 23:29:10 UTC: both scan processes started (A root pid 35644, B root pid 17192; the driver's pre-checks, including the 26 planted controls, passed at 23:29:08). **System check, first line of each log: "the record system" on both**: |F| 2.7802867306e-10 against the record's 2.7770681699e-10 (0.12%), steps 2190 against 2190.

## Amendment 1 to Part 3's reading (the coordinator's hc, received about 23:30 UTC 21 Nov; recorded 2026-11-21 23:33 UTC by `date -u`)

**Before any result:** the scan had started at 23:29:10 UTC and no point had finished when the hc arrived (both processes had printed their system-check line only; at 23:31:44 UTC each log held 0 points).

The coordinator's tightening of "within 0.02", made before any result: **compare the k_c 55 change's det-linear estimate (as d18f_read and xfkappa's readers compute it) with the k_c 63 root. Within 0.02 is stable; otherwise the root depends on k_c. The bracket-to-root distance, with its inside and straddling marks, stays in the report as information. A bracket as wide as the band would otherwise let a 0.04 difference count as stable.**

What changed and what did not:

- **The rule is now:** a robust k_c 55 change is STABLE if its det-linear estimate is within 0.02 of a k_c 63 root (1.3885, 1.7425, 2.3187), else k_c-DEPENDENT (k_c 55 only); a k_c 63 root with no robust k_c 55 change whose estimate is within 0.02 is k_c-DEPENDENT (k_c 63 only); a k_c 63 root with only a non-robust change near it is UNDETERMINED; a change outside the k_c 63 coverage is not compared. This replaces "the distance from the root to the 0.02-wide bracket is at most 0.02" of the "Reading, fixed now" section above (my reading of "within 0.02", which the coordinator has tightened).
- **The estimate** is the zero of the line through the bracket's two points of f = sign x exp(ln - ref), ref the scan's largest ln|det| (it cancels): x_a + (x_b - x_a) f_a / (f_a - f_b), the formula of `changes()` in xfkappa's `d185_scan_read.py` (raw `I1025-mac/d18`, blob 7c9d400fd0966a35ac306b5495febb4ec4efe7da, kept in `in/`, `in/pins_amend_1.txt`; its `lin`, which `d18f_read.py` (5fb96dce) uses through that module). It is the same as the det-linear estimate `read_fine.py` printed in Part 2 (1.677016 on the k_c 63 scan). The planted controls check this script's estimate against xfkappa's own `changes()` on a real scan to 5e-7.
- **Kept as information in every line:** the bracket-to-root distance with its mark (wholly inside the band, straddling its edge, or outside it), and the summary's counts of the marks. The orientation is printed as information and not used; orientation readings wait for xfkappa's sign-convention check. The ln|det| minima without a change and the dip fits are unchanged.
- **Files:** `kc_compare2.py` is replaced (new blob 809f5fa8; the first version, the bracket rule, is kept as `kc_compare2_v1_bracket_rule.py`, a7289a19); `plant_checks_d1825.py` is replaced (new blob 91c4abe7; the first version is kept as `plant_checks_d1825_v1.py`, c98856e2). `d1825_driver.sh` (68969ab8) is not changed: it is running, and its reading step calls `kc_compare2.py` by path with the same arguments when the scans end, so it uses the amended version. The driver's pre-check at 23:29:08 UTC ran the first controls (26 cases, the bracket rule, all passing); the amended controls (29 cases: the amendment case, in which a bracket straddling the band edge and 0.0085 from a root has its estimate 0.0276 away and is now k_c-DEPENDENT, and the estimate against xfkappa's code) were run by hand at 23:33 UTC and pass (`plant_checks_d1825_amended.log`). `merge_fine.py`, `read_fine.py` and `dip_fit2.py` are unchanged. The "26 cases" of Part 3's Controls section describes the first version.
- 2026-11-21 23:29:10 to 2026-11-22 02:03:50 UTC: B ended 01:58:03 (exit 0, 8933 s) and A 02:03:50 (exit 0, 9280 s), neither capped; 284 to 345 s a point (mean 320 s). The sampler (`d1825_samples.csv`) was ended by its exact pid at 02:03:51. Merge, reading, comparison and dip fit by the driver at 02:03:53 to 02:03:54 (`d1825_merge.log`, `d1825_reading.log`, `d1825_compare.log`, `d1825_dipfit.log`); the comparison ran with the amended `kc_compare2.py` (Amendment 1).

## Result (Part 3, 2026-11-22 02:05 UTC by `date -u`)

**Repeat check (lambda 1.86, first in both halves): PASS.** Hybrid sign -1 in A and B; ln|det| -1607.6617428467364 in both, difference 0.000e+00 (bar 1e-6); noise robust in both; float64 sign -1 in both; 299 s and 298 s. The merged 56-point scan was written (`d1825_scan_merged.jsonl`).

**Reading of the scan (`read_fine.py` at step 0.02):** every point is noise robust. Hybrid signs: plus at 1.30 to 1.74 (23 points), minus at 1.76 to 1.94 (10), plus at 1.96 to 2.40 (23). **Two robust changes: (1.74, 1.76) plus-to-minus, det-linear estimate 1.742625, and (1.94, 1.96) minus-to-plus, det-linear estimate 1.946659** (centre to centre 0.2000, estimates 0.204034 apart; the "FINE READING: PAIR" line of `read_fine.py` is Part 2's rule and is not used here). ln|det| local minima: at 1.74 (ln -1612.211470) and at 1.94 (ln -1608.097878), each beside a change; **at 1.46 (ln -1609.506979) WITHOUT a change**, below its neighbours by 0.0054 and 0.0022. The float64 sign differs from the hybrid's at 2 of 56 points (1.76 and 1.94; information).

**The k_c test, the rule as amended (`kc_compare2.py`, `d1825_compare.log`):** k_c 63 roots 1.3885, 1.7425, 2.3187 (xfkappa, comment 7070296128), within 0.02 of the det-linear estimate.

| root | what | verdict |
|---|---|---|
| k_c 55 (1.74, 1.76), estimate 1.742625 | plus-to-minus | **STABLE**: 0.0001 from the k_c 63 root 1.7425 |
| k_c 55 (1.94, 1.96), estimate 1.946659 | minus-to-plus | **k_c-DEPENDENT (k_c 55 only)**: 0.2042 from the nearest k_c 63 root 1.7425 |
| k_c 63 root 1.3885 | plus-to-minus | **k_c-DEPENDENT (k_c 63 only)**: no k_c 55 change within 0.02 |
| k_c 63 root 1.7425 | minus-to-plus | MATCHED by the k_c 55 change in (1.74, 1.76) |
| k_c 63 root 2.3187 | plus-to-minus | **k_c-DEPENDENT (k_c 63 only)**: no k_c 55 change within 0.02 |

Summary: 2 robust k_c 55 changes; **stable 1** (information, the bracket marks: 1 wholly inside a band, 0 straddling, 0 outside); **k_c-dependent: 1 k_c 55 only and 2 k_c 63 only**; undetermined 0; not compared 0. The bracket reading of the first version of the rule would have given the same verdicts (the stable change's bracket is wholly inside the band 1.7225 to 1.7625; the other change's bracket is 0.1975 from the nearest root). **Orientation, information, not read:** the matched k_c 63 root 1.7425 is minus-to-plus, the k_c 55 change is plus-to-minus, the opposite; orientation readings wait for xfkappa's sign-convention check.

**The ln|det| minimum without a change, and its dip fit (`dip_fit2.py`, `d1825_dipfit.log`; information, a model fit):** at 1.460 (ln -1609.506979, below its neighbours by 0.0054 and 0.0022: shallow). The fit over the 11 points 1.36 to 1.56: l0 1.65802 (+- 0.00426), e 0.06700 (+- 0.00044), max residual 3.9e-4, rms 2.6e-4; over the same points a quartic polynomial leaves 1.2e-4 and a quadratic 1.1e-2. `dip_fit2.py` flags the fit "resolved at this step" (|e| above half a step, small uncertainty). **Two limits of this fit, reported and not fixed:** its centre l0 = 1.658 lies 0.098 above the window it was fitted on (the script does not check that), 0.085 from the k_c 55 root at 1.7426, and the quartic polynomial fits the same 11 points better than the model does. So the fit does not support a separate root pair near 1.46, and I read nothing from it. The ln|det| over 1.30 to 1.62 is a smooth shallow trough: -1609.1064 (1.30), -1609.5070 (1.46), -1609.4467 (1.60).

**cpu and memory (`d1825_samples.csv`, a sample every 60 s, 152 samples 23:29:10 to 02:03:50 UTC; my processes only).** The two python children (pids 40712 and 36640; the roots are launcher stubs): peak working set 0.78 and 0.73 GiB, private 1.29 and 1.28 GiB; 13051 and 12614 cpu-s; BelowNormal throughout; together at most 1.50 GiB working set and 2.56 GiB private in one sample. Machine: cpu mean 42.8% (1 s samples), max 58.5%; commit 51.7 to 58.9 of 101.5 GiB; free physical at least 46.1 GiB.
