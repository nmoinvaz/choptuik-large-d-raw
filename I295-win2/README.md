# I295-win2: does sigma depend on K at J 1500 (K 15 at 1.10), before a K 33 J 1500 run

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/295 (win2's recommendation in #228's summary, step 1 added by the coordinator).

Step 1 (`run_i295_step1.sh`): `amp_flint_par.py 1.10 15 1500 1280 --procs 3 --fit phys --mf 6:12` from `solver/inner_amp/` of
`D:\choptuik-large-d` at 188853c, `venv-t126` (Python 3.12.8, python-flint 0.9.0 / FLINT 3.6.0), Normal priority, no affinity, the checkout
and interpreter that made #82's and #228's files. It waits for #287 (18 threads) to end, since 18 + 3 threads exceed the machine's 20.

`compare_295.py` (`--selftest`) compares sigma_1 to sigma_6 strings of the K 15 file with #228's K 45 J 1500 file at 1.10, bit for bit, and
runs the control, the same comparison against #82's K 45 J 1500 file at 1.09, which must differ at n = 1 (exit 2 if it does not).
Reading rule, written before the run (the issue's): all six equal means sigma at interior orders does not depend on K at J 1500, step 2
(K 33 J 1500 at 1.09, 1.10, 1.11) is not run; a difference at some n <= 6 is reported with the first n and its relative size, then step 2.

## Result of step 1 (2026-11-10 07:24 UTC)

Run: started 2026-11-10 07:03:59 UTC (12 s after #287 ended), exit 0 at 07:22:48 UTC, wall 1129 s (18 min 49 s), 3 processes, `w1.10_K15.log`, `exits.txt`.
The file has 8 sigma entries (sigma_0 to sigma_7).

`compare_295.py` (`--selftest` ok), output in `compare_295_result.txt`, exit 0:
- **sigma_1 to sigma_6 of the K 15 file equal #228's K 45 J 1500 file at 1.10 bit for bit** (re and im strings, all six pairs in the output). So do
  sigma_0 and sigma_7 (the run's last entry, which the issue leaves out of the comparison).
- The control, the K 15 file against #82's 1.09 K 45 J 1500 file, differs at n = 1 (and at n = 2 to 6): the comparison can fail.

Reading rule (the issue's, written before the run): sigma at interior orders does not depend on K at J 1500, step 2 (K 33 J 1500 at 1.09, 1.10, 1.11)
is not run. `jstep_295.py` (`--selftest` ok, output `jstep_295_result.txt`) gives the J steps at n = 6, 7, 15, 16 from the existing files (K 33 J 1000 of
T155-win2 and I202-win2, K 45 J 1250 of I213-win2, K 45 J 1500 of I82-win2): at all three nodes the whole gap is the J 1000 to J 1250 step, and the
J 1250 to J 1500 step is at most 9.4e-17 relative (n = 16, 1.09), at 1.10 2.3e-17 (n = 15) and 4.9e-17 (n = 16).

No crash, WHEA, Kernel-Power 41, BugCheck or Application Error event since the watchers' restart at 23:44 UTC on 2026-11-08 (queried at 2026-11-10 07:24 UTC, 0 events).
