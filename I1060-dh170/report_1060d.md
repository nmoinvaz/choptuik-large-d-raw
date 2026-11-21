leg 10 step 17 on dh370 (1aa4a4fb build, --series_split 1): a 0.1777320584971952, D 260.8483415339, 1 attempt, 3 od steps, series (t_coef) 394 s, corrector 1149 s

| run | exit, wall | a | D | attempts, od steps | series s | corrector s | state vs leg 10 (bits) | series file vs leg 10 | prediction vs leg 10 |
|---|---|---|---|---|---|---|---|---|---|
| split 1 --base_polish 0 | exit 0, 3121 s | 0.1777320584971952 | 260.8483415339 | 1, 3 | 556 | 2112 | DIFFERENT: exactly summed parts: Delta difference -1.592e-46, max |dS_i| 2.736e-45: DIFFER; information: parts with differing bytes {'z2': 919, 'z3': 5609, 'z4': 5861, 'z5': 5773, 'z6': 5856, 'z7': 5829} (8 parts compared); M1 per p | DIFFERENT: files: 1 arrays identical, differing bytes {'z1': 24141, 'z2': 170203, 'z3': 178498, 'z4': 180047, 'z5': 175054, 'z6': 172810, 'z7': 173238} | DIFFERENT: files: 2 arrays identical, differing bytes {'z2': 2576, 'z3': 5783}, arrays in one file only none, meta keys that differ ['source'] |

cmp1060.py bits, leg 10's step 17 state against this run's (verdict: D_str, a, Delta and the exactly summed parts; bytes and M1 are information):
bits: D_str equal True (260.8483415339, 260.8483415339), a equal True (0.1777320584971952, 0.1777320584971952)
  exactly summed parts: Delta difference -1.592e-46, max |dS_i| 2.736e-45: DIFFER
  information: parts with differing bytes {'z2': 919, 'z3': 5609, 'z4': 5861, 'z5': 5773, 'z6': 5856, 'z7': 5829} (8 parts compared); M1 per part zh 0.0e+00, zl 0.0e+00, z2 4.6e-13, z3 1.3e+00, z4 1.7e+00, z5 1.5e+00, z6 1.1e+00, z7 1.2e+00
DIFFERENT

series and prediction against leg 10's, by order (seriesdiff1060.py, information; its own controls first):
controls: series against itself, row 3: 0 entries differ (must be 0); with one part of one entry moved one ulp: 1 differ (must be 1)
series (8 parts per entry, 769 entries per order row):
  order row  0: 0/769 entries differ, max |dS| 0.000e+00, max |S| 1.683e+00
  order row  1: 769/769 entries differ, max |dS| 2.112e-54, max |S| 3.239e-04
  order row  2: 769/769 entries differ, max |dS| 4.098e-48, max |S| 9.543e-07
  order row  3: 769/769 entries differ, max |dS| 2.851e-40, max |S| 2.096e-07
  order row  4: 769/769 entries differ, max |dS| 2.564e-40, max |S| 1.094e-07
  order row  5: 769/769 entries differ, max |dS| 1.096e-39, max |S| 4.347e-08
  order row  6: 769/769 entries differ, max |dS| 1.272e-39, max |S| 2.556e-09
  order row  7: 769/769 entries differ, max |dS| 8.262e-40, max |S| 1.240e-08
  order row  8: 769/769 entries differ, max |dS| 3.465e-40, max |S| 1.258e-08
  order row  9: 769/769 entries differ, max |dS| 5.899e-41, max |S| 7.958e-09
  order row 10: 769/769 entries differ, max |dS| 8.656e-41, max |S| 3.349e-09
  order row 11: 769/769 entries differ, max |dS| 9.221e-41, max |S| 5.098e-10
  order row 12: 769/769 entries differ, max |dS| 6.065e-41, max |S| 6.479e-10
  order row 13: 769/769 entries differ, max |dS| 2.714e-41, max |S| 7.970e-10
  order row 14: 769/769 entries differ, max |dS| 6.968e-42, max |S| 5.453e-10
  order row 15: 769/769 entries differ, max |dS| 2.498e-42, max |S| 2.528e-10
  order row 16: 769/769 entries differ, max |dS| 4.613e-42, max |S| 5.740e-11
  order row 17: 769/769 entries differ, max |dS| 3.524e-42, max |S| 3.088e-11
  order row 18: 769/769 entries differ, max |dS| 1.694e-42, max |S| 4.921e-11
  order row 19: 769/769 entries differ, max |dS| 2.685e-43, max |S| 3.678e-11
  order row 20: 769/769 entries differ, max |dS| 1.971e-43, max |S| 1.860e-11
  order row 21: 769/769 entries differ, max |dS| 3.548e-43, max |S| 5.359e-12
  order row 22: 769/769 entries differ, max |dS| 2.787e-43, max |S| 1.181e-12
  order row 23: 769/769 entries differ, max |dS| 1.466e-43, max |S| 2.958e-12
  order row 24: 769/769 entries differ, max |dS| 5.151e-44, max |S| 2.441e-12
  order row 25: 769/769 entries differ, max |dS| 3.104e-45, max |S| 1.339e-12
  order row 26: 769/769 entries differ, max |dS| 1.880e-44, max |S| 4.562e-13
  order row 27: 769/769 entries differ, max |dS| 1.508e-44, max |S| 2.868e-14
  order row 28: 769/769 entries differ, max |dS| 7.807e-45, max |S| 1.719e-13
  order row 29: 769/769 entries differ, max |dS| 1.930e-45, max |S| 1.593e-13
  order row 30: 769/769 entries differ, max |dS| 1.413e-45, max |S| 9.459e-14
  order row 31: 769/769 entries differ, max |dS| 2.130e-45, max |S| 3.668e-14
leg 10's series row 0 against its stored base state: 0 entries differ (must be 0 for the comparison to mean anything)
this run's series row 0 against the stored base state: 0 entries differ
prediction (zh+zl+z2+z3): 769/769 entries differ, max |dS| 1.876e-42, last component (Delta) |dS| 1.574e-42

READING (the coordinator's, fixed before the run): unequal bits with --keep_plan 1 --base_polish 0 (series row 0 differs from the stored base in 0 entries): a remaining cause, reported with the numbers.
