"""#941, the same-branch line: Delta of the order-240 states against the order-160 chain's Delta(D), interpolated.

    python samebranch941.py RAW            (run with the 935 worktree's .venv; RAW is the raw clone)

Delta is the sum of the eight parts' last entries (float64 sums of the eight parts, good to 1e-16). The order-160 Delta(D) at the
order-240 states' D is the cubic through the four nearest of dh610's states at D 229 to 234 (D 232.0000 is one of them, exact), and
the order difference it is compared with is Delta(135) - Delta(160) at D 230.1312 (order 135 against the same cubic).
A state is on the branch when |Delta(240) - Delta(160)| is at most 10 times that difference (one sample, so a factor of 10 for its
scatter; a step to another solution moves Delta by far more, and a shift of D by 2e-7 already does, since dDelta/dD is
-1.9e-4). Exit 1 if a state is off. --mutate adds 1e-9 to every order-240 Delta first, and every state must then be off (exit 1)."""
import os
import sys

import numpy as np

sys.path.insert(0, "/home/nathan/Source/choptuik-large-d-935/hp")
from octo_corrector import load_o  # noqa: E402

R = sys.argv[1]
W = "I903-win2/ks_chain/leg07_D222.0000_ks240"
H = "I903-dh610/chain_k160"
M = "I903-macm3/chain_k135"


def delta(path):
    z, m = load_o(os.path.join(R, path))
    return float(m["D"]), sum(float(p[-1]) for p in z)


h = [delta(f"{H}/anm_pin3_D{d}.0000.npz") for d in range(229, 235)]


def at(D):
    near = sorted(h, key=lambda x: abs(x[0] - D))[:4]
    return float(np.polyval(np.polyfit([x[0] for x in near], [x[1] for x in near], 3), D))


print("order 160 Delta(D):", ", ".join(f"D {D:.0f} {d:.15f}" for D, d in h), "(cubic through the four nearest)")
D135, d135 = delta(f"{M}/anm_pin3_D230.1312.npz")
scale = abs(d135 - at(D135))
print(f"order 135 at D {D135:.4f}: Delta {d135:.15f}, order 160 there {at(D135):.15f}, difference {d135 - at(D135):+.3e} (the order difference scale)")
off = 0
for d in ("229.0509", "229.9822", "230.9281", "231.7466", "232.0000"):
    p = f"{W}/anm_pin3_D{d}.npz"
    if not os.path.exists(os.path.join(R, p)):
        continue
    D, x = delta(p)
    x += 1e-9 if "--mutate" in sys.argv else 0.0
    ex = False
    dd = x - at(D)
    print(f"order 240 D {D:.4f}: Delta {x:.15f}, order 160 there {at(D):.15f}{' (EXTRAPOLATED)' if ex else ''}, difference {dd:+.3e}, "
          f"{abs(dd) / scale:.2f} x the 135-160 difference: {'on the branch' if abs(dd) <= 10 * scale else 'OFF'}")
    off += abs(dd) > 10 * scale
print(f"{'FAIL' if off else 'PASS'}: {off} of the order-240 states off the branch" + (" (--mutate, must FAIL)" if "--mutate" in sys.argv else ""))
sys.exit(1 if off else 0)
