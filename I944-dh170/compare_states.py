"""#944: two octo-double chain states compared exactly. Each component's eight parts are summed exactly (fractions), Delta is
the last component, as anm_run.py prints it. Exit 0 only when |Delta_A - Delta_B| <= LIM (1e-40, the corrector's tolerance
the issue names). The state's other components' differences are reported, not judged.

    python compare_states.py HP_DIR A.npz B.npz [--plant_delta X] [--lim 1e-40]

--plant_delta X adds X to part 2 of B's Delta before comparing (a control: 1e-39 must fail, 1e-41 must pass)."""
import sys
from fractions import Fraction

from mpmath import mp, mpf

mp.dps = 80


def exact(z):
    n = len(z[0])
    return [sum(Fraction(float(z[q][i])) for q in range(len(z))) for i in range(n)]


def main(argv):
    hp, pa, pb = argv[0], argv[1], argv[2]
    plant = float(argv[argv.index("--plant_delta") + 1]) if "--plant_delta" in argv else 0.0
    lim = mpf(argv[argv.index("--lim") + 1]) if "--lim" in argv else mpf("1e-40")
    sys.path.insert(0, hp)
    from octo_corrector import load_o
    za, ma = load_o(pa)
    zb, mb = load_o(pb)
    if len(za) != 8 or len(zb) != 8:
        raise SystemExit(f"parts {len(za)} and {len(zb)}, not eight")
    zb = [list(map(float, q)) for q in zb]
    if plant:
        zb[2][-1] += plant
    ea, eb = exact(za), exact(zb)
    to = lambda f: mpf(f.numerator) / mpf(f.denominator)   # noqa: E731
    dD = to(ea[-1] - eb[-1])
    diffs = [abs(to(a - b)) for a, b in zip(ea, eb)]
    imax = max(range(len(diffs)), key=lambda i: diffs[i])
    print(f"A {pa} D {ma.get('D_str', ma.get('D'))}\nB {pb} D {mb.get('D_str', mb.get('D'))}" + (f", Delta planted {plant:g}" if plant else ""))
    print(f"Delta A {mp.nstr(to(ea[-1]), 45)}\nDelta B {mp.nstr(to(eb[-1]), 45)}\n|dDelta| {mp.nstr(abs(dD), 6)} (limit {mp.nstr(lim, 3)})")
    print(f"components: {len(diffs)}, max |diff| {mp.nstr(diffs[imax], 6)} at {imax}, in {sum(1 for d in diffs if d == 0)} of them equal exactly")
    ok = abs(dD) <= lim
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
