# I744-win2: the homotopy in the horizon order at D 245.1366, the order-132 term weighted w = 0 to 1

Machine win2 (desktop-pc, 20 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/744.

Code: worktree D:/choptuik-i744 at wip/i744 c6468d2b, whose kernel has `Ctx::ks_w` (`anm_run.py --ks_w`): the order-ks
term of the horizon series weighted w, w = 0 the sum to order ks - 1 bit for bit and w = 1 as before (the unit test
`ksw_homotopy_ends_and_middle` checks both ends and the midpoint, and a weight planted on order ks - 1 fails it). Its own
venv `venv-i744` with this build. Scripts (written by the coordinator): `run_744.sh` and `compare_744.py`.

Runs, from #696's r131k base (ks 131), s132's flags, 10 threads: `c131` (ks 131, plan made again) and `w0` (ks 132,
w = 0), the ladder w = 1/16, 1/8, 1/4, 1/2, 1 (each rung from the last's base), and `jump` (w = 1 from r131k, one step).

Criteria, written before the run (#744):
- control: Delta(w0) - Delta(c131) within 1e-40 (w = 0 is order 131 bit for bit);
- mutation: jump's step-0 lines equal s132's (the 1.18e20 first step reproduced);
- the table: each rung's Newton steps, final max|F|, Delta, and its change from the rung before; w = 1 against s132's
  floor (4.5e-24). A rung that does not converge stops the ladder and is reported.
