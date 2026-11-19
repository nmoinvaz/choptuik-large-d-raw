# I1019-mac: B5(1), an independent check (P2 item 5), starting with whether its data cover (H8)'s certified delta

Machine: the Mac (Apple M5, shared), helper session xfchecks. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1019.
Code: choptuik-large-d main c39ed13e (branch `wip/p2-b5`), `/Users/nathan/venv-314/bin/python`, python-flint 0.9.0,
nice 10, one process.

## delta/: the first question (2026-11-19)

- `b5_jump_stored_delta.log`: `python3 b5_jump.py` as stored, which reads (H8)'s delta from `b8m_h8_K4_L73.89.log` at full
  precision; identical to the repository's `b5_jump.log`: x_Phi = (39784.4, 38775.8), C_E = 2.532366e+33.
- `h8_rounded_up.log`, `b5_jump_rounded_up.log`: the same with B8_constants.md 8.3's rounded-up delta
  (8.3e-5, 79.04, 3.232, 6.464) given by `--h8log`: x_Phi = (39789.7, 38781.0), C_E = 2.532706e+33.
- `b5_threshold_superposition.log`: `b5_threshold.leading_data_bound` with its DELTA0 (0, 76.56, 3.23125, 6.46251),
  with the leading coefficients rounded up (0, 76.5602, 3.231259, 6.462517), and with (H8)'s rounded-up delta.
