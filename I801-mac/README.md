# I801-mac: track C, Delta(D) at D 250-400 from a 1/n series matched to the data below D 245, and the fold at 259.9

Machine: mac (Apple M5, the coordinator's Mac), agent xfchecks, one process at nice 10. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/801 (pre-registration 21:23 UTC, amendments 21:28 and 21:32 UTC,
all before any fit to the real data).

Code: `hp/track_c.py` of choptuik-large-d, branch wip/i801 (venv-314: python-flint arb at 256 bits, mpmath), run from
`hp/`. Input: `hp/data/delta_all.csv` (dd "check", qd "starts", chain_fit, D <= 245.64) and #603's states past 245.64
(`I603-win2/chain/` and `chain_nsr/anm_pin3_D*.npz` of this repository; Delta is the state vector's last entry,
equal to each record's norms[0]).

- `planted_registered.log` and `.json`: the planted functions under the rule as registered (D_min 10, 20, 30). P1 and P2 are not accepted at any fit.
- `planted_amend1.log` and `.json`: under the first amendment (D_min to 100). P1 and P2 are still not accepted, and P0's error blows up.
- `planted.log` and `.json`: under the second amendment (D0 = the lowest D_min with at least 5 accepted fits, together with the next D_min). This run sets F = 1. The planted functions are:
  - P0, the README formula;
  - P1 and P2, with exponentially small terms;
  - P3, a planted fold;
  - P4, #313's comparison with the release bias planted.
- `real.log` and `.json`: the real fit, its values and errors, the slope, #313's comparison and #603's chain past 245.64.
- `beyond.txt`: all 86 states past 245.64, chain minus series, against E.
- `resid_150_245.txt`: the central fit's normalized residuals.
- `fold.log` and `.json`: post hoc. Chain minus series on D >= 253.5 is fitted to s sqrt(D* - D) + linear. That square-root term, planted under P0 on the real grid, is then run through all 135 fits.
