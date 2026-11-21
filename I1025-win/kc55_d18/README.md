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

Not started (22:02 UTC).
