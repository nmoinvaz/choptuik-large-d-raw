# I1025-win/kc71_d21375: lambda_1 at k_c 71 on leg 6's D 21.375 state, a hybrid sign scan at 0.765 to 0.795 (winb)

Written before the run, 2026-11-24 06:32:56 UTC (the time of the README-first push, 79c0e5fc4; later pushes keep it). No scan had been run for this folder when the order, the written lines and the estimates below were written. The dry test ran the pins, the `read_lower.py` selftests and the state check (read-only, 2 s each, outputs `*.txt.dry`); the real run repeats them first.

## Order (t5's hc of 2026-11-24 ~05:35 UTC, winb section; the D 21.3125 reading, 0.800114, is in `I1025-win/kc71_d213125` and #1025 comment 7123098606)

lambda_1 at k_c 71 on leg 6's D 21.375 state: win2's raw `I1025-win2/kc71_leap` (pushed 2026-11-24 06:29:35 UTC), tag `l1kc71Lw1025e`, commit 9af2e828, state blob 52f92e3b, record blob 6948a267, pinned by blob; `kc71_syscheck.py` accepts it, its controls exit 1. `d18_hybsign.py` at 0.765 to 0.795 by 0.005 (7 points) plus a repeat of 0.780, then `read_lower.py`. 4 processes, BelowNormal, raw `I1025-win/kc71_d21375/`, README first. Report the reading.

## Written before the run (t5's)

**One change within 0.01 of 0.779**, where 0.779 is my D 21.3125 reading 0.8001 minus 0.34 x 0.0625 (one leg step on, D 21.375 - 21.3125 = 0.0625; my readings 0.821699 at D 21.25 and 0.800114 at D 21.3125 give a slope of -0.3454). By position: the det-linear estimate of the one robust change that `read_lower.py` prints lies in [0.769, 0.789]. I check exactly that and print the reader's lines as they come; t5 rules. Not met by position if the reader prints no robust change, two or more, or one outside [0.769, 0.789]. The window ends (0.765, 0.795) are the only evaluated edges; below 0.765 and above 0.795 are not evaluated.

## The source (win2's, not mine)

| item | value |
|---|---|
| raw folder, commit | `I1025-win2/kc71_leap`, 9af2e828 ("leg 6 state D 21.375 (tag l1kc71Lw1025e)") |
| state | `states/sol_l1kc71Lw1025e_D21.375000.npy`, blob 52f92e3b (37368 bytes) |
| record | `states/l1kc71Lw1025e.jsonl`, blob 6948a267; the D 21.375 row: k_c 71, \|F\| 4.3390486020270884e-10, F_start 1.0197718386327924e-05, steps 2378, constraint 9.286976645150187e-03, Delta 1.12840586196258, Ks 30, u0 0.04, kappa 0.7, 2832 s |
| check | `kc71_syscheck.py`, blob 4cd86cd4 (win2's, at 9af2e828) |
| scanner, reader | `d18_hybsign.py` e089207a, `d185_scan_read.py` 7c9d400f, `read_lower.py` 89309d3c, the same blobs as my k_c 71 D 21.125, D 21.25 and D 21.3125 and k_c 95 D 19 scans |
| code | the worktree `choptuik-i1025k79` at 48c36355 (the solver code the k_c 79, 87, 95 and 71 D 21.125, D 21.25 and D 21.3125 runs used) |

The copies are in `inputs/` (not published; each is pinned by blob in `prep_kc71d21375_pins_1025.txt`).

## The checks, before the scan (the driver stops and hc's t5 if any is not as written)

| check | wanted |
|---|---|
| pins: the six blobs above, the worktree at 48c36355, no scan file yet | all match |
| `read_lower.py selftest`, `--mutate=shift`, `--mutate=round2` | exit 0, 1, 1 |
| `kc71_syscheck.py --selftest` | exit 0 |
| `kc71_syscheck.py REC STATE 21.375 WTM` | exit 0: "ACCEPTED: the record class's \|F\| with a step count that comes back" (dry test: state \|F\| 4.3409965177e-10 against the record's 4.3390486020e-10, `freeze_from` 2378 steps) |
| the same with `--mutate=F`, `--mutate=steps` | exit 1, 1 (the controls) |
| `d18_hybsign.py` itself, at its start | prints "the record system" (exit 3 and no scan if not) |

## The scan

`d18_hybsign.py` (the hybrid sign: float64 blocks 0 to 11 and a dd block 12, the 1e-15 noise test with 2 seeds, the float64 sign beside it) at D 21.375, in four processes, one share each (one thread each, BelowNormal; `P4_WT_MATTER` the worktree's `solver/matter`; each appends one JSON line per lambda to its own file):

| process | file | lambdas, in this order |
|---|---|---|
| p0 | `scan_kc71_D21375_p0.jsonl` | 0.765, 0.780 (the repeat) |
| p1 | `scan_kc71_D21375_p1.jsonl` | 0.770, 0.785 |
| p2 | `scan_kc71_D21375_p2.jsonl` | 0.775, 0.790 |
| p3 | `scan_kc71_D21375_p3.jsonl` | 0.780, 0.795 |

8 evaluations: 7 distinct points 0.765 to 0.795 by 0.005 and the repeat of 0.780 (p3's is the scan point, p0's the repeat, in another process). Cap 10800 s (3 h) by the exact pids. Then `read_lower.py . 0.765 0.795` (`D18_DIR` the inputs; it reads every `scan_*_p*.jsonl` of the folder, three-decimal keys, prints a robust change between adjacent points whatever the spacing). The driver hc's t5 every line it printed. A memory watcher (alert-only, its own process, kills nothing), a sampler (every 60 s) and a keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)`, power plan untouched) run beside it. The other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.

## Cost, written before the run

| item | estimate | basis |
|---|---|---|
| state check | 10 s | the D 21.3125 run: 6 s with the pins |
| each point | about 1300 to 1700 s with four processes at one thread on four cores | my D 21.125 points took 1624 to 1681 s (laptop CPU 81 %), my D 21.25 points 1476 to 1503 s (CPU 70 %) and my D 21.3125 points 1372 to 1508 s (CPU 69 %) in the same setup, the first points of each process 1372 to 1376 s and the second 1503 to 1508 s; D 21.375 has a slightly larger grid, and the other project's I114 jobs move the figure |
| the scan | 2 points per process: about 45 to 57 min | 2 x the range above plus the start |
| peak private | about 1.9 GB per worker, about 7.6 GB for the four | D 21.125, D 21.25 and D 21.3125: 1.81 to 1.82 GB per worker; free memory at the start about 23 GB |

The sampler (`rows/scan_samples.csv`) gives the real figures.

## Files made here

`kc71d21375_scan_driver_1025.py` (derived by hand from my k_c 71 D 21.3125 scan driver: the D, the pins and the window changed), `kc71d21375_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `sample_driver4_1025.ps1` (copies of the D 21.3125 ones with the folder name changed), `go_kc71d21375_1025.cmd`, `publish_kc71d21375_1025.sh`, `prep_kc71d21375_pins_1025.txt`, `selftest_scan_dry_1025.txt`.

## Run

Started outside my terminal: `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc71d21375_1025.cmd`.

## Status

**Finished 2026-11-24 07:22:47 UTC** (the driver's last line; the scan itself 06:33:21 to 07:21:36 UTC, 2895 s, exits 0, 0, 0, 0, reader exit 0). Started 2026-11-24 06:33:14 UTC (started through `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc71d21375_1025.cmd`; the scan processes started 06:33:21). README first: 79c0e5fc4 (pushed 06:32:56 UTC, before the start). win2 pushed the D 21.375 state at 06:29:35 UTC (commit 9af2e828); the dry test ran at 06:32:25.

- **Chain** (`rows/launcher_pid.txt`: 26360): conhost --headless 26360 <- cmd 7332 <- scan driver launcher 24164 and driver 26384 <- sampler 22392, alert-only watcher 10948, keep-awake helper 23940, and the four `d18_hybsign.py` processes p0 25924, p1 15732, p2 24972, p3 1160 (each with a worker 25864, 4500, 25544, 24800). All BelowNormal.
- **Session check** (`session_check_scan.txt`, exit 0): no `claude` in any chain, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain.
- **Before the scan** (06:33:14 to 06:33:21 UTC, 7 s): the pins matched; `read_lower.py` selftest 0 and its two controls 1, 1; `kc71_syscheck.py` selftest 0; the state accepted (exit 0; state |F| 4.3409965177e-10 against the record's 4.3390486020e-10, `freeze_from` 2378 steps, the record's); `--mutate=F` and `--mutate=steps` exit 1, 1 (`source_syscheck_*.txt`). All four `d18_hybsign.py` print "the record system".
- **Machine at the start:** free physical memory 23.40 GB, commit 10.74 GB, laptop CPU 73 % (the other project's I114 `convergence.py` jobs beside the scan, not touched). Checked after the run (07:22 UTC): battery status 2, charge 100, clock 2995 of 2995 MHz.
- **Machine over the run:** sampler (`rows/scan_samples.csv`, 49 stamps, 06:33:23 to 07:22:28) gap at most 63 s; memory watcher (alert-only): 0 alerts (sampler: lowest free 19.81 GB); laptop CPU 70 % mean, 88 % max; peak private per worker 1.811 GB (four workers, about 7.2 GB); keep-awake helper held 2985 s and cleared (`rows/scan_keepawake.log`); System log 06:30 to 07:23 UTC: no event from the Kernel-Power, Power-Troubleshooter, Kernel-Boot, Kernel-General or Kernel-Processor-Power providers; no standby. The other project's jobs were not touched.

Pushed 2026-11-24 07:23:41 UTC.

## Result

The reader's lines are in `read_lower_kc71_D21375.log` (exit 0) and `scan_kc71_D21375.log`, as printed:

```
points 7 in 0.765-0.795; not noise-robust: none
hybrid signs: 0.765- 0.770- 0.775- 0.780+ 0.785+ 0.790+ 0.795+
float64 sign differs from the hybrid sign at: none
repeated points: [(0.78, 'agree')]
  robust change (0.775, 0.780), - to +, det-linear 0.778223, range [0.777696, 0.778223]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: - at 0.765, + at 0.795
```

**One robust change, in (0.775, 0.780), `-` to `+`, det-linear 0.778223.** The window's ends are `-` at 0.765 and `+` at 0.795.

| lambda | process | hybrid sign | hybrid ln\|det\| | noise seeds | float64 sign | float64 ln\|det\| | wall s |
|---|---|---|---|---|---|---|---|
| 0.765 | p0 | - | -1964.857714 | -, - | - | -1964.490783 | 1401 |
| 0.770 | p1 | - | -1965.685254 | -, - | - | -1965.088353 | 1400 |
| 0.775 | p2 | - | -1967.037625 | -, - | - | -1965.764433 | 1408 |
| 0.780 | p3 | + | -1967.632995 | +, + | + | -1967.984343 | 1401 |
| 0.780 (repeat) | p0 | + | -1967.632995 | +, + | + | -1967.984343 | 1476 |
| 0.785 | p1 | + | -1966.773113 | +, + | + | -1967.072256 | 1470 |
| 0.790 | p2 | + | -1966.578235 | +, + | + | -1970.564524 | 1473 |
| 0.795 | p3 | + | -1966.568177 | +, + | + | -1969.370711 | 1479 |

The repeat of 0.780 (p0, another process) agrees with p3's to every digit printed. All 8 evaluations are noise-robust. The float64 sign equals the hybrid sign at every point (as at D 21.25; at D 21.3125 it differed at 0.805 and 0.810, at D 21.125 at 0.860 and 0.865).

The change lies 0.001777 below the grid point 0.780 (det-linear range [0.777696, 0.778223]). The hybrid ln|det| at 0.780 is -1967.633, which is 0.595 below its value at 0.775 and 0.860 below its value at 0.785 (a shallower dip than at D 21.3125, where the values were 4.46 and 3.76 below).

### Against the line written before (t5's)

| line | observed | |
|---|---|---|
| one robust change; its det-linear estimate in [0.769, 0.789] (0.779 within 0.01) | one robust change, det-linear 0.778223 (range [0.777696, 0.778223]), 0.000777 below 0.779 | met by position |
| not met if none, two or more, or one outside | none of those | not triggered |

By position only; t5 rules. Beside my k_c 71 readings: 0.800114 at D 21.3125 (`I1025-win/kc71_d213125`) gives a move of -0.021891 in 0.0625 of D, a slope of -0.3503 per unit D (the written trend used -0.34). From D 21.25 (0.821699): -0.043476 in 0.125 of D, -0.3478 per unit D. From D 21.125 (0.862215): -0.083992 in 0.25 of D, -0.3360 per unit D. The slopes between consecutive readings read -0.3241 (D 21.125 to 21.25), -0.3454 (to 21.3125) and -0.3503 (to 21.375).

Not evaluated: below 0.765, above 0.795. A change outside the window is not excluded; the two edge signs `-` and `+` differ, as one change needs. All 7 points are noise-robust, so a second change between two scanned points would show in the signs, and none does. Pairs of changes inside one 0.005 step are not excluded.

### Cost against the estimates written before

| item | written | observed |
|---|---|---|
| state check | 10 s | 7 s (06:33:14 to 06:33:21) |
| each point | 1300 to 1700 s | 1400 to 1408 s for the first point of each process, 1470 to 1479 s for the second (inside) |
| the scan | 45 to 57 min | 2895 s (48.3 min; inside) |
| end of the scan | 07:18 to 07:30 UTC | 07:21:36 UTC (inside) |
| peak private | about 1.9 GB per worker, about 7.6 GB | 1.811 GB per worker, about 7.2 GB |

The laptop CPU averaged 70 % (D 21.3125: 69 %; D 21.25: 70 %; D 21.125: 81 %), with the other project's I114 jobs beside the scan each time.
