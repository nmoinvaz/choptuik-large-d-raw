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
- `run_pin3_cont/`, `.log` and `run_pin3_cont_dnp/`, `.log`: the chain continued from the 79.27 state with stalls
  accepted below 1e-13: plain Newton takes no step from the predictions (1e-14..1e-13) past 80.5; the deflated
  corrector crawls to 82.12 on accepted stalls whose linearised Delta corrections are 6e-9 to 2e-8.
- `run_pin1_cont/`, `.log`: pin 1 (harmonics 3-13 held) from the 79.27 state: 80.52 and 81.86 accepted at 7e-20 and
  1.2e-19, then no progress; Delta differs from the pin-3 chain by 5e-6 at 80.5 (the stale held harmonics).
- `run_t101_pin13.log`, `run_t101_pin3/`, `.log`: the 0.85 layout from T101's last state (78.61): pivots 1e-19..1e-20,
  the coefficients unusable (z_1 ten times the tangent); section 13.17.
- `run_trend_pin3/`, `.log`, `run_trend_pin5.log`: the trend-held chains (`anm_run.py --trend T75`): pin 3 converges at
  75.27 and 77.27 with Delta within 1e-7 of the formula, then Newton takes no step from 1e-14 residuals at 77.5-79.3; pin 5's
  coefficients are polluted by its free harmonic 5 (pivot 4e-9). `run_trend_pin3_cont/`: continued with stalls accepted.
- `hopf/`: the Hopf tests (`hp/hopf_amp_mode.py`): the amplitude law and the growth-rate scans per state.
