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

chain/ stopped at D 195.5246 for T134b (18:55:45 UTC, at the step boundary right after that state was saved): 4 steps
from 193.7746 (194.2746, 194.7746, 195.0246, 195.5246), 1 halving (the a 0.5 step to 195.2746 failed, 0.25 converged),
4 quad-double stalls accepted, max|F| 1.3e-28, 3.9e-28, 2.3e-28, 2.5e-28. Delta against T129-win2/chain4 at the shared
points: 194.2746 -2.0e-18, 195.0246 +2.8e-18, 195.5246 +1.1e-17 (four-part states summed in mpmath).

T134b (comms 2026-11-06 18:44 UTC cloud to macm3): the octo-double corrector (main c496ac8, Python only, no rebuild)
from chain/anm_pin3_D195.5246.npz, the same command with --corrector od --tol_od 1e-40 in place of --corrector qd
--tol_qd 1e-28 --accept_stall_qd 1e-24 (chain_od.cmd), log chain_od.log, states in chain_od/. Same hang rule, 90 min
at any load the outer limit, at most 2 restarts (chain_od_r1, chain_od_r2, h_max 0.25). Stop on three halvings, a
degenerate series, or after 16 h.

chain_od/ stopped for T139 (comms 2026-11-07 04:05 UTC cloud to macm3) at 04:06:29 UTC, killed about a minute into
step 12's series, which is lost. Last state chain_od/anm_pin3_D201.5246.npz (saved 04:05 UTC), Delta
1.69470316737833128 (eight parts summed in mpmath). 12 steps from 195.5246, every one a 0.5: 0 halvings, 0 stalls,
0 restarts; final octo-double max|F| 3.4e-54 to 1.3e-50.
