# I1025-win/kc71_d2125: lambda_1 at k_c 71 on leg 6's D 21.25 state, a hybrid sign scan at 0.810 to 0.840 (winb)

Written before the run, 2026-11-24 02:51:20 UTC (the time of the README-first push, a25e7d281; later pushes keep it). No scan had been run for this folder when the order, the written lines and the estimates below were written. The dry test ran the pins, the `read_lower.py` selftests and the state check (read-only, 2 s each, outputs `*.txt.dry`); the real run repeats them first.

## Order (t5's hc of 2026-11-24, winb section; the D 21.125 reading, 0.862215, is in `I1025-win/kc71_d21125` and #1025 comment 7120469474)

lambda_1 at k_c 71 on leg 6's D 21.25 state: win2's raw `I1025-win2/kc71_leap` (pushed 2026-11-24 02:49:27 UTC), tag `l1kc71Lw1025e`, commit a1de2690, state blob 49440f0c, record blob 4d6b4cc3, pinned by blob; `kc71_syscheck.py` accepts it, its controls exit 1. `d18_hybsign.py` at 0.810 to 0.840 by 0.005 (7 points) plus a repeat of 0.825, then `read_lower.py`. 4 processes, BelowNormal, raw `I1025-win/kc71_d2125/`, README first. Report the reading.

## Written before the run (t5's)

**One change within 0.01 of 0.827**, where 0.827 is the k_c 79 trend 0.9095 - 0.30 x 0.25 = 0.8345, shifted -0.0077 (dh170's calibration at D 21.0: k_c 71 minus k_c 79 = -0.0077). By position: the det-linear estimate of the one robust change that `read_lower.py` prints lies in [0.817, 0.837]. I check exactly that and print the reader's lines as they come; t5 rules. Not met by position if the reader prints no robust change, two or more, or one outside [0.817, 0.837]. The window ends (0.810, 0.840) are the only evaluated edges; below 0.810 and above 0.840 are not evaluated.

## The source (win2's, not mine)

| item | value |
|---|---|
| raw folder, commit | `I1025-win2/kc71_leap`, a1de2690 ("leg 6 state D 21.25 (tag l1kc71Lw1025e)") |
| state | `states/sol_l1kc71Lw1025e_D21.250000.npy`, blob 49440f0c (37368 bytes) |
| record | `states/l1kc71Lw1025e.jsonl`, blob 4d6b4cc3; the D 21.25 row: k_c 71, \|F\| 4.4883178731798743e-10, F_start 1.0250780421979243e-05, steps 2388, constraint 8.587038853667243e-03, Delta 1.1250206869744896, Ks 30, u0 0.04, kappa 0.7, 3320 s |
| check | `kc71_syscheck.py`, blob 4cd86cd4 (win2's, at a1de2690) |
| scanner, reader | `d18_hybsign.py` e089207a, `d185_scan_read.py` 7c9d400f, `read_lower.py` 89309d3c, the same blobs as my k_c 71 D 21.125 and k_c 95 D 19 scans |
| code | the worktree `choptuik-i1025k79` at 48c36355 (the solver code the k_c 79, 87, 95 and 71 D 21.125 runs used) |

The copies are in `inputs/` (not published; each is pinned by blob in `prep_kc71d2125_pins_1025.txt`).

## The checks, before the scan (the driver stops and hc's t5 if any is not as written)

| check | wanted |
|---|---|
| pins: the six blobs above, the worktree at 48c36355, no scan file yet | all match |
| `read_lower.py selftest`, `--mutate=shift`, `--mutate=round2` | exit 0, 1, 1 |
| `kc71_syscheck.py --selftest` | exit 0 |
| `kc71_syscheck.py REC STATE 21.25 WTM` | exit 0: "ACCEPTED: the record class's \|F\| with a step count that comes back" (dry test: state \|F\| 4.4902425293e-10 against the record's 4.4883178732e-10, `freeze_from` 2388 steps) |
| the same with `--mutate=F`, `--mutate=steps` | exit 1, 1 (the controls) |
| `d18_hybsign.py` itself, at its start | prints "the record system" (exit 3 and no scan if not) |

## The scan

`d18_hybsign.py` (the hybrid sign: float64 blocks 0 to 11 and a dd block 12, the 1e-15 noise test with 2 seeds, the float64 sign beside it) at D 21.25, in four processes, one share each (one thread each, BelowNormal; `P4_WT_MATTER` the worktree's `solver/matter`; each appends one JSON line per lambda to its own file):

| process | file | lambdas, in this order |
|---|---|---|
| p0 | `scan_kc71_D2125_p0.jsonl` | 0.810, 0.825 (the repeat) |
| p1 | `scan_kc71_D2125_p1.jsonl` | 0.815, 0.830 |
| p2 | `scan_kc71_D2125_p2.jsonl` | 0.820, 0.835 |
| p3 | `scan_kc71_D2125_p3.jsonl` | 0.825, 0.840 |

8 evaluations: 7 distinct points 0.810 to 0.840 by 0.005 and the repeat of 0.825 (p3's is the scan point, p0's the repeat, in another process). Cap 10800 s (3 h) by the exact pids. Then `read_lower.py . 0.810 0.840` (`D18_DIR` the inputs; it reads every `scan_*_p*.jsonl` of the folder, three-decimal keys, prints a robust change between adjacent points whatever the spacing). The driver hc's t5 every line it printed. A memory watcher (alert-only, its own process, kills nothing), a sampler (every 60 s) and a keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)`, power plan untouched) run beside it. The other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.

## Cost, written before the run

| item | estimate | basis |
|---|---|---|
| state check | 10 s | the D 21.125 run: 2 s each, four calls, 6 s with the pins |
| each point | about 1600 to 2000 s with four processes at one thread on four cores | my D 21.125 points took 1624 to 1681 s in the same setup (I had written 600 to 1500 s); D 21.25 has a slightly larger grid |
| the scan | 2 points per process: about 55 to 70 min | 2 x the range above plus the start |
| peak private | about 1.9 GB per worker, about 7.6 GB for the four | D 21.125: 1.81 to 1.82 GB per worker; free memory at the start about 23 GB |

The sampler (`rows/scan_samples.csv`) gives the real figures.

## Files made here

`kc71d2125_scan_driver_1025.py` (derived by hand from my k_c 71 D 21.125 scan driver: the D, the pins and the window changed), `kc71d2125_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `sample_driver4_1025.ps1` (copies of the D 21.125 ones with the folder name changed), `go_kc71d2125_1025.cmd`, `publish_kc71d2125_1025.sh`, `prep_kc71d2125_pins_1025.txt`, `selftest_scan_dry_1025.txt`.

## Run

Started outside my terminal: `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc71d2125_1025.cmd`.

## Status

**Finished 2026-11-24 03:42:55 UTC** (the driver's last line; the scan itself 02:51:44 to 03:41:44 UTC, 3000 s, exits 0, 0, 0, 0, reader exit 0). Started 2026-11-24 02:51:37 UTC (started through `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc71d2125_1025.cmd`; the scan processes started 02:51:44). README first: a25e7d281 (pushed 02:51:20 UTC, before the start). win2 pushed the D 21.25 state at 02:49:27 UTC (earlier than the ~03:00 t5 expected); the dry test ran at 02:50:43.

- **Chain** (`rows/launcher_pid.txt`: 24052): conhost --headless 24052 <- cmd 8228 <- scan driver launcher 25296 and driver 11716 <- sampler 17116, alert-only watcher 20776, keep-awake helper 16536, and the four `d18_hybsign.py` processes p0 21040, p1 8312, p2 9068, p3 22248 (each with a worker). All BelowNormal.
- **Session check** (`session_check_scan.txt`, exit 0): no `claude` in any chain, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain.
- **Before the scan** (02:51:37 to 02:51:44 UTC, 7 s): the pins matched; `read_lower.py` selftest 0 and its two controls 1, 1; `kc71_syscheck.py` selftest 0; the state accepted (exit 0; state |F| 4.4902425293e-10 against the record's 4.4883178732e-10, `freeze_from` 2388 steps, the record's); `--mutate=F` and `--mutate=steps` exit 1, 1 (`source_syscheck_*.txt`). All four `d18_hybsign.py` print "the record system".
- **Machine at the start:** on AC (battery status 2, charge 100), clock 2995 of 2995 MHz, free physical memory 23.4 GB, beside it the other project's I114 `convergence.py` jobs (python 17024, 9968, 880), not touched.
- **Machine over the run:** sampler (`rows/scan_samples.csv`, 51 stamps, 02:51:40 to 03:42:51) gap at most 63 s; memory watcher (alert-only): lowest free 18.84 GB, 0 alerts (sampler: 19.35 GB); laptop CPU 70 % mean, 86 % max; peak private per worker 1.81 to 1.82 GB (four workers, about 7.3 GB); keep-awake helper held 3090 s and cleared (`rows/scan_keepawake.log`); System log 02:45 to 03:50 UTC: no Kernel-Power event, only two Kernel-General id 1 events at 02:53:48 and 02:54:18 (clock writes of 0 ms, as before) and two id 24; no standby. The other project's I114 jobs were not touched.

Pushed 2026-11-24 03:45:48 UTC.

## Result

The reader's lines are in `read_lower_kc71_D2125.log` (exit 0) and `scan_kc71_D2125.log`, as printed:

```
points 7 in 0.810-0.840; not noise-robust: none
hybrid signs: 0.810- 0.815- 0.820- 0.825+ 0.830+ 0.835+ 0.840+
float64 sign differs from the hybrid sign at: none
repeated points: [(0.825, 'agree')]
  robust change (0.820, 0.825), - to +, det-linear 0.821699, range [0.821270, 0.821699]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: - at 0.810, + at 0.840
```

**One robust change, in (0.820, 0.825), `-` to `+`, det-linear 0.821699.** The window's ends are `-` at 0.810 and `+` at 0.840.

| lambda | process | hybrid sign | hybrid ln\|det\| | noise seeds | float64 sign | float64 ln\|det\| | wall s |
|---|---|---|---|---|---|---|---|
| 0.810 | p0 | - | -1978.862309 | -, - | - | -1978.720841 | 1482 |
| 0.815 | p1 | - | -1979.779622 | -, - | - | -1979.303739 | 1480 |
| 0.820 | p2 | - | -1981.667846 | -, - | - | -1980.455943 | 1482 |
| 0.825 | p3 | + | -1981.003460 | +, + | + | -1980.929934 | 1476 |
| 0.825 (repeat) | p0 | + | -1981.003460 | +, + | + | -1980.929934 | 1499 |
| 0.830 | p1 | + | -1980.478219 | +, + | + | -1981.448094 | 1499 |
| 0.835 | p2 | + | -1980.359125 | +, + | + | -1981.046314 | 1500 |
| 0.840 | p3 | + | -1980.384139 | +, + | + | -1980.262675 | 1503 |

The repeat of 0.825 (p0, another process) agrees with p3's to every digit printed. All 8 evaluations are noise-robust. The float64 sign equals the hybrid sign at every point (at D 21.125 it differed at 0.860 and 0.865).

### Against the line written before (t5's)

| line | observed | |
|---|---|---|
| one robust change; its det-linear estimate in [0.817, 0.837] (0.827 within 0.01) | one robust change, det-linear 0.821699 (range [0.821270, 0.821699]), 0.0053 below 0.827 | met by position |
| not met if none, two or more, or one outside | none of those | not triggered |

By position only; t5 rules. Beside the D 21.125 reading in `I1025-win/kc71_d21125` (0.862215, the same state family, same pipeline): the change moved by -0.040516 in 0.125 of D, a slope of -0.3241 per unit D (the written trend used -0.30).

Not evaluated: below 0.810, above 0.840. A change outside the window is not excluded; the two edge signs `-` and `+` differ, as one change needs. All 7 points are noise-robust, so a second change between two scanned points would show in the signs, and none does. Pairs of changes inside one 0.005 step are not excluded.

### Cost against the estimates written before

| item | written | observed |
|---|---|---|
| state check | 10 s | 7 s (02:51:37 to 02:51:44) |
| each point | 1600 to 2000 s | 1476 to 1503 s (below the range by up to 124 s) |
| the scan | 55 to 70 min | 3000 s (50.0 min; below the range) |
| end of the scan | about 03:55 UTC (03:45 to 04:05) | 03:41:44 UTC (before the range) |
| peak private | about 1.9 GB per worker, about 7.6 GB | 1.81 to 1.82 GB per worker, about 7.3 GB |

This time my estimate was high (the D 21.125 estimate was low). The laptop CPU averaged 70 % against 81 % at D 21.125, with the other project's I114 jobs beside the scan both times.
