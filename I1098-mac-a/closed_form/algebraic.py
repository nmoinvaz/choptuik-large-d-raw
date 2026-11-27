"""#1098: is Delta_inf (provisional) a root of an integer polynomial of small degree and height? PSLQ (Ferguson, Bailey and
Arno, Math. Comp. 68 (1999) 351) on [1, x, ..., x^d], d = 2..8, at tol 10 x BAR relative, height bound 10^(P/(d+1))/10
(a tenth of the height at which a random number has a relation by chance).

    python3 algebraic.py VALUE BAR [--planted] [--random]

--planted: x is the real root of 2x^3 - 3x^2 - 2x - 1 = 0 plus 0.37 BAR, which must be found at d = 3 (and its multiples
at higher d); --random: a random number with BAR's precision, which must give none.
"""
import random
import sys

import mpmath as mp

mp.mp.dps = 60
args = [a for a in sys.argv[1:] if not a.startswith("--")]
val, bar = mp.mpf(args[0]), mp.mpf(args[1])
if "--planted" in sys.argv:
    val = mp.findroot(lambda t: 2 * t ** 3 - 3 * t ** 2 - 2 * t - 1, 2) + bar * mp.mpf("0.37")
if "--random" in sys.argv:
    rng = random.Random(11)
    val = mp.mpf(1) + mp.mpf(rng.random()) + mp.mpf(rng.random()) * mp.mpf(10) ** -16
P = float(-mp.log10(bar / abs(val)))
print(f"value {mp.nstr(val, 30)}, bar {mp.nstr(bar, 3)}, digits P {P:.1f}")
found = []
for d in range(2, 9):
    H = int(10 ** (P / (d + 1)) / 10)
    if H < 2:
        print(f"  degree {d}: height bound below 2, skipped")
        continue
    rel = mp.pslq([val ** k for k in range(d + 1)], tol=mp.mpf(10) * bar / abs(val), maxcoeff=H, maxsteps=10 ** 6)
    if rel:
        found.append((d, rel))
        print(f"  degree {d}: RELATION {rel} (height {max(abs(c) for c in rel)}, bound {H})")
    else:
        print(f"  degree {d}: none (height bound {H})")
if "--planted" in sys.argv:
    ok = any(d == 3 and [abs(c) for c in r] == [1, 2, 3, 2] for d, r in found)
    print("planted control:", "recovered" if ok else "NOT recovered")
elif "--random" in sys.argv:
    ok = not found
    print("random control:", "none" if ok else "FOUND a relation in a random number")
else:
    ok = True
    print(f"{len(found)} polynomials found")
sys.exit(0 if ok else 1)
