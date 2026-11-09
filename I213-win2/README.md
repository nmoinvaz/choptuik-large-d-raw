# I213-win2: sigma_18 to sigma_22 at K 45 with J 1250, against J 1500, at omega/omega_inf 1.09, 1.10, 1.11

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/213.

`run_i213.sh` runs `amp_flint_par.py <wf> 45 1250 1280 --procs 3 --fit phys --mf 6:12 --fit-step 1` at the three nodes at once
(9 worker processes, as #82 ran J 1500) on Python 3.14.10 (`venv-t177`, python-flint 0.9.0, FLINT 3.6.0), Normal priority,
no memory guard, beside #202 and negative-mass's jobs. The J 1500 files are `../I82-win2/sigF_w<wf>_K45_J1500_p1280.json`.
Acceptance, from the issue and written before the run: max |sigma_n(J 1250) - sigma_n(J 1500)| / |sigma_n| for n = 18 to 22 at
each node, against 1e-10.

## Results (2026-11-09 15:30 UTC)

The three nodes ended with exit 0 (`exits.txt`): w 1.09 after 47 402 s (15:28:42 UTC), w 1.10 after 47 471 s (15:29:51), w 1.11 after
47 472 s (15:29:52), started 02:18:40 UTC. Each: `--procs 3`, K 45, J 1250, 1280 bits, `--fit phys --mf 6:12 --fit-step 1`; products
about 7400 s, fits about 39 900 s. `compare_213.py` (`compare_213.log`, exit 0; its selftest ok): max over n = 18 to 22 of
|sigma_n(J 1250) - sigma_n(J 1500)| / |sigma_n| against `../I82-win2`, from the 20 stored digits, against the limit 1e-10:

| node | n 18 | n 19 | n 20 | n 21 | n 22 | max | limit / max |
|---|---|---|---|---|---|---|---|
| 1.09 | 2.72e-16 | 3.73e-16 | 3.20e-15 | 1.16e-14 | 4.07e-14 | 4.07e-14 | 2.5e3 |
| 1.10 | 1.76e-16 | 2.16e-16 | 7.21e-16 | 1.10e-15 | 4.40e-15 | 4.40e-15 | 2.3e4 |
| 1.11 | 1.73e-16 | 4.11e-16 | 6.46e-16 | 4.62e-15 | 1.66e-14 | 1.66e-14 | 6.0e3 |

For context, n = 1 to 8 (1.10: to 8, 1.09 and 1.11 also n = 9 or 10) are equal to all 20 digits, and the maximum over n = 7 to 17 is 9.4e-17
(1.09), 1.2e-15 (1.10) and 1.6e-16 (1.11). `sigma_err` is `inf` in both J files, as in #82.
