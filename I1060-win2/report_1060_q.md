## (1) series_split_check.py at D 260.6706 with --N 31
    newton_o at the state: 49.2 s
    N 31: default 347.4 s, split 213.0 s, ratio 1.63
    PASS: z_1 the same bits, worst d_split / (1e3 d_oa) 6.98e-09; control (l = 1 dropped) 4.34e+90 times the threshold, fired
    d_split per order (k: d_split, d_split/(1e3 d_oa)): 1: 0.00e+00, 0.0e+00, 2: 3.79e-43, 1.9e-17, 3: 2.90e-36, 6.6e-10, 4: 3.60e-36, 4.8e-10, 5: 3.56e-36, 3.0e-10, 6: 1.32e-35, 3.9e-10, 7: 3.68e-36, 1.4e-09, 8: 8.58e-37, 1.2e-10, 9: 2.37e-36, 2.7e-10, 10: 8.59e-36, 8.0e-10, 11: 2.75e-35, 4.0e-09, 12: 6.36e-36, 6.3e-10, 13: 4.53e-37, 4.2e-11, 14: 3.60e-36, 3.5e-10, 15: 5.50e-35, 3.3e-09, 16: 4.49e-36, 2.9e-10, 17: 3.74e-36, 2.6e-10, 18: 2.34e-36, 1.8e-10, 19: 2.90e-35, 7.0e-09, 20: 1.92e-35, 8.7e-10, 21: 9.38e-37, 5.2e-11, 22: 6.03e-36, 3.7e-10, 23: 3.37e-35, 3.8e-09, 24: 5.09e-35, 1.6e-09, 25: 1.52e-35, 6.8e-10, 26: 3.98e-36, 2.0e-10, 27: 1.38e-35, 1.0e-09, 28: 7.71e-35, 1.4e-09, 29: 1.03e-35, 3.8e-10, 30: 1.71e-36, 7.4e-11, 31: 1.84e-35, 1.1e-09
    orders past 24 (k = 25 to 31): d_split from 1.71e-36 to 7.71e-35; above 5.5e-35: 28 (7.71e-35)
    orders 3 to 24: d_split from 4.53e-37 to 5.50e-35; above 5.5e-35: none
    READING (1): d_split above 5.5e-35 at orders past 24: the check missed the gap by its order count

## (2) the step 17 A/B with --keep_plan 1
| run | exit, step s | a | D | accepted, attempts, od steps | series s | corrector s |
|---|---|---|---|---|---|---|
| step17_k1_s1 (--keep_plan 1) | exit 0, 574 s | 0.1777320584971952 | 260.8483415339437912 | True, 1, 3 | 140 | 330 |
| step17_k1_s2 (--keep_plan 1) | exit 0, 547 s | 0.1777320584971952 | 260.8483415339437912 | True, 1, 3 | 114 | 333 |
for comparison (--keep_plan 0, the first A/B): S = 1 622 s, series 139 s, corrector 377 s, 4 od steps; S = 2 703 s, series 112 s, corrector 495 s, 5 od steps
k1: S = 2 vs S = 1, bits: bits: D_str equal True (260.8483415339, 260.8483415339), a equal True (0.1777320584971952, 0.1777320584971952), parts with differing bytes {'z2': 791, 'z3': 5533, 'z4': 5841, 'z5': 5764, 'z6': 5824, 'z7': 5817} (8 parts compared) / DIFFERENT
k1: S = 2 vs S = 1, close (tol 1e-100): close (tol 1e-100): Delta REF 1.683264757534070378561608, relative difference 5.182e-49; M2 (exact sums, vs max |S| 1.68326) 1.648e-48 / M1 per part (max |dpart| / max |part|): zh 0.0e+00, zl 0.0e+00, z2 4.6e-16, z3 1.5e+00, z4 1.7e+00, z5 1.4e+00, z6 1.6e+00, z7 1.3e+00 / DISAGREE
series_agree_k1_s1_s2.txt: series step17_k1_s1/jet_pin3_D260.6706.npz against step17_k1_s2/jet_pin3_D260.6706.npz: 32 orders x 769 components
    per order max |dS| / max |S|: 0:0.0e+00, 1:0.0e+00, 2:3.1e-42, 3:1.8e-33, 4:3.4e-33, 5:3.7e-33, 6:1.5e-31, 7:1.9e-32, 8:8.0e-33, 9:2.7e-33, 10:9.2e-33, 11:6.4e-32, 12:3.6e-32, 13:1.9e-32, 14:1.2e-32, 15:4.6e-33, 16:3.0e-32, 17:6.2e-32, 18:2.9e-32, 19:2.3e-32, 20:1.3e-32, 21:3.3e-33, 22:8.6e-32, 23:3.1e-32, 24:2.1e-32, 25:1.4e-32, 26:2.4e-33, 27:2.8e-31, 28:3.7e-32, 29:2.3e-32, 30:2.2e-32, 31:1.7e-32
    orders above the check's 5.5e-35: 29 of 32; worst 2.809e-31
series_agree_s1_kp0_vs_kp1.txt: series step17_s1/jet_pin3_D260.6706.npz against step17_k1_s1/jet_pin3_D260.6706.npz: 32 orders x 769 components
    per order max |dS| / max |S|: 0:0.0e+00, 1:3.7e-19, 2:6.2e-17, 3:3.3e-16, 4:6.5e-16, 5:1.1e-15, 6:8.0e-15, 7:3.0e-16, 8:2.8e-16, 9:5.8e-16, 10:9.7e-16, 11:3.0e-15, 12:6.0e-16, 13:2.0e-16, 14:5.2e-16, 15:8.6e-16, 16:2.0e-15, 17:1.1e-15, 18:1.0e-16, 19:4.6e-16, 20:7.7e-16, 21:1.5e-15, 22:2.4e-15, 23:5.9e-17, 24:3.9e-16, 25:7.0e-16, 26:1.2e-15, 27:8.0e-15, 28:1.5e-16, 29:3.3e-16, 30:6.3e-16, 31:1.1e-15
    orders above the check's 5.5e-35: 31 of 32; worst 8.012e-15
    READING (2): per-order differences above 5.5e-35: the re-plan at the base is not (the whole) cause

WHICH: (1) the check missed it by its order count
