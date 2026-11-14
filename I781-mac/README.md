# I781-mac: box count of the D = infinity (kappa = 0) Stokes-jump determinant D(lambda) of css_inf_jump.py

Machine: mac (Apple M5, the coordinator's Mac), agent xfchecks, one process at nice 10. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/781

Code: `solver/matter/css_inf_jump.py` (main 371f0060, unchanged) and `solver/matter/css_inf_count.py` (new), branch
wip/i781 (venv-314: Python 3.14.7, numpy 2.5.4, scipy 1.18.1, sympy, mpmath 1.3.0), run from `solver/matter/`.
Box 0.05 < Re lambda < 5, |Im lambda| < 9, full boundary, initial steps 0.25, phase steps bisected to <= 0.5 rad.

## Files

- `probe.py`, `probe.log`: D at the box's corners, its left edge and +-i omega + 0.05, setting A (N 160, background
  selected by Newton). D(conj lam) = conj D(lam) at all six pairs to the printed digits; |D| runs from 41 at 0.05 to
  1.4e17 at 5 +- 9i.
- `iomega.py`, `iomega.log`: why #771's D(i omega) did not finish. At lambda = i omega the data (1, 0) is the exact
  shift mode (u = 1, v = w = 0); its series' v and w carry rounding noise from order 4 on (2e-15), and DOP853's
  absolute tolerance 1e-19 then forces steps that resolve the noise (the traceback after 60 s is in the ray
  integration's rhs). Stopped at 90 s.
- `iomega2.py`, `iomega2.log`: D(i omega + eps) for eps = 0.1 ... 1e-4, 1e-3 i, -1e-3 with the unchanged code:
  |D|/|eps| -> 3.39e4 from three directions, a simple zero. D(i omega) with the absolute tolerance raised to 1e-16
  for that point only: |D| = 7.8e-8 (at lambda = 2, 1.0e-8); the same tolerance leaves D(i omega + 0.001) unchanged to
  the printed digits.
- `selftest.log`: `css_inf_count.py selftest` (a synthetic D with e^{4 lambda} and six zeros inside, three zeros 0.02-0.05
  outside the edges: winding 6, planted 8, exit 0) and its control `--mutate=coarse` (one sample per edge: winding
  0, exit 1).
- `count_A.log`, `evals_A.jsonl` (every D evaluated), `counts.jsonl`: setting A (r0 0.1, r1 0.3, alpha 3pi/8, rtol
  1e-13, N 160): winding 4.000000000000003, largest step 0.4985 rad, 464 determinants, no bisection limit hit;
  D(conj lam) = conj D(lam) to 1.1e-9 relative over the 231 conjugate pairs of the contour; 1817 s.
- `count_A_plant.log`: the same with a pair planted at 3.1 +- 5i: winding 5.999999999999997 (20 new determinants).
- `count_B.log`, `evals_B.jsonl`: setting B (r0 0.11, r1 0.25, alpha 0.3 pi, rtol 1e-13, N 160): winding
  3.9999999999999956, largest step 0.4997 rad, 476 determinants, no bisection limit hit; D(conj lam) = conj D(lam) to
  7.7e-9 relative over 237 pairs; 2021 s.
- `count_B_plant.log`: the same with the pair at 3.1 +- 5i: winding 6.0000000000000036 (20 new determinants).

## Result

Four zeros in the box at both settings (lambda = 1, lambda = 2, the lambda_osc pair), six with the planted pair. The
code is css_inf_jump.py's D unchanged; only the counting (css_inf_count.py) is new. lambda = i omega, 0.05 outside the
left edge, is avoided by the contour and settled separately as a simple zero (iomega2.log).

## Recommended task (#781)

1. **The strip -0.05 < Re lambda < 0.05 at D = infinity.** What: `css_inf_count.py` with the box -0.05 < Re lambda <
   0.05, |Im lambda| < 9 (a `--box` option), at settings A and B. Why: neither method's count covers 0 <= Re lambda <=
   0.05 (CSS_STABILITY.md 1.4: "Not covered ... 0 < Re lambda < 0.05"), and it holds the exact zeros 0 and +-i omega,
   with the integrator's stall at i omega to avoid (the contour stays 0.05 from them). Acceptance (can fail): the
   winding is 3 (lambda = 0, +-i omega) at both settings, a planted pair at 0.02 +- 6i adds 2, every phase step at most
   0.5 rad. Depends on: #781. Estimate: about 1 h on one core.
