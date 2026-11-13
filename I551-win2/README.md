# I551-win2: #498's stage-1 box at kf 29 and kf 31 on the exact determinant (D 61.0264, M 48)

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), 9 threads, beside #603's chain and #588's cut run. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/551 (moved to win2 by the coordinator at 20:09 UTC, 2026-11-12, commands in its comment of 20:10 UTC).
Code: worktree `D:\choptuik-i551` detached at main 98ee71bd. `hp/modecount_circle.py` and `hp/modecount_common.py` are identical at 98ee71bd and at 4b33cc9 (the #594 code; `git diff` empty). Builds: venv-t126 (Python 3.12.8, python-flint 0.9.0), its `hpkernel` (`_hpkernel` pyd sha256 f3a697a3..., the build all earlier win2 runs of #573 to #594 used, not the multishoot 1.2.1 build of #600) and `modecount_cx` copied from `D:\choptuik-i573\hp\modecount_cx\build` (cp312, sha256 7ab672ea9a17b239eb77897a..., the double-double mode matrix; its source is unchanged between 80b5056 and 98ee71bd except Cargo.lock). Seed `hp/data/seeds/local/up23_D61.0264.npz` (sha256 c3393ce849de0f11406a02c5...).
Command: `run_551.sh`, for K = 29 and then 31: `modecount_circle.py data/seeds/local/up23_D61.0264.npz 2.043532530673195,0,0.2 2.85,0.25,0.36 3.35,0.25,0.36 2.85,-0.25,0.36 3.35,-0.25,0.36 --M=48 --kf=K --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kfK --ball=320 --threads=9 --data=<raw>/I551-win2/kfK/data`; starts and exits in `exits_551.txt`, stdout in `kfK/run.log`.
Acceptance (#551): the box's count at both cuts, with each circle closed within its point cap, and the control circle around lambda_phys winding +1 at both; or the task reports which circles reach the noise floor (a circle that passes its point cap is reported with its largest steps).



## Results (2026-11-12 20:13:07 to 2026-11-13 07:41:21 UTC)

`run_551.sh`, exit 0 for both cuts (`exits_551.txt`): kf 29 6 h 23 min (406 determinants, median 55.5 s), kf 31 5 h 05 min (346 determinants, median 52.5 s), 9 threads, one determinant at a time. Records `kf29/data/modecount_circles.jsonl`, `kf31/data/modecount_circles.jsonl`, caches `kf<K>/data/modecount_D61.0264_M48_kf<K>_ball320_evals.jsonl`, logs `kf<K>/run.log`. Every one of the ten circles is resolved (every step <= pi/4, no verification mismatch, no alias left, none near a point cap); none reached the noise floor.

| circle | kf 29: winding, points, alias bisections | kf 31: winding, points, alias bisections |
|---|---|---|
| control, R 0.2 around lambda_phys 2.043533 | **+1**, 28 + 2, 0 | **+1**, 28 + 2, 0 |
| R 0.36 at 2.85 + 0.25i | +3, 98 + 2, 38 | +3, 80 + 2, 10 |
| R 0.36 at 3.35 + 0.25i | +3, 86 + 2, 28 | **+2**, 74 + 2, 9 |
| R 0.36 at 2.85 - 0.25i | +3, 98 + 2, 38 | +3, 80 + 2, 10 |
| R 0.36 at 3.35 - 0.25i | +3, 86 + 2, 28 | **+2**, 74 + 2, 9 |

The lower circles are the mirrors of the upper ones: the same winding, points and alias bisections, and zeros that are the complex conjugates of the upper circles' to within 1.5e-5 (the zeros come from the circles' power sums, whose own estimates are 1.5e-3 to 7.6e-2 for a W = 2 or 3 circle at R 0.36).

**The box's count** (zeros in the union of the four R 0.36 circles, the control being lambda_phys, which the control circle winds +1 at both cuts):

| cut | zeros (positions from the circles, good to their estimates) | count |
|---|---|---|
| kf 29 | 2.734 +- 0.248i (left circles only); 3.341 +- 0.271i (right circles only); the pair near 3.10 (3.08 to 3.12, +- 0.004 to 0.017i), in all four circles (0.354 from each centre) | **6** |
| kf 31 | 2.648 +- 0.247i (left only); the pair 3.0266 - 0.0117i and 3.0271 + 0.0106i (both left circles, 0.40 from the right centres, outside them); 3.316 +- 0.192i and 3.472 +- 0.482i (right only) | **8** |

Reading: each circle's winding is the sum of its zeros; the pair is counted once because the same two zeros sit in every circle that contains them (kf 29: four circles, 12 = 6 + 6 counted twice over; kf 31: the two left circles, 10 = 8 + 2). The identification of the pair as two zeros common to those circles comes from the overlap of the circles and the conjugate symmetry of the zero set; a smaller circle around the pair would separate it and settle the count, which I did not run. From kf 29 to kf 31 the pair moves from about 3.10 to 3.027, the left outer zero from 2.734 to 2.648, and the right side gains one zero in each half plane (3.341 + 0.271i becomes 3.316 + 0.192i with 3.472 + 0.482i entering).

Builds (as the coordinator ordered at 20:15 UTC, consistent with #498): venv-t126's older hpkernel (the state at each kf solved on the double-double projector) and `modecount_cx` copied from `D:\choptuik-i573` (the double-double mode matrix); code worktree `D:\choptuik-i551` at main 98ee71bd; python-flint 0.9.0.

