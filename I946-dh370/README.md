# I946-dh370: step spread at D 250.1676 on #603's state re-converged to 3e-92

Machine dh370 (Fedora 45, i7-8700, 12 threads). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/946

`run946.sh` (stages `polish`, then `spread`; units `i946p`, `i946s`; nice 10): worktree `~/Source/choptuik-large-d-935` at main 043834d9,
its 4.8.2 `.venv`. `step_spread.py --selftest` exit 0 and `--selftest --mutate=bar` exit 1 (must fail) first (`selftest.log`,
`selftest_bar.log`).

Polish (14:45:07 to 14:51:05 UTC on 2026-11-17, `polish.log`): `anm_run.py` on `I603-win2/chain/anm_pin3_D250.1676.npz` with `--steps 0
--save_base 1`, #603's flags as #808's polish jobs took them (`--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0
--D_max 400 --corrector od --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1
--reseed_o 3`, `--save_pred` left out), the stored plan kept, `--threads 12`, and `--tol_od 1e-90` where #603 has 1e-60. It converged:

    on 0: |F| 3.05e-61 -> 3.05e-61, |dz| 7.65e-49 -> 7.23e-80, lam 1, dDelta +7.65e-49, piv 1.1e-29..5.1e+35, 119.25 s
    on 1: |F| 3.05e-61 -> 3.04e-92, |dz| 7.23e-80 -> 6.26e-98, lam 1, dDelta +7.23e-80, piv 1.1e-29..5.1e+35, 118.59 s
    on 2: |F| 3.04e-92 converged, Delta 1.68492798628514828 +4.3323e-17

358 s, 230 MB. The base is `polish/base_pin3_D250.1676.npz` (max|F| 3.0424e-92 on its own plan). Step 0 moved Delta by 7.65e-49, the
same as #851's unperturbed step on the stored state, and left max|F| unchanged.

Spread (14:51:28 to 15:11:44 UTC): `step_spread.py RAW polish/base_pin3_D250.1676.npz --rel 1e-77,1e-80,1e-82,1e-85 --seeds S --controls 0
--repeat 0 --threads 6`, one process per seed S = 1, 2 side by side (`seed1.log`, `seed2.log`, 1140 s and 1217 s, 177 and 198 MB), then
`step_spread.py power seed1.json seed2.json --quad 1.8,2.2 --lin 0.9,1.1` (`power.log`, `power.json`). `coef946.py` (log `coef946.log`)
prints c = |dev| / rel^2 beside #851's.

## Results

The unperturbed step on the polished base: dDelta +3.9855e-99, max|dz| 3.2953e-98, smallest pivot 1.0687e-29 (the stored state's 1.0687e-29).

| seed | rel | dev = dDelta(seed) - dDelta(unperturbed) | c = \|dev\| / rel^2 | smallest pivot | p from the next larger rel |
|---|---|---|---|---|---|
| 1 | 1e-77 | -8.728131e-55 | 8.72813e99 | 1.068665e-29 | |
| 1 | 1e-80 | -8.728131e-61 | 8.72813e99 | 1.068665e-29 | 2.0000 |
| 1 | 1e-82 | -8.728131e-65 | 8.72813e99 | 1.068665e-29 | 2.0000 |
| 1 | 1e-85 | -8.728131e-71 | 8.72813e99 | 1.068665e-29 | 2.0000 |
| 2 | 1e-77 | -8.558038e-55 | 8.55804e99 | 1.068665e-29 | |
| 2 | 1e-80 | -8.558038e-61 | 8.55804e99 | 1.068665e-29 | 2.0000 |
| 2 | 1e-82 | -8.558038e-65 | 8.55804e99 | 1.068665e-29 | 2.0000 |
| 2 | 1e-85 | -8.558038e-71 | 8.55804e99 | 1.068665e-29 | 2.0000 |

`power.log`: both seeds quadratic, with the unperturbed step the same in the four runs of each (pass); `step_spread: PASS` for both
processes and `power`. Seed 1's c is #851's value at the stored state (8.72803e99 at rel 1e-75, `coef946.log`) to 1.1e-5 relative, and
seed 2's is 1.9% below seed 1's. The sign change that #851 found at rel 1e-80 on the stored state (max|F| 3.05e-61) does not appear on
the polished one; the polish changed that state's residual and its Delta together, so this does not say which of the two the
sign change came from.
