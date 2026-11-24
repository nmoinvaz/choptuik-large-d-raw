# I1025-win/kc87_leg_lambda/21.125: lambda_1 at k_c 87 on dh370's leg state D 21.125, a hybrid sign scan at 0.865 to 0.890 (winb)

Written before the run, 2026-11-24 09:26:46 UTC (the time of the README-first push; later pushes keep it). No scan had been run for this folder when the order, the written line and the estimates below were written. The dry test ran the pins, the `read_lower.py` selftests and the state checks (read-only, 2 s each, outputs `*.txt.dry`); the real run repeats them first. Index and method of the series: `../README.md`.

## Order (t5's hcs of 2026-11-24, winb section)

t5's hc (~09:23 UTC, quoted): "D 21.09375 read: lambda_1 (k_c 87) 0.885927 (k_c 79 0.881686: +0.0042). One more point, a build check: dh370's k_c 87 state at D 21.125 (raw commit 4ab4abcb: I1025-dh370/kc87_leg/sol_l1kc87Ldh370_D21.125000.npy blob 078ab7d8, record l1kc87Ldh370.jsonl blob 8046644b), the same state macm3 read on macOS (0.877108). Same pipeline; d18_hybsign 0.865-0.890 by 0.005 plus a repeat of 0.875. Written before (README first): within 0.002 of macm3's 0.877108 (the build spread at k_c 87). Raw I1025-win/kc87_leg_lambda/21.125/. Then report and stop."

## Written before the run (t5's)

**One robust change within 0.002 of 0.877108** (macm3's k_c 87 reading of this same state on macOS: `I1025-macm3/kc87_leg_lambda/21.125/read_lower.txt`, - to + between 0.875 and 0.880, det-linear 0.877108, range [0.876463, 0.877108]; this run is the build check, the spread between builds at k_c 87). By position: the det-linear estimate of the one robust change that `read_lower.py` prints lies in [0.875108, 0.879108]. I check exactly that and print the reader's lines as they come; t5 rules. Not met by position if the reader prints no robust change, two or more, or one outside [0.875108, 0.879108]. The grid is t5's: 0.865 to 0.890 by 0.005 (6 points) plus a repeat of 0.875. The window ends (0.865, 0.890) are the only evaluated edges; below 0.865 and above 0.890 are not evaluated.

## The source (dh370's, not mine)

| item | value |
|---|---|
| raw folder, commit | `I1025-dh370/kc87_leg`, 4ab4abcb (I1025-dh370/kc87_leg: k_c 87 leg: the accepted state and record of D 21.125 (for dh170's scan)), pushed 2026-11-24 08:44:24 UTC |
| state | `sol_l1kc87Ldh370_D21.125000.npy`, blob 078ab7d8 (45688 bytes) |
| record | `l1kc87Ldh370.jsonl`, blob 8046644b; the D 21.125 row: k_c 87, \|F\| 4.613396630210219e-10, F_start 1.0235938203708346e-05, steps 2935, constraint 3.502685502149237e-03, Delta 1.1215772533972757, Ks 30, u0 0.04, kappa 0.7, 3953 s |
| checks | `kc87_syscheck_1025.py` 6df5d960 (dh610's; the same blob in `I1025-dh610/kc87_d195/in/` and dh170's `kc87_leg_lambda/common_in/`), `kc79_syscheck_1025.py` 29dce7ea (`I1025-win/kc79_d19/`; must refuse a k_c 87 state) |
| scanner, reader | `d18_hybsign.py` e089207a, `d185_scan_read.py` 7c9d400f, `read_lower.py` 89309d3c, the same blobs as my k_c 71 and k_c 95 scans |
| code | the worktree `choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, the code dh170's k_c 87 scan used) |
| macm3's k_c 87 reading of this state on macOS (the prediction's base) | 0.877108 (- to +, det-linear, range [0.876463, 0.877108]; hybrid signs 0.865- 0.870- 0.875- 0.880+ 0.885+, repeat 0.875 agrees), macm3's `I1025-macm3/kc87_leg_lambda/21.125` (`read_lower.txt`, `VERDICT.txt` ACCEPTED 2026-11-24 08:46:30 UTC), the same dh370 blobs 078ab7d8 and 8046644b |

The copies are in `inputs/` (not published; each is pinned by blob in `prep_pins_1025.txt`).

## The checks, before the scan (the driver stops and hc's t5 if any is not as written)

| check | wanted |
|---|---|
| pins: the seven blobs above, the worktree at 48c36355, no scan file yet | all match |
| `read_lower.py selftest`, `--mutate=shift`, `--mutate=round2` | exit 0, 1, 1 |
| `kc87_syscheck_1025.py --selftest`, `kc79_syscheck_1025.py --selftest` | exit 0, 0 |
| `kc87_syscheck_1025.py REC STATE 21.125 WTM` | exit 0: "ACCEPTED: the record class's \|F\| with a step count that comes back" (dry test: state \|F\| 4.6127376988e-10 against the record's 4.6133966302e-10, `freeze_from` 2935 steps = the record's 2935) |
| the same with `--mutate=F`, `--mutate=steps` | exit 1, 1 (the controls) |
| `kc79_syscheck_1025.py REC STATE 21.125 WTM` | exit 1 (refuses: not k_c 79) |
| `d18_hybsign.py` itself, at its start | prints "the record system" (exit 3 and no scan if not) |

## The scan

`d18_hybsign.py` (the hybrid sign: float64 blocks 0 to 11 and a dd block 12, the 1e-15 noise test with 2 seeds, the float64 sign beside it) at D 21.125, in four processes, one share each (one thread each, BelowNormal; `P4_WT_MATTER` the worktree's `solver/matter`; each appends one JSON line per lambda to its own file):

| process | file | lambdas, in this order |
|---|---|---|
| p0 | `scan_kc87_D21125_p0.jsonl` | 0.865, 0.875 (the repeat) |
| p1 | `scan_kc87_D21125_p1.jsonl` | 0.870, 0.885 |
| p2 | `scan_kc87_D21125_p2.jsonl` | 0.875, 0.890 |
| p3 | `scan_kc87_D21125_p3.jsonl` | 0.880 |

7 evaluations: 6 distinct points 0.865 to 0.890 by 0.005 and the repeat of 0.875 (in another process than the first); p3 has one evaluation, the others two. Cap 10800 s (3 h) by the exact pids. Then `read_lower.py . 0.865 0.890` (`D18_DIR` the inputs; it reads every `scan_*_p*.jsonl` of the folder, three-decimal keys, prints a robust change between adjacent points whatever the spacing). The driver hc's t5 every line it printed. A memory watcher (alert-only, its own process, kills nothing), a sampler (every 60 s) and a keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)`, power plan untouched) run beside it. The other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.

## Cost, written before the run

| item | estimate | basis |
|---|---|---|
| state check | 20 s | six checks of 1 to 2 s each (my k_c 71 runs: 6 to 7 s for four) |
| each point | about 3000 to 3300 s with four processes at one thread on four cores | my D 21.09375 points at k_c 87 took 3112 to 3167 s in this setup (same scanner, same kind of state); my k_c 71 points 1370 to 1680 s; macm3's k_c 87 points on an M3 at D 21.0625 619 to 627 s (round 1) and 395 to 400 s (round 2) |
| the scan | 2 rounds: about 100 to 110 min (p3 has one point, the other three processes two) | two rounds of one point per process; the D 21.09375 scan took 6300 s |
| peak private | about 2.8 GB per worker, 11 GB for four | my D 21.09375 workers peaked at 2.764 GB private each (working set 2.05 GB); free memory at the start 23.6 GB, minimum seen then 15.7 GB |

The sampler (`rows/scan_samples.csv`) gives the real figures.

## Files made here

`kc87_scan_driver_1025.py` (a general form of my k_c 71 scan driver: the D, the state and the pins come from `point.json`; the kc79 refusal is added to the state check), `kc87_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `sample_driver4_1025.ps1` (copies of the k_c 71 D 21.375 ones with the folder name changed), `go_kc87_1025.cmd`, `publish_kc87_1025.sh`, `prep_pins_1025.txt`, `selftest_scan_dry_1025.txt`, `point.json`.

## Run

Started outside my terminal: `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc87_1025.cmd`.

## Status

Not started. README first.

Pushed 2026-11-24 09:26:46 UTC.

## Result

Not yet run.
