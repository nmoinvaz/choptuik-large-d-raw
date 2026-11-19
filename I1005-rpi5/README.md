# I1005-rpi5: truncated hier-model amplitude expansions, does the sigma_{M+1} shift drift like ln J?

Machine rpi5 (Raspberry Pi 5, Cortex-A76 x 4, 8 GB, aarch64, Python 3.13.7), runner, now under the claude-me2 account (the coordinator's message of 2026-11-19: the old account hit its limit).
Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1005 (#996's follow-up), assigned by message. Code: worktree `~/Source/choptuik-large-d-964` at origin/main 551055bf, `solver/proof/amp_trunc_hiermodel.py`
(and `amp_trunc.py`, `amp_flint.py` it imports), venv `~/Source/venv-choptuik` (python-flint 0.9.0, numpy 2.5.4; the system python3 has no flint, so the issue's `python3` is the venv's python here).

## Written down before the runs

- **Prediction (the issue's, fixed before the run):** |sigma_4^[3] - sigma_4(full)| = 5.15e-5 +- 0.3e-5 at J 6000 (M = 3 truncated model, K 9, wf 1.0, 60 digits).
  The law holds if run 1 lands inside 4.85e-5 to 5.45e-5 and fails outside it. Either is a result. (From the coordinator's 3.743e-5, 4.145e-5, 4.375e-5, 4.538e-5, 4.765e-5 at J 500, 1000, 1500, 2000, 3000: +3.9 to 4.0e-6 per doubling of J.)
- sigma_4(full) is `solver/inner_amp/scan45J1500/sigF_w1.0000_K45_J1500_p1280.json` (K 45, J 1500, 1280 bits, `sigma_str[3]`).
- Run 1: `amp_trunc_hiermodel.py 3 9 6000 1.0`. Run 2: `amp_trunc_hiermodel.py 5 13 2000 1.0` (M = 5 model's own first truncated order, sigma_6, at a second J; dh170 has J 1000 in #996). Both from `solver/proof/`, nice 10, side by side;
  each writes `trunc_hier_M<M>_K<K>_J<J>_w1.0000.json`, copied here. 3 to 4 h at most expected.
- A pilot first (the script on a small J, and the coordinator's M = 3 value at J 500, 3.743e-5, as the check that this machine and the venv reproduce it).
- Report: sigma_4 of run 1 and its |sigma_4^[3] - sigma_4(full)|; sigma_6 of run 2 (against dh170's J 1000 value when it lands); each run's fit residual at its last order; time and memory.

## Stopped at the coordinator's request, 2026-11-19 10:27 UTC (no result for the prediction)

The coordinator closed #1005 as superseded (xfkappa's #1016 found and fitted the exact ln j term behind the drift) and told me to stop both runs and push the logs.
I sent SIGTERM to the two python pids (808328, 808329); `run_cap.py` (808324, 808326) wrote the exit files (`exit -15 after 14531 s`, ended 10:27:08 UTC) and ended.
Both runs started 06:24 UTC (22:24 PST, the Pi's local clock, which the log files' mtimes use) at nice 10, side by side.
Neither run reached its target order, so the 5.15e-5 +- 0.3e-5 prediction at J 6000 is neither confirmed nor refuted here, and no JSON was written (the script writes it at the end).

| run | last order printed | wall time to it | fit residual there |
|---|---|---|---|
| 1: M 3, K 9, J 6000 | sigma_1 (k 3) | 9144 s | 4.4e-51 |
| 2: M 5, K 13, J 2000 | sigma_5 (k 11) | 12886 s | 5.5e-58 |

Run 2's sigma_1 to sigma_5 are the orders the M = 5 model keeps exact. Against `sigF_w1.0000_K45_J1500_p1280.json` (15 printed digits) they differ by 1.7e-13, 1.9e-13, 1.3e-13, 4.9e-14, 1.0e-14 (sigma_1 to sigma_5), the 2e-13 level of #996.
Run 1's sigma_1 differs by 9e-16. Run 1's cost: sigma_1 alone took 9018 s of its own (k 1 to k 3) at J 6000, against 559 s for run 2 at J 2000. Scaling by run 2's k 3 to k 9 factor (14x) would put sigma_4 near 37 h, an extrapolation, far above the issue's 2 to 4 h estimate.
Run 2's fit residuals grow 9e-62, 2.7e-60, 6.9e-60, 2.0e-59, 9.2e-59, 5.5e-58 with order (60 digits).
Memory at the stop (RSS): 540 MB (run 1), 585 MB (run 2).

Files: `logs/amp_trunc_M3_K9_J6000.log` and `.exit`, `logs/amp_trunc_M5_K13_J2000.log` and `.exit`, the pilot (`logs/pilot_M3_K9_J500.*`, `logs/trunc_hier_M3_K9_J500_w1.0000.json`: J 500, M 3, K 9, |sigma_4 - sigma_4(full)| = 3.74253e-5, matching the issue's 3.743e-5; 239 s of calculation, 124 MB), `diff1005.py`, `run_cap.py`.
