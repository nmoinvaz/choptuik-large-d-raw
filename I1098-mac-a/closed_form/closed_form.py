"""#1098: integer-relation searches (PSLQ, H. R. P. Ferguson, D. H. Bailey and S. Arno, Math. Comp. 68 (1999) 351) for
Delta_inf, provisional, against small bases of classical constants and simple transforms of Delta_inf.

    python3 closed_form.py VALUE BAR [--planted] [--random]

VALUE is the decimal string, BAR its error bar. Each search runs PSLQ on [f(x), b_1, ..., b_k] at tol = 10 * BAR relative
and a coefficient bound H chosen so that chance relations are unlikely: with n = k + 1 numbers known to P digits,
random vectors have integer relations of height about 10^(P/n), so a relation is reported as found only when its
height is at most 10^(P/n) / 10 (a tenth of the chance height). Controls: --planted builds x from a known relation
(3 pi^2 - 7 log 2)/11 plus noise of size BAR, which must be recovered; --random uses a random number with BAR's
precision, which must give none.
"""
import random
import sys

import mpmath as mp

mp.mp.dps = 60
args = [a for a in sys.argv[1:] if not a.startswith("--")]
val, bar = mp.mpf(args[0]), mp.mpf(args[1])
if "--planted" in sys.argv:
    val = (3 * mp.pi ** 2 - 7 * mp.log(2)) / 11 + bar * mp.mpf("0.37")
if "--random" in sys.argv:
    rng = random.Random(7)
    val = mp.mpf(1) + mp.mpf(rng.random()) + mp.mpf(rng.random()) * mp.mpf(10) ** -16
P = float(-mp.log10(bar / abs(val)))            # digits known
C = dict(pi=mp.pi, pi2=mp.pi ** 2, ln2=mp.log(2), ln3=mp.log(3), z3=mp.zeta(3), gam=mp.euler, G=mp.catalan, e=mp.e,
         sqrt2=mp.sqrt(2), sqrt3=mp.sqrt(3), lnpi=mp.log(mp.pi))
BASES = {
    "pi, pi2, ln2": ["pi", "pi2", "ln2"],
    "pi, ln2, ln3": ["pi", "ln2", "ln3"],
    "pi2, z3, ln2": ["pi2", "z3", "ln2"],
    "pi, gam, G": ["pi", "gam", "G"],
    "e, pi, ln2": ["e", "pi", "ln2"],
    "sqrt2, sqrt3, pi": ["sqrt2", "sqrt3", "pi"],
    "pi, pi2, ln2, z3, gam": ["pi", "pi2", "ln2", "z3", "gam"],
}
F = {"x": lambda x: x, "x^2": lambda x: x * x, "1/x": lambda x: 1 / x, "exp(x)": mp.exp, "log|x|": lambda x: mp.log(abs(x)),
     "x/pi": lambda x: x / mp.pi, "x*pi": lambda x: x * mp.pi, "exp(x/2)": lambda x: mp.exp(x / 2)}
found = []
print(f"value {mp.nstr(val, 30)}, bar {mp.nstr(bar, 3)}, digits P {P:.1f}")
for fname, f in F.items():
    for bname, keys in BASES.items():
        v = [f(val), mp.mpf(1)] + [C[k] for k in keys]
        n = len(v)
        H = int(10 ** (P / n) / 10)
        if H < 2:
            continue
        rel = mp.pslq(v, tol=mp.mpf(10) * bar / abs(val), maxcoeff=H, maxsteps=10 ** 6)
        if rel and sum(1 for c in rel if c) >= 2:
            resid = mp.fsum(c * t for c, t in zip(rel, v))
            found.append((fname, bname, rel, resid))
            print(f"  RELATION {fname} on 1, {bname}: {rel} (height {max(abs(c) for c in rel)}, bound {H}), residual "
                  f"{mp.nstr(resid, 3)}")
        else:
            print(f"  none: {fname} on 1, {bname} (n {n}, height bound {H})")
ok = True
if "--planted" in sys.argv:
    ok = any(fn == "x" and bn == "pi, pi2, ln2" and max(abs(c) for c in r) <= 11 for fn, bn, r, _ in found)
    print("planted control:", "recovered" if ok else "NOT recovered")
elif "--random" in sys.argv:
    ok = not found
    print("random control:", "no relation" if ok else "FOUND a relation in a random number")
else:
    print(f"{len(found)} relations found")
sys.exit(0 if ok else 1)
