# I579-macm3: T = 0.2 rad phase-noise rule, tested on eight fresh points (D 61.03; four quiet, four stuck)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314. Kernel: the new modecount_cx built in the worktree ~/Source/choptuik-large-d-b80 at ecca9c53 on 2026-11-12 06:00 UTC (bit check: I517-macm3/bitcheck_473.log) with the Python hpkernel of 2026-11-09; modecount_pivots.py of main 80b5056 (the worktree is at 80b5056). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/579 (the coordinator's message of 2026-11-12 08:13 UTC). The eight points were listed on the issue before any run (comment of 08:15 UTC): q1 1.980000+0.749808i, q2 1.698092+1.097394i (D 61 M 64 kf 23, circles of #445 that closed), q3 3.595442+0.504558i, q4 4.530000-1.061769i (kf 27 M 48, circles of #507 that closed), s1 3.100221+0.002981i, s2 3.100564-0.016648i (kf 29 M 48, #498's R 0.01 circle), s3 0.132000+2.912795i, s4 -0.141205+3.186000i (D 61 M 64 kf 23, #445's unfinished R 0.2 circle).

Runs (run_579.sh NAME STATE RE IM M KF; chainA.sh runs q1, s3, q3, s1 and chainB.sh q2, s4, q4, s2, two threads, nice 10, caffeinate -is): python3 modecount_pivots.py STATE RE IM --M=M --kf=KF --fmax=1e-15 --json=<raw>/I579-macm3/NAME.json. States: I252-mac/states/modecount_state_D61.0264_M64_kf23.npz (sha256 179d0bd69aae77c9660518663896b59f232eedc7df1b89603767d525a17ddf6d), and from the worktree's hp/data the kf 27 state (sha256 1fd892fcd0e32627...) and the kf 29 state (sha256 bfe7150859d4b92c...), loaded through data/seeds/local/up23_D61.0264.npz.

Written before the run (the issue's). A point is at double-double's noise floor if one double-double ulp of dh[10,11] (part lo, both signs) changes arg det M by more than T = 0.2 rad at either sign. The rule holds if all four quiet points stay below 0.2 rad at both signs and all four stuck points exceed it at some sign, with the planted and consistency checks passing at each point. If any point lands on the wrong side, the rule fails and #569's and #571's verdicts stay open.

## Results

(2026-11-12 09:03 UTC, macm3) All eight runs exit 0 (exits.txt): q1 and q2 at 08:30:47 and 08:30:49 UTC, s3 and s4 at 08:47:35 and 08:47:36, q3 and q4 at 08:55:45 and 08:55:46, s1 and s2 at 09:02:45 and 09:02:46 UTC (started 08:15:25 UTC; 15 min per M 64 point, 7 min per M 48 point); planted controls twice, consistency with mode_det and determinism pass at every point.
Change of arg det (wrapped) under one double-double ulp (part lo) and one high-part ulp (hi) of dh[10,11]; T = 0.2 rad:
| point | class | plain arg det | lo +1 | lo -1 | hi +1 | hi -1 | smallest plain pivot | judged on lo |
|---|---|---|---|---|---|---|---|---|
| q1 1.980000+0.749808i | quiet | -1.2681 | -0.0044 | +0.0405 | +1.3885 | -0.9068 | 2.4e-14 | below T: right |
| q2 1.698092+1.097394i | quiet | -0.5660 | -0.0293 | +0.0621 | -2.6147 | +0.8452 | 1.2e-14 | below T: right |
| q3 3.595442+0.504558i | quiet | -1.0266 | +0.0024 | -0.0016 | +2.3185 | -0.1017 | 4.9e-14 | below T: right |
| q4 4.530000-1.061769i | quiet | -2.4681 | +0.0003 | +0.0000 | +0.9316 | -0.6836 | 8.1e-13 | below T: right |
| s1 3.100221+0.002981i | stuck | +2.9954 | -2.7518 | +1.4949 | -2.9121 | +0.2275 | 1.6e-16 | above T: right |
| s2 3.100564-0.016648i | stuck | +2.0519 | -0.1098 | -0.0035 | -2.5173 | +0.6355 | 7.4e-16 | **below T: WRONG side** |
| s3 0.132000+2.912795i | stuck | -1.7571 | +2.9527 | +0.5138 | +0.9372 | +2.0629 | 4.9e-16 | above T: right |
| s4 -0.141205+3.186000i | stuck | +2.4952 | -2.8486 | +1.0909 | -2.7448 | -1.8854 | 2.1e-16 | above T: right |
Verdict (the issue's): the rule fails, since stuck point s2 changes arg det by at most 0.1098 rad under lo, below T = 0.2 rad, at both signs. Seven of eight lie on the right side. The largest quiet value over all quiet points of #569 and #579 is 0.0621 rad, the smallest of the stuck points over the same two issues' values is 0.1098 rad (s2), then 0.715 (kf 29, #552).
Observation after the runs (not a rule, in-sample): the smallest pivot of the plain LU separates the eight, and the earlier points of #552, #568 and #569: stuck 1.6e-16 to 7.4e-16, quiet 1.2e-14 to 8.1e-13. Along whole circles of the existing caches (field pmin): the unfinished #445 circle 1.8e-17 to 1.35e-15 (1693 points), #498's R 0.01 circle 1.6e-16 to 8.1e-16 (42), and every circle that closed (#445's three, #498's kf 29 control, #506's, #507's) has pmin from 7.3e-15 upward at all its points.
