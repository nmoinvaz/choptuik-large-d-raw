| D | state | role | status | final bracket | root (lam_lin) | evals | \|F\| | steps | Delta | Delta - source |
|---|---|---|---|---|---|---|---|---|---|---|
| 15.0 | c150 | continuation | tol | (2.4204038816471365, 2.4204039316471366), width 5.00e-08 | 2.420403918 | 11 | 2.3783e-10 | 2719 | 0.9841306967650356 | 0 |
| 15.0 | r150 | re-solve | tol | (2.41987748586599, 2.4198775358659903), width 5.00e-08 | 2.419877523 | 11 | 2.3789e-10 | 2719 | 0.9841302706798702 | -4.261e-07 |
| 16.5 | c165 | continuation | nonrobust (widened) | (2.1426861165828943, 2.1429882363912793), width 3.02e-04 | 2.142687164 | 9 | 2.0080e-10 | 2481 | 1.0117787163237064 | 0 |
| 16.5 | r165 | re-solve | tol (widened) | (2.1459391706439113, 2.1459392206439114), width 5.00e-08 | 2.145939216 | 12 | 2.0094e-10 | 2481 | 1.0117784460550832 | -2.703e-07 |

- offset(D 15.0) = root(r150) - root(c150): lam_lin difference -5.2640e-04; range from the brackets -5.2645e-04 .. -5.2635e-04
- offset(D 16.5) = root(r165) - root(c165): lam_lin difference +3.2521e-03; range from the brackets +2.9509e-03 .. +3.2531e-03
- D 16 for comparison: +8.59e-04 (U40 against the source; U40b +7.5e-4, U40c +9.2e-4)
- verdict: both offsets are above 5e-4 in size but not both positive: not D 16's sign, mixed
