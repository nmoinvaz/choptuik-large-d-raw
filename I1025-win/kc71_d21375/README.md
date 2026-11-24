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

**Running.** Started 2026-11-24 06:33:14 UTC (`Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc71d21375_1025.cmd`; conhost pid 26360, driver 26384; the four scan processes started 06:33:21 UTC: p0 25924, p1 15732, p2 24972, p3 1160, each with a worker child). README first: 79c0e5fc4 (pushed 06:32:56 UTC, before the start). win2 pushed the D 21.375 state at 06:29:35 UTC (commit 9af2e828); the dry test ran at 06:32:25 UTC.

At the start: the pins matched; `read_lower.py` selftest 0 and controls 1, 1; `kc71_syscheck.py` selftest 0, the state ACCEPTED (exit 0), `--mutate=F` and `--mutate=steps` exit 1, 1. All four processes printed "the record system" (state |F| 4.3409965177e-10 against the record's 4.3390486020e-10, steps 2378 = 2378). All run BelowNormal; the session check (`session_check_1025.ps1 scan 26360`) exit 0: no `claude` in any chain, no Windows Terminal, a headless conhost in the chain. Machine at the start: free physical memory 23.40 GB, commit 10.74 GB, laptop CPU 73% (the other project's python jobs, not touched). Keep-awake helper holding `ES_SYSTEM_REQUIRED`, alert-only memory watcher, sampler running. Estimate for the end: 07:18 to 07:30 UTC.

Pushed 2026-11-24 06:34:19 UTC.

## Result

Not yet run.
