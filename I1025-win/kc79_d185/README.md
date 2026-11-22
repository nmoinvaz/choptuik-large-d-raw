# I1025-win/kc79_d185: the k_c 79 convergence check at D 18.5: win2's k_c 71 state regridded to k_c 79, then a 4-point hybrid scan (winb)

Written before the run, 2026-11-22 06:35:47 UTC (substituted from `date -u` when pushed).

Runner: the winb session that took over from the one at its weekly usage limit (surface-laptop-4, 4 cores, 8 threads, 32 GB). The coordinator t2j confirmed the run by hc after my first report of 06:30 UTC (the machine was idle); the order is t5's, given to the predecessor at about 03:15 UTC and recovered from its screen and transcript.

## Order

t5 (the #1025 lane), after the k_c 55 test at D 18: lambda_1 at D 18.5 is 1.677016 at k_c 63 and 1.675995 at k_c 71 (difference 1.0e-3). A k_c 79 value says whether that difference shrinks.

1. **Regrid** win2's k_c 71 D 18.5 state to k_c 79 "with the same command win2 used for its k_c 71 seed (its README in raw I1025-win2; quote the command first), accepted only by the same system check". Pilot first: report the regrid's time and peak memory before any scan.
2. **Hybrid scan** at lambda 1.66, 1.67, 1.68, 1.69, with the noise test and the float64 sign, 4 threads, BelowNormal, 8 h cap, raw `I1025-win/kc79_d185`, README first.
3. **Reading, fixed now:** the robust minus-to-plus change's det-linear estimate is lambda_1 at k_c 79. Report it beside 1.677016 (k_c 63) and 1.675995 (k_c 71).

Memory rule (Nathan's standing rule, via the coordinators): the memory watcher is **alert-only**, no guard that kills a process, and a separate process from the drivers.

## The command (win2's, only src, tag and kc changed)

win2 (`I1025-win2/kc71_d185/README.md`, comment 7073281788 on #1025; k_c 63 to k_c 71, exit 0 in 3372 s):

```
ell_refine.py l1kc63Wm1025 63 l1kc71Wm1025 71 1 18.5 2.1181259879 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
```

mine (k_c 71 to k_c 79; with `--no-gamma` the lambda search is skipped and `lam0` is not used, checked in `ell_refine.py`, so I give the same number):

```
ell_refine.py l1kc71Wm1025 71 l1kc79Wm1025 79 1 18.5 2.1181259879 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
```

cwd `solver/matter` of worktree `choptuik-i1025k79` at 48c36355 (solver code `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's; `ell_delta.py` and `ell_refine.py` (blob 631e5801) equal 48c36355's, all checked by the driver), `venv-md510` (multidouble 5.1.0), 4 BLAS threads, BelowNormal, cap 21600 s (win2's) by the exact pid. The source state is copied into the worktree's `data/` (blob 28bf6bac, checked). Outputs `data/sol_l1kc79Wm1025_D18.5000.npy` and `data/l1kc79Wm1025.jsonl`, copied here.

## Acceptance of the regrid (fixed before the run)

win2's rule, `kc71_syscheck.py` (blob 4cd86cd4), with k_c 71 replaced by k_c 79 in the file and nothing else (`kc79_syscheck_1025.py`, the diff is the docstring, the `kc` test and the selftest's planted record): the record's |F| is at most 1e-9 (the record class, 2.1e-10 to 2.8e-10 at k_c 55, 63, 71), the record is k_c 79 at D 18.5, the saved state reproduces its record the way `d18_hybsign.py` checks it (`freeze_from` gives the record's step count and |F| agrees within 1%). Controls: the same numbers with |F| x 1.5 and with steps + 1 must be refused, in the check itself and through `--mutate=F` and `--mutate=steps` (exit 1 each). Before the regrid the driver runs the selftest, and win2's original `kc71_syscheck.py` on win2's accepted k_c 71 state, which must accept on this machine. **A regrid that does not converge (non-zero exit, cap, no state or record, not accepted) stops the task with a report and no scan starts.**

## The scan (fixed before the run)

xfkappa's `d18_hybsign.py REC STATE 18.5 1.66,1.67,1.68,1.69 OUT` (`I1025-mac/d18`, blob e089207a, unchanged) from `solver/matter` of the same worktree (`P4_WT_MATTER`), one process, 4 threads, BelowNormal, cap 28800 s by the exact pid; it checks the record system first (exit 3 if the state does not come back), then per point the hybrid sign with the 1e-15 noise test on blocks 0 to 11 (2 seeds) and the float64 sign. Then `d18f_read.py window 18.5 1.66 1.69` (5fb96dce) and `read_kc79_1025.py` (mine, a printer of the window reader's output, selftested on planted text: `kc79_read_selftest.log`), which prints the robust minus-to-plus change's det-linear estimate beside 1.677016 and 1.675995, the two differences, and whether the k_c 79 minus k_c 71 difference is smaller than the k_c 71 minus k_c 63 one as information. Any other pattern (not exactly one robust change, not minus to plus, a non-robust point) is printed as found, with no lambda_1 value, and the coordinator rules.

## Inputs (raw origin/main by `git show`, `git hash-object --no-filters`; `prep_kc79_inputs_1025.log`)

| item | raw path | blob |
|---|---|---|
| k_c 71 D 18.5 state (win2, accepted) | `I1025-win2/kc71_d185/sol_l1kc71Wm1025_D18.5000.npy` | 28bf6bacc1e8e6563896ae003a3f85ca23ddce63 |
| its record | `I1025-win2/kc71_d185/l1kc71Wm1025.jsonl` | 1609d76bf9b1bbdb10dfa8a62576b8e505f8bc7 |
| win2's acceptance check | `I1025-win2/kc71_d185/kc71_syscheck.py` | 4cd86cd4c9001d7472fc5df625b0635e1884bf81 |
| win2's README (the command) | `I1025-win2/kc71_d185/README.md` | 7f3088b5eee62aff9f1d4871f157b8413bab27a0 |
| win2's reading | `I1025-win2/kc71_d185/kc71_read.txt` | 2f275e03bdaebcea5dd5c4193a72759e5eaf0650 |
| scanner | `I1025-mac/d18/d18_hybsign.py` | e089207a61fbd98614716abd309571cbc4888db2 |
| reader | `I1025-mac/d18/d18f_read.py` (imports the next three) | 5fb96dceb427e965b830b42db5b8f30255f20532 |
| readers it imports | `d185_scan_read.py`, `d18c_read.py`, `d18d_read.py` | 7c9d400f, 1383470f, 6b608903 |

## Run

`start_kc79_regrid_1025.cmd` starts `kc79_regrid_driver_1025.py` (BelowNormal, detached): pins, the controls, the regrid, the acceptance, an hc to the coordinator with the time and the peak memory, and, if accepted, `start_kc79_scan_1025.cmd` which starts `kc79_scan_driver_1025.py`. Each driver starts its own **alert-only memory watcher** (`kc79_watch_alert_1025.py`, its own process, pid in the log: free physical memory every 15 s, one hc alert to the coordinator below 1 GB, repeated at most every 30 min, it kills nothing) and the read-only sampler (`sample_driver4_1025.ps1`, every 60 s: cpu seconds, working set and private bytes with their peaks, and the laptop's free memory, load and commit; `rows/regrid_samples.csv`, `rows/scan_samples.csv`). The only kill is the time cap by exact pid. The drivers send their own hc at the end, so no waiter is needed. Logs `kc79_regrid_w.log`, `kc79_scan_w.log`, `regrid.log`, `regrid_summary.txt`, `syscheck*.txt`, `scan_kc79_D185_1025.jsonl`, `read_kc79_*.log`. The driver's cap path was tested on a dummy process (`kc79_regrid_driver_selftest.log`), the watcher's alert on a dry run (`rows/dry_memwatch_dry.log`).

**Estimate (nothing measured at k_c 79):** regrid 1.5 to 3 h (win2's k_c 71 took 3372 s on a Core Ultra 7 265K, winb's k_c 63 to 71 at D 16.5 took 2 h 22 min here); scan 4 points at about 18 to 25 min, 1.2 to 1.7 h; the machine was idle at 06:30 UTC (free memory 23.9 of 31.8 GB), no other choptuik job runs here; the negative-mass I96 jobs (not mine) count against the thread budget if they start.

## Status

Not started yet.
