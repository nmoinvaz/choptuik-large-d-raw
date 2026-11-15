# I825-mac: T4 at the real series' amplitude mix, Pade on #712's two tracks at D 255.77 (case T4fit)

Machine: the coordinator's Mac (Apple M5), agent xfkappa. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/825.
Code: `hp/jet_singularity.py planted --case T4fit --jet I712-dh370/repro/jet_pin3_D255.7661.npz`, registered at
wip/xf-825 8c7f5d44 (criteria in the docstring and on the issue before the first run), the outcome recorded at 3eca5041, on
main c044aef4. One process at nice 10, seconds per run.

## Runs

- `t4fit.log`, `t4fit.json`: the case, PASS (exit 0). `t4fit_rerun.log`: again, the JSON byte-identical.
- `t4fit_drop_pole.log`, `t4fit_drop_near.log`: the controls, exit 1.
- `check_numbers.log`: `check_numbers.py --selftest` at 3eca5041, 2012 of 2012, selftest 2012 of 2012.

## Result

The fit (T4's pairs held at their D*, complex amplitudes, orders 5-24, weights 1/|c_k|): relative residual 0.86 rms,
1.59 at most. Amplitudes |C|: A 9.1e-3, near 1.9e-3, B 0.38, C 9.6e-3. Each pair's |term| at orders 5, 12 and 24:
A 2.2e-7, 1.4e-11, 4.5e-20; near 4.2e-7, 1.9e-11, 1.4e-18; B 3.7e-6, 1.2e-11, 1.3e-21; C 2.3e-6, 2.9e-12, 8.8e-19.
The real series: root test 3.682, stable Pade poles |s| 3.996 (44.7 degrees), 4.235 (16.0), 5.016 (91.4).

| plant | root test (real 3.682) | A (5.012, 91.4) | near (3.998, 44.7) | B, C (reported) | other stable poles | verdict |
|---|---|---|---|---|---|---|
| T4 background, noise 1e-6 (judged) | 3.664 (-0.5%) | 5.012, 91.4 (n 3) | 3.998, 44.7 (n 3) | both found | 3.594, 43.7 | PASS |
| T4 background, 1e-12 | 3.664 | found | found | both | the same | PASS |
| real orders 1-4, 1e-6 and 1e-12 | 3.664 | found | found | both | the same | PASS |
| drop_pole (A left out) | 3.580 (-2.8%) | not found | 3.998, 44.7 (n 5) | both | 3.642, 46.7 | FAIL, as it must |
| drop_near (near left out) | 4.406 (+19.7%) | 5.012, 91.4 (n 5) | not found | both | none | FAIL, as it must |

Verdict by the issue's rule: the fitted mix's root test is within 10% of the real one, and Pade recovers A and the near
track, so it separates a pole at |s| 4 from one at 5 at the real series' balance of amplitudes. The four pairs fit the
coefficients poorly (a fifth real pole at |s| 4.235, 16 degrees, is not in the model), so the plant matches the real
series' root test and the least-squares amplitude scales, not its coefficients; it tests the method at that balance,
not the real poles themselves. No recommended task.
