# I1025-win2/d18hi: cross-machine control (the Mac's D 18 point at lambda 1.8) and the D 18.1875 hybrid scan above the d18mid window, lambda 1.95 to 2.35, on win2

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session, beside win2b's jobs. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task: the coordinator's hc of 2026-11-21
(~16:15 UTC), after `../d18mid/` (D 18.1875, lambda 1.70 to 1.95: one robust change, plus to minus in (1.75, 1.76); post 7065489728), in two parts: (1) the control I proposed, the Mac's D 18 point at lambda 1.8 on win2;
(2) a scan of D 18.1875 above that window, lambda 1.95 to 2.35 at 0.01, two processes with 1.95 repeated as the check.

## Setup (written 2026-11-21 16:16 UTC, before any run)

| | |
|---|---|
| part 1 command (the Mac's, `I1025-mac/d18/lane_d18b.sh`, quoted) | `timeout 3600 nice -n 10 $PY -u $Q/d18_hybsign.py $STUB $ST 18 1.8 $HS`, `ST=$Q/sol_l1kc63W1025_D18.000000.npy`, `STUB=$Q/d18_stub_l1kc63W1025.jsonl`, 4 threads (`OPENBLAS/OMP/MKL/RAYON_NUM_THREADS=4`), `P4_WT_MATTER=$W`, cwd the worktree's `solver/matter` |
| part 1 on win2 | `python.exe -u D:/choptuik-large-d-raw-push/I1025-mac/d18/d18_hybsign.py STUB ST 18 1.8 ctl_D18_lam1.8.jsonl` (absolute paths in the log's first line), the same blobs as the Mac (state 45e72c6a, stub 2cfdb833, `d18_hybsign.py` e089207a), 4 threads, BelowNormal, cap 3600 s by the exact root pid, venv-md510 (multidouble 5.1.0) in place of the Mac's venv-1025dd |
| the Mac's result (`I1025-mac/d18/d18_hybsign_1025.jsonl`) | sign +1, ln\|det\| -1925.018228986828, noise signs [1, 1], float64 +1 and -1920.991037082774, |F| 2.6296169382e-10 against the record's 2.6303452558e-10, steps 2552, 353 s |
| part 2 command | xfkappa's `d18_hybsign.py REC ST 18.1875 L OUT` as in `../d18mid/` (REC = `l1kc63Wm1025.jsonl` 08f4dbf3, ST = `sol_l1kc63Wm1025_D18.187500.npy` 3f06b92e), `P4_WT_MATTER=D:/choptuik-i1025d/solver/matter`, 4 threads each, BelowNormal, venv-md510; **process A**: L = 1.95, 1.96, ..., 2.15 (21 points), OUT = `scan_hi_D18.1875_A.jsonl`; **process B**: L = 1.95, then 2.16, 2.17, ..., 2.35 (the check point, then 20 points), OUT = `scan_hi_D18.1875_B.jsonl`; each capped at 28800 s (8 h) by the exact root pid (`taskkill /T /F /PID` after the command line is checked) |
| solver code | worktree `D:/choptuik-i1025d` at 48c36355: `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's (the pin of `lane_d18b.sh`) and `ell_delta.py` equals 48c36355's; the driver checks them and the blobs of every input (the d18mid blobs plus the D 18 state and stub) and refuses otherwise |
| reader | xfkappa's `d18d_read.py` (blob 6b608903, with `d185_scan_read.py` 7c9d400f and `d18c_read.py` 1383470f; copies in `../d18mid/pinned/`), unchanged |
| run | `run_d18hi.sh`: pins and controls, then the control, then (only if the control passed) the two scans side by side, then the reader on this window's two files and on all four D 18.1875 files (d18mid's two and these two, lambda 1.70 to 2.35), `points_table_hi.py` |
| memory | `mem_watch.ps1`, `commit_watch.ps1`: alert-only, 30 s samples, kill nothing. I tell the coordinator at commit over 99 GB, a page file up by 2 GB, or available under 1 GB for 5 min. win2b's scans share the machine |

## Windows (fixed before the run)

- Part 1: D 18, k_c 63, lambda 1.8, one point.
- Part 2: D 18.1875, k_c 63, **lambda 1.95 to 2.35 at 0.01: 41 points**, ascending, as two processes: A takes 1.95 to 2.15 (21 points), B takes 1.95 and 2.16 to 2.35 (21 evaluations). The check point 1.95 is in both, so the reader's repeated-point rule compares them
  (same sign, ln|det| within 1e-6); it is also the last point of `../d18mid/`'s process B, so the reading of all four files compares three evaluations of it. The reader prints lambda_0 = 2.1197426515 (error 5.2e-9) for D 18.1875, inside this window.
- Each point: the hybrid sign (float64 blocks 0-11, double-double block 12), the noise test (1e-15 relative noise on blocks 0-11, 2 seeds), the float64 sign beside.

## Readings fixed before the run (the coordinator's, with xfkappa's reader's definitions)

1. **Control (part 1): the same sign (+1) with ln|det| within 1e-2 of -1925.018228986828** (the hybrid's float64 noise) means win2's environment and the Mac's agree, so any sign pattern across D belongs to the states. **A different sign** means an environment difference, and then every cross-machine orientation is void.
   Added by me from xfkappa's rule: the point must be noise-robust; if the control run does not finish or fails, **the scan is not started** (AGENTS.md: a control that fires on real data stops the work until the cause is known) and I report it for the coordinator's decision.
2. **Scan (part 2): a robust sign change** (both grid points noise-robust; a change that touches a non-robust point is listed, not counted) **places the second root at D 18.1875**, with its bracket and estimator range (information, not a bound), its delta from lambda_0, and its orientation (the sign below to the sign above),
   **reported but not compared across states until xfkappa's sign-convention check is in**. Every ln|det| local minimum without a sign change beside it is reported. No robust change in 1.95 to 2.35 means no second root in that window (with d18mid's window: none in 1.76 to 2.35).
3. A cap that fires, or a scan that exits non-zero, is a result: the points done are read and reported as partial; nothing is rerun or loosened. Exit 3 (not the record system) stops that scan. A repeated point that disagrees is STOP-level, no reading.
4. Seconds per point are reported (this machine, this load), not compared with xfkappa's.

## Controls

- `ctl_check.py --selftest` (exit 0: the Mac's own values agree; the sign flipped, ln off by 0.05 and a non-robust point do not; ln off by 5e-3 does) and `--selftest --break` (exit 1), and the reader's selftest (0) and `--mutate=orient` (1), run by the driver before the control;
- the control itself (part 1), the scans' record-system check (exit 3 if the state does not reproduce its record's |F| and step count), and the repeated point 1.95.
- `points_table_hi.py` was tested on planted scans (42 rows: 41 points and the repeat).

## Result (control and scans 2026-11-21 16:17:14 to 19:00:09 UTC)

### Part 1, the control: agrees

The Mac's D 18 point at lambda 1.8 on win2 (516 s; the record-system check passed: |F| 2.6321882772e-10 here against 2.6296169382e-10 on the Mac and the record's 2.6303452558e-10, steps 2552 on both):

| | sign | ln\|det\| | noise signs (1e-15, 2 seeds) | float64 sign, ln\|det\| |
|---|---|---|---|---|
| Mac (`I1025-mac/d18/d18_hybsign_1025.jsonl`) | +1 | -1925.018228986828 | [+1, +1] | +1, -1920.991037082774 |
| win2 (`ctl_D18_lam1.8.jsonl`) | +1 | -1925.019115375994 | [+1, +1] | +1, -1923.714158510 |

Reading 1 (the coordinator's, fixed before the run): the same sign, ln|det| difference -8.9e-4 against the bar 1e-2, noise-robust: **win2's environment and the Mac's agree**, so a sign pattern across D belongs to the states (on this point; the control is one point). `ctl_check.txt` has the verdict;
`ctl_check.py --selftest` passes and `--selftest --break` exits 1 (`selftest_ctl*.txt`). The float64 ln|det| beside differs by 2.7 (float64 noise), the hybrid's does not.

### Part 2, the scan of D 18.1875 above the d18mid window

Both processes ran to the end (exit 0, no cap): A 21 points in 9254 s (425 to 495 s per point), B 21 points in 9190 s (420 to 513 s per point), 4 threads each, BelowNormal, win2b's scans on the machine. Both passed the scan's record-system check
(|F| 2.7545108188e-10 against the record's 2.7479600600e-10, steps 2519 = 2519). All 41 points are noise-robust. The reader (`d18d_read.py`, blob 6b608903; pins checked again at the end) on this window's two files (`read_hi_D18.1875.log`):

| reading (the coordinator's) | D 18.1875, lambda 1.95 to 2.35 at 0.01 (41 points) |
|---|---|
| robust sign changes | **none**: the hybrid sign is -1 at all 41 points, every one noise-robust |
| changes touching a non-robust point | none |
| ln\|det\| local minima without a sign change | **none**: ln\|det\| rises monotonically from -1910.6791 (1.95) to -1897.4803 (2.35), steps 0.312 to 0.362, with no dip at lambda_0 = 2.1197426515 (-1905.4704, -1905.1584, -1904.8462 at 2.11, 2.12, 2.13) |
| repeated point 1.95 (A and B) | agree: -1 in both, ln\|det\| -1910.6791132275 in both (difference 0.0); the same value as d18mid's process B (the third evaluation, `read_all_D18.1875.log`) |
| float64 beside | no float64 sign change in the window, and float64 agrees with the hybrid at all 41 points (in the d18mid window it differed at 6 of 26) |

So **no second root is placed at D 18.1875 in 1.95 to 2.35**. With d18mid's window (all four files, 66 points, 1.70 to 2.35, `read_all_D18.1875.log`): one robust change, plus to minus in (1.75, 1.76) (det-linear 1.754208, range [1.754208, 1.754399], delta -0.365535 from lambda_0), no ln|det| minimum without a change, the repeats 1.75 (d18mid) and 1.95 (three evaluations) agree exactly. The sign is -1 from 1.76 to 2.35. Orientation is not compared across states (the coordinator's reading: until xfkappa's sign-convention check is in); by the control's reading (one point, D 18) the sign pattern across D, including d18mid's flipped orientation, belongs to the states and not to the environment.

`points_hi_D18.1875.md` lists the 42 evaluations (41 points and the repeat). Memory: lowest available 50.22 GB, peak commit 50.48 GB of 101.47 GB, page file peak 2610 MB (as at the start); no alert fired (no `alerts.log`).
Slips: the driver wrote `ctl_check.txt` into the worktree's `solver/matter` (its cwd at that step); I moved it to this folder before 16:27 UTC (just after the control ended at 16:25:51), nothing else in the worktree was touched. The first line of `exits_d18hi.txt` onward is one run (driver pid 23296); no relaunch.
