# anm-mac/stall153: the large-D chain's stall at D 152.93 (T118), diagnosed on the Mac

Machine: the Mac (Apple M5), coordinator session, 2026-11-06, main's kernel (multidouble 3.2.0). notes/QUAD_DOUBLE.md
13.26 says what each file shows.

- `stepB.log`, `stepB_anm_run.jsonl`, `stepB_anm_pin3_D153.4309.npz`: T118's step from T118-win2/chain/anm_pin3_D152.9309.npz
  with the u0 polish refactoring (T121-win2/rung_fix_run.py); the step to 153.43 converges, the next series is
  degenerate (stopped in step 2).
- `stepC.log`: a restart from that stored 153.43 state: the base polish starts at |F| 2.85e-10 and takes no step.
- `project_state.py`, `stepB_proj_D153.4309.npz`: the stored state projected (horizon data re-inverted from its node).
- `stepD.log` and its state: the restart from the projected state: base polish 5.55e-32, a healthy series, the step to
  153.93 converges.
- `diag.log` (`rung_diag.py`): a first proxy (the base state at D + a), out of the basin, not used.
- `checkq.log`, `truth_res.py`, `step_vs_exact.py`: the polish from a converged state's horizon data rounded to
  double-double stalls at 2.43e-16 under both rules.
- `pred_pin3_D153.4309.npz`: the prediction at 152.93 + 0.5 before its re-seed (anm_run.py --save_pred 1 on main
  effab02), the input of `reseed.py checkq`.
- `stepE.log`, `stepE/`: main effab02 in memory from T118's 152.93 state, two steps at a 0.5 to 153.43 and 153.93
  with healthy series (the fixed chain), and the stored predictions.
