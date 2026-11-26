# I1098-mac: the ladder estimator for Delta_inf (planted truths, sigma table, controls, three-point check)

Machine: the coordinator's Mac. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098 (part 2, the ladder
estimator). Code: `hp/ladder_fit.py` and `hp/ladder_pade.py` on choptuik-large-d branch `wip/twenty-digits`; the
commit of each file is named below. Real direct points from raw I1088-dh610, I1088-dh370, I1088-mac-a, I1088-mm5 at
dd7573766 (the full system at D 300, 1000, 2000 only). Python 3.14 venv, mpmath 1.3.0, python-flint 0.9.0, scipy 1.18.1.

Rule and planted truths: the docstring of `hp/ladder_fit.py`. Each `planted` log ends in the table "sigma per point
needed for Delta_inf to 1e-20": the largest sigma of the grid at which the 90th percentile of F max(h, s) over 40
seeds is <= 1e-20, with >= 90% of the seeds quoted, coverage >= 90% on seeds 21-40 and the systematic patterns
covered. F is calibrated per ladder on seeds 1-20 (T1-T4 and three systematic patterns, every sigma). The error bar
E = F max(h, s) is a spread over fit choices and the propagated data error scaled to cover the planted cases. On the
held-out seeds 21-40 it covered 94-100% in every (ladder, truth, sigma) row of planted_E20r but two, both T2 at the
edge of what the ladder can do: A20 at 1e-22 (89%) and E at 1e-22 (one seed quoted, outside); 95-100% on ladder X.
It is conditional on Delta being analytic in 1/n at n = infinity.

Files (commit):
- planted_E20r.log/.json (d537beb9): every ladder, and X = the recommended ladder with rounded D (250, 300, 360, 432,
  519, 622, 747, 896, 1000, 1291, 1549, 2000, 2231, 2828.43, 3214, 4000, 4628, 5555, 6666, 8000). The table of record.
  planted_a, planted_b (42dce023) and planted_c (d537beb9, E25 and J20) are the same rule; their rows agree.
- budget.log/.json (42dce023), budget2.log/.json (d537beb9, adds the L1 gain): per ladder and degree the noise gain
  ||g|| and each truth's truncation bias, and an oracle's sigma (best degree knowing the truth; not the rule).
- cand_kstar, cand_one (42dce023): the two other candidate sets; F 5.16 and 10.24 on ladder A against 3.03.
- controls_A/E20 (42dce023): shift and tight without the leave-one-out check. On E20 the shift control did not fire:
  the rule climbed to degree 15, which interpolates the shifted point (leverage 1.000), and stayed inside E; the
  leave-one-out check was added for it.
- controls2_A/E20 (8a4e90d7): shift (D 1000 by +30 sigma) fires 10 of 10 on both (A: no quote; E20: leave-one-out
  |z| 17.5-22.1); tight fires; unmutated false alarms 0. control_lowdeg_*, control_var_* (42dce023): fire 10 of 10.
- loocheck.log/.json (8a4e90d7): the leave-one-out check (bar 10) on clean planted data: no alarm on T1-T3 in 304
  quoted cases (A, A20, E20; sigma 1e-22, 1e-23); on T4 and T5 it fires at the low points their exponential term
  contaminates. loocheck_notrunc_partial.log: an earlier form (bar 5, no truncation term), stopped part way; it
  fired on clean T1 and T3 data, which is why the form changed.
- probe_A/E20 (42dce023): c e^5 log e added to T1 (outside the hypothesis), sigma 1e-23: up to c = 1e-2 the quote
  stays inside E on A (20 of 20) and E20 (19 of 20); at c = 1 on E20 1 of 20 is outside E with no alarm.
- pade_E20.log/.json (ladder_pade.py at 8a4e90d7, ladder_fit at 42dce023): rational [L/2] in 1/(D-2) against the
  polynomial rule in that variable alone, seeds 1-10 (F) and 21-30 (coverage), sigma 1e-22 and 1e-23.
- mk_E20_T1/direct_s.jsonl: planted T1 records (sigma 1e-23, ladder E20) in the direct_s.jsonl format.
  realpath_E20_T1.log/.json (d537beb9): `real` on them: Delta_inf = T1's limit + 2.3e-22, E 4.9e-22, both checks
  pass; realpath_E20_T1_shift.log: --mutate=shift (D 1549 by +30 sigma): leave-one-out |z| 21.5, exit 1.
  realpath_*_before_fix.log (8a4e90d7): the same before the reader fix; no quote, because the parts were read
  through their decimal repr (off by up to 1e-17) and fit values were differenced in floats from a reference 4e-2
  away.
- real3.log/.json (d537beb9): the three real full points; the rule quotes nothing (3 < 5 points); the three-point
  check (quadratic in each variable) minus Track C's Delta_inf: +6.38e-7, +4.96e-7, +3.88e-7, with T1's same fit
  error +6.33e-7, +4.91e-7, +3.83e-7; with T1 subtracted, +5.1e-9, +4.9e-9, +4.7e-9.
