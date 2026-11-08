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
