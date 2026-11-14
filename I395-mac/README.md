# I395-mac: cross-check of #82's sigma_0..16 (K 45, J 1500) against K 33, J 1000 files, with a pre-set tolerance

Machine: mac (Apple M5), the coordinator's Mac, agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/395

Data comparison only, no new amplitude runs. Script `solver/inner_amp/sigma_xcheck.py` of choptuik-large-d (branch
wip/xf-checks), Python 3.14 venv-314, mpmath 1.3.0, reading only the `sigma_str` of the JSON files named below.

- `tol_ref.json`, `tol_ref.log`: the tolerance, written and committed before the target comparison was run. R_n is the
  largest r_n = |sigma_n(K45 J1500) - sigma_n(K33 J1000)| / |sigma_n| over wf = 0.99, 1.00, 1.01 (T99-win2 against
  T83-mac, the only wf where both exist). Verdicts: OK r <= max(R_n, floor_n), WATCH r <= 10 max(R_n, floor_n), BAD
  otherwise; floor_n is one unit in the 20th digit of each component of both strings over |sigma_n|.

Then, from `solver/inner_amp/` at branch commit 6c6447bd (`sigma_xcheck.py`, RAW = this repository):

- `selftest.log` (`selftest RAW --tol I395-mac/tol_ref.json`, exit 0): replica T103-mac against T99-win2 23 of 23
  equal, a changed digit at k = 3, 16, 22 found at k only; #82's 22 posted values recomputed; planted changes of
  30 max(R_n, floor_n) at n = 2, 9, 16 of the 1.10 file BAD at n, of 0.3 max(R_n, floor_n) silent; smoothness plants
  of 100 times the residual BAD.
- `compare.log`, `compare.json` (`compare`, exit 1 by design, one BAD): 46 OK, 4 WATCH (1.10 and 1.11 at n = 7 and 9),
  1 BAD (1.09 at n = 9, 3.2e-17 against R_9 = 2.4e-18, 13 times).
- `jseq.log`, `jseq.json` (`jseq`): J 1000, 1250 (I213-win2), 1500 at each node and at wf 1.00. At every WATCH and BAD
  entry J 1250 and J 1500 agree to 6.4e-21 or better, so the difference is in the J 1000 file.
- `k39_vs_k33.log`: I256-win2's K 39 J 1000 files equal the K 33 J 1000 files at n = 1..15 (all 20 digits).
- `smooth.log`, `smooth.json` (`smooth`, exit 0): each K 45 node against the degree-5 interpolant through the six other
  ladder nodes (1.06 ... 1.14); residuals equal to those of the pure K 33 ladder to six digits, 6e-12 (n = 1) to
  1.1e-8 (n = 16); no BAD.
