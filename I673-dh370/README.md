# I673-dh370: why the 0.975 start's first Newton step is 3e34 times its residual, near_null at both layouts and the other last-node rules (the dh370 run of #673)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB. Run at `nice -n 10`, 12 threads, `OPENBLAS_NUM_THREADS=1`, no memory guard.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/673 (recommended by #654, whose start and logs are in I654-dh370/).
Code: choptuik-large-d main at 37c7955c, worktree `choptuik-large-d-654` (as for #654), run in the venv of `choptuik-large-d-614` (the 3c35f0c build, multishoot 1.2.2, multidouble 4.2.1).
Start states: `I654-dh370/start/start_0975.npz` (the `--last horizon` renode of S, as #654 left it) and S = `I603-win2/chain/anm_pin3_D252.2497.npz`, both read in place.
