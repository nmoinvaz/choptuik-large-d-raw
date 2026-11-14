# I395-mac: cross-check of #82's sigma_0..16 (K 45, J 1500) against K 33, J 1000 files, with a pre-set tolerance

Machine: mac (Apple M5), the coordinator's Mac, agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/395

Data comparison only, no new amplitude runs. Script `solver/inner_amp/sigma_xcheck.py` of choptuik-large-d (branch
wip/xf-checks), Python 3.14 venv-314, mpmath 1.3.0, reading only the `sigma_str` of the JSON files named below.

- `tol_ref.json`, `tol_ref.log`: the tolerance, written and committed before the target comparison was run. R_n is the
  largest r_n = |sigma_n(K45 J1500) - sigma_n(K33 J1000)| / |sigma_n| over wf = 0.99, 1.00, 1.01 (T99-win2 against
  T83-mac, the only wf where both exist). Verdicts: OK r <= max(R_n, floor_n), WATCH r <= 10 max(R_n, floor_n), BAD
  otherwise; floor_n is one unit in the 20th digit of each component of both strings over |sigma_n|.
