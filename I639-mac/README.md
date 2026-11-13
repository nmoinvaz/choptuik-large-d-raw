# I639-mac: the sigma-model's Delta(eta) at D = 4 on the multishoot kernel (matter/sigma_ms), M = 32, 48 and 64, double- and quad-double

Machine mac (Apple M5, 10 cores, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/639, run by a
subagent of the coordinator. Code: branch `wip/i639-subagent` of choptuik-large-d, folder `matter/sigma_ms/` (crate
`sigmams` on multishoot 1.2.2 and multidouble 4.2.1, drivers `smdriver.py`, `planted.py`, `run_eta.py`, `chain.py`,
`tables.py`, `fit_min.py`). Python 3.14 (/Users/nathan/venv-314), the kernel built with `matter/sigma_ms/build.sh`
(FAST=1: no fat LTO, 16 codegen units) into a site directory of the subagent's scratch space. Seeds: sigdss's k_c 39
state at eta = inf of `I623-win/` (and at eta = 7 of `I631-win/` for the second start).

## Contents

- `planted/`: the planted-truth check (`planted.py`) at M = 8 and its four controls (`--mutate gamma`, `sigma_h`,
  `dropcol`, `qd_state`), and the unmutated check at M = 16: logs and `planted_records.jsonl`.
- `pilot/`: the first runs at eta = inf, M = 32 (exact Jacobian, from sigdss) and M = 48 (mixed Newton, from M = 32).
- `data/`: the production runs, `sm_records.jsonl` (one record per run of `run_eta.py`), `sm_<tag>.npz` (the states,
  double-double), `sm_<tag>.log`. Tags `eta<eta>_M<M>`; `sm_seed_inf_M32.npz` and `sm_seed_inf_M48.npz` are copies of the
  pilot states that started the chains. M = 32: the eps chain inf, 20, 14, 10, 8.5, 7, 6, 5 (exact Jacobian). M = 48:
  inf, 20, 14, 10, 8.5, 7 by the eps chain and 5, 6 resampled from M = 32 (mixed Newton). M = 64: inf and 7, resampled
  from M = 48.
- `checks/`: eta = 7 at M = 32 started from sigdss's k_c 39 state (`eta7_M32_sigseed`), and the quad-double Newton at
  eta = 7, M = 32 (`eta7_M32_qd`; its state has four parts).
- `logs/`: the driver logs of the chains and checks.

## Notes on the files

- The records' `Delta` string holds the hi part only: run_eta.py summed hi and lo with mpmath at its default 53 bits
  (fixed in the branch after these runs). `Delta_hi` and `Delta_lo` are exact, and the derived tables
  (`matter/sigma_ms/data/delta_eta.csv`, `checks.csv`) use hi + lo. The `qd` entry's `Delta` and
  `Delta_qd_minus_dd` in `checks/sm_records.jsonl` have the same defect; `checks.csv` takes the quad-double Delta from
  the four parts of `checks/sm_eta7_M32_qd.npz`.
- The last three lines of `data/sm_eta6_M48.log` (06:40 UTC) are from a duplicate run of eta = 6 at M = 48 by the first
  M = 48 chain, stopped at its start on purpose (the second chain had already run eta = 6); it wrote no record or state.

The summary and the tables are posted on the issue.
