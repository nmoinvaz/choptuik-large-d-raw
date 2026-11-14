# I783-win2: the order-132 climb between w = 1/4 and 1/2 at D 245.1366

Machine win2 (desktop-pc, 20 threads; 6 used beside #603's chain and #709), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/783.

Scripts (written by the coordinator): `run_783.sh` (rungs of `anm_run.py --ks 132 --ks_w W` with run_744.sh's flags,
6 threads and `--log_proj 1`, in the worktree D:/choptuik-i744 at wip/i744 c6468d2b with venv-i744) and `table_783.py`
(its selftest must pass).

Order and criteria, fixed before the run (#783): w = 3/8 from #744's w25 base; if it converges, 7/16 from its base and
then 1/2 from that; if not, 5/16 from w25's base. Each rung ends converged or not by its own last `octo-double Newton`
line; the table gives steps, final max|F|, Delta against w25's and the failed projections. A stalled rung's projection
lines say whether its failed projections sit at sound points or at blown-up trials, as #743 read them.
