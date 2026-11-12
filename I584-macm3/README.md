# I584-macm3: det M in balls (exact determinant of the double-double mode matrix) at #579's stuck points s1 and s2 on the kf 29 state

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314. Code: a git worktree ~/Source/choptuik-large-d-b584 at main 14db20a9 (hp/modecount_qdet.py); the modecount_cx built there on 2026-11-12 11:27 UTC with hp/modecount_build.sh (1 min 49 s, build.log; hp/modecount_cx and hp/src are identical to ecca9c53, whose build passed the bit check against #473's cached determinants; the bit check was not repeated on this build) and the Python hpkernel of 2026-11-09. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/584 (win3 runs the other eleven points; this folder is macm3's part, the coordinator's message of 2026-11-12 11:26 UTC).

Checks before the run: python3 hp/modecount_qdet.py --selftest passes (planted permuted triangular n 12: error 0.0; random 30 x 30 against mpmath at 80 digits: 8.1e-71 against the bound 1e-40) and --selftest --mutate=no_lo fails as it must (4.2e-16 against 1e-40); selftest.log and selftest_mutate_no_lo.log.

Run (run_584.sh, from the worktree's hp/, 3 threads, nice 10, caffeinate -is): python3 -u modecount_qdet.py data/seeds/local/up23_D61.0264.npz 3.100221,0.002981 3.100564,-0.016648 --M=48 --kf=29 --fmax=1e-15 --threads=3 --ulp --draws=4 --json=<raw>/I584-macm3/kf29_s1s2.json. The state: the kf 29 one of #498 (hp/data/modecount_state_D61.0264_M48_kf29.npz, sha256 bfe7150859d4b92c...), the same STATE, --M, --kf and --fmax as #579's s1 and s2.

Written before the run (the issue's, comment of 2026-11-12 11:01 UTC). Per point the draws' largest |d arg| is the phase floor that double-double entries allow: noise at double-double if the floor exceeds 0.1 rad; resolved at double-double entries if it is below 1e-3 rad; otherwise the floor is reported. Predictions: the closed circles' points stay below 0.1 rad and the stuck points s1 to s4 exceed it; a stuck point's floor below 1e-3 means the floor does not explain the stuck circles. Report per point: the LU's d arg, the ulp row and the floor.

## Results

(11:50 UTC, macm3) Run 1: 11:29:53 to 11:50:00 UTC (exit 0, 1207 s on 3 threads; the planted check passed first, "check: pass"). Both points: the 320-bit ball determinant of the double-double mode matrix has radius 4e-62 or less, the exact input flag is true, and cdet = mode_det (bit for bit).
| point | double-double LU arg | exact (ball) arg | LU's d arg | ulp up in Re: double-double d arg | exact dets d arg | draws d arg (4) | floor (largest abs) | verdict |
|---|---|---|---|---|---|---|---|---|
| s1 3.100221 +0.002981i | +2.995423 | -0.604943 | -2.683 | +2.260 | +3.0e-5 | -0.178, -0.136, +0.0496, +0.0500 | 0.1783 | noise (above 0.1) |
| s2 3.100564 -0.016648i | +2.051857 | +1.920770 | +0.131 | -0.195 | -4.9e-5 | +0.0558, -0.131, -0.0475, -0.0029 | 0.1305 | noise (above 0.1) |
ln|det|: s1 double-double -134.2001, exact -133.3430 (LU's d ln|det| -0.857), one ulp up in Re -0.187 (double-double), -4.0e-4 (exact); s2 double-double -131.1128, exact -131.0532 (-0.0597), -0.095 and +3.0e-5. Entries differing between the two matrices of the ulp row: 439619 and 439625 of 5308416 parts.
The rule of the issue (fixed before the run): the draws' largest abs d arg is the phase floor double-double entries allow; noise at double-double above 0.1 rad, resolved below 1e-3 rad. s1 (0.178) and s2 (0.131) are above 0.1: noise, as predicted for stuck points. win3 runs the other eleven points.

(14:45 UTC, macm3) The kf 27 half (win3's, taken over: the coordinator's message of 2026-11-12 14:44 UTC, win3 silent since 09:08): run_584_kf27.sh, started 14:45:04 UTC from the same worktree (main 4b33cc9d, the modecount_cx built at 14db20a9): python3 -u modecount_qdet.py <raw>/I280-macm3/hp_data_after/modecount_state_D61.0264_M48_kf27.npz 3.595442,0.504558 4.530000,-1.061769 1.923548,0.910715 2.396619,0.567672 2.7387538820250192,-0.9076196541337447 3.6,1.0 4.35,-1.75 --M=48 --kf=27 --fmax=1e-15 --threads=3 --ulp --draws=4 --json=<raw>/I584-macm3/kf27_M48.json (the state file is the one in the worktree's hp/data, sha256 1fd892fcd0e32627..., arrays equal to I280's; s1 and s2 above were run through the seed, which loads the same kind of saved state). The points are #579's q3 and q4 and #585's N1, N2, F1, F2, F3.

(15:43 UTC, macm3) The kf 27 run finished: kf27_M48 exit 0 at 2026-11-12 15:40:18 UTC (started 14:45:04 UTC, 3314 s on 3 threads, 'check: pass'); the ball determinant took 52 to 79 s a point. Per point (the rule of the issue: floor = the draws' largest abs d arg; noise above 0.1 rad, resolved below 1e-3 rad):
| point | λ | DD LU arg | ball arg | LU d arg | ulp row: DD d arg | ulp row: exact d arg | draws d arg (4) | floor | verdict |
|---|---|---|---|---|---|---|---|---|---|
| q3 | 3.595442 +0.504558i | -1.026575 | -1.026347 | -2.28e-04 | +6.80e-04 | +1.00e-06 | -0.000229, +0.000724, -0.000499, -0.000265 | 0.000724 | resolved |
| q4 | 4.530000 -1.061769i | -2.468116 | -2.467992 | -1.24e-04 | +1.17e-05 | -4.92e-08 | -1.58e-05, +7.34e-05, +5.02e-05, +3.35e-05 | 7.34e-05 | resolved |
| N1 | 1.923548 +0.910715i | +1.540219 | +1.535106 | +5.11e-03 | -4.95e-03 | -1.75e-05 | -0.000833, -0.000377, -0.000606, -0.000874 | 0.000874 | resolved |
| N2 | 2.396619 +0.567672i | +2.358157 | +2.358244 | -8.74e-05 | +3.99e-03 | -1.92e-05 | -0.00167, -0.000284, -0.00116, +0.0015 | 0.00167 | between |
| F1 | 2.738754 -0.907620i | -2.761251 | -2.761921 | +6.69e-04 | -5.43e-04 | +1.76e-06 | -3.36e-05, -9.43e-05, +9.36e-05, +7.4e-05 | 9.43e-05 | resolved |
| F2 | 3.600000 +1.000000i | +1.998320 | +1.998345 | -2.49e-05 | +4.21e-04 | -3.77e-07 | +0.000463, +0.00026, -0.000125, +2.31e-05 | 0.000463 | resolved |
| F3 | 4.350000 -1.750000i | -2.580762 | -2.580744 | -1.74e-05 | +1.92e-04 | +4.52e-08 | -4.68e-05, -2.63e-06, +6.31e-05, -7.77e-05 | 7.77e-05 | resolved |

Six of the seven points are resolved (floors 7.3e-5 to 8.7e-4 rad); N2 (2.396619 +0.567672i) is between (1.67e-3 rad). The largest LU error is 5.1e-3 rad (N1). The double-double LU's args at q3 and q4 equal #579's plain args (-1.026575 and -2.468116).
