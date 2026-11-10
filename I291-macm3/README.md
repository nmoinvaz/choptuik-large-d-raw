# I291-macm3: lam_phys at D 55.04, M 64 by gamma_dd's root search (--Mhi=64), at kf 23 and then kf 13

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon). Code: the worktree ../choptuik-large-d-i271 at 408b4d6 (the tip main 831d873 merged; nothing under hp/ changed after it).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/291. Beside I273, I285, I286 and I290.

Commands (run.sh, caffeinate -is, nice 10, one thread, kf 23 then kf 13): the issue's as written.

Written before the run. If the series gate refuses the M 64 state, the refusal is reported with its tails and that run stops; no override.
Report: lam(64) at each cut with its floor check and tails, and the misses of #282's two zeros (2.0476801581 +0.0000020922i with the node,
2.0476818248 +0.0000045415i without) from lam(64, kf 23), each against its circle's estimate (5.2e-06, 8.6e-06). The root's resolution is find_lam's,
not a bound.

## Results

