leg 10 on dh370 (1aa4a4fb, split 1, 10 threads): step 15 a 0.21931277659360876, D 260.47082389, 4 od steps, series 394 s, corrector 1614 s; step 16 a 0.19978558306115476, D 260.67060947, 3 od steps, series 396 s, corrector 1534 s

| state | run | exit, step s | a | D | accepted, attempts, od steps | series s | corrector s | state vs leg 10 stored next state (bits) |
|---|---|---|---|---|---|---|---|---|
| step 15 | S = 1 | exit 0, 772 s | 0.21931277659360876 | 260.4708238923854413 | True, 1, 6 | 143 | 531 | DIFFERENT: 360876, 0.21931277659360876), parts with differing bytes {'zl': 4037, 'z2': 5813, 'z3': 5750, 'z4': 5838, 'z5': 5766, 'z6': 5861, 'z7': 5839} (8 parts compared) |
| step 15 | S = 2 | exit 0, 758 s | 0.21931277659360876 | 260.4708238923854413 | True, 1, 6 | 109 | 556 | DIFFERENT: 360876, 0.21931277659360876), parts with differing bytes {'zl': 4037, 'z2': 5809, 'z3': 5764, 'z4': 5852, 'z5': 5762, 'z6': 5847, 'z7': 5854} (8 parts compared) |
| step 16 | S = 1 | exit 0, 862 s | 0.1997855830611548 | 260.6706094754465961 | True, 1, 6 | 147 | 616 | DIFFERENT: 6115476, 0.1997855830611548), parts with differing bytes {'zl': 4175, 'z2': 5778, 'z3': 5753, 'z4': 5838, 'z5': 5771, 'z6': 5823, 'z7': 5845} (8 parts compared) |
| step 16 | S = 2 | exit 0, 826 s | 0.1997855830611548 | 260.6706094754465961 | True, 1, 6 | 116 | 612 | DIFFERENT: 6115476, 0.1997855830611548), parts with differing bytes {'zl': 4175, 'z2': 5775, 'z3': 5770, 'z4': 5857, 'z5': 5737, 'z6': 5853, 'z7': 5832} (8 parts compared) |

step 15: same a and D by S = 1 and 2: True; od steps S = 1 6, S = 2 6; series 109/143 = 0.763; corrector 556/531 = 1.048; step 758/772 = 0.982
    S = 2 vs S = 1 close (information): close (tol 1e-100): Delta REF 1.683321184326974665616757, relative difference 3.474e-39; M2 (exact sums, vs max |S| 1.68332) 3.474e-39 / M1 per part (max |dpart| / max |part|): zh 0.0e+00, zl 0.0e+00, z2 9.7e-07, z3 2.0e+00, z4 1.5e+00, z5 1.8e+00, z6 1.5e+00, z7 2.1e+00 / DISAGREE
step 16: same a and D by S = 1 and 2: True; od steps S = 1 6, S = 2 6; series 116/147 = 0.784; corrector 612/616 = 0.994; step 826/862 = 0.958
    S = 2 vs S = 1 close (information): close (tol 1e-100): Delta REF 1.683291309428658675364744, relative difference 1.065e-46; M2 (exact sums, vs max |S| 1.68329) 1.065e-46 / M1 per part (max |dpart| / max |part|): zh 0.0e+00, zl 0.0e+00, z2 2.9e-14, z3 1.0e+00, z4 1.4e+00, z5 2.0e+00, z6 1.6e+00, z7 1.0e+00 / DISAGREE

READING: equal od steps at both states: step 17 was chance (the coordinator's reading)
