# T128-win2: octo-double pilot beside T127, 2 steps from T127's highest quad-double state

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2). Worktree `..\choptuik-t126` at origin/main 4eac02b (the T126
octo-double build, multidouble 4.0.0; 8e74094 -> 4eac02b is Python-only, no rebuild). venv-t126. 6 threads, below
normal, beside T127's chain2 (12 threads). Comms entry: 2026-11-06 06:30 UTC cloud to win2 (part 2).

Two octo-double steps (--jet_o 1) from T127's highest quad-double state D 171.2746 (T127-win2/chain/anm_pin3_D171.2746.npz),
where the quad-double series had collapsed (step 26: ratios 2-5 216.4 115.8 12.1 0.9, a_max 2.010, |z_N| 6.62e-25). The
pilot tests whether the octo-double series restores the high-order ratios at the same D.

  anm_run.py <raw> T128-win2\pilot --state T127-win2/chain/anm_pin3_D171.2746.npz --kfreeze 3 --N 24 --eps 1e-14
    --h_max 0.5 --steps 2 --D_max 200 --threads 6 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_o 1
    --reseed 2 --reseed_q 1
Post (beside T127's at the same D): ratios 2-5, a_max, |z_N|, predicted |F|, qd steps, Delta, seconds per step. The
coordinator decides the switch from that. The octo-double series is slow (T126's series_o was ~886 s at M 32).
