# I1025-win/kc87_leg_lambda/21.09375: lambda_1 at k_c 87 on dh370's leg state D 21.09375, a hybrid sign scan at 0.870 to 0.900 (winb)

Written before the run, 2026-11-24 07:37:51 UTC (the time of the README-first push; later pushes keep it). No scan had been run for this folder when the order, the written line and the estimates below were written. The dry test ran the pins, the `read_lower.py` selftests and the state checks (read-only, 2 s each, outputs `*.txt.dry`); the real run repeats them first. Index and method of the series: `../README.md`.

## Order (t5's hcs of 2026-11-24, winb section)

t5's first hc (~07:22 UTC, quoted): "Next task: lambda_1 on dh370's k_c 87 leg states (raw I1025-dh370/kc87_leg/, tag l1kc87Ldh370; dh370 pushes each accepted state), in rotation with macm3 and dh170: take D 21.09375 when it lands (~07:40 UTC), then each time the newest state not yet taken by them (check I1025-macm3/kc87_leg_lambda/ and I1025-dh170/kc87_leg_lambda/ on raw). Per point: pin by blob, kc87_syscheck_1025.py accept (controls exit 1, kc79 refusing), d18_hybsign 0.005 grid over +-0.015 around the prediction plus a repeat of the middle, read_lower. Prediction (README first): k_c 79's reading at that D + 0.002, within 0.005 (D 21.09375: 0.8837 from k_c 79's 0.881686). Raw I1025-win/kc87_leg_lambda/<D>/."

t5's second hc (~07:36 UTC, quoted): "your k_c 87 state is on raw: dh370's D 21.09375, commit 6fdda342, I1025-dh370/kc87_leg/sol_l1kc87Ldh370_D21.093750.npy blob e32cefac, record l1kc87Ldh370.jsonl blob fad4c79a. Prediction (README first): 0.8860 within 0.005 (macm3's k_c 87 0.894588 at D 21.0625 - 0.28 x 0.03125). After it macm3 takes every later point, so report and stop." So this folder holds one point only: the prediction is the second hc's 0.8860 (the first hc's 0.8837 is replaced).

## Written before the run (t5's)

**One robust change within 0.005 of 0.8860** (macm3's k_c 87 reading at D 21.0625, 0.894588 (`I1025-macm3/kc87_leg_lambda/21.0625`: - to +, det-linear, range [0.894232, 0.894588]), minus 0.28 x 0.03125 = 0.00875, that is 0.885838, given by t5 as 0.8860). By position: the det-linear estimate of the one robust change that `read_lower.py` prints lies in [0.8810, 0.8910]. I check exactly that and print the reader's lines as they come; t5 rules. Not met by position if the reader prints no robust change, two or more, or one outside [0.8810, 0.8910]. The grid: 0.8860 rounded to 0.005 is 0.885; the 0.005 grid over +-0.015 around it is 0.870 to 0.900 (7 points) plus a repeat of the middle 0.885. The window ends (0.870, 0.900) are the only evaluated edges; below 0.870 and above 0.900 are not evaluated.

## The source (dh370's, not mine)

| item | value |
|---|---|
| raw folder, commit | `I1025-dh370/kc87_leg`, 6fdda342 (I1025-dh370/kc87_leg: k_c 87 leg: the accepted state and record of D 21.09375 (for dh170's scan)), pushed 2026-11-24 07:35:57 UTC |
| state | `sol_l1kc87Ldh370_D21.093750.npy`, blob e32cefac (45688 bytes) |
| record | `l1kc87Ldh370.jsonl`, blob fad4c79a; the D 21.09375 row: k_c 87, \|F\| 4.6133565820297166e-10, F_start 1.0261820439700622e-05, steps 2939, constraint 3.419290116551296e-03, Delta 1.1207385736816906, Ks 30, u0 0.04, kappa 0.7, 3448 s |
| checks | `kc87_syscheck_1025.py` 6df5d960 (dh610's; the same blob in `I1025-dh610/kc87_d195/in/` and dh170's `kc87_leg_lambda/common_in/`), `kc79_syscheck_1025.py` 29dce7ea (`I1025-win/kc79_d19/`; must refuse a k_c 87 state) |
| scanner, reader | `d18_hybsign.py` e089207a, `d185_scan_read.py` 7c9d400f, `read_lower.py` 89309d3c, the same blobs as my k_c 71 and k_c 95 scans |
| code | the worktree `choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, the code dh170's k_c 87 scan used) |
| k_c 79's reading at D 21.09375 (the prediction's base) | 0.881686 (+ to -, det-linear, range [0.881196, 0.881686]; edges + at 0.865, - at 0.895), for reference only: the first order (~07:22 UTC) based the prediction on it (+ 0.002 = 0.8837), the second (below) replaced that base, dh610's `I1025-dh610/kc79_leg/D21.09375` |

The copies are in `inputs/` (not published; each is pinned by blob in `prep_pins_1025.txt`).

## The checks, before the scan (the driver stops and hc's t5 if any is not as written)

| check | wanted |
|---|---|
| pins: the seven blobs above, the worktree at 48c36355, no scan file yet | all match |
| `read_lower.py selftest`, `--mutate=shift`, `--mutate=round2` | exit 0, 1, 1 |
| `kc87_syscheck_1025.py --selftest`, `kc79_syscheck_1025.py --selftest` | exit 0, 0 |
| `kc87_syscheck_1025.py REC STATE 21.09375 WTM` | exit 0: "ACCEPTED: the record class's \|F\| with a step count that comes back" (dry test: state \|F\| 4.6141266196e-10 against the record's 4.6133565820e-10, `freeze_from` 2939 steps = the record's 2939) |
| the same with `--mutate=F`, `--mutate=steps` | exit 1, 1 (the controls) |
| `kc79_syscheck_1025.py REC STATE 21.09375 WTM` | exit 1 (refuses: not k_c 79) |
| `d18_hybsign.py` itself, at its start | prints "the record system" (exit 3 and no scan if not) |

## The scan

`d18_hybsign.py` (the hybrid sign: float64 blocks 0 to 11 and a dd block 12, the 1e-15 noise test with 2 seeds, the float64 sign beside it) at D 21.09375, in four processes, one share each (one thread each, BelowNormal; `P4_WT_MATTER` the worktree's `solver/matter`; each appends one JSON line per lambda to its own file):

| process | file | lambdas, in this order |
|---|---|---|
| p0 | `scan_kc87_D2109375_p0.jsonl` | 0.870, 0.885 (the repeat) |
| p1 | `scan_kc87_D2109375_p1.jsonl` | 0.875, 0.890 |
| p2 | `scan_kc87_D2109375_p2.jsonl` | 0.880, 0.895 |
| p3 | `scan_kc87_D2109375_p3.jsonl` | 0.885, 0.900 |

8 evaluations: 7 distinct points 0.870 to 0.900 by 0.005 and the repeat of 0.885 (in another process than the first). Cap 10800 s (3 h) by the exact pids. Then `read_lower.py . 0.870 0.900` (`D18_DIR` the inputs; it reads every `scan_*_p*.jsonl` of the folder, three-decimal keys, prints a robust change between adjacent points whatever the spacing). The driver hc's t5 every line it printed. A memory watcher (alert-only, its own process, kills nothing), a sampler (every 60 s) and a keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)`, power plan untouched) run beside it. The other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.

## Cost, written before the run

| item | estimate | basis |
|---|---|---|
| state check | 20 s | six checks of 1 to 2 s each (my k_c 71 runs: 6 to 7 s for four) |
| each point | about 1200 to 3000 s with four processes at one thread on four cores (wide: no k_c 87 timing at D 21 on this machine yet) | my k_c 71 points took 1370 to 1680 s in this setup; scaled by (87/71)^3 = 1.84 that is 2500 to 3100 s; my k_c 87 D 19 points took 1834 to 1863 s one process at a time and the k_c 95 ones 2357 to 2439 s; macm3's k_c 87 D 21.0625 points on an M3 took 619 to 627 s (round 1) and 395 to 400 s (round 2) |
| the scan | 2 points per process: about 40 to 100 min | 2 x the range above plus the start |
| peak private | about 1.6 to 4.1 GB per worker, 6.5 to 16 GB for the four | my k_c 71 workers peaked at 1.81 GB; macm3's k_c 87 workers at D 21.0625 at 1.62 to 3.22 GB RSS and at D 19.75 at 2.5 to 4.1 GB; free memory at the start about 23 GB |

The sampler (`rows/scan_samples.csv`) gives the real figures.

## Files made here

`kc87_scan_driver_1025.py` (a general form of my k_c 71 scan driver: the D, the state and the pins come from `point.json`; the kc79 refusal is added to the state check), `kc87_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `sample_driver4_1025.ps1` (copies of the k_c 71 D 21.375 ones with the folder name changed), `go_kc87_1025.cmd`, `publish_kc87_1025.sh`, `prep_pins_1025.txt`, `selftest_scan_dry_1025.txt`, `point.json`.

## Run

Started outside my terminal: `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc87_1025.cmd`.

## Status

**Running.** Started 2026-11-24 07:38:05 UTC (`Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc87_1025.cmd`; conhost pid 16500, driver 18732; the four scan processes started 07:38:16 UTC: p0 17800, p1 23308, p2 24972, p3 22448, each with a worker). README first: 859fe22af (pushed 07:37:51 UTC, before the start). dh370 pushed the D 21.09375 state at 07:35:57 UTC (commit 6fdda342); the dry test ran at 07:37:05 UTC.

At the start: the pins matched (7 blobs, worktree 48c36355); `read_lower.py` selftest 0 and controls 1, 1; both syscheck selftests 0; `kc87_syscheck_1025.py` accepted the state (exit 0; state |F| 4.6141266196e-10 against the record's 4.6133565820e-10, `freeze_from` 2939 steps = the record's); `--mutate=F` and `--mutate=steps` exit 1, 1; `kc79_syscheck_1025.py` on the state exit 1 (`source_syscheck_*.txt`). All four `d18_hybsign.py` print "the record system". All run BelowNormal; the session check (`session_check_1025.ps1 scan 16500`) exit 0: no `claude` in any chain, no Windows Terminal, a headless conhost in the chain. Machine at the start: free physical memory 23.24 GB, commit 10.53 GB, laptop CPU 49 % (the other project's I114 `convergence.py` jobs beside the scan, not touched). Keep-awake helper holding `ES_SYSTEM_REQUIRED`, alert-only memory watcher, sampler running. Estimate for the end: 08:20 to 09:20 UTC (written range 40 to 100 min).

Pushed 2026-11-24 07:38:47 UTC.

## Result

Not yet run.
