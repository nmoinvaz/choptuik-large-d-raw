# I273-macm3: lam(48) at kf 15 against kf 13 at D 40, 50 and 58 (gamma_dd --M48 --kf48, six runs)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon). Code: the worktree ../choptuik-large-d-i271 at 408b4d6 (the tip main 831d873 merged; nothing under hp/ changed after it).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/273. Beside I285, I286, I290 and I291.

Commands (run.sh, caffeinate -is, nice 10, one thread, one run after another): the coordinator's comment, for S in up7_D40.0201 up8_D50.0075
up12_D58.0060 and K in 13 15. The states are double-double with --polish=4; the quad-double polish of the issue's text is not used.

Written before the run. Reading: lam(48, kf 15) - lam(48, kf 13) at each D against the root's resolution (#266: about 1e-14 at D 50, 5e-13 at
D 58), with the verdict below 1e-12 or not, and each run's floor check and tails. A run whose floor check fires is reported and its difference is
not read as a measurement of the cut.

## Results

