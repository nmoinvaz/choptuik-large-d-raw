# I568-macm3: det M's pivots at the top point of #445's unfinished circle (D 61.03, M 64, kf 23, lambda = 0.032 + 3.286i)

Machine: macm3 (Apple M3, 24 GB RAM). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/568 (filed by the coordinator after #445; the command is his message of 2026-11-12 06:03 UTC).

Same script and build as #552: hp/modecount_pivots.py and the modecount_cx built in the worktree ~/Source/choptuik-large-d-b80 at ecca9c53 (build.log in I517-macm3/; bit check passed, I517-macm3/bitcheck_473.log), with the Python hpkernel of venv-macm3-314 built 2026-11-09 02:44 (older than the hp/src changes of 2026-11-11). The state is #445's: I252-mac/states/modecount_state_D61.0264_M64_kf23.npz, sha256 179d0bd69aae77c9660518663896b59f232eedc7df1b89603767d525a17ddf6d (I445-macm3/state_sha256.txt), given as the seed; its M is 64, so nothing is resampled.

Command (run_568.sh, from the worktree's hp/, one thread, nice 10, caffeinate -is, after #552's two runs on the same thread): python3 modecount_pivots.py <raw>/I252-mac/states/modecount_state_D61.0264_M64_kf23.npz 0.032 3.286 --M=64 --kf=23 --fmax=1e-15 --json=<raw>/I568-macm3/top.json > <raw>/I568-macm3/top.log 2>&1. The planted control runs first (it must print "pass" twice); exit 1 means a check failed.

Written before the run (#552's, which the issue refers to). Verdict per part and shift: "localized" if at most 5% of the pivots carry 90% of the shift, all of them below 1e3 u ||M||; "global" if the shift is spread over more than half the pivots; otherwise the numbers. The question: is the arg noise of #445's unfinished circle (the arg jumps by more than pi/4 between 1066 of 1692 neighbouring pairs, ln|det| smooth at 534 to 559) double-double rounding.

## Results

(2026-11-12 06:40 UTC, macm3) Exit 0 at 2026-11-12 06:39:59 UTC (started 06:25 UTC; the script's check took 901 s). Kernel: the new modecount_cx (worktree ~/Source/choptuik-large-d-b80 at ecca9c53, built 06:00 UTC, bit check passed: I517-macm3/bitcheck_473.log) with the Python hpkernel of 2026-11-09. State: I252-mac/states/modecount_state_D61.0264_M64_kf23.npz, sha256 179d0bd69aae77c9660518663896b59f232eedc7df1b89603767d525a17ddf6d. Checks: planted twice (r 3: moved 3, want 3, localized; r 0: moved 0, none), consistency with mode_det, determinism: all pass.
n = 1536 pivots; plain: ln|det| 547.837668, arg +1.660778, pmin 3.232e-16, pmax 2.112e+07, ||M||_F 1.777e+10.
| part, shift | change of ln\|det M\| | pivots moved by more than 1e-3 in ln | pivots carrying 90% | all below 1e3 u \|\|M\|\| | rows differ at | verdict |
|---|---|---|---|---|---|---|
| hi +1 | +272.976 | 126 of 1536 | 23 | no (2.0e-3) | 92 | between |
| hi -1 | +270.006 | 126 | 22 | no (2.0e-3) | 92 | between |
| lo +1 | +1.197 | 15 | 5 | no (2.2e-19) | 8 | between |
| lo -1 | -0.743 | 14 | 7 | no | 7 | between |
Top pivots (k, |u| plain -> perturbed, d ln): hi +1: 1534: 3.2e-16 -> 3.5e-8 (+18.49); 1532: 4.5e-15 -> 6.2e-8 (+16.45); 1533: 3.5e-15 -> 4.5e-8 (+16.36); 1535: 1.2e-15 -> 1.4e-8 (+16.31); lo +1: 1534: 3.2e-16 -> 9.8e-16 (+1.114); 1532: 4.5e-15 -> 1.0e-14 (+0.804); 1535: 1.2e-15 -> 5.5e-16 (-0.757); 1533: 3.5e-15 -> 6.7e-15 (+0.658); 1531: 3.1e-14 -> 1.8e-14 (-0.556); lo -1: 1535: 1.2e-15 -> 2.7e-16 (-1.458); 1528: -0.294; 1534: +0.293; 1530: +0.248; 1532: +0.223; 1533: +0.201 (full lists in top.log). The script prints the perturbed LU's ln|det| and pmin but not its arg det, so the change of the phase is not in the output.

(2026-11-12 07:16 UTC, macm3) Rerun with modecount_pivots.py of main 80b5056 (it prints arg det's change; worktree ~/Source/choptuik-large-d-b80 at 80b5056, same build and state; run_568_arg.sh, top_arg.log and top_arg.json; started 06:59:52 UTC, exit 0 at 07:15:14 UTC, 921 s). The checks pass again and the numbers of ln|det| are those above. Change of arg det (wrapped to (-pi, pi]), plain arg det +1.660778:
| part, shift | arg det | change of arg det |
|---|---|---|
| hi +1 | +1.312158 | -0.3486 rad |
| hi -1 | +2.067691 | +0.4069 rad |
| lo +1 | +2.855928 | +1.1952 rad |
| lo -1 | -2.811594 | +1.8108 rad |
Top pivots' change of arg (lo +1): k 1534 +0.426, k 1532 -2.515, k 1535 +0.080, k 1533 -0.228, k 1531 +0.295, k 1527 +3.087; (lo -1): k 1535 -1.109, k 1528 +0.045, k 1534 -0.488, k 1530 +3.030, k 1532 -2.633, k 1533 -0.051 (full lists in top_arg.log).
