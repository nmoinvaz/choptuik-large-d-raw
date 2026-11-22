# I1025-dh610/d1909: fine hybrid sign scan at D 19.09375 (k_c 63), lambda_1 1.480 to 1.540, with a control at D 19.0

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task from the coordinator (hc, 22 Nov 2026), beside #997's rerun (unit `i997t`) and #1067's series (unit `i1067d`), which are not touched.

Why: dh370 found two roots 0.055 apart at D 19, + to - at 1.4832 and - to + at 1.5380 (lambda_1); straight-line tracks put them together near D 19.08; dh170 scans D 19.03125 (`I1025-dh170/lower_root`, raw 439969da). A scan just past the predicted meeting shows whether both roots are still there at D 19.09375.

Budget: 6 processes of 1 thread (OMP, OPENBLAS, MKL, VECLIB, RAYON = 1), nice 10, one systemd user unit `i1025f` for the lane script. Worktree `~/Source/choptuik-large-d-1025f` at 505d8399 (detached, clean), `P4_WT_MATTER=<worktree>/solver/matter`, `~/Source/venv-i1058/bin/python` (numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, `multidouble.dd_logdet`).

## Inputs (raw origin/main c4ce326b, copied to `in/`, pinned by `git hash-object --no-filters`; `in_blobs.txt`; the lane script refuses to start on any other blob)

| file in `in/` | from | blob |
|---|---|---|
| `d18_hybsign.py` (xfkappa's, unmodified) | `I1025-dh170/kc_break/d18_hybsign.py` | e089207a |
| `sol_l1kc63dh370_D19.093750.npy` | `I1025-dh370/kc63_leap/` | 5583a185 |
| `sol_l1kc63dh370_D19.000000.npy` | `I1025-dh370/kc63_leap/` | 589b55d7 |
| `l1kc63dh370.jsonl` (record rows for D 19.0 and D 19.09375) | `I1025-dh370/kc63_leap/` | d75eade5 |
| `ref_dh370_scan_D19.000000_p0.jsonl` (dh370's timed lambda 1.55 at D 19: sign +1, ln|det| -1878.116180163286) | `I1025-dh370/hyb_D19.000000_time/scan_D19.000000_p0.jsonl` | 2b9be2cb |
| `scan_hyb.sh` (the model for splitting lambdas over processes) | `I1025-dh370/scan_hyb.sh` | 4be62f86 |
| `read_lower.py`, `d185_scan_read.py`, `d18c_read.py`, `repeat_check.py` (dh170's reader and its deps) | `I1025-dh170/lower_root/` | 89309d3c, 7c9d400f, 1383470f, aaf598a9 |

The coordinator's message named `scan_hyb.sh (b2fbeba6)` and `read_d19.py (dd910799)`: those are raw commits that added the files (their blobs are 4be62f86, unchanged between the two commits, and 13bd4997); the pins above are blobs.

## Commands (`lane_d1909.sh`, started by `start_d1909.sh`; log `exits_d1909.txt`)

1. Control, 1 process, cap 3 h by exact pid: `d18_hybsign.py in/l1kc63dh370.jsonl in/sol_l1kc63dh370_D19.000000.npy 19.0 1.55 control/scan_D19.0_p0.jsonl`. Pass (`control_check.py`): the log prints `the record system`, hybrid sign +1 equal to dh370's, ln|det| equal to dh370's -1878.116180163286 to 1e-6 relative. Otherwise stop, no scan: this machine's build differs.
2. Scan (only after the control passes and MemAvailable is at least 6 x the control's max RSS + 4 GB), 6 processes of 1 thread, cap 8 h each by exact pid: `d18_hybsign.py in/l1kc63dh370.jsonl in/sol_l1kc63dh370_D19.093750.npy 19.09375 <lambdas> scan/scan_D19.09375_p<p>.jsonl`; lambda 1.480 to 1.540 at 0.005 (13 values) plus a repeat of 1.510 at the end (14 evaluations); value i goes to process i mod 6 (scan_hyb.sh's splitting), so the repeat (index 13) runs on process 1 and its original (index 6) on process 0. The system check is `d18_hybsign.py`'s first line per process (rebuilt |F| and steps against the record; exit 3 stops that process).
3. Reading: `read_lower.py scan 1.480 1.540` (dh170's, three-decimal keys; dh370's `read_d19.py` rounds lambda to two decimals and cannot read a 0.005 grid) and `repeat_check.py` on the merged scan file.

## Pass rules (fixed before the run)

- the control matches (above); the system check passes on all six processes;
- the reader's planted selftest passes and its mutations `--mutate=shift` and `--mutate=round2` each exit 1; `repeat_check.py selftest` passes; `control_check.py selftest` passes and its `--mutate` exits 1 (all run by the lane script before the start; `selftest_*.log`, `selftest_exits.txt` 0 1 1 0 0 1 in that order);
- the repeat of 1.510 agrees (sign, noise signs, float64 sign, ln|det| within 1e-6; bit-identical is expected, as in dh170's runs);
- read: every robust sign change with its det-linear estimate and estimator range (a spread over interpolation choices, not an enclosure), orientation as printed (not compared across D); changes touching a non-robust point listed and not counted; every ln|det| minimum without a change flagged. The coordinator rules on the tracks.

Estimate (coordinator's): setup about 20 min, the scan 1 to 1.5 h on 6 processes; the 1-thread time of one point is measured by the control (dh370's timed point took 735 s on 6 threads).

Written as the run goes.
