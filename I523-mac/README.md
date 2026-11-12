# I523-mac: bit-identity checks of hp's kernel rebuilt on multishoot (port, exact kfreeze projector, deletions)

Machine: the M5 Mac (a subagent of the coordinator). Task: https://github.com/nmoinvaz/choptuik-large-d/issues/523

Branch `feat/i523-hp-on-multishoot` of choptuik-large-d. Each folder holds the logs (`<check>.log`, ending in
`exit N`) and JSON of the checks for one build:

- `base/`: main's build (hp/src at d83044f): the dump of every double-double entry point (`api_base.json`, made by
  the scratch script `api_bits.py`, 176 hashes at a low-D state and a kfreeze-3 state) and the Rust test log. The
  other baselines are the coordinator's (`xsolve_bits` `bits_base.json`, `highm_check` `ref_base.json`,
  `jets_base.json`, `scaled_base.json`).
- `c1_ms110/`: commit 1 on multishoot 1.1.0: xsolve_bits (18 of 21, the phase row of the quad jets), the dump (176
  of 176), and the rows of the quad jet that differed (`jq_*.npz`, `jetq_rows.py`).
- `c1/`: commit 1 on multishoot 1.2.1: every check of the issue; `jq232_*.npz` are the rows of the accepted Delta-read
  difference at D 232.63.
- `c2/`: commit 2 (kfreeze on multishoot's projected rows): the kfreeze-off checks, `kf_*.npz` and `kfrows.log` (where
  the residual changes), freeze_round.py on both kernels, the Delta polishes (`plain_step/`, a full undamped step).
- `c3/`: commit 3 (hp's copies of the engine deleted): every check, the comparisons with commit 2 (`*_vs_c2.log`) and
  modecount_check.

The scripts the checks ran beside the repository's own are copied here: `api_bits.py` (the dump of every
double-double entry point), `kf_rows.py` (where commit 2 changes the residual), `delta_polish2.py` (Delta after the
chain's octo-double polish), `freeze_round.py` (from the branch wip/i499-coordinator), `run_checks.sh` and
`run_c2_kf.sh` (the sequences).
