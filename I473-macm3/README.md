# I473-macm3: the box count at D 30, M 64 without the cut (#251's no-cut state), with the usual left column

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at bfe5fd54. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/473.
Pushed to the raw repository from a separate worktree after the rewrite; the state is not in this folder, only its sha256.

State: I251-macm3/hp_data_after/modecount_state_D30.0688_M64.npz (no cut; nodes [0.15, 0.3, ...], |F| 1.7e-26; sha256 in state_sha256.txt), copied into hp/data so the setup loads it with no refit. Command (count.cmd, caffeinate -is, nice 10, one thread), #463's with the cut removed:
python3 hp/modecount_wind.py hp/data/states/up6_D30.0688.npz --M=64 --kf=none --h0=0.6 --lam=2.079747703853262 --aLL=-0.096 --aL=0.124 --fmax=1e-15 --resolve=last --tag=D30.0688_M64 --data=<raw>/I473-macm3/data
Written before the run (the issue's). Each box's winding with 0 last-pass mismatches; the three expected zeros (0, lambda_g 0.8265, lambda_phys 2.0797) counted; any extra located by moment and circle. The summary states the number of points on each edge (#463's phase steps were small, 3 to 14 points per edge).

## Results

Count (count.cmd; started 00:25 UTC, exit 0 at 10:38:26 UTC on 2026-11-11, 544 determinants, count.log): not clean. g winds +2 in B0, 0 in U0, B1a and B1b, +6 in B1c, +6 in B1, +4 in U, +14 in the full box (kf 13 state of #463: 0 everywhere). The three expected zeros are counted (0 in B0, lambda_g in B1a, lambda_phys in B1b). B0 and B1c have no candidate pole inside, so their windings are extra zeros of det M: 2 and 6. Points per edge, largest step 0.393 rad, 0 mismatches in the last pass on all 14 edges: aR Im 0-y1 7, a2 7, a1 13, aL 27, aLL 13; y1 edges aR-a2 65, a2-a1 19, a1-aL 15, aL-aLL 7; Re edges y1-y2 aR 26, aL 33, aLL 48; y2 edges aR-aL 256, aL-aLL 9.
Moment (modecount_moment.py on the count's samples, moment.jsonl): upper-half zeros of g, B0 0.0553 +1.4114i; B1c 3.931 +0.180i, 4.296 +0.522i, 4.656 +1.392i (spreads 0.38, 0.27, 0.036); U 0.8470 +4.3336i, 1.0570 +2.9137i, 1.9786 +3.7212i, 4.0710 +2.5320i (spreads 1e-4 to 7e-4). The lower half is the mirror image (det M(conj lambda) = conj det M(lambda)); it was not circled.
Circles (circles_U.cmd and circles_B.cmd, circles_B2.cmd; 16:26 to 22:21 UTC; one cache copy per process, 120 and 212 new determinants; --M=64 --kf=none --n0=20 --fmax=1e-15): every circle winds as counted, 0 mismatches:

| circle | R | winding | points | largest step | alias bisections | zero inside | estimate |
|---|---|---|---|---|---|---|---|
| 2.0797 (lambda_phys, control) | 0.2 | +1 | 28 | 0.327 | 0 | 2.079748 -0.000000i | 1.4e-9 |
| 0.0553 +1.4114i (B0) | 0.06 | +1 | 28 | 0.355 | 0 | 0.055758 +1.411769i | 5.2e-11 |
| 4.656 +1.392i (B1c) | 0.1 | +1 | 28 | 0.355 | 0 | 4.656327 +1.390362i | 2.4e-11 |
| 4.10 +0.35i (B1c, two zeros) | 0.45 | +2 | 60 | 0.381 | 4 | 3.872835 +0.108001i, 4.285880 +0.550645i | 2.4e-2, 7.4e-3 |
| 3.872835 +0.108001i | 0.06 | +1 | 28 | 0.379 | 0 | 3.871717 +0.105316i | 7.3e-8 |
| 4.285880 +0.550645i | 0.06 | +1 | 28 | 0.357 | 0 | 4.285793 +0.551490i | 6.1e-12 |
| 0.84700 +4.33363i (U) | 0.06 | +1 | 28 | 0.354 | 0 | 0.847147 +4.333559i | 2.6e-12 |
| 1.05697 +2.91373i (U) | 0.06 | +1 | 28 | 0.358 | 0 | 1.057045 +2.913917i | 4.4e-10 |
| 1.97857 +3.72116i (U) | 0.06 | +1 | 28 | 0.355 | 0 | 1.978326 +3.721021i | 4.9e-12 |
| 4.07096 +2.53203i (U) | 0.06 | +1 | 28 | 0.353 | 0 | 4.070967 +2.532063i | 2.7e-12 |

The estimate is the script's distance between its n0 and n0/2 point sums, a range, not a bound. The circle positions are within 6e-4 of the moment positions, except 4.656 +1.392i (1.9e-3, spread 0.036) and the two near-axis zeros of B1c (0.03 from the half-contour positions, spreads 0.3 to 0.4). No zero lies at a candidate pole (nearest 0.38 away). #251's disc at 4.267 +1.324i (R 0.35, winding 0) holds none of the eight (4.656 +1.392i is 0.395 away).
