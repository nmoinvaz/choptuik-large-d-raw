# I796-win2: the order-132 climb from w = 1/2 to w = 1 at D 245.1366

Machine win2 (desktop-pc, 20 threads; 6 used beside #603 and #794), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/796.

Scripts (written by the coordinator): `run_796.sh` (#783's rungs continued, w = 5/8, 3/4, 7/8 and 1 from #783's w = 1/2
base, then a cold polish at w = 1 from the w = 1 base; worktree D:/choptuik-i744 at wip/i744 c6468d2b, venv-i744) and
`table_796.py` (#783's table, the rungs changed; its selftest must pass).

Criteria, fixed before the run (#796): each rung converges by its own last `octo-double Newton` line, or the first that
does not is reported with its projection lines; at w = 1, Delta - Delta(w = 0) and its change from w = 1/2; the cold
polish at w = 1 converges in at most 2 steps.
