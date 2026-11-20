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
