# I1021-mac/z7_m7/xi015b: box 7's zero at M = 7, rerun at xi1 0.15 under the criteria fixed on #1048

Machine: the Mac, helper session xfchecks, 1 nice-10 slot, one solve at a time. Issue #1021. Written 20 Nov 2026 08:54 UTC,
before the run. Code, venv and backend checks as `../README.md` (hier_nb.py at fc7dee4d, venv-i1021nb). Driver
`../run_m7b.sh z7`; walks `../walk1026b.py`, `../walk1027b.py` (walk1026.py and walk1027.py with the bars as options,
`../walk1026b.diff`, `../walk1027b.diff`); evaluator `../eval_m7b.py`. Start: box 7's M = 3 zero at xi1 0.17 with its M = 3
harmonics, `../inputs/z7_start.txt` (3.245479323269, 0.345852268456, B3 0.7431269380, C3 0.0158575223).

## The criteria (the coordinator, #1048 comment 7034798454 at 08:48 UTC, amended by comment 7034888111 at 08:53 UTC)

- Radius: xi1 0.15 only.
- Walk residual bar: |r_1| at the walk's best point at most 3x the measured |r_1| noise at the known zero: 3.8e-2 at M = 5,
  0.24 at M = 7 (#1048's table).
- Walk step bar: the Newton step from the best point under 1e-5 in A and in w/w_inf at M = 5, and under walk1027's 3e-4 at
  M = 7 (the amendment: M = 7's step noise there is 1.7e-5).
- Position bar: the controls' zeros within 1e-5 in A and in w/w_inf of their stored zeros: M = 5 (2.718579189, 0.999228404),
  M = 7 (2.71924, 1.000025), with the M = 7 control's |F7/F5| at its first solve within 5% of 0.0574. For a box walk, the
  last two accepted walk points (the best points before and after the last accepted step) within 1e-5 at M = 5 and 3e-4 at
  M = 7, in A and in w/w_inf.
- A walk converges at the first iteration where its residual, step and (box) position bars hold together. The solve bar
  stays |r_nu| < 1e-6 for nu >= 3, with #1027's perturbed repeats at M = 7.
- Gate: the box's result counts only if both controls (#1026's M = 5 walk from the known zero's M = 3 place, #1027's M = 7
  walk from its M = 5 zero) pass these criteria in this run. The driver runs the box walks only after both pass.
- Verdict: #1027's rule, unchanged: CONVERGES if |F7/F5| <= 0.2 at the M = 5 zero and the M = 7 walk converges with an M 5 to 7
  shift smaller than the M 3 to 5 shift; DOES NOT if |F7/F5| >= 0.3 or no M = 7 zero is found near it; UNDECIDED otherwise, or
  with no M = 5 zero.

These bars come from #1048's noise at the known zero, not from any box result. Controls of the code: `eval_m7b.py --selftest`
exits 0, and `--mutate=shift`, `pos7`, `nogate` and `ratio` each exit 1; `walk1026b.py` and `walk1027b.py --selftest` exit 0,
and `--mutate=noposbar` exits 1.

## Result (08:54-09:15 UTC, `exits.txt`, `eval.txt`, `logs/`, `walks/`)

The evaluator's, walks' and backend's checks give their expected exits. Gate: both controls PASS.
- #1026's M = 5 control: stops at iteration 5 (|r_1| 2.4e-2 against 3.8e-2, step (-2.4e-6, +7.2e-7)), zero (2.718581347,
  0.999229783), 2.2e-6 and 1.4e-6 from the stored zero (7 solves, 170 s).
- #1027's M = 7 control: stops at iteration 1 (|r_1| 0.14 against 0.24, step (2.7e-5, 1.1e-5) against 3e-4), zero (2.719239,
  1.000026), 1.4e-6 and 6.1e-7 from the stored zero, |F7/F5| 0.0573 (4 points, each after one repeat).
- Box 7's M = 5 walk fails at its start solve, the fixed-(A, w) M = 5 solve at the M = 3 zero from its M = 3 harmonics:
  |r_5| 4.2e3, |r_3| 4.6e5 (3 s). walk1026 has no repeats of a failed start, so there is no M = 5 zero, and the M = 7 walk
  did not run.

Verdict, counted since both controls pass: **UNDECIDED** (#1027's rule with no M = 5 zero).
