# T150-win2: the chain_fit chain from D 215 toward 400, junk frozen in the octo-double corrector

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2). Worktree `..\choptuik-t126` at 79d3e84 (has --od_junk; Python
only; no rebuild). venv-t126. 18 threads, below normal. Comms entry: 2026-11-07 15:44 UTC cloud to win2.

T138 stopped at D 215 because the octo-double corrector's Newton step is rejected along a direction whose pivot is
7e-16 (condition 2.4e30), falling ~0.6x per unit of D -- it is p1's highest harmonics, which carry no Delta. --od_junk 4
freezes that junk among the 4 weakest directions of each corrector's first Jacobian (as full_release.py --junk 4 does
for the release). No chain has run with it. Nathan wants the chain to D 400.

Pilot (3 steps) from T138-win2/chain_o/anm_pin3_D215.0000.npz:
  anm_run.py <raw> T150-win2\pilot --state T138-win2/chain_o/anm_pin3_D215.0000.npz --kfreeze 3 --held_fit data/held_fit.json
    --N 24 --eps 1e-14 --h_max 1.0 --steps 3 --D_max 400 --threads 18 --corrector od --tol_od 1e-40 --od_junk 4 --qd_it 12
    --jet_o 1 --reseed 2 --reseed_q 1 --save_pred 1
Pass: base polish converged (with junk frozen, "projected correction below ... converged" counts) and >= 2 of 3 steps
converge. Then the chain: same command into T150-win2\chain with --state <pilot's last state> --steps 400. Stop on a
three-halvings stop, after 24 h, or at D 400; hang rule (no log line 20 min + one core: py-spy dump, kill, restart h_max
halved). Hourly posts. Push at each.
