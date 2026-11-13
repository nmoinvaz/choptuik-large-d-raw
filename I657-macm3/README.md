# I657-macm3: #551's box at kf 33 on the exact determinant (the kf 33 half of #657)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, hpkernel cp314 neon of 2026-11-09), worktree ~/Source/choptuik-large-d-b596 at main b5d69cc2, modecount_cx built from 742bb879's source; hp/modecount_circle.py, modecount_common.py, modecount_cx and modecount_qdet.py are identical to #551's commit 98ee71bd (git diff empty, checked for #656). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/657 (recommended by #551; the coordinator's message of 2026-11-13 13:52 UTC: kf 33 on macm3, kf 27 on win2 after #674). This folder is in a worktree of the raw repository (~/Source/choptuik-large-d-raw-641), pushed from there. Started 13:53 UTC.

Command (run_657.sh), from hp/, nice 10, caffeinate -is: python3 -u modecount_circle.py data/seeds/local/up23_D61.0264.npz CIRCLE --M=48 --kf=33 --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kf33 --ball=320 --threads=1 --data=<raw>/I657-macm3/kf33/NAME/data, as I551-win2/run_551.sh with only the cut changed, with the five circles of its argument list run as five processes with their own caches (the control 2.043532530673195,0,0.2 and the R 0.36 circles at 2.85,0.25 / 3.35,0.25 / 2.85,-0.25 / 3.35,-0.25), one thread each, instead of one process on all five: the circles are independent, the single process would need about 8 to 9 h on 6 threads. The control process makes the kf 33 state with setup; the others start when it is saved.

Written before the run (the issue's and the message's). Acceptance: every circle resolved within its point cap, the control winding +1, and the box's count at kf 33 (#551: 6 at kf 29, 8 at kf 31); if the pair near the real axis appears again, an R 0.05 circle around it as in #656.

## Results (17:52 UTC; exits_657.txt: control 15:27:14, c_3.35 circles 16:42:55 and 16:43:04, c_2.85 circles 17:14:05 and 17:14:06, pair 17:51:46 UTC, all exit 0; the five circles started at 13:59:13 UTC, the pair circle at 17:14:31 UTC on 6 threads)

| circle (kf 33) | winding | points | max step (rad) | alias bisections | verification mismatches | zeros inside (estimate) |
|---|---|---|---|---|---|---|
| control R 0.2 at lambda_phys | +1 | 30 + 2 | 0.345 | 0 | 0 | 2.043533 +0.000000i (2.4e-05) |
| R 0.36 at 2.85 + 0.25i | +3 | 76 + 2 | 0.381 | 4 | 0 | 2.574564 +0.268834i (6.9e-03); 2.959328 +0.027190i (6.2e-02); 2.964319 -0.026219i (4.8e-02) |
| R 0.36 at 2.85 - 0.25i | +3 | 76 + 2 | 0.381 | 4 | 0 | 2.574564 -0.268833i (6.9e-03); 2.959331 -0.027186i (6.2e-02); 2.964315 +0.026215i (4.8e-02) |
| R 0.36 at 3.35 + 0.25i | +2 | 60 + 2 | 0.392 | 4 | 0 | 3.275554 +0.194618i (2.9e-02); 3.465438 +0.343339i (1.8e-02) |
| R 0.36 at 3.35 - 0.25i | +2 | 60 + 2 | 0.392 | 4 | 0 | 3.275555 -0.194618i (2.9e-02); 3.465438 -0.343339i (1.8e-02) |
| R 0.05 at 2.962 (the pair) | +2 | 40 + 2 | 0.365 | 0 | 0 | 2.961992 +0.018132i (1.3e-06); 2.961993 -0.018132i (1.2e-06) |

Count of the box at kf 33 (as #551): 8 = the left outer pair of zeros 2.5746 +- 0.2688i (inside the left circles only), the pair near the real axis 2.961992 +- 0.018132i (R 0.05 winding +2: two zeros, inside both left circles), the right outer zeros 3.2756 +- 0.1946i and 3.4654 +- 0.3433i (inside the right circles only). Windings: left circles 3 = 1 + 2, right circles 2. #551: 6 at kf 29, 8 at kf 31.
