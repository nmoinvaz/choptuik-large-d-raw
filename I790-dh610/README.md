# I790-dh610: the n3>n4 residual's u_1 share in p + m and p - m at #735's 0.80 and 0.92 starts

Machine dh610 (Fedora 45, i7-12700; 4 threads beside #608's chains), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/790.

Scripts (written by the coordinator): `uf790.py` (#786's uf786.py with `--pm`) and `run790.sh` (at #735's starts from
origin/main, in #772's build, main a879ccc3).

Criteria, fixed before the run (#790): the shares of the r_p + r_m part, the r_p - r_m part and the a and c rows add to 1
to 1e-10; the control (r_p = r_m = 1e-36 at one j alone) puts that row's share wholly in the sum part; #786's own bars
hold; each log ends `check: pass`.
