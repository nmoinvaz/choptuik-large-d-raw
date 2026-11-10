# I447-macm3: four R 0.36 circles over the box 2.6 < Re lambda < 3.6, |Im lambda| <= 0.5 at D 61.03, M 48, kf 25, and a small circle on each zero found

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at bfe5fd54. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/447 (was #279).

Method (coordinator, 15:33 UTC): modecount_wind.py cannot take the box (its horizontal edge y1 is omega/2 and the network is about 800 determinants), so four circles of R 0.36 at 2.85 +-0.25i and 3.35 +-0.25i cover it; zeros come in conjugate pairs, so the lower
circles are the control of the upper ones. Command (circles.cmd, caffeinate -is, nice 10, one thread): hp/modecount_circle.py on hp/data/seeds/local/up23_D61.0264.npz with the lambda_phys control (2.043532530673195, R 0.2) first, then the four circles,
--M=48 --kf=25 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf25. The saved kf 25 state of I244-macm3 (hp_data_after/, sha256 in state_sha256.txt) is copied into hp/data so the setup loads it with no refit, and I244-macm3/kf25/data (its cache: the lambda_phys circle,
the three row circles and the 3.0196 circle) is copied into data/, so the control is a replay of #244's determinants (same machine, same build) and the new circles are evaluated here.

Written before the run (coordinator's acceptance). Each circle's winding with its mismatches; equal windings above and below (or the difference reported); the lambda_phys control +1 (limit as the circles of #244: within 1e-5 of the kf 23 value is not claimed here, the control is reported with its miss);
a small circle (R 0.05 to 0.1, centred on the located zero) winding +1 on each zero found. Estimates are ranges, not bounds.

## Results

