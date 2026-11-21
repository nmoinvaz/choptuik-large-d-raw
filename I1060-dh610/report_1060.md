leg 10 step 17 on dh370 (1aa4a4fb build, --series_split 1): a 0.1777320584971952, D 260.8483415339, 1 attempt, 3 od steps, series (t_coef) 394 s, corrector 1149 s

| run | exit, wall | a | D | attempts, od steps | series s | corrector s | state vs leg 10 (bits) | series file vs leg 10 | prediction vs leg 10 |
|---|---|---|---|---|---|---|---|---|---|
| split 1 | exit 0, 1275 s | 0.1777320584971952 | 260.8483415339 | 1, 4 | 214 | 865 | DIFFERENT: exactly summed parts: Delta difference 1.188e-20, max |dS_i| 1.188e-20: DIFFER; information: parts with differing bytes {'zl': 3938, 'z2': 5812, 'z3': 5772, 'z4': 5873, 'z5': 5772, 'z6': 5872, 'z7': 5822} (8 parts compar | DIFFERENT: files: 0 arrays identical, differing bytes {'z0': 22099, 'z1': 177199, 'z2': 179733, 'z3': 180035, 'z4': 180901, 'z5': 176012, 'z6': 173505, | DIFFERENT: files: 1 arrays identical, differing bytes {'zl': 3053, 'z2': 5791, 'z3': 5742}, arrays in one file only none, meta keys that differ ['sourc |

cmp1060.py bits, leg 10's step 17 state against this run's (verdict: D_str, a, Delta and the exactly summed parts; bytes and M1 are information):
bits: D_str equal True (260.8483415339, 260.8483415339), a equal True (0.1777320584971952, 0.1777320584971952)
  exactly summed parts: Delta difference 1.188e-20, max |dS_i| 1.188e-20: DIFFER
  information: parts with differing bytes {'zl': 3938, 'z2': 5812, 'z3': 5772, 'z4': 5873, 'z5': 5772, 'z6': 5872, 'z7': 5822} (8 parts compared); M1 per part zh 0.0e+00, zl 1.1e-04, z2 2.0e+00, z3 1.6e+00, z4 1.5e+00, z5 1.0e+00, z6 1.1e+00, z7 1.0e+00
DIFFERENT
