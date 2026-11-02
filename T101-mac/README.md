# T101-mac: one jump from D 77.88 to D 100 in layout A (pin 7, double-double), the author's instruction of 2026-11-02

Machine: mac (coordinator), 2026-11-02 22:45 UTC. scan_hp.py at wip/qd-horizon dd0186e (~/Source/choptuik-mac-qd2,
~/venv-qd), T85's settings (folder T85-mac: pin 7, --qdh 1, kfreeze 13, layout A, nodes 0.3..0.8, kc 232 as the
frontier state's record, ks 130, tol 1e-19 growing 1.45 per unit of D as T84's jumps), from T85's layout-A frontier
state pin7_x80_D77.8806.npz with T85's waypoints 74, 75, 76 and 77 as the predictor's history (lagrange_dd through the
last four points), one step of 22.1194 to D = 100 (--max_fail_row 1: a single attempt). Nathan's instruction (comms
context, 2026-11-02 about 22:40 UTC): "just jump to 100", in place of the pin ladder and the steps of 1 that T85 took.
No caffeinate: the run is in the foreground of a coordinator command.

Written before the run. Expectation: T84's jumps of 0.5 to 5 from 73.27 converged in the 0.85 layout with waypoints
0.87 apart, because the predictor's error stayed below the horizon block's tolerance (about 1e-7 there, less in the
0.8 layout, notes/QUAD_DOUBLE.md 12.3); a jump of 22 extrapolates the cubic 22 spacings out, so the expectation is that
Newton does not converge from the predictor (the Levenberg-Marquardt polish may lower |F| without reaching tol, as at
T85's end). Reported either way: the re-converged start's Delta, the attempt's |F| trajectory and end, and if it
converges, Delta_full1 at D 100 and dDelta_pin, with the rational formula's value as a plausibility check only (T85's
points agreed with it to 1e-7). A converged point at 100 is a double-double point in the pinned system of layout A and
carries that layout's uncertainty (about 1e-6, T85); it is not a certified value. A second run with the scan's own
halving toward 100 follows if the single jump fails, and is recorded here with its date.

Files: jump100.jsonl, jump100_attempts.jsonl, jump100.log, run.sh (the command), the states pin7_jump100_x80_D*.npz.

## Amendment (2026-11-02 22:52 UTC): the single jump, and two halving ladders

The single jump did not reach a Newton iteration: at the predicted state for D 100 the kernel's horizon residual was
not finite (`jump100.log`: "singular or non-finite pivot at column 0 (NaN)", after an overflow in the residual norm),
and scan_hp.py raised out of its loop instead of halving the step. Patched in the Mac checkout (branch wip/t101-mac,
0129a65: a solve that raises on the predicted state is a failed step) and run again as two ladders, the scan's own
halving (factor 0.5) from the full jump down to 0.25, the step doubling after a success up to the full jump, 0.13 h
each, 4 threads, both at once:
- `ladder_x85`: the 0.85 layout from T75's pin 7 frontier 73.2657 with T75's waypoints 70.65, 71.5, 72.4 as history
  (T84's jump setting, in which a single jump of 5 converged at 78.2657), first step 26.7343 (to 100).
- `ladder_x80`: the 0.8 layout from T85's frontier 77.8806 with T85's waypoints 74..77 as history, first step 22.1194.
Expected: the first attempts fail as above; the x85 ladder lands at a step of a few units (T84: 5 lands, 26.7 is
untested); the x80 ladder, whose start sits where T85's steps of 0.005 failed, is expected to fail down to 0.25.
Reported: every attempt (`*_attempts.jsonl`), the landed points' D, |F|, Delta_full1 and dDelta_pin, and the end.

## Outcome (2026-11-02 22:54 UTC)

No jump to 100 lands, and no step of any size crosses D 79.3 from either start (`ladder_x85_attempts.jsonl`,
`ladder_x80_attempts.jsonl`, the logs). The x85 ladder from 73.2657: the jumps of 26.7, 13.4 and 6.7 fail at the
predictor's residual (|F| 7.7e48, 1.7e21 and 1.7e3, the horizon block off its domain), 3.34 lands at 76.6075 (|F|
1.1e-27, 41 iterations, dDelta_pin -9.5e-05), 2.67 fails (Newton stalls at 7.6e-06), 1.34 lands at 77.9442 (3.1e-21,
dDelta_pin +3.3e-05), 1.34 fails again (6.6e-06), 0.67 lands at 78.6126 (7.5e-27, but dDelta_pin -2.0e-03: the point
is off the branch along the undetermined directions, as T85's x85 run was at 76.4), then 0.53 gives a NaN pivot and
0.27 |F| 6.6e131: the halving ends below 0.25 after three landed points. The x80 ladder from 77.8806: 22.1 (NaN pivot),
11.1, 5.5 and 2.8 fail at the predictor's residual (|F| 1.4e133, 3.6e29, 7.9e7), and 1.38, 0.69 and 0.35 bring Newton
to |F| 2.9e-06, 5.2e-07 and 1.4e-07 and no further, as T85's steps of 0.4 to 0.005 did; nothing lands. So the wall
near D 78-79 that T85 met with steps of 1 is met by jumps of every size from two starts: it is the pinned
double-double system's Newton basin (notes/QUAD_DOUBLE.md 12.4), not the step rule. The three landed x85 points
(76.6075, 77.9442, 78.6126) are double-double points of the pinned system in layout B and carry its 1e-6..1e-3
uncertainty; they are not added to any table. The ladders ran 7.4 min of wall time at 4 threads each (the --max_hours
0.13 cap was not reached; both ended on their step rule).
