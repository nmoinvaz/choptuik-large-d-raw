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

## Control (22 Nov, 12:04:45 to 12:13:42 UTC): PASS

`d18_hybsign.py` at D 19.0, lambda 1.55 on dh370's state and record, 1 process of 1 thread: wall 537 s (the point's own 535 s; dh370's timed point took 735 s on 6 threads), peak RSS 1.12 GB, exit 0 (`control/control.log`, `control/control_check.txt`).
- the record system: |F| 2.6104982620e-10 against the record's 2.6080821854e-10, steps 2374 = 2374;
- hybrid sign +1 = dh370's, ln|det| -1878.1161801633 = dh370's -1878.116180163286, relative difference 0 (the bar is 1e-6; the printed ln has ten decimals, `control_check.py` compares the full floats);
- noise-robust: both seeds +1.
- the float64 sign beside it differs from dh370's: here sign -1, ln|det| -1878.0453604869; dh370's row has sign +1, ln|det| -1880.5874620354. It is the plain float64 slogdet of the unscaled blocks, which the hybrid replaces (its blocks 0-11 are float64 too, block 12 is double-double), and it is not part of the control's bar; reported as a disagreement with dh370's float64 row (thread count 1 here, 6 there).

Scan started 12:13:42 UTC on 6 processes; one point costs about 540 s on one thread, so the longest process (3 points: lambda 1.480, 1.510, 1.540 on process 0; 1.485, 1.515, repeat 1.510 on process 1) ends near 12:45 UTC.

## Scan (22 Nov, 12:13:42 to 12:51:26 UTC): both roots are still there at D 19.09375

Six processes of 1 thread at nice 10 (`scan/`), exits 0 at 12:41:37, 12:41:43, 12:50:51, 12:51:26 UTC (and two earlier); each point 567 to 860 s (the control's 535 s was run alone), wall per process 27:51 to 37:44, peak RSS 1.30 to 1.36 GB each, 36 to 56 GB available, load 5 to 12 (`scan/sampler.log`). The system check printed `the record system` on all six (|F| 2.6666494365e-10 against the record's 2.6665561747e-10, steps 2359 = 2359, `scan/scan_p<p>.log`). `scan/scan_D19.09375_1025.jsonl` is the merged file; the reading is `read_lower.txt` (dh170's `read_lower.py`, blob 89309d3c, run with its selftest and mutations before the start).

| lambda | hybrid sign | ln\|det\| | noise-robust | float64 sign |
|---|---|---|---|---|
| 1.480 | + | -1867.3408088559 | yes | + |
| 1.485 | + | -1867.7532532817 | yes | + |
| 1.490 | + | -1868.2150939343 | yes | + |
| 1.495 | + | -1868.7505890083 | yes | + |
| 1.500 | + | -1869.4099943488 | yes | + |
| 1.505 | + | -1870.3354617898 | yes | + |
| 1.510 | + | -1872.6550208164 | yes | + |
| 1.510 (repeat) | + | -1872.6550208164 | yes | + |
| 1.515 | - | -1871.3913024720 | yes | + |
| 1.520 | - | -1871.0945024343 | yes | + |
| 1.525 | - | -1871.3486835703 | yes | + |
| 1.530 | - | -1872.5429585918 | yes | + |
| 1.535 | + | -1871.7957682652 | yes | + |
| 1.540 | + | -1870.8148780892 | yes | + |

Reading (orientation as printed, not compared across D):
- robust change (1.510, 1.515), + to -: det-linear 1.511102, estimator range [1.510769, 1.511102];
- robust change (1.530, 1.535), - to +: det-linear 1.531607, estimator range [1.531607, 1.531755];
- changes touching a non-robust point: none; ln|det| minima without a sign change: none; endpoint signs + at 1.480 and + at 1.540; all 13 points noise-robust;
- the repeat of 1.510 (process 1, original on process 0) is bit-identical in sign, noise signs, float64 sign and ln|det| (`repeat_check.py`: PASS);
- the float64 sign is + at every one of the 13 points, so it shows no sign change; the hybrid shows two. Reported as a difference between the float64 slogdet and the hybrid at 1.515 to 1.530 (the same float64 difference as in the control).

The two roots are 0.020505 apart (det-linear estimates), against 0.0548 at D 19 (the coordinator's 1.4832 and 1.5380 from dh370): the lower one moved up by 0.0279, the upper one down by 0.0064 in 0.09375 of D. A straight line through these two D values (a two-point extrapolation, not a measurement; the tracks' curvature is unknown) closes the gap about 0.056 above D 19.09375, at D 19.150 and lambda 1.5278.

Acceptance: the control matches; the system check passes on all six processes; the reader's selftest passes and its mutations fail (`selftest_exits.txt` 0 1 1 0 0 1); the repeat agrees. All met.
