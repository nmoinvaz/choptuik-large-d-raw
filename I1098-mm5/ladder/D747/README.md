# I1098-mm5/ladder/D747: D 747 full direct solve on the Moebius horizon, recipe v2, tail at M 48 to h23 (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Command (coordinator's order, 2026-11-26 18:27 UTC; D 622 and D 747 moved from dh370 to this runner), detached, 6 threads, from the ladder folder:

```
KSBAR=1e-64 bash tools/ladder_point2.sh 747 200 6 <ladder>/D747 <ladder>/inputs/S300_D300_mob6_h13.npz <ladder>/inputs/S1000_D1000_base6_h13.npz 48 23
```

`tools/ladder_point2.sh` (blob da887d7143bf94d45d99fcd168550d0e56437370, verified; the same as D 1291's; the inputs are `../inputs/`, absolute paths because the script changes directory). kc 200, the Moebius horizon a = max(8, (D - 2)/400) = 8,
start **ks = ceil(1.5 (D - 2)) + 20 = 1138**, raised by 200 (at most 4 times) until the jump's ks+200 |dF| is at most KSBAR = 1e-64. That check is the quad-double residual's change, whose own floor read 1.2e-45 to 1.8e-45 at D 1291 (`../D1291/README.md`):
the ks the loop settles on is then confirmed by the octo-double gate `hp/ks_gate.py` (raw/main f398e829, in `~/Source/choptuik-fastmul6c`, bar 1e-64, 2 threads) on the jump state, run beside the point.
Stages (`run.log`, each log and state in its folder): `jump/`, `rls/` (h5..h11 to tol 1e-36), `rls13/` (h13 to 1e-48, ddelta 1e-25, octo-double residual), `tail/` (the h13 state resampled to M 48, h13 re-converged, then h15..h23, qq, od, tol 1e-48, ddelta 1e-25). fastmul6, Python 478e9d86.

## Bars, written before the run (coordinator's order)

- The jump converges and the ks gate passes (the ks it settled on is logged). h5..h13 are each released.
- The tail falls from h15 by about 1e2 or more per harmonic, h21's change is at most about 1e-23, and h23 is released with a pending dDelta at most about 1e-26: no turn.
- Stop and report on any inner solve that does not converge, or an outer step 3x its harmonic's first.
- Reported: the final Delta, each stage's time, the ks used; each point is pushed at its end. Times from `date -u`.

## Stopped 15 s after the start (2026-11-26 18:27:45 UTC, coordinator's amendment)

Started 18:27:30 UTC together with D 622 ( 49404), and stopped at 18:27:45 UTC by SIGTERM to the wrapper 49404 and the timeout 49434 (python 49437) on the coordinator's amendment (my launch crossed it): "start D 622 as sent, but NOT D 747. Its 6 threads take the M 64 rerun at D 1000 instead. D 747 goes back to the queue."
It was in its first jump, ks 1138, with no result; the partial files are in . The bars above stand for the later run.
