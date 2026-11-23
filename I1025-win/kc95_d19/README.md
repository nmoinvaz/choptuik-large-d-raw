# I1025-win/kc95_d19: k_c 95 at D 19, regridded from my accepted k_c 87 D 19 state, then a scan of both roots' windows (winb)

Written before the run, 2026-11-23 12:41:47 UTC (substituted from `date -u` when pushed; nothing had been run for this folder when the order, the predictions and the estimates below were written; the Status and Result sections are added after the runs).

Runner: the winb session (surface-laptop-4, 4 cores, 8 threads, 32 GB), the same one that ran `../kc79_d19/`, `../kc79_d19low/` (raw 40f1a01a), `../kc79_d19gap/` (raw fee69df5) and `../kc87_d19/` (raw 3b833805: the k_c 87 regrid and scan this run starts from). The coordinator is t5.

## Order (t5's hc of 2026-11-23, the comment on #1025 of 12:45 UTC, winb section: k_c 95 at D 19)

t5's reading of `../kc87_d19/`: the D 19 roots by position are lambda_1 1.5380 / 1.5365 / 1.5397 / 1.5390 and the lower root 1.4832 / 1.2963 / 1.4109 / 1.4145 at k_c 63 / 71 / 79 / 87; the lower root moved 0.115 between k_c 71 and 79 and 0.0037 between 79 and 87, "convergence, not a root that drifts with k_c". t5 withdrew the ruling that D 19's lower roots are discretization roots; they are `unidentified` until k_c 95 decides.

1. **Step 1, regrid:** my accepted k_c 87 D 19 state (`../kc87_d19/sol_l1kc87wind19_D19.0000.npy`, blob 100f63f7, record 4fae1621) to k_c 95. `kc87_syscheck_1025.py` (6df5d960) accepts the source (both controls exit 1) and dh610's `kc95_syscheck_1025.py` refuses it. Then
   `ell_refine.py l1kc87wind19 87 l1kc95wind19 95 1 19.0 2.1156378446 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, accepted by the k_c 95 check (selftest 0, `--mutate=F` and `--mutate=steps` exit 1), and the k_c 87 check must refuse the result.
2. **Step 2, scan, after ACCEPTED:** `d18_hybsign.py` at 1.395 to 1.435 by 0.005 (9 values), 1.530 to 1.550 by 0.005 (5 values) and a repeat of 1.415 (15 evaluations), then `read_lower.py` (with its selftest and both mutations).
3. Below-normal priority, the headless conhost and the keep-awake helper for each run's duration, one process, 4 threads. Memory: alerts only (no guard that kills).
4. **Written before the run (t5):** the lower root within 0.002 of 1.4145 means it converges (a second root to establish); moving more than 0.004 means a discretization root; lambda_1 stays within 0.002 of 1.539.
5. Report: Delta beside k_c 87's at D 19; every robust change by position, beside 1.414532 and 1.538986 (k_c 87) and 1.410862 and 1.539658 (k_c 79). Post on #1025 and send t5 the verdict.

## What the regrid takes from the k_c 87 run

| item | value |
|---|---|
| source state | `../kc87_d19/sol_l1kc87wind19_D19.0000.npy`, blob 100f63f7 (also the worktree's `solver/matter/data/` copy, same blob) |
| source record | `../kc87_d19/l1kc87wind19.jsonl` (blob 4fae1621): \|F\| 2.9006474406e-10, 3276 steps, constraint 3.9191e-4, Delta 1.0677698834525378, Ks 30, u0 0.04, kappa 0.7, seconds 7960 |
| accepted marker | `../kc87_d19/regrid_accepted.txt` (3d801469): ACCEPTED 2026-11-23 07:24:14 UTC |
| lambda_0 | `ell_delta.lam0_at(19.0, *lam0_table())` = (2.115637844554127, 4.027366928838205e-08), used as `2.1156378446` (t5's value; unused with `--no-gamma`) |
| worktree | `choptuik-i1025k79` at 48c36355 (solver code 505d8399; `ell_delta.py` and `ell_refine.py` 48c36355; `ell_refine.py` blob 631e5801), the one of every earlier regrid here |
| k_c 87 numbers to compare | wall 7965 s, cpu 13782 s, peak private 2.94 GB (the D 19 regrid, 4 threads, this laptop); roots at D 19: lower 1.414532 (- to +), lambda_1 1.538986 (+ to -); scan points 1834 to 1863 s |
| k_c 79 numbers | wall 5595 s, cpu 9425 s, peak private 2.48 GB; roots 1.410862 (- to +), 1.539658 (+ to -); scan points 1204 to 1695 s |
| dh610's k_c 95 at D 19.5 (information) | regrid wall 4293 s on 8 threads of a 20-thread machine; its lower root there 1.398815 |

## The checks (dh610's, inputs in `inputs/`, pins in `prep_kc95d19_pins_1025.txt`)

`kc87_syscheck_1025.py` (6df5d960, raw ec9fb489:I1025-dh610/kc87_d195/in/, the check that accepted my k_c 87 regrid) and `kc95_syscheck_1025.py` (d487e628, raw I1025-dh610/kc95_d195/in/, the version dh610 used at D 19.5) differ only in the k_c they require: three changed lines (the k_c test, its message and the selftest's planted record), `kc95_syscheck_1025_dh610.diff`; the diff of the two files here equals dh610's diff (cmp, three lines changed). Each accepts a record only if |F| is at most 1e-9, the record is that k_c at the given D, the state's |F| agrees with the record's within 1 % and `freeze_from` reproduces the record's step count; its two controls (|F| x 1.5, steps + 1) are refused. `--mutate=F` and `--mutate=steps` apply them to the record itself and must exit 1; `--selftest` runs planted cases.

The driver (`kc95d19_regrid_driver_1025.py`) does, in this order, and stops with an hc to t5 at the first failure:

1. the pins (the inputs, the source files, the worktree and its copies of the source state and record);
2. the selftest of both checks (exit 0 each);
3. the source: the k_c 87 check exit 0 and its `--mutate=F` and `--mutate=steps` exit 1; the k_c 95 check exit 1 (it refuses the source); outputs `source_kc87_syscheck*.txt`, `source_kc95_syscheck.txt`;
4. the regrid (one process, 4 threads, BelowNormal, cap 21600 s by the exact pid);
5. the verdict: ACCEPTED only if the k_c 95 check exits 0 on the result, its selftest exits 0, `--mutate=F` and `--mutate=steps` exit 1, and the k_c 87 check exits 1 on the result (it refuses it); outputs `syscheck.txt`, `syscheck_mutate.txt`, `syscheck_kc87_on_result.txt`, `selftest_kc95_syscheck_after.txt`.

`regrid_accepted.txt` is written from the driver's own python process, with the state and record blobs in it; the scan driver refuses unless the marker has the form `ACCEPTED <date> <time> UTC / state <blob> / record <blob>` and the state and record in this folder have those blobs.

## The scan (starts by itself after ACCEPTED)

| item | value |
|---|---|
| window | 1.395, 1.400, 1.405, 1.410, 1.415, 1.420, 1.425, 1.430, 1.435, then 1.530, 1.535, 1.540, 1.545, 1.550, then the repeat 1.415 (15 evaluations, in this order) |
| not scanned | (1.435, 1.530): nothing there is evaluated, and a change below 1.395 or above 1.550 shows only as an endpoint sign. `read_lower.py` gets `1.395 1.55` and prints a robust change between 1.435 and 1.530 if the two signs differ (it would be a change of unknown position in that gap) |
| scanner | `d18_hybsign.py` (xfkappa, raw `I1025-mac/d18`, blob e089207a, unchanged): float64 blocks 0-11 plus a dd block 12, the 1e-15 noise test on blocks 0-11 with 2 seeds, the float64 sign beside it |
| reader | `read_lower.py` (dh170, raw `I1025-dh170/lower_root`, blob 89309d3c; imports `d185_scan_read.py`, blob 7c9d400f), `read_lower.py . 1.395 1.55`, after its selftest and its two `--mutate` controls (0, 1, 1) |
| process | one, 4 BLAS threads, BelowNormal, cap 64800 s (18 h) by the exact pid |

`go_kc95d19_1025.cmd` runs the regrid driver and, only if `regrid_accepted.txt exists`, the scan driver, in one headless console. Each driver starts its own sampler (a line every 60 s), alert-only memory watcher (free physical memory every 15 s, one hc alert to t5 below 1 GB, at most every 30 min, kills nothing) and keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` until that driver's pid is gone, power plan untouched, kills nothing). The scan file is `scan_kc95_D19_p0.jsonl`. The reader's lines go to t5 as printed.

Dry tests (`selftest_scan_dry_1025.txt`, `selftest_*_syscheck.txt.dry`, `kc95_regrid_w.log.dry`): the regrid driver's pins and both selftests pass (exit 0, nothing started); the scan driver runs its checks on a fake stand-in marker, state and record (the k_c 87 files renamed to the k_c 95 tag) and reaches "would start" (exit 0), refuses a marker with a wrong blob, refuses a missing marker, and refuses seven bad windows (exit 2). The real marker, state and record exist only after the regrid.

## Cost, written before the run

| item | estimate | basis |
|---|---|---|
| source checks | about 10 s to a few minutes | the k_c 87 source checks took 10 s |
| regrid | about 2.7 to 3.5 h wall, peak private about 3.2 GB | k_c 79 took 5595 s (2.48 GB), k_c 87 took 7965 s (2.94 GB, x 1.42); x 1.2 to 1.5 on 7965 s is 9500 to 12000 s |
| scan | 15 points at 1850 to 2600 s: 7.7 to 10.8 h, peak private about 3.3 GB | k_c 87: 1834 to 1863 s per point (peak private 2.96 GB); k_c 79: 1204 to 1695 s; k_c 95 is larger |
| together | ends about 23:30 UTC on 2026-11-23 to 03:30 UTC on 2026-11-24, most likely about 01:00 UTC | start about 12:50 UTC |

The sampler (`rows/regrid_samples.csv`, `rows/scan_samples.csv`) gives the real figures. Another project's jobs (the negative-mass I114 `convergence.py` runs) share the laptop and are not touched. I record the clock speed and power state at each start.

## Files made here

`make_kc95d19_1025.py` writes `kc95d19_regrid_driver_1025.py`, `kc95d19_scan_driver_1025.py`, `kc95d19_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `go_kc95d19_1025.cmd` and `publish_kc95d19_1025.sh` from the k_c 87 D 19 ones (raw `I1025-win/kc87_d19` at 3b833805) by a fixed mapping (the source k_c 79 becomes 87, the target 87 becomes 95) plus asserted explicit text (the pins, the docstrings, the window, the scan cap 64800 s for 15 evaluations). `diff_regrid_driver_vs_kc87d19.txt`, `diff_scan_driver_vs_kc87d19.txt` and `diff_watcher_vs_kc87d19.txt` are the diffs against the k_c 87 files. The sampler is an unchanged copy.

## Run

Started outside my terminal: `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc95d19_1025.cmd`.

## Status

**Step 1 running since 2026-11-23 12:41:11 UTC** (the chain started through `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc95d19_1025.cmd`). README first: a5ebee62 (pushed before the start).

- **Chain** (`rows/launcher_pid_regrid.txt`: 10264): conhost --headless 10264 <- cmd 1540 <- regrid driver launcher 2000 and driver 23384 <- sampler 20132, alert-only watcher 15320, keep-awake helper 10568 (interpreter 20172), and the checks and the regrid below it. The python and powershell processes are BelowNormal.
- **Session check** (`session_check_regrid.txt`, exit 0): no `claude` in any chain, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain, every chain ends wininit.
- **Before the regrid** (12:41:11 to 12:41:23 UTC): the pins matched; the selftests of both checks exited 0; the source checks were as ordered: the k_c 87 check exit 0 on the source, `--mutate=F` and `--mutate=steps` exit 1, the k_c 95 check exit 1 (it refuses the source; `source_kc*_syscheck*.txt`). 12 s in all.
- **Regrid:** pid 21772 started 12:41:23 UTC: `ell_refine.py l1kc87wind19 87 l1kc95wind19 95 1 19.0 2.1156378446 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, cwd the worktree's `solver/matter`, 4 threads, BelowNormal, cap 21600 s by the exact pid.
- **Keep-awake:** helper 10568 holds `SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` until the regrid driver 23384 ends (`rows/regrid_keepawake.log`); the scan driver starts its own.
- **Machine at the start:** on AC (battery status 2), clock 2995 MHz of 2995 MHz max, free physical memory 23.3 GB; beside it the other project's I114 `convergence.py` jobs (python 880 and 4940), not touched.
- **ETA** (estimates above): the regrid ends about 15:30 UTC (range 15:20 to 16:15), the scan about 01:00 UTC on 2026-11-24 (range 23:30 to 03:30).

Pushed 2026-11-23 12:41:47 UTC.

## Result

Not yet run.
