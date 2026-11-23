# I1025-win/kc87_d19: k_c 87 at D 19, regridded from my own k_c 79 D 19 state, then a scan (winb)

Written before the run, 2026-11-23 05:11:38 UTC (substituted from `date -u` when pushed). Nothing has been run for this folder yet.

Runner: the winb session (surface-laptop-4, 4 cores, 8 threads, 32 GB), the same one that ran `../kc79_d19/` (the k_c 79 D 19 regrid and first scan), `../kc79_d19low/` (raw 40f1a01a) and `../kc79_d19gap/` (raw fee69df5). The coordinator is t5.

## Order (t5's hc of 2026-11-23, the comment on #1025 posted 05:10 UTC, winb section: k_c 87 at D 19, both roots)

1. **Step 1, regrid:** pin my k_c 79 D 19 state (the one of `kc79_d19low` and `kc79_d19gap`) and dh610's `kc87_syscheck_1025.py` (blob 6df5d960, raw ec9fb489:I1025-dh610/kc87_d195/in/). `kc79_syscheck_1025.py` accepts the source (both controls exit 1) and the k_c 87 check refuses it. Then
   `ell_refine.py l1kc79W19m1025 79 l1kc87wind19 87 1 19.0 <lam0_at(19.0) from ell_delta> --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`. Accept only by `kc87_syscheck_1025.py` (selftest 0, `--mutate=F` and `--mutate=steps` exit 1), with the k_c 79 check refusing the result.
2. **Step 2, scan, after ACCEPTED:** `d18_hybsign.py` at 1.380 to 1.580 by 0.025 (9 values) plus a repeat of 1.480, then `read_lower.py` with its selftest and both mutations.
3. Below-normal priority, the headless conhost and the keep-awake helper for each run's duration, as in the gap scan. Memory: alerts only (no guard that kills).
4. **Written before the run (t5):** lambda_1 at k_c 87 lies within 0.003 of 1.5397 (the build offset is about 0.003; this is my own build at both k_c). The lower root lies above 1.411, or is gone from the window.
5. Report: Delta beside k_c 79's at D 19; every robust change by position, beside 1.410862 and 1.5397. Post on #1025 and send t5 the verdict. t5's estimate: regrid 2 to 4 h on this laptop, scan 10 points at about 1650 s, about 4.6 h.

## What the regrid takes from the k_c 79 run

| item | value |
|---|---|
| source state | `../kc79_d19/sol_l1kc79W19m1025_D19.0000.npy`, blob 3a3b1999 (also the worktree's `solver/matter/data/` copy, same blob) |
| source record | `../kc79_d19/l1kc79W19m1025.jsonl` (blob 9e197e49, local CRLF form): |F| 2.8482007333e-10, 2976 steps, constraint 7.2755e-4, Delta 1.0677704363070795, Ks 30, u0 0.04, kappa 0.7 |
| accepted marker | `../kc79_d19/regrid_accepted.txt` (06aff278): ACCEPTED 2026-11-22 12:53:51 UTC |
| lambda_0 | `ell_delta.lam0_at(19.0, *lam0_table())` printed `(2.115637844554127, 4.027366928838205e-08)`; used as `2.1156378446`, the value of the k_c 71 to 79 regrid at D 19; unused with `--no-gamma` |
| worktree | `choptuik-i1025k79` at 48c36355 (solver code 505d8399; `ell_delta.py` and `ell_refine.py` 48c36355; `ell_refine.py` blob 631e5801) |
| k_c 79 numbers to compare | wall 5595 s, cpu 9425 s, peak private 2.48 GB (the D 19 regrid, 4 threads, this laptop); roots at D 19: lower 1.410862, lambda_1 1.539658 |
| k_c 71 numbers (for the scan) | roots at D 19: lower 1.296338 (+ to -, dh610 172112d0), lambda_1 1.536547 |

## The checks (dh610's, inputs copied from raw ec9fb489:I1025-dh610/kc87_d195/in/, pins in `prep_kc87d19_pins_1025.txt`)

`kc79_syscheck_1025.py` (29dce7ea) and `kc87_syscheck_1025.py` (6df5d960) differ only in the k_c they require (79 or 87). Each accepts a record only if |F| is at most 1e-9, the record is that k_c at the given D, the state's |F| agrees with the record's within 1 % and `freeze_from` reproduces the record's step count, and its two controls (|F| x 1.5, steps + 1) are refused on the same numbers. `--mutate=F` and `--mutate=steps` apply them to the record itself and must exit 1; `--selftest` runs planted cases.

The driver (`kc87d19_regrid_driver_1025.py`) does, in this order, and stops with an hc to t5 at the first failure:

1. the pins (the inputs, the source files, the worktree and its copies of the source state and record);
2. the selftest of both checks (exit 0 each);
3. the source: the k_c 79 check exit 0 and its `--mutate=F` and `--mutate=steps` exit 1; the k_c 87 check exit 1 (it refuses the source); outputs `source_kc79_syscheck*.txt`, `source_kc87_syscheck.txt`;
4. the regrid (one process, 4 threads, BelowNormal, cap 21600 s by the exact pid);
5. the verdict: ACCEPTED only if the k_c 87 check exits 0 on the result, its selftest exits 0, `--mutate=F` and `--mutate=steps` exit 1, and the k_c 79 check exits 1 on the result (it refuses it); outputs `syscheck.txt`, `syscheck_mutate.txt`, `syscheck_kc79_on_result.txt`, `selftest_kc87_syscheck_after.txt`.

`regrid_accepted.txt` is written from the driver's own python process, with the state and record blobs in it (win2's D 20 run wrote an empty marker once because its last step got MSYS paths). The scan driver refuses unless the marker has the form `ACCEPTED <date> <time> UTC / state <blob> / record <blob>` and the state and record in this folder have those blobs.

## The scan (starts by itself after ACCEPTED)

| item | value |
|---|---|
| window | 1.380, 1.405, 1.430, 1.455, 1.480, 1.505, 1.530, 1.555, 1.580, then the repeat 1.480 (10 points, in this order) |
| scanner | `d18_hybsign.py` (xfkappa, raw `I1025-mac/d18`, blob e089207a, unchanged): float64 blocks 0-11 plus a dd block 12, the 1e-15 noise test on blocks 0-11 with 2 seeds, the float64 sign beside it |
| reader | `read_lower.py` (dh170, raw `I1025-dh170/lower_root`, blob 89309d3c; imports `d185_scan_read.py`, blob 7c9d400f), `read_lower.py . 1.38 1.58`, after its selftest and its two `--mutate` controls (0, 1, 1) |
| process | one, 4 BLAS threads, BelowNormal, cap 36000 s (10 h) by the exact pid |

`go_kc87d19_1025.cmd` runs the regrid driver and, only if `regrid_accepted.txt exists`, the scan driver, in one headless console. Each driver starts its own sampler (a line every 60 s), alert-only memory watcher (free physical memory every 15 s, one hc alert to t5 below 1 GB, at most every 30 min, kills nothing) and keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` until that driver's pid is gone, power plan untouched, kills nothing). The scan file is `scan_kc87_D19_p0.jsonl`. The reader's lines go to t5 as printed.

Dry tests (`selftest_scan_dry_1025.txt`, `selftest_*_syscheck.txt.dry`, `kc87_regrid_w.log.dry`): the regrid driver's pins and both selftests pass (exit 0, nothing started); the scan driver runs its checks on a fake stand-in marker, state and record (the k_c 79 files renamed) and reaches "would start" (exit 0), refuses a marker with a wrong blob, refuses a missing marker, and refuses seven bad windows (exit 2). The real marker, state and record exist only after the regrid.

## Cost, written before the run

| item | estimate | basis |
|---|---|---|
| source checks | about 10 to 20 min | four runs of a check that re-freezes the state (the D 19 regrid's k_c 71 control took minutes) |
| regrid | about 2 to 2.5 h wall (t5: 2 to 4 h), peak private about 2.9 GB | k_c 79 at D 19 took 5595 s, 2.48 GB; win2's k_c 87 at D 20 took 6960 s against 5273 s for its k_c 79 (x 1.32) |
| scan | 10 points at 1500 to 2200 s: 4.2 to 6.1 h (t5: 4.6 h), peak private about 3 GB | k_c 79 at D 19: 1204 to 1695 s per point; k_c 87 is larger |
| together | ends about 12:00 to 14:30 UTC on 2026-11-23, most likely about 13:00 | start about 05:25 UTC |

The sampler (`rows/regrid_samples.csv`, `rows/scan_samples.csv`) gives the real figures. Another project's jobs (I114, earlier I129) share the laptop. I record the clock speed and power state at each start.

## Files made here

`make_kc87d19_1025.py` writes `kc87d19_regrid_driver_1025.py`, `kc87d19_scan_driver_1025.py`, `kc87d19_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `go_kc87d19_1025.cmd` and `publish_kc87d19_1025.sh`. The scan driver, watcher, keep-awake helper, session check and publish script are derived from the k_c 79 gap-scan ones (`diff_scan_driver_vs_gap.txt`, `diff_watcher_vs_gap.txt`) by asserted replacements; the regrid driver is a new text on the k_c 79 D 19 regrid driver's helpers (`diff_regrid_driver_vs_d19.txt`, large because the checks are new). The sampler is an unchanged copy.

## Run

Started outside my terminal: `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc87d19_1025.cmd`.

## Status

**Step 1 running since 2026-11-23 05:11:06 UTC** (the chain started through `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc87d19_1025.cmd`). README first: c83d0fbd (pushed before the start).

- **Chain** (`rows/launcher_pid_regrid.txt`: 10344): conhost --headless 10344 <- cmd 24168 <- regrid driver launcher 23684 and driver 14860 <- sampler 6216, alert-only watcher 25260, keep-awake helper 13972 (interpreter 25876), and the checks and the regrid below it. The python and powershell processes are BelowNormal.
- **Session check** (`session_check_regrid.txt`, exit 0, taken while the source checks ran): no `claude` in any chain, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain, every chain ends wininit.
- **Before the checks:** the pins matched, the selftests of both checks exited 0 (`selftest_kc87_syscheck.txt`, `selftest_kc79_syscheck.txt`).
- **Keep-awake:** helper 25876 set `SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` at 05:11:07 UTC (returned 0x80000000) and holds it until the regrid driver pid 14860 ends (`rows/regrid_keepawake.log`); the scan driver starts its own.
- **Machine at the start:** on AC (battery status 2, charge 100 %), clock 2995 MHz of 2995 MHz max, free physical memory 23.9 GB; beside it the other project's I114 job (`convergence.py 5`, two python processes, started 04:02 UTC; the I129 pair of the gap scan is gone). Not touched.
- **ETA** (estimates above): the source checks finish about 05:30, the regrid about 07:40 UTC (range 07:15 to 08:15), the scan about 12:00 to 14:30 UTC (most likely about 13:00).

Pushed 2026-11-23 05:11:38 UTC.

## Result

Not yet run.
