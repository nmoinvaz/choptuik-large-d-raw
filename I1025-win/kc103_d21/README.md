# I1025-win/kc103_d21: k_c 103 at D 21.0, regridded from my accepted k_c 95 D 21.0 state, then a hybrid sign scan at 0.905 to 0.925 (winb)

Written before the run, 2026-11-24 15:54:21 UTC (the time of the README-first push; later pushes keep it). Neither the regrid nor the scan had been run for this folder when the order, the prediction and the estimates below were written. Run beforehand, read-only: the dry run of the regrid driver (pins, both selftests), the source checks by hand (12 s), the scan driver's dry run on a stand-in marker, state and record. Runner: the winb session (surface-laptop-4, Windows 11, 4 cores, 32 GB); coordinator t5.

## Order (t5's hc of 2026-11-24, ~15:47 UTC, winb section, quoted)

"Coordinator (t5) to winb, #1025. Ruling on D 21.0: lambda_1 at k_c 95 = 0.913510 (by position, the only robust change). The k_c steps at D 21.0 are now +0.0021 (79 -> 87) and +0.0018 (87 -> 95), a ratio of 0.87 (0.79 at D 21.125): lambda_1 converges slowly in k_c.
Next task, after you push kc95_d21: k_c 103 at D 21.0, the third step there (dh170 runs the same at D 21.125).
Raw: a new folder I1025-win/kc103_d21/ (README first; the prediction below written before the scan).
1. Regrid your accepted k_c 95 state at D 21.0 to k_c 103 with ell_refine.py, exactly as your kc95_d21 regrid (same worktree, venv, threads and priority), changing only the source tag/k_c and the target k_c (103). Acceptance: the k_c 103 check dh170 made, kc103_syscheck_1025.py (blob 3ab58d16, in raw I1025-dh170/kc103_d21125/; dh610's kc95 check with only the k_c constant changed): its selftest 0, it must refuse your k_c 95 state (exit 1), and accept the regrid with --mutate=F and --mutate=steps both exit 1.
2. Scan with d18_hybsign.py as before, 4 processes: lambda 0.905, 0.910, ..., 0.925 and a repeat of 0.915. PREDICTION (register it): 0.913510 + 0.0016 = 0.9151 (bar 0.005), the root nearest the k_c 95 root by position.
Stop on: a regrid not accepted, an exception, no robust change in the window (report, do not widen), a step over 6 h. Report peak private memory of the regrid and of a scan point; nothing kills on memory."

My reading: "exactly as your kc95_d21 regrid" is the regrid in one process at 4 BLAS threads, BelowNormal, outside my terminal, the scan in four processes at one thread each. The cap of both steps is 21600 s (t5's 6 h) by the exact pids (the k_c 95 regrid had 28800 s). The k_c 95 folder `I1025-win/kc95_d21` is pushed: 7b7f37628 (README first 2d9cf0e93).

## Written before the scan (t5's prediction)

**PREDICTION: lambda_1 at k_c 103 = 0.913510 + 0.0016 = 0.9151, bar 0.005, the root nearest the k_c 95 root by position.** By position: `read_lower.py` prints one robust change and its det-linear estimate lies in [0.9101, 0.9201] (0.9151 +- 0.005); if it prints more than one robust change, the one nearest 0.913510 is the one compared (all are printed as they come). Not met if the nearest robust change lies outside [0.9101, 0.9201]. If the reader prints no robust change in the window the order says stop and report, not widen: I stop. If the regrid is not accepted there is no scan.

The grid is t5's: 0.905 to 0.925 by 0.005 (5 points) plus a repeat of 0.915 (6 evaluations). The window ends (0.905, 0.925) are the only evaluated edges; below 0.905 and above 0.925 are not evaluated. The reading is t5's to rule; I print the reader's lines as they come and do not interpret.

For reference, the k_c 95 reading at D 21.0 (mine, `I1025-win/kc95_d21/read_lower_kc95_D21.log`): one robust change (0.910, 0.915), `+` to `-` as printed, det-linear 0.913510, range [0.912716, 0.913510]; hybrid signs 0.900+ 0.905+ 0.910+ 0.915- 0.920- 0.925-; dh610's k_c 87 reading 0.911685 (printed `-` to `+`).

## The source (mine)

| item | value |
|---|---|
| raw folder, commit | `I1025-win/kc95_d21`, 7b7f37628 (README first 2d9cf0e93, regrid status bccb82b2f) |
| state | `sol_l1kc95winbg_D21.0000.npy`, blob d7a4844a76e47c015591ac9ad839dddc14a5b2ce (49848 bytes), ACCEPTED 2026-11-24 13:41:25 UTC (`regrid_accepted.txt`) |
| record | `l1kc95winbg.jsonl`, blob 2e8fe124f24534089f6cb29dff227db5789f8e96 (369 bytes, one row): k_c 95, D 21.0, kappa 0.7, u0 0.04, Ks 30, \|F\| 4.5952560080417797e-10, F_start 1.469260393434695e-05, steps 3219, constraint 1.6464811136992104e-03, Delta 1.1182248057026958, 8985 s |
| the k_c 95 checks | `kc95_syscheck_1025.py` d487e628 (dh610's, `I1025-dh610/kc95_d195/in/`; the k_c 87 check with 3 changed lines) |
| the k_c 103 check (t5's) | `kc103_syscheck_1025.py` 3ab58d16 (dh170's, `I1025-dh170/kc103_d21125/in/`): the k_c 95 check with only the k_c constant changed, 3 lines (`kc103_syscheck_1025_vs_kc95.diff`: `rec.get("kc") != 95` to `!= 103`, its message, and the selftest's planted `kc=95` to `kc=103`); blob checked against raw origin/main after fetch |
| scanner, reader | `d18_hybsign.py` e089207a, `d185_scan_read.py` 7c9d400f, `read_lower.py` 89309d3c, the same blobs as my k_c 87 and k_c 95 runs |
| code | the worktree `choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_delta.py` and `ell_refine.py` at 48c36355, `ell_refine.py` blob 631e5801), the one of every regrid here and the one of my k_c 95 regrid |
| lambda_0 | 2.1067409501 (the k_c 95 regrid's; unused with `--no-gamma`) |

The copies are in `inputs/` and the source state and record are also in the worktree's `solver/matter/data/` (where `ell_refine.py` wrote them and reads its source); each is pinned by blob in `prep_kc103d21_pins_1025.txt` and checked by the driver.

The source checks, run by hand at 15:53 UTC before writing this (read-only, `REC STATE 21.0 WTM` with absolute paths; 12 s in all): `kc95_syscheck_1025.py` exit 0 (record \|F\| 4.5952560080e-10, `freeze_from` 3219 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1, `kc103_syscheck_1025.py` exit 1 ("the record is not k_c 103 at D 21 (kc 95, D 21.0)"); the selftests of both checks exit 0. The driver repeats all of them and stops if any differs.

## The run

1. **Step 1, regrid** (`kc103d21_regrid_driver_1025.py`, a copy of the k_c 95 one with the pins, tags, source and target k_c and the cap changed, `diff_regrid_driver_vs_kc95d21.txt`): the pins; the selftests of both checks (exit 0); the source through the four checks above; then
   `ell_refine.py l1kc95winbg 95 l1kc103winbg 103 1 21.0 2.1067409501 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`
   in one process, 4 BLAS threads, BelowNormal, cap 21600 s (6 h) by the exact pid. ACCEPTED only if `kc103_syscheck_1025.py` exits 0 on the result, its selftest exits 0, `--mutate=F` and `--mutate=steps` exit 1, and `kc95_syscheck_1025.py` exits 1 on the result (refuses it). The marker `regrid_accepted.txt` (with the state and record blobs) is written from the driver's python process. The driver also prints the steps ratio (the k_c 87 to 95 regrid at D 21.0 had 3219/2948 = 1.092; information only, not an acceptance).
2. **Step 2, scan, only after ACCEPTED** (`kc103d21_scan_driver_1025.py`): `d18_hybsign.py` (the hybrid sign: float64 blocks 0 to 11 and a dd block 12, the 1e-15 noise test with 2 seeds, the float64 sign beside it) at D 21.0 in four processes, one share each, one thread each, BelowNormal, cap 21600 s by the exact pids; the reader first passes its selftest and its two `--mutate` controls (exit 0, 1, 1):

| process | file | lambdas, in this order |
|---|---|---|
| p0 | `scan_kc103_D21_p0.jsonl` | 0.915, 0.905 |
| p1 | `scan_kc103_D21_p1.jsonl` | 0.910 |
| p2 | `scan_kc103_D21_p2.jsonl` | 0.920, 0.925 |
| p3 | `scan_kc103_D21_p3.jsonl` | 0.915 (the repeat, another process than p0's) |

   6 evaluations: 5 distinct points 0.905 to 0.925 by 0.005 and the repeat of 0.915. Round 1 is the four points nearest the prediction (0.910, 0.915 twice, 0.920), round 2 the two edges (0.905 on p0, 0.925 on p2), so p1 and p3 end first. Then `read_lower.py . 0.905 0.925` (`D18_DIR` the inputs; it reads every `scan_*_p*.jsonl` of the folder, three-decimal keys, prints a robust change between adjacent points whatever the spacing). Each driver hc's t5 its end and every line the reader printed.
3. Each driver starts its own sampler (every 60 s), alert-only memory watcher (free physical memory every 15 s, one hc alert to t5 below 1 GB, at most every 30 min; kills nothing) and keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` until that driver's pid is gone, power plan untouched). The other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.
4. `go_kc103d21_1025.cmd` runs step 1 and, only if `regrid_accepted.txt` exists, step 2, in one headless console, started as `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc103d21_1025.cmd` (outside my terminal; the session check `session_check_1025.ps1` must show no `claude` in the chain).

Stops (t5's): a regrid not accepted, an exception, no robust change in the window, a step over 6 h. Any of them is reported to t5 at once, not widened.

Dry tests (`selftest_scan_dry_1025.txt`, `kc103_regrid_w.log.dry`): the regrid driver's pins and both selftests pass (exit 0, nothing started); the scan driver runs its checks on a stand-in marker, state and record (the k_c 95 D 21.0 files renamed to the k_c 103 tag, in a folder that is not published) and reaches "would start" for four processes (exit 0), refuses a missing marker, refuses a marker with a wrong blob, refuses seven bad share lists (exit 2) and refuses `--out` without `--dry`. The real marker, state and record exist only after the regrid.

## Cost, written before the run

| item | estimate | basis |
|---|---|---|
| source checks | about 15 s | 12 s by hand here, 12 s at k_c 95 |
| regrid | about 10500 to 13000 s (2.9 to 3.6 h), peak private about 3.9 to 4.4 GB | my k_c 95 regrid at D 21.0 took 9000 s (peak private 3.45 GB, cpu 16430 s, 3219 steps); the cost grew by 1.28 per k_c step of 8 at D 19 (79 to 87: 7965 s, 87 to 95: 10230 s), about (103/95)^3 = 1.27, which gives 11500 s; memory (103/95)^2 = 1.18 times 3.45 GB = 4.06 GB |
| each scan point | about 4900 to 5500 s in round 1 (four processes); 3900 to 4500 s in round 2 (two processes) | my k_c 95 points at D 21.0 took 4041 to 4055 s (four processes) and 3396 to 3398 s (three), times 1.27 |
| the scan | about 8800 to 10000 s (2.4 to 2.8 h); p1 and p3 (one point each) about 1.4 to 1.5 h | round 1 plus round 2 as above; the k_c 95 scan took 7470 s |
| peak private | about 3.7 to 4.2 GB per worker with two points, 2.5 to 3.0 GB for a worker with one; 15 to 16.5 GB for four | k_c 95 workers peaked at 3.332 to 3.336 GB (two points) and 2.31 GB (one point), times 1.18; free memory at the start about 23 GB, lowest at k_c 95 16.46 GB |
| together | start about 16:10 UTC; the regrid ends about 19:05 to 19:45 UTC; p1 and p3 end about 21:00 to 21:20, the scan about 21:30 to 22:40 UTC | the rows above |

The sampler (`rows/regrid_samples.csv`, `rows/scan_samples.csv`) gives the real figures.

## Files made here

`make_kc103d21_1025.py` writes `kc103d21_regrid_driver_1025.py`, `kc103d21_scan_driver_1025.py`, `kc103d21_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `sample_driver4_1025.ps1`, `go_kc103d21_1025.cmd` and `publish_kc103d21_1025.sh` from the k_c 95 D 21.0 ones (staging `kc95d21_1025`, raw `I1025-win/kc95_d21` at 7b7f37628) by asserted text replacements, and copies the source state and record and the pinned scripts into `inputs/`. `diff_regrid_driver_vs_kc95d21.txt` is the diff of the regrid driver against the k_c 95 one, `kc103_syscheck_1025_vs_kc95.diff` the diff of the two checks, `prep_kc103d21_pins_1025.txt` the pins.

## Status

**Step 1 ACCEPTED 2026-11-24 19:03:01 UTC (regrid 15:54:47 to 19:02:47 UTC); step 2, the scan, 19:04:12 to 22:04:12 UTC (10800 s, exits 0, 0, 0, 0); the Result is below.** The chain started 15:54:34 UTC through `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc103d21_1025.cmd`). README first: 84814983f (pushed 15:54:21 UTC, before the start).

- **Chain** (`rows/launcher_pid.txt`: 23592): conhost --headless 23592 <- cmd 6172 <- regrid driver launcher 4964 and driver 26180 <- sampler 1852, alert-only watcher 24592, keep-awake helper 15056, and the regrid process 19580 (worker 10484). The python and powershell processes are BelowNormal.
- **Session check** (`session_check_regrid.txt`, exit 0): no `claude` in any chain of the run, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain.
- **Before the regrid** (15:54:35 to 15:54:47 UTC, 12 s): the pins matched; the selftests of both checks exited 0; the source checks were as ordered: the k_c 95 check exit 0 on the source, `--mutate=F` and `--mutate=steps` exit 1, the k_c 103 check exit 1 (it refuses the source; `source_kc*_syscheck*.txt`).
- **Regrid:** pid 19580 started 15:54:47 UTC: `ell_refine.py l1kc95winbg 95 l1kc103winbg 103 1 21.0 2.1067409501 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, cwd the worktree's `solver/matter`, 4 threads, BelowNormal, cap 21600 s by the exact pid.
- **Machine at the start:** on AC (battery status 2, charge 100), clock 2995 MHz of 2995 MHz max, free physical memory 23.08 GB; beside it the other project's I114 `convergence.py` jobs, not touched.
- **Regrid result** (`regrid_summary.txt`, `kc103_regrid_w.log`, `l1kc103winbg.jsonl`; exit 0, wall 11280 s, inside the written 10500 to 13000 s):

| item | k_c 103 (this regrid) | k_c 95 source |
|---|---|---|
| wall | 11280 s (the record's seconds 11270) | 9000 s |
| record \|F\| | 4.579058467349325e-10 | 4.5952560080417797e-10 |
| F_start | 6.363778361219054e-06 | 1.469260393434695e-05 |
| steps | 3489 | 3219 |
| constraint | 1.0089054869257237e-03 | 1.6464811136992104e-03 |
| Delta | 1.1182226750306323 | 1.1182248057026958 |
| cpu | 21328 s | 16430 s |
| peak private (the largest python) | 4.01 GB (peak working set 3.64 GB) | 3.45 GB |

  Delta(k_c 103) minus Delta(k_c 95) = -2.1306720634495235e-06 (k_c 87 to 95 at D 21.0: -4.881e-06). Steps ratio 1.0839 (k_c 87 to 95: 3219/2948 = 1.092). Wall ratio 1.253 (written 1.27). Lowest free memory 20.49 GB (18:15:49 UTC), peak commit 14.4 GB, laptop CPU mean 41.6 % (max 74 %), 187 sampler rows, no gap over 90 s. Nothing alerted, nothing was killed.
- **Acceptance** (`syscheck.txt`, `syscheck_mutate.txt`, `syscheck_kc95_on_result.txt`, `selftest_kc103_syscheck_after.txt`): the k_c 103 check on the result exit 0 ("ACCEPTED: the record class's |F| with a step count that comes back"; state \|F\| equals the record's, `freeze_from` gives 3489 steps), its selftest exit 0, `--mutate=F` exit 1, `--mutate=steps` exit 1, the k_c 95 check on the result exit 1 ("the record is not k_c 95 at D 21"). Marker `regrid_accepted.txt`: ACCEPTED 19:03:01 UTC, state blob 253c58e2f22aeb941e236eb9c4d605d57c61dea5, record blob 43d672aea9267929ff32c9ae8428a62f7d9a8b55.
- **Scan** (19:04:12 UTC, by itself after the marker; `kc103d21_scan_w.log`): `read_lower.py` selftest exit 0 and its two `--mutate` controls exit 1, 1; 4 processes of `d18_hybsign.py`, 1 thread each, BelowNormal: p0 pid 21560 (0.915 then 0.905), p1 pid 2556 (0.910), p2 pid 21216 (0.920 then 0.925), p3 pid 22848 (0.915, the repeat). Scan driver 24392 (launcher 20668) under the same cmd 6172, sampler 25932, watcher 21624, keep-awake 20244. Session check `session_check_scan.txt` exit 0: no `claude` in any chain, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain. Machine at the start: on AC (battery status 2, charge 100), clock 2995 of 2995 MHz, free physical memory 23.31 GB.
- **ETA** (the estimates above counted from 19:04:12 UTC): p1 and p3 end about 20:30 UTC (written 4900 to 5500 s for round 1), the scan about 21:30 to 21:50 UTC (written 8800 to 10000 s). Observed: p1 and p3 ended 20:54:57 UTC (6645 s), p2 22:03:57, p0 22:04:12 (the scan 10800 s), the driver 22:05:22; later than this ETA, see the cost table below.

Pushed 2026-11-24 22:07:49 UTC.

## Result

The reader's lines are in `read_lower_kc103_D21.log` (exit 0) and `scan_kc103_D21.log`, as printed:

```
points 5 in 0.905-0.925; not noise-robust: none
hybrid signs: 0.905+ 0.910+ 0.915- 0.920- 0.925-
float64 sign differs from the hybrid sign at: [(0.915, '-', '+')]
repeated points: [(0.915, 'agree')]
  robust change (0.910, 0.915), + to -, det-linear 0.913448, range [0.912544, 0.913448]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: + at 0.905, - at 0.925
```

**One robust change, in (0.910, 0.915), `+` to `-`, det-linear 0.913448.** The window's ends are `+` at 0.905 and `-` at 0.925. The orientation `+` to `-` is as printed, the same as my k_c 95 scan (dh610's k_c 87 scan at D 21.0 printed `-` to `+`). I do not say what that means; t5 rules by position.

| lambda | process | hybrid sign | hybrid ln\|det\| | noise seeds | float64 sign | float64 ln\|det\| | wall s |
|---|---|---|---|---|---|---|---|
| 0.905 | p0 (second) | + | -3308.772109 | +, + | + | -3307.982711 | 4149 |
| 0.910 | p1 | + | -3310.286943 | +, + | + | -3309.683073 | 6628 |
| 0.915 | p0 (first) | - | -3311.085647 | -, - | + | -3310.888214 | 6625 |
| 0.915 (repeat) | p3 | - | -3311.085647 | -, - | + | -3310.888214 | 6619 |
| 0.920 | p2 (first) | - | -3310.383652 | -, - | - | -3309.868735 | 6620 |
| 0.925 | p2 (second) | - | -3310.356785 | -, - | - | -3310.094587 | 4148 |

The repeat of 0.915 (p3, another process) agrees with p0's to every digit printed (hybrid ln\|det\| -3311.0856473458, float64 -3310.8882141008 in both). All 6 evaluations are noise-robust. The float64 sign differs from the hybrid sign at 0.915 only (float64 `+`, hybrid `-`): the float64 column alone would put its change in (0.915, 0.920); the hybrid column, which the reader uses, changes in (0.910, 0.915). At my k_c 95 scan the float64 column differed at 0.910 (float64 `-`, hybrid `+`).

The change lies 0.003448 above the grid point 0.910 and 0.001552 below 0.915 (det-linear range [0.912544, 0.913448]). The hybrid ln\|det\| at 0.915 is -3311.086, which is 0.799 below its value at 0.910 and 0.702 below its value at 0.920. All four workers printed "the record system" first: \|F\| 4.5802037613e-10 (record 4.5790584673e-10), steps 3489 (record 3489).

### Against the line written before (t5's)

| line | observed | |
|---|---|---|
| the root nearest the k_c 95 root 0.913510 by position, det-linear in [0.9101, 0.9201] (0.913510 + 0.0016 = 0.9151, bar 0.005) | one robust change, det-linear 0.913448, which is 0.001652 below 0.9151 and 0.003348 above the lower edge 0.9101 | met by position |
| stop if no robust change in the window (report, do not widen) | one robust change | not triggered |

By position only; t5 rules. The step from my k_c 95 reading is 0.913448 - 0.913510 = -0.000062 (written +0.0016); from dh610's k_c 87 reading 0.911685 it is +0.001763.

### The k_c steps at D 21.0 (all by position, as printed)

| k_c | robust change, det-linear | between grid points | orientation as printed | step from the line above |
|---|---|---|---|---|
| 87 (dh610) | 0.911685 | 0.910 and 0.915 | - to + | |
| 95 (mine) | 0.913510 | 0.910 and 0.915 | + to - | +0.001825 |
| 103 (mine) | 0.913448 | 0.910 and 0.915 | + to - | -0.000062 |

t5's earlier figures: the steps at D 21.0 were +0.0021 (79 to 87) and +0.0018 (87 to 95).

Not evaluated: below 0.905, above 0.925. A change outside the window is not excluded; the two edge signs `+` and `-` differ, as one change needs. All 5 points are noise-robust, so a second change between two scanned points would show in the signs, and none does. Pairs of changes inside one 0.005 step are not excluded.

### Cost against the estimates written before

| item | written | observed |
|---|---|---|
| source checks | about 15 s | 12 s (15:54:35 to 15:54:47) |
| regrid | 10500 to 13000 s, peak private about 3.9 to 4.4 GB | 11280 s (inside), peak private 4.01 GB (inside), peak working set 3.64 GB, cpu 21328 s |
| each scan point, round 1 (four processes) | about 4900 to 5500 s | 6619 to 6628 s (above the range) |
| each scan point, round 2 (two processes) | about 3900 to 4500 s | 4148 and 4149 s (inside) |
| the scan | 8800 to 10000 s (2.4 to 2.8 h) | 10800 s (3.00 h; 800 s above the range) |
| end of the scan | p1 and p3 about 21:00 to 21:20 UTC, the scan about 21:30 to 22:40 (the "together" row) | p1 and p3 20:54:57 UTC (5 min before), p2 22:03:57, p0 22:04:12 (inside) |
| peak private | about 3.7 to 4.2 GB per worker with two points, 2.5 to 3.0 GB with one; 15 to 16.5 GB for four | p0 3.966 GB and p2 3.964 GB (two points), p1 2.691 GB and p3 2.689 GB (one point), all inside; the four peaks sum to 13.31 GB; peak commit 20.85 GB; lowest free memory 16.08 GB (sampler, 19:59:39 UTC) and 15.85 GB (the watcher's finer poll) |

The round-1 points took about 1.64 times my k_c 95 round-1 points (4041 to 4055 s), the round-2 points about 1.22 times my k_c 95 round-2 points (3396 to 3398 s); the written factor was 1.27. Each worker's cpu matched its wall: about 6453 s in 6645 s for p1 and p3, 10558 s in 10800 s for p0 and p2 (k_c 95: 3927 s for p3's one point, about 7312 s for the others). So the workers were not waiting for a core; they used more cpu seconds per round-1 point than the factor 1.27 gave. I did not measure the cause (the sampler records the laptop's cpu and memory, not memory bandwidth or core clocks). The laptop CPU averaged 72.9 % while four workers ran (max 98 %, min 63 %), 43.4 % while p0 and p2 ran alone, 64.0 % over the scan (max 98 %, min 9 %). Two of the other project's I114 `convergence.py` processes (started 2026-11-23 05:41 UTC) ran beside the scan, untouched, as beside the k_c 95 scan.

The sampler had 177 rows (steps of 60 to 65 s, no gap above 90 s); the alert-only memory watcher sent no alert; the keep-awake helper held 10875 s and cleared at 22:05:27 UTC; the System event log has no power event from 19:00 to 22:10 UTC, only one Kernel-General "system time changed" event at 21:03:33 UTC (a 0 ms change by `SurfaceService.exe`); the machine was on AC (battery status 2, charge 100 %), clock 2995 of 2995 MHz at the end. No exception in any log; exits 0, 0, 0, 0; nothing was killed.
