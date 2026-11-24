# I1025-win/kc71_d213125: lambda_1 at k_c 71 on leg 6's D 21.3125 state, a hybrid sign scan at 0.785 to 0.815 (winb)

Written before the run, 2026-11-24 04:45:08 UTC (the time of the README-first push, 9bba83eb9; later pushes keep it). No scan had been run for this folder when the order, the written lines and the estimates below were written. The dry test ran the pins, the `read_lower.py` selftests and the state check (read-only, 2 s each, outputs `*.txt.dry`); the real run repeats them first.

## Order (t5's hc of 2026-11-24 ~03:47 UTC, winb section; the D 21.25 reading, 0.821699, is in `I1025-win/kc71_d2125` and #1025 comment 7121402728)

lambda_1 at k_c 71 on leg 6's D 21.3125 state: win2's raw `I1025-win2/kc71_leap` (pushed 2026-11-24 04:41:51 UTC), tag `l1kc71Lw1025e`, commit 5fefca16, state blob 8456f980, record blob 05a5eaa2, pinned by blob; `kc71_syscheck.py` accepts it, its controls exit 1. `d18_hybsign.py` at 0.785 to 0.815 by 0.005 (7 points) plus a repeat of 0.800, then `read_lower.py`. 4 processes, BelowNormal, raw `I1025-win/kc71_d213125/`, README first. Report the reading.

## Written before the run (t5's)

**One change within 0.01 of 0.802**, where 0.802 is my D 21.25 reading 0.8217 minus 0.32 x 0.0625 (two leg steps on, D 21.3125 - 21.25 = 0.0625; my two readings, 0.862215 at D 21.125 and 0.821699 at D 21.25, give a slope of -0.3241). By position: the det-linear estimate of the one robust change that `read_lower.py` prints lies in [0.792, 0.812]. I check exactly that and print the reader's lines as they come; t5 rules. Not met by position if the reader prints no robust change, two or more, or one outside [0.792, 0.812]. The window ends (0.785, 0.815) are the only evaluated edges; below 0.785 and above 0.815 are not evaluated.

## The source (win2's, not mine)

| item | value |
|---|---|
| raw folder, commit | `I1025-win2/kc71_leap`, 5fefca16 ("leg 6 state D 21.3125 (tag l1kc71Lw1025e)") |
| state | `states/sol_l1kc71Lw1025e_D21.312500.npy`, blob 8456f980 (37368 bytes) |
| record | `states/l1kc71Lw1025e.jsonl`, blob 05a5eaa2; the D 21.3125 row: k_c 71, \|F\| 4.418610413158567e-10, F_start 1.0216381403228736e-05, steps 2381, constraint 8.931172405026108e-03, Delta 1.1267120174484186, Ks 30, u0 0.04, kappa 0.7, 3271 s |
| check | `kc71_syscheck.py`, blob 4cd86cd4 (win2's, at 5fefca16) |
| scanner, reader | `d18_hybsign.py` e089207a, `d185_scan_read.py` 7c9d400f, `read_lower.py` 89309d3c, the same blobs as my k_c 71 D 21.125 and D 21.25 and k_c 95 D 19 scans |
| code | the worktree `choptuik-i1025k79` at 48c36355 (the solver code the k_c 79, 87, 95 and 71 D 21.125 and D 21.25 runs used) |

The copies are in `inputs/` (not published; each is pinned by blob in `prep_kc71d213125_pins_1025.txt`).

## The checks, before the scan (the driver stops and hc's t5 if any is not as written)

| check | wanted |
|---|---|
| pins: the six blobs above, the worktree at 48c36355, no scan file yet | all match |
| `read_lower.py selftest`, `--mutate=shift`, `--mutate=round2` | exit 0, 1, 1 |
| `kc71_syscheck.py --selftest` | exit 0 |
| `kc71_syscheck.py REC STATE 21.3125 WTM` | exit 0: "ACCEPTED: the record class's \|F\| with a step count that comes back" (dry test: state \|F\| 4.4183469906e-10 against the record's 4.4186104132e-10, `freeze_from` 2381 steps) |
| the same with `--mutate=F`, `--mutate=steps` | exit 1, 1 (the controls) |
| `d18_hybsign.py` itself, at its start | prints "the record system" (exit 3 and no scan if not) |

## The scan

`d18_hybsign.py` (the hybrid sign: float64 blocks 0 to 11 and a dd block 12, the 1e-15 noise test with 2 seeds, the float64 sign beside it) at D 21.3125, in four processes, one share each (one thread each, BelowNormal; `P4_WT_MATTER` the worktree's `solver/matter`; each appends one JSON line per lambda to its own file):

| process | file | lambdas, in this order |
|---|---|---|
| p0 | `scan_kc71_D213125_p0.jsonl` | 0.785, 0.800 (the repeat) |
| p1 | `scan_kc71_D213125_p1.jsonl` | 0.790, 0.805 |
| p2 | `scan_kc71_D213125_p2.jsonl` | 0.795, 0.810 |
| p3 | `scan_kc71_D213125_p3.jsonl` | 0.800, 0.815 |

8 evaluations: 7 distinct points 0.785 to 0.815 by 0.005 and the repeat of 0.800 (p3's is the scan point, p0's the repeat, in another process). Cap 10800 s (3 h) by the exact pids. Then `read_lower.py . 0.785 0.815` (`D18_DIR` the inputs; it reads every `scan_*_p*.jsonl` of the folder, three-decimal keys, prints a robust change between adjacent points whatever the spacing). The driver hc's t5 every line it printed. A memory watcher (alert-only, its own process, kills nothing), a sampler (every 60 s) and a keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)`, power plan untouched) run beside it. The other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.

## Cost, written before the run

| item | estimate | basis |
|---|---|---|
| state check | 10 s | the D 21.25 run: 7 s with the pins |
| each point | about 1400 to 1800 s with four processes at one thread on four cores | my D 21.125 points took 1624 to 1681 s (laptop CPU 81 %) and my D 21.25 points 1476 to 1503 s (CPU 70 %) in the same setup; D 21.3125 has a slightly larger grid, and the other project's I114 jobs move the figure |
| the scan | 2 points per process: about 47 to 60 min | 2 x the range above plus the start |
| peak private | about 1.9 GB per worker, about 7.6 GB for the four | D 21.125 and D 21.25: 1.81 to 1.82 GB per worker; free memory at the start about 23 GB |

The sampler (`rows/scan_samples.csv`) gives the real figures.

## Files made here

`kc71d213125_scan_driver_1025.py` (derived by hand from my k_c 71 D 21.25 scan driver: the D, the pins and the window changed), `kc71d213125_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `sample_driver4_1025.ps1` (copies of the D 21.25 ones with the folder name changed), `go_kc71d213125_1025.cmd`, `publish_kc71d213125_1025.sh`, `prep_kc71d213125_pins_1025.txt`, `selftest_scan_dry_1025.txt`.

## Run

Started outside my terminal: `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc71d213125_1025.cmd`.

## Status

**Running since 2026-11-24 04:45:23 UTC** (started through `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc71d213125_1025.cmd`; the scan processes started 04:45:29). README first: 9bba83eb9 (pushed 04:45:08 UTC, before the start). win2 pushed the D 21.3125 state at 04:41:51 UTC (commit 5fefca16); the dry test ran at 04:44:53.

- **Chain** (`rows/launcher_pid.txt`: 23732): conhost --headless 23732 <- cmd 16652 <- scan driver launcher 10496 and driver 7632 <- sampler 15968, alert-only watcher 2120, keep-awake helper 24900, and the four `d18_hybsign.py` processes p0 600, p1 14928, p2 3200, p3 14304 (each with a worker). All BelowNormal.
- **Session check** (`session_check_scan.txt`, exit 0): no `claude` in any chain, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain.
- **Before the scan** (04:45:23 to 04:45:29 UTC, 6 s): the pins matched; `read_lower.py` selftest 0 and its two controls 1, 1; `kc71_syscheck.py` selftest 0; the state accepted (exit 0; state |F| 4.4183469906e-10 against the record's 4.4186104132e-10, `freeze_from` 2381 steps, the record's); `--mutate=F` and `--mutate=steps` exit 1, 1 (`source_syscheck_*.txt`). All four `d18_hybsign.py` print "the record system".
- **Machine at the start:** on AC (battery status 2, charge 100), clock 2995 of 2995 MHz, free physical memory 23.7 GB, beside it the other project's I114 `convergence.py` jobs, not touched.
- **ETA** (estimates above): the scan ends about 05:45 UTC (range 05:38 to 06:00).

Pushed 2026-11-24 04:45:46 UTC.

## Result

Not yet run.
