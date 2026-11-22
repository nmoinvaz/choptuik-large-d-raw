# I1025-win/kc79_d1925: win2's k_c 71 D 19.25 state regridded to k_c 79 (winb)

Written before the run, 2026-11-22 16:17:30 UTC (substituted from `date -u` when pushed). Nothing has been run for D 19.25 yet.

Runner: the winb session (surface-laptop-4, 4 cores, 8 threads, 32 GB), the same one that ran `../kc79_d185/` and `../kc79_d19/` (raw commit 010273bc: the D 19 regrid accepted at |F| 2.8482e-10 in 5595 s, the 8-point scan read as lambda_1 = 1.539658 at k_c 79). The coordinator is t5.

## Order (t5's hc, 2026-11-22 about 16:10 UTC)

1. Source: win2's k_c 71 D 19.25 state `I1025-win2/kc71_leap/states/sol_l1kc71Lw1025_D19.250000.npy` with its line in `states/l1kc71Lw1025.jsonl` (the record file has grown since t5's pointer, so the blobs are pinned below). win2's `kc71_syscheck.py` must accept it first.
2. `ell_refine.py` to k_c 79 as at D 19 (only D, the output tag and the lambda_0 argument change). Accepted only by `kc79_syscheck_1025.py` and its two controls.
3. 4 threads, BelowNormal, started outside my terminal through WMI. **No scan:** its window comes from dh170's k_c 71 reading (D 19.1875 and D 19.25, ending about 19:40 UTC), so the scan driver is derived and tested but not started.
4. Post the accepted record on #1025 and send t5 the commit. Stop and report on any refusal, failed control or non-converged regrid (no retry).

Why (t5): dh170 scans k_c 71 at D 19.1875 and D 19.25 to see whether k_c 71's pair of roots meets; a k_c 79 state at D 19.25 lets the same window be read at a third k_c.

Same budget as before: one process, 4 threads, BelowNormal; the memory watcher is alert-only (no guard that kills a process, a separate process; the only kill is the time cap by the exact pid).

## The command

At D 19 (`../kc79_d19/`, exit 0 in 5595 s):

```
ell_refine.py l1kc71Lw1025 71 l1kc79W19m1025 79 1 19 2.1156378446 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
```

At D 19.25 (changed: D, the output tag so that the D 19 record in the worktree's `data/` stays untouched, and the lambda_0 argument):

```
ell_refine.py l1kc71Lw1025 71 l1kc79W1925m1025 79 1 19.25 2.1144367878 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
```

The lambda_0 argument is not from my find script (it does not compute one). It is `ell_delta.lam0_at(19.25, *lam0_table())` in the worktree, 2.1144367878 (interpolation error 4.5e-9); the same call returns win2's quoted 2.1184454184 at D 18.4375 and my earlier 2.1181259879 (D 18.5) and 2.1156378446 (D 19). `--no-gamma` does not use it (checked in `ell_refine.py` at the D 18.5 run).

`ell_refine.py` reads `data/sol_l1kc71Lw1025_D19.2500.npy` (`{D:.4f}`), so the find script copies win2's `..._D19.250000.npy` there and checks it by blob. cwd `solver/matter` of worktree `choptuik-i1025k79` at 48c36355 (solver code `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's; `ell_delta.py` and `ell_refine.py` (blob 631e5801) equal 48c36355's; the driver checks all of it), `venv-md510` (multidouble 5.1.0), 4 BLAS threads, BelowNormal, cap 21600 s by the exact pid.

## The source (found on raw origin/main at 16:16 UTC by `prep_kc79d1925_find_1025.py`, exit 0)

| item | raw path | blob |
|---|---|---|
| win2's k_c 71 D 19.25 state (leap, first leg) | `I1025-win2/kc71_leap/states/sol_l1kc71Lw1025_D19.250000.npy` | 36bc6b837f1016f23f50948a7b1fb2b1bd172ade |
| its record (all leg-1 points; the D 19.25 line is used) | `I1025-win2/kc71_leap/states/l1kc71Lw1025.jsonl` | a0e217039531a0c996d9c955c1dbc48a1a280d70 |
| win2's acceptance check | `I1025-win2/kc71_leap/kc71_syscheck.py` | 4cd86cd4c9001d7472fc5df625b0635e1884bf81 (the file used at D 19) |
| win2's README (for reference) | `I1025-win2/kc71_leap/README.md` | 8c7596d73c8b808eb139ff7b76530ad8054dd0f8 |

The k_c 71 source record at D 19.25 (read from the pinned file): |F| 3.0024e-10, 2630 steps, constraint 1.990e-3, Delta 1.0737683214116, 2514 s (the leap step). The fixed pins are the D 19 run's, unchanged: scanner `d18_hybsign.py` e089207a, reader `d18f_read.py` 5fb96dce and its three imports (7c9d400f, 1383470f, 6b608903). The pins and config are `prep_kc79d1925_pins_1025.txt` and `kc79d1925_cfg_1025.txt` (`find_run_1025.txt` is the find script's output). The find script's planted cases (`selftest_find_1025.txt`: D 19.1875 only, one name, both names, two tags, two blobs, a k_c 63 state, D 19.0, D 19.3125, a k_c 79 tag) read as written; it takes only a `..._D19.250000.npy` or `..._D19.2500.npy` of one `l1kc71L*` tag, stops on more than one tag or two names with different blobs, and needs the record's D 19.25 line.

## Acceptance (fixed before the run)

Two steps, both with the D 19 rule:

1. **The source.** win2's own `kc71_syscheck.py` (blob 4cd86cd4) must **accept win2's k_c 71 D 19.25 state and record on this machine** before the regrid starts: the record's |F| at most 1e-9, the saved state reproducing its record (`freeze_from` gives the record's step count, |F| within 1%), and its two built-in controls refused. A refusal stops the task with a report; no regrid.
2. **The result.** `kc79_syscheck_1025.py` (the D 18.5 and D 19 file, unchanged): the record's |F| at most 1e-9, the record is k_c 79 at D 19.25, the saved state reproduces its record (`freeze_from` gives the record's steps, |F| within 1%). Controls: |F| x 1.5 and steps + 1 must be refused on the same numbers and through `--mutate=F` and `--mutate=steps` (exit 1 each). **A regrid that does not converge (non-zero exit, cap, no state or record, not accepted) stops with a report; no retry.**

The accepted record (|F|, steps, constraint, Delta) is posted on #1025 beside the k_c 71 source record at D 19.25 (the driver puts both in `regrid_summary.txt` and in its hc).

## Cost, written before the run

From the D 19 regrid on this laptop (`../kc79_d19/`): 5595 s wall, cpu 9425 s, peak working set 2.19 GB, peak private 2.48 GB, 4 threads, BelowNormal, with the two I129 jobs of the other project beside it; k_c 71 to 79 states have 2976 steps at D 19 (the k_c 71 source has 2676) and 3083 at D 18.5. The k_c 71 source at D 19.25 has 2630 steps (D 19: 2676). **Estimate for D 19.25: 1.5 to 1.7 h wall (t5: about 1.5 h), cpu about 9500 to 11000 s, peak private about 2.5 GB.** The two I129 jobs (`harm_circles.py`, boxes of the other project) share the laptop and count against the 6-thread budget with my 4; t5 cleared that at D 19. The sampler (`rows/regrid_samples.csv`, a line every 60 s) gives the real figures; the result section reports them.

## The drivers (derived from the D 19 ones; the diffs are in `diff_*_vs_d19.txt`)

`make_d1925_1025.py` writes `kc79d1925_regrid_driver_1025.py`, `kc79d1925_scan_driver_1025.py`, `kc79d1925_watch_alert_1025.py`, `prep_kc79d1925_find_1025.py`, the two launchers and `publish_kc79d1925_1025.sh` from the D 19 files (raw `../kc79_d19/`) by regex and asserted replacements. The sampler, the check and the fixed pins file are unchanged copies. What changed:

- **D:** 19 to 19.25 (the command, the check calls, the source record line `D == 19.25`, the state names `D19.2500`).
- **The output tag** `l1kc79W1925m1025`, the folder `kc79_d1925` and the file names `kc79d1925_*`; **lambda_0** 2.1144367878 (unused).
- **The find script:** the D 19.25 state names, the selftest cases above.
- **The scan driver** (not started): takes the comma-separated window as its argument, runs xfkappa's `d18f_read.py window 19.25 LO HI` afterwards and sends its change lines to t5 as printed; its files are `scan_kc79_D1925_1025.jsonl`, `read_kc79_D1925.log`. dh170's `read_lower.py` (three-decimal keys, used for 0.005 grids) can read the same scan file; which reader is t5's call.
- A bare '19' left in the derived files (docstrings naming the D 19 run, a regex) was looked at by `make_d1925_1025.py`'s own leftover scan.

Tests before the run: the find script's selftest, the regrid driver's cap selftest (`kc79_regrid_driver_selftest.log`: a dummy process killed at the cap by exact pid, none left).

## Run

Started outside my terminal: `Win32_Process.Create` of `cmd.exe /c start_kc79d1925_regrid_1025.cmd` (BelowNormal, one python process tree, 4 threads), which starts the driver, its sampler and its alert-only watcher (free physical memory every 15 s, one hc alert to t5 below 1 GB, at most every 30 min, kills nothing).

## Status

Not started yet: this README is pushed first. Pushed 2026-11-22 16:17:30 UTC.

## Result

Not yet run.
