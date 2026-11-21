# I1035-mac/stage2: the factored raise's Mac-side checks (FACTORED_HORIZON 5.3), the rung at D 262.0099, ks 315

Machine: the coordinator's M5 Mac, a subagent, one process at nice 10. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/1035

Code: `hp/factored_raise.py` and `hp/factored_horizon.py` (command raisecheck) on the branch `feat/factored-raise` of
choptuik-large-d (from main 6c4d845d), venv-314 (Python 3.14, mpmath 1.3.0, numpy 2.5.4). No hpkernel is used: the
raise itself runs on Linux (I1035-dh170 or I1035-dh610), and these are its kernel-free checks. Design, criteria and the
runner's commands are in notes/FACTORED_HORIZON.md 5.3, committed before any Linux run.

Inputs (read from this repository with `git cat-file blob`, each blob checked):
`I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.0099.npz` (eb34f3c8),
`I1064-dh610/ho2_D237.7132/ks307/base_pin3_D237.7132.npz` (861c79ff), `I1064-dh170/p315/ks315/base_pin3_D237.7132.npz`
(0f4858ee).

Files:
- `selftest.log`, `selftest_<mutation>.log`: `factored_raise.py selftest` on the D 237.7132 state and its controls.
- `raisecheck_a_D262.log/.json`: method A (the a rows for a_h, m_h fixed) at ks 315 with hp's 1/k, 512 bits: the
  start projection, then Delta moves of 1e-16, 1e-15 and 1e-14 from the linear and the second-order predictors.
- `raisecheck_ma_D262.log/.json`: the same with the chain's ElimO rung (the m and a rows for m_h and a_h).
- `rung_cols_D262_ks315.json`: the rung's Jacobian columns (finite differences at 1e-60 relative), shared by both.
- `queue.log`, `run_raisecheck2.sh`: the run order.
