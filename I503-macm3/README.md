# I503-macm3: the kf 27 lambda_phys control at R 0.0075 with n0 40 and 80, and at R 0.00375 with n0 20 (D 61.03, M 48)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at de63a118 (the hp build is the older one, no rebuild). Started 2026-11-11 19:38 UTC. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/503.

State: modecount_state_D61.0264_M48_kf27.npz (I280-macm3/hp_data_after, sha256 1fd892fc..., no refit). The cache `data/` is a copy of I500-macm3/data. The R 0.0075 circle with n0 = 40 and 80 shares the points of the n0 = 20 one that are already in the cache (the same determinants, by design), so only the new points are computed. Commands (control.cmd), #500's with the changed n0 or R, run one after the other, one thread, nice 10, caffeinate -is.

Written before the run (the issue's). If the zero found at R 0.0075 moves by 5e-7 or more between n0 20, 40 and 80, it is scatter and the estimate is too small. If it stays within 2e-7 of 2.0435315 - 0.00000076i, the 1.27e-6 miss of #500 is a displacement of the state's zero; it is then compared with the kf 22 state, whose control missed by 3.6e-8 at R 0.2.

## Results

Runs (control.cmd, three in turn, 19:38:20 UTC to 20:43:09 UTC on 2026-11-11, 1 h 05 min, 81 new determinants): R 0.0075 n0 40 exit 0 at 19:48:05, R 0.0075 n0 80 exit 0 at 20:20:49, R 0.00375 n0 20 exit 0 at 20:43:09. All wind +1, 0 verification mismatches, 0 alias bisections.

| R | n0 | points | largest step | zero, offset from lambda_phys (Re, Im) | miss | estimate (n0 against n0/2) | miss / R |
|---|---|---|---|---|---|---|---|
| 0.2 (#472) | 20 | 28 | | | 3.25e-5 | | 1.6e-4 |
| 0.06 (#496) | 20 | 28 | 0.354 | | 1.16e-5 | 1.8e-6 | 1.9e-4 |
| 0.03 (#496) | 20 | 28 | 0.353 | | 2.84e-6 | 1.8e-6 | 9.5e-5 |
| 0.015 (#500) | 20 | 28 | 0.353 | (+7.8e-7, +2.2e-6) | 2.37e-6 | 1.4e-6 | 1.6e-4 |
| 0.0075 (#500) | 20 | 28 | 0.353 | (-1.02e-6, -7.6e-7) | 1.27e-6 | 1.9e-7 | 1.7e-4 |
| 0.0075 | 40 | 40 | 0.280 | (-9.7e-7, -2.8e-7) | 1.01e-6 | 4.8e-7 | 1.3e-4 |
| 0.0075 | 80 | 80 | 0.140 | (-8.5e-7, +1.4e-7) | 8.65e-7 | 4.3e-7 | 1.2e-4 |
| 0.00375 | 20 | 28 | 0.353 | (-6.2e-7, -2.7e-7) | 6.70e-7 | 4.0e-7 | 1.8e-4 |

Acceptance by the rule written before the run: the zero at R 0.0075 moves by 9.2e-7 between n0 20 and n0 80 (4.8e-7 per doubling to 40, 4.3e-7 to 80), 5e-7 or more, so it is scatter and the estimate is too small (1.9e-7 at n0 20 against the 9.2e-7 it later moved). The displacement branch (within 2e-7 of 2.0435315 - 0.00000076i) does not hold, so the comparison with the kf 22 state's 3.6e-8 is not made by the rule.
Reading (mine, not the rule): the miss is below 1e-6 at R 0.0075 with n0 80 (8.65e-7) and at R 0.00375 with n0 20 (6.7e-7). Over R 0.2 to 0.00375 the misses are 1e-4 to 2e-4 times R (all but R 0.03, 9.5e-5), linear in R and not a floor, which fits a noise in ln det M of order 1e-3 per point averaged over the n0 points (the first moment weights ln h by R); I did not test the cause. #442 found ln|det M| moving by 3e-4 to 1.4e-2 for one-ulp changes of the double-double differentiation matrix, which is of that size. The kf 22 control, 3.6e-8 at R 0.2 (1.8e-7 times R), has about a thousandth of this at the same radius.
