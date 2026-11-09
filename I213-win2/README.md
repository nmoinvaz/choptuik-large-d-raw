# I213-win2: sigma_18 to sigma_22 at K 45 with J 1250, against J 1500, at omega/omega_inf 1.09, 1.10, 1.11

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/213.

`run_i213.sh` runs `amp_flint_par.py <wf> 45 1250 1280 --procs 3 --fit phys --mf 6:12 --fit-step 1` at the three nodes at once
(9 worker processes, as #82 ran J 1500) on Python 3.14.10 (`venv-t177`, python-flint 0.9.0, FLINT 3.6.0), Normal priority,
no memory guard, beside #202 and negative-mass's jobs. The J 1500 files are `../I82-win2/sigF_w<wf>_K45_J1500_p1280.json`.
Acceptance, from the issue and written before the run: max |sigma_n(J 1250) - sigma_n(J 1500)| / |sigma_n| for n = 18 to 22 at
each node, against 1e-10.
