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

## Addendum: seed 2 at D 245.6366 and D 252.6135 (the coordinator's order)

`run946_seed2.sh` (unit `i946b`, 15:13:44 to 15:30:04 UTC, same worktree and build, nice 10): `step_spread.py` with `--seeds 2` at #851's rels
(1e-70, 1e-75, 1e-80), `--controls 0 --repeat 0`, on the stored states `I603-win2/chain/anm_pin3_D245.6366.npz` and `..._D252.6135.npz`, side by
side at 6 threads (980 s and 910 s, 169 and 171 MB), `--ref 5.2645963792835124e-82` at D 252.6135 only (equal as a double: pass), then
`step_spread.py power` over both (`power_seed2.log`, `power_seed2.json`). Both seed-2 groups are quadratic: D 245.6366 p 2.0000, 2.0000;
D 252.6135 p 1.9988, 2.0000. Smallest pivots: D 245.6366 4.374269e-27 at rel 1e-75 and 1e-80 (4.374241e-27 at 1e-70); D 252.6135 7.286891e-31
at 1e-80 and 7.286881e-31 at 1e-75, against 6.326356e-31 at 1e-70 (13% off the unperturbed, as seed 1's 24% there).

`spread946.py` (log `spread946.log`) reads #851's `power.json` (seed 1, stored states at 245.6366 and 252.6135), #946's `power.json` (seeds 1 and 2 on
the re-converged state at 250.1676) and `power_seed2.json`. c = |dev| / rel^2 at rel 1e-80, the one rel that is pivot-clean and quadratic at
every D and in every source:

| D | seed 1 c | seed 2 c | seed 2 / seed 1 - 1 |
|---|---|---|---|
| 245.6366 | 9.24472e96 | 8.92378e96 | -3.5% |
| 250.1676 (re-converged) | 8.72813e99 | 8.55804e99 | -1.9% |
| 252.6135 | 1.05367e102 | 1.02319e102 | -2.9% |

The seed spread here is the difference between two seeds' c, not a confidence interval. The slope of ln c against D per unit D at rel 1e-80:
seed 1 1.5119 (245.6 to 250.2) and 1.9598 (250.2 to 252.6), least squares 1.6492; seed 2 1.5153 and 1.9558, least squares 1.6503. Against #805's 1.44 the
least-squares slope is 1.145 (seed 1) and 1.146 (seed 2) times it, against twice it 0.573 for both. At rel 1e-75 the two D where it is clean give the same c
to 1e-3 (`spread946.log`).
