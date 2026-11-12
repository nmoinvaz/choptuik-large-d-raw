# I607-macm3: at which cut above kf 45 does each of #473's extra pairs enter? D 30.07, M 64, kf 55 and kf 51 first, then bisection

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon of 2026-11-09, modecount_cx of 2026-11-06 with B = 5), main checkout at de63a118 (the build of #518's runs, kept for comparability). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/607 (macm3's #518 recommendation; the coordinator's message of 2026-11-12 18:27 UTC: queue it when M 80 ends).

Method: #518's command at the odd cut K: python3 hp/modecount_circle.py hp/data/states/up6_D30.0688.npz 2.079747703853262,0,0.2 <the eight R 0.3 circles at #473's eight upper-half positions> --M=64 --kf=K --fmax=1e-15 --n0=20 --tag=D30.0688_M64_kfK --data=<raw>/I607-macm3/kfK/PART/data. Each cut in two processes with their own caches so that two threads work on it: A = the lambda_phys control (R 0.2) and the circles 0.055758+1.411769i, 3.871717+0.105316i, 4.285793+0.551490i, 4.656327+1.390362i (it makes the state, about 21 min at the load of #518 and #609, saved in hp/data of the main checkout as modecount_state_D30.0688_M64_kfK.npz); B = 0.847147+4.333559i, 1.057045+2.913917i, 1.978326+3.721021i, 4.070967+2.532063i (it starts when that state file exists and #605's runs are done). run_607.sh starts A of kf 55 and kf 51 when M 80 (#517) has ended, then the two B parts. Cuts: kf 55 as the coordinator set out, and kf 51 beside it, so that the first round splits the nine odd cuts 47 to 63 into 47 to 51, 53 to 55 and 57 to 63 (a pair that enters at or below 51 shows at both; between 51 and 55 at kf 55 only; above 55 at neither); then the next cuts by bisection.

Written before the run (the issue's). At each cut, each circle's winding, and the lambda_phys control within 1e-6 (+1). For each pair, the first cut at which its circle winds +1, or that none does below the no-cut state. References: #518 (kf 21, 33, 45: all eight circles 0) and #473 (no cut, M 64: all eight +1, the near-axis one with its conjugate +2).

## Results


## Results (2026-11-12 22:34 UTC; all four processes exit 0, exits.txt: kf55 B 21:46:25, kf51 B 22:01:12, kf51 A 22:33:06, kf55 A 22:33:25 UTC)

| # | position (D 30.0688, M 64, R 0.3) | kf 55: winding, points, alias bisections | kf 51: winding, points, alias bisections |
|---|---|---|---|
| 1 | 0.055758+1.411769i | +0, 20, 0 | +0, 20, 0 |
| 2 | 3.871717+0.105316i | +0, 20, 0 | +0, 20, 0 |
| 3 | 4.285793+0.551490i | +0, 20, 0 | +0, 20, 0 |
| 4 | 4.656327+1.390362i | +0, 20, 0 | +0, 20, 0 |
| 5 | 0.847147+4.333559i | +0, 20, 0 | +0, 20, 0 |
| 6 | 1.057045+2.913917i | +0, 25, 0 | +0, 42, 10 |
| 7 | 1.978326+3.721021i | +0, 20, 0 | +0, 20, 0 |
| 8 | 4.070967+2.532063i | +0, 28, 0 | +0, 28, 0 |

The lambda_phys control (R 0.2) winds +1 at both cuts: zero 2.079747703854784 (kf 55, 8.7e-12 from 2.079747703853262) and 2.079747703853617 (kf 51, 5.5e-11), the script's n0 / n0/2 estimate 1.5e-9 (a range, not a bound). All 16 circles at #473's positions wind 0 and have 0 verification mismatches (the table is made by a script that asserts it). The cuts 57 to 63 were not run (the coordinator's message of 2026-11-12 22:26 UTC): the pairs enter above kf 55, or only at no cut.
Part A's first start at 18:28 UTC (a gate that matched an old line) was killed after about two minutes, before any state; the runs above started at 18:47:17 (A) and 19:19:18 UTC (B). The state making took about 21 min. #609 and #612's runs shared the machine from 19:50 UTC.
