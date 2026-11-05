# T114-mac: T113's chain from D 128.56 to 140 on the Mac, a pilot through the suspected wall at 131-134

Machine: the Mac (Apple M5), run by the coordinator session. Comms: 2026-11-05 cloud status at 17:55 UTC.

Command (from hp/ of the main checkout at 026f817, venv-qds), T113's options with --D_max 140:

    anm_run.py RAW RAW/T114-mac/chain --state anm-mac/pred_q/A2/anm_pin3_D128.5559.npz --kfreeze 3 --N 24 --eps 1e-14
        --h_max 1 --steps 40 --D_max 140 --threads 4 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1
        --pred_q 1

- `chain/`: the converged states and anm_run.jsonl; `chain.log`: the run's log.
