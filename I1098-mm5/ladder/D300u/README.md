# I1098-mm5/ladder/D300u: D 300's tail from the u horizon on fastmul6, ks 506 (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The coordinator's test (relayed from the jump agent) to explain the gap between this ladder's fastmul6 D 300 tail (Moebius a 8, ks 600; total so far -7.19e-17, its final value not yet in: it is at h21) and the old kfree300 tail (u horizon,
old kernel; total -4.34487e-17, Delta 1.678171015400871524283476784): the same tail from the **u horizon** on fastmul6 at ks 506 (the u state ks 306 + 200).

- Start: `../../fix6/D300_u6/release_ls_h13_D300.0000.npz` (fastmul6's D 300 u state, ks 306, Delta 1.678171015400871567861061965988636601014), made into `start.npz` by `tools/variant_state.py` (blob 19b05a5a70e1b6e49f700e176a4d86c265a0ea48, verified) with `ks+200`.
- Run (from `~/Source/choptuik-fastmul6/hp`, 478e9d86): `HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=~/Source/fastmul6-site nice -n 10 timeout 3h python -u form_s.py release_ls start.npz tail
  --harm 15,...,31 --kmax 31 --jac_by 15:qq,...,31:qq --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 4 --outer 8 --commit 478e9d86`, started while the D 300 Moebius tail (4 threads) is still running, so 20 threads on 18 cores.

## Bars, written before the run (2026-11-26 16:24 UTC; relayed by the coordinator)

- **Moebius is right, and the old kernel's tail was wrong,** if the final Delta is within **1e-23** of the Moebius tail's **1.678171015400871495985642658114**.
- **The horizons differ at high harmonics** if the final Delta lands near the old **1.678171015400871524283476784**.

Note, from the logs when this was written: 1.678171015400871495985642658114 is the Moebius tail's value after h19; the tail was still running at h21 (a pending step of +1.45e-23, above --ddelta, taken), so its final Delta
will differ from that number by more than 1e-23. The comparison below is made against the Moebius tail's final value as well, both quoted.

Reported: each harmonic's change and the final Delta against both numbers (by script from the logs' digits).
