# I656-macm3: separating #551's pair near the real axis: an R 0.05 circle at kf 29 and kf 31 on the exact determinant

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, hpkernel cp314 neon of 2026-11-09), worktree ~/Source/choptuik-large-d-b596 at main b5d69cc2; modecount_cx built from 742bb879's source. hp/modecount_circle.py, modecount_common.py, modecount_cx and modecount_qdet.py are identical to #551's commit 98ee71bd (git diff empty). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/656 (recommended by #551; assigned by the coordinator's message of 2026-11-13 11:35 UTC, then #650). This folder is in a worktree of the raw repository (~/Source/choptuik-large-d-raw-641), pushed from there. Started 11:36 UTC.

Command (run_656.sh), from hp/, nice 10, caffeinate -is, both cuts at once with 3 threads each: python3 -u modecount_circle.py data/seeds/local/up23_D61.0264.npz CENTRE,0,0.05 --M=48 --kf=K --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf$K --ball=320 --threads=3 --data=<raw>/I656-macm3/kf$K/data, CENTRE 3.10 at kf 29 and 3.027 at kf 31, as I551-win2/run_551.sh ran it (same seed, layout and options; the centre and the radius changed, threads 3 instead of 9). The kf K state is made by setup from the seed (about 13 min on win2).

Written before the run (the issue's). Acceptance: winding +2 at both cuts, or the number it gives, with the pair's positions to the circle's own estimate. A different winding changes #551's box counts (6 at kf 29, 8 at kf 31) and the summary says how. About 30 determinants and 30 min each.

## Results (12:37 UTC; exits_656.txt: kf29 exit 0 at 12:35:08, kf31 exit 0 at 12:36:58 UTC; started 11:36:19 UTC, states made in about 5 min, circles of 40 + 2 points)

| cut | circle | winding | points | max step (rad) | alias bisections | zeros inside | estimates (n0 vs n0/2 sums; a range, not a bound) |
|---|---|---|---|---|---|---|---|
| 29 | R 0.05 at 3.10 | +2 | 40 + 2 | 0.339 | 0 | 3.1034051 +0.0043327i and 3.1034052 -0.0043327i | 4.0e-07, 4.0e-07 |
MIRROR 29: dRe 5.00e-08, d|Im| 1.32e-08, verification mismatches 0
| 31 | R 0.05 at 3.027 | +2 | 40 + 2 | 0.327 | 0 | 3.0274957 +0.0083390i and 3.0274963 -0.0083390i | 8.7e-07, 8.9e-07 |
MIRROR 31: dRe 5.13e-07, d|Im| 2.92e-09, verification mismatches 0

Both circles wind +2: the pair near the real axis is two zeros at each cut (a conjugate pair), so #551's box counts stand: 6 at kf 29 (4 outer + the pair) and 8 at kf 31 (6 outer + the pair). The windings of #551's R 0.36 circles add up to 12 = 4 + 2 x 4 (kf 29) and 10 = 6 + 2 x 2 (kf 31) with the pair counted as two in every circle that contains it.
