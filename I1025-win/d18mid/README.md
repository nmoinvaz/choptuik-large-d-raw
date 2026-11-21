# I1025-win/d18mid: the hybrid sign scan at D 18.125, k_c 63, on xfkappa's leap state (winb)

Written before the run, 2026-11-21 13:36 UTC by my clock (the first push, a9e63b35, read 13:38 by a stamp I typed before checking the clock; corrected at 13:36 UTC).

## Order

The coordinator (hc, about 13:25 UTC): between D 18 (two roots, 1.775 minus-to-plus and 1.807 plus-to-minus) and D 18.25 (one root, 1.7425) the pair of roots either crossed or met. On a 0.25 grid in D the scans cannot tell which (xfkappa, #1025 comment 7063268832). The leap saved states between them. Scan D 18.125 with xfkappa's `d18_hybsign.py` (raw `I1025-mac/d18`, command quoted below) on raw `I1025-mac/d18/sol_l1kc63Wm1025_D18.125000.npy` (k_c 63), lambda 1.70 to 1.95 at 0.01, with the noise test and the float64 sign, 4 threads, BelowNormal, 8 h cap by exact pid. Window and reading go into this README before the run, raw `I1025-win/d18mid`. Post on #1025 with cpu and memory.

Change of plan, the coordinator's word (hc, about 13:34 UTC by my clock, after I asked): "split. Run two processes of 13 points each, 4 threads each, with the per-point seeds unchanged. Then check in the README that one point repeated in both halves gives the same sign and ln|det| to 1e-6." The points are independent: `d18_hybsign.py` builds the system once, then evaluates each lambda with its own fixed noise seeds (`default_rng(100 + k)`), so a split changes nothing per point.

## Inputs (raw origin/main, taken by `git show`, checked with `git hash-object --no-filters`; `prep_d18mid_inputs_1025.log`)

| item | raw path | blob |
|---|---|---|
| scanner | `I1025-mac/d18/d18_hybsign.py` | e089207a61fbd98614716abd309571cbc4888db2 |
| state | `I1025-mac/d18/sol_l1kc63Wm1025_D18.125000.npy` | 5bf7b711a2dbbabb664201e182f90b79d88bb037 (raw commit 500b1ed2) |
| record | `I1025-mac/d18/l1kc63Wm1025.jsonl`, the leap's D 18.125 line (F 2.711734411402158e-10, 2528 steps, kappa 0.7, u0 0.04, Ks 30, h 0.0625) | 08f4dbf367edba55814e5cf989ccd32a9a5dbe67 |
| the lane script quoted below | `I1025-mac/d18/lane_d185S.sh` | a019238b1dfbd91c7f258ea64d617c1edd2e9cb6 |
| D 18 and D 18.5 scans (reader tests) | `I1025-mac/d18/d18_scan_1025.jsonl`, `d185_scan_1025.jsonl` | ac80e9d5, 90540daf |

Code: worktree `C:/Users/nathan/Source/choptuik-i1025-lowd` at 505d8399 (`P4_WT_MATTER`; xfkappa's lane checks its solver code equals 505d8399), PY `venv-md510` (Python 3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble 5.1.0), BelowNormal, 4 BLAS and rayon threads per process.

## The scan command, quoted

`d18_hybsign.py` docstring: `usage (venv-1025dd): d18_hybsign.py STUB.jsonl STATE.npy D LAMS OUT.jsonl   (LAMS comma-separated)`; it takes the record line at D from the first file (the leap's jsonl works as it is), rebuilds the record's discrete system (`|F|` within 1% and equal steps, else exit 3) and, at each lambda, prints the hybrid sign and ln|det| (`p4_hybrid.py`'s `sd()`, unchanged) with its 1e-15 noise test on blocks 0 to 11 (2 seeds) and the plain float64 sign beside it.

xfkappa's D 18.5 scan in `lane_d185S.sh` (blob a019238b):

```
L=$($PY -c 'print(",".join(f"{1.55 + 0.01 * i:.2f}" for i in range(36)))')
timeout 21600 nice -n 10 $PY -u $Q/d18_hybsign.py $REC $ST 18.5 $L $SCAN < /dev/null 2>&1 | grep --line-buffered -vE 'Warning|^  [a-z]+ = ' > $Q/d185_scan.log
```

Mine, per process: `python -u d18_hybsign.py <raw l1kc63Wm1025.jsonl> <raw sol_l1kc63Wm1025_D18.125000.npy> 18.125 <LAMS> <OUT>`, started by `d18mid_driver_1025.py` (no `nice`, BelowNormal by the launcher; the same warning filter on the log copy).

## Window and lambda lists, fixed before the run

Window: lambda 1.70 to 1.95 at 0.01, 26 points. It holds both D 18 roots (1.7750 and 1.8063 to 1.8076), D 18.25's root (1.7425) and the region between; D 18.5's root is at 1.6772.

| process | lambda, in this order | points |
|---|---|---|
| A | 1.82, then 1.70, 1.71, ..., 1.81 | 13 |
| B | 1.82 again, then 1.83, 1.84, ..., 1.95 | 14 |

The repeated point (1.82, first in both) makes 27 evaluations for 26 distinct points; the coordinator asked for the repeat. Each process has a cap of 28800 s (8 h) and is killed at the cap by the exact pid of the process the driver started (`taskkill /PID <pid> /T /F`; tested on dummy children, `d18mid_driver_selftest.log`).

## Reading, fixed now (the coordinator's, hc about 13:25 UTC)

Report every robust change with its orientation and every ln|det| local minimum without a change. Two changes give the gap at D 18.125, beside D 18's 0.0325. No change where the pair was, with a ln|det| minimum, means they met before D 18.125.

Definitions, as implemented in `read_d18mid_1025.py` (tested on xfkappa's scans: D 18 gives the changes (1.77, 1.78) minus-to-plus and (1.80, 1.81) plus-to-minus with minima at 1.78 and 1.81 beside them; D 18.5 gives the change (1.67, 1.68) minus-to-plus and a minimum at 1.68 beside it; `vtest/read_d18_scan_1025.log`, `vtest/read_d185_scan_1025.log`):

- a point is robust if the hybrid's sign survives its 1e-15 noise test (2 seeds); a change is two consecutive points of different hybrid sign, robust if both points are; its orientation is minus-to-plus or plus-to-minus;
- a ln|det| local minimum is an interior point whose ln|det| is below both neighbours'; it is "beside a change" if its sign differs from a neighbour's, else "WITHOUT a change"; a point at the scan's end that is below its only neighbour is listed as "at the scan edge";
- with two robust changes the gap is given between the brackets and centre to centre; the step is 0.01, so the gap is known to about 0.01 (D 18's 0.0325 is the coordinator's figure; this reader gives 0.030 centre to centre on D 18's 0.01 grid);
- the float64 sign beside the hybrid is information.

A pair closer than 0.01 gives no change on this grid; the ln|det| minimum without a change is the reading for that case. Nothing else is read into the scan.

## Repeat check, fixed now

At the repeated lambda 1.82 the two records must have the same hybrid sign and ln|det| equal to 1e-6 (`merge_d18mid_1025.py`; planted cases pass or fail as they should, `vtest/merge_selftest.log`). The merged 26-point scan is written, and the reader run, only if this check passes and every lambda from 1.70 to 1.95 is present. The result of the check is written into this README after the run.

## Run

`d18mid_driver_1025.py` (launcher `start_d18mid_1025.cmd`, BelowNormal): checks the pins, runs the two processes, merges, reads. Output: `d18mid_w.log`, `d18mid_scanA_1025.jsonl`, `d18mid_scanB_1025.jsonl`, `d18mid_scan_1025.jsonl` (merged), the filtered logs `d18mid_scanA.log`, `d18mid_scanB.log`, `rows/*_raw.log`, `rows/d18mid_merge.log`, `rows/d18mid_reading.log`. A sampler (`sample_driver_1025.ps1`, invariant number format) writes every 60 s each python's cpu seconds, working set, private bytes and their peaks, and the laptop's free memory, cpu load and commit, to `rows/d18mid_samples.csv`. The D 18.5 driver ended at 13:32:24 UTC, so the scans start at once.

Estimate: one hybrid evaluation took 700 s at 4 threads on this laptop (the D 18.5 row), so 14 points take about 2.7 h per process, in parallel: done about 16:30 UTC. No RESUME.

## Status

Done 2026-11-21 16:48:28 UTC (the result section below).

## Repeat check, first result (13:54 UTC, from the first point of each half; `merge_d18mid_1025.py` on the two scan files)

At lambda 1.82 (computed first in both processes, 981 s and 982 s): hybrid sign -1 in A and -1 in B; ln|det| -1915.151114652328 in A and -1915.151114652328 in B, difference 0.000e+00 (bar 1e-6); noise robust True in both; float64 sign -1 in both. **PASS.** The final check on the merged run is repeated at the end.

Timing: a point takes about 980 s with the two processes running together (the laptop at 90 % cpu; one process alone took 700 s a point at D 18.5), so A (13 points) ends about 17:10 and B (14 points) about 17:30 UTC.



## Result (2026-11-21 13:36:57 to 16:47:18 UTC; written 16:50 UTC)

The two halves ran 13:36:57 to 16:36:58 (A, 13 points, 10800 s, exit 0) and to 16:47:18 (B, 14 points, 11420 s, exit 0); neither hit its cap. `d18mid_scan_1025.jsonl` holds the 26 merged points (1.70 to 1.95 at 0.01), `rows/d18mid_reading.log` the reading, `rows/d18mid_merge.log` the repeat check. Record system true in both processes (|F| 2.7166033527e-10 against 2.7117344114e-10, 2528 steps against 2528).

**Repeat check (final): PASS.** At lambda 1.82, computed first in both halves (981 s and 982 s): hybrid sign -1 in A and in B; ln|det| -1915.151114652328 in both, difference 0.000e+00 (bar 1e-6); noise robust in both; float64 sign -1 in both. All 26 lambda from 1.70 to 1.95 are present once in the merged file.

**The scan, read as the coordinator fixed it:**

| item | value |
|---|---|
| noise robustness | every one of the 26 points is noise robust |
| hybrid signs | plus at 1.70 to 1.77 (8 points), minus at 1.78 to 1.95 (18 points) |
| robust changes | **one**: in (1.77, 1.78), **plus-to-minus** |
| ln\|det\| local minima | 1.77 (ln -1919.1387), **beside the change**; 1.70 (ln -1916.9555), **at the scan edge** (it lies 0.024 below the value at 1.71, -1916.9318; at 1.77 the dip is 1.4 below both neighbours) |
| ln\|det\| local minima without a change | none inside the window; the 1.70 point is the window's edge |
| second change | none in 1.70 to 1.95, so no gap can be given at D 18.125 |
| float64 beside the hybrid (information) | its sign differs from the hybrid's at 7 of 26 points: 1.70, 1.72, 1.73, 1.74, 1.75, 1.76, 1.77 |

ln|det| along the scan (hybrid): 1.70 -1916.955, 1.71 -1916.932, 1.72 -1916.932, 1.73 -1916.968, 1.74 -1917.059, 1.75 -1917.248, 1.76 -1917.659, 1.77 -1919.139, 1.78 -1917.760, 1.79 -1916.734, 1.80 -1916.092, 1.81 -1915.586, 1.82 -1915.151, then rising by 0.3 to 0.4 per step to 1.95 (-1910.983).

For the coordinator's rules: D 18.125 shows one robust change, not two, so there is no gap to set beside D 18's 0.0325; and it is not "no change where the pair was": the one change sits in (1.77, 1.78), where D 18's minus-to-plus change was, with the orientation plus-to-minus, the orientation of D 18's upper change. Nothing near (1.80, 1.81), where D 18's upper root was, changes sign. The ln|det| profile has its one dip, at 1.77, and no dip near 1.80 to 1.81 (there ln|det| rises steadily). The scan's lower edge, 1.70, is where ln|det| turns down slightly (a possible further minimum below 1.70 is outside the window). Which reading applies is the coordinator's; the numbers above are the evidence.

**CPU and memory** (`rows/d18mid_samples.csv`, every 60 s, 730 rows; the peaks are the process counters): the two scan pythons (BelowNormal, up to 13 threads): A 15027 cpu s in 10800 s (1.39 cores on average), B 15982 cpu s in 11420 s (1.40 cores); working set peak 1.056 GB in both; private bytes peak 1.630 and 1.629 GB. Laptop: cpu 26 to 93 %, free memory at least 12.0 GB of 31.83 GB, commit at most 26.4 GB of limit 41.3 GB; other sessions' single-thread pythons ran beside. A point took 640 to 1070 s (981 s at 1.82), about 800 s on average, with the two processes together. The driver ended at 16:48:28 and the lambda 1.20 dd check (`I1025-win/d18ref120`) started at 16:48:57 UTC.


## Ruling on the reading (the coordinator, hc received 16:51 UTC by my clock)

Neither of the two readings fixed before the run applies. The result is recorded by position, as roots are now tracked within each state's map: **one robust root at D 18.125, in (1.77, 1.78)**. It lies on a smooth falling track through the states: 1.795 (D 18.0625), 1.775 (D 18.125), 1.754 (D 18.1875), 1.7425 (D 18.25), 1.677 (D 18.5). Its orientation (plus-to-minus here) is not compared across D, since other roots cross the references between these states. Where D 18's second root went is for win2b's and win2's scans above lambda 1.95 and for the lambda 1.20 dd check (`I1025-win/d18ref120`). The numbers in the Result section above stand unchanged.
