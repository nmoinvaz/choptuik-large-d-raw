# I780-mac: complex_imag.py's det M against complex_imag_dd.py's at the points of the double counts, D = 10 and 20.04

Machine: mac (Apple M5, the coordinator's Mac), agent xfchecks, one process at nice 10. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/780

Code: branch wip/i780 of choptuik-large-d (venv-314), run from `solver/matter/`: `complex_imag.py` (with
`--mutate=lightcone`), `complex_imag_dd.py` (unchanged), `i780_compare.py`, `i780_summary.py`. The double counts are
I95-mac's: `imag/evals_D20.jsonl`, `imag/evals_D10.jsonl` (their evaluation logs) and `imag/counts.jsonl`.
States: hp/data/states/up2_D20.0437.npz (M 32, 8 nodes 0.1-0.7) and up_D10.0000.npz (M 48, 10 nodes 0.02-0.7).

`--dd=0` keeps every propagator in complex_imag.py's double code (rtol 1e-11, as the counts), so only the light-cone
block (complex_imag_dd's horizon_dd, double-double) and the LU (double-double, banded) differ from complex_imag.py.
`--dd=all` puts the node segments in double-double too (Taylor, tol 1e-14).

## Files

- `pilot_*.jsonl`: two real-axis points per state in both modes (cost: 7 s and 45 s per determinant at D 20.04,
  22 s and 200 s at D 10).
- `control_lightcone.jsonl`, `control_lightcone_D20.log`, `evals_control_D20.jsonl`: `complex_imag.py count
  up2_D20.0437.npz B0 --mutate=lightcone` (P_1 of the light-cone series x 1.1): winding 0 against 1, the control fires.
- `run.sh`, `run.log`: the chain (18:44-19:57 UTC).
- `dd0_D20.jsonl`, `.log`; `dd0_D10.jsonl`, `.log`: complex_imag_dd at every unmutated point of the double counts
  (168 and 150), in complex_imag's "eval" format with the double value and the differences.
- `counts_dd0.jsonl`, `count_dd0_D*.log`: `complex_imag_dd.py count ... B0 U0 FULL --dd=0 --rtol=1e-11
  --evlog=dd0_D*.jsonl`: the windings over the same values (no new evaluation was needed).
- `ddall_D20.jsonl`, `ddall_D10.jsonl` and logs: full double-double at every 30th complex point (6 and 5).
- `diag_swap.py`, `diag_swap_D20.log`: at D 20.04's largest differences, the light-cone block and the LU swapped one
  at a time between double and double-double.
- `summary.log`: `python3 i780_summary.py <raw>/I780-mac <raw>/I95-mac/imag/counts.jsonl` (exit 0, PASS).
  `summary_control.log`: the same on a copy with one D 10 phase difference set to 2e-3 (exit 1, FAIL).

## Results

| | D = 20.04 | D = 10 | bound |
|---|---|---|---|
| points of the double counts | 168 | 150 | |
| largest phase difference, light-cone block in double-double | 3.4e-4 rad (B0's left edge, -0.05 + 1.98i) | 3.9e-6 rad | 1e-3 rad |
| windings B0 / U0 / FULL, double | 1 / 0 / 0 | 1 / 0 / 0 | |
| the same over the double-double values | 1 / 0 / 0 (same points) | 1 / 0 / 0 (same points) | equal |
| full double-double against `--dd=0`, sampled points | <= 5.7e-9 rad | <= 6.9e-10 rad | |
| full double-double against double, sampled points | <= 2.2e-5 rad | <= 3.0e-6 rad | |

At D 20.04's three largest differences, the whole difference is the light-cone block's (diag_swap_D20.log): its
entries differ by up to 1.3e-7 relative (4.9e-10 of the largest entry), which moves the phase by 3.44e-4 rad at
-0.05 + 1.98i, near the zero lambda = 0 where |det M| is small; the LU contributes 4e-8 rad.
