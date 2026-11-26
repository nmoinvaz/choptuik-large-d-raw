# I1098-mm5/ladder/D747: D 747 full direct solve on the Moebius horizon, recipe v2, tail at M 48 to h23 (#1098)

Part of `../`. Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Command (coordinator's order, 2026-11-26 18:27 UTC; D 622 and D 747 moved from dh370 to this runner), detached, 6 threads, from the ladder folder:

```
KSBAR=1e-64 bash tools/ladder_point2.sh 747 200 6 <ladder>/D747 <ladder>/inputs/S300_D300_mob6_h13.npz <ladder>/inputs/S1000_D1000_base6_h13.npz 48 23
```

`tools/ladder_point2.sh` (blob da887d7143bf94d45d99fcd168550d0e56437370, verified; the same as D 1291's; the inputs are `../inputs/`, absolute paths because the script changes directory). kc 200, the Moebius horizon a = max(8, (D - 2)/400) = 8,
start **ks = ceil(1.5 (D - 2)) + 20 = 1138**, raised by 200 (at most 4 times) until the jump's ks+200 |dF| is at most KSBAR = 1e-64. That check is the quad-double residual's change, whose own floor read 1.2e-45 to 1.8e-45 at D 1291 (`../D1291/README.md`):
the ks the loop settles on is then confirmed by the octo-double gate `hp/ks_gate.py` (raw/main f398e829, in `~/Source/choptuik-fastmul6c`, bar 1e-64, 2 threads) on the jump state, run beside the point.
Stages (`run.log`, each log and state in its folder): `jump/`, `rls/` (h5..h11 to tol 1e-36), `rls13/` (h13 to 1e-48, ddelta 1e-25, octo-double residual), `tail/` (the h13 state resampled to M 48, h13 re-converged, then h15..h23, qq, od, tol 1e-48, ddelta 1e-25). fastmul6, Python 478e9d86.

## Bars, written before the run (coordinator's order)

- The jump converges and the ks gate passes (the ks it settled on is logged). h5..h13 are each released.
- The tail falls from h15 by about 1e2 or more per harmonic, h21's change is at most about 1e-23, and h23 is released with a pending dDelta at most about 1e-26: no turn.
- Stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial (D 432's u tail), or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped (amended 2026-11-26 19:01 UTC, coordinator's order; the order first read: any inner solve that does not converge).
- Reported: the final Delta, each stage's time, the ks used; each point is pushed at its end. Times from `date -u`.

## Stopped 15 s after the start (2026-11-26 18:27:45 UTC, coordinator's amendment)

Started 18:27:30 UTC together with D 622 (wrapper pid 49404), and stopped at 18:27:45 UTC by SIGTERM to the wrapper 49404 and the timeout 49434 (python 49437) on the coordinator's amendment, which my launch crossed: "start D 622 as sent, but NOT D 747. Its 6 threads take the M 64 rerun at D 1000 instead. D 747 goes back to the queue."
It was in its first jump, ks 1138, with no result; the partial files are in `attempt0_stopped_18_27/`. The bars above stand for the later run.

## Setup for the restart (2026-11-26 19:10 UTC, coordinator's change of 19:06)

D 747 runs the fixed `tools/ladder_point2_8e67.sh` (raw a54aa2266 `I1098-mac-a/tools/ladder_point2.sh`, **blob 8e6779cf1cfedafc8050e2d237c94b771c877e18**, verified; D 622 and D 1291 still run `tools/ladder_point2.sh`, blob da887d71, untouched) with the Python of **fastmul6 f398e829** from a second worktree `~/Source/choptuik-fastmul6-f398` (detached; `~/Source/choptuik-fastmul6` stays at 478e9d86 for the running jobs), kernel `~/Source/fastmul6-site`:

```
HP=$HOME/Source/choptuik-fastmul6-f398/hp KSBAR=1e-64 bash tools/ladder_point2_8e67.sh 747 200 6 <ladder>/D747 <ladder>/inputs/S300_D300_mob6_h13.npz <ladder>/inputs/S1000_D1000_base6_h13.npz 48 23
```

It gates ks on the octo-double `ks_gate.py` (bar 1e-64, from the jump state, steps of 200), so no separate gate is run; `run.log` must show "ks gate (bar 1e-64): N (...)", and an exit 6 (no ks meets the bar) is a stop to report.
The stopped first attempt is in `attempt0_stopped_18_27/`; OUT holds no old jump.
**Amended stop rule** (coordinator's order, 2026-11-26 19:01 UTC): stop and report when a qq inner solve does not converge, when a harmonic's line search fails at every trial (D 432's u tail), or when an outer step is 3x its harmonic's first. A qd inner floor that hands over to qq is logged, not stopped.
Bars: as above (the jump converges and the ks gate passes, h5..h13 each released, the tail falls from h15 by about 1e2 or more per harmonic, h21's change at most about 1e-23, h23 released with a pending dDelta at most about 1e-26, no turn).

Two differences from D 622 and D 1291, noted before the run: (1) `form_s.py` at f398e829 differs from 478e9d86 in `release_ls`: the inner held solves chord-step with a kept Jacobian by default (`--inner_chord 1`, commit e1cd7a84; it reforms the Jacobian after any slow chord step; 4 more inner steps allowed), so its converged states agree with 478e9d86's to the tolerance, not bit for bit;
(2) the script passes `--commit 478e9d86`, so the commit field in this run's records reads 478e9d86 while the Python is f398e829.

### Amendment (2026-11-26 19:12 UTC, coordinator's order): the commit label and inner_chord

The command is started with `EXTRA="--commit f398e829"` in front: the script appends `$EXTRA` after its own `--commit 478e9d86`, and `form_s.py`'s `opts()` keeps the last value of a repeated option (checked: `opts(["--commit","478e9d86","--commit","f398e829"], ...)` returns f398e829 on f398e829's `hp/form_s.py`), so this run's records say f398e829.
The `inner_chord 1` default is accepted (it converges to the same tolerance, 1e-48; the dh370 and dh170 points run it too).

```
EXTRA="--commit f398e829" HP=$HOME/Source/choptuik-fastmul6-f398/hp KSBAR=1e-64 bash tools/ladder_point2_8e67.sh 747 200 6 <ladder>/D747 <ladder>/inputs/S300_D300_mob6_h13.npz <ladder>/inputs/S1000_D1000_base6_h13.npz 48 23
```

## Attempt 1 stopped (2026-11-26 20:02:38 UTC) and attempt 2, chord-free (coordinator's order, 20:03 UTC)

**Attempt 1** (started 19:20:08 UTC, `attempt1_chord_floor/`: its `rls/`, `rls13/`, `run.log`, `driver.log`, `ks_gate.log`; Python f398e829 with the `inner_chord 1` default): the jump at ks 1138 converged (51 s) and the ks gate chose ks 1338 (1138 -> 1338: 1.88e-55; 1338 -> 1538: 8.56e-66, bar 1e-64); rls h5..h11 rc 0 at 19:46:02 (25 min).
At **h13** (rls13) outer 0 (qd Jacobian) floored (|F| 1.79e-39 against 1.72e-39) and handed over to qq (logged, as agreed). Outer 1 (qq, 19:52:18): the trial at lam 1 **floored in 10 steps at |F| 1.75e-45, against the tol 1e-48** (the step was accepted, full-step dDelta -2.40e-16, residual 1.72e-39 -> 1.75e-45).
A qq inner solve that does not converge is a stop of the amended rule: D 747 was stopped by exact pid (wrapper 51580, timeout 52430, python 52431) at 20:02:38 UTC, 25 s into outer 2. D 432, D 519 and D 622 on 478e9d86 (no chord) reached 1.78e-76 (D 432) at that stage.

**Attempt 2** differs from attempt 1 only in `--inner_chord 0` (every inner solve chord-free, as on 478e9d86; f398e829 `form_s.py` line 1370 chords only when inner_chord is "1"): `jump/` kept (the converged ks 1138 jump; the script's "jump kept from the earlier run"), the ks gate run again (expect 1338 with 8.56e-66), then rls h5..h11, rls13 and the tail:

```
EXTRA="--commit f398e829 --inner_chord 0" HP=$HOME/Source/choptuik-fastmul6-f398/hp KSBAR=1e-64 bash tools/ladder_point2_8e67.sh 747 200 6 <ladder>/D747 <ladder>/inputs/S300_D300_mob6_h13.npz <ladder>/inputs/S1000_D1000_base6_h13.npz 48 23
```

Same bars and amended stop rule. If h13's qq inner solve floors again with inner_chord 0, stop and report: then the chord is not the cause.
