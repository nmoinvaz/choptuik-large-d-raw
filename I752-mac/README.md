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
