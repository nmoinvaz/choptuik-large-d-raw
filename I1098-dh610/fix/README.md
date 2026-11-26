# I1098-dh610/fix: wave 2 of the budget reruns and the d/dtheta storage term, on the fastmul5 kernel (#1098)

Machine: dh610 (Fedora 45, i7-12700, 20 threads; nice 10). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The kernel is wip/large-d-fastmul5 at f350aa62, with lane-precision reciprocals and the relaxed horizon products, in `site_x`. It
matches mm5's build bit for bit on one state's octo-double residual (`../xcmp/`). Common settings: `HP_EXACT_RECIP=1
HP_HORIZON_RELAXED=1`, `form_s.py release_ls --harm 13 --kmax 13 --jac_by 13:qq --res od --tol 1e-48 --tol_h 1e-44`.
Each rls.log ends with "h13's change", Delta's change from the state the run started from.

- `wave2.sh`: recip_check at D 300 and D 1000 (both PASS, `../xcmp/recip_check.log`). Then D1000_base, D1000_steps2 and
  D1000_M48 together (4 threads each) from the inputs of I1098-mm5/fix/inputs, then the M 48 tail h15..h23.
- `D1000_base/`: D 1000's full kfree-13 state re-converged with exact reciprocals. h13's change is **+4.002e-22**, the
  double-double 1/k error of the D 1000 records (D 300's is +1.288e-19, I1098-mm5/fix). Delta
  1.654240854145891738986194081376390745734, qd check 6.8e-63.
- `dmat.sh`, `after_d1000base.sh`, `D300_dmat12/`, `D300_dmat16/`: the error from storing the d/dtheta matrices in
  double-double (`hp/dmat_perturb.py`, a3e6ca3b). The run moves the matrices to D_dd - S e, where e is the rounding
  from 80-digit values. The change divided by S is the term, to first order. From D300_full_base (u, M 32), against
  mm5's fixed base 1.67817101540087156786106196598861494537:

  | run | S | change | change / S |
  |---|---|---|---|
  | D300_dmat12 | 2^12 | -8.869e-29 | -2.1653e-32 |
  | D300_dmat16 | 2^16 | -1.4192e-27 | -2.1656e-32 |

  The ratio is 16.002 (linear). **The term at D 300 is -2.17e-32.** These runs converge a perturbed system on purpose,
  so their states and direct records are left out of this folder.
- `D1000_dmat12/`, `D1000_dmat16/`: the same pair from D1000_base's state (Moebius a 8, ks 1517, M 32), against
  D1000_base's 1.654240854145891738986194081376390745734:

  | run | S | change | change / S |
  |---|---|---|---|
  | D1000_dmat12 (outer 1) | 2^12 | -4.96522e-21 | -1.21221e-24 |
  | D1000_dmat16 (released) | 2^16 | -7.94435e-20 | -1.21221e-24 |

  The ratio is 16.000. **The term at D 1000 is -1.212e-24**, 5.6e7 times D 300's. The fix is wip/large-d-fastmul6
  (d368a0c0): f64 remainders of the matrices on the quad- and octo-double lanes.
- `D1000_steps2/`: D 1000 with every Taylor step halved, from the inputs' steps2 state, re-converged with exact
  reciprocals. It ends at 1.654240854145891738986194081376390745734, the same as D1000_base to all 40 printed digits.
  **The step term is gone at D 1000.** It was -7.6e-23 with the double-double reciprocals.
- `after_dmat1000.sh`: the D 2000 pair from I1088-dh610/rls2000d's state. `after_tail.sh`: D 1000's M 48 tail
  continued, h25..h37 with kmax 37. `rebuild_y.sh`: the fastmul6 build into site_y, with its checks.
