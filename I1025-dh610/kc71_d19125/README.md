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
