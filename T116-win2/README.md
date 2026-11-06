# T116-win2: the large-D chain resumed from T113's state on the multidouble 3.2.0 build

Machine: win2 (Windows desktop, Intel Core Ultra 7 265K, 20 cores: 8 P + 12 E, no SMT, AVX2; 95.6 GB RAM; on AC). Worktree `..\choptuik-t115` at origin/main b25c271 (perf/md32 merged da41438 + Python-only changes; the only change from aeea2d1 is hp/anm_run.py, the fece0ba restart-polish fix, so venv-t115's multidouble 3.2.0 kernel is main's kernel, no rebuild). From `hp\` of choptuik-t115, venv-t115, below normal priority, 12 threads. Runs beside T115's step-4 trace (1 core).
Comms entry: 2026-11-06 00:32 UTC cloud to win2.

The large-D chain from T113-win/chain's highest state (anm_pin3_D146.5559.npz) toward D 200:
  anm_run.py <raw> T116-win2\chain --state T113-win/chain/anm_pin3_D146.5559.npz --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.5 --steps 300 --D_max 200 --threads 12 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1 --pred_q 1
The base polish (fece0ba, from all four stored parts) must converge at once: a "qn 0: |F| ~1e-30 converged" line. Stop if the first qd |F| is above 1e-25.
