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

## Scan (22 Nov, 15:00:58 to 16:17:27 UTC): 21 points and the repeat, one robust change

Six processes, all exit 0 (`exits_kc71low.txt`), each logged the record system first (|F| 2.7637774095e-10 against the record's 2.7619908383e-10, steps 2676 = 2676). Points took 939 to 1289 s (the control of `../kc71_d19125/` alone: 778 s). Files: `scan/scan_D19.0_p<p>.jsonl`, merged `scan/scan_D19.0_1025.jsonl`, `read_lower.txt`, logs `scan/scan_p<p>.log`.

| lambda_1 | hybrid sign | hybrid ln\|det\| | float64 sign | float64 ln\|det\| | s |
|---|---|---|---|---|---|
| 1.0 | + | -2186.7648661808 | + | -2186.6841 | 1204 |
| 1.02 | + | -2188.0496617573 | + | -2188.0142 | 1180 |
| 1.04 | + | -2189.3319828598 | + | -2189.4156 | 1189 |
| 1.06 | + | -2190.6128380338 | + | -2190.5168 | 1182 |
| 1.08 | + | -2191.8934784858 | + | -2192.0683 | 1183 |
| 1.1 | + | -2193.1755059682 | + | -2193.1741 | 1179 |
| 1.12 | + | -2194.4610304093 | + | -2194.4731 | 1247 |
| 1.14 | + | -2195.7529952200 | + | -2195.5617 | 1275 |
| 1.16 | + | -2197.0557015139 | + | -2197.0406 | 1235 |
| 1.18 | + | -2198.3758539482 | + | -2198.4297 | 1239 |
| 1.2 | + | -2199.7246163686 | + | -2199.8598 | 943 |
| 1.2 | + | -2199.7246163686 | + | -2199.8598 | 1289 |
| 1.22 | + | -2201.1219673874 | + | -2201.4398 | 1188 |
| 1.24 | + | -2202.6076768105 | + | -2202.6709 | 1194 |
| 1.26 | + | -2204.2776729186 | + | -2203.8031 | 1189 |
| 1.28 | + | -2206.5201023492 | + | -2205.2253 | 1193 |
| 1.3 | - | -2208.0155456237 | + | -2208.6466 | 1192 |
| 1.32 | - | -2208.1870658478 | - | -2208.8987 | 1185 |
| 1.34 | - | -2208.8251782442 | - | -2210.3403 | 1245 |
| 1.36 | - | -2208.8126883466 | - | -2208.9430 | 939 |
| 1.38 | - | -2208.4009090881 | - | -2208.1456 | 943 |
| 1.4 | - | -2208.0745088743 | - | -2208.0621 | 939 |

The second 1.2 row is the repeat (process 3); its hybrid sign and ln|det| equal the first (process 4) bit for bit.

Reading (`read_lower.py scan 1.00 1.40`, dh170's, unedited; `read_lower.txt`):
- 21 distinct points, all noise-robust (both noise seeds agree with the hybrid sign); no non-robust point;
- hybrid signs, as printed: + from 1.00 to 1.28, - from 1.30 to 1.40; endpoints + at 1.00 and - at 1.40;
- robust change: between 1.280 and 1.300, + to -, det-linear 1.296338, estimator range [1.285131, 1.296338] (a spread over interpolation choices, not an enclosure; the bracket is the 0.02 grid step); this is the lower root of k_c 71 at D 19, physical status open;
- ln|det| local minimum without a sign change: lambda 1.34, depth 0.0125 (ln|det| -2208.8252 against the lower neighbour's -2208.8127 at 1.36; the reader's depth is the smaller neighbour minus the point); no other;
- the repeat of 1.20: `repeat_check.py` PASS, 2 evaluations agree;
- the float64 sign differs from the hybrid at 1.30 only (hybrid -, float64 +), as in the earlier scans: the hybrid is read;
- orientation is as printed and not compared across D. Information only: k_c 71 at D 19.125 has changes 1.488137 (+ to -) and 1.511209 (- to +) (`../kc71_d19125/`), and win2's D 19 scan has the change 1.536547 (- to +); the k_c 63 lower root at D 19 is 1.4832 (the coordinator's number), so from k_c 63 to 71 the lower root moved by about -0.19 (1.4832 to 1.296338, -0.187).

Acceptance: no control rerun (the order); the control of `../kc71_d19125/` passed and the lane script refused to start without its PASS; system check on all six processes; reader selftest 0 and mutations `shift` 1, `round2` 1 (`selftest_exits.txt`: 0 1 1 0 as wanted); the repeat agrees.
