# I1098-mm5/fix6/m64_1000_6: D 1000 at M 64 on fastmul6, from tail6b's M 48 state after h23 (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Coordinator's order (2026-11-26 18:28 UTC): the M 64 rerun at D 1000 on fastmul6, for the D 1000 record's `err_xcheck_M`. It decides whether M 48 is enough at D >= 1000. D 747 (started 18:27:30 UTC with D 622) was stopped 15 s later, 18:27:45 UTC, on the coordinator's amendment (`../../ladder/D747/README.md`); its 6 threads are these.

```
cd <fix6>; bash tools/m64_1000.sh D1000_M48_tail6b/release_ls_h23_D1000.0000.npz <fix6>/m64_1000_6 6
```

`tools/m64_1000.sh` (raw 5d4e3f178 `I1098-mac-a/tools/m64_1000.sh`, blob 94dfb87a3165e5774b87c30632069fb4ca7f717a, verified) with `resample_m.py` (blob 4de5c3174ad1bad3a5a311f909db9d3ecec64b5b, verified) beside it in `../tools/` (absolute paths because the script changes directory).
Input: `../D1000_M48_tail6b/release_ls_h23_D1000.0000.npz` (tail6b's M 48 state after h23, blob 5cc180ce542def0a7541ec8b602cc1d0556562a6, verified), resampled to M 64, then `release_ls --harm 23,25,27,29,31 --kmax 31`,
qq Jacobians, od residual, tol 1e-48, tol_h 1e-44, --ddelta 1e-25, 6 threads, `timeout 8h`, nice 10; fastmul6 (Python 478e9d86, kernel `~/Source/fastmul6-site`).

## Bars, written before the run (coordinator's order)

- h23's re-converged Delta at M 64, against tail6b's Delta after h23 (**1.654240854145891716456558423843881519051**), gives `err_xcheck_M` at kfree 23.
- The final Delta, against tail6b's final (**1.654240854145891716456558423843881519051**, the same number: its h23-h31 were released without a step), gives it at kfree 31.
- **Both shifts below 1e-25: M 48 suffices for D <= 1000.**
- The old fastmul4 shift was +7.0e-22, from a kernel with dd 1/k and a dd matrix.
- Stop and report on an inner stall or an outer step 3x its harmonic's first.
- Expected time 1-2 h (the old run took 590 s per M 64 outer step on 9 threads).

Reported: both shifts (by script from the logs' digits), the final Delta, each stage's time; pushed at the end.

## h23 done (snapshot pushed 2026-11-26 18:52 UTC; the run goes on to h25..h31)

By script from `rls.log` (the digits of its Delta lines): resampled to M 64 at 18:28:43 UTC; **h23 outer 0** (883.4 s) re-converges every lower harmonic at M 64: trial lam 1 converged in 1 step (|F| 6.29e-50), Delta **1.654240854145891716456558423843881922324**,
which is tail6b's after h23 (1.654240854145891716456558423843881519051) **+ 4.03273e-34**: `err_xcheck_M` at kfree 23, applied. **h23 outer 1** (about 424 s): harmonic step 6.85e-15, pending dDelta **+1.35e-27**, released (below --ddelta, not applied); tail6b's own h23 pending at M 48 was +2.43e-27.
Bar (both shifts below 1e-25, so M 48 suffices for D <= 1000): met at kfree 23. The old fastmul4 shift was +7.0e-22. No stall, no outer step above 3x its harmonic's first.
Files here: `h23_M64.npz` (the resampled input), `release_ls_h23_D1000.0000_step.npz` and `release_ls_h23_D1000.0000.npz` (the h23 states), `release_ls.jsonl`, `rls.log`, `run.log`, `resample.log` (snapshots; the live files continue with h25).
