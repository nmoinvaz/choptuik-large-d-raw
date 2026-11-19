# I1010-mac: logs of the l = 2 mode's c2 in the M-harmonic truncation (c2 = -lambda_1)

Machine: mac (Apple M5), agent xfkappa. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1010

Code: branch wip/l2-c2-calc of choptuik-large-d (cafa2971 for the p = q runs), scripts in solver/inner_pert/
(`l2_c2_forcing.py`, `l2_c2.py`, `l2_c2_summary.py`), venv-314 (sympy 1.14.0, numpy, scipy, mpmath). One process at
nice 10 (two at most). The result JSONs these logs belong to stay in the code repository, solver/inner_pert/data/
(`l2_c2_*.json`), because they back notes/L2_MODE.md section 9.

- `l2_c2_forcing.log`: the forcings F/(sY) and the decomposition Ft(l2) + Ft(l0) = L0[(0, Phi_s)]; PASS
- `l2_c2_checks.log`: `l2_c2.py --checks` and its mutations ident, series, force
- `l2_c2_checks_main.log`: `l2_c2.py --checks` with the radius diagnostic (exit 1 from the control's check 3, reported)
- `l2_c2_M1_planted.log`: the planted lambda* of M = 1
- `l2_c2_M{1,3,5}.log`: c2, the control, lambda_1 (l0, sym); `l2_c2_M{1,3,5}_G.log`: G alone and the F_lambda relation
- `l2_c2_M5_mutate_gsign.log`: the planted lambda_1 with every forcing's sign flipped
- `l2_c2_summary.log`: the table and verdicts of section 9.5; PASS
- `l2_c2_forcing_p1.log`: `l2_c2_forcing.py --p1`, the p = 1 representative (section 9.6): Ft(p1) = Ft(l2); PASS
