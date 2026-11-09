# I242-mac: the planted test of the alias rule in hp/modecount_wind.py, with its controls

Machine: mac (Apple M5, 10 cores, macOS 27, shared with #208's two CAPD processes), venv-314 (Python 3.14, hpkernel and
multidouble NEON, python-flint 0.9.0). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/242. Code: branch
wip/i242 of the main repository (hp/modecount_wind.py 01f6c59, hp/modecount_planted.py bc9fd22). No determinants: the
tests run on synthetic det M.

## The rule

modecount_wind.py's edge() bisected only intervals whose phase step of g exceeded tol, and verified only steps above
tol/2. An interval that looked flat at the initial spacing was never checked, and whole turns could hide in it (#212's
kf 23 edge Im = 3 omega / 2 hid 3, #230). Now each interval's length h is also held against the local scale of g,
|Delta ln g| / h (the ln|g| change, which does not wrap, with the wrapped phase step). The scale is taken on the
interval and up to 3 intervals each side, and at an edge's first and last 3 intervals also on the other edges' 3
intervals at that corner, since |(ln g)'| does not depend on the direction. The interval is bisected while
h * scale > pi/2 (--alias). The edges are sampled in sweeps until no corner scale grows.

## Files

- planted/planted_controls_bc9fd22.log: `python3 hp/modecount_planted.py --controls` at bc9fd22, exit 0. The test
  and its three mutations, in this order: the test (all 39 cases pass, 16353 evaluations), --mutate=flat (the old
  rule: 27 cases fail, 11586 evaluations), --mutate=nolng (8 fail, the pairs), --mutate=nocorner (6 fail, the long
  rows).
- planted/moment_planted_controls_bc9fd22.log: `python3 hp/modecount_moment_planted.py --controls` with the new rule
  (the moment code's test calls modecount_wind.count): test passes, nok and shift fail, exit 0.

## Results

Pass criteria (fixed in the test's docstring before the held-out cases ran): in all 8 boxes wind(g) equals the
planted number to 1e-6, every box resolved, every step at most pi/4.

| group | cases | old rule | new rule | evaluations new / old |
|---|---|---|---|---|
| D 30 (the 8 cases from before) | 8 | pass | pass | 1.01 |
| the six moment-test configurations (#230) | 6 | 6 fail | pass | 1.37 |
| close pairs between two samples (5, and 4 held out) | 9 | 9 fail | pass | 1.31 |
| rows along Im = y2 (2 short, 3 long, 3 held out) | 8 | 7 fail | pass | 2.10 |
| held-out random configurations (seed 242) | 8 | 5 fail | pass | 1.14 |

With a row of zeros along the whole of Im = y2 the old rule counts U 0 for 22 (or 44) planted zeros, every edge
resolved; only the corner scales catch it (--mutate=nocorner fails there). The close pairs are caught through ln|g|
(--mutate=nolng fails there).
