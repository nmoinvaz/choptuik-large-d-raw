# T127-win2: the quad-double chain past D 162.31 with the a_h/m_h re-seed fix

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2; 95.6 GB RAM). Worktree `..\choptuik-t115` at origin/main 9eab461. venv-t115's installed kernel is multidouble 3.2.0 (the T115 build at aeea2d1); T127 uses --corrector qd / --jet_q 1 (quad-double), so no rebuild. NOTE: the pull 23d9448 -> 9eab461 also brought hp/src (osolve.rs etc., the octo-double Rust) besides the Python re-seed fix; that Rust is dormant for --jet_q and not rebuilt into venv-t115. From `hp\`, below normal, 12 threads, beside T126's build (4 cargo jobs).
Comms entry: 2026-11-06 05:50 UTC cloud to win2.

T122 stopped at D 162.306 because the re-seed's u0 polish no longer converged from the double-double rung; main now gives it an a_h and m_h least-squares step before Newton (QUAD_DOUBLE.md 13.27). On the Mac the fix steps 162.31 -> 162.81 at a 0.5 (re-seed ok, corrector 1.5e-39 in 6 steps).

The chain from T122-win2/chain/anm_pin3_D162.3059.npz toward D 200:
  anm_run.py <raw> T127-win2\chain --state T122-win2/chain/anm_pin3_D162.3059.npz --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.5 --steps 300 --D_max 200 --threads 12 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --save_pred 1
Stops: base polish not converging at once (first qd |F| >= 1e-25); a degenerate series (a_max < 1.0 or |z_N| > 1e-15, post at once); three halvings. --save_pred keeps each prediction (pred_pin3_D*.npz).
