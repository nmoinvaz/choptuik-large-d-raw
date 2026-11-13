# I611-dh370: the D 54.996085 polishes of #611, by double-double continuation (scan_hp.py) then quad-double polish (scan_qd.py)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/611
Code: choptuik-large-d main at be8bfb18818352f18b1c9020d526dccbbabf687f, worktree `choptuik-large-d-611`; the kernel is the
build of I604-dh370/ (hp/src, hp/python, the Cargo files and the pyprojects are unchanged since e835d94).
Steps (from `hp/`, nice 10): 1. `scan_hp.py` back from `up10_D55.0351.npz` and forward from `up10_D54.0414.npz` to D 54.996085,
`--kfreeze 13`, 4 threads each. 2. Their Delta must agree to 1e-20. 3. `scan_qd.py` at D 54.996085 from the back state with
`--kfreeze 13` and `--kfreeze -1`, 3 threads each. 4. The cut's effect against win's interpolated -1.2096e-15 (I611-win/README.md).

## Files

| file | what |
|---|---|
| hp_back_tol1e-27.log, hp_fwd_tol1e-27.log | the two pilot commands of the task, as first given (default `--tol` 1e-27, `--kc 40`): both end with `start did not converge`, exit 1, no step taken. The first start of hp_fwd was lost to a typo of mine in the launching shell and run again; the log is the run. |
| hp_back.log, hp_fwd.log | the same two commands with `--tol 1e-23` added (the coordinator's second message): the start re-converges (`ok True`, 2 s), then the first step to the next D ends in an uncaught `ValueError: singular or non-finite pivot at column 0 (NaN)` from `newton_step`, exit 1 |
| diag_start_kc.log | the back start alone (D_END = its own D) at `--kc 40` and `--kc 420` (the states' own metadata): both stall at 3.4e-24 and 3.2e-24, tolerance 1e-27 |
| diag_start_verbose.log, diag_start_verbose420.log | the same with `--verbose`: the start's own residual is 6.9e-16 (kc 40) and 1.5e-16 (kc 420), the deflated Newton then falls to 4e-24 and stalls |
| diag_start_old_kernel.log | the same at kc 40 with the pre-#523 kernel and the scan_hp.py of main 80b5056 (venv of I577-dh370/): the same start residual 6.91e-16, the same stall at 2.5e-24 |
