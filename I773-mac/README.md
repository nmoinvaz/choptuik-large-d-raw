# I773-mac: the two-endpoint zero law with 1/x corrections on planted zeros (P1, P2, control C) out to |x| = 40

Machine: mac (Apple M5, the coordinator's Mac), agent xfchecks, one process at nice 10. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/773 (pre-registration and its amendment in the issue's comments).

Code: `solver/harmony/stokes/stokes_series.py` of choptuik-large-d, branch wip/i773 (venv-314: Python 3.14.7,
mpmath 1.3.0, python-flint 0.9.0), run from `solver/harmony/stokes/`.

## Files (in the order run)

- `selftest.log`: `stokes_series.py selftest` (an arm of a known order-3 law: N = 3 recovers x0 to 4.6e-57, N = 2
  misses by 5.6e-4, a mislabelled zero by 4.6; exit 0) and its control `--mutate=nolog` (the q ln x column replaced;
  N = 3 misses by 0.43; exit 1).
- `zeros_200_first_c_imprecise.log`: the first zero search. Its completeness check fired for C (46 zeros found,
  winding 87): C = P1 (x - x0 - d)/(x - x0) was built from a 60-digit x0, and the division leaves a term
  eps sum x^n/x0^(n+1), eps = S(x0), that grows like (|x|/|x0|)^200. Fixed before any fit by refining x0 to 320 digits
  and building C there (`refine_root`); no JSON kept.
- `zeros_200.json`, `.log`: `zeros --nser=200`, zeros of P1, P2, C (d = 1), C0 (d = 0) in Omega = {|x| <= 46,
  Re x >= 2}, each count equal to the winding on the boundary (37, 29, 37, 37; exit 0).
- `zeros_300.json`, `.log`: the same with 300 terms (10, 9, 10, 10 zeros: the other 27 of P1's 200-term zeros in Omega
  are truncation zeros, none on the arm).
- `checks.json`, `.log`: arm zeros x0..x7 at 200 against 300 terms (largest shift 6.3e-17, P2 1.2e-19); S by
  quadrature (P1) and Kummer functions (P2) at x7: |S|/|S'| 6.3e-17 and 1.2e-19 (bound 1e-8; exit 0).
- `fit.json`, `.log`: the pre-registered test (exit 0, decisive at X = 35).
- `posthoc_w.json`, `.log` (post hoc): P1's e at x0 by order for the arc family at w = 1.09, 1.10, 1.11.
- `sensitivity.json`, `.log` (post hoc): |d x0_hat / d x_j| of the order-N law, P1 and P2.

## Results

Pre-registered (fit.log): P1's arm zeros lie at |x| = 13.5, 18.0, 22.3, 26.4, 30.5, 34.6, 38.6, 42.6, so the rule gives
N = 1, 3, 4 at X = 30, 35, 40.

| X | N | e1 (P1) | e2 (P2) | C: abs(x0_hat - (x0 + 1)) vs 3 e1 | C0 (d = 0) | decisive |
|---|---|---|---|---|---|---|
| 30 | 1 | 0.359 | 0.016 | 0.769 vs 1.078, does not fire | does not fire | no |
| 35 | 3 | 0.0117 | 0.0020 | 1.006 vs 0.035, fires | does not fire | yes |
| 40 | 4 | 0.132 | 0.0010 | 0.868 vs 0.397, fires | does not fire | yes |

Post hoc, e at x0 by order N (law on x1..x_{N+3}):

| N (outermost zero) | 0 (22.3) | 1 (26.4) | 2 (30.5) | 3 (34.6) | 4 (38.6) | 5 (42.6) |
|---|---|---|---|---|---|---|
| P1, w 1.09 | 0.509 | 0.362 | 0.222 | 0.0062 | 0.131 | 0.202 |
| P1, w 1.10 | 0.504 | 0.359 | 0.222 | 0.0117 | 0.132 | 0.207 |
| P1, w 1.11 | 0.498 | 0.357 | 0.222 | 0.0178 | 0.134 | 0.212 |
| P2 | 0.077 | 0.016 | 0.0045 | 0.0020 | 0.0010 | 0.0006 |

- P1's error is not monotone in the order: it dips at N = 3 at all three w and rises after. So the law's order has
  to be fixed (N = 3 on x1..x6), not taken as high as the zeros allow. P2's error falls at every order.
- With exact zeros, C's arm beyond x0 equals P1's (difference 0), so C fires whenever e1 < d/4. It checks the code
  path and adds no information beyond e1.
- Amplification (sensitivity.log): the N = 3 law's |d x0_hat / d x_j| for P1 is 81, 698, 2230, 3330, 2370, 646
  (sum 9.4e3). Errors in x1..x6 must stay below about 0.15 / 9.4e3 = 1.6e-5 (all aligned) to keep their effect on
  x0_hat below 0.15. #357 found its K = 40 sums give zeros to |x| about 26 with spread 0.02.

## Recommended tasks (#773)

1. **The K at which Borel-Pade zeros of P1 reach 2e-5 out to |x| = 35.** What: sum P1's exact sigma_0..sigma_K (with
   the data's 1e-14 relative noise) by Borel-Pade as #357 did, at K = 40, 60, 80, 100, and measure the errors of the
   arm zeros x1..x6 and the N = 3 law's x0_hat against the exact ones (`stokes_series.py` and `stokes_lines.bp_predict`
   on planted coefficients only). Why: the corrected law decides on exact zeros at X = 35, but it amplifies zero
   errors by about 1e4, so #357 section 5.3's estimate K = 1.5 X = 52 does not settle the amplitude run's order.
   Acceptance (can fail): a K at which every sum that enters gives e1 <= 0.15 with the d = 1 control firing on the
   summed coefficients, or the verdict that K = 100 does not suffice. Control: K = 40 must fail (its spread at
   |x| = 26 is 0.02). Depends on: #773. Estimate: a few hours on one core.
