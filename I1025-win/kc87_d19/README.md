# I1025-win/kc87_d19: k_c 87 at D 19, regridded from my own k_c 79 D 19 state, then a scan (winb)

Written before the run, 2026-11-23 12:35:51 UTC (substituted from `date -u` when pushed; nothing had been run for this folder when the order and estimates below were written; the Status and Result sections were added after the runs).

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

**Both steps done.** Step 1 (regrid) ACCEPTED 2026-11-23 07:24:14 UTC; step 2 (scan) 07:25:25 to 12:34:10 UTC, exit 0, 18525 s; the chain's cmd ended 12:35:21 UTC (driver done). README first: c83d0fbd; start status 265b7c59; step 1 record 483d8d53.

- **Chain** (one headless conhost, `rows/launcher_pid_regrid.txt`: 10344 <- cmd 24168 <- regrid driver 14860, then scan driver 9840): scan driver 9840 <- sampler 21168, alert-only watcher 26144, keep-awake helper 24384 (interpreter 15764), scanner 13660 (venv launcher) and its worker 23816. Session check `session_check_scan.txt`: exit 0, no `claude` in any chain, no Windows Terminal / OpenConsole / wt, headless conhost yes, chains end wininit.
- **Keep-awake:** the regrid's helper held `SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` 05:11:07 to 07:25:37 UTC, the scan's 07:25:25 to 12:35:25 UTC (cleared with ES_CONTINUOUS when driver 9840 ended). No standby event 506/507; sampler gap at most 62 s over 305 stamps of the scan.
- **Machine:** AC, clock 2995 MHz of 2995 max; the other project's I114 job (`convergence.py 5`) beside the run, not touched.

Pushed 2026-11-23 12:35:51 UTC.

## Result

### Step 1: the regrid (ACCEPTED)

`ell_refine.py l1kc79W19m1025 79 l1kc87wind19 87 1 19.0 2.1156378446 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, cwd `choptuik-i1025k79/solver/matter` (48c36355), one process, 4 threads, BelowNormal, started through `conhost.exe --headless cmd.exe /c` outside my terminal.

| item | k_c 79 at D 19 (source) | k_c 87 at D 19 (result) |
|---|---|---|
| \|F\| | 2.8482007333e-10 | 2.9006474406e-10 |
| F_start | 8.701e-06 | 2.9922068e-06 |
| steps | 2976 | 3276 |
| constraint | 7.2755e-4 | 3.9191e-4 |
| Delta | 1.0677704363070795 | 1.0677698834525378 |
| wall s | 5595 | 7965 (record's seconds 7960) |
| cpu s | 9425 | 13782 |
| peak private GB | 2.48 | 2.94 |

**Delta(k_c 87) minus Delta(k_c 79) = -5.528545417021746e-07** at D 19 (relative -5.18e-7). Information, not compared: win2's D 20 pair differs by -2.97e-6.

Verdict (`regrid_summary.txt`, `syscheck*.txt`):

| check | wanted | got |
|---|---|---|
| source, k_c 79 check | exit 0 | 0 |
| source, k_c 79 check `--mutate=F`, `--mutate=steps` | 1, 1 | 1, 1 |
| source, k_c 87 check | exit 1 (refuses) | 1 ("the record is not k_c 87 at D 19 (kc 79, D 19.0)") |
| result, k_c 87 check | 0 | 0 ("ACCEPTED: the record class's \|F\| with a step count that comes back"; state \|F\| 2.9006474406e-10, `freeze_from` 3276 steps) |
| result, k_c 87 selftest (after) | 0 | 0 |
| result, `--mutate=F` / `--mutate=steps` | 1 / 1 | 1 / 1 (state \|F\| not within 1 % of 4.351e-10; 3276 against 3277) |
| result, k_c 79 check | 1 (refuses) | 1 ("the record is not k_c 79 at D 19 (kc 87, D 19)") |

Marker `regrid_accepted.txt` (written by the driver): `ACCEPTED 2026-11-23 07:24:14 UTC`, state blob 100f63f7, record blob 4fae1621 (the local files hash to those).

Memory: lowest free physical memory 21.25 to 21.48 GB, 0 alerts; peak working set 2.64 GB, peak commit 13.2 GB. Standby: none. Estimates before the run: 2 to 2.5 h (t5: 2 to 4 h); it took 2.21 h.

### Step 2: the scan

**k_c 87, D 19: two robust changes, 1.414532 (- to +, range [1.412419, 1.414532]) and 1.538986 (+ to -, range [1.538986, 1.539478]).** The repeat of 1.480 agrees. No point is noise-fragile, the float64 sign equals the hybrid sign at every point, no ln|det| minimum without a change, edge signs `-` at 1.380 and `-` at 1.580.

| lambda | hybrid sign | hybrid ln\|det\| | float64 sign | wall s |
|---|---|---|---|---|
| 1.380 | - | -2879.0652 | - | 1863 |
| 1.405 | - | -2880.8140 | - | 1859 |
| 1.430 | + | -2880.3298 | + | 1859 |
| 1.455 | + | -2879.8261 | + | 1860 |
| 1.480 | + | -2879.8434 | + | 1845 |
| 1.505 | + | -2880.2060 | + | 1834 |
| 1.530 | + | -2881.4048 | + | 1849 |
| 1.555 | - | -2880.8270 | - | 1846 |
| 1.580 | - | -2879.8580 | - | 1851 |
| 1.480 (repeat) | + | -2879.8434 | + | 1846 |

The repeat matches in every printed digit.

`read_lower.py` (89309d3c), as printed (`read_lower_kc87_D19.log`):

```
points 9 in 1.380-1.580; not noise-robust: none
hybrid signs: 1.380- 1.405- 1.430+ 1.455+ 1.480+ 1.505+ 1.530+ 1.555- 1.580-
float64 sign differs from the hybrid sign at: none
repeated points: [(1.48, 'agree')]
  robust change (1.405, 1.430), - to +, det-linear 1.414532, range [1.412419, 1.414532]
  robust change (1.530, 1.555), + to -, det-linear 1.538986, range [1.538986, 1.539478]
robust changes: 2; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: - at 1.380, - at 1.580
read_lower exit 0
```

Beside the other k_c at D 19 (information, by position; orientation as printed, not compared across k_c):

| k_c | lower root | lambda_1 |
|---|---|---|
| 63 | 1.483 | 1.537988 |
| 71 | 1.296338 (+ to -) | 1.536547 |
| 79 | 1.410862 (- to +) | 1.539658 (+ to -) |
| 87 | **1.414532** (- to +) | **1.538986** (+ to -) |

k_c 87 minus k_c 79: lower root +0.003670, lambda_1 -0.000672. Delta(k_c 87) minus Delta(k_c 79) = -5.528545e-07.

**Written before the run (t5), checked:**

| line | result |
|---|---|
| lambda_1 within 0.003 of 1.5397 | held: 1.538986 is 0.000714 below 1.5397 (the range reaches 1.539478) |
| the lower root above 1.411, or gone from the window | held: 1.414532 (range [1.412419, 1.414532]), not gone |

What ran: `d18_hybsign.py` (e089207a) on the k_c 87 D 19 state (record check passed: |F| 2.9006474406e-10, 3276 steps), one process, 4 threads, BelowNormal, started through `conhost.exe --headless cmd.exe /c` outside my terminal. Exit 0 after 18525 s (07:25:25 to 12:34:10 UTC); reader selftest and both `--mutate` controls 0, 1, 1 before the scan; reader exit 0. Scanner cpu 27169 s, peak private 2.96 GB, lowest free physical memory 21.46 GB, peak commit 13.14 GB, 0 memory alerts.

Cost against what I wrote before the run: 5.15 h (estimate 4.2 to 6.1 h; t5 4.6 h); points 1834 to 1863 s (estimate 1500 to 2200 s; k_c 79 at D 19: 1204 to 1695 s). The whole chain, regrid and scan, took 05:11:06 to 12:35:21 UTC, 7.4 h (estimate 12:00 to 14:30 UTC end; it ended earlier).

`read_lower.py` sees only this scan file's points, so a change just outside 1.380 to 1.580 shows only as an endpoint sign. These are k_c 87 roots, not yet physical.
