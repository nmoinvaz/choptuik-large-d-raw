# I1095-mac: Track C refitted with the form-S direct solves, D 250-2000 (planted test, real fit, control)

Machine: the coordinator's Mac. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1095

Code: hp/track_c_direct.py at choptuik-large-d main df60a202; direct points from raw I1088-dh370, I1088-dh610, I1088-mac-a at f80109383.

- tcd_planted.log/.json: P0, P5, P6 through the same code; PASS (largest |fit - truth| / E = 0.15).
- tcd_real2.log/.json: the real fit; the residual check PASS (0.79 sigma).
- tcd_real2_mut.log: --mutate=shift (D 2000 moved by 1e-8); the check FAILS as it must (18.78 sigma), exit 1.
