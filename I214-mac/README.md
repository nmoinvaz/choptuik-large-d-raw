# I214-mac: #203's second-zero planted controls rerun on a non-Kummer arc family fitted to the data to 1e-4

Machine: the Apple M5 Mac (`mac`), one process under `nice -n 10`, Python 3.14 (`/Users/nathan/venv-314`).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/214

Code: `solver/independent_second_zero/` of nmoinvaz/choptuik-large-d, branch `wip/i214`. The new files are
`fit_arc.py`, `arc_fit.json` and `arc_family.py`. `second_zero.py` and `mutate_truncate.py` gained `--family arc`, and
`second_zero.py` gained `--noise` and `--mutate_wshift`. The estimator itself is #203's v2, unchanged (`lapl.py` and
the summary in `second_zero.py`).
Inputs: `I82-win2/sigF_w1.09_K45_J1500_p1280.json`, `sigF_w1.10_...` and `sigF_w1.11_...` of this repository, field
`sigma_str` only.

## The family (fixed 2026-11-09 03:05 UTC, before any approximant ran on it)

S(x; w) is a Laplace integral over a curved arc, normalized to S(0) = 1:

    S(x; w) = int_0^1 e^{x gamma(s)} rho(s) ds / int_0^1 rho(s) ds
    gamma(s) = za + s (zp - za) + kap s (1 - s)
    rho(s)   = s^(al-1) (1 - s)^(be-1) (e0 + e1 s)

All seven complex parameters are linear in w, p(w) = pA + pB (w - 1.10)/0.01. They come from one joint fit to the
three nodes (`fit_arc.py`, variable projection, 30 random starts at 1.10 with numpy seed 5). The coefficients are
the arc's moments, exact at any precision. The Kummer family of #203 is the special case of a straight arc
(kap = 0) with a pure Beta density (e1 = 0). Here the arc is curved and the density has a linear factor. So the
discontinuity of F(t) = sum n! sigma_n t^n, continued in zeta = gamma(s), is not of Beta/Kummer form. It has a
square-root branch point at the critical value of gamma.

Fit quality, max over n = 1..22 of |log(sigma_model/sigma_data)|:

| w | arc family (this folder) | Kummer family (#203, `kummer_fit.json`) |
|---|---|---|
| 1.09 | 9.2e-5 | 8.5e-3 (per n 1.7e-3 to 8.5e-3) |
| 1.10 | 7.5e-5 | 8.7e-3 (per n 1.5e-3 to 8.7e-3) |
| 1.11 | 8.4e-5 | 8.9e-3 (per n 1.2e-3 to 8.9e-3) |

The requirement was better than 1e-3 per coefficient. The per-n values are in `fit_arc.txt`. (The #203 summary's
"0.2-0.9%" is this Kummer range.)

Parameters at w = 1.10: za = 0.7965 + 0.0136i, zp = 1.7104 + 1.3390i, kap = -1.4269 + 0.7454i,
al = 3.412 - 1.443i, be = 10.665 - 0.061i, e0 = 0.672 - 1.106i, e1 = -0.023 + 4.408i.

The family's own zero near 13.5 is computed exactly (series to n = 200 at 160 digits, checked against tanh-sinh
quadrature of the integral to 3e-49). No approximant is involved:

| w | x1 of the fitted family | real data, #203 estimator (for reference) |
|---|---|---|
| 1.09 | 13.43493 + 0.05484i | 13.40094 + 0.10383i |
| 1.10 | 13.50254 - 0.04904i | 13.46562 - 0.01372i |
| 1.11 | 13.56897 - 0.15525i | 13.52899 - 0.13216i |

Im x1 of the fitted family is 0 at w_nat = 1.0953069. So matching sigma_0..sigma_22 to 1e-4 does not fix x1 to
better than about 0.04. Its next zero inward is near 7.75 - 0.80i at w = 1.10.

**Planting.** The planted family with crossing w_p is the fitted one shifted in w, S_p(x; w) = S(x; w - (w_p - w_nat)).
Its zero is real at w_p exactly, and its parameters move with w as the fit does. For P1 (w_p = 1.095) the shift is
-0.0003. For P2 (w_p = 1.15) the shift is +0.0547, a linear extrapolation of the parameters, so the P2 family is the
fitted family at w = 1.035-1.055.

*Correction (03:20 UTC, from `family_check.txt`; the criteria below are unchanged).* An earlier version of this
paragraph said that the P1 family matches the data to about 1e-4 at the nodes. That was wrong. The sigma_n change
fast with w, about 7% per 0.01 at n = 22, so even P1's shift of 0.0003 moves them. The P1 family is 2.1e-3 from the
data at the nodes (max over n), and the P2 family is 0.36 from it. Any family whose crossing is moved away from the
fitted family's own w_nat must leave the data by about this much.

## Acceptance criteria (written 2026-11-09 03:05 UTC, before any control ran)

These are fixed here and are not changed afterwards.

- **P1, crossing at 1.095.** `second_zero.py planted --family arc --wp 1.095 --seeds 1,...,10`. Each sigma_n is
  multiplied by (1 + 1e-12 (g1 + i g2)), g standard normal, as in #203. Pass when, for every seed, the primary
  crossing w_c satisfies |w_c - 1.095| <= 0.005.
- **P2, crossing at 1.15.** The same with `--wp 1.15`. Pass when, for every seed, the primary median Im x1 has one
  sign at all three nodes (no sign change in 1.09-1.11).
- **Estimator.** #203's v2, with its admission rules, pooling and thresholds unchanged.
- **Mutations, which must make a control fail.**
  - M1: `mutate_truncate.py 1 --family arc` (partial sum only, no continuation). P1's criterion must fail, exit 0.
  - M2: `second_zero.py planted --family arc --wp 1.095 --mutate_wshift 0.01 --seeds 1`. The family crosses at 1.105
    while the criterion tests 1.095, so P1 must fail, exit 1.
- **Spread comparison.** The spread at a node is the half-range of the primary set's x1, Re and Im separately, as
  in #203. For each node, take its median over the ten P1 seeds. Compare it with the real data's spread
  (`I203-mac/v2/real.json`: 7.8e-4/1.3e-3, 7.4e-4/1.1e-3, 6.9e-4/1.0e-3) and with the Kummer family's
  (`I203-mac/v2/P1_wp1.095.json`). The spread **matches** when the real-to-arc ratio lies in 1/3-3 at every node, for
  both Re and Im.
  - If it matches, the planted accuracy, max |w_c - 1.095| over the P1 seeds and max |x1 error| per node, is offered as
    an error estimate for the real crossing 1.09884. That is an estimator error on a family that agrees with the data
    to 1e-4. It is not a rigorous bound.
  - If it does not match, it is not offered.
- If a control fails, the cause is found and reported first. No threshold is loosened.

Information runs, not controls:
- the P1 family with noise 1e-14 (the data's own level, `I203-mac/v2/coef_err.txt`), seeds 1-5;
- the P1 family with no noise, seed 1.

## Runs

(filled in as they finish)
