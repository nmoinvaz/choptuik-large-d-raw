# I1098-mac-a/singularities: where Delta(D) is singular in e = 1/(D - 2), from the 16 ladder records, and what the ladder predicts at low D

Coordinator (t5), Mac, 2026-11-27 21:21 UTC. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1098.
Code `delta_singularities.py` (run from main's hp/ at e8f6934a, for ladder_fit's readers): rational fits [L/M], M 1-5,
to the ladder records at raw 7037bf243 (D 250-4000 and 3214; sigma err_sum), accepted when chi^2 <= the 0.99 quantile
and every |residual| <= 4 sigma; the poles of each accepted fit's denominator, clustered across fits.

- Planted first (ladder_fit.py's truths at the same 16 D and sigma, seed 1): T1's poles (n -13, -5) found at e -0.0769
  (21 of 23 fits) and -0.191 (15); T2's pair at e -0.01 +- 0.0173i found to 4 digits (11 of 11); T3's branch point at
  e -0.03 found as a pole string starting at -0.0337 (13 of 14), then -0.054 and -0.095.
- Real (`real.log`): 19 accepted fits; poles on the negative real axis at e -0.0607 (n -16.5, D -14.5; 18 of 19 fits,
  spread -0.0678 to -0.0596) and -0.0823 (14 of 19), then about -0.15: a pole string like T3's, so likely a branch
  point near e -0.054 to -0.061. No complex singularity recurs.
- Prediction (`predict_real.log`): every accepted fit evaluated at lower D, against delta_all.csv. Median minus the table:
  D 245.14 +1.95e-12, 200 -1.65e-12, 150 +4.6e-13, 100 +2.2e-13 (chain_fit rows, err 1e-12 to 4e-11); D 67.0 +1.32e-14,
  50.0 +1.3e-12, 40.0 +2.66e-11, 30.0 +1.04e-9, 25.1 +9.14e-9 (dd rows, err 1e-16 to 2e-15). Each is inside the fits'
  own range there (2e-11 at D 67, 1.5e-5 at D 25).
- (2026-11-27 21:25 UTC) `--taylor=6` (`taylor_real.log`): a0 1.643893745125357513722871 (range 6e-22), a1
  10.37528562845395538737 (1.6e-17), a2 -49.168737490066284 (2.5e-13), a3 399.18546066508068 (3.2e-9), a4 -4369.1118138
  (4e-5). `domb_sykes.py` on them is NOT used: on planted T1 (a pole at e -0.077, exponent -1) it reads e0 -0.054 to
  -0.064 with positive exponents (`taylor_T1.log`), and on T3 its ratios are erratic. So the singularity's type is
  not determined; its position is the Pade estimate above.
