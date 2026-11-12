# I569-macm3: the control of #569's 0.5 rad rule, the arg of det M under one double-double ulp at points where circles closed (D 61.03)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314. Kernel: the new modecount_cx built in the worktree ~/Source/choptuik-large-d-b80 at ecca9c53 on 2026-11-12 06:00 UTC (bit check passed: I517-macm3/bitcheck_473.log) with the Python hpkernel of 2026-11-09; modecount_pivots.py of main 80b5056 (the worktree is at 80b5056). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/569 (closed as not computable at double-double after the first step, I568-macm3/top_arg.log; this folder holds the control the coordinator asked for in his message of 2026-11-12 07:23 UTC). The results are posted on #569.

Runs (run_ctl.sh, from the worktree's hp/, one thread each, nice 10, caffeinate -is, python3 modecount_pivots.py STATE RE IM --M=M --kf=KF --fmax=1e-15 --json=<raw>/I569-macm3/NAME.json): kf22_2.0510 (data/seeds/local/up23_D61.0264.npz, 2.0510 0i, M 48, kf 22: a point of #506's R 0.0075 circle, the state sha256 7dd8e81469dbf2f7...), d61_1.98_1.50 (I252-mac/states/modecount_state_D61.0264_M64_kf23.npz, sha256 179d0bd69aae77c9660518663896b59f232eedc7df1b89603767d525a17ddf6d, 1.98 +1.50i, M 64, kf 23: the top of #445's 1.98 +1.20i R 0.3 circle, which closed with winding 0), d61_2.0435_0.2 (the same state, 2.0435 +0.2i: the top of #445's lambda_phys R 0.2 circle, which closed with winding +1).

Written before the run (the coordinator's). The rule's quiet side passes when every one of the three shows less than 0.01 rad of arg change under one double-double ulp (part lo), at both signs. If any shows more, the 0.5 rad rule cannot separate the cases, #569's closing must be reopened, and the numbers are reported. For reference, the points of the noisy side: 3.1023 -0.0068i at kf 29: lo +1 -0.715 rad, lo -1 +0.926 rad; 0.032 +3.286i at D 61 M 64 kf 23: lo +1 +1.195 rad, lo -1 +1.811 rad.

## Results

(2026-11-12 08:11 UTC, macm3) Exits (exits.txt): kf22_2.0510 07:55:36 UTC (7 min), d61_1.98_1.50 08:06:13 UTC (15 min), d61_2.0435_0.2 08:10:47 UTC (15 min); all exit 0, the planted controls twice, consistency with mode_det and determinism pass in each.
Change of arg det (wrapped) under one double-double ulp (lo) and one high-part ulp (hi) of dh[10,11]:
| point | plain arg det | lo +1 | lo -1 | hi +1 | hi -1 |
|---|---|---|---|---|---|
| kf 22, 2.0510 + 0i (M 48) | +3.6e-11 | -0.0000 | -0.0000 | -0.0000 | -0.0000 |
| D 61 M 64 kf 23, 1.98 +1.50i | +1.725234 | -0.0010 | **-0.0189** | -1.8719 | +0.9738 |
| D 61 M 64 kf 23, 2.0435 +0.2i | -0.035785 | +0.0095 | **-0.0323** | -0.6818 | -2.9540 |
Smallest pivots: kf 22 point 8.4e-14; 1.98 +1.50i 2.2e-14; 2.0435 +0.2i 2.2e-14 (the noisy points: 3.7e-16 at kf 29 and 3.2e-16 at D 61 M 64 0.032 +3.286i). The change of ln|det M| under lo: 0.000, +0.021 and -0.032, -0.025 and +0.083 (the noisy points: -0.19 and 1.20, -0.74).
Quiet side of the rule (every control below 0.01 rad at both signs): NOT passed by the threshold as written: two of the six values exceed 0.01 rad (-0.0189 at 1.98 +1.50i lo -1 and -0.0323 at 2.0435 +0.2i lo -1); the kf 22 point is on the real axis, where the arg is 0 whatever the perturbation (a sign flip is the only way to change it), so it can only fail by a flip. The largest quiet value (0.0323) is 22 times smaller than the smallest noisy value (0.715, kf 29), and 15 times below 0.5; the rule is reported against the coordinator's text and the decision is his.
