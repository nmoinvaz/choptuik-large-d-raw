# anm-mac: the Taylor continuation in D (notes/QUAD_DOUBLE.md 13.15), its tests J2-J4 on the Mac

Machine: the Mac (coordinator session), from 2026-11-03 22:00 UTC. The kernel with the jet lanes is built from the
worktree `choptuik-anm` (branch `anm` of the code repository) against multidouble's branch `feat/jet-lane`
(pull request #26) until release 1.9.0.

- `jet_check.jsonl`, `jet_check.log`: J2, `hp/jet_check.py`, the residual's Taylor coefficients in the dimension
  against the residual at D + h on T75's last state, with the two controls.
- `jet_check_basin.log`: the J2 run inside the basin (h 1e-14..1e-12, D + h exact); `jet_check_run1.log` is not
  kept, the earlier runs' records are the first lines of `jet_check.jsonl` (hs 0.25..1, then 1e-9..1e-7, then the
  basin run; the last line is the one 13.16 quotes).
- `highm_ref.log`, `highm_scaled.log`: the bit-identity checks of AGENTS.md with the jet-lane kernel against
  T81's references.
- `anm_J3.jsonl`, `anm_J3_pin5.log`, `anm_J3_pin3.log`, `anm_J3_control.log`: J3, `hp/anm_step.py` from
  T75's state at D 71.0 (the jsonl holds every run in order: kfreeze 13, then pins 5 and 3 with the base moved
  by a wrong offset (superseded), then pins 5, 3, 1, then the re-planned pins 5 and 3 that 13.16 quotes, and the
  frozen-dimension control).
- `anm_J4.jsonl`, `anm_J4_pin5.log`, `anm_J4_pin3.log`: J4 from T75's last state at D 73.27, pins 5 and 3.
- `newton_diag_h*.log`, `newton_diag2_h*.log`, `pred_pin3_D71_h*.npz`: the corrector diagnosis from the saved predictions
  at D 71.5 and 72 (`hp/anm_newton_diag.py`): plain Newton creeps in the horizon block's weak directions, the deflated
  phase reaches 2-4e-18, the junk-only phases have nothing to freeze.
- `run_pin3_float.log`: the chained pilot's first run (`hp/anm_run.py`), with D + a in float64: every prediction off by
  about 3e-8 (the rounding of D times the residual's 2e6 per unit of D); superseded.
- `run_pin3/`, `run_pin3.log`: the pilot with the deflated corrector: stalls at 1e-16 at every step size.
- `run_pin3_newton/`, `run_pin3_newton.log`: plain Newton, eps 1e-16 (steps of 1.67): 73.27 -> 77.87 in four steps,
  then stalls. `run_pin3_newton_e14/`, `.log`: eps 1e-14 (steps of 2): 73.27 -> 75.27 -> 77.27 -> 79.27 converged,
  then the predictions at 79.5-80.3 sit at 1e-14 and Newton takes no step. The converged states are the npz files.
