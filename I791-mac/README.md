# I791-mac: the strip -0.05 < Re lambda < 0.05, |Im lambda| < 9 of the D = infinity Stokes-jump determinant (#791)

Machine: mac (Apple M5, the coordinator's Mac), agent xfchecks, one process at nice 10. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/791

Code: `solver/matter/css_inf_count.py` (with `--box` and `locate`) and `solver/matter/css_inf_jump.py` (with `--atol`,
default unchanged: D(0.05 + 9i) at setting A equals #781's stored value bit for bit), branch wip/i791 (venv-314),
run from `solver/matter/` by `run.sh` (in this folder). Settings A (r0 0.1, r1 0.3, alpha 3pi/8) and B (r0 0.11,
r1 0.25, alpha 0.3pi), rtol 1e-13, N 160, the background selected by Newton at each setting. The plant is the
conjugate pair 0.02 +- 6i (the issue's "+-0.02 + 6i" read as the pair the counter plants, p and conj p).

The raised absolute tolerance (1e-16) is used only in `locate` for the zeros next to +-i omega. The counts and the
location of lambda = 0 use the default, 1e-30 + rtol 1e-6.

## Files

- `run.sh`: the whole run (selftests, the strip at A and B with their plants, the zero location).
- `selftest.log`: `css_inf_count.py selftest` (the #781 box: 6, planted 8; the strip: 3, planted 0.02 +- 6i 5; exit 0)
  and its control `--mutate=coarse` (0 in both; exit 1).
- `count_A.log`, `count_A_plant.log`, `evals_A.jsonl`; `count_B.log`, `count_B_plant.log`, `evals_B.jsonl`;
  `counts.jsonl` (the four count records).
- `locate_A.log`, `locate_B.log`, `locate.jsonl`: the secant from 0.02 + 0.01i (default tolerance) and from
  0.02 +- 3.97i (absolute tolerance 1e-16) at each setting.

## Results

| setting | winding | planted 0.02 +- 6i | largest step | determinants (plant: new) | D(conj lam) = conj D(lam) |
|---|---|---|---|---|---|
| A (0.1, 0.3, 3pi/8) | 2.9999999999999987 | 5.000000000000001 | 0.4978 rad | 356 (48) | 1.6e-9 (177 pairs) |
| B (0.11, 0.25, 0.3pi) | 2.999999999999998 | 4.999999999999999 | 0.4961 rad | 400 (48) | 1.0e-8 (199 pairs) |

No bisection limit was hit. The zeros (distance from the exact mode; the omega of each setting's selected background):

| zero | A | B | absolute tolerance |
|---|---|---|---|
| lambda = 0 | 2.1e-13 (5 secant steps) | 1.7e-13 (13) | default |
| +i omega | 4.5e-12 (40, the limit) | 2.6e-10 (26) | 1e-16 |
| -i omega | 2.0e-11 (19) | 2.9e-10 (40, the limit) | 1e-16 |

The secants that reach the 40-step limit stop at D's noise floor: |D| about 1e-6 there against |D'| = 3.4e4 at i omega,
a position noise of about 3e-11 (A) to 3e-10 (B).
