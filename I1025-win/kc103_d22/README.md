# I1025-win/kc103_d22: k_c 103 at D 22.0, regridded from win2's accepted k_c 95 state there, then a hybrid sign scan at 0.530 to 0.560 (winb)

Written before the run, 2026-11-25 12:40:28 UTC (the time of the README-first push; later pushes keep it). Neither the regrid nor the scan had been run for this folder when the order, the prediction and the estimates below were written. Run beforehand, read-only: the dry run of the regrid driver (pins, three selftests, lambda_0), the source checks by hand (under 1 min), the scan driver's dry run on a stand-in marker, state and record. Runner: the winb session (surface-laptop-4, Windows 11, 4 cores, 32 GB); coordinator t5.

## Order (t5's hc of 2026-11-25, read at about 12:35 UTC, winb section, quoted)

"Coordinator (t5): ruling: no root of k_c 95 in 0.52-0.76 at D 22.125, where k_c 87 has S at 0.6199: S is absent at k_c 95 there (registered outcome B). Post it on #1025. Next for winb, #1025: k_c 103 at D 22.0 from win2's accepted k_c 95 state (raw I1025-win2/kc95_d22, tag l1kc95win2d22; pin by blob; kc95 check accepts, controls 1 1, kc87 and kc103 refuse), your k_c 103 regrid recipe, cap 43200 s, then a scan 0.530 to 0.560 by 0.005 plus the repeat of 0.545, 4 procs. Register first: k_c 87 0.544982 and k_c 95 0.545920 (+0.0009); a converged F predicts 0.546 +- 0.005. Raw I1025-win/kc103_d22/, README first."

My reading: "your k_c 103 regrid recipe" is the one-process regrid at 4 BLAS threads, BelowNormal, outside my terminal, exactly as my k_c 103 regrids at D 21.0, 21.125 and 21.75, with the scan in four processes at one thread each. **The regrid's cap is 43200 s (12 h) by the exact pid, with one hc to t5 at 21600 s (6 h) if it is still running (as at D 21.75); nothing is stopped at 6 h. The scan's cap is 21600 s (6 h).** Stops (as before): a regrid not accepted (or capped), an exception, no robust change in the window (report, do not widen), a scan step over 6 h. Also as before: report the peak private memory of the regrid and of a scan point; nothing kills on memory. The D 22.125 high scan is pushed (`I1025-win/kc95_d22125_high` at dbc9a329d; #1025 comment 7162586928), so the laptop is free for this chain.

## Written before the scan (t5's registration)

**PREDICTION: lambda_1 at k_c 103 and D 22.0 = 0.546 +- 0.005 ("a converged F predicts 0.546 +- 0.005"; k_c 87 0.544982 and k_c 95 0.545920, a step of +0.0009).** By position: `read_lower.py` prints one robust change and its det-linear estimate lies in [0.541, 0.551]; if it prints more than one robust change, all are printed as they come and the one nearest k_c 95's root 0.545920 is the one compared. Not met if that robust change lies outside [0.541, 0.551]. If the reader prints no robust change in 0.530 to 0.560 the order's rule stands (stop and report, do not widen): I stop. If the regrid is not accepted there is no scan.

Position and orientation are reported as the reader prints them: the bracket (a grid step 0.005 wide), the det-linear estimate, the estimator range, and the orientation (`+ to -` or `- to +`), beside win2's k_c 95 reading and macm3's k_c 87 reading at this D (below). t5 rules by position; orientation is information (t5: not compared across k_c), and I do not interpret it.

The grid is t5's: 0.530 to 0.560 by 0.005 (7 points) plus a repeat of 0.545 (8 evaluations). The window ends (0.530, 0.560) are the only evaluated edges; its upper end is 0.0141 above k_c 95's root and its lower end 0.0159 below.

For reference (not predictions of mine):

| reading | by position | det-linear | range | orientation as printed | where |
|---|---|---|---|---|---|
| k_c 87, D 22.0, macm3 (macOS), part b2 | (0.540, 0.545) | 0.544982 | [0.544963, 0.544982] | - to + | `I1025-macm3/kc87_leg_lambda/22.0/read_lower.txt` (hybrid signs 0.535- 0.540- 0.545+ 0.550+ 0.555+, float64 agrees, repeat of 0.545 agrees) |
| k_c 95, D 22.0, win2 (Windows), regridded from macm3's part b2 state | (0.545, 0.550) | 0.545920 | [0.545581, 0.545920] | - to + | `I1025-win2/kc95_d22/read_lower.txt` (hybrid signs 0.535- 0.540- 0.545- 0.550+ 0.555+; the float64 sign differs at 0.550; repeat of 0.545 bit-identical, ln\|det\| -2800.4769864417) |

The k_c steps so far: k_c 87 to 95 is -0.000991 at D 21.75, +0.002113 at D 21.875 and +0.000938 here (0.544982 to 0.545920); k_c 95 to 103 is -0.00006 at D 21.0, +0.0033 at D 21.125 and +0.006816 at D 21.75 (`I1025-win/kc103_d21`, `kc103_d21125x`, `kc103_d2175`; t5's ruling at D 21.75: not converged in k_c). Those are the readings, not predictions of mine. win2's regrid at this D: 7662 s (record) on a 20-logical-CPU machine, 4 threads, 3139 steps (macm3's k_c 87: 2874), |F| 4.1701256268e-10, F_start 3.642e-05, constraint 3.910e-03, Delta 1.1456173904.

## The source (win2's)

| item | value |
|---|---|
| raw folder | `I1025-win2/kc95_d22` (origin/main dbc9a329d at my fetch; state and record committed in 309ff9991 "k_c 95 state at D 22.0 accepted (regrid 7668 s), scan started") |
| state | `sol_l1kc95win2d22_D22.0000.npy`, blob daae6b2e896d2c302be6ab26e25051c44da98a8e (49848 bytes), ACCEPTED by win2 2026-11-25 03:51 UTC (`regrid_accepted.txt`) |
| record | `l1kc95win2d22.jsonl`, blob 85e667361c8a8892022861886eaee945b0b5bb11 (371 bytes, one row; the same blob as `rec_k95_D22.0000.jsonl`): k_c 95, D 22.0, kappa 0.7, u0 0.04, Ks 30, \|F\| 4.170125626762462e-10, F_start 3.641896772097347e-05, steps 3139, constraint 3.909826878104982e-03, Delta 1.1456173904426914, 7662 s (src `l1kc87Lmacm3b2`) |
| the checks | `kc87_syscheck_1025.py` 6df5d960, `kc95_syscheck_1025.py` d487e628 (dh610's; the k_c 87 check with 3 changed lines), `kc103_syscheck_1025.py` 3ab58d16 (dh170's: the k_c 95 check with only the k_c constant changed, 3 lines, `kc103_syscheck_1025_vs_kc95.diff`) |
| scanner, reader | `d18_hybsign.py` e089207a, `d185_scan_read.py` 7c9d400f, `read_lower.py` 89309d3c, the same blobs as my earlier runs |
| code | the worktree `choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_delta.py` and `ell_refine.py` at 48c36355, `ell_refine.py` committed blob 631e5801), the one of my k_c 103 regrids at D 21.0, 21.125 and 21.75; win2's regrid used the same commit (`D:/choptuik-i1025k79` at 48c36355) |
| lambda_0 | 2.1028298859 (`ell_delta.lam0_at(22.0, *ell_delta.lam0_table())[0]` in that worktree, equal to win2's regrid command; unused with `--no-gamma`; the driver checks it) |

The copies are in `inputs/`; the source state and record are also in the worktree's `solver/matter/data/` (where `ell_refine.py` reads its source); each is pinned by blob in `prep_kc103d22_pins_1025.txt` and checked by the driver. Nothing of win2's is modified.

The source checks, run by hand at 12:38 UTC before writing this (read-only, `REC STATE 22.0 WTM` with absolute paths, 2 threads; `prep_source_checks_by_hand.txt`): `kc95_syscheck_1025.py` exit 0 ("ACCEPTED: the record class's \|F\| with a step count that comes back"; record \|F\| 4.1701256268e-10, the state's \|F\| on this machine 4.172124e-10 (0.05 % apart, inside the 1 % bar), `freeze_from` 3139 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (3139 against 3140), `kc87_syscheck_1025.py` exit 1 ("the record is not k_c 87 at D 22 (kc 95, D 22.0)"), `kc103_syscheck_1025.py` exit 1 ("the record is not k_c 103 at D 22 (kc 95, D 22.0)"); the selftests of all three checks exit 0. The driver repeats all of them and stops if any differs.

## The run

1. **Step 1, regrid** (`kc103d22_regrid_driver_1025.py`, a copy of my k_c 103 D 21.75 one with the pins, tags, D, source and lambda_0 changed, `diff_regrid_driver_vs_prev.txt`): the pins; the selftests of the three checks (exit 0) and the lambda_0 check; the source through the five checks above; then
   `ell_refine.py l1kc95win2d22 95 l1kc103win22 103 1 22.0 2.1028298859 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`
   in one process, 4 BLAS threads, BelowNormal, cap 43200 s (12 h) by the exact pid, one hc to t5 at 21600 s if it still runs. ACCEPTED only if `kc103_syscheck_1025.py` exits 0 on the result, its selftest exits 0, `--mutate=F` and `--mutate=steps` exit 1, and `kc95_syscheck_1025.py` exits 1 on the result (refuses it). The marker `regrid_accepted.txt` (with the state and record blobs) is written from the driver's python process. The driver also prints the steps ratio against win2's k_c 87 to 95 regrid at this D (2874 to 3139, 1.0922) and my k_c 95 to 103 regrids (3152 to 3417, 1.0841 at D 21.75; 3206 to 3476, 1.0842 at D 21.125; 3219 to 3489, 1.0839 at D 21.0); information only, not an acceptance.
2. **Step 2, scan, only after ACCEPTED** (`kc103d22_scan_driver_1025.py`): `d18_hybsign.py` (the hybrid sign: float64 blocks 0 to 11 and a dd block 12, the 1e-15 noise test with 2 seeds, the float64 sign beside it) at D 22.0 in four processes, one share each, one thread each, BelowNormal, cap 21600 s by the exact pids; the reader first passes its selftest and its two `--mutate` controls (exit 0, 1, 1):

| process | file | lambdas, in this order |
|---|---|---|
| p0 | `scan_kc103_D22_p0.jsonl` | 0.545, 0.530 |
| p1 | `scan_kc103_D22_p1.jsonl` | 0.550, 0.535 |
| p2 | `scan_kc103_D22_p2.jsonl` | 0.540, 0.555 |
| p3 | `scan_kc103_D22_p3.jsonl` | 0.545 (the repeat, another process than p0's), 0.560 |

   8 evaluations: 7 distinct points 0.530 to 0.560 by 0.005 and the repeat of 0.545. Round 1 is the four points nearest the prediction and win2's root (0.540, 0.545 twice, 0.550), round 2 the rest (0.530, 0.535, 0.555, 0.560); all four processes run in both rounds. Then `read_lower.py . 0.53 0.56` (`D18_DIR` the inputs; it reads every `scan_*_p*.jsonl` of the folder, three-decimal keys, prints a robust change between adjacent points whatever the spacing). Each driver hc's t5 its end and every line the reader printed.
3. Each driver starts its own sampler (every 60 s), alert-only memory watcher (free physical memory every 15 s, one hc alert to t5 below 1 GB, at most every 30 min; kills nothing) and keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` until that driver's pid is gone, power plan untouched). The other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.
4. `go_kc103d22_1025.cmd` runs step 1 and, only if `regrid_accepted.txt` exists, step 2, in one headless console, started as `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc103d22_1025.cmd` (outside my terminal; the session check `session_check_1025.ps1` must show no `claude` in the chain).

Dry tests (`selftest_scan_dry_1025.txt`, `kc103_regrid_w.log.dry`): the regrid driver's pins, three selftests and lambda_0 check pass (exit 0, nothing started; the planned command shows cap 43200 s); the scan driver runs its checks on a stand-in marker, state and record (win2's k_c 95 D 22.0 files renamed to the k_c 103 tag, in a folder that is not published) and reaches "would start" for four processes (exit 0), refuses a missing marker, refuses a marker with a wrong blob, refuses seven bad share lists (exit 2) and refuses `--out` without `--dry`. The real marker, state and record exist only after the regrid.

## Cost, written before the run

The regrid is the uncertain part. What I have:

| source of the estimate | number |
|---|---|
| my k_c 103 regrids on this machine (4 threads) | 11280 s at D 21.0 (3489 steps), 11520 s at D 21.125 (3476), 8415 s at D 21.75 (3417; cpu 15766 s); peak private 4.01 GB in all three |
| win2's k_c 87 to 95 regrid at this D (4 threads, 20-logical-CPU machine) | 7662 s, about 15500 cpu s; F_start 3.642e-05 against dh610's 2.942e-05 at D 21.75 |
| the source here | 3139 steps (k_c 95): the k_c 103 result should have about 3139 times 1.0841 = 3403 steps |
| my scan points, k_c 103, four processes | 6257 to 6275 s at D 21.125 (3476 steps), 6391 to 6415 s at D 21.75 (3417), 6619 to 6628 s at D 21.0 (3489) |
| my scan points, k_c 95, four processes | 4041 to 4055 s at D 21.0 (3219 steps), 4489 to 4619 s at D 22.125 (3132): per step about 1.17 times the D 21.0 ones |

The regrid at D 21.75 (8415 s) came in below my written range, so I take my three regrids, 8415 to 11520 s, as the basis and lean up from the lowest because F_start is larger here (win2's record 3.64e-05 against 2.94e-05 at D 21.75). The scan points: both rounds have four processes (8 evaluations on 4 processes), the slow case; per step the D 22.125 k_c 95 points were slower than the D 21.0 ones, so I take 6400 to 7800 s per point (3403 steps times about 1.9 to 2.3 s per step).

| item | estimate | basis |
|---|---|---|
| source checks | about 20 to 60 s | the by-hand run, 2 threads, under 1 min |
| regrid | about 7500 to 13000 s (2.1 to 3.6 h), central about 9000 s; cpu about 1.9 times wall; peak private about 3.8 to 4.4 GB | the table above; 4.01 GB at D 21.0, 21.125 and 21.75 |
| each scan point (both rounds, four processes) | about 6400 to 7800 s | 6257 to 6628 s at D 21.0 to 21.75 times 0.98 to 1.17 |
| the scan | about 12800 to 15600 s (3.6 to 4.3 h), central about 14000 s | two rounds of the point time |
| peak private | about 3.8 to 4.2 GB per worker (every worker has two points); the four peaks sum to about 15.5 to 16.5 GB | 3.960 and 3.963 GB for the two-point workers at D 21.75; free memory at the start about 23 GB when nothing else runs |
| lowest free memory in the scan | about 11 to 14 GB | 15.09 GB at D 21.75 with a worker sum of 13.3 GB; 14.93 GB at D 22.125 (also 13.3 GB) |
| together | start about 12:50 UTC; the hc at 21600 s about 18:50 UTC if the regrid still runs; the regrid ends about 14:55 to 16:30 UTC (central about 15:20); the scan ends about 18:30 to 20:40 UTC (central about 19:15) | the rows above |

The sampler (`rows/regrid_samples.csv`, `rows/scan_samples.csv`) gives the real figures.

## Files made here

`make_kc103d22_1025.py` writes `kc103d22_regrid_driver_1025.py`, `kc103d22_scan_driver_1025.py`, `kc103d22_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `sample_driver4_1025.ps1`, `go_kc103d22_1025.cmd` and `publish_kc103d22_1025.sh` from the k_c 103 D 21.75 ones (staging `kc103d2175_1025`, raw `I1025-win/kc103_d2175` at df17428bc) by asserted text replacements. `diff_regrid_driver_vs_prev.txt` is the diff of the regrid driver against the D 21.75 one, `kc103_syscheck_1025_vs_kc95.diff` the diff of the two checks, `prep_kc103d22_pins_1025.txt` the pins, `prep_source_checks_by_hand.txt` the by-hand source checks.

## Status

**Step 1, the regrid, RUNNING since 2026-11-25 12:41:03 UTC.** README first: 4bc829382 (pushed 12:40:28 UTC, before the start); chain started 12:40:47 UTC through `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc103d22_1025.cmd`. The D 22.125 chain ended 12:34:35 UTC and its reading was posted (#1025 comment 7162586928) and pushed (dbc9a329d) first.

- **Chain** (`rows/launcher_pid.txt`: 20960): conhost --headless 20960 <- cmd 14280 <- regrid driver launcher 22580 and driver 6588 <- sampler 23196, alert-only watcher 3568, keep-awake helper 5600, and the regrid process 25928 (worker 15468). The python and powershell processes are BelowNormal.
- **Session check** (`session_check_regrid.txt`, exit 0): no `claude` in any chain of the run, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain.
- **Before the regrid** (12:40:47 to 12:41:03 UTC, 16 s): the pins matched; the selftests of the three checks exited 0; ell_delta.lam0_at(22.0) = 2.1028298859; the source checks were as ordered: the k_c 95 check exit 0 on the source, `--mutate=F` and `--mutate=steps` exit 1, the k_c 87 check exit 1 and the k_c 103 check exit 1 (they refuse the source; `source_kc*_syscheck*.txt`).
- **Regrid:** pid 25928 started 12:41:03 UTC: `ell_refine.py l1kc95win2d22 95 l1kc103win22 103 1 22.0 2.1028298859 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, cwd the worktree's `solver/matter`, 4 threads, BelowNormal, cap 43200 s by the exact pid; the driver sends t5 one hc at 21600 s (18:41 UTC) if it still runs.
- **Machine at the start:** free physical memory 22.77 GB; beside it the other project's I114 `convergence.py` jobs, not touched.
- **ETA** (the estimates above counted from 12:41:03 UTC): the regrid ends about 14:55 to 16:30 UTC (central about 15:20); the scan then starts by itself about 71 s later and ends about 18:30 to 20:40 UTC (central about 19:15).

Pushed 2026-11-25 12:41:23 UTC.

## Result

Not yet run.
