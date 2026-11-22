# I1025-dh610/kc71_d19low: hybrid sign scan at D 19.0, k_c 71, lambda_1 1.00 to 1.40 at 0.02: where is the lower root at D 19?

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task from the coordinator (hc, 22 Nov 2026), after `../kc71_d19125/` (raw ee09203f): at D 19.125 k_c 71 has two robust changes, 1.488137 (+ to -) and 1.511209 (- to +). The coordinator's reading: at k_c 71 the signs below 1.48 are minus at D 19 and plus at D 19.125, so k_c 71 has a lower root too, below the 1.40 edge of win2's D 19 scan and rising to 1.488 by D 19.125; at k_c 63 it sat at 1.4832 at D 19. Called "the lower root" here, its physical status open.

Information, not a pass rule: the lower root should be below 1.40 at D 19 (the coordinator's reading); the scan covers 1.00 to 1.40. win2's D 19 rows (`in/ref_win2_scan_D19_P2.jsonl`, 1.50 to 1.60) have the hybrid sign - up to 1.53 and + from 1.54.

## Setup

Budget: 6 processes of 1 thread (OMP, OPENBLAS, MKL, VECLIB, RAYON = 1), nice 10, one systemd user unit `i1025i` (`lane_kc71low.sh`, started by `start_kc71low.sh`, log `exits_kc71low.txt`), beside #1067's series (unit `i1067d`, 10 threads), not touched. Worktree `~/Source/choptuik-large-d-1025f` at 505d8399 (clean), `~/Source/venv-i1058/bin/python`, `P4_WT_MATTER=<worktree>/solver/matter`, `d18_hybsign.py` unmodified.

No control run here (the coordinator's order): the control passed in `../kc71_d19125/control/` (22 Nov, same machine, build, state, record and script: D 19.0, lambda 1.55, record system, win2's hybrid sign, ln|det| within 6.158e-08 relative of win2's). The lane script refuses to start unless that control's check file says PASS.

Inputs (copied from `../kc71_d19125/in/`, raw ee09203f; pinned by `git hash-object --no-filters`, `in_blobs.txt`; the lane script refuses to start on any other blob): `d18_hybsign.py` e089207a, `sol_l1kc71Lw1025_D19.000000.npy` f320a4c1 (win2's state at D 19.0), `l1kc71Lw1025.jsonl` 18542c4c (win2's record rows), win2's `scan_D19_P2.jsonl` b5aaf575, the reader `read_lower.py` 89309d3c with `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9.

## Commands

1. Pre-run checks (lane script): the pins; worktree clean at 505d8399; the reader's selftest exits 0 and its mutations `shift` and `round2` each exit 1; `repeat_check.py selftest` 0 (`selftest_exits.txt`: 0 1 1 0); MemAvailable at least 6 x the control's max RSS (1556924 kB) + 4 GB.
2. Scan, 6 processes of 1 thread, cap 8 h each by exact pid: `d18_hybsign.py in/l1kc71Lw1025.jsonl in/sol_l1kc71Lw1025_D19.000000.npy 19.0 <lambdas> scan/scan_D19.0_p<p>.jsonl`; lambda 1.00 to 1.40 at 0.02 (21 values) plus a repeat of 1.20 at the end (22 evaluations); value i goes to process i mod 6 (`scan_hyb.sh`'s splitting), so the repeat (index 21) runs on process 3 and its original (index 10) on process 4; four rounds on processes 0 to 3, three on 4 and 5. The system check is `d18_hybsign.py`'s first line per process (exit 3 stops it).
3. Reading: `read_lower.py scan 1.00 1.40` (dh170's, unedited; keys `round(lambda, 4)`, spacing-agnostic) and `repeat_check.py` on the merged scan file.

## Acceptance and reading (the coordinator's)

- the system check passes on all six processes; the reader's selftest passes and its mutations each exit 1; the repeat of 1.20 agrees (ln|det| within 1e-6, bit-identical expected);
- read: every robust change with its det-linear estimate and estimator range (a spread over interpolation choices, not an enclosure), orientation as printed (not compared across D); any ln|det| minimum without a change; the repeat; changes touching a non-robust point listed and not counted. Roots are roots of this k_c, physical status open.

Estimate (coordinator's): about 1 h; points took 780 s alone and 1065 to 1380 s beside other jobs in the D 19.125 scan.

Written as the run goes.
