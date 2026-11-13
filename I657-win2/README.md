# I657-win2: #551's box at kf 27 on the exact determinant (D 61.0264, M 48; kf 33 is macm3's)

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), 9 threads, beside #603's chain. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/657 (recommended by #551, queued by the coordinator on the agent-msg channel, message 1794561759829-0, 2026-11-13: after #664).
Code and builds as #551 (`../I551-win2/README.md`): worktree `D:\choptuik-i551` at main 98ee71bd, venv-t126's older hpkernel, `modecount_cx` copied from `D:\choptuik-i573\hp\modecount_cx\build` (cp312, sha256 7ab672ea9a17b239eb77897a...; the double-double mode matrix), python-flint 0.9.0, seed `up23_D61.0264.npz` (sha256 c3393ce849de0f11406a02c5...).
Command: `run_657.sh`, for K = 27 only (the coordinator, message 1794577946594-0: kf 33 went to macm3, with the same exact-determinant circles): `modecount_circle.py data/seeds/local/up23_D61.0264.npz 2.043532530673195,0,0.2 2.85,0.25,0.36 3.35,0.25,0.36 2.85,-0.25,0.36 3.35,-0.25,0.36 --M=48 --kf=K --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kfK --ball=320 --threads=9 --data=<raw>/I657-win2/kfK/data`; starts and exits in `exits_657.txt`, stdout in `kfK/run.log`.
Acceptance (#657): every circle resolved within its point cap, the control circle around lambda_phys winding +1, and the box's count at each cut. For comparison #551 found 6 zeros at kf 29 and 8 at kf 31 (control +1 at both).

## Results (ended 2026-11-13 20:24:07 UTC, exit 0, wall 14547 s = 4 h 02 min, 302 determinants, 47.9 s mean)

| circle (kf 27) | winding | points | max step (rad) | alias bisections | verification mismatches | zeros inside (estimates are the script's n0 vs n0/2 range, not bounds) |
|---|---|---|---|---|---|---|
| control R 0.2 at lambda_phys | +1 | 28 + 2 | 0.373 | 0 | 0 | 2.0435325317 + 1.6e-7i (est 1.4e-6) |
| R 0.36 at 2.85 + 0.25i | +1 | 58 + 2 | 0.383 | 17 | 0 | 2.825820 + 0.247709i (3.3e-2) |
| R 0.36 at 3.35 + 0.25i | +3 | 74 + 2 | 0.380 | 15 | 0 | 3.157552 + 0.035371i (5.9e-3), 3.161153 - 0.043073i (2.5e-2), 3.426837 + 0.498401i (1.4e-3) |
| R 0.36 at 2.85 - 0.25i | +1 | 58 + 2 | 0.383 | 17 | 0 | 2.825819 - 0.247710i (3.3e-2) |
| R 0.36 at 3.35 - 0.25i | +3 | 74 + 2 | 0.380 | 15 | 0 | 3.157552 - 0.035371i (5.9e-3), 3.161153 + 0.043074i (2.5e-2), 3.426837 - 0.498401i (1.4e-3) |

The box's count at kf 27, as #551 counted it: **6** (the outer zero 2.8258 +- 0.2477i, 1 + 1; the pair near the real axis at about 3.159, inside both right circles and counted once, 2; the right outer zero 3.4268 +- 0.4984i, 1 + 1; the windings add up, left circles 1 and 1, right circles 3 and 3, each holding the pair and one outer zero). It equals #551's count at kf 29 (6), against 8 at kf 31 and 8 at kf 33 (macm3's half).
Acceptance: every circle resolved with 0 verification mismatches, the control circle +1. The lower circles are the mirrors of the upper ones by the reality of the determinant on the real axis, so they check the numerics, not new zeros: the zeros of circles 4 and 5 are those of 2 and 3 conjugated to 1.2e-6 and 5.9e-7 (their estimates are 3.3e-2 and 1.4e-3 to 2.5e-2).
Raw: `kf27/data/modecount_circles.jsonl` (the five circle records), `..._evals.jsonl` (the 302 determinants, a cache), `kf27/run.log`, `exits_657.txt`.
