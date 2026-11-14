# I375-mac: the real DSS's imaginary sector at large D in double-double (complex_imag_dd.py), checks and counts

Machine: mac (Apple M5), the coordinator's Mac, agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/375

Code: `solver/matter/complex_imag_dd.py` and `solver/matter/ddnp.py` of choptuik-large-d, branch wip/xf-checks
(Python 3.14 venv-314, numpy, scipy, mpmath; python-flint only in diag/diag_sens.py and diag_swap.py). States:
`hp/data/states/up6_D30.0688.npz`, `up7_D45.0507.npz`, `up13_D60.0020.npz` (M 32, nodes 0.3 ... 0.7).

- `diag/`: double-precision diagnostics of complex_imag.py (scripts and logs; the logs of diag_double, diag_sens,
  diag_swap and diag_stiff are copied from the terminal), the matching-point test (`subdiv_D30.log`,
  `subdiv_D60.log`), the block swaps between the double and double-double matrices (`blocks_D30.log`,
  `blocks_D60_ks200.log`) and the centre block's sensitivity (`centre_D60.log`).
- `check_D30.jsonl`, `check2_D30.jsonl`, `check_D60.jsonl`: `complex_imag_dd.py check` (tol 1e-20, K 32, nsub 5).
- `tolscan_D60_pilot.jsonl`: ln det M at lambda = 1.3 + 0.4i for tolerances 1e-12 ... 1e-24 (nsub 1).
- `pilot_B0_D30.log`, `counts.jsonl`, `evals_*.jsonl`: the pilot count (B0 at D = 30.07, tol 1e-14).
