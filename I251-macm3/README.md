# I251-macm3: the D 30 circles at M 64 on the fitted layout, without the cut and then with kf 13 (lam_phys control, the place of October's extra pair)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5).
Code: the worktree ../choptuik-large-d-i271 at 408b4d6 (the tip main 831d873 merged). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/251.
Beside I273, I285, I286, I290 and I291.

Commands (run.sh, caffeinate -is, nice 10, one thread, no cut and then kf 13): the coordinator's comment as written. No D 30.0688 M 64 state is in
the worktree's hp/data at the start (hp_data_before_all.txt), so each setup fits its layout and converges, and both caches start empty.

Written before the runs (coordinator's reading). Stop, per cut: setup refuses the layout or misses the 1e-15 gate. The lam_phys circle (R 0.2) is
the control and must wind +1; its miss from 2.079747703853262 is reported with the circle's own estimate, and a miss up to 1e-3 does not stop the
run. The circle at 4.267 +1.324i (R 0.35) winds 0 (no zero there at M 64) or +1 (the pair exists at M 64); anything else is reported as it is.
Estimates are ranges, not bounds.

## Results

First attempt (05:41:19 to 05:41:40 UTC, *_attempt1.log, exits_attempt1.txt): both cuts exit 1 in 10 s with "module 'modecount_cx' has no attribute
'CSolver'". The worktree has no hp/modecount_cx/build (the compiled module is an ignored build product of the main checkout), so no determinant
was evaluated and no state was saved. Second attempt: the same run.sh from the main checkout ~/Source/choptuik-large-d at bfe5fd54, whose
hp/modecount_circle.py, hp/modecount_common.py and hp/modecount_cx are identical to 408b4d6's (git diff bfe5fd54 408b4d6 lists only gamma_dd.py,
gamma_m48_gap.py and series_truncation.py under hp/). hp_data_before_all.txt now lists the main checkout's states.

Second attempt (main checkout, bfe5fd54): both cuts exit 0 (no cut 05:42:10 to 08:34:32 UTC, kf 13 to 10:08:19 UTC; the first hours on battery, throttled). Setups: both added a node at 0.15 (the centre series at x = 0.3 had ratio 1.086 and 1.041),
|F| 1.7e-26 (no cut) and 1.7e-25 (kf 13), series 6.8e-62 and 4.9e-32 (no cut), 1.7e-176 and 3.5e-41 (kf 13); both gates pass. Circles (R 0.2 and R 0.35, n0 20, 0 mismatches, 0 alias bisections, 52 determinants each):
  lam_phys 2.079747703853262: no cut winding +1, zero 2.0797477038502636 -0.0000000000008763i (estimate 1.1e-06), miss 3.0e-12; kf 13 winding +1, zero 2.0797477038492826 -0.0000000000013844i (estimate 1.5e-09), miss 4.0e-12.
  4.267 +1.324i (R 0.35): winding 0 at both cuts (20 points, largest steps 0.047 and 0.044 rad): no zero in that disc at M 64.
The states are in hp_data_after/ ... see the issue for the closing summary.
