# I493-macm3: hp/near_null.py on the 0.3-0.8 re-noded start of crawlJ's D 242.3642 state, and its control

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon), main checkout at de63a118 (near_null.py needs a9b0885 or later), started 2026-11-11 16:28 UTC. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/493.

Input: I489-mac/renode_L1_horizon_D242.3642.npz (blob 933970e8) read from RAW = my push worktree ~/Source/choptuik-large-d-raw-push at origin/main, not from this clone: this clone is on the pre-rewrite history and #445 still writes in it, so the coordinator chose option 2 (message 162541Z). Outputs are in this folder as the issue's commands write them.
Commands (run_near_null.sh): the issue's two, with RAW = the worktree, 2 threads, nice 10, caffeinate -is. The control (--mutate=sigma) runs only if the first run exits 0.

Written before the run (the issue's). Reading rule: sigma_1 is compared with #488's 2.55e-27 (0.3-0.7, same D): above it by more than 10x, the 0.8 layout widened the weakest direction (#495 may start); within 10x or below it, the 0.8 layout does not help. Acceptance: near_null's own check passes (exit 0) and the --mutate=sigma control fails (nonzero); sigma_1..sigma_4 and their top components are tabled against #488 (sigma_1 2.55e-27, sigma_2 2.53e-27, sigma_3 4.39e-26, sigma_4 7.93e-26), with the verdict on sigma_1.

## Results

near_null exit 0 at 16:40:04 UTC on 2026-11-11 (started 16:28), check pass (||J v_1|| / sigma_1 = 1.000000, converged sigma_1 to 0); control --mutate=sigma exit 1 at 16:51:52 UTC, check FAIL (ratio 0.952381), as it must. D 242.364, L 897, octo-double LU 331 s, pivots 7.8e-37 .. 4.4e+20 (near_null_L1.log, near_null_L1.json).

| | this start (0.3-0.8, L 897) | #488 (0.3-0.7, L 769) | ratio |
|---|---|---|---|
| sigma_1 | 8.433e-38, delta share 1.0, top m_h k1 0.01 | 2.55e-27, harmonic 3 pair | 3.3e-11 |
| sigma_2 | 6.954e-35, p1 k3 0.11, m_h k3 0.08, nodes 5 and 4 k3 | 2.53e-27, the same pair | 2.7e-8 |
| sigma_3 | 6.968e-35, the same pair, delta 1.5e-5 | 4.39e-26, delta 0.70, harmonic 1 | 1.6e-9 |
| sigma_4 | 1.766e-34, p1 k1 0.10, m_h k1 0.09, delta 7.8e-4 | 7.93e-26, delta 0.30, harmonic 1 | 2.2e-9 |

By direction (my matching by top components, not a script output): the harmonic 3 pair is sigma_2, sigma_3 here (6.954e-35, 6.968e-35) against 2.55e-27, 2.53e-27 in #488 (ratios 2.7e-8, 2.8e-8); the delta direction is sigma_1 here (8.433e-38, delta share 1.0) against #488's sigma_3 4.39e-26 (delta 0.70), ratio 1.9e-12; the harmonic 1 direction is sigma_4 here (1.766e-34) against 7.93e-26, ratio 2.2e-9. So the whole spectrum is 8 to 12 orders lower than at 0.3-0.7. The sigma are not scale-invariant across layouts (the rows and columns of the two systems are scaled differently), which I did not test; the horizon segment's amplification (0.7/0.8)^(D-3) = 1.3e-14 is of the right size, as an untested guess.

Verdict by the written rule: sigma_1 is below 2.55e-27 (by 3e10), so the 0.8 layout does not help and #495 does not start. The first Newton step's size by block and its delta component is not printed or stored by hp/near_null.py (it keeps the LU of newton_o, not the step), so it is not reported.
