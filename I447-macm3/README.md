# I447-macm3: four R 0.36 circles over the box 2.6 < Re lambda < 3.6, |Im lambda| <= 0.5 at D 61.03, M 48, kf 25, and a small circle on each zero found

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at bfe5fd54. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/447 (was #279).

Method (coordinator, 15:33 UTC): modecount_wind.py cannot take the box (its horizontal edge y1 is omega/2 and the network is about 800 determinants), so four circles of R 0.36 at 2.85 +-0.25i and 3.35 +-0.25i cover it; zeros come in conjugate pairs, so the lower
circles are the control of the upper ones. Command (circles.cmd, caffeinate -is, nice 10, one thread): hp/modecount_circle.py on hp/data/seeds/local/up23_D61.0264.npz with the lambda_phys control (2.043532530673195, R 0.2) first, then the four circles,
--M=48 --kf=25 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf25. The saved kf 25 state of I244-macm3 (hp_data_after/, sha256 in state_sha256.txt) is copied into hp/data so the setup loads it with no refit, and I244-macm3/kf25/data (its cache: the lambda_phys circle,
the three row circles and the 3.0196 circle) is copied into data/, so the control is a replay of #244's determinants (same machine, same build) and the new circles are evaluated here.

Written before the run (coordinator's acceptance). Each circle's winding with its mismatches; equal windings above and below (or the difference reported); the lambda_phys control +1 (limit as the circles of #244: within 1e-5 of the kf 23 value is not claimed here, the control is reported with its miss);
a small circle (R 0.05 to 0.1, centred on the located zero) winding +1 on each zero found. Estimates are ranges, not bounds.

## Results

Circles exit 0 at 18:59:10 UTC (started 16:02 UTC; 325 lines in the cache, 174 new). All five wind +1 with 0 verification mismatches:
  lambda_phys 2.043532530673195 (R 0.2, replay of I244): zero 2.043534609 +0.000003920i, estimate 9.5e-07.
  2.85 +0.25i (R 0.36): zero 2.904198 +0.244407i, estimate 1.4e-02, 44 points, 4 alias bisections, largest step 0.386.   2.85 -0.25i: zero 2.904184 -0.244432i, 1.4e-02, same counts.
  3.35 +0.25i (R 0.36): zero 3.256356 +0.226640i, estimate 8.5e-03, 39 points, 0 alias bisections, largest step 0.391.   3.35 -0.25i: zero 3.256354 -0.226645i, 8.5e-03, same counts.
The four circles cover the box 2.6 < Re < 3.6, |Im| <= 0.5 (the corners (2.6, +-0.5), (3.6, +-0.5) and the midpoints (3.1, 0) and (3.1, +-0.5) are 0.354 from a centre, inside R 0.36). Each zero is outside the other circle of its pair (0.407 and 0.446 from the other centre).
Small circles (R 0.06, centred on the four located zeros, small_circles.cmd, started 19:25 UTC): follow.
Small circles (R 0.06, started 19:25, exit 0 at 21:07:44 UTC; 360 lines in the cache), all winding +1, 28 points, largest steps 0.349 to 0.351, 0 mismatches, 0 alias bisections:
  2.904198 +0.244407i: zero 2.903462 +0.242781i (estimate 4.3e-06).   2.904184 -0.244432i: zero 2.903462 -0.242778i (1.2e-05).
  3.256356 +0.226640i: zero 3.256691 +0.226476i (1.0e-05).   3.256354 -0.226645i: zero 3.256693 -0.226477i (1.1e-05).
