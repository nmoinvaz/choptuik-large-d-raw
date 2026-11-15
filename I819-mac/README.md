# I819-mac: lam_g - r Delta at the fold, the plant that fails, and the inputs

Machine: the coordinator's Mac (Apple M5), agent xfkappa. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/819.
Code: `hp/fold_cancel.py` at wip/xf-819 403d9dae, on main ecb36f6e. Input: `I603-win2/chain_nsr` jets at raw f65c5e43,
#818's 26 bases (259.4928-259.8184). One process at nice 10. Stopped after the plant: the real combination was not typed.

## Runs

- `coeffs.log`, `coeffs.json`: the inputs, measured on lam_g's and Delta's series separately (the combination is not
  formed): c_10..c_24 fitted, each order weighted by 1/|c_k|, as b1 u + b3 u^3 + b5 u^5, u = sqrt(259.9033 - D).
- `planted.log`, `planted.json`: the plants of the two series' sizes, FAIL (exit 1).
- `diag.py`, `diag.log`: the plant's ingredients one at a time at four bases (plants only).

## Inputs

| series | b1 | b3 | b5 | largest relative residual |
|---|---|---|---|---|
| lam_g | +7.2163e-4 to +7.2272e-4 | +6.79e-4 to +8.08e-4 | -2.5e-5 to -2.3e-3 | 6.3e-6 to 2.6e-5 |
| Delta | +3.4954e-2 to +3.5003e-2 | +1.19e-2 to +1.79e-2 | -1.6e-2 to -1.24e-1 | 3.3e-6 to 3.0e-5 |

r = b1(lam_g)/b1(Delta) = 0.020646, from 0.020645 to 0.020648 over the 26 bases (a relative range of 1.2e-4). The
issue's 0.0203 is 1.7% low, and would leave a square-root term of 1.2e-5, larger than the combination's u^3 term at
orders near 20 for s below about 0.4. b3 and b5 drift with the base; b1 does not.

## The plant

At each base: both series from the medians of b, #782's near contamination at 0.3 of the fold's amplitude (+ for lam_g,
- for Delta, so it does not cancel), the real series' orders 1-9 beyond their fitted fold terms, noise 1e-12.

| X = lam_g - r Delta | ratio mu | Dlog mu | criterion met at |
|---|---|---|---|
| r = the plant's 0.020646 | +1.51 to +2.71 | +1.14 to +1.26 | 0 of 26 (expected 4 or more) |
| r + 10% | +0.49 to +1.17 | +0.84 to +0.91 | S band at 0 |
| r - 10% | -0.13 to +0.64 | +1.10 to +1.27 | S band at 0 |
| r = 0.0203 | +2.7 to +38.5 | +0.94 to +1.45 | 0 |
| lam_g's fold 0.01 above Delta's (r fitted) | -0.25 to +2.58 | +0.15 to +0.80 | cancels at 0 (expected fewer than 4) |

The ingredients (`diag.log`), at 259.4928, 259.6306, 259.7436 and 259.8184:

| plant | ratio mu | Dlog |
|---|---|---|
| clean (fold terms only) | +1.512 to +1.578, D* 259.9025-259.9033 | mu +1.500, D* 259.9033 |
| contamination only | +2.76, +2.06, +1.59, +1.51 | mu +1.08 to +1.13 |
| regular low orders only | +1.51 to +1.57 | pole at D 260.35-262.5 |
| both | +2.71, +2.06, +1.59, +1.51 | pole at D 260.14-260.21, mu +1.16 to +1.21 |

So the estimators type mu = 3/2 when the combination is clean, and the ratio estimator does so near the fold even with
the contamination. The Dlog estimator, which the acceptance requires as well, does not: the combination's u^3 term is s
times weaker than a square root, and the regular low orders and the uncancelled contamination then set its
approximants.

## A shared fold from r's constancy (observation)

With lam_g's fold 0.01 above Delta's, the fitted r (both fitted at 259.9033) runs from +0.0059 to -0.0034 over the
bases, a relative range of 20, against the real data's 1.2e-4. The recommended task calibrates that against smaller
shifts.

## Recommended task

*The shared fold from r's constancy across bases.* What: plant lam_g's fold at 259.9033 + delta for delta = 1e-3, 1e-4,
1e-5, 1e-6 and 0 (the two series' measured sizes, contamination and low orders as in this plant), fit r at every base
as `fold_cancel.py coeffs` does, and record the relative range of r against delta. Then read the real range, 1.2e-4,
against that calibration. Why: #819's estimator test cannot be validated (the Dlog estimator fails its plant), while the
fitted r moves by a relative 20 for delta = 0.01 and the real r is constant to 1.2e-4, a test of one branch point that
needs no exponent estimate. Acceptance (can fail): the range grows monotonically with delta in the plants, and the
delta = 0 plant's range lies below the real one's; then the bound on |D*(lam_g) - D*(Delta)| is the largest delta whose
plant range stays below 1.2e-4, or the result is reported as not bounded. Depends on: #819, #818.
