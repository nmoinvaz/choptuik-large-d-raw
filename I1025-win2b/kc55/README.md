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
