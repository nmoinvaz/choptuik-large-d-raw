leg 10 step 17 on dh370 (1aa4a4fb build, --series_split 1): a 0.1777320584971952, D 260.84834153394379127610669399928156053647398948669, 1 attempt, 3 od steps, series (t_coef) 394 s, corrector 1149 s

| run | exit, wall (step s) | a | D | accepted, attempts, od steps | series s | corrector s | state vs leg 10 stored (bits) | series file vs leg 10 | prediction vs leg 10 |
|---|---|---|---|---|---|---|---|---|---|
| split 1 | exit 0, 622 s | 0.1777320584971952 | 260.84834153394379127610669399928156053647398948669 | True, 1, 4 | 139 | 377 | DIFFERENT: bits: D_str equal True (260.8483415339, 260.8483415339), a equal True (0.1777320584971952, 0.1777320584971952), parts with differing bytes {'zl': 3938 | DIFFERENT: files: 0 arrays identical, differing bytes {'z0': 22099, 'z1': 177199, 'z2': 179733, 'z3': 180035, 'z4': 180901, 'z5': 176012, 'z6': 173505, 'z7': 174 | DIFFERENT: files: 1 arrays identical, differing bytes {'zl': 3053, 'z2': 5791, 'z3': 5742}, arrays in one file only none, meta keys that differ ['source'] |
| split 2 | exit 0, 703 s | 0.1777320584971952 | 260.84834153394379127610669399928156053647398948669 | True, 1, 5 | 112 | 495 | DIFFERENT: bits: D_str equal True (260.8483415339, 260.8483415339), a equal True (0.1777320584971952, 0.1777320584971952), parts with differing bytes {'zl': 3938 | DIFFERENT: files: 0 arrays identical, differing bytes {'z0': 22099, 'z1': 177197, 'z2': 179811, 'z3': 180250, 'z4': 180990, 'z5': 176161, 'z6': 173688, 'z7': 174 | DIFFERENT: files: 1 arrays identical, differing bytes {'zl': 3053, 'z2': 5794, 'z3': 5733}, arrays in one file only none, meta keys that differ ['source'] |

both accept the same a and D: True (split 1: a 0.1777320584971952, D 260.84834153394379127610669399928156053647398948669; split 2: a 0.1777320584971952, D 260.84834153394379127610669399928156053647398948669)
split 2 against split 1: step 703/622 = 1.130, series 112/139 = 0.804, corrector 495/377 = 1.314
split 2 vs split 1, bits: bits: D_str equal True (260.8483415339, 260.8483415339), a equal True (0.1777320584971952, 0.1777320584971952), parts with differing bytes {'z2': 2910, 'z3': 5769, 'z4': 5841, 'z5': 5779, 'z6': 5842, 'z7': 5810} (8 parts compared) / DIFFERENT
split 2 vs split 1, close (tol 1e-100):
    close (tol 1e-100): Delta REF 1.683264757534070378573492, relative difference 2.451e-40; M2 (exact sums, vs max |S| 1.68326) 2.451e-40
      M1 per part (max |dpart| / max |part|): zh 0.0e+00, zl 0.0e+00, z2 6.7e-08, z3 1.9e+00, z4 1.5e+00, z5 1.4e+00, z6 1.5e+00, z7 1.4e+00
    DISAGREE
    the coordinator's reading (every state part within 1e-100 of its max, M1): worst part 1.90e+00: FAIL; parts: zh 0.0e+00, zl 0.0e+00, z2 6.7e-08, z3 1.9e+00, z4 1.5e+00, z5 1.4e+00, z6 1.5e+00, z7 1.4e+00
    cmp1060 close exit 1 (Delta and M2 within 1e-100: DISAGREE)
