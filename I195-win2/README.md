# I195-win2: lemma 6a(5) on the 1e-20w sub-box at p-hat, on win2

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/195 (as #184 did for the 1e-18 sub-box, run on macm3).

`run_i195.sh` runs #184's commands on Python 3.14.10 (`venv-t177`, python-flint 0.9.0, FLINT 3.6.0) from `solver/proof/` of
`D:\choptuik-large-d`, one thread, Normal priority, with `--box=I103-macm3/A_M2_6a_M5_sub1e-20w.json` and `--x` = that file's
`p`; then the partial, coords and swap controls, `review_39/b_float.py` on the new B and its `--mutate=w` control. Pass
criteria, written before the run: rho_6a < 1 at p-hat (#103 had 0.088 at x-hat); `b_float.py` puts the flow at p-hat within
0.01 of rad(B); `--mutate=coords` fails (rho_6a not below 1), `--mutate=partial` fails (G_slow not square), `--mutate=swap`
fails (integration underflow), `b_float.py --mutate=w` exceeds 1.

## Results (2026-11-09 02:20 UTC)

Python 3.14.10, python-flint 0.9.0, FLINT 3.6.0 (`versions.txt`), main 188853c, beside #202 and negative-mass's jobs, Normal priority.
`run_i195.sh` ran 02:05:56 to 02:18:33 UTC; `exits.txt` has every step.

| item | result | #103 at x-hat |
|---|---|---|
| rho_6a at p-hat | [0.08734457904 +/- 1.22e-12] < 1 | [0.08801448685 +/- 2.00e-12] |
| max radius of B, \|H\|, G_slow^-1 | 3.67e-06, 14.6, 1.56 | 3.89e-06, 15.0, 1.56 |
| `--x` equals the box file's `p` (`centre_passed.txt`) | yes, every digit | |
| `b_float.py`, flow at p-hat over rad(B) | **4.62e-07** (criterion 0.01) | |
| `b_float.py`, flow at x-hat over rad(B) | 1.51, outside B | |
| `--mutate=partial` | exit 0, G_slow 13 x 17 not square | |
| `--mutate=coords` | exit 2, rho_6a 1.893, not below 1 | |
| `--mutate=swap` | exit 0, step size underflow at t = 0.0585847 | |
| `b_float.py --mutate=w` | exit 0, 1.9e+03 of rad(B) from both flows (must exceed 1) | |

`b_float.py` exits 3 on the plain run: its exit code needs the flows from both x-hat and p-hat inside B, and on this sub-box
rad(B) (3.67e-06) is smaller than the x-hat to p-hat shift of the flow (2.78e-06 at the worst entry, 1.51 of the radius there),
so the x-hat flow is outside. The p-hat flow, the quantity of the issue's criterion, is inside by a factor 2e6.
`b_diff_new_vs_I103_x_hat.log`: the new B against #103's B (centred at x-hat), 760 balls of X and B: midpoints differ in all
760, 19 pairs of balls are disjoint (largest midpoint difference 1.08e+03 of the larger radius, at an X entry).
