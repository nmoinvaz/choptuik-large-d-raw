# I644-win2: A/B of the octo-double corrector's trial test on #603's refused step at D 249.39

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), 9 threads per run. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/644 (assigned by the coordinator on the agent-msg channel, message 1794553286702-0, 2026-11-13 06:3x UTC; to start when #551 has ended).
Code: worktree `D:\choptuik-i644` detached at origin/main 5b9059ec ("octo_corrector: print each natural-test trial at the default verbosity"); venv-i600 (the #600 build, hpkernel `_hpkernel.cp314-win_amd64.pyd` sha256 4ede9afe..., the kernel #603 runs on); the A/B touches only Python files. #603's chain is read in place and left running: the start state is `I603-win2/chain/anm_pin3_D248.6298.npz`.
Command: `run_644.sh`: `anm_run.py ... --steps 1 --a0 0.762939453125 --od_accept own` and then `--od_accept natural` (a0 is #603's own a at that step, 0.610 x 1.25, exactly), the other flags #603's, 9 threads, BelowNormal (nice -n 5), OPENBLAS_NUM_THREADS=1. Outputs `own/` and `natural/`, logs `own.log` and `natural.log`, starts and exits in `exits_644.txt`.

To report (#644): (1) `own` must repeat #603's chain.log lines 432 to 441 (line 432 `a 0.7629: re-seeded (ok)` to line 441 `a 0.763 -> D 249.392721272 ... 767 s`, the a 0.763 attempt: |F| 6.92e-34 -> 4.89e-25 ..., "no trial step accepted" on step 4, refused); say whether the lines are identical. (2) `natural`: each "trial lam" line (lam, max|F|, the ratio and its bound), each step's |F| and |dz|, accepted or refused, its seconds against `own`'s. (3) If `natural` converges at a 0.763: its Delta (eight parts summed) against #603's state `I603-win2/chain/anm_pin3_D249.3927.npz` (1.685054158679257706013773262194860158710), and both D_str values; compare Delta only if the D_str values are equal.



## Results (2026-11-13 07:41:27 to 08:43:10 UTC)

`exits_644.txt`: own 07:41:27 to 08:18:10 (37 min), natural 08:18:10 to 08:40:48 (23 min), near_null 0763 08:40:48 to 08:41:56, near_null 0381 08:41:56 to 08:43:10; every exit 0.

**1. `own` (the control) repeats #603.** Its a 0.7629 attempt (own.log lines 8 to 17) against #603's chain.log lines 432 to 441: nine of ten lines identical with the seconds masked (every |F|, |dz|, lam and dDelta per Newton step the same: 6.92e-34 -> 4.89e-25 -> 4.50e-27 -> 1.97e-28 -> 1.44e-28, "no trial step accepted, stopping" on step 4, 5 steps, not converged, moved 4.7e-30); line 441 differs in the printed tol (1.3e-20 here, 8.2e-17 in #603: the ramp 1.0e-20 x 1.45^(D - D_base) restarts at the run's own base) and the seconds (884 s against 767 s). The retry at a 0.3815 (own.log 18 to 26, #603 442 to 450): eight of nine identical, the ninth differing in the tol (1.2e-20 against 7.1e-17) and seconds; accepted, 3 Newton steps, max|F| 2.0e-61.

**2. `natural` refuses the a 0.7629 attempt at its first Newton step** (natural.log lines 8 to 22): the start max|F| 6.92e-34, |dz| 3.9e-30; the trials of step 0, with the ratio (simplified correction / |dz|) and its bound:

| trial lam | max\|F\| | ratio | bound | verdict |
|---|---|---|---|---|
| 1 | 4.89e-25 | 5.589e+04 | 0.750 | refused |
| 0.5 | 1.22e-25 | 6.710e+03 | 0.875 | refused |
| 0.25 | 3.06e-26 | 8.221e+02 | 0.938 | refused |
| 0.125 | 7.64e-27 | 1.025e+02 | 0.969 | refused |
| 0.0625 | 1.91e-27 | 1.357e+01 | 0.984 | refused |
| 0.03125 | 4.77e-28 | 2.543 | 0.992 | refused |
| 0.015625 | 1.19e-28 | 1.181 | 0.996 | refused |
| 0.0078125 | 2.98e-29 | 1.017 | 0.998 | refused |
| 0.00390625 | 7.46e-30 | 0.9992 | 0.999 | refused |

"no trial step accepted, stopping": 1 octo-double step, not converged, 63 s for the attempt (own: 5 steps, 884 s). The ratio falls from 5.6e4 to 0.9992 as lam goes from 1 to 0.004 and stays above the bound 0.999 in the last trial (0.9992 > 0.999): even at lam 0.004 the simplified correction is as long as the step. The retry at a 0.3815: step 0 trial lam 1, max|F| 1.60e-35, ratio 4.919e-07 (bound 0.750), accepted; step 1 trial lam 1, max|F| 1.97e-61, ratio 1.275 (bound 0.750), accepted (it is below tol_od); converged, 3 Newton steps, max|F| 2.0e-61; 172 s (own: 195 s). The whole natural run took 22.6 min against own's 36.7 min, the saving being the refused attempt (63 s against 884 s).

**3. The test did not converge at a 0.763, so no Delta comparison is asked for.** As a check the other way: the accepted a 0.3815 retry state `anm_pin3_D249.0113.npz` of `own` and of `natural` has the same D_str as #603's (249.01125154495239261316641421473150330712087452411) and the same Delta, the eight parts summed exactly, 1.68511655685031179624120523443370911437019757 (the differences, own - #603, natural - #603 and natural - own, are exactly 0 at 60 digits).

**4. near_null on the two saved predictions** (`near_null_644.sh`, `--k=4 --threads=9`, 68 and 74 s; both `check: pass`, ||J v_1|| / sigma_1 = 1.000000; `near_null_pred_0763.log/json`, `near_null_pred_0381.log/json`). The saved `pred_pin3_*.npz` is the prediction before its re-seed (anm_run.py: `--save_pred 1` stores each prediction before its re-seed), and near_null makes the plan again at the state ("the state has no stored plan"), so these are the raw predictions' systems, not the corrector's re-seeded starts.

| | a 0.763 prediction (D 249.3927, refused in #603) | a 0.3815 prediction (D 249.0113, accepted) |
|---|---|---|
| pivots | 2.9e-01 .. 3.9e+35 | 4.6e-06 .. 3.4e+35 |
| sigma_1 | 1.371e-02 | 6.948e-07 |
| sigma_2 | 9.272e-02 | 3.272e-05 |
| sigma_3 | 9.615e-02 | 3.458e-05 |
| sigma_4 | 9.654e-02 | 4.246e-05 |
| v_1: share in Delta | 9.0e-03 | 1.0 |
| pinned step: norm \|dz\| | 3.593e+01 | 3.906e-10 |
| pinned step: max\|dz\| | 3.802 | 3.585e-10 |
| pinned step: Delta | -0.2764 | +3.585e-10 |
| V^T dz on v_1..v_4 | +27.0, -3.71, +1.71, +4.41 | +3.59e-10, -3.47e-11, -2.46e-11, +1.47e-10 |
| share of the pinned step on span(V) | 0.7699 | 1.0000 |
| share on v_1 alone (V^T dz_1 / norm) | 0.75 | 0.92 |

Reading, for the question "does the refused start's error lie along the weak directions": the accepted start's pinned step (3.9e-10) lies entirely on the four weakest directions (share 1.0000, 92% on v_1, which is pure Delta: delta share 1.0, sigma_1 6.9e-7); the refused start's pinned step is large (norm 36, max 3.8, eleven orders above the accepted start's) and 77% of it lies on the span of its four weakest directions (75% on v_1, whose singular value is 1.4e-2, with a Delta share of 0.9% and its weight on the node c blocks at harmonic k2), but these directions are not weak: sigma_1..4 are 1.4e-2 to 9.7e-2, 2e4 to 2e3 times those of the accepted start. So the refused raw prediction is far from the solution along the least-stable directions of its own system, which are not the nearly-singular Delta direction of the accepted start. Caveat: the two plans are made again at their states (pivots from 0.29 against 4.6e-6), so the two systems are not the same system; and in the chain these raw predictions are re-seeded (horizon data refined in octo-double) before the corrector starts, after which the first move is |dz| 3.9e-30 for the refused attempt and 6.6e-36 for the accepted (own.log), so the raw pinned steps say what the re-seed has to remove, not what Newton starts with.

