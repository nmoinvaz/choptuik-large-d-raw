# I821-mac: the near singularities' amplitude in lam_g's and Delta's series, and whether #820's bound applies

Machine: the coordinator's Mac (Apple M5), agent xfkappa. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/821.
Code: `hp/near_amp.py`, registered at wip/xf-821 d249d737 (the rule posted on the issue at 2026-11-15 04:52 UTC, before
the real fit), the `posthoc` command at 6201e043, on main aa89aa7f. Input: `I603-win2/chain_nsr` jets at raw f65c5e43,
#818's 26 bases. One process at nice 10.

## Runs

- `kmin/planted_k{4,8,10,12,14}.log`: the plants with the fit from order 4, 8, 10, 12 and 14 (plants only, before
  the real fit): 0, 0, 1, 8 and 7 usable bases. Order 12 was registered.
- `diag.py`, `diag.log`: the fit's floor and recovery with and without the regular part, at four bases (plants only).
- `planted.log`, `planted.json`: the registered plants, 8 of 26 bases usable, PASS.
- `real.log`, `real.json`: the real fit; #820's bound does not apply.
- `posthoc.log`, `posthoc.json`: a common fold offset in plants, and the real series with D* free.
- `check_numbers.log`: `check_numbers.py --selftest` at 6201e043, 1961 of 1961, selftest 1961 of 1961.
- The three commands rerun byte-identical from hp/.

## Result

| | a2 (D 260.17) | a3 (259.47 +- 1.17i) | largest relative residual |
|---|---|---|---|
| plants at the 8 usable bases, a = 0 | <= 6.4e-7 | <= 4.6e-4 | |
| plants, a = 0.003 to 0.3 | within 14% | within 14% | 1.9e-11 (a = 0.01) |
| real, the 8 usable bases | 0.020 to 0.53 | 0.53 to 1.0e3 | 2.6e-7 to 6.9e-7 |
| real, all 26 bases | 0.020 to 4.4e3 | 0.53 to 2.9e9 | to 5.0e-6 |
| post hoc plant, both folds 1e-5 above, no near terms | 0.11 to 1.1e4 | 1.2 to 7.6e9 | 6.4e-7 to 1.3e-5 |
| post hoc real, D* free | 1.6e-3 to 1.9e3 | 0.74 to 1.3e9 | 4.0e-9 to 2.2e-6 |

Registered verdict: #820's conditional bound does not apply. Post hoc: the real amplitudes grow toward the fold, by
the same pattern as a plant with a common fold offset and no near singularities, and are equal in lam_g and Delta near
the fold. So they measure the fixed D* = 259.9033 being off by a few 1e-6, not the contamination. With D* free, both
series put the fold at 259.903301-259.903306, and |D*(lam_g) - D*(Delta)| <= 8.3e-7 at every base, with no plant for
that fit.

## Recommended task

*The two folds' separation from free-D* fits, planted.* What: plant lam_g's fold at 259.9033 + eps + delta and Delta's
at 259.9033 + eps (eps a common offset, 1e-6 to 1e-5; delta 0, 1e-7, 1e-6, 1e-5), with the two series' sizes and
regular parts, fit each with D* free at each base as `near_amp.py posthoc` does, and record how well D*(lam_g) -
D*(Delta) recovers delta. Then read the real 8.3e-7 against that. Why: #821's free-D* fits put the two folds within
8.3e-7 of each other at every base, a direct separation test that needs neither the r calibration nor the
contamination's size, but it has no plant. Acceptance (can fail): delta = 1e-6 and 1e-5 are recovered to 30% at 4 or
more bases and delta = 0 reads below 1e-7 there; then the bound is the smallest delta whose recovered separation
exceeds the real one, or it is reported as not bounded. Depends on: #821, #820.
