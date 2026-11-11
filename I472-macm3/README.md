# I472-macm3: the box 2.6 < Re lambda < 3.6, |Im lambda| <= 0.5 at D 61.03, M 48, at kf 27 and kf 22 (four R 0.36 circles each, then small circles on the zeros found)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at bfe5fd54. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/472.
Pushed to the raw repository from a separate worktree after the rewrite (history rewritten 2026-11-10); the states are not in this folder, only their sha256.

States (sha256 in state_sha256.txt), copied into hp/data so the setups load them with no refit: kf 27 from I280-macm3/hp_data_after, kf 22 from I244-macm3/kf22/hp_data_after (kf 22 has the same projector as kf 21). Caches: copies of I280-macm3/kf27/data and I244-macm3/kf22/data (the lambda_phys R 0.2 circle and the row circles of those runs), so the control is a replay of those.
Stage 1 (stage1_kfK.cmd, caffeinate -is, nice 10, one thread per cut, both cuts at once): hp/modecount_circle.py on hp/data/seeds/local/up23_D61.0264.npz with the control 2.043532530673195 R 0.2 and the four circles 2.85 +0.25i, 3.35 +0.25i, 2.85 -0.25i, 3.35 -0.25i (R 0.36), --M=48 --kf=K --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kfK --data=<raw>/I472-macm3/kfK/data (#447's stage).
Stage 2, after stage 1 is read: R 0.06 circles on the zeros found (#447's).

Written before the run (the issue's). At each cut the windings above and below the real axis are equal; each zero found has a +1 circle; the control winds +1 within 1e-6 of lambda_phys. Reference: kf 23, one pair 3.0196 +-0.0958i (#230); kf 25, 2.90346 +-0.24278i and 3.25669 +-0.22648i (#447). Estimates are ranges, not bounds.
The control's miss from lambda_phys is expected to be larger than 1e-6 at these cuts (kf 25 4.7e-6, kf 27 3.25e-5 at R 0.2: #466); that is reported against the acceptance as it stands, not read away.

## Results


Stage 1 results (kf 22 exit 0 at 02:12:43 UTC, kf 27 exit 0 at 03:59:49 UTC; 0 verification mismatches in all circles):
  kf 22: control +1 (zero 2.043532495, miss 3.6e-8); 2.85 +0.25i +1 (zero 2.689687 +0.476164i, est 1.8e-3); 3.35 +0.25i 0; 2.85 -0.25i +1 (2.689688 -0.476164i); 3.35 -0.25i 0. Equal above and below. The row's zero 3 (2.6896 +0.4758i at kf 22, #244) lies inside the box; no pair near 3.02.
  kf 27: control +1 (zero 2.043503 -0.000013i, miss 3.25e-5); 2.85 +0.25i +1 (2.826066 +0.247866i, est 3.2e-2, 58 points, 17 alias bisections); 3.35 +0.25i +3 (3.158390 +0.035912i est 5.7e-3; 3.161668 -0.043153i est 2.5e-2; 3.427897 +0.498531i est 1.4e-3; 73 points, 15 alias bisections);
  2.85 -0.25i +1 (2.826359 -0.247980i); 3.35 -0.25i +3 (3.158245 -0.035106i; 3.162070 +0.042694i; 3.427904 -0.498522i). Equal above and below. The circles at 3.35 +-0.25i overlap across the real axis (R 0.36 > 0.25), so the pair near 3.16 +-0.04i is seen by both; distinct zeros in the box: 6 (three conjugate pairs).
Stage 2 (small circles, stage2_kf27.cmd and stage2_kf22.cmd): kf 27: 2.826066 +-0.2479i R 0.1 (the estimate is 3.2e-2), 3.160 +-0.040i R 0.06, 3.4279 +-0.4985i R 0.06; kf 22: 2.6897 +-0.4762i R 0.06.

Stage 2 results (kf 22 exit 0 at 06:03:02 UTC, kf 27 exit 0 at 07:10:31 UTC on 2026-11-11; every circle winds +1, 0 verification mismatches, 0 alias bisections; the estimate is the distance between the n0 and n0/2 point sums of the script, a range, not a bound):
  kf 22: 2.689714 +0.476098i (est 5.6e-8, 28 points), 2.689714 -0.476098i (est 1.3e-7).
  kf 27: 2.823023 +0.257395i (est 2.7e-5, R 0.1, 28 points), 2.823022 -0.257332i (5.0e-5); 3.158455 +0.037475i (4.3e-4, R 0.06, 34 points), 3.158473 -0.037591i (4.7e-4); 3.427902 +0.498586i (3.1e-5, 28 points), 3.427885 -0.498576i (6.7e-5).
Acceptance: windings above and below equal at both cuts (yes); each zero found has a +1 circle (kf 22 2 of 2, kf 27 6 of 6); the lambda_phys control winds +1 within 1e-6 (kf 22 yes, miss 3.6e-8; kf 27 NO, miss 3.25e-5, reported as it stands). The stage 2 circles at 3.160 +-0.040i overlap each other (centres 0.08 apart, R 0.06) and each holds one zero.
