# I829-mac: the fold's mirror branch at D* = 259.9033 from chain_nsr's series, by two approximant families

Machine: the Apple M5 Mac (xfkappa). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/829.
Code: `hp/fold_mirror.py` on wip/xf-829. Input: `I603-win2/chain_nsr/jet_pin3_D*.npz` at #818's 46 bases 258.7829 to
259.8352 (chain_nsr has since gone on to 259.8517; those newer jets are not used), and the measured Delta of every state
in [259.64, D*). Code: wip/xf-829 c8f1b7ec (on main 365d1bca).

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
- **A discrepancy.** I registered the 46 bases present from 258.7829 to 259.8352 and called them #818's. #818 had 42,
  to 259.8184. With those alone, 3 bases are usable, one fewer than the registered 4. Their mirror agrees with the
  table to 9.4e-10 (restricted818.log).

## Files
- `noise.log`: the jets' noise. The two-base least-squares residual of the forms (degrees 10-15, three base pairs) on
  plants of noise 1e-30, 1e-33, 1e-36 and on the real series. The QP plateau on the real series is 1e-34 to 8e-34
  relative. No mirror was evaluated. The plant carries 1e-30, the larger of the two (the registered rule).
- `config.log`: the configuration chosen on the plant at noise 1e-30 (dev/t3.py): two-base least squares at several
  degree sets and base sets.
- `planted.log`, `planted.json`: the registered plant at all 46 bases (`fold_mirror.py planted RAWDIR --json=...`).
- `literal.log`: the issue's first wording of method 1, the truncated series re-expanded around D* with no model.
  It returns its starting value (the chain's), as a polynomial must.
- `dev/`: the exploration scripts.
  - `explore.py`: the jets against the next states, 1e-37 to 5e-33.
  - `sizes.py`: the plant's sizes, from a least-squares fit of the measured Delta.
  - `t1.py`, `t2.py`, `t3.py`: approximants at one base, at two bases exact, and at two bases by least squares, on the plant.
  - `noise.py`: the noise measurement.

  The first plant runs of `t1.py` and `t2.py` had no noise. The noise term `1 + 1e-30 g` was rounded in floats; fixed
  in fold_mirror.py before any run here was judged.
