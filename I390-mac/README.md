# I390-mac: Eq. (16)'s w = F3/F1 and the higher ratios as series in A^2 from the D = infinity amplitude expansion

Machine: mac (Apple M5, the coordinator's Mac), agent xfchecks. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/390 (pre-registration in the issue's comments, 20:52 UTC).

Code: `solver/eeg_profile/w_series.py` of choptuik-large-d, branch wip/i390 (venv-314, mpmath), run from
`solver/eeg_profile/`. Input: `solver/inner_amp/scan45J1500/` and `scan45J1250/` (K 45, omega_inf, 1280 bits),
`scan43J1500/` (omega/omega_inf 0.99, 1.00, 1.01, for the omega shift of comparison 3).

- `planted.log`: `planted` (exit 0) and its controls `--mutate=index`, `--mutate=phase` (exit 1 each).
- `run.log`, `w_series.json`: `run --A=2.72` (exit 0): the q_m table, S = 0.055084558 e^{0.0987856i},
  T = 1.6e-12, the three comparisons, the leading order against the README, r_3 and r_5.

Results and the discrepancy (the issue's 0.05509 is a double rounding of 0.0550846) are in notes/EEG_PROFILE.md
section 9.
