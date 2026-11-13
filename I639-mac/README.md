# I639-mac: the sigma-model's Delta(eta) at D = 4 on the multishoot kernel (matter/sigma_ms), M = 32 and 48, double- and quad-double

Machine mac (Apple M5, 10 cores, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/639, run by a
subagent of the coordinator. Code: branch `wip/i639-subagent` of choptuik-large-d, folder `matter/sigma_ms/` (crate
`sigmams` on multishoot 1.2.2 and multidouble 4.2.1, drivers `smdriver.py`, `planted.py`, `run_eta.py`, `fit_min.py`).
Python 3.14 (/Users/nathan/venv-314), the kernel built with `matter/sigma_ms/build.sh` into a site directory of the
subagent's scratch space. Seeds: sigdss's k_c 39 states of `I623-win/`, `I630-win/`, `I631-win/`, `I633-win/`.

## Contents

- `planted/`: the planted-truth check (`planted.py`) and its controls: logs and records.
- `data/`: `sm_records.jsonl` (one record per converged run of `run_eta.py`), `sm_<tag>.npz` (the states, double-double
  and with `--qd` quad-double parts), `sm_<tag>.log` (the run logs).
- `logs/`: the driver logs of the batches.

The summary and the tables are posted on the issue.
