# I926-mac: the sonic valley of the low-D states near D 3.043, and why the predictor goes NaN

Machine: mac (Apple M5, shared and loaded, 4 threads at nice 10). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/926.
Code: branch `wip/sa-926` of choptuik-large-d, `hp/sonic_valley.py` and `hp/lowD_highM.py` (`--sonic_refine`,
`--sonic_stop`); the notes are notes/LOW_D.md section 17 on that branch. Inputs: M 320 states of T82-win, T100-win2,
T105-win2 and I343-win2 of this repository (read with `git show`, not copied here).

## The answer

The NaN of #343's predictor at D 3.04315 is not a horizon effect and not an irregular predictor. The p equation is
singular where x = c, and near D 3.04 the states' min over tau of c - x has a valley at x ~ 0.0143 (segment 0.01 ->
0.02) whose floor, the gap, closes linearly as D falls. The integration through it is stiff like 1 / (c - x), so the
last state's plan, made for a wider gap, blows up on the starts at the new D, the last state's own included. On that
plan with the valley's steps split 4 times the predictor is finite and keeps c above x by 1.69e-6, the line's value.
The line reaches gap 0 near D 3.0431.

## 1. The gap at M 320 (`depth_M320.*`, `tangency_M320.log`, `gap_dshift.*`)

`sonic_valley.py depth` (renamed `gap` since) on the M 320 states, each on its own stored plan at its own D; the
segment 0.01 -> 0.02 (the narrowest; all segments are in the jsonl). Grid: the smallest c - x over the 320 tau points;
between: by trigonometric interpolation of c. End mismatch: the integrated end against the next node, in
double-double (check end_ok, 1e-20: all pass, 1.8e-29 or less).

| D | state | plan steps in segment | gap, grid | x | grid point | gap, between grid points | end mismatch |
|---|---|---|---|---|---|---|---|
| 3.0475 | T82-win `lowDhm_x0.000157-0.975_D3.0475_M320` | 992 | 2.447411e-04 | 0.014765 | 22 | 2.445667e-04 | 3.9e-30 |
| 3.045 | T82-win `..._D3.0450_M320` | 1684 | 1.059580e-04 | 0.014448 | 22 | 1.058518e-04 | 3.8e-30 |
| 3.044375 | T100-win2 `..._D3.0444_M320` | 2150 | 7.103961e-05 | 0.014368 | 22 | 7.077465e-05 | 3.5e-30 |
| 3.04375 | T105-win2 `..._D3.0438_M320` | 3253 | 3.587670e-05 | 0.014340 | 23 | 3.552838e-05 | 4.2e-30 |
| 3.04355 | I343-win2 `lowD343_D3.0436_M320` | 4102 | 2.449190e-05 | 0.014314 | 23 | 2.421302e-05 | 6.2e-30 |
| 3.04335 | I343-win2 `lowD343_D3.043350_M320` | 4679 | 1.309667e-05 | 0.014288 | 23 | 1.287965e-05 | 4.1e-30 |

The line (`tangency --last N`; the spread over N is a spread over fit choices, not a bound):

| fit | D where the gap is 0 | slope | line residual / range | verdict |
|---|---|---|---|---|
| last 3 (3.04375–3.04335) | 3.043120 | 0.05695 | 1.5e-4 | a line (exit 0) |
| last 4 | 3.043117 (quadratic 3.043122) | 0.05650 | 1.8e-3 | not a line (exit 1) |
| all 6 | 3.043108 (quadratic 3.043117) | 0.05578 | 1.8e-3 | not a line (exit 1) |
| last 3, control `--mutate slope` | 3.043229 | 0.09695 | 6.9e-2 | not a line (exit 1), as it must |
| last 3, between grid points | 3.043122 | 0.05662 | | (computed from the table) |

The line's values: 7.40e-6 at 3.04325 and 1.71e-6 at 3.04315 (grid, M 320). The quadratic coefficient of the gaps is
-0.13 to -0.65 (3, 4, 6 points). The control of the end check, `--mutate dshift` (the equations at D + 1e-4) on the
3.0475 state: end mismatches 9.8e-5 to 1.2e-2, exit 1 (`gap_dshift.*`), as it must. Its gaps also give the
sensitivity at fixed data: +3.7e-6 for +1e-4 in the equations' D.

## 2. The predictor at 3.04315 (`explore/`)

The predictor of #343's leg 2 at 3.04315 (Lagrange through the three M 320 states of the history) integrated through
the segment 0.01 -> 0.02 with 3.04315's equations, on the last state's stored plan (5603 steps, 4679 in the segment):

| start | plan | result |
|---|---|---|
| predictor | stored | non-finite at x 0.01404396 (step 1933), c - x +1.02e-5 one step before |
| last state (3.04335) at 3.04315's equations | stored | non-finite at x 0.01418333 (step 2414), c - x +7.15e-6 one step before |
| predictor | stored, steps split 4 times | finite; gap 1.6869e-6 at x 0.014262, grid point 23; end mismatch 1.38e-5 |
| linear predictor at 3.04335 (#343's finite start) | stored | finite; gap 1.2866e-5 (the solution's 1.3097e-5); end mismatch 3.6e-4 |

The predictor's gap at 3.04315, 1.6869e-6, is the line's 1.71e-6 to 1.3%: it keeps c above x. Both blow-ups happen
with c - x still positive, one Taylor step after a point where the state is regular: a step past the stiff
integration's stability limit, not a crossing of x = c.

## 3. The planted check of the refined plan (`planplant*`)

Truth: the converged M 320 state at 3.04335 (|F| 1.17e-28 on its own 5603-step plan, gap 1.31e-5). Coarse plan: the
plan of the M 320 state at 3.0475 (1619 steps, 992 in the segment 0.01 -> 0.02, made for a gap of 2.45e-4, 19 times
wider, whose floor lies at x 0.01477 against the truth's 0.01429). The first run (`planplant_run1_interrupted.*`,
`--refine 4 --levels 2`) was stopped by the session's interruption after three residuals: the truth on its own plan
1.170e-28, on the coarse plan nan, on the coarse plan split 4 times near x = c (5000 steps, 3968 in the segment, fewer
than the truth's own 4679 and placed for the 3.0475 valley) nan. The second run (`planplant_run2_accuracy.*`, `--refine
16 --levels 1`) gave the truth 1.170e-28 on its own plan, nan on the coarse one, and 2.917e-21 on the coarse plan split
16 times (18524 steps): finite, but its first criterion, the truth's own residual (at most 100 times 1.2e-28), failed.
The split plan's steps are placed for the 3.0475 valley, and its truncation error would floor Newton far above the
tolerance. That is a property of any split plan, so lowD_highM.py was changed (48581ddb): the split plan is only a gate,
and a start it admits goes to the two passes on its own plan. The check was rewritten for that path, its criteria fixed
before its run (`sonic_valley.py`'s docstring): the planted case exists (the truth nan or above 1e-20 on the coarse
plan); the gate admits the truth moved by delta = 1e-8 in every node state; the truth is finite on the split plan; the
moved truth's residual on its own plan lies between delta / 100 and 1e4 delta. Control `--mutate norefine`.

The third run (`planplant_run3_gate_stopped.*`, `--refine 4 --levels 2`) was stopped at 02:01 UTC: load 95-117 on
10 cores gave it about 5% of a core, and the split-16 gate, the truth on that plan and the moved truth's own plan were
6-7 h away. Its lines so far:

| residual | plan | steps | |F| |
|---|---|---|---|
| truth | its own | 5603 | 1.170e-28 |
| truth | coarse (3.0475's) | 1619 | nan: the planted case exists |
| truth + 1e-8 | coarse split 4 near x = c | 5000 | nan: the gate does not admit it at split 4 |
| truth | coarse split 16 (run 2) | 18524 | 2.917e-21: finite, the gate admits the truth at split 16 |

The rest, the gate at split 16 for the moved truth and its own plan, is step 0 of `runner_task_M320.md`, at normal
load about 20 min.

(More sections follow as the runs finish: the leg's starts at 3.04315 on the plan lowD_highM.py reuses, and
criterion 3 at M 48 / 64.)

## Recommended tasks (full text; the closing comment of #926 lists them one line each)

1. **The point at 3.04315 with the refined plan (runner, win2).** What: `runner_task_M320.md`, lowD_highM.py with
   `--sonic_refine 4 --sonic_stop` from #343's history at 3.04335, M 320 / 384. Why: the Mac showed the predictor
   finite on the refined plan but cannot run Newton at M 320 (hours per call under its load); this is #926's real case
   at the real M. Criteria (each can fail): the four of the file (the predictor nan on the reused plan and finite on
   the refined one; Newton converged at both M; the gap of the M 384 solution within 20% of the line's value; the
   control without `--sonic_refine` falls back to the last state at |F| 2.7e-2). Depends on: #926; #343's leg2b
   stopped first or finished with 3.04325, since both use win2's threads.
2. **Stop #343's leg at the closing (a coordinator's decision).** What: rerun #343's leg with `--sonic_stop` (and
   `--sonic_refine 4`), or cut its targets to 3.04315 and above. Why: its targets 3.04295, 3.04275, ... lie below
   3.04312, where the gap's line is negative and T135 / #798's predictions cross x = c; the step halving would spend
   days down to the 0.00005 floor. Criterion: the leg's log states the stop with the closing D. Depends on: #926.
3. **The closing at M 384.** What: `sonic_valley.py gap` on the M 384 states at 3.045 (T82-win), 3.04375 (T105-win2),
   3.04355 and 3.04335 (I343-win2), then `tangency --M 384 --last 3`. Why: the closing at M 320 is a grid property
   (the grid point nearest the valley's floor); if it is the solution's, M 384 gives the same D. Criterion: |D_384 -
   D_320| at most 2e-5 (the spread of the M 320 fits is 1.4e-5); a larger difference is reported, not a stop.
   About 1 h at M 384 on one core. Depends on: #926.
4. **What the family does at the closing (research).** What: whether c - x reaches 0 in the continuum at the closing
   (a tangency of c = x in the (x, tau) plane) and what lies below: a patch with c below x, whose boundary would need
   regularity conditions as at a sonic point, or the end of the family. First check Ecker et al.'s exported fields
   below D 3.043 (`hp/lowD_ecker.py --fields`; their data are external, read only) for min c - x, in their variables.
   Why: notes/LOW_D.md 6 says the family degenerates as D -> 3; the closing at 3.0431 may be where, and Ecker et
   al. report solutions down to 3.01. Criterion: a table of their min c - x at D 3.01-3.05, or a statement of why
   their data cannot give it. Depends on: #926.

## Files

| file | what |
|---|---|
| `gap_M320.jsonl`, `gap_M320.log` | `sonic_valley.py gap` (written as `depth_M320.*` by the first version, whose field is `depth`) on six M 320 states |
| `explore/` | the first probes (`probe_pred.py`, `probes.log`, `pred3.04315_r4.log`) |
| `runner_task_M320.md` | the M 320 / 384 test at 3.04315 for a runner, with its commands and criteria |
| `run_c3.sh`, `c3_*` | criterion 3 at M 48 / 64 |
