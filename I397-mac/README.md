# I397-mac: the type of the D = infinity profile's singularity at theta_0, from the inner equations

Machine: mac (Apple M5, the coordinator's Mac), agent xfchecks, one process. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/397 (pre-registration 21:05 UTC and its amendment 21:09 UTC in the
issue's comments).

Code: `solver/eeg_profile/profile_singularity.py` of choptuik-large-d, branch wip/i397 (venv-314: sympy, mpmath),
run from `solver/eeg_profile/`. Input: `solver/inner_amp/scan45J1500/` (K 45, omega_inf, 1280 bits).

- `wtc.log`: `wtc --order=5`, the local expansion of the gauge-fixed inner equations (form A) and of the planted ODE
  (A0), order by order: fixed, zero and free coefficients (exit 0).
- `planted.log`: `planted` (exit 0): Q1 (a pole plus (w0 - w) ln(1 - w/w0) plus a far pole, exact coefficients,
  against the predicted finite-k curve), Q2 (the planted ODE Y' = VY + 0.3, V' = Y^2/4, Taylor series to order 90 at
  80 digits, against the prediction from b2 = k1/3) and its control k1 = 0.
- `profile.log`, `profile.json`: `profile --A=2.72` (exit 0): C_k and local exponents, test 1 (exponent), test 2
  (free residue fit), test 3 (fixed-residue consistency), and the post hoc fit with the predicted 1/nu^3 term.
