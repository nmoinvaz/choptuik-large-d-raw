# I1025-win/kc79_d19: win2's k_c 71 D 19 state regridded to k_c 79 (winb)

Written before the run, 2026-11-22 11:21:36 UTC (substituted from `date -u` when pushed). Nothing has been run for D 19 yet; the D 19 state of win2 has not landed.

Runner: the winb session (surface-laptop-4, 4 cores, 8 threads, 32 GB), the same one that ran `../kc79_d185/` (raw commit b895f104: the D 18.5 root at k_c 79 is 1.676555, the same root as k_c 71's 1.675995 by t5's ruling). The coordinator is t5.

## Order (t5's hc, 2026-11-22 about 09:41 UTC)

1. Wait for win2's k_c 71 D 19 state (win2 expects it near 10:15 UTC; it lands in raw `I1025-win2/` with its record). Use it only once win2's `kc71_syscheck.py` has accepted it.
2. New raw folder `I1025-win/kc79_d19/`, README first. Copy the D 18.5 regrid driver and scan driver and change only D, the source state, record and their pins. Write the acceptance (the same `kc79_syscheck` rule and its two controls) and the cost before the run.
3. Regrid k_c 71 to k_c 79 at D 19 with the same command as at D 18.5, then run the system check. Post the accepted record (|F|, steps, constraint, Delta against the k_c 71 source) on #1025.
4. **Do not start the scan:** its 4-point window is t5's to give, after win2's k_c 71 and dh370's k_c 63 D 19 readings. The scan driver takes the window as an argument, so it needs no edit.
5. Stop and report on any refusal, a failed control, or a regrid that does not converge. Estimate from t5: about 1.5 h for the regrid after the state lands.

Same budget as before: one process, 4 threads, BelowNormal, started outside my terminal through WMI; the memory watcher is alert-only (no guard that kills a process, a separate process; the only kill is the time cap by the exact pid).

## The command

At D 18.5 (`../kc79_d185/`, win2's command with only src, tag and kc changed, exit 0 in 5415 s):

```
ell_refine.py l1kc71Wm1025 71 l1kc79Wm1025 79 1 18.5 2.1181259879 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
```

At D 19 (same command; changed: D, the source tag, the output tag so that the D 18.5 record in the worktree's `data/` stays untouched, and the lambda_0 argument, which `--no-gamma` does not use: checked in `ell_refine.py` at the D 18.5 run; the number is win2's lambda_0(19) = 2.1156378446 from `ell_delta.lam0_at`, as quoted in `I1025-win2/kc71_leap/README.md`):

```
ell_refine.py SRC 71 l1kc79W19m1025 79 1 19 2.1156378446 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
```

`SRC` is the tag of win2's leap, `l1kc71Lw1025` (or `l1kc71Lw1025b` if the second leg makes D 19): `ell_refine.py` reads `data/sol_SRC_D19.0000.npy`, so the state is copied into the worktree under that name by the prep script, and checked by blob. cwd `solver/matter` of worktree `choptuik-i1025k79` at 48c36355 (solver code `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's; `ell_delta.py` and `ell_refine.py` (blob 631e5801) equal 48c36355's; the driver checks all of it), `venv-md510` (multidouble 5.1.0), 4 BLAS threads, BelowNormal, cap 21600 s by the exact pid.

## Finding the source (fixed before the run)

`prep_kc79d19_find_1025.py` looks in raw origin/main for `I1025-win2/.../sol_l1kc71L*_D19.0000.npy` or `..._D19.000000.npy` (the leap saves the `.4f` name at multiples of 0.5) and the record `TAG.jsonl` beside it. It writes nothing until both are there and the record has a D 19.0 line. Exit 3 means not there yet. It stops (exit 1, no regrid) when there is more than one candidate tag, when the two name forms hold different blobs, or on any blob mismatch. It fetches by `git show`, checks every file against its blob (`git hash-object --no-filters`), writes the pins file and the config (`SRC`, `SRCSTATE`, `SRCREC`, `SRCCHECK`) that the regrid driver reads, and copies the state into the worktree's `data/`. Its planted cases (`selftest_find_1025.txt`: none, one name, both names, two tags, two blobs, a k_c 63 state, D 19.5) all read as written, and a rehearsal on win2's present D 18.75 state (`rehearsal_find.txt`: fetch, five fixed pins, three win2 pins and its README, the D 18.75 line of the record) ran through with the same code and other output files.

A waiter polls raw every 5 minutes for it (cap 4 h); the regrid starts only after the find script's exit 0 and my reading of the record's D 19 line (kc 71, |F| inside the class bar). The pins of the fixed inputs are the D 18.5 run's, unchanged: scanner `d18_hybsign.py` e089207a, reader `d18f_read.py` 5fb96dce and its three imports (7c9d400f, 1383470f, 6b608903).

## Acceptance (fixed before the run)

Two steps, both with the D 18.5 rule:

1. **The source.** win2's own `kc71_syscheck.py` (raw blob 4cd86cd4, the same file in `kc71_d185/` and `kc71_leap/`; the driver runs the copy named in the config) must **accept win2's k_c 71 D 19 state and record on this machine** before the regrid starts: the record's |F| at most 1e-9, the saved state reproducing its record (`freeze_from` gives the record's step count, |F| within 1%), and its two built-in controls refused. A refusal stops the task with a report; no regrid. (The leap's own bar is `--fmax 1e-8`, so a D 19 record above 1e-9 is a refusal, not a rounding.)
2. **The result.** `kc79_syscheck_1025.py` (the D 18.5 file, unchanged, `cmp` equal; win2's rule with k_c 71 replaced by k_c 79): the record's |F| at most 1e-9, the record is k_c 79 at D 19, the saved state reproduces its record (`freeze_from` gives the record's steps, |F| within 1%). Controls: |F| x 1.5 and steps + 1 must be refused on the same numbers and through `--mutate=F` and `--mutate=steps` (exit 1 each). **A regrid that does not converge (non-zero exit, cap, no state or record, not accepted) stops with a report; no retry.**

The accepted record (|F|, steps, constraint, Delta) is posted on #1025 beside the k_c 71 source record at D 19 (the driver puts both in `regrid_summary.txt` and in its hc).

## Cost, written before the run

From the D 18.5 regrid on this laptop (`../kc79_d185/`): 5415 s wall, cpu 9802 s (about 1.8 cores), peak working set 2.19 GB, peak private 2.48 GB, 4 threads, BelowNormal; k_c 71 to 79 states have 3083 steps at D 18.5. **Estimate for D 19: 1.5 to 2 h wall (t5: about 1.5 h), cpu about 10000 to 13000 s, peak private 2.5 to 3 GB.** At 09:50 UTC the laptop has 24.0 of 31.8 GB free and 61% cpu in use: the negative-mass project's I129 jobs (two `harm_circles.py` processes, boxes `p7603_l2` and `p7603_l3`, not mine) are running, so the regrid shares the 4 cores with them and may run longer than the D 18.5 one, which ran on an idle machine. Their threads count against the budget; mine stay at 4. The sampler (`rows/regrid_samples.csv`, a line every 60 s: cpu, working set and private bytes with their peaks, free memory, load, commit) gives the real figures; the result section reports them.

## The drivers (derived from the D 18.5 ones; the diffs are in `diff_*_vs_d185.txt`)

`make_d19_1025.py` writes `kc79d19_regrid_driver_1025.py`, `kc79d19_scan_driver_1025.py` and `kc79d19_watch_alert_1025.py` from the D 18.5 files by exact string replacements, each asserted to occur once. The sampler (`sample_driver4_1025.ps1`) and the check (`kc79_syscheck_1025.py`) are unchanged copies. What changed:

- **D:** 18.5 to 19 (the command, the check calls, the state names `D19.0000`).
- **The source:** tag, state, record, check and their blobs come from the config and pins file that the find script writes (the D 18.5 driver had them as constants); the source state in the worktree is checked against its pinned blob.
- **The output tag** `l1kc79W19m1025` (the D 18.5 tag `l1kc79Wm1025` has its record in the same `data/`).
- **The coordinator** t5 in the hc and in the watcher (the D 18.5 ones had t2j).
- **No chain to the scan:** the regrid driver ends with the verdict and an hc; the scan driver is started by hand with the window.
- **The k_c 71 source record's D 19 numbers** (|F|, steps, constraint, Delta) are added to the summary line, for the post.
- **The scan driver** takes the comma-separated window as its argument (at least two distinct values in (0, 10), else it refuses), with a `--dry` mode that runs the checks and prints the planned command; after the scan it runs xfkappa's `d18f_read.py window 19 LO HI` and sends the reader's change lines to t5 as printed, with no reading of my own (`read_kc79_1025.py` and its k_c 63 and 71 constants belong to D 18.5). Tested: five bad windows refused (`selftest_scan_dry_1025.txt`), the dry run through the WMI launcher with the quoted window, the regrid driver's cap selftest (`kc79_regrid_driver_selftest.log`).

## Run

Started outside my terminal as at D 18.5: `Win32_Process.Create` of `cmd.exe /c start_kc79d19_regrid_1025.cmd` (BelowNormal, one python process tree, 4 threads), which starts the driver, its sampler and its alert-only watcher (free physical memory every 15 s, one hc alert to t5 below 1 GB, at most every 30 min, kills nothing). The scan is started only on t5's window: `start_kc79d19_scan_1025.cmd "L1,L2,..."` the same way, 8 h cap.

## The source that landed (found by the waiter at 11:20:08 UTC; `prep_kc79d19_find_1025.py` exit 0)

| item | raw path | blob |
|---|---|---|
| win2's k_c 71 D 19 state (leap) | `I1025-win2/kc71_leap/states/sol_l1kc71Lw1025_D19.0000.npy` | f320a4c14208a5bc49a09242f3aadfbcfa3579f7 |
| its record (all leap points; the D 19.0 line is used) | `I1025-win2/kc71_leap/states/l1kc71Lw1025.jsonl` | b60528cd4702e361229636070ad8dbd99c7cf608 |
| win2's acceptance check | `I1025-win2/kc71_leap/kc71_syscheck.py` | 4cd86cd4c9001d7472fc5df625b0635e1884bf81 (equal to `kc71_d185/`'s) |
| win2's README (the leap, for reference) | `I1025-win2/kc71_leap/README.md` | 2da802bd32e6e3205866eb62b91eb78d4233a62d |

The k_c 71 source record at D 19: |F| 2.7620e-10, 2676 steps, constraint 1.592e-3, Delta 1.067771890015 (F_start 5.038e-05, the leap step's 1272 s). **win2's `kc71_syscheck.py` accepts it on this machine** (`control_kc71_syscheck.txt`: the state's |F| 2.7629e-10, `freeze_from` gives 2676 steps = the record's, both controls refused), and the selftest of `kc79_syscheck_1025.py` passes (`selftest_syscheck79.txt`). The pins and config are `prep_kc79d19_pins_1025.txt` and `kc79d19_cfg_1025.txt`.

## Status

The regrid started 11:20:27 UTC, outside my terminal (`Win32_Process.Create` of `cmd.exe /c start_kc79d19_regrid_1025.cmd`; chain cmd 8264 <- driver 16988 and 20268 <- `ell_refine.py` 20304 and 18948), BelowNormal, 4 threads, cap 21600 s; free memory 24.1 GB, cpu 23% before the start, the I129 jobs of the other project beside it (t5: inside the 6-thread budget; no hold). The scan is not started (t5 gives the window). Pushed 2026-11-22 11:21:36 UTC.

## Result

Not yet run.
