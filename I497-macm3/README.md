# I497-macm3: the strip 0.5 < |Im lambda| <= 1 above #472's box at kf 27, D 61.03, M 48 (four R 0.36 circles, then small circles on the zeros found)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at de63a118 (the hp build is the older one, no rebuild). Started 2026-11-11 17:07 UTC. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/497.

State: modecount_state_D61.0264_M48_kf27.npz (I280-macm3/hp_data_after, sha256 1fd892fc..., no refit). The cache `data/` is a copy of I472-macm3/kf27/data, so the strip's circles are new determinants. Stage 1 (stage1.cmd): four R 0.36 circles at 2.85 +-0.75i and 3.35 +-0.75i (each 0.5 x 0.5 quarter of the strip has half-diagonal 0.354 < 0.36), --M=48 --kf=27 --n0=20 --fmax=1e-15, one thread, nice 10, caffeinate -is. Stage 2 after stage 1 is read: R 0.06 to 0.1 circles on every zero found.

Written before the run (the issue's). The windings above and below the real axis are equal, each zero found has a +1 circle, and the same circles find the pair at 3.4279 +-0.4985i again. Reference: #472's box at kf 27 holds 2.8230 +-0.2574i, 3.1585 +-0.0375i, 3.4279 +-0.4985i.

## Results

Stage 1 (stage1.cmd; started 17:07:38 UTC, exit 0 at 19:37:33 UTC on 2026-11-11, 0 verification mismatches and 0 alias bisections): 2.85 +0.75i winding 0 (41 points); 3.35 +0.75i +1 (43 points, zero 3.427865 +0.498603i, est 1.0e-3); 2.85 -0.75i 0 (42); 3.35 -0.75i +1 (43, zero 3.427889 -0.498527i, est 1.0e-3). Largest steps 0.378 to 0.393. The windings above and below are equal; the strip holds the pair at 3.4279 +-0.4985i of #472 and nothing else (the four circles reach Im 1.11).
Stage 2 (stage2.cmd; started 19:45 UTC, exit 0 at 20:34:01 UTC): R 0.06 on the two zeros, both +1, 28 points, largest step 0.358 and 0.355, 0 mismatches, 0 alias bisections: 3.427905 +0.498638i (est 7.9e-5) and 3.427855 -0.498621i (est 7.6e-5). #472's R 0.06 positions (3.427902 +0.498586i, 3.427885 -0.498576i) are 5.2e-5 and 5.4e-5 away, inside these estimates. The estimate is the script's distance between its n0 and n0/2 point sums, a range, not a bound.
Acceptance: windings above and below equal (yes); each zero found has a +1 circle (2 of 2); the same circles find the pair at 3.4279 +-0.4985i again (yes).
