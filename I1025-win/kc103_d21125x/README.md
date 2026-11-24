# I1025-win/kc103_d21125x: k_c 103 at D 21.125 on Windows, regridded from dh170's accepted k_c 95 state there (the cross-build repeat), then a hybrid sign scan at 0.875 to 0.895 (winb)

Written before the run, 2026-11-24 22:26:00 UTC (the time of the README-first push; later pushes keep it). Neither the regrid nor the scan had been run for this folder when the order, the predictions and the estimates below were written. Run beforehand, read-only: the dry run of the regrid driver (pins, three selftests, lambda_0), the source checks by hand (20 s), the scan driver's dry run on a stand-in marker, state and record. Runner: the winb session (surface-laptop-4, Windows 11, 4 cores, 32 GB); coordinator t5.

## Order (t5's hc of 2026-11-24, ~22:19 UTC, winb section, quoted)

"Coordinator (t5) to winb, #1025. Ruling: k_c 103 at D 21.0 = 0.913448, by position. Your step from k_c 95 is -0.00006, against +0.0033 for the same step at D 21.125 (dh170, Linux: 0.881040 -> 0.884383). Two neighbouring D should not converge that differently, so the next task is a cross-build repeat to separate the build and regrid path from D.
Next task: k_c 103 at D 21.125 on Windows, from dh170's accepted k_c 95 state there (raw I1025-dh170/kc95_d21125; pin state and record by blob, check with the kc95 check: accepts, controls 1 1, kc87 check refuses). Regrid to k_c 103 exactly as your kc103_d21 regrid; acceptance by kc103_syscheck (3ab58d16) with controls; then scan 0.875-0.895 by 0.005 with the repeat of 0.885, 4 processes. Raw I1025-win/kc103_d21125x/, README first.
PREDICTIONS, registered before the scan: if builds agree, 0.884383 +- 0.0005 (dh170's root, by position); if your D 21.0 pattern holds instead, near 0.881. Report the root and which one it meets. Stop rules as before."

My reading: "exactly as your kc103_d21 regrid" is the regrid in one process at 4 BLAS threads, BelowNormal, outside my terminal, the scan in four processes at one thread each, the cap of both steps 21600 s (6 h) by the exact pids. "Stop rules as before": a regrid not accepted, an exception, no robust change in the window (report, do not widen), a step over 6 h. Also as before: report the peak private memory of the regrid and of a scan point; nothing kills on memory. My k_c 103 D 21.0 folder `I1025-win/kc103_d21` is pushed: 3499f61a8 (README first 84814983f), #1025 comments 7141592285 and 7145851300.

## Written before the scan (t5's predictions)

Two predictions, both by position, on the det-linear estimate of the robust change `read_lower.py` prints:

| | prediction (t5's) | the interval I will test it against |
|---|---|---|
| A | builds agree: dh170's root, 0.884383 +- 0.0005 | det-linear estimate in [0.883883, 0.884883] |
| B | my D 21.0 pattern holds: near 0.881 | t5 gave no bar; I read "near 0.881" as 0.881 +- 0.0005, det-linear estimate in [0.880500, 0.881500] (the pattern: a k_c 95 to 103 step of -0.000062 on dh170's k_c 95 root 0.881040 gives 0.880978); this reading is mine, for the table only, t5 rules |

The two intervals do not overlap (the gap is 0.881500 to 0.883883), and both lie inside the bracket (0.880, 0.885) that dh170's k_c 95 and k_c 103 readings had, so the grid signs alone will not separate A from B: the det-linear estimate (a linear interpolation of the determinant between 0.880 and 0.885) does. If the reader prints more than one robust change, all are printed as they come and each is compared (A with the one nearest 0.884383, B with the one nearest 0.881). If the reader prints no robust change in the window the order says stop and report, not widen: I stop. If the regrid is not accepted there is no scan. I report the root and which prediction it meets (A, B, both, neither); the ruling is t5's, I print the reader's lines as they come and do not interpret.

The grid is t5's: 0.875 to 0.895 by 0.005 (5 points) plus a repeat of 0.885 (6 evaluations). The window ends (0.875, 0.895) are the only evaluated edges.

For reference (not predictions of mine):

| reading | by position | det-linear | range | orientation as printed | where |
|---|---|---|---|---|---|
| k_c 95, D 21.125, dh170 (Linux) | (0.880, 0.885) | 0.881040 | [0.880628, 0.881040] | + to - | `I1025-dh170/kc95_d21125/read_lower.txt` |
| k_c 103, D 21.125, dh170 (Linux), regridded from his k_c 95 state | (0.880, 0.885) | 0.884383 | [0.883700, 0.884383] | + to - | `I1025-dh170/kc103_d21125/read_lower.txt` |
| k_c 95, D 21.0, mine | (0.910, 0.915) | 0.913510 | [0.912716, 0.913510] | + to - | `I1025-win/kc95_d21/` |
| k_c 103, D 21.0, mine | (0.910, 0.915) | 0.913448 | [0.912544, 0.913448] | + to - | `I1025-win/kc103_d21/` |

dh170's k_c 103 scan at D 21.125: hybrid signs 0.875+ 0.880+ 0.885- 0.890- 0.895-, the float64 sign differing from the hybrid at 0.885 only, ln|det| 0.875 -3287.2635, 0.880 -3288.5882, 0.885 -3290.5492, 0.890 -3289.2423, 0.895 -3289.1552; the regrid took 7305 s on his machine (3476 steps, \|F\| 4.6264065251e-10, Delta 1.121570859155). After the scan I put my per-point ln|det| beside these.

## The source (dh170's)

| item | value |
|---|---|
| raw folder | `I1025-dh170/kc95_d21125` (origin/main 3499f61a8 at my fetch; the state and record were first pushed in 4798af546; dh170's README names 30befd983 as his k_c 103 inputs commit) |
| state | `sol_l1kc95dh170f_D21.1250.npy`, blob c9d3774447775d9457d26529d4d447c9e30afce4 (49848 bytes) |
| record | `l1kc95dh170f.jsonl`, blob 6df5a5ee09fbfb0dabdec50d6012017dcb727c6a (370 bytes, one row): k_c 95, D 21.125, kappa 0.7, u0 0.04, Ks 30, \|F\| 4.619942915854309e-10, F_start 1.6640686664917824e-05, steps 3206, constraint 1.85852280482262e-03, Delta 1.1215731965267701, 5520 s (src `l1kc87Ldh370`) |
| the checks | `kc87_syscheck_1025.py` 6df5d960 (the k_c 87 check, first pushed in `I1025-dh610/kc87_d195`; the same blob is in `I1025-dh170/kc95_d21125/in/`), `kc95_syscheck_1025.py` d487e628 (dh610's; the k_c 87 check with 3 changed lines), `kc103_syscheck_1025.py` 3ab58d16 (dh170's: the k_c 95 check with only the k_c constant changed, 3 lines, `kc103_syscheck_1025_vs_kc95.diff`); all three blobs equal those in dh170's raw folders |
| scanner, reader | `d18_hybsign.py` e089207a, `d185_scan_read.py` 7c9d400f, `read_lower.py` 89309d3c, the same blobs as my k_c 87, k_c 95 and k_c 103 runs |
| code | the worktree `choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_delta.py` and `ell_refine.py` at 48c36355, `ell_refine.py` blob 631e5801), the one of my k_c 103 D 21.0 regrid; dh170's own worktree was the same commit |
| lambda_0 | 2.1062343410 (`ell_delta.lam0_at(21.125, *ell_delta.lam0_table())[0]` in that worktree, equal to dh170's; unused with `--no-gamma`; the driver checks it) |

The copies are in `inputs/`; the source state and record are also in the worktree's `solver/matter/data/` (where `ell_refine.py` reads its source); each is pinned by blob in `prep_kc103d21125x_pins_1025.txt` and checked by the driver. Nothing of dh170's is modified.

The source checks, run by hand at 22:22 UTC before writing this (read-only, `REC STATE 21.125 WTM` with absolute paths; `prep_source_checks_by_hand.txt`): `kc95_syscheck_1025.py` exit 0 ("ACCEPTED: the record class's \|F\| with a step count that comes back"; record \|F\| 4.6199429159e-10, the state's \|F\| on this machine 4.6229497124e-10 (0.07 % apart, inside the 1 % bar), `freeze_from` 3206 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (3206 against 3207), `kc87_syscheck_1025.py` exit 1 ("the record is not k_c 87 at D 21.125 (kc 95, D 21.125)"), `kc103_syscheck_1025.py` exit 1 ("the record is not k_c 103 at D 21.125 (kc 95, D 21.125)"); the selftests of all three checks exit 0. The driver repeats all of them and stops if any differs.

## The run

1. **Step 1, regrid** (`kc103d21125x_regrid_driver_1025.py`, a copy of my k_c 103 D 21.0 one with the pins, tags, D, source, lambda_0 and the added k_c 87 check changed, `diff_regrid_driver_vs_kc103d21.txt`): the pins; the selftests of the three checks (exit 0) and the lambda_0 check; the source through the five checks above; then
   `ell_refine.py l1kc95dh170f 95 l1kc103winx 103 1 21.125 2.1062343410 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`
   in one process, 4 BLAS threads, BelowNormal, cap 21600 s (6 h) by the exact pid. ACCEPTED only if `kc103_syscheck_1025.py` exits 0 on the result, its selftest exits 0, `--mutate=F` and `--mutate=steps` exit 1, and `kc95_syscheck_1025.py` exits 1 on the result (refuses it). The marker `regrid_accepted.txt` (with the state and record blobs) is written from the driver's python process. The driver also prints the steps ratio against dh170's regrid at this D (3206 to 3476 steps, 1.0842, 7305 s on his machine) and my D 21.0 regrid (3219 to 3489, 1.0839); information only, not an acceptance.
2. **Step 2, scan, only after ACCEPTED** (`kc103d21125x_scan_driver_1025.py`): `d18_hybsign.py` (the hybrid sign: float64 blocks 0 to 11 and a dd block 12, the 1e-15 noise test with 2 seeds, the float64 sign beside it) at D 21.125 in four processes, one share each, one thread each, BelowNormal, cap 21600 s by the exact pids; the reader first passes its selftest and its two `--mutate` controls (exit 0, 1, 1):

| process | file | lambdas, in this order |
|---|---|---|
| p0 | `scan_kc103x_D21125_p0.jsonl` | 0.885, 0.875 |
| p1 | `scan_kc103x_D21125_p1.jsonl` | 0.880 |
| p2 | `scan_kc103x_D21125_p2.jsonl` | 0.890, 0.895 |
| p3 | `scan_kc103x_D21125_p3.jsonl` | 0.885 (the repeat, another process than p0's) |

   6 evaluations: 5 distinct points 0.875 to 0.895 by 0.005 and the repeat of 0.885. Round 1 is the four points nearest the two predictions (0.885 twice, 0.880, 0.890), round 2 the two edges (0.875 on p0, 0.895 on p2), so p1 and p3 end first. Then `read_lower.py . 0.875 0.895` (`D18_DIR` the inputs; it reads every `scan_*_p*.jsonl` of the folder, three-decimal keys, prints a robust change between adjacent points whatever the spacing). Each driver hc's t5 its end and every line the reader printed.
3. Each driver starts its own sampler (every 60 s), alert-only memory watcher (free physical memory every 15 s, one hc alert to t5 below 1 GB, at most every 30 min; kills nothing) and keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` until that driver's pid is gone, power plan untouched). The other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.
4. `go_kc103d21125x_1025.cmd` runs step 1 and, only if `regrid_accepted.txt` exists, step 2, in one headless console, started as `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc103d21125x_1025.cmd` (outside my terminal; the session check `session_check_1025.ps1` must show no `claude` in the chain).

Stops (t5's): a regrid not accepted, an exception, no robust change in the window, a step over 6 h. Any of them is reported to t5 at once, not widened.

Dry tests (`selftest_scan_dry_1025.txt`, `kc103_regrid_w.log.dry`): the regrid driver's pins, three selftests and lambda_0 check pass (exit 0, nothing started); the scan driver runs its checks on a stand-in marker, state and record (dh170's k_c 95 D 21.125 files renamed to the k_c 103 tag, in a folder that is not published) and reaches "would start" for four processes (exit 0), refuses a missing marker, refuses a marker with a wrong blob, refuses seven bad share lists (exit 2) and refuses `--out` without `--dry`. The real marker, state and record exist only after the regrid.

## Cost, written before the run

The basis is my k_c 103 D 21.0 run on this machine (same k_c, code, threads and priority; only D and the source's origin differ; 3489 steps there against dh170's 3476 at this D): regrid 11280 s (peak private 4.01 GB, cpu 21328 s), scan points 6619 to 6628 s in round 1 (four processes) and 4148 to 4149 s in round 2 (two processes), the scan 10800 s, worker peaks 3.966 and 3.964 GB (two points) and 2.691 and 2.689 GB (one point), lowest free memory 16.08 GB, peak commit 20.85 GB. The D 21.0 round-1 points ran 1.64 times my k_c 95 ones, not the 1.27 I had written, so I take the observed numbers, not the factor.

| item | estimate | basis |
|---|---|---|
| source checks | about 20 s | 20 s by hand here |
| regrid | about 10500 to 12500 s (2.9 to 3.5 h), peak private about 3.8 to 4.3 GB | 11280 s at D 21.0 times 3476/3489; peak private 4.01 GB |
| each scan point, round 1 (four processes) | about 6000 to 7500 s | 6619 to 6628 s at D 21.0 |
| each scan point, round 2 (two processes) | about 3800 to 4600 s | 4148 to 4149 s at D 21.0 |
| the scan | about 9800 to 12100 s (2.7 to 3.4 h); p1 and p3 (round 1 only) about 1.7 to 2.1 h | round 1 plus round 2 as above; 10800 s at D 21.0 |
| peak private | about 3.7 to 4.3 GB per worker with two points, 2.5 to 3.0 GB with one; the four peaks sum to about 13 to 14 GB | the D 21.0 workers; free memory at the start about 23 GB, lowest at D 21.0 16.08 GB |
| together | start about 22:35 UTC; the regrid ends about 01:30 to 02:05 UTC (25 Nov); p1 and p3 end about 03:10 to 04:10; the scan ends about 04:15 to 05:25 UTC | the rows above |

The sampler (`rows/regrid_samples.csv`, `rows/scan_samples.csv`) gives the real figures.

## Files made here

`make_kc103d21125x_1025.py` writes `kc103d21125x_regrid_driver_1025.py`, `kc103d21125x_scan_driver_1025.py`, `kc103d21125x_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `sample_driver4_1025.ps1`, `go_kc103d21125x_1025.cmd` and `publish_kc103d21125x_1025.sh` from the k_c 103 D 21.0 ones (staging `kc103d21_1025`, raw `I1025-win/kc103_d21` at 3499f61a8) by asserted text replacements. `diff_regrid_driver_vs_kc103d21.txt` is the diff of the regrid driver against the D 21.0 one, `kc103_syscheck_1025_vs_kc95.diff` the diff of the two checks, `prep_kc103d21125x_pins_1025.txt` the pins, `prep_source_checks_by_hand.txt` the by-hand source checks.

## Status

Not started; the order, the predictions and the estimates above are written before the run.

Pushed 2026-11-24 22:26:00 UTC.

## Result

Not yet run.
