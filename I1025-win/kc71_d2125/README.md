# I1025-win/kc71_d2125: lambda_1 at k_c 71 on leg 6's D 21.25 state, a hybrid sign scan at 0.810 to 0.840 (winb)

Written before the run, 2026-11-24 02:51:20 UTC (substituted from `date -u` when pushed). No scan had been run for this folder when the order, the written lines and the estimates below were written. The dry test ran the pins, the `read_lower.py` selftests and the state check (read-only, 2 s each, outputs `*.txt.dry`); the real run repeats them first.

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

Not started. README first.

Pushed 2026-11-24 02:51:20 UTC.

## Result

Not yet run.
