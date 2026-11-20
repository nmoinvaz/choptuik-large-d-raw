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

