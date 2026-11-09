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

Exit codes are in `exits.txt`. The scripts `run_fit.sh`, `run_pilot.sh`, `run_all.sh`, `run_info2.sh` and
`run_info3.sh` are run from `solver/independent_second_zero` of `wip/i214` 895ac75. The first `family_check exit 1`
in `exits.txt` is a missing `sys.path` entry under `python -I`, fixed in 895ac75 and rerun.

- `fit_arc.txt`, `arc_fit.json`: the fit. `family_check.txt`: the family's exact zero, w_nat, the quadrature check,
  and the planted families' distance from the data.
- `pilot_*`: w_p 1.105, seed 99, not a control. Crossing error 5.9e-6.
- `P1_*`, `P2_*`: the controls. `M1_*`, `M2_*`: the mutations.
- `info_noise0_*`, `info_noise1e-14_*`: the information runs named above.
- `spread_compare.md`: the pre-set spread comparison (`spread_compare.py`).
- Added after the controls (information only, not in the criteria):
  - `info_noise3e-12_*`: the P1 family at noise 3e-12, seeds 1-5.
  - `info_noise1e-11_stdout.txt`: stopped by hand during its first node.
  - `real_sens_noise1e-12_seed1.txt`: #203's `sens_noise.py` on the real data with 1e-12 added; the later runs of
    `run_info3.sh` were stopped, and `real_sens_noise1e-12_seed2.txt` is a partial log.
  - `spread_compare_all.md`: the comparison with every run.
  - From 04:03 UTC the Mac was in clamshell and maintenance sleep (pmset log). Wall times after that are not compute
    times, and the 1e-11 stop was caused by that, not by the noise.

## Results

| control | verdict | detail |
|---|---|---|
| P1, crossing at 1.095 | **pass**, 10/10 seeds | primary crossings 1.094990-1.094997 (error <= 1.0e-5); per-node \|x1 error\| <= 1.9e-4 |
| P2, crossing at 1.15 | **pass**, 10/10 seeds | primary median Im x1 +0.5823, +0.4909, +0.3973 (true +0.58234, +0.49098, +0.39736); no sign change; P1's criterion fails on it |
| M1, partial sum only | **fires** | zeros near -3.3 + 5.4i, no crossing; exit 0 |
| M2, crossing planted at 1.105, tested at 1.095 | **fires** | crossing 1.10500, P1 fails; exit 1 |
| spread match (pre-set rule) | **does not match** | real/arc primary ratios Re 1.9, 1.6, 1.4 and Im 3.8, 4.2, 2.8; Im exceeds 3 at 1.09 and 1.10 |

On the same metric the Kummer family of #203 gives ratios of 4.9-12, so the arc family closes most of the gap. The
P1 accuracy is still not offered as the real crossing's error bar.

Spread against noise. These are primary per-node half-ranges for the P1 family, with the real data's for comparison:

| input | Re | Im | real/planted | crossing error | admitted per node |
|---|---|---|---|---|---|
| arc, no noise | 1.4e-5 | 1.6e-5 | 48-83 | 4.5e-8 | 64/70 |
| arc, 1e-14 | 5.7e-5 to 9.8e-5 | 6.6e-5 to 1.3e-4 | 7.5-20 | <= 1.8e-6 | 45-64 |
| arc, 1e-12 (P1) | 4.1e-4 to 5.0e-4 | 2.7e-4 to 3.6e-4 | 1.4-4.2 | <= 1.0e-5 | 43-69 |
| arc, 3e-12 | 6.2e-4 to 1.0e-3 | 6.6e-4 to 1.0e-3 | 0.72-2.0 | <= 1.3e-5 | 40-68 |
| real data | 6.9e-4 to 7.8e-4 | 1.0e-3 to 1.3e-3 | 1 | | 70/70 |
| real data + 1e-12 | 5.4e-3 to 8.7e-3 | 1.8e-3 to 4.0e-3 | | crossing 1.09879 | 59-64 |

Reading:
- The arc structure needs about 3e-12 of added noise to reach the real data's spread, in the pooled set and in each of
  qhp23/22/21.
- The same 1e-12 noise added to the real data multiplies its spread by about 7 and costs it 6-11 approximants per
  node. The clean data has all 70. So the real sigma do not carry random errors at 1e-12, which agrees with the fit
  plateaus' 1.3e-14.
- The real data's spread therefore comes from its structure, or from smooth errors, that no planted family here
  reproduces at the data's noise level. Without noise the arc family is about 60 times easier than the data, and
  even then it rejects 6 approximants that the data admits.

What each figure is:
- Every spread is a half-range over approximant choices.
- Every crossing error is |w_c - w_p| on a planted family, an estimator error under that family.
- None is a bound. The real crossing 1.09884 keeps #203's spread envelope 1.09873-1.09894 as its stated uncertainty,
  and that too is a spread.
