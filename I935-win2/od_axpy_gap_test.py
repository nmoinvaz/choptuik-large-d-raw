"""#935: does the installed multidouble Python package (hp/pyproject.toml's pin, crate 4.6.0) carry the octo-double
renormalization bug of 3.0.0-4.8.0 (multidouble PR #56)? od_axpy(a, x, y) = y + a x for a float a and octo-double x, y,
checked against exact rational arithmetic on inputs with a gap (a part far below the ulp of the one above it, the
class PR #56 names). Prints the worst relative error in bits over the trials. A correct result has the relative error
near 2^-418 or below; the bug gives about 2^-325 (PR #56). Control: gap 0, the same run on gap-free inputs.
Prints one line per gap class."""
import sys
from fractions import Fraction
import numpy as np
import multidouble as md
print("multidouble from", md.__file__, flush=True)

rng = np.random.default_rng(12345)
N = 20000


def octo(gap):
    """a random octo-double input. gap 0: eight parts, each 2^-53 below the one above (a gap-free input). Otherwise
    the PR #56 class: k nonzero parts at random positions (zero parts between nonzero ones), each below the one above by
    53 to `gap` bits."""
    if gap:
        k = int(rng.integers(2, 5))
        pos = [0] + sorted(rng.choice(np.arange(1, 8), size=k - 1, replace=False))   # the leading part is nonzero
        h = rng.uniform(0.5, 2.0) * 2.0 ** int(rng.integers(-20, 20))
        parts, cur = [0.0] * 8, h
        pos = [int(q) for q in pos]
        for n_, q in enumerate(pos):
            parts[q] = cur * rng.uniform(0.5, 1.0) * rng.choice([-1.0, 1.0])
            cur = abs(parts[q]) * 2.0 ** -int(rng.integers(53, gap + 1))
        return parts
    parts, s = [], rng.uniform(0.5, 2.0)
    for q in range(8):
        parts.append(s)
        s = rng.uniform(-1, 1) * np.spacing(abs(parts[-1])) / 2   # normalized by construction
    return parts


def normalized(v):
    nz = [p for p in v if p != 0.0]
    return all(abs(b) <= np.spacing(abs(a_)) / 2 for a_, b in zip(nz, nz[1:]))


def value(parts):
    return sum((Fraction(float(p)) for p in parts), Fraction(0))


def worst(gap):
    w = -1000.0
    for _ in range(N):
        a = float(rng.uniform(-3, 3))
        x, y = octo(gap), octo(gap)
        if not (normalized(x) and normalized(y)):
            continue
        out = md.od_axpy(a, *[np.array([p]) for p in x], *[np.array([p]) for p in y])
        got = value([float(o[0]) for o in out])
        want = value(y) + Fraction(a) * value(x)
        if want == 0:
            continue
        rel = abs(got - want) / abs(want)
        if rel != 0:
            w = max(w, float(np.log2(float(rel))) if rel > Fraction(1, 2 ** 1000) else -1000.0)
        else:
            w = max(w, -1000.0)
    return w


for gap in (0, 60, 150, 250, 400):  # gap 0: gap-free control
    print(f"gap {gap:>3} bits: worst relative error of od_axpy over {N} trials 2^{worst(gap):.1f}", flush=True)
