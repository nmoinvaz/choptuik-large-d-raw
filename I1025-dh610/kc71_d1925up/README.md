# I1025-dh610/kc71_d1925up: hybrid sign scan at D 19.25, k_c 71, lambda_1 1.59 to 1.80 at 0.01: where is the change above 1.58?

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task from the coordinator (hc, 22 Nov 2026), after `../kc71_d1925/` (raw a61fee03): "Widen it upward now, same state, setup and reader ... lambda 1.59 to 1.80 at 0.01 (22 values) plus a repeat of 1.65, 6 processes of 1 thread, nice 10, a systemd unit." Why (the coordinator's): the sign at 1.58 flipped from + (D 19.125) to - (D 19.25), so a root crossed 1.58 in between; the D 19.125 - to + change (1.511209) has to be somewhere, and ln|det| still falls toward 1.58.

## k_c 71's changes so far (information, not a pass rule; orientation as printed, not compared across D)

| D | change | lambda_1 (det-linear) | source |
|---|---|---|---|
| 19.0 | + to - | 1.296338 (bracket 1.28 to 1.30, range [1.285131, 1.296338]) | `../kc71_d19low/` |
| 19.0 | - to + | 1.536547 | win2, raw 2c37fd37 |
| 19.125 | + to - | 1.488137 (bracket 1.48 to 1.49, range [1.486996, 1.488137]) | `../kc71_d19125/` |
| 19.125 | - to + | 1.511209 (bracket 1.51 to 1.52, range [1.511209, 1.511571]) | `../kc71_d19125/` |
| 19.25 | + to - | 1.475019 (bracket 1.47 to 1.48, range [1.474292, 1.475019]) | `../kc71_d1925/` |
| 19.25 | - to + | none in 1.42 to 1.58 (signs - from 1.48 to 1.58; ln\|det\| falling toward 1.58 in steps -0.1073, -0.1251, -0.1429) | `../kc71_d1925/` |

## Setup

Budget: 6 processes of 1 thread (OMP, OPENBLAS, MKL, VECLIB, RAYON = 1), nice 10, one systemd user unit `i1025m` (`lane_kc71_1925up.sh`, started by `start_kc71_1925up.sh`, log `exits_kc71_1925up.txt`), beside the #1067 series (`i1067d`, 10 threads): 16 of the 20 threads.

No control run here (the order says same setup; the previous order for this state had none): the control passed in `../kc71_d19125/control/` (same machine, build, script and record family), and `../kc71_d1925/` printed "the record system" on all six processes. The lane refuses to start without that PASS.

Inputs (win2's, raw `I1025-win2/kc71_leap/states/` at 8e4797ff; the same files as `../kc71_d1925/in/`, copied here; pinned by `git hash-object --no-filters`, `in_blobs.txt`; the lane refuses on any other blob): `sol_l1kc71Lw1025_D19.250000.npy` 36bc6b83, `l1kc71Lw1025.jsonl` c5fc14a9, `d18_hybsign.py` e089207a (xfkappa's, unmodified), `read_lower.py` 89309d3c, `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9 (dh170's, unedited). Worktree `~/Source/choptuik-large-d-1025f` clean at 505d8399; interpreter `~/Source/venv-i1058/bin/python`.

## Commands

1. Pre-run checks (lane script): the pins; worktree clean at 505d8399; the reader's selftest exits 0 and its mutations `shift` and `round2` each exit 1; `repeat_check.py selftest` 0 (`selftest_exits.txt`, wanted 0 1 1 0); MemAvailable at least 6 x the control's max RSS + 4 GB.
2. Scan, 6 processes of 1 thread, cap 8 h each by exact pid: `d18_hybsign.py in/l1kc71Lw1025.jsonl in/sol_l1kc71Lw1025_D19.250000.npy 19.25 <lambdas> scan/scan_D19.25_p<p>.jsonl`; lambda 1.59 to 1.80 at 0.01 (22 values) plus a repeat of 1.65 (23 evaluations); value i goes to process i mod 6 (`scan_hyb.sh`'s splitting); the repeat (index 22) runs on process 4 and its original (index 6) on process 0. The system check is `d18_hybsign.py`'s first line per process (exit 3 stops it).
3. Reading: `read_lower.py scan 1.59 1.80` (dh170's, unedited; keys `round(lambda, 4)`) and `repeat_check.py` on the merged scan file (`read_lower.txt`).

## Acceptance and reading (the coordinator's)

- the system check passes on all six processes; the reader's selftest passes and its mutations each exit 1; the repeat of 1.65 agrees (ln|det| within 1e-6, bit-identical expected);
- read: every robust change with its det-linear estimate and estimator range (a spread over interpolation choices, not an enclosure), the edge signs, any ln|det| minimum without a change; changes touching a non-robust point listed and not counted; call them k_c 71 roots (not yet physical). The sign at 1.58 of `../kc71_d1925/` is -; the sign at 1.59 here is read beside it. The window is not widened further without the coordinator's word.

Estimate (coordinator's): about 1 h; the 18-point scan of `../kc71_d1925/` took 71 min with 3 rounds of 6 processes, and this one is 23 evaluations (4 rounds), so about 1.5 h.

Written as the run goes.
