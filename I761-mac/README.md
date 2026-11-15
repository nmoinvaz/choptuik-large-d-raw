# I761-mac: a planted two-track series for Pade, poles at |s| 4 and 5 from D 255.77 (case T4)

Machine: the coordinator's Mac (Apple M5), agent xfkappa. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/761.
Code: `hp/jet_singularity.py planted --case T4`, registered at wip/xf-761 4b85400f (criteria in the docstring and on
the issue before the first run), the outcome recorded at cd7c6fb4, on main a095257c. One process at nice 10, seconds per run.

## Runs

- `t4.log`: the case, FAIL (exit 1). `t4_rerun.log`: the same command again, identical.
- `t4_drop_pole.log`, `t4_drop_near.log`: the controls (A, or the near track, left out), exit 1.
- `check_numbers.log`: `check_numbers.py --selftest` at cd7c6fb4, 1998 of 1998, selftest 1998 of 1998.

## Result

| mix | noise | A (5.012, 91.4) | near (3.998, 44.7) | B (6.752, 120.8), reported | C (4.482, 40.0), reported | root-test radius |
|---|---|---|---|---|---|---|
| o12 | 1e-6 (judged) | 5.012, 91.4 | 3.998, 44.7 | 6.752, 120.8 | 4.482, 40.0 | 4.440 |
| o12 | 1e-12 | the same | the same | the same | the same | 4.440 |
| o24 | 1e-6 (judged) | not found | not found | 6.751, 120.8 | not found | 6.755 |
| o24 | 1e-12 | not found | not found | 6.751, 120.8 | not found | 6.755 |

In o24 B's terms are the largest at every order to 24, so the root-test radius is B's and stable_poles drops the
poles inside 0.85 of it (5.74) as the approximant's. Controls, judged mix o12: drop_pole finds near, B and C and not A;
drop_near finds A, B and C and not the near track (C at 4.48 is not taken for it).

Verdict by the issue's rule: Pade misses both tracks in one mix, so #712's Pade reading of the two is untested
(notes/LARGE_D_WALL.md). The real series' root test at D 255.7661, 3.68 (#712), is below both tracks' |s|, unlike o24's
6.755; that fits a mix like o12, an inference.

## Recommended task

*T4 at the real series' amplitude mix.* What: set the four pairs' amplitudes by least squares to Delta's own
coefficients at D 255.7661 (I712-dh370's series), with the pairs fixed at the planted D*, and run T4's criterion on that
mix with the same noise and controls. Why: T4 passes at o12 and fails at o24, and which regime the real series is in is
read only from its root test. Acceptance (can fail): the fit's residual is reported; the fitted mix's planted root test
lies within 10% of the real 3.68; then A and the near track are recovered to 3% and 3 degrees, or the reading stays
untested. Depends on: #761, #712.
