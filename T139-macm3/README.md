# T139-macm3: a second, independent path of win2's T138 chain (harmonics held on the 1/n fit), h_max 0.75 from D 73

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), the T133 build (venv-macm3,
hpkernel NEON, multidouble 4.0.0), main 9349f23e (Python only past ada1fb89, no rebuild). Comms entry: 2026-11-07 04:05
UTC cloud to macm3 (T139).

From T81/conv_pin5_D73.0000_D73.000000.npz, from hp/ with venv-macm3, nice 10 under caffeinate -i, 6 threads:

  anm_run.py <raw> T139-macm3/<run> --state T81/conv_pin5_D73.0000_D73.000000.npz --kfreeze 3
    --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 0.75 --steps <4 | 400> --D_max 1000 --threads 6
    --corrector qd --tol_qd 1e-28 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --save_pred 1

pilot/ (pilot.cmd, pilot.log): 4 steps. Pass: all 4 converge with qd max|F| below 1e-28, the log prints "held values
from the fit data/held_fit.json", and Delta at D 76.0 (four parts summed in mpmath) differs from
T138-win2/chain/anm_pin3_D76.0000.npz's by less than 1e-20.
chain/ (chain.cmd, chain.log): the same with --steps 400 if the pilot passes. Above D 165, when the order-4 series ratio
falls below 30, stop at a step boundary and restart from the last state into chain_o/ with --jet_o 1 (no --jet_q,
--pred_q); two quad-double stalls above 1e-28 in a row: restart with --corrector od --tol_od 1e-40. Hang rule as T134's
(no log line for 30 min below 1.5 cores, or 90 min at any load; kill, restart from the last state at h_max 0.25, at most
2 restarts). Stop after 24 h or on a three-halvings stop.

Pilot (04:07:15 to 04:21:35 UTC, exit 0, 852 s): passed. 4 steps, every one a 0.75, re-seed ok each time, qd 2 steps
each, max|F| 6.9e-31, 1.5e-30, 1.7e-30, 6.9e-32; the held-fit line printed. Delta at D 76.0 (four parts, mpmath)
1.775981646448848179754, minus T138-win2/chain/anm_pin3_D76.0000.npz's: -2.0552e-22 (the coordinator's check command).
chain/ started 04:21:54 UTC, supervised by a script that applies the rules above (the order-4 ratio is read from each
"step k:" line, printed right after the series at the base, and the run is stopped there, before a step is taken on
that series).
