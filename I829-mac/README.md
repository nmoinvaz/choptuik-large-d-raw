# I829-mac: the fold's mirror branch at D* = 259.9033 from chain_nsr's series, by two approximant families

Machine: the Apple M5 Mac (xfkappa). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/829.
Code: `hp/fold_mirror.py` on wip/xf-829 c8f1b7ec (on main 365d1bca).

**Input.**
- Jets: `I603-win2/chain_nsr/jet_pin3_D*.npz` at the 46 bases registered on #829, 258.7829 to 259.8352. #818 had the
  first 42, to 259.8184. chain_nsr has since gone on to 259.8517; those newer jets are not used.
- Measured Delta: every state in [259.64, D*) of the raw clone at ee6cc048, up to 259.8484.

## Result
- **The plant passes.** It has 7 usable bases, 259.8068 to 259.8352. Over them, the mirror is within 5.5e-8 (M1)
  and 8.5e-8 (M2) of the plant's, and the + sheet within 7.3e-28.
- **The control fails, as it must.** With D* moved by 0.01, both methods miss by 2.0e-3.
- **On the real series:**
  - the + sheet meets the measured Delta to 5.4e-29;
  - M1 and M2 agree on the mirror to 8.0e-9;
  - the table runs from 1.6104224 at 259.64 to 1.6302764 at 259.90, with an error of 1.8e-7 at 259.64.
- **The Puiseux data:** D* 259.90330382883, Delta* 1.6323214210731, a1 0.035020554885, a2 -0.008654817400,
  a3 0.018417121619, a4 0.004191095534. M1's mu is 1/2 to 8.9e-15.
- **The rerun is byte-identical** (real.json and fold_mirror.csv).
- **check_numbers.py --selftest:** 2064 of 2064, and its selftest 2064 of 2064.
- **A discrepancy.** I registered the 46 bases present and called them #818's. #818 had 42. With those alone, 3 bases
  are usable, one fewer than the registered 4. Their mirror agrees with the table to 9.4e-10 (`restricted818.log`).

## Files
- `noise.log`: the exploratory noise measurement (`dev/noise.py`).
- `noise_cmd.log`, `noise.json`: the same measurement by `fold_mirror.py noise`.
  - Method: the two-base least-squares residual of the forms (degrees 10-15, three base pairs), on plants of noise
    1e-30, 1e-33 and 1e-36 and on the real series. No mirror is evaluated.
  - Result: the jets' relative noise is 5.7e-35 to 7.2e-34, so the plant carries 1e-30, the larger (the registered
    rule).
- `config.log`: the configuration chosen on the plant at noise 1e-30 (`dev/t3.py`), two-base least squares.
- `planted.log`, `planted.json`: the registered plant at all 46 bases.
- `control.log`, `control.json`: the plant with D* moved by 0.01, judged at the 7 bases against the unmoved plant.
- `real.log`, `real.json`, `fold_mirror.csv`: the real run at the 7 bases. `rerun_real.log`, `rerun_real.json`,
  `rerun_fold_mirror.csv` and `rerun.log` hold the byte-identical rerun.
- `planted_1pt.log`, `planted_1pt.json`: the forms matched at one base, 259.8352. M1 misses the plant by 5.5e-6 and
  M2 by 7.6e-7.
- `posthoc.log`, `posthoc.json`, `coeffs_planted.log`, `restricted818.log`: post hoc readings.
  - The plant's Puiseux data against the methods: worst a1 3.9e-14, a4 5.9e-11.
  - The plant's largest stated spread over its largest actual error: 44 (M1) and 116 (M2).
  - #818's 42 bases alone.
- `literal.log`: the issue's first wording of method 1, the truncated series re-expanded around D* with no model.
  It returns its starting value, the chain's.
- `check.log`: `check_numbers.py --selftest`.
- `dev/`: the exploration scripts.
  - `explore.py`: the jets against the next states, 1e-37 to 5e-33.
  - `sizes.py`: the plant's sizes.
  - `t1.py`, `t2.py`, `t3.py`: forms at one base, at two bases exactly, and at two bases by least squares, on the plant.
  - `noise.py`: the noise measurement.

  The first plant runs of `t1.py` and `t2.py` had no noise. The noise term `1 + 1e-30 g` was rounded in floats; it
  was fixed before any judged run.

## Recommended task: the mirror state polished by Newton
- **What:** apply fold_mirror.py's M2 forms (the same 7 usable bases and degree sets) to every component of the
  jets, not only Delta. Take the mirror state at D 259.80 and polish it with the chain's corrector at fixed D
  (hp's Newton, double-double or better).
- **Why:** the converged state's Delta tests the table with machinery that shares nothing with the approximants; only
  the seed comes from them. Away from D*, the Jacobian is regular on both sheets.
- **Acceptance (can fail):** Newton converges to |F| < 1e-30 from the mirror seed, with Delta within 1e-9 of the
  table's 1.6196534449 at 259.80 (the table's stated error there is 1.4e-10).
- **Control:** the chain-sheet seed from the same forms converges back to the chain's Delta, 1.6432968633, and not to
  the mirror.
- **Depends on:** #829.
