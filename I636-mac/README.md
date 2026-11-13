# I636-mac: chain states resampled from M = 32 to M = 48 and solved again, Delta and lam_g against M (hp/chain_dM.py)

Machine: mac (Apple M5, 10 cores, 32 GB, macOS 27), shared with other sessions. Subagent of the coordinator.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/636
Code: branch `wip/i636-subagent` of the code repository, `hp/chain_dM.py` (notes/QUAD_DOUBLE.md 13.31). hpkernel:
main's build at 3c35f0c (the exact freeze projector; quad-double for M = 32 and 48, octo-double for M = 32 only).
Python 3.14 (venv-314), nice 10. States read from the raw-data repository at 3046bc7d.
Threads: 5 for every run up to 07:39 UTC (the plants, D 100, D 150, the refusal control, the first two D 200 runs),
2 from then on (the coordinator's cap: D 200, D 240.12, the `--mutate=D` control); 1 for the grading, refit and ramp.

## Files

- `run_i636.sh`, `run_i636_large.sh`, `run_i636_d240.sh`: the run scripts; `exits.txt`: every command's start, exit
  status, and each stop with its reason.
- `planted/`: the plants. `planted_dd.log` (dd20 passes; dd40 stopped for time), `planted_chain80.log` (the D 80 plant
  with the polish), `stop_at_tol/` (its first run, which failed), `resolution_check_D80_thisbuild.log` (the plant's
  value on this build), `planted_graded.log` (both plants graded from their records, exit 0), `chain_dM.jsonl`,
  `m48_*.npz` (the M = 48 solutions, four parts).
- `chain/`: D 100, 150, 200 and 240.12 (`d*.log`, `chain_dM.jsonl`, `m48_*.npz`); the stopped runs' logs
  (`d200_it16_stopped.log`, `d200_it6_t5_stopped.log`, `d200_it4_t2_stopped.log`, `d240_it4_stopped.log`).
- `controls/`: `unconverged_d100.log` (the refusal control, exit 1), `planted_dd20_D.log` (the plant under
  `--mutate=D`, exit 1), `chain_dM.jsonl`.
- `refit/`: `refit.log` and the `lam_gauge_fit.py` logs and tables (`chain_dM.py refit`), `ramp.log`,
  `c0_response.log` (the first ramp, from `scripts/c0_response.py`).
- `scripts/`: `spec32.py` (the M = 32 spectra), `plan_cmp.py` (the D 80 plan against resolution_check's),
  `c0_response.py`.
- `debug/dd40.log`: the first D 40 plant with the re-seed (one M = 32 re-seed took 431 s), stopped.
