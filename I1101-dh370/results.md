| state | lambda | hybrid sign | noise-robust | robust (dln <= 0.1) | dln | float64 sign | ln\|det\| | seconds |
|---|---|---|---|---|---|---|---|---|
| A | 0.045 | +1 | True | True | 1.30e-05 | +1 | -3902.3590984513 | 7186 |
| A | 0.050 | -1 | True | True | 2.52e-06 | -1 | -3901.1429061235 | 6305 |
| B | 0.045 | +1 | True | True | 1.54e-05 | -1 | -3902.5303054577 | 6818 |
| B | 0.050 | -1 | True | True | 2.50e-06 | -1 | -3901.1035170558 | 6678 |

- state A: det-linear root from the two points: 0.046143036
- state B: det-linear root from the two points: 0.045967998
- **root scatter, root_B - root_A = -1.750e-04** (|.| = 1.750e-04)
- against t5's reading: below 1e-4 no; above 1e-3 no; between YES
- Delta_A 1.174322923415951, Delta_B 1.1743225027439044, **|Delta_B - Delta_A| = 4.2067e-07**; |F| A 3.193965e-10, B 3.194927e-10; steps 4179, 4179; psi-constraint 1.463841e-03, 1.463819e-03
- all four points noise-robust and robust: True
