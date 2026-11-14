# I797-win2: Delta(w) between w = 3/8 and 1/2 in the order-132 climb at D 245.1366

Machine win2 (desktop-pc, 20 threads; 5 used beside #603 and #796), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/797.

Scripts (written by the coordinator): `run_797.sh` (rungs w = 13/32 from #783's 3/8 base and 15/32 from its 7/16 base,
#783's flags at 5 threads; worktree D:/choptuik-i744 at wip/i744 c6468d2b, venv-i744) and `table_797.py` (#783's table
with these rungs between #783's; its selftest must pass).

Criteria, fixed before the run (#797): each rung converges; Delta - Delta(w = 1/4) stays between 8.7e-14 and 9.4e-14, or
the turn is shown with its size against each rung's final step's dDelta.
