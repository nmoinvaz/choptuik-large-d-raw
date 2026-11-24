# I1025-win/kc95_d21: k_c 95 at D 21.0, regridded from dh610's k_c 87 D 21.0 state, then a hybrid sign scan at 0.900 to 0.925 (winb)

Written before the run, 2026-11-24 11:10:48 UTC (the time of the README-first push; later pushes keep it). Neither the regrid nor the scan had been run for this folder when the order, the written line and the estimates below were written. Run beforehand, read-only: the dry run of the regrid driver (pins, both selftests), the source checks by hand (seconds), the scan driver's dry run on a stand-in marker, state and record. Runner: the winb session (surface-laptop-4, Windows 11, 4 cores, 32 GB); coordinator t5.

## Order (t5's hc of 2026-11-24, ~11:05 UTC, winb section, quoted)

"D 21.125 read: 0.877108 on Windows, equal to macm3's macOS value to 6 digits: the build spread at k_c 87 is nil. Next task (#1025): k_c 95 at D 21.0 from dh610's k_c 87 state (raw I1025-dh610/kc87_d21/: sol_l1kc87dh610e_D21.0000.npy blob 831d5977, record l1kc87dh610e.jsonl blob 9b090ba6; pin by blob): kc87_syscheck accept (controls exit 1), ell_refine.py l1kc87dh610e 87 l1kc95winbg 95 1 21.0 2.1067409501 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma (your thread budget), kc95_syscheck accept (controls exit 1, kc87 refusing); then d18_hybsign 0.900-0.925 by 0.005 plus a repeat of 0.910, read_lower. Written before (README first): |k95 - k87| <= 0.002 against k_c 87's 0.911685 (dh170 tests the same at D 21.125). Raw I1025-win/kc95_d21/."

My reading of "your thread budget": the regrid in one process at 4 threads (as at k_c 95 D 19), the scan in four processes at one thread each (as the k_c 87 leg scans).

## Written before the run (t5's)

**|k95 - k87| <= 0.002 against k_c 87's 0.911685** (dh610's k_c 87 reading at D 21.0, `I1025-dh610/kc87_d21/read_lower.txt`: - to + between 0.910 and 0.915, det-linear 0.911685, range [0.911139, 0.911685]; hybrid signs 0.895- 0.900- 0.905- 0.910- 0.915+ 0.920+ 0.925+, the repeat of 0.910 agrees). By position: the det-linear estimate of the one robust change that `read_lower.py` prints lies in [0.909685, 0.913685]. I check exactly that and print the reader's lines as they come; t5 rules. Not met by position if the reader prints no robust change, two or more, or one outside [0.909685, 0.913685]. The grid is t5's: 0.900 to 0.925 by 0.005 (6 points) plus a repeat of 0.910 (7 evaluations). The window ends (0.900, 0.925) are the only evaluated edges; below 0.900 and above 0.925 are not evaluated. If the regrid is not ACCEPTED there is no scan.

## The source (dh610's, not mine)

| item | value |
|---|---|
| raw folder, commit | `I1025-dh610/kc87_d21`, 6e89d6279 (I1025-dh610/kc87_d21: k_c 87 D 21.0 state+record, VERDICT ACCEPTED), pushed 2026-11-24 04:14:45 UTC |
| state | `sol_l1kc87dh610e_D21.0000.npy`, blob 831d5977 (45688 bytes) |
| record | `l1kc87dh610e.jsonl`, blob 9b090ba6 (one row): k_c 87, D 21.0, kappa 0.7, u0 0.04, Ks 30, \|F\| 4.610998301576713e-10, F_start 2.288336927471666e-05, steps 2948, constraint 3.1763514726419e-03, Delta 1.118229686747366 (the k_c 79 source's 1.1182445857206806), 5457 s |
| dh610's verdict | `VERDICT.txt`: ACCEPTED 2026-11-24 03:25:53 UTC; regrid from win2's k_c 79 leap state D 21.0, `ell_refine.py` exit 0, wall 5460 s |
| dh610's k_c 87 reading | 0.911685 (- to +, range [0.911139, 0.911685]), the line's base |
| lambda_0 | 2.1067409501 (t5's value; unused with `--no-gamma`) |
| checks | `kc87_syscheck_1025.py` 6df5d960 and `kc95_syscheck_1025.py` d487e628 (dh610's; the k_c 95 one is the k_c 87 one with three changed lines, `kc95_syscheck_1025_dh610.diff`; the version dh610 used at D 19.5 and I at D 19) |
| scanner, reader | `d18_hybsign.py` e089207a, `d185_scan_read.py` 7c9d400f, `read_lower.py` 89309d3c, the same blobs as my k_c 87 and k_c 95 runs |
| code | the worktree `choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_delta.py` and `ell_refine.py` at 48c36355, `ell_refine.py` blob 631e5801), the one of every regrid here |

The copies are in `inputs/` and, for the source state and record, also in the worktree's `solver/matter/data/` (where `ell_refine.py` reads its source); each is pinned by blob in `prep_kc95d21_pins_1025.txt`.

The source checks, run by hand at 11:09 UTC before writing this (read-only, `kc87_syscheck_1025.py REC STATE 21.0 WTM`): the k_c 87 check exit 0 (record |F| 4.6109983016e-10, state |F| 4.6109376036e-10, `freeze_from` 2948 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1, the k_c 95 check exit 1 ("the record is not k_c 95 at D 21"). The driver repeats all four and stops if any differs.

## The run

1. **Step 1, regrid** (`kc95d21_regrid_driver_1025.py`, a copy of the D 19 one with the pins, tags, D and lambda_0 changed, `diff_regrid_driver_vs_kc95d19.txt`): the pins; the selftests of both checks (exit 0); the source through the four checks above; then
   `ell_refine.py l1kc87dh610e 87 l1kc95winbg 95 1 21.0 2.1067409501 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`
   in one process, 4 BLAS threads, BelowNormal, cap 28800 s (8 h) by the exact pid (the D 19 one, 10230 s, had 21600 s). ACCEPTED only if `kc95_syscheck_1025.py` exits 0 on the result, its selftest exits 0, `--mutate=F` and `--mutate=steps` exit 1, and `kc87_syscheck_1025.py` exits 1 on the result (refuses it). The marker `regrid_accepted.txt` (with the state and record blobs) is written from the driver's python process.
2. **Step 2, scan, only after ACCEPTED** (`kc95d21_scan_driver_1025.py`, from the k_c 87 leg driver): `d18_hybsign.py` (the hybrid sign: float64 blocks 0 to 11 and a dd block 12, the 1e-15 noise test with 2 seeds, the float64 sign beside it) at D 21.0 in four processes, one share each, one thread each, BelowNormal, cap 21600 s by the exact pids; the reader first passes its selftest and its two `--mutate` controls (exit 0, 1, 1):

| process | file | lambdas, in this order |
|---|---|---|
| p0 | `scan_kc95_D21_p0.jsonl` | 0.900, 0.910 (the repeat) |
| p1 | `scan_kc95_D21_p1.jsonl` | 0.905, 0.920 |
| p2 | `scan_kc95_D21_p2.jsonl` | 0.910, 0.925 |
| p3 | `scan_kc95_D21_p3.jsonl` | 0.915 |

7 evaluations: 6 distinct points 0.900 to 0.925 by 0.005 and the repeat of 0.910 (in another process than the first); p3 has one evaluation, the others two. Then `read_lower.py . 0.9 0.925` (`D18_DIR` the inputs; it reads every `scan_*_p*.jsonl` of the folder, three-decimal keys, prints a robust change between adjacent points whatever the spacing). Each driver hc's t5 its end and every line the reader printed.
3. Each driver starts its own sampler (every 60 s), alert-only memory watcher (free physical memory every 15 s, one hc alert to t5 below 1 GB, at most every 30 min; kills nothing) and keep-awake helper (`SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` until that driver's pid is gone, power plan untouched). The other project's negative-mass I114 `convergence.py` jobs share the laptop and are not touched.
4. `go_kc95d21_1025.cmd` runs step 1 and, only if `regrid_accepted.txt` exists, step 2, in one headless console, started as `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc95d21_1025.cmd` (outside my terminal; the session check `session_check_1025.ps1` must show no `claude` in the chain).

Dry tests (`selftest_scan_dry_1025.txt`, `selftest_*_syscheck.txt.dry`, `kc95_regrid_w.log.dry`): the regrid driver's pins and both selftests pass (exit 0, nothing started); the scan driver runs its checks on a stand-in marker, state and record (the k_c 87 D 21.0 files renamed to the k_c 95 tag, in a folder that is not published) and reaches "would start" for four processes (exit 0), refuses a missing marker, refuses a marker with a wrong blob, refuses seven bad share lists (exit 2) and refuses `--out` without `--dry`. The real marker, state and record exist only after the regrid.

## Cost, written before the run

| item | estimate | basis |
|---|---|---|
| source checks | about 15 s | seconds each by hand here; 12 s in all at D 19 |
| regrid | about 9000 to 12500 s (2.5 to 3.5 h), peak private about 3.5 GB | my k_c 95 regrid at D 19 took 10230 s (peak private 3.45 GB, cpu 18179 s, 4 threads); dh610's k_c 87 regrid at D 21.0 took 5457 s on his machine; my k_c 79 to 87 regrids took 5595 s (D 19, k_c 71 to 79) and 7965 s (D 19, 79 to 87), so the cost does not grow fast with D here |
| each scan point | about 3900 to 4400 s with four processes at one thread on four cores | my k_c 87 points at D 21.09375 took 3112 to 3167 s in this setup (D 21.125: 2572 to 3168 s); k_c 95 over k_c 87 at D 19 was 1.28 to 1.31 times (2357 to 2439 s against 1834 to 1863 s) |
| the scan | about 7300 to 8800 s (2.0 to 2.4 h) for the two rounds; p3 (one point) about 1.1 to 1.2 h | the first round at 3900 to 4400 s, the second (three processes) 3300 to 4400 s |
| peak private | about 3.3 to 3.8 GB per scan worker, 13 to 15 GB for four | k_c 87 workers at D 21.09375 peaked at 2.764 GB; the D 19 k_c 95 over k_c 87 factor 3.45/2.94 = 1.17 gives 3.2 GB; free memory at the start about 23.5 GB |
| together | start about 11:25 UTC; the regrid ends about 13:55 to 15:00 UTC, the scan about 16:00 to 17:30 UTC (most likely about 16:30) | the rows above |

The sampler (`rows/regrid_samples.csv`, `rows/scan_samples.csv`) gives the real figures.

## Files made here

`make_kc95d21_1025.py` writes `kc95d21_regrid_driver_1025.py`, `kc95d21_watch_alert_1025.py`, `keepawake_1025.py`, `session_check_1025.ps1`, `sample_driver4_1025.ps1` and `go_kc95d21_1025.cmd` and `publish_kc95d21_1025.sh` from the k_c 95 D 19 ones (raw `I1025-win/kc95_d19` at f2bcf20e) by asserted text replacements; `kc95d21_scan_driver_1025.py` is written by hand from my k_c 87 leg scan driver (`I1025-win/kc87_leg_lambda`) with the marker logic of the k_c 95 D 19 scan driver. `diff_regrid_driver_vs_kc95d19.txt` is the diff of the regrid driver against the D 19 one, `prep_kc95d21_pins_1025.txt` the pins.

## Status

Not started. README first.

Pushed 2026-11-24 11:10:48 UTC.

## Result

Not yet run.
