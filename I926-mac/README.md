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

(More sections follow as the runs finish: the planted check of the refined plan, the leg's starts at 3.04315 on the
plan lowD_highM.py reuses, and criterion 3 at M 48 / 64.)

## Files

| file | what |
|---|---|
| `gap_M320.jsonl`, `gap_M320.log` | `sonic_valley.py gap` (written as `depth_M320.*` by the first version, whose field is `depth`) on six M 320 states |
| `explore/` | the first probes (`probe_pred.py`, `probes.log`, `pred3.04315_r4.log`) |
| `runner_task_M320.md` | the M 320 / 384 test at 3.04315 for a runner, with its commands and criteria |
| `run_c3.sh`, `c3_*` | criterion 3 at M 48 / 64 |
