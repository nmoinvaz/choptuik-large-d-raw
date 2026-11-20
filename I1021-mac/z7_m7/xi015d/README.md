# I1021-mac/z7_m7/xi015d: boxes 7 and 16 and b11-15's +1 at M = 7, xi1 0.15, M = 5 walks started from xi1 0.2 iterates

Machine: the Mac, helper session xfchecks, 2 nice-10 slots, one solve at a time per slot. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/1021. Written 20 Nov 2026 12:32 UTC, before any of the runs. Code,
venv and backend as `../README.md` (hier_nb.py at fc7dee4d, venv-i1021nb). Walks `../walk1026b.py` (now with `--x5 B5,C5`,
`../walk1026b_v3.diff`; the version of xi015b, xi015c and z16_m7 is `../walk1026b_v2.py`) and `../walk1027b.py`; evaluator
`../eval_m7b.py` (box b1115p added, `../eval_m7b_v2.diff`). Drivers:

- Slot 1: `../run_xi015d.sh`, which runs `../run_m7d.sh z7` and then `../run_m7d.sh z16`. Output `z7/`, `z16/`.
- Slot 2: `../run_b1115p.sh`, which runs b11-15's xi1 0.2 M = 5 solve and then `../run_m7d.sh b1115p`. Output `../../m5/b1115p_*`,
  `b1115p_m5_exits.txt`, `b1115p/`.

`run_m7d.sh` is `../run_m7b.sh` with the start below. Each box's run has its own controls.

## The start rule (the coordinator, #1021 comment 7039516484, 12:26 UTC)

"The M = 5 start may now also begin from the box's own best xi1 0.2 M = 5 iterate, its (B3, C3, B5, C5) ... This adds a start,
not a criterion. Every bar, the controls' gate and #1027's verdict rule stay as fixed on #1048. For b11-15's +1, run the M = 5
solve at 0.2 first to get such an iterate, then 0.15."

The box's M = 5 walk at xi1 0.15 starts at its M = 3 zero, as before. Its first fixed-(A, w) solve starts from that iterate:
the end state (F_3/F_1, F_5/F_1 times A, 6 printed decimals) of the attempt that `../../m5/m5_repeat.py` counted at xi1 0.2
(`../start02.py`, which exits 1 when the log is not at xi1 0.2 and at the box's (A, w); its control, another box's start, must
exit 1). The repeat rule below still applies to that first solve.

| box | M = 3 zero (A, w/w_inf) | xi1 0.2 attempt counted | its \|r_3\|, \|r_5\| | B3, C3, B5, C5 |
|---|---|---|---|---|
| 7 | 3.245479323269, 0.345852268456 | `m5/z7_6da7da7b_xi0.2_r2.log` | 2.8e-06, 2.0e-07 | 0.8250332987, 0.0100382675, 0.2624034942, 0.0157730295 |
| 16 | 3.553346604669, 0.413172284516 | `m5/z16_6da7da7b_xi0.2_r1.log` | 1.2e-04, 1.2e-06 | 0.8434010301, 0.0030061312, 0.2454332034, 0.0108554739 |
| b11-15 +1 | 3.526470822728, 0.211495027973 | made by `run_b1115p.sh` | | |

b11-15's +1 zero is the one located at xi1 0.18 (`../../loc/b1115p_r0.18_6da7da7b`, `../../m5/b1115p_start.txt`, M = 3
harmonics B3 0.9765102845, C3 -0.0017643829). Its xi1 0.2 solve is as boxes 7 and 16 had it: `hier.py 5 A w --x=B3,C3
--fixA --schur --procs 1 --verbose=1 --xi1=0.2` at 6da7da7b (numpy backend, venv-314), then up to three of #1027's repeats
(`m5_repeat.py`; the first attempt under |r_3|, |r_5| < 1e-6 counts, else the one of smallest |r_3|). The 0.15 route then
runs from the counted attempt whatever its |r_3|, as the coordinator asks.

## The criteria (the coordinator, #1048 comment 7034798454 at 08:48 UTC, amended by comment 7034888111 at 08:53 UTC)

- Radius: xi1 0.15 only.
- Walk residual bar: |r_1| at the walk's best point at most 3x the measured |r_1| noise at the known zero: 3.8e-2 at M = 5,
  0.24 at M = 7 (#1048's table).
- Walk step bar: the Newton step from the best point under 1e-5 in A and in w/w_inf at M = 5, and under walk1027's 3e-4 at
  M = 7.
- Position bar: the controls' zeros within 1e-5 in A and in w/w_inf of their stored zeros: M = 5 (2.718579189, 0.999228404),
  M = 7 (2.71924, 1.000025), with the M = 7 control's |F7/F5| at its first solve within 5% of 0.0574. For a box walk, the
  last two accepted walk points within 1e-5 at M = 5 and 3e-4 at M = 7, in A and in w/w_inf.
- A walk converges at the first iteration where its residual, step and (box) position bars hold together. The solve bar
  stays |r_nu| < 1e-6 for nu >= 3, with #1027's perturbed repeats at M = 7.
- Gate: the box's result counts only if both controls (#1026's M = 5 walk from the known zero's M = 3 place, #1027's M = 7
  walk from its M = 5 zero) pass these criteria in the same run. The driver runs the box walks only after both pass.
- Verdict: #1027's rule, unchanged: CONVERGES if |F7/F5| <= 0.2 at the M = 5 zero and the M = 7 walk converges with an M 5 to 7
  shift smaller than the M 3 to 5 shift; DOES NOT if |F7/F5| >= 0.3 or no M = 7 zero is found near it; UNDECIDED otherwise, or
  with no M = 5 zero.

## The repeat rule (the coordinator, #1021 comment 7035545338, 09:19 UTC)

A walk's start solve may use #1027's three perturbed repeats: up to three from the best attempt's end state, every harmonic
times (1 + 1e-7 u), u uniform in (-1, 1) from random.Random(1027), one generator per walk; the first attempt under the bar
counts, else the one of smallest |r_3|. `walk1026b.py --start_repeats 3` in both M = 5 walks; walk1027 repeats every attempt.

## Checks of each run (`BOX/exits.txt`, expected exit in brackets)

`start02.py` (0) and with another box's start (1); `eval_m7b.py --selftest` (0), `--mutate=shift`, `pos7`, `nogate`,
`ratio` (1 each), on the stored control (0) and `--mutate=shift` (1); `walk1026b.py` and `walk1027b.py --selftest` (0),
`--mutate=noposbar` (1), `walk1026b.py --mutate=norepeat` (1); the start-harmonics check on xi015c's first solve, which has
two harmonics (1), and on the box walk's first solve (0); `inner_nb.py` capcheck (0), capcheck at MAXFEV 100 (1), check 1 3
5 7 (0), check 3 5 `--mutate=sign` (1); `hier_nb.py selftest` (0), `--mutate=radius` (1).

## Result, box 7 (12:33-12:43 UTC, `z7/exits.txt`, `z7/eval.txt`, `z7/logs/`, `z7/walks/`)

The 22 checks, both gate walks and the evaluator give their expected exits. The box's M = 5 walk exits 1. Gate: both
controls PASS (M = 5: +2.16e-6 and +1.38e-6 from the stored zero, 51 s; M = 7: -1.43e-6 and +6.06e-7, |F7/F5| 0.0573,
556 s). The start-harmonics check confirms the box walk's first solve began from the four harmonics of the 0.2 iterate.

Box 7's M = 5 start solve at xi1 0.15 does not converge: |r_3| 4.6e2, |r_5| 8.4e-2 at the first attempt (2 s), then 5.0e2,
4.9e2 and 4.6e2 at the three repeats (|r_5| 7.9e-3, 0.10, 9.7e-2). The walk keeps the first attempt. There is no M = 5 zero,
and the M = 7 walk did not run. Verdict, counted since both controls pass: **UNDECIDED** (#1027's rule with no M = 5 zero).

Diagnostic (`z7/diag/`, nice 19, the same hier_nb.py solve at verbose=2): from the same start, hier_nb.py at xi1 0.2 reaches
|r_3| 2.3e-5, |r_5| 2.0e-7 in 3 s, close to hier.py's 2.8e-6. At xi1 0.15 the level-5 solves stop at hier's noise floor,
|g| 3.2e-2 to 5.2e-2 (three stops), against 6.8e-8 to 4.4e-7 (seven stops) at 0.2. The largest entries of hier's Jacobian K
grow from 0.2 to 0.15 by 5.4e5 (d r_3 / d x_3: 1.95e9 to 1.05e15) and 6.2e5 (d r_5 / d x_5: 1.80e7 to 1.12e13). So at box
7's (A, w) at 0.15 the double-precision floor of level 5 is 3e4 to 5e4 times the 1e-6 solve bar, and no start can meet
the bar there in this code.
