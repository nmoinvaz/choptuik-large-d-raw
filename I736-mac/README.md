# I736-mac: the plans' coefficient change split over the weak singular vectors, at D 252.2497 and 252.6135

Machine: the coordinator's Mac (Apple M5), agent xfkappa. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/736.
Code: `hp/plan_split.py`, registered at wip/xf-736 ecd82247 (the design posted on the issue before the run), the post
hoc command at c77c4888, on main 68f56b3d. Kernel: the 3c35f0c build (multishoot 1.2.2, multidouble 4.2.1,
`hp/src` unchanged since), `PYTHONPATH` to it, the venv-314 Python. One process at nice 10, 4 threads.
Inputs: I603-win2/chain states, I685-dh370/repro (the kept plan's series) and I686-dh370/newplan (the new plan's).

## Runs

- `split_D252.2497.log`, `split_D252.6135.log` (and `.json`, `_V.npz`, the vectors): the registered runs, exit 0.
  `run.log`: their times (05:09 to 05:37 UTC).
- `split_mutateV.log`: the planted control at D 252.6135 (v_2 replaced by a random vector before the planted split):
  the share comes back off by 1.1, exit 1. Its real split equals the registered run's in every number (a rerun of
  both LUs and subspace iterations).
- `posthoc.log`, `posthoc.json`: post hoc, from the runs' outputs.
- `check_numbers.log`: `check_numbers.py --selftest`, 1991 of 1991, selftest 1991 of 1991.

## Result

| | D 252.2497 | D 252.6135 |
|---|---|---|
| sigma of the 4 weakest vectors (kept plan) | 7.365e-32, 1.075e-31, 1.443e-31, 1.520e-31 | 3.855e-32, 7.132e-32, 9.823e-32, 9.975e-32 |
| ||J v_1|| / sigma_1 (exact Jacobian, 140 digits) | 1.000000 | 1.000000 |
| plan steps, kept / new | 61 / 23 | 61 / 23 |
| sigma(new)/sigma(kept) - 1 | up to 8.6e-8 | up to 4.4e-8 |
| the spans' smallest principal cosine | 1 - 1.1e-16 | 1 - 7.8e-16 |
| |dz_k|/|z_k| at k 7 and 13 (2-norm) | 7.1e-3, 1.45e-2 | 1.2e-3, 3.0e-3 |
| share of dz_k on span(V) at k 7 and 13, either plan | 0.9999995, 0.9999978 | 0.9999997, 0.9999986 |
| off-span part of dz_k, k 5-24 | 4.6e-4 to 1.0e-2 | 6.0e-4 to 3.4e-3 |
| off-span part of z_k, k 5-24 | 5.1e-4 to 4.4e-3 | 3.8e-4 to 6.5e-3 |
| weak coordinates' relative change at k 7 and 13 | 6.6e-4 to 2.6e-2 | 8.8e-4 to 5.2e-3 |
| planted share 0.6 along v_2, returned to | 3.1e-14 | 1.3e-13 |

Reading (registered): the share is above 0.9 at k 7 and 13 on both plans' span at both bases, so the plan's change lies
on the weak directions. The series' own coefficients lie on the same span to the same level, and the two plans share
it, so the plan moves the series' coordinates in the weak span and not the span.

Post hoc: one fixed 4x4 map of the weak coordinates (dc_k = B c_k, each order scaled to unit |c_k|) does not describe
the change: residual 0.49 and 0.42 over k 5-24; fitted on k 5-14 it misses k 15-24 by 0.72 and 0.61; the control
(dc_k against c_(k+1)) gives 0.78 and 0.65. The c_k over k 5-24 are effectively two-dimensional (singular values 1,
0.64-0.71, then about 0.01), as one conjugate pair of singularities makes them. So the split does not say why D* stays.

## Recommended task

None. Why D* is robust to a change of the series' weak coordinates is not answered by the split; a test of it would
compare the two plans' coefficient ratios c_k / c_(k-1) on the dominant pair, which is #686's Pade comparison in other
words, already done there.
