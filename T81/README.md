# raw/T81: the quad-double solver (feat/qd-solver), coordinator on the Mac, 2026-10-27

Built from feat/qd-solver (dfaec36; multidouble 1.7.0's sources) into ~/venv-qds.

- pin7_D72.8000.npz: T75's state (raw/T75), the input
- planted_D72.8.jsonl, .log: hp/qd_planted.py from 1e-24 (outside Newton's basin: every solver's first step lands
  2.3e-11 away)
- planted2_D72.8.jsonl, .log: the same from 1e-40, 1e-36, 1e-32, 1e-28 (pass criterion at 1e-40)
- pilot.jsonl, pilot_attempts.jsonl, .log: hp/scan_qd.py converging the D 72.8 state for the full system
- conv_<state>.jsonl, .log, conv_*_D*.npz: hp/scan_qd.py converging T75's pin 5 and pin 7 states at D 72.8 and 73.0
  (full system); along_step_D72.8.log, full_steps_D72.8.log (along_step.py, full_steps.py): the residual along the
  first Newton step, and full steps converging
- cont7.log: continuation from the converged D 72.8 state (fails); tangent_D72.8.log (tangent.py): the finite-difference
  tangent scales like h^2; blocks_dD_D72.8.log (blocks_dD.py): only the horizon block explodes as D moves, worse with ks;
  pred2.log (pred2.py): linear interpolation between the two solutions leaves the horizon block at 1e18
- bitid.sh and its logs: highm_check.py ref and scaled, main (1.5.1) against feat/qd-solver (1.7.0)
