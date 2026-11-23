# I1025-win/kc79_d19low: the k_c 79 lower-root scan at D 19 (winb)

Written before the run, 2026-11-23 02:53:58 UTC (substituted from `date -u` when pushed). Nothing has been run for this folder yet.

Runner: the winb session (surface-laptop-4, 4 cores, 8 threads, 32 GB), the same one that ran `../kc79_d185/`, `../kc79_d19/` (raw commit 010273bc: D 19 regrid accepted, 8-point scan read as lambda_1 = 1.539658 at k_c 79) and `../kc79_d1925/`. The coordinator is t5.

## Order (t5's hc, 2026-11-22 about 17:35 UTC; start ordered by t5's hc of about 21:03 UTC)

First queued behind the D 19.25 regrid. At about 21:03 UTC t5 ordered that regrid stopped (superseded by macm3's, `../kc79_d1925/regrid_stopped.txt`) and this scan started now, with two changes: launched through `conhost.exe --headless cmd.exe /c X.cmd` (win2's `cim_start.ps1` form, raw `I1025-win2/kc71_leap`, 4d5e575e: a console started by plain WMI `cmd.exe /c` is handed to Windows Terminal and dies if those windows close), and the laptop kept awake for exactly the scan's duration by a helper that holds `SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` until the scan ends (no change to the power plan), because Modern Standby froze the D 19.25 run for 2 h 12 min. t5 asks for the pids, the session check and the ETA.

1. Why it is mine: dh610 could not take it. Its control on my k_c 79 D 19 state missed the bar fixed before its run (ln|det| 1.9e-6 relative from mine, while its own thread spread is 2.9e-15). By that rule the Windows/Linux difference is real at k_c 79, so scans of my k_c 79 states stay on this machine.
2. The scan: my k_c 79 D 19 state (`../kc79_d19/`), lambda 0.92 to 1.32 at 0.04 (11 values) plus a repeat of 1.12; one process, 4 threads, BelowNormal, outside my terminal; read with dh170's `read_lower.py` (three-decimal keys).
3. New folder `I1025-win/kc79_d19low/`, README first.
4. Report: every robust change with its det-linear estimate and range, the edge signs, any minimum without a change. Post on #1025 and send t5 the verdict.

Why (t5): the lower root at D 19 sits at 1.483 at k_c 63 (dh370, raw a45fc80f) and at 1.296 at k_c 71 (dh610, raw 172112d0); at k_c 79 there is none in 1.475 to 1.49 (my first D 19 scan, `../kc79_d19/`). I report where mine is beside those two values. They are information, not a pass rule.

Same budget as before: one process, 4 threads, BelowNormal; the memory watcher is alert-only (no guard that kills a process, a separate process; the only kill is the time cap by the exact pid). Orientation labels (+ to - versus - to +) are printed as the reader gives them; t5 rules by position.

## The scan

| item | value |
|---|---|
| state | `../kc79_d19/sol_l1kc79W19m1025_D19.0000.npy` (the D 19 regrid's accepted k_c 79 state; the first D 19 scan used the same file) |
| record | `../kc79_d19/l1kc79W19m1025.jsonl` (|F| 2.848e-10, 2976 steps) |
| scanner | `d18_hybsign.py` (xfkappa, raw `I1025-mac/d18`, blob e089207a, unchanged): float64 blocks 0-11 plus a dd block 12, the 1e-15 noise test on blocks 0-11 with 2 seeds, the float64 sign beside it |
| window | 0.92, 0.96, 1.00, 1.04, 1.08, 1.12, 1.16, 1.20, 1.24, 1.28, 1.32, then the repeat 1.12 (12 points, in this order: the 11 values first, the repeat last) |
| reader | `read_lower.py` (dh170, raw `I1025-dh170/lower_root`, blob 89309d3c; imports `d185_scan_read.py`, blob 7c9d400f), `read_lower.py . 0.92 1.32` |
| process | one, 4 BLAS threads, BelowNormal, started through `Win32_Process.Create`, cap 28800 s by the exact pid |

`read_lower.py` globs `scan_*_p*.jsonl` in the folder, so the scanner writes straight to `scan_kc79_D19low_p0.jsonl` (no copy). It prints the points, the not noise-robust ones, the hybrid signs, the float64 differences, the repeated points (a repeat must agree in sign, noise signs, float64 sign and ln|det| within 1e-6), every robust change (bracket, orientation, det-linear estimate, estimator range), changes touching a non-robust point (not counted), the ln|det| minima without a sign change and the endpoint signs. The driver sends t5 every line it printed, as printed.

## Checks and refusals (fixed before the run)

The driver (`kc79d19low_scan_driver_1025.py`, derived from the D 19 one) starts the scan only if all of these hold, and otherwise stops with an hc to t5 (exit 2, no retry):

- The pins of `prep_kc79d19low_pins_1025.txt` match (scanner, reader, its import, the D 19 state, record and `regrid_accepted.txt`; the worktree `choptuik-i1025k79` is at 48c36355). The state is a binary file and equals the raw blob 3a3b1999; the record and the marker are text files written with CRLF here, their raw blobs are the LF form (3603895c, 3e0d6123).
- `../kc79_d19/regrid_accepted.txt` exists (the D 19 regrid's marker) and `scan_kc79_D19low_p0.jsonl` does not.
- The window has at least two distinct values in (0, 10), none more than twice.
- `read_lower.py selftest` exits 0 and its two controls (`--mutate=shift`, `--mutate=round2`) exit 1 each, run in this folder before the scan.

During the run: `d18_hybsign.py` first checks that the state comes back as its record system (exit 3 otherwise: no reading, an hc to t5). A scan that does not finish (non-zero exit, the cap) is reported with the points so far and not read. The reader is run only on a finished scan.

## Cost, written before the run

From the first D 19 scan on this laptop (`../kc79_d19/`): 10665 s for 8 points (1320 to 1344 s per point), peak private 2.45 GB, peak working set 1.68 GB, laptop cpu 28 to 73% with the two I129 jobs of the other project beside it. **Estimate: 12 points at about 1333 s is about 16000 s, 4.4 to 4.5 h wall (t5: about 4.5 h), peak private about 2.5 GB.** The first scan's per-point times differed by only 24 s over its two brackets (1.475 to 1.49 and 1.53 to 1.545); I do not know whether lambda 0.92 to 1.32 costs the same, and the result section reports the per-point times. The sampler (`rows/scan_samples.csv`, a line every 60 s) gives the real figures.

## The drivers (derived from the D 19 ones; the diffs are in `diff_*_vs_d19.txt`)

`make_d19low_1025.py` writes `kc79d19low_scan_driver_1025.py`, `kc79d19low_watch_alert_1025.py`, `start_kc79d19low_scan_1025.cmd` and `publish_kc79d19low_1025.sh` from the D 19 files (raw `../kc79_d19/`) by asserted replacements. The sampler is an unchanged copy. `keepawake_1025.py` and `session_check_1025.ps1` are new. What changed against the D 19 scan driver:

- Names: `kc79d19` to `kc79d19low`, the scan file `scan_kc79_D19low_p0.jsonl`, the reader log `read_lower_kc79_D19low.log`.
- Source: state, record and marker are read from `../kc79_d19/` (pinned by blob), not from this folder.
- Window: a value may appear twice (the repeat).
- Reader: `read_lower.py` instead of `d18f_read.py`, preceded by its selftest and its two controls.
- hc: every line the reader printed.
- Keep-awake: the driver starts `keepawake_1025.py DRIVER_PID scan 29400` as its own process (BelowNormal, no window, like the watcher). It sets `SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` from its main thread, polls the driver pid every 15 s, and clears the state with `ES_CONTINUOUS` and ends when the driver pid is gone (or after the driver's cap plus 600 s). It writes `rows/scan_keepawake.log`, changes no power setting and kills nothing. Its test: `--selftest` (the set call returned 0x80000000, the clear call returned 0x80000001, i.e. the thread held ES_SYSTEM_REQUIRED, exit 0), and a live run against a 25 s watched process (`rows/selftest_live_keepawake.log`: set ok, the helper ended 15 s after the watched pid and cleared the state, returned 0x80000001). `powercfg /requests` needs administrator rights here, so I cannot list the request from outside; the return values are the check.
- Launcher: `start "" /wait /belownormal /b` (no new console) instead of `start /min`, run as `conhost.exe --headless cmd.exe /c start_kc79d19low_scan_1025.cmd "<window>"` through `Win32_Process.Create`.
- Session check: `session_check_1025.ps1` (the Windows counterpart of macm3's `session_check_1025.py`, raw `I1025-macm3/kc79_d1925`): the parent chain of every process of the run up to the first parent that is not running, `session_check_scan.txt`; it exits 1 if `claude` is in a chain and reports Windows Terminal / OpenConsole / headless conhost in a chain.

Tests before the run (`selftest_scan_dry_1025.txt`): the planned window in `--dry` mode (checks run, nothing started, exit 0) and seven bad windows (one value, a value twice with no second value, a value three times, a non-number, 0, 10 and 11) refused with exit 2.

## Run

Started outside my terminal: `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c start_kc79d19low_scan_1025.cmd "<window>"` (BelowNormal, one python process tree, 4 threads), which starts the driver, its sampler, its alert-only watcher (free physical memory every 15 s, one hc alert to t5 below 1 GB, at most every 30 min, kills nothing) and the keep-awake helper.

## Status

**Finished 2026-11-23 02:24:20 UTC, exit 0** (started 2026-11-22 21:08:04 UTC; the scanner at 21:08:05; the driver ended 02:25:31). The D 19.25 regrid is stopped and superseded (`../kc79_d1925/`). README first: bbf7a4a0. The text below up to the Result section was written at the start of the run; the ETA in it was too early (see Result).

- **First try, 21:07:26 UTC, failed before anything started.** `conhost.exe --headless cmd.exe /c start_kc79d19low_scan_1025.cmd "<window>"` lost the quotes, cmd split the window at the commas, the driver printed its usage and exited 2 (`kc79d19low_scan_first_try_stdout.log`, `rows/launcher_pid_scan_first_try.txt`). No scan file, no sampler, no helper was created. Fix: `go_kc79d19low_scan_1025.cmd` holds the call with the quoted window and is the file launched headless.
- **Chain** (`rows/launcher_pid_scan.txt`: 24316): conhost --headless 24316 <- cmd 21256 <- driver launcher 2624 and driver 23340 <- scanner 21572 and 21304 (7 threads), watcher 21300 and 20308, sampler 8824, keep-awake helper 2768 and 24272. All python and powershell processes are BelowNormal (the cmd and the headless conhost are idle at Normal). The pairs are the venv launcher and the interpreter.
- **Session check** (`session_check_scan.txt`, 21:08:34 UTC): no `claude` in any chain, no Windows Terminal / OpenConsole / wt, a headless conhost in the chain; every chain ends WmiPrvSE <- svchost <- services <- wininit. My first version of the check listed the other project's I129 jobs as children of my scanner, because Windows reuses pids (cmd 1532, started 17:27, records the parent pid 21304, which my scanner's child took at 21:08). It now leaves out a child that is older than its parent; the saved file is from the fixed version.
- **Record check:** `d18_hybsign.py` printed `D 19.0 k_c 79: |F| 2.8482007333e-10 (record 2.8482007333e-10), steps 2976 (record 2976): the record system`. The reader's selftest exited 0 and its two controls 1, 1 (`selftest_read_lower_1025.txt`).
- **Keep-awake:** helper pid 24272 set `SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` at 21:08:06 UTC and holds it until the driver pid 23340 ends (`rows/scan_keepawake.log`).
- **ETA:** 12 points at about 1333 s each (the first D 19 scan: 1320 to 1344 s) is about 16,000 s, so the scan ends about 01:35 UTC on 2026-11-23. The first point (0.92) should print about 21:30 UTC. Free memory 22.1 GB at the start, the two I129 jobs of the other project beside it.

Pushed 2026-11-23 02:53:58 UTC.

## Result

**No sign change at k_c 79 between lambda 0.92 and 1.32 at D 19.** All 11 points are `-` and noise-robust, float64 agrees at every point, the repeat of 1.12 agrees, there is no ln|det| minimum without a change, both edges are `-`. Together with the first D 19 scan on the same state (`../kc79_d19/`: `+` at 1.475 to 1.535), the sign goes from `-` at 1.32 to `+` at 1.475, so an odd number of changes lies in (1.32, 1.475), which no scan has covered (see Beside k_c 63 and k_c 71).

### What ran

| item | value |
|---|---|
| scanner | `d18_hybsign.py` (blob e089207a), pid 21572 (interpreter 21304), exit 0 after 18975 s, record check: `D 19.0 k_c 79: |F| 2.8482007333e-10 (record 2.8482007333e-10), steps 2976 (record 2976): the record system` |
| reader | `read_lower.py` (blob 89309d3c), run by the driver at 02:24:21 UTC, exit 0 (`read_lower_kc79_D19low.log`); its selftest and the two `--mutate` controls gave 0, 1, 1 before the scan |
| driver | `kc79d19low_scan_driver_1025.py` done 02:25:31 UTC, no refusal, no cap |
| launch | `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc79d19low_scan_1025.cmd` (conhost 24316 <- cmd 21256 <- driver 23340); the scan kept going through the home-network outage of about 01:00 to 02:50 UTC and the loss of my terminal's API connection |
| keep-awake | helper 24272 held `SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)` from 21:08:06 and cleared it at 02:25:36 UTC (returned 0x80000001), 15 minute lines in `rows/scan_keepawake.log` |
| standby | no System event 506 or 507 after 20:58:16 UTC (the last of the D 19.25 run's), no sampler gap over 90 s in 312 samples, no reboot (last boot 2026-11-20 12:08 UTC) |
| memory watcher | alert-only, ended with the driver: minimum free memory 20.30 GB, 0 alerts (`rows/scan_memwatch.log`) |

### Reader's lines, as printed

```
points 11 in 0.920-1.320; not noise-robust: none
hybrid signs: 0.920- 0.960- 1.000- 1.040- 1.080- 1.120- 1.160- 1.200- 1.240- 1.280- 1.320-
float64 sign differs from the hybrid sign at: none
repeated points: [(1.12, 'agree')]
robust changes: 0; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: - at 0.920, - at 1.320
read_lower exit 0
```

### The points (scan file `scan_kc79_D19low_p0.jsonl`, 12 lines)

| lambda | hybrid sign | noise (2 seeds) | hybrid ln&#124;det&#124; | float64 sign | float64 ln&#124;det&#124; | wall s |
|---|---|---|---|---|---|---|
| 0.92 | - | -, - | -2519.2345057158 | - | -2519.4833367801 | 1648 |
| 0.96 | - | -, - | -2521.8532832273 | - | -2521.9631415747 | 1616 |
| 1.00 | - | -, - | -2524.4855991763 | - | -2524.6708126200 | 1596 |
| 1.04 | - | -, - | -2527.1163428652 | - | -2527.3405458506 | 1665 |
| 1.08 | - | -, - | -2529.7381951534 | - | -2529.7133252525 | 1647 |
| 1.12 | - | -, - | -2532.3542011068 | - | -2532.5280318553 | 1641 |
| 1.16 | - | -, - | -2534.9960232509 | - | -2534.7924185688 | 1646 |
| 1.20 | - | -, - | -2537.7673577741 | - | -2537.5863503529 | 1649 |
| 1.24 | - | -, - | -2540.6051667907 | - | -2540.5846846813 | 1695 |
| 1.28 | - | -, - | -2541.4476587966 | - | -2540.9662434220 | 1455 |
| 1.32 | - | -, - | -2541.7118424518 | - | -2541.6198458169 | 1357 |
| 1.12 (repeat, last) | - | -, - | -2532.3542011068 | - | -2532.5280318553 | 1349 |

The repeat of 1.12 matches the first 1.12 in every printed digit (sign, both noise signs, float64 sign, hybrid and float64 ln|det|).

The hybrid ln|det| falls by 2.62 to 2.64 per 0.04 step from 0.92 to 1.16 (2.619, 2.632, 2.631, 2.622, 2.616, 2.642), by 2.771 and 2.838 for the next two steps, then by 0.842 (1.24 to 1.28) and 0.264 (1.28 to 1.32): it flattens at the upper edge. The first D 19 scan has hybrid ln|det| -2543.2199 at 1.475 and -2543.2765 at 1.49 (sign `+` there). I report the numbers and rule nothing; the reader found no minimum inside 0.92 to 1.32 because 1.32 is an edge.

### Beside k_c 63 and k_c 71 (information, not a pass rule)

| k_c | lower root at D 19 | source |
|---|---|---|
| 63 | 1.483 | dh370, raw a45fc80f |
| 71 | 1.296 | dh610, raw 172112d0 |
| 79 (this scan) | none in 0.92 to 1.32; the sign is `-` at 1.32 and `+` at 1.475 (first scan), so a change lies in (1.32, 1.475) | `../kc79_d19/` and this folder |

At k_c 79 there is no change in 0.92 to 1.32, which holds k_c 71's 1.296, and none in 1.475 to 1.49 (first scan), which holds k_c 63's 1.483. The change that the two scans' signs require is inside the unscanned gap (1.32, 1.475). No scan of that gap has been run; t5 rules.

### Cost

| item | value |
|---|---|
| wall | 18975 s for 12 points (21:08:05 to 02:24:20 UTC), the estimate was about 16000 s (4.5 h) |
| per point | 1596 to 1695 s for points 1 to 9 (mean 1645 s), then 1455, 1357 and 1349 s for the last three; the first D 19 scan on this laptop took 1320 to 1344 s per point |
| scanner cpu | 26491.6 s (1.40 cores on average, up to 13 threads seen, 4 BLAS threads); per point 2222 to 2396 s for points 1 to 9, then 2079, 1900, 1905 s; cpu per wall second 1.35 to 1.44 at every point |
| memory | peak private 2.456 GB, peak working set 1.678 GB; free physical memory at least 20.5 GB (sampler) |
| laptop cpu | 14 to 78 %, mean 49.3 % (sampler, every 60 s), the other project's I129 job 17116 busy until about 22:54 UTC and a new I129 pair (18732, 24800) from 01:54 UTC |

The repeat of 1.12 (last) ran 1349 s against 1641 s for the first 1.12, with the same answer to the last digit, and its scanner cpu fell the same way (1905 s against about 2300 s). So the points from 1.28 on took about 18 % less cpu and wall on this laptop for the same work. The slow stretch began with this run and ended between 01:14 and 01:39 UTC, close to the start of the network outage. I did not log the clock speed during the run, so I do not know the cause. Nothing in the answer depends on it.

### Files

`scan_kc79_D19low_p0.jsonl` (12 lines), `read_lower_kc79_D19low.log`, `scan_kc79_D19low.log` and `rows/scan_kc79d19low_raw.log` (the scanner's own), `kc79d19low_scan_w.log` (driver), `rows/scan_samples.csv`, `rows/scan_keepawake.log`, `rows/scan_memwatch.log`, `session_check_scan.txt` (taken at 21:08:34 UTC).
