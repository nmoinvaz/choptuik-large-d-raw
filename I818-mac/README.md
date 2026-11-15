# I818-mac: lam_g's own series at the fold, typed by singularity_type.py's estimators beside Delta's

Machine: the coordinator's Mac (Apple M5), agent xfkappa. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/818.
Code: `hp/lam_singularity.py`, registered at wip/xf-818 9791a4e8 (the rule posted on the issue at 2026-11-15 04:12 UTC,
before the real series were typed); the post hoc `posthoc` command added at 64ffa4fb. Input: `I603-win2/chain_nsr` jets at
raw f65c5e43, 42 bases from D 258.7829 to 259.8184, each with its state. One process at nice 10.

## Runs

- `control.log`: lam_g's series construction. Order 0 against each base state's lam_g, 2.2e-199; the full product
  against lam_frontier.lam_jet at the next prediction's a, 2.7e-199 (bounds 1e-60), exit 0. `control_mutate.log`: with
  n in place of n - 1, both 1.1e-4, exit 1.
- `singularity_type_planted.log`: `singularity_type.py planted` as it stands, exit 1 (its contaminated plants at s 1.17
  fail its 10% bar, as its docstring records since #782; the clean and near plants pass).
- `planted.log`, `planted.json`: the plants of lam_g's size at each base, 39 of 42 discriminate, PASS.
- `real.log`, `real.json`: lam_g's and Delta's series, 26 discriminating bases meet the criterion.
- `posthoc.log`, `posthoc.json`: the fold's coefficient from orders 16-24, plants first.
- `rerun.log`: the three commands rerun from hp/ as notes/LARGE_D_WALL.md quotes them, each JSON byte-identical.
- `check_numbers.log`: `check_numbers.py --selftest` at wip/xf-818 64ffa4fb, 1924 of 1924, selftest 1924 of 1924.

## Result

Criterion (the issue's): both estimators put D* within 0.01 of 259.9033 and mu in [0.25, 0.75]. A base discriminates
when the square-root plant meets it and the pole plant and the moved plant (every singularity 0.5 further) do not.

| | bases | ratio D* | ratio mu | Dlog D* | Dlog mu |
|---|---|---|---|---|---|
| lam_g, meeting | 26 (259.4928-259.8184) | 259.9028-259.9033 | +0.508 to +0.551 | 259.9035-259.9057 | +0.252 to +0.405 |
| Delta, same bases | 26 | 259.9029-259.9033 | +0.504 to +0.541 | 259.9033-259.9037 | +0.466 to +0.489 |

- Verdict: "a square root at D 259.903" (26 >= 4).
- Delta meets at 36 of the 39 discriminating bases, from 259.1618.
- lam_g at 259.367-259.472: ratio meets, Dlog mu +0.196 to +0.234 (below the band). Below 259.33: Dlog pole at
  259.77-259.82, mu +1.3 to +1.8.
- The plants' Dlog mu is +0.49 at the meeting bases. lam_g's lower Dlog exponent is not explained. The A/10 plant gives
  a similar Dlog mu (0.31-0.37), but the post hoc amplitude is 1.4 times the full plant's, not a tenth.

Post hoc, a1 (the coefficient of sqrt(D* - D)) from c_k = a1 sqrt(s) binom(1/2, k) (-1)^k / s^k, k = 16..24,
s = 259.9033 - D0: the plants' 5e-4 and 5e-5 to a relative 9.4e-5; lam_g +6.87e-4 to +7.23e-4 at 31 bases from 259.367
(spread over k at most 2.3%); Delta +3.41e-2 to +3.52e-2; lam_g/Delta 0.0201 to 0.0206. #815's value fits left lam_g's
coefficient in 4.7e-4 to 8.7e-4.

## Recommended task

*The square root cancels in lam_g - r Delta.* What: with r = 0.0203, the ratio of the two coefficients at the same
bases, the combination's series should carry no sqrt(D* - D) term, so its leading singular term is (D* - D)^(3/2),
mu = 3/2. Why: it tests that lam_g and Delta share one branch point and one Puiseux variable, independent of the
estimators' low Dlog exponent on lam_g. Acceptance (can fail): a plant of the two series' sizes first; then at 4 or more
of the 26 bases both estimators give mu in [1.25, 1.75] with D* within 0.01 of 259.903, and with r moved by 10% mu
returns to the S band. Depends on: #818.
