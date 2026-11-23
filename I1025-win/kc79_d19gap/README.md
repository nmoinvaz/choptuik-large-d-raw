# I1025-win/kc79_d19gap: the k_c 79 gap (1.32, 1.475) at D 19 (winb)

Written before the run, 2026-11-23 02:57:47 UTC (substituted from `date -u` when pushed). Nothing has been run for this folder yet.

Runner: the winb session (surface-laptop-4, 4 cores, 8 threads, 32 GB), the same one that ran `../kc79_d19/` (D 19 regrid and the first scan), `../kc79_d19low/` (the lower-root scan, raw commit 40f1a01a) and the earlier k_c 79 folders. The coordinator is t5.

## Order (t5's hc of 2026-11-23, after the lower-root reading; the comment on #1025 posted 03:05 UTC, winb section)

1. The gap (1.32, 1.475) on the same state, pins and `d18_hybsign.py` as `../kc79_d19low/`, at lambda 1.345, 1.37, 1.395, 1.42, 1.445 plus a repeat of 1.395 (6 points).
2. One process, below-normal priority, started through the headless conhost, and the keep-awake helper for the run's duration. Memory alerts only (no guard that kills).
3. Then `read_lower.py` as before.
4. **Written before the run (t5):** the rising discretization root, below lambda_1 (1.5397 at D 19, k_c 79), lies in this gap.
5. Report every robust change by position, beside k_c 71's roots at D 19. Post on #1025 and send t5 the verdict.

## What is known before the run (two scans on this state)

| scan | window | signs | where |
|---|---|---|---|
| first D 19 scan | 1.475, 1.48, 1.485, 1.49, 1.53, 1.535, 1.54, 1.545 | `+` at 1.475 to 1.535, `-` at 1.54 and 1.545; one robust change + to - at lambda_1 = 1.539658 | `../kc79_d19/`, raw deaded8d |
| lower-root scan | 0.92 to 1.32 at 0.04, repeat 1.12 | `-` at all 11 points, no change, no minimum without a change | `../kc79_d19low/`, raw 40f1a01a |

So the sign is `-` at 1.32 (hybrid ln|det| -2541.7118) and `+` at 1.475 (-2543.2199): an odd number of changes lies in (1.32, 1.475). The lower scan's ln|det| flattens at its upper edge (steps of 0.84 and 0.26 at 1.28 and 1.32, against 2.6 before). k_c 71's roots at D 19, for the comparison t5 asks for: 1.296338 (+ to -, dh610, raw 172112d0, `../../I1025-dh610/kc71_d19low/`) and 1.536547 (lambda_1, as I have it from t5's earlier ruling). k_c 63: 1.483 and 1.537988. Orientation labels are not compared across k_c; t5 rules by position.

A limit of the planned reading: `read_lower.py` sees only the points of this folder's scan file (1.345 to 1.445). A change in (1.32, 1.345) or in (1.445, 1.475) shows there only as an endpoint sign equal to the neighbor scan's (`+` at 1.345 or `-` at 1.445), not as a robust change. I therefore also read the three scan files together once (copies in `combined/`, the files unchanged, same reader), and report that separately and labelled as mine; the ordered reading is the one in this folder's `read_lower_kc79_D19gap.log`.

## The scan

| item | value |
|---|---|
| state | `../kc79_d19/sol_l1kc79W19m1025_D19.0000.npy` (the D 19 regrid's accepted k_c 79 state, the same file as the first scan and the lower-root scan) |
| record | `../kc79_d19/l1kc79W19m1025.jsonl` (|F| 2.848e-10, 2976 steps) |
| scanner | `d18_hybsign.py` (xfkappa, raw `I1025-mac/d18`, blob e089207a, unchanged): float64 blocks 0-11 plus a dd block 12, the 1e-15 noise test on blocks 0-11 with 2 seeds, the float64 sign beside it |
| window | 1.345, 1.37, 1.395, 1.42, 1.445, then the repeat 1.395 (6 points, in this order) |
| reader | `read_lower.py` (dh170, raw `I1025-dh170/lower_root`, blob 89309d3c; imports `d185_scan_read.py`, blob 7c9d400f), `read_lower.py . 1.345 1.445` |
| process | one, 4 BLAS threads, BelowNormal, started through `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c`, cap 28800 s by the exact pid |

The pins are in `prep_kc79d19gap_pins_1025.txt` (the same as for the lower-root scan, re-hashed here). `read_lower.py` globs `scan_*_p*.jsonl` in the folder, so the scanner writes straight to `scan_kc79_D19gap_p0.jsonl`. The reader prints the points, the not noise-robust ones, the hybrid signs, the float64 differences, the repeated points (a repeat must agree), every robust change (bracket, orientation, det-linear estimate, estimator range), changes touching a non-robust point (not counted), the ln|det| minima without a sign change and the endpoint signs. The driver sends t5 every line it printed, as printed.

## Checks and refusals (fixed before the run, unchanged from the lower-root scan)

The driver (`kc79d19gap_scan_driver_1025.py`) starts the scan only if the pins match (scanner, reader, its import, the D 19 state, record and `regrid_accepted.txt`; the worktree `choptuik-i1025k79` at 48c36355), `../kc79_d19/regrid_accepted.txt` exists, `scan_kc79_D19gap_p0.jsonl` does not, the window has at least two distinct values in (0, 10) none more than twice, and `read_lower.py selftest` exits 0 with its two controls (`--mutate=shift`, `--mutate=round2`) exiting 1 each. Otherwise it stops with an hc to t5 (exit 2, no retry). During the run `d18_hybsign.py` checks that the state comes back as its record system (exit 3 otherwise: no reading, an hc to t5). A scan that does not finish (non-zero exit, the cap) is reported with the points so far and not read.

Dry tests (`selftest_scan_dry_1025.txt`): the planned window runs the checks and starts nothing (exit 0); seven bad windows (one value, a value twice with no second value, a value three times, a non-number, 0, 10 and 11) are refused with exit 2.

## Cost, written before the run

| item | value |
|---|---|
| t5's estimate | about 2.7 h at 1600 s a point |
| this laptop, same state and code | lower-root scan: 1596 to 1695 s per point for the first nine points, then 1455, 1357, 1349 s (cause of the change not known); first D 19 scan: 1320 to 1344 s per point |
| mine | 6 points at 1350 to 1700 s: 2.25 to 2.85 h, peak private about 2.5 GB, 4 threads |

The sampler (`rows/scan_samples.csv`, a line every 60 s) gives the real figures. The two I129 jobs of the other project share the laptop. At the start I record the clock speed and the power state in the Status section (the lower-root scan's slow stretch had no clock log).

## The drivers (derived from the lower-root ones; the diffs are in `diff_*_vs_d19low.txt`)

`make_d19gap_1025.py` writes `kc79d19gap_scan_driver_1025.py`, `kc79d19gap_watch_alert_1025.py`, `start_kc79d19gap_scan_1025.cmd`, `go_kc79d19gap_scan_1025.cmd`, `keepawake_1025.py`, `session_check_1025.ps1` and `publish_kc79d19gap_1025.sh` from the `kc79d19low` ones (raw `../kc79_d19low/`) by asserted replacements. Only names, the order text and the window changed. The sampler is an unchanged copy. The keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` from its main thread until the driver pid is gone, power plan untouched, kills nothing) and the session check (the parent chain of every process of the run; fails if `claude` is in a chain) are as in the lower-root scan.

## Run

Started outside my terminal: `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc79d19gap_scan_1025.cmd` (the quoted window is inside the `.cmd`: quotes do not survive the headless conhost command line), BelowNormal, one python process tree, 4 threads. The driver starts its sampler, its alert-only watcher (free physical memory every 15 s, one hc alert to t5 below 1 GB, at most every 30 min, kills nothing) and the keep-awake helper.

## Status

Written before the run. Pushed 2026-11-23 02:57:47 UTC.

## Result

Not yet run.
