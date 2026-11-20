# I1021-dh610/z16_m7/xi015: box 16's zero at M = 5 and M = 7 at xi1 0.15, with #1026's and #1027's controls as gates

Machine dh610 (Fedora 45, i7-12700). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1021, a #1021 step on the
coordinator's hc message of 20 Nov 2026 (about 06:58 UTC): the z16 run at 0.25 and 0.2 gave no verdict because #1027's M = 7
control, validated only at xi1 0.15, did not converge at 0.25 (|r_3| 42) or 0.2 (|r_3| 2.4e-2) (`../README.md`, comment 7032765302).
So the route is run at 0.15, the M = 5 walk from the M = 3 zero and then M = 7, with both controls at 0.15 as gates, in the same run.
Rule unchanged (#1027's, below). 2 processes at nice 10 (`--procs 2`, one walk at a time), beside #1031 and #1034.

Code and scripts: as `../README.md` (`~/Source/cl-995` fc7dee4d, venv `~/Source/venv-i1026`, `INNER_NB_RTOL=1e-13` for M = 7;
`../walk1026.py`, `../walk1027.py`, `../eval1027.py`, `../eval_z16.py` unchanged; `eval1026.py` here is a copy of I1026-dh610's;
`eval_z16_015.py` and `run_z16_015.sh` are new).

## Route and gates

1. Gate M = 5, #1026's control: `walk1026.py control5` from the known zero's M = 3 zero (2.726475886, 1.015603095) with its M = 3 harmonics
   (0.1444194785, 0.0110874259), xi1 0.15. Pass (eval1026.judge_control): converges to the stored M = 5 zero (2.718579189, 0.999228404) within 1e-5 in A and w.
   #1026 validated it at 0.2 only.
2. Gate M = 7, #1027's control: `walk1027.py control7` from the known zero's M = 5 zero with F_7 = 0, xi1 0.15. Pass (eval1027.judge_control):
   converges within 3e-4 of (2.71924, 1.000025) with |F7/F5| at its first solve within 5% of 0.0574. Validated at 0.15 in #1027 (4 solves, 525 s).
3. Box 16's M = 5 walk: `walk1026.py z16m5` from the M = 3 zero (A, w/w_inf) = (3.553346604669, 0.413172284516) (located at xi1 0.18 by xfchecks, raw
   `I1021-mac/loc/z16_6da7da7b/`) with its M = 3 harmonics (B3, C3) = (-2 Im F3, 2 Re F3) = (0.7598443752, 0.0120820005), F3 = 0.00604100027 - 0.37992218762i
   (the nearest record of that file's `points_M3_r0.18.jsonl`, 6e-10 away, `fix.ok`; F_3 does not depend on xi1 on one sheet), xi1 0.15: the M = 5 zero Z5 and
   s35 = |Z5 - Z3|.
4. Box 16's M = 7 walk from Z5 with the M = 5 solve's harmonics, F_7 = 0 (`walk1027.py z16`), when the M = 5 walk converged; and, as information, from the
   input's point (xfchecks's xi1 0.25 solve: A 3.553346605, w 0.413172285, x = 0.843294116, 0.003092743, 0.24539945, 0.010876743) (`z16in`).

## Reading (fixed before the runs; #1027's)

CONVERGES: |F_7/F_5| <= 0.2 at the first solve (at Z5) and the M = 7 walk converges to a zero with s57 < s35. DOES NOT: |F_7/F_5| >= 0.3, or no M = 7 zero
near it. UNDECIDED otherwise. Gates: the result counts only if both controls pass at 0.15 in this run; if either fails the result is no verdict, with the
control's residual. Every point is solved at xi1 0.15 (the input's own (A, w, x) of `z16in` is from the 0.25 solve).

## Files

| file | what |
|---|---|
| `run_z16_015.sh`, `eval_z16_015.py`, `eval1026.py` | the driver, the evaluator with the gates, #1026's evaluator copy |

## Result, 20 Nov 07:35 UTC (`eval_z16_015.txt`, `logs/eval_gates.log`)

Gate M = 5 (#1026's control) FAILS at 0.15, kept as a fail on the coordinator's word (a pass on position after the result would loosen the criterion; AGENTS.md): 12 solves, best point (2.718572997, 0.999226050), 5.8e-6 in A and 2.4e-6 in w from the
stored zero (inside the 1e-5 position bar), best |r_1| 2.0e-2 (components 1.4e-2 and -1.5e-2), stopped with "no step reduced |r_1| with a converged solve (five halvings)". Cause: the last five points (8 to 12), within 4.2e-6 in A and 1.5e-7 in w of each other, read |r_1| 6.6e-2,
4.1e-2, 5.8e-2, 2.7e-2 and 3.0e-2, so the r_1 noise at 0.15 (about 3e-2 to 6e-2) is above the walk's convergence bar |r_1| < 1e-2: this control cannot pass at 0.15 as built. Gate M = 7 (#1027's control) PASSES: zero (2.719236, 1.000024), difference (-3.82e-6, -6.78e-7) from the stored
(2.719240, 1.000025), |F7/F5| 0.0573 (stored 0.0574), 4 solves, 1438 s (loaded). So no box 16 walk was run: no verdict at M = 5 or M = 7 at 0.15.
