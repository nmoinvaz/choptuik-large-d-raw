# I1095-mac: Track C refitted with the form-S direct solves, D 250-2000 (planted test, real fit, control)

Machine: the coordinator's Mac. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1095

Code: hp/track_c_direct.py at choptuik-large-d main df60a202; direct points from raw I1088-dh370, I1088-dh610, I1088-mac-a at f80109383.

- tcd_planted.log/.json: P0, P5, P6 through the same code; PASS (largest |fit - truth| / E = 0.15).
- tcd_real2.log/.json: the real fit; the residual check PASS (0.79 sigma).
- tcd_real2_mut.log: --mutate=shift (D 2000 moved by 1e-8); the check FAILS as it must (18.78 sigma), exit 1.

Rerun 2026-11-26 with hp/track_c_direct.py at choptuik-large-d main 4fd73ce9 (a held point without its own first-order
bias now carries the same or nearest lower D's, 5.1e-10 at D 2000-8000, in place of 1e-11) and direct points from raw
I1088-dh370, I1088-dh610, I1088-mac-a, I1088-mm5 at 35b9f9f6 (D 250-8000, full at 300 and 1000):

- tcd_planted3.log/.json: P0, P5, P6; PASS (largest |fit - truth| / E = 0.07, F = 1).
- tcd_real3.log/.json: Delta(10^4) = 1.64493098975163 +- 4.09e-11 and Delta_inf = 1.64389374512694 +- 5.02e-11 (spread
  over fit choices, conditional on Delta analytic in 1/n); the residual check PASS (1.11 sigma, at D 8000).
- tcd_real3_mut.log: --mutate=shift (D 8000 moved by 1e-8); the check FAILS as it must (18.50 sigma), exit 1.
