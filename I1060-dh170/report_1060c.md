leg 10 step 17 on dh370 (1aa4a4fb build, --series_split 1): a 0.1777320584971952, D 260.8483415339, 1 attempt, 3 od steps, series (t_coef) 394 s, corrector 1149 s

| run | exit, wall | a | D | attempts, od steps | series s | corrector s | state vs leg 10 (bits) | series file vs leg 10 | prediction vs leg 10 |
|---|---|---|---|---|---|---|---|---|---|
| split 1 --base_polish 0 | exit 0, 2861 s | 0.1777320584971952 | 260.8483415339 | 1, 3 | 413 | 1950 | DIFFERENT: exactly summed parts: Delta difference -2.416e-47, max |dS_i| 2.736e-45: DIFFER; information: parts with differing bytes {'z2': 565, 'z3': 5443, 'z4': 5815, 'z5': 5771, 'z6': 5870, 'z7': 5802} (8 parts compared); M1 per p | DIFFERENT: files: 0 arrays identical, differing bytes {'z0': 3, 'z1': 130586, 'z2': 178859, 'z3': 179568, 'z4': 180542, 'z5': 175810, 'z6': 173211, 'z7 | DIFFERENT: files: 1 arrays identical, differing bytes {'zl': 1237, 'z2': 5744, 'z3': 5760}, arrays in one file only none, meta keys that differ ['sourc |

cmp1060.py bits, leg 10's step 17 state against this run's (verdict: D_str, a, Delta and the exactly summed parts; bytes and M1 are information):
bits: D_str equal True (260.8483415339, 260.8483415339), a equal True (0.1777320584971952, 0.1777320584971952)
  exactly summed parts: Delta difference -2.416e-47, max |dS_i| 2.736e-45: DIFFER
  information: parts with differing bytes {'z2': 565, 'z3': 5443, 'z4': 5815, 'z5': 5771, 'z6': 5870, 'z7': 5802} (8 parts compared); M1 per part zh 0.0e+00, zl 0.0e+00, z2 4.6e-13, z3 1.4e+00, z4 1.6e+00, z5 1.4e+00, z6 1.3e+00, z7 1.1e+00
DIFFERENT

series and prediction against leg 10's, by order (seriesdiff1060.py, information; its own controls first):
controls: series against itself, row 3: 0 entries differ (must be 0); with one part of one entry moved one ulp: 1 differ (must be 1)
series (8 parts per entry, 769 entries per order row):
  order row  0: 64/769 entries differ, max |dS| 5.436e-52, max |S| 1.683e+00
  order row  1: 769/769 entries differ, max |dS| 6.803e-28, max |S| 3.239e-04
  order row  2: 769/769 entries differ, max |dS| 3.347e-28, max |S| 9.543e-07
  order row  3: 769/769 entries differ, max |dS| 3.067e-28, max |S| 2.096e-07
  order row  4: 769/769 entries differ, max |dS| 3.003e-28, max |S| 1.094e-07
  order row  5: 769/769 entries differ, max |dS| 1.943e-28, max |S| 4.347e-08
  order row  6: 769/769 entries differ, max |dS| 8.640e-29, max |S| 2.556e-09
  order row  7: 769/769 entries differ, max |dS| 1.642e-29, max |S| 1.240e-08
  order row  8: 769/769 entries differ, max |dS| 1.396e-29, max |S| 1.258e-08
  order row  9: 769/769 entries differ, max |dS| 1.898e-29, max |S| 7.958e-09
  order row 10: 769/769 entries differ, max |dS| 1.351e-29, max |S| 3.349e-09
  order row 11: 769/769 entries differ, max |dS| 6.525e-30, max |S| 5.098e-10
  order row 12: 769/769 entries differ, max |dS| 1.672e-30, max |S| 6.479e-10
  order row 13: 769/769 entries differ, max |dS| 6.131e-31, max |S| 7.970e-10
  order row 14: 769/769 entries differ, max |dS| 1.158e-30, max |S| 5.453e-10
  order row 15: 769/769 entries differ, max |dS| 9.044e-31, max |S| 2.528e-10
  order row 16: 769/769 entries differ, max |dS| 4.750e-31, max |S| 5.740e-11
  order row 17: 769/769 entries differ, max |dS| 1.486e-31, max |S| 3.088e-11
  order row 18: 769/769 entries differ, max |dS| 1.882e-32, max |S| 4.921e-11
  order row 19: 769/769 entries differ, max |dS| 6.866e-32, max |S| 3.678e-11
  order row 20: 769/769 entries differ, max |dS| 5.958e-32, max |S| 1.860e-11
  order row 21: 769/769 entries differ, max |dS| 3.388e-32, max |S| 5.359e-12
  order row 22: 769/769 entries differ, max |dS| 1.228e-32, max |S| 1.181e-12
  order row 23: 769/769 entries differ, max |dS| 7.304e-34, max |S| 2.958e-12
  order row 24: 769/769 entries differ, max |dS| 3.919e-33, max |S| 2.441e-12
  order row 25: 769/769 entries differ, max |dS| 3.858e-33, max |S| 1.339e-12
  order row 26: 769/769 entries differ, max |dS| 2.373e-33, max |S| 4.562e-13
  order row 27: 769/769 entries differ, max |dS| 9.676e-34, max |S| 2.868e-14
  order row 28: 769/769 entries differ, max |dS| 1.221e-34, max |S| 1.719e-13
  order row 29: 769/769 entries differ, max |dS| 2.120e-34, max |S| 1.593e-13
  order row 30: 769/769 entries differ, max |dS| 2.452e-34, max |S| 9.459e-14
  order row 31: 769/769 entries differ, max |dS| 1.635e-34, max |S| 3.668e-14
leg 10's series row 0 against its stored base state: 0 entries differ (must be 0 for the comparison to mean anything)
this run's series row 0 against the stored base state: 64 entries differ
prediction (zh+zl+z2+z3): 769/769 entries differ, max |dS| 1.335e-28, last component (Delta) |dS| 1.335e-28

READING (the coordinator's, fixed before the run): unequal bits with --keep_plan 1 (series row 0 differs from the stored base in 64 entries): the re-plan at load is not the whole cause; the size of the difference and the base polish's part are reported as they are.
