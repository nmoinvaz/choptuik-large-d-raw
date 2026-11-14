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
- `check_D45.jsonl` (`check`, tol 1e-14, nsub 5, with the conjugation test).
- Pilot result: B0 at D = 30.07 (`count ... B0 --tol=1e-14`, code 8d3621b4): winding of g 1.0000000000000464, largest
  step 0.58 rad, 39 determinants, 1007 s (26 s each), no refinement-limit hit (`counts.jsonl`,
  `evals_D30.0688_tol1e-14.jsonl`, `pilot_B0_D30.log`).
- The full recount is `solver/matter/run_i375.sh` (branch wip/xf-checks, 38c2fbee), handed to a runner.
- Summary of dh370's run (`I375-dh370/`, 31438056): `summary_dh370.log` is `python3 solver/matter/i375_summary.py
  <raw>/I375-dh370 --other=<raw>/I375-mac/evals_D30.0688_tol1e-14.jsonl,<raw>/I375-dh370/evals_up6_D30.0688_B0.jsonl`
  (exit 0, PASS); `summary_control.log` is the same script on a copy of that folder whose D = 45.05 B0 count is replaced
  by the mutated-coupling count (exit 1, FAIL, as it must).
- `xmachine_det_D30.jsonl`: `complex_imag_dd.py det up6_D30.0688.npz -0.05 --tol=1e-14` on the Mac at 38c2fbee. It
  equals the Mac pilot's value bit for bit (-1059.4961934889302); dh370 gives -1059.496193329259 at the same point.
