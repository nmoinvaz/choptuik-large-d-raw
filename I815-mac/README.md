# I815-mac: lam_g past D 248, the fold's square root against the 1/p_min term (plants, real fit, post hoc)

Machine: the coordinator's Mac (Apple M5), agent xfkappa. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/815.
Code: `hp/lam_fold_fit.py`, registered at wip/xf-815 92140e52 (rule posted on the issue at 2026-11-15 03:44 UTC, before
the real fit), post hoc variant added at a47017d6. One process at nice 10. Raw input: I603-win2 at 688d9bad (p_min).

## Runs

- `planted.log`: `planted RAW` at 92140e52, 12 judged plants as expected on windows N and G, PASS, exit 0.
- `planted_mutate.log`: the same with `--mutate=dstar` (D*_C judged against 259.9033 + 0.5), 8 of 12 not as
  expected, exit 1.
- `real.log`: `real` at 92140e52, the registered verdicts.
- `posthoc.py`, `posthoc.log`: the post hoc variant (fold part of degree K = 4, 5, C_even's regular part of degree 2)
  on plants PS, PW, PM and the real states, run before it was folded into the script.
- `planted_a47017d6.log`, `real_a47017d6.log`: both commands at a47017d6, from the repository root as
  notes/MODE_COUNT.md 10.6 quotes them; they write `lam_fold_planted.json` and `lam_fold.json` (copies here, the
  originals in hp/data). The registered lines are identical to `real.log`. A second `real` run gave a byte-identical
  JSON.
- `check_numbers.log`: `check_numbers.py --selftest` at a47017d6, 1883 of 1883, selftest 1883 of 1883.
- `design/`: the experiments that chose the forms, windows and thresholds, on plants only (`forms*.py`), and the
  table of delta, sigma and p_min at the states (`explore.py`, `data2.json`), seen before the rule was posted. No form
  was fitted to the real delta before the post.

## Registered result

| window | r(S) | r(W) | r(C) | r(C_even) | C_even/C | S/C | C's D* | verdict |
|---|---|---|---|---|---|---|---|---|
| N, 258.07–259.74, 40 states | 2.6e6 | 1.8e6 | 1.2e3 | 1.5e5 | 130 | 2.2e3 | 259.882 | pmin, C incomplete |
| G, 248.02–259.74, 92 states | 1.8e7 | 3.9e6 | 5.4e5 | 3.7e6 | 6.8 | 33 | 259.779 | neither, C incomplete |

r is the largest |residual|/sigma, sigma = R's spread over 10.4's kept c0 = 1 fits (6e-13 to 1.9e-12), a spread over fit
choices. On N the square root's ratio passes (130 >= 100) but D*_C is 0.021 from 259.9033 (bar 0.01). So by the rule
the fit stays capped at D 244.64 (C is not complete on G).

## Post hoc (after the registered fit)

| window, K | r(S_K) | r(C_K) | r(C_even, degree 2) | C_even/C | S/C | D* | beta | omega | odd part / max abs(delta) | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| N, 4 | 5.3e4 | 86 | 1.7e5 | 2.0e3 | 620 | 259.9071 | 1.46 | 2.48 | 44 | both, incomplete |
| N, 5 | 3.3e4 | 46 | 1.7e5 | 3.7e3 | 730 | 259.9099 | 1.58 | 2.39 | 52 | both, incomplete |
| G, 4 | 8.7e6 | 1.1e5 | 3.1e6 | 28 | 80 | 259.892 | 1.51 | 1.23 | | neither |
| G, 5 | 5.8e6 | 6.1e4 | 3.1e6 | 50 | 94 | 259.973 | 1.53 | 1.14 | | neither |

The post hoc plants (PS, PW, PM at K 4 and 5, both windows) give the expected verdicts. On N the fold's square root at
Delta's fold is then needed, but the odd and even parts cancel at 44-52 times max abs(delta) (9.22e-5), so its
coefficient is not determined. C's W has omega 2.4-2.5, against the 1.19 of #805's plant (period 5.3). The chirped
plant (W with its period lengthening 2% per unit D) also leaves C incomplete on G (2.1e4).

## Recommended task

*lam_g's own series at the fold.* What: form lam_g's series in D from chain_nsr's jets (the a_h block, as #807's test J
does) at the bases from D 258.78 on, and run singularity_type.py's ratio and Dlog estimators on them. Why: the value
fits of #815 cannot fix the square root's coefficient (the parts cancel at 44-52 times max abs(delta)), and on window N
the registered D* missed Delta's fold by 0.021; the series test the type of lam_g's nearest singularity from its
analytic continuation, with no fit form over a window. Acceptance (can fail): singularity_type's planted test passes
first, with a plant of lam_g's size; then at 4 or more bases both estimators put D* within 0.01 of 259.903 and mu in
the S band [0.25, 0.75], or the result is reported as not a square root. Depends on: #815, #807, #782.
