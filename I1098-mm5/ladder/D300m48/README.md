# I1098-mm5/ladder/D300m48: D 300's tail at M 48, does M 32 cause the turn at h23? (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The coordinator's test (relayed from the jump agent), queued to start when `../D300u/` ends, on its 4 threads. The M 32 Moebius tail (`../D300/tail/`) stops falling at h23: h21 +1.4486e-23, then a pending step of -3.89e-22 at h23. This run: the same start (fix6's D300_mob6 state, `S300_input.npz`,
blob f6d3aa9a2fc4451656bd0e1b146a71aac48b6409) resampled to **M 48**, then `release_ls` over h13..h31 with the qq Jacobian for each, kernel `~/Source/fastmul6-site`, Python `~/Source/choptuik-fastmul6/hp` at 478e9d86, HP_EXACT_RECIP=1, HP_EXACT_DMAT=1, HP_HORIZON_RELAXED=1,
`--res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 4 --outer 8 --commit 478e9d86`, `timeout 4h`, nice 10. `tools/resample_m.py` blob 4de5c3174ad1bad3a5a311f909db9d3ecec64b5b (verified).
h13 first re-converges the resampled state at M 48: its change is the M 32 -> 48 shift at kfree 13 on fastmul6, **expected below 1e-25**.

## Bars, written before the run (2026-11-26 16:30 UTC; relayed by the coordinator)

- **M is the cause** if the M 48 tail keeps falling through h23 and past it: h21 near **+1.4e-23**, h23 at most a few **e-25**, and no **-3.9e-22** pending at h23. The M 32 values for h15..h21 should then agree with M 48's within about **1e-23**; a larger gap is a second M term.
- **It is not M** if the M 48 tail also turns at h23.

M 32 values to set beside (the Moebius tail, by script from its log): h15 **-7.1514e-17**, h17 **-3.6311e-19**, h19 **+1.6278e-21**, h21 **+1.4486e-23**, h23 pending **-3.89e-22**.
Reported: the h13 shift, each harmonic's change beside M 32's, and the verdict (by script from the logs' digits).
