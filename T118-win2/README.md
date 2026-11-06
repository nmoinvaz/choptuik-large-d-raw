# T118-win2: the large-D chain with the elimination corrector from 152.31

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2; 95.6 GB RAM). Worktree `..\choptuik-t115` at origin/main b25c271 (multidouble 3.2.0 kernel with QDLu, venv-t115). From `hp\`, below normal priority, 12 threads, beside T115's step-4 trace. The plain qd corrector stalled at D ~150 (T116); the elimination corrector (--reseed 2 --reseed_q 1, trial points re-seeded through the ladder each step) does not (T117 went 149.56 -> 152.31).
Comms entry: 2026-11-06 02:18 UTC cloud to win2.

The chain from T117-win/chain/anm_pin3_D152.3059.npz toward D 200:
  anm_run.py <raw> T118-win2\chain --state T117-win/chain/anm_pin3_D152.3059.npz --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.5 --steps 300 --D_max 200 --threads 12 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1
The base polish must converge at once (first qd |F| below 1e-25), else stop and post.
