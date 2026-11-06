# T134-macm3: a second path for the chain past D 193.77 with the quad-double stall rule, octo-double series

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), the T133 build (venv-macm3,
hpkernel NEON, multidouble 4.0.0), main ada1fb89 (Python only past the build, no rebuild). Comms entry: 2026-11-06 16:16
UTC cloud to macm3 (T134), the second run of win2's T129 chain4 rows.

From T129-win2/chain2/anm_pin3_D193.7746.npz, nice 10 under caffeinate -i, 4 threads (chain.cmd has the exact line):

  anm_run.py <raw> T134-macm3/chain --state T129-win2/chain2/anm_pin3_D193.7746.npz --kfreeze 3 --N 24 --eps 1e-14
    --h_max 0.5 --steps 300 --D_max 1000 --threads 4 --corrector qd --tol_qd 1e-28 --accept_stall_qd 1e-24 --qd_it 12
    --trend T75 --jet_o 1 --reseed 2 --reseed_q 1 --save_pred 1

Log chain.log, states and anm_run.jsonl in chain/. Stop on its own three-halvings stop, on a degenerate series (a_max
below 1.0 or |z_N| above 1e-15), or after 16 h. Hang rule: no log line for 30 min while the run uses less than 1.5 cores,
or for 90 min at any load (the coordinator's 30 min alone would fire inside every step: a 24-order octo-double series at
4 threads here takes about 31 min without a line, T133's t_series_o 1884 s); then kill, restart from the last state with
h_max 0.25 (chain_r1/, chain_r1.log, then chain_r2), at most 2 restarts, a native stack sample in <run>_hang_sample.txt.
