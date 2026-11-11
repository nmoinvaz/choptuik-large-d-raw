# I422-macm3: D = 4 at M 64, circles at lambda_g and lambda_phys (each must wind +1), and the rest of the real segment (0, 6) (each must wind 0)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at bfe5fd54. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/422 (was #201).

State: hp/data/lowD_states/lowDn_D4.0000_M64.npz (M 64, nodes 11, kt 36, kc 80, ks 200). Command (circles.cmd, caffeinate -is, nice 10, one thread): hp/modecount_circle.py on it with --M=64 --fmax=1e-15 --n0=20.
The coordinator's message said "by #70's job 3 command with the M 64 state". #70's job 3 command (I70-macm3/job3/count.cmd) is a count by modecount_wind.py at M 48, not circles; the issue body asks for circles, so this run is the issue body's.

Written before the run. Setup check first: |F| <= 1e-15 and Delta within 1e-8 of 3.4454524022410, else report and stop (the process is stopped after its setup lines). Part 1, the two controls (R 0.2): lambda_g = 0.6138552550 (the M 48 value of I70 job 3)
and lambda_phys = 2.6740838; each must wind +1. Part 2, the rest of the real segment (0, 6) with circles that each must wind 0, is NOT started: the issue names no centres or radii, and the circles must avoid the zero at 0, lambda_g and lambda_phys;
a set is proposed on the issue for the coordinator's approval. Reported per circle: winding, largest step, verification mismatches and alias bisections; estimates are ranges, not bounds.

## Results

Part 2 (coordinator's 15:33 UTC message, circles widened so that neighbours overlap and none passes within 0.07 of a known zero; each must wind 0): 0.3 R 0.2; 1.3 R 0.6; 2.2 R 0.32; 3.32 R 0.52; 4.35 R 0.57; 5.45 R 0.57,
all on the real axis, in a second process on its own cache (data_seg/), command in circles_segment.cmd. The two controls (R 0.2 at 0.6138552550 and 2.6740838) keep running in the first process. Gaps along the real axis, from the radii:
the controls cover 0.414 to 0.814 and 2.474 to 2.874; 0.3 R 0.2 covers 0.1 to 0.5, 1.3 R 0.6 covers 0.7 to 1.9, 2.2 R 0.32 covers 1.88 to 2.52, 3.32 R 0.52 covers 2.8 to 3.84, 4.35 R 0.57 covers 3.78 to 4.92, 5.45 R 0.57 covers 4.88 to 6.02.
So the real segment is covered from 0.1 to 6.02 with overlaps, and (0, 0.1) is not covered (the zero at 0 is 0.1 from the first circle's edge).
Controls exit 0 at 17:53:26 UTC; segment exit 0 at 21:01:10 UTC (started 17:54 UTC). Setup |F| 9.1e-30 (limit 1e-15). Delta of the state, zh[-1] + zl[-1] = 3.4454524040781, 1.84e-09 from 3.4454524022410 (limit 1e-8): passes.
Controls (R 0.2): lambda_g 0.6138552550 winding +1 (zero 0.613855 +0i, estimate 9.2e-07, 27 points, largest step 0.384); lambda_phys 2.6740838 winding +1 (zero 2.674078 -0i, estimate 1.8e-11, 28 points, 0.353).
Segment circles, all winding 0, 0 verification mismatches: 0.3 R 0.2 (22 points, 0.337); 1.3 R 0.6 (33, 0.337, 4 alias bisections); 2.2 R 0.32 (21, 0.357); 3.32 R 0.52 (24, 0.365); 4.35 R 0.57 (20, 0.035); 5.45 R 0.57 (20, 0.006).
