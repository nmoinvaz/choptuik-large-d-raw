# I509-win2: how one rounding in dtau_c becomes 8e-9 in ln|det M| at D 30

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, AVX2), issue https://github.com/nmoinvaz/choptuik-large-d/issues/509, continuing #485 with its harness: worktree `D:\choptuik-bisect2` at e043be2 (today's tree), venv `venv-bisect2` (python-flint 0.9.0, numpy 2.5.4), `hpkernel` of e043be2 built there.
Check points: October's D 30.0688 M 48 state (`I250-mac/states/modecount_state_D30.0688_M48_october.npz`) at lambda = 4.267 + 0.974 i and 3.94364216362105 + 1.1900607986722187 i, the two points of `I250-mac/scripts/fresh_vs_cache.py`.

## Method

1. Two builds of `modecount_cx` from e043be2 (`modecount_build_bisect.sh`, e043be2's `hp/modecount_build.sh`): `cxbuild_new` today's, `cxbuild_old` with `dtau_c` in the old `DotAcc` form (#485's `olddtau_on_e043be2.patch`). They give ln|det| -940.4586634376807 / -965.1149263918375 and -940.4586634457893 / -965.1149263751369 (the cache), as in #485 (`dump_matrices.py` prints them).
2. `dump_matrices.py HP_DIR CX_BUILD_DIR old|new OUT`: the complex mode matrix M (1152 x 1152) from `CSolver.mode_matrix` at both points, four double arrays each (re/im, hi/lo), in `mats/` (163 MB, not pushed; about 90 s to make again).
3. `first_order.py MATS POINT 320 [--control]` (python-flint, 320 bits): builds M_old and M_new exactly (hi + lo), the exact ln|det| of each by `acb_mat.det`, the difference dM = M_new - M_old and its size, the first-order estimate Re tr(M_old^-1 dM) with M_old^-1 dM from `acb_mat.solve(..., algorithm="approx")`, and the second-order remainder. `--control` plants eps = 1e-20 |M_ij| at the entry with the largest |(M^-1)_ji| and requires the exact change of ln|det| to equal Re(eps (M^-1)_ji) to 1e-6; exit 1 if not.
4. `patch_shiftstats.py` (effective diff `shiftstats_on_e043be2.patch`) instruments `dtau_c` of today's code: at each application it also forms the old form, keeps the new form's result (the determinant is unchanged), and counts the applications and the difference between the forms; `shift_stats.py` reads them per determinant. Its control `set_shift_plant(1e-20)` adds 1e-20 x (old hi) to the old form's lo part and requires the reported rms and max relative difference to be 1.0000e-20 (the first try failed because `1.0 + 1e-20` is `1.0` in f64; fixed).

## Results

| | point 1 (4.267, 0.974) | point 2 (3.9436, 1.1901) |
|---|---|---|
| ln\|det\| the code, old form / new form | -940.4586634457893 / -940.4586634376807 | -965.1149263751369 / -965.1149263918375 |
| the code's difference new - old | 8.1086e-09 | -1.67006e-08 |
| exact ln\|det M_old\| (320 bits) | -940.458663445790577 | -965.114926375135689 |
| exact ln\|det M_new\| | -940.458663437682414 | -965.114926391837071 |
| code minus exact (old / new) | 1.25e-12 / 1.71e-12 | -1.14e-12 / -3.4e-13 |
| exact difference new - old | 8.10816251e-09 +- 5e-24 | -1.67013819e-08 +- 4e-23 |
| first-order Re tr(M_old^-1 dM) | 8.10816260e-09 | -1.67013830e-08 |
| exact minus first order | -8.4e-17 | +1.1e-15 |
| first order / the code's difference | 0.99995 | 1.00005 |
| entries of M that differ (of 1 327 104) | 184 315 | 184 313 |
| max \|dM_ij\| / \|M_ij\|, rms over the differing entries | 5.0e-13, 2.9e-15 | 5.4e-13, 3.0e-15 |
| max \|dM\| (max \|M\| 3.1e+04), Frobenius \|dM\| / \|M\| | 5.8e-21, 1.75e-25 | 4.9e-21, 1.75e-25 |
| ln\|det\| change / Frobenius relative change of M | 4.6e+16 | 9.5e+16 |
| applications of the shift per determinant (8-lane records, re and im counted separately) | 4 336 128 | 4 336 128 |
| elements (lanes, re and im) | 34 397 664 | 34 397 664 |
| elements where the two forms differ | 11 754 533 (34.2%) | 11 632 502 (33.8%) |
| relative difference of the forms per element: rms, max | 2.05e-30, 8.2e-27 | 7.9e-30, 4.5e-26 |

Control of the first-order formula (`first_order_p1_control.log`): eps = 9.9124e-25 planted at M_old(8, 20), the entry with the largest |(M^-1)_ji| (1.48e+13): the exact change of ln|det| -1.466544293e-11, the prediction Re(eps (M^-1)_ji) -1.466544293e-11, ratio 1.000000000 +- 7e-12: passed.
Control of the counting (`shift_stats.json`): planted 1e-20 comes out as rms 1.0000e-20 and max 1.0000e-20: passed.
