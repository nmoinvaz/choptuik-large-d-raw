# I1025-dh610/kc79_d19low: hybrid sign scan at D 19.0, k_c 79, lambda_1 0.92 to 1.32 at 0.04: where is k_c 79's lower root at D 19?

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task from the coordinator (hc, 22 Nov 2026), after `../kc71_d19low/` (this machine) found k_c 71's lower root at D 19 between 1.28 and 1.30, and winb's k_c 79 scan at D 19 (`I1025-win/kc79_d19/`, raw deaded8d, read again at 010273bc) found one change, + to - at 1.539658, and none in 1.475 to 1.49. Called "the lower root" here, its physical status open.

Information, not a pass rule (the lower root's position at D 19 by k_c):

| k_c | lower root at D 19 | source |
|---|---|---|
| 63 | 1.4832 | the coordinator's number from the k_c 63 scan at D 19 |
| 71 | in (1.28, 1.30): det-linear 1.296338, estimator range [1.285131, 1.296338] | `../kc71_d19low/` (this machine, 22 Nov), a spread over interpolation choices, not an enclosure |
| 79 | this scan | here |

From k_c 63 to 71 it moved by about -0.19. If it keeps falling with k_c, it is a discretization root and its meeting with lambda_1 moves out (the coordinator's reading). The window 0.92 to 1.32 is the coordinator's.

## Setup

Budget: 1 process for the control, then 6 processes of 1 thread (OMP, OPENBLAS, MKL, VECLIB, RAYON = 1), nice 10, one systemd user unit `i1025j` (`lane_kc79low.sh`, started by `start_kc79low.sh`, log `exits_kc79.txt`), beside #1067's series (unit `i1067d`, 10 threads), not touched. Worktree `~/Source/choptuik-large-d-1025f` at 505d8399 (clean; winb's regrid used a worktree whose solver files equal its), `~/Source/venv-i1058/bin/python`, `P4_WT_MATTER=<worktree>/solver/matter`, `d18_hybsign.py` unmodified (winb's scan used the same blob e089207a).

Inputs (winb's, raw `I1025-win/kc79_d19/` at f712f94c or later, the state and record equal at f712f94c and 010273bc; pinned by `git hash-object --no-filters`, `in_blobs.txt`; the lane script refuses to start on any other blob): `sol_l1kc79W19m1025_D19.0000.npy` 3a3b1999 (the regridded k_c 79 state at D 19), `l1kc79W19m1025.jsonl` 3603895c (its record: |F| 2.848200733307459e-10, 2976 steps, constraint 7.28e-4, Delta 1.0677704363070795), winb's scan rows `scan_kc79_D19_1025.jsonl` 321fb621 (copied as `in/ref_winb_scan_kc79_D19_1025.jsonl`; its lambda 1.54 row: hybrid sign -1, ln|det| -2547.786620251229, both noise seeds -1, float64 +1 with ln -2544.7945, 1343 s on Windows). The scanner `d18_hybsign.py` e089207a, the reader `read_lower.py` 89309d3c with `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9 are the same blobs as in `../kc71_d19low/in/`.

## Commands

1. Control, 1 process, cap 3 h by exact pid: `d18_hybsign.py in/l1kc79W19m1025.jsonl in/sol_l1kc79W19m1025_D19.0000.npy 19.0 1.54 control/scan_D19.0_p0.jsonl`. Pass (`control_check.py`, `../kc71_d19125`'s with winb's reference row and label): the log prints `the record system`; the hybrid sign equals winb's; ln|det| equals winb's -2547.786620251229 to 1e-6 relative (winb is a Windows build). Otherwise stop and report, no scan.
2. Scan (only after the control passes and MemAvailable is at least 6 x the control's max RSS + 4 GB), 6 processes of 1 thread, cap 8 h each by exact pid: `d18_hybsign.py in/l1kc79W19m1025.jsonl in/sol_l1kc79W19m1025_D19.0000.npy 19.0 <lambdas> scan/scan_D19.0_p<p>.jsonl`; lambda 0.92 to 1.32 at 0.04 (11 values) plus a repeat of 1.12 (12 evaluations); value i goes to process i mod 6 (`scan_hyb.sh`'s splitting). The repeat is put at index 6 of the list (after the original, index 5), so that it runs on process 0 and the original on process 5; appended at the end it would run on process 5 beside the original. The system check is `d18_hybsign.py`'s first line per process (exit 3 stops it).
3. Reading: `read_lower.py scan 0.92 1.32` (dh170's, unedited; keys `round(lambda, 4)`, spacing-agnostic) and `repeat_check.py` on the merged scan file.

## Acceptance and reading (the coordinator's)

- the control matches; the system check passes on all six processes; the reader's selftest passes and its mutations `shift` and `round2` each exit 1 (`selftest_exits.txt`: read_lower 0, shift 1, round2 1, repeat_check 0, control_check 0, its mutate 1); the repeat of 1.12 agrees (ln|det| within 1e-6, bit-identical expected);
- read: every robust change with its det-linear estimate and estimator range (a spread over interpolation choices, not an enclosure), orientation as printed (not compared across D); any ln|det| minimum without a change; the repeat; changes touching a non-robust point listed and not counted. If no change shows, report the edge signs and any minimum without a change, and do not widen the window without the coordinator's word.

Estimate (coordinator's): about 45 min; winb's points took 1325 to 1344 s on a 4-core Windows laptop.

Written as the run goes.

## Control (22 Nov, 16:18:46 to 16:38:09 UTC): FAIL on the ln|det| bar; no scan

`d18_hybsign.py` at D 19.0, k_c 79, lambda 1.54 on winb's state and record, 1 process of 1 thread: wall 1163 s (the point's own 1156 s; winb's was 1343 s on Windows), peak RSS 1.84 GB, exit 0 (`control/control.log`, `control/control_check.txt`, `exits_kc79.txt`). The lane script stopped at the check, as written, and no scan started (the scan unit and the waiters ended with it; nothing was loosened).
- the record system: |F| 2.8477474518e-10 against the record's 2.8482007333e-10 (relative 1.6e-4, inside the check's 1e-2 bar), steps 2976 = 2976;
- hybrid sign -1 = winb's -1; both noise seeds -1 (noise_robust True);
- **ln|det| -2547.7914967589 against winb's -2547.786620251229: difference -4.877e-3, relative 1.914e-06 against the bar 1e-06: FAIL**;
- float64: sign -1 here against +1 in winb's row, ln -2544.9175487167 against -2544.7945061325 (difference -0.123, relative 4.8e-05); the float64 sign is not a determinant sign in these scans;
- for comparison, the k_c 71 control of `../kc71_d19125/` (win2's Windows build) differed by 1.4e-4 absolute, 6.158e-08 relative, and its float64 ln by 4.5.
Cause not diagnosed. Not run: a repeat of the control on this machine, or at another thread count, which would show how far this machine's own ln|det| moves from one run to another (the hybrid's blocks 0 to 11 come from `S.mode_matrix` in float64, whose last digits depend on the build, and the noise test perturbs them by 1e-15); a hypothesis, not tested.

## The control's own spread (the coordinator's order after the FAIL, 22 Nov; started 16:41:13 UTC, unit `i1025l`)

Order (t5): "(b), and no bar change until the cause is known": rerun the same control point (D 19.0, k_c 79, lambda 1.54, winb's state and record) at OMP/OPENBLAS/MKL = 2 and = 4, one process each, beside the k_c 71 D 19.25 scan (`../kc71_d1925/`, 6 processes, kept running); report the three ln|det| values (1, 2, 4 threads) with their relative spread, the |F| each prints, and winb's value beside them. The 1-thread value is the FAIL above (`control/`).

Reading, fixed before the runs (the coordinator's): own spread at least half the cross-machine 1.914e-6 (9.57e-7) means build rounding at k_c 79's size, and the k_c 79 bar is set from the measured spread; own spread below 1e-7 means the cross-machine difference is real, and k_c 79 scans stay on winb's machine; in between, neither rule applies (reported, not decided). `spread_read.py` computes the spread as (max - min) divided by the mean |ln|det|| of the three, and the cross-machine difference as the 1-thread value against winb's; its selftest has four planted triples (spreads 0, 3e-7, 1e-6, unequal signs) and a not-the-record-system log, and `--mutate` (lower bar 1e-5) must make it fail (`selftest_spread_exits.txt`: 0 1). It refuses to read when a log is not the record system or the hybrid signs differ among the runs.

Commands: `lane_kc79_spread.sh` (started by `start_kc79_spread.sh`, log `exits_kc79_spread.txt`): the pins as above, the worktree clean at 505d8399, then the two runs one after the other (so that the threads in use stay at 20 or fewer: 6 of the D 19.25 scan + 4 + #1067's 10), each `OMP_NUM_THREADS = OPENBLAS_NUM_THREADS = MKL_NUM_THREADS = N`, VECLIB and RAYON left at 1 as in the 1-thread control, nice 10, cap 3 h by exact pid, `d18_hybsign.py in/l1kc79W19m1025.jsonl in/sol_l1kc79W19m1025_D19.0000.npy 19.0 1.54 control_tN/scan_D19.0_p0.jsonl`; a sampler logs the process's thread count (nlwp) every 30 s to `control_tN/sampler.log` to show that the BLAS threads were present. Then `spread_read.py` writes `spread_read.txt`.

## The control's own spread: result (22 Nov, 16:41:13 to 17:42:37 UTC): own spread 2.9e-15, below 1e-7

Both reruns exited 0 on the record system (`control_t2/`, `control_t4/`; `exits_kc79_spread.txt`, `spread_read.txt`). The samplers show the BLAS threads were present: max nlwp 3 at N = 2 and 7 at N = 4 (`sampler.log`; pcpu 178 and 348). The reruns ran beside the k_c 71 D 19.25 scan (6 processes) and the #1067 series (10 threads), so their walls are longer than the 1-thread control's.

| threads | hybrid sign | ln\|det\| | vs winb's -2547.786620251229 (relative) | \|F\| printed (record 2.8482007333e-10) | float64 sign, ln | point sec |
|---|---|---|---|---|---|---|
| 1 | -1 (noise_robust) | -2547.7914967589 | -1.9140e-06 | 2.8477474518e-10 | -1, -2544.9175 | 1156 |
| 2 | -1 (noise_robust) | -2547.7914967590 | -1.9140e-06 | 2.8491364722e-10 | -1, -2543.3869 | 1910 |
| 4 | -1 (noise_robust) | -2547.7914967589 | -1.9140e-06 | 2.8479332052e-10 | +1, -2545.4448 | 1766 |
| winb (Windows) | -1 | -2547.786620251229 | | | +1, -2544.7945 | 1343 |

- Own spread of ln|det| over 1, 2, 4 threads: (max - min) / mean |ln| = 2.856e-15 (7.3e-12 absolute). The cross-machine difference is -4.8765077e-3 absolute (1.914e-6 relative) at each thread count, the same to 1e-12.
- Fixed reading (the coordinator's): spread below 1e-7 means the cross-machine difference is real, and k_c 79 scans stay on winb's machine. The bar was not changed.
- Information: the printed |F| moves by 4.9e-4 relative with thread count (all three inside the check's 1e-2 of the record); the float64 ln moves by 2.06 (8.1e-4 relative) and its sign flips at 4 threads; winb's float64 ln lies inside that range. The hybrid ln|det| is stable to 3e-15 through all of it.
- What this test varies and what it does not: the thread count changes the BLAS reduction order only. It does not change the compiled kernel or libm that assemble `S.mode_matrix`, so the hypothesis written above (blocks 0 to 11 depend on the build's last digits) is neither shown nor excluded. Measured at one lambda (1.54) only: whether the offset is smooth in lambda is not tested.
