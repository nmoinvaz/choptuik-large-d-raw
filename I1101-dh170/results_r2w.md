| lambda | hybrid sign | noise-robust | robust (dln <= 0.1) | dln | float64 sign | ln\|det\| | b12 | seconds |
|---|---|---|---|---|---|---|---|---|
| 0.035 | +1 | True | True | 1.33e-05 | -1 | -4210.6738318039 | rust | 4423 |
| 0.045 | +1 | True | True | 1.35e-05 | -1 | -4211.9503431400 | rust | 6625 |
| 0.050 | +1 | True | True | 1.35e-05 | +1 | -4212.5955870798 | rust | 6600 |
| 0.060 | +1 | True | True | 1.37e-05 | -1 | -4213.9037243145 | rust | 6493 |
| 0.070 | +1 | True | True | 1.38e-05 | -1 | -4215.2427588991 | rust | 6534 |
| 0.085 | +1 | True | True | 1.39e-05 | -1 | -4217.3438843690 | rust | 4411 |
| 0.100 | +1 | True | True | 1.35e-05 | -1 | -4219.6804690495 | rust | 4410 |
| 0.130 | -1 | True | True | 2.03e-05 | -1 | -4223.5174465975 | rust | 4418 |

- robust changes: [(0.1, 0.13)]
- bracket (first robust change): (0.1, 0.13)
- bracket (0.1, 0.13): run d18_secant.py run on it at tol 5e-5
