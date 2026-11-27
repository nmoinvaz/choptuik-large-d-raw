# I1098-dh610/ladder/D4628_guess: why D 4628's jump stalled, and the guess at a moved last node (#1098)

Machine: dh610 (Fedora, i7-12700), fastmul7 (hp_z, site_z at c21ba40d), 4 threads. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/1098

- `gtest.log` (`gtest_610.sh`, `jump_guess_resid.py`): the double-double residual of form_s.py jump's guess, per
  block, no Newton. The Moebius a changes nothing: the guess from D 4000's jump state alone (deg 0) reads a horizon
  block of 6.84e+03 at a 9.995 and at a 11.565, and d4628b's guess (deg 1, D 2000 base h13 and D 4000's jump) 1.82e+01
  at both, with the other blocks at 1e-6 and 1e-8.
- `ratio.log` (`ratio_610.sh`, form_s_lastnode.py ratio, the held guess, a 11.565, ks 6959, kc 260): the cause is the
  last node. Both inputs carry D 2000's x_l 0.7035589 (L = (n/2) ln(1/x_l^2 - 1) = 20 at D 2000, 46 at D 4628). The
  same deg-1 guess carried by Taylor steps to x_l 0.705576 (L 20) reads 2.8e-08 in the horizon block, 2.7 times the
  largest other block, against 1.8e+01 and 1.8e9 times at 0.7035589. Deg 2 from #1088's lastnode states (L 20 each) at
  D 4000, 5657 and 8000, carried to x_l 0.7062221 (D 8000's L 20 node, L 11.6 at D 4628): 8.0e-12, 3.9 times; from D
  2828, 4000 and 5657 at x_l 0.7058552: 1.2e-11.
- `inputs/`: the #1088 states, from raw main by `git show` (their blobs are in `ratio.log`).
