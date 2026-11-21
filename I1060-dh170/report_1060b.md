leg 10 step 17 on dh370 (1aa4a4fb build, --series_split 1): a 0.1777320584971952, D 260.8483415339, 1 attempt, 3 od steps, series (t_coef) 394 s, corrector 1149 s

| run | exit, wall | a | D | attempts, od steps | series s | corrector s | state vs leg 10 (bits) | series file vs leg 10 | prediction vs leg 10 |
|---|---|---|---|---|---|---|---|---|---|
| split 1 --base_polish 0 | exit 0, 3502 s | 0.1777320584971952 | 260.8483415339 | 1, 4 | 571 | 2503 | DIFFERENT: exactly summed parts: Delta difference 1.188e-20, max |dS_i| 1.188e-20: DIFFER; information: parts with differing bytes {'zl': 3938, 'z2': 5803, 'z3': 5762, 'z4': 5869, 'z5': 5773, 'z6': 5875, 'z7': 5836} (8 parts compar | DIFFERENT: files: 0 arrays identical, differing bytes {'z0': 22099, 'z1': 177211, 'z2': 179697, 'z3': 179847, 'z4': 180341, 'z5': 175588, 'z6': 173026, | DIFFERENT: files: 1 arrays identical, differing bytes {'zl': 3050, 'z2': 5763, 'z3': 5741}, arrays in one file only none, meta keys that differ ['sourc |

cmp1060.py bits, leg 10's step 17 state against this run's (verdict: D_str, a, Delta and the exactly summed parts; bytes and M1 are information):
bits: D_str equal True (260.8483415339, 260.8483415339), a equal True (0.1777320584971952, 0.1777320584971952)
  exactly summed parts: Delta difference 1.188e-20, max |dS_i| 1.188e-20: DIFFER
  information: parts with differing bytes {'zl': 3938, 'z2': 5803, 'z3': 5762, 'z4': 5869, 'z5': 5773, 'z6': 5875, 'z7': 5836} (8 parts compared); M1 per part zh 0.0e+00, zl 1.1e-04, z2 2.0e+00, z3 1.7e+00, z4 1.4e+00, z5 1.0e+00, z6 1.4e+00, z7 1.0e+00
DIFFERENT

series and prediction against leg 10's, by order (seriesdiff1060.py, information; its own controls first):
controls: series against itself, row 3: 0 entries differ (must be 0); with one part of one entry moved one ulp: 1 differ (must be 1)
series (8 parts per entry, 769 entries per order row):
  order row  0: 0/769 entries differ, max |dS| 0.000e+00, max |S| 1.683e+00
  order row  1: 769/769 entries differ, max |dS| 1.212e-22, max |S| 3.239e-04
  order row  2: 769/769 entries differ, max |dS| 5.900e-23, max |S| 9.543e-07
  order row  3: 769/769 entries differ, max |dS| 6.868e-23, max |S| 2.096e-07
  order row  4: 769/769 entries differ, max |dS| 7.147e-23, max |S| 1.094e-07
  order row  5: 769/769 entries differ, max |dS| 4.644e-23, max |S| 4.347e-08
  order row  6: 769/769 entries differ, max |dS| 2.048e-23, max |S| 2.556e-09
  order row  7: 769/769 entries differ, max |dS| 3.721e-24, max |S| 1.240e-08
  order row  8: 769/769 entries differ, max |dS| 3.477e-24, max |S| 1.258e-08
  order row  9: 769/769 entries differ, max |dS| 4.601e-24, max |S| 7.958e-09
  order row 10: 769/769 entries differ, max |dS| 3.244e-24, max |S| 3.349e-09
  order row 11: 769/769 entries differ, max |dS| 1.552e-24, max |S| 5.098e-10
  order row 12: 769/769 entries differ, max |dS| 3.872e-25, max |S| 6.479e-10
  order row 13: 769/769 entries differ, max |dS| 1.559e-25, max |S| 7.970e-10
  order row 14: 769/769 entries differ, max |dS| 2.816e-25, max |S| 5.453e-10
  order row 15: 769/769 entries differ, max |dS| 2.176e-25, max |S| 2.528e-10
  order row 16: 769/769 entries differ, max |dS| 1.132e-25, max |S| 5.740e-11
  order row 17: 769/769 entries differ, max |dS| 3.478e-26, max |S| 3.088e-11
  order row 18: 769/769 entries differ, max |dS| 5.120e-27, max |S| 4.921e-11
  order row 19: 769/769 entries differ, max |dS| 1.676e-26, max |S| 3.678e-11
  order row 20: 769/769 entries differ, max |dS| 1.436e-26, max |S| 1.860e-11
  order row 21: 769/769 entries differ, max |dS| 8.095e-27, max |S| 5.359e-12
  order row 22: 769/769 entries differ, max |dS| 2.893e-27, max |S| 1.181e-12
  order row 23: 769/769 entries differ, max |dS| 1.742e-28, max |S| 2.958e-12
  order row 24: 769/769 entries differ, max |dS| 9.609e-28, max |S| 2.441e-12
  order row 25: 769/769 entries differ, max |dS| 9.316e-28, max |S| 1.339e-12
  order row 26: 769/769 entries differ, max |dS| 5.682e-28, max |S| 4.562e-13
  order row 27: 769/769 entries differ, max |dS| 2.289e-28, max |S| 2.868e-14
  order row 28: 769/769 entries differ, max |dS| 2.659e-29, max |S| 1.719e-13
  order row 29: 769/769 entries differ, max |dS| 5.235e-29, max |S| 1.593e-13
  order row 30: 769/769 entries differ, max |dS| 5.935e-29, max |S| 9.459e-14
  order row 31: 769/769 entries differ, max |dS| 3.921e-29, max |S| 3.668e-14
leg 10's series row 0 against its stored base state: 0 entries differ (must be 0 for the comparison to mean anything)
this run's series row 0 against the stored base state: 0 entries differ
prediction (zh+zl+z2+z3): 769/769 entries differ, max |dS| 2.387e-23, last component (Delta) |dS| 2.387e-23

READING (the coordinator's, fixed before the run): unequal bits with the base unmoved (series row 0 equals the stored base): the build (1aa4a4fb python on a 40f4b4a5 kernel against main 8179068d) or the platform.
