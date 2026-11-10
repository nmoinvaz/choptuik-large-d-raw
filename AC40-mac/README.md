# AC40-mac: the order past EEG's NNLO (Psi_3, Pi_4, Omega_4, f_4) checked in two codes, logs of the final runs and of the coordinator's rerun

Machine mac (Apple M5), subagent of the coordinator. Issue https://github.com/nmoinvaz/agent-comms/issues/40.
Code: `solver/independent_eeg_nnlo/psi3.py` and `controls.py`, and `solver/inner_pert/third_order_eeg.py`, of the main
repository (branch wip/ac40-psi3, rebased onto main). Python: /Users/nathan/venv-314/bin/python (sympy 1.14.0, mpmath
1.3.0). One process, nice -n 10. The write-up is `solver/independent_eeg_nnlo/REPORT.md` of the main repository.

- `final/`: the subagent's final runs. `controls.py --full`, `psi3.py` and `psi3.py --print`, and `second_order_eeg.py`
  ran at the branch's commit 70ac34e (`commit.txt`), and `third_order_eeg.py` and its `--controls` after check I.
  `exits.txt` lists each exit. `controls/` holds the logs of each control row.
- `coordinator_rerun/`: the coordinator's rerun at the branch head before the rebase. `check.py`, `psi3.py`
  (default, `--crosscheck`, `--numeric`), `controls.py --full` (40 of 40) and `third_order_eeg.py` (default and
  `--controls`, 8 of 8), each exit 0. Exits and times are in `exits.txt`.
