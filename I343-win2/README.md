# I343-win2: the corrected low-D leg from D 3.04375 in steps of 0.0004

Machine win2 (desktop-pc, 20 threads; 10 beside #603), issue https://github.com/nmoinvaz/choptuik-large-d/issues/343.

Script (written by the coordinator): `run343.sh` (`hp/lowD_highM.py` from T105's converged pair at D 3.04375, M 320
and 384, `--dD 0.0004 --D_end 3.040 --min_step 0.00005 --diff_max 1e-8`, worktree D:/choptuik-i343 at main, venv-i600;
`--resume` continues after a stop).

Procedure and reading, fixed before the run (notes/LOW_D.md 16): the first two points are the pilot, the second
(3.04295) crossing 3.043. If the leg passes 3.043 with Newton converged at both resolutions and their difference within
1e-8, the freeze at 3.043 was the prediction's. If Newton fails at every step between 3.04335 and 3.043 down to the
0.00005 floor, or a plan never returns (no log line for 8 h), the branch meets a singular point near x 0.014, reported
with the last converged D and the frozen x.
