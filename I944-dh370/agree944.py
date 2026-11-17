"""#944: the agreement check of --od_weak_first at a base where the default converged.

    python agree944.py NEW.npz STORED.npz [--mutate delta]        (run with the 935 worktree's .venv, from its hp/)

NEW is the state the run with --od_weak_first 1 saved, STORED the chain's own next state (default option). Pass (fixed before the
run, #944): the same D and |Delta(NEW) - Delta(STORED)| <= 1e-40, with Delta the sum of the eight parts' last entries, exact in
mpmath at 200 digits. Also printed, not judged: the largest entry difference over the state, and each state's octo-double max|F|
is not recomputed here. --mutate delta adds 1e-30 to NEW's Delta first, and the check must then fail (exit 1)."""
import os
import sys

import mpmath as mp

sys.path.insert(0, "/home/nathan/Source/choptuik-large-d-935/hp")
from octo_corrector import load_o  # noqa: E402

mp.mp.dps = 200
TOL = mp.mpf("1e-40")
new, old = sys.argv[1], sys.argv[2]
mutate = "--mutate" in sys.argv and sys.argv[sys.argv.index("--mutate") + 1] == "delta"
zn, mn = load_o(new)
zo, mo = load_o(old)
D_n, D_o = mp.mpf(mn["D_str"]), mp.mpf(mo["D_str"])


def delta(z):
    return mp.fsum(mp.mpf(float(p[-1])) for p in z)


dn, do = delta(zn), delta(zo)
if mutate:
    dn += mp.mpf("1e-30")
worst = max(abs(mp.fsum(mp.mpf(float(zn[k][i])) for k in range(8)) - mp.fsum(mp.mpf(float(zo[k][i])) for k in range(8)))
            for i in range(len(zn[0])))
ok_D = D_n == D_o
ok_d = abs(dn - do) <= TOL
print(f"new {new}\nold {old}")
print(f"D: new {mp.nstr(D_n, 30)}, stored {mp.nstr(D_o, 30)}: {'equal' if ok_D else 'DIFFER'}")
print(f"Delta: new {mp.nstr(dn, 40)}, stored {mp.nstr(do, 40)}; |difference| {mp.nstr(abs(dn - do), 5)} (bound 1e-40): "
      f"{'within' if ok_d else 'NOT within'}")
print(f"largest entry difference over the {len(zn[0])} entries: {mp.nstr(worst, 5)}")
print(f"{'PASS' if ok_D and ok_d else 'FAIL'}" + (" (--mutate delta: Delta of NEW moved by 1e-30, must FAIL)" if mutate else ""))
sys.exit(0 if ok_D and ok_d else 1)
