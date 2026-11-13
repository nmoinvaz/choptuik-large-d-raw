# I636-mac: chain states resampled from M = 32 to M = 48 and solved again, Delta and lam_g against M (hp/chain_dM.py)

Machine: mac (Apple M5, 10 cores, 32 GB, macOS 27), shared with other sessions. Subagent of the coordinator.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/636
Code: branch `wip/i636-subagent` of the code repository, `hp/chain_dM.py`. hpkernel: main's build at 3c35f0c (the exact
projector; quad-double for M = 32 and 48, octo-double for M = 32 only). Python 3.14 (venv-314), nice 10.
States read from the raw-data repository at 3046bc7d.

## Files

- `planted/`: the planted checks (`chain_dM.py planted`), their controls and their logs.
- `chain/`: the chain states at D 100, 150, 200 and 240.12 (`chain_dM.py run`), the control `--mutate=unconverged`.
- `chain_dM.jsonl` in each folder: one record per state; `m48_*.npz`: the M = 48 solutions (four parts, save_q).
- `exits.txt`: every run's command and exit status.
