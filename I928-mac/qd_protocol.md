# The quad-double stage on the band: checks before it is used (#928)

Written 2026-11-17 14:10 UTC, before either run. The coordinator's terms are in the issue's comments.

The double-double error of Delta near the stop. Two double-double runs at one D differ in Delta by 3.4e-21 at
D 12.375 (one stalled at max |F| 1.1e-27, one converged at 6.7e-29) and by 2.7e-21 at D 12.46875
(`out/sm_records.jsonl`). The error quoted for a double-double Delta near the stop is 1e-20, three times the larger
difference, rounded up.

Check 1 (consistency). The quad-double Newton (`run_eta.py --qd --qd_jac dd`, the exact quad-double Jacobian) from
the converged double-double state at eta 0.3, D 12.375 (Delta 1.111899734008754743955872521, max |F| 6.7e-29).
Pass: the quad-double max |F| is at most 1e-28, and |Delta_qd - Delta_dd| <= 1e-20. A failure stops the route.

Check 2 (the stalled state). The same from the stalled state at D 12.5 (max |F| 8.1e-28), with the double-double
stage's tolerance at 3e-27 so that it hands over. Pass: the quad-double max |F| is at most 1e-28, and the
double-double residual of the result, its first two parts, is at most the stall's 8.1e-28.

Only if both pass does the chain continue in quad-double. The 1e-28 bound then applies to the quad-double residual
of those points, and the double-double chain's stop at D 12.46875 (eta 0.3) stays the record of where double-double
ends.

## Addendum: a looser hand-over, and the rule for accepting a quad-double point

Written 2026-11-17 14:46 UTC, after both checks passed and before any point of the continuation. The
coordinator's limits, from its messages of 2026-11-17:

(1) The double-double stage aims at 3e-27. Where it stalls above that, its state is handed over all the same when
    its max |F| is at most 1e-24, never above (`run_eta.py --handover_max 1e-24`).
(2') A quad-double point counts only if all of these hold (`run_eta.py`'s `qd_basin`, with `--qd_accept 1e-28`):
    - max |F| is at most 1e-28 within 4 Newton steps, and at the final state;
    - max |F| never rises from one step to the next;
    - from the second step on, max |F| is at most 1e10 times the square of the step before;
    - the size of the Newton step, max |dz|, is at most 1e10 times the square of the step before, at every step
      after the first.
    The first step is exempt in max |F| for a reason seen in both checks (6.67e-29 -> 6.24e-29 -> 4.68e-57 and
    8.13e-28 -> 2.09e-28 -> 4.92e-56). The distance to the root is the displacement along the band, about 3e-13, and
    it shows in the residual only at second order. The first quad-double step removes it and leaves the second-order
    remainder of a step of that size, so that step is quadratic in dz, not in |F|.
    One reading of mine, told to the coordinator: a step's max |F| also passes the third line when it is below
    1e-55, the quad-double Newton's own tolerance, since the arithmetic cannot follow a square below that.
(3) Each point's record holds the double-double residual at which it was handed over (`handover_F`), the
    tolerance, every step's max |F| and max |dz|, and which lines of (2') held. `chain_table.py` writes the
    hand-over residual into its csv.

The rule is applied to every quad-double point, also to those handed over at 3e-27. The first point that is not
accepted stops the chain (`chain.py --dD_min 0.0625`), and it is reported with its D.

The rule was tried on the two checks' histories, which pass, and on four made-up histories that must fail: linear
convergence in five steps, a rise at the first step, a second step as large as the first, and a third step that is
not quadratic in max |F|. All four are rejected. The checks did not record max |dz|, so the fourth line is first
seen on the continuation's points.

## Second addendum: the first step may raise max |F| by a bounded factor

Written 2026-11-17 18:10 UTC, after the rule above rejected a point. It was not fixed in advance.

What happened. Under the rule of the first addendum the continuation at eta 0.3 accepted D 12.5 and rejected
D 12.5625: handed over at max |F| 1.66e-28, its first quad-double step gave 2.49e-28, and the "never rises" line
stopped it. A diagnostic outside the rule (`qd_force.py`, `out/qd_force_eta0.3_D12.5625.txt`) continued the
Newton past that rise: 1.66e-28 -> 2.49e-28 -> 6.28e-56, with max |dz| 5.42e-13 then 8.83e-28. After the first
step the convergence is quadratic in both, as in the accepted cases.

The first-step ratios of max |F| seen so far, after over before: 0.94 (check 1, D 12.375), 0.26 (check 2,
D 12.5), 0.043 (D 12.5 on the chain), 1.5 (D 12.5625).

The reason. The residual at the start is a second-order effect of the displacement along the band, and the residual
after the first step is the second-order remainder of a Newton step of that displacement's size. Their ratio is of
order one and can fall on either side of 1. The "never rises" line was written from two cases in which it fell.

(2'') The coordinator's amendment, approved 2026-11-17: at the first quad-double step max |F| may rise by at most a
factor of 10. After the first step it must not rise. The other lines of (2') are unchanged: at most 1e-28 within 4
steps and at the end; from the second step on, max |F| at most 1e10 times the square of the step before; max |dz|
at most 1e10 times the square of the step before at every step after the first.
(`run_eta.py --qd_first_rise 10`; each record keeps the factor it was run with.)

D 12.5625 counts only from a fresh run under (2''), not from the diagnostic's state.

The amended rule was tried on the two real histories (D 12.5 passes with and without the amendment; D 12.5625's
forced history passes only with it) and on two made-up ones that must fail under it: a first rise by a factor of
30, and a rise at the second step. Both are rejected.
