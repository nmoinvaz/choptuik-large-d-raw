| lambda | hybrid sign | noise-robust | robust (dln <= 0.1) | dln | float64 sign | ln\|det\| | b12 | seconds |
|---|---|---|---|---|---|---|---|---|
| 0.040 | +1 | True | True | 3.21e-05 | +1 | -4213.8355983987 | rust | 5354 |
| 0.055 | +1 | True | True | 4.30e-05 | +1 | -4216.2320148322 | rust | 5542 |
| 0.070 | +1 | True | True | 1.43e-04 | +1 | -4219.7620966375 | rust | 5552 |
| 0.085 | -1 | True | True | 1.16e-05 | +1 | -4220.2872608844 | rust | 5369 |
| 0.100 | -1 | True | True | 1.20e-05 | +1 | -4221.2864886242 | rust | 4991 |
| 0.115 | -1 | True | True | 1.94e-05 | +1 | -4222.6749825989 | rust | 5599 |
| 0.130 | -1 | True | True | 2.45e-05 | +1 | -4224.2162780980 | rust | 5226 |
| 0.150 | -1 | True | True | 3.07e-05 | -1 | -4226.4083914770 | rust | 5657 |

- robust changes: [(0.07, 0.085)]
- bracket (first robust change): (0.07, 0.085)
- bracket (0.07, 0.085): run d18_secant.py run on it at tol 5e-5
