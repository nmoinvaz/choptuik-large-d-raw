# I822-mac: the two folds' separation from free-D* fits, planted, and the bound it gives

Machine: the coordinator's Mac (Apple M5), agent xfkappa. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/822.
Code: `hp/fold_separation.py`, registered at wip/xf-822 d6492064 (the design posted on the issue before the run), the
outcome recorded in its docstring at c5602b8e, on main 6201e043. Input: `I603-win2/chain_nsr` jets at raw f65c5e43,
#818's 26 bases. One process at nice 10.

## Runs

- `b7probe.py`, `b7probe.log`: plants only, before the run. A lam_g plant with exactly the fit's fold terms, fitted
  with D* free, misplaces D* by +2.5e-7, +1.6e-6 and -1.7e-6 at three bases, with residuals of 1.6e-8 to 6.4e-7 (about
  1e-11 at the true D*). So the minimizer, bounded Brent on the largest residual, does not find the true minimum at the
  1e-6 level. The planned misfit variant was dropped.
- `planted.log`, `planted.json`: the registered plants, 23 of 26 bases usable, PASS.
- `real.log`, `real.json`: the real separations and the bound.
- `check_numbers.log`: `check_numbers.py --selftest` at c5602b8e, 1973 of 1973, selftest 1973 of 1973.
- Both commands rerun byte-identical.

## Result

| planted delta | recovered D*(lam_g) - D*(Delta) at the 23 usable bases, both eps |
|---|---|
| 0 | -4.4e-8 to +6.9e-8 |
| 1e-7 (reported) | +4.9e-8 to +1.8e-7 |
| 1e-6 | +8.07e-7 to +1.23e-6 |
| 1e-5 | +7.50e-6 to +1.22e-5 |
| -1e-6 (reported) | -4.7e-6 to +2.8e-6 |
| -1e-5 (reported) | -1.56e-5 to -7.4e-6 |

The minimizer misplaces each series' D* by up to 3.5e-6 (lam_g) and 2.5e-6 (Delta), but the error is common to both and
cancels in the separation. The near singularities planted at 0.01 change the separations by at most 6e-14 (the fit
holds those terms). Not usable: 259.7603, 259.7864 and 259.8012.

Real: D* 259.9033006 to 259.9033058 for both series. The separation at the usable bases is -8.29e-7 at 259.4928 and
-2.97e-7 at 259.5183, and at most 1.11e-7 in magnitude at the other 21. S = 8.29e-7 lies above the smallest recovered
1e-6 separation (8.07e-7) and below the smallest recovered 1e-5 one (7.50e-6). Registered verdict: |D*(lam_g) -
D*(Delta)| < 1e-5.

## No recommended task

This closes the #818-#822 chain. A tighter bound would need either a planted delta between 1e-6 and 1e-5 (the issue's
grid steps by decades), or a minimizer that finds the true D* (the probe's error, up to 3.5e-6, is what limits single
series). Either is for the coordinator to decide; neither is recommended here.
