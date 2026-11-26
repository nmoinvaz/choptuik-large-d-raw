# I1098-mm5/fix6: D 300 and D 1000 re-solves and the D 1000 M 48 tail on fastmul6, exact 1/k and d/dtheta remainders (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The jump agent's fastmul6 tests (relayed by coordinator t5), with `tools/fix6_mm5.sh` (blob 9c3af9c8510914169bdfd6d4c3441d58b8652224, raw ef8bd0cb `I1098-mac-a/tools/`, verified with `git hash-object --no-filters`).
Kernel: `~/Source/fastmul6-site` (d368a0c0: exact 1/k and the d/dtheta matrices' f64 remainders); Python: `~/Source/choptuik-fastmul6/hp` at f1b3cb8b (taylor_mp_check now uses the solver's own matrices, hi + lo + c when the remainders are on;
horizon_mp_check.py added; Python only, no rebuild). Settings: HP_EXACT_RECIP=1, HP_EXACT_DMAT=1, HP_HORIZON_RELAXED=1, qq Jacobian, od residual, tol 1e-48.

## Bars, written before the runs (2026-11-26 15:03 UTC; relayed by the coordinator)

1. **taylor_mp_check at D 300**, with HP_EXACT_DMAT=1 and with 0: both must PASS, and the first must print "hi + lo + c".
2. **D 300**: D300_mob6 - D300_u6 **below 1e-23**. D300_u6's change from its start should be **+1.288e-19** (plus about 2e-32) and D300_mob6's **+1.289e-19**. If the gap stays at 3.2e-21, the row-sum reading is wrong.
3. **D 1000**: D1000_base6's change is the remainders' effect by a direct re-solve; dmat_perturb predicts **+1.212e-24 within 1%**.
4. **M 32 -> 48 at kfree 13**: D1000_M48_6 minus D1000_base6, against fastmul5's **-8.40e-25**.
5. **The tail** (D1000_M48_tail6, h15..h31 from D1000_M48_6's state): each harmonic's change, beside the old m48_1000 numbers (h17 shift +1.39e-19, h19 +1.21e-19, h21 -3.48e-21, h23 -1.51e-21).

Stop rules: an exception, the floor stop, or an outer step 3x its harmonic's first. Reported: the two check lines, then each run's change and the verdicts as they land (all differences by script from the logs' digits).

## Inputs (`inputs/`, blobs verified) and runs

| file | from | blob |
|---|---|---|
| D300_full_base.npz | I1098-mac-a/budget300_src | 569779b213ca7334c01417ae53b7389863220cc9 |
| D300_full_mob8,ks=600.npz | I1098-dh610/budget300_src | b8e2b0008c7cca3c1ad4102888eddb2499045341 |
| D1000_base.npz | I1098-dh610/fix/D1000_base/release_ls_h13_D1000.0000.npz | 57af5b81bf3f21bb583bbbd6773bb0a4e28a6fbc |
| D1000_M48.npz | I1098-dh610/fix/D1000_M48/release_ls_h13_D1000.0000.npz | a3735a1f1f1c756bdd6f143a54e273c0d681b428 |

`bash tools/fix6_mm5.sh inputs <this folder>`, detached, nice 10: first the two taylor_mp_check runs; then together on 16 threads D300_u6 and D300_mob6 (3 threads each, 1 h cap), D1000_base6 (4, 3 h) and D1000_M48_6 (6, 3 h), all
`release_ls --harm 13 --kmax 13 --jac_by 13:qq --outer 8`; then D1000_M48_tail6 from D1000_M48_6's state (`--harm 15,...,31 --kmax 31`, qq for each, 16 threads, 12 h cap). The script logs no kernel path, so each run's `rls.log` starts without a
`hpkernel` line; the kernel is the `PYTHONPATH=~/Source/fastmul6-site` one set in the script (checked: `fastmul6-site/hpkernel/__init__.py`).
