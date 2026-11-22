# I1025-dh610/kc71_d1925: hybrid sign scan at D 19.25, k_c 71, lambda_1 1.42 to 1.58 at 0.01: where are k_c 71's two changes at D 19.25?

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task from the coordinator (hc, 22 Nov 2026), after `../kc71_d19125/` (raw ee09203f) and `../kc71_d19low/` (raw 172112d0). dh170 ran this window on its lane 2 and stopped it after four points to hand it to this machine (`I1025-dh170/kc71_meet/lane2_stopped/`, raw 7143608c): those four points are the cross-machine check here.

## k_c 71's changes so far (information, not a pass rule; orientation as printed, not compared across D)

| D | change | lambda_1 (det-linear) | source |
|---|---|---|---|
| 19.0 | + to - | 1.296338 (bracket 1.28 to 1.30, range [1.285131, 1.296338]) | `../kc71_d19low/` (this machine), the lower root |
| 19.0 | - to + | 1.536547 | win2, raw 2c37fd37 |
| 19.125 | + to - | 1.488137 (bracket 1.48 to 1.49, range [1.486996, 1.488137]) | `../kc71_d19125/` |
| 19.125 | - to + | 1.511209 (bracket 1.51 to 1.52, range [1.511209, 1.511571]) | `../kc71_d19125/` |
| 19.25 | | this scan | here |

Straight lines through the two D values (two points make a line, not a law; the changes are not known to be the same roots from D 19 to D 19.125): the + to - change rises at 1.5344 per unit D (1.296338 to 1.488137) and would be near 1.680 at D 19.25, above the window; the - to + change falls at -0.2027 per unit D (1.536547 to 1.511209) and would be near 1.486 at D 19.25. The two lines cross near D 19.138, before D 19.25. dh170's lane-2 points: hybrid sign + at 1.42, 1.43, 1.44, 1.45 (ln|det| -2186.7629, -2187.2342, -2187.7516, -2188.3516).

## Setup

Budget: 6 processes of 1 thread (OMP, OPENBLAS, MKL, VECLIB, RAYON = 1), nice 10, one systemd user unit `i1025k` (`lane_kc71_1925.sh`, started by `start_kc71_1925.sh`, log `exits_kc71_1925.txt`). It starts after the k_c 79 scan of `../kc79_d19low/` (unit `i1025j`) ends, beside #1067's series (unit `i1067d`, 10 threads), not touched. Worktree `~/Source/choptuik-large-d-1025f` at 505d8399 (clean), `~/Source/venv-i1058/bin/python`, `P4_WT_MATTER=<worktree>/solver/matter`, `d18_hybsign.py` unmodified.

No control run here (the order): the control passed in `../kc71_d19125/control/` (22 Nov, same machine, build, script and record family: D 19.0, lambda 1.55, record system, win2's hybrid sign, ln|det| within 6.158e-08 relative of win2's). The lane script refuses to start unless that control's check file says PASS.

Inputs (win2's, raw `I1025-win2/kc71_leap/states/` at 8e4797ff, taken with `git show`; pinned by `git hash-object --no-filters`, `in_blobs.txt`; the lane script refuses to start on any other blob): `sol_l1kc71Lw1025_D19.250000.npy` 36bc6b83, `l1kc71Lw1025.jsonl` c5fc14a9 (12 rows, D 18.5625 to 19.25; the D 19.25 row: |F| 3.002396449323892e-10, 2630 steps, constraint 1.990e-3, Delta 1.0737683214116145; the file at the raw head has moved on to a0e21703, the pin is the 8e4797ff one). dh170's four points `ref_dh170_lane2_scan_D19.25_p0.jsonl` 607c4427 (raw 7143608c; 4 threads each, 911 to 956 s a point). The scanner `d18_hybsign.py` e089207a, the reader `read_lower.py` 89309d3c with `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9 are the same blobs as in `../kc71_d19125/in/`.

## Commands

1. Pre-run checks (lane script): the pins; worktree clean at 505d8399; the reader's selftest exits 0 and its mutations `shift` and `round2` each exit 1; `repeat_check.py selftest` 0; `compare_dh170.py selftest` 0 and its `--mutate` 1 (`selftest_exits.txt`: 0 1 1 0 0 1); MemAvailable at least 6 x the control's max RSS (1556924 kB) + 4 GB.
2. Scan, 6 processes of 1 thread, cap 8 h each by exact pid: `d18_hybsign.py in/l1kc71Lw1025.jsonl in/sol_l1kc71Lw1025_D19.250000.npy 19.25 <lambdas> scan/scan_D19.25_p<p>.jsonl`; lambda 1.42 to 1.58 at 0.01 (17 values) plus a repeat of 1.50 at the end (18 evaluations); value i goes to process i mod 6, so three rounds, and the repeat (index 17) runs on process 5 and its original (index 8) on process 2. The system check is `d18_hybsign.py`'s first line per process (exit 3 stops it).
3. Reading: `read_lower.py scan 1.42 1.58` (dh170's, unedited; keys `round(lambda, 4)`) and `repeat_check.py` on the merged scan file; then `compare_dh170.py` of the merged scan against dh170's four points (1.42 to 1.45): per shared lambda the hybrid sign, both noise flags, the float64 sign and the relative difference of ln|det| (bar 1e-9, information; dh170 ran 4 threads per point, this scan 1, so the last digits may differ).

## Acceptance and reading (the coordinator's)

- the system check passes on all six processes; the reader's selftest passes and its mutations each exit 1; the repeat of 1.50 agrees (ln|det| within 1e-6, bit-identical expected);
- read: every robust change with its det-linear estimate and estimator range (a spread over interpolation choices, not an enclosure), orientation as printed, beside the D 19.125 changes 1.488137 and 1.511209; any ln|det| minimum without a change (a merged pair would show as one); the repeat; changes touching a non-robust point listed and not counted; the cross-machine comparison as information. Roots are k_c 71 roots, not yet physical ones.

Estimate (coordinator's): about 45 min; three rounds of about 800 to 1300 s.

Written as the run goes.
