# I196-win2: lemma 6a(5) at p-hat reproduced on win2, with the cross-load of macm3's B

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/196 (reproduces #184, run on macm3 in I184-macm3/).

`run_i196.sh` runs #184's commands on Python 3.14.10 (`venv-t177`, python-flint 0.9.0, FLINT 3.6.0) from `solver/proof/` of
`D:\choptuik-large-d`, one thread, Normal priority, then #184's controls, `review_39/b_float.py` and its `--mutate=w`, then
`--load-B=` of macm3's B (I184-macm3) at p-hat and `I110-win2/b_diff.py` of the two B files. Pass criteria, written before
the run: rho_6a < 1 at p-hat (own B); the cross-load of macm3's B gives rho_6a < 1; `b_float.py` puts the flow at p-hat
within 0.01 of rad(B); `--mutate=coords` fails, `--mutate=partial` fails, `--mutate=swap` fails and `b_float.py
--mutate=w` exceeds 1, as in I184-macm3. Results are added below as the run ends.

## Results (2026-11-09 01:46 UTC)

Python 3.14.10, python-flint 0.9.0, FLINT 3.6.0 (`versions.txt`), main 188853c, 20 threads busy with #204's load, Normal priority.
`run_i196.sh` ran 01:30:41 to 01:45:00 UTC, every step exit 0 except `coords` (exit 2, a failure expected); `exits.txt`.

| item | win2 | I184-macm3 |
|---|---|---|
| rho_6a at p-hat (own B) | [0.2081327454 +/- 8.77e-12] < 1 | [0.2120798569 +/- 1.46e-11] |
| max radius of B, \|H\|, G_slow^-1 | 3.21e-05, 63.9, 5.16 | 3.03e-05, 65.4, 5.30 |
| macm3's B loaded on win2 | [0.2120798570 +/- 2.97e-11] < 1 (H 65.4, G_slow^-1 5.30) | |
| `b_float.py`, flow at p-hat, over rad(B) | 5.85e-08 (from x-hat 0.184) | 5.31e-08 (0.183) |
| `--mutate=coords` | exit 2, rho_6a 3.200, not below 1 | exit 2, 3.234 |
| `--mutate=partial` | exit 0, G_slow 13 x 17 not square | the same |
| `--mutate=swap` | exit 0, step size underflow at t = 0.0585847 | at t = 0.0585256 |
| `b_float.py --mutate=w` | exit 0, 232 of rad(B) from both flows (must exceed 1) | 231 |

`b_diff.py` (win2's B against macm3's, 760 balls of X and B): midpoints differ in 41 entries, the largest |mid difference| over
the larger radius is 1.04e-14; radii differ in all 760 (ratio win2/macm3 0.88 to 1.26, median 1.014); no pair of balls is
disjoint. Its selftest passes. The two rho_6a balls are disjoint (0.2081 against 0.2121) although the boxes, midpoints and
centre are the same: the enclosures' radii depend on the integration path, as in #104 and #110. `centre_passed.txt` (the
`--x` argument) equals I184-macm3's and the box file's `p`; the log prints no centre line (as in #184).
