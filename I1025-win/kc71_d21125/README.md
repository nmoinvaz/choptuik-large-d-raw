# I1025-win/kc71_d21125: lambda_1 at k_c 71 on leg 6's D 21.125 state, a hybrid sign scan at 0.855 to 0.885 (winb)

Written before the run, 2026-11-24 01:47:10 UTC (substituted from `date -u` when pushed). No scan had been run for this folder when the order, the written lines and the estimates below were written. The dry test ran the pins, the `read_lower.py` selftests and the state check (read-only, 2 s each, outputs `*.txt.dry`); the real run repeats them first.

## Order (t5's hc of 2026-11-24, winb section; the #1025 comments 7116849518 and 7118341764 closed the k_c 95 D 19 reading)

lambda_1 at k_c 71 on leg 6's D 21.125 state: win2's raw `I1025-win2/kc71_leap`, tag `l1kc71Lw1025e`, commit 189abc19, state blob d6463b11, record blob 95317a7e, pinned by blob; `kc71_syscheck.py` accepts it, its controls exit 1. `d18_hybsign.py` at 0.855 to 0.885 by 0.005 (7 points) plus a repeat of 0.870, then `read_lower.py`. 4 processes, BelowNormal, raw `I1025-win/kc71_d21125/`, README first. Report the reading.

## Written before the run (t5's)

**One change within 0.01 of 0.869**, where 0.869 is the k_c 79 trend 0.9095 - 0.30 x 0.125 = 0.872, shifted -0.003 for k_c 71. By position: the det-linear estimate of the one robust change that `read_lower.py` prints lies in [0.859, 0.879]. I check exactly that and print the reader's lines as they come; t5 rules. Not met by position if the reader prints no robust change, two or more, or one outside [0.859, 0.879]. The window ends (0.855, 0.885) are the only evaluated edges; below 0.855 and above 0.885 are not evaluated.

## The source (win2's, not mine)

| item | value |
|---|---|
| raw folder, commit | `I1025-win2/kc71_leap`, 189abc19 ("leg 6 state D 21.125 (tag l1kc71Lw1025e)") |
| state | `states/sol_l1kc71Lw1025e_D21.125000.npy`, blob d6463b11 (37368 bytes; the same blob as `states/sol_l1kc71Lw1025e_last.npy`) |
| record | `states/l1kc71Lw1025e.jsonl`, blob 95317a7e; the D 21.125 row: k_c 71, \|F\| 4.610439358408408e-10, F_start 1.0298814037044392e-05, steps 2396, constraint 7.932465137335244e-03, Delta 1.1216517578922631, Ks 30, u0 0.04, kappa 0.7, 3407 s |
| check | `kc71_syscheck.py`, blob 4cd86cd4 (win2's, at 189abc19) |
| scanner, reader | `d18_hybsign.py` e089207a, `d185_scan_read.py` 7c9d400f, `read_lower.py` 89309d3c, the same blobs as my k_c 95 D 19 scan |
| code | the worktree `choptuik-i1025k79` at 48c36355 (the solver code the k_c 79, 87 and 95 D 19 runs used) |

The copies are in `inputs/` (not published; each is pinned by blob in `prep_kc71d21125_pins_1025.txt`).

## The checks, before the scan (the driver stops and hc's t5 if any is not as written)

| check | wanted |
|---|---|
| pins: the six blobs above, the worktree at 48c36355, no scan file yet | all match |
| `read_lower.py selftest`, `--mutate=shift`, `--mutate=round2` | exit 0, 1, 1 |
| `kc71_syscheck.py --selftest` | exit 0 |
| `kc71_syscheck.py REC STATE 21.125 WTM` | exit 0: "ACCEPTED: the record class's \|F\| with a step count that comes back" (dry test: state \|F\| 4.6119732398e-10 against the record's 4.6104393584e-10, `freeze_from` 2396 steps) |
| the same with `--mutate=F`, `--mutate=steps` | exit 1, 1 (the controls) |
| `d18_hybsign.py` itself, at its start | prints "the record system" (exit 3 and no scan if not) |

## The scan

`d18_hybsign.py` (the hybrid sign: float64 blocks 0 to 11 and a dd block 12, the 1e-15 noise test with 2 seeds, the float64 sign beside it) at D 21.125, in four processes, one share each (one thread each, BelowNormal; `P4_WT_MATTER` the worktree's `solver/matter`; each appends one JSON line per lambda to its own file):

| process | file | lambdas, in this order |
|---|---|---|
| p0 | `scan_kc71_D21125_p0.jsonl` | 0.855, 0.870 (the repeat) |
| p1 | `scan_kc71_D21125_p1.jsonl` | 0.860, 0.875 |
| p2 | `scan_kc71_D21125_p2.jsonl` | 0.865, 0.880 |
| p3 | `scan_kc71_D21125_p3.jsonl` | 0.870, 0.885 |

8 evaluations: 7 distinct points 0.855 to 0.885 by 0.005 and the repeat of 0.870 (p3's is the scan point, p0's the repeat, in another process). Cap 10800 s (3 h) by the exact pids. Then `read_lower.py . 0.855 0.885` (`D18_DIR` the inputs; it reads every `scan_*_p*.jsonl` of the folder, three-decimal keys, prints a robust change between adjacent points whatever the spacing). The driver hc's t5 every line it printed. A memory watcher (alert-only, its own process, kills nothing), a sampler (every 60 s) and a keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)`, power plan untouched) run beside it. The other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.

## Cost, written before the run

| item | estimate | basis |
|---|---|---|
| state check | 10 s | the dry test: 2 s each, four calls |
| each point | about 600 to 1500 s with four processes at one thread on four cores | win2's k_c 71 points at D 19.375 took 584 to 690 s in four parallel processes on its machine; my k_c 95 points took 2357 to 2439 s at 4 threads in one process; k_c 71 has the smaller grid, D 21.125 the larger n |
| the scan | 2 points per process: about 20 to 50 min | |
| peak private | about 2 GB per process, about 8 GB for the four | my k_c 79 scan peaked at 2.5 GB, k_c 95 at 3.5 GB; free memory at the start about 23 GB |

The sampler (`rows/scan_samples.csv`) gives the real figures.

## Files made here

`kc71d21125_scan_driver_1025.py` (derived by hand from my k_c 95 D 19 scan driver: no regrid marker, the pins above, the state check, four processes), `kc71d21125_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `sample_driver4_1025.ps1` (copies of the k_c 95 ones with the folder name changed), `go_kc71d21125_1025.cmd`, `publish_kc71d21125_1025.sh`, `prep_kc71d21125_pins_1025.txt`, `selftest_scan_dry_1025.txt`.

## Run

Started outside my terminal: `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc71d21125_1025.cmd`.

## Status

**Running since 2026-11-24 01:46:10 UTC** (started through `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc71d21125_1025.cmd`). README first: fdfc8806 (pushed before the start).

- **Chain** (`rows/launcher_pid.txt`: 20416): conhost --headless 20416 <- cmd 4768 <- scan driver launcher 21232 and driver 23484 <- sampler 24080, alert-only watcher 15836, keep-awake helper 11964, and the four `d18_hybsign.py` processes p0 24208, p1 25760, p2 22900, p3 13568 (each with its worker). All BelowNormal.
- **Session check** (`session_check_scan.txt`, exit 0): no `claude` in any chain, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain.
- **Before the scan** (01:46:11 to 01:46:17 UTC, 6 s): the pins matched; `read_lower.py` selftest 0 and its two controls 1, 1; `kc71_syscheck.py` selftest 0; the state accepted (exit 0; state |F| 4.6119732398e-10 against the record's 4.6104393584e-10, `freeze_from` 2396 steps, the record's); `--mutate=F` and `--mutate=steps` exit 1, 1 (`source_syscheck_*.txt`). All four `d18_hybsign.py` print "the record system".
- **Machine at the start:** on AC (battery status 2, charge 100), clock 2995 of 2995 MHz, free physical memory 23.4 GB, beside it the other project's I114 `convergence.py` jobs (python 880 and 4940), not touched.
- **ETA** (estimates above): the scan ends about 02:30 UTC (range 02:10 to 03:00).

Pushed 2026-11-24 01:47:10 UTC.

## Result

Not yet run.
