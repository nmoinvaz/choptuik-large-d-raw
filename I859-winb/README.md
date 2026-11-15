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

Walk b (D 9, kc 23; 21:59:28 to 22:05:19 UTC, 351 s, exit 0): stopped by the 1e-9 rule after 14 Jacobians, with Delta
1.027051411571 (-3.19e-05 from the kernel, +1.47e-04 from the march), |F| 3.0152e-11. The changes fell from -1.38e-06
(jac 0) to -9.6e-08 (jac 12), a ratio of about 0.79 per Jacobian, and jac 13 made no step (change +1.0e-14, |F| from
3.0150e-11 up to 3.0152e-11), which is what the rule read as settled. Width at its end (exit 0, the two g agree): g
3.4715e+05, W 1.047e-05, Newton's Delta step -7.28e-07, which would put Delta at 1.02705068. By the pre-registered
definition (W <= 1e-6) it has not settled, W being 10 times the bar.

Walk c (D 10, kc 15; 21:52:50 to 22:06:48 UTC, 838 s, exit 0): stopped by the 1e-9 rule after 109 Jacobians, with Delta
1.022082021836 (-1.355e-03 from the kernel's 1.02343724954, -4.060e-03 from the march's 1.026141550), |F| 8.1629e-10 at
the last Jacobian. The changes were about -2.3e-06 per Jacobian through jac 105, then -7.3e-07, -7.3e-09 and, at jac 108,
-2.2e-14 with |F| unchanged, so again the last Jacobian made no step. Width at its end (exit 0, the two g agree): |F|
8.2668e-10 (1.3% above the walk's last, 8.1629e-10; the walk freezes the RK steps once from its starting state and
`width` freezes them from this end state, which I did not test as the cause), g 1.4949e+06, W 1.236e-03, Newton's Delta
step +5.23e-05, which would put Delta at 1.022134. By the pre-registered definition (W <= 1e-6) it has not settled, W
being 1200 times the bar.
Walk e (D 10, kc 23; 22:06:54 to 22:27:02 UTC, 1208 s, exit 0): stopped by the 1e-9 rule after 54 Jacobians, with Delta
1.023202578726 (-2.347e-04 from the kernel, -2.939e-03 from the march), |F| 1.5485e-10. The changes were about -1.0e-06
per Jacobian (-1.00e-06, -9.66e-07), and jac 53 made no step (change +4.4e-16, |F| up from 1.5471e-10), which the rule
read as settled. Width at its end (exit 0, the two g agree): g 1.4456e+06, W 2.239e-04, Newton's Delta step -5.35e-06,
which would put Delta at 1.02319723. By the pre-registered definition (W <= 1e-6) it has not settled, W being 220 times
the bar.

## Result (2026-11-15 22:27 UTC, the four walks took 34 min 32 s with two at a time)

No walk has settled by the definition (last change below 1e-9 and W <= 1e-6 at its end).

| walk | D | kc | Jacobians | s | Delta at the end | \|F\| | last change | W | Newton's Delta | stopped on |
|---|---|---|---|---|---|---|---|---|---|---|
| a | 9 | 15 | 49 | 391 | 1.026906208730 | 1.577e-10 | -7.3e-10 | 5.458e-05 | 1.02690437 | a change below 1e-9, after -4.7e-09 and -9.5e-09 |
| b | 9 | 23 | 14 | 351 | 1.027051411571 | 3.015e-11 | +1.0e-14 | 1.047e-05 | 1.02705068 | a Jacobian with no step (stall), after -9.6e-08 |
| c | 10 | 15 | 109 | 838 | 1.022082021836 | 8.163e-10 | -2.2e-14 | 1.236e-03 | 1.02213430 | a Jacobian with no step (stall), after -7.3e-09 |
| e | 10 | 23 | 54 | 1208 | 1.023202578726 | 1.549e-10 | +4.4e-16 | 2.239e-04 | 1.02319723 | a Jacobian with no step (stall), after -9.7e-07 |

The kernel's Delta is 1.02708332095 at D 9 and 1.02343724954 at D 10, the march's 1.026904414 and 1.026141550. Width at
each end: g 3.4614e+05 (a), 3.4715e+05 (b), 1.4949e+06 (c), 1.4456e+06 (e); |F| from `width` equals the walk's last
for a, b and e, and is 8.267e-10 for c (the walk's last is 8.163e-10).

| reading (the issue's), with the ends | numbers | verdict |
|---|---|---|
| D 9 same solution: a within 1e-6 of the march's 1.026904414 | a is 1.795e-06 from it; Newton's step from a gives 1.02690437 | does not hold; a not settled (W 5.5e-05) |
| D 9 truncation: \|b - kernel\| <= \|a - kernel\| / 3 | 3.191e-05 and 1.771e-04, factor 5.55 (Newton's prediction 5.4) | numbers meet the bar; a and b not settled (W 5.5e-05, 1.0e-05) |
| D 10 prior: c settles 1e-3 or more from the march's 1.026141550 | c is 4.060e-03 from it | numbers meet the bar; c not settled (W 1.2e-03, stalled) |
| D 10 truncation: \|e - kernel\| <= \|c - kernel\| / 3 | 2.347e-04 and 1.355e-03, factor 5.78 | numbers meet the bar; c and e not settled (W 1.2e-03, 2.2e-04, both stalled) |

Also seen:
- b, c and e stopped on a Jacobian that made no step (change +1.0e-14, -2.2e-14, +4.4e-16), with |F| not lower (b
  3.0150e-11 up to 3.0152e-11, e 1.5471e-10 up to 1.5485e-10, c unchanged at 8.1629e-10 after rising from 8.1610e-10 one
  Jacobian earlier), while Delta was still moving by 9.6e-08 (b), 7.3e-09 (c) and 9.7e-07 (e) in the Jacobian before.
  The rule read each as settled. Main 750f902b reports such a stop as stalled; these runs used cf479ad5.
- Walk a took 49 Jacobians where the issue expected about 120 from its first four changes (ratio 0.93).
- Newton's Delta step at the march's D 8 and D 9 states differs from the issue's Mac table (stage 1).
- Every exit 0, no traceback, and the two g agree to 1e-6 in all eight `width` runs.

Files: `width_*.log` and `width.jsonl`, `walk_?.log`, `walk_?.npy` (each end's state) and `walk.jsonl` (the per-Jacobian
history), `width_walk_?.log`, `exits_859.txt`, `run859a.sh` and `run859w.sh`.
