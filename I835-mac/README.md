# I835-mac: the largest square-root fold of the continuum near D 260 that track C's fit and checks would pass

Machine: the Apple M5 Mac (xfkappa). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/835.
Code: `hp/track_c_fold.py` on wip/xf-835 3fdedb48, off main 6ff8f6e2. Input: `hp/data/delta_all.csv` through
`track_c.load_real` (1354 points, D 8.5 to 245.64).

## Result
- **The baseline.** `track_c.py real` with a = 0 gives 124 of 135 fits accepted, D0 = 10 (7 accepted at D_min 10) and
  19 fits used. It reproduces the stored series rows: Delta(300), Delta(400) and Delta_inf to 7e-17, against E of
  1.24e-10, 2.33e-10 and 1.93e-9 (`real_baseline.log`).
- **The chain's fold is flagged.** a = 0.035 at D*_p 259.903 leaves 0 of 135 fits accepted, so track C has no estimate.
- **The bound.** |a|_max(D*_p), the largest |a| that leaves D0 = 10, is 2.28e-10 to 2.99e-10 over D*_p 259 to 270.
  - At 259.903 it is 2.54e-10 (a > 0) and 2.31e-10 (a < 0).
  - At every D*_p it is set by the D_min-10 fits 1/(D-2) K18, 1/(D-1) K18 and 1/D K16.
  - It is verified through the full code path at every D*_p and both signs: unflagged at 0.9x, and at 1.1x D0 becomes 20.
- **Reported beside the bound.**
  - At 0.9x the bound, the plant passes unflagged but moves Delta(250), Delta(300), Delta(400) and Delta_inf by 1.4 to
    2.6 E. The central fit's largest residual on D 150-245 is then 7.1 to 8.5 sigma, against the real 2.76.
  - The first of the 135 fits changes acceptance at |a| of 1.0e-10 to 2.4e-10.
- **The rerun is byte-identical** (`rerun_bounds.json`).
- **check_numbers.py --selftest:** 2109 of 2109, and its selftest 2109 of 2109.

## Files
- `bounds.log`, `bounds.json`: the run over D*_p 259, 259.5, 259.903, 260, 260.5, 261, 262, 263, 265, 267.5 and 270,
  both signs.
- `rerun_*`, `rerun.log`: the byte-identical rerun.
- `real_baseline.*`: track C's own real run, the baseline.
- `test_259.903.log`: the first test at D*_p 259.903.
- `check.log`: `check_numbers.py --selftest`.
