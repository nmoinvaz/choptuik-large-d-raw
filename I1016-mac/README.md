# I1016-mac: hier's truncated model in amp_flint_par.py (--trunc), its checks, and the ln j term it carries

Machine: mac (Apple M5), agent xfkappa. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1016

Code: branch wip/amp-trunc-phys of choptuik-large-d, `solver/inner_amp/amp_flint_par.py` (--trunc, --fit-logs,
--fit-log-lambda), `amp_trunc_checks.py`, `run_trunc_checks.py`, `amp_trunc_zero.py`, `amp_trunc_basis.py`;
venv-314 (python-flint 0.9.0). One process per job at nice 10, two jobs at most.

- `run_trunc_checks.log` and the `P_*`, `F_*`, `T3_*`, `T5_*`, `C3_*`, `C5_*`, `L_*`, `L3_*` runs: the checks' runs
  (planted, exactness, control, J); `amp_trunc_checks.log` their verdicts (the J check fails as fixed)
- `T3all_*`: M 3 with every family; `T3log_*`, `T5log_*`: with `--fit-logs 1`; `F_K13_*`, `T5_K13_*`: M 5 at k 13
  (`run_m5.sh`)
- `pilot_b_*`: the calibration pilot (M 3, wf 1.0156, K 17) with log columns; its fits break down from k 11
- `basis_*`: `amp_trunc_basis.py` for S_1 at k 9 and S_3 at k 7 of M 3
- `amp_trunc_zero_planted*.log`: the zero solver's planted series and its control
