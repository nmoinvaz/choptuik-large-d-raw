# I795-dh370: #776's series at D 259.26 and 259.49 on a new plan, to test the square-root point near 259.90

Machine dh370 (Fedora 45, i7-8700, 12 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/795.

Scripts (written by the coordinator): `run795.sh` (#776's series command with `--keep_plan 0`, as #686, at #603's states
D 259.2582 and 259.4928, in #712's worktree choptuik-large-d-685 and #776's venv) and `compare795.py` (#782's
`singularity_type.py` estimators on #776's kept-plan series and on these).

Criteria, fixed before the new series were read (#795): (A) at each base Delta's Dlog D* and the 24 rows' ratio median D*
on the new plan within 0.01 of the kept plan's; (B) Delta's mu by the ratio and the Dlog estimators in [0.25, 0.75] on both
plans at D0 259.4928; (C) the control `--mutate=shift` (the new plan's D* moved by 0.5) fails (A) at both bases.
`compare795.txt` and `compare795_shift.txt` end `exit 0` when they hold.

## Results (dh370, 2026-11-14)

Runs. `run795.sh` as the user unit `i795` (under `systemd-inhibit`, log `~/scratch795_run.log`), 12 threads at nice 10, 18:00:52 to 19:39:09 UTC.
Series with `--keep_plan 0` exit 0, wall 2907 s (D 259.2582, ended 18:49:19 UTC) and 2987 s (D 259.4928, ended 19:39:06 UTC), no Traceback,
`Result=success`. `compare795.txt` ends `exit 1`, `compare795_shift.txt` ends `exit 0`. Code: worktree choptuik-large-d-685 at main f40deb4a, venv of
choptuik-large-d-614, raw origin/main 5dee0183, `hp/singularity_type.py` from the code repository's origin/main 220f1770.

The new plan's base polish did not converge at either base, as at D 252 (#686): the first trial step has max|F| 1.77e64 (D 259.2582) and 2.75e68
(D 259.4928), ten trial steps are refused, the octo-double Newton ends "1 steps, not converged" (double-double |F| of its first two parts 6.0e+08
and 6.7e+08), and the log says "base polish not adopted: the stored state is the base". The series is formed at the stored state (1355 s and
1354 s of the walls).

The estimators (`compare795.txt`; S = square-root band):

| D0 | plan | Delta ratio: D*, mu | Delta dlog: D*, mu | rows' ratio median D* |
|---|---|---|---|---|
| 259.2582 | kept | 259.8997, +0.724 S | 259.9047, +0.448 S | 259.9007 |
| 259.2582 | new | 259.9099, +0.785 unclassified | 259.9161, +0.446 S | 259.9113 |
| 259.4928 | kept | 259.9029, +0.541 S | 259.9037, +0.469 S | 259.9028 |
| 259.4928 | new | 259.9131, +0.543 S | 259.9140, +0.467 S | 259.9130 |

The bars, as written before the run (#795):

| criterion | D0 259.2582 | D0 259.4928 |
|---|---|---|
| (A) Delta's Dlog D* and the rows' ratio median D* on the new plan within 0.01 of the kept plan's | FAILED: Dlog +0.0114, rows +0.0106 | FAILED: Dlog +0.0103, rows +0.0102 |
| (B) Delta's mu by both estimators in [0.25, 0.75] on both plans | not asked (ratio mu on the new plan 0.785, outside) | met: 0.541 and 0.469 kept, 0.543 and 0.467 new |
| (C) `--mutate=shift` (new plan's D* + 0.5) fails (A) | met (exit 0) | met (exit 0) |
| largest relative change of Delta's coefficients 5..24 between the plans | 3.44e-01 | 4.44e-01 |

Readings and caveats. (A) fails at both bases by 0.0003 to 0.0014 over the bound: all six D* values (ratio, Dlog and rows at two bases) move by
the same sign and size, +0.0102 to +0.0114, which is 2% to 14% above the 0.01 bound and 2% of the control's 0.5. The control fires, so the check can
detect a 0.5 move, but (A) already fails without the shift, so the control says nothing on whether (A) could pass at a smaller bound. At D0
259.4928 the exponent is the same on both plans (ratio 0.541 and 0.543, Dlog 0.469 and 0.467), while Delta's coefficients differ by up to 34% and 44%;
`compare795.py` does not print the order at which the largest change occurs. The kept-plan numbers are the #776 series' own (the same as the
coordinator's #782 reading: 259.903, mu +0.54 and +0.47 at 259.4928).

Recommended tasks (for the coordinator): (1) the per-order relative change of Delta's coefficients between the two plans at both bases and D* from
the series cut at orders 12, 16, 20 and 24 on each plan, from the stored npz (no run), accepted when it reproduces 3.44e-01 and 4.44e-01 and shows
the orders where the +0.010 shift arises; (2) a third plan on the base D 259.4928 made as #686 made its second, accepted when the three plans'
Dlog D* are given against the 0.01 bar, to see whether +0.010 is a fixed offset or scatter.
