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
