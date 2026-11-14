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
