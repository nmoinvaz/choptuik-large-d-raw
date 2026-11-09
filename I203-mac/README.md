# I203-mac: independent check of the second zero of S1 near omega/omega_inf 1.0989, without Borel-Pade

Machine: the Apple M5 Mac (`mac`), one process under `nice -n 10`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/203

Code: `solver/independent_second_zero/` of nmoinvaz/choptuik-large-d, branch `wip/i203`.
Inputs: `I82-win2/sigF_w1.09_K45_J1500_p1280.json`, `sigF_w1.10_...` and `sigF_w1.11_...` of this repository
(commit 3e4a94f and earlier on origin/main), field `sigma_str` only.

## Planted-truth criteria (written 2026-11-08 23:07 UTC, before any zero of S1 was computed from the real data)

These are fixed here and are not changed afterwards.

- P1, crossing at 1.095. A synthetic family S(x; w) with a known zero x1(w) near x = 13.5, whose imaginary part
  crosses 0 at w = 1.095, is sampled at w = 1.09, 1.10, 1.11 as 23 coefficients sigma_0..sigma_22, each multiplied
  by (1 + 1e-12 (g1 + i g2)) with g1, g2 standard normal (seeds 1 to 5). It goes through the same code as the real
  data. Pass when, for every seed, the code's crossing w_c satisfies |w_c - 1.095| <= 0.005.
- P2, crossing at 1.15. The same family shifted so that Im x1 = 0 at w = 1.15. Pass when, for every seed, the code's
  Im x1 has one sign at all three nodes (no sign change in 1.09-1.11).
- The synthetic family has a singularity structure comparable to the data's: the same kind of coefficient growth
  (the ratios sigma_{n-1}/sigma_n growing linearly in n with complex slope), two exponential contributions whose
  interference makes the zero, and |x1| near 13.5. Its construction is described in the code's docstring.
- If either control fails, the real-data result is not reported as a test, and the cause is found first. No threshold
  is loosened to make a control pass.

## Real-data acceptance (from the issue)

The method finds a sign change of Im x1 between w = 1.09 and 1.11, or it does not. Its crossing is compared with
the claimed 1.0988-1.0989, and its x1 at 1.10 with the claimed 13.465 - 0.013i.

## Method (code `solver/independent_second_zero/`, docstrings of `lapl.py` and `second_zero.py`)

F(t) = sum n! sigma_n t^n, the Laplace transform of S at 1/t, has a finite radius. It is continued by quadratic
Hermite-Pade approximants (P F^2 + Q F + R = O(t^{p+q+r+2}), degrees 5-9, primary) and by linear Pade of F in t
(cross-check). The approximant's Taylor coefficients c~_n (n <= 220) give S~(x) = sum c~_n x^n/n!, and x1 is the
Newton zero of that series from x = 13.5. Approximants are admitted by fixed rules (`lapl.admissible`).

## Runs

- `fit_kummer.log`: the Kummer fit that sets the planted family's parameters (no zero computed).
- `dev_wp1.105_seed99.log`: development family (w_p 1.105, seed 99, not a control), used to fix the estimator.
- `v1/`: estimator v1 (code 0d352f4, primary = the 23-coefficient qhp set). **P1 and P2 both FAILED at seed 3**:
  at w = 1.11 (noise seed 2003) every 23-coefficient qhp approximant had a far singularity (growth 2.7-6.3 against
  the A2 bound 2.3), so the primary set was empty there. Seeds 1, 2, 4, 5 passed (P1 crossings 1.09500 +- 1e-5).
  The real-data step of `v1/run_all.sh` was stopped before it ran, so v1 never saw the real data.
- `v2/`: estimator v2 (code 3af9d9b), which pools the qhp sets of 21, 22 and 23 coefficients; the admission rules and
  the criteria above are unchanged. Seeds 1-5 are the controls; seeds 6-10 are extra, not seen before.

## Results (v2, real-data run ended 2026-11-09 00:27 UTC; tables in `v2/report.md`, per-approximant records in the JSONs)

Controls (seeds 1-5 are the controls named above, seeds 6-10 extra):

| control | verdict | detail |
|---|---|---|
| P1, crossing at 1.095 | pass, 10/10 seeds | crossings 1.09499-1.09500 (error <= 8e-6), max x1 error 1.5e-4 |
| P2, crossing at 1.15 | pass, 10/10 seeds | Im x1 medians +0.436, +0.361, +0.286 (true values to 1e-4), no sign change |
| mutation, partial sum only (`mutate_truncate.py`) | fires | zeros near 8.5-0.6i, no crossing, P1's criterion fails |
| stress, eps 0.3, w_p 1.10 (information only) | crossing 1.10000 | error <= 5e-6, 3 seeds |

Real data (primary set = 52 qhp approximants at each node, all 52 admitted at all three nodes):

| w | x1 | +- (half-range over approximants) |
|---|---|---|
| 1.09 | 13.40094 + 0.10383i | 7.8e-4, 1.3e-3 i |
| 1.10 | 13.46562 - 0.01372i | 7.4e-4, 1.1e-3 i |
| 1.11 | 13.52899 - 0.13216i | 6.9e-4, 1.0e-3 i |

Im x1 changes sign between 1.09 and 1.11. The crossing (quadratic through the medians) is 1.09884, with envelope
1.09873-1.09894 over the degree spread, and all 52 approximants' own crossings lie in 1.09875-1.09894. The order sets
give 1.09884 (23 coefficients), 1.09884 (22) and 1.09880 (21). The Laplace-plane linear Pade cross-check gives
1.09894, envelope 1.09863-1.09923. The +- values are spreads over approximant choices, not error bounds.
