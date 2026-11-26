# I1025-win/kc103_d22875: k_c 103 at D 22.875, regridded from win2's accepted k_c 95 state there, then a hybrid sign scan at 0.04 to 0.20 (winb)

Written before the run, 2026-11-25 19:00:40 UTC (the time of the README-first push; later pushes keep it). Neither the regrid nor the scan had been run for this folder when the order, the registration and the estimates below were written. Run beforehand, read-only: the dry run of the regrid driver (pins, three selftests, lambda_0), the source checks by hand (under 1 min), the scan driver's dry run on a stand-in marker, state and record. Runner: the winb session (surface-laptop-4, Windows 11, 4 cores, 32 GB); coordinator t5.

## Order (t5's hc of 2026-11-25, read at about 18:54 UTC, winb section, quoted)

"Coordinator (t5): ruling: k_c 103 at D 22.0, lambda_1 (F) = 0.547345 by position (range [0.546590, 0.547345]); registered [0.541, 0.551] MET; k_c steps +0.0009 (87->95), +0.0014 (95->103). Post it on #1025. Next for winb: k_c 103 at D 22.875 from win2's accepted k_c 95 state (raw I1025-win2/kc95_d22875, state blob a14f0d50, record 5381f89d; kc95 check accepts, controls 1 1, kc87 and kc103 refuse), your k_c 103 recipe, cap 43200 s, then a scan 0.04 to 0.20 by 0.02 plus the repeat of 0.10, 4 procs. Register first: k_c 95's root there is in (0.10, 0.12), k_c 87's lambda_1 0.128; a converged lambda_1 predicts 0.10-0.13; a second root (an S-like newcomer, as k_c 87 has at 0.162) would show by k_c parity at 103. Raw I1025-win/kc103_d22875/, README first."

The D 22.0 ruling is posted (#1025 comment 7171599582; raw `I1025-win/kc103_d22` at 78aa1bc90).

My reading: "your k_c 103 recipe" is the one-process regrid at 4 BLAS threads, BelowNormal, outside my terminal, exactly as my k_c 103 regrids at D 21.0, 21.125, 21.75 and 22.0, with the scan in four processes at one thread each. **The regrid's cap is 43200 s (12 h) by the exact pid, with one hc to t5 at 21600 s (6 h) if it is still running (as at D 22.0); nothing is stopped at 6 h. The scan's cap is 21600 s (6 h), my standing cap.** Stops (as before): a regrid not accepted (or capped), an exception, no robust change in the window (report, do not widen), a scan step over 6 h. Also as before: report the peak private memory of the regrid and of a scan point; nothing kills on memory. The laptop is otherwise idle for this chain (the D 22.0 chain ended 18:54:48 UTC).

**Source quality (said in every table):** win2's k_c 95 state here descends from macm3's part c k_c 87 state (h 0.0625, k_c 87 constraint 9.932e-03); the k_c 95 record's psi-constraint is 7.114e-03 (the k_c 95 source at D 22.0: 3.910e-03), F_start 7.521e-05 (D 22.0: 3.642e-05). win2's README calls it a normal-quality source. t5 at D 22.875 (relayed in win2's README): printed orientation is not comparable across source runs.

## Written before the scan (t5's registration)

**PREDICTION: lambda_1 at k_c 103 and D 22.875 lies in 0.10 to 0.13 ("a converged lambda_1 predicts 0.10-0.13"; k_c 95's root there is in (0.10, 0.12), k_c 87's lambda_1 is 0.128).** By position: `read_lower.py` prints a robust change whose det-linear estimate lies in [0.10, 0.13]. If it prints more than one robust change, all are printed as they come and the one nearest 0.11 (the middle of k_c 95's bracket (0.10, 0.12)) is the one compared with [0.10, 0.13]. Not met if that robust change lies outside [0.10, 0.13]. If the reader prints no robust change in 0.04 to 0.20 the order's rule stands (stop and report, do not widen): I stop. If the regrid is not accepted there is no scan.

**A second root** ("an S-like newcomer, as k_c 87 has at 0.162, would show by k_c parity at 103"): any further robust change in 0.04 to 0.20 is reported as the reader prints it (bracket, orientation, det-linear estimate, range), with the hybrid signs and ln\|det\| beside it; the reader's count ("robust changes: N") is the count. Whether a change is S-like, a k_c parity effect or neither is t5's reading, not mine.

Position and orientation are reported as the reader prints them, beside win2's k_c 95 reading and macm3's k_c 87 numbers at this D as t5 gives them (below). t5 rules by position; orientation is information (t5: not compared across k_c or across source runs), and I do not interpret it.

The grid is t5's: 0.04 to 0.20 by 0.02 (9 points) plus a repeat of 0.10 (10 evaluations). The window ends (0.04, 0.20) are the only evaluated edges; its upper end is 0.07 above the top of the predicted range and its lower end 0.06 below the bottom.

For reference (not predictions of mine):

| reading | by position | orientation as printed | where |
|---|---|---|---|
| k_c 87, D 22.875, macm3 | lambda_1 0.128 (win2's README: L 0.1278); a second root at 0.162 (t5's order; win2's README, 16:25 UTC: "F about 0.171 (0.16 to 0.20, being refined by macm3)") | not given to me | as t5 relays it |
| k_c 95, D 22.875, win2 | one change in (0.10, 0.12): hybrid sign + at 0.10 and - at 0.12, 0.14, 0.16, 0.18, 0.20, 0.22 (win2's README at 16:25 UTC, 7 distinct points of 19; the final reading is not in raw at my fetch of 18:56 UTC) | + to - (round 1) | `I1025-win2/kc95_d22875/README.md` |

The k_c steps so far at other D: k_c 87 to 95 is +0.000938 and 95 to 103 +0.001425 at D 22.0 (`I1025-win/kc103_d22`). Those are readings, not predictions of mine. win2's regrid at this D: 5901 s (record) on a 20-logical-CPU machine, 4 threads, 3126 steps (k_c 87 source: 2862), |F| 3.5210384141e-10, F_start 7.521e-05, constraint 7.114e-03, Delta 1.170668364710.

## The source (win2's)

| item | value |
|---|---|
| raw folder | `I1025-win2/kc95_d22875` (origin/main 28b5f287f at my fetch; state and record committed in 55161c546 "k_c 95 state at D 22.875 accepted (regrid 5916 s)") |
| state | `sol_l1kc95win2d22875_D22.8750.npy`, blob a14f0d50edb575e85387851a61cb2324c1983317 (49848 bytes), ACCEPTED by win2 2026-11-25 14:20 UTC (`regrid_accepted.txt`) |
| record | `l1kc95win2d22875.jsonl`, blob 5381f89d5fe4f81a113295cdde8eb6358de937e8 (371 bytes, one row; the same blob as `rec_k95_D22.8750.jsonl`): k_c 95, D 22.875, kappa 0.7, u0 0.04, Ks 30, \|F\| 3.5210384140874643e-10, F_start 7.520694957814806e-05, steps 3126, constraint 7.113644147048331e-03, Delta 1.170668364709999, 5901 s (src `l1kc87Lmacm3c`) |
| the checks | `kc87_syscheck_1025.py` 6df5d960, `kc95_syscheck_1025.py` d487e628 (dh610's; the k_c 87 check with 3 changed lines), `kc103_syscheck_1025.py` 3ab58d16 (dh170's: the k_c 95 check with only the k_c constant changed, 3 lines, `kc103_syscheck_1025_vs_kc95.diff`) |
| scanner, reader | `d18_hybsign.py` e089207a, `d185_scan_read.py` 7c9d400f, `read_lower.py` 89309d3c, the same blobs as my earlier runs |
| code | the worktree `choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_delta.py` and `ell_refine.py` at 48c36355, `ell_refine.py` committed blob 631e5801), the one of my k_c 103 regrids at D 21.0, 21.125, 21.75 and 22.0; win2's regrid used the same commit (`D:/choptuik-i1025k79` at 48c36355) |
| lambda_0 | 2.0996545550 (`ell_delta.lam0_at(22.875, *ell_delta.lam0_table())[0]` in that worktree, equal to win2's regrid command; unused with `--no-gamma`; the driver checks it) |

The copies are in `inputs/`; the source state and record are also in the worktree's `solver/matter/data/` (where `ell_refine.py` reads its source); each is pinned by blob in `prep_kc103d22875_pins_1025.txt` and checked by the driver. Nothing of win2's is modified.

The source checks, run by hand at 18:58 UTC before writing this (read-only, `REC STATE 22.875 WTM` with absolute paths, 2 threads; `prep_source_checks_by_hand.txt`): `kc95_syscheck_1025.py` exit 0 ("ACCEPTED: the record class's \|F\| with a step count that comes back"; record \|F\| 3.5210384141e-10, the state's \|F\| on this machine 3.5258608347e-10 (0.14 % apart, inside the 1 % bar), `freeze_from` 3126 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (3126 against 3127), `kc87_syscheck_1025.py` exit 1 ("the record is not k_c 87 at D 22.875 (kc 95, D 22.875)"), `kc103_syscheck_1025.py` exit 1 ("the record is not k_c 103 at D 22.875 (kc 95, D 22.875)"); the selftests of all three checks exit 0. The driver repeats all of them and stops if any differs.

## The run

1. **Step 1, regrid** (`kc103d22875_regrid_driver_1025.py`, a copy of my k_c 103 D 22.0 one with the pins, tags, D, source and lambda_0 changed, `diff_regrid_driver_vs_prev.txt`): the pins; the selftests of the three checks (exit 0) and the lambda_0 check; the source through the five checks above; then
   `ell_refine.py l1kc95win2d22875 95 l1kc103win22875 103 1 22.875 2.0996545550 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`
   in one process, 4 BLAS threads, BelowNormal, cap 43200 s (12 h) by the exact pid, one hc to t5 at 21600 s if it still runs. ACCEPTED only if `kc103_syscheck_1025.py` exits 0 on the result, its selftest exits 0, `--mutate=F` and `--mutate=steps` exit 1, and `kc95_syscheck_1025.py` exits 1 on the result (refuses it). The marker `regrid_accepted.txt` (with the state and record blobs) is written from the driver's python process. The driver also prints the steps ratio against win2's k_c 87 to 95 regrids (2862 to 3126, 1.0923, at this D; 2874 to 3139, 1.0922, at D 22.0) and my k_c 95 to 103 regrids (3139 to 3402, 1.0838 at D 22.0; 3152 to 3417, 1.0841 at D 21.75; 3206 to 3476, 1.0842 at D 21.125; 3219 to 3489, 1.0839 at D 21.0); information only, not an acceptance.
2. **Step 2, scan, only after ACCEPTED** (`kc103d22875_scan_driver_1025.py`): `d18_hybsign.py` (the hybrid sign: float64 blocks 0 to 11 and a dd block 12, the 1e-15 noise test with 2 seeds, the float64 sign beside it) at D 22.875 in four processes, one share each, one thread each, BelowNormal, cap 21600 s by the exact pids; the reader first passes its selftest and its two `--mutate` controls (exit 0, 1, 1):

| process | file | lambdas, in this order |
|---|---|---|
| p0 | `scan_kc103_D22875_p0.jsonl` | 0.10, 0.08, 0.04 |
| p1 | `scan_kc103_D22875_p1.jsonl` | 0.12, 0.16, 0.20 |
| p2 | `scan_kc103_D22875_p2.jsonl` | 0.14, 0.06 |
| p3 | `scan_kc103_D22875_p3.jsonl` | 0.10 (the repeat, another process than p0's), 0.18 |

   10 evaluations: 9 distinct points 0.04 to 0.20 by 0.02 and the repeat of 0.10. Round 1 is the points on and beside the predicted range (0.10 twice, 0.12, 0.14), round 2 the next ones (0.08, 0.16, 0.06, 0.18) on all four processes, round 3 the two ends (0.04 on p0, 0.20 on p1) on two processes (p2 and p3 are done). Then `read_lower.py . 0.04 0.2` (`D18_DIR` the inputs; it reads every `scan_*_p*.jsonl` of the folder, three-decimal keys, prints a robust change between adjacent points whatever the spacing). Each driver hc's t5 its end and every line the reader printed. If the cap (21600 s) hit in round 3, the driver would kill p0 and p1 by exact pid and report no reading from the reader (rounds 1 and 2 would be in the jsonl files); I would report that to t5 and not widen.
3. Each driver starts its own sampler (every 60 s), alert-only memory watcher (free physical memory every 15 s, one hc alert to t5 below 1 GB, at most every 30 min; kills nothing) and keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` until that driver's pid is gone, power plan untouched). The other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.
4. `go_kc103d22875_1025.cmd` runs step 1 and, only if `regrid_accepted.txt` exists, step 2, in one headless console, started as `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc103d22875_1025.cmd` (outside my terminal; the session check `session_check_1025.ps1` must show no `claude` in the chain).

Dry tests (`selftest_scan_dry_1025.txt`, `kc103_regrid_w.log.dry`): the regrid driver's pins, three selftests and lambda_0 check pass (exit 0, nothing started; the planned command shows cap 43200 s); the scan driver runs its checks on a stand-in marker, state and record (win2's k_c 95 D 22.875 files renamed to the k_c 103 tag, in a folder that is not published) and reaches "would start" for four processes (exit 0), refuses a missing marker, refuses a marker with a wrong blob, refuses seven bad share lists (exit 2) and refuses `--out` without `--dry`. The real marker, state and record exist only after the regrid.

## Cost, written before the run

The regrid is the uncertain part. What I have:

| source of the estimate | number |
|---|---|
| my k_c 103 regrids on this machine (4 threads) | 11280 s at D 21.0 (3489 steps), 11520 s at D 21.125 (3476), 8415 s at D 21.75 (3417), 10230 s at D 22.0 (3402; cpu 20591 s); peak private 4.01 GB in all four |
| win2's k_c 95 regrids (4 threads, 20-logical-CPU machine) | 7662 s at D 22.0 (3139 steps), 5901 s at D 22.875 (3126); mine at D 22.0 took 1.335 times win2's (10230 against 7662); F_start 7.521e-05 here against 3.642e-05 at D 22.0 |
| the source here | 3126 steps (k_c 95): the k_c 103 result should have about 3126 times 1.0838 = 3388 steps |
| my scan points, k_c 103, four processes | 5955 to 6034 s at D 22.0 (3402 steps), 6391 to 6415 s at D 21.75 (3417), 6257 to 6275 s at D 21.125 (3476), 6619 to 6628 s at D 21.0 (3489); peak private 3.963 to 3.967 GB per worker at D 22.0 (sum 15.86 GB), lowest free memory 13.66 GB |
| my scan points with fewer than four processes | none measured for k_c 103 |

The regrid at D 22.0 (10230 s) came in above its central estimate and inside its range; win2's regrid here is 0.77 times his at D 22.0, so I take 1.335 times 5901 s = 7900 s as the centre and a range around it from my four regrids (8415 to 11520 s) and win2's ratio. The scan points: rounds 1 and 2 have four processes (the D 22.0 figure 5955 to 6034 s for 3402 steps, here about 3388 steps, and the machine is the same); round 3 has two processes (less contention; not measured, so I allow 4500 to 6600 s).

| item | estimate | basis |
|---|---|---|
| source checks | about 15 to 60 s | 16 s at D 22.0; the by-hand run here, 2 threads, under 1 min |
| regrid | about 6500 to 11500 s (1.8 to 3.2 h), central about 8500 s; cpu about 2.0 times wall; peak private about 3.8 to 4.4 GB | the table above; 4.01 GB at all four earlier D |
| each scan point in rounds 1 and 2 (four processes) | about 5800 to 6600 s | 5955 to 6034 s at D 22.0 (3402 steps), 3388 steps here |
| the round 3 points (two processes) | about 4500 to 6600 s | not measured |
| the scan | about 16100 to 19800 s (4.5 to 5.5 h), central about 17500 s | two rounds of 5800 to 6600 s plus round 3 |
| peak private | about 3.8 to 4.2 GB per worker; the four peaks sum to about 15.5 to 16.5 GB in rounds 1 and 2 | 3.963 to 3.967 GB per worker at D 22.0 |
| lowest free memory in the scan | about 11 to 14 GB | 13.66 GB at D 22.0 (sampler), 12.85 GB (watcher); 14.93 GB at D 22.125 |
| together | start about 19:15 UTC; the hc at 21600 s about 01:15 UTC (26 Nov) if the regrid still runs; the regrid ends about 21:05 to 22:30 UTC (central about 21:35); the scan ends about 01:35 to 04:00 UTC on 26 Nov (central about 02:30: 21:35 plus 17500 s plus 1 min) | the rows above |

The sampler (`rows/regrid_samples.csv`, `rows/scan_samples.csv`) gives the real figures. At the top of the scan range (19800 s plus the start 71 s after the regrid) the scan would finish about 1800 s inside its 21600 s cap.

## Files made here

`make_kc103d22875_1025.py` writes `kc103d22875_regrid_driver_1025.py`, `kc103d22875_scan_driver_1025.py`, `kc103d22875_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `sample_driver4_1025.ps1`, `go_kc103d22875_1025.cmd` and `publish_kc103d22875_1025.sh` from the k_c 103 D 22.0 ones (staging `kc103d22_1025`, raw `I1025-win/kc103_d22` at 78aa1bc90) by asserted text replacements. `diff_regrid_driver_vs_prev.txt` is the diff of the regrid driver against the D 22.0 one, `kc103_syscheck_1025_vs_kc95.diff` the diff of the two checks, `prep_kc103d22875_pins_1025.txt` the pins, `prep_source_checks_by_hand.txt` the by-hand source checks.

## Status

**Step 1, the regrid, ACCEPTED 2026-11-25 21:58:38 UTC. Step 2, the scan, DONE 2026-11-26 03:46:50 UTC (started 21:59:50, 20821 s, exits 0, 0, 0, 0; the chain ended 03:48:05 UTC).** The reading is in Result below. The secant refinement of the root started 03:48:13 UTC (`secant/`, its own README). README first: 922c75666 (pushed 19:00:40 UTC, before the start); running status c84b8da4b; chain started 19:00:56 UTC through `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc103d22875_1025.cmd`. The D 22.0 chain ended 18:54:48 UTC and its reading was posted (#1025 comment 7171599582) and pushed (78aa1bc90) first.

**Regrid (`regrid_summary.txt`, `regrid.log`, `l1kc103win22875.jsonl`):**

| item | k_c 103 result | win2's k_c 95 source |
|---|---|---|
| run | 19:01:12 to 21:58:27 UTC, pid 25032 (worker 3724), exit 0, 10635 s wall (the record's seconds: 10632) | 5901 s (record), 20-logical-CPU machine |
| \|F\| | 3.4634221167e-10 | 3.5210384141e-10 |
| F_start | 3.2876e-05 | 7.5207e-05 |
| steps | 3387 | 3126 |
| steps ratio | 1.0835 | win2's k_c 87 to 95 at this D: 1.0923 |
| constraint | 4.6176e-03 | 7.1136e-03 |
| Delta | 1.1706557197960814 | 1.170668364709999 |
| Delta(k_c 103) minus Delta(k_c 95) | -1.2645e-05 | |
| marker `regrid_accepted.txt` | state 280515313e580cccbf14a6e0828e4eaa9b22086d, record f623d3e67b94a5ac4e38e2c55d05d3bf247e4c71 | state a14f0d50, record 5381f89d |

Acceptance (`syscheck.txt`, `syscheck_mutate.txt`, `syscheck_kc95_on_result.txt`, `selftest_kc103_syscheck_after.txt`, 11 s): `kc103_syscheck_1025.py` on the result exit 0 ("ACCEPTED: the record class's \|F\| with a step count that comes back"; state \|F\| 3.4634221167e-10 equal to the record's, `freeze_from` 3387 steps = the record's), its selftest exit 0, `--mutate=F` exit 1, `--mutate=steps` exit 1, `kc95_syscheck_1025.py` on the result exit 1 ("the record is not k_c 95 at D 22.875 (kc 103, D 22.875)").

My k_c 103 regrids beside this one (4 threads, same code, same recipe):

| D | source | wall | steps | steps ratio | peak private |
|---|---|---|---|---|---|
| 21.0 | dh610's k_c 95 | 11280 s | 3489 | 1.0839 | 4.01 GB |
| 21.125 | dh610's k_c 95 | 11520 s | 3476 | 1.0842 | 4.01 GB |
| 21.75 | dh610's k_c 95 | 8415 s | 3417 | 1.0841 | 4.01 GB |
| 22.0 | win2's k_c 95 | 10230 s | 3402 | 1.0838 | 4.007 GB |
| 22.875 | win2's k_c 95 | 10635 s | 3387 | 1.0835 | 4.006 GB |

**Cost against the written estimates (regrid):**

| item | written | measured |
|---|---|---|
| source checks | about 15 to 60 s | 16 s (19:00:56 to 19:01:12; also the pins and selftests) |
| regrid | 6500 to 11500 s, central about 8500 s | 10635 s (inside the range, above the centre; my basis was win2's 5901 s times 1.335, 7900 s: the ratio of mine to win2's is 1.80 here) |
| steps | about 3388 (3126 times 1.0838) | 3387 |
| cpu | about 2.0 times wall | 21420 s (2.01 times wall) |
| peak private | 3.8 to 4.4 GB | 4.006 GB (peak working set 3.65 GB) |
| lowest free memory | not written for the regrid | 19.31 GB at 21:34:30 UTC (22.93 GB at the start) |
| peak commit | not written | 15.4 GB |
| laptop cpu | not written | mean 44.1 %, max 100 % (sampler: 176 sample times, no gap over 90 s) |

The memory watcher raised no alert (`rows/regrid_memwatch.log`: "minimum free memory seen 19.29 GB; 0 alert(s) sent") and the keep-awake helper held until the driver ended (last line 21:45:57 UTC, 9900 s; "pid 24316 is gone after 10740 s"); the System log shows no power event in 19:00 to 22:05 UTC. `rows/regrid_raw.log` holds 24 RuntimeWarning lines from `dss_ell.py` (overflow and invalid value in the Newton step, as at D 22.0 and 21.75); the record and the acceptance are unaffected. The 21600 s hc was not needed.

**Scan, started by itself 71 s after the marker:**

- **Chain** (`rows/launcher_pid.txt`: 3284): conhost --headless 3284 <- cmd 26024 <- scan driver launcher 25476 and driver 24884 <- sampler 21672, alert-only watcher 24080, keep-awake helper 3096, and the four `d18_hybsign.py` workers p0 6764 (0.10, 0.08, 0.04), p1 3988 (0.12, 0.16, 0.20), p2 15080 (0.14, 0.06), p3 11740 (0.10 repeat, 0.18), each with child processes. BelowNormal, one thread each, cap 21600 s by the exact pids.
- **Before the scan** (21:59:49 to 21:59:50 UTC): the reader's selftest exit 0 and its two `--mutate` controls exit 1, 1 as wanted.
- **Session check** (`session_check_scan.txt`, exit 0): no `claude` in any chain of the run, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain.
- **Machine at the start:** free physical memory 22.12 GB; the other project's I114 `convergence.py` jobs are beside it and not touched.
- **End:** the scan ended 03:46:50 UTC (written ETA about 01:20 to 03:45 UTC, central about 02:15: it came in 1 to 2 minutes past the upper end and 779 s inside its cap); reader lines in Result.

Pushed 2026-11-26 03:50:51 UTC.

## Result

Reader (`read_lower_kc103_D22875.log`, `read_lower.py` 89309d3c on this folder, window 0.040 to 0.200), lines as printed:

```
points 9 in 0.040-0.200; not noise-robust: none
hybrid signs: 0.040- 0.060- 0.080- 0.100- 0.120+ 0.140+ 0.160+ 0.180+ 0.200+
float64 sign differs from the hybrid sign at: none
repeated points: [(0.1, 'agree')]
  robust change (0.100, 0.120), - to +, det-linear 0.119801, range [0.103345, 0.119801]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: - at 0.040, + at 0.200
read_lower exit 0
```

The 10 evaluations (`scan_kc103_D22875_p0..p3.jsonl`; every worker first printed the record system: \|F\| 3.4630896969e-10 against the record's 3.4634221167e-10, 3387 steps = the record's; the scan driver's exits 0, 0, 0, 0). Source quality as said above: constraint 7.114e-03 (k_c 95 source), 4.618e-03 (this k_c 103 state).

| lambda | process | hybrid sign | hybrid ln\|det\| | float64 sign | float64 ln\|det\| | noise-robust (2 seeds) | seconds |
|---|---|---|---|---|---|---|---|
| 0.04 | p0 (round 3) | - | -2958.8211687077 | - | -2958.8469572543 | yes | 4433 |
| 0.06 | p2 (round 2) | - | -2961.0200804811 | - | -2960.9710526170 | yes | 8208 |
| 0.08 | p0 (round 2) | - | -2963.3435030002 | - | -2963.3124143217 | yes | 8213 |
| 0.10 | p0 (round 1) | - | -2965.9784565466 | - | -2965.8396194327 | yes | 8153 |
| 0.10 (repeat) | p3 (round 1) | - | -2965.9784565466 | - | -2965.8396194327 | yes | 8171 |
| 0.12 | p1 (round 1) | + | -2970.5766920529 | + | -2969.5443838089 | yes | 8172 |
| 0.14 | p2 (round 1) | + | -2969.6720641035 | + | -2969.5881525267 | yes | 8175 |
| 0.16 | p1 (round 2) | + | -2970.9222343133 | + | -2970.8142420917 | yes | 8208 |
| 0.18 | p3 (round 2) | + | -2972.4418032965 | + | -2972.6509282725 | yes | 8219 |
| 0.20 | p1 (round 3) | + | -2974.0759244266 | + | -2973.9804787766 | yes | 4427 |

The repeat of 0.10 (p3) is bit-identical to p0's: same hybrid and float64 ln\|det\|. All 10 evaluations are noise-robust, and the float64 sign equals the hybrid sign at every point.

**Against the registration** (the table "Written before the scan", t5's): registered, a robust change with det-linear estimate in [0.10, 0.13]; the second-root clause reports any further robust change as printed. Printed: **one** robust change, (0.100, 0.120), `- to +`, det-linear **0.119801**, range [0.103345, 0.119801]. **Met by position** (0.119801 lies in [0.10, 0.13]; 0.0098 above 0.11, the middle of k_c 95's bracket (0.10, 0.12); the reader's count is "robust changes: 1": no second robust change in 0.04 to 0.20, no non-robust point touching a change, no ln\|det\| minimum without a sign change). Beside it, as t5 relays it and win2's README states it, not interpreted by me:

| reading at D 22.875 | by position | orientation as printed |
|---|---|---|
| k_c 87, macm3 (as t5 relays) | lambda_1 0.128; a second root at 0.162 | not given to me |
| k_c 95, win2 (README at 16:25 UTC) | one change in (0.10, 0.12) | + to - (round 1) |
| k_c 103, this scan | one change in (0.100, 0.120), det-linear 0.119801, range [0.103345, 0.119801] | - to + |

t5's ruling on the scan (hc, read at about 03:47 UTC on 26 Nov, quoted): "k_c 103 at D 22.875, lambda_1 (F) by position in (0.100, 0.120), det-linear 0.119801; registered 0.10-0.13 MET; no second root in 0.04-0.20 (k_c 87 had the newcomer at 0.162; at k_c 103 none in this window). Go ahead with the queued secant refinement on that bracket (0.100, 0.120)." The refinement is in `secant/` (its own README).

**Cost against the estimates written before the run (scan):**

| item | written | measured |
|---|---|---|
| each scan point in rounds 1 and 2 (four processes) | 5800 to 6600 s | 8153 to 8219 s: **above** the written range (1.24 to 1.40 times) |
| the round 3 points (two processes) | 4500 to 6600 s | 4427 and 4433 s (just below the range's lower end) |
| the scan | 16100 to 19800 s, central about 17500 s | 20821 s (21:59:50 to 03:46:50 UTC): **above** the written range, 779 s inside the 21600 s cap |
| peak private per worker | 3.8 to 4.2 GB (sum 15.5 to 16.5 GB in rounds 1 and 2) | 3.965, 3.968, 3.968, 3.969 GB (sum 15.87 GB); working set peak about 2.98 GB |
| cpu per worker | not written | 20293 and 20294 s (p0, p1), 15942 and 15946 s (p2, p3) against walls of 20821 and 16395 s: cpu/wall 0.97 to 0.99 |
| lowest free memory | 11 to 14 GB | 13.87 GB in the sampler (01:11:29 UTC), 12.39 GB in the alert-only watcher (15 s polls); 22.12 GB at the start |

Commit up to 26.34 GB, laptop cpu 36 to 100 % (mean 68.9 %), 339 sample times with no gap over 65 s (the gap test across midnight). No alert, nothing killed (`rows/scan_memwatch.log`: "minimum free memory seen 12.39 GB; 0 alert(s) sent"); the keep-awake helper held until the driver ended (`rows/scan_keepawake.log`); the System log shows no power event in 21:55 UTC to 03:55 UTC. The point times were 1.24 to 1.40 times my written figure and 1.37 times the D 22.0 scan's (5955 to 6034 s for 3402 steps); the workers' cpu seconds rose by the same factor (cpu/wall 0.97 to 0.99, so not a stall), and the other project's I114 `convergence.py` jobs ran beside the whole scan; the cause is unmeasured. The written range came from the D 22.0 figure.

Run summary: README first 922c75666 (19:00:40 UTC); regrid 19:01:12 to 21:58:27 UTC (10635 s); scan 21:59:50 to 03:46:50 UTC (20821 s); chain ended 03:48:05 UTC; chain wall 8 h 47 min.
