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

Not started (13:36 UTC).
