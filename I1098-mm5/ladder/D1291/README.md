# I1098-mm5/ladder/D1291: D 1291 full direct solve on the Moebius horizon, recipe v2, tail at M 48 to h31 (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Command (coordinator's order, 2026-11-26 18:03 UTC), detached, 6 threads, from the ladder folder:

```
KSBAR=1e-70 bash tools/ladder_point2.sh 1291 220 6 <ladder>/D1291 <ladder>/inputs/S300_D300_mob6_h13.npz <ladder>/inputs/S1000_D1000_base6_h13.npz 48 31
```

`tools/ladder_point2.sh` (raw a9ed0f2f `I1098-mac-a/tools/ladder_point2.sh`, blob da887d7143bf94d45d99fcd168550d0e56437370, verified; `S300` and `S1000` of the order are the two inputs of `../inputs/`, absolute paths because the script changes directory).
kc 220, the Moebius horizon a = max(8, (D - 2)/400) = 8, start **ks = ceil(1.5 (D - 2)) + 20 = 1954**, raised by 200 (at most 4 times, to 2554) until the jump's ks+200 |dF| is at most KSBAR = 1e-70 (KMAX 31 needs about 1e-70: the gain at kfree 31 is 1.5e47 at D 300).
Stages (`run.log`, each log and state in its folder): `jump/` (the held solve at M 32 from a degree-1 fit in 1/n to the two inputs, double-double solve, qd check), `rls/` (h5..h11 to tol 1e-36), `rls13/` (h13 to 1e-48, ddelta 1e-25, octo-double residual),
`tail/` (the h13 state resampled to M 48, h13 re-converged, then h15..h31, qq, od, tol 1e-48, ddelta 1e-25). fastmul6, Python 478e9d86.

## Bars, written before the run (coordinator's order)

- The jump converges, and the ks it settled on is logged.
- h5..h13 are each released, and the tail falls.
- Stop and report on any inner solve that does not converge, or an outer step 3x its harmonic's first.
- Reported: the final Delta, each stage's time and the ks used.
