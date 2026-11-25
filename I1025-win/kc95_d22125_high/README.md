# I1025-win/kc95_d22125_high: a k_c 95 HIGH hybrid sign scan of dh610's accepted D 22.125 state, lambda 0.52 to 0.76 (winb)

Written before the run, 2026-11-25 09:55:27 UTC (the time of the README-first push; later pushes keep it). Neither the source driver nor the scan had been run for this folder when the order, the prediction and the estimates below were written. Run beforehand, read-only: the source checks by hand (under 2 min), the dry runs of both drivers. Runner: the winb session (surface-laptop-4, Windows 11, 4 cores, 32 GB); coordinator t5.

## Order (t5's hc of 2026-11-25, read at about 09:38 UTC, winb section, quoted)

"Coordinator (t5), #1025, next after your k_c 103 D 21.75 reading (do not stop it): a k_c 95 HIGH scan of dh610's accepted D 22.125 state (raw I1025-dh610/kc95_d22125; pin by blob; kc95 check accepts, controls 1 1, kc87 and kc103 refuse), lambda 0.52 to 0.76 by 0.04 plus the repeat of 0.64, 4 procs. Reason: at k_c 87 a second mode S has a root at 0.6199 at D 22.125 ('+ to -' by rank, above lambda_1 = 0.491); if k_c 95 has no root there, S is a k_c 87 artefact. Register first: S at k_c 95 within 0.05 of 0.62 (one change, '+ to -'), or none. Raw I1025-win/kc95_d22125_high/, README first."

My reading:
- **The k_c 103 D 21.75 scan is not stopped.** It is in its last round (p0 and p2 each on their second point); this scan starts only after that chain has ended and its reader lines are with t5 ("next after your reading"). The laptop has 4 cores and 32 GB; two 4-process scans together would overload it. Everything here that is not the scan (pins, checks by hand, drivers, dry runs, this README) was done beside it with at most 2 threads.
- "dh610's accepted D 22.125 state" is his regridded k_c 95 state (macm3's k_c 87 b2 state at D 22.125 regridded to k_c 95; regrid ACCEPTED 2026-11-25 04:34:32 UTC, commit ce4fce87f). **It is scanned as it is; there is no regrid here.**
- "HIGH": above lambda_1, whose k_c 95 root at this D is 0.491072 (dh610's scan, window 0.475 to 0.505). The scan is 4 processes of `d18_hybsign.py`, 1 thread each, BelowNormal, 2 evaluations each, cap 21600 s by the exact pids.
- Stops as before: an exception, a scan step over 6 h. **No robust change in the window is registered outcome (B) below: I report it and do not widen the window.** Also as before: the peak private memory of a scan point is reported; nothing kills on memory.

## Written before the scan (t5's registration)

**PREDICTION: "S at k_c 95 within 0.05 of 0.62 (one change, '+ to -'), or none."** Read as two registered outcomes, by position and orientation, both as `read_lower.py` prints them:

| outcome | what the reader prints |
|---|---|
| (A) S exists at k_c 95 near its k_c 87 place | exactly one robust change in 0.52 to 0.76, orientation `+ to -`, det-linear estimate in [0.570, 0.670] (0.62 +- 0.05) |
| (B) no S at k_c 95 | "robust changes: 0" in 0.52 to 0.76 (every sign the same) |

Anything else is reported as printed and is neither (A) nor (B): a robust change outside [0.570, 0.670], a `- to +` change, two or more changes, a change touching a non-robust point (counted separately by the reader). I do not interpret; t5 rules (by position, orientation as printed). If outcome (B), t5's reason says S would be a k_c 87 artefact; that reading is t5's.

The grid is t5's: lambda 0.52, 0.56, 0.60, 0.64, 0.68, 0.72, 0.76 (7 points) plus a repeat of 0.64 (8 evaluations). The window ends 0.52 and 0.76 are the only evaluated edges.

For reference (not predictions of mine):

| reading | by position | det-linear | range | orientation as printed | where |
|---|---|---|---|---|---|
| k_c 87, D 22.125, macm3 (macOS), the HIGH scan, lambda 0.50 to 0.70 by 0.02 plus a repeat of 0.60 | (0.600, 0.620) | 0.619895 | [0.606686, 0.619895] | + to - | `I1025-macm3/kc87_leg_lambda/22.125_high/read_lower.txt` (hybrid signs + at 0.50 to 0.60, - at 0.62 to 0.70; the float64 sign differs from the hybrid at 0.50 and 0.60; the repeat of 0.60 bit-identical; 12 of 12 noise-robust) |
| k_c 87, D 22.125, macm3, lambda_1 (F) | 0.4908 | | | - to + | `I1025-macm3/kc87_leg_lambda/README.md` (rescan 0.490845) |
| k_c 95, D 22.125, dh610 (Linux), lambda_1 (F), window 0.475 to 0.505 | (0.490, 0.495) | 0.491072 | [0.490684, 0.491072] | - to + | `I1025-dh610/kc95_d22125/README.md` |

dh610's k_c 95 scan of this state (window 0.475 to 0.505): hybrid signs 0.475- 0.480- 0.485- 0.490- 0.495+ 0.500+ 0.505+, the float64 sign agreeing everywhere, ln|det| 0.490 -2781.0889, 0.495 -2779.7909, 0.500 -2779.4464, 0.505 -2779.4475. Nothing of this state above 0.505 has been scanned. t5's reading of the k_c 87 data (README of `I1025-macm3/kc87_leg_lambda`, "two-branch picture"): F (flat, lambda_1) and S (steep, from above) cross near D 22.171; "printed orientation is rank". Those are t5's and macm3's readings, not mine.

## The source (dh610's)

| item | value |
|---|---|
| raw folder | `I1025-dh610/kc95_d22125` (state and record from his regrid commit ce4fce87f; origin/main 33f6e5929 at my fetch) |
| state | `in/sol_l1kc95dh610d22125_D22.1250.npy`, blob 06c5082f523c3eb9f1a2669415ac6981e2f82ae2 (49848 bytes), ACCEPTED by dh610 2026-11-25 04:34:32 UTC |
| record | `in/l1kc95dh610d22125.jsonl`, blob 64ecb0474d17c1bcd1e4cb0d7ec8f41eafc71580 (370 bytes, one row; the same blob as the folder's top-level `l1kc95dh610d22125.jsonl`): k_c 95, D 22.125, kappa 0.7, u0 0.04, Ks 30, \|F\| 4.062791113494692e-10, F_start 4.045238658261682e-05, steps 3132, constraint 4.293368242355247e-03, Delta 1.1491338668995048, 5219 s (src `l1kc87Lmacm3b2`) |
| the checks | `kc87_syscheck_1025.py` 6df5d960, `kc95_syscheck_1025.py` d487e628 (dh610's), `kc103_syscheck_1025.py` 3ab58d16 (dh170's: the k_c 95 check with only the k_c constant changed, 3 lines, `kc103_syscheck_1025_vs_kc95.diff`) |
| scanner, reader | `d18_hybsign.py` e089207a, `d185_scan_read.py` 7c9d400f, `read_lower.py` 89309d3c, the same blobs as my earlier runs |
| code | the worktree `choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's), the one of my k_c 95 and 103 runs; dh610's regrid used the same commit (`choptuik-large-d-1025g`) |
| lambda_0 | 2.1023628304 (`ell_delta.lam0_at(22.125, *ell_delta.lam0_table())[0]` in that worktree, equal to dh610's README; the driver checks it; not used by the scan) |

The copies are in `inputs/` (taken with `git show origin/main:<path>`, blobs checked); each is pinned in `prep_kc95d22125h_pins_1025.txt` and checked by the driver. Nothing of dh610's is modified.

The source checks, run by hand at 09:51 to 09:53 UTC before writing this (read-only, `REC STATE 22.125 WTM` with absolute paths, 2 threads; `prep_source_checks_by_hand.txt`): `kc95_syscheck_1025.py` exit 0 ("ACCEPTED: the record class's \|F\| with a step count that comes back"; record \|F\| 4.0627911135e-10, the state's \|F\| on this machine 4.0668576397e-10 (0.10 % apart, inside the 1 % bar), `freeze_from` 3132 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (3132 against 3133), `kc87_syscheck_1025.py` exit 1 ("the record is not k_c 87 at D 22.125 (kc 95, D 22.125)"), `kc103_syscheck_1025.py` exit 1 ("the record is not k_c 103 at D 22.125 (kc 95, D 22.125)"); the selftests of all three checks exit 0; lambda_0 reads 2.1023628304. The driver repeats all of them and stops if any differs.

## The run

1. **Step 1, source** (`kc95d22125h_source_driver_1025.py`, the regrid driver of my k_c 103 D 21.75 run without its regrid, `diff_source_driver_vs_regrid_driver.txt`): the pins; the selftests of the three checks (exit 0) and the lambda_0 check; the source through the five checks above; the marker `source_accepted.txt` (with the state and record blobs) written from the driver's python process, the state, record and reader copied beside it.
2. **Step 2, scan, only after the marker** (`kc95d22125h_scan_driver_1025.py`): `d18_hybsign.py` (the hybrid sign: float64 blocks 0 to 11 and a dd block 12, the 1e-15 noise test with 2 seeds, the float64 sign beside it) at D 22.125 in four processes, one share each, one thread each, BelowNormal, cap 21600 s by the exact pids; the reader first passes its selftest and its two `--mutate` controls (exit 0, 1, 1):

| process | file | lambdas, in this order |
|---|---|---|
| p0 | `scan_kc95_D22125_high_p0.jsonl` | 0.60, 0.52 |
| p1 | `scan_kc95_D22125_high_p1.jsonl` | 0.64, 0.56 |
| p2 | `scan_kc95_D22125_high_p2.jsonl` | 0.68, 0.72 |
| p3 | `scan_kc95_D22125_high_p3.jsonl` | 0.64 (the repeat, another process than p1's), 0.76 |

   8 evaluations: 7 distinct points 0.52 to 0.76 by 0.04 and the repeat of 0.64. Round 1 is the three points nearest the k_c 87 place of S (0.60, 0.64 twice, 0.68), round 2 the rest (0.52, 0.56, 0.72, 0.76); all four processes run in both rounds. Then `read_lower.py . 0.52 0.76` (`D18_DIR` the inputs; it reads every `scan_*_p*.jsonl` of the folder, three-decimal keys, prints a robust change between adjacent points whatever the spacing). Each driver hc's t5 its end and every line the reader printed.
3. Each driver starts its own sampler (every 60 s), alert-only memory watcher (free physical memory every 15 s, one hc alert to t5 below 1 GB, at most every 30 min; kills nothing) and keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` until that driver's pid is gone, power plan untouched). The other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.
4. `go_kc95d22125h_1025.cmd` runs step 1 and, only if `source_accepted.txt` exists, step 2, in one headless console, started as `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc95d22125h_1025.cmd` (outside my terminal; the session check `session_check_1025.ps1` must show no `claude` in the chain).

Dry tests (`selftest_scan_dry_1025.txt`, `kc95d22125h_source_w.log.dry`): the source driver's pins, three selftests and lambda_0 check pass (exit 0, nothing started); the scan driver runs its checks on a stand-in marker, state and record (dh610's k_c 95 D 22.125 files, same names and blobs, in a folder that is not published) and reaches "would start" for four processes (exit 0), refuses a missing marker, refuses a marker with a wrong blob, refuses seven bad share lists (exit 2) and refuses `--out` without `--dry`. The real marker and the copies in this folder exist only after step 1.

## Cost, written before the run

No regrid here, so the cost is the scan only. What I have:

| source of the estimate | number |
|---|---|
| my k_c 95 scan at D 21.0 (`I1025-win/kc95_d21`, 3219 steps) | round 1 (4 processes) 4041 to 4055 s per point, round 2 (3 processes) 3396 to 3398 s; peak private 3.33 GB for the three workers with two points, 2.31 GB for the one-point worker |
| my k_c 103 scans at D 21.0 (3489 steps), D 21.125 (3476), D 21.75 (3417, round 1) | 6619 to 6628 s, 6257 to 6275 s, 6391 to 6415 s per point with 4 processes: the point time moves little with D at a fixed k_c |
| dh610's k_c 95 scan of this state (Linux, 4 processes of 2 evaluations, beside other jobs) | 2645 to 3153 s per point, 5840 s for the scan; my machine was 1.65 times slower than his in the regrids at D 21.0 |
| this state | 3132 steps against 3219 (k_c 95, D 21.0): 0.973 times |

Here both rounds have four processes running (8 evaluations on 4 processes), unlike my D 21.0 run whose round 2 had three; four concurrent points are the slow case.

| item | estimate | basis |
|---|---|---|
| source checks (step 1) | about 60 to 120 s | the by-hand run, 2 threads, under 90 s |
| each scan point (both rounds, four processes) | about 3500 to 5200 s | 4041 to 4055 s at D 21.0 times about 0.97 (the lower end), dh610's 2645 to 3153 s times 1.65 (the upper end) |
| the scan | about 7000 to 10400 s (1.9 to 2.9 h), central about 8200 s | two rounds of the point time |
| peak private | about 3.0 to 3.5 GB per worker (every worker has two points); the four peaks sum to about 12 to 14 GB | 3.33 GB at D 21.0; free memory at the start about 23 GB when nothing else runs |

The sampler (`rows/source_samples.csv`, `rows/scan_samples.csv`) gives the real figures.

## Files made here

`make_kc95d22125h_1025.py` writes `kc95d22125h_source_driver_1025.py`, `kc95d22125h_scan_driver_1025.py`, `kc95d22125h_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `sample_driver4_1025.ps1`, `go_kc95d22125h_1025.cmd` and `publish_kc95d22125h_1025.sh` from the k_c 103 D 21.75 ones (staging `kc103d2175_1025`, raw `I1025-win/kc103_d2175`) by asserted text replacements. `diff_source_driver_vs_regrid_driver.txt` is the diff of the source driver against that regrid driver, `kc103_syscheck_1025_vs_kc95.diff` the diff of the two checks, `prep_kc95d22125h_pins_1025.txt` the pins, `prep_source_checks_by_hand.txt` the by-hand source checks.

## Status

**Prepared, not started** (README first). The scan starts after the k_c 103 D 21.75 chain has ended and its reading has been reported to t5.

Pushed 2026-11-25 09:55:27 UTC.

## Result

Not yet run.
