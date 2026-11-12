# I605-macm3: is det M at M 64 smooth in lambda at the f64-ulp scale? Ulp rows of the exact determinant at #584's s3 and at #596's root

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314. Code: the git worktree ~/Source/choptuik-large-d-b596 at main 742bb879 (hp/modecount_qdet.py, hp/gamma_dd.py), the modecount_cx built there on 2026-11-12 12:53 UTC (unchanged source since ecca9c53), the Python hpkernel of 2026-11-09. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/605 (recommended by macm3 in #584's closing summary, with #596's root added; the coordinator's message of 2026-11-12 17:33 UTC).

Method (the coordinator's message of 2026-11-12 17:35 UTC, which replaced the driver I had started to write; that driver ran for about a minute and was stopped, nothing of it is used): hp/modecount_qdet.py --ulps=1,2,4,8 (main 84f99e4f, the tool of the coordinator) takes the exact determinant of the double-double mode matrix (python-flint at 320 bits) at Re lambda moved by each k f64 ulps up and down, against the point's own. Run from the hp/ of the worktree ~/Source/choptuik-large-d-b596 (main 84f99e4f; the modecount_cx built there from 742bb879's source, which the coordinator says still agrees with newer main; the Python hpkernel of 2026-11-09), 4 threads, python3 -u modecount_qdet.py STATE RE,IM --M=64 --kf=K --fmax=1e-15 --threads=4 --ulps=1,2,4,8 --json=...: s3 (D 61.03, #445's state I252-mac/states/modecount_state_D61.0264_M64_kf23.npz, sha256 179d0bd6..., 0.132000,2.912795, kf 23) and #596's root point (the D 55.04 state hp/data/states/up10_D55.0351.npz, 2.0476841270,0, kf 33, Im lambda = 0; the sign is the arg, 0 or pi), each run twice (s3.json and s3_repeat.json, root.json and root_repeat.json) as the bit-equality control. run_605.sh. The self test passes and --selftest --mutate=no_lo fails (exit 1) on this tree.

Written before the run (the issue's). Control: repeats at the identical argument are bit for bit equal. The reading: a derivative if the phase change grows linearly in the number of ulps (within a factor 2 from 1 to 8), noise if it does not. At the real root, whether the sign sequence over +-1 to 8 ulps is monotone.

## Results


(19:40 UTC, macm3) All runs finished (exits.txt): s3 17:59:38 UTC (started 17:38:25; 1272 s), s3_repeat 18:21:01, root 18:41:34, root_repeat 18:53:54, s3_extra (--ulps=3,5,6,7) 19:19:05, root_repeat2 19:39:09 UTC. Self test passes and --mutate=no_lo fails on this tree. Controls: s3_repeat is bit for bit equal to s3 (base and all eight rows). root_repeat is NOT bit for bit equal to root (ln|det| -150.74167495833788 against -150.74167495844003, the double-double LU's -150.79095801356 against -150.79095893224; the rows' d ln|det| differ by up to 2.5e-10; every sign and every d arg is identical); root_repeat2 is bit for bit equal to root_repeat (base and all eight rows). The first run made the D 55 M 64 state (534 s, saved as modecount_state_D55.0351_M64_kf33.npz) and used it in memory, the second and the third loaded the saved one: the likely reason, not tested here, is that the state in memory and the saved one reloaded differ in the last bits; loaded states reproduce exactly (runs 2 and 3).

s3 (D 61.03, M 64, kf 23, lambda = 0.132 + 2.912795i), exact determinant at Re lambda moved by k f64 ulps, change of arg (wrapped) and of ln|det| against the point's own (s3.json for 1, 2, 4, 8; s3_ulps3567.json for 3, 5, 6, 7):
| k (ulps) | Re λ | d arg (rad, wrapped) | d ln\|det\| |
|---|---|---|---|
| +1 | 0.13200000000000003 | +2.774 | +0.061 |
| +2 | 0.13200000000000006 | -2.836 | +0.414 |
| +3 | 0.1320000000000001 | +2.734 | +0.824 |
| +4 | 0.13200000000000012 | +2.164 | +0.103 |
| +5 | 0.13200000000000014 | -2.952 | -0.199 |
| +6 | 0.13200000000000017 | -2.436 | +0.857 |
| +7 | 0.1320000000000002 | +1.523 | -0.376 |
| +8 | 0.13200000000000023 | -2.794 | +0.994 |
| -1 | 0.13199999999999998 | -2.817 | +0.862 |
| -2 | 0.13199999999999995 | +2.024 | +0.329 |
| -3 | 0.13199999999999992 | +2.112 | +0.257 |
| -4 | 0.1319999999999999 | +1.308 | +0.683 |
| -5 | 0.13199999999999987 | +2.661 | +0.512 |
| -6 | 0.13199999999999984 | -2.945 | +0.248 |
| -7 | 0.1319999999999998 | +2.082 | +0.368 |
| -8 | 0.13199999999999978 | -2.831 | +0.372 |

Steps between consecutive ulps (wrapped): upward 1 to 8: +2.774, +0.672, -0.713, -0.570, +1.167, +0.516, -2.324, +1.967; downward: -2.817, -1.443, +0.088, -0.803, +1.353, +0.676, -1.256, +1.371. Unwrapped phase along k (0 to 8 up): 0, 2.77, 3.45, 2.73, 2.16, 3.33, 3.85, 1.52, 3.49; (down): 0, -2.82, -4.26, -4.17, -4.97, -3.62, -2.95, -4.20, -2.83. A jump of about 2.8 rad at the first ulp, then a wander of +-1 rad about the new level; no growth with k.

Root (D 55.04, M 64, kf 33, up10_D55.0351.npz, lambda = 2.0476841270 + 0i; the values of root_repeat, equal to root_repeat2):
| k (ulps) | Re λ | sign vs the point's | d ln\|det\| |
|---|---|---|---|
| -8 | 2.0476841269999966 | **flipped** | +0.155 |
| -4 | 2.0476841269999984 | same | +2.804 |
| -2 | 2.0476841269999992 | same | +1.045 |
| -1 | 2.0476841269999997 | same | -0.126 |
| +1 | 2.0476841270000006 | same | +2.732 |
| +2 | 2.047684127000001 | **flipped** | +2.631 |
| +4 | 2.047684127000002 | same | +0.877 |
| +8 | 2.0476841270000037 | **flipped** | +2.415 |
| 0 | 2.047684127 | negative (arg π), ln\|det\| -150.741674958 | |
