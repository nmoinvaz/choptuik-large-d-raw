# I1025-win/kc55_d18: the k_c 55 test at D 18, hybrid sign scan of lambda 1.70 to 1.85 on the Mac's k_c 55 state (winb)

Written before the run, 2026-11-21 22:02 UTC by my clock (substituted from `date -u` when pushed).

## Order

The coordinator (hc, about 22:00 UTC), after the low-lambda scans: he does not link the root that rose through 1.20 to D 18.25's 1.3885 yet. win2b's interim at D 18.5, k_c 55, has no root near k_c 63's 1.6772, so the roots past D 18 may depend on k_c, and the k_c test comes before any tracking. **The k_c test at D 18, ONE process only, because of the laptop's memory.** Scan the Mac's k_c 55 state `I1025-mac/out/sol_l1kc55F1025_D18.000000.npy` (its record line from `I1025-mac/out/l1kc55F1025.jsonl`, with the system check first), lambda 1.70 to 1.85 at 0.01 (16 points), with the same script, noise test and float64 sign, 4 threads, BelowNormal, 8 h cap. Window and reading go into the README first, raw `I1025-win/kc55_d18`. If free memory falls below 1 GB, stop the scan by exact pid and report. Post on #1025.

## Window and reading, fixed now

Window: lambda 1.70 to 1.85 at 0.01, 16 points (k_c 63's D 18 roots, 1.7750 and 1.8074, lie inside it).

**Reading (the coordinator's): compare with k_c 63 at D 18 (roots 1.7750 and 1.8074, signs minus, plus, minus). The same two changes within 0.01 means the D 18 pair is k_c-stable. Any other pattern means it depends on k_c.**

How I apply it (mine, to make it exact; `read_kc55_1025.py`): the scan is read by `d18f_read.py window 18.0 1.70 1.85` (xfkappa's reader, 5fb96dce), a change counts only if both of its grid points are noise-robust (1e-15 on blocks 0 to 11, two seeds), and its position is the reader's det-linear estimate (the four-estimator range is printed beside it, information, not a bound). "The same two changes within 0.01" is: exactly two robust changes, none touching a non-robust point, the lower minus-to-plus and the upper plus-to-minus as for k_c 63 in this window, with the lower position within 0.01 of 1.7750 and the upper within 0.01 of 1.8074. Anything else (another count, a position further off, a non-robust point) is "depends on k_c", reported as found with its details. One case the order does not name: two changes at the right places with the orientation reversed (plus-to-minus, then minus-to-plus), because the hybrid's overall sign is not comparable across states; it is printed as that and left to the coordinator. The ln|det| minima without a sign change and the float64 sign are reported as information.

k_c 63's own D 18 values in this window, read by the same reader on xfkappa's scan (`vtest/kc63_D18_control.log`): signs minus at 1.70 to 1.77, plus at 1.78 to 1.80, minus at 1.81 to 1.85; changes (1.77, 1.78) minus to plus, det-linear 1.775263, range [1.774793, 1.775263] (his bisected root 1.7749781), and (1.80, 1.81) plus to minus, det-linear 1.806298, range [1.806298, 1.807635]; no ln|det| minimum without a change; float64 differs from the hybrid at 13 of 16 points. Through my reading script this gives "the same two changes within 0.01" (+0.0003 and -0.0011 from 1.7750 and 1.8074), as a control must; five planted cases give the wanted readings (shifted upper change, one change only, reversed orientation, a change touching a non-robust point, three changes).

## Inputs (raw origin/main by `git show`, `git hash-object --no-filters`; `prep_kc55_inputs_1025.log`)

| item | raw path | blob |
|---|---|---|
| scanner | `I1025-mac/d18/d18_hybsign.py` | e089207a61fbd98614716abd309571cbc4888db2 |
| readers | `I1025-mac/d18/d18f_read.py` (imports d185_scan_read.py, d18c_read.py, d18d_read.py) | 5fb96dceb427e965b830b42db5b8f30255f20532; 7c9d400f, 1383470f, 6b608903 |
| k_c 55 D 18 state | `I1025-mac/out/sol_l1kc55F1025_D18.000000.npy` | b2c3c30278f92d8c4ce0ae4f235add7ea437eb16 |
| its record | `I1025-mac/out/l1kc55F1025.jsonl`, the D 18.0 line (k_c 55, kappa 0.7, u0 0.04, Ks 30, F 2.7150279607819496e-10, 2230 steps; a leap record, no lambda) | 0fb77df8281d634e6ecf2d3b2038e3706df3c960 |
| k_c 63 D 18 scan (control) | `I1025-mac/d18/d18_scan_1025.jsonl` | ac80e9d5bd9c42b1ff10eea65d26258b3314021f |
| signtest.py (system check only) | `I1025-mac/signtest.py` | 179ea09681b0a75f7cefdff98984b48051b3f085 |

**System check first** (`smoke_syscheck_kc55.log`, `signtest.py ... syscheck` on a stub of the record line plus a placeholder lam, `stub_kc55_D18.jsonl`; 22:00:15 UTC): the state rebuilds F 2.720513545369973e-10 against the record's 2.7150279607819496e-10 (2.0e-03 relative, inside 1%) and 2230 steps against 2230: same true. `d18_hybsign.py` checks it again at the start of the scan (exit 3 if it does not hold).

## The command

`d18_hybsign.py REC STATE D LAMS OUT` as xfkappa's (ii) and my D 18.125 and low-lambda scans (`lane_d18f.sh`, quoted in `I1025-win/scan_low/README.md`), once, from `solver/matter` of worktree `choptuik-i1025-lowd` at 505d8399 (`P4_WT_MATTER`), PY `venv-md510`, BelowNormal, 4 BLAS and rayon threads:

```
python -u d18_hybsign.py <l1kc55F1025.jsonl> <sol_l1kc55F1025_D18.000000.npy> 18.0 1.70,1.71,...,1.85 scan_kc55_D18_1025.jsonl
```

## Memory rule and cap

`kc55_driver_1025.py` polls the laptop's free physical memory every 15 s (`FreePhysicalMemory`, the figure my samplers log) and, if it falls below 1 GB, stops the scan by the exact pid of the process it started (`taskkill /PID <pid> /T /F`) and tells the coordinator by hc; the points so far stay in the scan file and no reading is made. The 8 h cap (28800 s) is killed the same way. Both paths are tested on dummy children (`kc55_driver_selftest.log`: the cap and a memory stop, no process left). Earlier today free memory fell to 1.39 GB while another job's python held 19 GB; it is 12.8 GB now.

## Run

`kc55_driver_1025.py` (launcher `start_kc55_1025.cmd`, BelowNormal): one scan process, then the reader and the reading. Output: `kc55_w.log`, `scan_kc55_D18_1025.jsonl`, `scan_kc55_D18.log`, `read_kc55_D18.log`, `read_kc55_1025.log`, `rows/kc55_samples.csv` (a sampler, `sample_driver3_1025.ps1`, every 60 s: the python's cpu seconds, working set, private bytes and peaks, and the laptop's memory and load). Estimate: k_c 55 costs about two thirds of k_c 63 per point (the Mac's 270 s against 403 s), so about 470 s a point alone, 16 points in about 2.1 h plus the setup: done about 00:20 UTC if it starts at 22:05. No RESUME.

## Status

Scan done 2026-11-22 00:08:51 UTC; the result is in the section below.


## Change: the memory watcher is alert-only (the coordinator's correction, received 22:03 UTC by my clock; done 22:04:06 to 22:05:08 UTC)

**Reason:** Nathan's standing rule is no guard that kills processes for memory; alert-only watchers are fine. The coordinator's order of about 22:00 UTC ("if free memory falls below 1 GB, stop the scan by exact pid and report") broke it, and he corrected it: make the memory watcher alert-only, stop only the watcher by its exact pid, do not touch the scan, do not edit the running driver script, start an alert-only watcher (free memory every 15 s, below 1 GB one hc alert, repeated at most every 30 min, no kill), and record the change, its time and the reason here. The section "Memory rule and cap" above is superseded from 22:04:06 UTC.

**What was done, and one fact the order did not foresee:** the memory guard was not a separate process. It was the polling loop inside the driver python (`kc55_driver_1025.py`, pid 16660), which also held the scan's 8 h cap, the sampler and the final reading. So the only way to stop the guard by an exact pid was to stop that driver python: `Stop-Process -Id 16660` at 22:04:06 UTC (exact pid, no children; its launcher stub 16184 ended with it). **The scan was not touched:** its launcher (pid 17520) and worker (pid 532) kept running at BelowNormal, its output file and log are unchanged, and the system check line was already in its log. The driver script file was not edited (it stays in this folder as it ran).

**Replacements, started 22:05:08 UTC (`start_kc55_aux_1025.cmd`, BelowNormal, detached):**

- `kc55_watch_alert_1025.py` (pid 10108): the alert-only watcher. Free physical memory every 15 s; below 1 GB one hc alert to the coordinator, repeated at most every 30 min while it stays below; it kills nothing; it ends when the scan's launcher pid is gone. Log `rows/kc55_memwatch.log`; a dry run (threshold 1000 GB, nothing sent) printed the alert text (`rows/kc55_memwatch_dry.log`).
- `kc55_finish_1025.py` (pid 5288): replaces the driver's other parts. It waits for the scan pid, starts the read-only sampler (same CSV, `rows/kc55_samples.csv`), applies the order's **8 h time cap** (not a memory rule) by the exact pid 17520 at 2026-11-22 06:02:36 UTC if the scan is still running, and when the scan has ended with all 16 points it runs `d18f_read.py window` and `read_kc55_1025.py` exactly as the driver would have (log `kc55_w.log`).

The reading is unchanged. The coordinator accepts the case the order does not name (two changes in the right places with the orientation reversed) as printed and rules on it if it occurs.


## Result (scan 2026-11-21 22:02:36 to 2026-11-22 00:08:51 UTC; written 03:28 UTC): ONE robust change, so by the fixed reading the D 18 pair DEPENDS on k_c

The scan ended by itself at 00:08:51 UTC with all 16 points written (2 h 6 min, 417 to 533 s a point; no cap hit, no memory alert; its exit code was not recorded, the finisher is not its parent). `kc55_finish_1025.py` ran the reader and the reading at once (`kc55_w.log`, `read_kc55_D18.log`, `read_kc55_1025.log`). I did not see it until the coordinator's ping at about 03:30 UTC: the harness had reaped my background waiter earlier for memory, I had not restarted it, and the finisher did not send an hc. This README, the push and the post are from that ping. (From the next task on, a driver sends its own hc when it ends.)

| item | value |
|---|---|
| points | 16 of 16, lambda 1.70 to 1.85 at 0.01; every point noise-robust (1e-15 on blocks 0 to 11, two seeds) |
| record system | true (|F| 2.7206437480e-10 against 2.7150279608e-10, 2230 steps against 2230) |
| hybrid signs | minus at 1.70 to 1.80, plus at 1.81 to 1.85 |
| robust changes | **one**, in (1.80, 1.81), minus to plus: det-linear 1.809055, four-estimator range [1.809055, 1.809155] |
| ln\|det\| | 1.70 -1623.240, 1.71 -1622.142, 1.72 -1621.656, 1.73 -1621.364, 1.74 -1621.180, 1.75 -1621.074, 1.76 -1621.039, 1.77 -1621.076, 1.78 -1621.207, 1.79 -1621.484, 1.80 -1622.096, **1.81 -1624.355**, 1.82 -1621.694, 1.83 -1620.913, 1.84 -1620.363, 1.85 -1619.871 |
| ln\|det\| minima | 1.81 (-1624.355), beside the change; none without a change in the window (the reader's list); the lower edge 1.70 is the lowest value of the window and still falling toward the edge (1.10 below the value at 1.71), a possible minimum below 1.70 that this scan cannot see |
| float64 (information) | no sign change; its sign is minus at all 16 points and differs from the hybrid's at 5 of 16 (1.81 to 1.85) |

**Reading (the coordinator's, fixed before the run, applied as written above): not the same two changes within 0.01, so any other pattern: the D 18 pair DEPENDS on k_c.** At k_c 63 (same window, same reader) the changes are at 1.775263 (minus to plus) and 1.806298 (plus to minus); at k_c 55 there is one change, at 1.809055 (minus to plus), 0.0028 above k_c 63's upper position, and none near 1.775. The hybrid's overall sign is not comparable across states, so I draw nothing from the orientations (the reversed-orientation case of my reading does not arise: there is one change, not two).

CPU and memory (`rows/kc55_samples.csv`, every 60 s, 124 rows; peaks are the process counters; the first minute of samples is from the stopped driver's sampler, the rest from the finisher's): the scan python (pid 532, BelowNormal, up to 14 threads) used 10558 cpu s in 7455 s (1.42 cores on average); working set peak 0.809 GB; private bytes peak 1.299 GB. Laptop: cpu 25 to 77 %; free memory 4.7 to 23.3 GB (the alert-only watcher's minimum 4.78 GB, 0 alerts, nothing below 1 GB); commit at most 30.0 GB of the 41.3 GB limit; other sessions' pythons ran beside.
