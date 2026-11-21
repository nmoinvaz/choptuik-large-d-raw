| run | exit, step s | a | D | accepted, attempts, od steps | series s | corrector s |
|---|---|---|---|---|---|---|
| step17_t0_s1 (--jet_tangent_from 0) | exit 0, 888 s | 0.1777320584971952 | 260.8483415339437912 | True, 1, 5 | 229 | 558 |
| step17_t0_s2 (--jet_tangent_from 0) | exit 0, 713 s | 0.1777320584971952 | 260.8483415339437912 | True, 1, 5 | 170 | 440 |

for comparison (--jet_tangent_from 1, the A/B): S = 1 622 s, series 139 s, corrector 377 s, 4 od steps; S = 2 703 s, series 112 s, corrector 495 s, 5 od steps
t0: S = 2 vs S = 1, bits: bits: D_str equal True (260.8483415339, 260.8483415339), a equal True (0.1777320584971952, 0.1777320584971952), parts with differing bytes {'z2': 1335, 'z3': 5713, 'z4': 5803, 'z5': 5762, 'z6': 5858, 'z7': 5837} (8 parts compared) / DIFFERENT
t0: S = 2 vs S = 1, close (tol 1e-100): close (tol 1e-100): Delta REF 1.683264757534070378573492, relative difference 9.2e-45; M2 (exact sums, vs max |S| 1.68326) 9.2e-45 / M1 per part (max |dpart| / max |part|): zh 0.0e+00, zl 0.0e+00, z2 2.5e-12, z3 1.7e+00, z4 1.8e+00, z5 9.4e-01, z6 1.1e+00, z7 1.2e+00 / DISAGREE
series_agree_t0_s1_s2.txt: series step17_t0_s1/jet_pin3_D260.6706.npz against step17_t0_s2/jet_pin3_D260.6706.npz: 32 orders x 769 components
    per order max |dS| / max |S|: 0:0.0e+00, 1:0.0e+00, 2:4.7e-41, 3:3.0e-32, 4:2.9e-32, 5:7.2e-32, 6:1.2e-30, 7:1.6e-31, 8:7.2e-32, 9:2.1e-32, 10:4.4e-32, 11:3.9e-31, 12:2.2e-31, 13:8.6e-32, 14:3.2e-32, 15:2.6e-32, 16:2.1e-31, 17:3.1e-31, 18:1.0e-31, 19:4.2e-32, 20:1.1e-32, 21:1.4e-31, 22:5.3e-31, 23:1.2e-31, 24:5.3e-32, 25:5.7e-33, 26:9.1e-32, 27:1.4e-30, 28:1.5e-31, 29:6.4e-32, 30:1.3e-32, 31:6.1e-32
    orders above the check's 5.5e-35: 29 of 32; worst 1.419e-30
series_agree_s1_t1_vs_t0.txt: series step17_s1/jet_pin3_D260.6706.npz against step17_t0_s1/jet_pin3_D260.6706.npz: 32 orders x 769 components
    per order max |dS| / max |S|: 0:0.0e+00, 1:0.0e+00, 2:3.7e-42, 3:3.5e-33, 4:9.2e-34, 5:1.0e-32, 6:1.5e-31, 7:1.8e-32, 8:1.4e-33, 9:9.7e-33, 10:3.1e-32, 11:1.3e-31, 12:5.5e-32, 13:1.8e-32, 14:4.7e-33, 15:4.1e-33, 16:2.0e-32, 17:8.0e-33, 18:1.5e-32, 19:2.5e-32, 20:3.8e-32, 21:7.4e-32, 22:1.4e-31, 23:1.4e-32, 24:1.7e-33, 25:9.1e-33, 26:1.9e-32, 27:8.3e-32, 28:1.1e-32, 29:2.3e-32, 30:3.1e-32, 31:4.8e-32
    orders above the check's 5.5e-35: 29 of 32; worst 1.548e-31

READING: per-order differences up to 1.42e-30, above the check's 5.5e-35: series_split_check does not cover part of the pipeline
