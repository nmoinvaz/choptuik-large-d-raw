# I752-mac: the crawl of the full system's a = 1 step from D 117 to 118, rebuilt and probed

Machine mac (the coordinator's Apple M5 Mac, an hc agent, mac752), issue https://github.com/nmoinvaz/choptuik-large-d/issues/752
(recommended by #742, raw `I742-win/` c5ec16fb). Worktree `choptuik-large-d-752`, branch `wip/i752` from main d71aa59d,
venv-314 (Python 3.14), `OPENBLAS_NUM_THREADS=1`, nice 10, 4 threads. The kernel is venv-314's installed build of
2026-11-09, from before #523 (the freeze projector rounded), because #742 ran on such a build (next section).

## The kernel #742 ran on (2026-11-14 09:10 UTC)

The first try of run R used the build of main 3c35f0c (multishoot 1.2.2, multidouble 4.2.1, the exact freeze projector
of #523; `hp/src` and `hp/Cargo.toml` are the same at main d71aa59d and at #742's 5249c432). Its base polish took a
Newton step (`logs/R_try1_site2.log`: start max|F| 2.01e-34, |dz| 4.07e-13), where #742's N and M converged at step 0
(1.75e-64). `base_resid.py` evaluates the stored `I742-win/L/anm_pin13_D117.0000.npz` (the state itself and its
projection, switch 0):

| kernel | max\|F\| of the state | its largest blocks | the projection's displacement | log |
|---|---|---|---|---|
| main 3c35f0c's build (exact projector) | 2.012e-34 | 5p (the horizon block's p rows) 2.0e-34, then 0c 1.75e-64 | 0 | `logs/base_resid_site2.log` |
| venv-314's build of 2026-11-09 (before #523) | 1.751e-64 | 0c 1.75e-64, 0m 4.6e-65 | 0 | `logs/base_resid_venv314.log` |
| win, #742 (N.log, M.log) | 1.75e-64 | | | |

Every block except 5p agrees between the two builds to all printed digits. So #742's states solve the equations of a
build with the rounded freeze projector, and under main's build they are 2.0e-34 off in the frozen p rows of the
horizon block. Run R therefore uses the pre-#523 build. This is reported to the coordinator, not resolved here.

## Plan, written before the runs (2026-11-14 09:40 UTC)

**Code** (`hp/crawl_probe.py` on wip/i752): `anm` runs `anm_run.main` itself on #742's arguments, with every
`ElimO.newton_o` call of an attempt recorded and `newton_od` capped at `--stop + 1` steps. It saves each attempt's iterate
at Newton step `--stop` with its step, as `ElimO.newton_o` returned them, and the attempt's pieces (plan, held offset,
re-seeder options, ElimO's switch), and then reports the attempt not converged, so `anm_run` halves a and runs the next
attempt from the same base and series. `probe` rebuilds the attempt from those pieces (`build_saved`). Its `--own 1`
splits the default test's trial corrections into the projection's displacement P(zt) - zt and the Newton step from
P(zt). `logcmp` compares the rebuilt log with #742's, timings and step numbers dropped.

**Run R** (`anm`, `--stop 1 --attempts 2`): from `I742-win/L/anm_pin13_D117.0000.npz` with #742's flags (`run_742.py`:
`--kfreeze 13 --N 24 --eps 1e-14 --D_max 400 --corrector od --tol_od 1e-60 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2
--reseed_q 1 --reseed_o 3 --save_pred 1 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --elim_switch 0`, `--h_max 1.0 --a0 1.0`,
the default own test). Attempt 0 is L's crawling a = 1 attempt (D 117 to 118), attempt 1 is M's first attempt (a = 1/2,
D 117 to 117.5, converged at lam 1 every step), the control. Each runs to Newton step 2 and saves its iterate at step 1.

**Checks of the rebuild, fixed before the run** (each can fail):

1. The planted check: `crawl_probe.py selftest` passes and each of its six mutations fails (`logs/selftest.log`).
2. The rebuilt predictions equal #742's stored ones bit for bit: `pred_pin13_D118.0000.npz` against L's (equal to N's)
   and `pred_pin13_D117.5000.npz` against M's.
3. The rebuilt log's lines equal #742's (`logcmp`, every printed digit): the base polish against N.log, the series line
   against L.log, attempt 0 (re-seed, step 0, the refused lam 1 trial of step 1 with raw |dz_t| 2.977e-15, step 1 at
   lam 0.5) against L.log, attempt 1 (re-seed, steps 0 and 1) against M.log. logcmp's control (`--mutate digit`) must
   fail (`logs/logcmp_control.log`).
4. The saved iterate's max|F| and |dz| equal `newton_od`'s records of that step, and `probe` forms the step at the
   iterate again bit for bit.

**Probe** at each saved iterate, arms U (never projected), E (ElimO as the attempt ran it, switch 0) and P (always
projected): `locate_jump` on the ladder lam 0.5 to 1 (6 rungs), K = 1e3. With switch 0 arms E and P are the same
residual, which is itself a check (they must agree). Then the natural test's ratio at lam 1 and 1/2, and the own test's
trial corrections at lam 1 and 1/2 split into displacement and step, by unknown group, with their share in the four
weakest directions of the Jacobian at the projected point.

**Acceptance (the issue's)**: (a) the iterate and step are saved, and arm E is affine (no jump past K) along lam in the
control; (b) in the crawling case either lam* and the rows carrying 99% of its jump are found, or the residual is affine
to the last rung (the fault is then in the acceptance test); (c) the result is set against #700's mechanism (ElimO's
switch, which `--elim_switch 0` removes).

**Expectation, not a criterion**: arm E affine to lam = 1 in both, since L's lam 1 trial's own max|F| was 1.39e-28;
the own test's correction at lam 1 is then not the residual's, and its split names what it is.

## The rebuild, run R (pre-#523 build; 2026-11-14 09:10 to 09:50 UTC)

`logs/R.log`, the iterates `R/crawl_iter_D118.0000_s1.npz` (the crawl) and `R/crawl_iter_D117.5000_s1.npz` (the
control), the rebuilt predictions `R/pred_pin13_D*.npz`. Checks (`logs/checks_R.log`):

| check | result | control |
|---|---|---|
| 1. planted check of `locate_jump` (`logs/selftest.log`) | PASS | shift, comp, smooth, control, coarse, hint_trust each FAIL |
| 2. predictions against #742's, every part (`cmp_pred.py`) | D 118 equal bit for bit to L's and N's, D 117.5 to M's | one ulp moved: FAIL |
| 3a. base polish against N.log | 4 of 4 lines equal (converged at step 0, 1.75e-64) | |
| 3b. series line against L.log | equal | |
| 3c. a = 1 attempt against L.log | 4 of 4 equal: step 0 1.49e-29 -> 1.39e-15, the refused lam 1 trial (1.39e-28, raw \|dz_t\| 2.977e-15 vs 1.683e-15), step 1 at lam 0.5 | one digit changed: FAIL |
| 3d. a = 1/2 attempt against M.log | 3 of 3 equal: steps 0 and 1 at lam 1 | |
| 4. saved iterate against newton_od's records; the step formed again by probe | equal; bit for bit (both iterates) | |

## The probe at the two iterates (pre-#523 build)

`logs/probe_L.log` (crawl, 1324 s), `logs/probe_M.log` (control, 681 s), records `probe/crawl_probe_D*.jsonl`.

### Along lam (`locate_jump`, rungs 0.5 to 1)

| | crawl (a = 1, D 118, step 1) | control (a = 1/2, D 117.5, step 1) |
|---|---|---|
| \|dz\| | 1.683e-15 | 3.846e-16 |
| arm E (the corrector's residual, switch 0) at lam 0 | 1.388e-15 | 3.171e-16 |
| arm E: e(lam) / lam² on the six rungs | 1.393e-28 at every rung (4 digits) | 6.123e-28 at every rung (4 digits) |
| arm E at lam 1 | 1.393e-28 | 6.123e-28 |
| arm E verdict | affine to lam = 1 | affine to lam = 1 |
| arm P (always projected) | equal to arm E at every rung | (not run: equal to E under switch 0) |
| arm U (never projected) at lam 0 | 1.425e-05 | 2.551e-06 |
| arm U: e at lam 0.5, at lam 1 | 9.6e-11, 6.6e-19 | 3.1e-12, 2.8e-20 |
| arm U verdict | affine to lam = 1 (growth at most 0.67) | affine to lam = 1 (growth at most 0.67) |

The corrector's residual along the step is the affine model plus its quadratic remainder, c lam² with c constant to
four digits on every rung, in both. `locate_jump`'s floor (1e-12 max|F0|, 1.4e-27 in the crawl) lies above that
remainder, so its growth (0.10 in the crawl) reads the floor; the c lam² fit is the finer statement. No jump exists
at any rung: at lam 1 the residual is 1.39e-28, 1e13 below the iterate's.

### The tests at lam 1 and 1/2

| | crawl | control |
|---|---|---|
| natural test at lam 1 (ratio, bound 0.75) | 5.85e-05, accepted | 9.37e-04, accepted |
| natural test at lam 1/2 (bound 0.875) | 0.5000 | 0.5000 |
| own test at lam 1: the trial's own correction | 2.9769e-15, refused (\|dz\| 1.6831e-15) | 2.6229e-17, accepted (\|dz\| 3.8464e-16) |
| its projection's displacement P(zt) - zt | 4.96e-33 | 2.10e-34 |
| its step from P(zt) | 2.9769e-15, in p1 (then n0p, n0m 3.6e-16) | 2.6229e-17, in p1 (then n0p, n0m 3.4e-18) |
| its share in the four weakest directions at P(zt) | 1.000 | 1.000 |
| those directions' singular values at P(zt) | 8.27e-25, 8.27e-25, 4.91e-28, 4.91e-28 | 8.64e-25, 8.64e-25, 5.21e-28, 5.21e-28 |
| own test at lam 1/2 | 8.4157e-16, accepted | 1.9231e-16, accepted |
| weakest singular values at P(z), the iterate | 2.64e-21, 2.60e-21, 1.12e-21, 5.05e-22 | 5.63e-22, 5.56e-22, 2.42e-22, 1.09e-22 |
| at P(z + dz/2) | 1.26e-21, 1.24e-21, 5.62e-22, 2.53e-22 | 2.83e-22, 2.79e-22, 1.21e-22, 5.45e-23 |
| the iterate's step: displacement, step from P(z), share in the weak directions | 6.1e-20 (m_h), 1.68e-15 (c0, p1), 0.002 | 1.3e-20 (m_h), 3.85e-16 (c0, p1), 0.025 |

The four weakest singular values halve from the iterate to the half step in both attempts. At the full step they fall
to two pairs, about 8.5e-25 and 5e-28, the same pairs in both. The iterate's own steps hardly touch these directions.
The trial's own correction lies wholly in them, and the own test compares that correction with the iterate's step.

## The refused full step taken (pre-#523 build)

`crawl_probe.py fixrun ... --accept own --start_lam 1 --switch 0` (`logs/fix_own_from1.log`, 474 s): the corrector
started from z1 + d1, the point the crawl refused, with its own test and switch 0.

| step | max\|F\| | \|dz\| | lam |
|---|---|---|---|
| 0 | 1.39e-28 -> 3.26e-31 | 2.98e-15 -> 9.82e-23 | 1 |
| 1 | 3.26e-31 -> 3.43e-46 | 9.82e-23 -> 3.38e-32 | 1 |
| 2 | 3.43e-46 -> 4.16e-65 | 3.38e-32 -> 1.76e-56 | 1 |
| 3 | 4.16e-65, converged | | |

Delta 1.729915772540067188606175429102600883886 (`fix/fixrun_D118.0000_s1_switch0_own_from1.npz`, the projected
point; the point itself 4.06e-55). So the 2.98e-15 correction the own test refused is the step that converges.
M's D 118 state (a = 1/2 steps) has Delta 1.729915772540067188606164966063807771721, 1.05e-20 lower. The two states
solve different plans (the same 4, 3, 3, 3 steps at other points: each attempt plans its own prediction), so this is
the plan's effect on the root, not a corrector difference.

## What the weak directions are (pre-#523 build)

`crawl_probe.py weak` (`logs/weak.log`, records `probe/weak.jsonl`): the four weakest right singular directions of the
pinned octo-double Jacobian (`junk_subspace_o`, every direction kept).

| point | max\|F\| | sigma (k = 11 pair) | sigma (k = 13 pair) |
|---|---|---|---|
| L's D 117 state | 1.75e-64 | 9.040e-25 | 5.533e-28 |
| M's D 117.5 state | 8.57e-79 | 8.643e-25 | 5.210e-28 |
| M's D 118 state | 6.86e-74 | 8.267e-25 | 4.908e-28 |
| the crawl's refused trial, projected | 1.39e-28 | 8.267e-25 | 4.908e-28 |

At every point the four directions are two cos/sin pairs of p1, the centre data: its harmonic 11 (the pair at about
8.5e-25) and its harmonic 13 (the pair at about 5e-28), the highest free harmonics under `--kfreeze 13`. Each has
about 0.24 of its unit norm in that harmonic of p1, 0.03 to 0.04 in node 0's p and m, and a Delta component of 7e-9
to 1.2e-6. These are the junk directions of notes/QUAD_DOUBLE.md 13.29 (p1's highest harmonics, no Delta content).
The refused correction lies wholly in the k = 13 pair (components -0.607 and -0.795): it is 2.9e-15 in p1's
harmonic 13, 2.1e-16 in harmonic 11.

## Where the harmonic-13 error comes from

`junk_err.py` (`logs/junk_err.log`; its control plants 1e-20 in harmonic 17 of the iterate's last part and reads
1.00e-20): each point's error in p1's harmonics against the root of the same plan (for the crawl the root above, for
the control M's D 117.5 state).

| point | crawl: max error | crawl: p1 k = 13 | crawl: k = 11 | control: max error | control: k = 13 | control: k = 11 |
|---|---|---|---|---|---|---|
| prediction | 1.95e-07 | 1.91e-07 | 1.42e-08 | 9.36e-08 | 9.07e-08 | 6.77e-09 |
| iterate z1 (after step 0) | 4.14e-15 | 2.92e-15 | 2.15e-16 | 3.86e-16 | 3.59e-17 | 2.65e-18 |
| full-step trial z1 + d1 | 2.98e-15 | 2.92e-15 | 2.15e-16 | 2.62e-17 | 2.59e-17 | 1.55e-18 |

The prediction's error is almost all in p1's harmonic 13. The first step removes all but 2.92e-15 of it at a = 1
and all but 3.6e-17 at a = 1/2. The next step from the iterate leaves it unchanged (2.92e-15 at z1 and at z1 + d1):
at the iterate the k = 13 pair's singular values are 5e-22 to 2.6e-21, raised by the iterate's other errors (they
halve with the distance along d), so its Newton step does not see the harmonic-13 error. At the full-step trial the
other errors are gone, the pair's singular value is the root's 4.9e-28, and the trial's own correction is that error.

## The own test's margin over #742's attempts

`margin.py` (`margin_out.md`; its selftest reads planted lines, and a parser that halves the refused trial's W fails
it): at Newton step 1 of each attempt, Y the iterate's |dz| after step 0 and W the lam 1 trial's own correction.

| run | a | D reached | start \|dz\| | Y | W | W / Y | step 1 |
|---|---|---|---|---|---|---|---|
| P | 1 | 114 | 3.38e-09 | 4.88e-19 | 4.39e-20 | 0.090 | accepted |
| L | 1 | 115 | 3.52e-09 | 5.27e-19 | 7.86e-20 | 0.149 | accepted |
| L | 1 | 116 | 1.27e-08 | 6.87e-18 | 4.73e-19 | 0.069 | accepted |
| L | 1 | 117 | 8.81e-09 | 3.38e-18 | 1.25e-19 | 0.037 | accepted |
| L | 1 | (118, stopped) | 1.95e-07 | 1.68e-15 | 2.977e-15 | 1.772 | refused, the crawl |
| M | 1/2 | 117.5 | 9.36e-08 | 3.85e-16 | 2.62e-17 | 0.068 | accepted |
| M | 1/2 | 118 | 1.52e-07 | 1.01e-15 | 8.25e-17 | 0.082 | accepted |
| M | 1/2 | 118.5 | 1.92e-07 | 1.61e-15 | 2.02e-16 | 0.125 | accepted |
| M | 1/2 | 119 | 4.45e-08 | 8.76e-17 | 1.19e-17 | 0.136 | accepted |
| M | 1/2 | 119.5 | 1.39e-07 | 8.62e-16 | 3.92e-16 | 0.455 | accepted |
| M | 1/2 | 120 | 2.64e-07 | 3.10e-15 | 5.61e-16 | 0.181 | accepted |

W is the harmonic-13 error left by step 0 in the crawl and the control (measured above). For the other attempts that
reading of W is an inference. Every attempt but the crawl has W / Y between 0.037 and 0.455. The start's |dz| does not
order them: M's D 118.5 step started at 1.92e-7, next to the crawl's 1.95e-7, and had W / Y 0.125.

## The same attempt on main's build (3c35f0c, exact freeze projector; 10:29 to 10:51 UTC)

`crawl_probe.py anm ... --stop 3` with `PYTHONPATH` on main's build, the rest of run R unchanged (`logs/AB_main.log`).
The base polish moves the D 117 state first (it is 2.0e-34 off in 5p under this build): five steps, |dz| 4.07e-13 at
the first, dDelta +1.57e-20, converged at 1.46e-106. #774 owns what that does to Delta.

| | pre-#523 build (#742, run R) | main's build |
|---|---|---|
| series: \|z_N\|, ratios 2-5, a_max | 2.87e-27; 141.8 42.7 3.6 3.3; 2.615 | 2.58e-28; 144.1 85.4 7.0 3.3; 2.904 |
| a = 1 start \|dz\| | 1.95e-07 | 4.93e-08 |
| step 0 | 1.49e-29 -> 1.39e-15, \|dz\| -> 1.68e-15 | 9.31e-31 -> 8.69e-17, \|dz\| -> 1.05e-16 |
| step 1 | lam 1 refused (W 2.977e-15, W / Y 1.77), lam 1/2 | lam 1, 8.69e-17 -> 6.15e-30 (W 4.15e-17, W / Y 0.395) |
| steps 2, 3 | the crawl (8 steps at lam 1/2 on win) | lam 1: 6.15e-30 -> 6.23e-35 -> 2.57e-53 |

So on main's build this attempt does not crawl. One attempt is not a rule: its W / Y, 0.395, is near the largest of
the accepted ones on the old build (0.455).

## Answer

**(a)** Met. Both iterates and their steps are saved (`R/crawl_iter_D118.0000_s1.npz`, `R/crawl_iter_D117.5000_s1.npz`),
the rebuild reproduces #742 bit for bit in every compared line and prediction, and in the control the corrector's
residual along the step is affine to lam = 1, with deviation 6.123e-28 lam² to four digits.

**(b)** The second branch: the residual is smooth to the last rung. In the crawl, arm E (switch 0, every point
projected) deviates from the affine model by 1.393e-28 lam² to four digits on all six rungs, and arm P equals it. No
lam* exists, so the fault is in the acceptance test. The own test judges the lam 1 trial by its own Newton correction,
and that correction (2.977e-15) lies wholly in the k = 13 pair of p1's junk directions, singular value 4.9e-28 at the
root. It is the error in p1's harmonic 13 that the first step left (2.92e-15). The iterate's Jacobian cannot see that
error, because there the pair's singular values are 5e-22 to 2.6e-21, raised by the iterate's other errors. So every
lam 1 trial's correction is 2.977e-15 while |dz| halves, and the test never passes. Taking the refused step converges
in three lam 1 steps (to 4.16e-65). In #742's other eleven attempts W / Y was 0.037 to 0.455.

**(c)** Not #700's mechanism. #700's residual jumped at lam* = 1 - 7.77e-15, where ElimO's switch stopped projecting.
Here every trial is projected (switch 0), the residual has no jump, and the trial's projection displacement is
5e-33. One feature is shared: the full first step leaves the iterate's own residual large (1.4e-5 here, 0.129 in
#700), carried by horizon data off the projection by 6.1e-20. Under switch 0 that is harmless, and the control
carries it too (2.6e-6). #700's lam = 1/2 signature (ratio 0.5000, |F| halving) appears here for a different reason:
the lam 1/2 trial is accepted because its own Jacobian, like the iterate's, does not see the harmonic-13 error.

## Measured and inferred

Measured, on the pre-#523 build unless marked:

- the rebuild against #742's logs and predictions;
- the residual along the step (arms U, E, P) at both iterates;
- both trial tests at lam 1 and 1/2, the own corrections split, and the weak directions there;
- the weak directions at L's D 117 and M's D 117.5 and 118 states;
- the p1 harmonic errors of the prediction, iterate and trial against a root of the same plan;
- the refused step taken, converging;
- the same attempt on main's build, not crawling.

Inferred, not measured:

- that W is the harmonic-13 error in #742's other attempts (measured only in the crawl and the control);
- why the first step leaves 81 times more harmonic-13 error at a = 1 than at a = 1/2. The prediction's own k = 13
  error is only 2.1 times larger, 1.91e-7 against 9.07e-8;
- whether N's crawl (`--od_accept natural`, lam 1/128 at step 0, then lam 1/2 without progress) is the same pair seen
  through the start's Jacobian. At this iterate the natural test accepts lam 1 (ratio 5.85e-5), but N never reached it.

## Recommended tasks

1. **The own test's full-step drop.**
   - What: give newton_od's own test the full_drop rule that #709 gave the natural test: a lam 1 trial is also
     accepted when its max|F| is at most f times the iterate's. A/B at this attempt on the pre-#523 build
     (`crawl_probe.py fixrun ... --accept own` from `R/crawl_iter_D118.0000_s1.npz` with the new option, f = 1e-6), and
     `octo_corrector.py planted` and `wall` with it.
   - Why: the refused trial lowered max|F| by 1e13, and taking it converged in three steps.
   - Acceptance (can fail): the A/B converges to at most 1e-60 within 6 steps, the same run without the option
     crawls (lam 1/2 at step 1), and planted and wall pass with their controls still failing.
   - Depends on #752.
2. **N's crawl, probed.**
   - What: extend `crawl_probe.py anm` to the natural test (record PinnedO.newton_o as well), rebuild N's attempt
     (#742's flags plus `--od_accept natural`) to Newton step 1, and run `weak` and probe's theta there.
   - Why: N stalled at max|F| 1e-19 with ratios 0.96 to 1.006 at lam 1. Whether that is the same k = 13 pair, seen
     through the start's Jacobian, is unknown.
   - Acceptance (can fail): either the simplified correction at lam 1 has share above 0.9 in the four weakest
     directions, or it does not, and then its largest unknown groups are named.
   - Depends on #752.
3. **The first step's harmonic-13 remainder against a.**
   - What: on main's build, from the D 117 state polished there, run `anm --stop 1` at a = 1, 1/2 and 1/4, with
     `junk_err.py` (extended to take its roots as arguments) against roots of the same plans, from `fixrun`.
   - Why: on the old build the first step left 2.92e-15 at a = 1 and 3.6e-17 at a = 1/2, and that remainder against
     the iterate's |dz| decides the own test. On main's build W / Y was 0.395 at a = 1.
   - Acceptance (can fail): W measured equals the harmonic-13 error at each a, to 10%, or it does not.
   - Depends on #752 and #774.
