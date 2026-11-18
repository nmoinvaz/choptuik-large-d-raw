"""#948: Delta of each ladder rung's base, its difference from the ks 240 rung's, and the control (240 rung against the state).

    python delta948.py RAW [--mutate]        (run with the 935 worktree's .venv; RAW is the raw clone)

Delta is the sum of the eight parts' last entries, exact in mpmath at 200 digits. The ks 240 rung (`up_K240_from240`) starts from
`I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D232.0000.npz` with --keep_plan 0, which makes the plan again, so its Delta differs from
the state's by the plan's floor (2.75e-25 at D 232.0). The coordinator's amendment (#948): report that difference as the floor, and read a
rung's Delta difference below 3e-25 as zero. Control: the floor must be at most 3e-25 (exit 1 if not); --mutate adds 1e-20 to the 240
rung's Delta first, and the control must then fail. Printed for every rung present: K, Delta, Delta(K) - Delta(240 rung), marked
`zero` when below 3e-25."""
import glob
import os
import re
import sys

import mpmath as mp

sys.path.insert(0, "/home/nathan/Source/choptuik-large-d-935/hp")
from octo_corrector import load_o  # noqa: E402

mp.mp.dps = 200
R = sys.argv[1]
mutate = "--mutate" in sys.argv


def delta(path):
    z, m = load_o(path)
    return mp.fsum(mp.mpf(float(p[-1])) for p in z), m


state = os.path.join(R, "I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D232.0000.npz")
d_state, _ = delta(state)
rows = []
for p in glob.glob(os.path.join(R, "I948-dh370", "*_K*_from*", "base_pin3_D232.0000.npz")):
    name = os.path.basename(os.path.dirname(p))
    K = int(re.search(r"_K(\d+)_from", name).group(1))
    d, m = delta(p)
    rows.append((K, name, d, m))
rows.sort()
ctl = [r for r in rows if r[1] == "up_K240_from240"]
if not ctl:
    print("no control rung (up_K240_from240) yet")
    sys.exit(2)
d240 = ctl[0][2] + (mp.mpf("1e-20") if mutate else 0)
diff = abs(d240 - d_state)
FLOOR = mp.mpf("3e-25")
ok = diff <= FLOOR
print(f"state Delta {mp.nstr(d_state, 40)}")
print(f"control up_K240_from240: Delta {mp.nstr(d240, 40)}, |difference from the state| {mp.nstr(diff, 5)} = the plan's floor (at most 3e-25): "
      f"{'pass' if ok else 'FAIL'}{' (--mutate: +1e-20, must FAIL)' if mutate else ''}")
print("K    rung                  Delta                                     Delta(K) - Delta(240 rung)")
for K, name, d, m in rows:
    print(f"{K:<4} {name:<21} {mp.nstr(d, 30)}   {mp.nstr(d - d240, 8)}{'  (zero, below 3e-25)' if abs(d - d240) < FLOOR else ''}")
sys.exit(0 if ok else 1)
