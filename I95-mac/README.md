# I95-mac: growth rates of the complex scalar's two critical solutions, the CSS (kappa = 0) and the real DSS's imaginary sector

Machine: Apple M5 Mac (`mac`), a subagent of the coordinator session, 2 processes at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/95

Scripts (main repository, branch wip/i95): `solver/matter/complex_css.py` (the CSS's growth rates, followed in D and
counted), `solver/matter/complex_imag_eqs.py` (sympy derivation of the imaginary sector), `solver/matter/complex_imag.py`
(det M of the imaginary sector on hp states, and its winding counts). The note is matter/COMPLEX_CRITICAL.md.

- `css/`: jsonl records and logs of complex_css.py (follow, count, controls).
- `imag/`: jsonl records and logs of complex_imag.py (checks, counts, controls).
- `states/`: copies of the hp states used that were not in any repository (the D = 4 lowDn states of the main
  checkout's untracked hp/data/lowD_states).
