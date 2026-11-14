# I749-macm3: #708's box near Re 3 at D 61.0264, M 48, at the cuts kf 39 and kf 41

Machine macm3 (Apple M3, 8 cores, 24 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/749.

Code: the worktree ~/Source/choptuik-large-d-749 at wip/i749 bd7df22f, which is b5d69cc2 (the build of #708's circles,
venv-macm3-314's modecount_cx unchanged) with `modecount_circle.py` and its planted cases from main 672d01b7 (positions
up to winding 6). The planted check `modecount_circle_planted.py --controls` passed on the coordinator's Mac and runs
again here first. The scripts `common.sh`, `job.sh` and `run_749.sh` were written by the coordinator from #708's, with only
the cut, the paths and the commit check changed.

Run: `run_749.sh P`, ten single-thread circles at most P at a time: at each cut the control (R 0.2 at lam_phys) and the
four R 0.36 circles at 2.85 +- 0.25i and 3.35 +- 0.25i. The small circles (the pair near the real axis, and any zero
shared by a left and a right circle) are placed by the coordinator from these circles' positions.

Pass criteria, written before the run (#749): every circle resolved with 0 verification mismatches; the control winds +1;
the count at each cut with its basis; the pair's position from a small circle holding both zeros; a circle that winds +7
or more stops the work until a planted case exists. Prediction from #708's pattern, written before the run: 12 at kf 39.
