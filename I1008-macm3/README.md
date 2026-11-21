# I1008-macm3: the order-135 chain across its fold by arclength (pilot and run)

Machine macm3 (the M3 Mac, runner macm3b), issue https://github.com/nmoinvaz/choptuik-large-d/issues/1008 (from #903's
recommendation 1; the coordinator's hc of 2026-11-19). The question: does the fold move with the horizon order? Order 130's
fold: #603 D* 259.9033, #842's arclength chain stopped at D 259.903269724106.

- Start: `I903-macm3/chain_k135b/anm_pin3_D259.1072.npz`, the order-135 chain's last accepted state, D 259.107228285
  (raw ddf884afd). Step 53 of that chain was refused three times, so continuation in D cannot reach the fold.
- Code: worktree `choptuik-large-d-1008` at main d68818a4 (hp/arclength.py, `anm_run.py --arclength`), venv
  `venv-macm3-main` with the 1f3cda09 hpkernel build (no `Solver.series_o`, no `octo_tangents`; anm_run takes the series
  by the jets and one tangent per evaluation, with notices, the same bits), 6 threads, `nice -n 10` under caffeinate.
- Command: `run_1008.sh pilot|full STEPS CAP_SECONDS`, the flags of `I903-macm3/run_903_k135b.sh` unchanged (`--qd_it 40`),
  plus `--arclength 1 --arc_sign 1 --turns_max 2` and #842's arc flags (`--arc_dhold 1e-12`, `--guard 0.05`, `--border 1`),
  and `--a0 0.0455` for the first arclength step. `capped_run.py` enforces the wall-clock cap.
- Output: `pilot/` (2 steps, 3 h cap), then `full/` (24 h cap); each has `arc.jsonl`, `arc_<n>_D<D>.npz` states and
  `arcjet_*`/`jet_pin3_*` series. Logs `pilot.log`, `full.log`, exits in `exits_1008.txt`.
- The fold is where the tangent's D component t_D changes sign.

## Pilot and pilot2

- `pilot/`, `pilot.log` (main d68818a4): exit 1 after 1491 s at the first attempt, a `TypeError` in the held fit after the strong chord's first
  correction (|dw| 1.9e23) took the iterate's D out of D > 2; `pilot/arcjet_000_D259.107228.npz` is its saved series.
- `pilot2/`, `pilot2.log` (main 997072bd, which raises `ValueError` there, so the chord is refused as in the D chain): the same command with
  `EXTRA="--arc_jet <abs>/pilot/arcjet_000_D259.107228.npz"`, `--steps 2`, 3 h cap.

## Arc step 0 (pilot2, the #1008 run)

Arc step 0 accepted: a 0.0455, D 259.1527280846019, t_D 0.9999955928 -> 0.9999955952, cond max 1.000084, corrector 33 steps, max|F| 1.05e-70, 11228.2 s
(`pilot2/arc.jsonl`, `pilot2/arc_001_D259.152728.npz`). The process (anm_run pid 37512) goes on into arc step 1 with `--steps 2`.

## Arc step 1 (pilot2) and run1

Arc step 1 accepted (pilot2 step 1). pilot2's anm_run exited at 13:16:42 UTC (`--steps 2`). run1 (`run1/`, `run1.log`) started 13:17:47 UTC from `pilot2/arc_002_D259.209603.npz` with `--steps 20`, 36 h cap, nice 10 (`run_1008.sh run1 20 129600 I1008-macm3/pilot2/arc_002_D259.209603.npz`). A first launch at nice 15 was stopped by pid after 40 s and its folder moved to `~/Trash` (see `exits_1008.txt`). `stop_watch_1008.py`: SIGTERM by exact pid one accepted step after the step whose record carries a `turn`. `step_note2.py` builds each step's post.

## Arc step 2 (run1 step 0)

run1 step 0 accepted: `run1/arc_001_D259.255103.npz`, series `run1/arcjet_000_D259.209603.npz`. Step lengths restart at `--a0 0.0455` and grow by `--a_grow 1.25`.

## Arc step 3 (run1 step 1)

run1 step 1 accepted: `run1/arc_002_*.npz`.

## Arc step 4 (run1 step 2)

run1 step 2 accepted: `run1/arc_003_*.npz`.

## run1 stopped, and the AB runs (the coordinator's change of plan, 2026-11-20)

run1 (arc steps 2 to 4 accepted, arc step 5's attempts 1 and 2 refused by the stall rule: 5338 s and 11457 s, 3 and 8 corrections) was stopped
at 02:51 UTC by SIGTERM to its anm_run pid 55767 (`exits_1008.txt`); its last accepted state is `run1/arc_003_D259.383071.npz`. The order's
hypothesis (1): arc steps 2 to 4 spent 20 to 25 corrections each at lam 0.5 because the full step's trial has a quad-double |F| below ElimO's
switch (1e-15), so it is not projected, and the half step is; `--elim_switch 0` should remove that tail. Hypothesis (2): attempt 2's crawl is a
separate problem, every projection above lam 1/16 fails.

AB1 (`ab1/`, `ab1.log`): run1's command and flags unchanged (code worktree `choptuik-large-d-1008`, `git rev-parse HEAD` 997072bd6277515f189c0fae1cf7076ad65de7f6,
venv-macm3-main, 6 threads, nice 10, caffeinate) via `run_ab.sh` (run_1008.sh with `--a0` taken from `$A0`, since anm_run's parser takes an
option once), plus `--elim_switch 0`, `--state I1008-macm3/run1/arc_002_D259.311977.npz`, `--arc_jet` the abs path of `run1/arcjet_002_D259.311977.npz`,
`--a0 0.07109375` (run1/arc.jsonl step 2's exact `a`), `--steps 1`, 3 h cap. It repeats arc step 4 (run1 step 2) from the same prediction.
Pass criteria, fixed before the run (the coordinator's): (1) converged to `--tol_od 1e-60`; (2) D equal to arc_003's, and
|Delta - Delta(arc_003)| <= 1e-30, all eight parts compared; (3) at most 10 corrections; (4) corrector under 3300 s. The control is run1's own
arc step 4: 36 corrections, 9997 s. AB2 (only if AB1 passes): from `run1/arc_003_D259.383071.npz` with `arcjet_003`, `--a0 0.0444334`,
`--elim_switch 0`, `--steps 1`, 2 h cap, output `ab2/`, stopped at once if corrections 0 and 1 both accept lam <= 1/16.

## AB1 result and AB2 start (2026-11-20)

AB1 (`ab1/`, `ab1.log`; 02:52:54 to 04:08:58 UTC, exit 0, wall 4563 s) passes all four criteria: converged (final max|F| 8.62e-71), D identical to arc_003's,
|Delta - Delta(arc_003)| 9.47e-40 (all 769 entries within 2.6e-38, parts zh and zl bit-identical), 7 corrector steps (6 corrections and the converged check),
corrector 2945.3 s. The control, run1's arc step 4: 36 corrector steps, 9996.8 s. Its first four corrections are the numbers of run1's; at correction 4
run1's lam-1 trial was refused unprojected (point max|F| 2.4e-16) and AB1's was accepted (7.92e-52). `ab_compare.py` (in this folder; reads `D_str` of the meta and sums each entry's eight parts in mpmath;
controls: arc_003 against itself passes, against arc_002 fails) made the comparison; the same numbers are in the #1008 comment of that date.
Correction of a label: the `a` printed for arc step 5's refused attempts in comments 7026936360 and 7028894936 (0.0888668, 0.0444334) is the move in D;
the arclength steps are 0.0888671875 and 0.04443359375.

AB2 (`ab2/`, `ab2.log`; started 04:09:48 UTC, anm_run pid 83930): from `run1/arc_003_D259.383071.npz` with `run1/arcjet_003_D259.383071.npz`, `--a0 0.0444334`
(the coordinator's literal value, 4.4e-6 below attempt 2's arclength step), `--elim_switch 0`, `--steps 1`, 2 h cap. `stop_ab2.py` and `watch_ab.py` (in this folder) stop and watch it; `stop_ab2.py` stops it by exact pid if corrections
0 and 1 both accept lam <= 1/16 (the coordinator's rule).

AB2 interim (05:00 UTC): correction 0 of the attempt accepted lam 0.25 (trials lam 1 and 0.5 refused with failed ladders, point |F| 6.74e+08 and 4.43e+07),
so the stop rule cannot fire. `stop_ab2.py`'s first version read the base polish's `on 0:` line as the attempt's correction 0 and ended itself at
04:33:01 UTC; the fixed version (only lines after `attempt at D`) is armed since 04:33:23 UTC. The cap is capped_run.py's own timer (SIGTERM 06:09:48 UTC), left as is.
AB2's cap moved to 2026-11-20 10:10:00 UTC at the coordinator's order (05:06 UTC): `capped_run.py` (pid 83927) stopped by pid, anm_run pid 83930 continues, `hold_run.py`
holds `caffeinate -is -w 83930` and the new deadline (`exits_1008.txt`; its `ab2 exit 143 wall 3388s` line is the stopped wrapper's). anm_run's own stall rule is unchanged.

## AB2 result: arc step 5 accepted (2026-11-20 06:08 UTC)

**Arc step 5 is accepted, and t_D has not changed sign.** AB2 converged to `--tol_od 1e-60` (max|F| 6.57e-65, 10 corrector steps = 9 corrections and the check, corrector 5367.3 s) at D 259.42750402623674815, 0.044433205 above arc step 4's D. Accepted lam per correction: 0.25, 0.25, 0.25, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0. Record counts: ladder 11, failed 9, skipped 0 (`--elim_switch 0`: nothing skipped). The log has 7 `projection failed` lines (numbered 2, 3, 4, 5, 6, 7, 8); I have not reconciled the record's 9 failed projections with them.

Arclength steps so far (all from `arc.jsonl`; D move = a x t_D at the start, to 7 digits; `t_D` is the tangent's D component at the start and the end of the step):

| arc step | run | arclength a | D | t_D start | t_D end | D below 259.903269724106 |
|---|---|---|---|---|---|---|
| 0 | pilot2/0 | 0.0455 | 259.15272808460191 | 0.9999955928 | 0.9999955952 | 0.750542 |
| 1 | pilot2/1 | 0.056875 | 259.20960283416388 | 0.9999955952 | 0.9999955982 | 0.693667 |
| 2 | run1/0 | 0.0455 | 259.25510263393521 | 0.9999955982 | 0.9999956006 | 0.648167 |
| 3 | run1/1 | 0.056875 | 259.31197738380136 | 0.9999956006 | 0.9999956035 | 0.591292 |
| 4 | run1/2 | 0.07109375 | 259.38307082137117 | 0.9999956035 | 0.9999956072 | 0.520199 |
| 5 | ab2/0 | 0.0444334 | 259.42750402623675 | 0.9999956072 | 0.9999956095 | 0.475766 |

t_D is 0.9999956095 and still rising, by 2.31e-09 over arc step 5 (5.2e-08 per unit of arclength) and 3.7e-09 over arc step 4 (5.21e-08 per unit), so there is no turn yet. D is 0.475766 below order 130's D_max, which is 10.7 steps of this length.

Against run1's attempt 2 of the same step (default switch, arclength a 0.04443359375): refused by the stall rule after 8 corrections, lam 0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.03125, 0.03125, 11457.4 s. AB2 differs in `--elim_switch 0` and in a (4.4e-6 relative shorter, your `--a0 0.0444334`), one run each, so this is one comparison, not a replicate. Refused trials in AB2: 7 (lam 1 or 0.5, every one with a failed projection ladder at point max|F| 1.31e+07 to 6.74e+08), none after correction 3; from correction 4 on every full step is accepted (lam 1).

AB2 is over (anm_run pid 83930 ended on its own at 06:05:31 UTC, `done` in ab2.log; hold_run.py ended with deadline_hit False). `ab2/` holds arc.jsonl and arc_001_D259.427504.npz and no arcjet file (`ab1/` has none either, `run1/` has one per accepted step); the next step would need the series at D 259.42750402623675 computed or supplied. The code worktree `choptuik-large-d-1008` and the main checkout moved to main 9980cd93 (fast-forward) after AB2 ended.

## run2: the arclength run continued from arc step 5 (2026-11-20 06:11 UTC)

Coordinator's order (hc, 2026-11-20 ~06:10 UTC; AB2 accepted as arc step 5, CRAWL.md section 15, 32ad9fe5): run2 continues the #1008 arclength run from `ab2/arc_001_D259.427504.npz` (D 259.42750402623674815).
Command: `A0=0.0444334 EXTRA="--elim_switch 0" run_ab.sh run2 20 129600 I1008-macm3/ab2/arc_001_D259.427504.npz` (run_ab.sh: run_1008.sh's flags F and ARC unchanged, `--a0 0.0444334`, `--elim_switch 0`, `--steps 20`, `--D_max 262`, 36 h cap through capped_run, 6 threads, nice 10 under caffeinate), output `run2/`, log `run2.log`.
No `--arc_jet`: the series at the new base is computed. Code: worktree `choptuik-large-d-1008` at main 9980cd93 with the venv-macm3-main kernel (the 1f3cda09 build). Stop rule: `stop_watch_1008.py run2` (the step that holds the first turn, then one more accepted step, then SIGTERM by exact pid); anm_run's own stall rule (`--lam_stall 0.04`) stays.
Pilot check first, as ordered: anm_run must start and pass its base polish (a kernel-API mismatch shows at once). If it fails, the run goes to a worktree detached at run1's commit 997072bd and the coordinator is told.
Per arc step: arclength a (the D move named as such), D, t_D, the D distance to 259.903269724106, corrections, lam, seconds, counts.

### run2 pilot: base polish passed (2026-11-20 06:36 UTC)
Base polished: D 259.4275040262367481536151164164618, max|F| 4.37e-38 -> 7.21e-71 in 2 steps, converged, Delta moved -1.77e-39; no Traceback; the kernel-API notices are the ones AB1 and AB2 printed (no octo_tangents, residual_sub, jacobian_sub, newton_o_residual). The pilot condition (anm_run starts and passes its base polish on main 9980cd93 with the venv-macm3-main kernel) holds, so run2 continues on this worktree. Next in the log: the series at the base, computed (no arcjet), then arc step 6's first attempt. anm_run pid 98367 (elapsed 25:28, 592.3% cpu, rss 219 MB).

### run2: arc step 6 accepted (2026-11-20 08:22 UTC)

| arc step | arclength a | D move | D | Delta | t_D start | t_D end | D below 259.903269724106 | corrections | accepted lam | ladder / failed / skipped | corrector s | refused attempts | first \|dz\| | first \|dz\| / a |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 (AB2) | 0.0444334 | 0.044433205 | 259.42750402623675 | 1.68347789279812 | 0.9999956072 | 0.9999956095 | 0.475766 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5367.3 | 0 | 1.96e-15 | 4.41e-14 |
| 6 | 0.0444334 | 0.044433205 | 259.47193723120494 | 1.68347117889185 | 0.9999956095 | 0.9999956118 | 0.431332 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5222.6 | 0 | 2.89e-15 | 6.5e-14 |

Accepted steps in run2: 1. No turn recorded (anm_run's own detection of D'(s) = 0 inside an accepted step). t_D has not changed sign. t_D start of the first step of run2 0.9999956095, end of the last 0.9999956118; its change per unit arclength over the last accepted step 5.194e-08.

Step 6's accepted attempt: 7 refused trials (lam 0.5, 1, at corrections 0, 1, 2, 3, 7 `projection failed` lines, trial |F| 9.64e+06 to 3.52e+08) and 1 refused strong-chord check(s), which together took 1574 s of the corrector's 5222.6 s. The series at the base took 1091.2 s (computed by the jets, no arcjet).

anm_run pid 98367: elapsed 02:11:29, 590.1% cpu, rss 348 MB; run2 started 06:11:16 UTC, 2.19 h ago; cap 36 h (SIGTERM at 2026-11-21 18:11:16 UTC).


### run2: arc step 7, attempt 1 refused by the stall rule (2026-11-20 10:12 UTC)

Arc step 7 is not accepted yet. Its first attempt (a = 0.0444334 x 1.25 = 0.05554175, D move 0.055541506, checked: D move / a = 0.99999561 against t_D 0.99999561) from arc step 6's D 259.47193723120494 to D 259.527478737559 refused by the stall rule: on 3: lam at or below 0.04 twice in a row, stopping (stalled). The corrections took 5073 s (4621 s of trials and chord checks). The stall rule (`--lam_stall 0.04`) and `--qd_it 40` are as in run1; the stop watcher stays armed and anm_run goes on to the next attempt with a halved.

Per trial (every refused trial's ladder failed: the point |F| is the one before projection, and the trial |F| after the failed projection is the same point):

| correction | trial lam | projection | \|F\| before projection | trial max\|F\| (after) | simplified correction / \|dz\| (bound) | result | seconds |
|---|---|---|---|---|---|---|---|
| 0 | strong chord | not logged | not logged | | theta inf (bound 0.75) | refused | 250.22 |
| 0 | 1 | attempted, ladder failed | 6.49e+09 | 6.49e+09 | 2.783e+54 (0.750) | refused | 240.97 |
| 0 | 0.5 | attempted, ladder failed | 4.13e+08 | 4.13e+08 | 1.739e+53 (0.875) | refused | 219.46 |
| 0 | 0.25 | attempted, ladder failed | 2.76e+07 | 2.76e+07 | 1.087e+52 (0.938) | refused | 180.41 |
| 0 | 0.125 | projected, ladder converged | not logged | 1.94e-29 | 8.753e-01 (0.969) | accepted | 247.7 |
| 1 | 1 | attempted, ladder failed | 4.32e+09 | 4.32e+09 | 1.852e+54 (0.750) | refused | 240.43 |
| 1 | 0.5 | attempted, ladder failed | 2.96e+08 | 2.96e+08 | 1.252e+53 (0.875) | refused | 239.39 |
| 1 | 0.25 | attempted, ladder failed | 2.75e+07 | 2.75e+07 | 1.114e+52 (0.938) | refused | 234.66 |
| 1 | 0.125 | projected, ladder converged | not logged | 3.30e-29 | 8.743e-01 (0.969) | accepted | 246.23 |
| 2 | 1 | attempted, ladder failed | 2.69e+09 | 2.69e+09 | 1.236e+54 (0.750) | refused | 239.48 |
| 2 | 0.5 | attempted, ladder failed | 2.00e+08 | 2.00e+08 | 9.092e+52 (0.875) | refused | 236.44 |
| 2 | 0.25 | attempted, ladder failed | 2.48e+07 | 2.48e+07 | 1.106e+52 (0.938) | refused | 232.15 |
| 2 | 0.125 | attempted, ladder failed | 1.14e+07 | 1.14e+07 | 3.539e+51 (0.969) | refused | 171.76 |
| 2 | 0.0625 | attempted, ladder failed | 9.27e+06 | 9.27e+06 | 2.477e+51 (0.984) | refused | 171.41 |
| 2 | 0.03125 | projected, ladder converged | not logged | 3.27e-29 | 9.687e-01 (0.992) | accepted | 239.31 |
| 3 | 1 | attempted, ladder failed | 2.32e+09 | 2.32e+09 | 1.112e+54 (0.750) | refused | 239.5 |
| 3 | 0.5 | attempted, ladder failed | 1.75e+08 | 1.75e+08 | 8.265e+52 (0.875) | refused | 227.26 |
| 3 | 0.25 | attempted, ladder failed | 2.26e+07 | 2.26e+07 | 1.039e+52 (0.938) | refused | 167.46 |
| 3 | 0.125 | attempted, ladder failed | 1.11e+07 | 1.11e+07 | 3.473e+51 (0.969) | refused | 177.55 |
| 3 | 0.0625 | attempted, ladder failed | 9.14e+06 | 9.14e+06 | 2.485e+51 (0.984) | refused | 176.92 |
| 3 | 0.03125 | projected, ladder converged | not logged | 3.24e-29 | 9.687e-01 (0.992) | accepted | 242.71 |

Per correction:

| correction | accepted lam | max\|F\| before -> after | \|dz\| before -> after | seconds |
|---|---|---|---|---|
| 0 | 0.125 | 3.77e-36 -> 1.94e-29 | 8.11e-15 -> 7.12e-15 | 1254.16 |
| 1 | 0.125 | 1.94e-29 -> 3.30e-29 | 7.12e-15 -> 6.19e-15 | 1073.55 |
| 2 | 0.03125 | 3.30e-29 -> 3.27e-29 | 6.19e-15 -> 6.00e-15 | 1403.1 |
| 3 | 0.03125 | 3.27e-29 -> 3.24e-29 | 6.00e-15 -> 5.81e-15 | 1342.52 |

First |dz| of every attempt against the arclength step a (D rises down the table; run1's last two are the refused attempts of arc step 5; AB1, AB2 and run2 ran with `--elim_switch 0`):

| run | arclength a | first \|dz\| | first \|dz\| / a | accepted lam at correction 0 |
|---|---|---|---|---|
| pilot2 | 0.0455 | 5.37e-15 | 1.18e-13 | 0.25 |
| pilot2 | 0.056875 | 4.60e-16 | 8.09e-15 | 1 |
| run1 | 0.0455 | 6.20e-16 | 1.36e-14 | 1 |
| run1 | 0.056875 | 8.92e-16 | 1.57e-14 | 0.5 |
| run1 | 0.07109375 | 8.83e-16 | 1.24e-14 | 0.5 |
| run1 | 0.0888671875 | 9.21e-15 | 1.04e-13 | 0.125 |
| run1 | 0.04443359375 | 4.82e-15 | 1.08e-13 | 0.0625 |
| ab1 | 0.07109375 | 8.83e-16 | 1.24e-14 | 0.5 |
| ab2 | 0.0444334 | 1.96e-15 | 4.41e-14 | 0.25 |
| run2 | 0.0444334 | 2.89e-15 | 6.5e-14 | 0.25 |
| run2 | 0.05554175 | 8.11e-15 | 1.46e-13 | 0.125 |

Next: anm_run's attempt 2 halves a to 0.027770875 (D move 0.027770753). If first |dz| / a stays at this attempt's 1.46e-13, its first |dz| is 4.05e-15, between 2.89e-15 (arc step 6, accepted lam 0.25 x3) and 4.82e-15 (run1's refused attempt 2 of arc step 5), and pilot2's step 0 was accepted at 5.37e-15 with lam 0.25, so the table does not fix where the crawl starts. A halved attempt costs about the corrector time of this one if it is refused as well (this attempt: 5073 s of corrections). The series at arc step 6's D is in `run2/arcjet_001_D259.471937.npz` if a restart with another `--a0` is wanted (`--arc_jet` reads it, saving the 1085 s of forming it); I have not changed anything.

anm_run pid 98367: elapsed 04:01:20, 124.5% cpu, rss 323 MB; D 0.431332 below 259.903269724106 at arc step 6's D.

### run2: arc step 7, attempt 2 refused by the stall rule (2026-11-20 11:21 UTC)

Arc step 7 is not accepted yet. Its attempt 2 (a = 0.0444334 x 1.25 / 2 = 0.027770875, D move 0.027770753, checked: D move / a = 0.99999561 against t_D 0.99999561) from arc step 6's D 259.47193723120494 to D 259.499707984362 refused by the stall rule: on 1: lam at or below 0.04 twice in a row, stopping (stalled). The corrector line says 3843.6 s; its corrections took 3212 s (2985 s of trials and chord checks). The stall rule (`--lam_stall 0.04`) and `--qd_it 40` are as in run1; the stop watcher stays armed and anm_run goes on to the next attempt with a halved.

Per trial (every refused trial's ladder failed: the point |F| is the one before projection, and the trial |F| after the failed projection is the same point):

| correction | trial lam | projection | \|F\| before projection | trial max\|F\| (after) | simplified correction / \|dz\| (bound) | result | seconds |
|---|---|---|---|---|---|---|---|
| 0 | strong chord | not logged | not logged | | theta inf (bound 0.75) | refused | 240.5 |
| 0 | 1 | attempted, ladder failed | 3.51e+11 | 3.51e+11 | 6.225e+55 (0.750) | refused | 236.36 |
| 0 | 0.5 | attempted, ladder failed | 2.20e+10 | 2.20e+10 | 3.891e+54 (0.875) | refused | 236.08 |
| 0 | 0.25 | attempted, ladder failed | 1.39e+09 | 1.39e+09 | 2.432e+53 (0.938) | refused | 236.31 |
| 0 | 0.125 | attempted, ladder failed | 8.99e+07 | 8.99e+07 | 1.520e+52 (0.969) | refused | 216.07 |
| 0 | 0.0625 | attempted, ladder failed | 9.68e+06 | 9.68e+06 | 9.499e+50 (0.984) | refused | 232.04 |
| 0 | 0.03125 | projected, ladder converged | not logged | 8.05e-30 | 9.688e-01 (0.992) | accepted | 242.98 |
| 1 | 1 | attempted, ladder failed | 3.21e+11 | 3.21e+11 | 5.603e+55 (0.750) | refused | 236.45 |
| 1 | 0.5 | attempted, ladder failed | 2.02e+10 | 2.02e+10 | 3.516e+54 (0.875) | refused | 238.24 |
| 1 | 0.25 | attempted, ladder failed | 1.30e+09 | 1.30e+09 | 2.244e+53 (0.938) | refused | 237.18 |
| 1 | 0.125 | attempted, ladder failed | 9.17e+07 | 9.17e+07 | 1.532e+52 (0.969) | refused | 220.38 |
| 1 | 0.0625 | attempted, ladder failed | 1.17e+07 | 1.17e+07 | 1.337e+51 (0.984) | refused | 164.98 |
| 1 | 0.03125 | projected, ladder converged | not logged | 1.56e-29 | 9.688e-01 (0.992) | accepted | 247.32 |

Per correction:

| correction | accepted lam | max\|F\| before -> after | \|dz\| before -> after | seconds |
|---|---|---|---|---|
| 0 | 0.03125 | 1.14e-35 -> 8.05e-30 | 2.01e-14 -> 1.95e-14 | 1756.06 |
| 1 | 0.03125 | 8.05e-30 -> 1.56e-29 | 1.95e-14 -> 1.89e-14 | 1455.95 |

First |dz| of every attempt against the arclength step a (D rises down the table; run1's last two are the refused attempts of arc step 5; AB1, AB2 and run2 ran with `--elim_switch 0`):

| run | arclength a | first \|dz\| | first \|dz\| / a | accepted lam at correction 0 |
|---|---|---|---|---|
| pilot2 | 0.0455 | 5.37e-15 | 1.18e-13 | 0.25 |
| pilot2 | 0.056875 | 4.60e-16 | 8.09e-15 | 1 |
| run1 | 0.0455 | 6.20e-16 | 1.36e-14 | 1 |
| run1 | 0.056875 | 8.92e-16 | 1.57e-14 | 0.5 |
| run1 | 0.07109375 | 8.83e-16 | 1.24e-14 | 0.5 |
| run1 | 0.0888671875 | 9.21e-15 | 1.04e-13 | 0.125 |
| run1 | 0.04443359375 | 4.82e-15 | 1.08e-13 | 0.0625 |
| ab1 | 0.07109375 | 8.83e-16 | 1.24e-14 | 0.5 |
| ab2 | 0.0444334 | 1.96e-15 | 4.41e-14 | 0.25 |
| run2 | 0.0444334 | 2.89e-15 | 6.5e-14 | 0.25 |
| run2 | 0.05554175 | 8.11e-15 | 1.46e-13 | 0.125 |
| run2 | 0.027770875 | 2.01e-14 | 7.24e-13 | 0.03125 |

Next: anm_run's attempt 3 halves a to 0.0138854375 (D move 0.013885377); `--a_grow 1.25` and the halving allow up to 4 attempts per step, so up to 2 more. First |dz| went from 8.11e-15 at a = 0.05554175 to 2.01e-14 at a = 0.027770875: a factor 2.48 for an a ratio of 0.5, so first |dz| / a went from 1.46e-13 to 7.24e-13. A first |dz| proportional to a (run1's two refused attempts of arc step 5 gave 9.21e-15 at a 0.0888671875 and 4.82e-15 at a 0.04443359375) would have fallen to 4.05e-15. Same base, same series, same re-seed code; the predicted max|F| is 1.14e-35 here against 3.77e-36 for the longer step. The series at arc step 6's D is in `run2/arcjet_001_D259.471937.npz` if a restart with another `--a0` is wanted (`--arc_jet` reads it, saving the 1085 s of forming it); I have not changed anything.

anm_run pid 98367: elapsed 05:09:58, 591.1% cpu, rss 328 MB; D 0.431332 below 259.903269724106 at arc step 6's D.



### run2: arc step 7 accepted on attempt 3 (2026-11-20 13:24 UTC)

| arc step | arclength a | D move | D | Delta | t_D start | t_D end | D below 259.903269724106 | corrections | accepted lam | ladder / failed / skipped | corrector s | refused attempts | first \|dz\| | first \|dz\| / a |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 (AB2) | 0.0444334 | 0.044433205 | 259.42750402623675 | 1.68347789279812 | 0.9999956072 | 0.9999956095 | 0.475766 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5367.3 | 0 | 1.96e-15 | 4.41e-14 |
| 6 | 0.0444334 | 0.044433205 | 259.47193723120494 | 1.68347117889185 | 0.9999956095 | 0.9999956118 | 0.431332 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5222.6 | 0 | 2.89e-15 | 6.5e-14 |
| 7 | 0.0138854375 | 0.013885377 | 259.48582260777852 | 1.68346908127357 | 0.9999956118 | 0.9999956126 | 0.417447 | 12 | 0.25 x2, 0.125 x3, 0.5, 1 x6 | 14 / 16 / 0 | 7284.8 | 2 | 4.76e-15 | 3.43e-13 |

Accepted steps in run2: 2. No turn recorded (anm_run's own detection of D'(s) = 0 inside an accepted step). t_D has not changed sign. t_D start of the first step of run2 0.9999956095, end of the last 0.9999956126; its change per unit arclength over the last accepted step 5.19e-08.

Step 7's accepted attempt: 14 refused trials (lam 0.25, 0.5, 1, at corrections 0, 1, 2, 3, 4, 5, 14 `projection failed` lines, trial |F| 9.54e+06 to 1.08e+09) and 1 refused strong-chord check(s), which together took 2825 s of the corrector's 7284.8 s. The series at the base took 1091.2 s (computed by the jets, no arcjet).

anm_run pid 98367: elapsed 07:13:19, 591.9% cpu, rss 463 MB; run2 started 06:11:16 UTC, 7.22 h ago; cap 36 h (SIGTERM at 2026-11-21 18:11:16 UTC).

Every attempt of every log, with the predicted max|F| (the series' residual at the re-seeded point, before any correction):

| log | attempt | D move | D of the attempt | predicted max\|F\| | first \|dz\| | first \|dz\| / predicted max\|F\| | refused trial lam at correction 0 | accepted lam at correction 0 | accepted lam x first \|dz\| | corrector steps | corrector s | outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pilot2 | 1 | 0.045500 | 259.15272808 | 8.9e-36 | 5.37e-15 | 6.03e+20 | 1, 0.5 | 0.25 | 1.34e-15 | 33 | 11228.2 | accepted |
| pilot2 | 2 | 0.056875 | 259.20960283 | 1.26e-36 | 4.6e-16 | 3.65e+20 | none | 1 | 4.6e-16 | 26 | 9721.7 | accepted |
| run1 | 1 | 0.045500 | 259.25510263 | 1.4e-36 | 6.2e-16 | 4.43e+20 | none | 1 | 6.2e-16 | 24 | 7446.4 | accepted |
| run1 | 2 | 0.056875 | 259.31197738 | 2.61e-36 | 8.92e-16 | 3.42e+20 | 1 | 0.5 | 4.46e-16 | 35 | 9788.8 | accepted |
| run1 | 3 | 0.071093 | 259.38307082 | 1.66e-36 | 8.83e-16 | 5.32e+20 | 1 | 0.5 | 4.41e-16 | 36 | 9996.8 | accepted |
| run1 | 4 | 0.088867 | 259.47193762 | 6.28e-36 | 9.21e-15 | 1.47e+21 | 1, 0.5, 0.25 | 0.125 | 1.15e-15 | 3 | 5338.2 | refused (stall rule) |
| run1 | 5 | 0.044433 | 259.42750422 | 7.16e-36 | 4.82e-15 | 6.73e+20 | 1, 0.5, 0.25, 0.125 | 0.0625 | 3.01e-16 | 8 | 11457.4 | refused (stall rule) |
| ab1 | 1 | 0.071093 | 259.38307082 | 1.66e-36 | 8.83e-16 | 5.32e+20 | 1 | 0.5 | 4.41e-16 | 7 | 2945.3 | accepted |
| ab2 | 1 | 0.044433 | 259.42750403 | 2.97e-36 | 1.96e-15 | 6.6e+20 | 1, 0.5 | 0.25 | 4.9e-16 | 10 | 5367.3 | accepted |
| run2 | 1 | 0.044433 | 259.47193723 | 2.2e-36 | 2.89e-15 | 1.31e+21 | 1, 0.5 | 0.25 | 7.23e-16 | 10 | 5222.6 | accepted |
| run2 | 2 | 0.055542 | 259.52747874 | 3.77e-36 | 8.11e-15 | 2.15e+21 | 1, 0.5, 0.25 | 0.125 | 1.01e-15 | 4 | 5716.4 | refused (stall rule) |
| run2 | 3 | 0.027771 | 259.49970798 | 1.14e-35 | 2.01e-14 | 1.76e+21 | 1, 0.5, 0.25, 0.125, 0.0625 | 0.03125 | 6.28e-16 | 2 | 3843.6 | refused (stall rule) |
| run2 | 4 | 0.013885 | 259.48582261 | 2.86e-36 | 4.76e-15 | 1.66e+21 | 1, 0.5 | 0.25 | 1.19e-15 | 13 | 7284.8 | accepted |

13 attempts in 5 logs, 12 distinct points (run1's attempt 3 and ab1's attempt 1 are the same point).

1. The predicted max|F| is 1.3e-36 to 1.1e-35 for D moves of 0.0139 to 0.0889. Over this range it does not fall with a shorter step. Ordered by D move, the predicted max|F| is 2.9e-36, 1.1e-35, 3e-36, 2.2e-36, 7.2e-36, 8.9e-36, 1.4e-36, 3.8e-36, 1.3e-36, 2.6e-36, 1.7e-36, 6.3e-36 (D moves 0.0139, 0.0278, 0.0444, 0.0444, 0.0444, 0.0455, 0.0455, 0.0555, 0.0569, 0.0569, 0.0711, 0.0889).

2. First |dz| / predicted max|F| is 3.4e+20 to 6.7e+20 at the 7 points below D 259.45 and 1.3e+21 to 2.2e+21 at the 5 points above it. Ordered by D: 259.1527: 6e+20, 259.2096: 3.7e+20, 259.2551: 4.4e+20, 259.3120: 3.4e+20, 259.3831: 5.3e+20, 259.4275: 6.6e+20, 259.4275: 6.7e+20, 259.4719: 1.3e+21, 259.4719: 1.5e+21, 259.4858: 1.7e+21, 259.4997: 1.8e+21, 259.5275: 2.2e+21.

3. At one D move (0.0444, 3 distinct points) the predicted max|F| is 2.2e-36, 3e-36, 7.2e-36, a spread of x3.3, against x9.0 over all 12 points.

4. First |dz| runs from 4.6e-16 to 2e-14 (x44). At the 10 points where correction 0 accepts lam below 1, accepted lam times first |dz| is 3e-16 to 1.3e-15 (x4.5), and the smallest refused trial lam at correction 0 times first |dz| is 6e-16 to 2.7e-15. The two ranges overlap, so there is no sharp threshold in lam times |dz|.

5. Arc step 7 took 4.98 h from arc step 6's record (08:21:34 UTC) to its own (13:20:25 UTC). Its three attempts took 5716.4 + 3843.6 + 7284.8 = 16844.8 s of corrector time, and the series at its base 1085.3 s, against 5222.6 s of corrector time and 1091.2 s of series for arc step 6 (series at its base, the first line of run2.log).

What the table says about the first |dz| (observed, not explained):

- The predicted max|F| is a floor of about 1e-36 at every attempt, whatever the D move (statement 1) and at one D move it still scatters by a factor of 3.3, against 9.0 over all 12 points (statement 3). The first |dz| follows it, so the earlier reading that the first |dz| scales with a was wrong. Run1's refused pair was a coincidence. Halving a does not lower it.
- The factor from predicted max|F| to first |dz| has risen with D, from 3.4e+20 to 6.7e+20 up to D 259.43 to 1.3e+21 to 2.2e+21 from D 259.47 (statement 2).
- The first correction the corrector accepts at lam below 1 has a size lam times first |dz| of 3e-16 to 1.3e-15, a factor of 4.5, while the first |dz| spans a factor of 44 (statement 4). A larger first |dz| therefore means a smaller lam, more corrections before lam reaches 1, and the stall rule (lam at or below 0.04 twice in a row) once lam falls that low.

The source of the 1e-36 floor is not identified. I changed no flag. The earlier options message is unanswered, so run2 goes on from arc step 7 as launched: the series at its D 259.4858226077785 is being formed now (1085 to 1091 s at the last two bases), then arc step 8's first attempt. Its a comes from anm_run's rule and goes in the next post. t_D is 0.9999956126 and has not changed sign, no turn is recorded, and D is 0.417447 below 259.903269724106.


### run2: arc step 8 accepted at its first attempt (2026-11-20 14:56 UTC)

| arc step | arclength a | D move | D | Delta | t_D start | t_D end | D below 259.903269724106 | corrections | accepted lam | ladder / failed / skipped | corrector s | refused attempts | first \|dz\| | first \|dz\| / a |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 (AB2) | 0.0444334 | 0.044433205 | 259.42750402623675 | 1.68347789279812 | 0.9999956072 | 0.9999956095 | 0.475766 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5367.3 | 0 | 1.96e-15 | 4.41e-14 |
| 6 | 0.0444334 | 0.044433205 | 259.47193723120494 | 1.68347117889185 | 0.9999956095 | 0.9999956118 | 0.431332 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5222.6 | 0 | 2.89e-15 | 6.5e-14 |
| 7 | 0.0138854375 | 0.013885377 | 259.48582260777852 | 1.68346908127357 | 0.9999956118 | 0.9999956126 | 0.417447 | 12 | 0.25 x2, 0.125 x3, 0.5, 1 x6 | 14 / 16 / 0 | 7284.8 | 2 | 4.76e-15 | 3.43e-13 |
| 8 | 0.0138854375 | 0.013885377 | 259.49970798436211 | 1.68346698388404 | 0.9999956126 | 0.9999956133 | 0.403562 | 9 | 0.25 x2, 0.5, 1 x6 | 11 / 7 / 0 | 4593.6 | 0 | 3.16e-15 | 2.28e-13 |

Accepted steps in run2: 3. No turn recorded (anm_run's own detection of D'(s) = 0 inside an accepted step). t_D has not changed sign. t_D start of the first step of run2 0.9999956095, end of the last 0.9999956133; its change per unit arclength over the last accepted step 5.188e-08.

Step 8's accepted attempt: 5 refused trials (lam 0.5, 1, at corrections 0, 1, 2, 5 `projection failed` lines, trial |F| 1.2e+07 to 2.6e+08) and 1 refused strong-chord check(s), which together took 1273 s of the corrector's 4593.6 s. The series at the base took 1049.9 s (formed by the jets inside the run, which also saves its arcjet).

anm_run pid 98367: elapsed 08:45:00, 573.7% cpu, rss 393 MB; run2 started 06:11:16 UTC, 8.75 h ago; cap 36 h (SIGTERM at 2026-11-21 18:11:16 UTC).

Every attempt of every log, with the predicted max|F| (the series' residual at the re-seeded point, before any correction):

| log | attempt | D move | D of the attempt | predicted max\|F\| | first \|dz\| | first \|dz\| / predicted max\|F\| | refused trial lam at correction 0 | accepted lam at correction 0 | accepted lam x first \|dz\| | corrector steps | corrector s | outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pilot2 | 1 | 0.045500 | 259.15272808 | 8.9e-36 | 5.37e-15 | 6.03e+20 | 1, 0.5 | 0.25 | 1.34e-15 | 33 | 11228.2 | accepted |
| pilot2 | 2 | 0.056875 | 259.20960283 | 1.26e-36 | 4.6e-16 | 3.65e+20 | none | 1 | 4.6e-16 | 26 | 9721.7 | accepted |
| run1 | 1 | 0.045500 | 259.25510263 | 1.4e-36 | 6.2e-16 | 4.43e+20 | none | 1 | 6.2e-16 | 24 | 7446.4 | accepted |
| run1 | 2 | 0.056875 | 259.31197738 | 2.61e-36 | 8.92e-16 | 3.42e+20 | 1 | 0.5 | 4.46e-16 | 35 | 9788.8 | accepted |
| run1 | 3 | 0.071093 | 259.38307082 | 1.66e-36 | 8.83e-16 | 5.32e+20 | 1 | 0.5 | 4.41e-16 | 36 | 9996.8 | accepted |
| run1 | 4 | 0.088867 | 259.47193762 | 6.28e-36 | 9.21e-15 | 1.47e+21 | 1, 0.5, 0.25 | 0.125 | 1.15e-15 | 3 | 5338.2 | refused (stall rule) |
| run1 | 5 | 0.044433 | 259.42750422 | 7.16e-36 | 4.82e-15 | 6.73e+20 | 1, 0.5, 0.25, 0.125 | 0.0625 | 3.01e-16 | 8 | 11457.4 | refused (stall rule) |
| ab1 | 1 | 0.071093 | 259.38307082 | 1.66e-36 | 8.83e-16 | 5.32e+20 | 1 | 0.5 | 4.41e-16 | 7 | 2945.3 | accepted |
| ab2 | 1 | 0.044433 | 259.42750403 | 2.97e-36 | 1.96e-15 | 6.6e+20 | 1, 0.5 | 0.25 | 4.9e-16 | 10 | 5367.3 | accepted |
| run2 | 1 | 0.044433 | 259.47193723 | 2.2e-36 | 2.89e-15 | 1.31e+21 | 1, 0.5 | 0.25 | 7.23e-16 | 10 | 5222.6 | accepted |
| run2 | 2 | 0.055542 | 259.52747874 | 3.77e-36 | 8.11e-15 | 2.15e+21 | 1, 0.5, 0.25 | 0.125 | 1.01e-15 | 4 | 5716.4 | refused (stall rule) |
| run2 | 3 | 0.027771 | 259.49970798 | 1.14e-35 | 2.01e-14 | 1.76e+21 | 1, 0.5, 0.25, 0.125, 0.0625 | 0.03125 | 6.28e-16 | 2 | 3843.6 | refused (stall rule) |
| run2 | 4 | 0.013885 | 259.48582261 | 2.86e-36 | 4.76e-15 | 1.66e+21 | 1, 0.5 | 0.25 | 1.19e-15 | 13 | 7284.8 | accepted |
| run2 | 5 | 0.013885 | 259.49970798 | 1.87e-36 | 3.16e-15 | 1.69e+21 | 1, 0.5 | 0.25 | 7.9e-16 | 10 | 4593.6 | accepted |

14 attempts in 5 logs, 13 distinct points (run1's attempt 3 and ab1's attempt 1 are the same point).

1. The predicted max|F| is 1.3e-36 to 1.1e-35 for D moves of 0.0139 to 0.0889. Over this range it does not fall with a shorter step. Ordered by D move, the predicted max|F| is 2.9e-36, 1.9e-36, 1.1e-35, 3e-36, 2.2e-36, 7.2e-36, 8.9e-36, 1.4e-36, 3.8e-36, 1.3e-36, 2.6e-36, 1.7e-36, 6.3e-36 (D moves 0.0139, 0.0139, 0.0278, 0.0444, 0.0444, 0.0444, 0.0455, 0.0455, 0.0555, 0.0569, 0.0569, 0.0711, 0.0889).

2. First |dz| / predicted max|F| is 3.4e+20 to 6.7e+20 at the 7 points below D 259.45 and 1.3e+21 to 2.2e+21 at the 6 points above it. Ordered by D: 259.1527: 6e+20, 259.2096: 3.7e+20, 259.2551: 4.4e+20, 259.3120: 3.4e+20, 259.3831: 5.3e+20, 259.4275: 6.6e+20, 259.4275: 6.7e+20, 259.4719: 1.3e+21, 259.4719: 1.5e+21, 259.4858: 1.7e+21, 259.4997: 1.8e+21, 259.4997: 1.7e+21, 259.5275: 2.2e+21.

3. At one D move (0.0444, 3 distinct points) the predicted max|F| is 2.2e-36, 3e-36, 7.2e-36, a spread of x3.3, against x9.0 over all 13 points.

4. First |dz| runs from 4.6e-16 to 2e-14 (x44). At the 11 points where correction 0 accepts lam below 1, accepted lam times first |dz| is 3e-16 to 1.3e-15 (x4.5), and the smallest refused trial lam at correction 0 times first |dz| is 6e-16 to 2.7e-15. The two ranges overlap, so there is no sharp threshold in lam times |dz|.

5. Arc step 8 took 1.57 h from arc step 7's record (13:20:25 UTC) to its own (14:54:30 UTC). Its 1 attempt took 4593.6 s of corrector time, and the series at its base 1049.9 s. Arc step 7: 3 attempts, 5716.4 + 3843.6 + 7284.8 = 16844.8 s of corrector time, series 1085.3 s.

6. The target D 259.49970798 was attempted from 2 bases: run2 attempt 3, D move 0.0278, predicted max|F| 1.14e-35, first |dz| 2.01e-14, ratio 1.76e+21, refused (stall rule); run2 attempt 5, D move 0.0139, predicted max|F| 1.87e-36, first |dz| 3.16e-15, ratio 1.69e+21, accepted. Predicted max|F| is x6.1 lower from the shorter step and the ratio differs by x1.04.

7. Spearman rank correlation between D move and predicted max|F| over the 13 distinct attempts: -0.20 (ranks, ties by order; +1 is a monotone rise with the D move, -1 a monotone fall, 0 no trend).

Step 8 was accepted at its first attempt with the same arclength a as step 7: with `--a_hold 1` a step that needed a halving keeps its length for the next one (anm_run.py line 114). It had no refused attempt and took 1.57 h, against 4.98 h for step 7.

New in the table: the target D 259.49970798 was attempted twice, from bases 0.0278 and 0.0139 below it (statement 6). The predicted max|F| was x6.1 lower from the shorter step, but the factor from predicted max|F| to first |dz| agreed within x1.04. For this one pair that is consistent with the factor belonging to the target D and not to the base. Over all 13 points the predicted max|F| shows no monotone trend with the D move (statement 7). The source of the 1e-36 floor is still not identified.

I changed no flag. run2 goes on: the series at D 259.4997 is being formed (1050 to 1091 s at the last bases), then arc step 9's first attempt. By the grow rule, a step accepted at its first attempt grows the next one by `--a_grow 1.25`, so its arclength a should be 0.0138854375 x 1.25 = 0.017356796875. The log will show it. t_D is 0.9999956133, no turn, and D is 0.403562 below 259.903269724106.


### run2 progress, arc step 9 attempt 1 in progress (2026-11-20 18:11 UTC)

Arc step 9's first attempt (arclength a 0.01735679688 = step 8's a 0.0138854 x 1.25, as the grow rule gives, D move 0.017356721) from D 259.49970798436209 to D 259.517064705106 is in its corrector, 11 corrections done, none refused by the stall rule so far (`--lam_stall 0.04`). The 11 corrections took 10330 s. Last accepted state: arc step 8, t_D 0.9999956133, no turn recorded, D 0.403562 below 259.903269724106 at its D and 0.386205 below it at this attempt's D.

| correction | accepted lam | max\|F\| before -> after | \|dz\| before -> after | refused trials | seconds |
|---|---|---|---|---|---|
| 0 | 0.125 | 3.46e-36 -> 1.45e-29 | 7.03e-15 -> 6.17e-15 | 4 | 1205.17 |
| 1 | 0.125 | 1.45e-29 -> 2.44e-29 | 6.17e-15 -> 5.38e-15 | 3 | 967.02 |
| 2 | 0.125 | 2.44e-29 -> 3.05e-29 | 5.38e-15 -> 4.69e-15 | 3 | 893.35 |
| 3 | 0.0625 | 3.05e-29 -> 3.03e-29 | 4.69e-15 -> 4.39e-15 | 4 | 1075.14 |
| 4 | 0.0625 | 3.03e-29 -> 2.99e-29 | 4.39e-15 -> 4.12e-15 | 4 | 1112.27 |
| 5 | 0.0625 | 2.99e-29 -> 2.94e-29 | 4.12e-15 -> 3.86e-15 | 4 | 1100.98 |
| 6 | 0.125 | 2.94e-29 -> 3.04e-29 | 3.86e-15 -> 3.37e-15 | 3 | 959.34 |
| 7 | 0.125 | 3.04e-29 -> 3.00e-29 | 3.37e-15 -> 2.95e-15 | 3 | 886.4 |
| 8 | 0.125 | 3.00e-29 -> 2.89e-29 | 2.95e-15 -> 2.59e-15 | 3 | 929.47 |
| 9 | 0.25 | 2.89e-29 -> 2.95e-29 | 2.59e-15 -> 1.95e-15 | 2 | 677.76 |
| 10 | 0.5 | 2.95e-29 -> 3.24e-29 | 1.95e-15 -> 9.87e-16 | 1 | 523.51 |

Predicted max|F| 3.46e-36 (the prediction moved +3.55e-31 in D and -5.36e-35 in Delta at the re-seed), first |dz| 7.03e-15, first |dz| / predicted max|F| 2.03e+21 at this target D (the table of the last post gave 1.7e+21 at D 259.4997 and 2.2e+21 at D 259.5275). Refused trials so far 33 of 44 trial lines, 33 `projection failed` lines, refused trial lam 0.125 to 1 (trial |F| 8.63e+06 to 3.67e+09). Accepted lam so far: 0.125, 0.125, 0.125, 0.0625, 0.0625, 0.0625, 0.125, 0.125, 0.125, 0.25, 0.5.

anm_run pid 98367: elapsed 12:00:07, 578.9% cpu, rss 331 MB; cap 36 h (SIGTERM at 2026-11-21 18:11:16 UTC).



### run2 progress, arc step 9 attempt 1 at correction 12 (2026-11-20 18:18 UTC)

Arc step 9's first attempt (arclength a 0.01735679688 = step 8's a 0.0138854 x 1.25, as the grow rule gives, D move 0.017356721) from D 259.49970798436209 to D 259.517064705106 is in its corrector, 12 corrections done, none refused by the stall rule so far (`--lam_stall 0.04`). The 12 corrections took 10776 s. Last accepted state: arc step 8, t_D 0.9999956133, no turn recorded, D 0.403562 below 259.903269724106 at its D and 0.386205 below it at this attempt's D.

| correction | accepted lam | max\|F\| before -> after | \|dz\| before -> after | refused trials | seconds |
|---|---|---|---|---|---|
| 0 | 0.125 | 3.46e-36 -> 1.45e-29 | 7.03e-15 -> 6.17e-15 | 4 | 1205.17 |
| 1 | 0.125 | 1.45e-29 -> 2.44e-29 | 6.17e-15 -> 5.38e-15 | 3 | 967.02 |
| 2 | 0.125 | 2.44e-29 -> 3.05e-29 | 5.38e-15 -> 4.69e-15 | 3 | 893.35 |
| 3 | 0.0625 | 3.05e-29 -> 3.03e-29 | 4.69e-15 -> 4.39e-15 | 4 | 1075.14 |
| 4 | 0.0625 | 3.03e-29 -> 2.99e-29 | 4.39e-15 -> 4.12e-15 | 4 | 1112.27 |
| 5 | 0.0625 | 2.99e-29 -> 2.94e-29 | 4.12e-15 -> 3.86e-15 | 4 | 1100.98 |
| 6 | 0.125 | 2.94e-29 -> 3.04e-29 | 3.86e-15 -> 3.37e-15 | 3 | 959.34 |
| 7 | 0.125 | 3.04e-29 -> 3.00e-29 | 3.37e-15 -> 2.95e-15 | 3 | 886.4 |
| 8 | 0.125 | 3.00e-29 -> 2.89e-29 | 2.95e-15 -> 2.59e-15 | 3 | 929.47 |
| 9 | 0.25 | 2.89e-29 -> 2.95e-29 | 2.59e-15 -> 1.95e-15 | 2 | 677.76 |
| 10 | 0.5 | 2.95e-29 -> 3.24e-29 | 1.95e-15 -> 9.87e-16 | 1 | 523.51 |
| 11 | 1 | 3.24e-29 -> 1.91e-29 | 9.87e-16 -> 1.11e-16 | 0 | 445.81 |

Predicted max|F| 3.46e-36 (the prediction moved +3.55e-31 in D and -5.36e-35 in Delta at the re-seed), first |dz| 7.03e-15, first |dz| / predicted max|F| 2.03e+21 at this target D (the table of the last post gave 1.7e+21 at D 259.4997 and 2.2e+21 at D 259.5275). Refused trials so far 33 of 45 trial lines, 33 `projection failed` lines, refused trial lam 0.125 to 1 (trial |F| 8.63e+06 to 3.67e+09). Accepted lam so far: 0.125, 0.125, 0.125, 0.0625, 0.0625, 0.0625, 0.125, 0.125, 0.125, 0.25, 0.5, 1.

anm_run pid 98367: elapsed 12:06:59, 572.1% cpu, rss 72 MB; cap 36 h (SIGTERM at 2026-11-21 18:11:16 UTC).



### run2: arc step 9 accepted at its first attempt (2026-11-20 18:48 UTC)

| arc step | arclength a | D move | D | Delta | t_D start | t_D end | D below 259.903269724106 | corrections | accepted lam | ladder / failed / skipped | corrector s | refused attempts | first \|dz\| | first \|dz\| / a |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 (AB2) | 0.0444334 | 0.044433205 | 259.42750402623675 | 1.68347789279812 | 0.9999956072 | 0.9999956095 | 0.475766 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5367.3 | 0 | 1.96e-15 | 4.41e-14 |
| 6 | 0.0444334 | 0.044433205 | 259.47193723120494 | 1.68347117889185 | 0.9999956095 | 0.9999956118 | 0.431332 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5222.6 | 0 | 2.89e-15 | 6.5e-14 |
| 7 | 0.0138854375 | 0.013885377 | 259.48582260777852 | 1.68346908127357 | 0.9999956118 | 0.9999956126 | 0.417447 | 12 | 0.25 x2, 0.125 x3, 0.5, 1 x6 | 14 / 16 / 0 | 7284.8 | 2 | 4.76e-15 | 3.43e-13 |
| 8 | 0.0138854375 | 0.013885377 | 259.49970798436211 | 1.68346698388404 | 0.9999956126 | 0.9999956133 | 0.403562 | 9 | 0.25 x2, 0.5, 1 x6 | 11 / 7 / 0 | 4593.6 | 0 | 3.16e-15 | 2.28e-13 |
| 9 | 0.01735679688 | 0.017356721 | 259.51706470510565 | 1.68346436247007 | 0.9999956133 | 0.9999956142 | 0.386205 | 17 | 0.125 x6, 0.0625 x3, 0.25, 0.5, 1 x6 | 19 / 35 / 0 | 12934.4 | 0 | 7.03e-15 | 4.05e-13 |

Accepted steps in run2: 4. No turn recorded (anm_run's own detection of D'(s) = 0 inside an accepted step). t_D has not changed sign. t_D start of the first step of run2 0.9999956095, end of the last 0.9999956142; its change per unit arclength over the last accepted step 5.186e-08.

Step 9's accepted attempt: 33 refused trials (lam 0.125, 0.25, 0.5, 1, at corrections 0, 1, 10, 2, 3, 4, 5, 6, 7, 8, 9, 33 `projection failed` lines, trial |F| 8.63e+06 to 3.67e+09) and 1 refused strong-chord check(s), which together took 6628 s of the corrector's 12934.4 s. The series at the base took 1042.3 s (formed by the jets inside the run, which also saves its arcjet).

anm_run pid 98367: elapsed 12:36:45, 542.2% cpu, rss 181 MB; run2 started 06:11:16 UTC, 12.61 h ago; cap 36 h (SIGTERM at 2026-11-21 18:11:16 UTC).

Every attempt of every log, with the predicted max|F| (the series' residual at the re-seeded point, before any correction):

| log | attempt | D move | D of the attempt | predicted max\|F\| | first \|dz\| | first \|dz\| / predicted max\|F\| | refused trial lam at correction 0 | accepted lam at correction 0 | accepted lam x first \|dz\| | corrector steps | corrector s | outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pilot2 | 1 | 0.045500 | 259.15272808 | 8.9e-36 | 5.37e-15 | 6.03e+20 | 1, 0.5 | 0.25 | 1.34e-15 | 33 | 11228.2 | accepted |
| pilot2 | 2 | 0.056875 | 259.20960283 | 1.26e-36 | 4.6e-16 | 3.65e+20 | none | 1 | 4.6e-16 | 26 | 9721.7 | accepted |
| run1 | 1 | 0.045500 | 259.25510263 | 1.4e-36 | 6.2e-16 | 4.43e+20 | none | 1 | 6.2e-16 | 24 | 7446.4 | accepted |
| run1 | 2 | 0.056875 | 259.31197738 | 2.61e-36 | 8.92e-16 | 3.42e+20 | 1 | 0.5 | 4.46e-16 | 35 | 9788.8 | accepted |
| run1 | 3 | 0.071093 | 259.38307082 | 1.66e-36 | 8.83e-16 | 5.32e+20 | 1 | 0.5 | 4.41e-16 | 36 | 9996.8 | accepted |
| run1 | 4 | 0.088867 | 259.47193762 | 6.28e-36 | 9.21e-15 | 1.47e+21 | 1, 0.5, 0.25 | 0.125 | 1.15e-15 | 3 | 5338.2 | refused (stall rule) |
| run1 | 5 | 0.044433 | 259.42750422 | 7.16e-36 | 4.82e-15 | 6.73e+20 | 1, 0.5, 0.25, 0.125 | 0.0625 | 3.01e-16 | 8 | 11457.4 | refused (stall rule) |
| ab1 | 1 | 0.071093 | 259.38307082 | 1.66e-36 | 8.83e-16 | 5.32e+20 | 1 | 0.5 | 4.41e-16 | 7 | 2945.3 | accepted |
| ab2 | 1 | 0.044433 | 259.42750403 | 2.97e-36 | 1.96e-15 | 6.6e+20 | 1, 0.5 | 0.25 | 4.9e-16 | 10 | 5367.3 | accepted |
| run2 | 1 | 0.044433 | 259.47193723 | 2.2e-36 | 2.89e-15 | 1.31e+21 | 1, 0.5 | 0.25 | 7.23e-16 | 10 | 5222.6 | accepted |
| run2 | 2 | 0.055542 | 259.52747874 | 3.77e-36 | 8.11e-15 | 2.15e+21 | 1, 0.5, 0.25 | 0.125 | 1.01e-15 | 4 | 5716.4 | refused (stall rule) |
| run2 | 3 | 0.027771 | 259.49970798 | 1.14e-35 | 2.01e-14 | 1.76e+21 | 1, 0.5, 0.25, 0.125, 0.0625 | 0.03125 | 6.28e-16 | 2 | 3843.6 | refused (stall rule) |
| run2 | 4 | 0.013885 | 259.48582261 | 2.86e-36 | 4.76e-15 | 1.66e+21 | 1, 0.5 | 0.25 | 1.19e-15 | 13 | 7284.8 | accepted |
| run2 | 5 | 0.013885 | 259.49970798 | 1.87e-36 | 3.16e-15 | 1.69e+21 | 1, 0.5 | 0.25 | 7.9e-16 | 10 | 4593.6 | accepted |
| run2 | 6 | 0.017357 | 259.51706471 | 3.46e-36 | 7.03e-15 | 2.03e+21 | 1, 0.5, 0.25 | 0.125 | 8.79e-16 | 18 | 12934.4 | accepted |

15 attempts in 5 logs, 14 distinct points (run1's attempt 3 and ab1's attempt 1 are the same point).

1. The predicted max|F| is 1.3e-36 to 1.1e-35 for D moves of 0.0139 to 0.0889. Over this range it does not fall with a shorter step. Ordered by D move, the predicted max|F| is 2.9e-36, 1.9e-36, 3.5e-36, 1.1e-35, 3e-36, 2.2e-36, 7.2e-36, 8.9e-36, 1.4e-36, 3.8e-36, 1.3e-36, 2.6e-36, 1.7e-36, 6.3e-36 (D moves 0.0139, 0.0139, 0.0174, 0.0278, 0.0444, 0.0444, 0.0444, 0.0455, 0.0455, 0.0555, 0.0569, 0.0569, 0.0711, 0.0889).

2. First |dz| / predicted max|F| is 3.4e+20 to 6.7e+20 at the 7 points below D 259.45 and 1.3e+21 to 2.2e+21 at the 7 points above it. Ordered by D: 259.1527: 6e+20, 259.2096: 3.7e+20, 259.2551: 4.4e+20, 259.3120: 3.4e+20, 259.3831: 5.3e+20, 259.4275: 6.6e+20, 259.4275: 6.7e+20, 259.4719: 1.3e+21, 259.4719: 1.5e+21, 259.4858: 1.7e+21, 259.4997: 1.8e+21, 259.4997: 1.7e+21, 259.5171: 2e+21, 259.5275: 2.2e+21.

3. At one D move (0.0444, 3 distinct points) the predicted max|F| is 2.2e-36, 3e-36, 7.2e-36, a spread of x3.3, against x9.0 over all 14 points.

4. First |dz| runs from 4.6e-16 to 2e-14 (x44). At the 12 points where correction 0 accepts lam below 1, accepted lam times first |dz| is 3e-16 to 1.3e-15 (x4.5), and the smallest refused trial lam at correction 0 times first |dz| is 6e-16 to 2.7e-15. The two ranges overlap, so there is no sharp threshold in lam times |dz|.

5. Arc step 9 took 3.88 h from arc step 8's record (14:54:30 UTC) to its own (18:47:28 UTC). Its 1 attempt took 12934.4 s of corrector time, and the series at its base 1042.3 s. Arc step 8: 1 attempt, 4593.6 s = 4593.6 s of corrector time, series 1049.9 s.

6. The target D 259.49970798 was attempted from 2 bases: run2 attempt 3, D move 0.0278, predicted max|F| 1.14e-35, first |dz| 2.01e-14, ratio 1.76e+21, refused (stall rule); run2 attempt 5, D move 0.0139, predicted max|F| 1.87e-36, first |dz| 3.16e-15, ratio 1.69e+21, accepted. Predicted max|F| is x6.1 lower from the shorter step and the ratio differs by x1.04.

7. Spearman rank correlation between D move and predicted max|F| over the 14 distinct attempts: -0.16 (ranks, ties by order; +1 is a monotone rise with the D move, -1 a monotone fall, 0 no trend).

Step 9 was accepted at its first attempt, and a grew by `--a_grow 1.25` as the rule gives (0.0138854375 x 1.25 = 0.017356796875). It is the slowest first-attempt step so far: 3.88 h, 17 corrections, 12934.4 s of corrector time (33 refused trials took 6628 s of it), against 1.57 h and 4593.6 s for step 8. Its first |dz| 7.03e-15 is the largest of any accepted attempt. Accepted lam stayed at 0.125 (x6) and 0.0625 (x3) for the first nine corrections and never reached the stall rule's 0.04.

The target D 259.5171 adds a point to statement 2: first |dz| / predicted max|F| is 2.03e+21 there (1.7e+21 at D 259.4997, 2.2e+21 at D 259.5275). Predicted max|F| was 3.46e-36, inside the 1.3e-36 to 1.1e-35 range of statement 1. Over 14 distinct points the rank correlation of the predicted max|F| with the D move is -0.16 (statement 7).

I changed no flag. run2 is between steps now: the series at D 259.5171 is being formed (1042 to 1091 s at the last bases), then step 10's first attempt with a = 0.017356796875 x 1.25 = 0.0216959961 by the grow rule. I have not received the diagnostic command yet. t_D is 0.9999956142 and has not changed sign, no turn is recorded, and D is 0.386205 below 259.903269724106.

### run2: arc step 10 accepted at its first attempt (2026-11-20 20:31 UTC)

| arc step | arclength a | D move | D | Delta | t_D start | t_D end | D below 259.903269724106 | corrections | accepted lam | ladder / failed / skipped | corrector s | refused attempts | first \|dz\| | first \|dz\| / a |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 (AB2) | 0.0444334 | 0.044433205 | 259.42750402623675 | 1.68347789279812 | 0.9999956072 | 0.9999956095 | 0.475766 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5367.3 | 0 | 1.96e-15 | 4.41e-14 |
| 6 | 0.0444334 | 0.044433205 | 259.47193723120494 | 1.68347117889185 | 0.9999956095 | 0.9999956118 | 0.431332 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5222.6 | 0 | 2.89e-15 | 6.5e-14 |
| 7 | 0.0138854375 | 0.013885377 | 259.48582260777852 | 1.68346908127357 | 0.9999956118 | 0.9999956126 | 0.417447 | 12 | 0.25 x2, 0.125 x3, 0.5, 1 x6 | 14 / 16 / 0 | 7284.8 | 2 | 4.76e-15 | 3.43e-13 |
| 8 | 0.0138854375 | 0.013885377 | 259.49970798436211 | 1.68346698388404 | 0.9999956126 | 0.9999956133 | 0.403562 | 9 | 0.25 x2, 0.5, 1 x6 | 11 / 7 / 0 | 4593.6 | 0 | 3.16e-15 | 2.28e-13 |
| 9 | 0.01735679688 | 0.017356721 | 259.51706470510565 | 1.68346436247007 | 0.9999956133 | 0.9999956142 | 0.386205 | 17 | 0.125 x6, 0.0625 x3, 0.25, 0.5, 1 x6 | 19 / 35 / 0 | 12934.4 | 0 | 7.03e-15 | 4.05e-13 |
| 10 | 0.02169599609 | 0.021695901 | 259.53876060605705 | 1.68346108620971 | 0.9999956142 | 0.9999956153 | 0.364509 | 10 | 0.25 x3, 0.5, 1 x6 | 12 / 9 / 0 | 4961.0 | 0 | 4.65e-15 | 2.14e-13 |

Accepted steps in run2: 5. No turn recorded (anm_run's own detection of D'(s) = 0 inside an accepted step). t_D has not changed sign. t_D start of the first step of run2 0.9999956095, end of the last 0.9999956153; its change per unit arclength over the last accepted step 5.183e-08.

Step 10's accepted attempt: 7 refused trials (lam 0.5, 1, at corrections 0, 1, 2, 3, 7 `projection failed` lines, trial |F| 1.08e+07 to 3.97e+08) and 1 refused strong-chord check(s), which together took 1428 s of the corrector's 4961.0 s. The series at the base took 1277.8 s (formed by the jets inside the run, which also saves its arcjet).

anm_run pid 98367: elapsed 14:21:25, 564.6% cpu, rss 76 MB; run2 started 06:11:16 UTC, 14.36 h ago; cap 36 h (SIGTERM at 2026-11-21 18:11:16 UTC).

Every attempt of every log, with the predicted max|F| (the series' residual at the re-seeded point, before any correction):

| log | attempt | D move | D of the attempt | predicted max\|F\| | first \|dz\| | first \|dz\| / predicted max\|F\| | refused trial lam at correction 0 | accepted lam at correction 0 | accepted lam x first \|dz\| | corrector steps | corrector s | outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pilot2 | 1 | 0.045500 | 259.15272808 | 8.9e-36 | 5.37e-15 | 6.03e+20 | 1, 0.5 | 0.25 | 1.34e-15 | 33 | 11228.2 | accepted |
| pilot2 | 2 | 0.056875 | 259.20960283 | 1.26e-36 | 4.6e-16 | 3.65e+20 | none | 1 | 4.6e-16 | 26 | 9721.7 | accepted |
| run1 | 1 | 0.045500 | 259.25510263 | 1.4e-36 | 6.2e-16 | 4.43e+20 | none | 1 | 6.2e-16 | 24 | 7446.4 | accepted |
| run1 | 2 | 0.056875 | 259.31197738 | 2.61e-36 | 8.92e-16 | 3.42e+20 | 1 | 0.5 | 4.46e-16 | 35 | 9788.8 | accepted |
| run1 | 3 | 0.071093 | 259.38307082 | 1.66e-36 | 8.83e-16 | 5.32e+20 | 1 | 0.5 | 4.41e-16 | 36 | 9996.8 | accepted |
| run1 | 4 | 0.088867 | 259.47193762 | 6.28e-36 | 9.21e-15 | 1.47e+21 | 1, 0.5, 0.25 | 0.125 | 1.15e-15 | 3 | 5338.2 | refused (stall rule) |
| run1 | 5 | 0.044433 | 259.42750422 | 7.16e-36 | 4.82e-15 | 6.73e+20 | 1, 0.5, 0.25, 0.125 | 0.0625 | 3.01e-16 | 8 | 11457.4 | refused (stall rule) |
| ab1 | 1 | 0.071093 | 259.38307082 | 1.66e-36 | 8.83e-16 | 5.32e+20 | 1 | 0.5 | 4.41e-16 | 7 | 2945.3 | accepted |
| ab2 | 1 | 0.044433 | 259.42750403 | 2.97e-36 | 1.96e-15 | 6.6e+20 | 1, 0.5 | 0.25 | 4.9e-16 | 10 | 5367.3 | accepted |
| run2 | 1 | 0.044433 | 259.47193723 | 2.2e-36 | 2.89e-15 | 1.31e+21 | 1, 0.5 | 0.25 | 7.23e-16 | 10 | 5222.6 | accepted |
| run2 | 2 | 0.055542 | 259.52747874 | 3.77e-36 | 8.11e-15 | 2.15e+21 | 1, 0.5, 0.25 | 0.125 | 1.01e-15 | 4 | 5716.4 | refused (stall rule) |
| run2 | 3 | 0.027771 | 259.49970798 | 1.14e-35 | 2.01e-14 | 1.76e+21 | 1, 0.5, 0.25, 0.125, 0.0625 | 0.03125 | 6.28e-16 | 2 | 3843.6 | refused (stall rule) |
| run2 | 4 | 0.013885 | 259.48582261 | 2.86e-36 | 4.76e-15 | 1.66e+21 | 1, 0.5 | 0.25 | 1.19e-15 | 13 | 7284.8 | accepted |
| run2 | 5 | 0.013885 | 259.49970798 | 1.87e-36 | 3.16e-15 | 1.69e+21 | 1, 0.5 | 0.25 | 7.9e-16 | 10 | 4593.6 | accepted |
| run2 | 6 | 0.017357 | 259.51706471 | 3.46e-36 | 7.03e-15 | 2.03e+21 | 1, 0.5, 0.25 | 0.125 | 8.79e-16 | 18 | 12934.4 | accepted |
| run2 | 7 | 0.021696 | 259.53876061 | 1.75e-36 | 4.65e-15 | 2.66e+21 | 1, 0.5 | 0.25 | 1.16e-15 | 11 | 4961.0 | accepted |

16 attempts in 5 logs, 15 distinct points (run1's attempt 3 and ab1's attempt 1 are the same point).

1. The predicted max|F| is 1.3e-36 to 1.1e-35 for D moves of 0.0139 to 0.0889. Over this range it does not fall with a shorter step. Ordered by D move, the predicted max|F| is 2.9e-36, 1.9e-36, 3.5e-36, 1.7e-36, 1.1e-35, 3e-36, 2.2e-36, 7.2e-36, 8.9e-36, 1.4e-36, 3.8e-36, 1.3e-36, 2.6e-36, 1.7e-36, 6.3e-36 (D moves 0.0139, 0.0139, 0.0174, 0.0217, 0.0278, 0.0444, 0.0444, 0.0444, 0.0455, 0.0455, 0.0555, 0.0569, 0.0569, 0.0711, 0.0889).

2. First |dz| / predicted max|F| is 3.4e+20 to 6.7e+20 at the 7 points below D 259.45 and 1.3e+21 to 2.7e+21 at the 8 points above it. Ordered by D: 259.1527: 6e+20, 259.2096: 3.7e+20, 259.2551: 4.4e+20, 259.3120: 3.4e+20, 259.3831: 5.3e+20, 259.4275: 6.6e+20, 259.4275: 6.7e+20, 259.4719: 1.3e+21, 259.4719: 1.5e+21, 259.4858: 1.7e+21, 259.4997: 1.8e+21, 259.4997: 1.7e+21, 259.5171: 2e+21, 259.5275: 2.2e+21, 259.5388: 2.7e+21.

3. At one D move (0.0444, 3 distinct points) the predicted max|F| is 2.2e-36, 3e-36, 7.2e-36, a spread of x3.3, against x9.0 over all 15 points.

4. First |dz| runs from 4.6e-16 to 2e-14 (x44). At the 13 points where correction 0 accepts lam below 1, accepted lam times first |dz| is 3e-16 to 1.3e-15 (x4.5), and the smallest refused trial lam at correction 0 times first |dz| is 6e-16 to 2.7e-15. The two ranges overlap, so there is no sharp threshold in lam times |dz|.

5. Arc step 10 took 1.73 h from arc step 9's record (18:47:28 UTC) to its own (20:31:29 UTC). Its 1 attempt took 4961.0 s of corrector time, and the series at its base 1277.8 s. Arc step 9: 1 attempt, 12934.4 s = 12934.4 s of corrector time, series 1042.3 s.

6. The target D 259.49970798 was attempted from 2 bases: run2 attempt 3, D move 0.0278, predicted max|F| 1.14e-35, first |dz| 2.01e-14, ratio 1.76e+21, refused (stall rule); run2 attempt 5, D move 0.0139, predicted max|F| 1.87e-36, first |dz| 3.16e-15, ratio 1.69e+21, accepted. Predicted max|F| is x6.1 lower from the shorter step and the ratio differs by x1.04.

7. Spearman rank correlation between D move and predicted max|F| over the 15 distinct attempts: -0.10 (ranks, ties by order; +1 is a monotone rise with the D move, -1 a monotone fall, 0 no trend).

Step 10 was accepted at its first attempt, and a grew by `--a_grow 1.25` as the rule gives (0.017356796875 x 1.25 = 0.02169599609375). It took 1.73 h: 10 corrections (accepted lam 0.25 x3, 0.5, 1 x6) and 4961.0 s of corrector time, of which 7 refused trials and 1 refused strong-chord check took 1428 s, against 12934.4 s for step 9. Its first |dz| 4.65e-15 is below step 9's 7.03e-15 (the largest so far), because the predicted max|F| was 1.75e-36, about half of step 9's 3.46e-36.

The gain first |dz| / predicted max|F| keeps rising with the target D: 2.66e+21 at D 259.5388, against 2.03e+21 at 259.5171 and 2.2e+21 at 259.5275 (statement 2). Over 15 distinct points the rank correlation of the predicted max|F| with the D move is -0.10 (statement 7). The series at step 10's base took 1277.8 s against 1042.3 s at step 9's, and #1058's four checks (nice 19) ran beside it for its whole length, so I do not read that as a trend.

I changed no flag. Your 20:18 UTC order (#1058 comment 7049678470) moved #1058's target to main 8179068d. Its build started at 20:23 UTC beside run2 (venv-macm3-1058b, worktree choptuik-large-d-1058b, 2 jobs, nice 19, alert only), and the four checks follow. When they are as wanted, a watcher stops run2 at the next accepted step by its exact pid and restarts from that step's state on venv-macm3-1058b with the same flags. Only `--state`, `--a0` (the first-attempt length run2 would have used next), `--steps` (20 minus the accepted steps) and the output folder (`run3`) change, and the 36 h cap keeps its end (2026-11-21 18:11:16 UTC). The code worktree stays choptuik-large-d-1008 at 9980cd93, as for run2. Main 8179068d's anm_run.py, arclength.py and reseed.py differ from it (in arclength.py I read the exact_recip option, off by default, and the floor probe); tell me if you want that code instead. The next base's series is saved about 21 min after the step's record, so I do not wait for it: the restart forms it on the new kernel. `hpkernel.__file__` goes into exits_1008.txt at the restart.

run2 is forming the series at D 259.5388, the base of step 11, now. t_D is 0.9999956153 and has not changed sign, no turn is recorded, and D is 0.364509 below 259.903269724106.

### run2: arc step 11 accepted at its first attempt; run2 stopped, run3 started on main 8179068d (2026-11-20 22:37 UTC)

| arc step | arclength a | D move | D | Delta | t_D start | t_D end | D below 259.903269724106 | corrections | accepted lam | ladder / failed / skipped | corrector s | refused attempts | first \|dz\| | first \|dz\| / a |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 (AB2) | 0.0444334 | 0.044433205 | 259.42750402623675 | 1.68347789279812 | 0.9999956072 | 0.9999956095 | 0.475766 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5367.3 | 0 | 1.96e-15 | 4.41e-14 |
| 6 | 0.0444334 | 0.044433205 | 259.47193723120494 | 1.68347117889185 | 0.9999956095 | 0.9999956118 | 0.431332 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5222.6 | 0 | 2.89e-15 | 6.5e-14 |
| 7 | 0.0138854375 | 0.013885377 | 259.48582260777852 | 1.68346908127357 | 0.9999956118 | 0.9999956126 | 0.417447 | 12 | 0.25 x2, 0.125 x3, 0.5, 1 x6 | 14 / 16 / 0 | 7284.8 | 2 | 4.76e-15 | 3.43e-13 |
| 8 | 0.0138854375 | 0.013885377 | 259.49970798436211 | 1.68346698388404 | 0.9999956126 | 0.9999956133 | 0.403562 | 9 | 0.25 x2, 0.5, 1 x6 | 11 / 7 / 0 | 4593.6 | 0 | 3.16e-15 | 2.28e-13 |
| 9 | 0.01735679688 | 0.017356721 | 259.51706470510565 | 1.68346436247007 | 0.9999956133 | 0.9999956142 | 0.386205 | 17 | 0.125 x6, 0.0625 x3, 0.25, 0.5, 1 x6 | 19 / 35 / 0 | 12934.4 | 0 | 7.03e-15 | 4.05e-13 |
| 10 | 0.02169599609 | 0.021695901 | 259.53876060605705 | 1.68346108620971 | 0.9999956142 | 0.9999956153 | 0.364509 | 10 | 0.25 x3, 0.5, 1 x6 | 12 / 9 / 0 | 4961.0 | 0 | 4.65e-15 | 2.14e-13 |
| 11 | 0.02711999512 | 0.027119876 | 259.5658804822806 | 1.68345699168165 | 0.9999956153 | 0.9999956167 | 0.337389 | 11 | 0.25 x3, 0.125, 0.5, 1 x6 | 13 / 11 / 0 | 6357.0 | 0 | 5.76e-15 | 2.12e-13 |

Accepted steps in run2: 6. No turn recorded (anm_run's own detection of D'(s) = 0 inside an accepted step). t_D has not changed sign. t_D start of the first step of run2 0.9999956095, end of the last 0.9999956167; its change per unit arclength over the last accepted step 5.179e-08.

Step 11's accepted attempt: 10 refused trials (lam 0.25, 0.5, 1, at corrections 0, 1, 2, 3, 4, 10 `projection failed` lines, trial |F| 8.72e+06 to 5.51e+08) and 1 refused strong-chord check(s), which together took 2350 s of the corrector's 6357.0 s. The series at the base took 1149.7 s (formed by the jets inside the run, which also saves its arcjet).

anm_run pid 98367 is no longer running.  run2 exit 241 wall 59133s 2026-11-20 22:36:49 UTC

Every attempt of every log, with the predicted max|F| (the series' residual at the re-seeded point, before any correction):

| log | attempt | D move | D of the attempt | predicted max\|F\| | first \|dz\| | first \|dz\| / predicted max\|F\| | refused trial lam at correction 0 | accepted lam at correction 0 | accepted lam x first \|dz\| | corrector steps | corrector s | outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pilot2 | 1 | 0.045500 | 259.15272808 | 8.9e-36 | 5.37e-15 | 6.03e+20 | 1, 0.5 | 0.25 | 1.34e-15 | 33 | 11228.2 | accepted |
| pilot2 | 2 | 0.056875 | 259.20960283 | 1.26e-36 | 4.6e-16 | 3.65e+20 | none | 1 | 4.6e-16 | 26 | 9721.7 | accepted |
| run1 | 1 | 0.045500 | 259.25510263 | 1.4e-36 | 6.2e-16 | 4.43e+20 | none | 1 | 6.2e-16 | 24 | 7446.4 | accepted |
| run1 | 2 | 0.056875 | 259.31197738 | 2.61e-36 | 8.92e-16 | 3.42e+20 | 1 | 0.5 | 4.46e-16 | 35 | 9788.8 | accepted |
| run1 | 3 | 0.071093 | 259.38307082 | 1.66e-36 | 8.83e-16 | 5.32e+20 | 1 | 0.5 | 4.41e-16 | 36 | 9996.8 | accepted |
| run1 | 4 | 0.088867 | 259.47193762 | 6.28e-36 | 9.21e-15 | 1.47e+21 | 1, 0.5, 0.25 | 0.125 | 1.15e-15 | 3 | 5338.2 | refused (stall rule) |
| run1 | 5 | 0.044433 | 259.42750422 | 7.16e-36 | 4.82e-15 | 6.73e+20 | 1, 0.5, 0.25, 0.125 | 0.0625 | 3.01e-16 | 8 | 11457.4 | refused (stall rule) |
| ab1 | 1 | 0.071093 | 259.38307082 | 1.66e-36 | 8.83e-16 | 5.32e+20 | 1 | 0.5 | 4.41e-16 | 7 | 2945.3 | accepted |
| ab2 | 1 | 0.044433 | 259.42750403 | 2.97e-36 | 1.96e-15 | 6.6e+20 | 1, 0.5 | 0.25 | 4.9e-16 | 10 | 5367.3 | accepted |
| run2 | 1 | 0.044433 | 259.47193723 | 2.2e-36 | 2.89e-15 | 1.31e+21 | 1, 0.5 | 0.25 | 7.23e-16 | 10 | 5222.6 | accepted |
| run2 | 2 | 0.055542 | 259.52747874 | 3.77e-36 | 8.11e-15 | 2.15e+21 | 1, 0.5, 0.25 | 0.125 | 1.01e-15 | 4 | 5716.4 | refused (stall rule) |
| run2 | 3 | 0.027771 | 259.49970798 | 1.14e-35 | 2.01e-14 | 1.76e+21 | 1, 0.5, 0.25, 0.125, 0.0625 | 0.03125 | 6.28e-16 | 2 | 3843.6 | refused (stall rule) |
| run2 | 4 | 0.013885 | 259.48582261 | 2.86e-36 | 4.76e-15 | 1.66e+21 | 1, 0.5 | 0.25 | 1.19e-15 | 13 | 7284.8 | accepted |
| run2 | 5 | 0.013885 | 259.49970798 | 1.87e-36 | 3.16e-15 | 1.69e+21 | 1, 0.5 | 0.25 | 7.9e-16 | 10 | 4593.6 | accepted |
| run2 | 6 | 0.017357 | 259.51706471 | 3.46e-36 | 7.03e-15 | 2.03e+21 | 1, 0.5, 0.25 | 0.125 | 8.79e-16 | 18 | 12934.4 | accepted |
| run2 | 7 | 0.021696 | 259.53876061 | 1.75e-36 | 4.65e-15 | 2.66e+21 | 1, 0.5 | 0.25 | 1.16e-15 | 11 | 4961.0 | accepted |
| run2 | 8 | 0.027120 | 259.56588048 | 1.73e-36 | 5.76e-15 | 3.33e+21 | 1, 0.5 | 0.25 | 1.44e-15 | 12 | 6357.0 | accepted |

17 attempts in 5 logs, 16 distinct points (run1's attempt 3 and ab1's attempt 1 are the same point).

1. The predicted max|F| is 1.3e-36 to 1.1e-35 for D moves of 0.0139 to 0.0889. Over this range it does not fall with a shorter step. Ordered by D move, the predicted max|F| is 2.9e-36, 1.9e-36, 3.5e-36, 1.7e-36, 1.7e-36, 1.1e-35, 3e-36, 2.2e-36, 7.2e-36, 8.9e-36, 1.4e-36, 3.8e-36, 1.3e-36, 2.6e-36, 1.7e-36, 6.3e-36 (D moves 0.0139, 0.0139, 0.0174, 0.0217, 0.0271, 0.0278, 0.0444, 0.0444, 0.0444, 0.0455, 0.0455, 0.0555, 0.0569, 0.0569, 0.0711, 0.0889).

2. First |dz| / predicted max|F| is 3.4e+20 to 6.7e+20 at the 7 points below D 259.45 and 1.3e+21 to 3.3e+21 at the 9 points above it. Ordered by D: 259.1527: 6e+20, 259.2096: 3.7e+20, 259.2551: 4.4e+20, 259.3120: 3.4e+20, 259.3831: 5.3e+20, 259.4275: 6.6e+20, 259.4275: 6.7e+20, 259.4719: 1.3e+21, 259.4719: 1.5e+21, 259.4858: 1.7e+21, 259.4997: 1.8e+21, 259.4997: 1.7e+21, 259.5171: 2e+21, 259.5275: 2.2e+21, 259.5388: 2.7e+21, 259.5659: 3.3e+21.

3. At one D move (0.0444, 3 distinct points) the predicted max|F| is 2.2e-36, 3e-36, 7.2e-36, a spread of x3.3, against x9.0 over all 16 points.

4. First |dz| runs from 4.6e-16 to 2e-14 (x44). At the 14 points where correction 0 accepts lam below 1, accepted lam times first |dz| is 3e-16 to 1.4e-15 (x4.8), and the smallest refused trial lam at correction 0 times first |dz| is 6e-16 to 2.9e-15. The two ranges overlap, so there is no sharp threshold in lam times |dz|.

5. Arc step 11 took 2.09 h from arc step 10's record (20:31:29 UTC) to its own (22:36:37 UTC). Its 1 attempt took 6357.0 s of corrector time, and the series at its base 1149.7 s. Arc step 10: 1 attempt, 4961.0 s = 4961.0 s of corrector time, series 1277.8 s.

6. The target D 259.49970798 was attempted from 2 bases: run2 attempt 3, D move 0.0278, predicted max|F| 1.14e-35, first |dz| 2.01e-14, ratio 1.76e+21, refused (stall rule); run2 attempt 5, D move 0.0139, predicted max|F| 1.87e-36, first |dz| 3.16e-15, ratio 1.69e+21, accepted. Predicted max|F| is x6.1 lower from the shorter step and the ratio differs by x1.04.

7. Spearman rank correlation between D move and predicted max|F| over the 16 distinct attempts: -0.06 (ranks, ties by order; +1 is a monotone rise with the D move, -1 a monotone fall, 0 no trend).

Step 11 was accepted at its first attempt, and a grew by `--a_grow 1.25` as the rule gives (0.02169599609375 x 1.25 = 0.0271199951171875). It took 2.09 h: 11 corrections (accepted lam 0.25 x3, 0.125, 0.5, 1 x6) and 6357.0 s of corrector time, of which 10 refused trials and 1 refused strong-chord check took 2350 s, against 4961.0 s for step 10. Its first |dz| 5.76e-15 and its predicted max|F| 1.73e-36 are both within the range of the earlier steps. The gain first |dz| / predicted max|F| rises again with the target D: 3.33e+21 at D 259.5659, against 2.66e+21 at 259.5388 (statement 2). The series at step 11's base took 1149.7 s.

t_D is 0.9999956167 at the end of step 11 and has not changed sign, no turn is recorded, and D is 0.337389 below 259.903269724106.

**run2 stopped and run3 started, as ordered.** #1058's four checks at main 8179068d are as wanted (comment 7051018848), so the restart watcher stopped run2 at this step boundary: SIGTERM by the exact pid 98367 at 22:36:40 UTC, 3 s after the step's record (22:36:37 UTC), exit at 22:36:49 UTC after 59133 s (16.43 h; capped_run's `cap_hit False`, rc -15). run3 started at 22:36:54 UTC from run2's state `arc_006_D259.565880.npz` (arc step 11's end, the same base run2 would have formed its series at next).

| | run2 (arc steps 6 to 11) | run3 (from arc step 12) |
|---|---|---|
| code worktree | `choptuik-large-d-1008` at 9980cd93 | `choptuik-large-d-1008b` at 8179068d |
| venv | `venv-macm3-main` | `venv-macm3-1058b` |
| `hpkernel.__file__` | `/Users/nathan/Source/venv-macm3-main/lib/python3.14/site-packages/hpkernel/__init__.py` | `/Users/nathan/Source/venv-macm3-1058b/lib/python3.14/site-packages/hpkernel/__init__.py` |
| `_hpkernel` .so sha1 (first 12) | baaf3435bca7 | 6d8213c28d71 |
| multidouble Python package | 0.1.0, commit a93e0896 | 5.1.0, commit 8c4360ac |
| ISA (hpkernel, multidouble) | neon, neon | neon, neon |
| Python | 3.14.3 | 3.14.3 |

The flags are the same: `run_restart.sh`'s F and ARC strings have the same md5 as `run_ab.sh`'s (268b00e0 and 5b67f35c, before `--a0`), and `ps` shows run3's anm_run with them. Only `--state`, `--steps` (14 = 20 minus the 6 accepted), `--a0` (0.033899993896484376 = 0.0271199951171875 x 1.25, the first-attempt length run2 would have used next) and the output folder (`run3`) differ, and `--elim_switch 0` stays. No `--arc_jet`: run3 forms the series at D 259.5659 itself on the new kernel. The cap is 70475 s from run3's start, so it ends at about 18:11:30 UTC on 2026-11-21, within 14 s of run2's 18:11:16.

The turn stop watcher and the wake watcher are re-armed on run3. run3's `arc.jsonl` starts at step 0, so run3's step i is arc step 12 + i.

### run3, arc step 12: attempt 1 at the arclength step a 0.0338999939 refused by the stall rule after 2 corrections, accepted lam 0.03125, 0.015625 (2026-11-20 23:24 UTC)

Arc step 12 is not accepted yet. Its attempt 1 (a = 0.02711999512 x 1.25 = 0.0338999939, D move 0.033899845, checked: D move / a = 0.99999562 against t_D 0.99999562) from arc step 11's D 259.5658804822806 to D 259.599780327614 refused by the stall rule: on 1: lam at or below 0.04 twice in a row, stopping (stalled). The corrector line says 1744.4 s; its corrections took 1447 s (1272 s of trials and chord checks). The stall rule (`--lam_stall 0.04`) and `--qd_it 40` are as in run1; the stop watcher stays armed and anm_run goes on to the next attempt with a halved.

Per trial (every refused trial's ladder failed: the point |F| is the one before projection, and the trial |F| after the failed projection is the same point):

| correction | trial lam | projection | \|F\| before projection | trial max\|F\| (after) | simplified correction / \|dz\| (bound) | result | seconds |
|---|---|---|---|---|---|---|---|
| 0 | strong chord | not logged | not logged | | theta inf (bound 0.75) | refused | 97.71 |
| 0 | 1 | attempted, ladder failed | 1.50e+12 | 1.50e+12 | 1.027e+56 (0.750) | refused | 94.34 |
| 0 | 0.5 | attempted, ladder failed | 9.38e+10 | 9.38e+10 | 6.420e+54 (0.875) | refused | 94.59 |
| 0 | 0.25 | attempted, ladder failed | 5.89e+09 | 5.89e+09 | 4.013e+53 (0.938) | refused | 93.7 |
| 0 | 0.125 | attempted, ladder failed | 3.75e+08 | 3.75e+08 | 2.508e+52 (0.969) | refused | 90.26 |
| 0 | 0.0625 | attempted, ladder failed | 2.51e+07 | 2.51e+07 | 1.567e+51 (0.984) | refused | 66.92 |
| 0 | 0.03125 | projected, ladder converged | not logged | 2.97e-29 | 9.681e-01 (0.992) | accepted | 98.87 |
| 1 | 1 | attempted, ladder failed | 1.85e+12 | 1.85e+12 | 9.687e+55 (0.750) | refused | 92.75 |
| 1 | 0.5 | attempted, ladder failed | 1.16e+11 | 1.16e+11 | 6.076e+54 (0.875) | refused | 94.32 |
| 1 | 0.25 | attempted, ladder failed | 7.42e+09 | 7.42e+09 | 3.866e+53 (0.938) | refused | 94.15 |
| 1 | 0.125 | attempted, ladder failed | 5.04e+08 | 5.04e+08 | 2.610e+52 (0.969) | refused | 94.41 |
| 1 | 0.0625 | attempted, ladder failed | 4.32e+07 | 4.32e+07 | 2.202e+51 (0.984) | refused | 91.59 |
| 1 | 0.03125 | attempted, ladder failed | 1.07e+07 | 1.07e+07 | 3.515e+50 (0.992) | refused | 70.42 |
| 1 | 0.015625 | projected, ladder converged | not logged | 3.72e-29 | 9.841e-01 (0.996) | accepted | 98.29 |

Per correction:

| correction | accepted lam | max\|F\| before -> after | \|dz\| before -> after | seconds |
|---|---|---|---|---|
| 0 | 0.03125 | 1.17e-35 -> 2.97e-29 | 4.83e-14 -> 4.58e-14 | 723.95 |
| 1 | 0.015625 | 2.97e-29 -> 3.72e-29 | 4.58e-14 -> 4.45e-14 | 723.36 |

First |dz| of every attempt against the arclength step a (D rises down the table; run1's last two are the refused attempts of arc step 5; AB1, AB2, run2 and run3 ran with `--elim_switch 0`; run3 is on main 8179068d and the new kernel):

| run | arclength a | first \|dz\| | first \|dz\| / a | accepted lam at correction 0 |
|---|---|---|---|---|
| pilot2 | 0.0455 | 5.37e-15 | 1.18e-13 | 0.25 |
| pilot2 | 0.056875 | 4.60e-16 | 8.09e-15 | 1 |
| run1 | 0.0455 | 6.20e-16 | 1.36e-14 | 1 |
| run1 | 0.056875 | 8.92e-16 | 1.57e-14 | 0.5 |
| run1 | 0.07109375 | 8.83e-16 | 1.24e-14 | 0.5 |
| run1 | 0.0888671875 | 9.21e-15 | 1.04e-13 | 0.125 |
| run1 | 0.04443359375 | 4.82e-15 | 1.08e-13 | 0.0625 |
| ab1 | 0.07109375 | 8.83e-16 | 1.24e-14 | 0.5 |
| ab2 | 0.0444334 | 1.96e-15 | 4.41e-14 | 0.25 |
| run2 | 0.0444334 | 2.89e-15 | 6.5e-14 | 0.25 |
| run2 | 0.05554175 | 8.11e-15 | 1.46e-13 | 0.125 |
| run2 | 0.027770875 | 2.01e-14 | 7.24e-13 | 0.03125 |
| run2 | 0.0138854375 | 4.76e-15 | 3.43e-13 | 0.25 |
| run2 | 0.0138854375 | 3.16e-15 | 2.28e-13 | 0.25 |
| run2 | 0.01735679688 | 7.03e-15 | 4.05e-13 | 0.125 |
| run2 | 0.02169599609 | 4.65e-15 | 2.14e-13 | 0.25 |
| run2 | 0.02711999512 | 5.76e-15 | 2.12e-13 | 0.25 |
| run3 | 0.0338999939 | 4.83e-14 | 1.42e-12 | 0.03125 |

Next: anm_run's attempt 2 halves a to 0.01694999695 (D move 0.016949923); `--a_grow 1.25` and the halving allow up to 4 attempts per step, so up to 3 more. The series at arc step 11's D is in `run3/arcjet_000_D259.565880.npz` if a restart with another `--a0` is wanted (`--arc_jet` reads it, saving the 274.4 s of forming it); I have not changed anything.

anm_run pid 54500: elapsed 47:44, 597.2% cpu, rss 339 MB; D 0.337389 below 259.903269724106 at arc step 11's D.

Gain first |dz| / predicted max|F| of this attempt: 4.83e-14 / 1.17e-35 = 4.13e+21 at D 259.59978, against 3.33e+21 at D 259.5659 and 2.66e+21 at 259.5388 (the accepted steps 11 and 10 of run2). Its first |dz| is x2.4 the largest of the 17 earlier attempts (2.01e-14, run2).

Kernel: the series at this base (D 259.56588) took 274.4 s on the new kernel (run3), against 1149.7 s at arc step 11's base and 1277.8 s at arc step 10's on the old one (run2), x4.2 and x4.7; the old figures include hours when #1058's builds and checks ran beside run2, no #1058 job ran beside run3. The 11 refused trials of over 5 s here took 89 s on average against 200 s for the 102 in run2 (the base D and the trial points differ, so this is not a like-for-like timing).

### run3, arc step 12: attempt 2 at the arclength step a 0.01694999695 refused by the stall rule after 2 corrections, accepted lam 0.03125, 0.03125 (2026-11-20 23:51 UTC)

Arc step 12 is not accepted yet. Its attempt 2 (a = 0.02711999512 x 1.25 / 2 = 0.01694999695, D move 0.016949923, checked: D move / a = 0.99999562 against t_D 0.99999562) from arc step 11's D 259.5658804822806 to D 259.58283040494 refused by the stall rule: on 1: lam at or below 0.04 twice in a row, stopping (stalled). The corrector line says 1680.9 s; its corrections took 1381 s (1205 s of trials and chord checks). The stall rule (`--lam_stall 0.04`) and `--qd_it 40` are as in run1; the stop watcher stays armed and anm_run goes on to the next attempt with a halved.

Per trial (every refused trial's ladder failed: the point |F| is the one before projection, and the trial |F| after the failed projection is the same point):

| correction | trial lam | projection | \|F\| before projection | trial max\|F\| (after) | simplified correction / \|dz\| (bound) | result | seconds |
|---|---|---|---|---|---|---|---|
| 0 | strong chord | not logged | not logged | | theta inf (bound 0.75) | refused | 98.28 |
| 0 | 1 | attempted, ladder failed | 5.38e+11 | 5.38e+11 | 5.273e+55 (0.750) | refused | 93.7 |
| 0 | 0.5 | attempted, ladder failed | 3.37e+10 | 3.37e+10 | 3.296e+54 (0.875) | refused | 94.48 |
| 0 | 0.25 | attempted, ladder failed | 2.12e+09 | 2.12e+09 | 2.060e+53 (0.938) | refused | 94.52 |
| 0 | 0.125 | attempted, ladder failed | 1.37e+08 | 1.37e+08 | 1.287e+52 (0.969) | refused | 85.79 |
| 0 | 0.0625 | attempted, ladder failed | 1.21e+07 | 1.21e+07 | 8.046e+50 (0.984) | refused | 94.4 |
| 0 | 0.03125 | projected, ladder converged | not logged | 1.61e-29 | 9.685e-01 (0.992) | accepted | 98.8 |
| 1 | 1 | attempted, ladder failed | 5.32e+11 | 5.32e+11 | 4.531e+55 (0.750) | refused | 93.6 |
| 1 | 0.5 | attempted, ladder failed | 3.34e+10 | 3.34e+10 | 2.844e+54 (0.875) | refused | 94.13 |
| 1 | 0.25 | attempted, ladder failed | 2.14e+09 | 2.14e+09 | 1.814e+53 (0.938) | refused | 94.9 |
| 1 | 0.125 | attempted, ladder failed | 1.49e+08 | 1.49e+08 | 1.238e+52 (0.969) | refused | 94.48 |
| 1 | 0.0625 | attempted, ladder failed | 1.54e+07 | 1.54e+07 | 1.080e+51 (0.984) | refused | 69.18 |
| 1 | 0.03125 | projected, ladder converged | not logged | 3.19e-29 | 9.682e-01 (0.992) | accepted | 98.26 |

Per correction:

| correction | accepted lam | max\|F\| before -> after | \|dz\| before -> after | seconds |
|---|---|---|---|---|
| 0 | 0.03125 | 9.49e-36 -> 1.61e-29 | 3.43e-14 -> 3.29e-14 | 748.02 |
| 1 | 0.03125 | 1.61e-29 -> 3.19e-29 | 3.29e-14 -> 3.14e-14 | 633.1 |

First |dz| of every attempt against the arclength step a (D rises down the table; run1's last two are the refused attempts of arc step 5; AB1, AB2, run2 and run3 ran with `--elim_switch 0`; run3 is on main 8179068d and the new kernel):

| run | arclength a | first \|dz\| | first \|dz\| / a | accepted lam at correction 0 |
|---|---|---|---|---|
| pilot2 | 0.0455 | 5.37e-15 | 1.18e-13 | 0.25 |
| pilot2 | 0.056875 | 4.60e-16 | 8.09e-15 | 1 |
| run1 | 0.0455 | 6.20e-16 | 1.36e-14 | 1 |
| run1 | 0.056875 | 8.92e-16 | 1.57e-14 | 0.5 |
| run1 | 0.07109375 | 8.83e-16 | 1.24e-14 | 0.5 |
| run1 | 0.0888671875 | 9.21e-15 | 1.04e-13 | 0.125 |
| run1 | 0.04443359375 | 4.82e-15 | 1.08e-13 | 0.0625 |
| ab1 | 0.07109375 | 8.83e-16 | 1.24e-14 | 0.5 |
| ab2 | 0.0444334 | 1.96e-15 | 4.41e-14 | 0.25 |
| run2 | 0.0444334 | 2.89e-15 | 6.5e-14 | 0.25 |
| run2 | 0.05554175 | 8.11e-15 | 1.46e-13 | 0.125 |
| run2 | 0.027770875 | 2.01e-14 | 7.24e-13 | 0.03125 |
| run2 | 0.0138854375 | 4.76e-15 | 3.43e-13 | 0.25 |
| run2 | 0.0138854375 | 3.16e-15 | 2.28e-13 | 0.25 |
| run2 | 0.01735679688 | 7.03e-15 | 4.05e-13 | 0.125 |
| run2 | 0.02169599609 | 4.65e-15 | 2.14e-13 | 0.25 |
| run2 | 0.02711999512 | 5.76e-15 | 2.12e-13 | 0.25 |
| run3 | 0.0338999939 | 4.83e-14 | 1.42e-12 | 0.03125 |
| run3 | 0.01694999695 | 3.43e-14 | 2.02e-12 | 0.03125 |

Next: anm_run's attempt 3 halves a to 0.008474998474 (D move 0.0084749613); `--a_grow 1.25` and the halving allow up to 4 attempts per step, so up to 2 more. First |dz| went from 4.83e-14 at a = 0.0338999939 to 3.43e-14 at a = 0.01694999695: a factor 0.71 for an a ratio of 0.5, so first |dz| / a went from 1.42e-12 to 2.02e-12. A first |dz| proportional to a (run1's two refused attempts of arc step 5 gave 9.21e-15 at a 0.0888671875 and 4.82e-15 at a 0.04443359375) would have fallen to 2.41e-14. Same base, same series, same re-seed code; the predicted max|F| is 9.49e-36 here against 1.17e-35 for the longer step. The series at arc step 11's D is in `run3/arcjet_000_D259.565880.npz` if a restart with another `--a0` is wanted (`--arc_jet` reads it, saving the 274.4 s of forming it); I have not changed anything.

anm_run pid 54500: elapsed 01:14:45, 549.0% cpu, rss 312 MB; D 0.337389 below 259.903269724106 at arc step 11's D.

Attempts from one base (a: predicted max|F|, first |dz|, outcome), for every arc step with more than one attempt: arc step 7: 0.055542: 3.77e-36, 8.11e-15, refused, 0.027771: 1.14e-35, 2.01e-14, refused, 0.013885: 2.86e-36, 4.76e-15, accepted; arc step 12: 0.0339: 1.17e-35, 4.83e-14, refused, 0.01695: 9.49e-36, 3.43e-14, refused. Over the same base, the predicted max|F| does not follow a in run2 either.

Gain first |dz| / predicted max|F| of this attempt: 3.43e-14 / 9.49e-36 = 3.61e+21 at D 259.58283, against 3.33e+21 at D 259.5659 and 2.66e+21 at 259.5388 (the accepted steps 11 and 10 of run2). Its first |dz| is x0.7 the largest of the 18 earlier attempts (4.83e-14, run3).

Kernel: the series at this base (D 259.56588) took 274.4 s on the new kernel (run3), against 1149.7 s at arc step 11's base and 1277.8 s at arc step 10's on the old one (run2), x4.2 and x4.7; the old figures include hours when #1058's builds and checks ran beside run2, no #1058 job ran beside run3. The 10 refused trials of over 5 s here took 91 s on average against 200 s for the 102 in run2 (the base D and the trial points differ, so this is not a like-for-like timing).

### run3, arc step 12: attempt 3 at the arclength step a 0.008474998474 refused by the stall rule after 5 corrections, accepted lam 0.0625, 0.0625, 0.0625, 0.03125, 0.03125 (2026-11-21 00:44 UTC)

Arc step 12 is not accepted yet. Its attempt 3 (a = 0.02711999512 x 1.25 / 4 = 0.008474998474, D move 0.0084749613, checked: D move / a = 0.99999562 against t_D 0.99999562) from arc step 11's D 259.5658804822806 to D 259.574355443608 refused by the stall rule: on 4: lam at or below 0.04 twice in a row, stopping (stalled). The corrector line says 3216.5 s; its corrections took 2916 s (2473 s of trials and chord checks). The stall rule (`--lam_stall 0.04`) and `--qd_it 40` are as in run1; the stop watcher stays armed and anm_run goes on to the next attempt with a halved.

Per trial (every refused trial's ladder failed: the point |F| is the one before projection, and the trial |F| after the failed projection is the same point):

| correction | trial lam | projection | \|F\| before projection | trial max\|F\| (after) | simplified correction / \|dz\| (bound) | result | seconds |
|---|---|---|---|---|---|---|---|
| 0 | strong chord | not logged | not logged | | theta inf (bound 0.75) | refused | 98.84 |
| 0 | 1 | attempted, ladder failed | 2.41e+10 | 2.41e+10 | 5.215e+54 (0.750) | refused | 99.01 |
| 0 | 0.5 | attempted, ladder failed | 1.52e+09 | 1.52e+09 | 3.259e+53 (0.875) | refused | 113.22 |
| 0 | 0.25 | attempted, ladder failed | 9.84e+07 | 9.84e+07 | 2.037e+52 (0.938) | refused | 66.67 |
| 0 | 0.125 | attempted, ladder failed | 1.02e+07 | 1.02e+07 | 1.273e+51 (0.969) | refused | 92.67 |
| 0 | 0.0625 | projected, ladder converged | not logged | 1.34e-29 | 9.371e-01 (0.984) | accepted | 102.73 |
| 1 | 1 | attempted, ladder failed | 2.03e+10 | 2.03e+10 | 4.067e+54 (0.750) | refused | 94.19 |
| 1 | 0.5 | attempted, ladder failed | 1.30e+09 | 1.30e+09 | 2.587e+53 (0.875) | refused | 95.43 |
| 1 | 0.25 | attempted, ladder failed | 9.15e+07 | 9.15e+07 | 1.763e+52 (0.938) | refused | 63.96 |
| 1 | 0.125 | attempted, ladder failed | 1.19e+07 | 1.19e+07 | 1.554e+51 (0.969) | refused | 67.96 |
| 1 | 0.0625 | projected, ladder converged | not logged | 2.52e-29 | 9.368e-01 (0.984) | accepted | 99.65 |
| 2 | 1 | attempted, ladder failed | 1.70e+10 | 1.70e+10 | 3.333e+54 (0.750) | refused | 93.73 |
| 2 | 0.5 | attempted, ladder failed | 1.11e+09 | 1.11e+09 | 2.158e+53 (0.875) | refused | 93.59 |
| 2 | 0.25 | attempted, ladder failed | 8.40e+07 | 8.40e+07 | 1.596e+52 (0.938) | refused | 87.9 |
| 2 | 0.125 | attempted, ladder failed | 1.32e+07 | 1.32e+07 | 1.844e+51 (0.969) | refused | 71.42 |
| 2 | 0.0625 | projected, ladder converged | not logged | 3.50e-29 | 9.365e-01 (0.984) | accepted | 97.09 |
| 3 | 1 | attempted, ladder failed | 1.37e+10 | 1.37e+10 | 2.792e+54 (0.750) | refused | 94.22 |
| 3 | 0.5 | attempted, ladder failed | 9.11e+08 | 9.11e+08 | 1.839e+53 (0.875) | refused | 95.2 |
| 3 | 0.25 | attempted, ladder failed | 7.42e+07 | 7.42e+07 | 1.469e+52 (0.938) | refused | 91.52 |
| 3 | 0.125 | attempted, ladder failed | 1.39e+07 | 1.39e+07 | 2.120e+51 (0.969) | refused | 64.28 |
| 3 | 0.0625 | attempted, ladder failed | 8.32e+06 | 8.32e+06 | 8.027e+50 (0.984) | refused | 70.6 |
| 3 | 0.03125 | projected, ladder converged | not logged | 3.64e-29 | 9.686e-01 (0.992) | accepted | 97.46 |
| 4 | 1 | attempted, ladder failed | 1.19e+10 | 1.19e+10 | 2.505e+54 (0.750) | refused | 94.33 |
| 4 | 0.5 | attempted, ladder failed | 7.94e+08 | 7.94e+08 | 1.660e+53 (0.875) | refused | 95.62 |
| 4 | 0.25 | attempted, ladder failed | 6.65e+07 | 6.65e+07 | 1.360e+52 (0.938) | refused | 93.76 |
| 4 | 0.125 | attempted, ladder failed | 1.37e+07 | 1.37e+07 | 2.093e+51 (0.969) | refused | 68.36 |
| 4 | 0.0625 | attempted, ladder failed | 8.44e+06 | 8.44e+06 | 8.487e+50 (0.984) | refused | 72.65 |
| 4 | 0.03125 | projected, ladder converged | not logged | 3.76e-29 | 9.686e-01 (0.992) | accepted | 97.26 |

Per correction:

| correction | accepted lam | max\|F\| before -> after | \|dz\| before -> after | seconds |
|---|---|---|---|---|
| 0 | 0.0625 | 4.44e-36 -> 1.34e-29 | 1.56e-14 -> 1.46e-14 | 661.67 |
| 1 | 0.0625 | 1.34e-29 -> 2.52e-29 | 1.46e-14 -> 1.35e-14 | 509.98 |
| 2 | 0.0625 | 2.52e-29 -> 3.50e-29 | 1.35e-14 -> 1.25e-14 | 532.17 |
| 3 | 0.03125 | 3.50e-29 -> 3.64e-29 | 1.25e-14 -> 1.21e-14 | 601.81 |
| 4 | 0.03125 | 3.64e-29 -> 3.76e-29 | 1.21e-14 -> 1.16e-14 | 610.78 |

First |dz| of every attempt against the arclength step a (D rises down the table; run1's last two are the refused attempts of arc step 5; AB1, AB2, run2 and run3 ran with `--elim_switch 0`; run3 is on main 8179068d and the new kernel):

| run | arclength a | first \|dz\| | first \|dz\| / a | accepted lam at correction 0 |
|---|---|---|---|---|
| pilot2 | 0.0455 | 5.37e-15 | 1.18e-13 | 0.25 |
| pilot2 | 0.056875 | 4.60e-16 | 8.09e-15 | 1 |
| run1 | 0.0455 | 6.20e-16 | 1.36e-14 | 1 |
| run1 | 0.056875 | 8.92e-16 | 1.57e-14 | 0.5 |
| run1 | 0.07109375 | 8.83e-16 | 1.24e-14 | 0.5 |
| run1 | 0.0888671875 | 9.21e-15 | 1.04e-13 | 0.125 |
| run1 | 0.04443359375 | 4.82e-15 | 1.08e-13 | 0.0625 |
| ab1 | 0.07109375 | 8.83e-16 | 1.24e-14 | 0.5 |
| ab2 | 0.0444334 | 1.96e-15 | 4.41e-14 | 0.25 |
| run2 | 0.0444334 | 2.89e-15 | 6.5e-14 | 0.25 |
| run2 | 0.05554175 | 8.11e-15 | 1.46e-13 | 0.125 |
| run2 | 0.027770875 | 2.01e-14 | 7.24e-13 | 0.03125 |
| run2 | 0.0138854375 | 4.76e-15 | 3.43e-13 | 0.25 |
| run2 | 0.0138854375 | 3.16e-15 | 2.28e-13 | 0.25 |
| run2 | 0.01735679688 | 7.03e-15 | 4.05e-13 | 0.125 |
| run2 | 0.02169599609 | 4.65e-15 | 2.14e-13 | 0.25 |
| run2 | 0.02711999512 | 5.76e-15 | 2.12e-13 | 0.25 |
| run3 | 0.0338999939 | 4.83e-14 | 1.42e-12 | 0.03125 |
| run3 | 0.01694999695 | 3.43e-14 | 2.02e-12 | 0.03125 |
| run3 | 0.008474998474 | 1.56e-14 | 1.84e-12 | 0.0625 |

Next: anm_run's attempt 4 halves a to 0.004237499237 (D move 0.0042374807); `--a_grow 1.25` and the halving allow up to 4 attempts per step, so up to 1 more. First |dz| went from 3.43e-14 at a = 0.01694999695 to 1.56e-14 at a = 0.008474998474: a factor 0.45 for an a ratio of 0.5, so first |dz| / a went from 2.02e-12 to 1.84e-12. A first |dz| proportional to a (run1's two refused attempts of arc step 5 gave 9.21e-15 at a 0.0888671875 and 4.82e-15 at a 0.04443359375) would have fallen to 1.72e-14. Same base, same series, same re-seed code; the predicted max|F| is 4.44e-36 here against 9.49e-36 for the longer step. The series at arc step 11's D is in `run3/arcjet_000_D259.565880.npz` if a restart with another `--a0` is wanted (`--arc_jet` reads it, saving the 274.4 s of forming it); I have not changed anything.

anm_run pid 54500: elapsed 02:07:49, 563.6% cpu, rss 313 MB; D 0.337389 below 259.903269724106 at arc step 11's D.

Attempts from one base (a: predicted max|F|, first |dz|, outcome), for every arc step with more than one attempt: arc step 7: 0.055542: 3.77e-36, 8.11e-15, refused, 0.027771: 1.14e-35, 2.01e-14, refused, 0.013885: 2.86e-36, 4.76e-15, accepted; arc step 12: 0.0339: 1.17e-35, 4.83e-14, refused, 0.01695: 9.49e-36, 3.43e-14, refused, 0.008475: 4.44e-36, 1.56e-14, refused. Over the same base, the predicted max|F| does not follow a in run2 either.

Gain first |dz| / predicted max|F| of this attempt: 1.56e-14 / 4.44e-36 = 3.51e+21 at D 259.57436, against 3.33e+21 at D 259.5659 and 2.66e+21 at 259.5388 (the accepted steps 11 and 10 of run2). Its first |dz| is x0.3 the largest of the 19 earlier attempts (4.83e-14, run3).

Kernel: the series at this base (D 259.56588) took 274.4 s on the new kernel (run3), against 1149.7 s at arc step 11's base and 1277.8 s at arc step 10's on the old one (run2), x4.2 and x4.7; the old figures include hours when #1058's builds and checks ran beside run2, no #1058 job ran beside run3. The 22 refused trials of over 5 s here took 85 s on average against 200 s for the 102 in run2 (the base D and the trial points differ, so this is not a like-for-like timing).

### run3: arc step 12 accepted at its fourth attempt (2026-11-21 02:08 UTC)

| arc step | arclength a | D move | D | Delta | t_D start | t_D end | D below 259.903269724106 | corrections | accepted lam | ladder / failed / skipped | corrector s | refused attempts | first \|dz\| | first \|dz\| / a |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 (AB2) | 0.0444334 | 0.044433205 | 259.42750402623675 | 1.68347789279812 | 0.9999956072 | 0.9999956095 | 0.475766 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5367.3 | 0 | 1.96e-15 | 4.41e-14 |
| 6 | 0.0444334 | 0.044433205 | 259.47193723120494 | 1.68347117889185 | 0.9999956095 | 0.9999956118 | 0.431332 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5222.6 | 0 | 2.89e-15 | 6.5e-14 |
| 7 | 0.0138854375 | 0.013885377 | 259.48582260777852 | 1.68346908127357 | 0.9999956118 | 0.9999956126 | 0.417447 | 12 | 0.25 x2, 0.125 x3, 0.5, 1 x6 | 14 / 16 / 0 | 7284.8 | 2 | 4.76e-15 | 3.43e-13 |
| 8 | 0.0138854375 | 0.013885377 | 259.49970798436211 | 1.68346698388404 | 0.9999956126 | 0.9999956133 | 0.403562 | 9 | 0.25 x2, 0.5, 1 x6 | 11 / 7 / 0 | 4593.6 | 0 | 3.16e-15 | 2.28e-13 |
| 9 | 0.01735679688 | 0.017356721 | 259.51706470510565 | 1.68346436247007 | 0.9999956133 | 0.9999956142 | 0.386205 | 17 | 0.125 x6, 0.0625 x3, 0.25, 0.5, 1 x6 | 19 / 35 / 0 | 12934.4 | 0 | 7.03e-15 | 4.05e-13 |
| 10 | 0.02169599609 | 0.021695901 | 259.53876060605705 | 1.68346108620971 | 0.9999956142 | 0.9999956153 | 0.364509 | 10 | 0.25 x3, 0.5, 1 x6 | 12 / 9 / 0 | 4961.0 | 0 | 4.65e-15 | 2.14e-13 |
| 11 | 0.02711999512 | 0.027119876 | 259.5658804822806 | 1.68345699168165 | 0.9999956153 | 0.9999956167 | 0.337389 | 11 | 0.25 x3, 0.125, 0.5, 1 x6 | 13 / 11 / 0 | 6357.0 | 0 | 5.76e-15 | 2.12e-13 |
| 12 | 0.004237499237 | 0.0042374807 | 259.57011796294397 | 1.68345635199211 | 0.9999956167 | 0.9999956169 | 0.333152 | 15 | 0.125 x6, 0.25 x2, 0.5, 1 x6 | 17 / 24 / 0 | 4937.4 | 3 | 8.73e-15 | 2.06e-12 |

Accepted steps in run2 and run3: 7 (6 and 1). No turn recorded (anm_run's own detection of D'(s) = 0 inside an accepted step). t_D has not changed sign. t_D start of the first step of run2 0.9999956095, end of the last 0.9999956169; its change per unit arclength over the last accepted step 5.177e-08.

Step 12's accepted attempt: 23 refused trials (lam 0.25, 0.5, 1, at corrections 0, 1, 2, 3, 4, 5, 6, 7, 8, 23 `projection failed` lines, trial |F| 8.77e+06 to 2.1e+09) and 1 refused strong-chord check(s), which together took 1982 s of the corrector's 4937.4 s. The series at the base took 274.4 s (formed inside the run, which also saves its arcjet).

anm_run pid 54500 (run3): elapsed 03:31:26, 582.5% cpu, rss 1601 MB; run3 started 22:36:54 UTC, 3.52 h ago; cap 70475 s from its start (SIGTERM at 2026-11-21 18:11:29 UTC).

Every attempt of every log, with the predicted max|F| (the series' residual at the re-seeded point, before any correction):

| log | attempt | D move | D of the attempt | predicted max\|F\| | first \|dz\| | first \|dz\| / predicted max\|F\| | refused trial lam at correction 0 | accepted lam at correction 0 | accepted lam x first \|dz\| | corrector steps | corrector s | outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pilot2 | 1 | 0.045500 | 259.15272808 | 8.9e-36 | 5.37e-15 | 6.03e+20 | 1, 0.5 | 0.25 | 1.34e-15 | 33 | 11228.2 | accepted |
| pilot2 | 2 | 0.056875 | 259.20960283 | 1.26e-36 | 4.6e-16 | 3.65e+20 | none | 1 | 4.6e-16 | 26 | 9721.7 | accepted |
| run1 | 1 | 0.045500 | 259.25510263 | 1.4e-36 | 6.2e-16 | 4.43e+20 | none | 1 | 6.2e-16 | 24 | 7446.4 | accepted |
| run1 | 2 | 0.056875 | 259.31197738 | 2.61e-36 | 8.92e-16 | 3.42e+20 | 1 | 0.5 | 4.46e-16 | 35 | 9788.8 | accepted |
| run1 | 3 | 0.071093 | 259.38307082 | 1.66e-36 | 8.83e-16 | 5.32e+20 | 1 | 0.5 | 4.41e-16 | 36 | 9996.8 | accepted |
| run1 | 4 | 0.088867 | 259.47193762 | 6.28e-36 | 9.21e-15 | 1.47e+21 | 1, 0.5, 0.25 | 0.125 | 1.15e-15 | 3 | 5338.2 | refused (stall rule) |
| run1 | 5 | 0.044433 | 259.42750422 | 7.16e-36 | 4.82e-15 | 6.73e+20 | 1, 0.5, 0.25, 0.125 | 0.0625 | 3.01e-16 | 8 | 11457.4 | refused (stall rule) |
| ab1 | 1 | 0.071093 | 259.38307082 | 1.66e-36 | 8.83e-16 | 5.32e+20 | 1 | 0.5 | 4.41e-16 | 7 | 2945.3 | accepted |
| ab2 | 1 | 0.044433 | 259.42750403 | 2.97e-36 | 1.96e-15 | 6.6e+20 | 1, 0.5 | 0.25 | 4.9e-16 | 10 | 5367.3 | accepted |
| run2 | 1 | 0.044433 | 259.47193723 | 2.2e-36 | 2.89e-15 | 1.31e+21 | 1, 0.5 | 0.25 | 7.23e-16 | 10 | 5222.6 | accepted |
| run2 | 2 | 0.055542 | 259.52747874 | 3.77e-36 | 8.11e-15 | 2.15e+21 | 1, 0.5, 0.25 | 0.125 | 1.01e-15 | 4 | 5716.4 | refused (stall rule) |
| run2 | 3 | 0.027771 | 259.49970798 | 1.14e-35 | 2.01e-14 | 1.76e+21 | 1, 0.5, 0.25, 0.125, 0.0625 | 0.03125 | 6.28e-16 | 2 | 3843.6 | refused (stall rule) |
| run2 | 4 | 0.013885 | 259.48582261 | 2.86e-36 | 4.76e-15 | 1.66e+21 | 1, 0.5 | 0.25 | 1.19e-15 | 13 | 7284.8 | accepted |
| run2 | 5 | 0.013885 | 259.49970798 | 1.87e-36 | 3.16e-15 | 1.69e+21 | 1, 0.5 | 0.25 | 7.9e-16 | 10 | 4593.6 | accepted |
| run2 | 6 | 0.017357 | 259.51706471 | 3.46e-36 | 7.03e-15 | 2.03e+21 | 1, 0.5, 0.25 | 0.125 | 8.79e-16 | 18 | 12934.4 | accepted |
| run2 | 7 | 0.021696 | 259.53876061 | 1.75e-36 | 4.65e-15 | 2.66e+21 | 1, 0.5 | 0.25 | 1.16e-15 | 11 | 4961.0 | accepted |
| run2 | 8 | 0.027120 | 259.56588048 | 1.73e-36 | 5.76e-15 | 3.33e+21 | 1, 0.5 | 0.25 | 1.44e-15 | 12 | 6357.0 | accepted |
| run3 | 1 | 0.033900 | 259.59978033 | 1.17e-35 | 4.83e-14 | 4.13e+21 | 1, 0.5, 0.25, 0.125, 0.0625 | 0.03125 | 1.51e-15 | 2 | 1744.4 | refused (stall rule) |
| run3 | 2 | 0.016950 | 259.58283040 | 9.49e-36 | 3.43e-14 | 3.61e+21 | 1, 0.5, 0.25, 0.125, 0.0625 | 0.03125 | 1.07e-15 | 2 | 1680.9 | refused (stall rule) |
| run3 | 3 | 0.008475 | 259.57435544 | 4.44e-36 | 1.56e-14 | 3.51e+21 | 1, 0.5, 0.25, 0.125 | 0.0625 | 9.75e-16 | 5 | 3216.5 | refused (stall rule) |
| run3 | 4 | 0.004237 | 259.57011796 | 2.51e-36 | 8.73e-15 | 3.48e+21 | 1, 0.5, 0.25 | 0.125 | 1.09e-15 | 16 | 4937.4 | accepted |

21 attempts in 6 logs, 20 distinct points (run1's attempt 3 and ab1's attempt 1 are the same point).

1. The predicted max|F| is 1.3e-36 to 1.2e-35 for D moves of 0.0042 to 0.0889. Over this range it does not fall with a shorter step. Ordered by D move, the predicted max|F| is 2.5e-36, 4.4e-36, 2.9e-36, 1.9e-36, 9.5e-36, 3.5e-36, 1.7e-36, 1.7e-36, 1.1e-35, 1.2e-35, 3e-36, 2.2e-36, 7.2e-36, 8.9e-36, 1.4e-36, 3.8e-36, 1.3e-36, 2.6e-36, 1.7e-36, 6.3e-36 (D moves 0.0042, 0.0085, 0.0139, 0.0139, 0.0169, 0.0174, 0.0217, 0.0271, 0.0278, 0.0339, 0.0444, 0.0444, 0.0444, 0.0455, 0.0455, 0.0555, 0.0569, 0.0569, 0.0711, 0.0889).

2. First |dz| / predicted max|F| is 3.4e+20 to 6.7e+20 at the 7 points below D 259.45 and 1.3e+21 to 4.1e+21 at the 13 points above it. Ordered by D: 259.1527: 6e+20, 259.2096: 3.7e+20, 259.2551: 4.4e+20, 259.3120: 3.4e+20, 259.3831: 5.3e+20, 259.4275: 6.6e+20, 259.4275: 6.7e+20, 259.4719: 1.3e+21, 259.4719: 1.5e+21, 259.4858: 1.7e+21, 259.4997: 1.8e+21, 259.4997: 1.7e+21, 259.5171: 2e+21, 259.5275: 2.2e+21, 259.5388: 2.7e+21, 259.5659: 3.3e+21, 259.5701: 3.5e+21, 259.5744: 3.5e+21, 259.5828: 3.6e+21, 259.5998: 4.1e+21.

3. At one D move (0.0444, 3 distinct points) the predicted max|F| is 2.2e-36, 3e-36, 7.2e-36, a spread of x3.3, against x9.3 over all 20 points.

4. First |dz| runs from 4.6e-16 to 4.8e-14 (x105). At the 18 points where correction 0 accepts lam below 1, accepted lam times first |dz| is 3e-16 to 1.5e-15 (x5.0), and the smallest refused trial lam at correction 0 times first |dz| is 6e-16 to 3e-15. The two ranges overlap, so there is no sharp threshold in lam times |dz|.

5. Arc step 12 took 3.50 h from arc step 11's record (22:36:37 UTC) to its own (02:06:24 UTC). Its 4 attempts took 1744.4 + 1680.9 + 3216.5 + 4937.4 = 11579.2 s of corrector time, and the series at its base 274.4 s. Arc step 11: 1 attempt, 6357.0 s = 6357.0 s of corrector time, series 1149.7 s.

6. The target D 259.49970798 was attempted from 2 bases: run2 attempt 3, D move 0.0278, predicted max|F| 1.14e-35, first |dz| 2.01e-14, ratio 1.76e+21, refused (stall rule); run2 attempt 5, D move 0.0139, predicted max|F| 1.87e-36, first |dz| 3.16e-15, ratio 1.69e+21, accepted. Predicted max|F| is x6.1 lower from the shorter step and the ratio differs by x1.04.

7. Spearman rank correlation between D move and predicted max|F| over the 20 distinct attempts: -0.14 (ranks, ties by order; +1 is a monotone rise with the D move, -1 a monotone fall, 0 no trend).

Step 12 (run3's step 0, the first on main 8179068d and the new kernel) was accepted at its fourth attempt, after three refusals by the stall rule (`--lam_stall 0.04`). The accepted attempt is a = 0.0271199951171875 x 1.25 / 8 = 0.004237499237060547, D move 0.0042374807, D 259.57011796294397, t_D 0.9999956169 at the end. No turn is recorded, t_D has not changed sign, and D is 0.333152 below 259.903269724106.

The four attempts, from one base (D 259.5658804822806):

| attempt | a | D | predicted max\|F\| | first \|dz\| | gain first \|dz\| / predicted max\|F\| | accepted lam at correction 0 | corrections | corrector s | outcome |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.0339 | 259.59978 | 1.17e-35 | 4.83e-14 | 4.13e+21 | 0.03125 | 2 | 1744.4 | refused (stall rule) |
| 2 | 0.01695 | 259.58283 | 9.49e-36 | 3.43e-14 | 3.61e+21 | 0.03125 | 2 | 1680.9 | refused (stall rule) |
| 3 | 0.008475 | 259.57436 | 4.44e-36 | 1.56e-14 | 3.51e+21 | 0.0625 | 5 | 3216.5 | refused (stall rule) |
| 4 | 0.0042375 | 259.57012 | 2.51e-36 | 8.73e-15 | 3.48e+21 | 0.125 | 15 | 4937.4 | accepted |

At this base the predicted max|F| fell with every halving of a, by x0.81, x0.47 and x0.57, and the first |dz| fell with it (x0.71, x0.45, x0.56). Statement 1 pools twenty points from different bases and shows no fall with the D move (rank correlation -0.14, statement 7), and at arc step 7's base run2's predicted max|F| was not monotone in a (3.77e-36, 1.14e-35, 2.86e-36 for a 0.0555, 0.0278, 0.0139). The gain keeps rising with D (3.48e+21 at D 259.5701, 3.33e+21 at 259.5659, 2.66e+21 at 259.5388). The attempt that was accepted took lam x first |dz| = 1.09e-15 at correction 0, inside the range of statement 4. The three refused attempts took 6641.8 s of corrector time and the accepted one 4937.4 s, of which 23 refused trials and 1 refused strong-chord check took 1982 s; the series at the base took 274.4 s on the new kernel.

Next attempt: with `--a_hold 1` an accepted step that needed a refusal sets a_prev = a / 1.25, so the next first attempt is a_prev x 1.25 = 0.004237499237060547 again; I will check it against the next attempt's D move when its log line prints. At that a the 0.333152 to 259.903269724106 is 78.6 steps. The 13 steps that remain of `--steps 14`, each accepted at its first attempt with `--a_grow 1.25`, would cover at most 0.2914 (a from 0.0042375 to 0.0771), to D 259.8615 and 0.0418 short of 259.903269724106. The cap leaves 16.06 h, which at the accepted attempt's 4937.4 s plus the series's 274.4 s per step is 11.1 steps, and at step 11's 6357.0 s plus 274.4 s is 8.7. I changed no flag and restarted nothing.

Open question for you, not started: the predicted max|F| at this base (1.17e-35 at a 0.0339) is 6.8 times that of the previous step's accepted attempt (1.73e-36 at a 0.0271) for a 1.25 times longer step, and it is the first step after the kernel change. #1058's four checks say the new kernel gives the same bits as the old one on the stored references. To tell the base from the kernel, I could form the series at `run2/arc_006_D259.565880.npz` on `venv-macm3-main` (the old kernel, code 9980cd93) and compare it with run3's `arcjet_000_D259.565880.npz` bit for bit. Run2's series took 1042.3 to 1277.8 s at steps 9 to 11, so it would run for about 20 min beside run3, at nice 19, and slow it; I run nothing beside run3 without your word.

### run3: arc step 13 accepted at its first attempt (2026-11-21 02:50 UTC)

| arc step | arclength a | D move | D | Delta | t_D start | t_D end | D below 259.903269724106 | corrections | accepted lam | ladder / failed / skipped | corrector s | refused attempts | first \|dz\| | first \|dz\| / a |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 (AB2) | 0.0444334 | 0.044433205 | 259.42750402623675 | 1.68347789279812 | 0.9999956072 | 0.9999956095 | 0.475766 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5367.3 | 0 | 1.96e-15 | 4.41e-14 |
| 6 | 0.0444334 | 0.044433205 | 259.47193723120494 | 1.68347117889185 | 0.9999956095 | 0.9999956118 | 0.431332 | 9 | 0.25 x3, 0.5, 1 x5 | 11 / 9 / 0 | 5222.6 | 0 | 2.89e-15 | 6.5e-14 |
| 7 | 0.0138854375 | 0.013885377 | 259.48582260777852 | 1.68346908127357 | 0.9999956118 | 0.9999956126 | 0.417447 | 12 | 0.25 x2, 0.125 x3, 0.5, 1 x6 | 14 / 16 / 0 | 7284.8 | 2 | 4.76e-15 | 3.43e-13 |
| 8 | 0.0138854375 | 0.013885377 | 259.49970798436211 | 1.68346698388404 | 0.9999956126 | 0.9999956133 | 0.403562 | 9 | 0.25 x2, 0.5, 1 x6 | 11 / 7 / 0 | 4593.6 | 0 | 3.16e-15 | 2.28e-13 |
| 9 | 0.01735679688 | 0.017356721 | 259.51706470510565 | 1.68346436247007 | 0.9999956133 | 0.9999956142 | 0.386205 | 17 | 0.125 x6, 0.0625 x3, 0.25, 0.5, 1 x6 | 19 / 35 / 0 | 12934.4 | 0 | 7.03e-15 | 4.05e-13 |
| 10 | 0.02169599609 | 0.021695901 | 259.53876060605705 | 1.68346108620971 | 0.9999956142 | 0.9999956153 | 0.364509 | 10 | 0.25 x3, 0.5, 1 x6 | 12 / 9 / 0 | 4961.0 | 0 | 4.65e-15 | 2.14e-13 |
| 11 | 0.02711999512 | 0.027119876 | 259.5658804822806 | 1.68345699168165 | 0.9999956153 | 0.9999956167 | 0.337389 | 11 | 0.25 x3, 0.125, 0.5, 1 x6 | 13 / 11 / 0 | 6357.0 | 0 | 5.76e-15 | 2.12e-13 |
| 12 | 0.004237499237 | 0.0042374807 | 259.57011796294397 | 1.68345635199211 | 0.9999956167 | 0.9999956169 | 0.333152 | 15 | 0.125 x6, 0.25 x2, 0.5, 1 x6 | 17 / 24 / 0 | 4937.4 | 3 | 8.73e-15 | 2.06e-12 |
| 13 | 0.004237499237 | 0.0042374807 | 259.57435544360826 | 1.68345571232439 | 0.9999956169 | 0.9999956172 | 0.328914 | 4 | 1 x4 | 10 / 0 / 0 | 2239.4 | 0 | 9.50e-16 | 2.24e-13 |

Accepted steps in run2 and run3: 8 (6 and 2). No turn recorded (anm_run's own detection of D'(s) = 0 inside an accepted step). t_D has not changed sign. t_D start of the first step of run2 0.9999956095, end of the last 0.9999956172; its change per unit arclength over the last accepted step 5.176e-08.

Step 13's accepted attempt: no refused trials, 0 refused strong-chord check(s), 0 `projection failed` lines; the corrector took 2239.4 s. The series at the base took 289.8 s (formed inside the run, which also saves its arcjet).

anm_run pid 54500 (run3): elapsed 04:12:59, 413.7% cpu, rss 375 MB; run3 started 22:36:54 UTC, 4.22 h ago; cap 70475 s from its start (SIGTERM at 2026-11-21 18:11:29 UTC).

Every attempt of every log, with the predicted max|F| (the series' residual at the re-seeded point, before any correction):

| log | attempt | D move | D of the attempt | predicted max\|F\| | first \|dz\| | first \|dz\| / predicted max\|F\| | refused trial lam at correction 0 | accepted lam at correction 0 | accepted lam x first \|dz\| | corrector steps | corrector s | outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pilot2 | 1 | 0.045500 | 259.15272808 | 8.9e-36 | 5.37e-15 | 6.03e+20 | 1, 0.5 | 0.25 | 1.34e-15 | 33 | 11228.2 | accepted |
| pilot2 | 2 | 0.056875 | 259.20960283 | 1.26e-36 | 4.6e-16 | 3.65e+20 | none | 1 | 4.6e-16 | 26 | 9721.7 | accepted |
| run1 | 1 | 0.045500 | 259.25510263 | 1.4e-36 | 6.2e-16 | 4.43e+20 | none | 1 | 6.2e-16 | 24 | 7446.4 | accepted |
| run1 | 2 | 0.056875 | 259.31197738 | 2.61e-36 | 8.92e-16 | 3.42e+20 | 1 | 0.5 | 4.46e-16 | 35 | 9788.8 | accepted |
| run1 | 3 | 0.071093 | 259.38307082 | 1.66e-36 | 8.83e-16 | 5.32e+20 | 1 | 0.5 | 4.41e-16 | 36 | 9996.8 | accepted |
| run1 | 4 | 0.088867 | 259.47193762 | 6.28e-36 | 9.21e-15 | 1.47e+21 | 1, 0.5, 0.25 | 0.125 | 1.15e-15 | 3 | 5338.2 | refused (stall rule) |
| run1 | 5 | 0.044433 | 259.42750422 | 7.16e-36 | 4.82e-15 | 6.73e+20 | 1, 0.5, 0.25, 0.125 | 0.0625 | 3.01e-16 | 8 | 11457.4 | refused (stall rule) |
| ab1 | 1 | 0.071093 | 259.38307082 | 1.66e-36 | 8.83e-16 | 5.32e+20 | 1 | 0.5 | 4.41e-16 | 7 | 2945.3 | accepted |
| ab2 | 1 | 0.044433 | 259.42750403 | 2.97e-36 | 1.96e-15 | 6.6e+20 | 1, 0.5 | 0.25 | 4.9e-16 | 10 | 5367.3 | accepted |
| run2 | 1 | 0.044433 | 259.47193723 | 2.2e-36 | 2.89e-15 | 1.31e+21 | 1, 0.5 | 0.25 | 7.23e-16 | 10 | 5222.6 | accepted |
| run2 | 2 | 0.055542 | 259.52747874 | 3.77e-36 | 8.11e-15 | 2.15e+21 | 1, 0.5, 0.25 | 0.125 | 1.01e-15 | 4 | 5716.4 | refused (stall rule) |
| run2 | 3 | 0.027771 | 259.49970798 | 1.14e-35 | 2.01e-14 | 1.76e+21 | 1, 0.5, 0.25, 0.125, 0.0625 | 0.03125 | 6.28e-16 | 2 | 3843.6 | refused (stall rule) |
| run2 | 4 | 0.013885 | 259.48582261 | 2.86e-36 | 4.76e-15 | 1.66e+21 | 1, 0.5 | 0.25 | 1.19e-15 | 13 | 7284.8 | accepted |
| run2 | 5 | 0.013885 | 259.49970798 | 1.87e-36 | 3.16e-15 | 1.69e+21 | 1, 0.5 | 0.25 | 7.9e-16 | 10 | 4593.6 | accepted |
| run2 | 6 | 0.017357 | 259.51706471 | 3.46e-36 | 7.03e-15 | 2.03e+21 | 1, 0.5, 0.25 | 0.125 | 8.79e-16 | 18 | 12934.4 | accepted |
| run2 | 7 | 0.021696 | 259.53876061 | 1.75e-36 | 4.65e-15 | 2.66e+21 | 1, 0.5 | 0.25 | 1.16e-15 | 11 | 4961.0 | accepted |
| run2 | 8 | 0.027120 | 259.56588048 | 1.73e-36 | 5.76e-15 | 3.33e+21 | 1, 0.5 | 0.25 | 1.44e-15 | 12 | 6357.0 | accepted |
| run3 | 1 | 0.033900 | 259.59978033 | 1.17e-35 | 4.83e-14 | 4.13e+21 | 1, 0.5, 0.25, 0.125, 0.0625 | 0.03125 | 1.51e-15 | 2 | 1744.4 | refused (stall rule) |
| run3 | 2 | 0.016950 | 259.58283040 | 9.49e-36 | 3.43e-14 | 3.61e+21 | 1, 0.5, 0.25, 0.125, 0.0625 | 0.03125 | 1.07e-15 | 2 | 1680.9 | refused (stall rule) |
| run3 | 3 | 0.008475 | 259.57435544 | 4.44e-36 | 1.56e-14 | 3.51e+21 | 1, 0.5, 0.25, 0.125 | 0.0625 | 9.75e-16 | 5 | 3216.5 | refused (stall rule) |
| run3 | 4 | 0.004237 | 259.57011796 | 2.51e-36 | 8.73e-15 | 3.48e+21 | 1, 0.5, 0.25 | 0.125 | 1.09e-15 | 16 | 4937.4 | accepted |
| run3 | 5 | 0.004237 | 259.57435544 | 1.03e-36 | 9.5e-16 | 9.22e+20 | none | 1 | 9.5e-16 | 5 | 2239.4 | accepted |

22 attempts in 6 logs, 21 distinct points (run1's attempt 3 and ab1's attempt 1 are the same point).

1. The predicted max|F| is 1e-36 to 1.2e-35 for D moves of 0.0042 to 0.0889. Over this range it does not fall with a shorter step. Ordered by D move, the predicted max|F| is 2.5e-36, 1e-36, 4.4e-36, 2.9e-36, 1.9e-36, 9.5e-36, 3.5e-36, 1.7e-36, 1.7e-36, 1.1e-35, 1.2e-35, 3e-36, 2.2e-36, 7.2e-36, 8.9e-36, 1.4e-36, 3.8e-36, 1.3e-36, 2.6e-36, 1.7e-36, 6.3e-36 (D moves 0.0042, 0.0042, 0.0085, 0.0139, 0.0139, 0.0169, 0.0174, 0.0217, 0.0271, 0.0278, 0.0339, 0.0444, 0.0444, 0.0444, 0.0455, 0.0455, 0.0555, 0.0569, 0.0569, 0.0711, 0.0889).

2. First |dz| / predicted max|F| is 3.4e+20 to 6.7e+20 at the 7 points below D 259.45 and 9.2e+20 to 4.1e+21 at the 14 points above it. Ordered by D: 259.1527: 6e+20, 259.2096: 3.7e+20, 259.2551: 4.4e+20, 259.3120: 3.4e+20, 259.3831: 5.3e+20, 259.4275: 6.6e+20, 259.4275: 6.7e+20, 259.4719: 1.3e+21, 259.4719: 1.5e+21, 259.4858: 1.7e+21, 259.4997: 1.8e+21, 259.4997: 1.7e+21, 259.5171: 2e+21, 259.5275: 2.2e+21, 259.5388: 2.7e+21, 259.5659: 3.3e+21, 259.5701: 3.5e+21, 259.5744: 3.5e+21, 259.5744: 9.2e+20, 259.5828: 3.6e+21, 259.5998: 4.1e+21.

3. At one D move (0.0444, 3 distinct points) the predicted max|F| is 2.2e-36, 3e-36, 7.2e-36, a spread of x3.3, against x11.4 over all 21 points.

4. First |dz| runs from 4.6e-16 to 4.8e-14 (x105). At the 18 points where correction 0 accepts lam below 1, accepted lam times first |dz| is 3e-16 to 1.5e-15 (x5.0), and the smallest refused trial lam at correction 0 times first |dz| is 6e-16 to 3e-15. The two ranges overlap, so there is no sharp threshold in lam times |dz|.

5. Arc step 13 took 0.70 h from arc step 12's record (02:06:24 UTC) to its own (02:48:34 UTC). Its 1 attempt took 2239.4 s of corrector time, and the series at its base 289.8 s. Arc step 12: 4 attempts, 1744.4 + 1680.9 + 3216.5 + 4937.4 = 11579.2 s of corrector time, series 274.4 s.

6. The target D 259.49970798 was attempted from 2 bases: run2 attempt 3, D move 0.0278, predicted max|F| 1.14e-35, first |dz| 2.01e-14, ratio 1.76e+21, refused (stall rule); run2 attempt 5, D move 0.0139, predicted max|F| 1.87e-36, first |dz| 3.16e-15, ratio 1.69e+21, accepted. Predicted max|F| is x6.1 lower from the shorter step and the ratio differs by x1.04.

6. The target D 259.57435544 was attempted from 2 bases: run3 attempt 3, D move 0.0085, predicted max|F| 4.44e-36, first |dz| 1.56e-14, ratio 3.51e+21, refused (stall rule); run3 attempt 5, D move 0.0042, predicted max|F| 1.03e-36, first |dz| 9.5e-16, ratio 9.22e+20, accepted. Predicted max|F| is x4.3 lower from the shorter step and the ratio differs by x3.81.

7. Spearman rank correlation between D move and predicted max|F| over the 21 distinct attempts: +0.01 (ranks, ties by order; +1 is a monotone rise with the D move, -1 a monotone fall, 0 no trend).

Step 13 (run3's step 1) was accepted at its first attempt, with a = 0.004237499237060547, the value the `--a_hold 1` rule gave (a_prev = a / 1.25 after step 12's fourth attempt, so a_prev x 1.25 = a); its D move 0.0042374807 equals step 12's. It took 0.70 h: 4 corrections, all accepted at lam 1, and 2239.4 s of corrector time, against 4937.4 s for step 12's accepted attempt. D is 259.57435544360826, t_D is 0.9999956172 at the end, no turn is recorded, t_D has not changed sign, and D is 0.328914 below 259.903269724106.

The first |dz| is 9.50e-16 and the predicted max|F| 1.03e-36, so the gain first |dz| / predicted max|F| is 9.22e+20. The same target D 259.5744 was attempted twice, from two bases:

| attempt | base | a | predicted max\|F\| | first \|dz\| | gain | accepted lam at correction 0 | outcome |
|---|---|---|---|---|---|---|---|
| step 12, attempt 3 | arc_006 (D 259.5659, run2's state, reloaded and polished by run3) | 0.008475 | 4.44e-36 | 1.56e-14 | 3.51e+21 | 0.0625 | refused (stall rule) |
| step 13, attempt 1 | arc_001 (D 259.5701, run3's own accepted point) | 0.0042375 | 1.03e-36 | 9.50e-16 | 9.22e+20 | 1 | accepted |

From arc_001 the first |dz| is x0.061 and the predicted max|F| x0.23 of what they were from arc_006 for the same target, and at the same a (0.0042375, step 12's accepted attempt, target D 259.5701) x0.11 and x0.41. So the gain is not a function of the target D alone: statement 2's rise with D compares points from different bases, and the one pair at one D shows x0.26 here. Every attempt from arc_006 has been hard (4 attempts, 3 refused, 15 corrections for the accepted one); the one attempt so far from a base that run3 made itself is easy. I do not know the cause. The series check on `venv-macm3-main` at arc_006 (code 9980cd93, nice 19, started 02:11:23 UTC, in the base polish at 02:48 UTC) will say whether the kernel differs at that base.

Next attempt: a_prev x 1.25 = 0.004237499237060547 x 1.25 = 0.005296874046325684 (D move 0.0052968508), which I will check against the next attempt's D move when its log line prints. At that a the 0.328914 to 259.903269724106 is 77.6 steps; the 12 steps that remain of `--steps 14` could cover 0.2871 at most (to D 259.8615) if each is accepted at its first attempt with growth. The cap leaves 15.37 h. I changed no flag and restarted nothing; run3 goes on to its cap as ordered.

### Series check: run3's first base on the old kernel, equal (2026-11-21 03:26 UTC)

Result: **equal.** The series at `run2/arc_006_D259.565880.npz` (D 259.565880482281, N 24) formed by the old code and kernel is bit for bit the series run3 formed on main 8179068d and the new kernel. There is no part-wise relative difference to report: it is 0 at every order.

| | old (the check) | new (run3) |
|---|---|---|
| code | `choptuik-large-d-1008` at 9980cd93 | `choptuik-large-d-1008b` at 8179068d |
| kernel | `venv-macm3-main`, `_hpkernel` .so sha1 baaf3435bca7 | `venv-macm3-1058b`, 6d8213c28d71 |
| series path | the jets (this hpkernel has no `Solver.series_o`) | `series_o` |
| priority | nice 19, beside run3 | nice 10, alone |
| series seconds | 1825.8 | 274.4 |
| arcjet file | `chk_old/arcjet_000_D259.565880.npz` | `run3/arcjet_000_D259.565880.npz` |

What was compared (`compare_arcjet.py`): the eight parts z0 to z7 of the series, each 25 orders x 769 elements, as 64-bit patterns. 0 of 19225 elements differ in each part, 153800 doubles in all. The meta fields present in both files (D_str, N, jet, norms, parts, pivots) are identical. The only difference is a key: run3's file has `exact_recip: 0`, which the new code adds. The base polish before the series also agrees line for line apart from the times: strong chord theta 6.454e-34, max|F| 8.84e-38 -> 4.68e-71 in 2 steps, Delta moved -3.97e-39, pivots 2.3e-30..1.4e+37, |w_1| 3.260e-04, |w_N| 6.313e-24.

How it ran: `chk_series_old.sh` is run3's command with the output folder `chk_old` and `--steps 1` (a token diff against run3's `ps` line shows only those two differences), `--threads 6`, no `--arc_jet`. It started at 02:11:23 UTC, formed the series (about 02:54:35 to 03:25:01 UTC), and `chk_series_watch.py` stopped it by the exact pid 70031 once the series line printed. No attempt started (0 `attempt at D` lines). Run3 went on beside it unchanged: step 13 was accepted at 02:48:34 UTC, 0.70 h after step 12.

The script's first verdict was NOT EQUAL with an empty per-order table, because it counted the extra `exact_recip` key as a difference. I changed it to compare the keys both files have and to list the others; the first output is kept as `chk_old_compare_first.txt`. Its controls: identical input gives EQUAL, and one planted ulp in part 3 at order 17 is found (part-wise relative difference 1.131e-16, order 17, part 3, 1 of 25 orders).

So the kernel's series does not explain the hard attempts from arc_006. The old build's log shows what else it lacks: `Solver.residual_sub` and `Solver.jacobian_sub` (the re-seed's ladder takes the full residual and Jacobian), `Solver.newton_o_residual` (PinnedO), and the octo-tangent Jacobian. The re-seed, the predicted max|F| and the corrector all run after the series, so attempt 1 at arc_006 (predicted max|F| 1.17e-35, first |dz| 4.83e-14 at a 0.0339) is not compared yet.

Next check, not started: the old code with `--arc_jet run3/arcjet_000_D259.565880.npz` (the series is equal, so it is skipped), nice 19, stopped at the first attempt's predicted max|F| and first |dz|, to see whether 1.17e-35 and 4.83e-14 reproduce. The base polish alone took about 43 min beside run3, so it would take about 1.5 to 2 h. I run it when you say so.
