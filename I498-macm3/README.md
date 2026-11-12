# I498-macm3: #472's box 2.6 < Re lambda < 3.6, |Im lambda| <= 0.5 at D 61.03, M 48, at the cuts kf 24, 26 and 28 (kf 24 first)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at de63a118 (the hp build is the older one, no rebuild). Started 2026-11-11 17:07 UTC. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/498.

Stage 1 at kf 24 (kf24/stage1.cmd): #472's command with --kf=24 --tag=D61.0264_M48_kf24 --data=<raw>/I498-macm3/kf24/data: the lambda_phys control (2.043532530673195, R 0.2) and four R 0.36 circles at 2.85 +-0.25i and 3.35 +-0.25i, --M=48 --n0=20 --fmax=1e-15, one thread, nice 10, caffeinate -is, on hp/data/seeds/local/up23_D61.0264.npz. There is no kf 24 state or cache: the setup makes the state from the seed (the time it takes and where it is saved are reported below), and the cache starts empty, so the control is a real run, not a replay. Stage 2 (R 0.06 to 0.1 circles on the zeros found) follows when stage 1 is read; kf 26 and 28 follow when a thread frees.

Written before the run (the issue's). At each cut the windings above and below are equal, each zero found has a +1 circle, and the lambda_phys control's miss is reported. Reference counts in the box: kf 22: 1 pair (2.6897 +-0.4761i); kf 23: 1 pair (3.0196 +-0.0958i, #230); kf 25: 2 pairs (#447); kf 27: 3 pairs (#472).

## Results


(2026-11-12 03:44 UTC, macm3) **Stopped early, stage 1 not finished at any cut.** kf 24 and kf 26 were stopped at 2026-11-11 20:23:54 and 20:23:40 UTC (exit 143): an even kf is the odd cut below it (plow_odd sums the odd harmonics k <= kf), so kf 24 is kf 23 and kf 26 is kf 25 (the kf 26 state is byte-identical to kf 25's, sha256 48ac56a2...; the coordinator agreed the premise was his error). Their partial logs are in kf24/ and kf26/ (kf 24: control 2.043533, first pair 3.016775 +-0.0995i, estimate 2.5e-2; kf 26: control 2.043535, pairs 2.9042 +0.2444i and 3.2564 +0.2266i). kf 29 and kf 31 (kf29/, kf31/, started 20:23:57 UTC, states made in 12 min 30 s each, saved as hp/data/modecount_state_D61.0264_M48_kf29.npz and ..._kf31.npz): the lambda_phys control (R 0.2) winds +1 with the zero at 2.043549 +0.000220i (kf 29, miss 2.2e-4) and 2.042244 -0.001476i (kf 31, miss 2.0e-3); the first R 0.36 circle (2.85 +0.25i) did not close at either cut: kf 31 was stopped by the coordinator's decision at 02:39:45 UTC (exit 143, 328 points on the circle, cache kept so the circle can resume) and kf 29 at 03:43:03 UTC (exit 143, 384 points on the circle) after the test below. At both cuts most of the points sit in one part of the circle (kf 29: 266 of the 320 points present at 02:33 UTC within 0.06 rad of -45.5 deg, lambda 3.1023 -0.0068i, smallest angular step 7.7e-5 rad; kf 31: 207 of 322 within 0.06 rad of -57.4 deg, lambda 3.0440 -0.0532i, 1.9e-5 rad), where the arg jumps between neighbouring points while ln|det| varies by 5 (kf 29) and 1.4 (kf 31) units.

**The ulp test** (the coordinator's message 023811Z; ulp29/, started 02:39 UTC). The R 0.01 circle around 3.1023 -0.0068i (n0 20, --M=48 --kf=29 --fmax=1e-15) on the kf 29 state, with I506's wrapper (ulp_circle.py, copied here, identical to I506-macm3/ulp_circle.py; the coordinator's message called it ulp_sensitivity.py), once as it is (plain, shift 0) and once with dh[10,11] one ulp up, each with an empty cache. plain: stopped by me at 03:19:31 UTC (exit 143) after 40 min, circle open (44 determinants, 42 on the circle: the 20 starting points and 22 bisection points; its 20 starting points alone give a winding of +1 with steps up to 2.33 rad, 8 of the 42 steps above pi/4, so it is not a result). ulp: exit 0 at 03:41:12 UTC (22 min), the circle closed, winding 0, 20 points, largest step 6.3e-5 rad, 0 mismatches. The two runs share 22 points (same lambda to the last bit):

| angle on the circle | \|λ − c\| | arg plain | arg +1 ulp | \|Δarg\| | ln\|det\| plain | ln\|det\| +1 ulp |
|---|---|---|---|---|---|---|
| -162° | 0.01 | +1.037 | -0.277 | 1.313 | -131.9 | 134.0 |
| -144° | 0.01 | +0.955 | -0.355 | 1.310 | -131.2 | 134.0 |
| -126° | 0.01 | +1.529 | -0.416 | 1.945 | -131.3 | 134.1 |
| -108° | 0.01 | +1.557 | -0.456 | 2.013 | -131.0 | 134.2 |
| -90° | 0.01 | +2.324 | -0.470 | 2.793 | -131.0 | 134.3 |
| -72° | 0.01 | +2.534 | -0.456 | 2.990 | -130.8 | 134.3 |
| -54° | 0.01 | +3.007 | -0.416 | 2.860 | -130.8 | 134.4 |
| -36° | 0.01 | -2.889 | -0.354 | 2.535 | -130.9 | 134.5 |
| -18° | 0.01 | -2.365 | -0.276 | 2.089 | -131.2 | 134.5 |
| 0° | 0.01 | -1.858 | -0.190 | 1.668 | -131.7 | 134.5 |
| 18° | 0.01 | -0.807 | -0.104 | 0.704 | -131.1 | 134.5 |
| 36° | 0.01 | -0.302 | -0.026 | 0.276 | -132.2 | 134.5 |
| 54° | 0.01 | +0.283 | +0.036 | 0.247 | -131.6 | 134.4 |
| 72° | 0.01 | +0.665 | +0.076 | 0.589 | -132.8 | 134.3 |
| 90° | 0.01 | +0.102 | +0.089 | 0.012 | -132.8 | 134.3 |
| 108° | 0.01 | -2.225 | +0.076 | 2.300 | -133.9 | 134.2 |
| 126° | 0.01 | -0.156 | +0.036 | 0.193 | -132.4 | 134.1 |
| 144° | 0.01 | +0.108 | -0.026 | 0.134 | -132.6 | 134.0 |
| 162° | 0.01 | +0.338 | -0.104 | 0.442 | -131.9 | 134.0 |
| 180° | 0.01 | +0.691 | -0.190 | 0.881 | -131.9 | 134.0 |
| 0° (beta point) | 0.02 | -1.016 | -0.190 | 0.826 | -129.5 | 134.8 |
| 180° (beta point) | 0.02 | +0.234 | -0.190 | 0.425 | -131.3 | 133.7 |

Criteria (the coordinator's, fixed before the run): **noise** if at matched points arg det differs by more than 0.5 rad somewhere or the two windings differ. Result: |Δarg| exceeds 0.5 rad at 15 of the 22 matched points, the largest is 2.990 rad at -72 deg (lambda 3.10539 -0.01631i), the smallest 0.012 rad (at 90 deg), so the condition is met, and the windings differ (plain open, +1 on its starting points; +1 ulp closed at 0). By the criterion the stuck arc is rounding noise and the stage 1 of both cuts is "not finished: phase at the noise floor".

Not in the criteria, found while comparing: **ln|det| differs by +264.3 to +268.1 at every matched point** (plain -129.5 to -133.9, +1 ulp +133.7 to +134.8), and the smallest pivot pmin goes from 1.6e-16 to 1.0e-15 to 1.05e-11 to 2.13e-11. The same offset is in the caches of #506 (+224.2 to +224.6 at kf 27, +109.3 to +109.6 at kf 22) and #520 (+199 to +238 for the other entries and directions), which I did not report there: those posts gave the movement of the zero only. A constant offset does not change a winding, but it says that the absolute value of det M is not fixed by the inputs to one ulp in this build. Reading (mine, not tested): in the plain run the args at the 18 deg points rise from +1.04 at -162 deg to +3.01 at -54 deg and go on through -2.89, -2.37, -1.86 (wrapped) at -36, -18 and 0 deg, a smooth turn of the kind that goes with a zero inside the circle, with an irregular stretch between 81 and 113 deg, plus noise; under +1 ulp the phase is flat, so either that zero moved by more than 0.01 or the plain phase was noise. This test cannot tell the two apart; both leave the count near 3.10 -0.007i at kf 29 undetermined.
