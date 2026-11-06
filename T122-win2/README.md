# T122-win2: the large-D chain to 200 from T118's D 152.93 on the fixed re-seed and projection

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2; 95.6 GB RAM). Worktree `..\choptuik-t115` at origin/main 23d9448 (includes effab02, merged 9f77e49; only hp Python/data changed from b25c271 -- anm_run.py and reseed.py -- so venv-t115's multidouble 3.2.0 kernel stands, no rebuild). From `hp\`, venv-t115, below normal, 12 threads.
Comms entry: 2026-11-06 03:48 UTC cloud to win2.

T122 replaces T121. The D ~152.93 stall had two causes, both fixed (QUAD_DOUBLE.md 13.26): the re-seed u0 polish quit after 6 steps / at the first non-halving step (now allows 16 and refactors), and the elimination corrector's last iterate was stored unprojected (3e-10 off the root, degenerating the next series; now projected). On the Mac the fix steps 152.93 -> 153.43 -> 153.93 at a 0.5 with healthy series.

The chain from T118-win2/chain/anm_pin3_D152.9309.npz toward D 200:
  anm_run.py <raw> T122-win2\chain --state T118-win2/chain/anm_pin3_D152.9309.npz --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.5 --steps 300 --D_max 200 --threads 12 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1
Stops: base polish not converging at once (first qd |F| >= 1e-25); a degenerate series (a step's a_max below 1.0 or |z_N| above 1e-15); the script's own (three halvings).
