# I829-mac: the fold's mirror branch at D* = 259.9033 from chain_nsr's series, by two approximant families

Machine: the Apple M5 Mac (xfkappa). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/829.
Code: `hp/fold_mirror.py` on wip/xf-829. Input: `I603-win2/chain_nsr/jet_pin3_D*.npz` at #818's 46 bases 258.7829 to
259.8352 (chain_nsr has since gone on to 259.8517; those newer jets are not used), and the measured Delta of every state
in [259.64, D*). Work in progress; the closing summary will replace the status section.

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
