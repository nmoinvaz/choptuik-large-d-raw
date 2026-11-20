# I1021-mac/z16_m7: box 16's zero at M = 7 on the Mac, at xi1 0.15 under the criteria fixed on #1048

Machine: the Mac, helper session xfchecks, 1 nice-10 slot, one solve at a time. Issue #1021. Written 20 Nov 2026 08:56 UTC,
before the run. Code, venv and backend checks as `../z7_m7/README.md` (hier_nb.py at fc7dee4d, venv-i1021nb). Driver
`../z7_m7/run_m7b.sh z16`; walks `../z7_m7/walk1026b.py`, `../z7_m7/walk1027b.py` (walk1026.py and walk1027.py with the bars
as options); evaluator `../z7_m7/eval_m7b.py --box z16`. Start: box 16's M = 3 zero located at xi1 0.18 (at 0.17 the locate
is under the 10 sigma guard) with its M = 3 harmonics, `../z7_m7/inputs/z16_start.txt` (3.553346604669, 0.413172284516,
B3 0.7598443752, C3 0.0120820005). The M 3 to 5 shift is taken from that 0.18 location. dh610 ran box 16 at 0.25, 0.2 and
0.15 under the earlier criteria; this run is the Mac's, under the fixed ones.

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

## The repeat rule (the coordinator, #1021 comment 7035545338, 09:19 UTC, before box 16's result)

A walk's start solve (the fixed-(A, w) M = 5 or M = 7 solve at the previous M's zero) may use #1027's three perturbed
repeats (as `m5/m5_repeat.py`), and every bar, the gate and the verdict rule stay as above. This run started at 09:17 UTC
with `run_m7b_v1.sh`, before the rule. Its box M = 5 walk runs `walk1026b.py` without repeats: the file was replaced at
09:20:44 UTC by the version with `--start_repeats N`, which at the default 0 is the earlier code (`../z7_m7/walk1026b_v2.diff`).
If the box's start solve fails here, the rule is applied in `rep3/`: a full run (controls and box) with `run_m7b.sh z16 3`,
whose README is written before it starts. walk1027 already repeats every attempt (#1027), so the M = 7 start has its repeats
in both runs.
