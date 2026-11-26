# I1098-mm5/ladder/D300: D 300's tail from fix6's D300_mob6 state, Moebius a 8, ks 600, M 32 (#1098)

Part of `../` (recipe v1). Run from `../inputs/S300_D300_mob6_h13.npz` (Delta 1.678171015400871567861054353749636973374) by `release_ls --harm 15,...,31 --kmax 31 --jac_by 15:qq,... --res od --ddelta 1e-25 --threads 4 --outer 8 --commit 478e9d86`
on fastmul6 (d368a0c0 kernel, Python 478e9d86); `tail/rls.log`, `tail/release_ls.jsonl`, the states after each harmonic.

## Stopped (2026-11-26 16:32 UTC) at h23, on the coordinator's order

Stopped by hand, with SIGTERM to the `timeout` pid 39971 (python 39972), after 21 min 36 s. Reason: at h23 the inner solve floors at **1.36e-42 against the target 4.24e-53**, after the pending -3.89e-22 step was taken (lam 1: `inner floor in 3 steps (|F| 1.36e-42)`,
202 s; lam 0.5: 8.12e-44, 355 s), the same signature as D 1000 at M 32 (inner floor 1.71e-40 against 2.77e-46), which M 48 removed. The M 48 comparison is `../D300m48/`.

Values kept (by script from `tail/rls.log`'s digits): h15 **-7.1514e-17** (233.4 s; released at outer 1, pending +9.79e-32), h17 **-3.6311e-19** (180.7 s; pending -6.84e-35), h19 **+1.6278e-21** (180.9 s; pending +2.14e-35), h21 **+1.4486e-23**
(141.6 s; pending -9.50e-34); total through h21 -7.18754e-17, Delta 1.678171015400871495985657143659770710284. h23: not released (pending dDelta -3.89e-22 at outer 0; two trials, both floored). h25-h31 not reached.
