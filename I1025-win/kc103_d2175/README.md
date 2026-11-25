# I1025-win/kc103_d2175: k_c 103 at D 21.75, regridded from dh610's accepted k_c 95 state there, then a hybrid sign scan at 0.635 to 0.655 (winb)

Written before the run, 2026-11-25 04:35:59 UTC (the time of the README-first push; later pushes keep it). Neither the regrid nor the scan had been run for this folder when the order, the prediction and the estimates below were written. Run beforehand, read-only: the dry run of the regrid driver (pins, three selftests, lambda_0), the source checks by hand (20 s), the scan driver's dry run on a stand-in marker, state and record. Runner: the winb session (surface-laptop-4, Windows 11, 4 cores, 32 GB); coordinator t5.

## Order (t5's hc of 2026-11-25, ~04:30 UTC, winb section, quoted; and the reply on the cap)

"Coordinator (t5): ruling: k_c 103 at D 21.125 on Windows = 0.884384, by position, in window A (dh170's Linux 0.884383): builds agree. Next task (#1025): k_c 103 at D 21.75 from dh610's accepted k_c 95 state there (raw I1025-dh610/kc95_d2175; pin by blob; the kc95 check accepts it, controls 1 1, the kc87 and kc103 checks refuse it). Regrid as your kc103 runs, then scan 0.635 to 0.655 by 0.005 with the repeat of 0.645, 4 procs. Prediction: k_c 95's root 0.645855 minus 0.001 = 0.6449 (bar 0.005); report position AND orientation. Raw I1025-win/kc103_d2175/, README first."

My question to t5 (hc ~04:34 UTC): dh610's own k_c 95 regrid at this D took 9339 s on 8 threads, so my 4-thread k_c 103 regrid is estimated at 15000 to 29000 s and may hit the 6 h stop; t5's answer (hc ~04:35 UTC): "cap 43200 s for the regrid, with your hc at 21600 s if it is still running; the scan keeps 21600 s."

My reading: "as your kc103 runs" is the regrid in one process at 4 BLAS threads, BelowNormal, outside my terminal, the scan in four processes at one thread each. **The regrid's cap is 43200 s (12 h) by the exact pid, with one hc to t5 at 21600 s (6 h) if it is still running; nothing is stopped at 6 h. The scan's cap is 21600 s (6 h).** Stops (as before): a regrid not accepted (or capped), an exception, no robust change in the window (report, do not widen), a scan step over 6 h. Also as before: report the peak private memory of the regrid and of a scan point; nothing kills on memory. My folders `I1025-win/kc103_d21` (3499f61a8) and `I1025-win/kc103_d21125x` (c58c9430a, README first 51dc82cb2) are pushed; #1025 comments 7145851300 and 7152929405.

## Written before the scan (t5's prediction)

**PREDICTION: lambda_1 at k_c 103 and D 21.75 = 0.645855 - 0.001 = 0.6449, bar 0.005, report position and orientation.** By position: `read_lower.py` prints one robust change and its det-linear estimate lies in [0.6399, 0.6499] (0.6449 +- 0.005); if it prints more than one robust change, all are printed as they come and the one nearest dh610's k_c 95 root 0.645855 is the one compared. Not met if that robust change lies outside [0.6399, 0.6499]. If the reader prints no robust change in the window the order says stop and report, not widen: I stop. If the regrid is not accepted there is no scan.

Position and orientation are reported as the reader prints them: the bracket (a grid step 0.005 wide), the det-linear estimate, the estimator range, and the orientation (`+ to -` or `- to +`), beside dh610's k_c 95 reading and macm3's k_c 87 reading at this D (below). t5 rules by position; orientation is information, and I do not interpret it.

The grid is t5's: 0.635 to 0.655 by 0.005 (5 points) plus a repeat of 0.645 (6 evaluations). The window ends (0.635, 0.655) are the only evaluated edges.

For reference (not predictions of mine):

| reading | by position | det-linear | range | orientation as printed | where |
|---|---|---|---|---|---|
| k_c 87, D 21.75, macm3 (macOS) | (0.645, 0.650) | 0.646846 | [0.646292, 0.646846] | - to + | `I1025-macm3/kc87_leg_lambda/21.75/` (as dh610's README quotes it) |
| k_c 95, D 21.75, dh610 (Linux), regridded from macm3's k_c 87 state | (0.645, 0.650) | 0.645855 | [0.645557, 0.645855] | - to + | `I1025-dh610/kc95_d2175/read_lower.txt` |

dh610's k_c 95 scan at D 21.75 (window 0.640 to 0.665): hybrid signs 0.640- 0.645- 0.650+ 0.655+ 0.660+ 0.665+, the float64 sign differing from the hybrid at 0.640 and 0.660, ln|det| 0.640 -2838.894, 0.645 -2841.526, 0.650 -2839.947, 0.655 -2839.593; his k_c 87 to 95 step at this D is -0.000991 (0.646846 to 0.645855). The k_c steps at D 21.0 (+0.0018, then mine -0.000062 for 95 to 103) and D 21.125 (+0.0039, then +0.0033) are in `I1025-win/kc103_d21` and `kc103_d21125x`. dh610's regrid at this D: 9339 s on 8 threads (loaded), 3152 steps (macm3's k_c 87: 2887), |F| 4.3937655374e-10, constraint 3.214e-03, Delta 1.1386286581, peak RSS 2.84 GiB.

## The source (dh610's)

| item | value |
|---|---|
| raw folder | `I1025-dh610/kc95_d2175` (state and record from his regrid commit dc5a6edb; origin/main 6889e8299 at my fetch) |
| state | `in/sol_l1kc95dh610d2175_D21.7500.npy`, blob ee18ab90e3dc826d2d45c600b0e6938b20ccd48e (49848 bytes), ACCEPTED by dh610 2026-11-24 19:53:52 UTC |
| record | `in/l1kc95dh610d2175.jsonl`, blob 6bde1c86007d67e7c3c6e36c2d9e64fc743d75a7 (373 bytes, one row; the same blob as the folder's top-level `l1kc95dh610d2175.jsonl`): k_c 95, D 21.75, kappa 0.7, u0 0.04, Ks 30, \|F\| 4.3937655373792033e-10, F_start 2.9424622522010715e-05, steps 3152, constraint 3.2139850093208574e-03, Delta 1.1386286581052725, 9337 s (src `l1kc87Lmacm3b`) |
| the checks | `kc87_syscheck_1025.py` 6df5d960, `kc95_syscheck_1025.py` d487e628 (dh610's; the k_c 87 check with 3 changed lines), `kc103_syscheck_1025.py` 3ab58d16 (dh170's: the k_c 95 check with only the k_c constant changed, 3 lines, `kc103_syscheck_1025_vs_kc95.diff`); the first two blobs equal those in dh610's `in/` |
| scanner, reader | `d18_hybsign.py` e089207a, `d185_scan_read.py` 7c9d400f, `read_lower.py` 89309d3c, the same blobs as my earlier runs |
| code | the worktree `choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_delta.py` and `ell_refine.py` at 48c36355, `ell_refine.py` blob 631e5801), the one of my k_c 103 regrids at D 21.0 and 21.125; dh610's regrid used the same commit (`choptuik-large-d-1025g` at 48c36355) |
| lambda_0 | 2.1037780803 (`ell_delta.lam0_at(21.75, *ell_delta.lam0_table())[0]` in that worktree, equal to dh610's; unused with `--no-gamma`; the driver checks it) |

The copies are in `inputs/`; the source state and record are also in the worktree's `solver/matter/data/` (where `ell_refine.py` reads its source); each is pinned by blob in `prep_kc103d2175_pins_1025.txt` and checked by the driver. Nothing of dh610's is modified.

The source checks, run by hand at 04:33 UTC before writing this (read-only, `REC STATE 21.75 WTM` with absolute paths; `prep_source_checks_by_hand.txt`): `kc95_syscheck_1025.py` exit 0 ("ACCEPTED: the record class's \|F\| with a step count that comes back"; record \|F\| 4.3937655374e-10, the state's \|F\| on this machine 4.3938889411e-10 (0.003 % apart, inside the 1 % bar), `freeze_from` 3152 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1 (3152 against 3153), `kc87_syscheck_1025.py` exit 1 ("the record is not k_c 87 at D 21.75 (kc 95, D 21.75)"), `kc103_syscheck_1025.py` exit 1 ("the record is not k_c 103 at D 21.75 (kc 95, D 21.75)"); the selftests of all three checks exit 0. The driver repeats all of them and stops if any differs.

## The run

1. **Step 1, regrid** (`kc103d2175_regrid_driver_1025.py`, a copy of my k_c 103 D 21.125 one with the pins, tags, D, source and lambda_0 changed and the cap raised to 43200 s with an hc at 21600 s, `diff_regrid_driver_vs_crossbuild.txt`): the pins; the selftests of the three checks (exit 0) and the lambda_0 check; the source through the five checks above; then
   `ell_refine.py l1kc95dh610d2175 95 l1kc103win2175 103 1 21.75 2.1037780803 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`
   in one process, 4 BLAS threads, BelowNormal, cap 43200 s (12 h) by the exact pid. ACCEPTED only if `kc103_syscheck_1025.py` exits 0 on the result, its selftest exits 0, `--mutate=F` and `--mutate=steps` exit 1, and `kc95_syscheck_1025.py` exits 1 on the result (refuses it). The marker `regrid_accepted.txt` (with the state and record blobs) is written from the driver's python process. The driver also prints the steps ratio against dh610's k_c 87 to 95 regrid at this D (2887 to 3152, 1.0918) and my k_c 95 to 103 regrids (3206 to 3476, 1.0842 at D 21.125; 3219 to 3489, 1.0839 at D 21.0); information only, not an acceptance.
2. **Step 2, scan, only after ACCEPTED** (`kc103d2175_scan_driver_1025.py`): `d18_hybsign.py` (the hybrid sign: float64 blocks 0 to 11 and a dd block 12, the 1e-15 noise test with 2 seeds, the float64 sign beside it) at D 21.75 in four processes, one share each, one thread each, BelowNormal, cap 21600 s by the exact pids; the reader first passes its selftest and its two `--mutate` controls (exit 0, 1, 1):

| process | file | lambdas, in this order |
|---|---|---|
| p0 | `scan_kc103_D2175_p0.jsonl` | 0.645, 0.635 |
| p1 | `scan_kc103_D2175_p1.jsonl` | 0.640 |
| p2 | `scan_kc103_D2175_p2.jsonl` | 0.650, 0.655 |
| p3 | `scan_kc103_D2175_p3.jsonl` | 0.645 (the repeat, another process than p0's) |

   6 evaluations: 5 distinct points 0.635 to 0.655 by 0.005 and the repeat of 0.645. Round 1 is the four points nearest the prediction and dh610's root (0.645 twice, 0.640, 0.650), round 2 the two edges (0.635 on p0, 0.655 on p2), so p1 and p3 end first. Then `read_lower.py . 0.635 0.655` (`D18_DIR` the inputs; it reads every `scan_*_p*.jsonl` of the folder, three-decimal keys, prints a robust change between adjacent points whatever the spacing). Each driver hc's t5 its end and every line the reader printed.
3. Each driver starts its own sampler (every 60 s), alert-only memory watcher (free physical memory every 15 s, one hc alert to t5 below 1 GB, at most every 30 min; kills nothing) and keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` until that driver's pid is gone, power plan untouched). The other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.
4. `go_kc103d2175_1025.cmd` runs step 1 and, only if `regrid_accepted.txt` exists, step 2, in one headless console, started as `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc103d2175_1025.cmd` (outside my terminal; the session check `session_check_1025.ps1` must show no `claude` in the chain).

Dry tests (`selftest_scan_dry_1025.txt`, `kc103_regrid_w.log.dry`): the regrid driver's pins, three selftests and lambda_0 check pass (exit 0, nothing started; the planned command shows cap 43200 s); the scan driver runs its checks on a stand-in marker, state and record (dh610's k_c 95 D 21.75 files renamed to the k_c 103 tag, in a folder that is not published) and reaches "would start" for four processes (exit 0), refuses a missing marker, refuses a marker with a wrong blob, refuses seven bad share lists (exit 2) and refuses `--out` without `--dry`. The real marker, state and record exist only after the regrid.

## Cost, written before the run

The regrid is the uncertain part. What I have:

| source of the estimate | number |
|---|---|
| my k_c 103 regrids on this machine (4 threads) | 11280 s at D 21.0 (3489 steps), 11520 s at D 21.125 (3476 steps); peak private 4.01 GB both; cpu 21328 and 21732 s |
| dh610's k_c 87 to 95 regrid at D 21.0 against mine (same step, his machine against mine) | 5457 s against 9000 s: my machine is 1.65 times slower |
| dh610's k_c 87 to 95 regrid at D 21.75 (8 threads, nice 10, loaded: two 8-process scans and a recount beside it) | 9339 s, 2.9 times the cpu work of his D 19.75 regrid (3066 s); F_start 2.94e-05, 8.8 times that of D 19.75; 3152 steps |
| my k_c 95 to 103 step cost over the k_c 87 to 95 step | 1.25 (D 21.0: 9000 to 11280 s); 1.32 (dh170's D 21.125: 5523 to 7305 s) |

So 9339 s times 1.65 (machine) times 1.25 to 1.32 (k_c step) is 19300 to 20300 s; if his figure was inflated by load, the cost is nearer my D 21.0 and 21.125 regrids (about 11500 s, a lower bound at the same step count about 3420). The scan points do not depend on D through anything but the step count (3417 expected here against 3476 at D 21.125); dh610's 7736 to 9925 s per point at this D were with 15 scan processes on 20 logical CPUs, against 2442 to 2770 s at D 19.75 with 4 processes, so I take my D 21.125 points as the basis and flag that as uncertain.

| item | estimate | basis |
|---|---|---|
| source checks | about 20 s | 20 s by hand here, 16 s at D 21.125 |
| regrid | about 15000 to 29000 s (4.2 to 8.1 h), central about 19000 s (5.3 h); cpu about 1.9 times wall; peak private about 3.8 to 4.4 GB | the table above; peak private 4.01 GB at D 21.0 and 21.125 (dh610's RSS here 2.84 GiB against dh170's 3.00 GiB at D 21.125) |
| each scan point, round 1 (four processes) | about 5500 to 7500 s | 6257 to 6275 s at D 21.125, 6619 to 6628 s at D 21.0 |
| each scan point, round 2 (two processes) | about 3700 to 4700 s | 3870 and 3879 s at D 21.125, 4148 and 4149 s at D 21.0 |
| the scan | about 9300 to 12200 s (2.6 to 3.4 h); p1 and p3 (round 1 only) about 1.5 to 2.1 h | round 1 plus round 2 as above; 10155 s at D 21.125 |
| peak private | about 3.7 to 4.3 GB per worker with two points, 2.5 to 3.0 GB with one; the four peaks sum to about 13 to 14 GB | the D 21.125 workers (3.964, 3.966, 2.892, 2.897 GB); free memory at the start about 23 GB, lowest at D 21.125 15.95 GB |
| together | start about 04:50 UTC; the hc at 21600 s about 10:50 UTC if the regrid still runs; the regrid ends about 09:00 to 12:55 UTC (central about 10:05); the scan ends about 11:35 to 16:15 UTC (central about 13:00) | the rows above |

The sampler (`rows/regrid_samples.csv`, `rows/scan_samples.csv`) gives the real figures.

## Files made here

`make_kc103d2175_1025.py` writes `kc103d2175_regrid_driver_1025.py`, `kc103d2175_scan_driver_1025.py`, `kc103d2175_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `sample_driver4_1025.ps1`, `go_kc103d2175_1025.cmd` and `publish_kc103d2175_1025.sh` from the k_c 103 D 21.125 ones (staging `kc103d21125x_1025`, raw `I1025-win/kc103_d21125x` at c58c9430a) by asserted text replacements. `diff_regrid_driver_vs_crossbuild.txt` is the diff of the regrid driver against the D 21.125 one, `kc103_syscheck_1025_vs_kc95.diff` the diff of the two checks, `prep_kc103d2175_pins_1025.txt` the pins, `prep_source_checks_by_hand.txt` the by-hand source checks.

## Status

**Step 1 running since 2026-11-25 04:36:28 UTC** (the chain started 04:36:11 UTC through `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc103d2175_1025.cmd`). README first: 00815e29b (pushed 04:35:59 UTC, before the start).

- **Chain** (`rows/launcher_pid.txt`: 8672): conhost --headless 8672 <- cmd 18848 <- regrid driver launcher 3772 and driver 7672 <- sampler 18396, alert-only watcher 3800, keep-awake helper 16680, and the regrid process 18616 (worker 22920). The python and powershell processes are BelowNormal.
- **Session check** (`session_check_regrid.txt`, exit 0): no `claude` in any chain of the run, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain.
- **Before the regrid** (04:36:11 to 04:36:28 UTC, 16 s): the pins matched; the selftests of the three checks exited 0; ell_delta.lam0_at(21.75) = 2.1037780803; the source checks were as ordered: the k_c 95 check exit 0 on the source, `--mutate=F` and `--mutate=steps` exit 1, the k_c 87 check exit 1 and the k_c 103 check exit 1 (they refuse the source; `source_kc*_syscheck*.txt`).
- **Regrid:** pid 18616 started 04:36:28 UTC: `ell_refine.py l1kc95dh610d2175 95 l1kc103win2175 103 1 21.75 2.1037780803 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, cwd the worktree's `solver/matter`, 4 threads, BelowNormal, cap 43200 s by the exact pid; the driver sends t5 one hc at 21600 s (10:36 UTC) if it still runs.
- **Machine at the start:** on AC (battery status 2, charge 100), clock 2995 MHz of 2995 MHz max, free physical memory 23.32 GB; beside it the other project's two I114 `convergence.py` jobs (started 2026-11-23 05:41 UTC), not touched.
- **ETA** (the estimates above counted from the actual start 04:36:28 UTC, 14 min before the 04:50 the table assumed): the regrid ends about 08:50 to 12:40 UTC (written 15000 to 29000 s; central about 09:55), the scan about 11:25 to 16:05 UTC (central about 12:50). The scan starts by itself after ACCEPTED.

Pushed 2026-11-25 04:36:46 UTC.

## Result

Not yet run.
