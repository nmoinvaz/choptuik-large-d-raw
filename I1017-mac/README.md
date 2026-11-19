# I1017-mac: (H8) of B8_constants.md section 8 recomputed independently (P2 item 3): logs and records

Machine: the Mac (Apple M5, shared), helper session xfchecks. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1017.
Code: `solver/proof/review_p2c/p2c_h8.py` on branch `wip/p2-h8` of choptuik-large-d at 1506f53f, mpmath complex intervals
(256 bits), `/Users/nathan/venv-314/bin/python`, nice 10, one process. Protocol: `notes/P2_remaining.md` section 5.1
(9374659d), committed before the runs. `b8m_h8.py`, B8's other code and their logs were not opened before these runs.

Criteria (the protocol's): (P1) the series' residual orders, the leading coefficients against B8's printed digits and
the inner series against `series_arb.py`; (P2) delta <= delta_ref = (1, 200, 10, 20) for every n >= e^73.89 over the
box; (P3), (P4) the comparison with `b8m_h8`'s logs, made after these numbers are committed. Controls: K1 A x (1 + 1e-3)
(must fail P1), K2 h_S x (1 + 1e-3) (must be flagged by P3), K3 a sign flip in the series (must fail P1).

Files: `run.sh` (the commands), `logs/*.log`, `p2c_h8_*.json` (the records of the box runs).
