# I385-win2: first-order lambda files regenerated from scratch with first_order_run.py (M 1 and M 3), and their check

Machine: win2 (NATHAN-PC, Windows 11, x86-64, 20 logical cores). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/385

Code: worktree `D:\choptuik-i385` at `98736556` (`wip/i385-first-order-data`), no code changes. Python:
`C:\Users\nathan\Source\venv-md510` (numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0), nothing installed into it. One thread per process
(`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`), three processes side by side, from `solver/inner_pert` with `--fresh`
(the stored M 1 file is of an older format and cannot be resumed):

    first_order_run.py 1 --xi1=0.2   --fresh --out=<this folder>/first_order_M1_xi0.2.json
    first_order_run.py 3 --xi1=0.2   --fresh --out=<this folder>/first_order_M3_xi0.2.json
    first_order_run.py 3 --xi1=0.175 --fresh --out=<this folder>/first_order_M3_xi0.175.json

## Files

| file | holds |
|---|---|
| `first_order_M{1,3}_xi*.json`, `.log`, `.err` | the three new files, each run's log and stderr (empty, no traceback) |
| `old/` | the three stored files of 98736556, as they were before |
| `check.log` | `first_order_check.py` on the new files (exit 0, 3 of 3) and with `--mutate=ell`, `jen`, `lam1` (each exit 1, 0 of 3) |
| `check_tracked.log` | the same check on the files copied into the worktree (exit 0, 3 of 3) |
| `comparison.md`, `compare_old_new.py` | old against new, per quantity (step 3) |
| `check_numbers_selftest.log` | `check_numbers.py --selftest` in venv-md510: traceback, `No module named 'hpkernel'` (see below) |
| `run_one.ps1`, `rerun_stats/` | the launcher, and a second run of the three (same commands) for wall, cpu, memory and exit code |

## Runs

The first runs (all three started 03:19:13 UTC 22 Nov; each log ends on `wrote ...` and stderr is empty) took 12 s, 36 s and 35 s
by the script's own clock. Their launcher measured the venv's `python.exe` stub, not the interpreter, which is the stub's child
(cpu 0, 4 MB, exit code null), and it set BelowNormal on the stub after the start, so the priority of those three interpreters
is not recorded. The second run of the same three commands (03:22:03 UTC; the launcher takes the interpreter child and
inherits BelowNormal from the start) wrote files identical to the first run's (`cmp`, all three) and gives:

| run | wall | cpu | peak working set | exit code | priority |
|---|---|---|---|---|---|
| M 1, xi1 0.2 | 13.3 s | 12.55 s | 79.3 MB | 0 | BelowNormal |
| M 3, xi1 0.2 | 36.5 s | 35.56 s | 87.7 MB | 0 | BelowNormal |
| M 3, xi1 0.175 | 35.8 s | 34.94 s | 87.6 MB | 0 | BelowNormal |

cpu is about wall: one thread each. M 3 was not measured before (the Mac's M 1 took 15 s).

## Check

`first_order_check.py` on the stored files (control, step 0): exit 1, 0 of 3 files pass (relative difference 1.00 in lam1 for all
three; M 3's stored ell.Jel -65257 and -115886 against recomputed 5.1e8 and 5.1e8). On the new files: exit 0, 3 of 3
(lam1 against -ell.Jen/ell.Jel: relative differences 0, 1.9e-11, 2.6e-13; ell.Jel stored against recomputed 0, 4.6e-13, 2.6e-13).
The three mutations each exit 1 with 0 of 3 passing (`ell` 3.4e-2 to 1.5e2, `jen` 2.2e-2 to 3.1e3, `lam1` 1.00e-6 against
tol 1e-9).

## Old against new

Full table: `comparison.md`. Reading fixed before the run: x, omega, omega1, lam and lam1 within 1e-6 relative are reproduced.

- x, dx, omega, omega1, lam, lam1: reproduced in all three files, relative differences 3.6e-12 to 7.2e-8 (largest: M 3 xi1 0.175
  lam1 7.2e-8, dx 3.9e-8). The zero's residual |r| is 4e-8 (M 1), 8e-7 (M 3 xi1 0.2) and 9e-6 (M 3 xi1 0.175); the cause of the
  differences was not tested.
- M 1: **lam1_sym 1.594805 (old) against 1.685171 (new), 5.7%; lam_mismatch -0.127482 against -0.129323, 1.4%.** The old M 1 file
  is of an older format (no `jac_sv`, no `rtol`). The Mac's M 1 run from scratch gives lam1_sym 1.6851712, the same as here.
- M 3: lam1_sym and lam_mismatch change by 2.3e-9 to 3.6e-8, not a change in value.

## check_numbers.py --selftest

Not passing in this interpreter, and not because of the files: it stops at its `hopf_law` check (`hp/hopf_amp_mode.py` imports
`hp/gamma_dd.py`, which imports the Rust module `hpkernel`), and venv-md510 does not have `hpkernel`. `check_numbers.py` reads none
of the three replaced files (it reads `first_order_hier_*.json`; grep for `first_order_M` finds no use). Venvs on this machine with
`hpkernel`: venv-i1058b, venv-md491, venv-hp and others.

The coordinator then had it run with venv-i1058b's python (import only, nothing installed; one thread; worktree root, after the
commit 482adb4d that holds the new files): `check_numbers_selftest_i1058b.log`, exit 1. Last two lines: `2259 of 2262 checks
pass` and `selftest: 2262 of 2262 checks reject a value shifted by one unit`. The three failing checks are the group
`formula_refit` (0 of 3: the refit of the 4-30.2 formula against the stored Delta and gamma, `formula_all.refit_distance()`,
computed 0.0 where 1 is quoted), which does not read the three files. `first_order` (11 of 11) and `first_order_lam` (4 of 4)
pass. Reported, not fixed, not investigated.
