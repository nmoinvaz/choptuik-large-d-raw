# I859-winb: sigdss's arms a, b, c, e of #846 walked to convergence, and Delta's width

Machine: winb (Surface Laptop 4, Windows 11, Python 3.14.10, numpy 2.5.4, scipy 1.18.1). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/859. Code: main cf479ad5 (`solver/matter/sigdss_band.py`), worktree
`choptuik-i859`. Inputs: `I846-winb/sigdss_sol_ref_i846{a,b,c,e}_D*.npy` (raw eea37726, read from raw main ae203bd5) and
`solver/matter/data/sigdss_m1up.npz`, `sigdss_m1up_part6.npz`. Below-normal priority, `OPENBLAS_NUM_THREADS=3`, two
walks at a time (arms a then b in one pipeline, c then e in the other). Launchers: `run859a.sh` (the four widths) and
`run859w.sh` (the walks and the width at each walk's end, given the arms as arguments); `exits_859.txt` has each step's
exit code and UTC time.

## Stage 1: the widths at the march's states and the control (2026-11-15 21:52 UTC)

All four exit 0, and in each the two g (SVD and solve) agree to 1e-6.

| state | Delta | \|F\| | g | W = g\|F\| | Newton's Delta step | Mac (issue): g, W, step |
|---|---|---|---|---|---|---|
| march D 8 | 1.022509370 | 2.845e-14 | 8.2385e+04 | 2.344e-09 | +7.878e-10 | 8.24e4, 2.2e-9, -1.1e-10 |
| march D 9 (no prior) | 1.026904414 | 5.305e-13 | 3.4618e+05 | 1.837e-07 | +5.177e-09 | 3.46e5, 1.9e-7, +1.3e-8 |
| march D 10 (prior 1e-8) | 1.026141550 | 4.120e-09 | 1.6284e+06 | 6.710e-03 | -4.414e-03 | 1.63e6, 6.7e-3, -4.4e-3 |
| control, D 9 with `--mutate dcol` | 1.026904414 | 5.305e-13 | 3.4618e+11 | 1.837e-01 | +5.177e-03 | 3.46e11 |

The control's g is 1.000e+06 times the unmutated D 9 one (bar 1e5). The g and W agree with the Mac's at all three
states. Newton's step at D 8 and D 9 differs from the Mac's (a different sign at D 8, 5.2e-9 against 1.3e-8 at D 9); both
|F| are at 1e-13 to 1e-14, where the step is below W and set by the direction of the rounding in F.

## Stage 2: the walks
Walk a (D 9, kc 15; 21:52:50 to 21:59:21 UTC, 391 s, exit 0): stopped by the 1e-9 rule after 49 Jacobians, with Delta
1.026906208730 (-1.77e-04 from the kernel's 1.02708332095, +1.79e-06 from the march's 1.026904414), |F| 1.5769e-10,
last change -7.3e-10. The changes fell from 7.6e-06 (jac 0) through 8.9e-08 (jac 29) and 4.7e-09 (jac 46), and the
last two were -9.5e-09 and -7.3e-10. Width at its end (exit 0, the two g agree): g 3.4614e+05, W 5.458e-05, Newton's
Delta step -1.841e-06, which would put Delta at 1.02690437. So by the pre-registered definition (last change below
1e-9 and W <= 1e-6) it has not settled, W being 55 times the bar.
(walks b, c, e follow)
