# raw/T81: the quad-double solver (feat/qd-solver), coordinator on the Mac, 2026-10-27

Built from feat/qd-solver (dfaec36; multidouble 1.7.0's sources) into ~/venv-qds.

- pin7_D72.8000.npz: T75's state (raw/T75), the input
- planted_D72.8.jsonl, .log: hp/qd_planted.py from 1e-24 (outside Newton's basin: every solver's first step lands
  2.3e-11 away)
- planted2_D72.8.jsonl, .log: the same from 1e-40, 1e-36, 1e-32, 1e-28 (pass criterion at 1e-40)
- pilot.jsonl, pilot_attempts.jsonl, .log: hp/scan_qd.py converging the D 72.8 state for the full system
