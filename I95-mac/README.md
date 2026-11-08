# I95-mac: growth rates of the complex scalar's two critical solutions, the CSS (kappa = 0) and the real DSS's imaginary sector

Machine: Apple M5 Mac (`mac`), a subagent of the coordinator session, 2 processes at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/95

Scripts (main repository, branch wip/i95): `solver/matter/complex_css.py` (the CSS's growth rates, followed in D and
counted), `solver/matter/complex_imag_eqs.py` (sympy derivation of the imaginary sector), `solver/matter/complex_imag.py`
(det M of the imaginary sector on hp states, and its winding counts). The note is matter/COMPLEX_CRITICAL.md.

- `css/`: complex_css.py records and logs: `follow_k0` (fixed steps, lost the oscillatory root at D = 5), `track_k0`,
  `track_k0_b` (the adaptive track to D = 80), `boxes_k0` (box counts with trend removal; `boxes_k0_v1_notrend`, the
  first version, stopped), `locate_k0` (the strip's zeros at two radii), `roots_k0`, `scan_k0` (css_scan.py collocation
  at D = 4-8), and the queue scripts `queue2.sh`, `queue5.sh` with their logs.
- `imag/`: complex_imag.py records and logs: `checks.jsonl` (first round, with D = 60) and `checks2.jsonl` (second round,
  with the tolerance test), `counts.jsonl`, `roots.jsonl`, the determinant caches `evals_*.jsonl`, the sympy log
  `complex_imag_eqs.log`, the queue scripts and logs (`queue1.sh` was stopped at D = 60, where det M in double precision
  is noise), and `crate/`: the D = 60 count with hp/modecount_test.py (double-double).
- `states/`: copies of the hp states used that were not in any repository (the D = 4 lowDn states of the main
  checkout's untracked hp/data/lowD_states).
