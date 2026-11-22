# I1025-dh610/kc71_d19125: hybrid sign scan at D 19.125, k_c 71, lambda_1 1.44 to 1.58 at 0.01: is k_c 71 clean where k_c 63 broke?

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task from the coordinator (hc, 22 Nov 2026), after `../d1909/` (raw f2405ef9) and `../d19125/` (raw fedc68ff), which showed k_c 63 failing past D 19.1 (at D 19.125 no sign change in 1.505 to 1.545). win2's k_c 71 scan at D 19 (`I1025-win2/kc71_leap`, raw 2c37fd37) has one robust change, lambda_1 1.536547 (- to +), none near 1.4832, no minimum without a change. The test: does k_c 71 stay clean at D 19.125?

Information, not a pass rule: lambda_1's straight line from 1.675995 (D 18.5) to 1.536547 (D 19) (slope -0.2789 per unit D) puts it near 1.502 at D 19.125, inside the window.

## Setup

Budget: 1 process for the control, then 6 processes of 1 thread (OMP, OPENBLAS, MKL, VECLIB, RAYON = 1), nice 10, one systemd user unit `i1025h` (`lane_kc71.sh`, started by `start_kc71.sh`, log `exits_kc71.txt`), beside #997's rerun (unit `i997t`) and #1067's series (unit `i1067d`), not touched. Worktree `~/Source/choptuik-large-d-1025f` at 505d8399 (clean), `~/Source/venv-i1058/bin/python`, `P4_WT_MATTER=<worktree>/solver/matter`, `d18_hybsign.py` unmodified.

Inputs (raw origin/main fedc68ff, copied to `in/`, pinned by `git hash-object --no-filters`, `in_blobs.txt`; the lane script refuses to start on any other blob): `d18_hybsign.py` e089207a, `sol_l1kc71Lw1025_D19.000000.npy` f320a4c1, `sol_l1kc71Lw1025_D19.125000.npy` 42a4e4cc, `l1kc71Lw1025.jsonl` 18542c4c (record rows: D 19.0 |F| 2.7619908382539706e-10, 2676 steps; D 19.125 |F| 2.8421697420329494e-10, 2651 steps), win2's `scan_D19_P2.jsonl` b5aaf575 (its lambda 1.55 row: hybrid +1, ln|det| -2208.97905006932), the reader `read_lower.py` 89309d3c with `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9. All from `I1025-win2/kc71_leap/` or `I1025-dh610/d1909/in/`.

## Commands

1. Control, 1 process, cap 3 h by exact pid: `d18_hybsign.py in/l1kc71Lw1025.jsonl in/sol_l1kc71Lw1025_D19.000000.npy 19.0 1.55 control/scan_D19.0_p0.jsonl`. Pass (`control_check.py`, d1909's with the fixed +1 dropped so that it compares win2's sign, whatever it is): the log prints `the record system`; the hybrid sign equals win2's; ln|det| equals win2's -2208.97905006932 to 1e-6 relative (win2 is a Windows build). Otherwise stop and report, no scan.
2. Scan (only after the control passes and MemAvailable is at least 6 x the control's max RSS + 4 GB), 6 processes of 1 thread, cap 8 h each by exact pid: `d18_hybsign.py in/l1kc71Lw1025.jsonl in/sol_l1kc71Lw1025_D19.125000.npy 19.125 <lambdas> scan/scan_D19.125_p<p>.jsonl`; lambda 1.44 to 1.58 at 0.01 (15 values) plus a repeat of 1.50 at the end (16 evaluations); value i goes to process i mod 6 (`scan_hyb.sh`'s splitting), so the repeat (index 15) runs on process 3 and its original (index 6) on process 0. The system check is `d18_hybsign.py`'s first line per process (exit 3 stops it).
3. Reading: `read_lower.py scan 1.44 1.58` (dh170's, unedited; keys `round(lambda, 4)`) and `repeat_check.py` on the merged scan file.

## Acceptance and reading (the coordinator's, as before)

- the control matches; the system check passes on all six processes; the reader's selftest passes and its mutations `shift` and `round2` each exit 1 (`selftest_exits.txt`: read_lower 0, shift 1, round2 1, repeat_check 0, control_check 0, its mutate 1); the repeat of 1.50 agrees (ln|det| within 1e-6, bit-identical expected);
- read: every robust change with its det-linear estimate and estimator range (a spread over interpolation choices, not an enclosure), orientation as printed (not compared across D); any ln|det| minimum without a change; the repeat; changes touching a non-robust point listed and not counted. Roots are k_c 71 roots, not yet physical ones.

Estimate (coordinator's): about 45 min; win2's points took 671 s each on Windows; the control here measures one point alone, and the scan runs three rounds.

Written as the run goes.

## Control (22 Nov, 13:42:21 to 13:55:19 UTC): PASS

`d18_hybsign.py` at D 19.0, k_c 71, lambda 1.55 on win2's state and record, 1 process of 1 thread: wall 778 s (the point's own 775 s; win2's was 671 s on Windows), peak RSS 1.56 GB, exit 0 (`control/control.log`, `control/control_check.txt`; the checker's message labels the reference "dh370", a leftover string of the d1909 copy, the reference is win2's row `in/ref_win2_scan_D19_P2.jsonl`).
- the record system: |F| 2.7637774095e-10 against the record's 2.7619908383e-10 (win2's own log shows 2.7619908383e-10; the 6.5e-4 relative difference is inside the check's 1e-2 bar and the steps equal, 2676 = 2676), noting a Windows and a Linux build;
- hybrid sign +1 = win2's; ln|det| -2208.9791860890 against win2's -2208.97905006932, relative difference 6.158e-08 (bar 1e-06); both noise seeds +1;
- the float64 sign +1 equals win2's too, with ln|det| -2211.7827794789 against win2's -2207.274918285948 (float64 values differ by 4.5, as in the k_c 63 control).

Scan started 13:55:19 UTC on 6 processes (peak RSS of the control 1.56 GB, 6 x that fits in the 30 GB available). Points take about 780 s alone and 800 to 900 s beside the other runs; three rounds end near 14:50 UTC.

## Scan (22 Nov, 13:55:19 to 14:56:10 UTC): 15 points and the repeat, two robust changes

Six processes, all exit 0 (`exits_kc71.txt`), each logged the record system first (|F| 2.8436825420e-10 against the record's 2.8421697420e-10, steps 2651 = 2651). Points took 1065 to 1380 s each beside the other runs (the control alone: 778 s). Files: `scan/scan_D19.125_p<p>.jsonl`, merged `scan/scan_D19.125_1025.jsonl`, `read_lower.txt`, logs `scan/scan_p<p>.log`.

| lambda_1 | hybrid sign | hybrid ln\|det\| | float64 sign | float64 ln\|det\| | s |
|---|---|---|---|---|---|
| 1.44 | + | -2200.2158683400 | + | -2200.7690 | 1350 |
| 1.45 | + | -2200.7709471405 | + | -2198.5641 | 1361 |
| 1.46 | + | -2201.4134587150 | + | -2201.2072 | 1310 |
| 1.47 | + | -2202.2262366179 | - | -2200.3327 | 1339 |
| 1.48 | + | -2203.4969803381 | + | -2200.5475 | 1373 |
| 1.49 | - | -2204.9714703424 | + | -2201.6460 | 1380 |
| 1.5 | - | -2204.1731401735 | - | -2200.5331 | 1092 |
| 1.5 | - | -2204.1731401735 | - | -2200.5331 | 1176 |
| 1.51 | - | -2205.7298526121 | - | -2205.2004 | 1183 |
| 1.52 | + | -2203.7457971907 | + | -2203.7806 | 1158 |
| 1.53 | + | -2202.8034093328 | + | -2202.1814 | 1172 |
| 1.54 | + | -2202.2631656217 | + | -2202.3600 | 1167 |
| 1.55 | + | -2201.8926029996 | + | -2202.4863 | 1201 |
| 1.56 | + | -2201.6209927474 | + | -2202.4852 | 1122 |
| 1.57 | + | -2201.4169757782 | + | -2200.9305 | 1065 |
| 1.58 | + | -2201.2646088986 | + | -2203.5831 | 1134 |

The second 1.5 row is the repeat (process 3); its hybrid sign and ln|det| equal the first (process 0) bit for bit.

Reading (`read_lower.py scan 1.44 1.58`, dh170's, unedited; `read_lower.txt`):
- 15 distinct points, all noise-robust (both noise seeds agree with the hybrid sign); no non-robust point;
- hybrid signs, as printed: + from 1.44 to 1.48, - at 1.49, 1.50, 1.51, + from 1.52 to 1.58; endpoints + and +;
- robust change 1: between 1.480 and 1.490, + to -, det-linear 1.488137, estimator range [1.486996, 1.488137];
- robust change 2: between 1.510 and 1.520, - to +, det-linear 1.511209, estimator range [1.511209, 1.511571];
- the ranges are spreads over interpolation choices, not enclosures; the brackets are the grid steps (0.01);
- ln|det| local minima without a sign change: none (the two minima, 1.49 and 1.51 with the global one at 1.51, -2205.7298526121, each sit beside a change);
- the repeat of 1.50: `repeat_check.py` PASS, 2 evaluations agree;
- the float64 sign differs from the hybrid at 1.47 (hybrid +, float64 -) and 1.49 (hybrid -, float64 +), as in the k_c 63 scans: float64 is not a determinant sign here, the hybrid is read;
- orientation is as printed and not compared across D. Information only: the straight line of lambda_1 gave about 1.502, between the two changes (0.0231 apart); which change, if any, continues win2's D 19 change at 1.536547 is not decided here. The D 19 rows in `in/ref_win2_scan_D19_P2.jsonl` cover 1.50 to 1.60 only; the coordinator's remark "none near 1.4832" at D 19 comes from win2's full scan, not read here.

Acceptance: control passed; system check on all six processes; reader selftest 0 and mutations `shift` 1, `round2` 1 (`selftest_exits.txt`: 0 1 1 0 0 1 as wanted); the repeat agrees. Roots are k_c 71 roots at D 19.125, not yet physical ones.
