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

## Result, and stopped at h25 (2026-11-26 17:58:38 UTC, coordinator's order)

The run was stopped by SIGTERM to the exact pid 41632 (`timeout`; python 41633) at 17:58:38 UTC, 29 s into h25 outer 1, because its h25-h31 carry the ks 600 truncation (`../h23test/README.md`).
By script from `tail/rls.log` (Delta after each outer-0 step, differences of the logged digits). Values through h23 stand; **h25 is unconverged and not to be used** (below).

| harmonic | M 48 change in Delta | M 32 change (`../D300/tail/rls.log`) | M 48 - M 32 |
|---|---|---|---|
| h13 (re-converge at M 48) | +7.27206e-26 (o0 -1.7204e-22, o1 +1.7272e-22, o2 -6.0125e-25) | none (the M 32 tail starts after h13) | the M 32 -> 48 shift at kfree 13, a valid cross-check |
| h15 | -7.15139e-17 | -7.15139e-17 | -8.21e-28 |
| h17 | -3.63109e-19 | -3.63109e-19 | +1.11e-28 |
| h19 | +1.62781e-21 | +1.62781e-21 | +2.23e-28 |
| h21 | +1.44853e-23 | +1.44855e-23 | -2.48e-28 |
| h23 | -3.88494e-22 (outer 0, 402.3 s; outer 1 pending -1.33e-32, released) | pending -3.89e-22, inner floor 1.36e-42, no step taken | the turn is the same; the M 32 floor is not in M 48 |

- **h15-h21: M 32 and M 48 agree to 8.2e-28**, far inside the 1e-23 bar. h13's M 32 -> 48 shift is +7.27206e-26, below the 1e-25 expected.
- **Verdict, by the bars above: it is not M.** M 48 also turns at h23, by -3.88494e-22, with the harmonic-23 step 3.54e-10 as in M 32.
  `../h23test/` then showed the turn is the Moebius horizon's ks 600 truncation: at ks 800 and 1000 (and a 4, a 6) h23 takes u's step 7.45e-14 and the -3.9e-22 is gone.
- **h25 at M 48, ks 600 (unconverged):** pending dDelta +2.07e-22 at outer 0, lam 1 not converged in 4 steps (|F| 1.14e-47), lam 0.5 converged in 3 steps (|F| 3.29e-50), Delta moved by +1.0333e-22 (half the step), 911.5 s;
  outer 1 had started 17:58:09 UTC and was stopped. Total at the stop, -7.18757e-17 from the start (through h23: -7.18758e-17 from h13's start state); Delta at the stop 1.678171015400871495985372051322685117275 includes the unconverged h25 half step.
  The last converged state is `tail/release_ls_h23_D300.0000.npz`.
