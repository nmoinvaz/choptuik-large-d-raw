# I657-win2: #551's box at kf 27 and kf 33 on the exact determinant (D 61.0264, M 48)

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), 9 threads, beside #603's chain. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/657 (recommended by #551, queued by the coordinator on the agent-msg channel, message 1794561759829-0, 2026-11-13: after #664).
Code and builds as #551 (`../I551-win2/README.md`): worktree `D:\choptuik-i551` at main 98ee71bd, venv-t126's older hpkernel, `modecount_cx` copied from `D:\choptuik-i573\hp\modecount_cx\build` (cp312, sha256 7ab672ea9a17b239eb77897a...; the double-double mode matrix), python-flint 0.9.0, seed `up23_D61.0264.npz` (sha256 c3393ce849de0f11406a02c5...).
Command: `run_657.sh`, for K = 27 and then 33: `modecount_circle.py data/seeds/local/up23_D61.0264.npz 2.043532530673195,0,0.2 2.85,0.25,0.36 3.35,0.25,0.36 2.85,-0.25,0.36 3.35,-0.25,0.36 --M=48 --kf=K --n0=20 --fmax=1e-15 --tag=D61.0264_M48_kfK --ball=320 --threads=9 --data=<raw>/I657-win2/kfK/data`; starts and exits in `exits_657.txt`, stdout in `kfK/run.log`.
Acceptance (#657): every circle resolved within its point cap, the control circle around lambda_phys winding +1, and the box's count at each cut. For comparison #551 found 6 zeros at kf 29 and 8 at kf 31 (control +1 at both).

Results follow when the runs end.
