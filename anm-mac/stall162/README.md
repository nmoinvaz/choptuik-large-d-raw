# anm-mac/stall162: the large-D chain's stop at D 162.31 (T122), diagnosed on the Mac

Machine: the Mac (Apple M5), coordinator session, 2026-11-06, main's kernel (multidouble 3.2.0) and, for the
octo-double comparison, the od-jets build. notes/QUAD_DOUBLE.md 13.27 says what each file shows.

- `step_octo.py`: the u0 rung block's quad-double Jacobian against the octo-double one at T118's 152.93 state, and the
  polish step with each LU; they agree, so the stall is not precision.
- `rung_svd.py`: the block's singular values at 152.93 and 162.31 (32 near G, 32 near 1; no near-null direction).
- `renode_q.py`, `x80_D162.3059.npz`, `x80.log`: T122's 162.31 state with the last node moved to 0.8; its base polish
  stalls at 7.9e-18 (pivots down to 9e-20).
- `ah_first.py`: from converged states' horizon data rounded to double-double, plain Newton against an a_h
  least-squares step first.
- `pred_pin3_D162.8059.npz`: the prediction at 162.31 + 0.5 (anm_run.py --save_pred 1), the failing input;
  `ah162.log` its run; `polish_variants.py` the rules compared on it.
- `checkq3.log`: reseed.py checkq with the a_h, m_h steps and Newton on the predictions at 153.43 and 162.81, and the
  control (13.26's rule) at 162.81.
- `am162.log`, `am162/`: main 5423d2b from 162.31, two steps at a 0.5 to 162.81 and 163.31 (corrector 1.5e-39,
  2.3e-39), with the states and the stored predictions.
